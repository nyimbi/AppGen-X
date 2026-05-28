# Sustainability ESG Reporting Release Evidence

The package directory `pbcs/sustainability_esg_reporting` contains the executable PBC implementation, manifest, schema, migrations, models, services, API routes, AppGen-X events, idempotent handlers, UI workbench fragments, permissions, configuration, rules, parameters, seed data, agent skills, chatbot contracts, and tests.

## Evidence

- Owned tables are under the `sustainability_esg_reporting_` prefix and foreign datastore mutation is rejected.
- Migrations create package-owned tables for PostgreSQL, MySQL, and MariaDB compatible SQL.
- Services expose command/query contracts with owned datastore plus outbox transaction boundaries.
- Events use the AppGen-X outbox, inbox, retry, idempotency, and dead-letter contract.
- Agent skills support document instruction intake and governed datastore CRUD previews.
- Release readiness is executable through `release_evidence.py` and package-local tests.
