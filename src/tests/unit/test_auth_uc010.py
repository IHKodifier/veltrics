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
from app.models.audit_log import AuditLog
from app.models.revoked_token import RevokedToken

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

def test_uc010_successful_logout_and_revocation(client):
    """
    AC 1: GIVEN an authenticated user session with a valid refresh token
    WHEN submitted to POST /api/v1/auth/logout
    THE SYSTEM SHALL revoke the refresh token and write an audit log entry.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "logout.user@veltrics.com",
        "password": "Password123",
        "full_name": "Logout User",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    refresh_token = reg_resp.json()["refresh_token"]
    user_id = reg_resp.json()["user"]["id"]

    logout_resp = client.post("/api/v1/auth/logout", json={
        "refresh_token": refresh_token
    })
    assert logout_resp.status_code == 200
    assert "message" in logout_resp.json()

    db = TestingSessionLocal()
    revoked = db.query(RevokedToken).filter(RevokedToken.token == refresh_token).first()
    assert revoked is not None
    assert revoked.user_id == user_id

    audit = db.query(AuditLog).filter(AuditLog.actor_id == user_id, AuditLog.action == "USER_LOGOUT").first()
    assert audit is not None
    db.close()

def test_uc010_revoked_token_refresh_rejection(client):
    """
    AC 2: GIVEN a revoked refresh token
    WHEN submitted to POST /api/v1/auth/refresh
    THE SYSTEM SHALL reject the request with HTTP 401 Unauthorized.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "revoked.refresh@veltrics.com",
        "password": "Password123",
        "full_name": "Revoked Token User",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    refresh_token = reg_resp.json()["refresh_token"]

    # Logout to revoke token
    logout_resp = client.post("/api/v1/auth/logout", json={
        "refresh_token": refresh_token
    })
    assert logout_resp.status_code == 200

    # Attempt to refresh using revoked token
    refresh_resp = client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert refresh_resp.status_code == 401
    assert "TOKEN_REVOKED" in refresh_resp.json()["detail"]

def test_uc010_invalid_or_malformed_logout_token(client):
    """
    AC 3: GIVEN a malformed or invalid refresh token
    WHEN submitted to POST /api/v1/auth/logout
    THE SYSTEM SHALL return HTTP 401 Unauthorized.
    """
    logout_resp = client.post("/api/v1/auth/logout", json={
        "refresh_token": "malformed.invalid.jwt"
    })
    assert logout_resp.status_code == 401

def test_uc010_repeat_logout_idempotency(client):
    """
    AC 4: GIVEN a refresh token that has already been revoked
    WHEN logout is called again with the same token
    THE SYSTEM SHALL handle the request idempotently with HTTP 200 OK.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "idempotent.logout@veltrics.com",
        "password": "Password123",
        "full_name": "Idempotent User",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    refresh_token = reg_resp.json()["refresh_token"]

    first = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert first.status_code == 200

    second = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert second.status_code == 200
