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

def test_uc005_sign_in_google_existing_user(client):
    """
    AC 1: WHEN an existing Google user signs in,
    THE SYSTEM SHALL return HTTP 200 OK with valid AuthSessionDTO containing access & refresh tokens.
    """
    # 1. Initial registration
    reg_payload = {
        "id_token": "google-token-existing-101",
        "auth_provider": "google",
        "email": "returning.google@veltrics.com",
        "full_name": "Returning Google User",
        "firebase_uid": "fb-uid-returning-google"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_resp.status_code == 200

    # 2. Subsequent Sign-in
    login_payload = {
        "id_token": "google-token-existing-101",
        "auth_provider": "google",
        "email": "returning.google@veltrics.com",
        "firebase_uid": "fb-uid-returning-google"
    }
    response = client.post("/api/v1/auth/register", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "returning.google@veltrics.com"
    assert "google" in data["user"]["linked_providers"]

def test_uc005_sign_in_facebook_existing_user(client):
    """
    AC 2: WHEN an existing Facebook user signs in,
    THE SYSTEM SHALL return HTTP 200 OK with valid AuthSessionDTO.
    """
    # 1. Initial registration
    reg_payload = {
        "id_token": "facebook-token-existing-202",
        "auth_provider": "facebook",
        "email": "returning.facebook@veltrics.com",
        "full_name": "Returning Facebook User",
        "firebase_uid": "fb-uid-returning-facebook"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_resp.status_code == 200

    # 2. Subsequent Sign-in
    login_payload = {
        "id_token": "facebook-token-existing-202",
        "auth_provider": "facebook",
        "email": "returning.facebook@veltrics.com",
        "firebase_uid": "fb-uid-returning-facebook"
    }
    response = client.post("/api/v1/auth/register", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "returning.facebook@veltrics.com"
    assert "facebook" in data["user"]["linked_providers"]

def test_uc005_sign_in_email_password_existing_user(client):
    """
    AC 3: WHEN an existing Email/Password user signs in via POST /api/v1/auth/login,
    THE SYSTEM SHALL return HTTP 200 OK with valid AuthSessionDTO.
    """
    # 1. Initial registration
    reg_payload = {
        "email": "returning.email@veltrics.com",
        "password": "ValidPassword123!",
        "full_name": "Returning Email User",
        "auth_provider": "email"
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_resp.status_code == 200

    # 2. Subsequent Login
    login_payload = {
        "email": "returning.email@veltrics.com",
        "password": "ValidPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "returning.email@veltrics.com"
    assert data["user"]["full_name"] == "Returning Email User"

def test_uc005_account_linking_multi_provider(client):
    """
    AC 4 (Account Linking Flow A1): WHEN an existing user registered via email
    subsequently signs in via Google or Facebook using the same email,
    THE SYSTEM SHALL attach the new auth provider to linked_providers list.
    """
    # 1. Register with email & password
    reg_payload = {
        "email": "multi.auth@veltrics.com",
        "password": "Password123!",
        "full_name": "Multi Auth User",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    # 2. Sign in using Google with same email
    google_payload = {
        "id_token": "google-token-link-303",
        "auth_provider": "google",
        "email": "multi.auth@veltrics.com",
        "firebase_uid": "fb-uid-multi-auth-g"
    }
    response_g = client.post("/api/v1/auth/register", json=google_payload)
    assert response_g.status_code == 200
    data_g = response_g.json()
    assert "email" in data_g["user"]["linked_providers"]
    assert "google" in data_g["user"]["linked_providers"]

    # 3. Sign in using Facebook with same email
    fb_payload = {
        "id_token": "fb-token-link-404",
        "auth_provider": "facebook",
        "email": "multi.auth@veltrics.com",
        "firebase_uid": "fb-uid-multi-auth-fb"
    }
    response_fb = client.post("/api/v1/auth/register", json=fb_payload)
    assert response_fb.status_code == 200
    data_fb = response_fb.json()
    assert "email" in data_fb["user"]["linked_providers"]
    assert "google" in data_fb["user"]["linked_providers"]
    assert "facebook" in data_fb["user"]["linked_providers"]

def test_uc005_incorrect_password(client):
    """
    Edge Case: Incorrect password on email login returns HTTP 401 Unauthorized.
    """
    reg_payload = {
        "email": "wrong.pass@veltrics.com",
        "password": "CorrectPassword123!",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_payload = {
        "email": "wrong.pass@veltrics.com",
        "password": "WrongPassword999!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    assert "INVALID_CREDENTIALS" in response.json()["detail"]

def test_uc005_nonexistent_email(client):
    """
    Edge Case: Sign in with non-existent email returns HTTP 401 Unauthorized.
    """
    login_payload = {
        "email": "notfound@veltrics.com",
        "password": "SomePassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    assert "INVALID_CREDENTIALS" in response.json()["detail"]

def test_uc005_disabled_user_account(client):
    """
    Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 Forbidden.
    """
    reg_payload = {
        "email": "disabled.uc005@veltrics.com",
        "password": "ValidPassword123!",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    # Disable user in database
    db = TestingSessionLocal()
    user = db.query(User).filter_by(email="disabled.uc005@veltrics.com").first()
    assert user is not None
    user.is_active = False
    db.commit()
    db.close()

    login_payload = {
        "email": "disabled.uc005@veltrics.com",
        "password": "ValidPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 403
    assert "USER_DISABLED" in response.json()["detail"]

def test_uc005_soft_deleted_user_account(client):
    """
    Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HTTP 403 Forbidden.
    """
    reg_payload = {
        "email": "deleted.uc005@veltrics.com",
        "password": "ValidPassword123!",
        "auth_provider": "email"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    # Soft delete user in database
    db = TestingSessionLocal()
    user = db.query(User).filter_by(email="deleted.uc005@veltrics.com").first()
    assert user is not None
    user.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.close()

    login_payload = {
        "email": "deleted.uc005@veltrics.com",
        "password": "ValidPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 403
    assert "USER_DISABLED" in response.json()["detail"]
