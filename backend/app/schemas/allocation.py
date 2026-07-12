from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class AllocationBase(BaseModel):
    asset_id: int
    employee_id: int

class AllocationCreate(AllocationBase):
    pass

class AllocationTransferRequest(BaseModel):
    transfer_to_employee_id: int = Field(..., description="Target employee ID for the transfer")

class AllocationOut(AllocationBase):
    id: int
    allocated_by_id: Optional[int]
    allocated_at: datetime
    returned_at: Optional[datetime]
    status: str
    transfer_to_employee_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True