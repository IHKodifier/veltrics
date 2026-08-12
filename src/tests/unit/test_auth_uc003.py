import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add src/backend to python sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app
from app.db.session import Base, get_db
from app.models.user import User
from app.models.organization import Organization

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
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_uc003_email_registration_success(client):
    """
    AC 1: WHEN valid email/password details are submitted THE SYSTEM SHALL return HTTP 200/201
    containing user and organization IDs, with auth_provider = 'email' and 'email' in linked_providers.
    """
    payload = {
        "email": "jane.doe@veltrics.com",
        "password": "SecurePassword123",
        "full_name": "Jane Doe",
        "auth_provider": "email"
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

    user_dto = data["user"]
    assert user_dto["email"] == "jane.doe@veltrics.com"
    assert user_dto["full_name"] == "Jane Doe"
    assert user_dto["auth_provider"] == "email"
    assert "email" in user_dto["linked_providers"]

    org_dto = data["organization"]
    assert org_dto["is_personal"] is True
    assert org_dto["max_vehicles"] == 3
    assert org_dto["owner_id"] == user_dto["id"]

    db = TestingSessionLocal()
    db_user = db.query(User).filter_by(email="jane.doe@veltrics.com").first()
    assert db_user is not None
    assert db_user.auth_provider == "email"
    assert "email" in db_user.linked_providers
    assert db_user.password_hash is not None
    db.close()

def test_uc003_account_linking_email(client):
    """
    Alternate Flow A1: Account Linking
    If user signed up via Google, submitting email registration with same email links the 'email' provider.
    """
    google_payload = {
        "id_token": "google-token-789",
        "email": "linked.user@veltrics.com",
        "full_name": "Linked User",
        "firebase_uid": "fb-uid-google-789",
        "auth_provider": "google"
    }
    resp1 = client.post("/api/v1/auth/register", json=google_payload)
    assert resp1.status_code == 200
    initial_user = resp1.json()["user"]
    assert initial_user["auth_provider"] == "google"
    assert initial_user["linked_providers"] == ["google"]

    email_payload = {
        "email": "linked.user@veltrics.com",
        "password": "NewStrongPass1",
        "full_name": "Linked User",
        "auth_provider": "email"
    }
    resp2 = client.post("/api/v1/auth/register", json=email_payload)
    assert resp2.status_code == 200
    linked_user = resp2.json()["user"]

    assert linked_user["id"] == initial_user["id"]
    assert "google" in linked_user["linked_providers"]
    assert "email" in linked_user["linked_providers"]

def test_uc003_weak_password_validation(client):
    """
    Edge Case: Weak passwords (less than 8 chars, missing upper, missing digit) return HTTP 400 Bad Request.
    """
    # Too short
    resp1 = client.post("/api/v1/auth/register", json={
        "email": "user1@veltrics.com",
        "password": "Pass1",
        "auth_provider": "email"
    })
    assert resp1.status_code == 400
    assert "WEAK_PASSWORD" in resp1.json()["detail"]

    # No uppercase
    resp2 = client.post("/api/v1/auth/register", json={
        "email": "user2@veltrics.com",
        "password": "password123",
        "auth_provider": "email"
    })
    assert resp2.status_code == 400
    assert "WEAK_PASSWORD" in resp2.json()["detail"]

    # No digit
    resp3 = client.post("/api/v1/auth/register", json={
        "email": "user3@veltrics.com",
        "password": "PasswordOnly",
        "auth_provider": "email"
    })
    assert resp3.status_code == 400
    assert "WEAK_PASSWORD" in resp3.json()["detail"]

def test_uc003_missing_email_or_password(client):
    """
    Edge Case: Missing email or missing password for email auth provider returns HTTP 400 Bad Request.
    """
    resp_no_email = client.post("/api/v1/auth/register", json={
        "password": "ValidPassword1",
        "auth_provider": "email"
    })
    assert resp_no_email.status_code == 400
    assert "EMAIL_REQUIRED" in resp_no_email.json()["detail"]

    resp_no_pass = client.post("/api/v1/auth/register", json={
        "email": "nopass@veltrics.com",
        "auth_provider": "email"
    })
    assert resp_no_pass.status_code == 400
    assert "PASSWORD_REQUIRED" in resp_no_pass.json()["detail"]
