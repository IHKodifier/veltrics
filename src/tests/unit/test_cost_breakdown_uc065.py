import sys
import os
import pytest
from datetime import datetime, date
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
from app.models.maintenance import ServiceRecord
from app.models.expense_log import ExpenseLog

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

    org = Organization(id="org-cb-uc065", name="Veltrics Cost Breakdown Test Org", created_at=datetime.utcnow())
    db.add(org)

    vehicle = Vehicle(
        id="veh-cb-065",
        organization_id="org-cb-uc065",
        vin="1HGCR2F83HA000065",
        license_plate="CB-065",
        make="Toyota",
        model="Fortuner",
        year=2024,
        current_odometer_km=5000.0,
        fuel_type="DIESEL",
        status="ACTIVE",
        created_at=datetime.utcnow()
    )
    db.add(vehicle)

    # Seed 1 Fuel Log (5000 PKR)
    fuel = FuelLog(
        id="fl-cb-065",
        organization_id="org-cb-uc065",
        vehicle_id="veh-cb-065",
        odometer_km=4000.0,
        quantity_liters=40.0,
        price_per_liter=125.0,
        total_cost=5000.0,
        is_full_tank=True,
        log_date=datetime.utcnow(),
        created_at=datetime.utcnow()
    )
    db.add(fuel)

    # Seed 1 Maintenance Service Record (12000 PKR)
    mnt = ServiceRecord(
        id="ml-cb-065",
        organization_id="org-cb-uc065",
        vehicle_id="veh-cb-065",
        total_cost=12000.0,
        service_date=date.today(),
        created_at=datetime.utcnow()
    )
    db.add(mnt)

    # Seed 1 General Expense Log (1500 PKR)
    exp = ExpenseLog(
        id="exp-cb-065",
        organization_id="org-cb-uc065",
        vehicle_id="veh-cb-065",
        category="TOLL",
        amount=1500.0,
        currency="PKR",
        expense_date=datetime.utcnow(),
        created_at=datetime.utcnow()
    )
    db.add(exp)

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
        "org_id": "org-cb-uc065",
        "vehicle_id": "veh-cb-065"
    }

def test_get_cost_breakdown_all_vehicles(client, test_setup):
    org_id = test_setup["org_id"]

    r = client.get(f"/api/v1/dashboard/cost-breakdown?timeframe=6m&organization_id={org_id}")
    assert r.status_code == 200
    data = r.json()

    assert data["total_fuel_cost"] == 5000.0
    assert data["total_maintenance_cost"] == 12000.0
    assert data["total_other_expense_cost"] == 1500.0
    assert data["grand_total_cost"] == 18500.0
    assert len(data["items"]) > 0

def test_get_cost_breakdown_single_vehicle(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    r = client.get(f"/api/v1/dashboard/cost-breakdown?timeframe=6m&vehicle_id={veh_id}&organization_id={org_id}")
    assert r.status_code == 200
    data = r.json()

    assert data["vehicle_id"] == veh_id
    assert data["grand_total_cost"] == 18500.0
