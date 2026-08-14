import os
import sys
import json
import pytest
import hmac
import hashlib
from datetime import datetime, timezone

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
from app.models.vehicle import Vehicle
from app.models.driver import Driver
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
client = TestClient(app)

ADMOB_SECRET = "test_admob_ssv_secret_key"


def create_access_token(data: dict) -> str:
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def generate_admob_ssv_signature(token: str, reward_type: str, org_id: str, secret: str = ADMOB_SECRET) -> str:
    message = f"{token}:{reward_type}:{org_id}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()


@pytest.fixture(autouse=True)
def setup_database():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def create_test_user_and_org(db_session, user_email="owner_ad@example.com", org_name="Ad Engine Org"):
    user = User(
        firebase_uid=f"uid_{user_email}",
        email=user_email,
        full_name="Ad Test Owner",
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
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Organization-ID": org.id,
    }

    return user, org, headers


def test_uc086_087_vehicle_and_driver_quota_wall_enforcement():
    """UC-086 & UC-087: Vehicle and Driver Quota Wall Enforcement"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "quota_test@example.com", "Quota Org")

    # Add 3 vehicles (up to max_vehicles=3)
    for i in range(1, 4):
        v_payload = {
            "organization_id": org.id,
            "name": f"Vehicle {i}",
            "make": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "vin": f"VIN1000000000000{i}",
            "license_plate": f"LEA-00{i}",
        }
        res = client.post("/api/v1/vehicles", json=v_payload, headers=headers)
        assert res.status_code == 201, res.text

    # 4th vehicle creation must trigger HTTP 402 QUOTA_EXCEEDED
    v_4 = {
        "organization_id": org.id,
        "name": "Vehicle 4 Overflow",
        "make": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "vin": "VIN10000000000004",
        "license_plate": "LEA-004",
    }
    res_overflow = client.post("/api/v1/vehicles", json=v_4, headers=headers)
    assert res_overflow.status_code == 402, res_overflow.text
    assert "VEHICLE_QUOTA_EXCEEDED" in res_overflow.json()["detail"]

    # Add 3 drivers (up to max_drivers=3)
    for i in range(1, 4):
        d_payload = {
            "full_name": f"Driver {i}",
            "phone": f"+92300111220{i}",
            "license_number": f"LIC-900{i}",
        }
        res_d = client.post("/api/v1/drivers", json=d_payload, headers=headers)
        assert res_d.status_code == 201, res_d.text

    # 4th driver creation must trigger HTTP 402 DRIVER_QUOTA_EXCEEDED
    d_4 = {
        "full_name": "Driver 4 Overflow",
        "phone": "+923001112204",
        "license_number": "LIC-9004",
    }
    res_d_overflow = client.post("/api/v1/drivers", json=d_4, headers=headers)
    assert res_d_overflow.status_code == 402, res_d_overflow.text
    assert "DRIVER_QUOTA_EXCEEDED" in res_d_overflow.json()["detail"]
    db_session.close()


def test_uc100_120_verify_ad_reward_signature_and_slot_increment():
    """UC-100 & UC-120: Verify Rewarded Ad Completion & Increment Bonus Quota"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "reward_test@example.com", "Reward Org")

    # Watch rewarded ad for vehicle slot
    token_v = "ad_token_veh_001"
    sig_v = generate_admob_ssv_signature(token_v, "vehicle_slot", org.id)
    reward_v_payload = {
        "organization_id": org.id,
        "reward_type": "vehicle_slot",
        "admob_ssv_token": token_v,
        "signature": sig_v,
    }
    res_v = client.post("/api/v1/ads/verify-reward", json=reward_v_payload, headers=headers)
    assert res_v.status_code == 200, res_v.text
    data_v = res_v.json()
    assert data_v["new_ad_bonus_slots"] == 1
    assert data_v["new_max_quota"] == 4

    db_session.refresh(org)
    assert org.ad_bonus_vehicles == 1
    assert org.max_vehicles == 4

    # Watch rewarded ad for driver slot
    token_d = "ad_token_drv_001"
    sig_d = generate_admob_ssv_signature(token_d, "driver_slot", org.id)
    reward_d_payload = {
        "organization_id": org.id,
        "reward_type": "driver_slot",
        "admob_ssv_token": token_d,
        "signature": sig_d,
    }
    res_d = client.post("/api/v1/ads/verify-reward", json=reward_d_payload, headers=headers)
    assert res_d.status_code == 200, res_d.text
    data_d = res_d.json()
    assert data_d["new_ad_bonus_slots"] == 1
    assert data_d["new_max_quota"] == 4

    db_session.refresh(org)
    assert org.ad_bonus_drivers == 1
    assert org.max_drivers == 4
    db_session.close()


def test_uc122_ad_gate_signature_forgery_rejection():
    """UC-122: Ad-Gate Signature Forgery & Token Replay Prevention"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "adgate_test@example.com", "AdGate Org")

    # Invalid signature forgery
    payload_forged = {
        "organization_id": org.id,
        "reward_type": "vehicle_slot",
        "admob_ssv_token": "token_hack",
        "signature": "fake_signature_123",
    }
    res_forged = client.post("/api/v1/ads/verify-reward", json=payload_forged, headers=headers)
    assert res_forged.status_code == 400
    assert "INVALID_AD_SIGNATURE" in res_forged.json()["detail"]

    # Replay attack (reuse token)
    token = "token_valid_once"
    sig = generate_admob_ssv_signature(token, "vehicle_slot", org.id)
    valid_payload = {
        "organization_id": org.id,
        "reward_type": "vehicle_slot",
        "admob_ssv_token": token,
        "signature": sig,
    }
    res_1 = client.post("/api/v1/ads/verify-reward", json=valid_payload, headers=headers)
    assert res_1.status_code == 200

    # Second request with same token must fail
    res_replay = client.post("/api/v1/ads/verify-reward", json=valid_payload, headers=headers)
    assert res_replay.status_code == 400
    assert "AD_TOKEN_ALREADY_USED" in res_replay.json()["detail"]
    db_session.close()


def test_uc089_enterprise_sales_inquiry_submission():
    """UC-089: Contact Enterprise Sales Inquiry Submission (>25 Fleets)"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "enterprise_inquiry@example.com", "Enterprise Org")

    inquiry_payload = {
        "organization_id": org.id,
        "contact_name": "Enterprise Fleet Lead",
        "email": "lead@enterprisefleet.com",
        "phone": "+923009998877",
        "fleet_size": 150,
        "message": "We have 150 heavy trucks operating across provinces.",
    }

    res = client.post("/api/v1/ads/enterprise-inquiry", json=inquiry_payload, headers=headers)
    assert res.status_code == 200, res.text
    data = res.json()
    assert "inquiry_id" in data
    assert data["status"] == "submitted"

    # Check AuditLog entry created
    audit = db_session.query(AuditLog).filter_by(action="ENTERPRISE_SALES_INQUIRY").first()
    assert audit is not None
    assert audit.organization_id == org.id
    db_session.close()


def test_uc101_pro_tier_ad_suppression_logic():
    """UC-101: Render Ad-Free Experience & Unlimited Quota for Pro Subscribers"""
    db_session = TestingSessionLocal()
    user, org, headers = create_test_user_and_org(db_session, "pro_adfree@example.com", "Pro AdFree Org")

    org.tier = "pro"
    org.max_vehicles = 25
    org.max_drivers = 15
    db_session.commit()

    # Pro tier org can add vehicles up to 25 without quota wall
    for i in range(1, 6):
        v_payload = {
            "organization_id": org.id,
            "name": f"Pro Vehicle {i}",
            "make": "Volvo",
            "model": "FH16",
            "year": 2024,
            "vin": f"VIN9000000000000{i}",
            "license_plate": f"PRO-00{i}",
        }
        res = client.post("/api/v1/vehicles", json=v_payload, headers=headers)
        assert res.status_code == 201
    db_session.close()
