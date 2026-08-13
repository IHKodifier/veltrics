from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class TripStart(BaseModel):
    vehicle_id: str
    driver_id: Optional[str] = None
    start_odometer_km: float = Field(..., ge=0)
    origin_name: Optional[str] = None
    trip_purpose: str = "BUSINESS"
    start_time: Optional[datetime] = None

class TripStop(BaseModel):
    end_odometer_km: float = Field(..., ge=0)
    destination_name: Optional[str] = None
    end_time: Optional[datetime] = None
    gps_polyline_json: Optional[str] = None
    notes: Optional[str] = None

class TripCreate(BaseModel):
    vehicle_id: str
    driver_id: Optional[str] = None
    start_odometer_km: float = Field(..., ge=0)
    end_odometer_km: Optional[float] = Field(None, ge=0)
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    trip_purpose: str = "BUSINESS"
    is_manual: bool = False
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    gps_polyline_json: Optional[str] = None
    notes: Optional[str] = None

class TripUpdate(BaseModel):
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    start_odometer_km: Optional[float] = Field(None, ge=0)
    end_odometer_km: Optional[float] = Field(None, ge=0)
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    trip_purpose: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    gps_polyline_json: Optional[str] = None
    notes: Optional[str] = None


class TripResponse(BaseModel):
    id: str
    organization_id: str
    vehicle_id: str
    driver_id: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    start_odometer_km: float
    end_odometer_km: Optional[float] = None
    distance_km: Optional[float] = None
    trip_purpose: str
    is_manual: bool
    status: str
    gps_polyline_json: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TripPaginatedResponse(BaseModel):
    items: List[TripResponse]
    total: int
    page: int
    limit: int
    pages: int

class TripSummaryResponse(BaseModel):
    vehicle_id: Optional[str] = None
    total_distance_km: float
    business_distance_km: float
    personal_distance_km: float
    total_trips_count: int
    estimated_tax_deduction: float

class QuickTripCreate(BaseModel):
    vehicle_id: str
    driver_id: Optional[str] = None
    distance_km: float = Field(..., gt=0)
    origin_name: Optional[str] = "Quick Log Start"
    destination_name: Optional[str] = "Quick Log Destination"
    trip_purpose: str = "BUSINESS"
    notes: Optional[str] = None

class MileageSummaryResponse(BaseModel):
    vehicle_id: Optional[str] = None
    total_distance_km: float
    business_distance_km: float
    personal_distance_km: float
    total_trips_count: int
    business_trips_count: int
    personal_trips_count: int
    average_trip_distance_km: float
    estimated_tax_deduction: float



