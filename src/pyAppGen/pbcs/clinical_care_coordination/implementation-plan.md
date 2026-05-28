# Clinical Care Coordination Implementation Plan

## Intent

Turn `clinical_care_coordination` from a generic generated package into a usable one-PBC application for care coordination teams. The app must operate without shared tables: it owns care plans, care teams, referrals, encounters, care gaps, transitions, outcome measures, coordination tasks, source evidence, AppGen-X outbox/inbox/dead-letter contracts, UI surfaces, agent skills, rules, parameters, and release evidence.

## Domain Slice

This pass implements the care coordination command center slice described in `improve1.md`:

- Longitudinal care-plan state management with child goals and closure guards.
- Consent-aware interdisciplinary care-team roster.
- Closed-loop referral lifecycle with duplicate detection and result reconciliation tasks.
- Encounter-derived coordination tasks with source note span traceability.
- Typed care gap taxonomy with closure evidence requirements.
- Transition-of-care packet completeness and handoff controls.
- Outcome measure baseline, target, current value, trend, confidence, and care-plan attribution.
- Workbench queues for high-risk patients, unscheduled referrals, unreconciled results, active transitions, blocked care gaps, outreach due today, care-team coverage gaps, and control failures.
- Agent document/instruction mutation planning for care plans, referrals, transitions, and care gaps.

## Executable Design

`care_coordination_app.py` is the package-local runtime for the slice. It uses an in-memory state object shaped after the owned datastore tables so tests can prove behavior without external services. All command functions return new state, AppGen-X outbox evidence, and `side_effects: ()`. This keeps registration and discovery side-effect-free while making the PBC usable in a generated one-PBC app.

The existing package surfaces are extended rather than replaced:

- `runtime.py` exposes forms, wizards, controls, and a single-PBC app contract.
- `services.py` dispatches real care coordination commands through `ClinicalCareCoordinationService`.
- `routes.py` maps domain routes to service operations.
- `ui.py` exposes queue-oriented forms, wizards, controls, and workbench metadata.
- `agent.py` produces stable document digests and domain-specific CRUD mutation plans.
- `release_evidence.py` includes single-PBC app, forms, wizards, and controls in readiness evidence.

## Controls

The first implemented controls are consent-scope disclosure guard, active-goal closure guard, duplicate referral guard, transition packet completeness guard, care-gap closure evidence guard, and owned-table boundary guard. These controls are surfaced in UI contracts and validated in package tests.

## Review And Validation Plan

Focused tests must prove invalid care-plan closure, consent-limited disclosure refusal, duplicate referral blocking, referral result reconciliation, encounter task extraction, care-gap evidence enforcement, transition packet blocking, outcome trend calculation, service dispatch, route mapping, UI app contract, agent document-instruction planning, and release smoke behavior.

The validation gate for this slice is:

- `python3 -m py_compile` for touched package modules.
- `./.venv/bin/pytest -q src/pyAppGen/pbcs/clinical_care_coordination/tests`
- `pbc_implementation_release_audit(("clinical_care_coordination",))`
- `pbc_generation_smoke_audit(("clinical_care_coordination",))`

## Remaining Expansion

Future passes should deepen guideline versioning, social-needs resource performance, medication reconciliation checkpoints, education comprehension evidence, caregiver collaboration revocation history, referral network analytics, readmission watchlists, and patient timeline replay. The current slice establishes the executable app foundation and proves the package can stand alone.
