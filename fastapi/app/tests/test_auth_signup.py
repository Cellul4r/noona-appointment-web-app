from fastapi.testclient import TestClient

url = "/auth/signup"


def test_auth_signup(client: TestClient):
    response = client.post(
        url,
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "password_hash" not in data


def test_auth_signup_existing_email(client: TestClient):
    response = client.post(
        url,
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword",
        },
    )

    response = client.post(
        url,
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword",
        },
    )
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
