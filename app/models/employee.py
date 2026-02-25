
# Defines the Employee SQLAlchemy model with one-to-one relationship to User.


from datetime import datetime, date
from sqlalchemy import String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import db
import enum


class EmployeeStatus(str, enum.Enum):
    ACTIVE = "active"
    SEPARATED = "separated"


class Employee(db.Model):

    
    __tablename__ = "employees"
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Foreign Key to User (one-to-one)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    
    # Employee fields
    join_date: Mapped[date] = mapped_column(Date, nullable=False)
    separation_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[EmployeeStatus] = mapped_column(
        Enum(EmployeeStatus),
        nullable=False,
        default=EmployeeStatus.ACTIVE
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
    
    # Relationship to User
    user: Mapped["User"] = relationship("User", back_populates="employee")
    
    # Relationship to AssetAssignments
    assignments: Mapped[list["AssetAssignment"]] = relationship("AssetAssignment", back_populates="employee")
    
    def to_dict(self) -> dict:
        """Convert employee instance to dictionary"""
        return {
            "join_date": self.join_date.isoformat() if self.join_date else None,
            "separation_date": self.separation_date.isoformat() if self.separation_date else None,
            "status": self.status.value if self.status else None,
        }
