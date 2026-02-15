from fastapi import HTTPException, status
from fastapi_sso import OpenID
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserPrivate
from app.models import User
from app.security import hash_password
from app.models.oauth_user import OAuthUser


class UserService:

    def get_user_by_email(self, email: str, db: Session) -> User | None:
        return (
            db.execute(select(User).where(func.lower(User.email) == email.lower()))
            .scalars()
            .first()
        )

    def get_oauth_user(self, oauth_user: OpenID, db: Session) -> OAuthUser | None:
        return (
            db.execute(
                select(OAuthUser)
                .where(OAuthUser.provider == oauth_user.provider)
                .where(OAuthUser.provider_user_id == oauth_user.id)
            )
            .scalars()
            .first()
        )

    def create_user(self, user: UserCreate, db: Session) -> User:
        new_user = User(
            email=user.email,
            full_name=user.full_name,
            password_hash=hash_password(user.password),
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def create_oauth_user(self, oauth_user: OpenID, db: Session) -> User:

        existing_oauth_user = self.get_oauth_user(oauth_user, db)

        # account already exists
        if existing_oauth_user:
            return existing_oauth_user.user

        if oauth_user.provider == "google":
            full_name = oauth_user.first_name + " " + oauth_user.last_name
        elif oauth_user.provider == "github":
            full_name = oauth_user.display_name
        else:
            full_name = "Annonymous"

        existing_user = (
            db.execute(
                select(User).where(func.lower(User.email) == oauth_user.email.lower())
            )
            .scalars()
            .first()
        )

        # user never link with This OAuth Account and No email in user database
        if not existing_user:
            # create new user and link to OAuth Account
            existing_user = User(
                email=oauth_user.email,
                full_name=full_name,
                password_hash=None,  # let the user set the password later on
                profile_image=oauth_user.picture,
            )
            db.add(existing_user)
            db.flush()  # to get existing_user id

        new_oauth_user = OAuthUser(
            provider=oauth_user.provider,
            provider_user_id=oauth_user.id,
            user=existing_user,
        )

        db.add(new_oauth_user)
        db.commit()
        db.refresh(existing_user)
        return existing_user

    def set_verified(self, user: User, db: Session):
        pass
