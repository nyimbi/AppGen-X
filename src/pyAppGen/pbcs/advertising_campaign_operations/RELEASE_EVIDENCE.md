# Release Evidence - Advertising Campaign Operations

Package directory: `src/pyAppGen/pbcs/advertising_campaign_operations`.

This slice now includes package-local models, schema/service contracts, stateful service execution, route dispatch, UI forms/wizards/controls, assistant CRUD planning, workflows, governance, handlers, standalone app wiring, release evidence, and focused package tests.

## Evidence Areas

- Schema and model contracts: owned-table schema contract plus domain model contracts for briefs, plans, launch reports, and document plans.
- Services and routes: method/path route contracts align with stateful package-local service operations.
- UI: standalone app shell exposes forms, wizards, controls, navigation, workbench cards, and launch queue output.
- Assistant: document instruction planning returns governed CRUD previews with required confirmation.
- Governance: permissions, configuration, parameters, and rule evaluation remain inside the package boundary.
- Events and handlers: AppGen-X inbox/outbox/dead-letter handling stays package-local and idempotent.

## Executed Validation

- `PYTHONPATH=src python3 -m py_compile src/pyAppGen/pbcs/advertising_campaign_operations/*.py src/pyAppGen/pbcs/advertising_campaign_operations/tests/*.py`
  - passed
- direct Python harness across `src/pyAppGen/pbcs/advertising_campaign_operations/tests/test_contract.py` and `test_standalone.py`
  - passed 9 tests
- package-local audit harness for:
  - `pyAppGen.pbcs.advertising_campaign_operations.smoke_test`
  - `pyAppGen.pbcs.advertising_campaign_operations.routes.smoke_test`
  - `pyAppGen.pbcs.advertising_campaign_operations.services.smoke_test`
  - `pyAppGen.pbcs.advertising_campaign_operations.standalone.smoke_test`
  - `pyAppGen.pbcs.advertising_campaign_operations.workflows.smoke_test`
  - `pyAppGen.pbcs.advertising_campaign_operations.release_evidence.validate_release_evidence`
  - all returned `True`

## Environment Note

- Direct `pytest` execution is currently unavailable because `/usr/local/bin/pytest` points to a missing Python 3.9 interpreter.
