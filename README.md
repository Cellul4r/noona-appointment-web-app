# Noona Appointment

A registration platform for multi-session events, built so the last seat can only go to one person.

**Live demo:** https://noona-appointment.vercel.app/

| Register for a session | Waitlisted when full |
| --- | --- |
| ![Session with free seats](docs/screenshot/register-available.png) | ![Session full, user waitlisted](docs/screenshot/register-waitlisted.png) |
| **Participant dashboard** | **Host view of registered users** |
| ![Participant dashboard](docs/screenshot/dashboard-1.png) | ![Host managing registered users](docs/screenshot/host-registered-users.png) |

## Features

**Hosts**
- Create events with multiple sessions, each with its own time, location and seat capacity (or unlimited seats).
- Limit how many sessions one participant can book per event (`max_sessions_per_user`).
- Share a public event overview by link (events stay private while they are drafts).
- See who registered for each session, and remove participants.

**Participants**
- Register for a session: you get a seat if one is free, otherwise you join the waitlist.
- When a seat frees up, waitlisted participants are notified and can claim it.
- Dashboard of your registrations, and a calendar shown in your own timezone.
- Sign up with email (with verification and password reset), or log in with Google or GitHub.

**Email notifications**
- Six types: session reminder, seat available, registration summary, event updated, event cancelled, and removed by host.
- Up to 2 reminders per session, at times the participant chooses.
- "Seat available" emails go out at most once per hour per registration.
- Participants can turn emails off in their settings.

## Tech stack

| Layer | Tools |
| --- | --- |
| Frontend | Vue 3, Vite, Tailwind CSS 4, DaisyUI |
| Backend | FastAPI, Pydantic, SQLAlchemy 2.0, Alembic, fastapi-mail, fastapi-sso |
| Data | PostgreSQL on Supabase, Supabase Storage (profile images) |
| Hosting | Vercel: static frontend + Python function + Cron, region `sin1` |
| Email | Gmail SMTP |
| Local dev | Docker Compose |

## Architecture

```mermaid
flowchart LR
    SPA["Vue 3 SPA"] -->|"HTTPS, JWT cookie + CSRF token"| API

    subgraph API["FastAPI (Vercel Python function)"]
        direction TB
        MW["CORS middleware<br/>+ auth / CSRF dependencies"] --> R["Routers"]
        R --> S["Services<br/>(business rules, transactions)"]
        S --> M["SQLAlchemy models"]
    end

    M --> PG[("Supabase PostgreSQL")]
    S --> ST["Supabase Storage"]
    S --> SMTP["Gmail SMTP"]

    CRON["Vercel Cron<br/>every 5 min"] -->|"GET /api/notifications/dispatch<br/>Authorization: Bearer CRON_SECRET"| R
```

Services use SQLAlchemy sessions directly. There is no separate repository layer.

## How the last seat works

Each registration is in one of three states:

| State | Meaning |
| --- | --- |
| `CONFIRMED` | Holds a seat (counted in `sessions.seat_taken`). |
| `WAITLIST` | The session was full when the user registered. |
| `AVAILABLE` | A seat opened up. The user has been notified and may claim it. |

Nobody is promoted automatically. When a confirmed participant leaves, every `WAITLIST` registration becomes `AVAILABLE` and those users are emailed. **The first one to accept gets the seat.** When the session fills again, the remaining `AVAILABLE` users go back to `WAITLIST`, and their pending "seat available" emails are cancelled.

**The race.** Claiming a seat is read-check-write: read `seat_taken`, check it is below `seat_capacity`, then write `seat_taken + 1`. If two people accept the last seat at the same moment, both could read 9 of 10 and both could be confirmed.

**The fix** (in [`session_service.py`](fastapi/app/services/session_service.py)):
- `register_session` and `confirm_session` start with `SELECT … FROM sessions WHERE id = … FOR UPDATE`, so requests for the same session run one at a time.
- PostgreSQL's default `READ COMMITTED` isolation means the second request, once it gets the lock, reads the row as the first request committed it.
- The capacity check runs **after** the lock is taken, so it always sees the current `seat_taken`.
- A unique constraint on `(session_id, user_id)` stops a double-click from creating two registrations.

This is tested on real PostgreSQL in [`fastapi/app/tests/concurrency/test_seat_races.py`](fastapi/app/tests/concurrency/test_seat_races.py):
- two users accepting the last seat at once (20 rounds);
- a test proving the second request really waits for the lock;
- 20 users racing for 5 seats;
- a double-click.

## Email queue

Emails are not sent inside the request. They are written to a `notification_jobs` table, and the Vercel Cron job calls `/api/notifications/dispatch` every 5 minutes to send due jobs in batches.

- `dedupe_key` (unique) stops the same reminder from being queued twice.
- Failed sends are retried with a backoff of `min(2^(n-1), 60)` minutes after the n-th attempt, up to 5 attempts. After that the job is marked `FAILED`.

## Getting started

Requirements: Docker Desktop.

1. Copy the environment template and fill it in:
   ```sh
   cp .env.example .env
   ```

   | Variable | Purpose |
   | --- | --- |
   | `DATABASE_URL` | Local Postgres connection string (used when `USE_SUPABASE=false`) |
   | `USE_SUPABASE`, `SUPABASE_DB_URL` | Use the Supabase database instead of local Postgres |
   | `SUPABASE_URL`, `SUPABASE_KEY`, `BUCKET_NAME` | Supabase Storage for profile images |
   | `SECRET_KEY`, `JWT_SECRET_KEY` | Signing keys (random strings) |
   | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | Google login |
   | `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET` | GitHub login |
   | `MAIL_USERNAME`, `MAIL_PASSWORD` | Gmail SMTP account |
   | `FRONTEND_BASE_URL`, `VITE_API_BASE_URL`, `ALLOWED_ORIGINS`, `FRONTEND_LOGIN_SUCCESS_URI` | URLs and CORS |
   | `CRON_SECRET` | Bearer token for `/notifications/dispatch` |

2. Start everything:
   ```sh
   ./run.sh
   ```
   With `USE_SUPABASE=true` in `.env`, this starts the API and frontend only. Otherwise it also starts a local Postgres container (Compose profile `with-db`).

3. Open the frontend at http://localhost:8080. The API runs at http://localhost:56733 (docs at `/docs`).

## Running tests

Run all commands from `fastapi/`. The app reads some settings when it is imported, so set placeholders first:

```sh
cd fastapi
pip install -r requirements.txt
export GITHUB_CLIENT_ID= GITHUB_CLIENT_SECRET= SUPABASE_URL=http://localhost:54321 SUPABASE_KEY=test-key
```

**Unit tests (SQLite, in memory):**
```sh
pytest --ignore=app/tests/concurrency
```

**Concurrency tests (PostgreSQL).** SQLite ignores `SELECT … FOR UPDATE`, so these need a real Postgres database. They create and drop their own tables, so use a throwaway database:
```sh
docker run --rm -d --name noona-test-pg -p 55432:5432 -e POSTGRES_PASSWORD=test postgres:16-alpine
TEST_DATABASE_URL=postgresql://postgres:test@localhost:55432/postgres pytest app/tests/concurrency
docker stop noona-test-pg
```
Without `TEST_DATABASE_URL`, these tests are skipped.

GitHub Actions ([`.github/workflows/tests.yml`](.github/workflows/tests.yml)) runs both suites on every push and pull request. It uses a temporary Postgres service container.

## Project structure

```
.
├── frontend/              Vue 3 SPA (views, components, Pinia store, router)
├── fastapi/
│   ├── app/
│   │   ├── routers/       HTTP endpoints
│   │   ├── services/      Business logic and transactions
│   │   ├── models/        SQLAlchemy models
│   │   ├── schemas/       Pydantic request/response models
│   │   ├── dependencies/  Auth, CSRF, SSO, Supabase client
│   │   ├── templates/     Email templates
│   │   └── tests/         Unit tests + concurrency/ (PostgreSQL)
│   └── alembic/           Migrations
├── docs/                  DBML schema (noona-schema.dbml) and screenshots
├── design/                Database and UI design files
├── docker-compose.yml
├── run.sh
└── vercel.json            Builds, routes, cron and region
```

## Deployment

The app is deployed on Vercel ([`vercel.json`](vercel.json)):
- The frontend is built as static files (`frontend/dist`).
- `fastapi/main.py` runs as a Python serverless function, serving `/api/*`.
- A cron job calls `/api/notifications/dispatch?size=50` every 5 minutes.
- Region `sin1` (Singapore). The database is PostgreSQL on Supabase.

## Known limitations

- **First to accept, not first in line.** When a seat frees up, every waitlisted user is notified at once, and whoever accepts first gets it. Waitlist order isn't kept.
- **Email delay.** Emails are sent by a cron job every 5 minutes, so they can arrive up to about 5 minutes late.
- **Per-participant limit race.** `max_sessions_per_user` is checked under the *session's* row lock, not a per-user lock. If one user registers for two different sessions of the same event at the same moment, both can succeed. A strict `xfail` test documents this, so the test suite will flag it once it's fixed.

## Course context

Built for **204212 Modern Application Development**, Semester 2/2025.

- **Group:** 24cs212g05 (Project 5: appointment booking system)
- **Mentor:** นภพล สวัสดิ์วงค์ (พี่ก้าหาร)
- **Main development:** February–March 2026
- **Presentation feedback:** slide นำเสนอหน้า user flow diagram ตัวอักษรใน diagram ควรใหญ่กว่านี้ และควรทำให้รูปใช้พื้นที่ว่างที่เหลือในหน้านั้นให้เต็ม

## Team

| Name | GitHub | Role |
| --- | --- | --- |
| Theerada Siri | [Cellul4r](https://github.com/Cellul4r) | Fullstack |
| Punchita Sittisarit | [q28jes](https://github.com/q28jes) | Fullstack |
| Pitchayanat Patthamasewee | [Fres26](https://github.com/Fres26) | Frontend |
| Krit Thongjib | [Not-Tan](https://github.com/Not-Tan) | Fullstack |

## License

[MIT](LICENSE)
