# Insurance Claims and Policy Release Evidence

The package directory `pbcs/insurance_claims_policy` contains the executable PBC implementation, manifest, schema, migrations, models, services, API routes, AppGen-X events, idempotent handlers, UI workbench fragments, permissions, configuration, rules, parameters, seed data, agent skills, chatbot contracts, and tests.

## Evidence

- Owned tables are under the `insurance_claims_policy_` prefix and foreign datastore mutation is rejected.
- Migrations create package-owned tables for PostgreSQL, MySQL, and MariaDB compatible SQL.
- Services expose command/query contracts with owned datastore plus outbox transaction boundaries.
- Events use the AppGen-X outbox, inbox, retry, idempotency, and dead-letter contract.
- Agent skills support document instruction intake and governed datastore CRUD previews.
- Release readiness is executable through `release_evidence.py` and package-local tests.
