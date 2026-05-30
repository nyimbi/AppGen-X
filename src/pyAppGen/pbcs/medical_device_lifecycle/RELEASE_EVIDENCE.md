# Release Evidence - Medical Device Lifecycle

Package directory: `pbcs/medical_device_lifecycle`.

This PBC includes owned schema, migration DDL, models, services, routes, events, handlers, UI workbench surfaces, agent skills, permissions, configuration, seed data, package metadata, side-effect-free registration, package-local forms/wizards/controls, a standalone one-PBC app shell, and focused package tests.

## Evidence

- Release Evidence: schema, service, route, event, handler, UI, agent, and governance contracts are materialized.
- Owned datastore boundary: every owned table starts with `medical_device_lifecycle_` and cross-PBC collaboration uses AppGen-X events or declared APIs.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence.
- Package-local operational surfaces: `forms.py`, `wizards.py`, and `controls.py` cover device intake, assignment governance, calibration/maintenance return-to-service, recall containment, evidence packets, and assistant previews.
- Standalone shell: `standalone.py` exercises in-memory device registration, assignment, calibration, usage traceability, recalls, evidence attachment, control-center rendering, and governed document previews.
- Package tests: `tests/test_contract.py` and `tests/test_standalone.py` validate schema/service/release, event contracts, side-effect-free registration, package-local UI/assistant surfaces, standalone routing, assignment blocking, and recall containment.
