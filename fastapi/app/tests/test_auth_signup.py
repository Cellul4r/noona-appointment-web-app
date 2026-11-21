from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models.user import User
from app.tests.helpers import signup, verify_email

url = "/auth/signup"


def test_auth_signup(client: TestClient, db):
    response = signup(client, db, password="testpassword")
    # The route declares 201, but returns its own JSONResponse, which is 200.
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "User created successfully."}

    user = db.execute(
        select(User).where(User.email == "test@example.com")
    ).scalar_one()
    assert user.full_name == "Test User"
    assert user.password_hash and user.password_hash != "testpassword"


def test_auth_signup_without_verified_email(client: TestClient):
    response = client.post(
        url,
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword",
        },
    )
    assert response.status_code == 401


def test_auth_signup_without_csrf_token(client: TestClient, db):
    verify_email(client, db, "test@example.com")
    del client.headers["X-CSRF-Token"]
    response = client.post(
        url,
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword",
        },
    )
    # fastapi-csrf-protect answers a missing header with 422.
    assert response.status_code == 422
    assert "X-CSRF-Token" in response.json()["detail"], response.text


def test_auth_signup_existing_email(client: TestClient, db):
    response = signup(client, db, password="testpassword")
    assert response.status_code == 200, response.text

    response = signup(client, db, password="testpassword")
    assert response.status_code == 400


def test_too_short_password(client: TestClient):
    response = client.post(
        url,
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "test12",
        },
    )
    assert response.status_code == 422


def test_invalid_email(client: TestClient):
    response = client.post(
        url,
        json={
            "email": "test@.com",
            "full_name": "Test User",
            "password": "testpassword",
        },
    )
    assert response.status_code == 422


def test_missing_fields(client: TestClient):
    response = client.post(
        url,
        json={
            "full_name": "Test User",  # missing email
            "password": "testpassword",
        },
    )
    assert response.status_code == 422
    response = client.post(
        url,
        json={
            "email": "test@example.com",  # missing full_name
            "password": "testpassword",
        },
    )
    assert response.status_code == 422
    response = client.post(
        url,
        json={
            "email": "test@example.com",  # missing password
            "full_name": "Test User",
        },
    )
    assert response.status_code == 422


def test_long_full_name(client: TestClient):
    response = client.post(
        url,
        json={
            "email": "test@example.com",
            "full_name": "T" * 256,
            "password": "testpassword",
        },
    )
    assert response.status_code == 422
