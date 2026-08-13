from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.seed import seed_database
from app.models.user import User
from app.models.organization import Organization
from app.models.vehicle import Vehicle, VehicleType
from app.schemas.vehicle import VehicleCreateRequest, VehicleResponse, VehicleTypeResponse

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.get("/types", response_model=List[VehicleTypeResponse])
def get_vehicle_types(
    q: Optional[str] = Query(None, description="Search term for make or model"),
    make: Optional[str] = Query(None, description="Filter models by specific make"),
    db: Session = Depends(get_db)
):
    """
    UC-024: Typeahead autocomplete lookup against seeded Vehicle Master Catalogue.
    Auto-seeds if database table is empty.
    """
    if db.query(VehicleType).count() == 0:
        seed_database(db)

    query = db.query(VehicleType)
    if make:
        query = query.filter(VehicleType.make.ilike(f"%{make}%"))
    if q:
        search_pattern = f"%{q}%"
        query = query.filter(
            (VehicleType.make.ilike(search_pattern)) | 
            (VehicleType.model.ilike(search_pattern))
        )
    return query.order_by(VehicleType.make.asc(), VehicleType.model.asc()).all()

def ensure_organization(db: Session, org_id: str) -> Organization:
    org = db.query(Organization).filter(
        Organization.id == org_id,
        Organization.deleted_at == None
    ).first()

    if not org:
        # Create default demo user if needed
        demo_user = db.query(User).filter_by(id="user-demo-101").first()
        if not demo_user:
            demo_user = User(
                id="user-demo-101",
                firebase_uid="demo-firebase-uid-101",
                email="alex@veltrics.com",
                full_name="Alex Rivera",
                auth_provider="google"
            )
            db.add(demo_user)
            db.flush()

        org = Organization(
            id=org_id,
            name="Default Fleet Workspace",
            owner_id=demo_user.id,
            is_personal=True,
            max_vehicles=10
        )
        db.add(org)
        db.commit()
        db.refresh(org)
    
    return org

@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(req: VehicleCreateRequest, db: Session = Depends(get_db)):
    """
    UC-024: Register New Vehicle with organization quota validation & duplicate VIN detection.
    """
    # 1. Validate Organization existence (auto-creates if demo workspace)
    org = ensure_organization(db, req.organization_id)

    # 2. Check Organization vehicle quota limit
    active_vehicle_count = db.query(Vehicle).filter(
        Vehicle.organization_id == req.organization_id,
        Vehicle.deleted_at == None
    ).count()

    if active_vehicle_count >= org.max_vehicles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vehicle quota limit reached ({org.max_vehicles} vehicles max for your workspace tier)."
        )

    # 3. Check duplicate VIN within organization
    if req.vin:
        existing_vin = db.query(Vehicle).filter(
            Vehicle.organization_id == req.organization_id,
            Vehicle.vin == req.vin,
            Vehicle.deleted_at == None
        ).first()
        if existing_vin:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="VIN already exists in fleet."
            )

    # 4. Auto-index custom Make & Model into master VehicleType catalogue if not present
    existing_type = db.query(VehicleType).filter(
        VehicleType.make.ilike(req.make.strip()),
        VehicleType.model.ilike(req.model.strip())
    ).first()

    if not existing_type:
        new_type = VehicleType(
            make=req.make.strip().title(),
            model=req.model.strip().title(),
            category="Custom",
            default_fuel_type=req.fuel_type,
            recommended_oil_interval_km=5000,
            recommended_oil_interval_days=180
        )
        db.add(new_type)
        db.flush()

    # 5. Create Vehicle record
    vehicle = Vehicle(
        organization_id=req.organization_id,
        assigned_driver_id=req.assigned_driver_id,
        vin=req.vin,
        license_plate=req.license_plate.upper().strip(),
        registration_province=req.registration_province.strip(),
        make=req.make.strip().title(),
        model=req.model.strip().title(),
        year=req.year,
        fuel_type=req.fuel_type,
        initial_odometer_km=req.initial_odometer_km,
        current_odometer_km=req.current_odometer_km or req.initial_odometer_km,
        photo_url=req.photo_url,
        custom_specs=req.custom_specs,
        status="ACTIVE"
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle

@router.get("", response_model=List[VehicleResponse])
def list_vehicles(
    organization_id: str = Query(..., description="Organization ID to filter vehicles"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by vehicle status (ACTIVE, MAINTENANCE, INACTIVE)"),
    search: Optional[str] = Query(None, description="Search term for license plate, make, or model"),
    fuel_type: Optional[str] = Query(None, description="Filter by fuel type (Petrol, Diesel, Hybrid, EV, CNG)"),
    province: Optional[str] = Query(None, description="Filter by registration province/region"),
    db: Session = Depends(get_db)
):
    """
    UC-025: List Organization Vehicles directory with status, search, fuel type, and province filtering.
    """
    ensure_organization(db, organization_id)

    query = db.query(Vehicle).filter(
        Vehicle.organization_id == organization_id,
        Vehicle.deleted_at == None
    )
    if status_filter and status_filter.upper() != "ALL":
        query = query.filter(Vehicle.status == status_filter.upper())
    
    if fuel_type:
        query = query.filter(Vehicle.fuel_type.ilike(f"%{fuel_type}%"))

    if province:
        query = query.filter(Vehicle.registration_province.ilike(f"%{province}%"))

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Vehicle.license_plate.ilike(search_pattern)) |
            (Vehicle.make.ilike(search_pattern)) |
            (Vehicle.model.ilike(search_pattern)) |
            (Vehicle.vin.ilike(search_pattern))
        )

    return query.all()

from app.models.driver import Driver
from app.models.maintenance import MaintenanceSchedule, ServiceRecord
from app.models.audit_log import AuditLog
from app.schemas.vehicle import (
    VehicleCreateRequest,
    VehicleStatusUpdateRequest,
    VehicleUpdateRequest,
    VehicleResponse,
    VehicleDetailResponse,
    VehicleTypeResponse,
)

@router.get("/{vehicle_id}", response_model=VehicleDetailResponse)
def get_vehicle_detail(
    vehicle_id: str,
    organization_id: str = Query(..., description="Organization ID for tenant isolation verification"),
    db: Session = Depends(get_db)
):
    """
    UC-026: View Vehicle Detailed Overview.
    Enforces tenant isolation and returns full metadata with summary counts.
    """
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    if vehicle.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Vehicle belongs to a different organization."
        )

    # Driver details
    driver_name = None
    driver_phone = None
    if vehicle.assigned_driver_id:
        driver = db.query(Driver).filter_by(id=vehicle.assigned_driver_id).first()
        if driver:
            driver_name = driver.full_name
            driver_phone = driver.phone_number

    # Summary counts
    schedules_count = db.query(MaintenanceSchedule).filter_by(vehicle_id=vehicle.id).count()
    service_records = db.query(ServiceRecord).filter_by(vehicle_id=vehicle.id).all()
    records_count = len(service_records)
    total_cost = sum(r.total_cost for r in service_records if r.total_cost)

    return VehicleDetailResponse(
        id=vehicle.id,
        organization_id=vehicle.organization_id,
        assigned_driver_id=vehicle.assigned_driver_id,
        assigned_driver_name=driver_name,
        assigned_driver_phone=driver_phone,
        vin=vehicle.vin,
        license_plate=vehicle.license_plate,
        registration_province=vehicle.registration_province,
        make=vehicle.make,
        model=vehicle.model,
        year=vehicle.year,
        fuel_type=vehicle.fuel_type,
        initial_odometer_km=vehicle.initial_odometer_km,
        current_odometer_km=vehicle.current_odometer_km,
        status=vehicle.status,
        photo_url=vehicle.photo_url,
        is_ad_rewarded=vehicle.is_ad_rewarded,
        custom_specs=vehicle.custom_specs or {},
        created_at=vehicle.created_at,
        updated_at=vehicle.updated_at,
        active_schedules_count=schedules_count,
        total_service_records_count=records_count,
        total_expenses_cost=total_cost,
    )

@router.patch("/{vehicle_id}/status", response_model=VehicleResponse)
def update_vehicle_status(
    vehicle_id: str,
    req: VehicleStatusUpdateRequest,
    organization_id: str = Query(..., description="Organization ID for tenant isolation"),
    db: Session = Depends(get_db)
):
    """
    UC-026: Update Vehicle Status (ACTIVE, MAINTENANCE, INACTIVE).
    """
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    if vehicle.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Vehicle belongs to a different organization."
        )

    new_status = req.status.upper().strip()
    if new_status not in ["ACTIVE", "MAINTENANCE", "INACTIVE"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status. Must be ACTIVE, MAINTENANCE, or INACTIVE."
        )

    vehicle.status = new_status
    db.commit()
    db.refresh(vehicle)
    return vehicle

@router.patch("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: str,
    req: VehicleUpdateRequest,
    organization_id: str = Query(..., description="Organization ID for tenant isolation"),
    db: Session = Depends(get_db)
):
    """
    UC-027: Update Vehicle Metadata & Specifications.
    Validates organization ownership, checks custom specs payload, and logs audit record if manual odometer correction > 500km.
    """
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.deleted_at == None
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    if vehicle.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Vehicle belongs to a different organization."
        )

    if req.custom_specs is not None and not isinstance(req.custom_specs, dict):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid custom specs structure. Must be a key-value dictionary."
        )

    # Alternate Flow A1 — Odometer manual correction audit log
    if req.current_odometer_km is not None:
        discrepancy = abs(req.current_odometer_km - vehicle.current_odometer_km)
        if discrepancy > 500.0:
            audit_entry = AuditLog(
                organization_id=organization_id,
                action="ODOMETER_MANUAL_CORRECTION",
                payload={
                    "vehicle_id": vehicle_id,
                    "previous_odometer_km": vehicle.current_odometer_km,
                    "new_odometer_km": req.current_odometer_km,
                    "discrepancy_km": req.current_odometer_km - vehicle.current_odometer_km,
                }
            )
            db.add(audit_entry)

    # Apply updates
    if req.license_plate is not None:
        vehicle.license_plate = req.license_plate.upper().strip()
    if req.registration_province is not None:
        vehicle.registration_province = req.registration_province.strip()
    if req.make is not None:
        vehicle.make = req.make.strip().title()
    if req.model is not None:
        vehicle.model = req.model.strip().title()
    if req.year is not None:
        vehicle.year = req.year
    if req.fuel_type is not None:
        vehicle.fuel_type = req.fuel_type
    if req.current_odometer_km is not None:
        vehicle.current_odometer_km = req.current_odometer_km
    if req.assigned_driver_id is not None:
        vehicle.assigned_driver_id = req.assigned_driver_id
    if req.photo_url is not None:
        vehicle.photo_url = req.photo_url
    if req.custom_specs is not None:
        updated_specs = dict(vehicle.custom_specs or {})
        updated_specs.update(req.custom_specs)
        vehicle.custom_specs = updated_specs

    db.commit()
    db.refresh(vehicle)
    return vehicle

