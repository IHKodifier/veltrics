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
from app.models.organization import Organization
from app.models.vehicle import Vehicle
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
def sample_fleet(client):
    db = TestingSessionLocal()
    org = Organization(name="Test Directory Org", is_personal=False, max_vehicles=10)
    db.add(org)
    db.commit()
    db.refresh(org)

    v1 = Vehicle(
        organization_id=org.id,
        license_plate="LEA-100",
        registration_province="Punjab",
        make="Toyota",
        model="Corolla",
        year=2023,
        fuel_type="Petrol",
        status="ACTIVE"
    )
    v2 = Vehicle(
        organization_id=org.id,
        license_plate="SND-200",
        registration_province="Sindh",
        make="Honda",
        model="Civic",
        year=2024,
        fuel_type="Petrol",
        status="MAINTENANCE"
    )
    v3 = Vehicle(
        organization_id=org.id,
        license_plate="ICT-300",
        registration_province="ICT Islamabad",
        make="BYD",
        model="Atto 3",
        year=2025,
        fuel_type="EV",
        status="ACTIVE"
    )
    db.add_all([v1, v2, v3])
    db.commit()
    db.close()
    return org

def test_list_vehicles_status_filter(client, sample_fleet):
    """
    Test 1: Verify GET /api/v1/vehicles?status=MAINTENANCE returns only vehicles in MAINTENANCE state.
    """
    response = client.get(f"/api/v1/vehicles?organization_id={sample_fleet.id}&status=MAINTENANCE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["license_plate"] == "SND-200"
    assert data[0]["status"] == "MAINTENANCE"

def test_list_vehicles_search_query(client, sample_fleet):
    """
    Test 2: Verify search query matches license plate, make, or model.
    """
    # Search by plate
    res1 = client.get(f"/api/v1/vehicles?organization_id={sample_fleet.id}&search=ICT-300")
    assert res1.status_code == 200
    assert len(res1.json()) == 1
    assert res1.json()[0]["make"] == "BYD"

    # Search by make
    res2 = client.get(f"/api/v1/vehicles?organization_id={sample_fleet.id}&search=Honda")
    assert res2.status_code == 200
    assert len(res2.json()) == 1
    assert res2.json()[0]["model"] == "Civic"

def test_list_vehicles_province_filter(client, sample_fleet):
    """
    Test 3: Verify filtering by province (e.g. Sindh).
    """
    response = client.get(f"/api/v1/vehicles?organization_id={sample_fleet.id}&province=Sindh")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["registration_province"] == "Sindh"
