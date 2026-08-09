from pydantic import BaseModel, ConfigDict, Field

class DashboardSummaryResponse(BaseModel):
    total_vehicles: int = Field(..., ge=0, description="Count of active non-deleted vehicles in organization")
    total_drivers: int = Field(..., ge=0, description="Count of active non-deleted drivers in organization")
    monthly_total_cost: float = Field(..., ge=0, description="Total maintenance & service cost for current calendar month")
    upcoming_maintenance_count: int = Field(..., ge=0, description="Count of maintenance schedules due within 7 days or 500 km")
    overdue_maintenance_count: int = Field(..., ge=0, description="Count of maintenance schedules past due date or odometer limit")

    model_config = ConfigDict(from_attributes=True)
