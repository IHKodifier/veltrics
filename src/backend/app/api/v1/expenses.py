from datetime import datetime
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.organization import Organization
from app.schemas.expense_log import ExpenseLogCreate, ExpenseLogResponse, ExpensePaginatedResponse, ExpenseSummaryResponse, ExpenseLogUpdate, QuickExpenseCreate
from app.services import expense_service

router = APIRouter(prefix="/expenses", tags=["Expenses"])

def resolve_organization(db: Session, org_id: Optional[str] = None) -> str:
    if org_id:
        org = db.query(Organization).filter(Organization.id == org_id, Organization.deleted_at == None).first()
        if org:
            return org.id
    first_org = db.query(Organization).filter(Organization.deleted_at == None).first()
    if first_org:
        return first_org.id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active organization found.")

@router.post("", response_model=ExpenseLogResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=ExpenseLogResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_expense(
    payload: ExpenseLogCreate,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-058: Log General Fleet Expense.
    """
    org_id = resolve_organization(db, organization_id)
    return expense_service.log_expense(db=db, organization_id=org_id, payload=payload)

@router.get("/summary", response_model=ExpenseSummaryResponse)
def get_expense_summary(
    vehicle_id: Optional[str] = Query(None, description="Filter expenses by vehicle ID"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-059: Expense Category & Cost Summary Metrics.
    """
    org_id = resolve_organization(db, organization_id)
    return expense_service.get_expense_summary(
        db=db,
        organization_id=org_id,
        vehicle_id=vehicle_id,
        start_date=start_date,
        end_date=end_date
    )

@router.get("", response_model=Union[List[ExpenseLogResponse], ExpensePaginatedResponse])
@router.get("/", include_in_schema=False)
def list_expenses(
    vehicle_id: Optional[str] = Query(None, description="Filter expenses by vehicle ID"),
    category: Optional[str] = Query(None, description="Filter expenses by category"),
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    page: Optional[int] = Query(None, description="Page number for pagination"),
    limit: Optional[int] = Query(None, description="Items per page"),
    paginated: bool = Query(False, description="Set to true for paginated wrapper format"),
    db: Session = Depends(get_db)
):
    """
    UC-059: View Expense History.
    """
    org_id = resolve_organization(db, organization_id)
    if paginated or (page is not None and limit is not None):
        p_page = page or 1
        p_limit = limit or 20
        items, total = expense_service.get_expenses(
            db=db, organization_id=org_id, vehicle_id=vehicle_id, category=category, page=p_page, limit=p_limit
        )
        pages = (total + p_limit - 1) // p_limit if p_limit > 0 else 1
        if paginated:
            return {
                "items": items,
                "total": total,
                "page": p_page,
                "limit": p_limit,
                "pages": pages
            }
        return items
    items, _ = expense_service.get_expenses(db=db, organization_id=org_id, vehicle_id=vehicle_id, category=category)
    return items

@router.patch("/{expense_id}", response_model=ExpenseLogResponse)
def update_expense(
    expense_id: str,
    payload: ExpenseLogUpdate,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-060: Edit Expense Entry.
    """
    org_id = resolve_organization(db, organization_id)
    return expense_service.update_expense(
        db=db, organization_id=org_id, expense_id=expense_id, payload=payload
    )

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: str,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-061: Soft Delete Expense Entry.
    """
    org_id = resolve_organization(db, organization_id)
    return expense_service.delete_expense(
        db=db, organization_id=org_id, expense_id=expense_id
    )

@router.post("/quick", response_model=ExpenseLogResponse, status_code=status.HTTP_201_CREATED)
def quick_create_expense(
    payload: QuickExpenseCreate,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-062: Quick-Log Expense from Dashboard.
    """
    org_id = resolve_organization(db, organization_id)
    return expense_service.quick_log_expense(
        db=db, organization_id=org_id, payload=payload
    )


