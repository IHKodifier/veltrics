from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class InspectionCreateRequest(BaseModel):
    vehicle_id: str
    inspection_type: str = "PRE_TRIP"
    overall_status: str = "PASSED"
    items_json: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class InspectionResponse(BaseModel):
    id: str
    organization_id: str
    vehicle_id: str
    inspector_id: Optional[str] = None
    inspection_type: str
    overall_status: str
    items_json: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
