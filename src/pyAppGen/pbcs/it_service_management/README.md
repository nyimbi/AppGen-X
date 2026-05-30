# IT Service Management PBC

`it_service_management` is a standalone AppGen-X PBC for service desk, incident response, request fulfillment, change enablement, problem management, CMDB governance, knowledge publication, and SLA/OLA control. It owns its datastore boundary and can generate a single-PBC application with forms, wizards, controls, APIs, event contracts, an assistant surface, and release evidence.

## Domain Coverage

The package covers routine and major incidents, impact/urgency priority derivation, duplicate outage rollups, incident timeline evidence freeze, milestone-based SLA clocks, resolver swarming and handoff controls, service catalog requests, access request entitlement and segregation checks, multi-step fulfillment, requester confirmation, standard/normal/emergency changes, change risk scoring, maintenance windows, CAB decisions, backout plans, post-implementation review, problem linkage, RCA templates, known error publication, recurrence detection, CI relationship graphs, CI ownership, drift detection, service dependency impact previews, SLA/OLA/underpinning commitments, and calendar-aware pause/resume logic.

## Executable Surfaces

- `standalone.py` implements an in-memory but executable single-PBC application flow.
- `forms.py` exposes professional task forms for every major ITSM operating area.
- `wizards.py` provides guided workflows for incidents, requests, access, change, problem, and CMDB work.
- `controls.py` enforces governance blockers for priority, handoff, entitlement, change windows, backout, RCA, CMDB ownership, and SLA pauses.
- `agent.py` contributes governed assistant skills for guidance, document intake, mutation preview, and datastore CRUD confirmation.

The PBC uses AppGen-X events only, keeps stream-engine choices hidden from users, and allows PostgreSQL, MySQL, or MariaDB as database backends.

## Validation

Run focused validation from the repository root:

```bash
PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/it_service_management
PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/it_service_management/tests
```
