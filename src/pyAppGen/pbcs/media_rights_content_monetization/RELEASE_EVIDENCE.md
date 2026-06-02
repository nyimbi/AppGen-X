# Release Evidence - Media Rights and Content Monetization

Package directory: `pbcs/media_rights_content_monetization`.

This PBC includes owned schema, migration DDL, models, services, routes, events, handlers, UI workbench surfaces, package-local forms/wizards/controls, a standalone one-PBC application surface, agent skills, permissions, configuration, seed data, package metadata, side-effect-free registration, and focused package tests.

## Evidence

- Release evidence: schema, service, route, event, handler, UI, agent, governance, and standalone contracts are materialized.
- Standalone evidence: `standalone.py` exercises rights intake, licensing scope, window review, territory carve-outs, availability resolution, usage approval, royalty simulation, assistant preview, and control-center readiness.
- Owned datastore boundary: every owned table starts with `media_rights_content_monetization_` and cross-PBC collaboration uses AppGen-X events or declared APIs.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence.
- Package tests: `tests/test_contract.py` validates schema/service/release, event contracts, side-effect-free registration, routes, governance, and idempotent handlers. `tests/test_standalone_surface.py` validates the standalone app, form/wizard/control catalogs, and release evidence coverage for the new app surface.
