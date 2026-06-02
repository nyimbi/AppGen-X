# Education Student Lifecycle

`education_student_lifecycle` is a standalone AppGen-X packaged business capability for admissions, enrollment, curriculum, advising, progression, risk, graduation, and credential operations.

## What This Package Provides

- Owned schema, models, services, routes, events, handlers, permissions, configuration, seed data, tests, and release evidence.
- A one-PBC executable app surface for applicant intake, document review, enrollment activation, curriculum planning, course registration, assessment finalization, intervention tracking, petitions, degree audit, graduation clearance, and credential conferral.
- Forms, wizards, and controls that keep mutations inside the PBC-owned datastore boundary with AppGen-X outbox/inbox semantics.
- Assistant document-routing plans for transcripts, petitions, advising/risk packets, degree audits, and graduation reviews.
- Workbench queues for admissions readiness, registration blockers, high-risk students, intervention follow-up, petition review, graduation candidates, clearance, and exception backlog.

## Standalone Surface

Primary executable commands:

- `register_student_applicant`
- `review_applicant_documents`
- `activate_enrollment`
- `maintain_curriculum_plan`
- `register_course_attempt`
- `finalize_assessment_result`
- `open_advising_case`
- `record_intervention_plan`
- `submit_academic_petition`
- `record_transfer_credit`
- `evaluate_degree_audit`
- `project_student_risk`
- `prepare_graduation_clearance`
- `award_credential`

Primary query:

- `build_student_lifecycle_workbench`

## Boundaries

The package owns only `education_student_lifecycle_*` tables plus its AppGen-X event tables. Shared-table access is disallowed. External dependencies must arrive as explicit APIs or event projections.

## Verification

Focused verification lives in `tests/test_contract.py` and `tests/test_student_lifecycle_app.py`.
