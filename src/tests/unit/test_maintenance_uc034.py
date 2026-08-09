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
        license_plate="MNT-1034",
        registration_province="Punjab",
        make="Toyota",
        model="Corolla",
        year=2023,
        fuel_type="Petrol",
        initial_odometer_km=10000.0,
        current_odometer_km=10000.0,
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

def test_get_maintenance_schedules_autopopulate(client, test_setup):
    """UC-034: GET /api/v1/maintenance/schedules should auto-populate schedule templates for new vehicle."""
    response = client.get(
        f"/api/v1/maintenance/schedules?vehicle_id={test_setup['vehicle_id']}",
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    task_names = [item["task_name"] for item in data]
    assert "Engine Oil & Filter Change" in task_names

    # Check next_due calculation
    oil_task = next(item for item in data if item["task_name"] == "Engine Oil & Filter Change")
    assert oil_task["vehicle_id"] == test_setup["vehicle_id"]
    assert oil_task["next_due_km"] == 15000.0  # 10000 + 5000

def test_log_maintenance_task_success(client, test_setup):
    """UC-034: POST /api/v1/maintenance logs record, updates odometer, and resets schedule."""
    # First query schedules to auto-populate
    client.get(
        f"/api/v1/maintenance/schedules?vehicle_id={test_setup['vehicle_id']}",
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )

    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "service_type": "Engine Oil & Filter Change",
        "cost": 6500.0,
        "service_date": str(date.today()),
        "odometer_reading": 12500.0,
        "service_provider_name": "Toyota Authorized Service",
        "notes": "Replaced synthetic oil and genuine filter"
    }

    response = client.post(
        "/api/v1/maintenance",
        json=payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert response.status_code == 201
    res_data = response.json()
    assert res_data["total_cost"] == 6500.0
    assert res_data["odometer_km"] == 12500.0
    assert res_data["service_center_name"] == "Toyota Authorized Service"

    # Verify vehicle current odometer updated in DB
    db = TestingSessionLocal()
    veh = db.query(Vehicle).filter(Vehicle.id == test_setup["vehicle_id"]).first()
    assert veh.current_odometer_km == 12500.0

    # Verify maintenance schedule reset
    sched = db.query(MaintenanceSchedule).filter(
        MaintenanceSchedule.vehicle_id == test_setup["vehicle_id"],
        MaintenanceSchedule.task_name == "Engine Oil & Filter Change"
    ).first()
    assert sched is not None
    assert sched.last_performed_km == 12500.0
    assert sched.next_due_km == 17500.0  # 12500 + 5000
    db.close()

def test_log_maintenance_negative_cost_rejected(client, test_setup):
    """UC-034: POST /api/v1/maintenance rejects negative cost with HTTP 422."""
    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "service_type": "OIL_CHANGE",
        "cost": -500.0,
        "service_date": str(date.today()),
        "odometer_reading": 11000.0
    }

    response = client.post(
        "/api/v1/maintenance",
        json=payload,
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert response.status_code == 422

def test_maintenance_tenant_isolation(client, test_setup):
    """UC-034: Tenant cross-access rejected."""
    # Attempting to access org1's vehicle with org2's header
    response = client.get(
        f"/api/v1/maintenance/schedules?vehicle_id={test_setup['vehicle_id']}",
        headers={"X-Organization-ID": test_setup["org2_id"]}
    )
    assert response.status_code == 404

    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "service_type": "OIL_CHANGE",
        "cost": 1000.0,
        "service_date": str(date.today()),
        "odometer_reading": 11000.0
    }
    post_res = client.post(
        "/api/v1/maintenance",
        json=payload,
        headers={"X-Organization-ID": test_setup["org2_id"]}
    )
    assert post_res.status_code == 404
