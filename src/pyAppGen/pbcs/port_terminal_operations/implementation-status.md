# port_terminal_operations Implementation Status

## Improve1 Slice

- Status: executable improve1 port terminal controls implemented for all 50 backlog features.
- Code artifact/model: `port_control.py` maps every feature to port-owned control tables, required fields, and proof fields.
- UI surface: `ui.py` exposes 50 port control panels, service actions, and agent tools while preserving the standalone forms, wizards, and controls.
- Service/API: `runtime.py` exposes `evaluate_port_control` and `improve1_port_control_contract`; each feature has a `POST /port-terminal-operations/improve1/<slug>` service route contract.
- Release evidence: `release_evidence.py` and runtime release evidence include the improve1 port control contract.
- Tests: `tests/test_domain_behavior.py` verifies all 50 controls, vessel/berth/crane/yard/gate/customs gates, AppGen-X eventing, database allowlist, owned-table boundaries, projection-only dependencies, and side-effect-free sample payloads.

## Constraints

- Datastore backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Eventing uses the AppGen-X event contract and the package topic.
- Cross-PBC dependencies are represented as declared APIs, events, or projections, not shared table access.
- Agent-assisted vessel, yard, gate, customs, and reefer actions remain preview-first and require human confirmation before operational mutation.
