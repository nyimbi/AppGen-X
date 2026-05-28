# Customer 360 Implementation Plan

## Goal

Deepen `src/pyAppGen/pbcs/customer_360` into a stronger standalone one-PBC package without changing global files or other PBCs.

## Constraints

- Stay entirely inside `src/pyAppGen/pbcs/customer_360`.
- Preserve repo-level source-package gates already expected for `customer_360`.
- Keep deployment-facing contracts on the package’s owned PostgreSQL/MySQL/MariaDB boundary while allowing a package-local sqlite dev harness for focused execution and testing.

## Workstreams

1. Package-local standalone data layer
   Add a sqlite-backed owned-table slice for profiles, identities, consents, preferences, touchpoints, engagement events, merge cases, and AppGen-X inbox/outbox/dead-letter evidence.

2. Executable services and routes
   Expose a package-local service and route surface for profile onboarding, consent/preference editing, touchpoint capture, engagement ingestion, merge handling, timeline queries, workbench queries, and inbox event processing.

3. UI/workbench depth
   Add explicit forms, wizards, and control catalogs so the workbench contract is not just fragments and panels.

4. Agent planning depth
   Enrich document-intake and CRUD planning with standalone route, form, wizard, and table candidates.

5. Release artifacts
   Materialize README, implementation status, and release evidence that now covers the standalone slice as part of package-local readiness.

## Validation Plan

- `py_compile` for modified package modules
- focused `pytest` for `src/pyAppGen/pbcs/customer_360/tests`
- repo-level audits scoped to `customer_360`
