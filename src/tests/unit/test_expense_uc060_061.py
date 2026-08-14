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
    org = Organization(id="org-exp-uc060", name="Veltrics Expense Edit Test Org", created_at=datetime.utcnow())
    db.add(org)
    vehicle = Vehicle(
        id="veh-exp-060",
        organization_id="org-exp-uc060",
        vin="1HGCR2F83HA000060",
        license_plate="EXP-060",
        make="Toyota",
        model="Corolla",
        year=2024,
        current_odometer_km=8000.0,
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
        "org_id": "org-exp-uc060",
        "vehicle_id": "veh-exp-060"
    }

def test_update_expense_success(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    create_res = client.post(
        f"/api/v1/expenses?organization_id={org_id}",
        json={"vehicle_id": veh_id, "category": "TOLL", "amount": 300.0, "notes": "Initial toll"}
    )
    assert create_res.status_code == 201
    expense_id = create_res.json()["id"]

    patch_res = client.patch(
        f"/api/v1/expenses/{expense_id}?organization_id={org_id}",
        json={"category": "PARKING", "amount": 450.0, "notes": "Updated parking note"}
    )
    assert patch_res.status_code == 200
    updated_data = patch_res.json()
    assert updated_data["category"] == "PARKING"
    assert updated_data["amount"] == 450.0
    assert updated_data["notes"] == "Updated parking note"

def test_soft_delete_expense_success(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    create_res = client.post(
        f"/api/v1/expenses?organization_id={org_id}",
        json={"vehicle_id": veh_id, "category": "WASH", "amount": 600.0}
    )
    assert create_res.status_code == 201
    expense_id = create_res.json()["id"]

    del_res = client.delete(f"/api/v1/expenses/{expense_id}?organization_id={org_id}")
    assert del_res.status_code == 200

    list_res = client.get(f"/api/v1/expenses?vehicle_id={veh_id}&organization_id={org_id}")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 0

    sum_res = client.get(f"/api/v1/expenses/summary?vehicle_id={veh_id}&organization_id={org_id}")
    assert sum_res.status_code == 200
    assert sum_res.json()["total_expense_amount"] == 0.0

def test_delete_nonexistent_expense_returns_404(client, test_setup):
    org_id = test_setup["org_id"]
    del_res = client.delete(f"/api/v1/expenses/nonexistent-exp-id?organization_id={org_id}")
    assert del_res.status_code == 404
