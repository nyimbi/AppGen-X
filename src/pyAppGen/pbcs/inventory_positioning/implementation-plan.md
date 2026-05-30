# Inventory Positioning Implementation Plan

## Goal

Make `inventory_positioning` executable as a standalone one-PBC AppGen-X app
without touching files outside this package. The package should expose a
coherent runtime, schema/migration evidence, services, routes, UI/workbench
surfaces, AppGen-X event contracts, permissions, seed data, agent/chatbot
planning, release evidence, and focused tests.

## Current Problems

- Generated modules disagree on event topics, dead-letter table names,
  permissions, route paths, and emitted events.
- Schema and release evidence reference migrations that do not exist.
- The service layer is contract-only and does not provide a real standalone
  app/service shell that can execute a one-PBC workflow end to end.
- UI metadata lacks explicit forms, wizards, and controls for the workbench
  described in the specification.
- Seed data and agent planning are minimal and do not reflect the inventory
  positioning domain.
- Existing tests depend on `pytest`, which is not currently available in this
  shell.

## Implementation Approach

1. Keep `runtime.py` as the domain engine for in-memory workflow execution.
2. Rebuild package-level modules around a single source of truth so contracts
   are internally consistent.
3. Add a package-local standalone app/service shell for one-PBC execution.
4. Expand UI metadata with forms, wizards, controls, and agent-safe panels.
5. Expand seed data and assistant planning with inventory-specific evidence.
6. Replace `pytest`-only focused tests with plain-assert modules plus a local
   focused runner that works with the standard library interpreter.

## Planned File Changes

- `manifest.py`
  Align manifest metadata with runtime, routes, UI, permissions, and events.
- `config.py`
  Define coherent runtime configuration, parameter, and rule governance.
- `models.py`, `schema_contract.py`, `service_contract.py`,
  `release_evidence.py`
  Replace inconsistent generated blobs with compact derived contracts and real
  migration coverage evidence from `migrations/001_initial.sql`.
- `services.py`, `routes.py`, `standalone.py`
  Provide executable stateful service and route dispatch for a standalone
  one-PBC app.
- `ui.py`
  Add workbench forms, wizards, controls, workflow lanes, and operator panels.
- `events.py`, `handlers.py`
  Unify AppGen-X topics, inbox/outbox/dead-letter tables, and idempotent
  handler behavior.
- `permissions.py`, `seed_data.py`, `agent.py`
  Align domain governance, starter data, and assistant planning.
- `tests/*`
  Add focused runtime and standalone tests that run without external test
  dependencies.
- `README.md`, `implementation-status.md`
  Document the implemented surface, verification, and remaining gaps.

## Verification Plan

- `python3 -m compileall` on the package.
- A plain-Python focused test runner that imports the package and executes all
  `test_*` functions under `tests/`.
- Additional import and smoke checks for the standalone app descriptor and
  release evidence.

## Constraints

- Edit only `src/pyAppGen/pbcs/inventory_positioning`.
- Do not revert unrelated work.
- Keep the diff reviewable and package-local.
