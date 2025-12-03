"""Simulated Azure connector."""
from __future__ import annotations

from typing import Any

from backend.types import CloudConnector
from backend.utils.logging_utils import get_logger

LOGGER = get_logger(__name__)


class AzureMockConnector(CloudConnector):
    """Mock Azure connector that returns deterministic resources."""

    def __init__(self) -> None:
        self.resources: list[dict[str, Any]] = [
            {"id": "blob-001", "name": "public-container", "type": "blob"},
            {"id": "func-001", "name": "legacy-function", "type": "function"},
        ]

    def list_resources(self) -> list[dict[str, Any]]:
        """Return predefined Azure resources for simulation."""

        return self.resources

    def get_config(self, resource_id: str) -> dict[str, Any]:
        """Return a configuration map for the requested resource."""

        if resource_id == "blob-001":
            return {"public": True, "unencrypted": True, "missing_mfa": True}
        if resource_id == "func-001":
            return {"lambda_runtime_vulnerable": True}
        return {}

    def apply_change(self, change: dict[str, Any]) -> None:
        """Log the simulated change for auditability."""

        LOGGER.info("Azure change applied (simulated): %s", change)

    def simulate_failure(self) -> bool:
        """Return False to keep simulations deterministic for tests."""

        return False
