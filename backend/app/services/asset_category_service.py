from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.asset_category import AssetCategory
from app.schemas.asset_category import AssetCategoryCreate, AssetCategoryUpdate

def get_category_by_id(db: Session, category_id: int) -> Optional[AssetCategory]:
    return db.query(AssetCategory).filter(AssetCategory.id == category_id).first()

def get_category_by_code(db: Session, code: str) -> Optional[AssetCategory]:
    return db.query(AssetCategory).filter(AssetCategory.code == code.upper()).first()

def get_category_by_name(db: Session, name: str) -> Optional[AssetCategory]:
    return db.query(AssetCategory).filter(AssetCategory.name == name).first()

def list_categories(db: Session, skip: int = 0, limit: int = 100) -> List[AssetCategory]:
    return db.query(AssetCategory).offset(skip).limit(limit).all()

def create_category(db: Session, category_in: AssetCategoryCreate) -> AssetCategory:
    if get_category_by_code(db, category_in.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Asset category with code '{category_in.code}' already exists"
        )
    if get_category_by_name(db, category_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Asset category with name '{category_in.name}' already exists"
        )

    db_category = AssetCategory(
        name=category_in.name,
        code=category_in.code.upper(),
        description=category_in.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_in: AssetCategoryUpdate) -> AssetCategory:
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset category with ID {category_id} not found"
        )

    if category_in.name is not None and category_in.name != db_category.name:
        if get_category_by_name(db, category_in.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset category with name '{category_in.name}' already exists"
            )
        db_category.name = category_in.name

    if category_in.code is not None and category_in.code.upper() != db_category.code:
        code_upper = category_in.code.upper()
        if get_category_by_code(db, code_upper):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset category with code '{code_upper}' already exists"
            )
        db_category.code = code_upper

    if category_in.description is not None:
        db_category.description = category_in.description

    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> AssetCategory:
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset category with ID {category_id} not found"
        )

    db.delete(db_category)
    db.commit()
    return db_category