from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_assets: int
    available_assets: int
    allocated_assets: int
    under_maintenance_assets: int
    retired_assets: int
    total_departments: int
    active_allocations: int
    pending_maintenance: int
    active_bookings: int