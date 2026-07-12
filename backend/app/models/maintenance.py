from datetime import datetime
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Maintenance(Base):
    __tablename__ = "maintenance_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("assets.id"), nullable=False)
    
    reported_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    technician_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    
    issue_description: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Status Workflow: Pending, Approved, Technician Assigned, In Progress, Resolved
    status: Mapped[str] = mapped_column(String(30), default="Pending", nullable=False)
    
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    resolution_notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    asset = relationship("Asset", foreign_keys=[asset_id])
    reported_by = relationship("User", foreign_keys=[reported_by_id])
    technician = relationship("User", foreign_keys=[technician_id])