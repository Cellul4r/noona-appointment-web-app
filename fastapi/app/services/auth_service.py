from datetime import datetime, timedelta
import secrets
from app.models.auth_token import AuthToken, AuthType
from app.services.mail_service import EmailService
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
            )

        return user

    # save cookies on client with jwt token
    def attach_token_cookie(self, response: Response, token: str, key: str = "jwt"):
        response.set_cookie(
            key=key,
            value=token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings.access_token_expire_minutes
            * 60,  # seconds to expire of this cookies
        )

    async def send_registration_confirmation_email(self, email: str, db: Session):
        # Generate a unique token and save it to the database with an expiration time
        token = secrets.token_urlsafe(128)
        expires_at = datetime.utcnow() + timedelta(minutes=30)  # Token valid for 30 minutes

        auth_token = AuthToken(
            email=email,
            type=AuthType.EMAIL_VERIFICATION,
            hashed_token=hash_password(token),
            expires_at=expires_at,
        )

        db.add(auth_token)
        db.commit()

        # Send the email with the confirmation link containing the token
        confirmation_link = f"{settings.frontend_base_url}/confirm-email?token={token}"


        email_service = EmailService()

        await email_service.send_email_confirmation(
            recipient_email=email,
            confirmation_link=confirmation_link
        )

    async def send_password_reset_email(self, email: str, db: Session):
        # Generate a unique token and save it to the database with an expiration time
        token = secrets.token_urlsafe(128)
        expires_at = datetime.utcnow() + timedelta(minutes=30)  # Token valid for 30 minutes

        auth_token = AuthToken(
            email=email,
            type=AuthType.PASSWORD_RESET,
            hashed_token=hash_password(token),
            expires_at=expires_at,
        )

        db.add(auth_token)
        db.commit()

        # Send the email with the password reset link containing the token
        reset_link = f"{settings.frontend_base_url}/reset-password?token={token}"

        email_service = EmailService()

        await email_service.send_password_reset_email(
            recipient_email=email,
            reset_link=reset_link
        )