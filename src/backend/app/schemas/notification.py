from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class NotificationItemResponse(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    category: str = "GENERAL"
    is_read: bool = False
    created_at: datetime

class NotificationPreferenceDTO(BaseModel):
    push_enabled: bool = True
    email_enabled: bool = True
    maintenance_alerts: bool = True
    billing_alerts: bool = True

class BillingAlertCreateRequest(BaseModel):
    alert_type: str
    message: str

class BillingAlertResponse(BaseModel):
    id: str
    alert_type: str
    message: str
    created_at: datetime

class PurgeTokenResponse(BaseModel):
    status: str = "success"
    purged_count: int
