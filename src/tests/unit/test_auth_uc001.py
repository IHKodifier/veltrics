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
from app.models.organization import Organization

# In-memory SQLite database for testing
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

def test_uc001_new_user_google_one_tap_creates_user_and_personal_org(client):
    """
    AC 1: WHEN a new user authenticates with Google One-Tap THE SYSTEM SHALL
    create a `users` row and a personal `organizations` row with `max_vehicles=3` in a single transaction.
    """
    payload = {
        "id_token": "mock-google-id-token-12345",
        "email": "driver.test@veltrics.com",
        "full_name": "Test Driver",
        "photo_url": "https://example.com/avatar.jpg",
        "firebase_uid": "fb-uid-test-12345"
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()

    # Validate response structure
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    
    # Validate User DTO
    user_dto = data["user"]
    assert user_dto["email"] == "driver.test@veltrics.com"
    assert user_dto["full_name"] == "Test Driver"
    assert user_dto["firebase_uid"] == "fb-uid-test-12345"
    assert user_dto["auth_provider"] == "google"

    # Validate Organization DTO
    org_dto = data["organization"]
    assert org_dto["is_personal"] is True
    assert org_dto["max_vehicles"] == 3
    assert org_dto["max_drivers"] == 3
    assert org_dto["owner_id"] == user_dto["id"]

    # Verify DB records
    db = TestingSessionLocal()
    db_user = db.query(User).filter_by(email="driver.test@veltrics.com").first()
    assert db_user is not None
    
    db_org = db.query(Organization).filter_by(owner_id=db_user.id).first()
    assert db_org is not None
    assert db_org.max_vehicles == 3
    assert db_org.is_personal is True
    db.close()

def test_uc001_existing_user_google_one_tap_returns_existing_data(client):
    """
    AC 2: WHEN an existing user authenticates with Google One-Tap THE SYSTEM SHALL
    return the user's existing organization and profile payload without creating duplicate DB records.
    """
    payload = {
        "id_token": "mock-google-id-token-12345",
        "email": "existing.user@veltrics.com",
        "full_name": "Existing User",
        "firebase_uid": "fb-uid-existing-999"
    }

    # Initial registration
    resp1 = client.post("/api/v1/auth/register", json=payload)
    assert resp1.status_code == 200
    user_id_1 = resp1.json()["user"]["id"]
    org_id_1 = resp1.json()["organization"]["id"]

    # Second login call with same credentials
    resp2 = client.post("/api/v1/auth/register", json=payload)
    assert resp2.status_code == 200
    user_id_2 = resp2.json()["user"]["id"]
    org_id_2 = resp2.json()["organization"]["id"]

    # Assert no duplicate users/orgs created
    assert user_id_1 == user_id_2
    assert org_id_1 == org_id_2

    db = TestingSessionLocal()
    user_count = db.query(User).filter_by(email="existing.user@veltrics.com").count()
    org_count = db.query(Organization).filter_by(owner_id=user_id_1).count()
    assert user_count == 1
    assert org_count == 1
    db.close()
