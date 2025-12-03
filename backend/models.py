"""Shared data models for the autonomous self-healing cloud agent."""
from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Severity levels for misconfigurations."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Alert(BaseModel):
    """Incoming alert payload from monitoring systems."""

    id: str | None = Field(None, description="Unique alert identifier")
    issue_type: str | None = Field(None, description="Suspected issue type")
    resource: dict[str, Any] | None = Field(
        default=None, description="Resource metadata provided by the alerting system"
    )
    source: str | None = Field(None, description="Source system raising the alert")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Alert timestamp"
    )


class Issue(BaseModel):
    """Represents a detected cloud misconfiguration."""

    issue_type: str = Field(..., description="Type of the misconfiguration")
    severity: Severity = Field(..., description="Risk severity")
    resource: dict[str, Any] = Field(..., description="Metadata about the affected resource")
    recommended_fix: str = Field(..., description="Human readable fix guidance")
    detected_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Detection timestamp",
    )


class AgentDecision(BaseModel):
    """Represents a decision taken by the self-healing agent."""

    step: str
    detail: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    success: bool = True
    metadata: dict[str, Any] | None = None


class FixPlan(BaseModel):
    """Infrastructure-as-code plan to remediate an issue."""

    tool: str
    content: str
    validation_passed: bool
    output_path: str


class AgentRunResult(BaseModel):
    """Outcome of executing the agent on an alert."""

    alert: Alert | dict[str, Any]
    validated: bool
    remediation_applied: bool
    decisions: list[AgentDecision]
    generated_fix: FixPlan | None = None
    issues: list[Issue] = Field(default_factory=list)
    compliance_notes: dict[str, Any] | None = None
    ticket_update: str = ""
