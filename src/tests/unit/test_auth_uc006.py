import sys
import os
import pytest
from datetime import datetime, timezone, timedelta
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
from app.core.config import settings

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

def test_uc006_forgot_password_success(client):
    """
    AC 1: WHEN a registered user requests a password reset link/token for their email
    THE SYSTEM SHALL issue a reset token with a 5-minute expiration and return HTTP 200 OK.
    """
    # 1. Register a test user
    reg_payload = {
        "email": "reset.user@veltrics.com",
        "password": "OldPassword123",
        "full_name": "Reset User",
        "auth_provider": "email"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_resp.status_code == 200

    # 2. Request forgot password reset token
    forgot_payload = {"email": "reset.user@veltrics.com"}
    forgot_resp = client.post("/api/v1/auth/forgot-password", json=forgot_payload)
    assert forgot_resp.status_code == 200
    res_data = forgot_resp.json()
    assert "reset_token" in res_data
    assert res_data["reset_token"] is not None

def test_uc006_forgot_password_user_not_found(client):
    """
    AC 2: WHEN a reset request is submitted for a non-existent email
    THE SYSTEM SHALL return HTTP 404 NOT_FOUND.
    """
    forgot_payload = {"email": "nonexistent@veltrics.com"}
    forgot_resp = client.post("/api/v1/auth/forgot-password", json=forgot_payload)
    assert forgot_resp.status_code == 404
    assert forgot_resp.json()["detail"] == "USER_NOT_FOUND"

def test_uc006_reset_password_success(client):
    """
    AC 3: WHEN a user submits a valid reset token and strong new password
    THE SYSTEM SHALL update user's password hash and return HTTP 200 OK, allowing subsequent logins with new password.
    """
    # 1. Register user
    reg_payload = {
        "email": "user.reset.flow@veltrics.com",
        "password": "OldPassword123",
        "full_name": "Reset Flow User",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    # 2. Request reset token
    forgot_resp = client.post("/api/v1/auth/forgot-password", json={"email": "user.reset.flow@veltrics.com"})
    reset_token = forgot_resp.json()["reset_token"]

    # 3. Reset password
    reset_payload = {
        "token": reset_token,
        "new_password": "NewStrongPassword123"
    }
    reset_resp = client.post("/api/v1/auth/reset-password", json=reset_payload)
    assert reset_resp.status_code == 200
    assert "successfully reset" in reset_resp.json()["message"].lower()

    # 4. Old password login must fail
    old_login = client.post("/api/v1/auth/login", json={"email": "user.reset.flow@veltrics.com", "password": "OldPassword123"})
    assert old_login.status_code == 401

    # 5. New password login must succeed
    new_login = client.post("/api/v1/auth/login", json={"email": "user.reset.flow@veltrics.com", "password": "NewStrongPassword123"})
    assert new_login.status_code == 200

def test_uc006_reset_password_invalid_or_wrong_token(client):
    """
    AC 4: WHEN an invalid token or token of wrong type (e.g. access token) is submitted
    THE SYSTEM SHALL return HTTP 400 BAD_REQUEST.
    """
    # 1. Register user
    reg_payload = {
        "email": "invalid.token@veltrics.com",
        "password": "ValidPassword123",
        "auth_provider": "email"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    access_token = reg_resp.json()["access_token"]

    # 2. Try resetting with invalid string token
    res1 = client.post("/api/v1/auth/reset-password", json={"token": "invalid-jwt-token-str", "new_password": "NewPassword123"})
    assert res1.status_code == 400
    assert "INVALID_TOKEN" in res1.json()["detail"]

    # 3. Try resetting with an access token (wrong token type)
    res2 = client.post("/api/v1/auth/reset-password", json={"token": access_token, "new_password": "NewPassword123"})
    assert res2.status_code == 400
    assert "INVALID_TOKEN" in res2.json()["detail"]

def test_uc006_reset_password_weak_password(client):
    """
    AC 5: WHEN a new password does not satisfy password policy (min 8 chars, 1 upper, 1 digit)
    THE SYSTEM SHALL return HTTP 400 BAD_REQUEST with WEAK_PASSWORD detail.
    """
    reg_payload = {
        "email": "weak.pass@veltrics.com",
        "password": "ValidPassword123",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    forgot_resp = client.post("/api/v1/auth/forgot-password", json={"email": "weak.pass@veltrics.com"})
    reset_token = forgot_resp.json()["reset_token"]

    # Attempt weak password reset
    res = client.post("/api/v1/auth/reset-password", json={"token": reset_token, "new_password": "weak"})
    assert res.status_code == 400
    assert "WEAK_PASSWORD" in res.json()["detail"]
