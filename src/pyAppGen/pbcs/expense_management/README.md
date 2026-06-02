# Expense Management PBC

`expense_management` is the AppGen-X packaged business capability for employee expense operations. It is designed to run as a standalone one-PBC application: an app composed with only this package can capture reports and lines, attach receipts, ingest card transactions, validate policy, route approvals, manage reimbursements, handle cash advances, calculate mileage and per diem, sample audits, detect duplicates, resolve exceptions, and guide users through an AI assistant.

## Owned Boundary

The PBC owns only `expense_management_` tables. It does not directly read or mutate employee master data, payment execution, payroll, fraud case management, travel booking, or general ledger tables. Those dependencies are represented through declared AppGen-X events, API dependencies, or package-local projections.

Owned operational areas include expense reports, expense lines, receipt artifacts, card transactions, merchant profiles, policies, policy violations, approval tasks, reimbursement batches and payments, cash advances, mileage claims, per diem claims, audit samples, duplicate signals, exception cases, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X outbox/inbox/dead-letter tables.

Supported ordinary database backends are PostgreSQL, MySQL, and MariaDB.

## Core Workflows

- Create and submit expense reports with readiness checks for employee context, report period, currency, business purpose, required receipts, policy version, approver eligibility, and exception status.
- Capture expense lines with category intelligence, merchant evidence, allocation, tax, currency, attendee, travel, mileage, per diem, and receipt requirements.
- Attach receipts with artifact fingerprints, OCR/semantic extraction evidence, duplicate detection, redaction status, and receipt-card matching.
- Ingest corporate card transactions with idempotency, pending/posting/reversal/dispute lifecycle, merchant normalization, and employee assignment evidence.
- Validate expense policy with versioned rules, thresholds, effective dates, employee groups, regions, categories, receipt requirements, and approval requirements.
- Open and resolve policy violations and exception cases with severity, rule version, impacted amount, approver evidence, employee response, and resolution outcome.
- Route approvals across manager, project owner, finance, compliance, audit, and executive nodes with segregation-of-duty checks and SLA escalation.
- Create reimbursement batches only after approval, duplicate/fraud holds, cash advance offsets, employee/payment eligibility, and cutoff evidence are clear.
- Reconcile reimbursement payment execution, failures, reversals, partial payment, retry, and audit evidence.
- Run audit sampling, duplicate detection, fraud/abuse signal review, continuous control testing, and spend intelligence dashboards.

## UI Surface

The package exposes a generated UI contract for a standalone workbench. Expected views include an expense workbench, receipt inbox, policy violation queue, approval board, reimbursement console, audit sampling panel, and employee spend analytics.

Forms and wizards map to executable service commands. Controls cover tenant scope, report status, category filters, policy version, reimbursement cycle, audit risk, duplicate confidence, receipt requirements, and configuration/rule/parameter editors. The UI also exposes AppGen-X event status, dead-letter triage, release evidence, and the package assistant panel.

## Agent Skills

The PBC contributes skills under the `expense_management_skills` namespace. The agent can explain tasks, parse receipts and policy instructions, recommend CRUD plans, choose forms and wizards, reject foreign table writes, require human confirmation before mutations, and preview AppGen-X events, idempotency keys, permissions, and validation warnings.

These skills are intended to integrate into the composed application's single AI assistant.

## Events

The package uses the AppGen-X event contract only. It emits expense lifecycle events such as report creation, policy violation opening, approval, reimbursement scheduling, audit sampling, and duplicate detection. It consumes employee, card transaction, payment, and policy events through idempotent handlers with retry and dead-letter evidence.

No user-facing stream-engine picker is exposed.

## Configuration, Rules, And Parameters

Configuration includes database backend, AppGen-X event topic, retry limits, tenant isolation, workbench limits, confirmation requirements, and default expense policies.

Rules cover receipt requirements, merchant/category policy, approval limits, duplicate detection, reimbursement readiness, audit sampling, and exception handling. Parameters include receipt thresholds, auto-approval limits, duplicate confidence thresholds, mileage rates, audit sample rates, and workbench limits.

## Testing

Run package checks from the repository root:

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

## Extension Points

Future work should deepen real database adapters, mobile receipt capture UX, payment provider reconciliation, calendar/travel projection integrations, and jurisdiction-specific tax recovery. Those extensions must preserve the owned-table boundary and use APIs/events/projections for cross-PBC collaboration.
