"""
Routes module

Exports all route blueprints.
"""

from .auth import auth_bp
from .user_routes import user_bp
from .asset import asset_bp
from .conference_room_routes import conference_room_bp
from .booking_routes import booking_bp

__all__ = ["auth_bp", "user_bp", "asset_bp", "conference_room_bp", "booking_bp"]
