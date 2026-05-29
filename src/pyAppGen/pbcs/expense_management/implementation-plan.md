# Expense Management PBC Implementation Plan

## Objective

Make `expense_management` complete as a standalone one-PBC application for enterprise expense operations. A generated application containing only this PBC must allow finance teams, employees, managers, auditors, and reimbursement operators to manage the full expense lifecycle with database-backed records, forms, wizards, controls, workflows, AppGen-X events, agent assistance, and release evidence.

## Domain Scope

The PBC owns employee expense report operations after employee identity, payment, and card activity have been projected into the package through declared APIs or AppGen-X events. It does not own employee master data, card issuer settlement, payroll, bank payment execution, fraud adjudication outside expense scope, or general ledger posting.

The owned domain includes expense reports, expense lines, receipt artifacts, card transactions, merchant profiles, expense policies, violations, approvals, reimbursements, cash advances, mileage, per diem, audit samples, duplicate signals, exceptions, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X runtime event tables.

## Capability Plan

1. Preserve executable package evidence already present in the PBC.
   - Validate schema, migration, model, service, route, event, handler, UI, agent, configuration, permission, seed, release evidence, and test surfaces.
   - Keep all changes scoped to `src/pyAppGen/pbcs/expense_management`.

2. Confirm table-stakes expense management coverage.
   - Report creation, submission readiness, return, approval, audit review, reimbursement scheduling, payment reconciliation, reopening, and withdrawal.
   - Expense line capture with category intelligence, merchant evidence, allocation, tax, currency, attendees, travel linkage, mileage, per diem, and receipt rules.
   - Receipt upload, fingerprinting, semantic extraction, duplicate artifact detection, receipt-card matching, redaction status, and audit notes.
   - Card transaction ingestion with pending/posting/reversal/dispute lifecycle, idempotency, employee assignment, merchant normalization, and dead-letter handling.
   - Policy versioning, rule compilation, violation lifecycle, exception requests, approval routing, segregation-of-duty checks, and SLA escalation.
   - Reimbursement batch readiness, cash advance netting, payment status reconciliation, spend accrual evidence, and close support.
   - Risk-based audit sampling, duplicate detection, anomaly/fraud signal review, continuous control tests, and spend intelligence dashboards.

3. Confirm advanced capabilities.
   - Semantic receipt extraction with confidence and confirmation requirements.
   - Probabilistic duplicate detection across receipts, card transactions, reports, amounts, dates, merchants, and employee context.
   - Counterfactual policy coaching before submission.
   - Continuous spend control testing for approval conflicts, missing receipts, duplicate signals, stale advances, and reimbursement-before-approval defects.
   - Risk-based audit sampling with explainable drivers.
   - Carbon-aware travel spend insights where route/category evidence exists.

4. Confirm standalone application behavior.
   - UI contracts expose an expense workbench, receipt inbox, violation queue, approval board, reimbursement console, audit sampling panel, employee spend analytics, forms, wizards, controls, and assistant surfaces.
   - Services and routes map to executable operations and preserve owned-table boundaries.
   - The agent can parse documents and instructions, plan governed CRUD, reject foreign tables, require confirmation for writes, and export skills to the composed application agent.

5. Complete human-facing handoff artifacts.
   - Add this implementation plan.
   - Add README with operating scope, owned boundary, workflows, UI, agent, events, configuration, and testing guidance.
   - Add implementation status with review findings, validation results, and known gaps.

## Verification Plan

Run:

```text
python3 -m py_compile src/pyAppGen/pbcs/expense_management/*.py src/pyAppGen/pbcs/expense_management/tests/*.py
/Volumes/Media/src/pjs/appgen/.venv/bin/pytest -q src/pyAppGen/pbcs/expense_management/tests
```

Run PBC gates:

```python
from pyAppGen.pbc import (
    pbc_specification_contract,
    pbc_source_artifact_contract,
    pbc_implementation_release_audit,
    pbc_generation_smoke_audit,
)

key = "expense_management"
assert pbc_specification_contract(key)["ok"]
assert pbc_source_artifact_contract(key)["ok"]
assert pbc_implementation_release_audit((key,))["ok"]
assert pbc_generation_smoke_audit((key,))["ok"]
```
