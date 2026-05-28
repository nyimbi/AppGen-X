# Construction Project Controls Implementation Plan

## Goal

Turn `construction_project_controls` into a coherent one-PBC construction controls app slice that stays fully package-local and executable. The slice chosen from `improve1.md` centers on WBS hierarchy, baseline freeze, quantity-driven progress, earned-value rollups, float-based exception handling, governed assistant previews, and release-readiness evidence.

## Scope

- Keep all edits under `src/pyAppGen/pbcs/construction_project_controls`.
- Do not touch the central generator, shared DSL, or other PBCs.
- Preserve the owned datastore boundary and AppGen-X event contract.
- Prefer one coherent operational slice over broad placeholder coverage.

## Work Items

1. Replace placeholder runtime behavior with an executable domain slice
   - Add project, baseline, work-package, progress, risk, change, and reporting-period logic.
   - Compute WBS rollups, EV metrics, forecast confidence, and exception state package-locally.

2. Align package-local wrappers to the runtime
   - Update services, routes, UI, agent, config, permissions, events, handlers, and release evidence.
   - Ensure the compatibility alias `POST /site-progresss` remains supported.

3. Add one-PBC app surfaces
   - Add package-local `forms.py`, `wizards.py`, and `controls.py`.
   - Surface the forms, wizards, and controls through the UI and package metadata.

4. Add realistic seeds and release artifacts
   - Seed on-track, delayed, change-heavy, and contractor-overstatement scenarios.
   - Refresh `README.md`, `RELEASE_EVIDENCE.md`, and `implementation-status.md`.

5. Add focused tests and smoke checks
   - Cover baseline approval, WBS/progress/EV flow, float escalation, assistant previews, route alias support, and package contract surfaces.

## Non-Goals

- No central AppGen-X generator or DSL changes.
- No cross-PBC schema or route coupling.
- No third-party dependencies.

## Verification Plan

- Run `pytest` for `src/pyAppGen/pbcs/construction_project_controls/tests`.
- Run Python compilation on the package-local modules.
- Run package-local smoke imports for runtime, routes, services, UI, and release evidence.
