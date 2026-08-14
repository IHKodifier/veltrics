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
        firebase_uid="firebase-user-uc015-1",
        email="owner1_uc015@veltrics.com",
        full_name="User One",
        auth_provider="google"
    )
    user2 = User(
        firebase_uid="firebase-user-uc015-2",
        email="owner2_uc015@veltrics.com",
        full_name="User Two",
        auth_provider="google"
    )
    db.add_all([user1, user2])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)

    org1 = Organization(
        name="User One Org Alpha",
        owner_id=user1.id,
        is_personal=True,
        max_vehicles=3,
        max_drivers=3
    )
    org2 = Organization(
        name="User One Org Beta",
        owner_id=user1.id,
        is_personal=False,
        max_vehicles=10,
        max_drivers=5
    )
    org_user2 = Organization(
        name="User Two Org Only",
        owner_id=user2.id,
        is_personal=True,
        max_vehicles=3,
        max_drivers=3
    )
    db.add_all([org1, org2, org_user2])
    db.commit()
    db.refresh(org1)
    db.refresh(org2)
    db.refresh(org_user2)
    db.close()

    return {
        "user1_id": user1.id,
        "user2_id": user2.id,
        "org1_id": org1.id,
        "org2_id": org2.id,
        "user2_org_id": org_user2.id
    }

def test_switch_organization_context_success(client, test_setup):
    """UC-015: POST /api/v1/organizations/switch switches active context for valid user membership."""
    payload = {
        "target_organization_id": test_setup["org2_id"],
        "user_id": test_setup["user1_id"]
    }
    response = client.post(
        "/api/v1/organizations/switch",
        json=payload,
        headers={"X-User-ID": test_setup["user1_id"]}
    )

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Active organization switched successfully"
    assert data["active_organization"]["id"] == test_setup["org2_id"]
    assert data["active_organization"]["name"] == "User One Org Beta"

def test_switch_organization_unauthorized_access_forbidden(client, test_setup):
    """UC-015: Switch attempt to organization owned by another user yields HTTP 403 Forbidden."""
    payload = {
        "target_organization_id": test_setup["user2_org_id"],
        "user_id": test_setup["user1_id"]
    }
    response = client.post(
        "/api/v1/organizations/switch",
        json=payload
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "User does not have access to target organization"

def test_switch_organization_non_existent_not_found(client, test_setup):
    """UC-015: Switch attempt to non-existent organization yields HTTP 404 Not Found."""
    payload = {
        "target_organization_id": "non-existent-org-uuid",
        "user_id": test_setup["user1_id"]
    }
    response = client.post(
        "/api/v1/organizations/switch",
        json=payload
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Organization not found"

def test_get_active_organization_success(client, test_setup):
    """UC-015: GET /api/v1/organizations/active returns current primary organization for user."""
    response = client.get(
        f"/api/v1/organizations/active?user_id={test_setup['user1_id']}"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["owner_id"] == test_setup["user1_id"]
    assert data["id"] in [test_setup["org1_id"], test_setup["org2_id"]]

def test_get_active_organization_not_found(client, test_setup):
    """UC-015: GET /api/v1/organizations/active for user with no org returns HTTP 404 Not Found."""
    response = client.get("/api/v1/organizations/active?user_id=non-existent-user-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Active organization not found"
