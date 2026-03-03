from __future__ import annotations

from datetime import datetime
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.schemas.session import SessionWithOptionalStatus


@lru_cache(maxsize=1)
def _template_env() -> Environment:
    templates_root = Path(__file__).resolve().parents[1] / "templates"
    return Environment(
        loader=FileSystemLoader(str(templates_root)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def build_event_overview_url(
    frontend_login_success_uri: str, event_share_uuid: str
) -> str:
    login_success_url = urlsplit(frontend_login_success_uri)
    origin = f"{login_success_url.scheme}://{login_success_url.netloc}"
    return f"{origin}/event/overview/{event_share_uuid}"


def render_available_seat_html(
    *,
    app_name: str,
    event_title: str,
    session_start: datetime,
    session_end: datetime,
    overview_url: str,
    timezone: str = "Europe/London",
) -> str:
    template = _template_env().get_template("email/available_seat_notification.html")
    session_start_local = session_start.astimezone(ZoneInfo(timezone))
    session_end_local = session_end.astimezone(ZoneInfo(timezone))

    return template.render(
        app_name=app_name,
        event_title=event_title,
        session_start=session_start_local.strftime("%d %b %Y, %I:%M %p"),
        session_end=session_end_local.strftime("%d %b %Y, %I:%M %p"),
        overview_url=overview_url,
        current_year=datetime.utcnow().year,
        timezone=timezone,
    )


def render_registration_summary_html(
    *,
    app_name: str,
    full_name: str,
    event_title: str,
    event_location: str | None,
    session_registrations: list[SessionWithOptionalStatus],
    overview_url: str,
    timezone: str = "Europe/London",
) -> str:
    template = _template_env().get_template("email/registration_summary.html")
    tz = ZoneInfo(timezone)

    rows = []
    for session in session_registrations:
        status_value = session.registration_status
        if hasattr(status_value, "value"):
            status_value = status_value.value
        status_value = (status_value or "unknown").lower()

        rows.append(
            {
                "session_uuid": str(session.uuid),
                "start": session.start_datetime.astimezone(tz).strftime(
                    "%d %b %Y, %I:%M %p"
                ),
                "end": session.end_datetime.astimezone(tz).strftime(
                    "%d %b %Y, %I:%M %p"
                ),
                "location": session.location or event_location or "-",
                "status": status_value,
            }
        )

    return template.render(
        app_name=app_name,
        full_name=full_name,
        event_title=event_title,
        session_rows=rows,
        overview_url=overview_url,
        current_year=datetime.utcnow().year,
        timezone=timezone,
    )


def render_session_reminder_html(
    *,
    app_name: str,
    full_name: str,
    event_title: str,
    session_start: datetime,
    session_end: datetime,
    session_location: str,
    overview_url: str,
    minutes_before: int | None = None,
    timezone: str = "Europe/London",
) -> str:
    template = _template_env().get_template("email/session_reminder.html")
    tz = ZoneInfo(timezone)

    session_start_local = session_start.astimezone(tz)
    session_end_local = session_end.astimezone(tz)

    return template.render(
        app_name=app_name,
        full_name=full_name,
        event_title=event_title,
        session_start=session_start_local.strftime("%d %b %Y, %I:%M %p"),
        session_end=session_end_local.strftime("%d %b %Y, %I:%M %p"),
        session_location=session_location,
        minutes_before=minutes_before,
        overview_url=overview_url,
        current_year=datetime.utcnow().year,
        timezone=timezone,
    )
