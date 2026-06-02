# Inventory Positioning Implementation Status

## Status

Implemented as a standalone one-PBC package-local app shell with coherent
contracts, executable in-memory workflows, release evidence, assistant
planning, and focused tests.

## Completed

- Unified manifest, permissions, configuration, parameters, and rule metadata.
- Unified AppGen-X topics, inbox/outbox/dead-letter tables, and handler
  contracts.
- Added stateful standalone service and route dispatch aligned to the published
  `/inventory/*` API surface.
- Added standalone one-PBC app bootstrap and workbench rendering.
- Rebuilt schema/model/migration evidence around the actual
  `migrations/001_initial.sql` artifact.
- Added UI forms, wizards, controls, workflow lanes, and agent-safe panels.
- Expanded seed/bootstrap data for items, nodes, rules, parameters, and
  receipts.
- Expanded assistant/document/CRUD planning surface.
- Replaced dependency-only focused tests with a plain-Python focused runner.

## Self-Review Pass

Issues found and fixed during review:

- Removed dead-letter naming drift by standardizing on
  `inventory_positioning_dead_letter_event`.
- Removed event topic drift by standardizing on `appgen.inventory.events`.
- Replaced route/service path mismatches with a single `/inventory/*` route
  surface.
- Replaced migration references to non-existent per-table SQL files with actual
  coverage from `migrations/001_initial.sql`.
- Replaced mismatched permission bundles with inventory-specific action
  permissions used consistently by UI, services, and routes.

## Remaining Risks

- Verification is limited to compile/import/focused functional checks because
  `pytest` is not installed in the current shell.
- `runtime.py` still contains the original broad synthetic runtime smoke logic;
  package-level contracts now wrap it coherently, but future cleanup could make
  the runtime internals less synthetic.

## 2026-05-30 Domain Behavior Traceability Slice

- Expanded `tests/test_domain_behavior.py` with route, standalone app, assistant document/CRUD planning, owned-boundary, UI, and release-evidence checks.
- Updated `IMPROVE1_TRACEABILITY.md` so all 50 improve1 rows cite `tests/test_domain_behavior.py` as direct inventory positioning behavior evidence.
- Updated `improve1_capabilities.py` so every feature execution plan carries the domain behavior test artifact.
- Validation: `/Volumes/Media/src/pjs/appgen/.venv/bin/pytest src/pyAppGen/pbcs/inventory_positioning/tests`.
