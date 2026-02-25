from flask import request
from app.services import asset_service
from app.models import User, UserRole
from typing import Tuple


class AssetController:
    
    @staticmethod
    def create_asset(current_user_email: str) -> Tuple[dict, int]:
        """Create a new asset (Admin/HR only)"""
        
        data = request.get_json()
        if not data:
            return {"error": "Request body is required"}, 400
        
        # Get current user
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        # RBAC: Only Admin and HR can create assets
        if current_user.role not in [UserRole.ADMIN, UserRole.HR]:
            return {"error": "Access denied. Admin or HR role required"}, 403
        
        success, response = asset_service.create_asset(data, current_user.id)
        
        if not success:
            return response, 400
        
        return response, 201
    
    @staticmethod
    def assign_asset(asset_id: int, current_user_email: str) -> Tuple[dict, int]:
        """Assign an asset to an employee (Admin/HR only)"""
        
        data = request.get_json()
        if not data:
            return {"error": "Request body is required"}, 400
        
        employee_id = data.get("employee_id")
        if not employee_id:
            return {"error": "employee_id is required"}, 400
        
        # Get current user
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        # RBAC: Only Admin and HR can assign assets
        if current_user.role not in [UserRole.ADMIN, UserRole.HR]:
            return {"error": "Access denied. Admin or HR role required"}, 403
        
        success, response = asset_service.assign_asset(asset_id, employee_id, current_user.id)
        
        if not success:
            return response, 400
        
        return response, 200
    
    @staticmethod
    def unassign_asset(asset_id: int, current_user_email: str) -> Tuple[dict, int]:
        """Unassign (return) an asset (Admin/HR only)"""
        
        # Get current user
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        # RBAC: Only Admin and HR can unassign assets
        if current_user.role not in [UserRole.ADMIN, UserRole.HR]:
            return {"error": "Access denied. Admin or HR role required"}, 403
        
        success, response = asset_service.unassign_asset(asset_id, current_user.id)
        
        if not success:
            return response, 400
        
        return response, 200
    
    @staticmethod
    def get_employee_assets(employee_id: int, current_user_email: str) -> Tuple[dict, int]:
        """Get assets assigned to an employee"""
        
        # Get current user
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        # RBAC: Employee can only view their own assets, HR/Admin can view any
        if current_user.role == UserRole.EMPLOYEE:
            if not current_user.employee or current_user.employee.id != employee_id:
                return {"error": "Access denied. You can only view your own assets"}, 403
        
        success, response = asset_service.get_employee_assets(employee_id)
        
        if not success:
            return response, 404
        
        return response, 200
    
    @staticmethod
    def get_all_assets(current_user_email: str) -> Tuple[dict, int]:
        """Get all assets (Admin/HR only)"""
        
        # Get current user
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        # RBAC: Only Admin and HR can view all assets
        if current_user.role not in [UserRole.ADMIN, UserRole.HR]:
            return {"error": "Access denied. Admin or HR role required"}, 403
        
        filters = {}
        if request.args.get("status"):
            filters["status"] = request.args.get("status")
        if request.args.get("search"):
            filters["search"] = request.args.get("search")
        
        # Pagination
        try:
            offset = int(request.args.get("offset", 0))
            limit = int(request.args.get("limit", 10))
            limit = min(limit, 100)
        except ValueError:
            offset = 0
            limit = 10
        
        filters["offset"] = offset
        filters["limit"] = limit
        
        # Sorting
        filters["sort_by"] = request.args.get("sort_by", "created_at")
        filters["order"] = request.args.get("order", "desc")
        
        assets, total = asset_service.get_all_assets(filters)
        
        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "assets": [asset.to_dict() for asset in assets]
        }, 200
    
    @staticmethod
    def update_asset(asset_id: int, current_user_email: str) -> Tuple[dict, int]:
        """Update an asset (Admin/HR only)"""
        
        data = request.get_json()
        if not data:
            return {"error": "Request body is required"}, 400
        
        # Get current user
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        # RBAC: Only Admin and HR can update assets
        if current_user.role not in [UserRole.ADMIN, UserRole.HR]:
            return {"error": "Access denied. Admin or HR role required"}, 403
        
        success, response = asset_service.update_asset(asset_id, data)
        
        if not success:
            return response, 400
        
        return response, 200
    
    @staticmethod
    def delete_asset(asset_id: int, current_user_email: str) -> Tuple[dict, int]:
        """Delete an asset (Admin/HR only)"""
        
        # Get current user
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return {"error": "User not found"}, 404
        
        # RBAC: Only Admin and HR can delete assets
        if current_user.role not in [UserRole.ADMIN, UserRole.HR]:
            return {"error": "Access denied. Admin or HR role required"}, 403
        
        success, response = asset_service.delete_asset(asset_id)
        
        if not success:
            return response, 400
        
        return response, 200
