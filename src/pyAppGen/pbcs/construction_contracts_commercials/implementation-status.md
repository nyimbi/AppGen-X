# Construction Contracts and Commercials Implementation Status

## Completed

- Added an executable package-local commercial-controls core with owned schema, runtime state, rules, parameters, RBAC, event helpers, UI metadata, and release simulation.
- Rewired runtime, services, routes, UI, events, handlers, config, permissions, agent support, seed data, and manifest wrappers to use the executable core.
- Replaced scaffold tests with focused behavioral tests for lifecycle controls, overclaim rejection, waiver-gated certification, variation value control, workbench queues, agent governance, and route/handler execution.
- Added package-local documentation: `README.md`, `implementation-plan.md`, and updated `RELEASE_EVIDENCE.md`.
- Updated migration DDL to reflect the package’s domain-specific schema fields.

## Validation Evidence

- `python3 -m compileall src/pyAppGen/pbcs/construction_contracts_commercials`
  - Passed for the full package tree.
- `PYTHONPATH=src python3 -c "...runtime_smoke/service_smoke/route_smoke..."`
  - Returned `True True True`.
- `PYTHONPATH=src python3 -c "...import test_contract and execute all test_* functions..."`
  - Executed 11 focused tests.
  - Result: `failures=0`.

## Pending / Risks

- The slice is intentionally in-memory and contract-driven; it does not include a real persistence adapter or HTTP server binding inside this PBC.
- `SPECIFICATION.md` remains broader than the implemented subset and may still describe ambitions beyond the current executable slice.
- Release verification evidence should be refreshed if additional route surfaces or new governed operations are added later.
- `pytest` was not available in the active interpreter, so the focused test module was executed through a direct Python harness instead.
