# predictive_demand Implementation Status

## Improve1 Slice

- Status: executable improve1 predictive demand controls implemented for all 50 backlog features.
- Code artifact/model: `demand_control.py` maps every feature to demand-owned control tables, required fields, and proof fields.
- UI surface: `ui.py` exposes 50 demand control panels, service actions, and agent tools while preserving forms, wizards, controls, and the single-PBC app surface.
- Service/API: `runtime.py` exposes `evaluate_demand_control` and `improve1_demand_control_contract`; each feature has a `POST /predictive-demand/improve1/<slug>` service route contract.
- Release evidence: `release_evidence.py` and runtime release evidence include the improve1 demand control contract.
- Tests: `tests/test_domain_behavior.py` verifies all 50 controls, signal/forecast/consensus/shortage/agent gates, AppGen-X eventing, database allowlist, owned-table boundaries, projection-only dependencies, and side-effect-free sample payloads.

## Constraints

- Datastore backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Eventing uses the AppGen-X event contract and the package topic.
- Cross-PBC dependencies are represented as declared APIs, events, or projections, not shared table access.
- Agent-assisted forecasting, scenario, override, replenishment, shortage, and publication actions remain preview-first and require human confirmation before mutation.
