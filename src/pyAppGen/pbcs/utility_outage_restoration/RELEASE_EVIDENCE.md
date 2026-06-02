# Release Evidence - Utility Outage Restoration

Package directory: `pbcs/utility_outage_restoration`.

This PBC includes owned schema, migration DDL, models, services, routes, events, handlers, UI workbench surfaces, agent skills, permissions, configuration, seed data, package metadata, side-effect-free registration, focused package tests, and a package-local standalone outage-restoration slice.

## Evidence

- Release evidence: schema, service, route, event, handler, UI, agent, governance, standalone-app, and documentation contracts are materialized.
- Owned datastore boundary: every deployment-owned table starts with `utility_outage_restoration_`, and cross-PBC collaboration uses AppGen-X events or declared APIs only.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence. No stream-engine selector is exposed.
- Standalone execution: the package-local slice exercises network asset projection, outage intake, trouble calls, OMS events, crew dispatch, switching, safety isolation, damage assessment, ETR, nested outages, notifications, mutual aid, restoration verification, storm mode, and regulatory indices.
- Governed assistance: agent skills expose `governed_datastore_crud`, require confirmation for all mutations, and plan only against package-owned tables or package-local standalone tables.
- Package tests: `tests/test_contract.py` validates source-package contracts, while `tests/test_standalone_app.py` validates the standalone store, services, routes, UI, agent workspace, release evidence, and documentation artifacts.
