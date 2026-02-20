from fastapi.testclient import TestClient


def test_auth_login(client: TestClient):
    # First, create a user to log in with
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "stringst",
        },
    )

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
