from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict

class VehicleTypeResponse(BaseModel):
    id: str
    make: str
    model: str
    category: str
    default_fuel_type: str
    recommended_oil_interval_km: int
    recommended_oil_interval_days: int

    model_config = ConfigDict(from_attributes=True)

class VehicleCreateRequest(BaseModel):
    organization_id: str
    license_plate: str
    registration_province: str = "Punjab"
    make: str
    model: str
    year: int
    fuel_type: str = "Petrol"
    initial_odometer_km: float = 0.0
    current_odometer_km: float = 0.0
    vin: Optional[str] = None
    assigned_driver_id: Optional[str] = None
    photo_url: Optional[str] = None
    custom_specs: Dict[str, Any] = {}

class VehicleStatusUpdateRequest(BaseModel):
    status: str  # ACTIVE, MAINTENANCE, INACTIVE

class VehicleUpdateRequest(BaseModel):
    license_plate: Optional[str] = None
    registration_province: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    fuel_type: Optional[str] = None
    current_odometer_km: Optional[float] = None
    assigned_driver_id: Optional[str] = None
    photo_url: Optional[str] = None
    custom_specs: Optional[Dict[str, Any]] = None


class VehicleResponse(BaseModel):
    id: str
    organization_id: str
    assigned_driver_id: Optional[str] = None
    vin: Optional[str] = None
    license_plate: str
    registration_province: str = "Punjab"
    make: str
    model: str
    year: int
    fuel_type: str
    initial_odometer_km: float
    current_odometer_km: float
    status: str
    photo_url: Optional[str] = None
    is_ad_rewarded: bool
    custom_specs: Dict[str, Any] = {}
    created_at: Any
    updated_at: Any

    model_config = ConfigDict(from_attributes=True)

class VehicleDetailResponse(VehicleResponse):
    assigned_driver_name: Optional[str] = None
    assigned_driver_phone: Optional[str] = None
    active_schedules_count: int = 0
    total_service_records_count: int = 0
    total_expenses_cost: float = 0.0

class OdometerUpdateRequest(BaseModel):
    current_odometer_km: float
    reading_date: Optional[str] = None
    is_correction: bool = False

class AssignDriverRequest(BaseModel):
    driver_id: str

class VehicleDocumentCreate(BaseModel):
    document_type: str = "REGISTRATION"  # REGISTRATION, INSURANCE, PERMIT, OTHER
    document_url: str
    file_name: Optional[str] = None
    expiration_date: Optional[Any] = None

class VehicleDocumentResponse(BaseModel):
    id: str
    vehicle_id: str
    organization_id: str
    document_type: str
    document_url: str
    file_name: Optional[str] = None
    expiration_date: Optional[Any] = None
    created_at: Any

    model_config = ConfigDict(from_attributes=True)

