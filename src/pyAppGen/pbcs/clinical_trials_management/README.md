# Clinical Trials Management PBC

`clinical_trials_management` is a package-local AppGen-X slice for trial protocol governance, site activation, subject screening and enrollment, informed consent, visit execution, adverse-event escalation, monitoring follow-up, lock readiness, and governed assistant support.

## What This Package Owns

- Clinical-trial-owned schema and migrations for protocols, study sites, subjects, consent records, visit schedules, adverse events, monitoring findings, rules, parameters, schema extensions, control assertions, governed models, inbox, outbox, and dead letters.
- Executable package-local contracts for services, routes, events, handlers, workbench UI, forms, wizards, controls, RBAC, configuration, and release evidence.
- Assistant document/instruction planning that stays inside the PBC boundary and requires preview plus confirmation before mutation.

## Domain Shape

This package is optimized for clinical operations teams who need to:

- activate protocols and sites with evidence-backed gates,
- enroll subjects only after consent and eligibility checks,
- manage visit windows and protocol deviations,
- escalate serious adverse events within configured SLAs,
- close monitoring findings and inspect lock blockers,
- tune trial rules and runtime parameters without leaving the package,
- use a package-local assistant to preview governed CRUD changes from trial notes or memos.

## Key Entry Points

- Runtime: [runtime.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/runtime.py)
- Services: [services.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/services.py)
- Routes: [routes.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/routes.py)
- Workbench UI: [ui.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/ui.py)
- Forms: [forms.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/forms.py)
- Wizards: [wizards.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/wizards.py)
- Controls: [controls.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/controls.py)
- Assistant support: [agent.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/agent.py)
- Standalone one-PBC app: [standalone.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/standalone.py)
- Release evidence: [release_evidence.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/release_evidence.py)

## One-PBC App Surface

The package exposes:

- protocol, site, subject, consent, visit, safety, monitoring, rule, and parameter forms,
- guided wizards for startup, enrollment, visit/safety follow-up, lock review, and assistant previews,
- operational controls for activation gates, safety SLAs, lock readiness, and assistant guardrails,
- workbench bindings for amendment queues, site activation, screening, visit readiness, safety reporting, monitoring issues, and data-lock blockers,
- assistant previews that classify uploaded notes into bounded CRUD plans over package-owned tables only.

## Standalone App Contract

`ClinicalTrialsManagementStandaloneApp` proves that this PBC can run as the only package in a composed application. The smoke path configures trial parameters, registers safety and lock-readiness rules, receives a sponsor amendment event, and executes a realistic clinical-operations path:

- active protocol creation with amendment and regulatory evidence,
- site activation with investigator, IRB, readiness, and contract metadata,
- consent capture, subject enrollment, visit completion, and deviation tracking,
- serious adverse-event escalation against configured reporting windows,
- monitoring finding creation/resolution and data-lock readiness assessment,
- governed model registration and assistant preview generation for bounded CRUD changes.

The generated app contract exposes package-owned models, services, routes, event contracts, handlers, forms, wizards, controls, workbench views, assistant skills, RBAC, configuration, seed data, and release evidence without stream-engine pickers or shared tables.

## Verification

Primary verification lives in package-local tests under [tests](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/tests) and in the executable runtime smoke path inside [runtime.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/clinical_trials_management/runtime.py).

Latest focused verification for this slice:

- `PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/clinical_trials_management`
- `PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/clinical_trials_management/tests` -> 13 passed
- `standalone_smoke_test()` and `validate_release_evidence()` -> true
- focused source, package-local, specification, agent, implementation, implemented-capability, and generation audits -> true
- `git diff --check -- src/pyAppGen/pbcs/clinical_trials_management`
