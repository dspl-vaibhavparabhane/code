from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app.models import db, Booking, ConferenceRoom, BookingStatus


class BookingService:
    
    @staticmethod
    def check_overlap(room_id: int, start_time: datetime, end_time: datetime, exclude_booking_id: int = None) -> bool:
        """Check if booking overlaps with existing confirmed bookings"""
        query = Booking.query.filter(
            and_(
                Booking.room_id == room_id,
                Booking.status == BookingStatus.CONFIRMED,
                or_(
                    and_(Booking.start_time < end_time, Booking.end_time > start_time)
                )
            )
        )
        
        if exclude_booking_id:
            query = query.filter(Booking.id != exclude_booking_id)
        
        return query.first() is not None
    
    @staticmethod
    def validate_booking(room_id: int, start_time: datetime, end_time: datetime) -> tuple[bool, str]:
        """Validate booking constraints"""
        # Check if room exists and is active
        room = ConferenceRoom.query.get(room_id)
        if not room:
            return False, "Conference room not found"
        if not room.is_active:
            return False, "Conference room is not active"
        
        now = datetime.now(timezone.utc)
        
        # Check if booking is in the past
        if start_time < now:
            return False, "Booking date cannot be in the past"
        
        # Check if start time is before end time
        if start_time >= end_time:
            return False, "Start time must be earlier than end time"
        
        # Check for overlapping bookings
        if BookingService.check_overlap(room_id, start_time, end_time):
            return False, "Room is already booked for the selected time slot"
        
        return True, "Valid"
    
    @staticmethod
    def create_booking(room_id: int, user_id: int, start_time: datetime, end_time: datetime, purpose: str) -> tuple[Booking | None, str]:
        """Create a new booking with validation"""
        from sqlalchemy.exc import OperationalError
        
        try:
            
            room = db.session.query(ConferenceRoom)\
                .with_for_update(nowait=True)\
                .filter_by(id=room_id)\
                .first()
            
            if not room:
                return None, "Conference room not found"
            
            if not room.is_active:
                return None, "Conference room is not active"
            
            now = datetime.now(timezone.utc)
            
            # Check if booking is in the past
            if start_time < now:
                return None, "Booking date cannot be in the past"
            
            # Check if start time is before end time
            if start_time >= end_time:
                return None, "Start time must be earlier than end time"
            
            # Check minimum booking duration (15 minutes)
            duration = (end_time - start_time).total_seconds() / 60
            if duration < 15:
                return None, "Minimum booking duration is 15 minutes"
            
            # Check if booking is within the same date
            if start_time.date() != end_time.date():
                return None, "Booking must be within the same date. Cannot span multiple days"
            
            # Check for overlapping bookings
            if BookingService.check_overlap(room_id, start_time, end_time):
                return None, "Room is already booked for the selected time slot"
            
            booking = Booking(
                room_id=room_id,
                user_id=user_id,
                start_time=start_time,
                end_time=end_time,
                purpose=purpose,
                status=BookingStatus.CONFIRMED
            )
            
            db.session.add(booking)
            db.session.commit()
            db.session.refresh(booking)
            
            return booking, "Booking confirmed successfully"
            
        except OperationalError:
            db.session.rollback()
            return None, "This room is being booked by another user right now. Please try again in a moment."
        except Exception as e:
            db.session.rollback()
            print(f"Error creating booking: {str(e)}")
            return None, f"Failed to create booking: {str(e)}"
    
    @staticmethod
    def update_completed_bookings():
        """Update bookings to COMPLETE when end_time has passed"""
        now = datetime.now(timezone.utc)
        Booking.query.filter(
            Booking.status == BookingStatus.CONFIRMED,
            Booking.end_time < now
        ).update({"status": BookingStatus.COMPLETE})
        db.session.commit()
    
    @staticmethod
    def get_user_bookings(user_id: int, upcoming_only: bool = False, status: str = "", search: str = "", sort_by: str = "start_time", order: str = "desc", limit: int = 10, offset: int = 0):
        """Get bookings for a specific user with pagination"""
        BookingService.update_completed_bookings()
        
        query = Booking.query.filter_by(user_id=user_id)
        
        if upcoming_only:
            now = datetime.now(timezone.utc)
            query = query.filter(Booking.start_time >= now, Booking.status == BookingStatus.CONFIRMED)
        
        if status:
            query = query.filter(Booking.status == BookingStatus[status.upper()])
        
        if search:
            search_filter = f"%{search}%"
            query = query.join(ConferenceRoom).filter(
                or_(
                    ConferenceRoom.name.ilike(search_filter),
                    Booking.purpose.ilike(search_filter)
                )
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        if sort_by == "room_name":
            query = query.join(ConferenceRoom)
            column = ConferenceRoom.name
        elif hasattr(Booking, sort_by):
            column = getattr(Booking, sort_by)
        else:
            column = Booking.start_time
        
        query = query.order_by(column.desc() if order == "desc" else column.asc())
        
        # Apply pagination
        bookings = query.limit(limit).offset(offset).all()
        
        return bookings, total
    
    @staticmethod
    def get_all_bookings(upcoming_only: bool = False, status: str = "", search: str = "", sort_by: str = "start_time", order: str = "desc", limit: int = 10, offset: int = 0):
        """Get all bookings (for HR/Admin) with pagination"""
        BookingService.update_completed_bookings()
        
        query = Booking.query
        
        if upcoming_only:
            now = datetime.now(timezone.utc)
            query = query.filter(Booking.start_time >= now, Booking.status == BookingStatus.CONFIRMED)
        
        if status:
            query = query.filter(Booking.status == BookingStatus[status.upper()])
        
        if search:
            search_filter = f"%{search}%"
            query = query.join(ConferenceRoom).filter(
                or_(
                    ConferenceRoom.name.ilike(search_filter),
                    Booking.purpose.ilike(search_filter)
                )
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        if sort_by == "room_name":
            query = query.join(ConferenceRoom)
            column = ConferenceRoom.name
        elif hasattr(Booking, sort_by):
            column = getattr(Booking, sort_by)
        else:
            column = Booking.start_time
        
        query = query.order_by(column.desc() if order == "desc" else column.asc())
        
        # Apply pagination
        bookings = query.limit(limit).offset(offset).all()
        
        return bookings, total
    
    @staticmethod
    def cancel_booking(booking_id: int, user_id: int, is_admin: bool = False) -> tuple[bool, str]:
        """Cancel a booking"""
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return False, "Booking not found"
        
        if booking.status == BookingStatus.CANCELLED:
            return False, "Booking is already cancelled"
        
        now = datetime.now(timezone.utc)
        
        # Make booking.start_time timezone-aware if it's naive
        start_time = booking.start_time
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        
        # Check if booking is in the past
        if start_time < now:
            return False, "Cannot cancel past bookings"
        
        # Check ownership unless admin
        if not is_admin and booking.user_id != user_id:
            return False, "You can only cancel your own bookings"
        
        booking.status = BookingStatus.CANCELLED
        db.session.commit()
        
        return True, "Booking cancelled successfully"
    
    @staticmethod
    def get_room_availability(room_id: int, start_date: datetime, end_date: datetime):
        """Get booked slots for a room within a date range"""
        from sqlalchemy.orm import joinedload
        
        bookings = Booking.query.options(
            joinedload(Booking.room),
            joinedload(Booking.user)
        ).filter(
            and_(
                Booking.room_id == room_id,
                Booking.status == BookingStatus.CONFIRMED,
                Booking.start_time >= start_date,
                Booking.start_time < end_date
            )
        ).order_by(Booking.start_time).all()
        
        return [b.to_dict() for b in bookings]
