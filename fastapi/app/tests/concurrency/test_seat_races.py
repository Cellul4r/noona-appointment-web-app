"""Data-race tests for seat booking, run on real PostgreSQL.

Each simulated user gets their own ORM Session (own DB connection), and the
threads are released together by a Barrier so the requests really overlap.
"""

import threading
import time

import pytest
from fastapi import HTTPException
from sqlalchemy import event, func, select, text

from app.models import Session as SessionModel, SessionRegistration
from app.models.session_registration import RegistrationStatus
from app.services.session_service import SessionService
from app.tests.concurrency.helpers import run_concurrently

service = SessionService()


def _statuses(db, session_id):
    rows = db.execute(
        select(SessionRegistration.user_id, SessionRegistration.status).where(
            SessionRegistration.session_id == session_id
        )
    ).all()
    return {user_id: st for user_id, st in rows}


def _seat_taken(db, session_id):
    return db.execute(
        select(SessionModel.seat_taken).where(SessionModel.id == session_id)
    ).scalar_one()


# 1. Last seat, two accepts -------------------------------------------------


@pytest.mark.parametrize("attempt", range(20))
def test_last_seat_two_accepts_only_one_wins(attempt, factory, make_db):
    host = factory.user("host")
    a, b = factory.users(2)
    event_id = factory.event(host)
    sid = factory.session(event_id, seat_capacity=10, seat_taken=9)
    factory.registration(sid, a, RegistrationStatus.AVAILABLE)
    factory.registration(sid, b, RegistrationStatus.AVAILABLE)

    db_a, db_b = make_db(), make_db()
    results = run_concurrently(
        [
            lambda: service.confirm_session(sid, a, db_a),
            lambda: service.confirm_session(sid, b, db_b),
        ]
    )

    oks = [r for r in results if r[0] == "ok"]
    errs = [r[1] for r in results if r[0] == "err"]
    assert len(oks) == 1, results
    assert len(errs) == 1, results
    assert isinstance(errs[0], HTTPException)
    assert errs[0].status_code == 400  # loser was moved to WAITLIST by the winner

    check = make_db()
    statuses = _statuses(check, sid)
    assert sorted(statuses.values(), key=lambda s: s.name) == [
        RegistrationStatus.CONFIRMED,
        RegistrationStatus.WAITLIST,
    ]
    assert _seat_taken(check, sid) == 10


# 2. The lock really waits (deterministic) ---------------------------------


def test_confirm_waits_for_row_lock(factory, make_db, pg_engine):
    host = factory.user("host")
    a = factory.user()
    event_id = factory.event(host)
    sid = factory.session(event_id, seat_capacity=10, seat_taken=9)
    factory.registration(sid, a, RegistrationStatus.AVAILABLE)

    blocker = pg_engine.connect()
    tx = blocker.begin()
    blocker.execute(
        text("SELECT id FROM sessions WHERE id = :id FOR UPDATE"), {"id": sid}
    )

    db = make_db()
    done = threading.Event()
    outcome = {}

    def worker():
        try:
            outcome["result"] = service.confirm_session(sid, a, db).status
        except Exception as exc:  # noqa: BLE001
            outcome["error"] = exc
        finally:
            done.set()

    t = threading.Thread(target=worker)
    t.start()
    try:
        assert not done.wait(0.3), "confirm_session did not wait for the row lock"
    finally:
        tx.commit()
        blocker.close()

    assert done.wait(10), "confirm_session never finished after the lock was released"
    t.join()
    assert "error" not in outcome, outcome
    assert outcome["result"] == RegistrationStatus.CONFIRMED
    assert _seat_taken(make_db(), sid) == 10


# 3. Crowd registers --------------------------------------------------------


def test_crowd_registers_for_five_seats(factory, make_db):
    host = factory.user("host")
    users = factory.users(20)
    event_id = factory.event(host)
    sid = factory.session(event_id, seat_capacity=5)

    sessions = [make_db() for _ in users]
    results = run_concurrently(
        [
            (lambda u=u, db=db: service.register_session(sid, u, db).status)
            for u, db in zip(users, sessions)
        ]
    )

    assert all(r[0] == "ok" for r in results), results
    check = make_db()
    statuses = list(_statuses(check, sid).values())
    assert len(statuses) == 20
    assert statuses.count(RegistrationStatus.CONFIRMED) == 5
    assert statuses.count(RegistrationStatus.WAITLIST) == 15
    assert _seat_taken(check, sid) == 5


# 4. Double-click -----------------------------------------------------------


def test_double_click_creates_one_registration(factory, make_db):
    host = factory.user("host")
    a = factory.user()
    event_id = factory.event(host)
    sid = factory.session(event_id, seat_capacity=5)

    db1, db2 = make_db(), make_db()
    results = run_concurrently(
        [
            lambda: service.register_session(sid, a, db1).status,
            lambda: service.register_session(sid, a, db2).status,
        ]
    )

    assert results == [
        ("ok", RegistrationStatus.CONFIRMED),
        ("ok", RegistrationStatus.CONFIRMED),
    ]
    check = make_db()
    count = check.execute(
        select(func.count(SessionRegistration.id)).where(
            SessionRegistration.session_id == sid, SessionRegistration.user_id == a
        )
    ).scalar_one()
    assert count == 1
    assert _seat_taken(check, sid) == 1


# 5. Known limitation: per-participant limit across sessions ----------------


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Known limitation: max_sessions_per_user is checked under the *session* "
        "row lock, not a per-user lock, so concurrent registrations for two "
        "different sessions of the same event can both pass."
    ),
)
def test_max_sessions_per_user_holds_under_concurrency(factory, make_db):
    host = factory.user("host")
    a = factory.user()
    event_id = factory.event(host, max_sessions_per_user=1)
    s1 = factory.session(event_id, seat_capacity=5)
    s2 = factory.session(event_id, seat_capacity=5)

    # Make the interleaving deterministic: each request pauses right after its
    # "how many sessions has this user confirmed?" count query until the other
    # request has run its count too. If a future fix serialises the two
    # requests, the barrier times out and both carry on, so the test can pass.
    gate = threading.Barrier(2, timeout=5)

    def pause_after_count(conn, cursor, statement, *args):
        if "count(session_registrations.id)" in statement:
            try:
                gate.wait()
            except threading.BrokenBarrierError:
                pass

    db1, db2 = make_db(), make_db()
    for db in (db1, db2):
        event.listen(db.connection(), "after_cursor_execute", pause_after_count)

    run_concurrently(
        [
            lambda: service.register_session(s1, a, db1),
            lambda: service.register_session(s2, a, db2),
        ]
    )

    check = make_db()
    confirmed = check.execute(
        select(func.count(SessionRegistration.id)).where(
            SessionRegistration.user_id == a,
            SessionRegistration.status == RegistrationStatus.CONFIRMED,
        )
    ).scalar_one()
    assert confirmed <= 1
