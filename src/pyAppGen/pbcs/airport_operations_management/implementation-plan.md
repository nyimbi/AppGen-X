# Airport Operations Management Implementation Plan

## Target Slice

Implement a real executable slice of backlog item 1, "Gate and stand compatibility matrix with operational constraints," with a small extension into assistant decision rationale. The slice must stay package-local and remain aligned with AppGen-X contracts and ordinary relational backends.

## Scope

1. Add a package-local compatibility evaluator for gate and stand planning.
2. Produce machine-readable reject reasons for blocked assignments.
3. Wire the evaluator into runtime command/query paths so an assignment request can be accepted or rejected for operational reasons.
4. Surface decision-support metadata in service, UI, and agent contracts.
5. Add focused tests for narrowbody, widebody, international, remote-stand, and adjacent-shadow scenarios.

## Planned File Touches

- `src/pyAppGen/pbcs/airport_operations_management/compatibility.py`
  Real decision logic for stand evaluation, compatibility matrix building, and decision explanation.
- `src/pyAppGen/pbcs/airport_operations_management/runtime.py`
  Runtime entry points for compatibility evaluation, command execution, workbench summaries, and smoke coverage.
- `src/pyAppGen/pbcs/airport_operations_management/services.py`
  Query exposure for compatibility planning.
- `src/pyAppGen/pbcs/airport_operations_management/ui.py`
  Decision-support panels and workbench metadata.
- `src/pyAppGen/pbcs/airport_operations_management/agent.py`
  Assistant-facing rationale surface for stand selection and rejection explanation.
- `tests/test_pbc_airport_operations_management_implementation.py`
  Focused execution tests for the implemented slice.

## Explicit Non-Goals

- Full turnaround milestone graph implementation.
- Full runway/taxiway operating model.
- New external datastore dependencies beyond PostgreSQL, MySQL, or MariaDB.
- Any event model outside the AppGen-X contract.
- Broad route proliferation or unrelated package refactors.

## Acceptance Signals

1. A viable stand is selected for compatible flight/stand combinations.
2. Blocked combinations return machine-readable reason codes.
3. Rejected assignment commands emit the AppGen-X exception event path.
4. Workbench and assistant surfaces expose decision-support metadata.
5. Focused tests pass for compatibility and rejection scenarios.
