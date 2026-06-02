# Production Control Implementation Status

## improve1 executable completion

- Implemented `production_control_control.py` as the package-local executable contract for all 50 improve1 backlog features.
- Every feature maps to a production-owned control table, required fields, UI panel, service/API route, test evidence, AppGen-X event contract proof, declared API/event/projection dependencies, and release evidence.
- Runtime, UI, and release evidence surfaces expose the control contract without stream-engine pickers, shared-table access, or non-owned datastore assumptions.
- `tests/test_domain_behavior.py` verifies work center readiness, routing, finite scheduling, dispatch, operation sequencing, starts, pauses/splits/merges, confirmations, material/WIP, labor/machine time, downtime/OEE, maintenance projections, quality gates, scrap/rework, completion and asset handoff, exceptions, capacity allocation, simulations, carbon scheduling, audit, policy screening, event reliability, boundary proof, agent safety, anomaly/model governance, resilience, crypto authorization, handover, readiness, and end-to-end execution proof.

## constraints

- Datastore backends remain restricted to PostgreSQL, MySQL, and MariaDB.
- Eventing remains AppGen-X only.
- Cross-PBC data is declared as API/event/projection dependencies, not shared tables.
- Agent-assisted shop-floor flows remain side-effect-free previews unless human approval is present.
