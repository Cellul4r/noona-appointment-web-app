from datetime import datetime, timedelta
import email
import logging
import uuid

from fastapi import HTTPException, status
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
    ) -> NotificationJob:
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
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A similar notification job is already scheduled. Please try again later.",
            )
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

    def enqueue_registration_summary_job(self, user_id: int, event_uuid: uuid.UUID):
        now = datetime.utcnow()
        run_at = now + timedelta(minutes=30)
        dedupe_window = run_at.strftime("%Y%m%d%H") + (
            "00" if run_at.minute < 30 else "30"
        )
        payload = {"event_uuid": str(event_uuid)}
        self.enqueue_notification_job(
            notification_type=NotificationType.REGISTRATION_SUMMARY,
            user_id=user_id,
            payload=payload,
            run_at=run_at,
            dedupe_key=f"registration_summary:{user_id}:{event_uuid}:{dedupe_window}",
        )

    def enqueue_session_reminder_job(
        self, user_id: int, session_id: int, start_time: datetime, reminders: list[int]
    ):
        reminders = sorted(reminders, reverse=True)[:2]
        for minutes_before in reminders:  # limit to max 2 reminder alerts
            run_at = start_time - timedelta(minutes=minutes_before)
            payload = {
                "session_id": session_id,
                "minutes_before": minutes_before,
                "start_time": start_time.isoformat(),
            }
            # reminders is expected to be a list of minutes before session start
            self.enqueue_notification_job(
                notification_type=NotificationType.SESSION_REMINDER,
                user_id=user_id,
                session_id=session_id,
                run_at=run_at,
                payload=payload,
                dedupe_key=f"session_reminder:{user_id}:{session_id}:{minutes_before}",
            )

    def _calculate_next_retry_at(self, attempts: int, now: datetime) -> datetime:
        delay_minutes = min(2 ** max(attempts - 1, 0), 60)
        return now + timedelta(minutes=delay_minutes)

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

            # re-instantiate to avoid potential issues with long-running process
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

                        await self.email_service.send_available_seat_email(
                            [user.email], job.session_id
                        )
                    elif job.type == NotificationType.REGISTRATION_SUMMARY:
                        event_uuid = (job.payload or {}).get("event_uuid")
                        if not event_uuid:
                            job.status = NotificationJobStatus.CANCELLED
                            result["skipped"] += 1
                            continue
                        await self.email_service.send_registration_summary_email(
                            user_id=job.user_id,
                            event_uuid=uuid.UUID(str(event_uuid)),
                        )
                    elif job.type == NotificationType.SESSION_REMINDER:
                        if job.session_id is None:
                            job.status = NotificationJobStatus.CANCELLED
                            result["skipped"] += 1
                            continue
                        minutes_before = (job.payload or {}).get("minutes_before")
                        await self.email_service.send_session_reminder_email(
                            user_id=job.user_id,
                            session_id=job.session_id,
                            minutes_before=minutes_before,
                        )
                    else:
                        job.status = NotificationJobStatus.CANCELLED
                        job.next_retry_at = None
                        result["skipped"] += 1
                        continue

                    job.status = NotificationJobStatus.SENT
                    job.sent_at = datetime.utcnow()
                    job.next_retry_at = None
                    job.last_error = None
                    result["sent"] += 1
                except Exception as exc:
                    job.attempts += 1
                    job.last_error = str(exc)
                    if job.attempts >= job.max_attempts:
                        job.status = NotificationJobStatus.FAILED
                        job.next_retry_at = None
                    else:
                        next_retry_at = self._calculate_next_retry_at(job.attempts, now)
                        job.status = NotificationJobStatus.PENDING
                        job.next_retry_at = next_retry_at
                        job.run_at = next_retry_at
                    result["failed"] += 1

            db.commit()
            return result
        except Exception:
            db.rollback()
            logger.exception("Failed to dispatch pending notification jobs")
            raise
        finally:
            db.close()
