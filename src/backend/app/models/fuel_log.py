from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.user import generate_uuid, utc_now

class FuelLog(Base):
    __tablename__ = "fuel_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    driver_id = Column(String(36), ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True, index=True)
    log_date = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    odometer_km = Column(Float, nullable=False, default=0.0)
    fuel_type = Column(String(32), nullable=False, default="Petrol")
    quantity_liters = Column(Float, nullable=False, default=0.0)
    price_per_liter = Column(Float, nullable=False, default=0.0)
    total_cost = Column(Float, nullable=False, default=0.0)
    currency = Column(String(3), nullable=False, default="PKR")
    station_name = Column(String(128), nullable=True)
    receipt_photo_url = Column(String(512), nullable=True)
    is_full_tank = Column(Boolean, nullable=False, default=True)
    calculated_efficiency_kpl = Column(Float, nullable=True, default=None)
    distance_km = Column(Float, nullable=True, default=None)
    is_leak_alert = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    # Relationships
    vehicle = relationship("Vehicle", backref="fuel_logs")
    driver = relationship("Driver", backref="fuel_logs")
