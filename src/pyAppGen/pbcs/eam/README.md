# EAM PBC

`eam` is the standalone Enterprise Asset Management PBC package for AppGen-X. It owns equipment, maintenance plans, work orders, safety permits, spare usage, reliability evidence, AppGen-X event inbox/outbox/dead-letter tables, and the workbench/agent surfaces needed to operate a one-PBC maintenance application.

## Package Surface

- Runtime: side-effect-free EAM lifecycle operations in `runtime.py`
- Schema and migration evidence: `schema_contract.py`, `models.py`, `migrations/001_initial.sql`
- Services and routes: `services.py`, `routes.py`
- AppGen-X events and handlers: `events.py`, `handlers.py`
- Governance: `config.py`, `permissions.py`, `seed_data.py`
- UI and agent planning: `ui.py`, `agent.py`
- Release audit evidence: `release_evidence.py`, `RELEASE_EVIDENCE.md`
- Focused tests: `tests/test_contract.py`

## Standalone Proof Goals

The package is considered standalone-ready when it proves all of the following from inside `src/pyAppGen/pbcs/eam`:

- Owned tables, models, and migration evidence stay EAM-local.
- Runtime configuration is restricted to PostgreSQL, MySQL, or MariaDB with the AppGen-X event contract locked on.
- Services, routes, UI fragments, forms, wizards, controls, workflows, permissions, seed data, and agent/document/CRUD planning are internally consistent.
- AppGen-X emitted and consumed events are typed, idempotent, and bounded to package-owned or declared dependency surfaces.
- Focused compile and pytest gates pass for the package.
