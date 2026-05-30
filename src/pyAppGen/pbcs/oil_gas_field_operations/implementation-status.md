# oil_gas_field_operations implementation status

## Improve1 executable controls

- Status: implemented for 50 of 50 improve1 backlog features.
- Control module: `field_operations_control.py`.
- Runtime wiring: `oil_gas_field_operations_runtime_capabilities()` exposes `field_operations_control` and `evaluate_field_operations_control`.
- UI wiring: `oil_gas_field_operations_ui_contract()` and `oil_gas_field_operations_render_workbench()` expose 50 field-operations control panels, service actions, and agent tools.
- Release evidence: `validate_release_evidence()` includes the field operations control contract and blocks on failed improve1 controls.
- Tests: `tests/test_domain_behavior.py` validates ownership, AppGen-X eventing, database backend allowlist, projection-only dependencies, human approval gates, agent preview gates, non-mutating simulations, and field-risk evidence gates.

## Domain surface covered

The controls cover well hierarchy, wellbore intervals, well lifecycle, daily production by phase and disposition, production tests, separator/gauge quality, commingled allocation, meter factors, tank and LACT reconciliation, artificial lift, rod pump/ESP/gas lift/plunger operations, downtime and deferred production, workover ranking and readiness, field tickets, routes, chemicals, HSE boundaries, permits, regulatory and environmental reporting, water handling, haul tickets, integrity, surveillance, typed AppGen-X events, replayable timelines, release scenarios, production UI, pad maps, mobile capture, allocation audit UI, assistant skills, escalations, tenant/operator boundaries, lifting-cost traceability, handovers, restart checklists, injection support, target tracking, fixtures, and go-live evidence.

## Boundary assertions

- Database backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Eventing remains AppGen-X on `pbc.oil_gas_field_operations.events`.
- No stream-engine picker is exposed.
- Cross-PBC facts are represented through declared APIs, events, or projections, not shared table mutation.
- All control evaluations are side-effect free and return release evidence.
