"""Fixtures for concurrency tests that need a real PostgreSQL database.

SQLite (used by the other tests) ignores ``SELECT ... FOR UPDATE``, so row
locking can only be tested on Postgres. Set ``TEST_DATABASE_URL`` to a
throwaway database, e.g.::

    docker run --rm -d -p 55432:5432 -e POSTGRES_PASSWORD=test postgres:16-alpine
    TEST_DATABASE_URL=postgresql://postgres:test@localhost:55432/postgres pytest app/tests/concurrency

Without ``TEST_DATABASE_URL`` every test in this folder is skipped.
The schema is created and dropped around each test, so the database must not
hold data you care about.
"""

import os
import threading
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


def pytest_collection_modifyitems(config, items):
    if TEST_DATABASE_URL:
        return
    skip = pytest.mark.skip(reason="TEST_DATABASE_URL is not set (needs PostgreSQL)")
    here = os.path.dirname(__file__)
    for item in items:
        if str(item.fspath).startswith(here):
            item.add_marker(skip)


@pytest.fixture
def pg_engine():
    from app.db import Base
    import app.models  # noqa: F401  (register all tables on Base.metadata)

    engine = create_engine(TEST_DATABASE_URL, pool_size=30, max_overflow=10)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def make_db(pg_engine):
    """Factory: each call returns a new ORM Session on its own pooled connection.

    Give every simulated user their own session, just like separate HTTP
    requests in the app.
    """
    factory = sessionmaker(bind=pg_engine, autocommit=False, autoflush=False)
    opened = []

    def _make():
        s = factory()
        opened.append(s)
        return s

    yield _make
    for s in opened:
        s.close()


class _DummyNotificationService:
    """Replaces NotificationService so tests never touch the app DB or email."""

    calls: list = []
    _lock = threading.Lock()

    def dequeue_waitlist_available_jobs(self, *, user_ids, session_id):
        with self._lock:
            self.calls.append({"user_ids": list(user_ids), "session_id": session_id})


@pytest.fixture(autouse=True)
def stub_notifications(monkeypatch):
    import app.services.notification_service as ns

    _DummyNotificationService.calls = []
    monkeypatch.setattr(ns, "NotificationService", _DummyNotificationService)
    return _DummyNotificationService


@pytest.fixture
def factory(make_db):
    """Helpers to seed users, an event, sessions and registrations."""
    from app.models import Event, Session as SessionModel, SessionRegistration, User

    db = make_db()
    counter = {"n": 0}

    class Factory:
        def user(self, name="user"):
            counter["n"] += 1
            u = User(email=f"{name}{counter['n']}@example.com", full_name=name)
            db.add(u)
            db.commit()
            return u.id

        def users(self, count, name="participant"):
            return [self.user(name) for _ in range(count)]

        def event(self, owner_id, max_sessions_per_user=None):
            e = Event(
                owner_id=owner_id,
                title="Test event",
                is_draft=False,
                max_sessions_per_user=max_sessions_per_user,
            )
            db.add(e)
            db.commit()
            return e.id

        def session(self, event_id, seat_capacity, seat_taken=0):
            start = datetime.now(timezone.utc) + timedelta(days=7)
            s = SessionModel(
                event_id=event_id,
                start_datetime=start,
                end_datetime=start + timedelta(hours=1),
                location="Room 1",
                seat_capacity=seat_capacity,
                seat_taken=seat_taken,
            )
            db.add(s)
            db.commit()
            return s.id

        def registration(self, session_id, user_id, status):
            r = SessionRegistration(session_id=session_id, user_id=user_id, status=status)
            db.add(r)
            db.commit()
            return r.id

    return Factory()
