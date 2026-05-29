# Advertising Campaign Operations

This package now exposes a standalone, package-local AppGen-X slice for advertising campaign planning, launch readiness, assistant CRUD planning, and release evidence.

## Implemented Standalone Slice

- Canonical campaign brief normalization and deterministic campaign-plan creation.
- Launch-readiness review with explicit blockers and launch-attempt handling.
- Package-local standalone app surface with in-memory state ownership.
- Route, service, UI, workflow, permission, configuration, assistant, and release-evidence contracts aligned to the implemented slice.
- Focused package tests under `src/pyAppGen/pbcs/advertising_campaign_operations/tests`.

## Package Entry Points

- `standalone.py`
  - `AdvertisingCampaignOperationsStandaloneApp`
  - `standalone_app_manifest`
  - `smoke_test`
- `services.py`
  - `AdvertisingCampaignOperationsService`
  - `service_operation_contracts`
- `routes.py`
  - `api_route_contracts`
  - `dispatch_route`
- `ui.py`
  - `advertising_campaign_operations_standalone_app_contract`
  - `advertising_campaign_operations_render_standalone_app`
- `agent.py`
  - `campaign_brief_preview`
  - `launch_readiness_preview`
  - `document_instruction_plan`
- `release_evidence.py`
  - `build_release_evidence`

## Behavior Summary

The implemented slice requires every campaign brief to provide:

- `objective`
- `offer`
- `audience_promise`
- `channels`
- `primary_kpi`
- `guardrails`
- `launch_dependencies`

Equivalent briefs normalize to the same deterministic fingerprint. Launch attempts stay blocked until budget, creative, audience, placements, tracking, supplier, and policy readiness are all satisfied and all declared dependencies are marked ready.

## Validation Evidence

Executed in the isolated worktree:

- `PYTHONPATH=src python3 -m py_compile src/pyAppGen/pbcs/advertising_campaign_operations/*.py src/pyAppGen/pbcs/advertising_campaign_operations/tests/*.py`
  - passed
- `PYTHONPATH=src python3 - <<'PY' ...`
  - direct execution harness passed 9 package-local tests from `test_contract.py` and `test_standalone.py`
- `PYTHONPATH=src python3 - <<'PY' ...`
  - package, routes, services, standalone, workflows, and release-evidence smoke/audit entry points all returned `True`

Environment note:

- `pytest` could not be used directly because `/usr/local/bin/pytest` points to a missing Python 3.9 interpreter on this machine.
