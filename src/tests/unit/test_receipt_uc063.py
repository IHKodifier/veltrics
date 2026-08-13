import sys
import os
import io
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

    org = Organization(id="org-rec-uc063", name="Veltrics Receipt Test Org", created_at=datetime.utcnow())
    db.add(org)

    vehicle = Vehicle(
        id="veh-rec-063",
        organization_id="org-rec-uc063",
        vin="1HGCR2F83HA000063",
        license_plate="REC-063",
        make="Hyundai",
        model="Elantra",
        year=2023,
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
        "org_id": "org-rec-uc063",
        "vehicle_id": "veh-rec-063"
    }

def test_upload_receipt_success(client):
    file_bytes = b"fake-image-bytes-data-for-receipt"
    files = {"file": ("test_receipt.png", io.BytesIO(file_bytes), "image/png")}

    r = client.post("/api/v1/uploads/receipt", files=files)
    assert r.status_code == 201
    data = r.json()
    assert "file_url" in data
    assert data["file_url"].startswith("/uploads/receipts/")

def test_attach_receipt_to_expense(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    payload = {
        "vehicle_id": veh_id,
        "category": "MAINTENANCE",
        "amount": 3500.0,
        "expense_date": datetime.utcnow().isoformat(),
        "receipt_photo_url": "/uploads/receipts/rec_test_expense.jpg"
    }

    r = client.post(f"/api/v1/expenses?organization_id={org_id}", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["receipt_photo_url"] == "/uploads/receipts/rec_test_expense.jpg"

def test_attach_receipt_to_fuel_log(client, test_setup):
    org_id = test_setup["org_id"]
    veh_id = test_setup["vehicle_id"]

    payload = {
        "vehicle_id": veh_id,
        "log_date": datetime.utcnow().isoformat(),
        "odometer_km": 12500.0,
        "quantity_liters": 45.0,
        "price_per_liter": 270.0,
        "total_cost": 12150.0,
        "receipt_photo_url": "/uploads/receipts/rec_test_fuel.jpg"
    }

    r = client.post(f"/api/v1/fuel?organization_id={org_id}", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["receipt_photo_url"] == "/uploads/receipts/rec_test_fuel.jpg"
