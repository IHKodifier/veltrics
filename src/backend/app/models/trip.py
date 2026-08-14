import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Text
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Trip(Base):
    __tablename__ = "trips"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=False, index=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.id"), nullable=False, index=True)
    driver_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)

    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    origin_name = Column(String(255), nullable=True)
    destination_name = Column(String(255), nullable=True)

    start_odometer_km = Column(Float, nullable=False)
    end_odometer_km = Column(Float, nullable=True)
    distance_km = Column(Float, nullable=True)

    trip_purpose = Column(String(50), nullable=False, default="BUSINESS")
    is_manual = Column(Boolean, nullable=False, default=False)
    status = Column(String(50), nullable=False, default="IN_PROGRESS")

    gps_polyline_json = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
