from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

SUPPORTED_CURRENCIES = {"USD", "EUR", "PKR", "GBP", "CAD", "AUD", "SAR", "AED", "JPY", "CNY", "INR", "CHF", "NZD", "SGD"}

class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the organization")
    is_personal: bool = Field(default=False, description="Whether this is a personal organization")
    max_vehicles: int = Field(default=3, ge=1, description="Maximum vehicle capacity limit")
    max_drivers: int = Field(default=3, ge=1, description="Maximum driver capacity limit")
    owner_id: Optional[str] = Field(default=None, description="User ID of owner")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Organization name cannot be empty or whitespace only.")
        return stripped

class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(default=None, description="Updated organization name")
    address: Optional[str] = Field(default=None, description="Organization physical address")
    phone: Optional[str] = Field(default=None, description="Contact phone number")
    tax_id: Optional[str] = Field(default=None, description="Tax Identification Number")
    currency: Optional[str] = Field(default=None, description="ISO 4217 Currency Code")
    website: Optional[str] = Field(default=None, description="Website URL")
    logo_url: Optional[str] = Field(default=None, description="Logo URL")

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        code = v.strip().upper()
        if code not in SUPPORTED_CURRENCIES:
            raise ValueError(f"Invalid ISO 4217 currency code '{v}'. Must be one of: {', '.join(sorted(SUPPORTED_CURRENCIES))}")
        return code

class PersonalOrganizationCreate(BaseModel):
    user_id: str = Field(..., description="ID of user for whom to auto-provision personal organization")
    user_name: Optional[str] = Field(default=None, description="Optional full name or email of user")

class OrganizationResponse(BaseModel):
    id: str
    name: str
    owner_id: Optional[str] = None
    is_personal: bool
    max_vehicles: int
    max_drivers: int
    address: Optional[str] = None
    phone: Optional[str] = None
    tax_id: Optional[str] = None
    currency: str = "USD"
    website: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SwitchOrganizationRequest(BaseModel):
    target_organization_id: str = Field(..., description="ID of organization to switch active context to")
    user_id: Optional[str] = Field(default=None, description="User ID requesting context switch")

class SwitchOrganizationResponse(BaseModel):
    message: str = Field(default="Active organization switched successfully")
    active_organization: OrganizationResponse


