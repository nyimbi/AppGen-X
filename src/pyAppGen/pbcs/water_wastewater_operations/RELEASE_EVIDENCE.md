# Release Evidence - Water and Wastewater Operations

Package directory: `pbcs/water_wastewater_operations`.

This PBC includes owned schema, migration DDL, models, services, routes, events, handlers, UI workbench surfaces, agent skills, permissions, configuration, seed data, package metadata, side-effect-free registration, and focused package tests.

## Evidence

- Release Evidence: schema, service, route, event, handler, UI, agent, and governance contracts are materialized.
- Owned datastore boundary: every owned table starts with `water_wastewater_operations_` and cross-PBC collaboration uses AppGen-X events or declared APIs.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence.
- Package tests: `tests/test_contract.py` validates schema/service/release, event contracts, side-effect-free registration, routes, governance, and idempotent handlers.
