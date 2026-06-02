# Airline Operations Control Standalone Implementation Plan

## Scope

Implement a one-PBC standalone app surface for `airline_operations_control` entirely inside the package directory. The slice must stay package-local, avoid shared generator or DSL changes, and make the existing timeline/rotation/turn logic executable through standalone runtime, services, routes, UI, assistant planning, and focused package tests.

## Slice Goals

1. Preserve and expose the current authoritative `flight_leg` timeline, tail rotation continuity graph, and minimum-turn feasibility engine.
2. Wrap that planning core in executable package-local state, route dispatch, and standalone app bootstrap/render flows.
3. Add package-local CRUD and planning support for `crew_pairing`, `disruption_event`, `reaccommodation_plan`, `operations_decision`, and `delay_code` records.
4. Publish forms, wizards, controls, permissions, document-instruction planning, and release evidence in one coherent package surface.
5. Verify with compile checks, package tests, and available PBC audits only for this package.

## Concrete File Changes

- Rewrite `runtime.py` as the stateful package core for contracts, commands, queries, permissions, and release evidence.
- Rewrite `services.py` and `routes.py` to expose dispatchable package-local API operations.
- Rewrite `ui.py` with standalone shell metadata, forms, wizards, controls, and rendered workbench output.
- Rewrite `agent.py`, `permissions.py`, `config.py`, `release_evidence.py`, and `models.py` to align with the standalone surface.
- Add `standalone.py` for bootstrap/demo/render/release flows.
- Update `__init__.py`, `README.md`, `RELEASE_EVIDENCE.md`, and `implementation-status.md` for the standalone slice.
- Replace package tests with focused standalone and contract coverage under `src/pyAppGen/pbcs/airline_operations_control/tests`.

## Acceptance Shape

The slice is complete when the package can:

- bootstrap one tenant-local standalone OCC workspace,
- dispatch routes without external dependencies,
- render a workbench showing an impossible outbound turn from a late inbound,
- expose permissions, assistant CRUD planning, and release evidence,
- pass focused compile/tests/audits without editing files outside the package.
