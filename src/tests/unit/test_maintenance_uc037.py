import sys
import os
import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app
from app.db.session import Base, get_db
from app.models.organization import Organization
from app.models.vehicle import Vehicle
from app.models.maintenance import MaintenanceSchedule, ServiceRecord
from app.db.seed import seed_database

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    org1 = Organization(name="Primary Org", is_personal=False)
    org2 = Organization(name="Secondary Org", is_personal=False)
    db.add_all([org1, org2])
    db.commit()
    db.refresh(org1)
    db.refresh(org2)

    veh1 = Vehicle(
        organization_id=org1.id,
        license_plate="HIST-037",
        registration_province="Punjab",
        make="Honda",
        model="Civic",
        year=2022,
        fuel_type="Petrol",
        initial_odometer_km=10000.0,
        current_odometer_km=25000.0,
        status="ACTIVE"
    )
    veh2 = Vehicle(
        organization_id=org2.id,
        license_plate="OTHER-999",
        registration_province="Sindh",
        make="Toyota",
        model="Corolla",
        year=2021,
        fuel_type="Petrol",
        initial_odometer_km=5000.0,
        current_odometer_km=15000.0,
        status="ACTIVE"
    )
    db.add_all([veh1, veh2])
    db.commit()
    db.refresh(veh1)
    db.refresh(veh2)

    # Add 3 service records for veh1
    rec1 = ServiceRecord(
        organization_id=org1.id,
        vehicle_id=veh1.id,
        service_date=date(2026, 5, 10),
        odometer_km=12000.0,
        total_cost=4500.0,
        service_center_name="Honda Pitstop",
        notes="First free checkup & oil change",
        invoice_photo_url="https://storage.veltrics.com/inv1.jpg"
    )
    rec2 = ServiceRecord(
        organization_id=org1.id,
        vehicle_id=veh1.id,
        service_date=date(2026, 7, 20),
        odometer_km=18000.0,
        total_cost=8500.0,
        service_center_name="Honda Avenue",
        notes="Brake pads replacement & wheel alignment"
    )
    rec3 = ServiceRecord(
        organization_id=org1.id,
        vehicle_id=veh1.id,
        service_date=date(2026, 8, 5),
        odometer_km=25000.0,
        total_cost=12000.0,
        service_center_name="Honda Authorized Service",
        notes="Full synthetic oil change & air filter"
    )
    # Add 1 service record for veh2 (org2)
    rec_org2 = ServiceRecord(
        organization_id=org2.id,
        vehicle_id=veh2.id,
        service_date=date(2026, 8, 1),
        odometer_km=15000.0,
        total_cost=6000.0,
        service_center_name="Toyota Care"
    )

    db.add_all([rec1, rec2, rec3, rec_org2])
    db.commit()
    db.refresh(rec1)
    db.refresh(rec2)
    db.refresh(rec3)
    db.refresh(rec_org2)
    db.close()

    return {
        "org1_id": org1.id,
        "org2_id": org2.id,
        "veh1_id": veh1.id,
        "veh2_id": veh2.id,
        "rec1_id": rec1.id,
        "rec2_id": rec2.id,
        "rec3_id": rec3.id,
    }

def test_get_service_history_success(client, test_setup):
    """UC-037: GET /api/v1/maintenance/records retrieves service records sorted by service_date descending."""
    response = client.get(
        f"/api/v1/maintenance/records?vehicle_id={test_setup['veh1_id']}",
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

    # Assert descending order by service_date
    assert data[0]["id"] == test_setup["rec3_id"]
    assert data[0]["service_date"] == "2026-08-05"
    assert data[0]["total_cost"] == 12000.0
    assert data[0]["odometer_km"] == 25000.0
    assert data[0]["service_center_name"] == "Honda Authorized Service"

    assert data[1]["id"] == test_setup["rec2_id"]
    assert data[1]["service_date"] == "2026-07-20"

    assert data[2]["id"] == test_setup["rec1_id"]
    assert data[2]["service_date"] == "2026-05-10"
    assert data[2]["invoice_photo_url"] == "https://storage.veltrics.com/inv1.jpg"

def test_get_service_history_pagination(client, test_setup):
    """UC-037: Pagination limit and offset parameters operate correctly."""
    # Fetch top 2
    res_page1 = client.get(
        f"/api/v1/maintenance/records?vehicle_id={test_setup['veh1_id']}&limit=2&offset=0",
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert res_page1.status_code == 200
    data1 = res_page1.json()
    assert len(data1) == 2
    assert data1[0]["id"] == test_setup["rec3_id"]
    assert data1[1]["id"] == test_setup["rec2_id"]

    # Fetch remaining 1 with offset 2
    res_page2 = client.get(
        f"/api/v1/maintenance/records?vehicle_id={test_setup['veh1_id']}&limit=2&offset=2",
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert res_page2.status_code == 200
    data2 = res_page2.json()
    assert len(data2) == 1
    assert data2[0]["id"] == test_setup["rec1_id"]

def test_get_service_history_invalid_vehicle(client, test_setup):
    """UC-037: Returns 404 when vehicle_id does not exist in active organization."""
    response = client.get(
        "/api/v1/maintenance/records?vehicle_id=invalid-uuid-1234",
        headers={"X-Organization-ID": test_setup["org1_id"]}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found in active organization"

def test_tenant_isolation_uc037(client, test_setup):
    """UC-037: Header requirements and cross-tenant boundaries are strictly enforced."""
    # Missing header -> 400
    res_no_hdr = client.get(
        f"/api/v1/maintenance/records?vehicle_id={test_setup['veh1_id']}"
    )
    assert res_no_hdr.status_code == 400

    # Wrong org header for veh1 -> 404
    res_wrong_org = client.get(
        f"/api/v1/maintenance/records?vehicle_id={test_setup['veh1_id']}",
        headers={"X-Organization-ID": test_setup["org2_id"]}
    )
    assert res_wrong_org.status_code == 404

    # Querying veh2 under org2 returns only org2 records
    res_org2 = client.get(
        f"/api/v1/maintenance/records?vehicle_id={test_setup['veh2_id']}",
        headers={"X-Organization-ID": test_setup["org2_id"]}
    )
    assert res_org2.status_code == 200
    data_org2 = res_org2.json()
    assert len(data_org2) == 1
    assert data_org2[0]["total_cost"] == 6000.0
