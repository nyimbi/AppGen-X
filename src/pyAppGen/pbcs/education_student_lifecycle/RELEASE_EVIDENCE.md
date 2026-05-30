# Release Evidence - Education Student Lifecycle

Package directory: `pbcs/education_student_lifecycle`.

This PBC includes owned schema, migration DDL references, models, services, routes, events, handlers, UI workbench surfaces, forms, wizards, controls, agent skills, permissions, configuration, seed data, package metadata, side-effect-free registration, standalone app smoke coverage, and focused package tests.

## Evidence

- Release evidence materializes schema, service, route, event, handler, UI, form, wizard, control, agent, governance, and single-PBC app contracts.
- Owned datastore boundary: every owned table starts with `education_student_lifecycle_` and cross-PBC collaboration uses AppGen-X events or declared APIs.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence.
- Standalone app: executable flows cover admissions readiness, enrollment activation, curriculum and registration, risk and interventions, petitions, degree audit, graduation clearance, and credential conferral.
- Package tests: `tests/test_contract.py` and `tests/test_student_lifecycle_app.py` validate contracts, runtime smoke, assistant routing, blocking controls, and the end-to-end standalone flow.
