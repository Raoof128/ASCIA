"""Tests for helper scripts to ensure demos stay functional."""
from __future__ import annotations

from pathlib import Path

from scripts import run_demo


def test_run_demo_outputs_fix(capsys, monkeypatch, tmp_path):
    monkeypatch.setattr(run_demo.AGENT.fix_generator, "output_dir", tmp_path)

    run_demo.main()
    output = capsys.readouterr().out

    assert "Decisions:" in output
    plan_files = list(Path(tmp_path).glob("*.tf"))
    assert plan_files, "Expected demo run to generate a Terraform plan"
