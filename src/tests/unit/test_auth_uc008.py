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

def test_uc008_get_user_profile(client):
    """
    AC 1: GIVEN an authenticated registered user
    WHEN they request GET /api/v1/users/me
    THE SYSTEM SHALL return the current user's full profile payload (email, full_name, phone, city, job_role, avatar_url, auth_provider).
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "view.profile@veltrics.com",
        "password": "Password123",
        "full_name": "Alice Operator",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    user_id = reg_resp.json()["user"]["id"]
    access_token = reg_resp.json()["access_token"]

    headers = {"X-User-ID": user_id, "Authorization": f"Bearer {access_token}"}

    get_resp = client.get("/api/v1/users/me", headers=headers)
    assert get_resp.status_code == 200
    profile = get_resp.json()

    assert profile["id"] == user_id
    assert profile["email"] == "view.profile@veltrics.com"
    assert profile["full_name"] == "Alice Operator"
    assert profile["auth_provider"] == "email"
    assert "city" in profile
    assert "job_role" in profile
    assert "avatar_url" in profile

def test_uc008_patch_user_profile(client):
    """
    AC 2: GIVEN an authenticated user updating their profile details
    WHEN they submit PATCH /api/v1/users/me with new fields (full_name, phone_number, city, job_role, avatar_url)
    THE SYSTEM SHALL persist the updated details in DB and return the updated profile payload.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "edit.profile@veltrics.com",
        "password": "Password123",
        "full_name": "Bob Original",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    user_id = reg_resp.json()["user"]["id"]
    access_token = reg_resp.json()["access_token"]

    headers = {"X-User-ID": user_id, "Authorization": f"Bearer {access_token}"}

    patch_payload = {
        "full_name": "Bob Master Mechanic",
        "phone_number": "+15559876543",
        "city": "Dallas",
        "job_role": "Fleet Manager",
        "avatar_url": "https://cdn.veltrics.com/avatars/bob.png"
    }

    patch_resp = client.patch("/api/v1/users/me", json=patch_payload, headers=headers)
    assert patch_resp.status_code == 200
    updated = patch_resp.json()

    assert updated["full_name"] == "Bob Master Mechanic"
    assert updated["phone_number"] == "+15559876543"
    assert updated["city"] == "Dallas"
    assert updated["job_role"] == "Fleet Manager"
    assert updated["avatar_url"] == "https://cdn.veltrics.com/avatars/bob.png"

    # Re-fetch via GET to confirm persistence
    get_resp = client.get("/api/v1/users/me", headers=headers)
    assert get_resp.status_code == 200
    refetched = get_resp.json()
    assert refetched["full_name"] == "Bob Master Mechanic"
    assert refetched["city"] == "Dallas"
    assert refetched["job_role"] == "Fleet Manager"

def test_uc008_profile_field_validation(client):
    """
    AC 3: GIVEN a profile update request with invalid full name length (< 2 characters)
    THE SYSTEM SHALL reject the update request with HTTP 400 or 422 Unprocessable Entity.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "validation.profile@veltrics.com",
        "password": "Password123",
        "full_name": "Charlie Valid",
        "auth_provider": "email"
    })
    user_id = reg_resp.json()["user"]["id"]
    headers = {"X-User-ID": user_id}

    # Attempt short name
    invalid_patch = {"full_name": "C"}
    res = client.patch("/api/v1/users/me", json=invalid_patch, headers=headers)
    assert res.status_code in [400, 422]

def test_uc008_unauthenticated_access(client):
    """
    AC 4: GIVEN an unauthenticated request to profile endpoints without user identity
    THE SYSTEM SHALL return HTTP 401 Unauthorized or HTTP 403 Forbidden.
    """
    get_resp = client.get("/api/v1/users/me")
    assert get_resp.status_code in [401, 403]

    patch_resp = client.patch("/api/v1/users/me", json={"full_name": "Hacker Name"})
    assert patch_resp.status_code in [401, 403]
