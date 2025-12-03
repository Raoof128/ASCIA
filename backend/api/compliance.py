"""Compliance endpoints."""
from __future__ import annotations

from fastapi import APIRouter

from backend.app_state import AGENT

router = APIRouter()


@router.get("/compliance", response_model=dict)
async def compliance_overview() -> dict:
    """Return compliance mapping and risk score."""
    issues = AGENT.detector.detect()
    mapping = AGENT.compliance_engine.map_to_controls(issues)
    score = AGENT.compliance_engine.risk_score(issues)
    return {"mapping": mapping, "risk_score": score, "issue_count": len(issues)}
