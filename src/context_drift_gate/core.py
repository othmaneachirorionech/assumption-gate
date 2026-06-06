from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DriftDecision(str, Enum):
    CONTINUE = "continue"
    PAUSE_FOR_REVIEW = "pause_for_review"
    STOP = "stop"


@dataclass(frozen=True)
class ContextContract:
    """
    The operating context that authorizes a workflow or agent run.

    This is intentionally simple. v0.1 is a control primitive, not a platform.
    """

    workflow_id: str
    purpose: str
    allowed_tools: list[str] = field(default_factory=list)
    allowed_data: list[str] = field(default_factory=list)
    assumptions: dict[str, Any] = field(default_factory=dict)
    risk_level: RiskLevel = RiskLevel.LOW
    max_cost_usd: float | None = None
    max_runtime_seconds: int | None = None
    human_reauthorization_required_on: list[str] = field(default_factory=lambda: [
        "purpose",
        "risk_level",
        "sensitive_data",
        "legal_or_financial_consequence",
        "external_execution",
    ])


@dataclass(frozen=True)
class ContextEvent:
    """A runtime signal that may change the operating context."""

    name: str
    changes: dict[str, Any] = field(default_factory=dict)
    evidence: str | None = None
    cost_usd: float | None = None
    runtime_seconds: int | None = None
    introduces_sensitive_data: bool = False
    introduces_legal_or_financial_consequence: bool = False
    requests_external_execution: bool = False


@dataclass(frozen=True)
class DriftResult:
    decision: DriftDecision
    reason: str
    changed_keys: list[str] = field(default_factory=list)
    requires_human_reauthorization: bool = False
    evidence: str | None = None
