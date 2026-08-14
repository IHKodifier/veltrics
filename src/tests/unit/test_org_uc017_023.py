import os
import sys
from datetime import datetime, timezone, timedelta
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
from app.models.user import User
from app.models.organization import Organization
from app.models.organization_invitation import OrganizationInvitation
from app.models.user_organization import UserOrganization
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.fuel_log import FuelLog
from app.models.trip import Trip
from app.models.expense_log import ExpenseLog
from app.models.maintenance import MaintenanceSchedule, ServiceRecord
from app.models.audit_log import AuditLog

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_setup():
    db = TestingSessionLocal()
    owner = User(
        id="owner-uc017-id",
        firebase_uid="uid-owner-uc017",
        email="owner_uc017@example.com",
        password_hash="hashed_pw_123",
        full_name="Org Owner"
    )
    admin = User(
        id="admin-uc017-id",
        firebase_uid="uid-admin-uc017",
        email="admin_uc017@example.com",
        password_hash="hashed_pw_123",
        full_name="Org Admin"
    )
    member = User(
        id="member-uc017-id",
        firebase_uid="uid-member-uc017",
        email="member_uc017@example.com",
        password_hash="hashed_pw_123",
        full_name="Org Member"
    )
    other_user = User(
        id="other-uc017-id",
        firebase_uid="uid-other-uc017",
        email="other_uc017@example.com",
        password_hash="hashed_pw_123",
        full_name="Other User"
    )
    db.add_all([owner, admin, member, other_user])
    db.commit()

    org = Organization(
        id="org-uc017-id",
        name="Veltrics Test Fleet",
        owner_id=owner.id,
        is_personal=False,
        max_vehicles=10,
        max_drivers=10,
        currency="USD"
    )
    personal_org = Organization(
        id="personal-org-uc017-id",
        name="Owner's Personal Org",
        owner_id=owner.id,
        is_personal=True,
        max_vehicles=3,
        max_drivers=3
    )
    db.add_all([org, personal_org])
    db.commit()

    user_org_owner = UserOrganization(
        user_id=owner.id,
        organization_id=org.id,
        role="owner",
        status="active"
    )
    user_org_admin = UserOrganization(
        user_id=admin.id,
        organization_id=org.id,
        role="admin",
        status="active"
    )
    user_org_member = UserOrganization(
        user_id=member.id,
        organization_id=org.id,
        role="driver",
        status="active"
    )
    db.add_all([user_org_owner, user_org_admin, user_org_member])
    db.commit()

    vehicle = Vehicle(
        id="veh-uc017-id",
        organization_id=org.id,
        make="Toyota",
        model="Hilux",
        year=2023,
        license_plate="PKR-1234",
        assigned_driver_id=member.id,
        status="ACTIVE"
    )
    db.add(vehicle)
    db.commit()

    owner_id = owner.id
    admin_id = admin.id
    member_id = member.id
    other_user_id = other_user.id
    org_id = org.id
    personal_org_id = personal_org.id
    vehicle_id = vehicle.id

    db.close()
    return {
        "owner_id": owner_id,
        "admin_id": admin_id,
        "member_id": member_id,
        "other_user_id": other_user_id,
        "org_id": org_id,
        "personal_org_id": personal_org_id,
        "vehicle_id": vehicle_id,
    }


def test_uc017_edit_organization_profile_success(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]

    payload = {
        "name": "Updated Veltrics Logistics",
        "address": "123 Fleet Way, Tech City",
        "phone": "+923001234567",
        "tax_id": "TAX-998877",
        "currency": "PKR",
        "website": "https://veltrics.io",
        "logo_url": "https://veltrics.io/logo.png"
    }

    response = client.patch(
        f"/api/v1/organizations/{org_id}",
        json=payload,
        headers={"X-User-ID": owner_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Veltrics Logistics"
    assert data["currency"] == "PKR"
    assert data["address"] == "123 Fleet Way, Tech City"

    db = TestingSessionLocal()
    audit = db.query(AuditLog).filter(
        AuditLog.organization_id == org_id,
        AuditLog.action == "EDIT_ORGANIZATION_PROFILE"
    ).first()
    assert audit is not None
    db.close()


def test_uc017_edit_organization_invalid_currency(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]

    payload = {
        "currency": "INVALID_CODE"
    }

    response = client.patch(
        f"/api/v1/organizations/{org_id}",
        json=payload,
        headers={"X-User-ID": owner_id}
    )
    assert response.status_code == 422


def test_uc017_edit_organization_forbidden(client, test_setup):
    org_id = test_setup["org_id"]
    other_user_id = test_setup["other_user_id"]

    payload = {"name": "Hacked Name"}
    response = client.patch(
        f"/api/v1/organizations/{org_id}",
        json=payload,
        headers={"X-User-ID": other_user_id}
    )
    assert response.status_code == 403


def test_uc018_invite_member_email_and_phone(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]

    payload = {
        "email": "invited_driver@example.com",
        "phone": "+923119876543",
        "role": "driver"
    }

    response = client.post(
        f"/api/v1/organizations/{org_id}/invitations",
        json=payload,
        headers={"X-User-ID": owner_id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "invited_driver@example.com"
    assert data["phone"] == "+923119876543"
    assert data["role"] == "driver"
    assert len(data["token"]) == 64
    assert data["status"] == "PENDING"


def test_uc018_invite_member_resend_update(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]

    payload1 = {
        "email": "resend_driver@example.com",
        "role": "driver"
    }
    r1 = client.post(f"/api/v1/organizations/{org_id}/invitations", json=payload1, headers={"X-User-ID": owner_id})
    token1 = r1.json()["token"]

    payload2 = {
        "email": "resend_driver@example.com",
        "role": "manager"
    }
    r2 = client.post(f"/api/v1/organizations/{org_id}/invitations", json=payload2, headers={"X-User-ID": owner_id})
    token2 = r2.json()["token"]

    assert r2.status_code == 201
    assert r2.json()["role"] == "manager"
    assert token1 != token2

    db = TestingSessionLocal()
    inv_count = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.organization_id == org_id,
        OrganizationInvitation.email == "resend_driver@example.com"
    ).count()
    assert inv_count == 1
    db.close()


def test_uc018_invite_member_missing_contact(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]

    payload = {"role": "driver"}
    response = client.post(
        f"/api/v1/organizations/{org_id}/invitations",
        json=payload,
        headers={"X-User-ID": owner_id}
    )
    assert response.status_code == 400


def test_uc019_accept_invitation_success(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]
    other_user_id = test_setup["other_user_id"]

    r_inv = client.post(
        f"/api/v1/organizations/{org_id}/invitations",
        json={"email": "other_uc017@example.com", "role": "manager"},
        headers={"X-User-ID": owner_id}
    )
    token = r_inv.json()["token"]

    r_inspect = client.get(f"/api/v1/invitations/{token}")
    assert r_inspect.status_code == 200
    assert r_inspect.json()["role"] == "manager"

    r_accept = client.post(
        f"/api/v1/invitations/{token}/accept",
        headers={"X-User-ID": other_user_id}
    )
    assert r_accept.status_code == 200
    assert r_accept.json()["role"] == "manager"

    db = TestingSessionLocal()
    membership = db.query(UserOrganization).filter(
        UserOrganization.organization_id == org_id,
        UserOrganization.user_id == other_user_id
    ).first()
    assert membership is not None
    assert membership.role == "manager"

    invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.token == token
    ).first()
    assert invitation.status == "ACCEPTED"
    db.close()


def test_uc019_accept_invitation_expired(client, test_setup):
    db = TestingSessionLocal()
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]
    other_user_id = test_setup["other_user_id"]

    expired_inv = OrganizationInvitation(
        organization_id=org_id,
        email="expired@example.com",
        role="driver",
        token="expired_token_64_characters_long_12345678901234567890123456789012",
        status="PENDING",
        invited_by_user_id=owner_id,
        expires_at=datetime.now(timezone.utc) - timedelta(days=1)
    )
    db.add(expired_inv)
    db.commit()

    token = expired_inv.token
    db.close()

    r_inspect = client.get(f"/api/v1/invitations/{token}")
    assert r_inspect.status_code == 410
    assert r_inspect.json()["detail"] == "INVITATION_EXPIRED"

    r_accept = client.post(
        f"/api/v1/invitations/{token}/accept",
        headers={"X-User-ID": other_user_id}
    )
    assert r_accept.status_code == 410
    assert r_accept.json()["detail"] == "INVITATION_EXPIRED"


def test_uc020_redeem_invitation_code(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]
    other_user_id = test_setup["other_user_id"]

    r_inv = client.post(
        f"/api/v1/organizations/{org_id}/invitations",
        json={"email": "redeem@example.com", "role": "admin"},
        headers={"X-User-ID": owner_id}
    )
    token = r_inv.json()["token"]

    redeem_payload = {
        "invitation_code": token,
        "user_id": other_user_id
    }
    response = client.post("/api/v1/invitations/redeem", json=redeem_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["organization_id"] == org_id
    assert data["role"] == "admin"
    assert data["status"] == "active"


def test_uc021_remove_member_success(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]
    member_id = test_setup["member_id"]
    vehicle_id = test_setup["vehicle_id"]

    response = client.delete(
        f"/api/v1/organizations/{org_id}/members/{member_id}",
        headers={"X-User-ID": owner_id}
    )
    assert response.status_code == 200

    db = TestingSessionLocal()
    membership = db.query(UserOrganization).filter(
        UserOrganization.organization_id == org_id,
        UserOrganization.user_id == member_id
    ).first()
    assert membership is None

    veh = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    assert veh.assigned_driver_id is None

    audit = db.query(AuditLog).filter(
        AuditLog.organization_id == org_id,
        AuditLog.action == "REMOVE_ORG_MEMBER"
    ).first()
    assert audit is not None
    db.close()


def test_uc021_remove_owner_forbidden(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]
    admin_id = test_setup["admin_id"]

    response = client.delete(
        f"/api/v1/organizations/{org_id}/members/{owner_id}",
        headers={"X-User-ID": admin_id}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot remove organization owner"


def test_uc022_cancel_invitation(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]

    r_inv = client.post(
        f"/api/v1/organizations/{org_id}/invitations",
        json={"email": "cancel_me@example.com", "role": "viewer"},
        headers={"X-User-ID": owner_id}
    )
    inv_id = r_inv.json()["id"]

    response = client.delete(
        f"/api/v1/organizations/{org_id}/invitations/{inv_id}",
        headers={"X-User-ID": owner_id}
    )
    assert response.status_code == 200

    db = TestingSessionLocal()
    inv = db.query(OrganizationInvitation).filter(OrganizationInvitation.id == inv_id).first()
    assert inv.status == "REVOKED"
    db.close()


def test_uc023_soft_delete_organization_success(client, test_setup):
    org_id = test_setup["org_id"]
    owner_id = test_setup["owner_id"]
    vehicle_id = test_setup["vehicle_id"]

    response = client.delete(
        f"/api/v1/organizations/{org_id}",
        headers={"X-User-ID": owner_id}
    )
    assert response.status_code == 200

    db = TestingSessionLocal()
    org = db.query(Organization).filter(Organization.id == org_id).first()
    assert org.deleted_at is not None

    veh = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    assert veh.deleted_at is not None

    audit = db.query(AuditLog).filter(
        AuditLog.organization_id == org_id,
        AuditLog.action == "DELETE_ORGANIZATION"
    ).first()
    assert audit is not None
    db.close()


def test_uc023_soft_delete_personal_org_blocked(client, test_setup):
    personal_org_id = test_setup["personal_org_id"]
    owner_id = test_setup["owner_id"]

    response = client.delete(
        f"/api/v1/organizations/{personal_org_id}",
        headers={"X-User-ID": owner_id}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Personal organization cannot be deleted"
