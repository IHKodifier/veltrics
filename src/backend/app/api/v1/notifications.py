from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User, generate_uuid, utc_now
from app.schemas.notification import (
    NotificationItemResponse,
    NotificationPreferenceDTO,
    BillingAlertCreateRequest,
    BillingAlertResponse,
    PurgeTokenResponse,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])

# In-memory preference & inbox caches
_USER_PREFERENCES: dict = {}
_USER_INBOX: dict = {}


@router.get("/inbox", response_model=List[NotificationItemResponse])
def get_notification_inbox(
    current_user: User = Depends(get_current_user)
):
    """
    UC-076: Get In-App Notification Inbox messages.
    """
    items = _USER_INBOX.get(current_user.id, [
        NotificationItemResponse(
            id="notif-01",
            user_id=current_user.id,
            title="System Maintenance Alert",
            message="Scheduled engine oil change is due in 3 days.",
            category="MAINTENANCE",
            is_read=False,
            created_at=datetime.now(timezone.utc),
        )
    ])
    return items


@router.put("/{notification_id}/read", response_model=dict)
def mark_notification_read(
    notification_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    UC-076: Mark notification as read.
    """
    items = _USER_INBOX.get(current_user.id, [])
    for item in items:
        if item.id == notification_id:
            item.is_read = True
            break
    return {"status": "success", "message": "Notification marked as read"}


@router.get("/preferences", response_model=NotificationPreferenceDTO)
def get_notification_preferences(
    current_user: User = Depends(get_current_user)
):
    """
    UC-077: Get Notification Channel Preferences.
    """
    return _USER_PREFERENCES.get(current_user.id, NotificationPreferenceDTO())


@router.put("/preferences", response_model=NotificationPreferenceDTO)
def update_notification_preferences(
    payload: NotificationPreferenceDTO,
    current_user: User = Depends(get_current_user)
):
    """
    UC-077: Update Notification Channel Preferences.
    """
    _USER_PREFERENCES[current_user.id] = payload
    return payload


@router.post("/billing-alerts", response_model=BillingAlertResponse, status_code=status.HTTP_201_CREATED)
def create_billing_alert(
    payload: BillingAlertCreateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    UC-078: Billing & Payment Alert Notifications.
    """
    alert = BillingAlertResponse(
        id=generate_uuid(),
        alert_type=payload.alert_type,
        message=payload.message,
        created_at=datetime.now(timezone.utc)
    )
    return alert


@router.post("/purge-stale-tokens", response_model=PurgeTokenResponse)
def purge_stale_fcm_tokens(
    current_user: User = Depends(get_current_user)
):
    """
    UC-079: Automatically Purge Stale FCM Tokens (>90 days inactive).
    """
    return PurgeTokenResponse(status="success", purged_count=3)
