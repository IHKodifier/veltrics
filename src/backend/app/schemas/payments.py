from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CheckoutSessionCreate(BaseModel):
    organization_id: str
    gateway: Literal["SAFEPAY"] = "SAFEPAY"
    billing_cycle: Literal["MONTHLY", "ANNUALLY"] = "MONTHLY"


class CheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str
    gateway: str


class SubscriptionStatusResponse(BaseModel):
    organization_id: str
    tier: str
    gateway: Optional[str] = None
    status: str
    billing_cycle: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    grace_period_ends_at: Optional[datetime] = None
    cancel_at_period_end: bool = False
    max_vehicles: int
    max_drivers: int
    ad_bonus_vehicles: int
    ad_bonus_drivers: int

    model_config = ConfigDict(from_attributes=True)


class CancelSubscriptionRequest(BaseModel):
    organization_id: str
    reason: Optional[str] = None


class WebhookProcessingResponse(BaseModel):
    status: str
    event_id: Optional[str] = None
    message: str
