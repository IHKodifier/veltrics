from datetime import datetime
from typing import Optional
from pydantic import BaseModel

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

    class Config:
        orm_mode = True
