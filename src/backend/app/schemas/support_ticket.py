from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator

class SupportTicketCreate(BaseModel):
    category: str = "OTHER"
    description: str
    device_info: Optional[Dict[str, Any]] = None

    @field_validator("category")
    def validate_category(cls, v):
        if v is not None:
            v_upper = v.upper().strip()
            if v_upper not in ["BUG", "FEATURE_REQUEST", "BILLING", "OTHER"]:
                raise ValueError("INVALID_CATEGORY: Must be BUG, FEATURE_REQUEST, BILLING, or OTHER")
            return v_upper
        return v

    @field_validator("description")
    def validate_description(cls, v):
        if not v or not v.strip():
            raise ValueError("EMPTY_DESCRIPTION: Support ticket description cannot be empty")
        return v.strip()

class SupportTicketResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    category: str
    description: str
    device_info: Optional[Dict[str, Any]] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
