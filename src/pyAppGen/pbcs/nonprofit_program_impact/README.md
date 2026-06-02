# Nonprofit Program Impact PBC

`nonprofit_program_impact` is a package-local standalone AppGen-X slice for nonprofit program design, beneficiary targeting, service delivery, outcome evidence, donor reporting, and governed assistant previews.

## What This Package Owns

- Nonprofit-impact-owned schema, migrations, runtime contracts, routes, handlers, UI metadata, assistant skills, and release evidence.
- Package-local forms, wizards, controls, and a domain-deep standalone service for single-PBC execution.
- Theory-of-change, eligibility, dosage, evidence-quality, and donor-reporting guardrails that stay inside the package-owned boundary.

## Domain Shape

This package is optimized for nonprofit operations and monitoring teams who need to:

- define a program theory of change and target population,
- enroll eligible beneficiaries with usable consent,
- capture dosage and fidelity for service episodes,
- record outcomes and case evidence with quality scoring,
- freeze donor reports only after evidence and attribution gates pass,
- use a bounded assistant preview before any governed mutation.

## Key Entry Points

- Runtime: `runtime.py`
- Standalone app: `standalone.py`
- Workbench UI: `ui.py`
- Forms: `forms.py`
- Wizards: `wizards.py`
- Controls: `controls.py`
- Assistant support: `agent.py`
- Release evidence: `release_evidence.py`

## One-PBC App Surface

The package exposes:

- a standalone in-memory service for program design, beneficiary journeys, outcomes, evidence packs, donor reports, and timelines,
- workbench forms for program setup, beneficiary enrollment, service capture, outcome follow-up, donor-report freeze, and assistant document intake,
- guided wizards for startup, beneficiary journey, donor reporting, and assistant preview,
- control evidence for theory-of-change readiness, eligibility and consent, dosage fidelity, evidence quality, donor-report freeze, and assistant guardrails,
- a workbench render contract with program, beneficiary, outcome, donor-report, and control-center panels.

## Verification

Primary verification lives in package-local tests under `tests/` and in the executable standalone smoke path inside `standalone.py`.
