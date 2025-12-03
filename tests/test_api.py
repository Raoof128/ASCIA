"""API-level tests using FastAPI's TestClient."""
from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_agent_run_endpoint_returns_decisions():
    payload = {"id": "alert-1", "issue_type": "Publicly exposed storage"}
    response = client.post("/run_agent", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["validated"] is True
    assert data["issues"], "Expected detected issues"
    assert any(decision["step"] == "apply_fix" for decision in data["decisions"])


def test_dashboard_contains_latest_fix():
    # Trigger a fix to ensure a plan exists
    payload = {"id": "alert-2", "issue_type": "Publicly exposed storage"}
    client.post("/run_agent", json=payload)
    response = client.get("/dashboard")
    assert response.status_code == 200
    body = response.json()
    assert "issues" in body
    # latest_fix may be null before first run; ensure dashboard returns the field
    assert "latest_fix" in body
