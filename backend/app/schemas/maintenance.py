from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class MaintenanceBase(BaseModel):
    asset_id: int
    issue_description: str = Field(..., min_length=5, max_length=500)

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceAssign(BaseModel):
    technician_id: int

class MaintenanceResolve(BaseModel):
    cost: Optional[float] = Field(None, ge=0)
    resolution_notes: str = Field(..., min_length=5, max_length=500)

class MaintenanceOut(MaintenanceBase):
    id: int
    reported_by_id: int
    technician_id: Optional[int]
    status: str
    cost: Optional[float]
    resolution_notes: Optional[str]
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True