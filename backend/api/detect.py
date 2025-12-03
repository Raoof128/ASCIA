"""Detection API endpoints."""
from __future__ import annotations

from fastapi import APIRouter

from backend.app_state import AGENT
from backend.models import Alert, Issue

router = APIRouter()


@router.get("/issues", response_model=list[Issue])
async def list_issues() -> list[Issue]:
    """Return currently detected misconfigurations."""
    return AGENT.detector.detect()


@router.post("/alert", response_model=dict)
async def receive_alert(alert: Alert) -> dict:
    """Receive an alert and echo with acknowledgement."""
    return {"received": True, "alert": alert}
