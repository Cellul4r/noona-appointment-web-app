from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.session import Session


class RegistrationStatus(PyEnum):
    CONFIRMED = "confirmed"
    WAITLIST = "waitlist"
    AVAILABLE = "available"


class SessionRegistration(Base):
    __tablename__ = "session_registrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[RegistrationStatus] = mapped_column(
        SAEnum(RegistrationStatus), nullable=False
    )

    session: Mapped["Session"] = relationship(back_populates="sessions_registered")
