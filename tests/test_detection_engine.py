"""Detection engine tests to ensure coverage of simulated rules."""
from __future__ import annotations

from backend.engines.detection_engine import DetectionEngine
from connectors.aws_mock import AWSMockConnector
from connectors.azure_mock import AzureMockConnector
from connectors.gcp_mock import GCPMockConnector


def test_detection_engine_reports_expected_issue_types():
    connectors = {
        "aws": AWSMockConnector(),
        "azure": AzureMockConnector(),
        "gcp": GCPMockConnector(),
    }
    engine = DetectionEngine(connectors)

    issues = engine.detect()

    issue_types = {issue.issue_type for issue in issues}
    assert "Publicly exposed storage" in issue_types
    assert "IAM privilege escalation risk" in issue_types
    assert "Vulnerable runtime" in issue_types


class FailingConnector(AWSMockConnector):
    """Connector that simulates failure to ensure detection skips it."""

    def simulate_failure(self) -> bool:  # type: ignore[override]
        return True


def test_detection_engine_skips_failing_connectors():
    connectors = {"aws": FailingConnector()}
    engine = DetectionEngine(connectors)

    issues = engine.detect()

    assert issues == []
