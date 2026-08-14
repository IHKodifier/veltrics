from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class VendorCreateRequest(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    rating: float = 5.0

class VendorResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    rating: float
    created_at: datetime
