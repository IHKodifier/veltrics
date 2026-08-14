import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.user import generate_uuid, utc_now

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    is_personal = Column(Boolean, nullable=False, default=True)
    max_vehicles = Column(Integer, nullable=False, default=3)
    max_drivers = Column(Integer, nullable=False, default=3)
    tier = Column(String(20), nullable=False, default="free")
    ad_bonus_vehicles = Column(Integer, nullable=False, default=0)
    ad_bonus_drivers = Column(Integer, nullable=False, default=0)
    address = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    tax_id = Column(String(50), nullable=True)
    currency = Column(String(3), nullable=False, default="USD")
    website = Column(String(255), nullable=True)
    logo_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    owner = relationship("User", back_populates="organizations")
    invitations = relationship("OrganizationInvitation", back_populates="organization", cascade="all, delete-orphan")
    members = relationship("UserOrganization", back_populates="organization", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="organization", uselist=False, cascade="all, delete-orphan")


