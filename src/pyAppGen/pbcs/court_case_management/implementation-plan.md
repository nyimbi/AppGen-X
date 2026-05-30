# Court Case Management Implementation Plan

## Intent

Turn `court_case_management` into a usable standalone court operations slice rather than a generic package shell. The PBC must let clerks, chambers staff, and courtroom operators open cases, manage parties, triage filings, preserve docket chronology, lodge evidence, schedule hearings, enter orders, track operational tasks, and operate workbench queues using only package-owned tables and AppGen-X events.

## Domain Slice

This standalone pass implements the highest-value court operations slice from `improve1.md`:

- Canonical case numbering by court, division, filing year, and sequence.
- Party role and representation capture with counsel, self-represented flags, aliases, service addresses, and representation history.
- Filing intake with deficiency codes, cure deadlines, review tasks, rejected or cured states, and automatic docketing after acceptance.
- Evidence intake with exhibit numbers, custody events, admission review tasks, and docket linkage.
- Immutable docket sequence controls that reject chronology gaps.
- Hearing scheduling with courtroom and judge conflict controls plus hearing-prep tasks.
- Order drafting, signature verification, entry, and docket linkage.
- Operational case tasks for clerk, chambers, evidence, and service follow-up.
- Workbench queues for clerk deficiencies, accepted filings, evidence review, chambers order review, courtroom calendars, pending tasks, restricted items, and open cases.
- Agent document planning for cases, filings, evidence, hearings, orders, and tasks.

## Executable Design

`court_operations_app.py` is the package-local execution engine. `standalone.py` wraps it into a mutable one-PBC application shell with runtime defaults, focused release audits, and documentation checks. `services.py`, `routes.py`, `ui.py`, `agent.py`, and `release_evidence.py` expose the same slice through service, route, UI, assistant, and release-evidence surfaces.

## UI And Controls

The PBC surfaces seven forms, seven wizards, and nine controls:

- Case intake, party representation, filing intake, evidence intake, hearing scheduling, order drafting, and task assignment forms.
- Case opening, filing deficiency, evidence intake, hearing calendar, hearing packet, order entry, and task follow-up wizards.
- Case-number uniqueness, filing deficiency acceptance, docket sequence integrity, courtroom double-booking, judge double-booking, evidence custody, signed-order entry, task completion authority, and sealed-record access controls.

## Validation Plan

Focused tests prove duplicate case-number rejection, filing deficiency review-task creation and cure behavior, docket sequence blocking, hearing conflict blocking, evidence intake and detail timelines, signed-order entry, standalone route and service execution, and local release audits.

Validation commands:

- `python3 -m py_compile src/pyAppGen/pbcs/court_case_management/*.py src/pyAppGen/pbcs/court_case_management/tests/*.py`
- `PYTHONPATH=src pytest -q src/pyAppGen/pbcs/court_case_management/tests`
- `PYTHONPATH=src python3 -c "from pyAppGen.pbcs.court_case_management.audit import run_court_case_management_pbc_audit; print(run_court_case_management_pbc_audit()['ok'])"`
- `PYTHONPATH=src python3 -c "from pyAppGen.pbc import pbc_implementation_release_audit, pbc_generation_smoke_audit; keys=('court_case_management',); print(pbc_implementation_release_audit(keys)['ok']); print(pbc_generation_smoke_audit(keys)['ok'])"`

## Remaining Expansion

Future passes should deepen service of process, public/internal docket projections, continuance workflows, transcript readiness, appeals, related-case consolidation, and judge reassignment. This pass establishes the executable standalone app foundation and the main operational controls.
