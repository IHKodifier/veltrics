from typing import List, Optional
from pydantic import BaseModel

class CostBreakdownItem(BaseModel):
    period: str
    fuel_cost: float
    maintenance_cost: float
    other_expense_cost: float
    total_cost: float

class CostBreakdownResponse(BaseModel):
    timeframe: str
    vehicle_id: Optional[str] = None
    total_fuel_cost: float
    total_maintenance_cost: float
    total_other_expense_cost: float
    grand_total_cost: float
    items: List[CostBreakdownItem]
