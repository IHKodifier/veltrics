import sys
import os
import pytest
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
        license_plate="LEA-9999",
        registration_province="Punjab",
        make="Toyota",
        model="Fortuner",
        year=2024,
        fuel_type="Diesel",
        initial_odometer_km=1000.0,
        current_odometer_km=1200.0,
        status="ACTIVE"
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    db.close()

    return {"org1": org1, "org2": org2, "vehicle": vehicle}

def test_get_vehicle_detail_success(client, test_setup):
    """
    Test 1: Verify GET /api/v1/vehicles/{vehicle_id} returns detailed vehicle metadata and summary fields.
    """
    vehicle_id = test_setup["vehicle"].id
    org1_id = test_setup["org1"].id

    response = client.get(f"/api/v1/vehicles/{vehicle_id}?organization_id={org1_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == vehicle_id
    assert data["make"] == "Toyota"
    assert data["model"] == "Fortuner"
    assert data["license_plate"] == "LEA-9999"
    assert data["registration_province"] == "Punjab"
    assert data["status"] == "ACTIVE"
    assert "active_schedules_count" in data
    assert "total_expenses_cost" in data

def test_get_vehicle_detail_not_found(client, test_setup):
    """
    Test 2: Verify non-existent vehicle ID returns HTTP 404 Not Found.
    """
    org1_id = test_setup["org1"].id
    response = client.get(f"/api/v1/vehicles/non-existent-id-999?organization_id={org1_id}")
    assert response.status_code == 404
    assert "Vehicle not found" in response.json()["detail"]

def test_get_vehicle_detail_tenant_forbidden(client, test_setup):
    """
    Test 3: Verify requesting another tenant's vehicle returns HTTP 403 Forbidden.
    """
    vehicle_id = test_setup["vehicle"].id
    org2_id = test_setup["org2"].id  # Wrong organization ID

    response = client.get(f"/api/v1/vehicles/{vehicle_id}?organization_id={org2_id}")
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

def test_update_vehicle_status(client, test_setup):
    """
    Test 4: Verify PATCH /api/v1/vehicles/{vehicle_id}/status updates vehicle status in DB.
    """
    vehicle_id = test_setup["vehicle"].id
    org1_id = test_setup["org1"].id

    # Update to MAINTENANCE
    patch_resp = client.patch(
        f"/api/v1/vehicles/{vehicle_id}/status?organization_id={org1_id}",
        json={"status": "MAINTENANCE"}
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "MAINTENANCE"

    # Verify updated detail
    detail_resp = client.get(f"/api/v1/vehicles/{vehicle_id}?organization_id={org1_id}")
    assert detail_resp.json()["status"] == "MAINTENANCE"
