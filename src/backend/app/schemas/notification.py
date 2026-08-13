from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class DeviceTokenCreate(BaseModel):
    user_id: Optional[str] = None
    device_token: str
    device_type: str = "ANDROID"

class DeviceTokenResponse(BaseModel):
    id: str
    user_id: str
    device_token: str
    device_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationResponse(BaseModel):
    id: str
    user_id: str
    organization_id: Optional[str] = None
    title: str
    body: str
    category: str
    is_read: bool
    read_at: Optional[datetime] = None
    action_url: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationPaginatedResponse(BaseModel):
    unread_count: int
    total: int
    items: List[NotificationResponse]

class NotificationPreferencesUpdate(BaseModel):
    user_id: Optional[str] = None
    maintenance_reminders: bool = True
    document_expirations: bool = True
    quota_alerts: bool = True
    system_news: bool = True
