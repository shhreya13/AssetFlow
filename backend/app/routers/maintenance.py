from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.routers.dependencies import get_current_user
from app.models.user import User
from app.schemas.maintenance import MaintenanceCreate, MaintenanceAssign, MaintenanceResolve, MaintenanceOut
from app.schemas.response import ApiResponse, success_response
import app.services.maintenance as maint_service

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

def require_admin_or_asset_manager(current_user: User = Depends(get_current_user)):
    if not hasattr(current_user, "role") or current_user.role not in ["Admin", "Asset Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Admin or Asset Manager role required."
        )
    return current_user

@router.post("/", response_model=ApiResponse[MaintenanceOut], status_code=status.HTTP_201_CREATED)
def report_issue(
    request_in: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    maint = maint_service.create_maintenance(db, request_in, current_user.id)
    return success_response(
        message="Maintenance request registered successfully. Status: Pending.",
        data=MaintenanceOut.model_validate(maint)
    )

@router.get("/", response_model=ApiResponse[List[MaintenanceOut]])
def get_all_requests(
    asset_id: Optional[int] = Query(None, description="Filter by Asset ID"),
    status: Optional[str] = Query(None, description="Filter by status (Pending, Approved, Technician Assigned, In Progress, Resolved)"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    requests = maint_service.list_maintenances(
        db, 
        asset_id=asset_id, 
        status_filter=status, 
        skip=skip, 
        limit=limit
    )
    data = [MaintenanceOut.model_validate(r) for r in requests]
    return success_response(
        message="Maintenance requests retrieved successfully",
        data=data
    )

@router.get("/{id}", response_model=ApiResponse[MaintenanceOut])
def get_request_detail(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    maint = maint_service.get_maintenance_by_id(db, id)
    if not maint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance request with ID {id} not found"
        )
    return success_response(
        message="Maintenance request retrieved successfully",
        data=MaintenanceOut.model_validate(maint)
    )

@router.post("/{id}/approve", response_model=ApiResponse[MaintenanceOut])
def approve_request(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_asset_manager)
):
    maint = maint_service.approve_maintenance(db, id)
    return success_response(
        message="Maintenance request approved successfully. Asset is now Under Maintenance.",
        data=MaintenanceOut.model_validate(maint)
    )

@router.post("/{id}/assign", response_model=ApiResponse[MaintenanceOut])
def assign_tech(
    id: int,
    assign_in: MaintenanceAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_asset_manager)
):
    maint = maint_service.assign_technician(db, id, assign_in)
    return success_response(
        message="Technician assigned successfully.",
        data=MaintenanceOut.model_validate(maint)
    )

@router.post("/{id}/start", response_model=ApiResponse[MaintenanceOut])
def start_work(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    maint = maint_service.get_maintenance_by_id(db, id)
    if not maint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance request not found"
        )

    if maint.technician_id != current_user.id and current_user.role not in ["Admin", "Asset Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to start work on this maintenance task."
        )

    maint = maint_service.start_maintenance_work(db, id)
    return success_response(
        message="Maintenance work started. Status: In Progress.",
        data=MaintenanceOut.model_validate(maint)
    )

@router.post("/{id}/resolve", response_model=ApiResponse[MaintenanceOut])
def resolve_request(
    id: int,
    resolve_in: MaintenanceResolve,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    maint = maint_service.get_maintenance_by_id(db, id)
    if not maint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance request not found"
        )

    if maint.technician_id != current_user.id and current_user.role not in ["Admin", "Asset Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to resolve this maintenance task."
        )

    maint = maint_service.resolve_maintenance(db, id, resolve_in)
    return success_response(
        message="Maintenance request resolved successfully. Asset is now Available.",
        data=MaintenanceOut.model_validate(maint)
    )