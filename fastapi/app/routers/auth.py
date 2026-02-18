#!/usr/bin/env python3
# fastapi/app/routers/auth.py
import logging
import secrets
from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso import GithubSSO, GoogleSSO
from app.security import (
    create_access_token,
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db

from app.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.dependencies.auth import get_current_user
from app.schemas.user import UserCreate, UserPrivate
from app.models.user import User
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


@router.post(
    "/signup",
    response_model=UserPrivate,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):

    existing_user = user_service.get_user_by_email(user.email, db)

    if existing_user:
        logger.warning(f"Attempt to create user with existing email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = user_service.create_user(user, db)
    logger.info(f"Created new user: {new_user.email}")

    return new_user


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = auth_service.authenticate_user(form_data.username, form_data.password, db)

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    response = JSONResponse(
        content={
            "message": "Login successful",
        }
    )

    auth_service.attach_token_cookie(response, access_token)
    logger.info(f"User logged in: {user.email}")
    return response


@router.get("/google/login", response_description="Redirects to Google Callback")
async def google_login(google_sso: GoogleSSO = Depends(get_google_sso)):
    async with google_sso:
        return await google_sso.get_login_redirect(params={"prompt": "consent"})


@router.get("/google/callback")
async def google_auth(
    request: Request,
    google_sso: GoogleSSO = Depends(get_google_sso),
    db: Session = Depends(get_db),
):
    async with google_sso:
        user = await google_sso.verify_and_process(request)

        user = user_service.create_oauth_user(user, db)

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        response = JSONResponse(
            content={
                "message": "Login successful",
            }
        )

        auth_service.attach_token_cookie(response, access_token)
        return response


@router.get("/github/login", response_description="Redirects to Github Callback")
async def github_login(github_sso: GithubSSO = Depends(get_github_sso)):
    async with github_sso:
        return await github_sso.get_login_redirect(params={"prompt": "consent"})


@router.get("/github/callback")
async def github_auth(
    request: Request,
    github_sso: GithubSSO = Depends(get_github_sso),
    db: Session = Depends(get_db),
):
    async with github_sso:
        user = await github_sso.verify_and_process(request)

        user = user_service.create_oauth_user(user, db)

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        response = JSONResponse(
            content={
                "message": "Login successful",
            }
        )

        auth_service.attach_token_cookie(response, access_token)
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
