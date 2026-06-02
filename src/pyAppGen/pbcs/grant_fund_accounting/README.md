# Grant and Fund Accounting PBC

`grant_fund_accounting` is a standalone AppGen-X PBC for award setup, restrictions, budgets, allowable costs, allocations, drawdowns, receipts, match, funder reports, milestones, compliance evidence, exceptions, and grant closeout.

## Standalone Application Surface

`GrantFundAccountingStandaloneApp` proves the PBC can run alone. It configures grant accounting rules, activates awards from source evidence, defines restrictions, approves budgets, validates costs against restrictions and budgets, blocks unallowable costs, prepares drawdowns, tracks match, builds funder reports, seals compliance evidence, closes grants, and offers assistant document extraction previews.

## UI, Controls, and Agent

The PBC exposes forms for award intake, restrictions, budget versions, allowable cost rules, costs, drawdowns, match, reports, evidence, and closeout. Wizards guide award extraction, cost allowability, allocation, drawdown, reporting, and closeout. Continuous controls cover activation, lifecycle, restrictions, budgets, draw readiness, receipt reconciliation, match, report-to-ledger reconciliation, evidence retention, closeout, and assistant mutation governance.

The composed app receives `grant_fund_accounting_skills` for guided help, award document interpretation, and bounded CRUD previews. Mutations require confirmation and remain inside owned tables.

## Verification

- `PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/grant_fund_accounting`
- `PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/grant_fund_accounting/tests`
- `standalone_smoke_test()` and `validate_release_evidence()`
- focused AppGen-X PBC audits where available
