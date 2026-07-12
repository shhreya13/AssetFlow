from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, model_validator

class BookingBase(BaseModel):
    asset_id: int
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = Field(None, max_length=255)

    @model_validator(mode="after")
    def validate_times(self) -> "BookingBase":
        now = datetime.now(timezone.utc)
        
        # Convert start/end to offset-aware utc if they are naive
        start = self.start_time
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
            
        end = self.end_time
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)
            
        if start < now:
            raise ValueError("Booking start time must be in the future")
            
        if end <= start:
            raise ValueError("Booking end time must be after the start time")
            
        return self

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True