from app.models import db, ConferenceRoom, Booking


class ConferenceRoomService:
    
    @staticmethod
    def create_room(name: str, capacity: int, location: str) -> tuple[ConferenceRoom | None, str]:
        """Create a new conference room"""
        existing = ConferenceRoom.query.filter_by(name=name).first()
        if existing:
            return None, "Conference room with this name already exists"
        
        room = ConferenceRoom(name=name, capacity=capacity, location=location)
        db.session.add(room)
        db.session.commit()
        
        return room, "Conference room created successfully"
    
    @staticmethod
    def get_all_rooms(is_active: str = None, search: str = "", sort_by: str = "created_at", order: str = "desc", limit: int = 10, offset: int = 0):
        """Get all conference rooms with filtering, sorting and pagination"""
        query = ConferenceRoom.query
        
        if is_active is not None and is_active != "":
            query = query.filter(ConferenceRoom.is_active == (is_active.lower() == "true"))
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (ConferenceRoom.name.ilike(search_filter)) |
                (ConferenceRoom.location.ilike(search_filter))
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Map frontend field names to backend column names
        if sort_by == "room_name":
            sort_by = "name"
        
        # Apply sorting
        if hasattr(ConferenceRoom, sort_by):
            column = getattr(ConferenceRoom, sort_by)
            query = query.order_by(column.desc() if order == "desc" else column.asc())
        
        # Apply pagination
        rooms = query.limit(limit).offset(offset).all()
        
        return rooms, total
    
    @staticmethod
    def get_room(room_id: int) -> ConferenceRoom | None:
        """Get a specific conference room"""
        return ConferenceRoom.query.get(room_id)
    
    @staticmethod
    def update_room(room_id: int, name: str = None, capacity: int = None, location: str = None, is_active: bool = None) -> tuple[ConferenceRoom | None, str]:
        """Update conference room details"""
        from datetime import datetime, timezone
        from app.models.booking import BookingStatus
        
        room = ConferenceRoom.query.get(room_id)
        if not room:
            return None, "Conference room not found"
        
        # Check if trying to deactivate room with active/upcoming bookings
        if is_active is False and room.is_active is True:
            upcoming_bookings = Booking.query.filter(
                Booking.room_id == room_id,
                Booking.end_time > datetime.now(timezone.utc),
                Booking.status == BookingStatus.CONFIRMED
            ).count()
            
            if upcoming_bookings > 0:
                return None, f"Cannot deactivate room. There are {upcoming_bookings} active/upcoming booking(s) for this room"
        
        if name and name != room.name:
            existing = ConferenceRoom.query.filter_by(name=name).first()
            if existing:
                return None, "Conference room with this name already exists"
            room.name = name
        
        if capacity is not None:
            room.capacity = capacity
        if location:
            room.location = location
        if is_active is not None:
            room.is_active = is_active
        
        db.session.commit()
        return room, "Conference room updated successfully"
    
    @staticmethod
    def delete_room(room_id: int) -> tuple[bool, str]:
        """Permanently delete a conference room"""
        room = ConferenceRoom.query.get(room_id)
        if not room:
            return False, "Conference room not found"
        
        # Delete all bookings for this room first
        Booking.query.filter_by(room_id=room_id).delete()
        
        db.session.delete(room)
        db.session.commit()
        return True, "Conference room deleted successfully"