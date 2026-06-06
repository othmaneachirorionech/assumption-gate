import unittest

from context_drift_gate import ContextContract, ContextDriftGate, ContextEvent, DriftDecision, RiskLevel


class ContextDriftGateTests(unittest.TestCase):
    def test_continue_when_no_material_change(self):
        gate = ContextDriftGate(ContextContract(
            workflow_id="w1",
            purpose="Draft outreach emails",
            assumptions={"lead_type": "private_company"},
            risk_level=RiskLevel.LOW,
        ))

        result = gate.evaluate(ContextEvent(
            name="company_size_updated",
            changes={"company_size": "10-50"},
        ))

        self.assertEqual(result.decision, DriftDecision.CONTINUE)
        self.assertFalse(result.requires_human_reauthorization)

    def test_pause_when_assumption_changes(self):
        gate = ContextDriftGate(ContextContract(
            workflow_id="w1",
            purpose="Draft outreach emails",
            assumptions={"lead_type": "private_company"},
            risk_level=RiskLevel.LOW,
        ))

        result = gate.evaluate(ContextEvent(
            name="lead_type_changed",
            changes={"lead_type": "government_agency"},
        ))

        self.assertEqual(result.decision, DriftDecision.PAUSE_FOR_REVIEW)
        self.assertTrue(result.requires_human_reauthorization)
        self.assertIn("lead_type", result.changed_keys)

    def test_stop_when_cost_limit_exceeded(self):
        gate = ContextDriftGate(ContextContract(
            workflow_id="w1",
            purpose="Draft outreach emails",
            max_cost_usd=1.0,
        ))

        result = gate.evaluate(ContextEvent(
            name="cost_update",
            cost_usd=1.25,
        ))

        self.assertEqual(result.decision, DriftDecision.STOP)
        self.assertTrue(result.requires_human_reauthorization)

    def test_stop_on_critical_risk(self):
        gate = ContextDriftGate(ContextContract(
            workflow_id="w1",
            purpose="Draft outreach emails",
            risk_level=RiskLevel.LOW,
        ))

        result = gate.evaluate(ContextEvent(
            name="risk_escalated",
            changes={"risk_level": "critical"},
        ))

        self.assertEqual(result.decision, DriftDecision.STOP)


if __name__ == "__main__":
    unittest.main()
