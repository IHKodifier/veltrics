import os
import sys
import json
import pytest
import hmac
import hashlib
from datetime import datetime, timedelta, timezone

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

try:
    import jwt
except ImportError:
    from jose import jwt

from app.core.config import settings
from app.main import app
from app.db.session import Base, get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.user_organization import UserOrganization
from app.models.subscription import Subscription
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


client = TestClient(app)

SAFEPAY_SECRET = "test_safepay_secret_key"


def create_access_token(data: dict) -> str:
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def generate_safepay_signature(payload_bytes: bytes, secret: str = SAFEPAY_SECRET) -> str:
    return hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()


@pytest.fixture(autouse=True)
def setup_database():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def create_test_user_and_org(db_session, user_email="owner_pay@example.com", org_name="Payment Test Org"):
    user = User(
        firebase_uid=f"uid_{user_email}",
        email=user_email,
        full_name="Payment Owner",
        password_hash="hashed_pass_123",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    org = Organization(
        name=org_name,
        owner_id=user.id,
        tier="free",
        max_vehicles=3,
        max_drivers=3,
        ad_bonus_vehicles=0,
        ad_bonus_drivers=0,
    )
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)

    member_assoc = UserOrganization(user_id=user.id, organization_id=org.id, role="OWNER")
    db_session.add(member_assoc)
    db_session.commit()

    token = create_access_token(data={"sub": user.id, "email": user.email})
    headers = {"Authorization": f"Bearer {token}"}

    return user, org, headers


def test_uc080_checkout_session_safepay():
    """UC-080: Initiate Pro Subscription Checkout (Safepay)"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "safepay_checkout@example.com", "Safepay Org")

    payload = {
        "organization_id": org.id,
        "gateway": "SAFEPAY",
        "billing_cycle": "MONTHLY",
    }
    response = client.post("/api/v1/payments/checkout-session", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "checkout_url" in data
    assert "session_id" in data
    assert data["gateway"] == "SAFEPAY"

    sub = db_session.query(Subscription).filter_by(organization_id=org.id).first()
    assert sub is not None
    assert sub.status == "PENDING"
    assert sub.gateway == "SAFEPAY"
    assert sub.billing_cycle == "MONTHLY"

    # Test non-owner access (create another user)
    other_user = User(firebase_uid="uid_other_user@example.com", email="other_user@example.com", full_name="Other User", password_hash="pw")
    db_session.add(other_user)
    db_session.commit()
    other_token = create_access_token(data={"sub": other_user.id, "email": other_user.email})
    other_headers = {"Authorization": f"Bearer {other_token}"}

    resp_forbidden = client.post("/api/v1/payments/checkout-session", json=payload, headers=other_headers)
    assert resp_forbidden.status_code == 403
    db_session.close()


def test_uc081_safepay_webhook_entitlement_activation():
    """UC-081 & UC-121: Safepay Webhook Processing & Entitlement Activation"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "safepay_webhook@example.com", "Safepay Webhook Org")

    # Initiate checkout to create PENDING sub
    sub = Subscription(
        organization_id=org.id,
        gateway="SAFEPAY",
        status="PENDING",
        billing_cycle="MONTHLY",
    )
    db_session.add(sub)
    db_session.commit()

    webhook_payload = {
        "event_id": "evt_safepay_1001",
        "event_type": "payment.completed",
        "tracker_id": "trk_990011",
        "organization_id": org.id,
        "amount": 1900,
        "currency": "PKR",
        "customer": {"email": user.email},
    }

    raw_body = json.dumps(webhook_payload).encode("utf-8")
    signature = generate_safepay_signature(raw_body)

    response = client.post(
        "/api/v1/payments/webhooks/safepay",
        content=raw_body,
        headers={"Content-Type": "application/json", "X-Safepay-Signature": signature},
    )
    assert response.status_code == 200, response.text
    res_json = response.json()
    assert res_json["status"] == "success"

    db_session.refresh(sub)
    assert sub.status == "ACTIVE"
    assert sub.gateway_payload is not None

    db_session.refresh(org)
    assert org.tier == "pro"
    assert org.max_vehicles == 25
    assert org.max_drivers == 15

    # Check audit log
    audit = db_session.query(AuditLog).filter_by(action="SUBSCRIPTION_ACTIVATED").first()
    assert audit is not None
    db_session.close()


def test_uc082_safepay_webhook_payment_failure():
    """UC-082 & UC-121: Handle Payment Checkout Failure & Grace Period"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "safepay_fail@example.com", "Safepay Fail Org")

    # Active subscription
    now = datetime.now(timezone.utc)
    sub = Subscription(
        organization_id=org.id,
        gateway="SAFEPAY",
        status="ACTIVE",
        billing_cycle="MONTHLY",
        current_period_end=now + timedelta(days=20),
    )
    org.tier = "pro"
    org.max_vehicles = 25
    org.max_drivers = 15
    db_session.add(sub)
    db_session.commit()

    webhook_payload = {
        "event_id": "evt_safepay_fail_1002",
        "event_type": "payment.failed",
        "tracker_id": "trk_990012",
        "organization_id": org.id,
        "reason": "Insufficient funds",
    }
    raw_body = json.dumps(webhook_payload).encode("utf-8")
    signature = generate_safepay_signature(raw_body)

    response = client.post(
        "/api/v1/payments/webhooks/safepay",
        content=raw_body,
        headers={"Content-Type": "application/json", "X-Safepay-Signature": signature},
    )
    assert response.status_code == 200, response.text

    db_session.refresh(sub)
    assert sub.status == "PAST_DUE"
    grace_end = sub.grace_period_ends_at
    if grace_end and grace_end.tzinfo is None:
        grace_end = grace_end.replace(tzinfo=timezone.utc)
    assert grace_end > now
    db_session.close()


def test_uc083_view_subscription_status():
    """UC-083: View Subscription Status & Billing History"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "sub_status@example.com", "Status Org")

    response = client.get(f"/api/v1/payments/subscription-status?organization_id={org.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["tier"] == "free"
    assert data["max_vehicles"] == 3
    assert data["max_drivers"] == 3
    assert data["status"] == "NO_SUBSCRIPTION"
    db_session.close()


def test_uc084_cancel_subscription():
    """UC-084: Cancel Active Subscription"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "cancel_sub@example.com", "Cancel Sub Org")

    now = datetime.now(timezone.utc)
    period_end = now + timedelta(days=15)
    sub = Subscription(
        organization_id=org.id,
        gateway="SAFEPAY",
        status="ACTIVE",
        billing_cycle="MONTHLY",
        current_period_end=period_end,
    )
    org.tier = "pro"
    org.max_vehicles = 25
    org.max_drivers = 15
    db_session.add(sub)
    db_session.commit()

    payload = {"organization_id": org.id, "reason": "No longer needed"}
    response = client.post("/api/v1/payments/cancel-subscription", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["cancel_at_period_end"] is True

    db_session.refresh(sub)
    assert sub.cancel_at_period_end is True

    # Test canceling already scheduled cancellation returns 400 Bad Request
    resp_again = client.post("/api/v1/payments/cancel-subscription", json=payload, headers=headers)
    assert resp_again.status_code == 400
    db_session.close()


def test_uc085_downgrade_bonus_slot_preservation():
    """UC-085 & UC-120: Pro-to-Free Downgrade & Bonus Slot Preservation Protocol"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "downgrade@example.com", "Downgrade Org")

    past_time = datetime.now(timezone.utc) - timedelta(days=1)
    sub = Subscription(
        organization_id=org.id,
        gateway="SAFEPAY",
        status="ACTIVE",
        billing_cycle="MONTHLY",
        cancel_at_period_end=True,
        current_period_end=past_time,
    )
    org.tier = "pro"
    org.max_vehicles = 25
    org.max_drivers = 15
    org.ad_bonus_vehicles = 2  # Earned 2 bonus slots on free tier previously!
    org.ad_bonus_drivers = 1
    db_session.add(sub)
    db_session.commit()

    # Trigger downgrade protocol
    response = client.post("/api/v1/payments/process-downgrades")
    assert response.status_code == 200
    res_data = response.json()
    assert org.id in res_data["downgraded_organizations"]

    db_session.refresh(sub)
    assert sub.status == "CANCELED"

    db_session.refresh(org)
    assert org.tier == "free"
    # Preserved bonus slots: 3 base + 2 bonus = 5 max_vehicles
    assert org.max_vehicles == 5
    # 3 base + 1 bonus = 4 max_drivers
    assert org.max_drivers == 4
    db_session.close()


def test_uc121_webhook_idempotency_and_unrecognized_events():
    """UC-121: Safepay Webhook Idempotency & Unrecognized Event Logging"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "idempotent@example.com", "Idempotent Org")

    sub = Subscription(
        organization_id=org.id,
        gateway="SAFEPAY",
        status="PENDING",
        billing_cycle="MONTHLY",
    )
    db_session.add(sub)
    db_session.commit()

    webhook_payload = {
        "event_id": "evt_duplicate_555",
        "event_type": "payment.completed",
        "tracker_id": "trk_555",
        "organization_id": org.id,
    }
    raw_body = json.dumps(webhook_payload).encode("utf-8")
    signature = generate_safepay_signature(raw_body)
    headers_hook = {"Content-Type": "application/json", "X-Safepay-Signature": signature}

    # First call
    r1 = client.post("/api/v1/payments/webhooks/safepay", content=raw_body, headers=headers_hook)
    assert r1.status_code == 200

    # Second duplicate call
    r2 = client.post("/api/v1/payments/webhooks/safepay", content=raw_body, headers=headers_hook)
    assert r2.status_code == 200
    assert r2.json()["message"] == "Event already processed"

    # Unrecognized event type
    unrec_payload = {
        "event_id": "evt_unrec_777",
        "event_type": "unknown.custom.event",
        "organization_id": org.id,
    }
    raw_unrec = json.dumps(unrec_payload).encode("utf-8")
    sig_unrec = generate_safepay_signature(raw_unrec)
    r3 = client.post("/api/v1/payments/webhooks/safepay", content=raw_unrec, headers={"Content-Type": "application/json", "X-Safepay-Signature": sig_unrec})
    assert r3.status_code == 200
    assert "Ignored unrecognized event type" in r3.json()["message"]
    db_session.close()
