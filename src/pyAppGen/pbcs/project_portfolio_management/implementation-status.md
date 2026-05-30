# Project Portfolio Management Implementation Status

## improve1 executable completion

- Implemented `ppm_control.py` as the package-local executable contract for all 50 improve1 backlog features.
- Every feature maps to a PPM-owned control table, required fields, UI panel, service/API route, test evidence, AppGen-X event contract proof, declared API/event/projection dependencies, and release evidence.
- Runtime, UI, and release evidence surfaces expose the control contract without stream-engine pickers, shared-table access, or non-owned datastore assumptions.
- `tests/test_domain_behavior.py` verifies strategic objective graphs, intake readiness, archetypes, business-case assumptions, benefit hypotheses, scoring governance, multi-objective prioritization, capital allocation, capacity and conflicts, dependency analysis, stage gates, lifecycle flow, executive scenarios, real options, risk appetite, issues, change impact, benefits attribution, financial variance, funding tranches, stop/pause/pivot controls, health fusion, predictive risk, agendas, authority, policy studio, parameter simulation, control assertions, audit reconstruction, cryptographic proofs, document ingestion, business-case critique, exceptions, intake marketplace, stakeholder maps, compliance commitments, sustainability, anomaly detection, continuous close, evidence-cited narrative, role workbenches, and release matrix proof.

## constraints

- Datastore backends remain restricted to PostgreSQL, MySQL, and MariaDB.
- Eventing remains AppGen-X only.
- Cross-PBC data is declared as API/event/projection dependencies, not shared tables.
- Agent-assisted portfolio governance flows remain side-effect-free previews unless human approval is present.
