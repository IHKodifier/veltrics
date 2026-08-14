from typing import List, Optional
from pydantic import BaseModel

class ManagerDashboardKpiResponse(BaseModel):
    organization_id: str
    total_vehicles: int
    active_vehicles: int
    maintenance_vehicles: int
    inactive_vehicles: int
    availability_percentage: float
    monthly_fuel_cost: float
    monthly_maintenance_cost: float
    total_monthly_cost: float
    active_trips_count: int

class VehicleCostRankingItem(BaseModel):
    rank: int
    vehicle_id: str
    license_plate: str
    make_model: str
    fuel_cost: float
    maintenance_cost: float
    total_cost: float
    current_odometer_km: float
    cost_per_km: float

class VehicleCostRankingResponse(BaseModel):
    organization_id: str
    total_vehicles: int
    rankings: List[VehicleCostRankingItem]

class VehicleAvailabilityResponse(BaseModel):
    organization_id: str
    total_vehicles: int
    available_count: int
    maintenance_count: int
    in_use_count: int
    availability_percentage: float

class WidgetItem(BaseModel):
    widget_id: str
    visible: bool = True
    position: int = 1

class DashboardLayoutConfigRequest(BaseModel):
    widgets: List[WidgetItem]

class DashboardLayoutConfigResponse(BaseModel):
    user_id: str
    widgets: List[WidgetItem]
