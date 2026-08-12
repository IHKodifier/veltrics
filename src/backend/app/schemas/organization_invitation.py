import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

ALLOWED_ROLES = {"admin", "manager", "driver", "viewer"}

class OrganizationInvitationCreate(BaseModel):
    email: str = Field(..., description="Recipient email address for organization invitation")
    role: str = Field(default="viewer", description="Assigned role: admin, manager, driver, or viewer")

    @field_validator("email")
    def validate_email(cls, v: str) -> str:
        email = v.strip() if v else ""
        if not email:
            raise ValueError("Email address cannot be empty")
        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email.lower()

    @field_validator("role")
    def validate_role(cls, v: str) -> str:
        role = v.strip().lower() if v else ""
        if role not in ALLOWED_ROLES:
            raise ValueError(f"Invalid role '{v}'. Allowed roles: {', '.join(sorted(ALLOWED_ROLES))}")
        return role

class OrganizationInvitationResponse(BaseModel):
    id: str
    organization_id: str
    email: str
    role: str
    token: str
    status: str
    invited_by_user_id: Optional[str] = None
    expires_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
