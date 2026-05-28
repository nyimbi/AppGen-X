# Clinical Care Coordination PBC

`clinical_care_coordination` is an AppGen-X Packaged Business Capability for the operational work of coordinating patient care across care plans, teams, referrals, encounters, care gaps, transitions, and outcomes. A generated application can include only this PBC and still provide a usable care coordination command center with database-backed records, forms, wizards, controls, workbench queues, service commands, routes, AppGen-X events, and an assistant panel.

## What It Owns

The PBC owns its clinical coordination datastore boundary. Its records are modeled around `patient_care_plan`, `care_team`, `referral`, `encounter`, `care_gap`, `transition_plan`, `outcome_measure`, coordination tasks, source evidence, policy rules, runtime parameters, schema extensions, control assertions, and AppGen-X event tables. Other PBCs may interact through APIs, events, or projections, but they do not write shared clinical coordination tables.

Supported ordinary database backends remain PostgreSQL, MySQL, and MariaDB. Ordinary eventing uses the AppGen-X outbox/inbox/dead-letter contract. Users are not offered a stream-engine picker.

## Application Surface

The one-PBC app exposes:

- Care plan form for problems, goals, responsible role, patient preferences, barriers, cadence, and source evidence.
- Care team roster form for coordinator, clinician, specialist, caregiver, interpreter, escalation, coverage, and consent scope.
- Referral lifecycle form for specialty, urgency, authorization, expected turnaround, result receipt, and reconciliation.
- Encounter task extraction form that turns clinical encounters or notes into coordination tasks.
- Care gap form for preventive, immunization, chronic monitoring, medication reconciliation, behavioral health, social determinant, post-discharge, missed appointment, and outreach gaps.
- Transition packet form for discharge source, receiving setting, medication reconciliation, follow-up, patient instructions, caregiver confirmation, and transportation.
- Outcome measure form for baseline, target, current value, source, confidence, and trend.

Wizards guide longitudinal care-plan activation, closed-loop referrals, transition-of-care packet completion, and care-gap closure. Controls block unsafe goal closure, duplicate referrals, incomplete transition packets, unsupported care-gap closure, consent violations, and foreign-table writes.

## Workbench

`ClinicalCareCoordinationWorkbench` is organized as an operational command center:

- High-risk patients.
- Unscheduled referrals.
- Unreconciled results.
- Active transitions.
- Blocked care gaps.
- Outreach due today.
- Care-team coverage gaps.
- Control failures.

The workbench is intentionally queue-oriented so a coordinator can move from risk to action without leaving the PBC.

## Agent And Chatbot

`ClinicalCareCoordinationAssistantPanel` contributes skills to the composed application agent. The assistant can read documents or instructions, identify whether the user is asking for a care plan, referral, transition, or care gap action, and produce a governed CRUD mutation plan. Mutations require human confirmation and execute through package services rather than direct table writes.

The assistant respects care-team consent limits. It refuses protected disclosures when the care-team member lacks matching consent scope or protected-detail authorization.

## Developer Entry Points

- `care_coordination_app.py` contains the executable domain slice.
- `services.py` exposes `ClinicalCareCoordinationService`.
- `routes.py` maps HTTP route contracts to service operations.
- `ui.py` exposes forms, wizards, controls, and workbench metadata.
- `agent.py` exposes assistant, document instruction, CRUD, and composed-agent skill contracts.
- `release_evidence.py` summarizes readiness evidence.

## Validation

Run package tests:

```bash
./.venv/bin/pytest -q src/pyAppGen/pbcs/clinical_care_coordination/tests
```

Run release checks:

```bash
./.venv/bin/python - <<'PY'
from pyAppGen.pbc import pbc_generation_smoke_audit, pbc_implementation_release_audit
keys = ("clinical_care_coordination",)
print(pbc_implementation_release_audit(keys)["ok"])
print(pbc_generation_smoke_audit(keys)["ok"])
PY
```
