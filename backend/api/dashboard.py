"""Dashboard endpoint to aggregate agent data."""
from __future__ import annotations

from fastapi import APIRouter

from backend.api.fix import load_latest_fix
from backend.app_state import AGENT

router = APIRouter()


@router.get("/dashboard", response_model=dict)
async def dashboard() -> dict:
    """Return aggregated dashboard information."""
    issues = AGENT.detector.detect()
    risk_score = AGENT.compliance_engine.risk_score(issues)
    compliance = AGENT.compliance_engine.map_to_controls(issues)
    latest_fix = load_latest_fix()
    return {
        "issues": [issue.model_dump() for issue in issues],
        "risk_score": risk_score,
        "compliance": compliance,
        "latest_fix": latest_fix.model_dump() if latest_fix else None,
    }
