#!/usr/bin/env python3
# fastapi/app/routers/auth.py
import logging
import secrets
from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso import GithubSSO, GoogleSSO
from sqlalchemy import func, select
from app.security import (
    create_access_token,
    hash_password,
    oauth2_scheme,
    verify_password,
)
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.auth import UserResponse, Message

from app.models.authuser import AuthUser
from app.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta
from httpx import AsyncClient

from app.dependencies.auth import get_current_user
from app.schemas.user import UserCreate, UserPrivate
from app.models.user import User
from app.schemas.auth import Token
from app.dependencies.sso import get_github_sso, get_google_sso
from app.services.auth import (
    attach_token_cookie,
    authenticate_user,
    get_or_create_oauth_user,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this logger to DEBUG

router = APIRouter()


@router.get("/", response_model=Message)
async def hello():
    """
    **Root Auth Endpoint**

    Returns a simple greeting message to verify the auth router is active.
    """
    logger.info("Auth hello endpoint accessed")
    return {"message": "From auth.py: Hello World!"}


@router.post(
    "/signup",
    response_model=UserPrivate,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(
        select(User).filter(func.lower(User.email) == user.email.lower())
    )
    existing_user = result.scalars().first()

    if existing_user:
        logger.warning(f"Attempt to create user with existing email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        email=user.email,
        full_name=user.full_name,
        password_hash=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"Created new user: {new_user.email}")

    return new_user


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    response = RedirectResponse(settings.frontend_login_success_uri)

    attach_token_cookie(response, access_token)
    logger.info(f"User logged in: {user.email}")
    return response


@router.get("/google/login", response_description="Redirects to Google Callback")
async def google_login(google_sso: GoogleSSO = Depends(get_google_sso)):
    return await google_sso.get_login_redirect()


@router.get("/google/callback", response_model=Token)
async def google_auth(
    request: Request,
    google_sso: GoogleSSO = Depends(get_google_sso),
    db: Session = Depends(get_db),
):
    user = await google_sso.verify_and_process(request)

    user = get_or_create_oauth_user(user, "google", db)

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    response = RedirectResponse(settings.frontend_login_success_uri)

    attach_token_cookie(response, access_token)
    return response


@router.get("/github/login", response_description="Redirects to Github Callback")
async def github_login(github_sso: GithubSSO = Depends(get_github_sso)):
    return await github_sso.get_login_redirect()


@router.get("/github/callback", response_model=Token)
async def github_auth(
    request: Request,
    github_sso: GithubSSO = Depends(get_github_sso),
    db: Session = Depends(get_db),
):
    user = await github_sso.verify_and_process(request)

    user = get_or_create_oauth_user(user, "github", db)

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    response = RedirectResponse(settings.frontend_login_success_uri)

    attach_token_cookie(response, access_token)
    return response


@router.get("/logout")
async def logout(response: Response):
    # To logout remove jwt token from cookies

    response.delete_cookie(key="jwt")
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
        "email": current_user.email,
        "full_name": current_user.full_name,
        "profile_image": current_user.profile_image,
    }
