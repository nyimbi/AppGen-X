# Clinical Care Coordination Implementation Status

## Status

Implemented an executable one-PBC care coordination app slice inside `src/pyAppGen/pbcs/clinical_care_coordination`.

## Delivered

- Added `care_coordination_app.py` with care-plan lifecycle, consent-aware care-team roster, referral lifecycle, encounter-derived coordination tasks, care gap evidence controls, transition-of-care packet controls, outcome trend calculation, workbench queues, forms, wizards, controls, single-PBC app contract, document-instruction mutation planning, and smoke tests.
- Extended runtime capabilities with forms, wizards, controls, and single-PBC app evidence.
- Extended services and route contracts to execute domain commands instead of only generic operation manifests.
- Extended UI contract with concrete forms, wizards, controls, queue names, and single-PBC app metadata.
- Updated agent document-instruction planning to use stable hashes and domain-specific mutation plans.
- Updated release readiness evidence to include single-PBC app, forms, wizards, and controls.
- Added tests proving the main care coordination behavior and single-PBC app surface.
- Added this status file and a descriptive README.

## Review Findings Resolved

- Replaced Python `hash()` use in assistant document digests with SHA-256 for deterministic release evidence.
- Added service command coverage for care team, referral, encounter task extraction, care gap, transition, outcome, and referral result workflows.
- Added route-to-operation mapping so API contracts point to executable service operations.
- Added controls for the highest-risk clinical edge cases from `improve1.md`: consent, unsafe closure, duplicate referral, transition packet completeness, and closure evidence.

## Validation

Validation commands for this slice:

- `python3 -m py_compile src/pyAppGen/pbcs/clinical_care_coordination/care_coordination_app.py src/pyAppGen/pbcs/clinical_care_coordination/runtime.py src/pyAppGen/pbcs/clinical_care_coordination/services.py src/pyAppGen/pbcs/clinical_care_coordination/ui.py src/pyAppGen/pbcs/clinical_care_coordination/agent.py src/pyAppGen/pbcs/clinical_care_coordination/release_evidence.py src/pyAppGen/pbcs/clinical_care_coordination/routes.py`
- `./.venv/bin/pytest -q src/pyAppGen/pbcs/clinical_care_coordination/tests`
- `pbc_implementation_release_audit(("clinical_care_coordination",))`
- `pbc_generation_smoke_audit(("clinical_care_coordination",))`

## Remaining Risks

The slice is intentionally package-local and executable, but it is not yet a full clinical-grade implementation of every backlog item. Future passes should add guideline version impact analysis, patient timeline replay, social barrier resolution workflows, medication reconciliation detail, education comprehension evidence, readmission watchlists, caregiver revocation history, referral destination performance analytics, and richer ABAC policy evaluation.
