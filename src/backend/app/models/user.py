import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    firebase_uid = Column(String(128), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    phone_number = Column(String(32), nullable=True)
    city = Column(String(128), nullable=True)
    job_role = Column(String(128), nullable=True)
    photo_url = Column(String(1024), nullable=True)
    avatar_url = Column(String(1024), nullable=True)
    auth_provider = Column(String(64), nullable=False, default="google")
    linked_providers = Column(JSON, nullable=False, default=list)
    password_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_super_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    organizations = relationship("Organization", back_populates="owner", cascade="all, delete-orphan")
    org_memberships = relationship("UserOrganization", back_populates="user", cascade="all, delete-orphan")

