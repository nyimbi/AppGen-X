# Clinical Care Coordination Implementation Plan

## Intent

Deliver `clinical_care_coordination` as a usable standalone AppGen-X PBC slice that can run as a one-PBC command-center app without shared tables. The package must remain self-contained inside `src/pyAppGen/pbcs/clinical_care_coordination` while covering the executable surfaces called out in `improve1.md`.

## Scope Chosen

This pass implements the operational care coordination slice with package-local behavior for:

- Longitudinal care-plan lifecycle, child-goal closure guards, and active-plan workbench visibility.
- Consent-aware interdisciplinary care-team rostering.
- Closed-loop referral creation and result reconciliation.
- Encounter-derived coordination tasks with source-note traceability.
- Typed care-gap creation and evidence-based closure.
- Transition-of-care packet validation and handoff completion.
- Outcome measure capture with baseline, target, current value, and trend.
- Queue-oriented workbench rendering for high-risk patients, referrals, transitions, gaps, outreach, coverage gaps, and control failures.
- Governed AI assistant document-instruction CRUD planning.
- Standalone one-PBC app bootstrapping, route dispatch, rendering, and release snapshot evidence.

## Package-Local Design

The main executable domain logic remains in `care_coordination_app.py`. This pass layers a thin package-local application shell around it:

- `services.py` dispatches real commands and queries against a stateful in-memory owned-data boundary.
- `routes.py` maps the local HTTP contract to executable service operations and local UI metadata endpoints.
- `ui.py` exposes the standalone shell contract and renders the workbench from package-owned state.
- `standalone.py` provides a one-PBC app bootstrap path and demo workspace loader.
- `config.py` uses deterministic rule compilation hashes.
- `release_evidence.py` includes standalone app readiness alongside the core package evidence.

## Validation Plan

Validation for this slice is intentionally focused and package-local:

- `python3 -m py_compile` on touched package modules and standalone tests.
- Focused package tests for contract, app slice, and standalone app behavior.
- `pbc_implementation_release_audit(("clinical_care_coordination",))`
- `pbc_generation_smoke_audit(("clinical_care_coordination",))`

## Constraints

- No edits outside `src/pyAppGen/pbcs/clinical_care_coordination`.
- No shared generator, DSL, or ledger changes.
- Reuse existing package-local patterns and state contracts rather than introducing new shared abstractions.
