from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base
from datetime import datetime

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    HR = "hr"
    EMPLOYEE = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="user", uselist=False)

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    employees = relationship("Employee", back_populates="department")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String)
    phone = Column(String)
    address = Column(String)
    hire_date = Column(Date, nullable=False)
    position = Column(String, nullable=False)
    base_salary = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="employee")
    department = relationship("Department", back_populates="employees")
    payrolls = relationship("Payroll", back_populates="employee")
    attendances = relationship("Attendance", back_populates="employee")

class PayrollStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    PAID = "paid"

class Payroll(Base):
    __tablename__ = "payrolls"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    base_salary = Column(Float, nullable=False)
    overtime_pay = Column(Float, default=0.0)
    deductions = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    net_salary = Column(Float, nullable=False)
    status = Column(Enum(PayrollStatus), default=PayrollStatus.PENDING)
    payment_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="payrolls")

class AttendanceType(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LEAVE = "leave"
    HALF_DAY = "half_day"

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceType), nullable=False)
    check_in = Column(DateTime(timezone=True))
    check_out = Column(DateTime(timezone=True))
    work_hours = Column(Float)
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="attendances")

    def calculate_work_hours(self):
        """Calculate work hours if both check_in and check_out are present"""
        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            self.work_hours = delta.total_seconds() / 3600  # Convert to hours
