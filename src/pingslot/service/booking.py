from __future__ import annotations
from typing import TYPE_CHECKING

from pingslot.models import Booking, BookingStatus

if TYPE_CHECKING:
    from sqlmodel import Session
    from pingslot.bot.base import Bot


class BookingService:
    def __init__(self, session: Session, bot: Bot):
        self.bot = bot
        self.session = session

    async def create_booking(self, user_id: int, resource_id: int) -> Booking:
        booking = Booking(
            user_id=user_id, resource_id=resource_id, status=BookingStatus.PENDING
        )
        self.session.add(booking)
        self.session.commit()
        self.session.refresh(booking)
        await self.bot.notify("boo")
        return booking
