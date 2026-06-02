# Lending Origination and Servicing PBC

`lending_origination_servicing` is a standalone AppGen-X PBC for loan intake, borrower verification, underwriting, offers, closing, funding, boarding, amortization, servicing, collections, workout, payoff, compliance notices, complaints, covenants, and governed AI assistance. It owns its schema and exposes generated models, services, routes, AppGen-X events, forms, wizards, controls, UI fragments, and agent skills.

## Domain Coverage

The package covers borrower and application normalization, co-borrowers and beneficial owners, document stipulations, income and cash-flow verification, KYC/fraud gates, bureau snapshots and disputes, collateral and liens, affordability ratios, underwriting policy lineage, adverse action, offer pricing and expiration, approval-to-fund conditions, loan boarding, executed note linkage, disbursement reconciliation, amortization libraries, accrual basis, escrow, payment allocation, reversals, delinquency buckets, promises to pay, hardship trial plans, modification accounting, payoff quotes, lien release, charge-off/recovery, bankruptcy/deceased/legal hold servicing, insurance/tax exceptions, complaints, disclosures/notices, fair-lending monitoring, and covenant breach workflows.

## Executable Surfaces

- `standalone.py` runs a full origination-to-servicing demo with critical blockers.
- `forms.py` defines forms for intake, stipulations, verification, collateral, decisions, offers, funding, repayment, and collections.
- `wizards.py` guides application-to-decision, collateral, offer-to-funding, boarding, payment/payoff, collections/workout, and compliance/covenant flows.
- `controls.py` blocks unsafe lending actions until evidence exists.
- `agent.py` contributes confirmation-gated assistant CRUD previews for lending files.

The PBC uses AppGen-X events only, hides stream-engine choices, and permits PostgreSQL, MySQL, or MariaDB.

## Validation

```bash
PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/lending_origination_servicing
PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest -q src/pyAppGen/pbcs/lending_origination_servicing/tests
```
