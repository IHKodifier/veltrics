from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.notification import (
    DeviceTokenCreate,
    DeviceTokenResponse,
    NotificationResponse,
    NotificationPaginatedResponse,
    NotificationPreferencesUpdate
)
from app.services import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])

def resolve_user(user_id: Optional[str] = Query(None, description="User ID query parameter")) -> str:
    return user_id or "usr-notif-072"

@router.post("/devices", response_model=DeviceTokenResponse, status_code=status.HTTP_201_CREATED)
def register_device(
    payload: DeviceTokenCreate,
    user_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    UC-072: Register FCM Device Push Token.
    """
    uid = payload.user_id or user_id or "usr-notif-072"
    return notification_service.register_device_token(
        db=db, user_id=uid, payload=payload
    )

@router.get("", response_model=NotificationPaginatedResponse)
def get_notifications(
    unread_only: bool = Query(False, description="Filter unread notifications only"),
    organization_id: Optional[str] = Query(None, description="Organization ID"),
    user_id: Optional[str] = Query(None, description="User ID"),
    db: Session = Depends(get_db)
):
    """
    UC-073: In-App Notification Center Directory & Unread Counter.
    """
    uid = resolve_user(user_id)
    return notification_service.get_notifications(
        db=db, user_id=uid, organization_id=organization_id, unread_only=unread_only
    )

@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: str,
    user_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    UC-074: Mark Notification as Read / Deep Link Routing.
    """
    uid = resolve_user(user_id)
    return notification_service.mark_as_read(
        db=db, user_id=uid, notification_id=notification_id
    )

@router.post("/mark-all-read")
def mark_all_read(
    organization_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    UC-073 (A1): Mark All Notifications as Read.
    """
    uid = resolve_user(user_id)
    return notification_service.mark_all_as_read(
        db=db, user_id=uid, organization_id=organization_id
    )

@router.patch("/preferences")
def update_preferences(
    payload: NotificationPreferencesUpdate,
    user_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    UC-075: Configure Notification Channel Preferences.
    """
    uid = payload.user_id or user_id or "usr-notif-072"
    return notification_service.update_notification_preferences(
        db=db, user_id=uid, payload=payload
    )
