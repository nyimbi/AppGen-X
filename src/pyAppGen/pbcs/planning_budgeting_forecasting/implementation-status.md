# planning_budgeting_forecasting Implementation Status

## Improve1 Slice

- Status: executable improve1 planning controls implemented for all 50 backlog features.
- Code artifact/model: `planning_control.py` maps every feature to planning-owned control tables, required fields, and proof fields.
- UI surface: `ui.py` exposes 50 planning control panels, service actions, and agent tools.
- Service/API: `runtime.py` exposes `evaluate_planning_control` and `improve1_planning_control_contract`; each feature has a `POST /planning-budgeting-forecasting/improve1/<slug>` service route contract.
- Release evidence: `release_evidence.py` and runtime release evidence include the improve1 planning control contract.
- Tests: `tests/test_domain_behavior.py` verifies all 50 controls, planning gates, AppGen-X eventing, database allowlist, owned-table boundaries, projection-only dependencies, and side-effect-free sample payloads.

## Constraints

- Datastore backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Eventing uses the AppGen-X event contract and the package topic.
- Cross-PBC dependencies are represented as declared APIs, events, or projections, not shared table access.
- Agent-assisted budget and forecast actions remain preview-first and require human confirmation before CRUD.
