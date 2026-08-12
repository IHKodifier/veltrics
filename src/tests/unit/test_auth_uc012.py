import sys
import os
import pytest
from unittest.mock import patch
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
from app.models.audit_log import AuditLog
from app.services.audit_service import AuditService

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

def test_uc012_audit_log_registration(client):
    """
    AC 1: System creates immutable AuditLog entry upon user registration.
    """
    reg_payload = {
        "email": "audit.register@veltrics.com",
        "password": "ValidPassword123",
        "full_name": "Audit Register User",
        "auth_provider": "email"
    }
    response = client.post("/api/v1/auth/register", json=reg_payload, headers={"User-Agent": "VeltricsTestAgent/1.0"})
    assert response.status_code == 200

    db = TestingSessionLocal()
    audit = db.query(AuditLog).filter(AuditLog.action == "USER_REGISTER").first()
    assert audit is not None
    assert audit.actor_id == response.json()["user"]["id"]
    assert audit.organization_id == response.json()["organization"]["id"]
    assert audit.payload["ip_address"] == "testclient" or audit.payload["ip_address"] == "127.0.0.1"
    assert audit.payload["user_agent"] == "VeltricsTestAgent/1.0"
    db.close()

def test_uc012_audit_log_login_success(client):
    """
    AC 2: System records USER_LOGIN_SUCCESS audit entry with IP & User-Agent metadata.
    """
    reg_payload = {
        "email": "audit.login@veltrics.com",
        "password": "ValidPassword123",
        "full_name": "Audit Login User",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_payload = {
        "email": "audit.login@veltrics.com",
        "password": "ValidPassword123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload, headers={"User-Agent": "CustomApp/2.0"})
    assert response.status_code == 200

    db = TestingSessionLocal()
    audit = db.query(AuditLog).filter(AuditLog.action == "USER_LOGIN_SUCCESS").order_by(AuditLog.created_at.desc()).first()
    assert audit is not None
    assert audit.actor_id == response.json()["user"]["id"]
    assert audit.organization_id == response.json()["organization"]["id"]
    assert audit.payload["user_agent"] == "CustomApp/2.0"
    db.close()

def test_uc012_audit_log_login_failure_unauthenticated(client):
    """
    A1: Unauthenticated attempt records USER_LOGIN_FAILURE with actor_id = None.
    """
    login_payload = {
        "email": "nonexistent.audit@veltrics.com",
        "password": "WrongPassword123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload, headers={"User-Agent": "TestScanner/1.0"})
    assert response.status_code == 401

    db = TestingSessionLocal()
    audit = db.query(AuditLog).filter(AuditLog.action == "USER_LOGIN_FAILURE").first()
    assert audit is not None
    assert audit.actor_id is None
    assert audit.payload["email"] == "nonexistent.audit@veltrics.com"
    assert audit.payload["reason"] == "USER_NOT_FOUND"
    assert audit.payload["user_agent"] == "TestScanner/1.0"
    db.close()

def test_uc012_audit_log_password_reset_flow(client):
    """
    AC 3: System records USER_PASSWORD_RESET_REQUEST and USER_PASSWORD_RESET_SUCCESS audit entries.
    """
    reg_payload = {
        "email": "reset.audit@veltrics.com",
        "password": "OldPassword123",
        "full_name": "Reset User",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    # Forgot password
    forgot_resp = client.post("/api/v1/auth/forgot-password", json={"email": "reset.audit@veltrics.com"})
    assert forgot_resp.status_code == 200
    token = forgot_resp.json()["reset_token"]

    # Reset password
    reset_resp = client.post("/api/v1/auth/reset-password", json={"token": token, "new_password": "NewPassword123"})
    assert reset_resp.status_code == 200

    db = TestingSessionLocal()
    req_audit = db.query(AuditLog).filter(AuditLog.action == "USER_PASSWORD_RESET_REQUEST").first()
    succ_audit = db.query(AuditLog).filter(AuditLog.action == "USER_PASSWORD_RESET_SUCCESS").first()

    assert req_audit is not None
    assert req_audit.payload["email"] == "reset.audit@veltrics.com"

    assert succ_audit is not None
    assert succ_audit.payload["email"] == "reset.audit@veltrics.com"
    db.close()

def test_uc012_audit_log_logout(client):
    """
    AC 4: System records USER_LOGOUT audit entry upon session termination.
    """
    reg_payload = {
        "email": "logout.audit@veltrics.com",
        "password": "ValidPassword123",
        "auth_provider": "email"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    refresh_token = reg_resp.json()["refresh_token"]

    logout_resp = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert logout_resp.status_code == 200

    db = TestingSessionLocal()
    audit = db.query(AuditLog).filter(AuditLog.action == "USER_LOGOUT").first()
    assert audit is not None
    assert audit.actor_id == reg_resp.json()["user"]["id"]
    assert audit.payload["refresh_token_revoked"] is True
    db.close()

def test_uc012_non_blocking_audit_error_handling():
    """
    Edge Case: Audit log DB write exception is handled safely and does not block user request flow.
    """
    db = TestingSessionLocal()
    # Mocking db.add to raise an Exception when adding AuditLog
    with patch.object(db, 'add', side_effect=Exception("Database connection timeout")):
        result = AuditService.log_event(
            db,
            action="USER_LOGIN_SUCCESS",
            actor_id="some-user-id",
            payload={"test": "data"}
        )
        # Audit log creation returns None on exception without crashing
        assert result is None
    db.close()
