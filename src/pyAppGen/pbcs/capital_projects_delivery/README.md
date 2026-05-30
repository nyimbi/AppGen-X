# Capital Projects Delivery

`capital_projects_delivery` is a standalone AppGen-X packaged business capability for capital project lifecycle control. The package owns its schema contracts, executable runtime, service layer, API routes, workbench UI, forms, wizards, controls, workflow descriptors, AppGen-X event contract, governed assistant planning surface, release evidence, and standalone bootstrap path.

## What This Package Now Provides

- A package-local runtime that governs capital project stage-gate transitions, checklist evidence, approvals, rollback rebaselining, inbox/outbox/dead-letter eventing, and workbench projections.
- Runtime-driven schema, model, service, route, workflow, permission, seed, and release contracts so the standalone slice stays aligned with executable behavior.
- A standalone one-PBC app surface in `standalone.py` that bootstraps configuration, parameters, rules, policy events, demo project data, route dispatch, workbench rendering, and release snapshots entirely inside this package.
- UI contracts for workbench fragments plus explicit forms, wizards, controls, navigation, and permission-aware rendering for intake, checklist, approval, assistant, and release-review flows.
- Agent/document-planning helpers that extract capital-project facts from text and return governed CRUD or mutation previews with routes, permissions, idempotency keys, workflows, and AppGen-X event expectations.

## Key Entrypoints

- Runtime: `runtime.py`
- Services: `services.py`
- Routes: `routes.py`
- UI/workbench: `ui.py`
- Agent planning: `agent.py`
- Standalone app: `standalone.py`
- Release audit: `release_evidence.py`

## Implemented Standalone Slice

The package executes a real capital-project stage-gate slice inside a one-PBC app shell:

- create a governed capital project in `idea`,
- record gate checklist evidence,
- approve or reject stage transitions with approver-role controls,
- require a rebaseline reason on backward moves,
- expose lifecycle state in detail, workbench, workflows, and assistant planning,
- bootstrap and render the slice as a standalone package-local app surface,
- keep all eventing AppGen-X only and all writes inside owned `capital_projects_delivery_*` tables.

## Validation

Focused package-local validation is captured in `tests/test_contract.py`, `tests/test_lifecycle_app_slice.py`, `tests/test_standalone.py`, `implementation-status.md`, and `RELEASE_EVIDENCE.md`.
