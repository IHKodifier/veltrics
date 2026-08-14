import hmac
import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.subscription import Subscription
from app.models.user_organization import UserOrganization
from app.models.audit_log import AuditLog
from app.schemas.payments import (
    CheckoutSessionCreate,
    CheckoutSessionResponse,
    SubscriptionStatusResponse,
    CancelSubscriptionRequest,
    WebhookProcessingResponse,
)

SAFEPAY_SECRET_KEY = "test_safepay_secret_key"


def verify_safepay_signature(raw_body: bytes, signature_header: Optional[str]) -> bool:
    if not signature_header:
        return False
    expected_sig = hmac.new(SAFEPAY_SECRET_KEY.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_sig, signature_header)


class PaymentService:
    @staticmethod
    def create_checkout_session(db: Session, user_id: str, payload: CheckoutSessionCreate) -> CheckoutSessionResponse:
        org = db.query(Organization).filter(Organization.id == payload.organization_id, Organization.deleted_at.is_(None)).first()
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")

        # Check ownership
        user_org = db.query(UserOrganization).filter(
            UserOrganization.user_id == user_id,
            UserOrganization.organization_id == org.id,
        ).first()
        if not user_org or (org.owner_id != user_id and user_org.role != "OWNER"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only organization owner can initiate subscription checkout.")

        sub = db.query(Subscription).filter(Subscription.organization_id == org.id).first()
        if sub:
            if sub.status == "ACTIVE" and not sub.cancel_at_period_end:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization already has an active Pro subscription.")
            sub.status = "PENDING"
            sub.gateway = payload.gateway
            sub.billing_cycle = payload.billing_cycle
        else:
            sub = Subscription(
                organization_id=org.id,
                gateway=payload.gateway,
                status="PENDING",
                billing_cycle=payload.billing_cycle,
            )
            db.add(sub)

        db.commit()
        db.refresh(sub)

        checkout_url = f"https://sandbox.api.safepay.com/checkout/pay?tracker={sub.id}"

        return CheckoutSessionResponse(
            checkout_url=checkout_url,
            session_id=sub.id,
            gateway="SAFEPAY",
        )

    @staticmethod
    def reconcile_safepay_webhook(db: Session, raw_body: bytes, signature_header: Optional[str]) -> WebhookProcessingResponse:
        if not verify_safepay_signature(raw_body, signature_header):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Safepay webhook signature.")

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON payload.")

        event_id = payload.get("event_id") or payload.get("tracker_id") or f"evt_{datetime.now(timezone.utc).timestamp()}"
        event_type = payload.get("event_type", "payment.completed")
        org_id = payload.get("organization_id")

        # Idempotency check via audit logs
        existing_logs = db.query(AuditLog).filter(
            AuditLog.action == "WEBHOOK_PROCESSED",
        ).all()
        for log in existing_logs:
            if isinstance(log.payload, dict) and log.payload.get("event_id") == event_id:
                return WebhookProcessingResponse(
                    status="success",
                    event_id=event_id,
                    message="Event already processed",
                )

        if event_type in ["payment.completed", "invoice.payment_succeeded"]:
            if not org_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing organization_id in webhook payload.")

            org = db.query(Organization).filter(Organization.id == org_id).first()
            if not org:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")

            sub = db.query(Subscription).filter(Subscription.organization_id == org_id).first()
            now = datetime.now(timezone.utc)
            period_days = 365 if (sub and sub.billing_cycle == "ANNUALLY") else 30

            if not sub:
                sub = Subscription(
                    organization_id=org_id,
                    gateway="SAFEPAY",
                    status="ACTIVE",
                    billing_cycle="MONTHLY",
                    current_period_start=now,
                    current_period_end=now + timedelta(days=period_days),
                    gateway_payload=payload,
                )
                db.add(sub)
            else:
                sub.status = "ACTIVE"
                sub.gateway = "SAFEPAY"
                sub.current_period_start = now
                sub.current_period_end = now + timedelta(days=period_days)
                sub.grace_period_ends_at = None
                sub.cancel_at_period_end = False
                sub.gateway_payload = payload

            # Upgrade organization entitlements
            org.tier = "pro"
            org.max_vehicles = 25
            org.max_drivers = 15

            audit = AuditLog(
                organization_id=org_id,
                action="SUBSCRIPTION_ACTIVATED",
                payload={"event_id": event_id, "details": "Subscription activated via Safepay"},
            )
            db.add(audit)

            webhook_audit = AuditLog(
                organization_id=org_id,
                action="WEBHOOK_PROCESSED",
                payload={"event_id": event_id, "type": event_type},
            )
            db.add(webhook_audit)

            db.commit()

            return WebhookProcessingResponse(
                status="success",
                event_id=event_id,
                message="Subscription activated successfully",
            )

        elif event_type in ["payment.failed"]:
            if org_id:
                sub = db.query(Subscription).filter(Subscription.organization_id == org_id).first()
                if sub and sub.status == "ACTIVE":
                    sub.status = "PAST_DUE"
                    sub.grace_period_ends_at = datetime.now(timezone.utc) + timedelta(days=7)

                webhook_audit = AuditLog(
                    organization_id=org_id,
                    action="WEBHOOK_PROCESSED",
                    payload={"event_id": event_id, "details": "Processed Safepay payment failure"},
                )
                db.add(webhook_audit)
                db.commit()

            return WebhookProcessingResponse(
                status="success",
                event_id=event_id,
                message="Payment failure handled",
            )

        else:
            # Unrecognized event type
            if org_id:
                webhook_audit = AuditLog(
                    organization_id=org_id,
                    action="WEBHOOK_PROCESSED",
                    payload={"event_id": event_id, "type": event_type, "ignored": True},
                )
                db.add(webhook_audit)
                db.commit()

            return WebhookProcessingResponse(
                status="success",
                event_id=event_id,
                message=f"Ignored unrecognized event type: {event_type}",
            )

    @staticmethod
    def get_subscription_status(db: Session, user_id: str, org_id: str) -> SubscriptionStatusResponse:
        org = db.query(Organization).filter(Organization.id == org_id, Organization.deleted_at.is_(None)).first()
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")

        sub = db.query(Subscription).filter(Subscription.organization_id == org_id).first()
        if not sub:
            return SubscriptionStatusResponse(
                organization_id=org.id,
                tier=org.tier,
                gateway="SAFEPAY",
                status="NO_SUBSCRIPTION",
                max_vehicles=org.max_vehicles,
                max_drivers=org.max_drivers,
                ad_bonus_vehicles=org.ad_bonus_vehicles,
                ad_bonus_drivers=org.ad_bonus_drivers,
            )

        return SubscriptionStatusResponse(
            organization_id=org.id,
            tier=org.tier,
            gateway=sub.gateway,
            status=sub.status,
            billing_cycle=sub.billing_cycle,
            current_period_start=sub.current_period_start,
            current_period_end=sub.current_period_end,
            grace_period_ends_at=sub.grace_period_ends_at,
            cancel_at_period_end=sub.cancel_at_period_end,
            max_vehicles=org.max_vehicles,
            max_drivers=org.max_drivers,
            ad_bonus_vehicles=org.ad_bonus_vehicles,
            ad_bonus_drivers=org.ad_bonus_drivers,
        )

    @staticmethod
    def cancel_subscription(db: Session, user_id: str, payload: CancelSubscriptionRequest) -> SubscriptionStatusResponse:
        org = db.query(Organization).filter(Organization.id == payload.organization_id, Organization.deleted_at.is_(None)).first()
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")

        user_org = db.query(UserOrganization).filter(
            UserOrganization.user_id == user_id,
            UserOrganization.organization_id == org.id,
        ).first()
        if not user_org or (org.owner_id != user_id and user_org.role != "OWNER"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only organization owner can cancel subscription.")

        sub = db.query(Subscription).filter(Subscription.organization_id == org.id).first()
        if not sub or sub.status != "ACTIVE" or sub.cancel_at_period_end:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active subscription to cancel or already canceled.")

        sub.cancel_at_period_end = True

        audit = AuditLog(
            organization_id=org.id,
            actor_id=user_id,
            action="SUBSCRIPTION_CANCELED",
            payload={"reason": payload.reason or "N/A", "period_end": sub.current_period_end.isoformat() if sub.current_period_end else None},
        )
        db.add(audit)

        db.commit()
        db.refresh(sub)

        return PaymentService.get_subscription_status(db, user_id, org.id)

    @staticmethod
    def execute_downgrade_protocol(db: Session) -> Dict[str, List[str]]:
        now = datetime.now(timezone.utc)
        downgraded_ids = []

        # Find subscriptions due for downgrade
        subs_to_downgrade = db.query(Subscription).filter(
            ((Subscription.cancel_at_period_end.is_(True)) & (Subscription.current_period_end <= now))
            | ((Subscription.status == "PAST_DUE") & (Subscription.grace_period_ends_at <= now))
        ).all()

        for sub in subs_to_downgrade:
            sub.status = "CANCELED"
            org = db.query(Organization).filter(Organization.id == sub.organization_id).first()
            if org:
                org.tier = "free"
                # Preserve bonus quota rule (UC-120): base 3 + ad bonus slots
                org.max_vehicles = 3 + org.ad_bonus_vehicles
                org.max_drivers = 3 + org.ad_bonus_drivers

                audit = AuditLog(
                    organization_id=org.id,
                    action="SUBSCRIPTION_DOWNGRADED",
                    payload={"max_vehicles": org.max_vehicles, "ad_bonus_vehicles": org.ad_bonus_vehicles},
                )
                db.add(audit)
                downgraded_ids.append(org.id)

        db.commit()
        return {"downgraded_organizations": downgraded_ids}
