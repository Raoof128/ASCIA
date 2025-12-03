"""Simulated AWS connector that avoids real cloud interactions."""
from __future__ import annotations

from typing import Any

from backend.types import CloudConnector
from backend.utils.logging_utils import get_logger

LOGGER = get_logger(__name__)


class AWSMockConnector(CloudConnector):
    """Mock AWS connector with deterministic resources."""

    def __init__(self) -> None:
        self.resources: list[dict[str, Any]] = [
            {"id": "s3-001", "name": "open-bucket", "type": "s3"},
            {"id": "sg-001", "name": "web-sg", "type": "security_group"},
        ]

    def list_resources(self) -> list[dict[str, Any]]:
        """Return predefined AWS resources for simulation."""

        return self.resources

    def get_config(self, resource_id: str) -> dict[str, Any]:
        """Return a configuration map for the requested resource."""

        if resource_id == "s3-001":
            return {"public": True, "unencrypted": True}
        if resource_id == "sg-001":
            return {"open_ports": [22, 80], "iam_escalation": True}
        return {}

    def apply_change(self, change: dict[str, Any]) -> None:
        """Log the simulated change for auditability."""

        LOGGER.info("AWS change applied (simulated): %s", change)

    def simulate_failure(self) -> bool:
        """Return False to keep simulations deterministic for tests."""

        return False
