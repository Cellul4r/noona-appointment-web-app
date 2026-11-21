"""Helpers for the API tests (SQLite)."""

import secrets
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.auth_token import AuthToken, AuthType
from app.security import hash_password


def verify_email(client: TestClient, db: Session, email: str) -> None:
    """Do the email-verification step without sending an email.

    POST /auth/request/sign-up would email a token; instead store one directly
    and call the real POST /auth/verify-email, which sets the
    ``registration_jwt`` cookie that POST /auth/signup requires.
    """
    token = secrets.token_urlsafe(32)
    db.add(
        AuthToken(
            email=email,
            type=AuthType.EMAIL_VERIFICATION,
            hashed_token=hash_password(token),
            expires_at=datetime.utcnow() + timedelta(minutes=30),
        )
    )
    db.commit()
    response = client.post("/auth/verify-email", params={"token": token})
    assert response.status_code == 200, response.text


def signup(
    client: TestClient,
    db: Session,
    email: str = "test@example.com",
    full_name: str = "Test User",
    password: str = "stringst",
):
    verify_email(client, db, email)
    return client.post(
        "/auth/signup",
        json={"email": email, "full_name": full_name, "password": password},
    )


def login(client: TestClient, email: str = "test@example.com", password: str = "stringst"):
    response = client.post("/auth/token", data={"username": email, "password": password})
    if response.status_code == 200:
        # Login issues a fresh CSRF cookie; keep the header in sync with it.
        client.headers["X-CSRF-Token"] = response.json()["csrf_token"]
    return response
