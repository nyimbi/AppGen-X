# Release Evidence - Energy Grid Operations

Package directory: `pbcs/energy_grid_operations`.

This package now includes executable owned-state runtime behavior, standalone one-PBC app composition, grid-specific forms and workbench controls, AppGen-X event evidence, bounded governance surfaces, and focused package-local tests.

## Evidence Areas

- Owned schema and migration evidence for grid assets, forecasts, switching, dispatch, outages, topology, reliability constraints, governance, and AppGen-X runtime tables.
- Service and route execution evidence for the standalone app and declared public APIs.
- AppGen-X emitted and consumed event contract evidence with inbox, outbox, idempotency, and dead-letter handling.
- UI evidence for forms, wizards, controls, workbench cards, queues, and release-ready navigation.
- Agent evidence for switching simulation previews, outage summaries, governed CRUD previews, and document-intake planning.
- Release-readiness evidence assembled in `release_evidence.py`, with exact command results recorded in `implementation-status.md`.

## Required Package Artifacts

- `README.md`
- `SPECIFICATION.md`
- `implementation-plan.md`
- `implementation-status.md`
- `RELEASE_EVIDENCE.md`
- `standalone.py`
- `tests/test_contract.py`
- `tests/test_standalone.py`
