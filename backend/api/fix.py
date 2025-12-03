"""Fix generation endpoints."""
from __future__ import annotations

import glob
from pathlib import Path

from fastapi import APIRouter

from backend.app_state import AGENT
from backend.models import FixPlan, Issue
from backend.utils.logging_utils import get_logger

router = APIRouter()
LOGGER = get_logger(__name__)


def load_latest_fix() -> FixPlan | None:
    """Return the most recent IaC fix plan stored on disk."""
    try:
        files = sorted(glob.glob("iac_versions/*.tf"))
        if not files:
            return None
        path = Path(files[-1])
        content = path.read_text(encoding="utf-8")
        return FixPlan(
            tool="terraform", content=content, validation_passed=True, output_path=str(path)
        )
    except OSError as exc:  # pragma: no cover - defensive
        LOGGER.error("Unable to load latest fix: %s", exc)
        return None


@router.post("/fix", response_model=FixPlan)
async def generate_fix(issues: list[Issue]) -> FixPlan:
    """Generate and validate a fix for supplied issues."""
    plan = AGENT.fix_generator.generate(issues)
    return plan


@router.get("/fix/latest", response_model=FixPlan | None)
async def latest_fix() -> FixPlan | None:
    """Return the latest generated IaC file content if present."""
    return load_latest_fix()
