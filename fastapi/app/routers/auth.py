#!/usr/bin/env python3
# fastapi/app/routers/auth.py
import logging
import secrets
from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, status
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this logger to DEBUG

router = APIRouter()

# Google OAuth Configuration
GOOGLE_CLIENT_ID = settings.google_client_id or "your-google-client-id"
GOOGLE_CLIENT_SECRET = settings.google_client_secret or "your-google-client-secret"
GOOGLE_REDIRECT_URI = "http://localhost:8080/auth/google/auth"  # Adjust as needed
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"


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


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(
        select(User).where(func.lower(User.email) == form_data.username.lower())
    )
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    logger.info(f"User logged in: {user.email}")
    return Token(access_token=access_token, token_type="bearer")


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
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google authentication failed or user has not verified email.",
        )

    result = db.execute(
        select(User).where(func.lower(User.email) == user.email.lower())
    )
    existing_user = result.scalars().first()

    if not existing_user:
        new_user = User(
            email=user.email,
            full_name=user.first_name + " " + user.last_name,
            password_hash=hash_password(secrets.token_urlsafe(16)),
            profile_image=user.picture,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        existing_user = new_user
        logger.info(f"Created new user from Google SSO: {new_user.email}")

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(existing_user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


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
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Github authentication failed or user has not verified email.",
        )

    result = db.execute(
        select(User).where(func.lower(User.email) == user.email.lower())
    )

    existing_user = result.scalars().first()

    if not existing_user:
        new_user = User(
            email=user.email,
            full_name=user.display_name,
            password_hash=hash_password(secrets.token_urlsafe(16)),
            profile_image=user.picture,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        existing_user = new_user
        logger.info(f"Created new user from Github SSO: {new_user.email}")

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(existing_user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/logout", response_model=Message)
async def logout():
    """
    **Logout User**

    Instructs the client to clear the JWT token.
    Note: Real server-side logout would require a token blacklist.
    """
    logger.info("User logged out")
    return JSONResponse(
        content={"message": "Logout successful. Remove JWT token on frontend."}
    )


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: AuthUser = Depends(get_current_user)):
    """
    **Get Current User Profile**

    Returns the profile information of the currently authenticated user.
    Requires a valid JWT token in the `jwt` cookie or Authorization header (logic depends on `get_current_user`).
    """
    logger.info(f"Fetching profile for {current_user.email}")
    return {
        "email": current_user.email,
        "name": current_user.name,
        "avatar_url": current_user.avatar_url,
    }
