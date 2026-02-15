import secrets
from fastapi_sso import OpenID
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi import HTTPException, Response, status

from app.models.user import User
from app.security import hash_password, verify_password
from app.schemas.user import UserPrivate
from app.config import settings
from app.models.oauth_user import OAuthUser
from app.services.user_service import UserService


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def authenticate_user(self, email: str, password: str, db: Session):

        user = self.user_service.get_user_by_email(email, db)

        if (
            not user
            or user.password_hash is None
            or not verify_password(password, user.password_hash)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    # save cookies on client with jwt token
    def attach_token_cookie(self, response: Response, token: str):
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings.access_token_expire_minutes
            * 60,  # seconds to expire of this cookies
        )
