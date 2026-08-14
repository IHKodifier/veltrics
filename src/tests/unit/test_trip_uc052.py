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
    org = Organization(id="org-trip-uc052", name="Veltrics Trip Test Org", created_at=datetime.utcnow())
    db.add(org)
    vehicle = Vehicle(
        id="veh-trip-052",
        organization_id="org-trip-uc052",
        vin="1HGCR2F83HA000052",
        license_plate="TRIP-052",
        make="Toyota",
        model="Corolla",
        year=2023,
        current_odometer_km=10000.0,
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
        "org_id": "org-trip-uc052",
        "vehicle_id": "veh-trip-052"
    }

def test_start_and_stop_trip_success(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    # 1. Start active GPS trip
    start_payload = {
        "vehicle_id": veh_id,
        "start_odometer_km": 10000.0,
        "origin_name": "Lahore Hub",
        "trip_purpose": "BUSINESS",
        "start_time": datetime.utcnow().isoformat()
    }
    r_start = client.post(f"/api/v1/trips/start?organization_id={org_id}", json=start_payload)
    assert r_start.status_code == 201
    trip_data = r_start.json()
    trip_id = trip_data["id"]
    assert trip_data["status"] == "IN_PROGRESS"
    assert trip_data["origin_name"] == "Lahore Hub"

    # 2. Stop active GPS trip
    stop_payload = {
        "end_odometer_km": 10150.0,
        "destination_name": "Islamabad Station",
        "end_time": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
        "notes": "Completed highway delivery trip",
        "gps_polyline_json": "[{\"lat\": 31.52, \"lng\": 74.35}, {\"lat\": 33.68, \"lng\": 73.04}]"
    }
    r_stop = client.post(f"/api/v1/trips/{trip_id}/stop?organization_id={org_id}", json=stop_payload)
    assert r_stop.status_code == 200
    stop_data = r_stop.json()
    assert stop_data["status"] == "COMPLETED"
    assert stop_data["distance_km"] == 150.0
    assert stop_data["destination_name"] == "Islamabad Station"

    # 3. Verify vehicle current odometer updated
    r_veh = client.get(f"/api/v1/vehicles/{veh_id}?organization_id={org_id}")
    assert r_veh.status_code == 200
    assert r_veh.json()["current_odometer_km"] == 10150.0

def test_log_manual_trip_success(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    now = datetime.utcnow()
    manual_payload = {
        "vehicle_id": veh_id,
        "start_odometer_km": 10150.0,
        "end_odometer_km": 10210.0,
        "origin_name": "Islamabad Station",
        "destination_name": "Rawalpindi Depot",
        "trip_purpose": "BUSINESS",
        "is_manual": True,
        "start_time": (now - timedelta(hours=1)).isoformat(),
        "end_time": now.isoformat(),
        "notes": "Client meeting trip"
    }

    r = client.post(f"/api/v1/trips?organization_id={org_id}", json=manual_payload)
    assert r.status_code == 201
    data = r.json()
    assert data["status"] == "COMPLETED"
    assert data["distance_km"] == 60.0
    assert data["is_manual"] is True

    # Check vehicle current odometer
    r_veh = client.get(f"/api/v1/vehicles/{veh_id}?organization_id={org_id}")
    assert r_veh.json()["current_odometer_km"] == 10210.0

def test_reject_invalid_end_odometer(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    invalid_payload = {
        "vehicle_id": veh_id,
        "start_odometer_km": 10000.0,
        "end_odometer_km": 9900.0, # invalid lower end odometer
        "origin_name": "Lahore",
        "destination_name": "Kasur",
        "trip_purpose": "PERSONAL",
        "is_manual": True
    }

    r = client.post(f"/api/v1/trips?organization_id={org_id}", json=invalid_payload)
    assert r.status_code == 422
    assert "greater than or equal to" in r.json()["detail"]

def test_get_trips_history(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    now = datetime.utcnow()
    # Create two trips
    client.post(
        f"/api/v1/trips?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "start_odometer_km": 10000.0,
            "end_odometer_km": 10050.0,
            "origin_name": "A",
            "destination_name": "B",
            "trip_purpose": "BUSINESS",
            "is_manual": True,
            "start_time": (now - timedelta(hours=2)).isoformat(),
            "end_time": (now - timedelta(hours=1)).isoformat()
        }
    )

    r_hist = client.get(f"/api/v1/trips?vehicle_id={veh_id}&organization_id={org_id}")
    assert r_hist.status_code == 200
    trips = r_hist.json()
    assert len(trips) == 1
    assert trips[0]["distance_km"] == 50.0
