import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app import fastapi_app as app
from app.db import get_db, Base
from app.config import settings


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # 👈 THIS FIXES IT
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    # The app sets every cookie with Secure, so talk to it over https or the
    # client will never send the cookies back.
    test_client = TestClient(app, base_url="https://testserver")
    # State-changing routes require a CSRF token: the signed cookie from
    # GET /auth/csrf plus the raw token in the X-CSRF-Token header.
    response = test_client.get("/auth/csrf")
    test_client.headers["X-CSRF-Token"] = response.json()["csrf_token"]
    yield test_client
    app.dependency_overrides.clear()
