# Release Evidence - Chemical Batch Compliance

Implemented slice: controlled formula release, batch execution evidence, quality
hold escalation, regulatory dossier assembly, and governed assistant
document-instruction CRUD.

## Evidence Scope

- owned schema and migration DDL are package-local
- service and route contracts are executable
- AppGen-X outbox, inbox, idempotency, retry, and dead-letter behavior are present
- workbench UI includes forms, wizards, controls, and assistant cards
- RBAC, configuration, rules, parameters, and seed data are package-local
- focused tests cover the implemented slice

## Expected Verification Commands

- `python -m compileall src/pyAppGen/pbcs/chemical_batch_compliance`
- `python -m pytest src/pyAppGen/pbcs/chemical_batch_compliance/tests -q`
- runtime smoke via `chemical_batch_compliance_runtime_smoke()`

## Latest Recorded Outcome

- `python3 -m compileall src/pyAppGen/pbcs/chemical_batch_compliance` -> exit `0`
- `./.venv/bin/python -m pytest src/pyAppGen/pbcs/chemical_batch_compliance/tests -q` -> exit `0`, `11 passed in 0.46s`
- runtime smoke -> `True`, with `1` open hold in the triage queue and a dossier status of `ready_for_submission`

`implementation-status.md` records the exact command text and outputs from the latest run.
