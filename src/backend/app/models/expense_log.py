from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.user import generate_uuid, utc_now

class ExpenseLog(Base):
    __tablename__ = "expense_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    fuel_log_id = Column(String(36), ForeignKey("fuel_logs.id", ondelete="SET NULL"), nullable=True, index=True)
    category = Column(String(32), nullable=False, default="FUEL")  # FUEL, tax, insurance, toll, permit, fine, washing, other
    amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(3), nullable=False, default="PKR")
    expense_date = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    receipt_photo_url = Column(String(512), nullable=True)
    notes = Column(String(1024), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    # Relationships
    vehicle = relationship("Vehicle", backref="expense_logs")
    fuel_log = relationship("FuelLog", backref="expense_logs")
