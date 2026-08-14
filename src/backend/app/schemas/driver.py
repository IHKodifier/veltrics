from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class DriverCreateRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: Optional[str] = Field(None, max_length=32)
    phone_number: Optional[str] = Field(None, max_length=32)
    license_number: Optional[str] = Field(None, max_length=64)
    license_expiry_date: Optional[date] = None


class DriverResponse(BaseModel):
    id: str
    organization_id: str
    full_name: str
    phone_number: Optional[str] = None
    license_number: Optional[str] = None
    status: str = "ACTIVE"
    is_ad_rewarded: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
