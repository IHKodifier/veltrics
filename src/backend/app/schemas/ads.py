from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class AdRewardVerifyRequest(BaseModel):
    organization_id: str = Field(..., description="Organization target for ad reward")
    reward_type: Literal["vehicle_slot", "driver_slot"] = Field(..., description="Type of slot unlocked by rewarded ad")
    admob_ssv_token: str = Field(..., description="Unique completion token or AdMob SSV token")
    signature: str = Field(..., description="HMAC SHA-256 signature validating completion")


class AdRewardVerifyResponse(BaseModel):
    status: str = Field("success", description="Verification status")
    reward_type: str = Field(..., description="Claimed reward slot type")
    new_ad_bonus_slots: int = Field(..., description="Updated total bonus slots earned via ads")
    new_max_quota: int = Field(..., description="Updated total organization slot quota")


class EnterpriseInquiryRequest(BaseModel):
    organization_id: str = Field(..., description="Organization submitting inquiry")
    contact_name: str = Field(..., description="Full name of contact person")
    email: str = Field(..., description="Contact email address")
    phone: Optional[str] = Field(None, description="Contact phone number")
    fleet_size: int = Field(..., ge=1, description="Estimated fleet size requiring custom enterprise plan")
    message: Optional[str] = Field(None, description="Optional custom inquiry message")


class EnterpriseInquiryResponse(BaseModel):
    inquiry_id: str = Field(..., description="Generated enterprise inquiry tracking ID")
    status: str = Field("submitted", description="Submission status")
    submitted_at: datetime = Field(..., description="Timestamp of submission")
