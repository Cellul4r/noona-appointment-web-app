from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID


class EventBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    location: str | None = None
    description: str | None = None
    limit_sessions_per_user: bool = False
    max_sessions_per_user: int | None = Field(default=None, ge=1)

class EventCreate(EventBase):
    is_draft: bool = True


class EventPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    location: str | None
    description: str | None
    share_uuid: UUID


class EventPrivate(EventPublic):
    owner_id: int
    is_draft: bool
    limit_sessions_per_user: bool
    max_sessions_per_user: int | None
    created_at: datetime
    updated_at: datetime


class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    location: str | None = None
    description: str | None = None
    is_draft: bool | None = None
    limit_sessions_per_user: bool | None = None
    max_sessions_per_user: int | None = Field(default=None, ge=1)