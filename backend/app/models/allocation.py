from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Allocation(Base):
    __tablename__ = "allocations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("assets.id"), nullable=False)
    
    # Employee who currently holds the asset
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Manager/Admin who allocated the asset
    allocated_by_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    
    allocated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Status: Active, Returned, Transfer Pending
    status: Mapped[str] = mapped_column(String(30), default="Active", nullable=False)

    # Fields for transfer request workflow
    transfer_to_employee_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    asset = relationship("Asset", foreign_keys=[asset_id])
    employee = relationship("User", foreign_keys=[employee_id])
    allocated_by = relationship("User", foreign_keys=[allocated_by_id])
    transfer_to = relationship("User", foreign_keys=[transfer_to_employee_id])