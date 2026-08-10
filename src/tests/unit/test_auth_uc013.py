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
from app.models.user_session import UserSession
from app.models.revoked_token import RevokedToken

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

def test_uc013_list_active_sessions(client):
    """
    AC 1: WHEN GET /api/v1/users/me/sessions is called THE SYSTEM SHALL return active sessions.
    """
    reg_payload = {
        "email": "session.user@veltrics.com",
        "password": "ValidPassword123",
        "full_name": "Session User",
        "auth_provider": "email"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload, headers={"User-Agent": "MobileApp/1.0"})
    assert reg_resp.status_code == 200
    access_token = reg_resp.json()["access_token"]

    sessions_resp = client.get("/api/v1/users/me/sessions", headers={"Authorization": f"Bearer {access_token}"})
    assert sessions_resp.status_code == 200

    data = sessions_resp.json()
    assert len(data) >= 1
    session = data[0]
    assert "id" in session
    assert session["user_id"] == reg_resp.json()["user"]["id"]
    assert "device_model" in session
    assert "ip_address" in session

def test_uc013_revoke_session(client):
    """
    AC 2: User can revoke a specific session.
    """
    reg_payload = {
        "email": "revoke.user@veltrics.com",
        "password": "ValidPassword123",
        "auth_provider": "email"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    access_token = reg_resp.json()["access_token"]

    login_resp = client.post("/api/v1/auth/login", json={"email": "revoke.user@veltrics.com", "password": "ValidPassword123"})
    assert login_resp.status_code == 200

    sessions_resp = client.get("/api/v1/users/me/sessions", headers={"Authorization": f"Bearer {access_token}"})
    sessions = sessions_resp.json()
    assert len(sessions) >= 2

    target_session_id = sessions[0]["id"]
    del_resp = client.delete(f"/api/v1/users/me/sessions/{target_session_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert del_resp.status_code == 200
    assert del_resp.json()["revoked_session_id"] == target_session_id

    # Check session count decreased
    after_resp = client.get("/api/v1/users/me/sessions", headers={"Authorization": f"Bearer {access_token}"})
    assert len(after_resp.json()) == len(sessions) - 1

def test_uc013_revoked_session_blocked_on_refresh(client):
    """
    Acceptance Criterion: WHEN a session is revoked via API THE SYSTEM SHALL block any subsequent refresh requests using that refresh token with HTTP 401.
    """
    reg_payload = {
        "email": "blocked.refresh@veltrics.com",
        "password": "ValidPassword123",
        "auth_provider": "email"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    access_token = reg_resp.json()["access_token"]
    refresh_token = reg_resp.json()["refresh_token"]

    sessions_resp = client.get("/api/v1/users/me/sessions", headers={"Authorization": f"Bearer {access_token}"})
    target_session_id = sessions_resp.json()[0]["id"]

    # Revoke session
    client.delete(f"/api/v1/users/me/sessions/{target_session_id}", headers={"Authorization": f"Bearer {access_token}"})

    # Attempt to refresh token using revoked refresh token
    refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 401
    assert "TOKEN_REVOKED" in refresh_resp.json()["detail"]

def test_uc013_revoke_all_other_sessions(client):
    """
    A1: User can revoke all other active sessions.
    """
    reg_payload = {
        "email": "revoke.others@veltrics.com",
        "password": "ValidPassword123",
        "auth_provider": "email"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    access_token = reg_resp.json()["access_token"]

    # Trigger additional login
    client.post("/api/v1/auth/login", json={"email": "revoke.others@veltrics.com", "password": "ValidPassword123"})
    client.post("/api/v1/auth/login", json={"email": "revoke.others@veltrics.com", "password": "ValidPassword123"})

    sessions_before = client.get("/api/v1/users/me/sessions", headers={"Authorization": f"Bearer {access_token}"}).json()
    assert len(sessions_before) >= 3

    revoke_others_resp = client.post("/api/v1/users/me/sessions/revoke-others", headers={"Authorization": f"Bearer {access_token}"})
    assert revoke_others_resp.status_code == 200
    assert revoke_others_resp.json()["revoked_count"] >= 1
