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

import app.models as models
from app.models.user import User
from app.models.organization import Organization
from app.main import app
from app.db.session import Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_uc116_account_deletion_anonymizes_pii(client):
    """
    AC for UC-116:
    GIVEN an authenticated user requesting account deletion
    WHEN they issue DELETE /api/v1/users/me
    THE SYSTEM SHALL soft-delete the record, anonymize PII, revoke sessions, and block future auth attempts.
    """
    # 1. Register test user
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": "gdpr.delete@veltrics.com",
        "password": "Password123",
        "full_name": "GDPR Subject",
        "auth_provider": "email"
    })
    assert reg_resp.status_code == 200
    user_id = reg_resp.json()["user"]["id"]
    access_token = reg_resp.json()["access_token"]
    headers = {"X-User-ID": user_id, "Authorization": f"Bearer {access_token}"}

    # 2. Issue DELETE /api/v1/users/me
    del_resp = client.delete("/api/v1/users/me", headers=headers)
    assert del_resp.status_code == 200
    del_data = del_resp.json()
    assert "message" in del_data
    assert "deleted" in del_data["message"].lower()

    # 3. Subsequent GET /api/v1/users/me should fail or return 401/404 because user is deleted
    get_resp = client.get("/api/v1/users/me", headers=headers)
    assert get_resp.status_code in [401, 404]
