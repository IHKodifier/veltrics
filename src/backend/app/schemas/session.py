from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSessionDTO(BaseModel):
    id: str
    user_id: str
    device_model: str
    os_name: str
    ip_address: str
    user_agent: str
    last_active_at: datetime
    created_at: datetime
    is_current: bool = False

    class Config:
        from_attributes = True

class SessionRevokeResponse(BaseModel):
    message: str
    revoked_session_id: Optional[str] = None
    revoked_count: int = 1
