from datetime import datetime
import logging
from pathlib import Path
from urllib.parse import urlsplit

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
    ) -> str:
        template = self.template_env.get_template(
            "email/available_seat_notification.html"
        )
        return template.render(
            app_name=settings.mail_from_name,
            event_title=event_title,
            session_start=session_start.strftime("%d %b %Y, %I:%M %p UTC"),
            session_end=session_end.strftime("%d %b %Y, %I:%M %p UTC"),
            overview_url=overview_url,
            current_year=datetime.utcnow().year,
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
            html_body = self._render_available_seat_html(
                event_title=session.event.title,
                session_start=session.start_datetime,
                session_end=session.end_datetime,
                overview_url=overview_url,
            )

            await self.email_service.send_emails(
                "Yay! A Seat is now available.",
                EmailSchema(email=recipients),
                html_body,
            )

            now = datetime.utcnow()
            for recipient in recipients:
                user = db.execute(
                    select(User).where(User.email == recipient)
                ).scalar_one_or_none()
                if not user:
                    continue

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
