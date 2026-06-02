# Banking Core Accounts Implementation Status

## Outcome

Implemented an executable deposit-account lifecycle slice that makes `banking_core_accounts` usable as a one-PBC app for this domain slice. The package now exposes database-backed lifecycle fields, executable lifecycle commands and queries, package-local forms, wizards, controls, workflow surfaces, permission mapping, assistant/document CRUD planning, workbench views, release evidence, and lifecycle-focused tests.

## Code-Review Findings Resolved

1. Standalone app workflows were implied but not executable. Fixed by adding explicit package-local workflow contracts and wiring them into runtime, UI, services, and release evidence.
2. Permission handling did not explain which roles could execute which domain operation. Fixed by adding operation-to-permission mapping, role permissions, and assistant-facing permission previews.
3. Assistant document-instruction planning did not carry workflow, route, or CRUD execution metadata. Fixed by enriching document and CRUD plans with workflow selection, route preview, required permission, and confirmation policy.

## Validation Evidence

### Passed

Command:

```bash
/Volumes/Media/src/pjs/appgen/.venv/bin/python -m compileall /private/tmp/appgen-pbc-banking-core-accounts-standalone/src/pyAppGen/pbcs/banking_core_accounts
```

Result:

- Exit code `0`
- Package modules and focused tests compiled successfully

Command:

```bash
PYTHONPATH=/private/tmp/appgen-pbc-banking-core-accounts-standalone/src /Volumes/Media/src/pjs/appgen/.venv/bin/python -m pytest /private/tmp/appgen-pbc-banking-core-accounts-standalone/src/pyAppGen/pbcs/banking_core_accounts/tests -q
```

Result:

- Exit code `0`
- `12 passed in 1.96s`

Command:

```bash
PYTHONPATH=/private/tmp/appgen-pbc-banking-core-accounts-standalone/src /Volumes/Media/src/pjs/appgen/.venv/bin/python -c "from pyAppGen.pbcs.banking_core_accounts.runtime import banking_core_accounts_runtime_smoke; smoke=banking_core_accounts_runtime_smoke(); print(smoke['ok']); print(smoke['workflow_surface']['workflow_state_coverage'][0]['workflow_id']); print(len(smoke['app_surface']['workflows']))"
```

Result:

- Exit code `0`
- `True`
- `banking_core_accounts_create_deposit_account_workflow`
- `3`

Command:

```bash
PYTHONPATH=/private/tmp/appgen-pbc-banking-core-accounts-standalone/src /Volumes/Media/src/pjs/appgen/.venv/bin/python -c "from pyAppGen.pbcs.banking_core_accounts.capability_assurance import validate_table_stakes_capability_coverage; from pyAppGen.pbcs.banking_core_accounts.release_evidence import validate_release_evidence; print(validate_table_stakes_capability_coverage()['ok']); print(validate_release_evidence()['ok'])"
```

Result:

- Exit code `0`
- `True`
- `True`

## Changed Files

- `agent.py`
- `implementation-plan.md`
- `implementation-status.md`
- `README.md`
- `RELEASE_EVIDENCE.md`
- `SPECIFICATION.md`
- `manifest.py`
- `permissions.py`
- `release_evidence.py`
- `runtime.py`
- `services.py`
- `tests/test_contract.py`
- `tests/test_lifecycle_app.py`
- `ui.py`
- `workflows.py`

## Remaining Risks

- The earlier lifecycle-only slice has been superseded by `account_control.py`, which now covers balance decomposition, hold waterfalls, overdraft rules, statements, mandates, restrictions, reconciliation, assistant behavior, sealing, and release gates from `improve1.md`.
- Permission planning is executable metadata for this standalone slice; it is not yet connected to a shared auth provider or external identity system.

## improve1 Full Traceability Evidence

Branch: `pbc/improve1-full-traceability`

Current slice evidence:

- Added `account_control.py` as executable, side-effect-free domain code for all 50 `improve1.md` banking-core account controls.
- Bound account-control evidence into `runtime.py` release evidence and `ui.py` account-control panels so every feature has a surfaced workbench/control entry.
- Added `tests/test_domain_behavior.py` to exercise all 50 control primitives plus runtime, UI, route, service, agent, database-backend, and owned-table boundary behavior.
- Updated `IMPROVE1_TRACEABILITY.md` so all 50 rows point to `account_control.py` and `tests/test_domain_behavior.py` as direct executable evidence.
- Updated `improve1_capabilities.py` so every capability registry row names the account-control artifact and domain behavior test.

Verification log:

- Passed: `/Volumes/Media/src/pjs/appgen/.venv/bin/pytest src/pyAppGen/pbcs/banking_core_accounts/tests` (`21 passed`).
- Passed: improve1 traceability/capability/runtime sweep across all PBCs (`877 passed`).
- Passed: `git diff --check -- src/pyAppGen/pbcs`.
