import sys
import os
import pytest
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
from app.models.audit_log import AuditLog
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
        license_plate="LEA-1027",
        registration_province="Punjab",
        make="Honda",
        model="Civic",
        year=2023,
        fuel_type="Petrol",
        initial_odometer_km=5000.0,
        current_odometer_km=5200.0,
        status="ACTIVE",
        custom_specs={"engine_capacity_cc": 1500}
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    db.close()

    return {"org1": org1, "org2": org2, "vehicle": vehicle}

def test_update_vehicle_success(client, test_setup):
    """
    Test 1: Verify PATCH /api/v1/vehicles/{vehicle_id} successfully updates vehicle metadata & specs.
    """
    vehicle_id = test_setup["vehicle"].id
    org1_id = test_setup["org1"].id

    payload = {
        "license_plate": "LEC-8888",
        "registration_province": "Sindh",
        "fuel_type": "Hybrid",
        "custom_specs": {
            "tire_pressure_psi": 32,
            "oil_type": "0W-20"
        }
    }

    response = client.patch(f"/api/v1/vehicles/{vehicle_id}?organization_id={org1_id}", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == vehicle_id
    assert data["license_plate"] == "LEC-8888"
    assert data["registration_province"] == "Sindh"
    assert data["fuel_type"] == "Hybrid"
    assert data["custom_specs"]["engine_capacity_cc"] == 1500
    assert data["custom_specs"]["tire_pressure_psi"] == 32
    assert data["custom_specs"]["oil_type"] == "0W-20"

def test_update_vehicle_tenant_isolation(client, test_setup):
    """
    Test 2: Verify updating vehicle under wrong organization_id returns HTTP 403 Forbidden.
    """
    vehicle_id = test_setup["vehicle"].id
    org2_id = test_setup["org2"].id

    payload = {"license_plate": "HACK-999"}
    response = client.patch(f"/api/v1/vehicles/{vehicle_id}?organization_id={org2_id}", json=payload)
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

def test_update_vehicle_not_found(client, test_setup):
    """
    Test 3: Verify updating non-existent vehicle returns HTTP 404 Not Found.
    """
    org1_id = test_setup["org1"].id
    payload = {"license_plate": "NON-0000"}
    response = client.patch(f"/api/v1/vehicles/non-existent-id-999?organization_id={org1_id}", json=payload)
    assert response.status_code == 404
    assert "Vehicle not found" in response.json()["detail"]

def test_update_vehicle_odometer_audit_log(client, test_setup):
    """
    Test 4: Verify manual odometer update with discrepancy > 500 km generates an AuditLog entry.
    """
    vehicle_id = test_setup["vehicle"].id
    org1_id = test_setup["org1"].id

    # Current odometer is 5200.0. Update to 6000.0 (discrepancy = 800 km > 500 km)
    payload = {"current_odometer_km": 6000.0}
    response = client.patch(f"/api/v1/vehicles/{vehicle_id}?organization_id={org1_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["current_odometer_km"] == 6000.0

    # Query DB directly to check audit log creation
    db = TestingSessionLocal()
    audit_logs = db.query(AuditLog).filter(
        AuditLog.organization_id == org1_id,
        AuditLog.action == "ODOMETER_MANUAL_CORRECTION"
    ).all()
    db.close()

    assert len(audit_logs) == 1
    log = audit_logs[0]
    assert log.payload["vehicle_id"] == vehicle_id
    assert log.payload["previous_odometer_km"] == 5200.0
    assert log.payload["new_odometer_km"] == 6000.0
    assert log.payload["discrepancy_km"] == 800.0

def test_update_vehicle_invalid_custom_specs(client, test_setup):
    """
    Test 5: Verify non-dictionary custom_specs payload returns HTTP 422 Unprocessable Entity.
    """
    vehicle_id = test_setup["vehicle"].id
    org1_id = test_setup["org1"].id

    payload = {"custom_specs": "invalid_string_instead_of_dict"}
    response = client.patch(f"/api/v1/vehicles/{vehicle_id}?organization_id={org1_id}", json=payload)
    assert response.status_code == 422
