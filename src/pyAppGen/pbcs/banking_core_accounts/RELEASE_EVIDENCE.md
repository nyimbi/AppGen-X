# Release Evidence - Banking Core Accounts

## Implemented Domain Slice

This release evidence covers the executable deposit-account lifecycle slice delivered inside `banking_core_accounts`.

## Evidence Summary

- Owned-table boundary preserved: all implemented writes target `banking_core_accounts_*`
- Eventing preserved: AppGen-X only
- Stream-engine picker: not exposed
- Shared-table access: not used
- Single-PBC app surface present: forms, wizards, controls, workbench, detail query, assistant help
- Lifecycle state machine exercised through package-local tests and runtime smoke

## Scenario Evidence

### Lifecycle happy path

- open account in `pending`
- approve to `approved` with maker-checker
- activate to `active`
- close to `closed` with reason and maker-checker
- reopen to `reopened` with reason and maker-checker

### Control evidence

- invalid direct `pending -> active` transition rejected
- self-approval on `approved` transition rejected
- duplicate opening request handled idempotently

### Usability evidence

- app surface exposes 3 forms, 2 wizards, and 5 controls
- workbench summary returns lifecycle counts for filtered accounts
- assistant help manifest points operators to the correct form, wizard, and controls

## Validation Commands

- `/Volumes/Media/src/pjs/appgen/.venv/bin/python -m compileall /Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/banking_core_accounts`
- `/Volumes/Media/src/pjs/appgen/.venv/bin/python -m pytest /Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/banking_core_accounts/tests -q`
- `PYTHONPATH=/Volumes/Media/src/pjs/appgen/src /Volumes/Media/src/pjs/appgen/.venv/bin/python -c "from pyAppGen.pbcs.banking_core_accounts.runtime import banking_core_accounts_runtime_smoke; ..."`

Exact outputs are recorded in `implementation-status.md`.
