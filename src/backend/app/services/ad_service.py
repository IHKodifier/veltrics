import hmac
import hashlib
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.organization import Organization
from app.models.audit_log import AuditLog
from app.models.user import generate_uuid
from app.schemas.ads import (
    AdRewardVerifyRequest,
    AdRewardVerifyResponse,
    EnterpriseInquiryRequest,
    EnterpriseInquiryResponse,
)

ADMOB_SECRET = "test_admob_ssv_secret_key"


class AdService:
    @staticmethod
    def verify_and_claim_ad_reward(db: Session, user_id: str, payload: AdRewardVerifyRequest) -> AdRewardVerifyResponse:
        # 1. Validate HMAC signature (AdMob SSV / HMAC security protocol UC-122)
        message = f"{payload.admob_ssv_token}:{payload.reward_type}:{payload.organization_id}".encode("utf-8")
        expected_sig = hmac.new(ADMOB_SECRET.encode("utf-8"), message, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected_sig, payload.signature):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="INVALID_AD_SIGNATURE: Ad completion signature verification failed.",
            )

        # 2. Token replay check via AuditLog idempotency
        existing_logs = db.query(AuditLog).filter(
            AuditLog.action == "AD_REWARD_CLAIMED",
        ).all()
        for log in existing_logs:
            if isinstance(log.payload, dict) and log.payload.get("token") == payload.admob_ssv_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="AD_TOKEN_ALREADY_USED: Ad reward completion token has already been redeemed.",
                )

        # 3. Retrieve Organization
        org = db.query(Organization).filter(Organization.id == payload.organization_id, Organization.deleted_at.is_(None)).first()
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")

        # 4. Increment bonus slot & update max quota (UC-100 & UC-120)
        if payload.reward_type == "vehicle_slot":
            org.ad_bonus_vehicles = (org.ad_bonus_vehicles or 0) + 1
            org.max_vehicles = 25 if org.tier == "pro" else (3 + org.ad_bonus_vehicles)
            new_bonus = org.ad_bonus_vehicles
            new_max = org.max_vehicles
        elif payload.reward_type == "driver_slot":
            org.ad_bonus_drivers = (org.ad_bonus_drivers or 0) + 1
            org.max_drivers = 15 if org.tier == "pro" else (3 + org.ad_bonus_drivers)
            new_bonus = org.ad_bonus_drivers
            new_max = org.max_drivers
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported reward_type")

        audit = AuditLog(
            organization_id=org.id,
            actor_id=user_id,
            action="AD_REWARD_CLAIMED",
            payload={
                "token": payload.admob_ssv_token,
                "reward_type": payload.reward_type,
                "new_ad_bonus_slots": new_bonus,
                "new_max_quota": new_max,
            },
        )
        db.add(audit)
        db.commit()

        return AdRewardVerifyResponse(
            status="success",
            reward_type=payload.reward_type,
            new_ad_bonus_slots=new_bonus,
            new_max_quota=new_max,
        )

    @staticmethod
    def submit_enterprise_inquiry(db: Session, user_id: str, payload: EnterpriseInquiryRequest) -> EnterpriseInquiryResponse:
        org = db.query(Organization).filter(Organization.id == payload.organization_id, Organization.deleted_at.is_(None)).first()
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")

        inquiry_id = generate_uuid()
        now = datetime.now(timezone.utc)

        audit = AuditLog(
            organization_id=org.id,
            actor_id=user_id,
            action="ENTERPRISE_SALES_INQUIRY",
            payload={
                "inquiry_id": inquiry_id,
                "contact_name": payload.contact_name,
                "email": payload.email,
                "phone": payload.phone,
                "fleet_size": payload.fleet_size,
                "message": payload.message,
                "submitted_at": now.isoformat(),
            },
        )
        db.add(audit)
        db.commit()

        return EnterpriseInquiryResponse(
            inquiry_id=inquiry_id,
            status="submitted",
            submitted_at=now,
        )
