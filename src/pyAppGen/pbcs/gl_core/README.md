# GL Core

`gl_core` is a standalone AppGen-X packaged business capability for general
ledger operations. This package owns its schema contracts, executable runtime,
repository, service layer, API routes, workbench UI, forms, wizards, controls,
AppGen-X event contract, governed agent surface, tests, and release evidence.

## What This Package Provides

- A package-local runtime with immutable journal events, close controls,
  projections, reconciliation, policy evaluation, AppGen-X inbox/outbox
  semantics, and audit-proof generation.
- A standalone one-PBC app surface in `standalone.py` that bootstraps GL
  configuration, parameters, rules, seed data, inbound source events, journal
  drafts, posting, close snapshots, and workbench rendering.
- A database-backed repository layer in `repository.py` for chart accounts,
  accounting periods, journal drafts, semantic source documents,
  reconciliation cases, and close snapshots.
- UI contracts for a GL workbench plus explicit forms, wizards, and reusable
  controls for chart governance, journal preparation, reconciliation, close,
  and audit review.
- Agent/document-planning helpers that derive ledger accounts from finance text
  and return governed mutation previews with routes, permissions, forms,
  controls, and AppGen-X event expectations.

## Key Entrypoints

- Runtime: `runtime.py`
- Repository: `repository.py`
- Models: `models.py`
- Services: `services.py`
- Routes: `routes.py`
- UI/workbench: `ui.py`
- Standalone app: `standalone.py`
- Agent planning: `agent.py`
- Release audit: `release_evidence.py`

## Validation

Focused package-local validation is captured in `tests/test_contract.py`,
`tests/test_standalone.py`, `implementation-status.md`, and
`RELEASE_EVIDENCE.md`.
