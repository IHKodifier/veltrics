from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ExpenseLogCreate(BaseModel):
    vehicle_id: str
    category: str = "OTHER"
    amount: float = Field(..., gt=0)
    currency: str = "PKR"
    expense_date: Optional[datetime] = None
    receipt_photo_url: Optional[str] = None
    notes: Optional[str] = None

class ExpenseLogResponse(BaseModel):
    id: str
    organization_id: str
    vehicle_id: str
    fuel_log_id: Optional[str] = None
    category: str
    amount: float
    currency: str
    expense_date: datetime
    receipt_photo_url: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ExpensePaginatedResponse(BaseModel):
    items: List[ExpenseLogResponse]
    total: int
    page: int
    limit: int
    pages: int

class ExpenseSummaryResponse(BaseModel):
    vehicle_id: Optional[str] = None
    total_expense_amount: float
    total_expenses_count: int
    category_breakdown: Dict[str, float]

class ExpenseLogUpdate(BaseModel):
    vehicle_id: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = None
    expense_date: Optional[datetime] = None
    receipt_photo_url: Optional[str] = None
    notes: Optional[str] = None

class QuickExpenseCreate(BaseModel):
    vehicle_id: str
    category: str = "OTHER"
    amount: float = Field(..., gt=0)
    currency: str = "PKR"
    notes: Optional[str] = None



