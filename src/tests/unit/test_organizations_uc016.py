import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app
from app.db.session import Base, get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.organization_invitation import OrganizationInvitation
from app.db.seed import seed_database

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
        firebase_uid="firebase-user-uc016-owner",
        email="owner_uc016@veltrics.com",
        full_name="Owner User",
        auth_provider="google"
    )
    user2 = User(
        firebase_uid="firebase-user-uc016-other",
        email="other_uc016@veltrics.com",
        full_name="Other User",
        auth_provider="google"
    )
    db.add_all([user1, user2])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)

    org1 = Organization(
        name="Owner Org Fleet",
        owner_id=user1.id,
        is_personal=False,
        max_vehicles=10,
        max_drivers=5
    )
    org2 = Organization(
        name="Other User Org",
        owner_id=user2.id,
        is_personal=True,
        max_vehicles=3,
        max_drivers=3
    )
    db.add_all([org1, org2])
    db.commit()
    db.refresh(org1)
    db.refresh(org2)
    db.close()

    return {
        "user1_id": user1.id,
        "user2_id": user2.id,
        "org1_id": org1.id,
        "org2_id": org2.id
    }

def test_create_organization_invitation_success(client, test_setup):
    """UC-016: Owner can create organization invitation, generating a secure 64-char token with 7-day TTL."""
    payload = {
        "email": "invitee@veltrics.com",
        "role": "manager"
    }
    response = client.post(
        f"/api/v1/organizations/{test_setup['org1_id']}/invitations",
        json=payload,
        headers={"X-User-ID": test_setup["user1_id"]}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["organization_id"] == test_setup["org1_id"]
    assert data["email"] == "invitee@veltrics.com"
    assert data["role"] == "manager"
    assert data["status"] == "PENDING"
    assert len(data["token"]) == 64
    assert data["invited_by_user_id"] == test_setup["user1_id"]
    assert "expires_at" in data

def test_create_invitation_invalid_email(client, test_setup):
    """UC-016: Inviting with invalid or blank email yields HTTP 422 Unprocessable Entity."""
    payload = {
        "email": "not-an-email-address",
        "role": "driver"
    }
    response = client.post(
        f"/api/v1/organizations/{test_setup['org1_id']}/invitations",
        json=payload,
        headers={"X-User-ID": test_setup["user1_id"]}
    )

    assert response.status_code == 422

def test_create_invitation_invalid_role(client, test_setup):
    """UC-016: Inviting with unsupported role string yields HTTP 422 Unprocessable Entity."""
    payload = {
        "email": "valid.driver@veltrics.com",
        "role": "superman"
    }
    response = client.post(
        f"/api/v1/organizations/{test_setup['org1_id']}/invitations",
        json=payload,
        headers={"X-User-ID": test_setup["user1_id"]}
    )

    assert response.status_code == 422

def test_create_invitation_duplicate_updates_ttl(client, test_setup):
    """UC-016: Re-inviting same email updates existing invitation token and TTL without creating duplicate active row."""
    payload = {
        "email": "duplicate@veltrics.com",
        "role": "driver"
    }
    res1 = client.post(
        f"/api/v1/organizations/{test_setup['org1_id']}/invitations",
        json=payload,
        headers={"X-User-ID": test_setup["user1_id"]}
    )
    assert res1.status_code == 201
    inv1_id = res1.json()["id"]
    token1 = res1.json()["token"]

    payload["role"] = "admin"
    res2 = client.post(
        f"/api/v1/organizations/{test_setup['org1_id']}/invitations",
        json=payload,
        headers={"X-User-ID": test_setup["user1_id"]}
    )
    assert res2.status_code == 201
    data2 = res2.json()

    assert data2["id"] == inv1_id
    assert data2["role"] == "admin"
    assert len(data2["token"]) == 64

    # Verify directly in DB that only 1 record exists
    db = TestingSessionLocal()
    count = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.organization_id == test_setup["org1_id"],
        OrganizationInvitation.email == "duplicate@veltrics.com"
    ).count()
    db.close()
    assert count == 1

def test_create_invitation_unauthorized_non_owner(client, test_setup):
    """UC-016: Non-owner caller attempting to send invitation yields HTTP 403 Forbidden."""
    payload = {
        "email": "forbidden@veltrics.com",
        "role": "viewer"
    }
    response = client.post(
        f"/api/v1/organizations/{test_setup['org1_id']}/invitations",
        json=payload,
        headers={"X-User-ID": test_setup["user2_id"]}
    )

    assert response.status_code == 403
    assert "User does not have access" in response.json()["detail"]

def test_list_organization_invitations_success(client, test_setup):
    """UC-016: Owner can list all pending invitations for organization."""
    client.post(
        f"/api/v1/organizations/{test_setup['org1_id']}/invitations",
        json={"email": "member1@veltrics.com", "role": "driver"},
        headers={"X-User-ID": test_setup["user1_id"]}
    )
    client.post(
        f"/api/v1/organizations/{test_setup['org1_id']}/invitations",
        json={"email": "member2@veltrics.com", "role": "viewer"},
        headers={"X-User-ID": test_setup["user1_id"]}
    )

    response = client.get(
        f"/api/v1/organizations/{test_setup['org1_id']}/invitations",
        headers={"X-User-ID": test_setup["user1_id"]}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    emails = {item["email"] for item in data}
    assert "member1@veltrics.com" in emails
    assert "member2@veltrics.com" in emails

def test_list_invitations_non_existent_org(client, test_setup):
    """UC-016: Listing invitations for non-existent org yields HTTP 404 Not Found."""
    response = client.get(
        "/api/v1/organizations/non-existent-org-id/invitations",
        headers={"X-User-ID": test_setup["user1_id"]}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Organization not found"
