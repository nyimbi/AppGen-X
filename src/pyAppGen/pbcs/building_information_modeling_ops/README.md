# Building Information Modeling Operations

This package now implements an executable BIM operations improvement slice focused on:

- federation registry and discipline package mapping
- shared coordinates and georeferencing assurance
- model issue-purpose governance
- release evidence for approved federations

## Single-PBC App Surface

The package is usable as a one-PBC app for this slice and keeps all behavior inside owned tables and AppGen-X events only.

- Database-backed owned models and migration: [models.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/models.py), [001_initial.sql](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/migrations/001_initial.sql)
- Executable federation logic: [federation_governance.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/federation_governance.py)
- Runtime and services: [runtime.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/runtime.py), [services.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/services.py)
- Forms, wizards, controls, and workbench views: [ui.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/ui.py)
- Agent help and guided workflows: [agent.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/agent.py)
- Route, event, and handler contracts: [routes.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/routes.py), [events.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/events.py), [handlers.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/handlers.py)
- Package-local validation: [tests/test_contract.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/tests/test_contract.py), [tests/test_federation_slice.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/building_information_modeling_ops/tests/test_federation_slice.py)

## Implemented User Flows

1. Configure the project coordinate baseline.
2. Register model packages with discipline, checksum, issue purpose, approval state, and spatial coverage.
3. Run controls that check coordinate alignment, publishable issue purpose, approval lineage, and owned-table boundaries.
4. Assemble an approved federation and generate release evidence with contributor checksums and approval states.
5. React to `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` through AppGen-X-only inbound handling.

## Explicit Constraints Kept

- Eventing remains `AppGen-X`.
- Stream-engine picker remains hidden.
- Shared table access remains disabled.
- All edits and artifacts stay inside this PBC directory.
