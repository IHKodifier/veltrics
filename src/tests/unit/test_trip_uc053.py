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
    org = Organization(id="org-trip-uc053", name="Veltrics Trip History Test Org", created_at=datetime.utcnow())
    db.add(org)
    vehicle = Vehicle(
        id="veh-trip-053",
        organization_id="org-trip-uc053",
        vin="1HGCR2F83HA000053",
        license_plate="TRIP-053",
        make="Toyota",
        model="Camry",
        year=2024,
        current_odometer_km=20000.0,
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
        "org_id": "org-trip-uc053",
        "vehicle_id": "veh-trip-053"
    }

def test_get_trips_filtered_by_purpose(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]
    now = datetime.utcnow()

    # Create 2 business trips and 1 personal trip
    client.post(
        f"/api/v1/trips?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "start_odometer_km": 20000.0,
            "end_odometer_km": 20100.0,
            "origin_name": "Site A",
            "destination_name": "Site B",
            "trip_purpose": "BUSINESS",
            "is_manual": True,
            "start_time": (now - timedelta(hours=5)).isoformat(),
            "end_time": (now - timedelta(hours=4)).isoformat()
        }
    )
    client.post(
        f"/api/v1/trips?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "start_odometer_km": 20100.0,
            "end_odometer_km": 20150.0,
            "origin_name": "Site B",
            "destination_name": "HQ",
            "trip_purpose": "BUSINESS",
            "is_manual": True,
            "start_time": (now - timedelta(hours=3)).isoformat(),
            "end_time": (now - timedelta(hours=2)).isoformat()
        }
    )
    client.post(
        f"/api/v1/trips?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "start_odometer_km": 20150.0,
            "end_odometer_km": 20180.0,
            "origin_name": "HQ",
            "destination_name": "Home",
            "trip_purpose": "PERSONAL",
            "is_manual": True,
            "start_time": (now - timedelta(hours=1)).isoformat(),
            "end_time": now.isoformat()
        }
    )

    # Filter BUSINESS
    r_biz = client.get(f"/api/v1/trips?vehicle_id={veh_id}&trip_purpose=BUSINESS&organization_id={org_id}")
    assert r_biz.status_code == 200
    biz_trips = r_biz.json()
    assert len(biz_trips) == 2
    assert all(t["trip_purpose"] == "BUSINESS" for t in biz_trips)

    # Filter PERSONAL
    r_per = client.get(f"/api/v1/trips?vehicle_id={veh_id}&trip_purpose=PERSONAL&organization_id={org_id}")
    assert r_per.status_code == 200
    per_trips = r_per.json()
    assert len(per_trips) == 1
    assert per_trips[0]["trip_purpose"] == "PERSONAL"

def test_get_trip_summary_metrics(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]
    now = datetime.utcnow()

    client.post(
        f"/api/v1/trips?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "start_odometer_km": 20000.0,
            "end_odometer_km": 20100.0,
            "trip_purpose": "BUSINESS",
            "is_manual": True,
            "start_time": (now - timedelta(hours=3)).isoformat()
        }
    )
    client.post(
        f"/api/v1/trips?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "start_odometer_km": 20100.0,
            "end_odometer_km": 20150.0,
            "trip_purpose": "BUSINESS",
            "is_manual": True,
            "start_time": (now - timedelta(hours=2)).isoformat()
        }
    )
    client.post(
        f"/api/v1/trips?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "start_odometer_km": 20150.0,
            "end_odometer_km": 20180.0,
            "trip_purpose": "PERSONAL",
            "is_manual": True,
            "start_time": (now - timedelta(hours=1)).isoformat()
        }
    )

    r_summary = client.get(f"/api/v1/trips/summary?vehicle_id={veh_id}&organization_id={org_id}")
    assert r_summary.status_code == 200
    summary = r_summary.json()
    assert summary["total_distance_km"] == 180.0
    assert summary["business_distance_km"] == 150.0
    assert summary["personal_distance_km"] == 30.0
    assert summary["total_trips_count"] == 3
    assert summary["estimated_tax_deduction"] == 97.5 # 150 km * $0.65/km

def test_trip_history_pagination(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]
    now = datetime.utcnow()

    for i in range(3):
        client.post(
            f"/api/v1/trips?organization_id={org_id}",
            json={
                "vehicle_id": veh_id,
                "start_odometer_km": 20000.0 + (i * 10),
                "end_odometer_km": 20000.0 + ((i + 1) * 10),
                "trip_purpose": "BUSINESS",
                "is_manual": True,
                "start_time": (now - timedelta(hours=3 - i)).isoformat()
            }
        )

    r_page = client.get(f"/api/v1/trips?vehicle_id={veh_id}&paginated=true&page=1&limit=2&organization_id={org_id}")
    assert r_page.status_code == 200
    data = r_page.json()
    assert len(data["items"]) == 2
    assert data["total"] == 3
    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["pages"] == 2
