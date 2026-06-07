# Assumption Decay Doctrine

## Core Idea

Every operational assumption has a shelf life.

A workflow can continue running even after the assumptions that justified its execution are no longer true.

This creates a hidden failure mode:

> The system still works technically, but it is no longer operating under valid assumptions.

## Why This Matters

Most monitoring systems detect technical failure:

* crashed jobs
* failed API calls
* invalid inputs
* timeout errors
* broken integrations

But many workflow failures begin before anything breaks.

They begin when the context changes.

Examples:

* The customer segment changes.
* The data source changes.
* The approval owner changes.
* The legal context changes.
* The risk level changes.
* The tool behavior changes.
* The workflow purpose changes.
* The operating environment changes.

The workflow may still execute successfully.

That is the problem.

## The Doctrine

Assumption Decay Doctrine states:

> If an operational assumption is not revalidated after material context change, it decays into operational risk while still being treated as truth.

This means continuity is not evidence of validity.

A workflow that keeps running is not necessarily a workflow that is still allowed to continue.

## Assumption Debt

Assumption debt appears when a system continues to rely on assumptions that are:

* undocumented
* unverified
* outdated
* inherited from an earlier workflow state
* no longer aligned with the current operating context

Like technical debt, assumption debt accumulates silently.

Unlike technical debt, it often remains invisible because the system may continue to produce outputs.

## Hidden Assumptions

Many workflow assumptions are not explicitly documented.

They are often hidden inside:

* prompts
* routing logic
* filters
* scoring rules
* field mappings
* API mappings
* approval rules
* default values
* human habits
* undocumented operating procedures

Before assumptions can be monitored, they must first be surfaced.

A practical control path is:

```text
Hidden Assumption Surfacing
        ↓
Assumption Registry
        ↓
Expiry / Decay Monitoring
        ↓
Runtime Admissibility Gate
        ↓
Human Gate / Hold / Execute
```

## Material Context Change

A material context change is any change that may affect whether continued execution is still valid.

Examples:

* A lead changes from private company to public institution.
* A workflow begins processing sensitive data.
* A human approver is no longer responsible.
* A tool changes behavior or pricing.
* A model version changes.
* A legal or compliance constraint changes.
* The business purpose of the workflow changes.
* The workflow moves from test mode to production mode.

When material context changes occur, continuation should not be treated as automatically valid.

## Design Rule

```text
No continuation after material context change without reauthorization.
```

## Relationship to assumption-gate

`assumption-gate` is a small Python control primitive inspired by this doctrine.

It does not try to solve all governance problems.

It implements one narrow control idea:

> Pause or stop execution when material context changes require reauthorization.

The doctrine explains the failure mode.

The primitive provides one executable control point.

## What This Is Not

Assumption Decay Doctrine is not:

* a full governance framework
* a compliance guarantee
* a security model
* a replacement for observability
* a replacement for human judgment
* a claim that all assumptions can be detected automatically

It is a practical operating principle for workflow and AI-agent control.

## Practical Use Cases

This doctrine can apply to:

* AI agents
* automation workflows
* lead qualification systems
* email outreach agents
* CRM enrichment pipelines
* document processing workflows
* approval gates
* model-driven routing systems
* AI-assisted business operations

## Minimal Control Pattern

A minimal implementation should include:

1. A declared workflow purpose.
2. A list of key assumptions.
3. A way to detect material context changes.
4. A decision policy:

   * continue
   * pause for review
   * stop
5. An audit record explaining why execution continued, paused, or stopped.

## Final Principle

A system should not continue executing merely because it has not crashed.

Execution must remain valid under the current context.

When the assumptions expire, the workflow must be reviewed.



