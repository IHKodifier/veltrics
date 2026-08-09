import sys
import os
import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app
from app.db.session import Base, get_db
from app.models.organization import Organization
from app.models.vehicle import Vehicle
from app.models.maintenance import MaintenanceSchedule, ServiceRecord
from app.db.seed import seed_database

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    seed_database(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_setup(client):
    db = TestingSessionLocal()
    org1 = Organization(name="Primary Org", is_personal=False)
    org2 = Organization(name="Secondary Org", is_personal=False)
    db.add_all([org1, org2])
    db.commit()
    db.refresh(org1)
    db.refresh(org2)

    vehicle = Vehicle(
        organization_id=org1.id,
        license_plate="LOG-1036",
        registration_province="Sindh",
        make="Toyota",
        model="Corolla",
        year=2023,
        fuel_type="Petrol",
        initial_odometer_km=5000.0,
        current_odometer_km=10000.0,
        status="ACTIVE"
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    schedule = MaintenanceSchedule(
        organization_id=org1.id,
        vehicle_id=vehicle.id,
        task_name="Engine Oil & Filter Change",
        interval_km=5000,
        interval_days=180,
        last_performed_km=5000.0,
        last_performed_date=date(2026, 1, 1),
        next_due_km=10000.0,
        next_due_date=date(2026, 7, 1),
        is_active=True
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    db.close()

    return {
        "org1_id": org1.id,
        "org2_id": org2.id,
        "vehicle_id": vehicle.id,
        "schedule_id": schedule.id,
    }

def test_log_service_record_success(client, test_setup):
    """UC-036: POST /api/v1/maintenance logs service record and updates linked schedule targets."""
    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "maintenance_schedule_id": test_setup["schedule_id"],
        "service_type": "Engine Oil & Filter Change",
        "cost": 6500.0,
        "service_date": "2026-08-01",
        "odometer_reading": 11000.0,
        "service_provider_name": "Toyota Central Motors",
        "notes": "Replaced synthetic oil and OEM oil filter",
        "photo_url": "https://storage.veltrics.com/invoices/inv-1001.jpg"
    }

    response = client.post(
        "/api/v1/maintenance",
        json=payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["vehicle_id"] == test_setup["vehicle_id"]
    assert data["maintenance_schedule_id"] == test_setup["schedule_id"]
    assert data["total_cost"] == 6500.0
    assert data["odometer_km"] == 11000.0
    assert data["service_center_name"] == "Toyota Central Motors"
    assert data["notes"] == "Replaced synthetic oil and OEM oil filter"

    # Verify Schedule Reset in DB
    db = TestingSessionLocal()
    sched = db.query(MaintenanceSchedule).filter(MaintenanceSchedule.id == test_setup["schedule_id"]).first()
    assert sched.last_performed_km == 11000.0
    assert sched.last_performed_date == date(2026, 8, 1)
    assert sched.next_due_km == 16000.0  # 11000 + 5000
    assert sched.next_due_date == date(2026, 8, 1) + timedelta(days=180)
    db.close()

def test_log_service_record_auto_update_odometer(client, test_setup):
    """UC-036: Odometer reading > current_odometer_km updates vehicle current_odometer_km."""
    # Log higher odometer
    payload_high = {
        "vehicle_id": test_setup["vehicle_id"],
        "service_type": "Brake Inspection",
        "cost": 2500.0,
        "service_date": "2026-08-05",
        "odometer_reading": 14500.0,
    }

    res_high = client.post(
        "/api/v1/maintenance",
        json=payload_high,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert res_high.status_code == 201

    db = TestingSessionLocal()
    veh = db.query(Vehicle).filter(Vehicle.id == test_setup["vehicle_id"]).first()
    assert veh.current_odometer_km == 14500.0
    db.close()

    # Log lower odometer reading (e.g. past record)
    payload_low = {
        "vehicle_id": test_setup["vehicle_id"],
        "service_type": "Wiper Replacement",
        "cost": 800.0,
        "service_date": "2026-07-15",
        "odometer_reading": 12000.0,
    }
    res_low = client.post(
        "/api/v1/maintenance",
        json=payload_low,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert res_low.status_code == 201

    db = TestingSessionLocal()
    veh2 = db.query(Vehicle).filter(Vehicle.id == test_setup["vehicle_id"]).first()
    assert veh2.current_odometer_km == 14500.0  # Remains unchanged
    db.close()

def test_log_service_record_match_by_service_type(client, test_setup):
    """UC-036: Omitting maintenance_schedule_id matches schedule item by task name substring."""
    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "service_type": "Engine Oil",
        "cost": 5000.0,
        "service_date": "2026-08-07",
        "odometer_reading": 12500.0
    }

    response = client.post(
        "/api/v1/maintenance",
        json=payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["maintenance_schedule_id"] == test_setup["schedule_id"]

    db = TestingSessionLocal()
    sched = db.query(MaintenanceSchedule).filter(MaintenanceSchedule.id == test_setup["schedule_id"]).first()
    assert sched.last_performed_km == 12500.0
    assert sched.next_due_km == 17500.0
    db.close()

def test_log_service_record_validation_errors(client, test_setup):
    """UC-036: Rejects negative cost, negative odometer, whitespace service_type, or invalid vehicle_id."""
    # Negative cost
    res_neg_cost = client.post(
        "/api/v1/maintenance",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "service_type": "Oil Change",
            "cost": -100.0,
            "service_date": "2026-08-01",
            "odometer_reading": 10000.0
        },
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert res_neg_cost.status_code == 422

    # Negative odometer
    res_neg_odo = client.post(
        "/api/v1/maintenance",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "service_type": "Oil Change",
            "cost": 500.0,
            "service_date": "2026-08-01",
            "odometer_reading": -50.0
        },
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert res_neg_odo.status_code == 422

    # Whitespace service type
    res_ws = client.post(
        "/api/v1/maintenance",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "service_type": "   ",
            "cost": 500.0,
            "service_date": "2026-08-01",
            "odometer_reading": 10000.0
        },
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert res_ws.status_code == 422

    # Invalid vehicle ID
    res_inv_veh = client.post(
        "/api/v1/maintenance",
        json={
            "vehicle_id": "non-existent-vehicle-id",
            "service_type": "Oil Change",
            "cost": 500.0,
            "service_date": "2026-08-01",
            "odometer_reading": 10000.0
        },
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert res_inv_veh.status_code == 404

def test_tenant_isolation_uc036(client, test_setup):
    """UC-036: Enforces X-Organization-ID header presence and cross-tenant access protection."""
    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "service_type": "Transmission Service",
        "cost": 12000.0,
        "service_date": "2026-08-01",
        "odometer_reading": 10000.0
    }

    # Missing header -> 400
    res_no_hdr = client.post("/api/v1/maintenance", json=payload)
    assert res_no_hdr.status_code == 400

    # Wrong org header -> 404
    res_wrong_org = client.post(
        "/api/v1/maintenance",
        json=payload,
        headers={"X-Organization-ID": test_setup["org2_id"]}
    )
    assert res_wrong_org.status_code == 404
