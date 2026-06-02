# Implementation Status

## Completed

- Standalone executable domain engine added in `standalone.py`.
- Incident lifecycle states now include draft, triaged, recordability review, regulator notified, investigation open, corrective action open, closed, and reopened.
- Serious-incident notification clocks, acknowledgement evidence, and overdue control assertions are executable.
- Near-miss cluster promotion creates or updates hazard records with lineage.
- Corrective action verification can reopen failed actions and linked incidents.
- Permit conflict checks and offline inspection sync are executable.
- Policy change, audit seal, and KPI events are handled idempotently.
- UI/forms/wizards/controls, workflows, agent skills, docs, and release evidence are package-local.

## Remaining gaps

- The slice is in-memory and contract-focused; it does not connect to a live database adapter yet.
- Bulk ingest, export rendering, and document parsing are governed previews rather than full external integrations.
- Training lapse assertions are modeled in metadata but only lightly seeded.

## 2026-05-30 improve1 EHS-Control Execution Slice

All 50 environment health and safety improve1 backlog features are now bound to `ehs_control.py`, with package-local evaluations for owned tables, declared API/event dependencies, UI panels, service/API routes, AppGen-X eventing, PostgreSQL/MySQL/MariaDB datastore boundaries, release evidence, and focused domain behavior tests.
