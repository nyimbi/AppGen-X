# Court Case Management PBC

`court_case_management` is the AppGen-X Packaged Business Capability for trial-court operations: case opening, parties and representation, filing intake, docket chronology, hearing calendars, orders, judgments, workbench queues, and governed assistant help. A generated application can include only this PBC and still provide a working court operations surface backed by owned tables, services, routes, forms, wizards, controls, AppGen-X events, and an assistant panel.

## Owned Boundary

The PBC owns court cases, filings, hearings, docket entries, parties, judgments, court orders, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X event tables. Other PBCs can interact through declared APIs, consumed events, emitted events, or projections, but no shared foreign court table is required for core operation.

Supported ordinary datastore backends are PostgreSQL, MySQL, and MariaDB. Ordinary eventing uses AppGen-X outbox, inbox, and dead-letter evidence only.

## Application Surface

The one-PBC app includes:

- Case intake form for venue-aware case numbering.
- Party representation form for role, counsel, pro se status, service addresses, and aliases.
- Filing intake form with deficiency codes and cure deadlines.
- Hearing schedule form with courtroom, session block, judge, readiness, interpreter, and mode.
- Order drafting form with signature and entry controls.

Wizards guide case opening, filing deficiency review, hearing calendar placement, and order entry. Controls prevent duplicate case numbers, unsafe filing acceptance, docket sequence gaps, courtroom double booking, unsigned order entry, and sealed-record leakage.

## Workbench

`CourtCaseManagementWorkbench` is organized around court operations:

- Clerk deficiency queue.
- Accepted filings.
- Chambers order review.
- Courtroom calendar.
- Sealed or restricted items.
- Open cases.

`CourtCaseManagementDetail` is the case-level timeline and detail surface. `CourtCaseManagementAssistantPanel` contributes court-specific skills to the composed application agent.

## Agent And Documents

The assistant can read a filing packet, order draft, hearing request, party notice, or case-opening instruction and produce a governed CRUD mutation preview. It chooses a target table, explains the proposed action, requires human confirmation for mutation, and stays inside owned tables.

## Developer Entry Points

- `court_operations_app.py` contains the executable slice.
- `services.py` exposes `CourtCaseManagementService`.
- `routes.py` maps court routes to service operations.
- `ui.py` exposes forms, wizards, controls, and workbench metadata.
- `agent.py` exposes document instruction and datastore CRUD planning.
- `release_evidence.py` includes single-PBC app readiness evidence.

## Validation

Run package tests:

```bash
./.venv/bin/pytest -q src/pyAppGen/pbcs/court_case_management/tests
```

Run release checks:

```bash
./.venv/bin/python - <<'PY'
from pyAppGen.pbc import pbc_generation_smoke_audit, pbc_implementation_release_audit
keys = ("court_case_management",)
print(pbc_implementation_release_audit(keys)["ok"])
print(pbc_generation_smoke_audit(keys)["ok"])
PY
```
