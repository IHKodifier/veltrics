import sys
import os
import pytest
from datetime import date, timedelta
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
from app.models.organization import Organization
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.maintenance import MaintenanceSchedule, ServiceRecord
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
def dashboard_setup(client):
    db = TestingSessionLocal()
    org1 = Organization(name="Org One", is_personal=False)
    org2 = Organization(name="Org Two", is_personal=False)
    empty_org = Organization(name="Empty Org", is_personal=False)
    db.add_all([org1, org2, empty_org])
    db.commit()

    # Org1: 2 Vehicles
    v1 = Vehicle(
        organization_id=org1.id,
        license_plate="ORG1-V1",
        make="Toyota",
        model="Corolla",
        year=2022,
        current_odometer_km=10000.0,
        status="ACTIVE"
    )
    v2 = Vehicle(
        organization_id=org1.id,
        license_plate="ORG1-V2",
        make="Honda",
        model="Civic",
        year=2023,
        current_odometer_km=25000.0,
        status="ACTIVE"
    )
    db.add_all([v1, v2])

    # Org2: 1 Vehicle
    v_org2 = Vehicle(
        organization_id=org2.id,
        license_plate="ORG2-V1",
        make="Suzuki",
        model="Alto",
        year=2021,
        current_odometer_km=5000.0,
        status="ACTIVE"
    )
    db.add(v_org2)
    db.commit()

    # Drivers: 2 for Org1, 1 for Org2
    d1 = Driver(organization_id=org1.id, full_name="Driver One", status="ACTIVE")
    d2 = Driver(organization_id=org1.id, full_name="Driver Two", status="ACTIVE")
    d3 = Driver(organization_id=org2.id, full_name="Driver Three", status="ACTIVE")
    db.add_all([d1, d2, d3])

    # Maintenance Schedules for Org1:
    # 1. Upcoming (due in 4 days, or within 500 km)
    sched_upcoming = MaintenanceSchedule(
        organization_id=org1.id,
        vehicle_id=v1.id,
        task_name="Tire Rotation",
        interval_km=5000,
        interval_days=90,
        last_performed_km=6000.0,
        last_performed_date=date.today() - timedelta(days=86),
        next_due_km=10200.0,  # 200 km remaining (within 500 km)
        next_due_date=date.today() + timedelta(days=4), # 4 days away
        is_active=True
    )
    # 2. Overdue (due 5 days ago)
    sched_overdue = MaintenanceSchedule(
        organization_id=org1.id,
        vehicle_id=v2.id,
        task_name="Brake Inspection",
        interval_km=10000,
        interval_days=180,
        last_performed_km=10000.0,
        last_performed_date=date.today() - timedelta(days=185),
        next_due_km=20000.0,  # current is 25000 km -> overdue by km!
        next_due_date=date.today() - timedelta(days=5),
        is_active=True
    )
    db.add_all([sched_upcoming, sched_overdue])

    # Service Records for Org1:
    # Current month record = 7500.0
    # Past month record = 3000.0
    today = date.today()
    first_of_month = date(today.year, today.month, 1)
    past_month_date = first_of_month - timedelta(days=15)

    rec1 = ServiceRecord(
        organization_id=org1.id,
        vehicle_id=v1.id,
        service_date=first_of_month,
        odometer_km=10000.0,
        total_cost=7500.0,
        notes="Current month service"
    )
    rec2 = ServiceRecord(
        organization_id=org1.id,
        vehicle_id=v1.id,
        service_date=past_month_date,
        odometer_km=9000.0,
        total_cost=3000.0,
        notes="Past month service"
    )
    # Org2 Service Record = 12000.0
    rec_org2 = ServiceRecord(
        organization_id=org2.id,
        vehicle_id=v_org2.id,
        service_date=first_of_month,
        odometer_km=5000.0,
        total_cost=12000.0,
        notes="Org 2 service"
    )
    db.add_all([rec1, rec2, rec_org2])
    db.commit()

    org1_id = org1.id
    org2_id = org2.id
    empty_org_id = empty_org.id
    db.close()

    return {
        "org1_id": org1_id,
        "org2_id": org2_id,
        "empty_org_id": empty_org_id,
    }

def test_get_dashboard_summary_metrics(client, dashboard_setup):
    """
    UC-064: GET /api/v1/dashboard/summary calculates total_vehicles, total_drivers,
    monthly_total_cost, upcoming_maintenance_count, and overdue_maintenance_count accurately.
    """
    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"X-Organization-ID": dashboard_setup["org1_id"]}
    )
    assert response.status_code == 200
    data = response.json()

    assert data["total_vehicles"] == 2
    assert data["total_drivers"] == 2
    assert data["monthly_total_cost"] == 7500.0
    assert data["upcoming_maintenance_count"] == 1
    assert data["overdue_maintenance_count"] == 1

def test_dashboard_tenant_isolation(client, dashboard_setup):
    """
    UC-064: Requests for Org 2 return only Org 2's metrics.
    """
    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"X-Organization-ID": dashboard_setup["org2_id"]}
    )
    assert response.status_code == 200
    data = response.json()

    assert data["total_vehicles"] == 1
    assert data["total_drivers"] == 1
    assert data["monthly_total_cost"] == 12000.0
    assert data["upcoming_maintenance_count"] == 0
    assert data["overdue_maintenance_count"] == 0

def test_dashboard_empty_organization(client, dashboard_setup):
    """
    UC-064: Empty organization returns 0 stats so client can render onboarding card.
    """
    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"X-Organization-ID": dashboard_setup["empty_org_id"]}
    )
    assert response.status_code == 200
    data = response.json()

    assert data["total_vehicles"] == 0
    assert data["total_drivers"] == 0
    assert data["monthly_total_cost"] == 0.0
    assert data["upcoming_maintenance_count"] == 0
    assert data["overdue_maintenance_count"] == 0

def test_dashboard_missing_header_rejected(client):
    """
    UC-064: GET /api/v1/dashboard/summary returns 400 if X-Organization-ID is missing.
    """
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 400
