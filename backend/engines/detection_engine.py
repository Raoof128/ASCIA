"""Simulated detection engine for cloud misconfigurations."""
from __future__ import annotations

from backend.models import Issue, Severity
from backend.types import CloudConnector
from backend.utils.logging_utils import get_logger

LOGGER = get_logger(__name__)


class DetectionEngine:
    """Detects misconfigurations from simulated cloud connectors."""

    def __init__(self, connectors: dict[str, CloudConnector]):
        self.connectors = connectors

    def detect(self) -> list[Issue]:
        """Run detection across connectors and return issues."""
        issues: list[Issue] = []
        for name, connector in self.connectors.items():
            LOGGER.info("Scanning connector %s", name)
            if hasattr(connector, "simulate_failure") and connector.simulate_failure():
                LOGGER.warning("Skipping %s scan due to simulated failure", name)
                continue
            try:
                resources = connector.list_resources()
            except Exception as exc:  # pragma: no cover - defensive
                LOGGER.error("Failed to list resources for %s: %s", name, exc)
                continue

            for resource in resources:
                try:
                    config = connector.get_config(resource["id"])
                except Exception as exc:  # pragma: no cover - defensive
                    LOGGER.error(
                        "Failed to get config for %s:%s: %s",
                        name,
                        resource.get("id"),
                        exc,
                    )
                    continue
                issues.extend(self._evaluate_resource(name, resource, config))
        return issues

    def _evaluate_resource(
        self, provider: str, resource: dict[str, str], config: dict[str, object]
    ) -> list[Issue]:
        """Evaluate resource config against simulated rules."""
        detected: list[Issue] = []
        if config.get("public", False):
            detected.append(
                Issue(
                    issue_type="Publicly exposed storage",
                    severity=Severity.CRITICAL,
                    resource={"provider": provider, **resource},
                    recommended_fix="Enable private access and block public ACLs/policies.",
                )
            )
        if config.get("unencrypted", False):
            detected.append(
                Issue(
                    issue_type="Unencrypted storage",
                    severity=Severity.HIGH,
                    resource={"provider": provider, **resource},
                    recommended_fix="Enable default encryption using KMS-managed keys.",
                )
            )
        if config.get("open_ports"):
            detected.append(
                Issue(
                    issue_type="Exposed network ports",
                    severity=Severity.HIGH,
                    resource={"provider": provider, **resource},
                    recommended_fix="Restrict security group ingress to trusted CIDRs only.",
                )
            )
        if config.get("iam_escalation"):
            detected.append(
                Issue(
                    issue_type="IAM privilege escalation risk",
                    severity=Severity.CRITICAL,
                    resource={"provider": provider, **resource},
                    recommended_fix=(
                        "Replace wildcard IAM roles with least privilege policies and require MFA."
                    ),
                )
            )
        if config.get("missing_mfa"):
            detected.append(
                Issue(
                    issue_type="Missing MFA",
                    severity=Severity.MEDIUM,
                    resource={"provider": provider, **resource},
                    recommended_fix="Enforce MFA for console and API usage.",
                )
            )
        if config.get("kms_misconfigured"):
            detected.append(
                Issue(
                    issue_type="Misconfigured KMS keys",
                    severity=Severity.MEDIUM,
                    resource={"provider": provider, **resource},
                    recommended_fix=(
                        "Rotate KMS keys and enforce key policies aligned with least privilege."
                    ),
                )
            )
        if config.get("lambda_runtime_vulnerable"):
            detected.append(
                Issue(
                    issue_type="Vulnerable runtime",
                    severity=Severity.HIGH,
                    resource={"provider": provider, **resource},
                    recommended_fix="Upgrade runtime to a patched LTS version and retest.",
                )
            )
        return detected
