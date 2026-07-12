from datetime import datetime, date
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    asset_tag: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    serial_number: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)
    
    # Status can be: Available, Allocated, Under Maintenance, Retired
    status: Mapped[str] = mapped_column(String(30), default="Available", nullable=False)
    
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("asset_categories.id"), nullable=False)
    department_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("departments.id"), nullable=True)
    
    purchase_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships to existing models
    category = relationship("AssetCategory", foreign_keys=[category_id])
    department = relationship("Department", foreign_keys=[department_id])