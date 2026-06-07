# assumption-gate

**assumption-gate** is a tiny Python primitive for workflow and AI-agent control.

It answers one question during execution:

> Is the context that authorized this workflow still valid?

Most systems authorize a workflow at the start. assumption-gate checks whether continuation is still allowed after material context changes.

## Why this exists

Tracing tells you what happened.

Guardrails validate inputs, outputs, or risky actions.

Budget limits stop execution after a fixed threshold.

assumption-gate focuses on a different failure mode:

> The workflow is still running, but the assumptions that made it safe are no longer true.

## Core idea

```text
Context Contract -> Runtime Events -> Drift Detection -> Decision

Decision = CONTINUE | PAUSE_FOR_REVIEW | STOP
```

## Example

```python
from context_drift_gate import (
    ContextContract,
    ContextEvent,
    ContextDriftGate,
    RiskLevel,
)

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

result = gate.evaluate(
    ContextEvent(
        name="lead_context_changed",
        changes={"lead_type": "government_agency"},
        evidence="Lead domain belongs to a public institution.",
    )
)

print(result.decision)
print(result.reason)
```

Expected result:

```text
PAUSE_FOR_REVIEW
Material context change detected.
```

## Quick Start

```bash
git clone https://github.com/othmaneachirorionech/assumption-gate.git

cd assumption-gate

python -m venv .venv

source .venv/bin/activate

pip install -e .

python examples/email_agent_example.py
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## What This Is Not

* Not a full governance platform.
* Not a replacement for observability.
* Not a security sandbox.
* Not an autonomous decision-maker.
* Not a compliance guarantee.
* Not a replacement for human approval.

It is a small control primitive:

> Pause or stop execution when material context changes require reauthorization.

## Design Rule

```text
No continuation after material context change without reauthorization.
```

## Background

assumption-gate is inspired by the Assumption Decay Doctrine:

> Every operational assumption has a shelf life.

A workflow may continue executing long after the assumptions that justified its execution have changed.

When material context changes occur, continued execution should not be treated as automatically valid.

## Background

assumption-gate is inspired by the [Assumption Decay Doctrine](docs/assumption-decay-doctrine.md):

> Every operational assumption has a shelf life.

A workflow may continue executing long after the assumptions that justified its execution have changed.

When material context changes occur, continued execution should not be treated as automatically valid.
## Status

v0.1.1 — Experimental.

Intended for developers building:

* AI agents
* Workflow systems
* Approval gates
* Automation pipelines
* Local-first agent architectures

## Feedback

If you are building AI agents, workflow systems, governance layers, or execution controls, open an issue and share your use case.

Contributions, discussions, and critiques are welcome.

## License

See the LICENSE file for details.
