# Pharmacy Benefits Management Implementation Status

Status: improve1 executable control slice complete for all 50 backlog features.

Evidence:
- `benefits_control.py` maps feature 1-50 to owned PBM control tables, required fields, UI surfaces, service/API routes, declared event/API/projection dependencies, tests, and release evidence.
- Runtime exposes `benefits_control` and the `evaluate_benefits_control` operation.
- UI exposes 50 PBM benefits control panels, service actions, and agent tool identifiers.
- Release evidence and validation include the pharmacy benefits management improve1 control contract.
- `tests/test_domain_behavior.py` gates formulary lifecycle, therapeutic identity, tiering, step therapy, prior authorization intake and criteria, urgent review SLAs, PA renewal, claim edits, quantity limits, refill and adherence logic, specialty routing, network contracts, rebates, utilization review, medication safety, controlled substances, affordability, substitution policy, appeals, criteria ingestion, benefit configuration, simulations, reversals, RTBC, quality metrics, FWA, member notices, prescriber collaboration, reviewer assignment, conflict detection, accumulator boundaries, shortage handling, jurisdictions, dead letters, agent summaries, governed CRUD, ethical guardrails, timelines, audit evidence rooms, cryptographic proofs, analytics, policy impact, seed scenarios, persona coverage, model registry, release simulation, boundary proof, and composition DSL exposure.

Constraints preserved:
- Allowed database backends remain PostgreSQL, MySQL, and MariaDB.
- Eventing uses the AppGen-X event contract and `pbc.pharmacy_benefits_management.events` topic.
- Cross-PBC inputs are declared as APIs, events, or projections; shared table access remains rejected.
