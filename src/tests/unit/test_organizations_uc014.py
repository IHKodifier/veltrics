import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app
from app.db.session import Base, get_db
import app.models as models
from app.models.user import User
from app.models.organization import Organization
from app.db.seed import seed_database

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
    db = TestingSessionLocal()
    seed_database(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_setup(client):
    db = TestingSessionLocal()
    user1 = User(
        firebase_uid="firebase-user-uc014-1",
        email="owner1@veltrics.com",
        full_name="Ahmad Khan",
        auth_provider="google"
    )
    user2 = User(
        firebase_uid="firebase-user-uc014-2",
        email="owner2@veltrics.com",
        full_name="Sara Malik",
        auth_provider="google"
    )
    db.add_all([user1, user2])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    db.close()

    return {
        "user1_id": user1.id,
        "user2_id": user2.id,
    }

def test_create_commercial_organization_success(client, test_setup):
    """UC-014: POST /api/v1/organizations creates commercial organization and sets owner role/ID."""
    payload = {
        "name": "LogiTrans Logistics Ltd",
        "is_personal": False,
        "max_vehicles": 10,
        "max_drivers": 10,
        "owner_id": test_setup["user1_id"]
    }
    response = client.post(
        "/api/v1/organizations",
        json=payload
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "LogiTrans Logistics Ltd"
    assert data["is_personal"] is False
    assert data["owner_id"] == test_setup["user1_id"]
    assert data["max_vehicles"] == 10

def test_auto_create_personal_organization(client, test_setup):
    """UC-014: POST /api/v1/organizations/personal auto-creates personal organization for user."""
    payload = {
        "user_id": test_setup["user1_id"],
        "user_name": "Ahmad Khan"
    }
    response = client.post(
        "/api/v1/organizations/personal",
        json=payload
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Ahmad Khan's Personal Org"
    assert data["is_personal"] is True
    assert data["owner_id"] == test_setup["user1_id"]

    # Subsequent call returns the existing personal org (idempotent)
    response_again = client.post(
        "/api/v1/organizations/personal",
        json=payload
    )
    assert response_again.status_code == 201
    assert response_again.json()["id"] == data["id"]

def test_create_organization_blank_name_rejected(client, test_setup):
    """UC-014: Blank or whitespace organization name rejected with HTTP 422."""
    payload = {
        "name": "   ",
        "owner_id": test_setup["user1_id"]
    }
    response = client.post(
        "/api/v1/organizations",
        json=payload
    )

    assert response.status_code == 422

def test_get_organizations_filtered_by_user(client, test_setup):
    """UC-014: GET /api/v1/organizations?user_id={id} returns list of user organizations."""
    # Create org for user1
    client.post(
        "/api/v1/organizations",
        json={"name": "Org Alpha", "owner_id": test_setup["user1_id"]}
    )
    # Create org for user2
    client.post(
        "/api/v1/organizations",
        json={"name": "Org Beta", "owner_id": test_setup["user2_id"]}
    )

    response = client.get(f"/api/v1/organizations?user_id={test_setup['user1_id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(o["name"] == "Org Alpha" for o in data)
    assert not any(o["name"] == "Org Beta" for o in data)

def test_get_organization_by_id_success_and_not_found(client, test_setup):
    """UC-014: GET /api/v1/organizations/{id} returns detail or 404 if not found."""
    create_res = client.post(
        "/api/v1/organizations",
        json={"name": "Detail Org", "owner_id": test_setup["user1_id"]}
    )
    org_id = create_res.json()["id"]

    get_res = client.get(f"/api/v1/organizations/{org_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Detail Org"

    invalid_res = client.get("/api/v1/organizations/non-existent-org-uuid")
    assert invalid_res.status_code == 404
    assert invalid_res.json()["detail"] == "Organization not found"
