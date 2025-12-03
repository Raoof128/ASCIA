from backend.engines.compliance_engine import ComplianceEngine
from backend.models import Issue, Severity


def test_map_to_controls_and_risk_score():
    engine = ComplianceEngine()
    issues = [
        Issue(
            issue_type="Publicly exposed storage",
            severity=Severity.CRITICAL,
            resource={"id": "s3-001", "name": "open-bucket"},
            recommended_fix="Close public access",
        ),
        Issue(
            issue_type="Missing MFA",
            severity=Severity.MEDIUM,
            resource={"id": "iam-001", "name": "admin"},
            recommended_fix="Enforce MFA",
        ),
    ]

    mapping = engine.map_to_controls(issues)
    assert "ACSC Essential Eight" in mapping
    assert "Multi-factor authentication" in mapping["ACSC Essential Eight"]
    assert "Information security risk treatment" in mapping["ISO/IEC 42001"]

    risk = engine.risk_score(issues)
    assert risk == 13
