import os
import sys
import pytest
from datetime import datetime, timezone, timedelta, date

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
from app.models.maintenance import ServiceRecord
from app.models.fuel_log import FuelLog

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
        id="org-mgr-301",
        name="Manager Dashboard Fleet",
        owner_id="user-mgr-301",
        tier="pro",
    )
    db.add(org)

    # Create User
    user = User(
        id="user-mgr-301",
        firebase_uid="uid-mgr-301",
        email="mgr@dashfleet.com",
        full_name="Fleet Manager",
        password_hash="hashed_pass_123",
    )
    db.add(user)

    # Create UserOrganization Link
    user_org = UserOrganization(
        user_id="user-mgr-301",
        organization_id="org-mgr-301",
        role="OWNER",
    )
    db.add(user_org)

    # Create Vehicles
    veh1 = Vehicle(
        id="veh-mgr-01",
        organization_id="org-mgr-301",
        vin="1FTFW1E84MFC33333",
        make="Ford",
        model="F-150",
        year=2022,
        license_plate="MGR-101",
        status="ACTIVE",
        current_odometer_km=50000.0,
    )
    veh2 = Vehicle(
        id="veh-mgr-02",
        organization_id="org-mgr-301",
        vin="1FTFW1E84MFC44444",
        make="Isuzu",
        model="NPR Truck",
        year=2021,
        license_plate="MGR-202",
        status="MAINTENANCE",
        current_odometer_km=80000.0,
    )
    db.add_all([veh1, veh2])

    # Create Service Records & Fuel Logs
    record1 = ServiceRecord(
        id="rec-mgr-01",
        organization_id="org-mgr-301",
        vehicle_id="veh-mgr-01",
        service_date=date.today(),
        odometer_km=50000.0,
        total_cost=300.0,
        service_center_name="Speedy Repair",
    )
    fuel1 = FuelLog(
        id="fuel-mgr-01",
        organization_id="org-mgr-301",
        vehicle_id="veh-mgr-02",
        log_date=datetime.now(timezone.utc),
        odometer_km=80000.0,
        quantity_liters=60.0,
        total_cost=180.0,
    )
    db.add_all([record1, fuel1])

    db.commit()

    token_payload = {
        "sub": "user-mgr-301",
        "email": "mgr@dashfleet.com",
        "org_id": "org-mgr-301",
        "role": "OWNER",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    token = create_access_token(token_payload)

    yield {
        "token": token,
        "org_id": "org-mgr-301",
        "veh1_id": "veh-mgr-01",
        "veh2_id": "veh-mgr-02",
    }

    db.close()
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_uc067_fleet_manager_kpi_aggregation(setup_database):
    """UC-067: Verify Fleet Manager Web Dashboard KPI Aggregation."""
    token = setup_database["token"]
    org_id = setup_database["org_id"]
    headers = {"Authorization": f"Bearer {token}", "X-Organization-ID": org_id}

    response = client.get("/api/v1/dashboard/manager", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["total_vehicles"] == 2
    assert data["active_vehicles"] == 1
    assert data["maintenance_vehicles"] == 1
    assert "availability_percentage" in data
    assert data["monthly_fuel_cost"] >= 0.0
    assert data["monthly_maintenance_cost"] >= 0.0


def test_uc068_fleet_cost_ranking_table(setup_database):
    """UC-068: Verify Fleet Cost Ranking Table & Heatmap endpoint."""
    token = setup_database["token"]
    org_id = setup_database["org_id"]
    headers = {"Authorization": f"Bearer {token}", "X-Organization-ID": org_id}

    response = client.get("/api/v1/dashboard/cost-ranking", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()

    assert "rankings" in data
    rankings = data["rankings"]
    assert len(rankings) == 2
    # Verify rankings are sorted by total cost descending
    assert rankings[0]["total_cost"] >= rankings[1]["total_cost"]


def test_uc069_vehicle_availability_widget(setup_database):
    """UC-069: Verify Fleet Vehicle Availability Widget endpoint."""
    token = setup_database["token"]
    org_id = setup_database["org_id"]
    headers = {"Authorization": f"Bearer {token}", "X-Organization-ID": org_id}

    response = client.get("/api/v1/dashboard/vehicle-availability", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["total_vehicles"] == 2
    assert data["available_count"] == 1
    assert data["maintenance_count"] == 1
    assert data["availability_percentage"] == 50.0


def test_uc071_customize_dashboard_layout(setup_database):
    """UC-071: Verify customizing & saving dashboard widget layout preferences."""
    token = setup_database["token"]
    headers = {"Authorization": f"Bearer {token}"}

    layout_payload = {
        "widgets": [
            {"widget_id": "kpi_cards", "visible": True, "position": 1},
            {"widget_id": "cost_ranking", "visible": True, "position": 2},
            {"widget_id": "availability", "visible": False, "position": 3},
        ]
    }

    save_resp = client.put("/api/v1/dashboard/layout", json=layout_payload, headers=headers)
    assert save_resp.status_code == 200, save_resp.text

    get_resp = client.get("/api/v1/dashboard/layout", headers=headers)
    assert get_resp.status_code == 200, get_resp.text
    saved_layout = get_resp.json()
    assert len(saved_layout["widgets"]) == 3
    assert saved_layout["widgets"][0]["widget_id"] == "kpi_cards"
