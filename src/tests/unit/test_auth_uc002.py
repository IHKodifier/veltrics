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

from app.main import app
from app.db.session import Base, get_db
import app.models as models
from app.models.user import User
from app.models.organization import Organization

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

def test_uc002_new_user_facebook_registration(client):
    """
    AC 1: WHEN a user registers via Facebook THE SYSTEM SHALL store "facebook" inside the
    linked_providers JSON array of the users record and auto-provision a personal organization.
    """
    payload = {
        "id_token": "mock-facebook-id-token-12345",
        "email": "facebook.user@veltrics.com",
        "full_name": "Facebook Driver",
        "photo_url": "https://example.com/fb_avatar.jpg",
        "firebase_uid": "fb-uid-facebook-999",
        "auth_provider": "facebook"
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

    user_dto = data["user"]
    assert user_dto["email"] == "facebook.user@veltrics.com"
    assert user_dto["full_name"] == "Facebook Driver"
    assert user_dto["auth_provider"] == "facebook"
    assert "facebook" in user_dto["linked_providers"]

    org_dto = data["organization"]
    assert org_dto["is_personal"] is True
    assert org_dto["max_vehicles"] == 3
    assert org_dto["owner_id"] == user_dto["id"]

    db = TestingSessionLocal()
    db_user = db.query(User).filter_by(email="facebook.user@veltrics.com").first()
    assert db_user is not None
    assert db_user.auth_provider == "facebook"
    assert "facebook" in db_user.linked_providers
    db.close()

def test_uc002_account_linking_facebook(client):
    """
    Alternate Flow A1: Account Linking
    If email matches existing account with different provider, backend attaches Facebook provider to linked_providers JSON array.
    """
    # Step 1: Register initial Google user
    google_payload = {
        "id_token": "google-token-123",
        "email": "shared.user@veltrics.com",
        "full_name": "Shared User",
        "firebase_uid": "fb-uid-google-123",
        "auth_provider": "google"
    }
    resp1 = client.post("/api/v1/auth/register", json=google_payload)
    assert resp1.status_code == 200
    initial_user = resp1.json()["user"]
    assert initial_user["auth_provider"] == "google"
    assert initial_user["linked_providers"] == ["google"]

    # Step 2: Register/login with Facebook using SAME email
    facebook_payload = {
        "id_token": "fb-token-456",
        "email": "shared.user@veltrics.com",
        "full_name": "Shared User FB",
        "firebase_uid": "fb-uid-facebook-456",
        "auth_provider": "facebook"
    }
    resp2 = client.post("/api/v1/auth/register", json=facebook_payload)
    assert resp2.status_code == 200
    linked_user = resp2.json()["user"]

    assert linked_user["id"] == initial_user["id"]
    assert "google" in linked_user["linked_providers"]
    assert "facebook" in linked_user["linked_providers"]

    db = TestingSessionLocal()
    db_user = db.query(User).filter_by(email="shared.user@veltrics.com").first()
    assert db_user is not None
    assert "google" in db_user.linked_providers
    assert "facebook" in db_user.linked_providers
    db.close()

def test_uc002_facebook_missing_email_returns_400(client):
    """
    Edge Case: Facebook permission denied for email -> API returns HTTP 400 Bad Request
    """
    payload = {
        "id_token": "mock-facebook-id-token-no-email",
        "email": None,
        "full_name": "No Email User",
        "firebase_uid": "fb-uid-no-email-123",
        "auth_provider": "facebook"
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert "EMAIL_REQUIRED" in response.json()["detail"] or "email" in response.json()["detail"].lower()
