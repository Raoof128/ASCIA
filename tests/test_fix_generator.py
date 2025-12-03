"""Tests for the fix generator to ensure IaC plans are persisted."""
from __future__ import annotations

from pathlib import Path

from backend.engines.fix_generator import FixGenerator
from backend.models import Issue, Severity


def test_fix_generator_writes_plan(tmp_path):
    generator = FixGenerator(output_dir=tmp_path)
    issue = Issue(
        issue_type="Publicly exposed storage",
        severity=Severity.CRITICAL,
        resource={"id": "s3-001", "name": "open-bucket"},
        recommended_fix="Close public access",
    )

    plan = generator.generate([issue])

    assert plan.output_path
    assert Path(plan.output_path).exists()
    assert plan.content
    assert "aws_s3_bucket_public_access_block" in plan.content
    assert plan.validation_passed is True
