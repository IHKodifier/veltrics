import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    category = Column(String(64), nullable=False, default="OTHER")  # BUG, FEATURE_REQUEST, BILLING, OTHER
    description = Column(Text, nullable=False)
    device_info = Column(JSON, nullable=True, default=dict)
    status = Column(String(32), nullable=False, default="OPEN")  # OPEN, IN_PROGRESS, RESOLVED, CLOSED
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
