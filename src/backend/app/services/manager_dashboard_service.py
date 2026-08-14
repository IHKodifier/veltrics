from datetime import date, datetime, timezone, timedelta
from typing import List, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.maintenance import ServiceRecord
from app.models.fuel_log import FuelLog
from app.models.trip import Trip
from app.schemas.dashboard_manager import (
    ManagerDashboardKpiResponse,
    VehicleCostRankingResponse,
    VehicleCostRankingItem,
    VehicleAvailabilityResponse,
    DashboardLayoutConfigResponse,
    WidgetItem,
)

# Global layout in-memory cache for user preferences
_USER_LAYOUT_CACHE: Dict[str, List[dict]] = {}

def get_manager_kpis(db: Session, organization_id: str) -> ManagerDashboardKpiResponse:
    vehicles = db.query(Vehicle).filter(
        Vehicle.organization_id == organization_id,
        Vehicle.deleted_at.is_(None)
    ).all()

    total_vehicles = len(vehicles)
    active_vehicles = sum(1 for v in vehicles if v.status == "ACTIVE")
    maintenance_vehicles = sum(1 for v in vehicles if v.status == "MAINTENANCE")
    inactive_vehicles = sum(1 for v in vehicles if v.status == "INACTIVE")

    avail_pct = (active_vehicles / total_vehicles * 100.0) if total_vehicles > 0 else 100.0

    today = date.today()
    start_of_month = date(today.year, today.month, 1)

    # Calculate monthly maintenance cost
    mnt_cost_scalar = db.query(func.coalesce(func.sum(ServiceRecord.total_cost), 0.0)).filter(
        ServiceRecord.organization_id == organization_id,
        ServiceRecord.deleted_at.is_(None),
        ServiceRecord.service_date >= start_of_month
    ).scalar()
    monthly_mnt_cost = float(mnt_cost_scalar or 0.0)

    # Calculate monthly fuel cost
    fuel_cost_scalar = db.query(func.coalesce(func.sum(FuelLog.total_cost), 0.0)).filter(
        FuelLog.organization_id == organization_id,
        FuelLog.deleted_at.is_(None)
    ).scalar()
    monthly_fuel_cost = float(fuel_cost_scalar or 0.0)

    # Active trips
    active_trips_count = db.query(Trip).filter(
        Trip.organization_id == organization_id,
        Trip.status == "IN_PROGRESS",
        Trip.deleted_at.is_(None)
    ).count()

    return ManagerDashboardKpiResponse(
        organization_id=organization_id,
        total_vehicles=total_vehicles,
        active_vehicles=active_vehicles,
        maintenance_vehicles=maintenance_vehicles,
        inactive_vehicles=inactive_vehicles,
        availability_percentage=round(avail_pct, 1),
        monthly_fuel_cost=round(monthly_fuel_cost, 2),
        monthly_maintenance_cost=round(monthly_mnt_cost, 2),
        total_monthly_cost=round(monthly_fuel_cost + monthly_mnt_cost, 2),
        active_trips_count=active_trips_count,
    )


def get_cost_ranking_table(db: Session, organization_id: str) -> VehicleCostRankingResponse:
    vehicles = db.query(Vehicle).filter(
        Vehicle.organization_id == organization_id,
        Vehicle.deleted_at.is_(None)
    ).all()

    rankings: List[VehicleCostRankingItem] = []

    for v in vehicles:
        mnt_cost = db.query(func.coalesce(func.sum(ServiceRecord.total_cost), 0.0)).filter(
            ServiceRecord.vehicle_id == v.id,
            ServiceRecord.deleted_at.is_(None)
        ).scalar()

        fuel_cost = db.query(func.coalesce(func.sum(FuelLog.total_cost), 0.0)).filter(
            FuelLog.vehicle_id == v.id,
            FuelLog.deleted_at.is_(None)
        ).scalar()

        mnt_c = float(mnt_cost or 0.0)
        fuel_c = float(fuel_cost or 0.0)
        tot_c = mnt_c + fuel_c

        odo = max(1.0, v.current_odometer_km)
        cost_per_km = round(tot_c / odo, 2)

        rankings.append(
            VehicleCostRankingItem(
                rank=0,  # assigned after sorting
                vehicle_id=v.id,
                license_plate=v.license_plate,
                make_model=f"{v.make} {v.model}",
                fuel_cost=round(fuel_c, 2),
                maintenance_cost=round(mnt_c, 2),
                total_cost=round(tot_c, 2),
                current_odometer_km=v.current_odometer_km,
                cost_per_km=cost_per_km,
            )
        )

    # Sort descending by total cost
    rankings.sort(key=lambda x: x.total_cost, reverse=True)

    for i, item in enumerate(rankings, start=1):
        item.rank = i

    return VehicleCostRankingResponse(
        organization_id=organization_id,
        total_vehicles=len(vehicles),
        rankings=rankings,
    )


def get_vehicle_availability(db: Session, organization_id: str) -> VehicleAvailabilityResponse:
    vehicles = db.query(Vehicle).filter(
        Vehicle.organization_id == organization_id,
        Vehicle.deleted_at.is_(None)
    ).all()

    total_vehicles = len(vehicles)
    avail_count = sum(1 for v in vehicles if v.status == "ACTIVE")
    mnt_count = sum(1 for v in vehicles if v.status == "MAINTENANCE")
    in_use_count = sum(1 for v in vehicles if v.status == "IN_USE")

    avail_pct = (avail_count / total_vehicles * 100.0) if total_vehicles > 0 else 100.0

    return VehicleAvailabilityResponse(
        organization_id=organization_id,
        total_vehicles=total_vehicles,
        available_count=avail_count,
        maintenance_count=mnt_count,
        in_use_count=in_use_count,
        availability_percentage=round(avail_pct, 1),
    )


def save_dashboard_layout(user_id: str, widgets: List[dict]) -> DashboardLayoutConfigResponse:
    _USER_LAYOUT_CACHE[user_id] = widgets
    items = [WidgetItem(**w) for w in widgets]
    return DashboardLayoutConfigResponse(user_id=user_id, widgets=items)


def get_dashboard_layout(user_id: str) -> DashboardLayoutConfigResponse:
    default_layout = [
        {"widget_id": "kpi_cards", "visible": True, "position": 1},
        {"widget_id": "cost_ranking", "visible": True, "position": 2},
        {"widget_id": "availability", "visible": True, "position": 3},
    ]
    widgets = _USER_LAYOUT_CACHE.get(user_id, default_layout)
    items = [WidgetItem(**w) for w in widgets]
    return DashboardLayoutConfigResponse(user_id=user_id, widgets=items)
