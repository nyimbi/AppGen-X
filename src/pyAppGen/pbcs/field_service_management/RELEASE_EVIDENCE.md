# Field Service Management Release Evidence

The package directory `pbcs/field_service_management` contains the executable PBC implementation, manifest, schema, migrations, models, services, API routes, AppGen-X events, idempotent handlers, UI workbench fragments, permissions, configuration, rules, parameters, seed data, agent skills, chatbot contracts, and tests.

## Evidence

- Owned tables are under the `field_service_management_` prefix and foreign datastore mutation is rejected.
- Migrations create package-owned tables for PostgreSQL, MySQL, and MariaDB compatible SQL.
- Services expose command/query contracts with owned datastore plus outbox transaction boundaries.
- Events use the AppGen-X outbox, inbox, retry, idempotency, and dead-letter contract.
- Agent skills support document instruction intake and governed datastore CRUD previews.
- Advanced field operations are executable through `field_operations.py`: consented live technician location tracking, technician availability, route optimization and reoptimization, mobile task dependency planning, job-tool requirement/calibration validation, tool reservation, and skill-location-tool assignment scoring.
- The UI exposes live workforce map, route optimizer, technician availability board, skill assignment console, job-tool planner, tool calibration/custody console, task dependency board, and offline mobile conflict queue surfaces.
- Release readiness is executable through `release_evidence.py` and package-local tests.
