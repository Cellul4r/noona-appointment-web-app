from __future__ import annotations
from typing import TYPE_CHECKING, List
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID


class EventBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    max_sessions_per_user: int | None = Field(default=None, ge=1)


class EventCreate(EventBase):
    is_draft: bool = True
    sessions: List[SessionCreate]


class EventPublic(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    share_uuid: UUID
    host: UserPublic
    is_draft: bool
    updated_at: datetime

class EventSessionPublic(EventPublic):
    sessions: List[SessionPublic]


class EventPrivate(EventPublic):
    is_draft: bool
    created_at: datetime
    updated_at: datetime


class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    is_draft: bool | None = None
    max_sessions_per_user: int | None = Field(default=None, ge=1)


from app.schemas.user import UserPublic
from app.schemas.session import SessionCreate, SessionPublic

EventSessionPublic.model_rebuild()
