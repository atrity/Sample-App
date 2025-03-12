from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentList,
    EmployeeList
)
from models import User
from auth import get_current_active_user, check_hr_permission
import crud

router = APIRouter(
    prefix="/departments",
    tags=["departments"]
)

@router.post("/", response_model=DepartmentResponse)
async def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Create a new department. Only HR and admin users can create departments.
    """
    # Check if department with same name exists
    existing_dept = db.query(crud.Department).filter(
        crud.Department.name == department.name
    ).first()
    
    if existing_dept:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department with this name already exists"
        )
    
    return crud.create_department(db, department)

@router.get("/", response_model=DepartmentList)
async def list_departments(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List all departments with optional search filter.
    """
    departments = crud.get_departments(
        db,
        skip=skip,
        limit=limit,
        search=search
    )
    return {
        "total": len(departments),
        "items": departments
    }

@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed information about a specific department.
    """
    department = crud.get_department(db, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return department

@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    department_update: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Update a department's information. Only HR and admin users can update departments.
    """
    # Verify department exists
    existing_dept = crud.get_department(db, department_id)
    if not existing_dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    # If name is being updated, check it's not already taken
    if department_update.name and department_update.name != existing_dept.name:
        name_exists = db.query(crud.Department).filter(
            crud.Department.name == department_update.name
        ).first()
        if name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department with this name already exists"
            )
    
    updated_department = crud.update_department(db, department_id, department_update)
    return updated_department

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Delete a department. Only HR and admin users can delete departments.
    """
    # Check if department has any employees
    department = crud.get_department(db, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    if department.employees:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete department with existing employees"
        )
    
    success = crud.delete_department(db, department_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete department"
        )

@router.get("/{department_id}/employees", response_model=EmployeeList)
async def list_department_employees(
    department_id: int,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List all employees in a specific department.
    """
    # Verify department exists
    department = crud.get_department(db, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    employees = crud.get_employees(
        db,
        skip=skip,
        limit=limit,
        search=search,
        department_id=department_id
    )
    
    return {
        "total": len(employees),
        "items": employees
    }

@router.get("/{department_id}/statistics")
async def get_department_statistics(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Get statistics about a department including employee count, average salary, etc.
    """
    department = crud.get_department(db, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    # Calculate department statistics
    employees = department.employees
    total_employees = len(employees)
    
    if total_employees > 0:
        total_salary = sum(emp.base_salary for emp in employees)
        avg_salary = total_salary / total_employees
    else:
        total_salary = 0
        avg_salary = 0
    
    return {
        "department_name": department.name,
        "total_employees": total_employees,
        "total_salary": total_salary,
        "average_salary": avg_salary,
        "created_at": department.created_at,
        "updated_at": department.updated_at
    }
