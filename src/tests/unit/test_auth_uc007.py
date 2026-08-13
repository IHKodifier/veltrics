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

def test_uc007_get_and_patch_user_profile(client):
    """
    AC 1: GIVEN an authenticated user
    WHEN they query GET /api/v1/users/me or update profile via PATCH /api/v1/users/me
    THE SYSTEM SHALL return updated profile with full_name, phone_number, city, job_role, avatar_url.
    """
    # 1. Register test user
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "profile.user@veltrics.com",
        "password": "Password123",
        "full_name": "Initial Name",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    user_id = reg_resp.json()["user"]["id"]
    access_token = reg_resp.json()["access_token"]

    headers = {"X-User-ID": user_id, "Authorization": f"Bearer {access_token}"}

    # 2. Get profile
    get_resp = client.get("/api/v1/users/me", headers=headers)
    assert get_resp.status_code == 200
    profile = get_resp.json()
    assert profile["email"] == "profile.user@veltrics.com"
    assert profile["full_name"] == "Initial Name"

    # 3. Patch profile
    patch_payload = {
        "full_name": "Updated Profile Name",
        "phone_number": "+923001234567",
        "city": "Lahore",
        "job_role": "Fleet Manager",
        "avatar_url": "https://cdn.veltrics.com/avatars/user1.png"
    }
    patch_resp = client.patch("/api/v1/users/me", json=patch_payload, headers=headers)
    assert patch_resp.status_code == 200
    updated = patch_resp.json()
    assert updated["full_name"] == "Updated Profile Name"
    assert updated["phone_number"] == "+923001234567"
    assert updated["city"] == "Lahore"
    assert updated["job_role"] == "Fleet Manager"
    assert updated["avatar_url"] == "https://cdn.veltrics.com/avatars/user1.png"

def test_uc007_profile_completion_endpoint(client):
    """
    AC 2: GIVEN a user completing onboarding on SCR-AUTH-007
    WHEN they submit POST /api/v1/users/me/complete-profile with display_name and city
    THE SYSTEM SHALL persist details and return updated session payload.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "complete.onboarding@veltrics.com",
        "password": "Password123",
        "full_name": "Temp Name",
        "auth_provider": "email"
    })
    user_id = reg_resp.json()["user"]["id"]
    headers = {"X-User-ID": user_id}

    comp_payload = {
        "full_name": "Verified Manager",
        "city": "Karachi",
        "phone_number": "+923219876543",
        "job_role": "Dispatcher"
    }
    comp_resp = client.post("/api/v1/users/me/complete-profile", json=comp_payload, headers=headers)
    assert comp_resp.status_code == 200
    session_data = comp_resp.json()
    assert session_data["user"]["full_name"] == "Verified Manager"
    assert session_data["user"]["city"] == "Karachi"

def test_uc007_display_name_validation(client):
    """
    AC 3: GIVEN a profile update request with invalid display name length (< 2 chars)
    THE SYSTEM SHALL return HTTP 422 or 400 validation error.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "validation.user@veltrics.com",
        "password": "Password123",
        "full_name": "Valid Name",
        "auth_provider": "email"
    })
    user_id = reg_resp.json()["user"]["id"]
    headers = {"X-User-ID": user_id}

    # Name too short (1 char)
    invalid_patch = {"full_name": "A"}
    res = client.patch("/api/v1/users/me", json=invalid_patch, headers=headers)
    assert res.status_code in [400, 422]

def test_uc007_multi_tenant_role_authorization(client):
    """
    AC 4: GIVEN tenant-scoped requests
    THE SYSTEM SHALL enforce multi-tenant role-based authorization:
      - Owner/Admin has permission.
      - Non-member user receives HTTP 403 Forbidden.
    """
    # 1. Register User A (Org Owner)
    reg_a = client.post("/api/v1/auth/register", json={
        "email": "owner.user@veltrics.com",
        "password": "Password123",
        "full_name": "Owner User",
        "auth_provider": "email"
    })
    user_a_id = reg_a.json()["user"]["id"]
    org_id = reg_a.json()["organization"]["id"]

    # 2. Register User B (Unrelated User)
    reg_b = client.post("/api/v1/auth/register", json={
        "email": "unrelated.user@veltrics.com",
        "password": "Password123",
        "full_name": "Unrelated User",
        "auth_provider": "email"
    })
    user_b_id = reg_b.json()["user"]["id"]

    # 3. User A accesses org endpoint -> Success (Owner)
    res_owner = client.get(
        "/api/v1/users/me/tenant-check",
        headers={"X-User-ID": user_a_id, "X-Organization-ID": org_id}
    )
    assert res_owner.status_code == 200
    assert res_owner.json()["role"] == "owner"

    # 4. User B attempts to access User A's Org -> 403 Forbidden
    res_unauthorized = client.get(
        "/api/v1/users/me/tenant-check",
        headers={"X-User-ID": user_b_id, "X-Organization-ID": org_id}
    )
    assert res_unauthorized.status_code == 403
    assert "FORBIDDEN" in res_unauthorized.json()["detail"] or "Forbidden" in res_unauthorized.json()["detail"]
