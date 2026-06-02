## Agriculture Farm Operations Implementation Plan

### Goal
Turn `agriculture_farm_operations` into a package-local one-PBC standalone app surface that can bootstrap demo state, dispatch package routes, render a workbench, and emit release evidence without touching shared AppGen-X code.

### Standalone slice chosen from the backlog
- `2. Season-aware crop plans`
- `3. Planting-window intelligence`
- `5. Pre-plant readiness gate`
- `33. Missed-window and blocked-operations inbox`
- `34. Agronomist copilot skill`
- `36. Document-to-draft agronomy intake`
- `49. Release evidence pack for farm-operation changes`

### Why this slice
- The package already has executable crop-plan logic, so the smallest correct standalone app is to wrap that logic with package-local services, routes, UI, workflows, permissions, assistant planning, and tests.
- These backlog items reinforce each other in one user-visible workbench: field setup, crop-plan intake, blocked-operation triage, assistant planning, and release assurance.
- The slice stays entirely inside `src/pyAppGen/pbcs/agriculture_farm_operations` and keeps eventing on the fixed AppGen-X contract.

### Package-local scope
- Add `standalone.py` with a package-owned app shell, bootstrap flow, workbench rendering entrypoint, and release snapshot.
- Upgrade runtime, services, routes, UI, agent, configuration, permissions, models, and release evidence contracts to describe and execute the standalone slice.
- Reuse the existing crop-plan evaluation logic as the domain core instead of broadening into unrelated irrigation or harvest implementations.
- Add focused tests under `src/pyAppGen/pbcs/agriculture_farm_operations/tests` only.

### Behavior to implement
1. Keep field creation and crop-plan recording executable through package-local runtime and service commands.
2. Expose route contracts and a dispatch path for runtime setup, field intake, crop-plan intake, workbench queries, release evidence, and assistant surface queries.
3. Render a one-PBC workbench with forms, wizards, controls, cards, workflow runs, planting-window alerts, and blocked-operation queues.
4. Add assistant/document-intake planning and governed CRUD planning that only targets package-owned tables and always requires human confirmation for mutations.
5. Tighten configuration, rules, parameters, permissions, and release evidence around the standalone slice.
6. Keep all datastore references, emitted events, consumed events, and handler flows inside AppGen-X and package-owned boundaries.

### Verification plan
- Compile the package: `python3 -m compileall src/pyAppGen/pbcs/agriculture_farm_operations`
- Run focused tests:
  - `src/pyAppGen/pbcs/agriculture_farm_operations/tests/test_contract.py`
  - `src/pyAppGen/pbcs/agriculture_farm_operations/tests/test_standalone.py`
  - `tests/test_pbc_agriculture_farm_operations_implementation.py`
  - `tests/test_pbc_agriculture_farm_operations_runtime.py`
- Run available PBC audits for this package only:
  - `pbc_implementation_release_audit(("agriculture_farm_operations",))`
  - `pbc_implemented_capability_audit(("agriculture_farm_operations",))`

### Non-goals
- No shared generator, DSL, or progress-ledger edits.
- No external persistence, shared-table coupling, or non-AppGen-X eventing.
- No attempt to implement the entire agronomy backlog beyond this standalone crop-planning-centered slice.
