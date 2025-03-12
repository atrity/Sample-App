from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

from database import get_db
from schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeList,
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendanceList
)
from models import User, Employee
from auth import get_current_active_user, check_hr_permission
import crud

router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)

@router.post("/", response_model=EmployeeResponse)
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Create a new employee. Only HR and admin users can create employees.
    """
    # Verify department exists
    department = crud.get_department(db, employee.department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    # If user_id is provided, verify user exists
    if employee.user_id:
        user = crud.get_user(db, employee.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if user is already associated with an employee
        existing_employee = db.query(Employee).filter(
            Employee.user_id == employee.user_id
        ).first()
        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already associated with an employee"
            )
    
    return crud.create_employee(db, employee)

@router.get("/", response_model=EmployeeList)
async def list_employees(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List all employees with optional filtering.
    """
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

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed information about a specific employee.
    """
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Update an employee's information. Only HR and admin users can update employees.
    """
    # Verify employee exists
    existing_employee = crud.get_employee(db, employee_id)
    if not existing_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # If department_id is being updated, verify new department exists
    if employee_update.department_id:
        department = crud.get_department(db, employee_update.department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
    
    updated_employee = crud.update_employee(db, employee_id, employee_update)
    return updated_employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Delete an employee. Only HR and admin users can delete employees.
    """
    success = crud.delete_employee(db, employee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

# Attendance-related routes
@router.post("/{employee_id}/attendance", response_model=AttendanceResponse)
async def create_attendance(
    employee_id: int,
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Create an attendance record for an employee.
    """
    # Verify employee exists
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Set employee_id from path parameter
    attendance.employee_id = employee_id
    
    return crud.create_attendance(db, attendance)

@router.get("/{employee_id}/attendance", response_model=AttendanceList)
async def list_employee_attendance(
    employee_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List attendance records for a specific employee.
    """
    # Verify employee exists
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    attendances = crud.get_attendances(
        db,
        skip=skip,
        limit=limit,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return {
        "total": len(attendances),
        "items": attendances
    }

@router.put("/{employee_id}/attendance/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(
    employee_id: int,
    attendance_id: int,
    attendance_update: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Update an attendance record for an employee.
    """
    # Verify attendance record exists and belongs to the employee
    attendance = crud.get_attendance(db, attendance_id)
    if not attendance or attendance.employee_id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    return crud.update_attendance(db, attendance_id, attendance_update)

@router.delete("/{employee_id}/attendance/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(
    employee_id: int,
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Delete an attendance record for an employee.
    """
    # Verify attendance record exists and belongs to the employee
    attendance = crud.get_attendance(db, attendance_id)
    if not attendance or attendance.employee_id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    crud.delete_attendance(db, attendance_id)
