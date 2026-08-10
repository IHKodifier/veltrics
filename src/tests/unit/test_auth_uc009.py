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

def test_uc009_valid_token_refresh(client):
    """
    AC 1: GIVEN a valid active refresh token
    WHEN submitted to POST /api/v1/auth/refresh
    THE SYSTEM SHALL return a new access token and a new refresh token.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "refresh.user@veltrics.com",
        "password": "Password123",
        "full_name": "Refresh Tester",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    old_refresh_token = reg_resp.json()["refresh_token"]

    refresh_resp = client.post("/api/v1/auth/refresh", json={
        "refresh_token": old_refresh_token
    })
    assert refresh_resp.status_code == 200
    data = refresh_resp.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0
    assert len(data["refresh_token"]) > 0

def test_uc009_invalid_or_expired_refresh_token(client):
    """
    AC 2: GIVEN an invalid, expired, or non-refresh token (e.g. access or reset token)
    WHEN submitted to POST /api/v1/auth/refresh
    THE SYSTEM SHALL reject the request with HTTP 401 Unauthorized.
    """
    # Case 1: Malformed string
    res_bad = client.post("/api/v1/auth/refresh", json={
        "refresh_token": "not.a.valid.jwt"
    })
    assert res_bad.status_code == 401

    # Case 2: Register user and send access_token instead of refresh_token
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "wrong.type@veltrics.com",
        "password": "Password123",
        "full_name": "Wrong Token Type",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    access_token = reg_resp.json()["access_token"]

    res_wrong_type = client.post("/api/v1/auth/refresh", json={
        "refresh_token": access_token
    })
    assert res_wrong_type.status_code == 401

def test_uc009_disabled_user_refresh_rejection(client):
    """
    AC 3: GIVEN a refresh token for a disabled or soft-deleted user account
    WHEN submitted to POST /api/v1/auth/refresh
    THE SYSTEM SHALL return HTTP 401 Unauthorized.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "disabled.refresh@veltrics.com",
        "password": "Password123",
        "full_name": "Disabled Refresh User",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    refresh_token = reg_resp.json()["refresh_token"]
    user_id = reg_resp.json()["user"]["id"]

    # Disable user in DB
    db = TestingSessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    user.is_active = False
    db.commit()
    db.close()

    res_disabled = client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert res_disabled.status_code == 401

def test_uc009_access_token_authorization(client):
    """
    AC 4: GIVEN a newly issued access token from POST /api/v1/auth/refresh
    WHEN used in Authorization header for protected endpoints (e.g. GET /api/v1/users/me)
    THE SYSTEM SHALL successfully authorize the request.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "auth.access@veltrics.com",
        "password": "Password123",
        "full_name": "Auth Access User",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    refresh_token = reg_resp.json()["refresh_token"]
    user_id = reg_resp.json()["user"]["id"]

    refresh_resp = client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert refresh_resp.status_code == 200
    new_access_token = refresh_resp.json()["access_token"]

    headers = {"X-User-ID": user_id, "Authorization": f"Bearer {new_access_token}"}
    me_resp = client.get("/api/v1/users/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["id"] == user_id
