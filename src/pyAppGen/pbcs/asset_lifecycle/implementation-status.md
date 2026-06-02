# Asset Lifecycle Implementation Status

## Delivered Slice

Implemented a package-local executable depreciation slice for:

1. Versioned straight-line depreciation schedules.
2. Schedule revision after maintenance-driven useful-life changes.
3. Idempotent depreciation runs that replay prior evidence instead of reposting.

This replaces the prior one-shot depreciation placeholder with deterministic fixed-asset accounting behavior and aligns the exposed AppGen-X contract metadata with that runtime.

## What Was Added

- A pure depreciation engine in `depreciation_engine.py` for:
  - period normalization
  - versioned schedule construction
  - rounded line allocation that still lands on the residual target
  - schedule-line lookup for period posting and replay keys
- Runtime state for:
  - active schedule version tracking
  - schedule history per asset
  - maintenance-triggered schedule revision flags
  - depreciation run idempotency keys
- A depreciation review query surface for workbench and assistant flows.
- Service preview support for depreciation schedule revisions.
- UI and agent exposure for depreciation revision review.
- AppGen-X contract cleanup across service, route, event, handler, and release-evidence surfaces.

## Changed Files

- `src/pyAppGen/pbcs/asset_lifecycle/depreciation_engine.py`
- `src/pyAppGen/pbcs/asset_lifecycle/runtime.py`
- `src/pyAppGen/pbcs/asset_lifecycle/services.py`
- `src/pyAppGen/pbcs/asset_lifecycle/routes.py`
- `src/pyAppGen/pbcs/asset_lifecycle/events.py`
- `src/pyAppGen/pbcs/asset_lifecycle/handlers.py`
- `src/pyAppGen/pbcs/asset_lifecycle/ui.py`
- `src/pyAppGen/pbcs/asset_lifecycle/agent.py`
- `src/pyAppGen/pbcs/asset_lifecycle/release_evidence.py`
- `src/pyAppGen/pbcs/asset_lifecycle/__init__.py`
- `src/pyAppGen/pbcs/asset_lifecycle/implementation-plan.md`
- `src/pyAppGen/pbcs/asset_lifecycle/implementation-status.md`
- `src/pyAppGen/pbcs/asset_lifecycle/README.md`
- `tests/test_pbc_asset_lifecycle_implementation.py`

## Self Code Review

Review focus:

- Schedule revisions preserve prior versions instead of mutating them in place.
- Depreciation reruns for the same period return stored evidence instead of posting again.
- Service, route, event, and handler metadata all stay AppGen-X-only and keep owned-table boundaries.

Issue found and fixed:

- The first pass exposed `review_depreciation_plan` behind `asset_lifecycle.read`, which broke the existing runtime expectation that the provided depreciation/operator permission bundle unlocks all visible workbench actions. The action now uses `asset_lifecycle.depreciation`, matching the slice’s operational intent and restoring the runtime test.

## Validation

Commands run:

- `python3 -m py_compile src/pyAppGen/pbcs/asset_lifecycle/depreciation_engine.py src/pyAppGen/pbcs/asset_lifecycle/runtime.py src/pyAppGen/pbcs/asset_lifecycle/services.py src/pyAppGen/pbcs/asset_lifecycle/routes.py src/pyAppGen/pbcs/asset_lifecycle/events.py src/pyAppGen/pbcs/asset_lifecycle/handlers.py src/pyAppGen/pbcs/asset_lifecycle/ui.py src/pyAppGen/pbcs/asset_lifecycle/agent.py src/pyAppGen/pbcs/asset_lifecycle/release_evidence.py src/pyAppGen/pbcs/asset_lifecycle/__init__.py`
- `./.venv/bin/pytest tests/test_pbc_asset_lifecycle_implementation.py tests/test_pbc_asset_lifecycle_runtime.py src/pyAppGen/pbcs/asset_lifecycle/tests/test_contract.py`

Result:

- Python compilation passed.
- Focused implementation, runtime, and package contract tests passed: `14 passed`.

## Remaining Backlog

Not implemented in this slice:

- Multi-method depreciation beyond straight-line.
- Depreciation journal reconciliation against downstream ledger acknowledgements.
- Component-level partial retirement and replacement accounting.
- Multi-book divergence handling and tax-book-specific schedule policy.

Those can build on the new versioned schedule and idempotent run foundation without changing the AppGen-X event boundary.

## 2026-05-30 Domain Behavior Traceability Slice

- Expanded `tests/test_domain_behavior.py` with route, standalone repository/app, assistant document/CRUD planning, owned-boundary, depreciation preview, and release-evidence checks.
- Updated `IMPROVE1_TRACEABILITY.md` so all 50 improve1 rows cite `tests/test_domain_behavior.py` as direct asset lifecycle behavior evidence.
- Updated `improve1_capabilities.py` so every feature execution plan carries the domain behavior test artifact.
- Validation: `/Volumes/Media/src/pjs/appgen/.venv/bin/pytest src/pyAppGen/pbcs/asset_lifecycle/tests`.
