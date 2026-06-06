from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .core import ContextContract, ContextEvent, DriftDecision, DriftResult, RiskLevel


_RISK_ORDER = {
    RiskLevel.LOW: 1,
    RiskLevel.MEDIUM: 2,
    RiskLevel.HIGH: 3,
    RiskLevel.CRITICAL: 4,
}


class ContextDriftGate:
    """
    Evaluates whether a workflow may continue after runtime context changes.

    v0.1 decision logic:
    - Continue on no material changes.
    - Pause for review when assumptions or protected context keys change.
    - Stop when limits are exceeded or critical risk appears.
    """

    def __init__(self, contract: ContextContract):
        self.contract = contract
        self.contract_fingerprint = self._fingerprint(asdict(contract))

    def evaluate(self, event: ContextEvent) -> DriftResult:
        changed_keys = list(event.changes.keys())

        limit_result = self._check_limits(event)
        if limit_result is not None:
            return limit_result

        critical_result = self._check_critical_transitions(event)
        if critical_result is not None:
            return critical_result

        protected_changes = self._protected_changes(event)
        assumption_changes = self._assumption_changes(event)

        if protected_changes or assumption_changes:
            keys = sorted(set(protected_changes + assumption_changes))
            return DriftResult(
                decision=DriftDecision.PAUSE_FOR_REVIEW,
                reason="Material context changed. Continuation requires human reauthorization.",
                changed_keys=keys,
                requires_human_reauthorization=True,
                evidence=event.evidence,
            )

        if changed_keys:
            return DriftResult(
                decision=DriftDecision.CONTINUE,
                reason="Context changed, but no material authorization boundary was crossed.",
                changed_keys=changed_keys,
                evidence=event.evidence,
            )

        return DriftResult(
            decision=DriftDecision.CONTINUE,
            reason="No context drift detected.",
            changed_keys=[],
            evidence=event.evidence,
        )

    def _check_limits(self, event: ContextEvent) -> DriftResult | None:
        if self.contract.max_cost_usd is not None and event.cost_usd is not None:
            if event.cost_usd > self.contract.max_cost_usd:
                return DriftResult(
                    decision=DriftDecision.STOP,
                    reason="Cost limit exceeded. Execution stopped.",
                    changed_keys=["cost_usd"],
                    requires_human_reauthorization=True,
                    evidence=event.evidence,
                )

        if self.contract.max_runtime_seconds is not None and event.runtime_seconds is not None:
            if event.runtime_seconds > self.contract.max_runtime_seconds:
                return DriftResult(
                    decision=DriftDecision.STOP,
                    reason="Runtime limit exceeded. Execution stopped.",
                    changed_keys=["runtime_seconds"],
                    requires_human_reauthorization=True,
                    evidence=event.evidence,
                )

        return None

    def _check_critical_transitions(self, event: ContextEvent) -> DriftResult | None:
        risk_value = event.changes.get("risk_level")
        if risk_value is not None:
            try:
                new_risk = RiskLevel(risk_value)
            except ValueError:
                return DriftResult(
                    decision=DriftDecision.PAUSE_FOR_REVIEW,
                    reason="Unknown risk level introduced. Human review required.",
                    changed_keys=["risk_level"],
                    requires_human_reauthorization=True,
                    evidence=event.evidence,
                )

            if _RISK_ORDER[new_risk] >= _RISK_ORDER[RiskLevel.CRITICAL]:
                return DriftResult(
                    decision=DriftDecision.STOP,
                    reason="Critical risk introduced. Execution stopped.",
                    changed_keys=["risk_level"],
                    requires_human_reauthorization=True,
                    evidence=event.evidence,
                )

        if event.introduces_legal_or_financial_consequence:
            return DriftResult(
                decision=DriftDecision.PAUSE_FOR_REVIEW,
                reason="Legal or financial consequence introduced. Human reauthorization required.",
                changed_keys=["legal_or_financial_consequence"],
                requires_human_reauthorization=True,
                evidence=event.evidence,
            )

        if event.requests_external_execution:
            return DriftResult(
                decision=DriftDecision.PAUSE_FOR_REVIEW,
                reason="External execution requested. Human reauthorization required.",
                changed_keys=["external_execution"],
                requires_human_reauthorization=True,
                evidence=event.evidence,
            )

        if event.introduces_sensitive_data:
            return DriftResult(
                decision=DriftDecision.PAUSE_FOR_REVIEW,
                reason="Sensitive data introduced. Human reauthorization required.",
                changed_keys=["sensitive_data"],
                requires_human_reauthorization=True,
                evidence=event.evidence,
            )

        return None

    def _protected_changes(self, event: ContextEvent) -> list[str]:
        protected = set(self.contract.human_reauthorization_required_on)
        return [key for key in event.changes.keys() if key in protected]

    def _assumption_changes(self, event: ContextEvent) -> list[str]:
        changed = []
        for key, new_value in event.changes.items():
            if key in self.contract.assumptions:
                old_value = self.contract.assumptions[key]
                if old_value != new_value:
                    changed.append(key)
        return changed

    @staticmethod
    def _fingerprint(payload: dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()
