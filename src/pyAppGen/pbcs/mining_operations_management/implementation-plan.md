# Mining Operations Management Standalone Implementation Plan

## Objective

Deliver a standalone, package-local Mining Operations Management app surface that can execute realistic mine-plan-to-shift workflows without editing shared generators or language/runtime scaffolding outside this PBC.

## Current Gap Summary

- The PBC already exposes schema, runtime, route, event, handler, UI, and agent contracts, but it does not yet provide a package-local standalone app surface.
- UI coverage stops at fragments and high-level capability metadata; there are no executable forms, guided wizards, or control-center checks for mine supervisors and ore-control users.
- Release evidence only validates the generated package shell. It does not prove standalone workbench readiness, documentation presence, or form/wizard/control wiring.
- There is no focused test coverage for a realistic weekly-plan, shift-dispatch, ore-boundary, stockpile, or geotech workflow inside this one PBC.

## Domain-Deep Focus

The standalone slice emphasizes the mining decisions that change every shift, not generic CRUD wrappers. The implementation focuses on the following improvement backlog themes:

1. Hierarchical mine plan intake and plan-to-shift decomposition.
2. Drill-and-blast readiness with clearance and re-entry gating.
3. Fleet capability and dispatch assignment under route and area constraints.
4. Ore-boundary governance tied to approval and downstream destination changes.
5. Stockpile genealogy and quality-aware movement capture.
6. Geotechnical conditional access and blocked-area visibility.
7. Shift handover evidence and unresolved-risk carryover.

## Planned Package-Local Surfaces

### 1. Standalone App

- Add `standalone.py` with a deterministic `MiningOperationsManagementStandaloneApp`.
- Keep state package-local and in-memory; no shared generator or shared runtime files are modified.
- Reuse existing runtime/domain contracts for event topics, owned-table boundaries, emitted events, and rule/parameter registration.
- Add route-style dispatch helpers for a standalone workbench, controls, release evidence, and wizard planning.

### 2. Forms

- Add executable forms for mine plan hierarchy intake, blast readiness, shift targeting, fleet capability, dispatch assignment, ore-boundary decisions, stockpile movement, geotech conditional access, and shift handover.
- Keep every form bound to owned tables and named domain operations.

### 3. Wizards

- Add guided wizards for weekly plan-to-shift, blast clearance, ore-to-plant nomination, and wet-weather dispatch recovery.
- Each wizard exposes blocking context so the workbench can show why a step is or is not ready.

### 4. Controls

- Add executable controls for blast clearance, dispatch boundary proof, ore-boundary governance, stockpile genealogy integrity, and release readiness.
- Controls read standalone state and prove that the standalone workflow still respects owned-table boundaries and approval gates.

### 5. UI and Exports

- Expand `ui.py` so the workbench contract advertises forms, wizards, controls, standalone blueprint, and richer summary cards.
- Export the new package-local surfaces from `__init__.py`.
- Update the manifest to trace new docs and tests while leaving shared registration untouched.

### 6. Release Evidence

- Extend release evidence to validate standalone app contract presence, form/wizard/control coverage, implementation-plan presence, and focused standalone tests.

## Verification Plan

- Compile the PBC package with `python -m compileall`.
- Run focused pytest coverage under `src/pyAppGen/pbcs/mining_operations_management/tests`.
- Run a focused Python audit that imports the package, exercises standalone smoke, and validates release evidence.

## Non-Goals

- No edits to shared generator, DSL, language packs, or progress ledgers.
- No attempt to redesign the broader AppGen-X multi-PBC runtime.
- No new external dependencies.
