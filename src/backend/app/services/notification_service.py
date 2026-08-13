from datetime import datetime
from typing import Optional, Dict
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.notification import UserDevice, AppNotification
from app.models.user import User
from app.schemas.notification import DeviceTokenCreate, NotificationPreferencesUpdate

def register_device_token(db: Session, user_id: str, payload: DeviceTokenCreate) -> UserDevice:
    device = db.query(UserDevice).filter(
        UserDevice.user_id == user_id,
        UserDevice.device_token == payload.device_token
    ).first()

    if device:
        device.device_type = payload.device_type
        device.updated_at = datetime.utcnow()
    else:
        device = UserDevice(
            user_id=user_id,
            device_token=payload.device_token,
            device_type=payload.device_type
        )
        db.add(device)

    db.commit()
    db.refresh(device)
    return device

def get_notifications(
    db: Session,
    user_id: str,
    organization_id: Optional[str] = None,
    unread_only: bool = False
) -> Dict:
    query = db.query(AppNotification).filter(
        AppNotification.user_id == user_id,
        AppNotification.deleted_at == None
    )

    if organization_id:
        query = query.filter(AppNotification.organization_id == organization_id)

    unread_count = query.filter(AppNotification.is_read == False).count()

    if unread_only:
        query = query.filter(AppNotification.is_read == False)

    notifications = query.order_by(AppNotification.created_at.desc()).all()

    return {
        "unread_count": unread_count,
        "total": len(notifications),
        "items": notifications
    }

def mark_as_read(db: Session, user_id: str, notification_id: str) -> AppNotification:
    notif = db.query(AppNotification).filter(
        AppNotification.id == notification_id,
        AppNotification.user_id == user_id,
        AppNotification.deleted_at == None
    ).first()

    if not notif:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID '{notification_id}' not found."
        )

    notif.is_read = True
    notif.read_at = datetime.utcnow()
    db.commit()
    db.refresh(notif)
    return notif

def mark_all_as_read(db: Session, user_id: str, organization_id: Optional[str] = None) -> Dict:
    query = db.query(AppNotification).filter(
        AppNotification.user_id == user_id,
        AppNotification.is_read == False,
        AppNotification.deleted_at == None
    )

    if organization_id:
        query = query.filter(AppNotification.organization_id == organization_id)

    unread = query.all()
    now = datetime.utcnow()
    for n in unread:
        n.is_read = True
        n.read_at = now

    db.commit()
    return {"message": "All notifications marked as read", "updated_count": len(unread)}

def update_notification_preferences(db: Session, user_id: str, payload: NotificationPreferencesUpdate) -> Dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found."
        )

    prefs = {
        "maintenance_reminders": payload.maintenance_reminders,
        "document_expirations": payload.document_expirations,
        "quota_alerts": payload.quota_alerts,
        "system_news": payload.system_news
    }

    return prefs
