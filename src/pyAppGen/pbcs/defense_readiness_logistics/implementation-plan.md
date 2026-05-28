# Defense Readiness Logistics Implementation Plan

## Objective

Make `defense_readiness_logistics` usable as a standalone AppGen-X application when selected as the only PBC. The PBC must provide database-backed owned records, executable command services, forms, wizards, blocking controls, a workbench, assistant skills, AppGen-X event evidence, and release proof without depending on any other PBC's tables.

## Domain Scope

This PBC owns the operational lifecycle for unit readiness, mission assets, maintenance status, supply readiness, deployment kits, movement orders, personnel qualifications, ammunition lots, fuel allocations, load plans, theater support requests, controlled-item custody, and readiness exceptions.

The package deliberately treats cross-PBC dependencies as future API/event projections only. It does not read or mutate foreign tables.

## Implementation Slices

1. Standalone app runtime
   - Add an in-memory executable readiness state used by generated tests and generated single-PBC apps.
   - Preserve PostgreSQL, MySQL, and MariaDB as the only ordinary database backend choices.
   - Emit only AppGen-X outbox events and keep stream-engine choice hidden.

2. Readiness command surface
   - Implement unit readiness assessment with personnel, certification, asset, supply, ammunition, fuel, and inspection blockers.
   - Implement mission asset registration and serviceability tracking.
   - Implement maintenance projection with parts, deferrals, projected return, safety blockers, and readiness impact.
   - Implement supply readiness scoring across demand, on-hand, in-transit, approved substitutes, ammunition restrictions, and fuel gaps.
   - Implement deployment kit validation, movement planning, load-plan checks, and final deployment release gates.

3. Single-PBC user experience
   - Surface forms for readiness, assets, maintenance, supply, deployment kits, movement orders, release approvals, and controlled custody.
   - Surface wizards for readiness validation, mission capability rollup, deployment release, maintenance recovery, movement order approval, and first-run app launch.
   - Surface blocking controls for certification, asset availability, serviceability, supply/ammunition/fuel, kit completeness, movement load/route, classification/redaction, and offline sync conflicts.

4. Agent and document intake
   - Route movement orders, maintenance narratives, supply shortage memos, asset documents, and readiness reports to domain-specific mutation plans.
   - Use stable document hashing for repeatable plans.
   - Require human confirmation and citations for mutations.

5. Service and release evidence
   - Make service methods execute the domain app commands and retain package-local state.
   - Extend release evidence with single-PBC app, forms, wizards, controls, and smoke proof.
   - Add package-local tests for the end-to-end executable flow.

## Acceptance Checks

- Package tests pass.
- Runtime smoke includes the single-PBC app smoke.
- Release evidence includes app, forms, wizards, controls, UI, agent, services, schema, events, and handlers.
- All owned data references remain inside `defense_readiness_logistics_*` tables.
- Generated users can start with one PBC and still receive a functional domain app with forms, controls, wizards, service commands, workbench views, agent assistance, and database-backed records.
