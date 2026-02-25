from datetime import datetime
from sqlalchemy import String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import db
import enum


class AssetStatus(str, enum.Enum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    MAINTENANCE = "maintenance"


class Asset(db.Model):
    __tablename__ = "assets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    asset_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    asset_name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(100), nullable=True)
    status: Mapped[AssetStatus] = mapped_column(
        Enum(AssetStatus),
        nullable=False,
        default=AssetStatus.AVAILABLE
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    assignments: Mapped[list["AssetAssignment"]] = relationship("AssetAssignment", back_populates="asset")
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    
    def to_dict(self) -> dict:
        from app.models import AssignmentStatus
        # Get active assignment if exists
        active_assignment = next(
            (a for a in self.assignments if a.status == AssignmentStatus.ASSIGNED),
            None
        )
        
        result = {
            "id": self.id,
            "asset_code": self.asset_code,
            "asset_name": self.asset_name,
            "asset_type": self.asset_type,
            "status": self.status.value,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        
        if active_assignment:
            result["assigned_to"] = active_assignment.employee.user.name if active_assignment.employee.user.name else active_assignment.employee.user.email
            result["assigned_by"] = active_assignment.assigner.name if active_assignment.assigner.name else active_assignment.assigner.email
        else:
            result["assigned_to"] = None
            result["assigned_by"] = None
        
        return result
