import sys
import os
import pytest
import io
from fastapi.testclient import TestClient

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_ocr_scan_receipt_success(client):
    fake_image_bytes = b"Shell Gas Station Receipt\nDate: 2026-08-13\nLiters: 45.0 L\nTotal: $112.50\nPrice/L: $2.50"
    files = {"file": ("receipt.jpg", io.BytesIO(fake_image_bytes), "image/jpeg")}

    r = client.post("/api/v1/fuel/ocr-scan", files=files)
    assert r.status_code == 200
    data = r.json()
    assert "total_cost" in data
    assert "quantity_liters" in data
    assert "station_name" in data
    assert "confidence_score" in data
    assert data["confidence_score"] > 0.0
