from datetime import datetime
import logging
from pathlib import Path
from urllib.parse import urlsplit
import uuid
from zoneinfo import ZoneInfo

from fastapi import BackgroundTasks
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import SessionLocal
from app.config import settings
from app.models.session import Session as SessionModel
from app.schemas.email import EmailSchema
from app.services.mail_service import EmailService

from app.models.session_registration import SessionRegistration
from app.models.user import User
from app.models.event import Event
from app.schemas.session import SessionWithOptionalStatus

from app.services.session_service import SessionService


logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.email_service = EmailService()
        templates_root = Path(__file__).resolve().parents[1] / "templates"
        self.template_env = Environment(
            loader=FileSystemLoader(str(templates_root)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def _build_event_overview_url(self, event_share_uuid: str) -> str:
        login_success_url = urlsplit(settings.frontend_login_success_uri)
        origin = f"{login_success_url.scheme}://{login_success_url.netloc}"
        return f"{origin}/event/overview/{event_share_uuid}"

    def _render_available_seat_html(
        self,
        event_title: str,
        session_start: datetime,
        session_end: datetime,
        overview_url: str,
        timezone: str = "Europe/London",
    ) -> str:
        template = self.template_env.get_template(
            "email/available_seat_notification.html"
        )
        session_start = session_start.astimezone(ZoneInfo(timezone))
        session_end = session_end.astimezone(ZoneInfo(timezone))
        return template.render(
            app_name=settings.mail_from_name,
            event_title=event_title,
            session_start=session_start.strftime("%d %b %Y, %I:%M %p"),
            session_end=session_end.strftime("%d %b %Y, %I:%M %p"),
            overview_url=overview_url,
            current_year=datetime.utcnow().year,
            timezone=timezone,
        )

    def _render_registration_summary_html(
        self,
        full_name: str,
        event_title: str,
        event_location: str | None,
        session_registrations: list[SessionWithOptionalStatus],
        overview_url: str,
        timezone: str = "Europe/London",
    ) -> str:
        template = self.template_env.get_template("email/registration_summary.html")
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
            app_name=settings.mail_from_name,
            full_name=full_name,
            event_title=event_title,
            session_rows=rows,
            overview_url=overview_url,
            current_year=datetime.utcnow().year,
            timezone=timezone,
        )

    async def send_available_seat_email(self, recipients: list[str], session_id: int):
        db = SessionLocal()
        try:
            session = (
                db.execute(
                    select(SessionModel)
                    .options(selectinload(SessionModel.event))
                    .where(SessionModel.id == session_id)
                )
                .scalars()
                .one_or_none()
            )

            if session is None or session.event is None:
                logger.warning(
                    "Skip available-seat email: session or event missing for session_id=%s",
                    session_id,
                )
                return

            overview_url = self._build_event_overview_url(str(session.event.share_uuid))

            now = datetime.utcnow()
            for recipient in recipients:
                user = db.execute(
                    select(User).where(User.email == recipient)
                ).scalar_one_or_none()
                if not user:
                    continue

                timezone = user.timezone or "Europe/London"
                html_body = self._render_available_seat_html(
                    event_title=session.event.title,
                    session_start=session.start_datetime,
                    session_end=session.end_datetime,
                    overview_url=overview_url,
                    timezone=timezone,
                )

                await self.email_service.send_emails(
                    "Yay! A Seat is now available.",
                    EmailSchema(email=[recipient]),
                    html_body,
                )

                registration = db.execute(
                    select(SessionRegistration).where(
                        SessionRegistration.session_id == session_id,
                        SessionRegistration.user_id == user.id,
                    )
                ).scalar_one_or_none()

                if registration is not None:
                    registration.last_available_notified_at = now

            db.commit()
        except Exception:
            db.rollback()
            logger.exception("Failed to update available-seat notification timestamps")
        finally:
            db.close()

    def queue_available_seat_email(
        self,
        background_tasks: BackgroundTasks,
        recipients: list[str],
        session_id: int,
    ):
        if not recipients:
            return

        background_tasks.add_task(
            self.send_available_seat_email,
            recipients,
            session_id,
        )

    async def send_registration_summary_email(
        self, user_id: int, event_uuid: uuid.UUID
    ):
        # function for send via email of registration summary
        db = SessionLocal()
        try:
            event_uuid_value = event_uuid

            user = db.execute(
                select(User).where(User.id == user_id)
            ).scalar_one_or_none()
            if not user:
                logger.warning(
                    "Failed to send registration summary email: user not found for user_id=%s",
                    user_id,
                )
                return

            event = db.execute(
                select(Event).where(Event.share_uuid == event_uuid_value)
            ).scalar_one_or_none()
            if not event:
                logger.warning(
                    "Failed to send registration summary email: event not found for event_uuid=%s",
                    event_uuid,
                )
                return

            session_service = SessionService()
            session_registrations = session_service.get_registration_summary(
                event_uuid_value, user_id, db
            )

            if not session_registrations:
                logger.warning(
                    "No session registrations found for user_id=%s, event_uuid=%s",
                    user_id,
                    event_uuid,
                )
                return

            overview_url = self._build_event_overview_url(str(event.share_uuid))
            html_body = self._render_registration_summary_html(
                full_name=user.full_name,
                event_title=event.title,
                event_location=event.location,
                session_registrations=session_registrations,
                overview_url=overview_url,
                timezone=user.timezone or "Europe/London",
            )

            await self.email_service.send_emails(
                f"Your Registration Summary for {event.title}",
                EmailSchema(email=[user.email]),
                html_body,
            )
        except Exception:
            logger.exception(
                "Failed to send registration summary email for user_id=%s, event_uuid=%s",
                user_id,
                event_uuid,
            )
        finally:
            db.close()

    def queue_registration_summary_email(
        self, background_tasks: BackgroundTasks, user_id: int, event_uuid: str
    ):
        background_tasks.add_task(
            self.send_registration_summary_email,
            user_id,
            event_uuid,
        )
