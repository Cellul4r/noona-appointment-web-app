from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_extra_types.timezone_name import TimeZoneName

from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    full_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str = Field(min_length=1, max_length=100)
    profile_image: str | None


class UserPrivate(UserPublic):
    id: int
    email: EmailStr = Field(max_length=120)
    timezone: TimeZoneName = Field(default="UTC", max_length=64)
    email_notifications: bool
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=120)
    profile_image: str | None = None
    timezone: TimeZoneName | None = Field(default="UTC", max_length=64)
    email_notifications: bool | None = None

class UserSignIn(BaseModel):
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=8)