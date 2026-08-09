from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_validator

class MaintenanceScheduleResponse(BaseModel):
    id: str
    organization_id: str
    vehicle_id: str
    task_name: str
    interval_km: int
    interval_days: int
    last_performed_km: float
    last_performed_date: Optional[date] = None
    next_due_km: float
    next_due_date: Optional[date] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MaintenanceScheduleCreate(BaseModel):
    vehicle_id: str
    task_name: str = Field(..., min_length=1, max_length=255, description="Name of the maintenance task")
    interval_km: int = Field(..., gt=0, description="Odometer interval in kilometers")
    interval_days: int = Field(..., gt=0, description="Time interval in days")
    last_performed_km: Optional[float] = Field(None, ge=0, description="Initial last performed odometer reading")
    last_performed_date: Optional[date] = Field(None, description="Initial last performed date")

    @field_validator("task_name")
    @classmethod
    def validate_task_name(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Task name cannot be empty or whitespace only.")
        return stripped

class MaintenanceScheduleUpdate(BaseModel):
    task_name: Optional[str] = Field(None, min_length=1, max_length=255)
    interval_km: Optional[int] = Field(None, gt=0)
    interval_days: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None

    @field_validator("task_name")
    @classmethod
    def validate_task_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError("Task name cannot be empty or whitespace only.")
            return stripped
        return v

class BulkAcceptSchedulesRequest(BaseModel):
    vehicle_id: str
    schedule_ids: Optional[List[str]] = Field(default_factory=list, description="List of schedule IDs to accept/activate. If empty or null, accepts all schedules for the vehicle.")


class ServiceRecordCreate(BaseModel):
    vehicle_id: str
    maintenance_schedule_id: Optional[str] = None
    service_type: str = Field(..., min_length=1, description="Maintenance task or service name")
    cost: float = Field(..., ge=0, description="Service total cost; must be non-negative")
    service_date: date
    odometer_reading: float = Field(..., ge=0, description="Vehicle odometer reading at time of service")
    service_provider_name: Optional[str] = None
    notes: Optional[str] = None
    photo_url: Optional[str] = None

    @field_validator("service_type")
    @classmethod
    def validate_service_type(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Service type cannot be empty or whitespace only.")
        return stripped

class ServiceRecordResponse(BaseModel):
    id: str
    organization_id: str
    vehicle_id: str
    maintenance_schedule_id: Optional[str] = None
    service_date: date
    odometer_km: float
    total_cost: float
    service_center_name: Optional[str] = None
    notes: Optional[str] = None
    performed_by: Optional[str] = None
    invoice_photo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
