from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.user import generate_uuid, utc_now

class VehicleType(Base):
    __tablename__ = "vehicle_types"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    make = Column(String(100), nullable=False, index=True)
    model = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False, default="Sedan")  # Sedan, SUV, Hatchback, Pickup, Commercial
    default_fuel_type = Column(String(50), nullable=False, default="Petrol")  # Petrol, Diesel, Hybrid, EV, CNG
    recommended_oil_interval_km = Column(Integer, nullable=False, default=5000)
    recommended_oil_interval_days = Column(Integer, nullable=False, default=180)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_driver_id = Column(String(36), ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True, index=True)
    vin = Column(String(64), nullable=True, unique=True, index=True)
    license_plate = Column(String(32), nullable=False, index=True)
    registration_province = Column(String(50), nullable=False, default="Punjab")
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    fuel_type = Column(String(50), nullable=False, default="Petrol")
    initial_odometer_km = Column(Float, nullable=False, default=0.0)
    current_odometer_km = Column(Float, nullable=False, default=0.0)
    status = Column(String(32), nullable=False, default="ACTIVE")  # ACTIVE, MAINTENANCE, INACTIVE
    photo_url = Column(String(1024), nullable=True)
    is_ad_rewarded = Column(Boolean, nullable=False, default=False)
    custom_specs = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    # Relationships
    maintenance_schedules = relationship("MaintenanceSchedule", back_populates="vehicle", cascade="all, delete-orphan")
    service_records = relationship("ServiceRecord", back_populates="vehicle", cascade="all, delete-orphan")
