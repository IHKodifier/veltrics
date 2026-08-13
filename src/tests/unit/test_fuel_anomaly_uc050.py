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
from app.models.user import User
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

    org = Organization(id="org-anomaly-uc050", name="Veltrics Anomaly Test Org", created_at=datetime.utcnow())
    db.add(org)

    user = User(
        id="usr-anomaly-050",
        firebase_uid="uid_anomaly_050",
        email="test_anomaly@veltrics.com",
        full_name="Anomaly Tester",
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(user)

    vehicle = Vehicle(
        id="veh-anomaly-050",
        organization_id="org-anomaly-uc050",
        make="Toyota",
        model="Hilux",
        year=2023,
        license_plate="ANO-5050",
        current_odometer_km=10000,
        fuel_tank_capacity=60.0,
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
        "org_id": "org-anomaly-uc050",
        "user_id": "usr-anomaly-050",
        "vehicle_id": "veh-anomaly-050"
    }

def test_exceed_tank_capacity_triggers_anomaly(client, test_setup):
    org_id = test_setup["org_id"]
    user_id = test_setup["user_id"]
    vehicle_id = test_setup["vehicle_id"]

    payload = {
        "vehicle_id": vehicle_id,
        "logged_by_user_id": user_id,
        "organization_id": org_id,
        "odometer_km": 10500,
        "quantity_liters": 95.0,  # Exceeds 60L capacity!
        "price_per_liter": 2.50,
        "total_cost": 237.50,
        "fuel_type": "DIESEL",
        "fill_type": "FULL_TANK",
        "station_name": "Shell Station",
        "log_date": "2026-08-13T10:00:00"
    }

    r = client.post("/api/v1/fuel", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["anomaly_detected"] is True
    assert "exceeds vehicle tank capacity" in data["anomaly_reason"].lower()

def test_fetch_unverified_anomalies(client, test_setup):
    org_id = test_setup["org_id"]
    user_id = test_setup["user_id"]
    vehicle_id = test_setup["vehicle_id"]

    # Log anomaly fuel
    client.post("/api/v1/fuel", json={
        "vehicle_id": vehicle_id,
        "logged_by_user_id": user_id,
        "organization_id": org_id,
        "odometer_km": 10500,
        "quantity_liters": 95.0,
        "price_per_liter": 2.50,
        "total_cost": 237.50,
        "fuel_type": "DIESEL",
        "fill_type": "FULL_TANK",
        "log_date": "2026-08-13T10:00:00"
    })

    r = client.get(f"/api/v1/fuel/anomalies?organization_id={org_id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 1
    assert data[0]["anomaly_detected"] is True
    assert data[0]["is_verified"] is False

def test_verify_fuel_anomaly(client, test_setup):
    org_id = test_setup["org_id"]
    user_id = test_setup["user_id"]
    vehicle_id = test_setup["vehicle_id"]

    # Log anomaly fuel
    log_res = client.post("/api/v1/fuel", json={
        "vehicle_id": vehicle_id,
        "logged_by_user_id": user_id,
        "organization_id": org_id,
        "odometer_km": 10500,
        "quantity_liters": 95.0,
        "price_per_liter": 2.50,
        "total_cost": 237.50,
        "fuel_type": "DIESEL",
        "fill_type": "FULL_TANK",
        "log_date": "2026-08-13T10:00:00"
    }).json()

    fuel_log_id = log_res["id"]

    r = client.patch(f"/api/v1/fuel/{fuel_log_id}/verify-anomaly")
    assert r.status_code == 200
    data = r.json()
    assert data["is_verified"] is True
