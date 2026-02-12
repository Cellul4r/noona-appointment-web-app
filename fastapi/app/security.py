from datetime import UTC, datetime, timedelta
import secrets

from jose import jwt

from app.config import settings

import bcrypt

# JWT Configuration
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def hash_password(password: str) -> str:
    password_byte = password.encode("utf-8")
    hashed_password_byte = bcrypt.hashpw(password_byte, bcrypt.gensalt())

    return hashed_password_byte.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password_byte = plain_password.encode("utf-8")
    hashed_password_byte = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_password_byte, hashed_password_byte)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes,
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def verify_access_token(token: str) -> str | None:
    """Verify a JWT access token and return the subject (user id) if valid."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub"]},
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    csrf_token = secrets.token_hex(16)
    to_encode["csrf_token"] = csrf_token
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
