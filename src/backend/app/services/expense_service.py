from typing import List, Optional, Tuple
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.models.expense_log import ExpenseLog
from app.schemas.expense_log import ExpenseLogCreate, ExpenseLogUpdate, QuickExpenseCreate

def log_expense(db: Session, organization_id: str, payload: ExpenseLogCreate) -> ExpenseLog:
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == payload.vehicle_id,
        Vehicle.organization_id == organization_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID '{payload.vehicle_id}' not found."
        )

    expense = ExpenseLog(
        organization_id=organization_id,
        vehicle_id=payload.vehicle_id,
        category=payload.category.upper(),
        amount=payload.amount,
        currency=payload.currency,
        expense_date=payload.expense_date or datetime.utcnow(),
        receipt_photo_url=payload.receipt_photo_url,
        notes=payload.notes
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_expenses(
    db: Session,
    organization_id: str,
    vehicle_id: Optional[str] = None,
    category: Optional[str] = None,
    page: Optional[int] = None,
    limit: Optional[int] = None
) -> Tuple[List[ExpenseLog], int]:
    query = db.query(ExpenseLog).filter(
        ExpenseLog.organization_id == organization_id,
        ExpenseLog.deleted_at == None
    )

    if vehicle_id:
        query = query.filter(ExpenseLog.vehicle_id == vehicle_id)
    if category:
        query = query.filter(ExpenseLog.category == category.upper())

    total = query.count()
    query = query.order_by(ExpenseLog.expense_date.desc())

    if page and limit:
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()
    else:
        items = query.all()

    return items, total

def get_expense_summary(
    db: Session,
    organization_id: str,
    vehicle_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> dict:
    query = db.query(ExpenseLog).filter(
        ExpenseLog.organization_id == organization_id,
        ExpenseLog.deleted_at == None
    )

    if vehicle_id:
        query = query.filter(ExpenseLog.vehicle_id == vehicle_id)
    if start_date:
        query = query.filter(ExpenseLog.expense_date >= start_date)
    if end_date:
        query = query.filter(ExpenseLog.expense_date <= end_date)

    expenses = query.all()

    total_amount = sum(e.amount for e in expenses)
    category_breakdown = {}
    for e in expenses:
        cat = e.category.upper()
        category_breakdown[cat] = category_breakdown.get(cat, 0.0) + e.amount

    return {
        "vehicle_id": vehicle_id,
        "total_expense_amount": round(total_amount, 2),
        "total_expenses_count": len(expenses),
        "category_breakdown": {k: round(v, 2) for k, v in category_breakdown.items()}
    }

def update_expense(db: Session, organization_id: str, expense_id: str, payload: ExpenseLogUpdate) -> ExpenseLog:
    expense = db.query(ExpenseLog).filter(
        ExpenseLog.id == expense_id,
        ExpenseLog.organization_id == organization_id,
        ExpenseLog.deleted_at == None
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense entry with ID '{expense_id}' not found."
        )

    if payload.vehicle_id is not None:
        expense.vehicle_id = payload.vehicle_id
    if payload.category is not None:
        expense.category = payload.category.upper()
    if payload.amount is not None:
        expense.amount = payload.amount
    if payload.currency is not None:
        expense.currency = payload.currency
    if payload.expense_date is not None:
        expense.expense_date = payload.expense_date
    if payload.receipt_photo_url is not None:
        expense.receipt_photo_url = payload.receipt_photo_url
    if payload.notes is not None:
        expense.notes = payload.notes

    db.commit()
    db.refresh(expense)
    return expense

def delete_expense(db: Session, organization_id: str, expense_id: str) -> dict:
    expense = db.query(ExpenseLog).filter(
        ExpenseLog.id == expense_id,
        ExpenseLog.organization_id == organization_id,
        ExpenseLog.deleted_at == None
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense entry with ID '{expense_id}' not found."
        )

    expense.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "Expense record deleted successfully"}

def quick_log_expense(db: Session, organization_id: str, payload: QuickExpenseCreate) -> ExpenseLog:
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == payload.vehicle_id,
        Vehicle.organization_id == organization_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID '{payload.vehicle_id}' not found."
        )

    expense = ExpenseLog(
        organization_id=organization_id,
        vehicle_id=payload.vehicle_id,
        category=payload.category.upper(),
        amount=payload.amount,
        currency=payload.currency,
        expense_date=datetime.utcnow(),
        notes=payload.notes
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense



