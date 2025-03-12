from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

from database import get_db
from schemas import (
    PayrollCreate,
    PayrollUpdate,
    PayrollResponse,
    PayrollList
)
from models import User, Employee, PayrollStatus
from auth import get_current_active_user, check_hr_permission
import crud

router = APIRouter(
    prefix="/payroll",
    tags=["payroll"]
)

@router.post("/", response_model=PayrollResponse)
async def create_payroll(
    payroll: PayrollCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Create a new payroll record. Only HR and admin users can create payroll records.
    """
    # Verify employee exists
    employee = crud.get_employee(db, payroll.employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Validate pay period
    if payroll.pay_period_end < payroll.pay_period_start:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pay period end date must be after start date"
        )
    
    # Check for existing payroll record in the same period
    existing_payroll = db.query(crud.Payroll).filter(
        crud.Payroll.employee_id == payroll.employee_id,
        crud.Payroll.pay_period_start <= payroll.pay_period_end,
        crud.Payroll.pay_period_end >= payroll.pay_period_start
    ).first()
    
    if existing_payroll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payroll record already exists for this period"
        )
    
    return crud.create_payroll(db, payroll)

@router.get("/", response_model=PayrollList)
async def list_payrolls(
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[PayrollStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    List all payroll records with optional filtering.
    """
    payrolls = crud.get_payrolls(
        db,
        skip=skip,
        limit=limit,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date
    )
    
    # Filter by status if provided
    if status:
        payrolls = [p for p in payrolls if p.status == status]
    
    return {
        "total": len(payrolls),
        "items": payrolls
    }

@router.get("/{payroll_id}", response_model=PayrollResponse)
async def get_payroll(
    payroll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Get detailed information about a specific payroll record.
    """
    payroll = crud.get_payroll(db, payroll_id)
    if not payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll record not found"
        )
    return payroll

@router.put("/{payroll_id}", response_model=PayrollResponse)
async def update_payroll(
    payroll_id: int,
    payroll_update: PayrollUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Update a payroll record. Only HR and admin users can update payroll records.
    """
    # Verify payroll record exists
    existing_payroll = crud.get_payroll(db, payroll_id)
    if not existing_payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll record not found"
        )
    
    # Prevent updates to paid payrolls
    if existing_payroll.status == PayrollStatus.PAID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update a paid payroll record"
        )
    
    updated_payroll = crud.update_payroll(db, payroll_id, payroll_update)
    return updated_payroll

@router.delete("/{payroll_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payroll(
    payroll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Delete a payroll record. Only HR and admin users can delete payroll records.
    """
    # Verify payroll record exists
    existing_payroll = crud.get_payroll(db, payroll_id)
    if not existing_payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll record not found"
        )
    
    # Prevent deletion of paid payrolls
    if existing_payroll.status == PayrollStatus.PAID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a paid payroll record"
        )
    
    success = crud.delete_payroll(db, payroll_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete payroll record"
        )

@router.post("/{payroll_id}/process", response_model=PayrollResponse)
async def process_payroll(
    payroll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Process a payroll record, calculating final amounts and setting status to processed.
    """
    payroll = crud.get_payroll(db, payroll_id)
    if not payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll record not found"
        )
    
    if payroll.status != PayrollStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot process payroll with status {payroll.status}"
        )
    
    # Update payroll status to processed
    payroll_update = PayrollUpdate(
        status=PayrollStatus.PROCESSED,
        net_salary=payroll.base_salary + payroll.overtime_pay - payroll.deductions - payroll.tax
    )
    
    return crud.update_payroll(db, payroll_id, payroll_update)

@router.post("/{payroll_id}/pay", response_model=PayrollResponse)
async def mark_payroll_as_paid(
    payroll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_hr_permission)
):
    """
    Mark a processed payroll record as paid.
    """
    payroll = crud.get_payroll(db, payroll_id)
    if not payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll record not found"
        )
    
    if payroll.status != PayrollStatus.PROCESSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only mark processed payrolls as paid"
        )
    
    # Update payroll status to paid and set payment date
    payroll_update = PayrollUpdate(
        status=PayrollStatus.PAID,
        payment_date=date.today()
    )
    
    return crud.update_payroll(db, payroll_id, payroll_update)
