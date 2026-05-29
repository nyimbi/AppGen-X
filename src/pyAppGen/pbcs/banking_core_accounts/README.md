# Banking Core Accounts

`banking_core_accounts` now includes an executable deposit-account lifecycle slice that can be used as a single-PBC app for its owned domain. The package stays inside AppGen-X boundaries, writes only to `banking_core_accounts_*` tables, and does not expose any stream-engine picker or shared-table access.

## Implemented Slice

- Database-backed owned `deposit_account` model with lifecycle-specific migration columns
- Lifecycle commands for opening and transitioning deposit accounts
- Guarded state machine for `pending`, `approved`, `active`, `restricted`, `dormant`, `closed`, and `reopened`
- Maker-checker enforcement for approval-sensitive transitions
- Account detail and lifecycle workbench queries
- Package-local forms, wizards, controls, and workflow surfaces for one-PBC usability
- Assistant help cards plus governed document-instruction and CRUD planning
- Package-local release tests and runtime smoke evidence

## One-PBC App Surface

- Forms:
  `deposit_account_opening_form`, `deposit_account_transition_form`, `account_detail_filter_form`
- Wizards:
  `deposit_account_opening_wizard`, `deposit_account_lifecycle_wizard`
- Controls:
  `tenant_boundary_check`, `mandatory_field_check`, `state_transition_guard`, `maker_checker_gate`, `reason_required_guard`
- Workflows:
  `banking_core_accounts_create_deposit_account_workflow`, `banking_core_accounts_deposit_account_lifecycle_workflow`, `banking_core_accounts_document_instruction_workflow`
- Views:
  `Lifecycle Queue`, `Approval Queue`, `Lifecycle Controls`

## Governance Surfaces

- Permissions:
  operator `read/create/update/operate`, approver `read/approve/operate`, auditor `read/admin`
- Assistant planning:
  document instructions are converted into workflow-aware CRUD previews that identify the route, permission, controls, and confirmation requirement before mutation

## Main Runtime Entry Points

- `banking_core_accounts_open_deposit_account(state, payload)`
- `banking_core_accounts_transition_deposit_account(state, payload)`
- `banking_core_accounts_query_account_detail(state, account_id)`
- `banking_core_accounts_query_workbench(state, filters=None)`
- `banking_core_accounts_build_workflow_surface(state=None, tenant="default")`
- `banking_core_accounts_build_app_surface(state=None, tenant="default")`

## Validation

- Compile: `/Volumes/Media/src/pjs/appgen/.venv/bin/python -m compileall /Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/banking_core_accounts`
- Tests: `/Volumes/Media/src/pjs/appgen/.venv/bin/python -m pytest /Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/banking_core_accounts/tests -q`
- Runtime smoke: `PYTHONPATH=/Volumes/Media/src/pjs/appgen/src /Volumes/Media/src/pjs/appgen/.venv/bin/python -c "from pyAppGen.pbcs.banking_core_accounts.runtime import banking_core_accounts_runtime_smoke; ..."`
- Package-local audits: `PYTHONPATH=/Volumes/Media/src/pjs/appgen/src /Volumes/Media/src/pjs/appgen/.venv/bin/python -c "from pyAppGen.pbcs.banking_core_accounts.capability_assurance import validate_table_stakes_capability_coverage; from pyAppGen.pbcs.banking_core_accounts.release_evidence import validate_release_evidence; print(validate_table_stakes_capability_coverage()['ok'], validate_release_evidence()['ok'])"`

See `implementation-status.md` for exact outcomes and remaining gaps.
