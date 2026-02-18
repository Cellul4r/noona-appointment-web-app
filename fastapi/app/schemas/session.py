from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator


class SessionBase(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    seat_capacity: int = Field(default=1, ge=1)

    @model_validator(mode="after")
    def validate_datetimes(self):
        if self.end_datetime <= self.start_datetime:
            raise ValueError("end_datetime must be after start_datetime")
        return self


class SessionCreate(SessionBase):
    pass


# For Users
class SessionPublic(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    seat_taken: int = Field(default=0, ge=0)


class SessionWithOptionalStatus(SessionPublic):
    registration_status: str | None = Field(default=None)


class SessionWithEventPublic(SessionWithOptionalStatus):
    event: EventPublic


class SessionPrivate(SessionPublic):
    created_at: datetime


class SessionUpdate(BaseModel):
    start_datetime: datetime | None = Field(default=None)
    end_datetime: datetime | None = Field(default=None)
    seat_capacity: int | None = Field(default=None, ge=1)


from app.schemas.event import EventPublic

SessionWithEventPublic.model_rebuild()
