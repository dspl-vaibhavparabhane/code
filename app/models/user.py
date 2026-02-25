

from datetime import datetime
from sqlalchemy import String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import db
import enum


class UserRole(str, enum.Enum):
    EMPLOYEE = "Employee"
    HR = "HR"
    ADMIN = "Admin"


class User(db.Model):

    __tablename__ = "users"
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Authentication fields
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Profile fields
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole | None] = mapped_column(
        Enum(UserRole),
        nullable=True,
        default=None
    )
    
    # Timestamp fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationship to Employee (one-to-one)
    employee: Mapped["Employee"] = relationship("Employee", back_populates="user", uselist=False)
    # Relationship to Bookings (one-to-many)
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user")
    def to_dict(self) -> dict:
        """Convert user instance to dictionary with employee data"""
        result = {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value if self.role else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        
        # Add employee data if exists
        if self.employee:
            result["employee"] = {"id": self.employee.id}
            result["join_date"] = self.employee.join_date.isoformat() if self.employee.join_date else None
            result["separation_date"] = self.employee.separation_date.isoformat() if self.employee.separation_date else None
            result["status"] = self.employee.status.value if self.employee.status else None
        else:
            result["employee"] = None
            result["join_date"] = None
            result["separation_date"] = None
            result["status"] = None
        
        return result
