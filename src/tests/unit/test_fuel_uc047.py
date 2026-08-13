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
import app.models as models
from app.models.organization import Organization
from app.models.vehicle import Vehicle
from app.models.fuel_log import FuelLog
from app.models.expense_log import ExpenseLog
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
    org = Organization(id="org-fuel-uc047", name="Fuel History Fleet", is_personal=False)
    db.add(org)
    db.commit()

    vehicle = Vehicle(
        id="veh-fuel-047",
        organization_id=org.id,
        license_plate="UC047-KPL",
        registration_province="Punjab",
        make="Toyota",
        model="Corolla",
        year=2022,
        fuel_type="Petrol",
        initial_odometer_km=50000.0,
        current_odometer_km=50000.0
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    db.close()

    return {"org_id": "org-fuel-uc047", "vehicle_id": "veh-fuel-047"}

def test_get_fuel_logs_history(client, test_setup):
    """
    UC-047: Test retrieving fuel log history via GET /api/v1/fuel.
    Should return entries sorted by log date descending.
    """
    # Insert 2 fuel logs
    client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "odometer": 50400.0,
            "fuel_amount_liters": 40.0,
            "cost_amount": 11200.0,
            "fuel_type": "Petrol",
            "is_full_tank": True
        }
    )

    client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "odometer": 50850.0,
            "fuel_amount_liters": 45.0,
            "cost_amount": 12600.0,
            "fuel_type": "Petrol",
            "is_full_tank": True
        }
    )

    response = client.get(
        f"/api/v1/fuel?vehicle_id={test_setup['vehicle_id']}&organization_id={test_setup['org_id']}"
    )

    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 2
    assert logs[0]["odometer_km"] == 50850.0
    assert logs[1]["odometer_km"] == 50400.0

def test_distance_and_efficiency_calculation(client, test_setup):
    """
    UC-047 Acceptance Criterion: WHEN two consecutive full-tank fuel logs are created
    THE SYSTEM SHALL calculate distance / liters and store the result in calculated_efficiency_kpl & distance_km.
    """
    # Log 1: 50,000 km (First fill-up)
    r1 = client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "odometer": 50000.0,
            "fuel_amount_liters": 40.0,
            "cost_amount": 11200.0,
            "is_full_tank": True
        }
    )
    assert r1.status_code == 201
    d1 = r1.json()
    assert d1["calculated_efficiency_kpl"] is None
    assert d1["distance_km"] is None

    # Log 2: 50,500 km (+500 km, 40 liters -> 12.5 km/L)
    r2 = client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "odometer": 50500.0,
            "fuel_amount_liters": 40.0,
            "cost_amount": 11200.0,
            "is_full_tank": True
        }
    )
    assert r2.status_code == 201
    d2 = r2.json()
    assert d2["distance_km"] == 500.0
    assert d2["calculated_efficiency_kpl"] == 12.5
    assert d2["is_leak_alert"] is False

def test_partial_fill_up_skips_efficiency(client, test_setup):
    """
    UC-047 Alternate Flow A1: Partial fill-up (is_full_tank = False) skips efficiency calculation.
    """
    # Log 1: Full tank at 50,000 km
    client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "odometer": 50000.0,
            "fuel_amount_liters": 40.0,
            "cost_amount": 11200.0,
            "is_full_tank": True
        }
    )

    # Log 2: Partial fill at 50,300 km
    r2 = client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "odometer": 50300.0,
            "fuel_amount_liters": 15.0,
            "cost_amount": 4200.0,
            "is_full_tank": False
        }
    )
    assert r2.status_code == 201
    d2 = r2.json()
    assert d2["is_full_tank"] is False
    assert d2["calculated_efficiency_kpl"] is None
    assert d2["distance_km"] is None

def test_fuel_leak_anomaly_detection_alert(client, test_setup):
    """
    UC-047 Main Flow 5: If efficiency is 30% lower than vehicle baseline average,
    system flags entry for review (is_leak_alert = True).
    """
    # 1. First full tank at 50,000 km
    client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "odometer": 50000.0,
            "fuel_amount_liters": 40.0,
            "cost_amount": 11200.0,
            "is_full_tank": True
        }
    )

    # 2. Second full tank at 50,500 km (+500 km, 40 L -> 12.5 km/L baseline)
    r2 = client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "odometer": 50500.0,
            "fuel_amount_liters": 40.0,
            "cost_amount": 11200.0,
            "is_full_tank": True
        }
    )
    assert r2.json()["calculated_efficiency_kpl"] == 12.5
    assert r2.json()["is_leak_alert"] is False

    # 3. Third full tank at 50,700 km (+200 km, 40 L -> 5.0 km/L)
    # Baseline average is 12.5 km/L. 5.0 km/L is 60% below baseline (> 30% drop threshold).
    r3 = client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json={
            "vehicle_id": test_setup["vehicle_id"],
            "odometer": 50700.0,
            "fuel_amount_liters": 40.0,
            "cost_amount": 11200.0,
            "is_full_tank": True
        }
    )
    assert r3.status_code == 201
    d3 = r3.json()
    assert d3["calculated_efficiency_kpl"] == 5.0
    assert d3["is_leak_alert"] is True
