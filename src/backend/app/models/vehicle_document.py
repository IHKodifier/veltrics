from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.user import generate_uuid, utc_now

class VehicleDocument(Base):
    __tablename__ = "vehicle_documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    vehicle_id = Column(String(36), ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    document_type = Column(String(50), nullable=False, default="REGISTRATION")  # REGISTRATION, INSURANCE, PERMIT, OTHER
    document_url = Column(String(1024), nullable=False)
    file_name = Column(String(255), nullable=True)
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    vehicle = relationship("Vehicle", back_populates="documents")
