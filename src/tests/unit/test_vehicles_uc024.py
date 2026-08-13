import sys
import os
import pytest
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
from app.models.user import User
from app.models.organization import Organization
from app.models.vehicle import Vehicle, VehicleType
from app.db.seed import seed_database

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
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
def sample_org():
    db = TestingSessionLocal()
    org = Organization(name="Test Fleet Org", is_personal=True, max_vehicles=2)
    db.add(org)
    db.commit()
    db.refresh(org)
    db.close()
    return org

def test_typeahead_vehicle_types_search(client):
    """
    Test 1: Verify GET /api/v1/vehicles/types?q=Toyota returns seeded Toyota models.
    """
    response = client.get("/api/v1/vehicles/types?q=Toyota")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    makes = [item["make"] for item in data]
    assert all(make == "Toyota" for make in makes)

def test_create_vehicle_success(client, sample_org):
    """
    Test 2: Verify POST /api/v1/vehicles registers new vehicle with tenant organization_id.
    """
    payload = {
        "organization_id": sample_org.id,
        "license_plate": "LEA-2024",
        "registration_province": "Punjab",
        "make": "Toyota",
        "model": "Corolla",
        "year": 2024,
        "fuel_type": "Petrol",
        "initial_odometer_km": 5000.0,
        "current_odometer_km": 5000.0,
        "vin": "1HGCR2F83HA000001",
        "photo_url": "https://example.com/corolla2024.jpg"
    }

    response = client.post("/api/v1/vehicles", json=payload)
    assert response.status_code == 201, response.text
    data = response.json()

    assert data["license_plate"] == "LEA-2024"
    assert data["registration_province"] == "Punjab"
    assert data["organization_id"] == sample_org.id
    assert data["make"] == "Toyota"
    assert data["status"] == "ACTIVE"
    assert data["photo_url"] == "https://example.com/corolla2024.jpg"

    # Verify vehicle directory listing
    list_resp = client.get(f"/api/v1/vehicles?organization_id={sample_org.id}")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

def test_duplicate_vin_conflict(client, sample_org):
    """
    Test 3: Verify duplicate VIN within same organization returns HTTP 409 Conflict.
    """
    payload = {
        "organization_id": sample_org.id,
        "license_plate": "LEA-1111",
        "make": "Honda",
        "model": "Civic",
        "year": 2023,
        "vin": "DUPLICATE-VIN-999"
    }

    # First vehicle registration
    res1 = client.post("/api/v1/vehicles", json=payload)
    assert res1.status_code == 201

    # Second registration with duplicate VIN
    payload["license_plate"] = "LEA-2222"
    res2 = client.post("/api/v1/vehicles", json=payload)
    assert res2.status_code == 409
    assert "VIN already exists" in res2.json()["detail"]

def test_organization_quota_exceeded(client, sample_org):
    """
    Test 4: Verify exceeding max_vehicles quota (max=2 for sample_org) returns HTTP 400 Bad Request.
    """
    v1 = {
        "organization_id": sample_org.id,
        "license_plate": "CAR-1",
        "make": "Toyota",
        "model": "Yaris",
        "year": 2022
    }
    v2 = {
        "organization_id": sample_org.id,
        "license_plate": "CAR-2",
        "make": "Honda",
        "model": "City",
        "year": 2023
    }
    v3 = {
        "organization_id": sample_org.id,
        "license_plate": "CAR-3",
        "make": "Suzuki",
        "model": "Swift",
        "year": 2024
    }

    assert client.post("/api/v1/vehicles", json=v1).status_code == 201
    assert client.post("/api/v1/vehicles", json=v2).status_code == 201

    # Third vehicle exceeds max_vehicles=2
    res3 = client.post("/api/v1/vehicles", json=v3)
    assert res3.status_code == 400
    assert "quota limit reached" in res3.json()["detail"]

def test_custom_vehicle_auto_indexing(client, sample_org):
    """
    Test 5: Verify custom make/model is dynamically indexed into VehicleType catalogue for future lookups.
    """
    custom_payload = {
        "organization_id": sample_org.id,
        "license_plate": "EV-007",
        "make": "Rivian",
        "model": "R1T",
        "year": 2025,
        "fuel_type": "EV"
    }

    # Register custom vehicle
    res = client.post("/api/v1/vehicles", json=custom_payload)
    assert res.status_code == 201

    # Verify typeahead search now returns Rivian R1T
    lookup_resp = client.get("/api/v1/vehicles/types?q=Rivian")
    assert lookup_resp.status_code == 200
    results = lookup_resp.json()
    assert len(results) == 1
    assert results[0]["make"] == "Rivian"
    assert results[0]["model"] == "R1T"
    assert results[0]["category"] == "Custom"
