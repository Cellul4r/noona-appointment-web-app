import secrets

from fastapi import HTTPException, status
from fastapi_sso import OpenID
from sqlalchemy import func, select, Enum

from sqlalchemy.orm import Session, joinedload
from app.schemas.user import UserCreate, UserPrivate, UserUpdate
from app.models import User
from app.security import hash_password
from app.models.oauth_user import OAuthUser
from app.services.storage_service import upload_user_profile_image
from app.dependencies.supabase import get_supabase
from supabase import Client

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
        default_avatar = self.gen_avatar_url(user.full_name)
        new_user = User(
            email=user.email,
            full_name=user.full_name,
            password_hash=hash_password(user.password),
            profile_image=default_avatar,
            timezone=user.timezone
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    def gen_avatar_url(self, full_name: str) -> str:
      
        bgcolor = secrets.token_hex(3)
        color = hex(int('0xffffff', 0) - int('0x' + bgcolor, 0)).replace('0x', '')
        lname = ""
        temp = full_name.split()
        fname = temp[0][0] if temp else ""
        if len(temp) > 1:
            lname = temp[1][0]

        return (
            "https://ui-avatars.com/api/?name="
            + fname
            + "+"
            + lname
            + "&background="
            + bgcolor
            + "&color="
            + color
        )

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

        # user never linked with this OAuth Account
        if not existing_user:
            avatar = oauth_user.picture or self.gen_avatar_url(oauth_user.email or "", full_name)
            existing_user = User(
                email=oauth_user.email,
                full_name=full_name,
                password_hash=None,  # User can't set password if they signed up with OAuth, even in setting.
                profile_image=avatar,
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

    def update_user_settings(self, db: Session, user_id: int, user_update: UserUpdate) -> UserPrivate:
        user = db.execute(select(User).where(User.id == user_id)).scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        data_updated = user_update.model_dump(exclude_unset=True)
        name_changed = False
        for k, v in data_updated.items():
            if k == "password":
                setattr(user, "password_hash", hash_password(v))
            else:
                if k == "full_name" and v != user.full_name:
                    name_changed = True
                setattr(user, k, v)
        # update avatar to match the name changes
        if name_changed:
            user.profile_image = self.gen_avatar_url(user.full_name)
        db.commit()
        db.refresh(user)
        return user

    def get_user_settings(self, db: Session, user_id: int) -> User:
        user = (
            db.execute(
                select(User)
                .options(joinedload(User.oauth_accounts))
                .where(User.id == user_id)
            )
            .scalars()
            .first()
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


    def unlink_oauth_account(self, db: Session, user_id: int, provider: str) -> None:
        user = db.execute(select(User).where(User.id == int(user_id))).scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        oauth_account = (
            db.execute(
                select(OAuthUser)
                .where(OAuthUser.user_id == int(user_id))
                .where(OAuthUser.provider == provider)
            )
            .scalars()
            .first()
        )
        if not oauth_account:
            raise HTTPException(status_code=404, detail=f"No linked {provider} account found")

        oauth_count = db.execute(
            select(func.count()).select_from(OAuthUser).where(OAuthUser.user_id == int(user_id))
        ).scalar()

        if not user.password_hash and oauth_count <= 1:
            raise HTTPException(status_code=400, detail="You cannot unlink Google because it is your only way to sign in. Please set a password or link another account first.")

        db.delete(oauth_account)
        db.commit()

    def set_verified(self, user: User, db: Session):
        pass

class OAuthProvider(str, Enum):
    google = "google"
    github = "github"