# Advertising Campaign Operations Implementation Plan

## Scope

Implement a real, executable slice from the advertising backlog that replaces placeholder behavior with domain-specific campaign operations logic. The chosen slice covers:

1. Canonical campaign brief and objective modeling.
2. Pre-launch readiness gating.

This stays inside the `advertising_campaign_operations` package and the single root test file owned for this task.

## Why This Slice

- It is directly grounded in the backlog in `improve1.md`.
- It turns the existing generic `command_ad_campaign` path into advertising-specific behavior.
- It produces testable business outcomes without broadening scope into unrelated integrations or storage layers.

## Planned Changes

### New package-local planning module

Add a focused helper module that:

- Normalizes campaign briefs into a deterministic shape.
- Validates required brief fields: objective, offer, audience promise, channels, primary KPI, guardrails, and launch dependencies.
- Builds a stable draft campaign plan from the normalized brief.
- Evaluates launch readiness against a fixed AppGen-X-compatible checklist.
- Produces a workbench-friendly command-center summary for draft plans.

### Runtime integration

Extend `runtime.py` to:

- Store campaign plans and launch reviews in runtime state.
- Add an executable `create_campaign_plan` command.
- Add an executable `review_launch_readiness` query/assessment path.
- Enrich `command_ad_campaign` when a structured brief is supplied.
- Emit only AppGen-X event types already declared by the PBC manifest.

### Service, UI, and agent integration

Extend package-local modules so the new slice is visible through the existing package surfaces:

- `services.py`: expose the new command/query operations.
- `ui.py`: return a launch command-center summary and planning panels.
- `agent.py`: provide brief preview and launch readiness preview helpers for the assistant surface.

## Acceptance Targets

- Incomplete structured briefs are rejected with itemized missing fields.
- Repeated brief submissions produce the same normalized draft shape and fingerprint.
- Launch readiness returns explicit blockers until required approvals and readiness evidence are present.
- A ready campaign can produce an approval event without introducing non-AppGen-X event contracts.
- Focused tests prove the behavior through runtime and service entry points.

## Verification Plan

- Run focused pytest coverage for the new implementation file.
- Re-run the existing advertising campaign operations runtime and contract tests.
- Run Python compilation checks on modified package files.

## Non-Goals

- No new dependencies.
- No edits outside this PBC package and `tests/test_pbc_advertising_campaign_operations_implementation.py`.
- No non-approved backend references; only ordinary PostgreSQL/MySQL/MariaDB language remains.
- No SAP, S/4, Salesforce, or QuickBooks terminology.
