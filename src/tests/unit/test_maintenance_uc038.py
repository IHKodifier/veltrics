import sys
import os
import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app
from app.db.session import Base, get_db
import app.models as models
from app.models.organization import Organization
from app.models.vehicle import Vehicle
from app.models.maintenance import MaintenanceSchedule
from app.db.seed import seed_database

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

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
    org1 = Organization(name="Primary Org UC038", is_personal=False)
    org2 = Organization(name="Secondary Org UC038", is_personal=False)
    db.add_all([org1, org2])
    db.commit()
    db.refresh(org1)
    db.refresh(org2)

    veh1 = Vehicle(
        organization_id=org1.id,
        license_plate="BULK-038",
        registration_province="Punjab",
        make="Toyota",
        model="Fortuner",
        year=2023,
        fuel_type="Diesel",
        initial_odometer_km=5000.0,
        current_odometer_km=15000.0,
        status="ACTIVE"
    )
    veh2 = Vehicle(
        organization_id=org2.id,
        license_plate="OTHER-038",
        registration_province="Sindh",
        make="Honda",
        model="Civic",
        year=2022,
        fuel_type="Petrol",
        initial_odometer_km=10000.0,
        current_odometer_km=20000.0,
        status="ACTIVE"
    )
    db.add_all([veh1, veh2])
    db.commit()
    db.refresh(veh1)
    db.refresh(veh2)

    sched1 = MaintenanceSchedule(
        organization_id=org1.id,
        vehicle_id=veh1.id,
        task_name="Oil Change",
        interval_km=5000,
        interval_days=180,
        last_performed_km=5000.0,
        next_due_km=10000.0,
        is_active=False
    )
    sched2 = MaintenanceSchedule(
        organization_id=org1.id,
        vehicle_id=veh1.id,
        task_name="Tire Rotation",
        interval_km=10000,
        interval_days=365,
        last_performed_km=5000.0,
        next_due_km=15000.0,
        is_active=False
    )
    db.add_all([sched1, sched2])
    db.commit()
    db.refresh(sched1)
    db.refresh(sched2)
    db.close()

    return {
        "org1_id": org1.id,
        "org2_id": org2.id,
        "veh1_id": veh1.id,
        "veh2_id": veh2.id,
        "sched1_id": sched1.id,
        "sched2_id": sched2.id,
    }

def test_bulk_accept_schedules_all(client, test_setup):
    """UC-038: POST /api/v1/maintenance/schedules/bulk-accept with empty schedule_ids accepts all schedules for vehicle."""
    payload = {
        "vehicle_id": test_setup["veh1_id"],
        "schedule_ids": []
    }
    response = client.post(
        "/api/v1/maintenance/schedules/bulk-accept",
        json=payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for item in data:
        assert item["is_active"] is True

def test_bulk_accept_schedules_specific_ids(client, test_setup):
    """UC-038: POST /api/v1/maintenance/schedules/bulk-accept with specific schedule_ids activates only those schedules."""
    payload = {
        "vehicle_id": test_setup["veh1_id"],
        "schedule_ids": [test_setup["sched1_id"]]
    }
    response = client.post(
        "/api/v1/maintenance/schedules/bulk-accept",
        json=payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == test_setup["sched1_id"]
    assert data[0]["is_active"] is True

    # Verify sched2 is still inactive in DB
    db = TestingSessionLocal()
    s2 = db.query(MaintenanceSchedule).filter(MaintenanceSchedule.id == test_setup["sched2_id"]).first()
    assert s2.is_active is False
    db.close()

def test_bulk_accept_schedules_invalid_vehicle(client, test_setup):
    """UC-038: Returns 404 when vehicle_id is not found in active organization."""
    payload = {
        "vehicle_id": "non-existent-vehicle-uuid",
        "schedule_ids": []
    }
    response = client.post(
        "/api/v1/maintenance/schedules/bulk-accept",
        json=payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found in active organization"

def test_bulk_accept_schedules_invalid_schedule_id(client, test_setup):
    """UC-038: Returns 404 when one or more schedule_ids do not belong to the vehicle."""
    payload = {
        "vehicle_id": test_setup["veh1_id"],
        "schedule_ids": [test_setup["sched1_id"], "invalid-schedule-uuid"]
    }
    response = client.post(
        "/api/v1/maintenance/schedules/bulk-accept",
        json=payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "One or more maintenance schedule IDs not found for this vehicle"

def test_tenant_isolation_uc038(client, test_setup):
    """UC-038: Headers and cross-tenant boundaries are strictly enforced."""
    # Missing header -> 400
    res_no_hdr = client.post(
        "/api/v1/maintenance/schedules/bulk-accept",
        json={"vehicle_id": test_setup["veh1_id"]}
    )
    assert res_no_hdr.status_code == 400

    # Wrong org header -> 404
    res_wrong_org = client.post(
        "/api/v1/maintenance/schedules/bulk-accept",
        json={"vehicle_id": test_setup["veh1_id"]},
        headers={"X-Organization-ID": test_setup["org2_id"]}
    )
    assert res_wrong_org.status_code == 404
