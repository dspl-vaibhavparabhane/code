from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import db
import enum


class BookingStatus(str, enum.Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETE = "COMPLETE"


class Booking(db.Model):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("conference_rooms.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.CONFIRMED, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    room: Mapped["ConferenceRoom"] = relationship("ConferenceRoom", back_populates="bookings")
    user: Mapped["User"] = relationship("User", back_populates="bookings")
    
    def to_dict(self) -> dict:
        try:
            room_name = self.room.name if self.room else None
            room_location = self.room.location if self.room else None
        except:
            room_name = None
            room_location = None
        
        try:
            user_name = self.user.name if self.user else None
            user_email = self.user.email if self.user else None
        except:
            user_name = None
            user_email = None
            
        return {
            "id": self.id,
            "room_id": self.room_id,
            "room_name": room_name,
            "room_location": room_location,
            "user_id": self.user_id,
            "user_name": user_name,
            "user_email": user_email,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_minutes": int((self.end_time - self.start_time).total_seconds() / 60),
            "purpose": self.purpose,
            "status": self.status.value.lower(),
            "created_at": self.created_at.isoformat()
        }
