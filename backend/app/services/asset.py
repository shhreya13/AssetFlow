from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.asset import Asset
from app.models.asset_category import AssetCategory
from app.models.department import Department
from app.schemas.asset import AssetCreate, AssetUpdate

def get_asset_by_id(db: Session, asset_id: int) -> Optional[Asset]:
    return db.query(Asset).filter(Asset.id == asset_id).first()

def get_asset_by_tag(db: Session, asset_tag: str) -> Optional[Asset]:
    return db.query(Asset).filter(Asset.asset_tag == asset_tag.upper()).first()

def get_asset_by_serial(db: Session, serial_number: str) -> Optional[Asset]:
    return db.query(Asset).filter(Asset.serial_number == serial_number).first()

def list_assets(
    db: Session, 
    category_id: Optional[int] = None, 
    department_id: Optional[int] = None, 
    status_filter: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[Asset]:
    query = db.query(Asset)
    if category_id is not None:
        query = query.filter(Asset.category_id == category_id)
    if department_id is not None:
        query = query.filter(Asset.department_id == department_id)
    if status_filter is not None:
        query = query.filter(Asset.status == status_filter)
    return query.offset(skip).limit(limit).all()

def generate_asset_tag(db: Session, category_code: str) -> str:
    # Pattern: AST-<CATEGORY_CODE>-<SEQUENTIAL_NUMBER_5_DIGITS>
    prefix = f"AST-{category_code.upper()}-"
    count = db.query(Asset).filter(Asset.asset_tag.like(f"{prefix}%")).count()
    next_num = count + 1
    
    # Ensure uniqueness in case of deletion gaps
    while True:
        tag = f"{prefix}{next_num:05d}"
        if not db.query(Asset).filter(Asset.asset_tag == tag).first():
            return tag
        next_num += 1

def create_asset(db: Session, asset_in: AssetCreate) -> Asset:
    # 1. Validate Category
    category = db.query(AssetCategory).filter(AssetCategory.id == asset_in.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset category with ID {asset_in.category_id} not found"
        )

    # 2. Validate Department
    if asset_in.department_id is not None:
        department = db.query(Department).filter(Department.id == asset_in.department_id).first()
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {asset_in.department_id} not found"
            )

    # 3. Validate Serial Number Uniqueness
    if asset_in.serial_number:
        existing_serial = get_asset_by_serial(db, asset_in.serial_number)
        if existing_serial:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset with serial number '{asset_in.serial_number}' already exists"
            )

    # 4. Auto-generate unique asset tag
    asset_tag = generate_asset_tag(db, category.code)

    db_asset = Asset(
        name=asset_in.name,
        asset_tag=asset_tag,
        serial_number=asset_in.serial_number,
        status="Available",  # Default status
        category_id=asset_in.category_id,
        department_id=asset_in.department_id,
        purchase_date=asset_in.purchase_date,
        cost=asset_in.cost,
        description=asset_in.description
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def update_asset(db: Session, asset_id: int, asset_in: AssetUpdate) -> Asset:
    db_asset = get_asset_by_id(db, asset_id)
    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found"
        )

    # Validate category update
    if asset_in.category_id is not None and asset_in.category_id != db_asset.category_id:
        category = db.query(AssetCategory).filter(AssetCategory.id == asset_in.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asset category with ID {asset_in.category_id} not found"
            )
        db_asset.category_id = asset_in.category_id

    # Validate department update
    if asset_in.department_id is not None and asset_in.department_id != db_asset.department_id:
        department = db.query(Department).filter(Department.id == asset_in.department_id).first()
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {asset_in.department_id} not found"
            )
        db_asset.department_id = asset_in.department_id
    elif asset_in.department_id is None and "department_id" in asset_in.model_fields_set:
        db_asset.department_id = None

    # Validate serial number uniqueness
    if asset_in.serial_number is not None and asset_in.serial_number != db_asset.serial_number:
        existing_serial = get_asset_by_serial(db, asset_in.serial_number)
        if existing_serial:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset with serial number '{asset_in.serial_number}' already exists"
            )
        db_asset.serial_number = asset_in.serial_number

    # Update simple fields
    if asset_in.name is not None:
        db_asset.name = asset_in.name
    if asset_in.status is not None:
        db_asset.status = asset_in.status
    if asset_in.purchase_date is not None:
        db_asset.purchase_date = asset_in.purchase_date
    if asset_in.cost is not None:
        db_asset.cost = asset_in.cost
    if asset_in.description is not None:
        db_asset.description = asset_in.description

    db.commit()
    db.refresh(db_asset)
    return db_asset

def delete_asset(db: Session, asset_id: int) -> Asset:
    db_asset = get_asset_by_id(db, asset_id)
    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found"
        )
    
    db.delete(db_asset)
    db.commit()
    return db_asset