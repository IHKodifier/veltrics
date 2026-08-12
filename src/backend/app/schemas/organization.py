from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

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
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SwitchOrganizationRequest(BaseModel):
    target_organization_id: str = Field(..., description="ID of organization to switch active context to")
    user_id: Optional[str] = Field(default=None, description="User ID requesting context switch")

class SwitchOrganizationResponse(BaseModel):
    message: str = Field(default="Active organization switched successfully")
    active_organization: OrganizationResponse

