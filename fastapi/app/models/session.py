from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.event import Event
    from app.models.session_registration import SessionRegistration


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    seat_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    recurrence_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    recurrence_interval: Mapped[int | None] = mapped_column(Integer, nullable=True)
    recurrence_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    recurrence_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.utcnow()
    )

    event: Mapped["Event"] = relationship("Event", back_populates="sessions")

    sessions_registered: Mapped[list["SessionRegistration"]] = relationship(
        "SessionRegistration", back_populates="session", cascade="all, delete-orphan"
    )
