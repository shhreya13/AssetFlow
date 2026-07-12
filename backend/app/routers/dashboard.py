from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.routers.dependencies import get_current_user
from app.models.user import User
from app.models.asset import Asset
from app.models.department import Department
from app.models.allocation import Allocation
from app.models.booking import Booking
from app.models.maintenance import Maintenance
from app.schemas.dashboard import DashboardSummary
from app.schemas.response import ApiResponse, success_response

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=ApiResponse[DashboardSummary])
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Query live counts directly from SQLite
    total_assets = db.query(Asset).count()
    available_assets = db.query(Asset).filter(Asset.status == "Available").count()
    allocated_assets = db.query(Asset).filter(Asset.status == "Allocated").count()
    under_maintenance_assets = db.query(Asset).filter(Asset.status == "Under Maintenance").count()
    retired_assets = db.query(Asset).filter(Asset.status == "Retired").count()
    
    total_departments = db.query(Department).count()
    
    active_allocations = db.query(Allocation).filter(Allocation.status == "Active").count()
    pending_maintenance = db.query(Maintenance).filter(Maintenance.status == "Pending").count()
    active_bookings = db.query(Booking).filter(Booking.status == "Approved").count()
    
    summary = DashboardSummary(
        total_assets=total_assets,
        available_assets=available_assets,
        allocated_assets=allocated_assets,
        under_maintenance_assets=under_maintenance_assets,
        retired_assets=retired_assets,
        total_departments=total_departments,
        active_allocations=active_allocations,
        pending_maintenance=pending_maintenance,
        active_bookings=active_bookings
    )
    
    return success_response(
        message="Dashboard summary retrieved successfully",
        data=summary
    )