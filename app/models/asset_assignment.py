from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import db
import enum


class AssignmentStatus(str, enum.Enum):
    ASSIGNED = "assigned"
    RETURNED = "returned"


class AssetAssignment(db.Model):
    __tablename__ = "asset_assignments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    assigned_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    returned_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[AssignmentStatus] = mapped_column(
        Enum(AssignmentStatus),
        nullable=False,
        default=AssignmentStatus.ASSIGNED
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    asset: Mapped["Asset"] = relationship("Asset", back_populates="assignments")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="assignments")
    assigner: Mapped["User"] = relationship("User", foreign_keys=[assigned_by])
    returner: Mapped["User"] = relationship("User", foreign_keys=[returned_by])
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "asset_id": self.asset_id,
            "employee_id": self.employee_id,
            "assigned_by": self.assigned_by,
            "assigned_at": self.assigned_at.isoformat(),
            "returned_by": self.returned_by,
            "returned_at": self.returned_at.isoformat() if self.returned_at else None,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
