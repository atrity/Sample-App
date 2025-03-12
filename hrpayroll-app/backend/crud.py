from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from fastapi import HTTPException, status

from models import User, Employee, Department, Payroll, Attendance
from schemas import (
    UserCreate, UserUpdate,
    EmployeeCreate, EmployeeUpdate,
    DepartmentCreate, DepartmentUpdate,
    PayrollCreate, PayrollUpdate,
    AttendanceCreate, AttendanceUpdate
)
from auth import get_password_hash

# User CRUD operations
def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[User]:
    """Get list of users with optional search."""
    query = db.query(User)
    if search:
        search_filter = or_(
            User.username.ilike(f"%{search}%"),
            User.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    return query.offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update a user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# Employee CRUD operations
def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
    """Create a new employee."""
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    """Get an employee by ID."""
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employees(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    department_id: Optional[int] = None
) -> List[Employee]:
    """Get list of employees with optional search and department filter."""
    query = db.query(Employee)
    
    if search:
        search_filter = or_(
            Employee.first_name.ilike(f"%{search}%"),
            Employee.last_name.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    
    return query.offset(skip).limit(limit).all()

def update_employee(
    db: Session,
    employee_id: int,
    employee_update: EmployeeUpdate
) -> Optional[Employee]:
    """Update an employee."""
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
    
    update_data = employee_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int) -> bool:
    """Delete an employee."""
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return False
    
    db.delete(db_employee)
    db.commit()
    return True

# Department CRUD operations
def create_department(db: Session, department: DepartmentCreate) -> Department:
    """Create a new department."""
    db_department = Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_department(db: Session, department_id: int) -> Optional[Department]:
    """Get a department by ID."""
    return db.query(Department).filter(Department.id == department_id).first()

def get_departments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[Department]:
    """Get list of departments with optional search."""
    query = db.query(Department)
    if search:
        query = query.filter(Department.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def update_department(
    db: Session,
    department_id: int,
    department_update: DepartmentUpdate
) -> Optional[Department]:
    """Update a department."""
    db_department = get_department(db, department_id)
    if not db_department:
        return None
    
    update_data = department_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_department, field, value)
    
    db.commit()
    db.refresh(db_department)
    return db_department

def delete_department(db: Session, department_id: int) -> bool:
    """Delete a department."""
    db_department = get_department(db, department_id)
    if not db_department:
        return False
    
    db.delete(db_department)
    db.commit()
    return True

# Payroll CRUD operations
def create_payroll(db: Session, payroll: PayrollCreate) -> Payroll:
    """Create a new payroll record."""
    db_payroll = Payroll(**payroll.model_dump())
    db.add(db_payroll)
    db.commit()
    db.refresh(db_payroll)
    return db_payroll

def get_payroll(db: Session, payroll_id: int) -> Optional[Payroll]:
    """Get a payroll record by ID."""
    return db.query(Payroll).filter(Payroll.id == payroll_id).first()

def get_payrolls(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[Payroll]:
    """Get list of payroll records with optional filters."""
    query = db.query(Payroll)
    
    if employee_id:
        query = query.filter(Payroll.employee_id == employee_id)
    
    if start_date:
        query = query.filter(Payroll.pay_period_start >= start_date)
    
    if end_date:
        query = query.filter(Payroll.pay_period_end <= end_date)
    
    return query.offset(skip).limit(limit).all()

def update_payroll(
    db: Session,
    payroll_id: int,
    payroll_update: PayrollUpdate
) -> Optional[Payroll]:
    """Update a payroll record."""
    db_payroll = get_payroll(db, payroll_id)
    if not db_payroll:
        return None
    
    update_data = payroll_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_payroll, field, value)
    
    db.commit()
    db.refresh(db_payroll)
    return db_payroll

def delete_payroll(db: Session, payroll_id: int) -> bool:
    """Delete a payroll record."""
    db_payroll = get_payroll(db, payroll_id)
    if not db_payroll:
        return False
    
    db.delete(db_payroll)
    db.commit()
    return True

# Attendance CRUD operations
def create_attendance(db: Session, attendance: AttendanceCreate) -> Attendance:
    """Create a new attendance record."""
    db_attendance = Attendance(**attendance.model_dump())
    if db_attendance.check_in and db_attendance.check_out:
        db_attendance.calculate_work_hours()
    
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_attendance(db: Session, attendance_id: int) -> Optional[Attendance]:
    """Get an attendance record by ID."""
    return db.query(Attendance).filter(Attendance.id == attendance_id).first()

def get_attendances(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[Attendance]:
    """Get list of attendance records with optional filters."""
    query = db.query(Attendance)
    
    if employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    
    if start_date:
        query = query.filter(Attendance.date >= start_date)
    
    if end_date:
        query = query.filter(Attendance.date <= end_date)
    
    return query.offset(skip).limit(limit).all()

def update_attendance(
    db: Session,
    attendance_id: int,
    attendance_update: AttendanceUpdate
) -> Optional[Attendance]:
    """Update an attendance record."""
    db_attendance = get_attendance(db, attendance_id)
    if not db_attendance:
        return None
    
    update_data = attendance_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_attendance, field, value)
    
    if db_attendance.check_in and db_attendance.check_out:
        db_attendance.calculate_work_hours()
    
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def delete_attendance(db: Session, attendance_id: int) -> bool:
    """Delete an attendance record."""
    db_attendance = get_attendance(db, attendance_id)
    if not db_attendance:
        return False
    
    db.delete(db_attendance)
    db.commit()
    return True
