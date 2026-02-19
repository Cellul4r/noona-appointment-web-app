#!/usr/bin/env python3
# fastapi/app/routers/user_router.py
import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_sso import GithubSSO, GoogleSSO
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.config import settings
from app.db import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.sso import get_google_sso, get_github_sso
from app.models.user import User
from app.services.user_service import UserService
from app.schemas.user import UserPrivate, UserUpdate
from datetime import timedelta
from app.security import create_access_token


logger = logging.getLogger(__name__)

router = APIRouter()

user_service = UserService()

@router.get("/settings", response_model=UserPrivate)
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
   
    return user_service.get_user_settings(db, current_user.id)


@router.patch("/me", response_model=UserPrivate)
def update_settings(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):


    return user_service.update_user_settings(db, current_user.id, user_update)
    

@router.get("/link-accounts/{provider}")
async def start_link(
    provider: str,
    current_user: User = Depends(get_current_user),
    google_sso: GoogleSSO = Depends(get_google_sso),
    github_sso: GithubSSO = Depends(get_github_sso),
):
    
    """
    Initiate the OAuth linking process for the current user.
    Generates a state token to prevent CSRF and starts the SSO flow for the chosen provider.
    """
    state_token = create_access_token(
        data={"sub": str(current_user.id), "action": "link"},
        expires_delta=timedelta(minutes=10)
    )

    if provider == "google":
        async with google_sso:
            return await google_sso.get_login_redirect(params={"prompt": "consent"})

    if provider == "github":
        async with github_sso:
            return await github_sso.get_login_redirect(params={"prompt": "consent"})
    raise HTTPException(status_code=400, detail="Unsupported provider")


@router.get("/link-accounts/{provider}/callback")
async def link_callback(
    provider: str,
    request: Request,
    db: Session = Depends(get_db),
    google_sso: GoogleSSO = Depends(get_google_sso),
    github_sso: GithubSSO = Depends(get_github_sso),
):
    """
    Callback endpoint for OAuth provider after user authorizes linking.
    Validates the state token and links the OAuth account to the current user.
    """
    # Process the OAuth callback and extract user info
    if provider == "google":
        async with google_sso:
            oauth_user = await google_sso.verify_and_process(request)
    elif provider == "github":
        async with github_sso:
            oauth_user = await github_sso.verify_and_process(request)
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    # State Validation
    state_token = request.query_params.get("state")
    if not state_token:
        raise HTTPException(status_code=400, detail="Missing state")

    try:
        payload = jwt.decode(
            state_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: int = int(payload.get("sub"))
        action: str = payload.get("action")
        if action != "link":
            raise HTTPException(status_code=400, detail="Invalid state action")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired state token")

    user_service.link_oauth_account(
        db=db,
        user_id=user_id,
        provider=provider,
        oauth_user=oauth_user,
    )

    return JSONResponse(
        content={"message": f"{provider} account linked successfully"}
    )



@router.delete("/unlink-accounts/{provider}")
def unlink_account(
    provider: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service.unlink_oauth_account(db, current_user.id, provider)
    return {"success": True, "message": f"{provider} account unlinked successfully"}