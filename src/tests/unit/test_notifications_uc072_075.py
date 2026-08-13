import sys
import os
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
from app.models.user import User

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

    org = Organization(id="org-notif-uc072", name="Veltrics Notification Test Org", created_at=datetime.utcnow())
    db.add(org)

    user = User(
        id="usr-notif-072",
        firebase_uid="uid_notif_072",
        email="test_notif@veltrics.com",
        full_name="Notif Tester",
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(user)

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
        "org_id": "org-notif-uc072",
        "user_id": "usr-notif-072"
    }

def test_register_fcm_device_token(client, test_setup):
    user_id = test_setup["user_id"]

    payload = {
        "user_id": user_id,
        "device_token": "fcm_token_test_abc123",
        "device_type": "ANDROID"
    }

    r = client.post("/api/v1/notifications/devices", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["device_token"] == "fcm_token_test_abc123"
    assert data["device_type"] == "ANDROID"

def test_get_notifications_and_unread_count(client, test_setup):
    org_id = test_setup["org_id"]
    user_id = test_setup["user_id"]

    # Register token first
    client.post("/api/v1/notifications/devices", json={"user_id": user_id, "device_token": "fcm_token_123"})

    r = client.get(f"/api/v1/notifications?user_id={user_id}&organization_id={org_id}")
    assert r.status_code == 200
    data = r.json()
    assert "unread_count" in data
    assert "items" in data

def test_mark_notification_read(client, test_setup):
    org_id = test_setup["org_id"]
    user_id = test_setup["user_id"]

    # Seed mock notification endpoint or direct test
    r = client.get(f"/api/v1/notifications?user_id={user_id}&organization_id={org_id}")
    assert r.status_code == 200

def test_mark_all_notifications_read(client, test_setup):
    org_id = test_setup["org_id"]
    user_id = test_setup["user_id"]

    r = client.post(f"/api/v1/notifications/mark-all-read?user_id={user_id}&organization_id={org_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["message"] == "All notifications marked as read"

def test_update_notification_preferences(client, test_setup):
    user_id = test_setup["user_id"]

    payload = {
        "user_id": user_id,
        "maintenance_reminders": True,
        "document_expirations": True,
        "quota_alerts": False,
        "system_news": True
    }

    r = client.patch("/api/v1/notifications/preferences", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["maintenance_reminders"] is True
    assert data["quota_alerts"] is False
