# Implementation Status

## Completed in This Slice

- Added a written implementation plan based on the AR backlog and the existing
  runtime, service, UI, agent, and release-evidence surfaces.
- Implemented `receivables_workflows.py` with executable onboarding review,
  invoice readiness review, receipt application, and collections follow-up
  workflows.
- Upgraded `services.py` from metadata-only planning into executable wrappers
  that keep the stable `command_ar_*` and `query_ar_*` contract names.
- Extended `runtime.py` cash application behavior to persist explicit cash
  application records and emit richer release evidence for the workflow slice.
- Extended `agent.py`, `ui.py`, and `release_evidence.py` so the executable
  slice is exposed consistently across assistant, workbench, and readiness
  evidence surfaces.
- Added focused implementation tests in
  `tests/test_pbc_ar_credit_implementation.py`.
- Added this status file and a package `README.md`.

## Review Notes

- The new workflow slice uses only owned AR tables and package-local state.
- AppGen-X remains the only event contract exposed by the implemented slice.
- No stream-engine selection or shared-table access was introduced.
- The service layer now executes real AR behavior for the selected backlog
  slice instead of returning metadata only.

## Validation Evidence

- `./.venv/bin/python -m py_compile src/pyAppGen/pbcs/ar_credit/__init__.py src/pyAppGen/pbcs/ar_credit/runtime.py src/pyAppGen/pbcs/ar_credit/services.py src/pyAppGen/pbcs/ar_credit/ui.py src/pyAppGen/pbcs/ar_credit/agent.py src/pyAppGen/pbcs/ar_credit/release_evidence.py src/pyAppGen/pbcs/ar_credit/receivables_workflows.py tests/test_pbc_ar_credit_implementation.py`
- `./.venv/bin/pytest tests/test_pbc_ar_credit_implementation.py tests/test_pbc_ar_credit_runtime.py src/pyAppGen/pbcs/ar_credit/tests/test_contract.py -q`

## Remaining Depth for Later Slices

- Expand dispute resolution from recommendation-only into full owned-case
  lifecycle state.
- Add promise-to-pay and collector work queue execution.
- Deepen credit policy compilation for temporary limits, authority bands, and
  review cadence.
- Add more generated-app coverage that exercises the new workflow operations
  through route dispatch and composed app surfaces.
