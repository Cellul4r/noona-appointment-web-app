from fastapi.testclient import TestClient

from app.tests.helpers import signup


def test_auth_login(client: TestClient, db):
    # First, create a user to log in with
    signup_response = signup(client, db, password="stringst")
    assert signup_response.status_code == 200, signup_response.text

    # wrong email but right password
    response = client.post(
        "/auth/token", data={"username": "wrong@example.com", "password": "stringst"}
    )
    print(response.json())
    assert response.status_code == 401
    # wrong email and password
    response = client.post(
        "/auth/token",
        data={"username": "wrong@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    # right email but wrong password
    response = client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    # right email and password
    response = client.post(
        "/auth/token", data={"username": "test@example.com", "password": "stringst"}
    )
    assert response.status_code == 200
