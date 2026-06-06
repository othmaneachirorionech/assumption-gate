from context_drift_gate import ContextContract, ContextDriftGate, ContextEvent, RiskLevel


def main() -> None:
    contract = ContextContract(
        workflow_id="lead-email-agent",
        purpose="Draft low-risk introductory outreach emails",
        allowed_tools=["email_draft"],
        allowed_data=["public_lead_profile"],
        assumptions={
            "lead_type": "private_company",
            "message_type": "introductory_only",
            "no_sensitive_data": True,
        },
        risk_level=RiskLevel.LOW,
        max_cost_usd=2.00,
    )

    gate = ContextDriftGate(contract)

    events = [
        ContextEvent(
            name="normal_profile_update",
            changes={"company_size": "50-200"},
            evidence="Company size found on public profile.",
        ),
        ContextEvent(
            name="lead_context_changed",
            changes={"lead_type": "government_agency"},
            evidence="Lead domain belongs to a public institution.",
        ),
        ContextEvent(
            name="cost_limit_exceeded",
            changes={},
            cost_usd=2.50,
            evidence="Provider billing counter passed allowed cost.",
        ),
    ]

    for event in events:
        result = gate.evaluate(event)
        print(f"\nEVENT: {event.name}")
        print(f"DECISION: {result.decision.value}")
        print(f"REASON: {result.reason}")
        print(f"CHANGED: {result.changed_keys}")


if __name__ == "__main__":
    main()
