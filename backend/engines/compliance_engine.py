"""Compliance and governance simulation layer."""
from __future__ import annotations

from backend.models import Issue
from backend.utils.logging_utils import get_logger

LOGGER = get_logger(__name__)

ESSENTIAL_EIGHT_CONTROLS = [
    "Application control",
    "Patch applications",
    "Configure Microsoft Office macro settings",
    "User application hardening",
    "Restrict administrative privileges",
    "Patch operating systems",
    "Multi-factor authentication",
    "Daily backups",
]


class ComplianceEngine:
    """Maps issues to simulated compliance frameworks."""

    def map_to_controls(self, issues: list[Issue]) -> dict[str, list[str]]:
        """Return a mapping of frameworks to the relevant controls for given issues."""
        mapping: dict[str, set[str]] = {
            "ACSC Essential Eight": set(),
            "SOCI Act": set(),
            "ISO/IEC 42001": set(),
        }
        for issue in issues:
            if issue.issue_type in ("Publicly exposed storage", "Unencrypted storage"):
                mapping["SOCI Act"].add("Protect critical infrastructure data")
                mapping["ISO/IEC 42001"].add("Information security risk treatment")
            if issue.issue_type == "Missing MFA":
                mapping["ACSC Essential Eight"].add("Multi-factor authentication")
            if issue.issue_type == "IAM privilege escalation risk":
                mapping["ACSC Essential Eight"].add("Restrict administrative privileges")
            if issue.issue_type == "Exposed network ports":
                mapping["SOCI Act"].add("Network exposure minimized")
            if issue.issue_type == "Vulnerable runtime":
                mapping["ISO/IEC 42001"].add("Secure development lifecycle")
        serialized = {key: sorted(value) for key, value in mapping.items()}
        LOGGER.info("Compliance mapping complete: %s", serialized)
        return serialized

    def risk_score(self, issues: list[Issue]) -> int:
        """Compute a simple risk score based on severity."""
        severity_weights = {"low": 1, "medium": 3, "high": 6, "critical": 10}
        return sum(severity_weights[issue.severity.value] for issue in issues)
