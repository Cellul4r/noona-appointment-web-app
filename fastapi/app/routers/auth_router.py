#!/usr/bin/env python3
# fastapi/app/routers/auth.py
import json
import logging
import secrets
from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_csrf_protect import CsrfProtect
from fastapi_sso import GithubSSO, GoogleSSO
from app.security import (
    create_access_token,
    verify_password,
    verify_access_token,
)
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.db import get_db

from app.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.dependencies.auth import csrf_protect, get_current_user, get_optional_user
from app.schemas.user import UserCreate, UserPrivate
from app.models.user import User
from app.models.auth_token import AuthToken, AuthType
from app.dependencies.sso import get_github_sso, get_google_sso
from app.services.auth_service import (
    AuthService,
)

from app.services.user_service import UserService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this logger to DEBUG

router = APIRouter()

user_service = UserService()
auth_service = AuthService(user_service)

FRONTEND_LOGIN_SUCCESS_URI = settings.frontend_login_success_uri


@router.post("/request/sign-up", status_code=status.HTTP_200_OK)
async def request_sign_up(
    email: str,
    db: Annotated[Session, Depends(get_db)],
):
    existing_user = user_service.get_user_by_email(email, db)

    if existing_user:
        logger.warning(f"Sign-up requested for already registered email: {email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    await auth_service.send_registration_confirmation_email(email, db)
    logger.info(f"Sent registration confirmation email to: {email}")
    return {"message": "Registration confirmation email sent."}

@router.post("/verify-email")
def verify_email(
    token: str,
    db: Annotated[Session, Depends(get_db)],
):
    logger.debug("Verifying email token")
    candidate_tokens = db.query(AuthToken).filter(
        AuthToken.type == AuthType.EMAIL_VERIFICATION,
        AuthToken.used_at.is_(None),
        AuthToken.expires_at > datetime.utcnow(),
    ).all()

    auth_token = next(
        (
            row
            for row in candidate_tokens
            if verify_password(token, row.hashed_token)
        ),
        None,
    )

    if not auth_token:
        logger.warning("Invalid or expired email verification token used")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    auth_token.used_at = datetime.utcnow()
    db.commit()

    logger.info(f"Email verified for: {auth_token.email}")

    registration_jwt = create_access_token(data={"sub": auth_token.email}, expires_delta=timedelta(minutes=30))
    response = JSONResponse(content={"message": "Email verified successfully. You can now complete your registration."})
    auth_service.attach_token_cookie(response, registration_jwt, "registration_jwt")
    return response

@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: Request,
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    registration_token = request.cookies.get("registration_jwt")
    if not registration_token:
        logger.error("Missing registration JWT cookie in create_user")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing registration token. Please verify your email first.",
        )
    
    existing_user = user_service.get_user_by_email(user.email, db)

    if existing_user:
        logger.warning(f"Attempt to create user with existing email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    email_in_token = verify_access_token(registration_token)
    if email_in_token != user.email:
        logger.error(f"Email in registration token does not match provided email. Token email: {email_in_token}, Provided email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid registration token for the provided email.",
        )
    
    new_user = user_service.create_user(user, db)
    logger.info(f"Created new user: {new_user.email}")
    response = JSONResponse(content={"message": "User created successfully."})
    response.delete_cookie("registration_jwt")
    return response


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
):
    user = auth_service.authenticate_user(form_data.username, form_data.password, db)

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

    response = JSONResponse(
        content={
            "message": "Login successful",
        }
    )

    auth_service.attach_token_cookie(response, access_token)
    csrf_protect.set_csrf_cookie(signed_token, response)
    logger.info(f"User logged in: {user.email}")
    return response


@router.get("/google/login", response_description="Redirects to Google Callback")
async def google_login(
    google_sso: GoogleSSO = Depends(get_google_sso),
    current_user: User | None = Depends(get_optional_user),
    link: bool = False,
):
    if link:
        if not current_user:
            raise HTTPException(
                status_code=401, detail="Authentication required to link accounts"
            )
        data = {"link": True, "user_id": str(current_user.id)}
    else:
        data = {}

    async with google_sso:
        return await google_sso.get_login_redirect(
            params={"prompt": "consent"}, state=json.dumps(data)
        )


@router.get("/google/callback")
async def google_auth(
    request: Request,
    google_sso: GoogleSSO = Depends(get_google_sso),
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
):
    state = request.query_params.get("state")
    data = json.loads(state) if state else {}
    link = data.get("link", False)
    user_id = data.get("user_id")

    if link:
        if not user_id:
            raise HTTPException(
                status_code=400, detail="Invalid state data for linking"
            )
        async with google_sso:
            user_info = await google_sso.verify_and_process(request)
            user_service.link_oauth_account(db, int(user_id), "google", user_info)
            return {"message": "Google account linked successfully"}
    else:
        async with google_sso:
            user = await google_sso.verify_and_process(request)

            user = user_service.create_oauth_user(user, db)

            access_token_expires = timedelta(
                minutes=settings.access_token_expire_minutes
            )
            access_token = create_access_token(
                data={"sub": str(user.id)}, expires_delta=access_token_expires
            )

            csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

            response = RedirectResponse(FRONTEND_LOGIN_SUCCESS_URI)

            auth_service.attach_token_cookie(response, access_token)
            csrf_protect.set_csrf_cookie(signed_token, response)
            return response


@router.get("/github/login", response_description="Redirects to Github Callback")
async def github_login(
    github_sso: GithubSSO = Depends(get_github_sso),
    current_user: User | None = Depends(get_optional_user),
    link: bool = False,
):
    if link:
        if not current_user:
            raise HTTPException(
                status_code=401, detail="Authentication required to link accounts"
            )
        data = {"link": True, "user_id": str(current_user.id)}
    else:
        data = {}

    async with github_sso:
        return await github_sso.get_login_redirect(
            params={"prompt": "consent"}, state=json.dumps(data)
        )


@router.get("/github/callback")
async def github_auth(
    request: Request,
    github_sso: GithubSSO = Depends(get_github_sso),
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
):
    state = request.query_params.get("state")
    data = json.loads(state) if state else {}
    link = data.get("link", False)
    user_id = data.get("user_id")

    if link:
        if not user_id:
            raise HTTPException(
                status_code=400, detail="Invalid state data for linking"
            )
        async with github_sso:
            user_info = await github_sso.verify_and_process(request)
            user_service.link_oauth_account(db, int(user_id), "github", user_info)
            return {"message": "Github account linked successfully"}
    else:
        async with github_sso:
            user = await github_sso.verify_and_process(request)

            user = user_service.create_oauth_user(user, db)

            access_token_expires = timedelta(
                minutes=settings.access_token_expire_minutes
            )
            access_token = create_access_token(
                data={"sub": str(user.id)}, expires_delta=access_token_expires
            )
            csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

            response = RedirectResponse(FRONTEND_LOGIN_SUCCESS_URI)

            auth_service.attach_token_cookie(response, access_token)
            csrf_protect.set_csrf_cookie(signed_token, response)
            return response


@router.get("/logout")
async def logout(response: Response):
    # To logout remove jwt token from cookies

    response.delete_cookie(key="jwt")
    response.delete_cookie(key="fastapi-csrf-token")
    logger.info("User logged out")
    return {"message": "Logout successful. JWT cookies removed."}


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    **Get Current User Profile**

    Returns the profile information of the currently authenticated user.
    Requires a valid JWT token in the `jwt` cookie or Authorization header (logic depends on `get_current_user`).
    """
    logger.info(f"Fetching profile for {current_user.email}")
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "profile_image": current_user.profile_image,
        "timezone": current_user.timezone,
    }
