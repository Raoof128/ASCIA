"""Shared typing primitives for connectors and engines."""
from __future__ import annotations

from typing import Any, Protocol


class CloudConnector(Protocol):
    """Protocol describing required connector behaviours."""

    def list_resources(self) -> list[dict[str, Any]]:
        """Return a deterministic list of resources available to scan."""

    def get_config(self, resource_id: str) -> dict[str, Any]:
        """Return a configuration dictionary for a given resource identifier."""

    def apply_change(self, change: dict[str, Any]) -> None:
        """Apply a simulated change to the resource configuration."""

    def simulate_failure(self) -> bool:
        """Indicate whether the connector should simulate a failure state."""

