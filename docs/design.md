# Context Drift Gate — Design Notes

## Problem

Many workflow and agent systems define permissions at the beginning of execution.
But execution context can change after the initial authorization.

Examples:

- A lead becomes a regulated entity.
- A draft becomes a financial commitment.
- Public data becomes sensitive data.
- A low-risk action becomes external execution.
- A harmless automation starts operating under a different purpose.

## Principle

```text
No continuation after material context change without reauthorization.
```

## Core objects

### ContextContract

The original operating context.

Includes:

- workflow_id
- purpose
- allowed_tools
- allowed_data
- assumptions
- risk_level
- cost/runtime limits
- fields that require human reauthorization

### ContextEvent

A runtime signal.

Includes:

- event name
- context changes
- evidence
- cost/runtime values
- sensitive/financial/external execution flags

### DriftResult

The decision:

- CONTINUE
- PAUSE_FOR_REVIEW
- STOP

## v0.1 boundaries

This package does not execute actions.
It only returns a decision.

Your application is responsible for enforcing the decision.

## Future roadmap

- JSON audit log
- Policy file support
- Pydantic models
- CLI
- FastAPI service
- LangGraph middleware example
- n8n/Make webhook adapter
- Signed execution receipts
