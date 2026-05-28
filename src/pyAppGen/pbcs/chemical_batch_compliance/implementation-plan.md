# Chemical Batch Compliance Implementation Plan

## Selected Slice

Implement a controlled chemical recipe and batch-release slice that makes
`chemical_batch_compliance` usable as a one-PBC app for chemical manufacturing
compliance work:

- controlled formula revisions with effectivity, approvals, and composition bands
- batch records bound to released formula revisions with stepwise execution data
- SDS and hazardous-material qualification gates required before formula release
- in-process quality testing with automatic compliance-hold creation on failure
- regulatory dossier assembly from owned records only
- governed document-instruction CRUD support for the assistant/chatbot surface
- package-local workbench UI, forms, wizards, controls, RBAC, configuration, and release evidence

## Scope Boundaries

- Stay inside `src/pyAppGen/pbcs/chemical_batch_compliance`
- Keep AppGen-X as the only event contract
- Keep all persistence contracts confined to `chemical_batch_compliance_*` tables
- Do not introduce shared-table reads, central generator changes, or new dependencies
- Keep the implementation executable in pure Python with package-local tests

## Planned Code Changes

1. Add a package-local domain application module that owns:
   - in-memory runtime state
   - owned table metadata
   - domain commands and queries
   - deterministic event envelopes and evidence hashing
   - workbench/app-surface assembly
2. Replace the generated runtime/service/route wrappers so they expose:
   - formula authoring and release
   - SDS and hazardous-material qualification
   - batch recording and review
   - quality-test and compliance-hold handling
   - document-instruction CRUD previews
3. Replace migration/model/schema artifacts with domain-specific fields for:
   - formula revisions
   - batch execution
   - safety documents
   - hazardous materials
   - submissions, holds, tests, rules, parameters, controls, and governed document instructions
4. Update UI, permissions, config, seed data, specification, README, and release evidence to describe the implemented slice rather than the generic scaffold.
5. Add focused tests for:
   - formula release preconditions
   - batch/quality/hold flow
   - document-instruction CRUD support
   - route and workbench surface contracts
   - handler idempotency and dead-letter behavior

## Validation Plan

- Run `compileall` on the PBC package
- Run package-local `pytest` for `chemical_batch_compliance/tests`
- Run a targeted runtime smoke command that exercises the implemented slice end to end
- Record exact outcomes in `implementation-status.md`

## Out Of Scope

- plant-wide inventory reconciliation outside owned records
- external lab integrations
- multi-PBC orchestration or shared projections
- advanced predictive models beyond deterministic risk scoring summaries
