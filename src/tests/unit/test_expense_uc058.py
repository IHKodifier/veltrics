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
    org = Organization(id="org-exp-uc058", name="Veltrics Expense Test Org", created_at=datetime.utcnow())
    db.add(org)
    vehicle = Vehicle(
        id="veh-exp-058",
        organization_id="org-exp-uc058",
        vin="1HGCR2F83HA000058",
        license_plate="EXP-058",
        make="Hyundai",
        model="Elantra",
        year=2023,
        current_odometer_km=5000.0,
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
        "org_id": "org-exp-uc058",
        "vehicle_id": "veh-exp-058"
    }

def test_log_expense_success(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    payload = {
        "vehicle_id": veh_id,
        "category": "TOLL",
        "amount": 450.0,
        "currency": "PKR",
        "notes": "Motorway M2 Toll Plaza",
        "receipt_photo_url": "https://storage.googleapis.com/veltrics/receipts/toll-058.jpg"
    }

    r = client.post(f"/api/v1/expenses?organization_id={org_id}", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["amount"] == 450.0
    assert data["category"] == "TOLL"
    assert data["receipt_photo_url"] == "https://storage.googleapis.com/veltrics/receipts/toll-058.jpg"

def test_reject_invalid_expense_amount(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    payload = {
        "vehicle_id": veh_id,
        "category": "PARKING",
        "amount": 0.0, # invalid 0 amount
        "notes": "Invalid amount test"
    }

    r = client.post(f"/api/v1/expenses?organization_id={org_id}", json=payload)
    assert r.status_code == 422

def test_get_expenses_list(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    client.post(
        f"/api/v1/expenses?organization_id={org_id}",
        json={"vehicle_id": veh_id, "category": "PARKING", "amount": 200.0}
    )
    client.post(
        f"/api/v1/expenses?organization_id={org_id}",
        json={"vehicle_id": veh_id, "category": "WASH", "amount": 800.0}
    )

    r_list = client.get(f"/api/v1/expenses?vehicle_id={veh_id}&organization_id={org_id}")
    assert r_list.status_code == 200
    expenses = r_list.json()
    assert len(expenses) == 2
