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
    org = Organization(id="org-trip-uc057", name="Veltrics Mileage Summary Test Org", created_at=datetime.utcnow())
    db.add(org)
    vehicle = Vehicle(
        id="veh-trip-057",
        organization_id="org-trip-uc057",
        vin="1HGCR2F83HA000057",
        license_plate="TRIP-057",
        make="Kia",
        model="Sportage",
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
        "org_id": "org-trip-uc057",
        "vehicle_id": "veh-trip-057"
    }

def test_get_mileage_summary_all(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    # Log 2 quick trips
    client.post(
        f"/api/v1/trips/quick?organization_id={org_id}",
        json={"vehicle_id": veh_id, "distance_km": 60.0, "trip_purpose": "BUSINESS"}
    )
    client.post(
        f"/api/v1/trips/quick?organization_id={org_id}",
        json={"vehicle_id": veh_id, "distance_km": 40.0, "trip_purpose": "PERSONAL"}
    )

    r = client.get(f"/api/v1/trips/mileage-summary?organization_id={org_id}")
    assert r.status_code == 200
    summary = r.json()

    assert summary["total_distance_km"] == 100.0
    assert summary["business_distance_km"] == 60.0
    assert summary["personal_distance_km"] == 40.0
    assert summary["total_trips_count"] == 2
    assert summary["business_trips_count"] == 1
    assert summary["personal_trips_count"] == 1
    assert summary["average_trip_distance_km"] == 50.0
    assert summary["estimated_tax_deduction"] == round(60.0 * 0.65, 2)

def test_get_mileage_summary_filtered_by_vehicle(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    client.post(
        f"/api/v1/trips/quick?organization_id={org_id}",
        json={"vehicle_id": veh_id, "distance_km": 80.0, "trip_purpose": "BUSINESS"}
    )

    r = client.get(f"/api/v1/trips/mileage-summary?vehicle_id={veh_id}&organization_id={org_id}")
    assert r.status_code == 200
    summary = r.json()

    assert summary["vehicle_id"] == veh_id
    assert summary["total_distance_km"] == 80.0
    assert summary["business_distance_km"] == 80.0
    assert summary["estimated_tax_deduction"] == round(80.0 * 0.65, 2)
