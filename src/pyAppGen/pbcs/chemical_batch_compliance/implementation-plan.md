# Chemical Batch Compliance Implementation Plan

## Target Outcome

Make `chemical_batch_compliance` executable as a standalone one-PBC AppGen-X application for chemical manufacturing compliance. A user composing an app with only this PBC should receive owned schema/model contracts, service commands, routes, event contracts, handlers, workbench UI, forms, wizards, controls, agent skills, configuration/rules/parameters, package metadata, release evidence, and tests.

## Domain Design

1. Controlled formula governance
   - model formula revision identity, lifecycle state, effectivity, target concentration, composition windows, approved substitutes, required SDS records, hazardous-material records, permits, equipment classes, approvals, process steps, and evidence hashes
   - enforce technical, quality, and EHS approvals plus current SDS/material evidence before release

2. Safety and hazardous-material qualification
   - model SDS jurisdiction, hazard summary, exposure controls, status, issue/expiration dates, and document digest
   - model hazardous material GHS classification, approved sources, storage class, PPE, and label profile
   - keep SDS and hazardous-material approval as explicit release gates instead of advisory metadata

3. Electronic batch execution
   - bind each batch to an effective formula revision
   - require line clearance, cleaning release, calibration state, and permit confirmation before execution
   - record step timelines, critical-step deviations, dispense reconciliation, parameter logs, sampling plans, release decision, and deterministic risk scoring

4. Quality disposition and holds
   - record quality test evidence with specifications, result values, and result status
   - create compliance holds automatically for failed or invalid quality results
   - expose hold resolution and batch detail projections for review-by-exception workflows

5. Regulatory dossiers
   - assemble regulatory submissions only from owned source records
   - track jurisdiction, type, product code, source record IDs, commitment actions, and dossier readiness

6. Agent and document instructions
   - parse uploaded documents/instructions into CRUD previews against owned tables
   - require human confirmation for mutations
   - reject foreign-table mutation attempts and expose the skill namespace to the composed application DSL

7. One-PBC UI and app shell
   - provide forms for formula intake, batch execution, quality review, and assistant document instructions
   - provide wizards for formula release, batch disposition, and regulatory dossiers
   - provide controls for boundary, release, line-clearance, quality-hold, and agent mutation gates
   - provide a standalone app wrapper that can bootstrap and run a realistic demo workflow from owned state

## Scope Boundaries

- Stay inside `src/pyAppGen/pbcs/chemical_batch_compliance`
- Keep all table references owned by `chemical_batch_compliance`
- Use AppGen-X events only; do not expose stream-engine selection
- Keep ordinary backend declarations limited to PostgreSQL, MySQL, and MariaDB
- Do not change global generator or language files in this slice

## Verification Plan

- Compile the package with `PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/chemical_batch_compliance`
- Run package-local tests with `PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/chemical_batch_compliance/tests`
- Run focused PBC audits for source artifacts, package-local assurance, specification, agent capability, implementation, implemented capability, and generation smoke
- Run `git diff --check -- src/pyAppGen/pbcs/chemical_batch_compliance`
