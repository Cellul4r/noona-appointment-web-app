import logging

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.config import settings

from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.security import verify_access_token

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this logger to DEBUG

# JWT Configuration
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


async def get_current_user(request: Request, db: Session = Depends(get_db)):
    logger.debug(f"Checking JWT cookie in get_current_user")
    token = request.cookies.get("jwt")
    logger.debug(f"JWT cookie: {token}")
    if not token:
        logger.error("Missing JWT cookie in get_current_user")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing JWT cookie"
        )
    try:
        user_id: str | None = verify_access_token(token)
        logger.debug(f"Extracted user_id from sub: {user_id}")
        if user_id is None:
            logger.error("Invalid token: subject missing")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: subject missing",
            )
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            logger.error(f"User not found for id: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        logger.debug(f"User found: {user.email}")
        return user
    except JWTError as e:
        logger.error(f"JWT decoding failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def get_optional_user(request: Request, db: Session = Depends(get_db)):
    logger.debug(f"Checking JWT cookie in get_optional_user")
    token = request.cookies.get("jwt")
    logger.debug(f"JWT cookie: {token}")
    if not token:
        logger.error("Missing JWT cookie in get_optional_user")
        return None
    try:
        user_id: str | None = verify_access_token(token)
        logger.debug(f"Extracted user_id from sub: {user_id}")
        if user_id is None:
            logger.error("Invalid token: subject missing")
            return None
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            logger.error(f"User not found for id: {user_id}")
            return None
        logger.debug(f"User found: {user.email}")
        return user
    except JWTError as e:
        logger.error(f"JWT decoding failed: {e}")
        return None
