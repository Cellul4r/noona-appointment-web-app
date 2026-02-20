import time
from tracemalloc import start
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, date


def login(client: TestClient):
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "stringst",
        },
    )
    login_response = client.post(
        "/auth/token", data={"username": "test@example.com", "password": "stringst"}
    )


def create_events(client: TestClient):
    start_date = date(2024, 1, 1)
    print(start_date)
    end_date = date(2025, 1, 1)
    while start_date <= end_date:
        sessions = []
        for i in range(5):
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = start_datetime + timedelta(hours=1)
            sessions.append(
                {
                    "start_datetime": start_datetime.isoformat(),
                    "end_datetime": end_datetime.isoformat(),
                    "seat_capacity": i * 2 + 10,
                }
            )
        client.post(
            "/events", json={"title": f"Event on {start_date}", "sessions": sessions}
        )
        start_date += timedelta(days=1)


def test_not_logged_in_calendar(client: TestClient):
    response = client.get("/calendar")

    assert response.status_code == 401


def test_logged_in_calendar(client: TestClient):
    login(client)
    response = client.get("/calendar")
    assert response.status_code == 200


def test_daily_calendar_events(client: TestClient):
    login(client)
    create_events(client)
    response = client.get("/calendar")
    print(response.json())
    assert response.status_code == 200, response.text
