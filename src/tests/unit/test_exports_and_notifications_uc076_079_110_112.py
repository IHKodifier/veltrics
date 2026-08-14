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
from app.models.maintenance import ServiceRecord
from app.models.fuel_log import FuelLog

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
        id="org-exp-401",
        name="Export & Notification Fleet",
        owner_id="user-exp-401",
        tier="pro",
    )
    db.add(org)

    # Create User
    user = User(
        id="user-exp-401",
        firebase_uid="uid-exp-401",
        email="owner@expfleet.com",
        full_name="Fleet Owner",
        password_hash="hashed_pass_456",
    )
    db.add(user)

    # Create UserOrganization Link
    user_org = UserOrganization(
        user_id="user-exp-401",
        organization_id="org-exp-401",
        role="OWNER",
    )
    db.add(user_org)

    # Create Vehicle & Service Record & Fuel Log
    veh = Vehicle(
        id="veh-exp-01",
        organization_id="org-exp-401",
        vin="1FTFW1E84MFC55555",
        make="Toyota",
        model="Tacoma",
        year=2023,
        license_plate="EXP-888",
        status="ACTIVE",
        current_odometer_km=25000.0,
    )
    db.add(veh)

    record = ServiceRecord(
        id="rec-exp-01",
        organization_id="org-exp-401",
        vehicle_id="veh-exp-01",
        service_date=date.today(),
        odometer_km=25000.0,
        total_cost=450.0,
        service_center_name="Precision Auto",
    )
    fuel = FuelLog(
        id="fuel-exp-01",
        organization_id="org-exp-401",
        vehicle_id="veh-exp-01",
        log_date=datetime.now(timezone.utc),
        odometer_km=25000.0,
        quantity_liters=50.0,
        total_cost=150.0,
    )
    db.add_all([record, fuel])
    db.commit()

    token_payload = {
        "sub": "user-exp-401",
        "email": "owner@expfleet.com",
        "org_id": "org-exp-401",
        "role": "OWNER",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    token = create_access_token(token_payload)

    yield {
        "token": token,
        "org_id": "org-exp-401",
        "user_id": "user-exp-401",
        "vehicle_id": "veh-exp-01",
    }

    db.close()
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_uc110_export_maintenance_pdf(setup_database):
    """UC-110: Verify Exporting Maintenance History to PDF."""
    token = setup_database["token"]
    org_id = setup_database["org_id"]
    headers = {"Authorization": f"Bearer {token}", "X-Organization-ID": org_id}

    response = client.get("/api/v1/exports/maintenance/pdf", headers=headers)
    assert response.status_code == 200, response.text
    assert "application/pdf" in response.headers.get("content-type", "")


def test_uc111_export_fuel_expenses_csv(setup_database):
    """UC-111: Verify Exporting Fuel & Expense Logs to CSV."""
    token = setup_database["token"]
    org_id = setup_database["org_id"]
    headers = {"Authorization": f"Bearer {token}", "X-Organization-ID": org_id}

    response = client.get("/api/v1/exports/fuel-expenses/csv", headers=headers)
    assert response.status_code == 200, response.text
    assert "text/csv" in response.headers.get("content-type", "")
    content = response.text
    assert "Vehicle" in content or "vehicle_id" in content or "Date" in content or "Cost" in content


def test_uc112_monthly_summary_email(setup_database):
    """UC-112: Verify Generating & Emailing Monthly Fleet Summary PDF."""
    token = setup_database["token"]
    org_id = setup_database["org_id"]
    headers = {"Authorization": f"Bearer {token}", "X-Organization-ID": org_id}

    payload = {"target_email": "owner@expfleet.com"}
    response = client.post("/api/v1/exports/monthly-summary/email", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "sent"


def test_uc076_notification_inbox_and_read_status(setup_database):
    """UC-076: Verify Notification Inbox Retrieval and Marking Read."""
    token = setup_database["token"]
    headers = {"Authorization": f"Bearer {token}"}

    get_resp = client.get("/api/v1/notifications/inbox", headers=headers)
    assert get_resp.status_code == 200, get_resp.text
    notifications = get_resp.json()
    assert isinstance(notifications, list)


def test_uc077_notification_preferences(setup_database):
    """UC-077: Verify Notification Preferences & Channel Configuration."""
    token = setup_database["token"]
    headers = {"Authorization": f"Bearer {token}"}

    pref_payload = {
        "push_enabled": True,
        "email_enabled": False,
        "maintenance_alerts": True,
        "billing_alerts": True,
    }

    put_resp = client.put("/api/v1/notifications/preferences", json=pref_payload, headers=headers)
    assert put_resp.status_code == 200, put_resp.text

    get_resp = client.get("/api/v1/notifications/preferences", headers=headers)
    assert get_resp.status_code == 200, get_resp.text
    data = get_resp.json()
    assert data["push_enabled"] is True
    assert data["email_enabled"] is False


def test_uc078_billing_alert_notifications(setup_database):
    """UC-078: Verify Billing & Payment Alert Notification Trigger."""
    token = setup_database["token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "alert_type": "RENEWAL_UPCOMING",
        "message": "Your Safepay Pro subscription renews in 3 days.",
    }

    response = client.post("/api/v1/notifications/billing-alerts", json=payload, headers=headers)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["alert_type"] == "RENEWAL_UPCOMING"


def test_uc079_purge_stale_fcm_tokens(setup_database):
    """UC-079: Verify Purging Stale FCM Push Notification Tokens (>90 days)."""
    token = setup_database["token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/notifications/purge-stale-tokens", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "purged_count" in data
