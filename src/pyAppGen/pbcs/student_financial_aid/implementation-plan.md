# Implementation Plan

## Goal

Turn `student_financial_aid` into a coherent package-local standalone PBC app with executable owned schema, database-backed contract artifacts, workflow services, route dispatch, UI/workbench metadata, governed assistant previews, focused tests, and release evidence without modifying shared generator or language infrastructure.

## Scope Chosen From `improve1.md`

The backlog is broader than one safe slice. This implementation covers the smallest standalone student-aid operating core that still reflects the requested domain breadth:

1. Aid year setup and packaging policy controls.
2. Student aid profile intake with FAFSA/ISIR-equivalent application capture.
3. Dependency review, verification tracking, and document intake governance.
4. Cost of attendance, need analysis, and award packaging across scholarships, grants, loans, and work study.
5. SAP, professional judgment, appeal, compliance, and communication records.
6. Disbursement scheduling, refund/return handling, and overaward controls.
7. Package-local workbench, detail views, forms, wizards, controls, and governed AI assistant previews.
8. AppGen-X inbox/outbox/dead-letter lineage, owned-table-only CRUD previews, and release audits.

## Architecture

### Shared Executable Core

- Add a package-local `slice_app.py` as the single executable source of truth.
- Keep owned-table metadata, route definitions, forms, wizards, controls, agent previews, and release-audit helpers in that shared core.
- Use a package-local SQLite harness only for smoke execution while public contracts continue to allow only PostgreSQL, MySQL, and MariaDB.

### Owned Models and Schema

- Replace the generic migration with one owned schema covering aid years, aid profiles, applications, dependency reviews, verification items, document tracking, SAP, cost of attendance, need analysis, award packages, award lines, scholarships, loans, work study, disbursements, return/refund cases, overaward cases, professional judgment cases, appeals, compliance obligations, communications, policies, parameters, controls, governed models, and AppGen-X event tables.
- Keep the model and schema contracts derived from the same owned table definitions so migrations, service contracts, and workbench metadata cannot drift.

### Runtime and Services

- Implement executable commands for the main domain workflows:
  - aid year setup
  - student aid profile creation
  - FAFSA/ISIR-equivalent intake
  - dependency review
  - verification document registration
  - SAP evaluation
  - cost-of-attendance capture
  - need analysis
  - award packaging
  - disbursement scheduling
  - refund/return and overaward review
  - professional judgment case handling
  - appeal recording
  - compliance obligation tracking
  - communication logging
- Keep runtime wrapper functions with the existing `student_financial_aid_*` entry points so repo tests still import the same symbols.

### UI and Governed Assistant

- Expose a workbench with domain panels, queues, KPIs, forms, wizards, controls, and release evidence navigation.
- Provide governed assistant document-intake and CRUD-preview plans that are limited to owned tables, require human confirmation for mutations, and never expose a stream-engine picker.

### Events and Handlers

- Keep AppGen-X as the only event contract.
- Preserve idempotent inbox handling, outbox evidence, and dead-letter capture for unexpected events.

## Validation Strategy

### Focused Tests

- Contract coverage:
  - schema, service, route, release, event, handler, UI, agent, config, and seed contracts
- Workflow coverage:
  - aid profile and application intake
  - dependency/verification and document tracking
  - need analysis and packaging
  - disbursement and overaward/refund handling
  - workbench projection and assistant previews
  - AppGen-X idempotency and dead-letter behavior

### Package Audits

- `python3 -m compileall src/pyAppGen/pbcs/student_financial_aid`
- `/Volumes/Media/src/pjs/appgen/.venv/bin/pytest src/pyAppGen/pbcs/student_financial_aid/tests tests/test_pbc_student_financial_aid_runtime.py`
- `git diff --check`
- focused source/package/spec/agent/implementation/capability/generation audits for `student_financial_aid`

## Requested Gate Mapping

- `pbc_source_artifact_contract`
  - satisfied by package-local schema, migration, models, service, route, event, handler, UI, agent, docs, and registration evidence.
- `pbc_implementation_release_audit`
  - satisfied by executable runtime smoke, workflow tests, workbench coverage, and package-local release evidence.
- `pbc_generation_smoke_audit`
  - satisfied by schema/model/route/workbench generation surfaces derived from the same shared core.

## Non-Goals For This Slice

- No foreign-table writes or shared-generator edits.
- No real external FAFSA, NSLDS, SIS, or payment-system integrations.
- No stream-processing selector or alternate event contract.
- No global framework plumbing outside this PBC directory.

## Deliverables

- Updated package-local code only under `src/pyAppGen/pbcs/student_financial_aid`
- `implementation-plan.md`
- `README.md`
- `implementation-status.md`
- refreshed `RELEASE_EVIDENCE.md`
- focused tests and verification evidence
