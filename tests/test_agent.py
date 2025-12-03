"""Unit tests for the self-healing agent."""
from __future__ import annotations

from backend.agents.self_healing_agent import SelfHealingAgent
from backend.app_state import AGENT
from backend.types import CloudConnector


def test_agent_runs_and_detects_issues():
    alert = {"id": "1", "issue_type": "Publicly exposed storage"}
    result = AGENT.run(alert)
    assert result.validated is True
    assert result.issues, "Expected issues to be detected"
    assert result.remediation_applied is True


def test_compliance_risk_score_positive():
    issues = AGENT.detector.detect()
    score = AGENT.compliance_engine.risk_score(issues)
    assert score > 0


def test_agent_rejects_unvalidated_alert():
    result = AGENT.run({"id": "missing-fields"})
    assert result.validated is False
    assert result.remediation_applied is False
    assert result.issues == []


class ApplyFailureConnector(CloudConnector):
    """Connector that succeeds during detection but fails when applying changes."""

    def list_resources(self) -> list[dict[str, str]]:
        return [{"id": "resource-1", "name": "demo"}]

    def get_config(self, resource_id: str) -> dict[str, object]:
        return {"public": True}

    def apply_change(self, change: dict[str, object]) -> None:
        raise RuntimeError("simulated failure")

    def simulate_failure(self) -> bool:
        return False


def test_agent_records_failed_apply(monkeypatch, tmp_path):
    agent = SelfHealingAgent({"aws": ApplyFailureConnector()})
    monkeypatch.setattr(agent.fix_generator, "output_dir", tmp_path)

    result = agent.run({"id": "2", "issue_type": "Publicly exposed storage"})

    assert result.remediation_applied is False
    assert any(
        decision.step == "apply_fix" and decision.success is False
        for decision in result.decisions
    )
