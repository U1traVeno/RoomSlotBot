from __future__ import annotations

from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship  # type: ignore


class Platform(str, Enum):
    TELEGRAM = "telegram"
    QQ = "qq"


class BookingStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    invite_code: str
    resources: list[Resource] = Relationship()
    bookings: list[Booking] = Relationship()
    user_bindings: list[UserBinding] = Relationship()


class UserBinding(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    platform: Platform
    platform_id: str


class Resource(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    name: str = Field(unique=True)
    description: str | None = None


class Booking(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    resource_id: int = Field(foreign_key="resource.id")
    status: BookingStatus = Field(default=BookingStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: User = Relationship(back_populates="bookings")
    resource: Resource = Relationship()
