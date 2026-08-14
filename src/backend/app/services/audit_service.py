import logging
from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
from fastapi import Request

from app.models.audit_log import AuditLog

logger = logging.getLogger(__name__)

class AuditService:
    @staticmethod
    def log_event(
        db: Session,
        action: str,
        actor_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None
    ) -> Optional[AuditLog]:
        """
        UC-012: Audit Log Recording for Authentication Events.
        Extracts event metadata (IP address, user agent, action string, actor_id, timestamp, org_id).
        Inserts record into immutable audit_logs table.
        Operates safely (non-blocking exception handling).
        """
        try:
            event_payload = dict(payload) if payload is not None else {}

            if request is not None:
                ip_address = "127.0.0.1"
                if hasattr(request, "headers") and "x-forwarded-for" in request.headers:
                    ip_address = request.headers["x-forwarded-for"].split(",")[0].strip()
                elif hasattr(request, "client") and request.client and getattr(request.client, "host", None):
                    ip_address = request.client.host

                user_agent = "Unknown"
                if hasattr(request, "headers") and "user-agent" in request.headers:
                    user_agent = request.headers.get("user-agent", "Unknown")

                event_payload.setdefault("ip_address", ip_address)
                event_payload.setdefault("user_agent", user_agent)
            else:
                event_payload.setdefault("ip_address", "127.0.0.1")
                event_payload.setdefault("user_agent", "Internal/Service")

            audit_entry = AuditLog(
                actor_id=actor_id,
                organization_id=organization_id,
                action=action,
                payload=event_payload
            )
            db.add(audit_entry)
            db.flush()
            return audit_entry
        except Exception as e:
            logger.warning(f"Failed to record audit log for action '{action}': {e}")
            return None
