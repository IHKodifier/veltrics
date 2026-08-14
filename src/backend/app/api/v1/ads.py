from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.ads import (
    AdRewardVerifyRequest,
    AdRewardVerifyResponse,
    EnterpriseInquiryRequest,
    EnterpriseInquiryResponse,
)
from app.services.ad_service import AdService

router = APIRouter(prefix="/ads", tags=["Monetization & Ads"])


@router.post("/verify-reward", response_model=AdRewardVerifyResponse, status_code=status.HTTP_200_OK)
def verify_ad_reward(
    payload: AdRewardVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    UC-100 & UC-120 & UC-122: Verify Rewarded Ad Completion Signature Token & Claim Bonus Quota Slot.
    Verifies AdMob SSV / HMAC signature, enforces single-use idempotency, and increments max_vehicles / max_drivers.
    """
    return AdService.verify_and_claim_ad_reward(db, current_user.id, payload)


@router.post("/enterprise-inquiry", response_model=EnterpriseInquiryResponse, status_code=status.HTTP_200_OK)
def submit_enterprise_sales_inquiry(
    payload: EnterpriseInquiryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    UC-089: Contact Enterprise Sales Inquiry Form (>25 Fleets).
    Submits custom enterprise sales inquiry for large commercial fleet pricing.
    """
    return AdService.submit_enterprise_inquiry(db, current_user.id, payload)
