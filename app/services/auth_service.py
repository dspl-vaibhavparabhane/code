
from app.models import db, User, UserRole
from app.utils.password_utils import  verify_password
from app.utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from typing import Tuple, Dict, Any


class AuthService:
    
    @staticmethod
    def login_user(email: str, password: str) -> Tuple[bool, Dict[str, Any]]:

        # Find user by email with employee relationship
        from sqlalchemy.orm import joinedload
        user = User.query.options(joinedload(User.employee)).filter_by(email=email).first()
        
        if not user:
            return False, {"error": "Invalid email or password. Please try again."}
        
        # Verify password
        if not verify_password(user.password, password):
            return False, {"error": "Invalid email or password. Please try again."}
        
        # Auto-assign EMPLOYEE role to legacy users with NULL role
        if user.role is None:
            user.role = UserRole.EMPLOYEE
            db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(
            user_id=user.id,
            user_email=user.email,
            user_role=user.role.value if user.role else None
        )
        refresh_token = create_refresh_token(user_id=user.id)
        
        return True, {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Tuple[bool, Dict[str, Any]]:

        # Verify refresh token
        is_valid, payload = verify_token(refresh_token)
        
        if not is_valid or payload.get("type") != "refresh":
            return False, {"error": "Invalid refresh token"}
        
        # Get user
        user_id = payload.get("user_id")
        user = User.query.get(user_id)
        
        if not user:
            return False, {"error": "User not found"}
        
        # Generate new access token
        access_token = create_access_token(
            user_id=user.id,
            user_email=user.email,
            user_role=user.role.value if user.role else None
        )
        
        return True, {
            "message": "Token refreshed successfully",
            "access_token": access_token,
        }
    
    @staticmethod
    def get_user_by_id(user_id: int) -> User:

        return User.query.get(user_id)
