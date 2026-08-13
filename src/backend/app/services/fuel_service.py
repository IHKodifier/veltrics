from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.models.fuel_log import FuelLog
from app.models.expense_log import ExpenseLog
from app.schemas.fuel_log import FuelLogCreate

def log_fuel_entry(db: Session, organization_id: str, payload: FuelLogCreate) -> FuelLog:
    # 1. Validate vehicle exists and belongs to organization
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == payload.vehicle_id,
        Vehicle.organization_id == organization_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID '{payload.vehicle_id}' not found in organization."
        )

    # 2. Odometer Validation: must be >= vehicle's current odometer reading
    odometer_reading = payload.odometer_val
    if odometer_reading < vehicle.current_odometer_km:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Odometer reading ({odometer_reading} km) cannot be lower than current vehicle odometer ({vehicle.current_odometer_km} km)."
        )

    # 3. Update vehicle current odometer if higher
    if odometer_reading > vehicle.current_odometer_km:
        vehicle.current_odometer_km = odometer_reading

    # 4. Calculate unit price per liter if omitted
    qty = payload.quantity_liters_val
    total_cost = payload.total_cost_val
    price_per_liter = payload.price_per_liter if payload.price_per_liter and payload.price_per_liter > 0 else (
        (total_cost / qty) if qty > 0 else 0.0
    )

    # 5. Calculate efficiency & distance delta if previous full tank log exists (UC-047 logic)
    calculated_efficiency = None
    distance_traveled = None
    is_leak_alert = False

    if payload.is_full_tank:
        prev_log = db.query(FuelLog).filter(
            FuelLog.vehicle_id == payload.vehicle_id,
            FuelLog.is_full_tank == True,
            FuelLog.deleted_at == None
        ).order_by(FuelLog.odometer_km.desc()).first()

        if prev_log and prev_log.odometer_km < odometer_reading:
            distance_traveled = round(odometer_reading - prev_log.odometer_km, 2)
            if distance_traveled > 0 and qty > 0:
                calculated_efficiency = round(distance_traveled / qty, 2)

                # Anomaly Detection: Compare against vehicle's historical baseline average efficiency
                past_full_tanks = db.query(FuelLog).filter(
                    FuelLog.vehicle_id == payload.vehicle_id,
                    FuelLog.is_full_tank == True,
                    FuelLog.calculated_efficiency_kpl != None,
                    FuelLog.deleted_at == None
                ).all()

                if past_full_tanks:
                    valid_efficiencies = [log.calculated_efficiency_kpl for log in past_full_tanks if log.calculated_efficiency_kpl is not None]
                    if valid_efficiencies:
                        baseline_avg = sum(valid_efficiencies) / len(valid_efficiencies)
                        # Flag review if current efficiency is >30% below historical baseline average
                        if calculated_efficiency < (baseline_avg * 0.70):
                            is_leak_alert = True

    # 6. Create FuelLog record
    fuel_log = FuelLog(
        organization_id=organization_id,
        vehicle_id=payload.vehicle_id,
        driver_id=payload.driver_id,
        log_date=payload.log_date_val,
        odometer_km=odometer_reading,
        fuel_type=payload.fuel_type,
        quantity_liters=qty,
        price_per_liter=price_per_liter,
        total_cost=total_cost,
        currency="PKR",
        station_name=payload.station_name,
        receipt_photo_url=payload.receipt_photo_url_val,
        is_full_tank=payload.is_full_tank,
        calculated_efficiency_kpl=calculated_efficiency,
        distance_km=distance_traveled,
        is_leak_alert=is_leak_alert
    )
    db.add(fuel_log)
    db.flush()

    # 7. Auto-create linked ExpenseLog under category 'FUEL' (Acceptance Criterion UC-046)
    expense_log = ExpenseLog(
        organization_id=organization_id,
        vehicle_id=payload.vehicle_id,
        fuel_log_id=fuel_log.id,
        category="FUEL",
        amount=total_cost,
        currency="PKR",
        expense_date=payload.log_date_val,
        receipt_photo_url=payload.receipt_photo_url_val,
        notes=f"Auto-generated expense record for Fuel Fill-up Log #{fuel_log.id}"
    )
    db.add(expense_log)

    db.commit()
    db.refresh(fuel_log)
    return fuel_log

def get_fuel_logs(db: Session, organization_id: str, vehicle_id: Optional[str] = None) -> List[FuelLog]:
    query = db.query(FuelLog).filter(
        FuelLog.organization_id == organization_id,
        FuelLog.deleted_at == None
    )
    if vehicle_id:
        query = query.filter(FuelLog.vehicle_id == vehicle_id)
    return query.order_by(FuelLog.log_date.desc(), FuelLog.created_at.desc()).all()
