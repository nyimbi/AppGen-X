# Release Evidence - Pharma Manufacturing Quality

Package directory: `pbcs/pharma_manufacturing_quality`.

This PBC includes owned schema, migration DDL, models, services, routes, events, handlers, UI workbench surfaces, agent skills, permissions, configuration, seed data, package metadata, side-effect-free registration, and focused package tests.

## Evidence

- Release Evidence: schema, service, route, event, handler, UI, agent, and governance contracts are materialized.
- Owned datastore boundary: every owned table starts with `pharma_manufacturing_quality_` and cross-PBC collaboration uses AppGen-X events or declared APIs.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence.
- Package tests: `tests/test_contract.py` validates schema/service/release, event contracts, side-effect-free registration, routes, governance, and idempotent handlers.
