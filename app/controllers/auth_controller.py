

from flask import request
from app.services import AuthService
from typing import Tuple


class AuthController:
    
    @staticmethod
    def login() -> Tuple[dict, int]:
        # Validate request
        data = request.get_json()
        
        if not data:
            return {"error": "Request body is required"}, 400
        
        email = data.get("email", "").strip()
        password = data.get("password", "")
        
        # Validate fields
        if not email:
            return {"error": "Email is required"}, 400
        
        if not password:
            return {"error": "Password is required"}, 400
        
        # Call service layer
        success, response = AuthService.login_user(email, password)
        
        if not success:
            return response, 401
        
        return response, 200
    
    @staticmethod
    def refresh() -> Tuple[dict, int]:
        # Validate request
        data = request.get_json()
        
        if not data:
            return {"error": "Request body is required"}, 400
        
        refresh_token = data.get("refresh_token", "").strip()
        
        if not refresh_token:
            return {"error": "Refresh token is required"}, 400
        
        # Call service layer
        success, response = AuthService.refresh_access_token(refresh_token)
        
        if not success:
            return response, 401
        
        return response, 200
