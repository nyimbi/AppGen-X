# Release Evidence - Bank Payments Clearing

Package directory: `src/pyAppGen/pbcs/bank_payments_clearing`.

This standalone slice now includes executable package-local schema/model contracts, services, routes, UI/workbench metadata, AppGen-X event/handler surfaces, assistant planning, release evidence, and focused tests.

## Evidence Areas

- Source artifacts: README, implementation plan/status, release evidence, standalone app module, migration, and focused tests are present in-package.
- Owned datastore boundary: surfaced tables remain under `bank_payments_clearing_*`; cross-PBC collaboration is limited to AppGen-X event evidence and declared route/API contracts.
- Service and route execution: payment intake, release, batching, settlement, returns, reconciliation, and release snapshot paths are executable through package-local service and route contracts.
- UI and assistant surface: forms, wizards, controls, workflows, workbench shell metadata, and governed document/CRUD planning are available for a one-PBC app.
- Release gates: `pbc_source_artifact_contract`, `pbc_implementation_release_audit`, and `pbc_generation_smoke_audit` are all checked in `release_evidence.py`.

## Validation Commands

- `python3 -m compileall src/pyAppGen/pbcs/bank_payments_clearing`
- Direct Python harness over `tests/test_contract.py`, `tests/test_payment_operations.py`, and `tests/test_standalone.py`
- Package-local smoke/audit functions from runtime, routes, UI, capability assurance, standalone app, and release evidence modules
