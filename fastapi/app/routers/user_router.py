#!/usr/bin/env python3
# fastapi/app/routers/user_router.py
import logging
from fastapi import APIRouter, Request, Depends, HTTPException, Body
from fastapi_sso import GithubSSO, GoogleSSO
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.dependencies.auth import csrf_protect, get_current_user
from app.dependencies.sso import get_google_sso, get_github_sso
from app.models.user import User
from app.services.user_service import UserService
from app.schemas.user import UserPrivate, UserUpdate
from datetime import timedelta
from app.security import create_access_token, verify_password


logger = logging.getLogger(__name__)

router = APIRouter()

user_service = UserService()


@router.get("/settings", response_model=UserPrivate)
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return user_service.get_user_settings(db, current_user.id)


@router.patch(
    "/me",
    response_model=UserPrivate,
    dependencies=[Depends(csrf_protect)],
)
def update_settings(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return user_service.update_user_settings(db, current_user.id, user_update)


@router.post(
    "/verify-password",
    dependencies=[Depends(csrf_protect)],
)
def verify_current_password(
    password: str = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
):

    logger.debug("Verifying password for user %s", current_user.email)

    if not current_user.password_hash:
        logger.warning(
            "User %s attempted password verify but has no password set",
            current_user.email,
        )
        raise HTTPException(status_code=400, detail="No password set for this account")

    try:
        valid = verify_password(password, current_user.password_hash)
    except Exception as exc:
        # bcrypt errors or encoding issues
        logger.error("Error checking password for %s: %s", current_user.email, exc)
        raise HTTPException(status_code=400, detail="Incorrect password")

    if not valid:
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"verified": True}


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
        expires_delta=timedelta(minutes=10),
    )

    if provider == "google":
        async with google_sso:
            return await google_sso.get_login_redirect(params={"prompt": "consent"})

    if provider == "github":
        async with github_sso:
            return await github_sso.get_login_redirect(params={"prompt": "consent"})
    raise HTTPException(status_code=400, detail="Unsupported provider")


@router.delete("/unlink-accounts/{provider}", dependencies=[Depends(csrf_protect)])
def unlink_account(
    provider: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service.unlink_oauth_account(db, current_user.id, provider)
    return {"success": True, "message": f"{provider} account unlinked successfully"}
