# Lease Lending and Equipment Finance PBC

`lease_lending_equipment_finance` is a standalone AppGen-X PBC for equipment leases, loans, rentals, TRAC/FMVs, residual-bearing contracts, servicing, collateral protection, collections, repossession, disposition, syndication, and investor remittance. It owns its datastore boundary and exposes generated schema, services, routes, events, UI fragments, forms, wizards, controls, and assistant skills.

## Domain Coverage

The package covers application-to-booking intake, product structure validation, obligor and guarantor party roles, serial-numbered collateral, vendor invoices and disbursement controls, credit approval conditions, pricing and schedule generation, tax/accounting classification, commencement and acceptance, usage billing, maintenance reserves, residual review, buyout quotes, end-of-term decisions, restructures, collateral perfection, insurance monitoring, collections, hardship relief, repossession, disposition, syndication, investor waterfalls, concentration views, exception taxonomy, manual overrides, and finance-pack document extraction.

## Executable Surfaces

- `standalone.py` runs a complete application-to-booking-to-recovery demo.
- `forms.py` defines operator forms for origination, structure, collateral, funding, schedules, residuals, buyouts, and recovery.
- `wizards.py` defines guided flows for booking, pricing, funding, usage/reserves, end-of-term, collections/repo, and investor remittance.
- `controls.py` blocks unsafe booking, structure, collateral, funding, pricing, protection, repo, and investor actions until required evidence exists.
- `agent.py` contributes confirmation-gated assistant skills and document CRUD previews.

The PBC uses AppGen-X events only, hides stream-engine choices, and allows PostgreSQL, MySQL, or MariaDB.

## Validation

```bash
PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/lease_lending_equipment_finance
PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest -q src/pyAppGen/pbcs/lease_lending_equipment_finance/tests
```
