import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

ALLOWED_ROLES = {"admin", "manager", "driver", "viewer"}

class OrganizationInvitationCreate(BaseModel):
    email: Optional[str] = Field(default=None, description="Recipient email address for organization invitation")
    phone: Optional[str] = Field(default=None, description="Recipient phone number for organization invitation")
    role: str = Field(default="viewer", description="Assigned role: admin, manager, driver, or viewer")

    @field_validator("email")

    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        email = v.strip()
        if not email:
            return None
        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email.lower()

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        role = v.strip().lower() if v else ""
        if role not in ALLOWED_ROLES:
            raise ValueError(f"Invalid role '{v}'. Allowed roles: {', '.join(sorted(ALLOWED_ROLES))}")
        return role

class OrganizationInvitationRedeem(BaseModel):
    invitation_code: str = Field(..., description="Invitation token or code to redeem")
    user_id: str = Field(..., description="ID of user redeeming the invitation")

class RedeemInvitationResponse(BaseModel):
    message: str = Field(default="Invitation redeemed successfully")
    organization_id: str
    role: str
    status: str = Field(default="active")

class OrganizationInvitationResponse(BaseModel):
    id: str
    organization_id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: str
    token: str
    status: str
    invited_by_user_id: Optional[str] = None
    expires_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

