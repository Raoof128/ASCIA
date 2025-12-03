"""Autonomous self-healing agent orchestrating detection and remediation."""
from __future__ import annotations

from typing import Any

from backend.engines.compliance_engine import ComplianceEngine
from backend.engines.detection_engine import DetectionEngine
from backend.engines.fix_generator import FixGenerator
from backend.engines.validator import validate_fix
from backend.models import AgentDecision, AgentRunResult, Alert, FixPlan, Issue
from backend.types import CloudConnector
from backend.utils.logging_utils import get_logger

LOGGER = get_logger(__name__)


class SelfHealingAgent:
    """LangGraph-style agent with reflection and tool loops."""

    def __init__(self, connectors: dict[str, CloudConnector]):
        self.connectors = connectors
        self.detector = DetectionEngine(connectors)
        self.fix_generator = FixGenerator()
        self.compliance_engine = ComplianceEngine()

    def run(self, alert: Alert | dict[str, Any]) -> AgentRunResult:
        """Execute the full remediation flow for a given alert."""
        decisions: list[AgentDecision] = []
        alert_payload = alert.model_dump() if isinstance(alert, Alert) else alert

        decisions.append(
            AgentDecision(step="receive_alert", detail="Alert received", metadata=alert_payload)
        )
        validated = self._validate_alert(alert_payload, decisions)
        if not validated:
            decisions.append(
                AgentDecision(
                    step="abort",
                    detail="Alert failed validation; skipping remediation",
                    success=False,
                )
            )
            return AgentRunResult(
                alert=alert if isinstance(alert, Alert) else Alert(**alert_payload),
                validated=False,
                remediation_applied=False,
                decisions=decisions,
                generated_fix=None,
                issues=[],
                compliance_notes={},
                ticket_update=self._update_ticket(alert, [], False),
            )
        issues = self.detector.detect()
        decisions.append(
            AgentDecision(
                step="detection",
                detail=f"Detected {len(issues)} issues",
                metadata={"count": len(issues)},
            )
        )

        remediation_possible = bool(issues)
        decisions.append(
            AgentDecision(
                step="decision",
                detail=(
                    "Remediation possible" if remediation_possible else "No remediation required"
                ),
                success=remediation_possible,
            )
        )

        generated_fix = None
        remediation_applied = False
        if remediation_possible:
            generated_fix = self.fix_generator.generate(issues)
            valid = validate_fix(generated_fix)
            decisions.append(
                AgentDecision(step="validate_fix", detail="Fix validated", success=valid)
            )
            remediation_applied = self._apply_fix(generated_fix, issues, decisions)
        compliance_notes = self.compliance_engine.map_to_controls(issues)
        ticket_update = self._update_ticket(alert, issues, remediation_applied)

        return AgentRunResult(
            alert=alert if isinstance(alert, Alert) else Alert(**alert_payload),
            validated=validated,
            remediation_applied=remediation_applied,
            decisions=decisions,
            generated_fix=generated_fix,
            issues=issues,
            compliance_notes=compliance_notes,
            ticket_update=ticket_update,
        )

    def _validate_alert(self, alert: dict[str, Any], decisions: list[AgentDecision]) -> bool:
        """Ensure the alert contains at least resource metadata or an issue type."""
        valid = bool(alert.get("resource") or alert.get("issue_type"))
        decisions.append(
            AgentDecision(step="validate_alert", detail="Alert validation complete", success=valid)
        )
        return valid

    def _apply_fix(
        self, fix_plan: FixPlan | None, issues: list[Issue], decisions: list[AgentDecision]
    ) -> bool:
        """Apply a generated fix to all connectors, capturing success state."""
        success = True
        for provider, connector in self.connectors.items():
            if hasattr(connector, "simulate_failure") and connector.simulate_failure():
                LOGGER.warning("Skipping fix application for %s due to simulated failure", provider)
                decisions.append(
                    AgentDecision(
                        step="apply_fix",
                        detail=f"Skipped {provider} due to simulated failure",
                        success=False,
                    )
                )
                success = False
                continue

            for issue in issues:
                try:
                    resource_id = issue.resource.get("id")
                    connector.apply_change(
                        {
                            "issue_type": issue.issue_type,
                            "fix_plan": fix_plan.content if fix_plan else "",
                            "resource": issue.resource,
                        }
                    )
                    decisions.append(
                        AgentDecision(
                            step="apply_fix",
                            detail=f"Applied fix for {issue.issue_type} to {resource_id}",
                            metadata={"provider": provider, **issue.resource},
                        )
                    )
                except Exception as exc:  # pragma: no cover - defensive
                    LOGGER.error("Failed to apply fix: %s", exc)
                    decisions.append(
                        AgentDecision(
                            step="apply_fix",
                            detail=f"Failed to apply fix for {issue.issue_type}",
                            success=False,
                            metadata={"provider": provider, **issue.resource},
                        )
                    )
                    success = False
        return success

    def _update_ticket(
        self, alert: Alert | dict[str, Any], issues: list[Issue], remediation_applied: bool
    ) -> str:
        alert_id = alert.id if isinstance(alert, Alert) else alert.get("id", "N/A")
        summary = (
            f"Alert {alert_id} handled. Issues: {len(issues)}. "
            f"Remediation applied: {remediation_applied}."
        )
        LOGGER.info(summary)
        return summary
