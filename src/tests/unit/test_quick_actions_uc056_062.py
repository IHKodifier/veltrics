import sys
import os
import pytest
from datetime import datetime
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
    org = Organization(id="org-qa-uc056", name="Veltrics Quick Actions Test Org", created_at=datetime.utcnow())
    db.add(org)
    vehicle = Vehicle(
        id="veh-qa-056",
        organization_id="org-qa-uc056",
        vin="1HGCR2F83HA000056",
        license_plate="QA-056",
        make="Honda",
        model="Vezel",
        year=2023,
        current_odometer_km=10000.0,
        fuel_type="HYBRID",
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
        "org_id": "org-qa-uc056",
        "vehicle_id": "veh-qa-056"
    }

def test_quick_log_trip_success(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    payload = {
        "vehicle_id": veh_id,
        "distance_km": 42.5,
        "origin_name": "Headquarters",
        "destination_name": "Client Site A",
        "trip_purpose": "BUSINESS"
    }

    r = client.post(f"/api/v1/trips/quick?organization_id={org_id}", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["distance_km"] == 42.5
    assert data["trip_purpose"] == "BUSINESS"
    assert data["start_odometer_km"] == 10000.0
    assert data["end_odometer_km"] == 10042.5

def test_quick_log_expense_success(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    payload = {
        "vehicle_id": veh_id,
        "category": "PARKING",
        "amount": 250.0,
        "notes": "Mall Parking Quick Log"
    }

    r = client.post(f"/api/v1/expenses/quick?organization_id={org_id}", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["category"] == "PARKING"
    assert data["amount"] == 250.0
    assert data["notes"] == "Mall Parking Quick Log"
