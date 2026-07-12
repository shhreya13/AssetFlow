from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.asset_category import (
    AssetCategoryCreate,
    AssetCategoryUpdate,
    AssetCategoryOut,
)
from app.schemas.response import ApiResponse, success_response
import app.services.asset_category_service as category_service

router = APIRouter(
    prefix="/asset-categories",
    tags=["Asset Categories"]
)


@router.post("/", response_model=ApiResponse[AssetCategoryOut], status_code=status.HTTP_201_CREATED)
def create_new_category(
    category_in: AssetCategoryCreate,
    db: Session = Depends(get_db),
):
    category = category_service.create_category(db, category_in)
    return success_response(
        message="Asset category created successfully",
        data=AssetCategoryOut.model_validate(category)
    )


@router.get("/", response_model=ApiResponse[List[AssetCategoryOut]])
def get_all_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    categories = category_service.list_categories(db, skip=skip, limit=limit)
    data = [AssetCategoryOut.model_validate(c) for c in categories]
    return success_response(
        message="Asset categories retrieved successfully",
        data=data
    )


@router.get("/{id}", response_model=ApiResponse[AssetCategoryOut])
def get_category_detail(
    id: int,
    db: Session = Depends(get_db),
):
    category = category_service.get_category_by_id(db, id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset category with ID {id} not found"
        )

    return success_response(
        message="Asset category retrieved successfully",
        data=AssetCategoryOut.model_validate(category)
    )


@router.put("/{id}", response_model=ApiResponse[AssetCategoryOut])
def update_category_detail(
    id: int,
    category_in: AssetCategoryUpdate,
    db: Session = Depends(get_db),
):
    category = category_service.update_category(db, id, category_in)

    return success_response(
        message="Asset category updated successfully",
        data=AssetCategoryOut.model_validate(category)
    )


@router.delete("/{id}", response_model=ApiResponse[AssetCategoryOut])
def remove_category(
    id: int,
    db: Session = Depends(get_db),
):
    category = category_service.delete_category(db, id)

    return success_response(
        message="Asset category deleted successfully",
        data=AssetCategoryOut.model_validate(category)
    )