"""Tests for fix plan loading helpers."""
from __future__ import annotations

import glob
from pathlib import Path

from backend.api.fix import load_latest_fix


def test_load_latest_fix_returns_none_when_absent(monkeypatch):
    monkeypatch.setattr(glob, "glob", lambda pattern: [])
    assert load_latest_fix() is None


def test_load_latest_fix_reads_latest_file(monkeypatch, tmp_path: Path):
    first = tmp_path / "fix_1.tf"
    second = tmp_path / "fix_2.tf"
    first.write_text("first", encoding="utf-8")
    second.write_text("second", encoding="utf-8")

    def _fake_glob(pattern: str) -> list[str]:
        return [str(first), str(second)]

    monkeypatch.setattr(glob, "glob", _fake_glob)

    plan = load_latest_fix()

    assert plan is not None
    assert plan.output_path.endswith("fix_2.tf")
    assert "second" in plan.content
