"""Validator for IaC plans (mocked)."""
from __future__ import annotations

from backend.models import FixPlan
from backend.utils.logging_utils import get_logger

LOGGER = get_logger(__name__)


def validate_fix(plan: FixPlan) -> bool:
    """Simulate validation of IaC plan and update flag."""
    LOGGER.info("Validating fix plan at %s", plan.output_path)
    if not plan.content.strip():
        LOGGER.error("Fix plan is empty")
        plan.validation_passed = False
        return False
    plan.validation_passed = True
    return plan.validation_passed
