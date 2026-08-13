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
from app.models.user_organization import UserOrganization
from app.models.audit_log import AuditLog

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

def test_uc011_successful_account_deletion_and_anonymization(client):
    """
    AC 1: GIVEN an authenticated user
    WHEN DELETE /api/v1/users/me is invoked
    THE SYSTEM SHALL soft-delete the user record, anonymize PII fields, and record an audit log entry.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "gdpr.user@veltrics.com",
        "password": "Password123",
        "full_name": "GDPR User Test",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    user_id = reg_resp.json()["user"]["id"]
    access_token = reg_resp.json()["access_token"]

    del_resp = client.delete(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}", "X-User-ID": user_id}
    )
    assert del_resp.status_code == 200
    assert "message" in del_resp.json()

    db = TestingSessionLocal()
    deleted_user = db.query(User).filter(User.id == user_id).first()
    assert deleted_user is not None
    assert deleted_user.deleted_at is not None
    assert deleted_user.is_active is False
    assert deleted_user.email == f"deleted_{user_id}@anonymized.local"
    assert deleted_user.full_name == "Deleted User"
    assert deleted_user.phone_number is None
    assert deleted_user.city is None
    assert deleted_user.job_role is None
    assert deleted_user.photo_url is None
    assert deleted_user.avatar_url is None

    audit = db.query(AuditLog).filter(
        AuditLog.actor_id == user_id,
        AuditLog.action == "USER_ACCOUNT_DELETED"
    ).first()
    assert audit is not None
    assert audit.payload["user_id"] == user_id
    db.close()

def test_uc011_sole_owner_blocking(client):
    """
    AC 2: GIVEN a user who is the sole owner of an active non-personal organization with active members
    WHEN DELETE /api/v1/users/me is requested
    THE SYSTEM SHALL block deletion with HTTP 400 Bad Request.
    """
    db = TestingSessionLocal()
    owner = User(
        firebase_uid="owner-uid-11",
        email="org.owner@veltrics.com",
        full_name="Org Owner",
        auth_provider="email"
    )
    member = User(
        firebase_uid="member-uid-11",
        email="org.member@veltrics.com",
        full_name="Org Member",
        auth_provider="email"
    )
    db.add_all([owner, member])
    db.flush()

    org = Organization(
        name="Enterprise Fleet Inc",
        owner_id=owner.id,
        is_personal=False
    )
    db.add(org)
    db.flush()

    user_org_owner = UserOrganization(user_id=owner.id, organization_id=org.id, role="owner", status="active")
    user_org_member = UserOrganization(user_id=member.id, organization_id=org.id, role="driver", status="active")
    db.add_all([user_org_owner, user_org_member])
    db.commit()

    owner_id = owner.id
    db.close()

    del_resp = client.delete(
        "/api/v1/users/me",
        headers={"X-User-ID": owner_id}
    )
    assert del_resp.status_code == 400
    assert "SOLE_OWNER_BLOCK" in del_resp.json()["detail"]

def test_uc011_post_deletion_auth_rejection(client):
    """
    AC 3: GIVEN a soft-deleted user account
    WHEN attempting to authenticate, access profile, or refresh token
    THE SYSTEM SHALL reject access with appropriate error status codes.
    """
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "postdel.user@veltrics.com",
        "password": "Password123",
        "full_name": "Post Del User",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    user_id = reg_resp.json()["user"]["id"]
    access_token = reg_resp.json()["access_token"]
    refresh_token = reg_resp.json()["refresh_token"]

    del_resp = client.delete(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}", "X-User-ID": user_id}
    )
    assert del_resp.status_code == 200

    # Profile fetch post-deletion should be unauthorized
    profile_resp = client.get(
        "/api/v1/users/me",
        headers={"X-User-ID": user_id}
    )
    assert profile_resp.status_code == 401

    # Login post-deletion should be forbidden
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "postdel.user@veltrics.com",
        "password": "Password123"
    })
    assert login_resp.status_code in [401, 403]

    # Token refresh post-deletion should be rejected
    refresh_resp = client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert refresh_resp.status_code == 401
    assert "USER_DISABLED" in refresh_resp.json()["detail"]
