# Chemical Batch Compliance

`chemical_batch_compliance` is a standalone AppGen-X PBC for controlled chemical manufacturing, batch execution, quality disposition, safety document governance, hazardous-material qualification, regulatory dossier assembly, and assistant-governed document instructions. The PBC is implemented inside its own directory and can run as a one-PBC application with owned models, forms, wizards, controls, service commands, AppGen-X events, handlers, UI contracts, agent skills, and release evidence.

## Domain Coverage

The implemented package covers the table-stakes chemical compliance workflow from controlled master recipe through batch review:

- master formula revisions with composition windows, target concentrations, approved substitutes, effectivity, equipment classes, permit requirements, and technical/quality/EHS approval gates
- SDS review with jurisdiction, hazard summary, exposure controls, document digest, approval state, and release dependency checks
- hazardous material qualification with GHS classification, storage class, approved sources, PPE requirements, and label profile evidence
- stepwise electronic batch records bound to effective formula revisions with equipment readiness, line clearance, cleaning release, calibration, permits, step timelines, dispense reconciliation, parameter logs, sampling plans, deviations, release decisions, and risk scores
- quality testing with specification evidence, OOS/OOT-style failure states, automatic compliance holds, and batch detail projections
- compliance hold placement/resolution with severity, disposition, release authority, and AppGen-X exception events
- regulatory submission dossiers assembled only from owned formula, batch, SDS, quality, and hold records
- configuration, bounded runtime parameters, policy rules, schema extensions, continuous control assertions, package-local release evidence, and source package registration metadata
- AI assistant skills for formula-release guidance, quality-hold triage, submission assembly, and document-instruction CRUD previews with human confirmation required for every mutation

## One-PBC Application

`standalone.py` exposes `ChemicalBatchComplianceStandaloneApp`, which bootstraps configuration, registers policy, receives AppGen-X policy events, creates SDS/hazard records, releases a formula, records a batch, opens a quality hold, assembles a regulatory dossier, and renders a workbench from the app-owned state. The standalone contract surfaces:

- forms for formula revision intake, batch execution, quality review, and assistant document instructions
- wizards for formula release, batch disposition, and regulatory dossiers
- controls for owned-table boundaries, formula release, line clearance, quality holds, and assistant mutation gating
- routes for forms, wizards, controls, formula release, batch execution, quality holds, regulatory dossiers, and agent preview
- DSL exposure for owned models, UI fragments, and the `chemical_batch_compliance_skills` namespace

## Main Runtime Entry Points

- `chemical_batch_compliance_create_formula_revision`
- `chemical_batch_compliance_release_formula_revision`
- `chemical_batch_compliance_review_sds_document`
- `chemical_batch_compliance_register_hazardous_material`
- `chemical_batch_compliance_record_batch`
- `chemical_batch_compliance_record_quality_test`
- `chemical_batch_compliance_place_compliance_hold`
- `chemical_batch_compliance_resolve_compliance_hold`
- `chemical_batch_compliance_create_regulatory_submission`
- `chemical_batch_compliance_create_document_instruction`
- `chemical_batch_compliance_query_workbench`
- `chemical_batch_compliance_build_workbench_view`
- `standalone_smoke_test`

## Boundaries

All datastore contracts are package-owned `chemical_batch_compliance_*` tables. Database backend declarations remain limited to PostgreSQL, MySQL, and MariaDB. Eventing uses the AppGen-X outbox/inbox/dead-letter contract, and no stream-engine picker is exposed to users.

## Validation

- `PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/chemical_batch_compliance`
- `PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/chemical_batch_compliance/tests`
- focused AppGen-X PBC release audits for source artifacts, package-local assurance, specification, agent capability, implementation, implemented capability, and generation smoke

See `implementation-status.md` for exact outcomes.
