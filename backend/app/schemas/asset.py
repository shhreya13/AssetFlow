from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class AssetBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    serial_number: Optional[str] = Field(None, max_length=100)
    category_id: int
    department_id: Optional[int] = None
    purchase_date: Optional[date] = None
    cost: Optional[float] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Asset name cannot be empty")
        return v

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    serial_number: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, description="Available, Allocated, Under Maintenance, Retired")
    category_id: Optional[int] = None
    department_id: Optional[int] = None
    purchase_date: Optional[date] = None
    cost: Optional[float] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=255)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            valid_statuses = ["Available", "Allocated", "Under Maintenance", "Retired"]
            v = v.strip().title()
            if v not in valid_statuses:
                raise ValueError(f"Status must be one of {valid_statuses}")
        return v

class AssetOut(AssetBase):
    id: int
    asset_tag: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True