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
    org = Organization(id="org-fuel-test-101", name="Fuel Test Fleet", is_personal=False)
    db.add(org)
    db.commit()

    vehicle = Vehicle(
        id="veh-fuel-101",
        organization_id=org.id,
        license_plate="FUEL-046",
        registration_province="Punjab",
        make="Honda",
        model="Civic",
        year=2023,
        fuel_type="Petrol",
        initial_odometer_km=10000.0,
        current_odometer_km=10000.0
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    db.close()

    return {"org_id": "org-fuel-test-101", "vehicle_id": "veh-fuel-101"}

def test_create_fuel_log_success(client, test_setup):
    """
    UC-046: Test successful fuel log creation & vehicle current odometer update.
    """
    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "odometer": 10500.0,
        "fuel_amount_liters": 40.0,
        "cost_amount": 11200.0,
        "fuel_type": "Petrol",
        "is_full_tank": True,
        "station_name": "TotalParco DHA"
    }

    response = client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json=payload
    )

    assert response.status_code == 201
    data = response.json()
    assert data["vehicle_id"] == test_setup["vehicle_id"]
    assert data["odometer_km"] == 10500.0
    assert data["quantity_liters"] == 40.0
    assert data["total_cost"] == 11200.0
    assert data["fuel_type"] == "Petrol"
    assert data["is_full_tank"] is True

    # Verify vehicle current odometer updated in database
    db = TestingSessionLocal()
    updated_vehicle = db.query(Vehicle).filter_by(id=test_setup["vehicle_id"]).first()
    assert updated_vehicle.current_odometer_km == 10500.0
    db.close()

def test_linked_expense_auto_creation(client, test_setup):
    """
    UC-046 Acceptance Criterion: WHEN a fuel log entry is saved
    THE SYSTEM SHALL automatically create a linked expense record under category 'FUEL'.
    """
    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "odometer": 10800.0,
        "fuel_amount_liters": 35.0,
        "cost_amount": 9800.0,
        "fuel_type": "Petrol",
        "is_full_tank": True
    }

    response = client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json=payload
    )
    assert response.status_code == 201
    fuel_data = response.json()

    # Query database for auto-created ExpenseLog record
    db = TestingSessionLocal()
    expense = db.query(ExpenseLog).filter_by(
        fuel_log_id=fuel_data["id"],
        vehicle_id=test_setup["vehicle_id"]
    ).first()

    assert expense is not None
    assert expense.category == "FUEL"
    assert expense.amount == 9800.0
    assert expense.organization_id == test_setup["org_id"]
    db.close()

def test_reject_lower_odometer(client, test_setup):
    """
    UC-046 Edge Case: Odometer entry lower than vehicle's current odometer -> API rejects with HTTP 400 Bad Request.
    """
    payload = {
        "vehicle_id": test_setup["vehicle_id"],
        "odometer": 9000.0,  # Current is 10000.0
        "fuel_amount_liters": 30.0,
        "cost_amount": 8400.0
    }

    response = client.post(
        f"/api/v1/fuel?organization_id={test_setup['org_id']}",
        json=payload
    )

    assert response.status_code == 400
    assert "cannot be lower than current vehicle odometer" in response.json()["detail"]

def test_efficiency_calculation_on_subsequent_full_tank(client, test_setup):
    """
    UC-046 & UC-047: Verify calculated km/L efficiency on 2nd full tank fill-up.
    """
    # 1st fill-up at 10000 km
    log1 = {
        "vehicle_id": test_setup["vehicle_id"],
        "odometer": 10000.0,
        "fuel_amount_liters": 40.0,
        "cost_amount": 11200.0,
        "is_full_tank": True
    }
    r1 = client.post(f"/api/v1/fuel?organization_id={test_setup['org_id']}", json=log1)
    assert r1.status_code == 201

    # 2nd fill-up at 10500 km (distance = 500 km, liters = 40.0 -> efficiency = 12.5 km/L)
    log2 = {
        "vehicle_id": test_setup["vehicle_id"],
        "odometer": 10500.0,
        "fuel_amount_liters": 40.0,
        "cost_amount": 11200.0,
        "is_full_tank": True
    }
    r2 = client.post(f"/api/v1/fuel?organization_id={test_setup['org_id']}", json=log2)
    assert r2.status_code == 201
    d2 = r2.json()
    assert d2["calculated_efficiency_kpl"] == 12.5
