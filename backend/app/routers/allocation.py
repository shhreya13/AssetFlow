from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.routers.dependencies import get_current_user
from app.models.user import User
from app.schemas.allocation import AllocationCreate, AllocationTransferRequest, AllocationOut
from app.schemas.response import ApiResponse, success_response
import app.services.allocation as alloc_service

router = APIRouter(prefix="/allocations", tags=["Allocations"])

def require_admin_or_asset_manager(current_user: User = Depends(get_current_user)):
    if not hasattr(current_user, "role") or current_user.role not in ["Admin", "Asset Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Admin or Asset Manager role required."
        )
    return current_user

@router.post("/", response_model=ApiResponse[AllocationOut], status_code=status.HTTP_201_CREATED)
def allocate_asset(
    alloc_in: AllocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_asset_manager)
):
    allocation = alloc_service.create_allocation(db, alloc_in, current_user.id)
    return success_response(
        message="Asset allocated successfully",
        data=AllocationOut.model_validate(allocation)
    )

@router.get("/", response_model=ApiResponse[List[AllocationOut]])
def get_all_allocations(
    asset_id: Optional[int] = Query(None, description="Filter by Asset ID"),
    employee_id: Optional[int] = Query(None, description="Filter by Employee User ID"),
    status: Optional[str] = Query(None, description="Filter by status (Active, Returned, Transfer Pending)"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    allocations = alloc_service.list_allocations(
        db, 
        asset_id=asset_id, 
        employee_id=employee_id, 
        status_filter=status, 
        skip=skip, 
        limit=limit
    )
    data = [AllocationOut.model_validate(a) for a in allocations]
    return success_response(
        message="Allocations retrieved successfully",
        data=data
    )

@router.get("/{id}", response_model=ApiResponse[AllocationOut])
def get_allocation_detail(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    allocation = alloc_service.get_allocation_by_id(db, id)
    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Allocation record with ID {id} not found"
        )
    return success_response(
        message="Allocation record retrieved successfully",
        data=AllocationOut.model_validate(allocation)
    )

@router.post("/{id}/return", response_model=ApiResponse[AllocationOut])
def return_allocated_asset(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_asset_manager)
):
    allocation = alloc_service.return_allocation(db, id)
    return success_response(
        message="Asset return registered successfully. Asset is now Available.",
        data=AllocationOut.model_validate(allocation)
    )

@router.post("/{id}/transfer-request", response_model=ApiResponse[AllocationOut])
def request_asset_transfer(
    id: int,
    request_in: AllocationTransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orig_alloc = alloc_service.get_allocation_by_id(db, id)
    if not orig_alloc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allocation record not found"
        )
    
    if orig_alloc.employee_id != current_user.id and current_user.role not in ["Admin", "Asset Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to transfer this asset. Only the current holder or Admin/Asset Manager can initiate a transfer."
        )

    allocation = alloc_service.request_transfer(db, id, request_in, current_user.id)
    return success_response(
        message="Transfer request submitted. Awaiting manager approval.",
        data=AllocationOut.model_validate(allocation)
    )

@router.post("/{id}/transfer-approve", response_model=ApiResponse[AllocationOut])
def approve_asset_transfer(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_asset_manager)
):
    new_allocation = alloc_service.approve_transfer(db, id, current_user.id)
    return success_response(
        message="Asset transfer approved successfully.",
        data=AllocationOut.model_validate(new_allocation)
    )

@router.post("/{id}/transfer-reject", response_model=ApiResponse[AllocationOut])
def reject_asset_transfer(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_asset_manager)
):
    allocation = alloc_service.reject_transfer(db, id)
    return success_response(
        message="Asset transfer request rejected. Asset remains with current owner.",
        data=AllocationOut.model_validate(allocation)
    )