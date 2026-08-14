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
    org1 = Organization(name="Primary Org", is_personal=False)
    org2 = Organization(name="Secondary Org", is_personal=False)
    db.add_all([org1, org2])
    db.commit()
    db.refresh(org1)
    db.refresh(org2)

    vehicle = Vehicle(
        organization_id=org1.id,
        license_plate="MNT-1035",
        registration_province="Punjab",
        make="Honda",
        model="Civic",
        year=2022,
        fuel_type="Petrol",
        initial_odometer_km=10000.0,
        current_odometer_km=12000.0,
        status="ACTIVE"
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    db.close()

    return {
        "org1_id": org1.id,
        "org2_id": org2.id,
        "vehicle_id": vehicle.id,
    }

def test_create_custom_maintenance_schedule_success(client, test_setup):
    """UC-035: POST /api/v1/maintenance/schedules creates custom schedule with default last_performed base."""
    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "task_name": "Brake Fluid Flush",
        "interval_km": 20000,
        "interval_days": 365,
    }

    response = client.post(
        "/api/v1/maintenance/schedules",
        json=payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["task_name"] == "Brake Fluid Flush"
    assert data["interval_km"] == 20000
    assert data["interval_days"] == 365
    assert data["last_performed_km"] == 12000.0
    assert data["next_due_km"] == 32000.0  # 12000 + 20000
    assert data["is_active"] is True
    assert data["vehicle_id"] == test_setup["vehicle_id"]

def test_create_schedule_with_custom_last_performed(client, test_setup):
    """UC-035: POST /api/v1/maintenance/schedules uses provided last_performed_km and last_performed_date."""
    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "task_name": "Spark Plug Replacement",
        "interval_km": 40000,
        "interval_days": 730,
        "last_performed_km": 8000.0,
        "last_performed_date": "2026-01-01"
    }

    response = client.post(
        "/api/v1/maintenance/schedules",
        json=payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["last_performed_km"] == 8000.0
    assert data["last_performed_date"] == "2026-01-01"
    assert data["next_due_km"] == 48000.0  # 8000 + 40000
    assert data["next_due_date"] == "2028-01-01"  # 2026-01-01 + 730 days

def test_create_schedule_validation(client, test_setup):
    """UC-035: Rejects zero/negative intervals or empty task names with 422."""
    # Zero interval_km
    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "task_name": "Tire Rotation",
        "interval_km": 0,
        "interval_days": 180
    }
    res = client.post("/api/v1/maintenance/schedules", json=payload, headers={"X-Organization-ID": test_setup["org1_id"]})
    assert res.status_code == 422

    # Empty task_name
    payload_empty = {
        "vehicle_id": test_setup["vehicle_id"],
        "task_name": "   ",
        "interval_km": 5000,
        "interval_days": 180
    }
    res_empty = client.post("/api/v1/maintenance/schedules", json=payload_empty, headers={"X-Organization-ID": test_setup["org1_id"]})
    assert res_empty.status_code == 422

def test_patch_maintenance_schedule_recalculation(client, test_setup):
    """UC-035: PATCH /api/v1/maintenance/schedules/{id} updates parameters and recalculates next due targets."""
    # Create initial schedule
    create_res = client.post(
        "/api/v1/maintenance/schedules",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "task_name": "Transmission Fluid Change",
            "interval_km": 30000,
            "interval_days": 365,
            "last_performed_km": 10000.0,
            "last_performed_date": "2026-01-01"
        },
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    sched_id = create_res.json()["id"]

    # Patch interval_km and task_name
    patch_payload = {
        "task_name": "Transmission Fluid & Filter Change",
        "interval_km": 25000,
        "is_active": False
    }
    patch_res = client.patch(
        f"/api/v1/maintenance/schedules/{sched_id}",
        json=patch_payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert patch_res.status_code == 200
    patched_data = patch_res.json()
    assert patched_data["task_name"] == "Transmission Fluid & Filter Change"
    assert patched_data["interval_km"] == 25000
    assert patched_data["next_due_km"] == 35000.0  # 10000 + 25000
    assert patched_data["is_active"] is False

def test_soft_delete_maintenance_schedule(client, test_setup):
    """UC-035: DELETE /api/v1/maintenance/schedules/{id} soft-deletes schedule task."""
    # Create schedule
    create_res = client.post(
        "/api/v1/maintenance/schedules",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "task_name": "Cabin Air Filter Change",
            "interval_km": 15000,
            "interval_days": 180
        },
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    sched_id = create_res.json()["id"]

    # Soft delete
    del_res = client.delete(
        f"/api/v1/maintenance/schedules/{sched_id}",
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert del_res.status_code == 200

    # Verify excluded from list
    list_res = client.get(
        f"/api/v1/maintenance/schedules?vehicle_id={test_setup['vehicle_id']}",
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert list_res.status_code == 200
    sched_ids = [s["id"] for s in list_res.json()]
    assert sched_id not in sched_ids

    # Verify deleted_at is populated in DB
    db = TestingSessionLocal()
    sched_in_db = db.query(MaintenanceSchedule).filter(MaintenanceSchedule.id == sched_id).first()
    assert sched_in_db is not None
    assert sched_in_db.deleted_at is not None
    db.close()

def test_tenant_isolation_uc035(client, test_setup):
    """UC-035: Header validation and tenant cross-access isolation."""
    # POST without header
    res_no_hdr = client.post("/api/v1/maintenance/schedules", json={
        "vehicle_id": test_setup["vehicle_id"],
        "task_name": "Test",
        "interval_km": 1000,
        "interval_days": 30
    })
    assert res_no_hdr.status_code == 400

    # POST with wrong org header
    res_wrong_org = client.post("/api/v1/maintenance/schedules", json={
        "vehicle_id": test_setup["vehicle_id"],
        "task_name": "Test",
        "interval_km": 1000,
        "interval_days": 30
    }, headers={"X-Organization-ID": test_setup["org2_id"]})
    assert res_wrong_org.status_code == 404

    # Create schedule in org1
    create_res = client.post(
        "/api/v1/maintenance/schedules",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "task_name": "Org1 Task",
            "interval_km": 5000,
            "interval_days": 90
        },
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    sched_id = create_res.json()["id"]

    # PATCH with org2 header
    patch_wrong_org = client.patch(
        f"/api/v1/maintenance/schedules/{sched_id}",
        json={"task_name": "Hacked"},
        headers={"X-Organization-ID": test_setup["org2_id"]}
    )
    assert patch_wrong_org.status_code == 404

    # DELETE with org2 header
    del_wrong_org = client.delete(
        f"/api/v1/maintenance/schedules/{sched_id}",
        headers={"X-Organization-ID": test_setup["org2_id"]}
    )
    assert del_wrong_org.status_code == 404
