from datetime import datetime
import logging
import uuid

from fastapi import BackgroundTasks
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.db import SessionLocal
from app.config import settings
from app.models.session import Session as SessionModel
from app.schemas.email import EmailSchema
from app.services.mail_service import EmailService

from app.models.session_registration import SessionRegistration
from app.models.user import User
from app.models.event import Event
from app.models.notification_job import (
    NotificationJob,
    NotificationJobStatus,
    NotificationType,
)
from app.services.email_template_service import (
    build_event_overview_url,
    render_available_seat_html,
    render_registration_summary_html,
)

from app.services.session_service import SessionService


logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.email_service = EmailService()

    def enqueue_notification_job(
        self,
        *,
        notification_type: NotificationType,
        user_id: int,
        run_at: datetime,
        payload: dict,
        event_id: int | None = None,
        session_id: int | None = None,
        dedupe_key: str | None = None,
    ) -> NotificationJob | None:
        db = SessionLocal()
        try:
            job = NotificationJob(
                type=notification_type,
                user_id=user_id,
                event_id=event_id,
                session_id=session_id,
                payload=payload,
                run_at=run_at,
                dedupe_key=dedupe_key,
            )
            db.add(job)
            db.commit()
            db.refresh(job)
            return job
        except IntegrityError:
            db.rollback()
            logger.info(
                "Skip duplicate notification job for dedupe_key=%s",
                dedupe_key,
            )
            return None
        finally:
            db.close()

    def enqueue_waitlist_available_jobs(
        self,
        *,
        session: SessionModel,
        recipient_user_ids: list[int],
        run_at: datetime | None = None,
    ) -> None:
        if not recipient_user_ids:
            return

        scheduled_at = run_at or datetime.utcnow()
        payload = {
            "session_uuid": str(session.uuid),
            "event_uuid": str(session.event.share_uuid),
            "event_title": session.event.title,
        }

        for target_user_id in recipient_user_ids:
            self.enqueue_notification_job(
                notification_type=NotificationType.WAITLIST_AVAILABLE,
                user_id=target_user_id,
                event_id=session.event_id,
                session_id=session.id,
                payload=payload,
                run_at=scheduled_at,
                dedupe_key=f"waitlist_available:{session.id}:{target_user_id}:{scheduled_at.strftime('%Y%m%d%H')}",
            )

    async def dispatch_pending_jobs(self, batch_size: int = 50) -> dict:
        db = SessionLocal()
        now = datetime.utcnow()
        result = {"processed": 0, "sent": 0, "failed": 0, "skipped": 0}
        try:
            jobs = (
                db.execute(
                    select(NotificationJob)
                    .where(
                        NotificationJob.status == NotificationJobStatus.PENDING,
                        NotificationJob.run_at <= now,
                    )
                    .order_by(NotificationJob.run_at.asc(), NotificationJob.id.asc())
                    .limit(batch_size)
                )
                .scalars()
                .all()
            )

            for job in jobs:
                result["processed"] += 1
                try:
                    if (
                        job.type == NotificationType.WAITLIST_AVAILABLE
                        and job.session_id is not None
                    ):
                        user = db.execute(
                            select(User).where(User.id == job.user_id)
                        ).scalar_one_or_none()
                        if not user or not user.email:
                            job.status = NotificationJobStatus.CANCELLED
                            result["skipped"] += 1
                            continue

                        await self.send_available_seat_email([user.email], job.session_id)
                    elif job.type == NotificationType.REGISTRATION_SUMMARY:
                        event_uuid = (job.payload or {}).get("event_uuid")
                        if not event_uuid:
                            job.status = NotificationJobStatus.CANCELLED
                            result["skipped"] += 1
                            continue
                        await self.send_registration_summary_email(
                            user_id=job.user_id,
                            event_uuid=uuid.UUID(str(event_uuid)),
                        )
                    else:
                        job.status = NotificationJobStatus.CANCELLED
                        result["skipped"] += 1
                        continue

                    job.status = NotificationJobStatus.SENT
                    job.sent_at = datetime.utcnow()
                    job.last_error = None
                    result["sent"] += 1
                except Exception as exc:
                    job.attempts += 1
                    job.last_error = str(exc)
                    if job.attempts >= job.max_attempts:
                        job.status = NotificationJobStatus.FAILED
                    result["failed"] += 1

            db.commit()
            return result
        except Exception:
            db.rollback()
            logger.exception("Failed to dispatch pending notification jobs")
            raise
        finally:
            db.close()

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
