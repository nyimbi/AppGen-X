# Maritime Shipping Operations PBC

`maritime_shipping_operations` is a standalone AppGen-X PBC for ocean voyage operations across vessels, voyage rotations, cargo bookings, charter parties, port calls, laytime, demurrage, bunkers, carbon, compliance, and governed maritime assistant work. It owns its datastore boundary and exposes generated schema, services, routes, AppGen-X events, UI fragments, forms, wizards, controls, and assistant skills.

## Domain Coverage

The package covers voyage legs and rotations, vessel schedule reliability, port-call berth windows, statement-of-facts capture, booking allocation, cutoff governance, bill-of-lading lifecycle, stowage, dangerous goods and special cargo, reefers, charter clauses, laytime, demurrage/detention exposure, claim dossiers, bunker planning, ROB and consumption variance, carbon and ECA indicators, crewing-boundary readiness signals, compliance obligations, sanctions and restricted corridor checks, dead-letter operations, governed policy rules, runtime guardrails, schema extensions, voyage boards, timeline views, schedule recovery, booking/bill intake, claims triage, and counterfactual voyage simulations.

## Executable Surfaces

- `standalone.py` runs a voyage-to-claim and bunker/compliance demo with critical blockers.
- `forms.py` defines forms for voyages, vessels, bookings, charters, port calls, stowage, claims, bunkers, and compliance.
- `wizards.py` guides voyage publishing, booking-to-bill, port execution, laytime/demurrage, bunker/carbon, compliance, and recovery.
- `controls.py` blocks unsafe voyage, booking, stowage, port-call, claim, bunker, and compliance actions.
- `agent.py` contributes confirmation-gated assistant CRUD previews for maritime documents and schedule actions.

The PBC uses AppGen-X events only, hides stream-engine choices, and permits PostgreSQL, MySQL, or MariaDB.

## Validation

```bash
PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/maritime_shipping_operations
PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest -q src/pyAppGen/pbcs/maritime_shipping_operations/tests
```
