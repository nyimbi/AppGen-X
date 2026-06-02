# Education Student Lifecycle Implementation Plan

## Objective

Make `education_student_lifecycle` usable as a standalone AppGen-X application when it is the only selected PBC. The package must support admissions, enrollment activation, curriculum planning, course registration, advising interventions, petitions, risk triage, graduation clearance, and credential conferral through owned records, command services, UI surfaces, assistant routing, and release evidence.

## Domain Scope

The PBC owns student applicants, applicant document evidence, enrollments, curriculum plans, course attempts, assessment results, advising cases, intervention plans, academic petitions, transfer-credit evaluations, degree audits, student risk signals, hold projections, engagement projections, accommodation projections, graduation clearances, credentials, governance records, and AppGen-X event tables.

Cross-PBC information is handled as future API or event projections. The package does not read or mutate foreign datastore tables.

## Implementation Slices

1. Standalone app runtime
   - Add an executable in-package student lifecycle app state and command surface.
   - Preserve PostgreSQL, MySQL, and MariaDB as the only normal backend choices.
   - Emit AppGen-X events through the package outbox contract.

2. Core lifecycle flows
   - Register applicants with stage and required-document checks.
   - Review applicant documents with confidence and reviewer gates.
   - Activate enrollment only after admission readiness and hold checks.
   - Manage curriculum plans, course attempts, assessment finalization, and transfer credit.

3. Student success and graduation flows
   - Open advising cases and block high-impact interventions until reviewer confirmation.
   - Track petitions, engagement projections, risk scores, and exception backlog.
   - Compute degree audits, graduation clearance, and credential conferral from owned records.

4. Single-PBC UI and assistant
   - Expose forms for applicants, documents, enrollment, curriculum, registration, advising, petitions, and credentials.
   - Expose guided wizards for applicant-to-matriculation, intervention, graduation clearance, and first-run setup.
   - Expose blocking controls for admissions decisions, course registration, interventions, clearance, and credential issuance.
   - Route transcripts, petitions, risk memos, graduation packets, and advising notes into confirmed mutation plans with stable document hashes.

5. Verification
   - Add package-local tests for the executable flow, controls, assistant routing, service state, release evidence, and runtime smoke.
   - Keep all edits inside `src/pyAppGen/pbcs/education_student_lifecycle`.

## Acceptance Checks

- Package-local tests pass.
- Runtime smoke includes the student lifecycle app smoke.
- Release evidence includes schema, services, APIs, events, handlers, UI, forms, wizards, controls, assistant, governance, and the single-PBC app.
- A one-PBC generated app has enough forms, wizards, controls, service methods, workbench queues, and assistant guidance to operate the student lifecycle domain.
