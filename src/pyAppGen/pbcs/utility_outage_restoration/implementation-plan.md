# Utility Outage Restoration Implementation Plan

## Goal

Deepen `src/pyAppGen/pbcs/utility_outage_restoration` into a stronger standalone one-PBC outage-restoration package without changing global files or sibling PBCs.

## Constraints

- Stay entirely inside `src/pyAppGen/pbcs/utility_outage_restoration`.
- Preserve the package-local source audits already expected for `utility_outage_restoration`.
- Keep deployment-facing contracts on the owned PostgreSQL/MySQL/MariaDB boundary while using SQLite only as a package-local execution harness.
- Preserve AppGen-X-only eventing and keep the stream-engine picker hidden everywhere.

## Workstreams

1. Standalone outage data layer
   Add a SQLite-backed package-local store for network asset projections, outage incidents, trouble calls, OMS events, switching plans, safety isolation, damage assessments, crew dispatch, ETR revisions, notifications, mutual aid, restoration verification, regulatory indices, governed assistance, and AppGen-X event evidence.

2. Executable services and routes
   Expose package-local operations for outage triage, device interruption clustering, crew dispatch, switching/safety, storm mode, nested outage handling, and reliability calculations.

3. UI/workbench depth
   Add explicit forms, wizards, and controls for triage, crew dispatch, switching restoration, storm coordination, and governed assistance so the workbench contract is executable rather than fragment-only.

4. Agent planning depth
   Enrich document-intake and governed CRUD planning with package-local route, form, wizard, and table candidates while keeping all mutation skills confirmation-gated.

5. Release artifacts
   Materialize `README.md`, `implementation-status.md`, and updated release evidence so the standalone slice is covered by package-local readiness checks.

## Validation Plan

- `python3 -m py_compile` for modified package modules and tests
- focused `pytest` for `src/pyAppGen/pbcs/utility_outage_restoration/tests`
- `git diff --check`
- focused source/package/spec/agent/implementation/capability/generation audits scoped to `utility_outage_restoration`
