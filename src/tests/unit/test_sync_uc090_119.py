import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.driver import Driver
from app.models.vehicle import Vehicle
from app.models.fuel_log import FuelLog
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
        id="user-owner-201",
        firebase_uid="firebase-owner-201",
        email="sync_owner@test.com",
        full_name="Sync Owner",
        auth_provider="password"
    )
    db.add(user)

    org = Organization(
        id="org-201",
        name="Sync Fleet Org",
        owner_id=user.id,
        is_personal=False,
        max_vehicles=10
    )
    db.add(org)
    db.commit()

    res_dict = {
        "user_id": str(user.id),
        "org_id": str(org.id),
    }
    db.close()
    return res_dict

# ==========================================
# UC-119 & UC-091: Batch Sync Engine & Client UUID Allocation
# ==========================================

def test_uc119_sync_batch_topological_success(client, test_data):
    # Pass operations out of topological order: fuel_log first, then vehicle, then driver
    # The batch engine sorts them into vehicle -> driver -> fuel_log before executing!
    payload = {
        "organization_id": test_data['org_id'],
        "operations": [
            {
                "op_id": "op-fuel-001",
                "entity_type": "fuel_logs",
                "action": "CREATE",
                "payload": {
                    "id": "fuel-batch-001",
                    "vehicle_id": "veh-batch-001",
                    "driver_id": "driver-batch-001",
                    "odometer_km": 12500.0,
                    "quantity_liters": 45.0,
                    "total_cost": 90.0,
                    "fuel_type": "Petrol"
                }
            },
            {
                "op_id": "op-veh-001",
                "entity_type": "vehicles",
                "action": "CREATE",
                "payload": {
                    "id": "veh-batch-001",
                    "license_plate": "BATCH-001",
                    "make": "Toyota",
                    "model": "Hilux",
                    "year": 2023,
                    "fuel_type": "Diesel",
                    "initial_odometer_km": 10000.0,
                    "current_odometer_km": 12500.0
                }
            },
            {
                "op_id": "op-driver-001",
                "entity_type": "drivers",
                "action": "CREATE",
                "payload": {
                    "id": "driver-batch-001",
                    "user_id": test_data['user_id'],
                    "full_name": "Batch Driver",
                    "phone_number": "+1234567890",
                    "license_number": "LIC-BATCH"
                }
            }
        ]
    }

    res = client.post("/api/v1/sync/batch", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["processed_count"] == 3
    assert all(r["status"] == "SUCCESS" for r in data["results"])

    db = TestingSessionLocal()
    v = db.query(Vehicle).filter_by(id="veh-batch-001").first()
    assert v is not None
    assert v.license_plate == "BATCH-001"

    d = db.query(Driver).filter_by(id="driver-batch-001").first()
    assert d is not None

    f = db.query(FuelLog).filter_by(id="fuel-batch-001").first()
    assert f is not None
    assert f.quantity_liters == 45.0
    db.close()

def test_uc119_sync_batch_rollback_on_constraint_failure(client, test_data):
    # Operation 2 has an invalid payload (passing string to float column odometer_km)
    payload = {
        "organization_id": test_data['org_id'],
        "operations": [
            {
                "op_id": "op-veh-good",
                "entity_type": "vehicles",
                "action": "CREATE",
                "payload": {
                    "id": "veh-should-rollback",
                    "license_plate": "ROLLBACK-01",
                    "make": "Honda",
                    "model": "Civic",
                    "year": 2022
                }
            },
            {
                "op_id": "op-fuel-bad",
                "entity_type": "fuel_logs",
                "action": "CREATE",
                "payload": {
                    "id": "fuel-bad",
                    "vehicle_id": "veh-should-rollback",
                    "odometer_km": "INVALID_FLOAT_STRING"  # Triggers DB/SQLAlchemy type conversion error
                }
            }
        ]
    }

    res = client.post("/api/v1/sync/batch", json=payload)
    assert res.status_code == 400
    assert "failed" in res.json()["detail"].lower()

    # Verify vehicle was NOT created due to full transaction rollback
    db = TestingSessionLocal()
    v = db.query(Vehicle).filter_by(id="veh-should-rollback").first()
    assert v is None
    db.close()

# ==========================================
# UC-094: Sync Conflict Resolution (Server-Wins)
# ==========================================

def test_uc094_sync_conflict_server_wins(client, test_data):
    # 1. Create a vehicle directly in DB
    db = TestingSessionLocal()
    old_time = datetime.now(timezone.utc) - timedelta(hours=2)
    v = Vehicle(
        id="veh-conflict-01",
        organization_id=test_data['org_id'],
        license_plate="SERVER-PLATE",
        make="Toyota",
        model="Corolla",
        year=2021,
        updated_at=datetime.now(timezone.utc)  # Updated recently on server
    )
    db.add(v)
    db.commit()
    db.close()

    # 2. Client submits UPDATE with base_updated_at from 2 hours ago (older than server updated_at)
    payload = {
        "organization_id": test_data['org_id'],
        "operations": [
            {
                "op_id": "op-conflict-update",
                "entity_type": "vehicles",
                "action": "UPDATE",
                "payload": {
                    "id": "veh-conflict-01",
                    "license_plate": "CLIENT-STALE-PLATE"
                },
                "base_updated_at": old_time.isoformat()
            }
        ]
    }

    res = client.post("/api/v1/sync/batch", json=payload)
    assert res.status_code == 200
    data = res.json()
    result = data["results"][0]
    assert result["status"] == "CONFLICT"
    assert result["server_entity"]["license_plate"] == "SERVER-PLATE"

    # Verify server entity was NOT modified
    db = TestingSessionLocal()
    v_db = db.query(Vehicle).filter_by(id="veh-conflict-01").first()
    assert v_db.license_plate == "SERVER-PLATE"
    db.close()

# ==========================================
# UC-096: Delta Sync Payload Fetching
# ==========================================

def test_uc096_delta_sync_with_since_timestamp(client, test_data):
    db = TestingSessionLocal()
    now = datetime.now(timezone.utc)
    t_old = now - timedelta(hours=2)
    t_since = now - timedelta(hours=1)

    v_old = Vehicle(
        id="veh-old",
        organization_id=test_data['org_id'],
        license_plate="OLD-101",
        make="Ford",
        model="Ranger",
        year=2019
    )
    v_new = Vehicle(
        id="veh-new",
        organization_id=test_data['org_id'],
        license_plate="NEW-101",
        make="Ford",
        model="F-150",
        year=2024
    )
    db.add_all([v_old, v_new])
    db.commit()

    # Explicitly set v_old updated_at to t_old using raw SQL
    db.execute(text("UPDATE vehicles SET updated_at = :t WHERE id = 'veh-old'"), {"t": t_old.strftime("%Y-%m-%d %H:%M:%S")})
    db.execute(text("UPDATE vehicles SET updated_at = :t WHERE id = 'veh-new'"), {"t": now.strftime("%Y-%m-%d %H:%M:%S")})
    db.commit()
    db.close()

    since_param = t_since.isoformat()
    res = client.get(f"/api/v1/sync/delta?organization_id={test_data['org_id']}&since={since_param}")
    assert res.status_code == 200
    data = res.json()
    vehicles = data["vehicles"]
    assert len(vehicles) == 1
    assert vehicles[0]["id"] == "veh-new"

def test_uc096_delta_sync_full_snapshot(client, test_data):
    db = TestingSessionLocal()
    v = Vehicle(
        id="veh-snap-01",
        organization_id=test_data['org_id'],
        license_plate="SNAP-101",
        make="Hyundai",
        model="Elantra",
        year=2022
    )
    db.add(v)
    db.commit()
    db.close()

    res = client.get(f"/api/v1/sync/delta?organization_id={test_data['org_id']}")
    assert res.status_code == 200
    data = res.json()
    assert len(data["vehicles"]) >= 1

# ==========================================
# UC-097: Media Attachment Integration in Sync Batch
# ==========================================

def test_uc097_media_attachment_queue_integration(client, test_data):
    payload = {
        "organization_id": test_data['org_id'],
        "operations": [
            {
                "op_id": "op-fuel-receipt",
                "entity_type": "fuel_logs",
                "action": "CREATE",
                "payload": {
                    "id": "fuel-receipt-101",
                    "vehicle_id": "veh-101",
                    "odometer_km": 15000.0,
                    "quantity_liters": 30.0,
                    "total_cost": 60.0,
                    "receipt_photo_url": "https://storage.veltrics.com/receipts/offline-rcpt.jpg"
                }
            }
        ]
    }
    res = client.post("/api/v1/sync/batch", json=payload)
    assert res.status_code == 200
    assert res.json()["results"][0]["status"] == "SUCCESS"

    db = TestingSessionLocal()
    f = db.query(FuelLog).filter_by(id="fuel-receipt-101").first()
    assert f is not None
    assert f.receipt_photo_url == "https://storage.veltrics.com/receipts/offline-rcpt.jpg"
    db.close()
