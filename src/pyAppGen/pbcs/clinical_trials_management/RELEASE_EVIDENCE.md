# Release Evidence - Clinical Trials Management

Package directory: `pbcs/clinical_trials_management`.

This PBC includes owned schema, migration DDL, models, services, routes, events, handlers, UI workbench surfaces, forms, wizards, controls, agent skills, permissions, configuration, seed data, package metadata, side-effect-free registration, and focused package tests.

## Evidence

- Release Evidence: schema, service, route, event, handler, UI, forms, wizards, controls, agent, and governance contracts are materialized.
- Owned datastore boundary: every owned table starts with `clinical_trials_management_` and cross-PBC collaboration uses AppGen-X events rather than foreign-table mutation.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence for policy, site-document, and lab-result events.
- Domain controls: release readiness now checks site activation evidence, consent/enrollment gates, serious-event reporting timeliness, monitoring closure, and data-lock blockers.
- Package tests: `tests/test_contract.py` validates schema/service/release, event contracts, assistant previews, workbench surfaces, enrollment/consent gating, runtime smoke, and idempotent handlers.
