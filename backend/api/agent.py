"""Agent execution endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app_state import AGENT
from backend.models import AgentRunResult, Alert

router = APIRouter()


@router.post("/run_agent", response_model=AgentRunResult)
async def run_agent(alert: Alert) -> AgentRunResult:
    """Trigger the autonomous agent for a given alert."""
    if not alert:
        raise HTTPException(status_code=400, detail="Alert payload required")
    result = AGENT.run(alert)
    if not result.validated:
        raise HTTPException(status_code=400, detail="Invalid alert payload; remediation aborted")
    return result
