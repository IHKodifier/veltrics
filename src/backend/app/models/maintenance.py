from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.user import generate_uuid, utc_now

class MaintenanceSchedule(Base):
    __tablename__ = "maintenance_schedules"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    task_name = Column(String(255), nullable=False)
    interval_km = Column(Integer, nullable=False, default=5000)
    interval_days = Column(Integer, nullable=False, default=180)
    last_performed_km = Column(Float, nullable=False, default=0.0)
    last_performed_date = Column(Date, nullable=True)
    next_due_km = Column(Float, nullable=False, default=5000.0)
    next_due_date = Column(Date, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    vehicle = relationship("Vehicle", back_populates="maintenance_schedules")
    service_records = relationship("ServiceRecord", back_populates="maintenance_schedule", cascade="all, delete-orphan")

class ServiceRecord(Base):
    __tablename__ = "service_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    maintenance_schedule_id = Column(String(36), ForeignKey("maintenance_schedules.id", ondelete="SET NULL"), nullable=True, index=True)
    service_date = Column(Date, nullable=False)
    odometer_km = Column(Float, nullable=False, default=0.0)
    total_cost = Column(Float, nullable=False, default=0.0)
    service_center_name = Column(String(255), nullable=True)
    notes = Column(String(1024), nullable=True)
    performed_by = Column(String(255), nullable=True)
    invoice_photo_url = Column(String(1024), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    vehicle = relationship("Vehicle", back_populates="service_records")
    maintenance_schedule = relationship("MaintenanceSchedule", back_populates="service_records")
