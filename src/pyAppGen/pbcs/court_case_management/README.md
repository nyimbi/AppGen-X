# Court Case Management PBC

`court_case_management` is the AppGen-X Packaged Business Capability for trial-court operations: case opening, party and counsel capture, filing intake, evidence lodging, docket chronology, hearing calendars, court orders, operational tasks, and governed assistant help. A generated application can include only this PBC and still provide a working court operations surface backed by owned tables, services, routes, forms, wizards, controls, AppGen-X events, and a package-local standalone app.

## Owned Boundary

The PBC owns court cases, filings, evidence items, hearings, case tasks, docket entries, parties, judgments, court orders, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X event tables. Other PBCs integrate through declared APIs, consumed events, or projections only.

Supported ordinary datastore backends are PostgreSQL, MySQL, and MariaDB. Ordinary eventing uses AppGen-X outbox, inbox, and dead-letter evidence only.

## Application Surface

The one-PBC app includes:

- Case intake form for venue-aware case numbering.
- Party representation form for role, counsel, pro se status, service addresses, and aliases.
- Filing intake form with deficiency codes and cure deadlines.
- Evidence intake form with exhibit numbers, custody events, and admission review.
- Hearing schedule form with courtroom, session block, judge, readiness, interpreter, and mode.
- Order drafting form with signature and entry controls.
- Task assignment form for clerk, chambers, evidence, and hearing follow-up work.

Wizards guide case opening, filing deficiency review, evidence intake, hearing calendar placement, hearing packet preparation, order entry, and task follow-up. Controls prevent duplicate case numbers, unsafe filing acceptance, docket sequence gaps, courtroom or judge double-booking, broken evidence custody, unsigned order entry, unauthorized task closure, and sealed-record leakage.

## Standalone Composition

`standalone.py` exposes `CourtCaseManagementStandaloneApplication` plus focused package-local audits. The standalone app can:

- Configure runtime defaults and register package-local rules and parameters.
- Open cases and add parties.
- Receive and cure filings.
- Lodge evidence and queue evidence review.
- Schedule hearings and queue hearing-prep tasks.
- Draft and enter orders.
- Create and complete operational tasks.
- Serve workbench and case-detail views.
- Preview governed agent mutations and receive AppGen-X events.

## Workbench

`CourtCaseManagementWorkbench` is organized around court operations:

- Clerk deficiency queue.
- Accepted filings.
- Evidence review queue.
- Chambers order review.
- Courtroom calendar.
- Pending tasks.
- Sealed or restricted items.
- Open cases.

`CourtCaseManagementDetail` exposes the case timeline, parties, filings, evidence, hearings, orders, tasks, and docket history. `CourtCaseManagementAssistantPanel` contributes filing triage, hearing preparation, and order follow-up skills to the composed application agent.

## Developer Entry Points

- `court_operations_app.py` contains the executable package-local app engine.
- `standalone.py` contains the mutable one-PBC application shell and focused audits.
- `services.py` exposes service operations and the standalone service wrapper.
- `routes.py` maps court routes to standalone and contract operations.
- `ui.py` exposes forms, wizards, controls, workbench metadata, and detail sections.
- `agent.py` exposes governed document-intake and CRUD planning.
- `audit.py` aggregates the focused standalone package audit.
- `release_evidence.py` bundles runtime evidence with standalone implementation and generation audits.

## Validation

Run package tests:

```bash
PYTHONPATH=src pytest -q src/pyAppGen/pbcs/court_case_management/tests
```

Run standalone audits:

```bash
PYTHONPATH=src python3 -c "from pyAppGen.pbcs.court_case_management.audit import run_court_case_management_pbc_audit; from pyAppGen.pbcs.court_case_management.standalone import pbc_generation_smoke_audit, pbc_implementation_release_audit; print(run_court_case_management_pbc_audit()['ok']); print(pbc_implementation_release_audit()['ok']); print(pbc_generation_smoke_audit()['ok'])"
```

Run repository PBC audits:

```bash
PYTHONPATH=src python3 -c "from pyAppGen.pbc import pbc_generation_smoke_audit, pbc_implementation_release_audit; keys=('court_case_management',); print(pbc_implementation_release_audit(keys)['ok']); print(pbc_generation_smoke_audit(keys)['ok'])"
```
