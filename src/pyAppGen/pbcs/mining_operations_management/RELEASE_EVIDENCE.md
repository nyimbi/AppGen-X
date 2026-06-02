# Release Evidence - Mining Operations Management

Package directory: `pbcs/mining_operations_management`.

This PBC includes owned schema, migration DDL, models, services, routes, events, handlers, UI workbench surfaces, package-local forms, guided wizards, operational controls, agent skills, permissions, configuration, seed data, package metadata, side-effect-free registration, a standalone one-PBC app surface, and focused package tests.

## Evidence

- Release Evidence: schema, service, route, event, handler, UI, agent, and governance contracts are materialized.
- Owned datastore boundary: every owned table starts with `mining_operations_management_` and cross-PBC collaboration uses AppGen-X events or declared APIs.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence.
- Standalone package-local app: forms, wizards, controls, route dispatch, and rendered workbench cards are executable through `standalone.py`.
- Package tests: `tests/test_contract.py` validates schema/service/release, event contracts, side-effect-free registration, routes, governance, and idempotent handlers. `tests/test_standalone.py` validates the standalone mine-plan-to-shift workflow and release evidence wiring.
