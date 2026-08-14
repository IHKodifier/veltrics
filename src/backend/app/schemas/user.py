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

class UserPreferencesDTO(BaseModel):
    theme: str = "SYSTEM"
    accent_color: str = "slate_teal"
    high_contrast: bool = False
    units: str = "METRIC"
    locale: str = "en"

class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    accent_color: Optional[str] = None
    high_contrast: Optional[bool] = None
    units: Optional[str] = None
    locale: Optional[str] = None

    @field_validator("theme")
    def validate_theme(cls, v):
        if v is not None:
            v_upper = v.upper()
            if v_upper not in ["LIGHT", "DARK", "SYSTEM"]:
                raise ValueError("INVALID_THEME: Theme must be LIGHT, DARK, or SYSTEM")
            return v_upper
        return v

    @field_validator("accent_color")
    def validate_accent_color(cls, v):
        if v is not None:
            v_lower = v.lower()
            if v_lower not in ["slate_teal", "amber_gold", "forest_green"]:
                raise ValueError("INVALID_ACCENT_COLOR: Must be slate_teal, amber_gold, or forest_green")
            return v_lower
        return v

    @field_validator("units")
    def validate_units(cls, v):
        if v is not None:
            v_upper = v.upper()
            if v_upper not in ["METRIC", "IMPERIAL"]:
                raise ValueError("INVALID_UNITS: Units must be METRIC or IMPERIAL")
            return v_upper
        return v

    @field_validator("locale")
    def validate_locale(cls, v):
        if v is not None:
            v_lower = v.lower().strip()
            if v_lower not in ["en", "ur", "ar"]:
                raise ValueError("INVALID_LOCALE: Locale must be en, ur, or ar")
            return v_lower
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
    preferences: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
