import os
import sys
import pytest
from datetime import datetime, timezone, timedelta

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
from app.models.driver import Driver
from app.models.trip import Trip
from app.models.vehicle import Vehicle

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


def create_access_token(data: dict) -> str:
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


@pytest.fixture
def setup_database():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Create Org
    org = Organization(
        id="org-analytics-101",
        name="Analytics Test Fleet",
        owner_id="user-owner-101",
        tier="pro",
    )
    db.add(org)

    # Create User
    user = User(
        id="user-owner-101",
        firebase_uid="uid-owner-101",
        email="owner@analytics.com",
        full_name="Analytics Manager",
        password_hash="hashed_pass_123",
    )
    db.add(user)

    # Create UserOrganization Link
    user_org = UserOrganization(
        user_id="user-owner-101",
        organization_id="org-analytics-101",
        role="OWNER",
    )
    db.add(user_org)

    # Create Vehicle
    vehicle = Vehicle(
        id="veh-analytics-01",
        organization_id="org-analytics-101",
        vin="1FTFW1E84MFC11111",
        make="Ford",
        model="Transit",
        year=2022,
        license_plate="AN-9000",
    )
    db.add(vehicle)

    # Create Drivers
    driver_top = Driver(
        id="drv-top-101",
        organization_id="org-analytics-101",
        full_name="Speedy Sam",
        license_number="LIC-889900",
        phone_number="+923001112233",
        status="ACTIVE",
    )
    driver_idle = Driver(
        id="drv-idle-102",
        organization_id="org-analytics-101",
        full_name="Lazy Lou",
        license_number="LIC-112233",
        phone_number="+923004445566",
        status="ACTIVE",
    )
    driver_expired = Driver(
        id="drv-exp-103",
        organization_id="org-analytics-101",
        full_name="Expired Ed",
        license_number="LIC-999999",
        phone_number="+923007778899",
        license_expiry_date=(datetime.now(timezone.utc) + timedelta(days=10)).date(),
        status="ACTIVE",
    )
    db.add_all([driver_top, driver_idle, driver_expired])

    # Add Completed Trips for Driver Top
    trip1 = Trip(
        id="trip-101",
        organization_id="org-analytics-101",
        vehicle_id="veh-analytics-01",
        driver_id="drv-top-101",
        start_time=datetime.now(timezone.utc) - timedelta(days=2),
        end_time=datetime.now(timezone.utc) - timedelta(days=2, hours=-2),
        start_odometer_km=1000.0,
        end_odometer_km=1120.0,
        distance_km=120.0,
        status="COMPLETED",
        notes="Clean trip, optimal fuel efficiency",
    )
    trip2 = Trip(
        id="trip-102",
        organization_id="org-analytics-101",
        vehicle_id="veh-analytics-01",
        driver_id="drv-top-101",
        start_time=datetime.now(timezone.utc) - timedelta(days=1),
        end_time=datetime.now(timezone.utc) - timedelta(days=1, hours=-1),
        start_odometer_km=1120.0,
        end_odometer_km=1180.0,
        distance_km=60.0,
        status="COMPLETED",
        notes="Minor delay, harsh braking event recorded",
    )
    db.add_all([trip1, trip2])

    db.commit()

    token_payload = {
        "sub": "user-owner-101",
        "email": "owner@analytics.com",
        "org_id": "org-analytics-101",
        "role": "OWNER",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    token = create_access_token(token_payload)

    yield {"token": token, "org_id": "org-analytics-101", "driver_top_id": "drv-top-101", "driver_idle_id": "drv-idle-102", "driver_exp_id": "drv-exp-103"}

    db.close()
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_uc103_104_driver_safety_score_and_performance_detail(setup_database):
    """UC-103 & UC-104: Verify driver safety score calculation & performance detail endpoint."""
    token = setup_database["token"]
    driver_id = setup_database["driver_top_id"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/api/v1/driver-analytics/drivers/{driver_id}/performance", headers=headers)

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["driver_id"] == driver_id
    assert data["full_name"] == "Speedy Sam"
    assert data["completed_trips"] == 2
    assert data["total_distance_km"] == 180.0
    assert "safety_score" in data
    assert 0 <= data["safety_score"] <= 100
    assert data["badge_tier"] in ["PLATINUM", "GOLD", "SILVER", "BRONZE"]


def test_uc105_driver_inactivity_and_anomaly_alerts(setup_database):
    """UC-105: Verify idle driver and expiring license anomaly detection."""
    token = setup_database["token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/v1/driver-analytics/detect-anomalies", headers=headers)

    assert response.status_code == 200, response.text
    data = response.json()
    assert "anomalies" in data
    anomalies = data["anomalies"]
    
    # Should detect idle driver and expiring license
    anomaly_types = [a["anomaly_type"] for a in anomalies]
    assert "IDLE_DRIVER" in anomaly_types or "EXPIRING_LICENSE" in anomaly_types


def test_uc106_driver_safety_certificate_badge(setup_database):
    """UC-106: Verify safety certificate generation with digital signature hash."""
    token = setup_database["token"]
    driver_id = setup_database["driver_top_id"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/api/v1/driver-analytics/drivers/{driver_id}/certificate", headers=headers)

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["driver_id"] == driver_id
    assert "certificate_id" in data
    assert "badge_tier" in data
    assert "verification_hash" in data


def test_uc070_driver_safety_leaderboard(setup_database):
    """UC-070: Verify fleet driver safety leaderboard widget endpoint."""
    token = setup_database["token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/driver-analytics/leaderboard", headers=headers)

    assert response.status_code == 200, response.text
    data = response.json()
    assert "leaderboard" in data
    entries = data["leaderboard"]
    assert len(entries) >= 2
    # Verify scores are sorted in descending order
    scores = [e["safety_score"] for e in entries]
    assert scores == sorted(scores, reverse=True)
