# Enterprise Risk Controls Implementation Status

## Status

Implemented as a package-local executable enterprise risk and controls slice with workbench app surfaces, assistant previews, release evidence, and focused tests, all inside `src/pyAppGen/pbcs/enterprise_risk_controls`.

## Completed

- Added `implementation-plan.md`, `README.md`, and this status file.
- Added executable `forms.py`, `wizards.py`, and `controls.py` for the one-PBC app surface.
- Replaced generic permissions, config, agent, services, routes, UI, events, handlers, service-contract, and release-evidence wrappers with enterprise-risk-specific package-local contracts.
- Wired forms, wizards, controls, control-center evidence, and assistant previews into package metadata through `__init__.py`.
- Added focused tests covering forms, wizards, controls, assistant preview, route/service visibility, UI bindings, and release evidence.

## Verification Target

- Package-local tests under `src/pyAppGen/pbcs/enterprise_risk_controls/tests`.
- Python compilation on the PBC directory.
- Package-local smoke and release-readiness checks.

## Remaining Risks

- The slice remains contract-first and side-effect-free; it does not mount a framework runtime or persist real records outside package-local smoke state.
- `SPECIFICATION.md` still reflects the generated package baseline and was not fully rewritten around the new one-PBC app-surface terminology.

## 2026-05-30 improve1 Risk-Control Execution Slice

All 50 enterprise risk/control improve1 backlog features are now bound to `risk_control.py`, with package-local evaluations for owned tables, declared API/event dependencies, UI panels, service/API routes, AppGen-X eventing, PostgreSQL/MySQL/MariaDB datastore boundaries, release evidence, and focused domain behavior tests.
