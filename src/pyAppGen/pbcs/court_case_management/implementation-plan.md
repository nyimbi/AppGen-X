# Court Case Management Implementation Plan

## Intent

Turn `court_case_management` into a usable one-PBC court operations app rather than a generic package shell. The PBC must let clerks, chambers staff, and courtroom operators open cases, manage parties, triage filings, preserve docket chronology, schedule hearings, enter orders, and operate workbench queues using only package-owned tables and AppGen-X events.

## Domain Slice

This pass implements the highest-risk court operations slice from `improve1.md`:

- Canonical case numbering by court, division, filing year, and sequence.
- Party role and representation capture with counsel, self-represented flags, aliases, service addresses, and representation history.
- Filing intake with deficiency codes, cure deadlines, rejected/cured/accepted states, and automatic docketing after acceptance.
- Immutable docket sequence controls that reject chronology gaps.
- Hearing scheduling with courtroom/session/judge controls and double-book prevention.
- Order drafting, signature verification, entry, and docket linkage.
- Workbench queues for clerk deficiencies, accepted filings, chambers order review, courtroom calendars, restricted items, and open cases.
- Agent document/instruction planning for cases, filings, parties, hearings, and orders.

## Executable Design

`court_operations_app.py` is the package-local executable app engine. It uses an in-memory state shaped after the owned datastore tables, returns new state from every command, emits AppGen-X outbox evidence, and never mutates foreign tables. The existing generated runtime remains intact but now exposes the court app contracts through runtime capabilities, service methods, routes, UI, agent, and release evidence.

## UI And Controls

The PBC surfaces five forms, four wizards, and six controls:

- Case intake, party representation, filing intake, hearing scheduling, and order drafting forms.
- Case opening, filing deficiency, hearing calendar, and order entry wizards.
- Case-number uniqueness, filing deficiency acceptance, docket sequence integrity, courtroom double booking, signed order entry, and sealed-record access controls.

## Validation Plan

Focused tests prove duplicate case-number rejection, filing deficiency cure behavior, docket sequence blocking, hearing conflict blocking, signed-order entry, route/service/UI/agent execution, and release smoke contracts.

Validation commands:

- `python3 -m py_compile` on touched modules.
- `./.venv/bin/pytest -q src/pyAppGen/pbcs/court_case_management/tests`
- `pbc_implementation_release_audit(("court_case_management",))`
- `pbc_generation_smoke_audit(("court_case_management",))`

## Remaining Expansion

Future passes should deepen service of process, public/internal docket projections, continuance workflows, summons/subpoena issuance, exhibit custody, appeals, related-case consolidation, and transcript readiness. This pass establishes the executable app foundation and the main operational controls.
