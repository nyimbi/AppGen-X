# Implementation Plan

## Goal

Turn `src/pyAppGen/pbcs/cybersecurity_operations_center` from a thin contract scaffold into a package-local, standalone one-PBC app slice with executable owned-model contracts, workflow services, route dispatch, UI/workbench metadata, governed agent planning, focused tests, and release evidence without touching any global files or other PBCs.

## Scope Chosen From `improve1.md`

The package does not need all fifty backlog items to become credible. This implementation concentrates on the smallest coherent slice that unlocks a standalone SOC app:

1. Alert lifecycle and detection-aware intake.
2. Deduplication/correlation and triage/enrichment commands.
3. Incident promotion preview with explainable severity.
4. Evidence chain-of-custody and sealing readiness.
5. Containment approval boundaries and staged playbook execution.
6. Workbench lanes, case detail graph, supervisor/evidence-review views.
7. AppGen-X inbox/outbox/dead-letter lineage.
8. Governed agent CRUD/document planning and shift handoff packet generation.
9. Focused package tests and release evidence aligned to requested gates.

## Architecture

### Owned Models and Schema

- `models.py` is the single source of truth for:
  - owned table names
  - typed record dataclasses
  - lifecycle enums and transition rules
  - parameter bounds
  - default policy bundle
  - SQL table definitions for migration/contract generation
- `migrations/001_initial.sql` mirrors the owned-table contract with explicit columns for alert lifecycle, incident ownership, evidence custody, playbook stages, and AppGen-X event tables.

### Runtime and Services

- `runtime.py` owns the package state machine and exposes executable commands/queries:
  - alert intake, enrich, transition, suppress
  - incident promotion
  - asset exposure review
  - threat intel approval
  - playbook simulation
  - containment creation
  - evidence capture
  - control assertion and governed model registration
  - workbench/detail/handoff/assessment/document parsing
- `services.py` wraps the runtime in a package-local service façade with explicit command/query operation contracts.
- `routes.py` maps stable HTTP-style route contracts onto the service surface.

### UI / Workbench

- `ui.py` exposes:
  - triage lanes
  - supervisor and evidence-review surfaces
  - forms
  - wizards
  - controls
  - assistant panel metadata
  - case detail graph/timeline tabs

### Events and Handlers

- `events.py` defines the AppGen-X event contract and envelope builder.
- `handlers.py` runs bounded consumed-event handling with idempotency and dead-letter evidence.

### Agent Surface

- `agent.py` provides:
  - triage summary skills
  - missing evidence skills
  - threat-intel recommendation skills
  - handoff packet planning
  - owned-table-only CRUD planning
  - document instruction planning with mutation previews

## Validation Strategy

### Focused Tests

- Contract coverage:
  - schema/service/release evidence
  - metadata/discovery smoke
  - route and event contracts
  - governance and agent surfaces
- Workflow coverage:
  - alert lifecycle and dedup
  - incident promotion
  - evidence custody
  - containment approval
  - workbench/detail/handoff projections

### Package Audits

- `python3 -m compileall .`
- focused `unittest` for `tests.test_contract` and `tests.test_workflows`
- file diagnostics on modified Python modules where available

## Requested Gate Mapping

- `pbc_source_artifact_contract`
  - satisfied by owned schema/model/service/route/event/agent/UI contracts and package docs.
- `pbc_implementation_release_audit`
  - satisfied by runtime smoke, workflow tests, and `RELEASE_EVIDENCE.md`.
- `pbc_generation_smoke_audit`
  - satisfied by package smoke plus the generated workbench/detail/handoff projections exercised in tests.

## Non-Goals For This Slice

- External network/SIEM/SOAR integrations.
- Cross-PBC writes.
- Full production persistence engine beyond owned schema contracts and executable in-package state logic.
- Background schedulers or asynchronous workers outside package-local smokeable behavior.

## Deliverables

- Updated package-local code only.
- `README.md`
- `implementation-status.md`
- `RELEASE_EVIDENCE.md`
- focused test suite and validation evidence
