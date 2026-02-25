
from flask import request
from app.services import user_service
from app.models import User, UserRole
from typing import Tuple


class UserController:
    
    @staticmethod
    def create_user(current_user_email: str) -> Tuple[dict, int]:

        data = request.get_json()
        
        if not data:
            return {"error": "Request body is required"}, 400
        
        # Validate required fields
        if not data.get("email"):
            return {"error": "Email is required"}, 400
        
        if not data.get("password"):
            return {"error": "Password is required"}, 400
        
        # Fetch current user from DB to get role
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        # RBAC: Only Admin and HR can create
        if current_user.role not in [UserRole.ADMIN, UserRole.HR]:
            return {"error": "Access denied. Insufficient permissions"}, 403
        
        success, response = user_service.create_user(data, current_user.role)
        
        if not success:
            return response, 400
        
        return response, 201
    
    @staticmethod
    def get_users(current_user_email: str) -> Tuple[dict, int]:

        # Fetch current user from DB to get role
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        current_role = current_user.role
        
        # RBAC: Determine allowed roles based on current user role
        if current_role == UserRole.ADMIN:
            allowed_roles = [UserRole.EMPLOYEE, UserRole.HR, UserRole.ADMIN]
        elif current_role == UserRole.HR:
            allowed_roles = [UserRole.EMPLOYEE]
        else:
            # Employee cannot access this endpoint
            return {"error": "Access denied. Insufficient permissions"}, 403
        
        # Extract and validate query parameters
        role_filter = request.args.get("role")
        status_filter = request.args.get("status")
        name_filter = request.args.get("name")
        email_filter = request.args.get("email")
        
        # Pagination parameters
        try:
            offset = int(request.args.get("offset", 0))
            limit = int(request.args.get("limit", 10))
            # Enforce max limit
            limit = min(limit, 100)
            if offset < 0 or limit < 1:
                return {"error": "Invalid pagination parameters"}, 400
        except ValueError:
            return {"error": "Invalid pagination parameters"}, 400
        
        # Sorting parameters
        sort_by = request.args.get("sort_by", "created_at")
        order = request.args.get("order", "desc")
        
        # Validate sort_by field
        valid_sort_fields = ["name", "email", "created_at"]
        if sort_by not in valid_sort_fields:
            sort_by = "created_at"
        
        # Validate order
        if order not in ["asc", "desc"]:
            order = "desc"
        
        # Call service layer
        users, total_count = user_service.get_users_with_filters(
            allowed_roles=allowed_roles,
            role_filter=role_filter,
            status_filter=status_filter,
            name_filter=name_filter,
            email_filter=email_filter,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            order=order
        )
        
        return {
            "total": total_count,
            "offset": offset,
            "limit": limit,
            "users": [user.to_dict() for user in users]
        }, 200
    
    @staticmethod
    def get_user_by_id(user_id: int, current_user_email: str) -> Tuple[dict, int]:

        # Fetch current user from DB
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        # Employee can only view their own details
        if current_user.role == UserRole.EMPLOYEE and user_id != current_user.id:
            return {"error": "Access denied. You can only view your own details"}, 403
        
        user = user_service.get_user_by_id(user_id)
        
        if not user:
            return {"error": "User not found"}, 404
        
        return {"user": user.to_dict()}, 200
    
    @staticmethod
    def update_user(user_id: int, current_user_email: str) -> Tuple[dict, int]:

        data = request.get_json()
        
        if not data:
            return {"error": "Request body is required"}, 400
        
        # Fetch current user from DB to get role
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        current_role = current_user.role
        
        # RBAC: Only Admin and HR can update
        if current_role not in [UserRole.ADMIN, UserRole.HR]:
            return {"error": "Access denied. Insufficient permissions"}, 403
        
        # HR cannot change role
        if current_role == UserRole.HR and "role" in data:
            return {"error": "HR cannot change user role"}, 403
        
        success, response = user_service.update_user(user_id, data, current_role)
        
        if not success:
            return response, 400
        
        return response, 200
    
    @staticmethod
    def delete_user(user_id: int, current_user_email: str) -> Tuple[dict, int]:

        # Fetch current user from DB to get role
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        # RBAC: Only Admin can delete
        if current_user.role != UserRole.ADMIN:
            return {"error": "Access denied. Admin role required"}, 403
        
        success, response = user_service.delete_user(user_id)
        
        if not success:
            return response, 400
        
        return response, 200
