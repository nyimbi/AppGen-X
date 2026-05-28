## Agriculture Farm Operations Implementation Plan

### Goal
Implement a real executable slice from the backlog by turning `record_crop_plan` into meaningful farm-operations behavior instead of a generic placeholder.

### Chosen backlog slice
- `2. Season-aware crop plans`
- `3. Planting-window intelligence`
- `5. Pre-plant readiness gate`

### Why this slice
- The package already exposes `POST /crop-plans` and `record_crop_plan`, so crop planning is the cleanest place to add real domain behavior without expanding scope into unrelated tables.
- These three backlog items reinforce each other: a crop plan is only useful when it is season-aware, checked against a planting window, and blocked when prerequisites are incomplete.
- The slice is executable and testable with package-local pure logic plus runtime integration.

### Package-local scope
- Add a package-local planning module for crop-plan evaluation.
- Extend runtime state to track crop plans and planning exceptions.
- Add a concrete `agriculture_farm_operations_record_crop_plan(...)` runtime command.
- Surface the result in service and workbench responses.
- Add focused tests in `tests/test_pbc_agriculture_farm_operations_implementation.py`.
- Write implementation status and package README after verification and self review.

### Behavior to implement
1. Normalize and validate a crop-plan request.
2. Detect overlapping active plans on the same field or management zone for the same season window.
3. Support replant linkage so a replacement plan can intentionally supersede a prior failed plan.
4. Classify the planting date as `early`, `optimal`, `late`, or `missed` using explicit planting-window inputs.
5. Evaluate a pre-plant readiness checklist and block execution when required prerequisites are incomplete.
6. Emit only AppGen-X event metadata and keep owned-table boundaries package-local.
7. Return workbench-ready summaries for accepted plans and blocked exceptions.

### Verification plan
- Run targeted package tests:
  - `tests/test_pbc_agriculture_farm_operations_implementation.py`
  - `tests/test_pbc_agriculture_farm_operations_runtime.py`
  - `src/pyAppGen/pbcs/agriculture_farm_operations/tests/test_contract.py`
- Run a package-local compile check for `src/pyAppGen/pbcs/agriculture_farm_operations`.

### Non-goals for this slice
- No new datastore backend beyond PostgreSQL/MySQL/MariaDB.
- No external integrations, stream-engine picker, or non-AppGen-X event contract.
- No broad schema rewrite across unrelated PBC modules.
