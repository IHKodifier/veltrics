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
from app.models.fuel_log import FuelLog
from app.db.seed import seed_database

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
    seed_database(db)
    db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_setup(client):
    db = TestingSessionLocal()
    org = Organization(id="org-fuel-uc048", name="Fleet Efficiency Corp", is_personal=False)
    db.add(org)
    db.commit()

    veh_a = Vehicle(
        id="veh-fuel-048a",
        organization_id=org.id,
        license_plate="UC048-VEHA",
        registration_province="Punjab",
        make="Toyota",
        model="Corolla",
        year=2023,
        fuel_type="Petrol",
        initial_odometer_km=10000.0,
        current_odometer_km=10000.0
    )
    veh_b = Vehicle(
        id="veh-fuel-048b",
        organization_id=org.id,
        license_plate="UC048-VEHB",
        registration_province="Sindh",
        make="Honda",
        model="Civic",
        year=2022,
        fuel_type="Petrol",
        initial_odometer_km=20000.0,
        current_odometer_km=20000.0
    )
    db.add(veh_a)
    db.add(veh_b)
    db.commit()
    db.close()

    return {"org_id": "org-fuel-uc048", "veh_a_id": "veh-fuel-048a", "veh_b_id": "veh-fuel-048b"}

def test_get_fuel_logs_paginated(client, test_setup):
    """
    UC-048 Main Flow: App queries GET /api/v1/fuel with pagination (page=1, limit=2).
    Should return paginated items sorted by log_date DESC.
    """
    org_id = test_setup["org_id"]
    veh_id = test_setup["veh_a_id"]

    now = datetime.utcnow()
    for i in range(5):
        log_date = (now - timedelta(days=5 - i)).isoformat()
        client.post(
            f"/api/v1/fuel?organization_id={org_id}",
            json={
                "vehicle_id": veh_id,
                "odometer": 10000.0 + (i + 1) * 100,
                "fuel_amount_liters": 30.0,
                "cost_amount": 9000.0,
                "fuel_type": "Petrol",
                "log_date": log_date,
                "is_full_tank": True
            }
        )

    # Page 1 (limit 2)
    resp1 = client.get(f"/api/v1/fuel?vehicle_id={veh_id}&organization_id={org_id}&page=1&limit=2&paginated=true")
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["total"] == 5
    assert data1["page"] == 1
    assert data1["limit"] == 2
    assert data1["pages"] == 3
    assert len(data1["items"]) == 2
    assert data1["items"][0]["odometer_km"] == 10500.0
    assert data1["items"][1]["odometer_km"] == 10400.0

    # Page 2 (limit 2)
    resp2 = client.get(f"/api/v1/fuel?vehicle_id={veh_id}&organization_id={org_id}&page=2&limit=2&paginated=true")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert len(data2["items"]) == 2
    assert data2["items"][0]["odometer_km"] == 10300.0
    assert data2["items"][1]["odometer_km"] == 10200.0

def test_fleet_aggregate_average_efficiency(client, test_setup):
    """
    UC-048 Acceptance Criterion: System returns fleet aggregate average efficiency across multiple vehicles.
    Vehicle A: +500 km on 40 L = 12.5 km/L
    Vehicle B: +400 km on 50 L = 8.0 km/L
    Fleet Aggregate Avg = (12.5 + 8.0) / 2 = 10.25 km/L
    """
    org_id = test_setup["org_id"]
    veh_a = test_setup["veh_a_id"]
    veh_b = test_setup["veh_b_id"]

    # Vehicle A fill-ups
    client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={"vehicle_id": veh_a, "odometer": 10000.0, "fuel_amount_liters": 40.0, "cost_amount": 12000.0, "is_full_tank": True}
    )
    client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={"vehicle_id": veh_a, "odometer": 10500.0, "fuel_amount_liters": 40.0, "cost_amount": 12000.0, "is_full_tank": True}
    )

    # Vehicle B fill-ups
    client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={"vehicle_id": veh_b, "odometer": 20000.0, "fuel_amount_liters": 50.0, "cost_amount": 15000.0, "is_full_tank": True}
    )
    client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={"vehicle_id": veh_b, "odometer": 20400.0, "fuel_amount_liters": 50.0, "cost_amount": 15000.0, "is_full_tank": True}
    )

    # Query trends
    resp = client.get(f"/api/v1/fuel/trends?organization_id={org_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["fleet_avg_efficiency_kpl"] == 10.25
    assert data["total_cost"] == 54000.0
    assert data["total_liters"] == 180.0

def test_fuel_efficiency_trends_monthly_aggregation(client, test_setup):
    """
    UC-048 Efficiency Trends: Monthly fuel cost totals and efficiency trends per vehicle.
    """
    org_id = test_setup["org_id"]
    veh_id = test_setup["veh_a_id"]

    d1 = datetime(2026, 7, 10, 10, 0, 0).isoformat()
    d2 = datetime(2026, 7, 25, 10, 0, 0).isoformat()
    d3 = datetime(2026, 8, 5, 10, 0, 0).isoformat()

    client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={"vehicle_id": veh_id, "odometer": 10000.0, "fuel_amount_liters": 40.0, "cost_amount": 10000.0, "log_date": d1, "is_full_tank": True}
    )
    client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={"vehicle_id": veh_id, "odometer": 10500.0, "fuel_amount_liters": 40.0, "cost_amount": 11000.0, "log_date": d2, "is_full_tank": True}
    )
    client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={"vehicle_id": veh_id, "odometer": 11000.0, "fuel_amount_liters": 50.0, "cost_amount": 14000.0, "log_date": d3, "is_full_tank": True}
    )

    resp = client.get(f"/api/v1/fuel/trends?vehicle_id={veh_id}&organization_id={org_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["vehicle_id"] == veh_id
    assert data["vehicle_avg_efficiency_kpl"] == 11.25 # (12.5 + 10.0)/2
    assert data["total_cost"] == 35000.0
    assert len(data["monthly_trends"]) >= 2

    jul_trend = next((m for m in data["monthly_trends"] if m["month"] == "2026-07"), None)
    assert jul_trend is not None
    assert jul_trend["total_cost"] == 21000.0
    assert jul_trend["total_liters"] == 80.0

    aug_trend = next((m for m in data["monthly_trends"] if m["month"] == "2026-08"), None)
    assert aug_trend is not None
    assert aug_trend["total_cost"] == 14000.0
    assert aug_trend["total_liters"] == 50.0
