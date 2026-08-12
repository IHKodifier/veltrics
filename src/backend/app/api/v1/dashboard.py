from datetime import date, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.maintenance import MaintenanceSchedule, ServiceRecord
from app.schemas.dashboard import DashboardSummaryResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def verify_organization_header(
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    organization_id: Optional[str] = Query(None, description="Fallback organization ID query param")
) -> str:
    org_id = x_organization_id or organization_id
    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Organization-ID header or organization_id parameter is required"
        )
    return org_id

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(
    org_id: str = Depends(verify_organization_header),
    db: Session = Depends(get_db)
):
    """
    UC-064: Get high-level KPI dashboard metrics summary for active organization.
    """
    # 1. Total Vehicles
    total_vehicles = db.query(Vehicle).filter(
        Vehicle.organization_id == org_id,
        Vehicle.deleted_at == None
    ).count()

    # 2. Total Drivers
    total_drivers = db.query(Driver).filter(
        Driver.organization_id == org_id,
        Driver.deleted_at == None
    ).count()

    # 3. Monthly Total Cost
    today = date.today()
    start_of_month = date(today.year, today.month, 1)
    if today.month == 12:
        end_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
    else:
        end_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

    cost_scalar = db.query(func.coalesce(func.sum(ServiceRecord.total_cost), 0.0)).filter(
        ServiceRecord.organization_id == org_id,
        ServiceRecord.deleted_at == None,
        ServiceRecord.service_date >= start_of_month,
        ServiceRecord.service_date <= end_of_month
    ).scalar()
    monthly_total_cost = float(cost_scalar or 0.0)

    # 4 & 5. Maintenance Schedules Status (Upcoming vs Overdue)
    schedules = db.query(MaintenanceSchedule, Vehicle).join(
        Vehicle, MaintenanceSchedule.vehicle_id == Vehicle.id
    ).filter(
        MaintenanceSchedule.organization_id == org_id,
        MaintenanceSchedule.is_active == True,
        MaintenanceSchedule.deleted_at == None,
        Vehicle.deleted_at == None
    ).all()

    upcoming_count = 0
    overdue_count = 0

    for sched, veh in schedules:
        is_overdue_by_date = (sched.next_due_date is not None) and (sched.next_due_date < today)
        is_overdue_by_km = veh.current_odometer_km > sched.next_due_km

        if is_overdue_by_date or is_overdue_by_km:
            overdue_count += 1
        else:
            is_upcoming_by_date = (sched.next_due_date is not None) and (today <= sched.next_due_date <= today + timedelta(days=7))
            is_upcoming_by_km = (veh.current_odometer_km <= sched.next_due_km <= veh.current_odometer_km + 500.0)

            if is_upcoming_by_date or is_upcoming_by_km:
                upcoming_count += 1

    return DashboardSummaryResponse(
        total_vehicles=total_vehicles,
        total_drivers=total_drivers,
        monthly_total_cost=monthly_total_cost,
        upcoming_maintenance_count=upcoming_count,
        overdue_maintenance_count=overdue_count
    )
