from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    job_role: Optional[str] = None
    avatar_url: Optional[str] = None

    @field_validator("full_name")

    def validate_full_name(cls, v):
        if v is not None:
            v_trimmed = v.strip()
            if len(v_trimmed) < 2 or len(v_trimmed) > 50:
                raise ValueError("FULL_NAME_INVALID_LENGTH: must be between 2 and 50 characters")
            return v_trimmed
        return v

class ProfileCompletionRequest(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    job_role: Optional[str] = None
    avatar_url: Optional[str] = None

    @field_validator("full_name")

    def validate_full_name(cls, v):
        if v is not None:
            v_trimmed = v.strip()
            if len(v_trimmed) < 2 or len(v_trimmed) > 50:
                raise ValueError("FULL_NAME_INVALID_LENGTH: must be between 2 and 50 characters")
            return v_trimmed
        return v

class UserProfileResponse(BaseModel):
    id: str
    firebase_uid: str
    email: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    job_role: Optional[str] = None
    photo_url: Optional[str] = None
    avatar_url: Optional[str] = None
    auth_provider: str
    linked_providers: List[str] = []
    is_super_admin: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
