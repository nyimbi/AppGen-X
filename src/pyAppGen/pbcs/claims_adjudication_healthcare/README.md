# Healthcare Claims Adjudication PBC

`claims_adjudication_healthcare` is an AppGen-X Packaged Business Capability for payer-side healthcare claim intake, line adjudication, coding review, benefit rule governance, denials, appeals, payment integrity, evidence handling, release controls, and governed assistant support.

## Owned Boundary

The PBC owns health claims, claim lines, coding reviews, benefit rules, denials, appeals, payment integrity cases, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X inbox/outbox/dead-letter tables.

It does not own member enrollment, provider master, prior authorization, accumulator, fee schedule, pharmacy benefit, EHR, or audit source-of-truth tables. Those dependencies are represented as declared AppGen-X event/API projections with freshness and boundary evidence.

## Standalone App Surface

`standalone.py` exposes the one-PBC app contract:

- `single_pbc_app_contract()` provides schema, service, API, runtime, UI, forms, wizards, controls, routes, DSL metadata, dependencies, and simulation evidence.
- `forms_contract()` surfaces intake, claim-line, benefit/medical necessity, denial/appeal, payment-integrity, attachment/document, and release-control forms.
- `wizards_contract()` covers claim intake to adjudication, line pricing and benefit checks, medical necessity/attachments, denial and appeal rework, payment integrity recovery, and release/agent publishing.
- `controls_contract()` enforces projection boundaries, duplicate replay, denial notices, clinical human review, payment integrity recovery, and agent mutation safety.
- `full_claims_adjudication_simulation()` exercises rule approval, claim creation, line adjudication, denial, appeal, document instruction planning, duplicate scoring, and boundary proof.

## UI and Agent

The UI exposes payer workbench surfaces for intake, line adjudication, coding and denials, appeals, payment integrity, configuration, and release evidence. The composed app agent receives `claims_adjudication_healthcare_skills`; assistant CRUD plans require preview, confirmation, AppGen-X eventing, and owned-table boundaries.

## Verification

Run focused checks:

```bash
PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/claims_adjudication_healthcare
PYTHONPATH=src python3 -m pytest -q src/pyAppGen/pbcs/claims_adjudication_healthcare/tests
```
