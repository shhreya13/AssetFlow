from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.routers.dependencies import get_current_user
from app.models.user import User
from app.schemas.asset import AssetCreate, AssetUpdate, AssetOut
from app.schemas.response import ApiResponse, success_response
import app.services.asset as asset_service

router = APIRouter(prefix="/assets", tags=["Assets"])

def require_admin_or_asset_manager(current_user: User = Depends(get_current_user)):
    if not hasattr(current_user, "role") or current_user.role not in ["Admin", "Asset Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Admin or Asset Manager role required."
        )
    return current_user

@router.post("/", response_model=ApiResponse[AssetOut], status_code=status.HTTP_201_CREATED)
def create_new_asset(
    asset_in: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_asset_manager)
):
    asset = asset_service.create_asset(db, asset_in)
    return success_response(
        message="Asset registered successfully",
        data=AssetOut.model_validate(asset)
    )

@router.get("/", response_model=ApiResponse[List[AssetOut]])
def get_all_assets(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    status: Optional[str] = Query(None, description="Filter by asset status (Available, Allocated, Under Maintenance, Retired)"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assets = asset_service.list_assets(
        db, 
        category_id=category_id, 
        department_id=department_id, 
        status_filter=status, 
        skip=skip, 
        limit=limit
    )
    data = [AssetOut.model_validate(a) for a in assets]
    return success_response(
        message="Assets retrieved successfully",
        data=data
    )

@router.get("/{id}", response_model=ApiResponse[AssetOut])
def get_asset_detail(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = asset_service.get_asset_by_id(db, id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {id} not found"
        )
    return success_response(
        message="Asset retrieved successfully",
        data=AssetOut.model_validate(asset)
    )

@router.put("/{id}", response_model=ApiResponse[AssetOut])
def update_asset_detail(
    id: int,
    asset_in: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_asset_manager)
):
    asset = asset_service.update_asset(db, id, asset_in)
    return success_response(
        message="Asset updated successfully",
        data=AssetOut.model_validate(asset)
    )

@router.delete("/{id}", response_model=ApiResponse[AssetOut])
def remove_asset(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_asset_manager)
):
    asset = asset_service.delete_asset(db, id)
    return success_response(
        message="Asset deleted successfully",
        data=AssetOut.model_validate(asset)
    )