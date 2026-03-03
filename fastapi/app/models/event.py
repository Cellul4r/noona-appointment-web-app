from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime


import uuid
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.session import Session
    from app.models.notification_job import NotificationJob


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    share_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), index=True, unique=True, default=uuid.uuid4
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_draft: Mapped[bool] = mapped_column(default=True)

    max_sessions_per_user: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.utcnow()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.utcnow()
    )

    host: Mapped["User"] = relationship(back_populates="events")
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )
    notification_jobs: Mapped[list[NotificationJob]] = relationship(
        back_populates="event",
        passive_deletes=True,
    )
