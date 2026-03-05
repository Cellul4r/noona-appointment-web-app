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


def render_registration_removed_by_host_html(
    *,
    app_name: str,
    full_name: str,
    event_title: str,
    session_start: datetime,
    session_end: datetime,
    session_location: str,
    overview_url: str,
    registration_status: str | None = None,
    timezone: str = "Europe/London",
) -> str:
    template = _template_env().get_template("email/registration_removed_by_host.html")
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
        registration_status=registration_status,
        overview_url=overview_url,
        current_year=datetime.utcnow().year,
        timezone=timezone,
    )


def render_event_updated_summary_html(
    *,
    app_name: str,
    full_name: str,
    event_title: str,
    overview_url: str,
    event_change: dict,
    session_changes: list[dict],
    timezone: str = "Europe/London",
) -> str:
    template = _template_env().get_template("email/event_updated_summary.html")

    rows: list[dict] = []
    tz = ZoneInfo(timezone)
    for change in session_changes or []:
        start_raw = change.get("start_datetime")
        end_raw = change.get("end_datetime")
        start_formatted = None
        end_formatted = None

        if start_raw:
            start_formatted = datetime.fromisoformat(str(start_raw)).astimezone(tz).strftime(
                "%d %b %Y, %I:%M %p"
            )
        if end_raw:
            end_formatted = datetime.fromisoformat(str(end_raw)).astimezone(tz).strftime(
                "%d %b %Y, %I:%M %p"
            )

        rows.append(
            {
                "action": change.get("action") or "update",
                "session_uuid": change.get("session_uuid"),
                "start": start_formatted,
                "end": end_formatted,
                "location": change.get("location") or "-",
            }
        )

    event_rows: list[dict] = []
    for field, values in (event_change or {}).items():
        event_rows.append(
            {
                "field": field,
                "old": (values or {}).get("old"),
                "new": (values or {}).get("new"),
            }
        )

    return template.render(
        app_name=app_name,
        full_name=full_name,
        event_title=event_title,
        event_rows=event_rows,
        session_rows=rows,
        overview_url=overview_url,
        timezone=timezone,
        current_year=datetime.utcnow().year,
    )


def render_event_cancelled_summary_html(
    *,
    app_name: str,
    full_name: str,
    event_title: str,
    session_rows: list[dict],
    timezone: str = "Europe/London",
) -> str:
    template = _template_env().get_template("email/event_cancelled_summary.html")

    return template.render(
        app_name=app_name,
        full_name=full_name,
        event_title=event_title,
        session_rows=session_rows,
        timezone=timezone,
        current_year=datetime.utcnow().year,
    )


def render_email_confirmation_html(
    *,
    app_name: str,
    confirmation_link: str,
) -> str:
    template = _template_env().get_template("email/email_confirmation.html")
    return template.render(
        app_name=app_name,
        confirmation_link=confirmation_link,
        current_year=datetime.utcnow().year,
    )


def render_reset_password_html(
    *,
    app_name: str,
    reset_link: str,
) -> str:
    template = _template_env().get_template("email/reset_password.html")
    return template.render(
        app_name=app_name,
        reset_link=reset_link,
        current_year=datetime.utcnow().year,
    )
