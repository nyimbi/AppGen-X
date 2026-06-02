# Legal Matter Management PBC

`legal_matter_management` is a standalone AppGen-X PBC for legal operations across intake, matter playbooks, conflicts, counsel governance, budgets, holds, custodians, deadlines, filings, documents, privilege, evidence custody, counsel invoices, exposure, settlement, and closure. It owns its datastore boundary and contributes generated schema, services, APIs, AppGen-X events, UI fragments, forms, wizards, controls, and assistant skills.

## Domain Coverage

The package covers matter intake triage, legal taxonomy, conflict screening, related parties, matter type playbooks, jurisdiction profiles, legal hold scope, custodian acknowledgement, preservation evidence ledgers, deadline computation, deadline propagation, filing dossiers, service-of-process, evidence binders, privilege review, privilege logs, chain of custody, eDiscovery requests, outside counsel panel governance, engagement scope, legal budgets, invoice compliance, accruals/reserves, exposure modeling, settlement strategy, approval matrices, legal risk heatmaps, investigations, regulatory inquiries, IP/employment/contract dispute extensions, insurance recovery, experts, witnesses, protective orders, task dependencies, matter timelines, and controlled legal-agent assistance.

## Executable Surfaces

- `standalone.py` runs an intake-to-close legal matter app flow.
- `forms.py` defines legal-ops forms for intake, conflicts, counsel, holds, deadlines, privilege, spend, and settlement.
- `wizards.py` guides intake, conflict/counsel, hold, deadline/filing, privilege/evidence, spend/reserve, and settlement/closure workflows.
- `controls.py` blocks unsafe legal work until classification, conflict, hold, deadline, privilege, invoice, and settlement authority evidence exists.
- `agent.py` contributes confirmation-gated assistant skills and legal document mutation previews.

The PBC uses AppGen-X events only, hides stream-engine choices, and permits PostgreSQL, MySQL, or MariaDB.

## Validation

```bash
PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/legal_matter_management
PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest -q src/pyAppGen/pbcs/legal_matter_management/tests
```
