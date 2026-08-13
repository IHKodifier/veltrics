import sys
import os
import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app
from app.db.session import Base, get_db
from app.models.organization import Organization
from app.models.vehicle import Vehicle
from app.models.trip import Trip

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    org = Organization(id="org-trip-uc054", name="Veltrics Trip Edit Test Org", created_at=datetime.utcnow())
    db.add(org)
    vehicle = Vehicle(
        id="veh-trip-054",
        organization_id="org-trip-uc054",
        vin="1HGCR2F83HA000054",
        license_plate="TRIP-054",
        make="Honda",
        model="Civic",
        year=2023,
        current_odometer_km=15000.0,
        fuel_type="PETROL",
        status="ACTIVE",
        created_at=datetime.utcnow()
    )
    db.add(vehicle)
    db.commit()
    db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_setup():
    return {
        "org_id": "org-trip-uc054",
        "vehicle_id": "veh-trip-054"
    }

def test_update_trip_success(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    # 1. Create initial trip
    r_create = client.post(
        f"/api/v1/trips?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "start_odometer_km": 15000.0,
            "end_odometer_km": 15050.0,
            "origin_name": "Lahore",
            "destination_name": "Sheikhupura",
            "trip_purpose": "PERSONAL",
            "is_manual": True
        }
    )
    assert r_create.status_code == 201
    trip_id = r_create.json()["id"]
    assert r_create.json()["distance_km"] == 50.0
    assert r_create.json()["trip_purpose"] == "PERSONAL"

    # 2. Update trip
    r_update = client.patch(
        f"/api/v1/trips/{trip_id}?organization_id={org_id}",
        json={
            "end_odometer_km": 15120.0,
            "destination_name": "Gujranwala",
            "trip_purpose": "BUSINESS",
            "notes": "Updated client meeting route"
        }
    )
    assert r_update.status_code == 200
    data = r_update.json()
    assert data["distance_km"] == 120.0
    assert data["destination_name"] == "Gujranwala"
    assert data["trip_purpose"] == "BUSINESS"
    assert data["notes"] == "Updated client meeting route"

def test_soft_delete_trip_success(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    r_create = client.post(
        f"/api/v1/trips?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "start_odometer_km": 15120.0,
            "end_odometer_km": 15180.0,
            "trip_purpose": "BUSINESS",
            "is_manual": True
        }
    )
    trip_id = r_create.json()["id"]

    # Delete trip
    r_del = client.delete(f"/api/v1/trips/{trip_id}?organization_id={org_id}")
    assert r_del.status_code == 200
    assert "deleted successfully" in r_del.json()["message"].lower()

    # Verify trip no longer in list
    r_list = client.get(f"/api/v1/trips?vehicle_id={veh_id}&organization_id={org_id}")
    assert r_list.status_code == 200
    assert len(r_list.json()) == 0

def test_delete_nonexistent_trip_returns_404(client, test_setup):
    org_id = test_setup["org_id"]
    r = client.delete(f"/api/v1/trips/nonexistent-id-055?organization_id={org_id}")
    assert r.status_code == 404
