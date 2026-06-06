# Context Drift Gate

**Context Drift Gate** is a tiny Python primitive for workflow and AI-agent control.

It answers one question during execution:

> Is the context that authorized this workflow still valid?

Most systems authorize a workflow at the start. Context Drift Gate checks whether continuation is still allowed after material context changes.

## Why this exists

Tracing tells you what happened.
Guardrails validate inputs, outputs, or risky actions.
Budget limits stop execution after a fixed threshold.

Context Drift Gate focuses on a different failure mode:

> The workflow is still running, but the assumptions that made it safe are no longer true.

## Core idea

```text
Context Contract -> Runtime Events -> Drift Detection -> Decision

Decision = CONTINUE | PAUSE_FOR_REVIEW | STOP
```

## Example

```python
from context_drift_gate import ContextContract, ContextEvent, ContextDriftGate, RiskLevel

contract = ContextContract(
    workflow_id="lead-email-agent",
    purpose="Send low-risk introductory outreach emails",
    allowed_tools=["email_draft"],
    allowed_data=["public_lead_profile"],
    assumptions={
        "lead_type": "private_company",
        "message_type": "introductory_only",
        "no_sensitive_data": True,
    },
    risk_level=RiskLevel.LOW,
)

gate = ContextDriftGate(contract)

result = gate.evaluate(ContextEvent(
    name="lead_context_changed",
    changes={"lead_type": "government_agency"},
    evidence="Lead domain belongs to a public institution.",
))

print(result.decision)  # PAUSE_FOR_REVIEW
print(result.reason)
```

## Install locally

```bash
git clone https://github.com/your-username/context-drift-gate.git
cd context-drift-gate
python -m venv .venv
source .venv/bin/activate
pip install -e .
python examples/email_agent_example.py
```

## Run tests

```bash
python -m unittest discover -s tests
```

## What this is not

- Not a full governance platform.
- Not a replacement for observability.
- Not a security sandbox.
- Not an autonomous decision-maker.
- Not a compliance guarantee.

It is a small control primitive: **pause or stop when material context changes require reauthorization.**

## Design rule

```text
No continuation after material context change without reauthorization.
```

## Status

v0.1 — Experimental. Intended for developers building local agents, automations, workflow tools, and approval gates.
