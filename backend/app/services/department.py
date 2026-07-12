from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.department import Department
from app.models.user import User
from app.schemas.department import DepartmentCreate, DepartmentUpdate

def get_department_by_id(db: Session, department_id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == department_id).first()

def get_department_by_code(db: Session, code: str) -> Optional[Department]:
    return db.query(Department).filter(Department.code == code.upper()).first()

def get_department_by_name(db: Session, name: str) -> Optional[Department]:
    return db.query(Department).filter(Department.name == name).first()

def list_departments(db: Session, skip: int = 0, limit: int = 100) -> List[Department]:
    return db.query(Department).offset(skip).limit(limit).all()

def create_department(db: Session, dept_in: DepartmentCreate) -> Department:
    if get_department_by_code(db, dept_in.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department with code '{dept_in.code}' already exists"
        )
    
    if get_department_by_name(db, dept_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department with name '{dept_in.name}' already exists"
        )
    
    if dept_in.manager_id is not None:
        manager = db.query(User).filter(User.id == dept_in.manager_id).first()
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {dept_in.manager_id} not found to assign as manager"
            )

    db_dept = Department(
        name=dept_in.name,
        code=dept_in.code.upper(),
        manager_id=dept_in.manager_id
    )
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

def update_department(db: Session, department_id: int, dept_in: DepartmentUpdate) -> Department:
    db_dept = get_department_by_id(db, department_id)
    if not db_dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID {department_id} not found"
        )

    if dept_in.name is not None and dept_in.name != db_dept.name:
        if get_department_by_name(db, dept_in.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Department with name '{dept_in.name}' already exists"
            )
        db_dept.name = dept_in.name

    if dept_in.code is not None and dept_in.code.upper() != db_dept.code:
        code_upper = dept_in.code.upper()
        if get_department_by_code(db, code_upper):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Department with code '{code_upper}' already exists"
            )
        db_dept.code = code_upper

    if dept_in.manager_id is not None and dept_in.manager_id != db_dept.manager_id:
        manager = db.query(User).filter(User.id == dept_in.manager_id).first()
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {dept_in.manager_id} not found to assign as manager"
            )
        db_dept.manager_id = dept_in.manager_id
    elif dept_in.manager_id is None and "manager_id" in dept_in.model_fields_set:
        db_dept.manager_id = None

    db.commit()
    db.refresh(db_dept)
    return db_dept

def delete_department(db: Session, department_id: int) -> Department:
    db_dept = get_department_by_id(db, department_id)
    if not db_dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID {department_id} not found"
        )
    
    # Check if there are employees assigned to this department to prevent orphan errors
    employees_count = db.query(User).filter(User.department_id == department_id).count()
    if employees_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete department with ID {department_id} because it has {employees_count} assigned employees"
        )

    db.delete(db_dept)
    db.commit()
    return db_dept