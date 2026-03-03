from __future__ import annotations

from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.event import Event
    from app.models.session import Session
    from app.models.user import User


class NotificationType(PyEnum):
    SESSION_REMINDER = "session_reminder"
    WAITLIST_AVAILABLE = "waitlist_available"
    REGISTRATION_SUMMARY = "registration_summary"
    EVENT_UPDATED = "event_updated"
    EVENT_CANCELLED = "event_cancelled"
    REGISTRATION_REMOVED_BY_HOST = "registration_removed_by_host"


class NotificationJobStatus(PyEnum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NotificationJob(Base):
    __tablename__ = "notification_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[NotificationType] = mapped_column(
        SAEnum(NotificationType), nullable=False, index=True
    )
    status: Mapped[NotificationJobStatus] = mapped_column(
        SAEnum(NotificationJobStatus),
        nullable=False,
        default=NotificationJobStatus.PENDING,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_id: Mapped[int | None] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=True, index=True
    )
    session_id: Mapped[int | None] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), nullable=True, index=True
    )

    payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    dedupe_key: Mapped[str | None] = mapped_column(
        String(255), nullable=True, unique=True
    )

    run_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    next_retry_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.utcnow()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    user: Mapped[User] = relationship(back_populates="notification_jobs")
    session: Mapped[Session | None] = relationship(back_populates="notification_jobs")
    event: Mapped[Event | None] = relationship(back_populates="notification_jobs")
