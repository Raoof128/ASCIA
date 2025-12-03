"""Simulated GCP connector."""
from __future__ import annotations

from typing import Any

from backend.types import CloudConnector
from backend.utils.logging_utils import get_logger

LOGGER = get_logger(__name__)


class GCPMockConnector(CloudConnector):
    """Mock GCP connector that returns deterministic resources."""

    def __init__(self) -> None:
        self.resources: list[dict[str, Any]] = [
            {"id": "bucket-001", "name": "open-gcs", "type": "gcs"},
            {"id": "kms-001", "name": "weak-kms", "type": "kms"},
        ]

    def list_resources(self) -> list[dict[str, Any]]:
        """Return predefined GCP resources for simulation."""

        return self.resources

    def get_config(self, resource_id: str) -> dict[str, Any]:
        """Return a configuration map for the requested resource."""

        if resource_id == "bucket-001":
            return {"public": True}
        if resource_id == "kms-001":
            return {"kms_misconfigured": True}
        return {}

    def apply_change(self, change: dict[str, Any]) -> None:
        """Log the simulated change for auditability."""

        LOGGER.info("GCP change applied (simulated): %s", change)

    def simulate_failure(self) -> bool:
        """Return False to keep simulations deterministic for tests."""

        return False
