# Professional Services Automation Implementation Status

## improve1 executable completion

- Implemented `psa_control.py` as the package-local executable contract for all 50 improve1 backlog features.
- Every feature maps to a PSA-owned control table, required fields, UI panel, service/API route, test evidence, AppGen-X event contract proof, declared API/event/projection dependencies, and release evidence.
- Runtime, UI, and release evidence surfaces expose the control contract without stream-engine pickers, shared-table access, or non-owned datastore assumptions.
- `tests/test_domain_behavior.py` verifies engagement lifecycle, archetypes, SOW semantic extraction, obligation ledgers, scope/change control, role architecture, skill graphs, staffing optimization, utilization forecasts, soft bookings, subcontractor governance, rate cards, time/expense controls, milestones, deliverables, client acceptance, billing readiness, leakage, margins, fixed-price/retainer controls, delivery risk, client health, exceptions, change orders, close, project-to-cash handoff, fairness, career staffing, playbooks, knowledge reuse, retrospectives, proposal handoff, kickoff readiness, demand forecasting, simulations, model governance, control assertions, boundary proof, dead-letter replay, carbon planning, agent skills, role workbenches, executive cockpit, and release matrix proof.

## constraints

- Datastore backends remain restricted to PostgreSQL, MySQL, and MariaDB.
- Eventing remains AppGen-X only.
- Cross-PBC data is declared as API/event/projection dependencies, not shared tables.
- Agent-assisted PSA flows remain side-effect-free previews unless human approval is present.
