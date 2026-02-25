

from app.models import db, User, UserRole, Employee, EmployeeStatus
from typing import Tuple, Dict, Any, List
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from datetime import datetime, date


def create_user(data: dict, current_user_role: UserRole) -> Tuple[bool, Dict[str, Any]]:

    # Validate role permissions
    target_role = data.get("role", "Employee")
    
    if current_user_role == UserRole.HR:
        if target_role != "Employee":
            return False, {"error": "HR can only create Employee users"}
    elif current_user_role != UserRole.ADMIN:
        return False, {"error": "Insufficient permissions"}
    
    # Check if email exists
    if User.query.filter_by(email=data.get("email")).first():
        return False, {"error": "Email already exists"}
    
    # Create user
    user = User(
        email=data["email"],
        password=data["password"],  
        name=data.get("name"),
        role=UserRole(target_role)
    )
    db.session.add(user)
    db.session.flush()  # Get user.id
    
    # Create employee record if join_date provided
    if data.get("join_date"):
        try:
            employee = Employee(
                user_id=user.id,
                join_date=datetime.fromisoformat(data["join_date"]).date(),
                separation_date=datetime.fromisoformat(data["separation_date"]).date() if data.get("separation_date") else None,
                status=EmployeeStatus(data.get("status", "active"))
            )
            db.session.add(employee)
        except (ValueError, AttributeError) as e:
            db.session.rollback()
            return False, {"error": "Invalid date format or status"}
    
    db.session.commit()
    
    # Reload with employee data
    user = User.query.options(joinedload(User.employee)).filter_by(id=user.id).first()
    
    return True, {
        "message": "User created successfully",
        "user": user.to_dict()
    }


def get_users_with_filters(
    allowed_roles: List[UserRole],
    role_filter: str = None,
    status_filter: str = None,
    name_filter: str = None,
    email_filter: str = None,
    offset: int = 0,
    limit: int = 10,
    sort_by: str = "created_at",
    order: str = "desc"
) -> Tuple[List[User], int]:

    # Base query - filter by allowed roles with joined employee data
    query = User.query.options(joinedload(User.employee)).filter(User.role.in_(allowed_roles))
    
    # Apply role filter if specified
    if role_filter:
        try:
            role_enum = UserRole(role_filter)
            if role_enum in allowed_roles:
                query = query.filter(User.role == role_enum)
        except ValueError:
            pass  # Invalid role, ignore filter
    
    # Apply status filter if specified
    if status_filter:
        try:
            status_enum = EmployeeStatus(status_filter)
            query = query.join(Employee, User.id == Employee.user_id, isouter=True)
            query = query.filter(Employee.status == status_enum)
        except ValueError:
            pass  # Invalid status, ignore filter
    
    # Apply name filter (partial match, case-insensitive)
    if name_filter:
        query = query.filter(User.name.ilike(f"%{name_filter}%"))
    
    # Apply email filter (partial match, case-insensitive)
    if email_filter:
        query = query.filter(User.email.ilike(f"%{email_filter}%"))
    
    # Get total count before pagination
    total_count = query.count()
    
    # Apply sorting
    sort_column = getattr(User, sort_by, User.created_at)
    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    # Apply pagination
    users = query.offset(offset).limit(limit).all()
    
    return users, total_count


def get_user_by_id(user_id: int) -> User:

    return User.query.options(joinedload(User.employee)).filter_by(id=user_id).first()


def update_user(user_id: int, data: dict, current_user_role: UserRole) -> Tuple[bool, Dict[str, Any]]:

    user = User.query.options(joinedload(User.employee)).filter_by(id=user_id).first()
    
    if not user:
        return False, {"error": "User not found"}
    
    # Define allowed fields based on role
    if current_user_role == UserRole.ADMIN:
        allowed_user_fields = ["name", "email", "role"]
        allowed_employee_fields = ["join_date", "separation_date", "status"]
    elif current_user_role == UserRole.HR:
        if user.role != UserRole.EMPLOYEE:
            return False, {"error": "HR can only edit Employee users"}
        allowed_user_fields = ["name", "email"]
        allowed_employee_fields = ["join_date", "separation_date", "status"]
    else:
        return False, {"error": "Insufficient permissions"}
    
    # Update User fields
    if "name" in data and "name" in allowed_user_fields:
        user.name = data["name"].strip() or None
    
    if "email" in data and "email" in allowed_user_fields:
        email = data["email"].strip()
        existing = User.query.filter(User.email == email, User.id != user_id).first()
        if existing:
            return False, {"error": "Email already exists"}
        user.email = email
    
    if "role" in data and "role" in allowed_user_fields:
        try:
            user.role = UserRole(data["role"])
        except ValueError:
            return False, {"error": "Invalid role"}
    
    # Update Employee fields
    employee_updated = False
    if "join_date" in data and "join_date" in allowed_employee_fields:
        if not user.employee:
            user.employee = Employee(user_id=user.id, join_date=date.today(), status=EmployeeStatus.ACTIVE)
        try:
            user.employee.join_date = datetime.fromisoformat(data["join_date"]).date()
            employee_updated = True
        except (ValueError, AttributeError):
            return False, {"error": "Invalid join_date format"}
    
    if "separation_date" in data and "separation_date" in allowed_employee_fields:
        if user.employee:
            if data["separation_date"]:
                try:
                    user.employee.separation_date = datetime.fromisoformat(data["separation_date"]).date()
                    employee_updated = True
                except (ValueError, AttributeError):
                    return False, {"error": "Invalid separation_date format"}
            else:
                user.employee.separation_date = None
                employee_updated = True
    
    if "status" in data and "status" in allowed_employee_fields:
        if user.employee:
            try:
                user.employee.status = EmployeeStatus(data["status"])
                employee_updated = True
            except ValueError:
                return False, {"error": "Invalid status"}
    
    db.session.commit()
    
    return True, {
        "message": "User updated successfully",
        "user": user.to_dict()
    }


def delete_user(user_id: int) -> Tuple[bool, Dict[str, Any]]:

    user = User.query.options(joinedload(User.employee)).filter_by(id=user_id).first()
    
    if not user:
        return False, {"error": "User not found"}
    
    # Delete employee record if exists (cascade should handle this, but explicit is better)
    if user.employee:
        db.session.delete(user.employee)
    
    db.session.delete(user)
    db.session.commit()
    
    return True, {"message": "User deleted successfully"}
