from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, status
from app.db import get_db

from app.models.user import User
from app.security import hash_password, verify_password
from app.schemas.user import UserPrivate


# Check user authentication validate with email and password
def authenticate_user(email: str, password: str, db: Session):

    result = db.execute(select(User).where(func.lower(User.email) == email.lower()))
    user = result.scalars().first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_or_create_oauth_user(
    oauth_user,
    provider: str,
    db: Session,
) -> UserPrivate:

    result = db.execute(
        select(User).where(func.lower(User.email) == oauth_user.email.lower())
    )
    user = result.scalars().first()

    if provider == "google":
        full_name = oauth_user.first_name + " " + oauth_user.last_name
    elif provider == "github":
        full_name = oauth_user.display_name
    else:
        full_name = "Annonymous"

    if not user:
        user = User(
            email=oauth_user.email,
            full_name=full_name,
            password_hash=hash_password(oauth_user.password),
            profile_image=oauth_user.picture,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    return user
