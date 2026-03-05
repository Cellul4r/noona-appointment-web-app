import logging
from datetime import datetime
import uuid
from zoneinfo import ZoneInfo

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.config import settings
from app.schemas.email import EmailSchema
from app.db import SessionLocal

from app.models.user import User

from app.services.session_service import SessionService

from app.services.email_template_service import (
    build_event_overview_url,
    render_available_seat_html,
    render_email_confirmation_html,
    render_event_cancelled_summary_html,
    render_event_updated_summary_html,
    render_registration_removed_by_host_html,
    render_registration_summary_html,
    render_session_reminder_html,
)

from app.models.session_registration import SessionRegistration, RegistrationStatus
from app.models.session import Session as SessionModel
from app.models.event import Event


logger = logging.getLogger(__name__)


class EmailService:

    def __init__(self):
        self.fm = FastMail(self.get_connection_config())

    def get_connection_config(self):
        return ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=settings.mail_from,
            MAIL_FROM_NAME=settings.mail_from_name,
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_SSL_TLS=settings.mail_ssl_tls,
            MAIL_STARTTLS=settings.mail_starttls,
            USE_CREDENTIALS=settings.use_credentials,
            VALIDATE_CERTS=settings.validate_certs,
        )

    async def send_emails(self, subject: str, email: EmailSchema, html: str):
        message = MessageSchema(
            subject=subject,
            recipients=email.model_dump().get("email"),
            body=html,
            subtype=MessageType.html,
        )

        await self.fm.send_message(message)
        return {"message": "Email has been sent"}

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

            overview_url = build_event_overview_url(
                settings.frontend_login_success_uri,
                str(session.event.share_uuid),
            )

            now = datetime.utcnow()
            for recipient in recipients:
                user = db.execute(
                    select(User).where(User.email == recipient)
                ).scalar_one_or_none()
                if not user:
                    continue

                timezone = user.timezone or "Europe/London"
                html_body = render_available_seat_html(
                    app_name=settings.mail_from_name,
                    event_title=session.event.title,
                    session_start=session.start_datetime,
                    session_end=session.end_datetime,
                    overview_url=overview_url,
                    timezone=timezone,
                )

                await self.send_emails(
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
            raise
        finally:
            db.close()

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

            overview_url = build_event_overview_url(
                settings.frontend_login_success_uri,
                str(event.share_uuid),
            )
            html_body = render_registration_summary_html(
                app_name=settings.mail_from_name,
                full_name=user.full_name,
                event_title=event.title,
                event_location=event.location,
                session_registrations=session_registrations,
                overview_url=overview_url,
                timezone=user.timezone or "Europe/London",
            )

            await self.send_emails(
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
            raise
        finally:
            db.close()

    async def send_session_reminder_email(
        self, user_id: int, session_id: int, minutes_before: int | None = None
    ):
        # function for send via email of session reminder
        db = SessionLocal()
        try:
            row = db.execute(
                select(SessionModel, User)
                .join(
                    SessionRegistration,
                    SessionRegistration.session_id == SessionModel.id,
                )
                .join(User, User.id == SessionRegistration.user_id)
                .options(selectinload(SessionModel.event))
                .where(
                    SessionModel.id == session_id,
                    SessionRegistration.user_id == user_id,
                    SessionRegistration.status == RegistrationStatus.CONFIRMED,
                )
            ).first()

            if not row:
                logger.warning(
                    "Skip session reminder: session/user registration not found for user_id=%s, session_id=%s",
                    user_id,
                    session_id,
                )
                return

            session, user = row
            if session.event is None or not user.email:
                logger.warning(
                    "Skip session reminder: missing event or user email for user_id=%s, session_id=%s",
                    user_id,
                    session_id,
                )
                return

            overview_url = build_event_overview_url(
                settings.frontend_login_success_uri,
                str(session.event.share_uuid),
            )

            html_body = render_session_reminder_html(
                app_name=settings.mail_from_name,
                full_name=user.full_name,
                event_title=session.event.title,
                session_start=session.start_datetime,
                session_end=session.end_datetime,
                session_location=session.location or session.event.location or "TBA",
                overview_url=overview_url,
                minutes_before=minutes_before,
                timezone=user.timezone or "Europe/London",
            )

            await self.send_emails(
                f"Reminder: Your session for {session.event.title} starts soon",
                EmailSchema(email=[user.email]),
                html_body,
            )

        except Exception:
            logger.exception(
                "Failed to send session reminder email for user_id=%s, session_id=%s",
                user_id,
                session_id,
            )
            raise
        finally:
            db.close()

    async def send_registration_removed_by_host(
        self, user_id: int, session_id: int, registration_status: RegistrationStatus
    ):
        db = SessionLocal()
        try:
            user = db.execute(
                select(User).where(User.id == user_id)
            ).scalar_one_or_none()
            if not user:
                logger.warning(
                    "Failed to send registration removed email: user not found for user_id=%s",
                    user_id,
                )
                return
            session = db.execute(
                select(SessionModel)
                .options(selectinload(SessionModel.event))
                .where(SessionModel.id == session_id)
            ).scalar_one_or_none()
            if not session:
                logger.warning(
                    "Failed to send registration removed email: session not found for session_id=%s",
                    session_id,
                )
                return
            if session.event is None:
                logger.warning(
                    "Failed to send registration removed email: event not found for session_id=%s",
                    session_id,
                )
                return

            if not user.email:
                logger.warning(
                    "Failed to send registration removed email: user has no email for user_id=%s",
                    user_id,
                )
                return

            overview_url = build_event_overview_url(
                settings.frontend_login_success_uri,
                str(session.event.share_uuid),
            )

            html_body = render_registration_removed_by_host_html(
                app_name=settings.mail_from_name,
                full_name=user.full_name,
                event_title=session.event.title,
                session_start=session.start_datetime,
                session_end=session.end_datetime,
                session_location=session.location or session.event.location or "TBA",
                registration_status=registration_status.value,
                overview_url=overview_url,
                timezone=user.timezone or "Europe/London",
            )

            await self.send_emails(
                f"Registration removed from {session.event.title}",
                EmailSchema(email=[user.email]),
                html_body,
            )

        except Exception:
            logger.exception(
                "Failed to send registration removed by host email for user_id=%s, session_id=%s",
                user_id,
                session_id,
            )
            raise
        finally:
            db.close()

    async def send_event_update_email(
        self,
        user_id: int,
        event_id: int,
        event_change: dict,
        session_changes: list[dict],
    ):
        # function for send via email of event updated, session updated/cancelled
        db = SessionLocal()
        try:
            user = db.execute(
                select(User).where(User.id == user_id)
            ).scalar_one_or_none()
            if not user or not user.email:
                logger.warning(
                    "Failed to send event update email: user not found/email missing for user_id=%s",
                    user_id,
                )
                return

            event = db.execute(
                select(Event).where(Event.id == event_id)
            ).scalar_one_or_none()
            if not event:
                logger.warning(
                    "Failed to send event update email: event not found for event_id=%s",
                    event_id,
                )
                return

            overview_url = build_event_overview_url(
                settings.frontend_login_success_uri,
                str(event.share_uuid),
            )
            html_body = render_event_updated_summary_html(
                app_name=settings.mail_from_name,
                full_name=user.full_name,
                event_title=event.title,
                overview_url=overview_url,
                event_change=event_change,
                session_changes=session_changes,
                timezone=user.timezone or "Europe/London",
            )

            await self.send_emails(
                f"Update summary for {event.title}",
                EmailSchema(email=[user.email]),
                html_body,
            )
        except Exception:
            logger.exception(
                "Failed to send event update email for user_id=%s, event_id=%s",
                user_id,
                event_id,
            )
            raise
        finally:
            db.close()

    async def send_event_cancelled_email(
        self,
        user_id: int,
        event_title: str,
        session_rows: list[dict],
    ):
        db = SessionLocal()
        try:
            user = db.execute(
                select(User).where(User.id == user_id)
            ).scalar_one_or_none()
            if not user or not user.email:
                logger.warning(
                    "Failed to send event cancelled email: user not found/email missing for user_id=%s",
                    user_id,
                )
                return

            timezone = user.timezone or "Europe/London"
            tz = ZoneInfo(timezone)
            formatted_rows: list[dict] = []
            for row in session_rows or []:
                start_raw = row.get("start_datetime")
                end_raw = row.get("end_datetime")
                start = (
                    datetime.fromisoformat(str(start_raw))
                    .astimezone(tz)
                    .strftime("%d %b %Y, %I:%M %p")
                    if start_raw
                    else "-"
                )
                end = (
                    datetime.fromisoformat(str(end_raw))
                    .astimezone(tz)
                    .strftime("%d %b %Y, %I:%M %p")
                    if end_raw
                    else "-"
                )

                formatted_rows.append(
                    {
                        "session_uuid": row.get("session_uuid"),
                        "start": start,
                        "end": end,
                        "location": row.get("location") or "-",
                        "registration_status": row.get("registration_status") or "unknown",
                    }
                )

            html_body = render_event_cancelled_summary_html(
                app_name=settings.mail_from_name,
                full_name=user.full_name,
                event_title=event_title,
                session_rows=formatted_rows,
                timezone=timezone,
            )

            await self.send_emails(
                f"{event_title} has been cancelled",
                EmailSchema(email=[user.email]),
                html_body,
            )
        except Exception:
            logger.exception(
                "Failed to send event cancelled email for user_id=%s",
                user_id,
            )
            raise
        finally:
            db.close()

    async def send_email_confirmation(
        self,
        recipient_email: str,
        confirmation_link: str,
    ):
        html_body = render_email_confirmation_html(
            app_name=settings.mail_from_name,
            confirmation_link=confirmation_link,
        )

        await self.send_emails(
            "Please confirm your email address",
            EmailSchema(email=[recipient_email]),
            html_body,
        )