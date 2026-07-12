from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.allocation import Allocation
from app.models.asset import Asset
from app.models.user import User
from app.schemas.allocation import AllocationCreate, AllocationTransferRequest

def get_allocation_by_id(db: Session, allocation_id: int) -> Optional[Allocation]:
    return db.query(Allocation).filter(Allocation.id == allocation_id).first()

def list_allocations(
    db: Session,
    asset_id: Optional[int] = None,
    employee_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Allocation]:
    query = db.query(Allocation)
    if asset_id is not None:
        query = query.filter(Allocation.asset_id == asset_id)
    if employee_id is not None:
        query = query.filter(Allocation.employee_id == employee_id)
    if status_filter is not None:
        query = query.filter(Allocation.status == status_filter)
    return query.offset(skip).limit(limit).all()

def create_allocation(db: Session, alloc_in: AllocationCreate, allocated_by_id: int) -> Allocation:
    # 1. Validate Asset exists
    asset = db.query(Asset).filter(Asset.id == alloc_in.asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {alloc_in.asset_id} not found"
        )
    
    # 2. Check if asset is available
    if asset.status != "Available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot allocate asset with status '{asset.status}'. It must be 'Available'."
        )

    # 3. Validate Employee exists
    employee = db.query(User).filter(User.id == alloc_in.employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {alloc_in.employee_id} not found"
        )

    # 4. Create Allocation
    db_alloc = Allocation(
        asset_id=alloc_in.asset_id,
        employee_id=alloc_in.employee_id,
        allocated_by_id=allocated_by_id,
        status="Active"
    )
    db.add(db_alloc)

    # 5. Update Asset Status
    asset.status = "Allocated"
    
    db.commit()
    db.refresh(db_alloc)
    return db_alloc

def return_allocation(db: Session, allocation_id: int) -> Allocation:
    # 1. Validate Allocation exists and is active
    db_alloc = get_allocation_by_id(db, allocation_id)
    if not db_alloc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Allocation with ID {allocation_id} not found"
        )
    
    if db_alloc.status not in ["Active", "Transfer Pending"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Allocation is already closed with status '{db_alloc.status}'"
        )

    # 2. Close Allocation
    db_alloc.status = "Returned"
    db_alloc.returned_at = datetime.utcnow()

    # 3. Reset Asset Status to Available
    asset = db.query(Asset).filter(Asset.id == db_alloc.asset_id).first()
    if asset:
        asset.status = "Available"

    db.commit()
    db.refresh(db_alloc)
    return db_alloc

def request_transfer(db: Session, allocation_id: int, request_in: AllocationTransferRequest, current_user_id: int) -> Allocation:
    db_alloc = get_allocation_by_id(db, allocation_id)
    if not db_alloc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Allocation with ID {allocation_id} not found"
        )
    
    # Check if active
    if db_alloc.status != "Active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot request transfer on an inactive allocation (status: {db_alloc.status})"
        )

    # Validate target employee exists
    target_employee = db.query(User).filter(User.id == request_in.transfer_to_employee_id).first()
    if not target_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target employee with ID {request_in.transfer_to_employee_id} not found"
        )

    # Prevent transferring to self
    if db_alloc.employee_id == request_in.transfer_to_employee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot transfer an asset to the same employee who currently holds it"
        )

    db_alloc.status = "Transfer Pending"
    db_alloc.transfer_to_employee_id = request_in.transfer_to_employee_id
    
    db.commit()
    db.refresh(db_alloc)
    return db_alloc

def approve_transfer(db: Session, allocation_id: int, approved_by_id: int) -> Allocation:
    db_alloc = get_allocation_by_id(db, allocation_id)
    if not db_alloc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Allocation with ID {allocation_id} not found"
        )

    if db_alloc.status != "Transfer Pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No pending transfer found for this allocation (status: {db_alloc.status})"
        )

    # 1. Close current allocation as Returned/Transferred
    db_alloc.status = "Returned"
    db_alloc.returned_at = datetime.utcnow()
    target_employee_id = db_alloc.transfer_to_employee_id

    # Clear target employee reference
    db_alloc.transfer_to_employee_id = None

    # 2. Create new Allocation for target employee
    new_alloc = Allocation(
        asset_id=db_alloc.asset_id,
        employee_id=target_employee_id,
        allocated_by_id=approved_by_id,
        status="Active"
    )
    db.add(new_alloc)

    # Asset status remains "Allocated", but we ensure it is correct
    asset = db.query(Asset).filter(Asset.id == db_alloc.asset_id).first()
    if asset:
        asset.status = "Allocated"

    db.commit()
    db.refresh(new_alloc)
    return new_alloc

def reject_transfer(db: Session, allocation_id: int) -> Allocation:
    db_alloc = get_allocation_by_id(db, allocation_id)
    if not db_alloc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Allocation with ID {allocation_id} not found"
        )

    if db_alloc.status != "Transfer Pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No pending transfer found for this allocation (status: {db_alloc.status})"
        )

    # Revert status to Active and clear target employee reference
    db_alloc.status = "Active"
    db_alloc.transfer_to_employee_id = None

    db.commit()
    db.refresh(db_alloc)
    return db_alloc