# WMS Core Implementation Plan

## Objective

Deliver `wms_core` as a standalone warehouse management PBC that can bootstrap its own runtime, expose database-backed operational forms, run domain workflows from receiving through shipping, surface operator controls, and publish package-local release evidence.

## Scope

- Keep all changes inside `src/pyAppGen/pbcs/wms_core`.
- Reuse the existing warehouse runtime/models/routes/services/events/handlers rather than rewriting them.
- Add the missing standalone shell, repository/read-model layer, UI forms/wizards/controls, and package documentation/evidence.

## Workstreams

1. Extend `ui.py` with explicit forms, wizards, controls, and standalone shell metadata for warehouse masters, inbound, outbound, and governance.
2. Add `repository.py` with WMS-owned form bindings and read models for warehouse, inbound, outbound, and governance consoles.
3. Add `standalone.py` to bootstrap configuration/parameters/rules, load demo warehouse data, execute one inbound-to-ship scenario, and render the standalone workbench.
4. Strengthen `seed_data.py`, `permissions.py`, `release_evidence.py`, and `__init__.py` so the package exports a coherent standalone surface.
5. Add focused standalone tests and document the slice in `README.md`, `implementation-status.md`, and `RELEASE_EVIDENCE.md`.

## Verification targets

- Compile the assigned Python files under `src/pyAppGen/pbcs/wms_core`.
- Run focused `wms_core` tests.
- Run relevant `pyAppGen.pbc` audits for `wms_core` if available.
