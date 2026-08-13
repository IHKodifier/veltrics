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
    org = Organization(id="org-exp-uc059", name="Veltrics Expense History Test Org", created_at=datetime.utcnow())
    db.add(org)
    vehicle = Vehicle(
        id="veh-exp-059",
        organization_id="org-exp-uc059",
        vin="1HGCR2F83HA000059",
        license_plate="EXP-059",
        make="Honda",
        model="Civic",
        year=2022,
        current_odometer_km=12000.0,
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
        "org_id": "org-exp-uc059",
        "vehicle_id": "veh-exp-059"
    }

def test_get_expense_history_filtered(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    client.post(
        f"/api/v1/expenses?organization_id={org_id}",
        json={"vehicle_id": veh_id, "category": "TOLL", "amount": 450.0}
    )
    client.post(
        f"/api/v1/expenses?organization_id={org_id}",
        json={"vehicle_id": veh_id, "category": "PARKING", "amount": 200.0}
    )

    r_toll = client.get(f"/api/v1/expenses?vehicle_id={veh_id}&category=TOLL&organization_id={org_id}")
    assert r_toll.status_code == 200
    toll_items = r_toll.json()
    assert len(toll_items) == 1
    assert toll_items[0]["category"] == "TOLL"
    assert toll_items[0]["amount"] == 450.0

def test_get_expense_summary_metrics(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    client.post(
        f"/api/v1/expenses?organization_id={org_id}",
        json={"vehicle_id": veh_id, "category": "TOLL", "amount": 450.0}
    )
    client.post(
        f"/api/v1/expenses?organization_id={org_id}",
        json={"vehicle_id": veh_id, "category": "PARKING", "amount": 200.0}
    )
    client.post(
        f"/api/v1/expenses?organization_id={org_id}",
        json={"vehicle_id": veh_id, "category": "INSURANCE", "amount": 15000.0}
    )

    r_sum = client.get(f"/api/v1/expenses/summary?vehicle_id={veh_id}&organization_id={org_id}")
    assert r_sum.status_code == 200
    summary = r_sum.json()

    assert summary["total_expense_amount"] == 15650.0
    assert summary["total_expenses_count"] == 3
    assert summary["category_breakdown"]["TOLL"] == 450.0
    assert summary["category_breakdown"]["PARKING"] == 200.0
    assert summary["category_breakdown"]["INSURANCE"] == 15000.0
