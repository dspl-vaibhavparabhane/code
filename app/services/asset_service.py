from app.models import db, Asset, AssetAssignment, Employee, User, AssetStatus, AssignmentStatus, EmployeeStatus
from typing import Tuple, Dict, Any, List
from sqlalchemy.orm import joinedload
from datetime import datetime


def create_asset(data: dict, created_by_user_id: int) -> Tuple[bool, Dict[str, Any]]:
    """Create a new asset"""
    
    if not data.get("asset_code"):
        return False, {"error": "Asset code is required"}
    
    if not data.get("asset_name"):
        return False, {"error": "Asset name is required"}
    
    # Check if asset_code already exists
    if Asset.query.filter_by(asset_code=data["asset_code"]).first():
        return False, {"error": "Asset code already exists"}
    
    asset = Asset(
        asset_code=data["asset_code"],
        asset_name=data["asset_name"],
        asset_type=data.get("asset_type"),
        status=AssetStatus.AVAILABLE,
        created_by=created_by_user_id
    )
    
    db.session.add(asset)
    db.session.commit()
    
    return True, {
        "message": "Asset created successfully",
        "asset": asset.to_dict()
    }


def assign_asset(asset_id: int, employee_id: int, assigned_by_user_id: int) -> Tuple[bool, Dict[str, Any]]:
    """Assign an asset to an employee"""
    
    asset = Asset.query.filter_by(id=asset_id).first()
    if not asset:
        return False, {"error": "Asset not found"}
    
    if asset.status != AssetStatus.AVAILABLE:
        return False, {"error": "Asset is not available for assignment"}
    
    employee = Employee.query.filter_by(id=employee_id).first()
    if not employee:
        return False, {"error": "Employee not found"}
    
    if employee.status != EmployeeStatus.ACTIVE:
        return False, {"error": "Employee is not active"}
    
    # Check for existing active assignment
    active_assignment = AssetAssignment.query.filter_by(
        asset_id=asset_id,
        status=AssignmentStatus.ASSIGNED
    ).first()
    
    if active_assignment:
        return False, {"error": "Asset already has an active assignment"}
    
    try:
        # Create assignment
        assignment = AssetAssignment(
            asset_id=asset_id,
            employee_id=employee_id,
            assigned_by=assigned_by_user_id,
            assigned_at=datetime.utcnow(),
            status=AssignmentStatus.ASSIGNED
        )
        
        # Update asset status
        asset.status = AssetStatus.ASSIGNED
        
        db.session.add(assignment)
        db.session.commit()
        
        return True, {
            "message": "Asset assigned successfully",
            "assignment": assignment.to_dict()
        }
    except Exception as e:
        db.session.rollback()
        return False, {"error": "Failed to assign asset"}


def unassign_asset(asset_id: int, returned_by_user_id: int) -> Tuple[bool, Dict[str, Any]]:
    """Unassign (return) an asset"""
    
    asset = Asset.query.filter_by(id=asset_id).first()
    if not asset:
        return False, {"error": "Asset not found"}
    
    # Find active assignment
    active_assignment = AssetAssignment.query.filter_by(
        asset_id=asset_id,
        status=AssignmentStatus.ASSIGNED
    ).first()
    
    if not active_assignment:
        return False, {"error": "No active assignment found for this asset"}
    
    try:
        # Update assignment
        active_assignment.returned_by = returned_by_user_id
        active_assignment.returned_at = datetime.utcnow()
        active_assignment.status = AssignmentStatus.RETURNED
        
        # Update asset status
        asset.status = AssetStatus.AVAILABLE
        
        db.session.commit()
        
        return True, {
            "message": "Asset unassigned successfully",
            "assignment": active_assignment.to_dict()
        }
    except Exception as e:
        db.session.rollback()
        return False, {"error": "Failed to unassign asset"}


def update_asset(asset_id: int, data: dict) -> Tuple[bool, Dict[str, Any]]:
    """Update an asset"""
    
    asset = Asset.query.filter_by(id=asset_id).first()
    if not asset:
        return False, {"error": "Asset not found"}
    
    # Check if trying to change status from assigned to available/maintenance
    if data.get("status") and asset.status == AssetStatus.ASSIGNED:
        new_status = data["status"]
        if new_status in ["available", "maintenance"]:
            return False, {"error": "Cannot change status of assigned asset. Please unassign first"}
    
    # Check if asset_code is being changed and if it already exists
    if data.get("asset_code") and data["asset_code"] != asset.asset_code:
        existing = Asset.query.filter_by(asset_code=data["asset_code"]).first()
        if existing:
            return False, {"error": "Asset code already exists"}
        asset.asset_code = data["asset_code"]
    
    if data.get("asset_name"):
        asset.asset_name = data["asset_name"]
    
    if "asset_type" in data:
        asset.asset_type = data["asset_type"]
    
    if data.get("status"):
        try:
            asset.status = AssetStatus(data["status"])
        except ValueError:
            return False, {"error": "Invalid status"}
    
    db.session.commit()
    
    return True, {
        "message": "Asset updated successfully",
        "asset": asset.to_dict()
    }


def delete_asset(asset_id: int) -> Tuple[bool, Dict[str, Any]]:
    """Delete an asset"""
    
    asset = Asset.query.filter_by(id=asset_id).first()
    if not asset:
        return False, {"error": "Asset not found"}
    
    # Check if asset is assigned
    if asset.status == AssetStatus.ASSIGNED:
        return False, {"error": "Cannot delete assigned asset"}
    
    try:
        # Delete all assignment history for this asset first
        AssetAssignment.query.filter_by(asset_id=asset_id).delete()
        
        # Delete the asset
        db.session.delete(asset)
        db.session.commit()
        
        return True, {"message": "Asset deleted successfully"}
    except Exception as e:
        db.session.rollback()
        return False, {"error": str(e)}


def get_employee_assets(employee_id: int) -> Tuple[bool, Dict[str, Any]]:
    """Get currently assigned assets for an employee"""
    
    employee = Employee.query.filter_by(id=employee_id).first()
    if not employee:
        return False, {"error": "Employee not found"}
    
    # Get active assignments with asset details
    assignments = AssetAssignment.query.options(
        joinedload(AssetAssignment.asset)
    ).filter_by(
        employee_id=employee_id,
        status=AssignmentStatus.ASSIGNED
    ).all()
    
    assets = []
    for assignment in assignments:
        asset_data = assignment.asset.to_dict()
        asset_data["assigned_at"] = assignment.assigned_at.isoformat()
        asset_data["assigned_by"] = assignment.assigned_by
        assets.append(asset_data)
    
    return True, {
        "employee_id": employee_id,
        "assets": assets
    }


def get_all_assets(filters: dict = None) -> Tuple[List[Asset], int]:
    """Get all assets with optional filters, search, pagination, and sorting"""
    query = Asset.query.options(
        joinedload(Asset.assignments).joinedload(AssetAssignment.employee).joinedload(Employee.user),
        joinedload(Asset.assignments).joinedload(AssetAssignment.assigner)
    )
    
    if filters:
        # Status filter
        if filters.get("status"):
            try:
                status = AssetStatus(filters["status"])
                query = query.filter_by(status=status)
            except ValueError:
                pass
        
        # Search filter
        if filters.get("search"):
            search_term = f"%{filters['search']}%"
            query = query.filter(
                db.or_(
                    Asset.asset_code.ilike(search_term),
                    Asset.asset_name.ilike(search_term),
                    Asset.asset_type.ilike(search_term)
                )
            )
    
    # Get total count before pagination
    total_count = query.count()
    
    # Sorting
    sort_by = filters.get("sort_by", "created_at") if filters else "created_at"
    order = filters.get("order", "desc") if filters else "desc"
    
    sort_column = getattr(Asset, sort_by, Asset.created_at)
    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    # Pagination
    offset = filters.get("offset", 0) if filters else 0
    limit = filters.get("limit", 10) if filters else 10
    
    assets = query.offset(offset).limit(limit).all()
    
    return assets, total_count
