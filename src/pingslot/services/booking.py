from sqlmodel import Session
from pingslot.models import Booking, BookingStatus

class BookingService:
    def __init__(self, session: Session):
        self.session = session

    def create_booking(self, user_id: int, resource_id: int) -> Booking:
        booking = Booking(user_id=user_id, resource_id=resource_id, status=BookingStatus.PENDING)
        self.session.add(booking)
        self.session.commit()
        self.session.refresh(booking)
        return booking