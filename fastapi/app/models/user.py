from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


if TYPE_CHECKING:
    from app.models.event import Event
    from app.models.oauth_user import OAuthUser
    from app.models.session_registration import SessionRegistration
    from app.models.notification_job import NotificationJob


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(200), nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    profile_image: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )
    timezone: Mapped[str] = mapped_column(
        String(64), default="Europe/London", nullable=False
    )
    email_notifications: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.utcnow()
    )

    events: Mapped[list["Event"]] = relationship(
        back_populates="host",
        cascade="all, delete-orphan",
    )

    oauth_accounts: Mapped[list["OAuthUser"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    sessions_registered: Mapped[list[SessionRegistration]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    notification_jobs: Mapped[list[NotificationJob]] = relationship(
        back_populates="user",
        passive_deletes=True,
    )

    @property
    def has_password(self) -> bool:
        """Indicates whether the user has a usable password set."""
        return bool(self.password_hash)

    """
    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"
    """
