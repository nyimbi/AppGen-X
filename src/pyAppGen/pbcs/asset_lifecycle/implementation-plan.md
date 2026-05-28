## Implementation Plan

### Scope

Implement an executable fixed-asset depreciation slice for `asset_lifecycle` focused on:

- versioned depreciation schedules
- schedule revision after asset-life changes
- idempotent depreciation runs with replayable evidence
- AppGen-X-only contract exposure across runtime, services, UI, agent, and release evidence

### Why This Slice

- It is directly supported by the backlog items for depreciation method depth, schedule versioning, run idempotency, and maintenance-driven useful-life adjustment.
- The package already has basic asset registration and depreciation placeholders, so this slice can turn existing surface area into real behavior without widening scope into new dependencies.
- It stays fully inside the owned asset tables and AppGen-X event boundary.

### Current Gaps

- Depreciation schedules are single-version snapshots with no revision history.
- Depreciation runs always post the first line and do not enforce idempotency.
- Maintenance life changes do not drive a schedule revision workflow.
- Service and event metadata contain contract drift around emitted events and AppGen-X eventing details.

### Planned Changes

1. Add a package-local depreciation engine that:
   - computes straight-line schedules against remaining carrying value
   - versions schedules while preserving prior versions
   - recalculates remaining-life schedules after maintenance-driven life changes
   - preserves exact residual-value landing through rounded line allocation
2. Update runtime behavior to:
   - track active schedule version per asset
   - mark assets as requiring schedule revision after life changes
   - post only the due period line during a depreciation run
   - store run idempotency evidence and replay prior run results on duplicates
   - expose a depreciation review/query surface for workbench and assistant use
3. Update package exposure to:
   - align service/event/handler metadata to AppGen-X-only topics and owned tables
   - expose depreciation review in the UI and agent surfaces
   - include release-evidence checks for schedule versioning and run idempotency
4. Add focused tests for:
   - schedule revision history after life-extension
   - idempotent rerun behavior
   - service/UI/agent/release-evidence exposure and contract alignment

### Files To Change

- `src/pyAppGen/pbcs/asset_lifecycle/depreciation_engine.py`
- `src/pyAppGen/pbcs/asset_lifecycle/runtime.py`
- `src/pyAppGen/pbcs/asset_lifecycle/services.py`
- `src/pyAppGen/pbcs/asset_lifecycle/ui.py`
- `src/pyAppGen/pbcs/asset_lifecycle/agent.py`
- `src/pyAppGen/pbcs/asset_lifecycle/events.py`
- `src/pyAppGen/pbcs/asset_lifecycle/handlers.py`
- `src/pyAppGen/pbcs/asset_lifecycle/release_evidence.py`
- `src/pyAppGen/pbcs/asset_lifecycle/__init__.py`
- `src/pyAppGen/pbcs/asset_lifecycle/implementation-status.md`
- `src/pyAppGen/pbcs/asset_lifecycle/README.md`
- `tests/test_pbc_asset_lifecycle_implementation.py`

### Constraints

- Keep AppGen-X as the only eventing contract.
- Stay within owned asset-lifecycle tables and declared dependencies.
- Do not add dependencies.
- Keep the diff package-local to `src/pyAppGen/pbcs/asset_lifecycle` and the assigned implementation test.

### Verification Plan

- `python3 -m py_compile` on modified Python files
- `./.venv/bin/pytest tests/test_pbc_asset_lifecycle_implementation.py`
- `./.venv/bin/pytest tests/test_pbc_asset_lifecycle_runtime.py src/pyAppGen/pbcs/asset_lifecycle/tests/test_contract.py`
