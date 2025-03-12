from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date
from models import UserRole, PayrollStatus, AttendanceType

# Base Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: Optional[UserRole] = UserRole.EMPLOYEE

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[date]
    gender: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    position: str
    base_salary: float = Field(gt=0)
    department_id: int

class PayrollBase(BaseModel):
    employee_id: int
    pay_period_start: date
    pay_period_end: date
    base_salary: float
    overtime_pay: float = 0.0
    deductions: float = 0.0
    tax: float = 0.0
    net_salary: float
    status: PayrollStatus = PayrollStatus.PENDING
    payment_date: Optional[date]

class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    status: AttendanceType
    check_in: Optional[datetime]
    check_out: Optional[datetime]
    work_hours: Optional[float]
    notes: Optional[str]

# Create Schemas
class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class DepartmentCreate(DepartmentBase):
    pass

class EmployeeCreate(EmployeeBase):
    hire_date: date
    user_id: Optional[int]

class PayrollCreate(PayrollBase):
    pass

class AttendanceCreate(AttendanceBase):
    pass

# Update Schemas
class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    is_active: Optional[bool]
    role: Optional[UserRole]

class DepartmentUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class EmployeeUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    position: Optional[str]
    base_salary: Optional[float] = Field(gt=0)
    department_id: Optional[int]

class PayrollUpdate(BaseModel):
    status: Optional[PayrollStatus]
    payment_date: Optional[date]
    overtime_pay: Optional[float]
    deductions: Optional[float]
    tax: Optional[float]
    net_salary: Optional[float]

class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceType]
    check_in: Optional[datetime]
    check_out: Optional[datetime]
    work_hours: Optional[float]
    notes: Optional[str]

# Response Schemas
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class EmployeeResponse(EmployeeBase):
    id: int
    user_id: Optional[int]
    hire_date: date
    created_at: datetime
    updated_at: Optional[datetime]
    department: DepartmentResponse

    class Config:
        from_attributes = True

class PayrollResponse(PayrollBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class AttendanceResponse(AttendanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# List Response Schemas
class UserList(BaseModel):
    total: int
    items: List[UserResponse]

class DepartmentList(BaseModel):
    total: int
    items: List[DepartmentResponse]

class EmployeeList(BaseModel):
    total: int
    items: List[EmployeeResponse]

class PayrollList(BaseModel):
    total: int
    items: List[PayrollResponse]

class AttendanceList(BaseModel):
    total: int
    items: List[AttendanceResponse]

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None
