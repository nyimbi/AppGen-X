# Building Information Modeling Operations

This package implements a standalone executable BIM operations slice focused on:

- federation registry and discipline package mapping
- shared coordinates and georeferencing assurance
- model issue-purpose governance
- assistant-backed document-instruction and CRUD planning
- release evidence for approved federations

## Single-PBC App Surface

The package is usable as a one-PBC app and keeps all behavior inside owned tables and AppGen-X events only.

- Database-backed owned models and migration live in `models.py` and `migrations/001_initial.sql`.
- Executable federation governance lives in `federation_governance.py`, `runtime.py`, and `services.py`.
- Route, event, and handler contracts live in `routes.py`, `events.py`, and `handlers.py`.
- Forms, wizards, controls, and workbench projections live in `ui.py`.
- Assistant help plus document-instruction and CRUD planning live in `agent.py` and `standalone.py`.
- Standalone bootstrap, demo workspace loading, workbench rendering, and release snapshots live in `standalone.py`.
- Package-local validation lives in `tests/test_contract.py`, `tests/test_federation_slice.py`, and `tests/test_standalone.py`.

## Implemented User Flows

1. Configure the project coordinate baseline.
2. Register model packages with discipline, checksum, issue purpose, approval state, and spatial coverage.
3. Run controls that check coordinate alignment, publishable issue purpose, approval lineage, and owned-table boundaries.
4. Assemble an approved federation and generate release evidence with contributor checksums, approval states, and lineage.
5. Produce assistant-ready document-instruction and datastore CRUD plans before any governed mutation is executed.
6. React to `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` through AppGen-X-only inbound handling.

## Explicit Constraints Kept

- Eventing remains `AppGen-X`.
- Stream-engine picker remains hidden.
- Shared table access remains disabled.
- All edits and artifacts stay inside this PBC directory.
