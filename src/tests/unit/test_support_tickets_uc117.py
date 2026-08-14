import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add src/backend to python sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

import app.models as models
from app.models.user import User
from app.models.organization import Organization
from app.models.support_ticket import SupportTicket
from app.main import app
from app.db.session import Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_uc117_create_and_list_support_tickets(client):
    """
    AC for UC-117:
    GIVEN a user submitting feedback or a support ticket
    WHEN they POST /api/v1/support/tickets with category, description, and device_info
    THE SYSTEM SHALL store the support ticket and auto-attach user ID and metadata.
    """
    # 1. Register test user
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "support.user@veltrics.com",
        "password": "Password123",
        "full_name": "Support User",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    user_id = reg_resp.json()["user"]["id"]
    access_token = reg_resp.json()["access_token"]
    headers = {"X-User-ID": user_id, "Authorization": f"Bearer {access_token}"}

    # 2. Submit support ticket
    ticket_payload = {
        "category": "BUG",
        "description": "Fuel log receipt scanner failed to process blurred receipt image.",
        "device_info": {
            "os": "Android 14",
            "device_model": "Pixel 7 Pro",
            "app_version": "1.0.0+1"
        }
    }
    create_resp = client.post("/api/v1/support/tickets", json=ticket_payload, headers=headers)
    assert create_resp.status_code == 201
    ticket_data = create_resp.json()
    assert ticket_data["id"] is not None
    assert ticket_data["user_id"] == user_id
    assert ticket_data["category"] == "BUG"
    assert "Fuel log receipt" in ticket_data["description"]
    assert ticket_data["status"] == "OPEN"
    assert ticket_data["device_info"]["device_model"] == "Pixel 7 Pro"

    # 3. Get list of user support tickets
    list_resp = client.get("/api/v1/support/tickets", headers=headers)
    assert list_resp.status_code == 200
    tickets = list_resp.json()
    assert len(tickets) == 1
    assert tickets[0]["id"] == ticket_data["id"]

def test_uc117_support_ticket_empty_description_validation(client):
    """
    WHEN description is empty or missing
    THE SYSTEM SHALL return HTTP 422 Unprocessable Entity error.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "support.invalid@veltrics.com",
        "password": "Password123",
        "full_name": "Support Invalid User",
        "auth_provider": "email"
    })
    user_id = reg_resp.json()["user"]["id"]
    headers = {"X-User-ID": user_id}

    # Empty description payload
    bad_payload = {
        "category": "BUG",
        "description": "   ",
        "device_info": {}
    }
    res = client.post("/api/v1/support/tickets", json=bad_payload, headers=headers)
    assert res.status_code == 422
