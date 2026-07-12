from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.routers.dependencies import get_current_user
from app.models.user import User
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut
from app.schemas.response import ApiResponse, success_response
import app.services.department as dept_service

router = APIRouter(prefix="/departments", tags=["Departments"])

def require_admin(current_user: User = Depends(get_current_user)):
    if not hasattr(current_user, "role") or current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Admin role required."
        )
    return current_user

@router.post("/", response_model=ApiResponse[DepartmentOut], status_code=status.HTTP_201_CREATED)
def create_new_department(
    dept_in: DepartmentCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    department = dept_service.create_department(db, dept_in)
    return success_response(
        message="Department created successfully",
        data=DepartmentOut.model_validate(department)
    )

@router.get("/", response_model=ApiResponse[List[DepartmentOut]])
def get_all_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    departments = dept_service.list_departments(db, skip=skip, limit=limit)
    data = [DepartmentOut.model_validate(d) for d in departments]
    return success_response(
        message="Departments retrieved successfully",
        data=data
    )

@router.get("/{id}", response_model=ApiResponse[DepartmentOut])
def get_department_detail(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    department = dept_service.get_department_by_id(db, id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID {id} not found"
        )
    return success_response(
        message="Department retrieved successfully",
        data=DepartmentOut.model_validate(department)
    )

@router.put("/{id}", response_model=ApiResponse[DepartmentOut])
def update_department_detail(
    id: int,
    dept_in: DepartmentUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    department = dept_service.update_department(db, id, dept_in)
    return success_response(
        message="Department updated successfully",
        data=DepartmentOut.model_validate(department)
    )

@router.delete("/{id}", response_model=ApiResponse[DepartmentOut])
def remove_department(
    id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    department = dept_service.delete_department(db, id)
    return success_response(
        message="Department deleted successfully",
        data=DepartmentOut.model_validate(department)
    )