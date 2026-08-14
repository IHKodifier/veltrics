from fastapi import APIRouter, Depends, Request, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.payments import (
    CheckoutSessionCreate,
    CheckoutSessionResponse,
    SubscriptionStatusResponse,
    CancelSubscriptionRequest,
    WebhookProcessingResponse,
)
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments & Subscriptions"])


@router.post("/checkout-session", response_model=CheckoutSessionResponse)
def create_checkout_session(
    payload: CheckoutSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """UC-080: Initiate Pro Subscription Checkout (Safepay)"""
    return PaymentService.create_checkout_session(db, current_user.id, payload)


@router.post("/webhooks/safepay", response_model=WebhookProcessingResponse)
async def safepay_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_safepay_signature: Optional[str] = Header(None, alias="X-Safepay-Signature"),
):
    """UC-081, UC-082 & UC-121: Safepay Webhook Processing & Reconciliation Engine"""
    raw_body = await request.body()
    return PaymentService.reconcile_safepay_webhook(db, raw_body, x_safepay_signature)


@router.get("/subscription-status", response_model=SubscriptionStatusResponse)
def get_subscription_status(
    organization_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """UC-083: View Subscription Status & Billing History"""
    return PaymentService.get_subscription_status(db, current_user.id, organization_id)


@router.post("/cancel-subscription", response_model=SubscriptionStatusResponse)
def cancel_subscription(
    payload: CancelSubscriptionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """UC-084: Cancel Active Subscription"""
    return PaymentService.cancel_subscription(db, current_user.id, payload)


@router.post("/process-downgrades")
def process_downgrades(
    db: Session = Depends(get_db),
):
    """UC-085 & UC-120: Process Pro-to-Free Subscription Downgrades & Preserved Quotas"""
    return PaymentService.execute_downgrade_protocol(db)
