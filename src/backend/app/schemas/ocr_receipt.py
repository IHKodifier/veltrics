from typing import Optional
from pydantic import BaseModel, ConfigDict

class ReceiptOcrResponse(BaseModel):
    total_cost: Optional[float] = None
    quantity_liters: Optional[float] = None
    price_per_liter: Optional[float] = None
    station_name: Optional[str] = None
    log_date: Optional[str] = None
    confidence_score: float = 0.95
    raw_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
