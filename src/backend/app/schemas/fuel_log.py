from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, root_validator

class FuelLogCreate(BaseModel):
    vehicle_id: str
    odometer: Optional[float] = None
    odometer_km: Optional[float] = None
    fuel_amount_liters: Optional[float] = None
    quantity_liters: Optional[float] = None
    cost_amount: Optional[float] = None
    total_cost: Optional[float] = None
    fuel_type: str = "Petrol"
    fill_date: Optional[datetime] = None
    log_date: Optional[datetime] = None
    is_full_tank: bool = True
    driver_id: Optional[str] = None
    station_name: Optional[str] = None
    receipt_image_url: Optional[str] = None
    receipt_photo_url: Optional[str] = None
    price_per_liter: Optional[float] = None

    @property
    def odometer_val(self) -> float:
        val = self.odometer if self.odometer is not None else self.odometer_km
        return val if val is not None else 0.0

    @property
    def quantity_liters_val(self) -> float:
        val = self.fuel_amount_liters if self.fuel_amount_liters is not None else self.quantity_liters
        return val if val is not None else 0.0

    @property
    def total_cost_val(self) -> float:
        val = self.cost_amount if self.cost_amount is not None else self.total_cost
        return val if val is not None else 0.0

    @property
    def receipt_photo_url_val(self) -> Optional[str]:
        return self.receipt_photo_url or self.receipt_image_url

    @property
    def log_date_val(self) -> datetime:
        return self.fill_date or self.log_date or datetime.utcnow()

    class Config:
        allow_population_by_field_name = True

class FuelLogResponse(BaseModel):
    id: str
    organization_id: str
    vehicle_id: str
    driver_id: Optional[str] = None
    log_date: datetime
    odometer_km: float
    fuel_type: str
    quantity_liters: float
    price_per_liter: float
    total_cost: float
    currency: str
    station_name: Optional[str] = None
    receipt_photo_url: Optional[str] = None
    is_full_tank: bool
    calculated_efficiency_kpl: Optional[float] = None
    distance_km: Optional[float] = None
    is_leak_alert: bool = False
    created_at: datetime

    class Config:
        orm_mode = True
