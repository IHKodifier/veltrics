from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.user import generate_uuid, utc_now

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    full_name = Column(String(255), nullable=False)
    license_number = Column(String(64), nullable=True)
    license_expiry_date = Column(Date, nullable=True)
    phone_number = Column(String(32), nullable=True)
    status = Column(String(32), nullable=False, default="ACTIVE")  # ACTIVE, INACTIVE, ON_LEAVE
    is_ad_rewarded = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)
