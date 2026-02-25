
from functools import wraps
from flask import current_app, request
from flask_jwt_extended import (
    create_access_token as fje_create_access_token,
    create_refresh_token as fje_create_refresh_token,
    jwt_required,
    get_jwt,
    decode_token,
)
from typing import Callable, Tuple, Dict, Any
from app.models import db, User, UserRole



def create_access_token(user_id: int, user_email: str, user_role: str = None) -> str:

    additional_claims = {
        "user_id": user_id,
        "email": user_email,
        "type": "access",
    }
    
    token = fje_create_access_token(
        identity=user_id,
        additional_claims=additional_claims,
        expires_delta=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES")
    )
    
    return token


def create_refresh_token(user_id: int) -> str:

    additional_claims = {
        "type": "refresh",
    }
    
    token = fje_create_refresh_token(
        identity=user_id,
        additional_claims=additional_claims,
        expires_delta=current_app.config.get("JWT_REFRESH_TOKEN_EXPIRES")
    )
    
    return token


def verify_token(token: str) -> Tuple[bool, Dict[str, Any]]:

    try:
        payload = decode_token(token)
        # Flatten the payload structure for backward compatibility
        # Flask-JWT-Extended stores identity as 'sub'
        flattened_payload = {
            "user_id": payload.get("sub"),  # extract identity
            "type": payload.get("type"),
            "email": payload.get("email"),
        }
        return True, flattened_payload
    except Exception:
        return False, {"error": "Invalid or expired token"}


def token_required(f: Callable) -> Callable:
    """
    Decorator to protect routes with JWT token validation.
    
    This decorator verifies the JWT token in the Authorization header
    and extracts user information into request context for backward compatibility.
    
    """
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        # Get JWT claims
        claims = get_jwt()
        
        # Store user info in request context (role will be fetched from DB when needed)
        request.user = {
            "user_id": claims.get("sub"),  # 'sub' is the identity (user_id)
            "email": claims.get("email"),
            "type": claims.get("type"),
        }
        
        return f(*args, **kwargs)
    
    return decorated


def role_required(required_role: str) -> Callable:
#     Decorator to enforce role-based access control.

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            # Ensure token_required is applied first
            if not hasattr(request, "user"):
                return {"error": "Authentication required"}, 401
            
            # Get email from token payload
            user_email = request.user.get("email")
            if not user_email:
                return {"error": "Invalid token payload"}, 401
            
            # Fetch user from DB to get current role
            user = User.query.filter_by(email=user_email).first()
            if not user:
                return {"error": "User not found"}, 404

            # Get role from DB (not from token)
            user_role = user.role.value if hasattr(user.role, "value") else user.role

            if user_role != required_role:
                return {"error": f"Access denied. {required_role} role required"}, 403
            
            return f(*args, **kwargs)
        
        return decorated
    
    return decorator
