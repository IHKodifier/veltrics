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
from app.models.driver import Driver
from app.models.maintenance import MaintenanceSchedule, ServiceRecord
from app.db.seed import seed_database, DEFAULT_VEHICLE_CATALOGUE

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
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_uc118_schema_instantiation():
    """
    Test 1: Verify all 7 core data models instantiate clean database tables.
    """
    db = TestingSessionLocal()
    # Create test organization
    org = Organization(name="Test Fleet Org", is_personal=False)
    db.add(org)
    db.flush()

    # Create test driver
    driver = Driver(organization_id=org.id, full_name="Tariq Driver", phone_number="+923001234567")
    db.add(driver)
    db.flush()

    # Create test vehicle
    vehicle = Vehicle(
        organization_id=org.id,
        assigned_driver_id=driver.id,
        license_plate="LES-1234",
        make="Toyota",
        model="Corolla",
        year=2023,
        fuel_type="Petrol",
        initial_odometer_km=15000.0,
        current_odometer_km=18500.0,
        photo_url="https://example.com/corolla.jpg"
    )
    db.add(vehicle)
    db.flush()

    # Create maintenance schedule & service record
    schedule = MaintenanceSchedule(
        organization_id=org.id,
        vehicle_id=vehicle.id,
        task_name="Engine Oil & Filter Change",
        interval_km=5000,
        interval_days=180
    )
    db.add(schedule)
    db.flush()

    record = ServiceRecord(
        organization_id=org.id,
        vehicle_id=vehicle.id,
        maintenance_schedule_id=schedule.id,
        service_date=vehicle.created_at.date(),
        odometer_km=18500.0,
        total_cost=8500.0,
        service_center_name="Toyota Motors Lahore"
    )
    db.add(record)
    db.commit()

    # Assert persistence
    assert db.query(Vehicle).filter_by(license_plate="LES-1234").first() is not None
    assert db.query(MaintenanceSchedule).filter_by(vehicle_id=vehicle.id).count() == 1
    assert db.query(ServiceRecord).filter_by(vehicle_id=vehicle.id).first().total_cost == 8500.0
    db.close()

def test_uc118_idempotent_database_seeding(client):
    """
    Test 2: Verify database seeding populates master vehicle catalogue idempotently.
    """
    db = TestingSessionLocal()
    
    # First seed run
    res1 = seed_database(db)
    assert res1["status"] == "success"
    assert res1["vehicle_types_added"] == len(DEFAULT_VEHICLE_CATALOGUE)

    # Second seed run (Idempotency check)
    res2 = seed_database(db)
    assert res2["status"] == "success"
    assert res2["vehicle_types_added"] == 0
    assert res2["vehicle_types_updated"] == len(DEFAULT_VEHICLE_CATALOGUE)

    # Verify Toyota Corolla entry
    corolla = db.query(VehicleType).filter_by(make="Toyota", model="Corolla").first()
    assert corolla is not None
    assert corolla.category == "Sedan"
    assert corolla.recommended_oil_interval_km == 5000
    db.close()

def test_uc118_seed_api_endpoint(client):
    """
    Test 3: Verify POST /api/v1/admin/seed endpoint.
    """
    response = client.post("/api/v1/admin/seed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "vehicle_types_added" in data
