# DAM Core

`dam_core` is a standalone AppGen-X packaged business capability for digital
asset management. This package owns its schema contracts, executable runtime,
stateful service layer, API routes, workbench UI, forms, wizards, controls,
AppGen-X event contract, governed agent planning surface, tests, and release
evidence.

## What This Package Now Provides

- A package-local runtime with owned DAM tables, configuration, parameters,
  rules, event inbox/outbox/dead-letter behavior, and workbench views.
- Runtime-driven schema, model, service, route, permission, seed, and release
  contracts so generated artifacts stay aligned with executable behavior.
- A standalone one-PBC app surface in `standalone.py` that bootstraps DAM
  state, dispatches package routes, loads a demo workspace, renders the
  workbench shell, and exposes a release snapshot.
- UI contracts for workbench fragments plus explicit forms, wizards, and
  reusable controls for asset intake, rights, metadata, rendition, document
  intake, and release review.
- Agent/document-planning helpers that extract owned-table facts from text and
  return governed CRUD or mutation previews with routes, permissions,
  idempotency keys, and AppGen-X event expectations.

## Key Entrypoints

- Runtime: `runtime.py`
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
