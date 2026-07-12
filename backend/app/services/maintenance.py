from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.maintenance import Maintenance
from app.models.asset import Asset
from app.models.user import User
from app.schemas.maintenance import MaintenanceCreate, MaintenanceAssign, MaintenanceResolve

def get_maintenance_by_id(db: Session, maintenance_id: int) -> Optional[Maintenance]:
    return db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()

def list_maintenances(
    db: Session,
    asset_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Maintenance]:
    query = db.query(Maintenance)
    if asset_id is not None:
        query = query.filter(Maintenance.asset_id == asset_id)
    if status_filter is not None:
        query = query.filter(Maintenance.status == status_filter)
    return query.offset(skip).limit(limit).all()

def create_maintenance(db: Session, request_in: MaintenanceCreate, reported_by_id: int) -> Maintenance:
    # Validate Asset exists
    asset = db.query(Asset).filter(Asset.id == request_in.asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {request_in.asset_id} not found"
        )
    
    # Create request with Pending status
    db_maint = Maintenance(
        asset_id=request_in.asset_id,
        reported_by_id=reported_by_id,
        issue_description=request_in.issue_description,
        status="Pending"
    )
    db.add(db_maint)
    db.commit()
    db.refresh(db_maint)
    return db_maint

def approve_maintenance(db: Session, maintenance_id: int) -> Maintenance:
    db_maint = get_maintenance_by_id(db, maintenance_id)
    if not db_maint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance request with ID {maintenance_id} not found"
        )
    
    if db_maint.status != "Pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve request with status '{db_maint.status}'"
        )

    db_maint.status = "Approved"

    # Automatically set Asset status to "Under Maintenance"
    asset = db.query(Asset).filter(Asset.id == db_maint.asset_id).first()
    if asset:
        asset.status = "Under Maintenance"

    db.commit()
    db.refresh(db_maint)
    return db_maint

def assign_technician(db: Session, maintenance_id: int, assign_in: MaintenanceAssign) -> Maintenance:
    db_maint = get_maintenance_by_id(db, maintenance_id)
    if not db_maint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance request with ID {maintenance_id} not found"
        )
    
    if db_maint.status not in ["Approved", "Pending"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot assign technician in current status '{db_maint.status}'"
        )

    # Validate technician exists
    tech = db.query(User).filter(User.id == assign_in.technician_id).first()
    if not tech:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Technician user with ID {assign_in.technician_id} not found"
        )

    db_maint.technician_id = assign_in.technician_id
    db_maint.status = "Technician Assigned"
    
    # If starting from Pending, make sure asset becomes Under Maintenance
    asset = db.query(Asset).filter(Asset.id == db_maint.asset_id).first()
    if asset and asset.status != "Under Maintenance":
        asset.status = "Under Maintenance"

    db.commit()
    db.refresh(db_maint)
    return db_maint

def start_maintenance_work(db: Session, maintenance_id: int) -> Maintenance:
    db_maint = get_maintenance_by_id(db, maintenance_id)
    if not db_maint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance request with ID {maintenance_id} not found"
        )
    
    if db_maint.status != "Technician Assigned":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot start work in status '{db_maint.status}'. Technician must be assigned first."
        )

    db_maint.status = "In Progress"
    db.commit()
    db.refresh(db_maint)
    return db_maint

def resolve_maintenance(db: Session, maintenance_id: int, resolve_in: MaintenanceResolve) -> Maintenance:
    db_maint = get_maintenance_by_id(db, maintenance_id)
    if not db_maint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Maintenance request with ID {maintenance_id} not found"
        )
    
    if db_maint.status not in ["In Progress", "Technician Assigned", "Approved"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot resolve maintenance request in status '{db_maint.status}'"
        )

    db_maint.status = "Resolved"
    db_maint.cost = resolve_in.cost
    db_maint.resolution_notes = resolve_in.resolution_notes
    db_maint.resolved_at = datetime.utcnow()

    # Automatically set Asset status back to "Available"
    asset = db.query(Asset).filter(Asset.id == db_maint.asset_id).first()
    if asset:
        asset.status = "Available"

    db.commit()
    db.refresh(db_maint)
    return db_maint