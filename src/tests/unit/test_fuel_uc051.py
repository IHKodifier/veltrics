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
    org = Organization(id="org-fuel-uc051", name="Edit Delete Fleet", is_personal=False)
    db.add(org)
    db.commit()

    vehicle = Vehicle(
        id="veh-fuel-051",
        organization_id=org.id,
        license_plate="UC051-EDIT",
        registration_province="Punjab",
        make="Toyota",
        model="Yaris",
        year=2023,
        fuel_type="Petrol",
        initial_odometer_km=50000.0,
        current_odometer_km=50000.0
    )
    db.add(vehicle)
    db.commit()
    db.close()

    return {"org_id": "org-fuel-uc051", "vehicle_id": "veh-fuel-051"}

def test_update_fuel_log_success(client, test_setup):
    """
    UC-051 Alternate Flow A1: PATCH /api/v1/fuel/{id} updates entry & recalculates efficiency chain.
    """
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    # Log 1
    r1 = client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "odometer": 50000.0,
            "fuel_amount_liters": 40.0,
            "cost_amount": 12000.0,
            "is_full_tank": True
        }
    )
    assert r1.status_code == 201

    # Log 2 (+500 km, 40 L -> 12.5 km/L)
    r2 = client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={
            "vehicle_id": veh_id,
            "odometer": 50500.0,
            "fuel_amount_liters": 40.0,
            "cost_amount": 12000.0,
            "is_full_tank": True
        }
    )
    assert r2.status_code == 201
    log2_id = r2.json()["id"]
    assert r2.json()["calculated_efficiency_kpl"] == 12.5

    # Update Log 2 quantity to 50 L and cost to 15000 -> recalculated efficiency should be 500 / 50 = 10.0 km/L
    r_patch = client.patch(
        f"/api/v1/fuel/{log2_id}?organization_id={org_id}",
        json={
            "quantity_liters": 50.0,
            "total_cost": 15000.0
        }
    )
    assert r_patch.status_code == 200
    patched_data = r_patch.json()
    assert patched_data["quantity_liters"] == 50.0
    assert patched_data["total_cost"] == 15000.0
    assert patched_data["calculated_efficiency_kpl"] == 10.0

    # Verify linked expense record updated
    db = TestingSessionLocal()
    linked_expense = db.query(ExpenseLog).filter(ExpenseLog.fuel_log_id == log2_id).first()
    assert linked_expense is not None
    assert linked_expense.amount == 15000.0
    db.close()

def test_soft_delete_fuel_log_recalculates_chain(client, test_setup):
    """
    UC-051 Main Flow: DELETE /api/v1/fuel/{id} soft-deletes log & linked expense and heals efficiency chain.
    Log 1: 50,000 km, 40 L
    Log 2: 50,500 km, 40 L -> 12.5 km/L (from Log 1)
    Log 3: 51,000 km, 50 L -> 10.0 km/L (from Log 2)
    Delete Log 2 -> Log 3 efficiency recalculates against Log 1: +1000 km / 50 L = 20.0 km/L
    """
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    r1 = client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={"vehicle_id": veh_id, "odometer": 50000.0, "fuel_amount_liters": 40.0, "cost_amount": 12000.0, "is_full_tank": True}
    )
    r2 = client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={"vehicle_id": veh_id, "odometer": 50500.0, "fuel_amount_liters": 40.0, "cost_amount": 12000.0, "is_full_tank": True}
    )
    r3 = client.post(
        f"/api/v1/fuel?organization_id={org_id}",
        json={"vehicle_id": veh_id, "odometer": 51000.0, "fuel_amount_liters": 50.0, "cost_amount": 15000.0, "is_full_tank": True}
    )

    log2_id = r2.json()["id"]
    log3_id = r3.json()["id"]
    assert r3.json()["calculated_efficiency_kpl"] == 10.0

    # Delete Log 2
    r_del = client.delete(f"/api/v1/fuel/{log2_id}?organization_id={org_id}")
    assert r_del.status_code == 200

    # Verify history list contains only Log 3 and Log 1
    r_hist = client.get(f"/api/v1/fuel?vehicle_id={veh_id}&organization_id={org_id}")
    assert r_hist.status_code == 200
    logs = r_hist.json()
    assert len(logs) == 2
    assert logs[0]["id"] == log3_id
    # Log 3 efficiency should be recalculated directly from Log 1 (+1000 km / 50 L = 20.0 km/L)
    assert logs[0]["distance_km"] == 1000.0
    assert logs[0]["calculated_efficiency_kpl"] == 20.0

    # Verify soft-delete flags in DB
    db = TestingSessionLocal()
    del_fuel = db.query(FuelLog).filter(FuelLog.id == log2_id).first()
    assert del_fuel.deleted_at is not None
    del_exp = db.query(ExpenseLog).filter(ExpenseLog.fuel_log_id == log2_id).first()
    assert del_exp.deleted_at is not None
    db.close()

def test_delete_nonexistent_fuel_log_returns_404(client, test_setup):
    """
    UC-051 Edge Case: Deleting or patching non-existent log returns HTTP 404.
    """
    org_id = test_setup["org_id"]
    r_del = client.delete(f"/api/v1/fuel/nonexistent-id?organization_id={org_id}")
    assert r_del.status_code == 404

    r_patch = client.patch(
        f"/api/v1/fuel/nonexistent-id?organization_id={org_id}",
        json={"quantity_liters": 50.0}
    )
    assert r_patch.status_code == 404
