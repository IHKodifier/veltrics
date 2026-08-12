from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from app.db.session import Base
from app.models.user import generate_uuid, utc_now

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    refresh_token = Column(String(512), nullable=False, unique=True, index=True)
    device_model = Column(String(100), nullable=True, default="Unknown Device")
    os_name = Column(String(100), nullable=True, default="Unknown OS")
    ip_address = Column(String(45), nullable=True, default="127.0.0.1")
    user_agent = Column(String(255), nullable=True, default="Unknown")
    is_revoked = Column(Boolean, nullable=False, default=False)
    last_active_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
