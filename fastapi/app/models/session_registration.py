from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text,Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class RegistrationStatus(Enum):
    CONFIRMED = "confirmed"
    WAITLIST = "waitlist"
    CANCELLED = "cancelled" 
    AVAILABLE = "available"  


class SessionRegistrations(Base):
    __tablename__ = "session_registrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey="sessions.id",
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey="users.id",
        nullable=False
    )
    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    status:Mapped[RegistrationStatus] = mapped_column(
        Enum(RegistrationStatus), 
        nullable=False
    )

    session: Mapped["Session"] = relationship("Session", back_populate="sessions_registered")
