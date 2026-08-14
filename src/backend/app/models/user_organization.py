import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.user import generate_uuid, utc_now

class UserOrganization(Base):
    __tablename__ = "user_organizations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(32), nullable=False, default="owner")  # owner, admin, manager, driver, viewer
    status = Column(String(32), nullable=False, default="active")  # invited, active, suspended
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)

    __table_args__ = (
        UniqueConstraint("user_id", "organization_id", name="uix_user_organization"),
    )

    user = relationship("User", back_populates="org_memberships")
    organization = relationship("Organization", back_populates="members")
