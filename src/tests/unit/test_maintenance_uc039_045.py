import os
import sys
import pytest
from datetime import datetime, timezone, timedelta, date

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

try:
    import jwt
except ImportError:
    from jose import jwt

from app.core.config import settings
from app.main import app
from app.db.session import Base, get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.user_organization import UserOrganization
from app.models.vehicle import Vehicle
from app.models.maintenance import MaintenanceSchedule, ServiceRecord

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


client = TestClient(app)


def create_access_token(data: dict) -> str:
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


@pytest.fixture
def setup_database():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Create Org
    org = Organization(
        id="org-mnt-201",
        name="Maintenance Test Fleet",
        owner_id="user-mnt-201",
        tier="pro",
    )
    db.add(org)

    # Create User
    user = User(
        id="user-mnt-201",
        firebase_uid="uid-mnt-201",
        email="mnt@testfleet.com",
        full_name="Mnt Manager",
        password_hash="hashed_pass_123",
    )
    db.add(user)

    # Create UserOrganization Link
    user_org = UserOrganization(
        user_id="user-mnt-201",
        organization_id="org-mnt-201",
        role="OWNER",
    )
    db.add(user_org)

    # Create Vehicle
    vehicle = Vehicle(
        id="veh-mnt-01",
        organization_id="org-mnt-201",
        vin="1FTFW1E84MFC22222",
        make="Ford",
        model="F-250",
        year=2023,
        license_plate="MNT-5500",
    )
    db.add(vehicle)

    # Create Baseline Maintenance Schedule Item
    schedule = MaintenanceSchedule(
        id="sched-mnt-01",
        organization_id="org-mnt-201",
        vehicle_id="veh-mnt-01",
        task_name="Transmission Fluid Service",
        interval_km=25000,
        interval_days=365,
        last_performed_km=10000.0,
        next_due_km=35000.0,
        is_active=True,
    )
    db.add(schedule)

    # Create Existing Service Record
    record = ServiceRecord(
        id="rec-mnt-01",
        organization_id="org-mnt-201",
        vehicle_id="veh-mnt-01",
        maintenance_schedule_id="sched-mnt-01",
        service_date=date.today(),
        odometer_km=10000.0,
        total_cost=150.0,
        service_center_name="Speedy Lube Central",
        notes="Standard fluid exchange",
    )
    db.add(record)

    db.commit()

    token_payload = {
        "sub": "user-mnt-201",
        "email": "mnt@testfleet.com",
        "org_id": "org-mnt-201",
        "role": "OWNER",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    token = create_access_token(token_payload)

    yield {
        "token": token,
        "org_id": "org-mnt-201",
        "vehicle_id": "veh-mnt-01",
        "schedule_id": "sched-mnt-01",
        "record_id": "rec-mnt-01",
    }

    db.close()
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_uc039_add_custom_maintenance_schedule_item(setup_database):
    """UC-039: Verify adding custom maintenance service item."""
    token = setup_database["token"]
    vehicle_id = setup_database["vehicle_id"]

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "vehicle_id": vehicle_id,
        "task_name": "Refrigeration Unit Annual Inspection",
        "interval_km": 15000,
        "interval_days": 180,
    }

    response = client.post("/api/v1/maintenance/schedules/custom", json=payload, headers=headers)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["task_name"] == "Refrigeration Unit Annual Inspection"
    assert data["vehicle_id"] == vehicle_id


def test_uc040_edit_existing_service_record(setup_database):
    """UC-040: Verify updating an existing service record."""
    token = setup_database["token"]
    record_id = setup_database["record_id"]

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "total_cost": 220.50,
        "service_center_name": "Apex Auto Master",
        "notes": "Updated synthetic fluid service with filter change",
    }

    response = client.put(f"/api/v1/maintenance/records/{record_id}", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["total_cost"] == 220.50
    assert data["service_center_name"] == "Apex Auto Master"


def test_uc041_delete_service_record_soft_delete(setup_database):
    """UC-041: Verify soft deleting a service record."""
    token = setup_database["token"]
    record_id = setup_database["record_id"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/api/v1/maintenance/records/{record_id}", headers=headers)
    assert response.status_code == 200, response.text
    assert response.json()["status"] == "success"


def test_uc042_filter_and_search_service_history(setup_database):
    """UC-042: Verify searching & filtering service history."""
    token = setup_database["token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/maintenance/records?search_query=Speedy", headers=headers)
    assert response.status_code == 200, response.text
    records = response.json()
    assert len(records) >= 1
    assert "Speedy" in records[0]["service_center_name"]


def test_uc043_vendor_management(setup_database):
    """UC-043: Verify maintenance vendor creation and directory endpoint."""
    token = setup_database["token"]

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "Metro Truck & Diesel Works",
        "contact_person": "Dave Smith",
        "phone_number": "+1-555-9000",
        "address": "400 Industrial Pkwy, Austin TX",
        "rating": 4.8,
    }

    create_resp = client.post("/api/v1/vendors", json=payload, headers=headers)
    assert create_resp.status_code == 201, create_resp.text

    list_resp = client.get("/api/v1/vendors", headers=headers)
    assert list_resp.status_code == 200, list_resp.text
    vendors = list_resp.json()
    assert len(vendors) >= 1
    assert vendors[0]["name"] == "Metro Truck & Diesel Works"


def test_uc044_vehicle_inspection_checklist(setup_database):
    """UC-044: Verify vehicle pre-trip/post-trip safety inspection checklist."""
    token = setup_database["token"]
    vehicle_id = setup_database["vehicle_id"]

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "vehicle_id": vehicle_id,
        "inspection_type": "PRE_TRIP",
        "overall_status": "PASSED",
        "items_json": {"tires": "PASS", "brakes": "PASS", "lights": "PASS", "fluids": "PASS"},
        "notes": "Pre-trip inspection passed without defects.",
    }

    response = client.post("/api/v1/inspections", json=payload, headers=headers)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["overall_status"] == "PASSED"
    assert data["vehicle_id"] == vehicle_id


def test_uc045_snooze_maintenance_alert(setup_database):
    """UC-045: Verify snoozing maintenance alert by days and kilometers."""
    token = setup_database["token"]
    schedule_id = setup_database["schedule_id"]

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "snooze_days": 14,
        "snooze_km": 1000.0,
    }

    response = client.post(f"/api/v1/maintenance/schedules/{schedule_id}/snooze", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "snoozed"
    assert "snoozed_until_date" in data
