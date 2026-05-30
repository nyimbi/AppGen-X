# Construction Project Controls Implementation Status

## Status

Implemented as a package-local executable construction controls slice inside `src/pyAppGen/pbcs/construction_project_controls`.

## Completed

- Replaced placeholder runtime logic with executable project, baseline, work-package, progress, risk, change, and reporting-period behavior.
- Added package-local `forms.py`, `wizards.py`, and `controls.py` and wired them into the UI, assistant, release evidence, and package metadata.
- Added domain-specific configuration, rules, parameters, RBAC, AppGen-X events, idempotent handlers, seed scenarios, and release-readiness scorecard support.
- Added package-local `README.md`, `implementation-plan.md`, and focused tests for WBS rollups, EV metrics, route aliases, assistant previews, and package contracts.

## Verification Target

- Package-local tests under `src/pyAppGen/pbcs/construction_project_controls/tests`
- Python compilation for the modified package
- Import-based package smoke for runtime, services, routes, UI, and release evidence

## Verification Performed

- `python3 -m compileall src/pyAppGen/pbcs/construction_project_controls`
- `python3 -c "import sys; sys.path.insert(0,'src'); ..."` package smoke covering package, service, route, UI, and single-PBC app contract
- Direct import runner that executed all `test_*` functions in:
  - `tests/test_contract.py`
  - `tests/test_app_slice.py`

`pytest` was not installed in the available interpreter, so the package-local tests were executed directly via Python imports instead of the `pytest` CLI.

## Remaining Risks

- The slice is still framework-light: services and routes are executable facades, not mounted HTTP handlers.
- `SPECIFICATION.md` remains broader than the newly implemented slice, so the new `README.md`, tests, and release evidence are the more accurate description of the current package behavior.

## 2026-05-30 improve1 Project-Control Execution Slice

- Added `project_control.py` as side-effect-free executable proof for all 50 improve1 construction project-controls capabilities.
- Bound each feature to owned tables, AppGen-X event metadata, UI/API route surfaces, agent skills, configuration handles, retry/dead-letter evidence, and traceability artifacts.
- Added package-local domain behavior tests for WBS hierarchy, baseline approval, progress evidence, schedule quality, change approval, assistant/document governance, adjacent-system boundaries, closeout blockers, and go-live readiness.
- Updated runtime, UI, release evidence, and improve1 traceability so every feature row points to executable project-control behavior and `tests/test_domain_behavior.py`.
