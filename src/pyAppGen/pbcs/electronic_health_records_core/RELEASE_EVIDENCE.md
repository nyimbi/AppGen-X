# Release Evidence - Electronic Health Records Core

Package directory: `pbcs/electronic_health_records_core`.

This PBC now includes an executable one-PBC EHR core with owned schema, migration DDL, model contracts, services, routes, AppGen-X events, idempotent handlers, queue-oriented UI surfaces, governed agent skills, permissions, configuration, seed data, package metadata, side-effect-free registration, and focused package tests.

## Evidence

- Owned datastore boundary: all owned tables start with `electronic_health_records_core_` and cross-PBC collaboration stays on declared APIs or AppGen-X events.
- One-PBC application: forms, wizards, controls, workbench queues, and assistant panel are materialized through `single_pbc_app_contract()`.
- Clinical safety controls: duplicate-chart review, encounter completeness, order transition guards, critical-result acknowledgement, note attestation, and summary redaction are executable and tested.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence remains package-local.
- Package tests cover contract integrity, executable chart/order/observation/note flows, route dispatch, UI surface, agent document planning, and runtime smoke behavior.
