from flask import request, jsonify
from app.services.conference_room_service import ConferenceRoomService
from app.models import User, UserRole


class ConferenceRoomController:
    
    @staticmethod
    def create_room(current_user_email: str):
        """Create a new conference room (HR/Admin only)"""
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user or user.role not in [UserRole.HR, UserRole.ADMIN]:
            return jsonify({"error": "Access denied. HR or Admin role required"}), 403
        
        data = request.get_json()
        
        required_fields = ["name", "capacity"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        
        room, message = ConferenceRoomService.create_room(
            name=data["name"],
            capacity=data["capacity"],
            location=data.get("location")
        )
        
        if not room:
            return jsonify({"error": message}), 400
        
        return jsonify({
            "message": message,
            "room": room.to_dict()
        }), 201
    
    @staticmethod
    def get_all_rooms():
        """Get all conference rooms"""
        is_active = request.args.get("is_active")
        search = request.args.get("search", "")
        sort_by = request.args.get("sort_by", "created_at")
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
        
        rooms, total = ConferenceRoomService.get_all_rooms(is_active, search, sort_by, order, limit, offset)
        
        return jsonify({
            "data": [r.to_dict() for r in rooms],
            "total": total,
            "limit": limit,
            "offset": offset
        }), 200
    
    @staticmethod
    def get_room(room_id):
        """Get a specific conference room"""
        room = ConferenceRoomService.get_room(room_id)
        
        if not room:
            return jsonify({"error": "Conference room not found"}), 404
        
        return jsonify({"room": room.to_dict()}), 200
    
    @staticmethod
    def update_room(room_id, current_user_email: str):
        """Update a conference room (HR/Admin only)"""
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user or user.role not in [UserRole.HR, UserRole.ADMIN]:
            return jsonify({"error": "Access denied. HR or Admin role required"}), 403
        
        data = request.get_json()
        
        room, message = ConferenceRoomService.update_room(
            room_id=room_id,
            name=data.get("name"),
            capacity=data.get("capacity"),
            location=data.get("location"),
            is_active=data.get("is_active")
        )
        
        if not room:
            return jsonify({"error": message}), 400
        
        return jsonify({
            "message": message,
            "room": room.to_dict()
        }), 200
    
    @staticmethod
    def delete_room(room_id, current_user_email: str):
        """Delete (deactivate) a conference room (HR/Admin only)"""
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user or user.role not in [UserRole.HR, UserRole.ADMIN]:
            return jsonify({"error": "Access denied. HR or Admin role required"}), 403
        
        success, message = ConferenceRoomService.delete_room(room_id)
        
        if not success:
            return jsonify({"error": message}), 404
        
        return jsonify({"message": message}), 200
