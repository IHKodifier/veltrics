from typing import List, Optional, Tuple
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.schemas.trip import TripStart, TripStop, TripCreate, TripUpdate, QuickTripCreate

def start_trip(db: Session, organization_id: str, payload: TripStart) -> Trip:
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == payload.vehicle_id,
        Vehicle.organization_id == organization_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID '{payload.vehicle_id}' not found."
        )

    existing_active = db.query(Trip).filter(
        Trip.vehicle_id == payload.vehicle_id,
        Trip.organization_id == organization_id,
        Trip.status == "IN_PROGRESS",
        Trip.deleted_at == None
    ).first()

    if existing_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vehicle '{vehicle.license_plate}' already has an active trip in progress."
        )

    trip = Trip(
        organization_id=organization_id,
        vehicle_id=payload.vehicle_id,
        driver_id=payload.driver_id,
        start_time=payload.start_time or datetime.utcnow(),
        origin_name=payload.origin_name,
        start_odometer_km=payload.start_odometer_km,
        trip_purpose=payload.trip_purpose,
        is_manual=False,
        status="IN_PROGRESS"
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip

def stop_trip(db: Session, organization_id: str, trip_id: str, payload: TripStop) -> Trip:
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.organization_id == organization_id,
        Trip.deleted_at == None
    ).first()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with ID '{trip_id}' not found."
        )

    if payload.end_odometer_km < trip.start_odometer_km:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"End odometer ({payload.end_odometer_km} km) must be greater than or equal to start odometer ({trip.start_odometer_km} km)."
        )

    trip.end_odometer_km = payload.end_odometer_km
    trip.distance_km = round(payload.end_odometer_km - trip.start_odometer_km, 2)
    if payload.destination_name:
        trip.destination_name = payload.destination_name
    trip.end_time = payload.end_time or datetime.utcnow()
    if payload.gps_polyline_json:
        trip.gps_polyline_json = payload.gps_polyline_json
    if payload.notes:
        trip.notes = payload.notes
    trip.status = "COMPLETED"

    vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()
    if vehicle and payload.end_odometer_km > vehicle.current_odometer_km:
        vehicle.current_odometer_km = payload.end_odometer_km

    db.commit()
    db.refresh(trip)
    return trip

def create_trip(db: Session, organization_id: str, payload: TripCreate) -> Trip:
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == payload.vehicle_id,
        Vehicle.organization_id == organization_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID '{payload.vehicle_id}' not found."
        )

    start_time = payload.start_time or datetime.utcnow()
    end_time = payload.end_time or start_time

    if payload.end_odometer_km is not None:
        if payload.end_odometer_km < payload.start_odometer_km:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"End odometer ({payload.end_odometer_km} km) must be greater than or equal to start odometer ({payload.start_odometer_km} km)."
            )
        distance_km = round(payload.end_odometer_km - payload.start_odometer_km, 2)
        trip_status = "COMPLETED"
    else:
        distance_km = None
        trip_status = "IN_PROGRESS"

    trip = Trip(
        organization_id=organization_id,
        vehicle_id=payload.vehicle_id,
        driver_id=payload.driver_id,
        start_time=start_time,
        end_time=end_time if trip_status == "COMPLETED" else None,
        origin_name=payload.origin_name,
        destination_name=payload.destination_name,
        start_odometer_km=payload.start_odometer_km,
        end_odometer_km=payload.end_odometer_km,
        distance_km=distance_km,
        trip_purpose=payload.trip_purpose,
        is_manual=payload.is_manual,
        status=trip_status,
        gps_polyline_json=payload.gps_polyline_json,
        notes=payload.notes
    )

    db.add(trip)

    if payload.end_odometer_km and payload.end_odometer_km > vehicle.current_odometer_km:
        vehicle.current_odometer_km = payload.end_odometer_km

    db.commit()
    db.refresh(trip)
    return trip

def get_trips(
    db: Session,
    organization_id: str,
    vehicle_id: Optional[str] = None,
    trip_purpose: Optional[str] = None,
    page: Optional[int] = None,
    limit: Optional[int] = None
) -> Tuple[List[Trip], int]:
    query = db.query(Trip).filter(
        Trip.organization_id == organization_id,
        Trip.deleted_at == None
    )

    if vehicle_id:
        query = query.filter(Trip.vehicle_id == vehicle_id)
    if trip_purpose:
        query = query.filter(Trip.trip_purpose == trip_purpose)

    total = query.count()
    query = query.order_by(Trip.start_time.desc())

    if page and limit:
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()
    else:
        items = query.all()

    return items, total

def get_trip_summary(
    db: Session,
    organization_id: str,
    vehicle_id: Optional[str] = None,
    tax_rate_per_km: float = 0.65
) -> dict:
    query = db.query(Trip).filter(
        Trip.organization_id == organization_id,
        Trip.deleted_at == None,
        Trip.status == "COMPLETED"
    )

    if vehicle_id:
        query = query.filter(Trip.vehicle_id == vehicle_id)

    trips = query.all()

    total_dist = sum(t.distance_km for t in trips if t.distance_km is not None)
    biz_dist = sum(t.distance_km for t in trips if t.trip_purpose == "BUSINESS" and t.distance_km is not None)
    per_dist = sum(t.distance_km for t in trips if t.trip_purpose == "PERSONAL" and t.distance_km is not None)
    tax_deduction = round(biz_dist * tax_rate_per_km, 2)

    return {
        "vehicle_id": vehicle_id,
        "total_distance_km": round(total_dist, 2),
        "business_distance_km": round(biz_dist, 2),
        "personal_distance_km": round(per_dist, 2),
        "total_trips_count": len(trips),
        "estimated_tax_deduction": tax_deduction
    }

def update_trip(db: Session, organization_id: str, trip_id: str, payload: TripUpdate) -> Trip:
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.organization_id == organization_id,
        Trip.deleted_at == None
    ).first()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with ID '{trip_id}' not found."
        )

    if payload.vehicle_id is not None:
        trip.vehicle_id = payload.vehicle_id
    if payload.driver_id is not None:
        trip.driver_id = payload.driver_id
    if payload.origin_name is not None:
        trip.origin_name = payload.origin_name
    if payload.destination_name is not None:
        trip.destination_name = payload.destination_name
    if payload.trip_purpose is not None:
        trip.trip_purpose = payload.trip_purpose
    if payload.start_time is not None:
        trip.start_time = payload.start_time
    if payload.end_time is not None:
        trip.end_time = payload.end_time
    if payload.gps_polyline_json is not None:
        trip.gps_polyline_json = payload.gps_polyline_json
    if payload.notes is not None:
        trip.notes = payload.notes

    if payload.start_odometer_km is not None:
        trip.start_odometer_km = payload.start_odometer_km
    if payload.end_odometer_km is not None:
        trip.end_odometer_km = payload.end_odometer_km

    if trip.end_odometer_km is not None and trip.start_odometer_km is not None:
        if trip.end_odometer_km < trip.start_odometer_km:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"End odometer ({trip.end_odometer_km} km) must be greater than or equal to start odometer ({trip.start_odometer_km} km)."
            )
        trip.distance_km = round(trip.end_odometer_km - trip.start_odometer_km, 2)

    db.commit()
    db.refresh(trip)
    return trip

def delete_trip(db: Session, organization_id: str, trip_id: str) -> dict:
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.organization_id == organization_id,
        Trip.deleted_at == None
    ).first()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with ID '{trip_id}' not found."
        )

    trip.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "Trip entry deleted successfully"}

def quick_log_trip(db: Session, organization_id: str, payload: QuickTripCreate) -> Trip:
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == payload.vehicle_id,
        Vehicle.organization_id == organization_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID '{payload.vehicle_id}' not found."
        )

    start_odo = vehicle.current_odometer_km or 0.0
    end_odo = start_odo + payload.distance_km
    now = datetime.utcnow()

    trip = Trip(
        organization_id=organization_id,
        vehicle_id=payload.vehicle_id,
        driver_id=payload.driver_id,
        start_time=now,
        end_time=now,
        origin_name=payload.origin_name,
        destination_name=payload.destination_name,
        start_odometer_km=start_odo,
        end_odometer_km=end_odo,
        distance_km=payload.distance_km,
        trip_purpose=payload.trip_purpose.upper(),
        is_manual=True,
        status="COMPLETED",
        notes=payload.notes
    )

    vehicle.current_odometer_km = end_odo

    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip

def get_mileage_summary(
    db: Session,
    organization_id: str,
    vehicle_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> dict:
    query = db.query(Trip).filter(
        Trip.organization_id == organization_id,
        Trip.deleted_at == None
    )

    if vehicle_id:
        query = query.filter(Trip.vehicle_id == vehicle_id)
    if start_date:
        query = query.filter(Trip.start_time >= start_date)
    if end_date:
        query = query.filter(Trip.start_time <= end_date)

    trips = query.all()

    total_dist = sum(t.distance_km or 0.0 for t in trips)
    biz_trips = [t for t in trips if t.trip_purpose == "BUSINESS"]
    per_trips = [t for t in trips if t.trip_purpose == "PERSONAL"]

    biz_dist = sum(t.distance_km or 0.0 for t in biz_trips)
    per_dist = sum(t.distance_km or 0.0 for t in per_trips)

    avg_dist = (total_dist / len(trips)) if trips else 0.0
    tax_deduction = round(biz_dist * 0.65, 2)

    return {
        "vehicle_id": vehicle_id,
        "total_distance_km": round(total_dist, 2),
        "business_distance_km": round(biz_dist, 2),
        "personal_distance_km": round(per_dist, 2),
        "total_trips_count": len(trips),
        "business_trips_count": len(biz_trips),
        "personal_trips_count": len(per_trips),
        "average_trip_distance_km": round(avg_dist, 2),
        "estimated_tax_deduction": tax_deduction
    }




