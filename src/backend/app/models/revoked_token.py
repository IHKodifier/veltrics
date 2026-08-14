from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.session import Base
from app.models.user import generate_uuid, utc_now

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    token = Column(String(512), nullable=False, unique=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    revoked_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
