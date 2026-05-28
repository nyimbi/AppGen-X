## Scope

Implement one executable accounts-payable automation slice inside `src/pyAppGen/pbcs/ap_automation` only.

## Backlog Slice

1. Vendor onboarding readiness
   Add executable evidence-pack readiness for vendor activation, including bank validation, tax proof completeness, screening, approval, and payment enablement.

2. Invoice intake and duplicate controls
   Add canonical capture artifacts, duplicate scoring across invoice metadata, and exception routing when invoices should not auto-flow.

3. Approval and hold-aware payment execution
   Add approval task creation, explicit payment holds, liquidity-aware scheduling that explains why invoices are scheduled or blocked, and batch/remittance execution evidence.

4. Vendor reconciliation
   Add vendor statement reconciliation that compares supplier balances to owned invoices and emits actionable discrepancy evidence.

5. Exposure alignment
   Wire the implemented operations into service, UI, agent, and release-evidence surfaces so the executable runtime and contract surfaces agree.

## Planned File Changes

- `runtime.py`
  Add the missing AP executable operations and extend state/workbench evidence.
- `services.py`
  Replace contract-only command facades with executable operation wrappers for the implemented AP workflows.
- `ui.py`
  Expose the new workflow actions and workbench cards/panels.
- `agent.py`
  Advertise the new governed AP actions and candidate operations.
- `release_evidence.py`
  Check the newly executable AP workflow coverage.
- `README.md`
  Document the implemented slice and how to exercise it.
- `implementation-status.md`
  Record what is complete, what is intentionally deferred, and validation evidence.
- `tests/test_implementation.py`
  Add focused behavior tests for the new executable slice.

## Non-Goals

- No shared-table access.
- No eventing contract other than AppGen-X.
- No changes outside the owned AP package.
- No docs-only placeholders counted as implementation.
