import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.driver import Driver
from app.models.vehicle import Vehicle
from app.models.vehicle_document import VehicleDocument
from app.models.maintenance import MaintenanceSchedule
from app.models.audit_log import AuditLog

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

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_data():
    db = TestingSessionLocal()

    user = User(
        id="user-owner-101",
        firebase_uid="firebase-owner-101",
        email="owner@test.com",
        full_name="Owner User",
        auth_provider="password"
    )
    db.add(user)

    org1 = Organization(
        id="org-101",
        name="Fleet Org 1",
        owner_id=user.id,
        is_personal=False,
        max_vehicles=2
    )
    org2 = Organization(
        id="org-102",
        name="Fleet Org 2",
        owner_id=user.id,
        is_personal=False,
        max_vehicles=5
    )
    db.add_all([org1, org2])
    db.flush()

    driver1 = Driver(
        id="driver-101",
        organization_id=org1.id,
        user_id=user.id,
        full_name="Driver One",
        phone_number="+1234567890",
        license_number="LIC-001"
    )
    driver_other_org = Driver(
        id="driver-102",
        organization_id=org2.id,
        user_id=user.id,
        full_name="Driver Other Org",
        phone_number="+0987654321",
        license_number="LIC-002"
    )
    db.add_all([driver1, driver_other_org])
    db.flush()

    vehicle1 = Vehicle(
        id="veh-101",
        organization_id=org1.id,
        assigned_driver_id=driver1.id,
        vin="VIN101",
        license_plate="ABC-101",
        registration_province="Punjab",
        make="Toyota",
        model="Corolla",
        year=2022,
        fuel_type="Petrol",
        initial_odometer_km=10000.0,
        current_odometer_km=15000.0,
        status="ACTIVE"
    )
    vehicle2 = Vehicle(
        id="veh-102",
        organization_id=org1.id,
        vin="VIN102",
        license_plate="XYZ-102",
        registration_province="Punjab",
        make="Honda",
        model="Civic",
        year=2023,
        fuel_type="Petrol",
        initial_odometer_km=5000.0,
        current_odometer_km=8000.0,
        status="ACTIVE"
    )
    db.add_all([vehicle1, vehicle2])
    db.flush()

    schedule1 = MaintenanceSchedule(
        id="sched-101",
        organization_id=org1.id,
        vehicle_id=vehicle1.id,
        task_name="Oil Change 20k",
        interval_km=5000,
        next_due_km=20000.0,
        is_active=True
    )
    db.add(schedule1)

    db.commit()

    res_dict = {
        "user_id": str(user.id),
        "org1_id": str(org1.id),
        "org2_id": str(org2.id),
        "driver1_id": str(driver1.id),
        "driver_other_org_id": str(driver_other_org.id),
        "vehicle1_id": str(vehicle1.id),
        "vehicle2_id": str(vehicle2.id),
    }
    db.close()
    return res_dict

# ==========================================
# UC-028: Soft Delete Vehicle
# ==========================================

def test_uc028_soft_delete_vehicle_success(client, test_data):
    res = client.delete(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}?organization_id={test_data['org1_id']}",
        headers={"X-User-ID": test_data['user_id']}
    )
    assert res.status_code == 200
    assert res.json()["message"] == "Vehicle soft-deleted successfully"

    db = TestingSessionLocal()
    v = db.query(Vehicle).filter_by(id=test_data['vehicle1_id']).first()
    assert v.deleted_at is not None

    audit = db.query(AuditLog).filter_by(action="DELETE_VEHICLE").first()
    assert audit is not None
    assert audit.payload["vehicle_id"] == test_data['vehicle1_id']
    db.close()

def test_uc028_soft_delete_vehicle_forbidden(client, test_data):
    res = client.delete(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}?organization_id={test_data['org2_id']}"
    )
    assert res.status_code == 403

# ==========================================
# UC-029: Log Manual Odometer Update
# ==========================================

def test_uc029_update_odometer_success(client, test_data):
    payload = {
        "current_odometer_km": 21000.0,
        "is_correction": False
    }
    res = client.post(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}/odometer?organization_id={test_data['org1_id']}",
        json=payload
    )
    assert res.status_code == 200
    data = res.json()
    assert data["current_odometer_km"] == 21000.0

    db = TestingSessionLocal()
    sched = db.query(MaintenanceSchedule).filter_by(id="sched-101").first()
    assert sched.is_active is True
    db.close()

def test_uc029_update_odometer_lower_reading_rejected(client, test_data):
    payload = {
        "current_odometer_km": 12000.0,
        "is_correction": False
    }
    res = client.post(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}/odometer?organization_id={test_data['org1_id']}",
        json=payload
    )
    assert res.status_code == 400
    assert "lower than existing reading" in res.json()["detail"]

def test_uc029_update_odometer_correction_success(client, test_data):
    payload = {
        "current_odometer_km": 12000.0,
        "is_correction": True
    }
    res = client.post(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}/odometer?organization_id={test_data['org1_id']}",
        json=payload,
        headers={"X-User-ID": test_data['user_id']}
    )
    assert res.status_code == 200
    assert res.json()["current_odometer_km"] == 12000.0

    db = TestingSessionLocal()
    audit = db.query(AuditLog).filter_by(action="ODOMETER_MANUAL_UPDATE").first()
    assert audit is not None
    assert audit.payload["is_correction"] is True
    db.close()

# ==========================================
# UC-030: Vehicle Document Management
# ==========================================

def test_uc030_upload_vehicle_document(client, test_data):
    payload = {
        "document_type": "REGISTRATION",
        "document_url": "https://storage.veltrics.com/docs/reg-101.pdf",
        "file_name": "reg-101.pdf",
        "expiration_date": "2027-12-31T23:59:59Z"
    }
    res = client.post(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}/documents?organization_id={test_data['org1_id']}",
        json=payload
    )
    assert res.status_code == 201
    data = res.json()
    assert data["document_type"] == "REGISTRATION"
    assert data["vehicle_id"] == test_data['vehicle1_id']
    assert data["organization_id"] == test_data['org1_id']

def test_uc030_get_vehicle_documents(client, test_data):
    # Upload doc first
    client.post(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}/documents?organization_id={test_data['org1_id']}",
        json={"document_type": "INSURANCE", "document_url": "https://storage.veltrics.com/docs/ins.pdf"}
    )
    res = client.get(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}/documents?organization_id={test_data['org1_id']}"
    )
    assert res.status_code == 200
    docs = res.json()
    assert len(docs) == 1
    assert docs[0]["document_type"] == "INSURANCE"

# ==========================================
# UC-031: Recover Deleted Vehicle
# ==========================================

def test_uc031_restore_deleted_vehicle_success(client, test_data):
    # Soft delete vehicle 1 first
    client.delete(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}?organization_id={test_data['org1_id']}"
    )

    # Restore vehicle 1
    res = client.post(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}/restore?organization_id={test_data['org1_id']}",
        headers={"X-User-ID": test_data['user_id']}
    )
    assert res.status_code == 200
    assert res.json()["id"] == test_data['vehicle1_id']

    db = TestingSessionLocal()
    v = db.query(Vehicle).filter_by(id=test_data['vehicle1_id']).first()
    assert v.deleted_at is None

    audit = db.query(AuditLog).filter_by(action="RECOVER_VEHICLE").first()
    assert audit is not None
    db.close()

def test_uc031_restore_vehicle_quota_exceeded(client, test_data):
    # org1 max_vehicles is 2. Both vehicle1 and vehicle2 are active.
    # Soft delete vehicle1
    client.delete(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}?organization_id={test_data['org1_id']}"
    )

    # Now add a new vehicle to fill org1 quota (active_count = 2)
    db = TestingSessionLocal()
    v3 = Vehicle(
        id="veh-103",
        organization_id=test_data['org1_id'],
        license_plate="NEW-103",
        make="Nissan",
        model="Sunny",
        year=2021,
        fuel_type="Petrol",
        initial_odometer_km=1000.0,
        current_odometer_km=1000.0,
        status="ACTIVE"
    )
    db.add(v3)
    db.commit()
    db.close()

    # Attempting to restore vehicle1 when active_count = 2 (max_vehicles = 2)
    res = client.post(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}/restore?organization_id={test_data['org1_id']}"
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "QUOTA_EXCEEDED"

# ==========================================
# UC-032 & UC-033: Assign & Unassign Driver
# ==========================================

def test_uc032_assign_primary_driver_success(client, test_data):
    payload = {"driver_id": test_data['driver1_id']}
    res = client.post(
        f"/api/v1/vehicles/{test_data['vehicle2_id']}/assign-driver?organization_id={test_data['org1_id']}",
        json=payload,
        headers={"X-User-ID": test_data['user_id']}
    )
    assert res.status_code == 200
    assert res.json()["assigned_driver_id"] == test_data['driver1_id']

    db = TestingSessionLocal()
    audit = db.query(AuditLog).filter_by(action="ASSIGN_PRIMARY_DRIVER").first()
    assert audit is not None
    assert audit.payload["driver_id"] == test_data['driver1_id']
    db.close()

def test_uc032_assign_driver_cross_tenant_forbidden(client, test_data):
    payload = {"driver_id": test_data['driver_other_org_id']}
    res = client.post(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}/assign-driver?organization_id={test_data['org1_id']}",
        json=payload
    )
    assert res.status_code == 403
    assert "belongs to another organization" in res.json()["detail"]

def test_uc033_unassign_driver_success(client, test_data):
    res = client.post(
        f"/api/v1/vehicles/{test_data['vehicle1_id']}/unassign-driver?organization_id={test_data['org1_id']}",
        headers={"X-User-ID": test_data['user_id']}
    )
    assert res.status_code == 200
    assert res.json()["assigned_driver_id"] is None

    db = TestingSessionLocal()
    v = db.query(Vehicle).filter_by(id=test_data['vehicle1_id']).first()
    assert v.assigned_driver_id is None

    audit = db.query(AuditLog).filter_by(action="UNASSIGN_PRIMARY_DRIVER").first()
    assert audit is not None
    db.close()
