from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import db


class ConferenceRoom(db.Model):
    __tablename__ = "conference_rooms"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="room")
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "location": self.location,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }
