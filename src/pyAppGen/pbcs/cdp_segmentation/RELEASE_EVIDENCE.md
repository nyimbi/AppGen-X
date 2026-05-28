# Customer Data Platform Segmentation Release Evidence

Directory: `src/pyAppGen/pbcs/cdp_segmentation`

## Release Gate Summary

- Runtime scope: one executable CDP segmentation slice with AppGen-X-only eventing
- Boundary policy: owned tables only, declared consumed events and projection dependencies only
- Verification mode in this environment: compile/import/smoke execution

## Evidence Areas

- owned schema contract and model coverage
- executable service and route surface
- AppGen-X outbox, inbox, idempotency, retry, and dead-letter handling
- runtime permissions, configuration schema, parameter bounds, and rule governance
- workbench UI with forms, wizards, controls, alerts, and release panels
- agent/chatbot document-instruction and governed CRUD planning support
- package-local docs: `README.md`, `implementation-plan.md`, `implementation-status.md`
- package-local tests: `tests/test_contract.py`, `tests/test_execution.py`

## Expected Readiness Checks

- `owned_schema_depth`
- `migration_per_owned_table`
- `model_per_owned_table`
- `service_contract_depth`
- `appgen_event_contract_only`
- `backend_allowlist`
- `permissions_cover_release_queries`
- `runtime_event_tables_owned`
- `no_shared_table_access`
- `documentation_present`
- `package_local_tests_present`
