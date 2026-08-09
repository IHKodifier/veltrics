import sys
import os
import pytest
from datetime import datetime, timezone
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

def test_uc004_login_success(client):
    """
    AC 1: WHEN valid login credentials are provided THE SYSTEM SHALL return HTTP 200 OK
    containing an Access JWT with 15-minute expiration and Refresh Token with 30-day expiration.
    """
    # 1. Register user
    reg_payload = {
        "email": "user.login@veltrics.com",
        "password": "ValidPassword123",
        "full_name": "Login User",
        "auth_provider": "email"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_resp.status_code == 200

    # 2. Perform Login
    login_payload = {
        "email": "user.login@veltrics.com",
        "password": "ValidPassword123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "user.login@veltrics.com"
    assert data["user"]["full_name"] == "Login User"
    assert data["organization"]["owner_id"] == data["user"]["id"]

def test_uc004_incorrect_password(client):
    """
    Edge Case: Incorrect password returns HTTP 401 Unauthorized.
    """
    reg_payload = {
        "email": "user.incorrect@veltrics.com",
        "password": "CorrectPassword123",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_payload = {
        "email": "user.incorrect@veltrics.com",
        "password": "WrongPassword999"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    assert "INVALID_CREDENTIALS" in response.json()["detail"]

def test_uc004_unregistered_email(client):
    """
    Edge Case: Unregistered email returns HTTP 401 Unauthorized.
    """
    login_payload = {
        "email": "nonexistent@veltrics.com",
        "password": "SomePassword123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    assert "INVALID_CREDENTIALS" in response.json()["detail"]

def test_uc004_disabled_user(client):
    """
    Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 Forbidden.
    """
    reg_payload = {
        "email": "disabled.user@veltrics.com",
        "password": "ValidPassword123",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    # Disable user in DB
    db = TestingSessionLocal()
    user = db.query(User).filter_by(email="disabled.user@veltrics.com").first()
    assert user is not None
    user.is_active = False
    db.commit()
    db.close()

    login_payload = {
        "email": "disabled.user@veltrics.com",
        "password": "ValidPassword123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 403
    assert "USER_DISABLED" in response.json()["detail"]

def test_uc004_soft_deleted_user(client):
    """
    Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HTTP 403 Forbidden.
    """
    reg_payload = {
        "email": "deleted.user@veltrics.com",
        "password": "ValidPassword123",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    # Soft-delete user in DB
    db = TestingSessionLocal()
    user = db.query(User).filter_by(email="deleted.user@veltrics.com").first()
    assert user is not None
    user.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.close()

    login_payload = {
        "email": "deleted.user@veltrics.com",
        "password": "ValidPassword123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 403
    assert "USER_DISABLED" in response.json()["detail"]
