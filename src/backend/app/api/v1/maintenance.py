from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import utc_now
from app.models.vehicle import Vehicle
from app.models.maintenance import MaintenanceSchedule, ServiceRecord
from app.schemas.maintenance import (
    MaintenanceScheduleResponse,
    MaintenanceScheduleCreate,
    MaintenanceScheduleUpdate,
    BulkAcceptSchedulesRequest,
    ServiceRecordCreate,
    ServiceRecordResponse,
)
from app.db.seed import DEFAULT_MAINTENANCE_TEMPLATES

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

def verify_organization_header(x_organization_id: Optional[str]) -> str:
    if not x_organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Organization-ID header is required"
        )
    return x_organization_id

@router.get("/schedules", response_model=List[MaintenanceScheduleResponse])
def get_maintenance_schedules(
    vehicle_id: str = Query(..., description="ID of vehicle to get maintenance schedules for"),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    db: Session = Depends(get_db)
):
    org_id = verify_organization_header(x_organization_id)

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.organization_id == org_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found in active organization"
        )

    schedules = db.query(MaintenanceSchedule).filter(
        MaintenanceSchedule.vehicle_id == vehicle_id,
        MaintenanceSchedule.organization_id == org_id,
        MaintenanceSchedule.deleted_at == None
    ).all()

    # Auto-populate if no schedules exist yet for this vehicle
    if not schedules:
        base_date = vehicle.created_at.date() if vehicle.created_at else date.today()
        new_schedules = []
        for tpl in DEFAULT_MAINTENANCE_TEMPLATES:
            sched = MaintenanceSchedule(
                organization_id=org_id,
                vehicle_id=vehicle_id,
                task_name=tpl["task_name"],
                interval_km=tpl["interval_km"],
                interval_days=tpl["interval_days"],
                last_performed_km=vehicle.initial_odometer_km,
                last_performed_date=base_date,
                next_due_km=vehicle.current_odometer_km + tpl["interval_km"],
                next_due_date=base_date + timedelta(days=tpl["interval_days"]),
                is_active=True
            )
            new_schedules.append(sched)
            db.add(sched)
        db.commit()
        schedules = db.query(MaintenanceSchedule).filter(
            MaintenanceSchedule.vehicle_id == vehicle_id,
            MaintenanceSchedule.organization_id == org_id,
            MaintenanceSchedule.deleted_at == None
        ).all()

    return schedules

@router.post("", response_model=ServiceRecordResponse, status_code=status.HTTP_201_CREATED)
def log_maintenance_task(
    payload: ServiceRecordCreate,
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    db: Session = Depends(get_db)
):
    org_id = verify_organization_header(x_organization_id)

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == payload.vehicle_id,
        Vehicle.organization_id == org_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found in active organization"
        )

    # 1. Create service record
    record = ServiceRecord(
        organization_id=org_id,
        vehicle_id=payload.vehicle_id,
        maintenance_schedule_id=payload.maintenance_schedule_id,
        service_date=payload.service_date,
        odometer_km=payload.odometer_reading,
        total_cost=payload.cost,
        service_center_name=payload.service_provider_name,
        notes=payload.notes,
        invoice_photo_url=payload.photo_url,
    )
    db.add(record)

    # 2. Vehicle odometer auto-update
    if payload.odometer_reading > vehicle.current_odometer_km:
        vehicle.current_odometer_km = payload.odometer_reading

    # 3. Schedule reset logic
    sched = None
    if payload.maintenance_schedule_id:
        sched = db.query(MaintenanceSchedule).filter(
            MaintenanceSchedule.id == payload.maintenance_schedule_id,
            MaintenanceSchedule.organization_id == org_id
        ).first()
    else:
        # Match schedule by task name
        schedules = db.query(MaintenanceSchedule).filter(
            MaintenanceSchedule.vehicle_id == payload.vehicle_id,
            MaintenanceSchedule.organization_id == org_id,
            MaintenanceSchedule.deleted_at == None
        ).all()
        for s in schedules:
            if s.task_name.lower() in payload.service_type.lower() or payload.service_type.lower() in s.task_name.lower():
                sched = s
                break

    if sched:
        if not record.maintenance_schedule_id:
            record.maintenance_schedule_id = sched.id
        sched.last_performed_km = payload.odometer_reading
        sched.last_performed_date = payload.service_date
        sched.next_due_km = payload.odometer_reading + sched.interval_km
        sched.next_due_date = payload.service_date + timedelta(days=sched.interval_days)

    db.commit()
    db.refresh(record)

    return record

@router.post("/schedules", response_model=MaintenanceScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance_schedule(
    payload: MaintenanceScheduleCreate,
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-035: Create custom maintenance schedule task item for a vehicle.
    """
    org_id = verify_organization_header(x_organization_id)

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == payload.vehicle_id,
        Vehicle.organization_id == org_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found in active organization"
        )

    last_performed_km = payload.last_performed_km if payload.last_performed_km is not None else vehicle.current_odometer_km
    last_performed_date = payload.last_performed_date if payload.last_performed_date is not None else date.today()

    next_due_km = last_performed_km + payload.interval_km
    next_due_date = last_performed_date + timedelta(days=payload.interval_days)

    schedule = MaintenanceSchedule(
        organization_id=org_id,
        vehicle_id=payload.vehicle_id,
        task_name=payload.task_name,
        interval_km=payload.interval_km,
        interval_days=payload.interval_days,
        last_performed_km=last_performed_km,
        last_performed_date=last_performed_date,
        next_due_km=next_due_km,
        next_due_date=next_due_date,
        is_active=True
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule

@router.patch("/schedules/{schedule_id}", response_model=MaintenanceScheduleResponse)
def update_maintenance_schedule(
    schedule_id: str,
    payload: MaintenanceScheduleUpdate,
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-035: Update schedule parameters (intervals, task name, active status) and recalculate due targets.
    """
    org_id = verify_organization_header(x_organization_id)

    schedule = db.query(MaintenanceSchedule).filter(
        MaintenanceSchedule.id == schedule_id,
        MaintenanceSchedule.organization_id == org_id,
        MaintenanceSchedule.deleted_at == None
    ).first()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance schedule not found in active organization"
        )

    if payload.task_name is not None:
        schedule.task_name = payload.task_name

    if payload.is_active is not None:
        schedule.is_active = payload.is_active

    interval_changed = False
    if payload.interval_km is not None:
        schedule.interval_km = payload.interval_km
        interval_changed = True

    if payload.interval_days is not None:
        schedule.interval_days = payload.interval_days
        interval_changed = True

    if interval_changed:
        base_km = schedule.last_performed_km if schedule.last_performed_km is not None else 0.0
        base_date = schedule.last_performed_date if schedule.last_performed_date is not None else date.today()
        schedule.next_due_km = base_km + schedule.interval_km
        schedule.next_due_date = base_date + timedelta(days=schedule.interval_days)

    db.commit()
    db.refresh(schedule)
    return schedule

@router.delete("/schedules/{schedule_id}")
def delete_maintenance_schedule(
    schedule_id: str,
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-035: Soft-delete schedule item.
    """
    org_id = verify_organization_header(x_organization_id)

    schedule = db.query(MaintenanceSchedule).filter(
        MaintenanceSchedule.id == schedule_id,
        MaintenanceSchedule.organization_id == org_id,
        MaintenanceSchedule.deleted_at == None
    ).first()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance schedule not found in active organization"
        )

    schedule.deleted_at = utc_now()
    db.commit()

    return {"message": "Maintenance schedule deleted successfully"}

@router.get("/records", response_model=List[ServiceRecordResponse])
def get_service_history(
    vehicle_id: str = Query(..., description="ID of vehicle to retrieve service history for"),
    limit: int = Query(50, ge=1, le=500, description="Maximum number of service records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-037: Retrieve chronological service records for a vehicle within the active organization.
    """
    org_id = verify_organization_header(x_organization_id)

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.organization_id == org_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found in active organization"
        )

    records = db.query(ServiceRecord).filter(
        ServiceRecord.organization_id == org_id,
        ServiceRecord.vehicle_id == vehicle_id,
        ServiceRecord.deleted_at == None
    ).order_by(
        ServiceRecord.service_date.desc(),
        ServiceRecord.created_at.desc()
    ).offset(offset).limit(limit).all()

    return records


@router.post("/schedules/bulk-accept", response_model=List[MaintenanceScheduleResponse])
def bulk_accept_maintenance_schedules(
    payload: BulkAcceptSchedulesRequest,
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-038: Bulk accept/acknowledge default maintenance schedules for a vehicle.
    """
    org_id = verify_organization_header(x_organization_id)

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == payload.vehicle_id,
        Vehicle.organization_id == org_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found in active organization"
        )

    # Ensure schedules exist (auto-populate defaults if none exist yet)
    schedules = db.query(MaintenanceSchedule).filter(
        MaintenanceSchedule.vehicle_id == payload.vehicle_id,
        MaintenanceSchedule.organization_id == org_id,
        MaintenanceSchedule.deleted_at == None
    ).all()

    if not schedules:
        base_date = vehicle.created_at.date() if vehicle.created_at else date.today()
        for tpl in DEFAULT_MAINTENANCE_TEMPLATES:
            sched = MaintenanceSchedule(
                organization_id=org_id,
                vehicle_id=payload.vehicle_id,
                task_name=tpl["task_name"],
                interval_km=tpl["interval_km"],
                interval_days=tpl["interval_days"],
                last_performed_km=vehicle.initial_odometer_km,
                last_performed_date=base_date,
                next_due_km=vehicle.current_odometer_km + tpl["interval_km"],
                next_due_date=base_date + timedelta(days=tpl["interval_days"]),
                is_active=True
            )
            db.add(sched)
        db.commit()
        schedules = db.query(MaintenanceSchedule).filter(
            MaintenanceSchedule.vehicle_id == payload.vehicle_id,
            MaintenanceSchedule.organization_id == org_id,
            MaintenanceSchedule.deleted_at == None
        ).all()

    if payload.schedule_ids:
        schedule_dict = {s.id: s for s in schedules}
        missing_ids = [sid for sid in payload.schedule_ids if sid not in schedule_dict]
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more maintenance schedule IDs not found for this vehicle"
            )
        target_schedules = [schedule_dict[sid] for sid in payload.schedule_ids]
    else:
        target_schedules = schedules

    for sched in target_schedules:
        sched.is_active = True

    db.commit()
    for sched in target_schedules:
        db.refresh(sched)

    return target_schedules



