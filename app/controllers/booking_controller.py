from flask import request, jsonify
from datetime import datetime, timezone
from app.services.booking_service import BookingService
from app.models import User, UserRole


class BookingController:
    
    @staticmethod
    def create_booking(current_user_email: str):
        """Create a new booking (Employee, HR, Admin)"""
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["room_id", "start_time", "end_time", "purpose"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"{field} is required"}), 400
        
        try:
            start_time = datetime.fromisoformat(data["start_time"].replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(data["end_time"].replace("Z", "+00:00"))
            
            # Ensure timezone-aware datetimes
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=timezone.utc)
        except ValueError:
            return jsonify({"error": "Invalid datetime format. Use ISO 8601 format"}), 400
        
        user = User.query.filter_by(email=current_user_email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        booking, message = BookingService.create_booking(
            room_id=data["room_id"],
            user_id=user.id,
            start_time=start_time,
            end_time=end_time,
            purpose=data["purpose"]
        )
        
        if not booking:
            return jsonify({"error": message}), 400
        
        return jsonify({
            "message": message,
            "booking": booking.to_dict()
        }), 201
    
    @staticmethod
    def get_my_bookings(current_user_email: str):
        """Get current user's bookings"""
        user = User.query.filter_by(email=current_user_email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        upcoming_only = request.args.get("upcoming_only", "false").lower() == "true"
        status = request.args.get("status", "")
        search = request.args.get("search", "")
        sort_by = request.args.get("sort_by", "start_time")
        order = request.args.get("order", "desc")
        limit = request.args.get("limit", 10, type=int)
        offset = request.args.get("offset", 0, type=int)
        
        # Validate limit
        if limit < 1 or limit > 1000:
            return jsonify({"error": "Limit must be between 1 and 1000"}), 400
        
        # Validate offset
        if offset < 0:
            return jsonify({"error": "Offset must be non-negative"}), 400
        
        # Validate order
        if order not in ["asc", "desc"]:
            return jsonify({"error": "Order must be 'asc' or 'desc'"}), 400
        
        bookings, total = BookingService.get_user_bookings(user.id, upcoming_only, status, search, sort_by, order, limit, offset)
        
        return jsonify({
            "data": [b.to_dict() for b in bookings],
            "total": total,
            "limit": limit,
            "offset": offset
        }), 200
    
    @staticmethod
    def get_all_bookings(current_user_email: str):
        """Get all bookings (HR/Admin only)"""
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user or user.role not in [UserRole.HR, UserRole.ADMIN]:
            return jsonify({"error": "Access denied. HR or Admin role required"}), 403
        
        upcoming_only = request.args.get("upcoming_only", "false").lower() == "true"
        status = request.args.get("status", "")
        search = request.args.get("search", "")
        sort_by = request.args.get("sort_by", "start_time")
        order = request.args.get("order", "desc")
        limit = request.args.get("limit", 10, type=int)
        offset = request.args.get("offset", 0, type=int)
        
        # Validate limit
        if limit < 1 or limit > 1000:
            return jsonify({"error": "Limit must be between 1 and 1000"}), 400
        
        # Validate offset
        if offset < 0:
            return jsonify({"error": "Offset must be non-negative"}), 400
        
        # Validate order
        if order not in ["asc", "desc"]:
            return jsonify({"error": "Order must be 'asc' or 'desc'"}), 400
        
        bookings, total = BookingService.get_all_bookings(upcoming_only, status, search, sort_by, order, limit, offset)
        
        return jsonify({
            "data": [b.to_dict() for b in bookings],
            "total": total,
            "limit": limit,
            "offset": offset
        }), 200
    
    @staticmethod
    def cancel_booking(booking_id, current_user_email: str):
        """Cancel a booking"""
        user = User.query.filter_by(email=current_user_email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        is_admin = user.role in [UserRole.HR, UserRole.ADMIN]
        success, message = BookingService.cancel_booking(booking_id, user.id, is_admin)
        
        if not success:
            return jsonify({"error": message}), 400
        
        return jsonify({"message": message}), 200
    
    @staticmethod
    def get_room_availability():
        """Get room availability for a date range"""
        room_id = request.args.get("room_id", type=int)
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        
        if not room_id or not start_date or not end_date:
            return jsonify({"error": "room_id, start_date, and end_date are required"}), 400
        
        try:
            start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        except ValueError:
            return jsonify({"error": "Invalid datetime format. Use ISO 8601 format"}), 400
        
        booked_slots = BookingService.get_room_availability(room_id, start_dt, end_dt)
        
        return jsonify({
            "room_id": room_id,
            "start_date": start_date,
            "end_date": end_date,
            "booked_slots": booked_slots
        }), 200
