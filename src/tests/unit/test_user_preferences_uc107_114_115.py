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

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_uc107_114_115_get_and_patch_user_preferences(client):
    """
    AC test for UC-107 (Theme), UC-114 (Units), and UC-115 (Locale):
    GIVEN an authenticated user
    WHEN they query GET /api/v1/users/me/preferences or update via PATCH /api/v1/users/me/preferences
    THE SYSTEM SHALL persist choices (theme, accent_color, high_contrast, units, locale) in users.preferences JSON.
    """
    # 1. Register test user
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "prefs.user@veltrics.com",
        "password": "Password123",
        "full_name": "Preference User",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    user_id = reg_resp.json()["user"]["id"]
    access_token = reg_resp.json()["access_token"]
    headers = {"X-User-ID": user_id, "Authorization": f"Bearer {access_token}"}

    # 2. Get default preferences
    get_resp = client.get("/api/v1/users/me/preferences", headers=headers)
    assert get_resp.status_code == 200
    prefs = get_resp.json()
    assert prefs["theme"] == "SYSTEM"
    assert prefs["accent_color"] == "slate_teal"
    assert prefs["high_contrast"] is False
    assert prefs["units"] == "METRIC"
    assert prefs["locale"] == "en"

    # 3. Update theme to DARK and locale to Urdu (ur) (RTL)
    patch_payload_1 = {
        "theme": "DARK",
        "accent_color": "amber_gold",
        "high_contrast": True,
        "units": "IMPERIAL",
        "locale": "ur"
    }
    patch_resp_1 = client.patch("/api/v1/users/me/preferences", json=patch_payload_1, headers=headers)
    assert patch_resp_1.status_code == 200
    updated_1 = patch_resp_1.json()
    assert updated_1["theme"] == "DARK"
    assert updated_1["accent_color"] == "amber_gold"
    assert updated_1["high_contrast"] is True
    assert updated_1["units"] == "IMPERIAL"
    assert updated_1["locale"] == "ur"

    # 4. Partial update — change locale to Arabic (ar) and theme back to LIGHT
    patch_payload_2 = {
        "theme": "LIGHT",
        "locale": "ar"
    }
    patch_resp_2 = client.patch("/api/v1/users/me/preferences", json=patch_payload_2, headers=headers)
    assert patch_resp_2.status_code == 200
    updated_2 = patch_resp_2.json()
    assert updated_2["theme"] == "LIGHT"
    assert updated_2["accent_color"] == "amber_gold"  # preserved
    assert updated_2["high_contrast"] is True  # preserved
    assert updated_2["units"] == "IMPERIAL"  # preserved
    assert updated_2["locale"] == "ar"

def test_uc107_114_115_invalid_preference_values_rejected(client):
    """
    WHEN invalid theme, units, or locale options are submitted
    THE SYSTEM SHALL return HTTP 422 Unprocessable Entity validation error.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "invalid.prefs@veltrics.com",
        "password": "Password123",
        "full_name": "Invalid Pref User",
        "auth_provider": "email"
    })
    user_id = reg_resp.json()["user"]["id"]
    headers = {"X-User-ID": user_id}

    # Invalid theme
    res = client.patch("/api/v1/users/me/preferences", json={"theme": "NEON_BLUE"}, headers=headers)
    assert res.status_code == 422

    # Invalid unit system
    res = client.patch("/api/v1/users/me/preferences", json={"units": "CUBITS"}, headers=headers)
    assert res.status_code == 422

    # Invalid locale code
    res = client.patch("/api/v1/users/me/preferences", json={"locale": " Klingon"}, headers=headers)
    assert res.status_code == 422
