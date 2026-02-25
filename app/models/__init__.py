"""
Models Package ->Exports all database models and database instance.
"""

from .db import db
from .user import User, UserRole
from .employee import Employee, EmployeeStatus
from .asset import Asset, AssetStatus
from .asset_assignment import AssetAssignment, AssignmentStatus
from .conference_room import ConferenceRoom
from .booking import Booking, BookingStatus

__all__ = ["db", "User", "UserRole", "Employee", "EmployeeStatus", "Asset", "AssetStatus", "AssetAssignment", "AssignmentStatus", "ConferenceRoom", "Booking", "BookingStatus"]
