# Chemical Batch Compliance Specification

## Purpose

`chemical_batch_compliance` is a packaged business capability for chemical
manufacturing quality, safety, and regulatory control. This implementation is
not a generic scaffold anymore. It now owns one coherent executable slice:
controlled formula revision release, batch execution evidence, in-process
quality escalation, compliance holds, regulatory dossier assembly, and governed
assistant-driven document instructions.

The slice is designed to let this PBC function as a one-PBC app inside AppGen-X
without any central generator edits or foreign-table access. The package stays
inside its own datastore boundary, exposes its own commands and queries, and
integrates with the rest of AppGen-X only through declared APIs and AppGen-X
events.

## Stable Identity

- PBC key: `chemical_batch_compliance`
- Mesh: `opsmfg`
- Package directory: `src/pyAppGen/pbcs/chemical_batch_compliance`
- Runtime entrypoint: `chemical_batch_compliance_runtime_capabilities()`
- UI entrypoint: `chemical_batch_compliance_ui_contract()`
- Registration entrypoint: `implementation_contract()`
- Eventing standard: `AppGen-X`
- Allowed backends: PostgreSQL, MySQL, MariaDB
- Stream-engine picker: forbidden and hidden

The package must remain side-effect-free for discovery and metadata validation.
Registration plans and package metadata are computed without mutating any shared
registry.

## Owned Boundary

The package owns the following business tables:

- `chemical_batch_compliance_chemical_formula`
- `chemical_batch_compliance_batch_record`
- `chemical_batch_compliance_sds_document`
- `chemical_batch_compliance_hazardous_material`
- `chemical_batch_compliance_regulatory_submission`
- `chemical_batch_compliance_quality_test`
- `chemical_batch_compliance_compliance_hold`
- `chemical_batch_compliance_chemical_batch_compliance_policy_rule`
- `chemical_batch_compliance_chemical_batch_compliance_runtime_parameter`
- `chemical_batch_compliance_chemical_batch_compliance_schema_extension`
- `chemical_batch_compliance_chemical_batch_compliance_control_assertion`
- `chemical_batch_compliance_chemical_batch_compliance_governed_model`

It also owns the AppGen-X event tables:

- `chemical_batch_compliance_appgen_outbox_event`
- `chemical_batch_compliance_appgen_inbox_event`
- `chemical_batch_compliance_appgen_dead_letter_event`

No shared-table writes are allowed. No foreign-table reads are required for the
implemented slice. Collaboration with other PBCs is represented only by
declared route contracts and consumed AppGen-X events.

## Schema, Migrations, And Models

The package contains a real `migrations/001_initial.sql` file with domain
columns for recipe release, batch evidence, quality escalation, submission
dossiers, and governed assistant artifacts. The migration intentionally uses
portable `TEXT`, `JSON`, `BOOLEAN`, and `NUMERIC` types because the package
declares a backend allowlist across PostgreSQL, MySQL, and MariaDB.

Owned models are exposed in `models.py` as package-local dataclasses for the
main business entities. The most important models are:

- controlled formula revision
- electronic batch record
- SDS document
- hazardous material qualification
- quality test
- compliance hold
- regulatory submission dossier
- governed assistant document instruction

This gives the PBC an owned model vocabulary instead of relying only on opaque
payload blobs.

## Service And API Contract

The implemented command surface focuses on the chosen domain slice:

- `create_formula_revision`
- `release_formula_revision`
- `review_sds_document`
- `register_hazardous_material`
- `record_batch`
- `record_quality_test`
- `place_compliance_hold`
- `resolve_compliance_hold`
- `create_regulatory_submission`
- `register_rule`
- `set_parameter`
- `register_schema_extension`
- `upsert_control_assertion`
- `create_document_instruction`
- `update_document_instruction`
- `delete_document_instruction`

The query surface exposes:

- formula detail
- batch detail
- document instruction detail
- workbench summary and queues
- app surface metadata
- release evidence snapshot

Public APIs remain package-local and AppGen-X aligned:

- `POST /chemical-formulas`
- `POST /batch-records`
- `POST /sds-documents`
- `POST /hazardous-materials`
- `POST /regulatory-submissions`
- `GET /chemical-batch-compliance-workbench`

Routes map to owned commands or read-only workbench queries. All mutating
operations remain within the package boundary and are reported with outbox
evidence.

## Eventing, Inbox, Outbox, Retry, And Dead Letter

The event contract is fixed to `AppGen-X`. The package emits:

- `ChemicalBatchComplianceCreated`
- `ChemicalBatchComplianceUpdated`
- `ChemicalBatchComplianceApproved`
- `ChemicalBatchComplianceExceptionOpened`

It consumes:

- `PolicyChanged`
- `AuditEventSealed`
- `OperationalKpiChanged`

Handlers are idempotent by `idempotency_key`. Known consumed events are accepted
once and duplicate replays are reported as duplicates. Unknown events are routed
to the package-owned dead-letter table with retry metadata. This keeps the slice
safe for inbox processing without introducing cross-PBC persistence.

## Domain Rules, Parameters, And Configuration

Rules are explicit artifacts, not implied comments. The implemented rule set
includes formula effectivity gates, substitution controls, line-clearance
enforcement, parameter alarm handling, quality release policy, dossier
completeness, and assistant mutation guardrails.

Parameters are bounded and package-owned. They include potency drift tolerance,
misweigh alert percentage, critical alarm hold duration, SDS expiry warning
lead time, regulatory commitment SLA, and the workbench record limit.

Configuration remains minimal and package-local:

- database backend
- AppGen-X event topic
- retry limit
- default policy

All configuration validation remains deterministic and side-effect-free.

## UI, Workbench, Forms, Wizards, And Controls

The workbench is domain-specific. It is centered on:

- formula release queue
- batch review board
- quality and hold triage
- regulatory dossier monitor

Package-local forms cover formula revision intake, batch execution evidence,
quality review, and assistant document instruction intake. Wizards guide formula
release, batch disposition, and dossier assembly. Controls enforce owned-table
boundaries, formula release gates, line-clearance gating, automatic quality
hold escalation, and assistant mutation confirmation.

This is the one-PBC app surface requested for the slice. It is not dependent on
external UI modules outside this package.

## RBAC And Assistant Surface

RBAC is package-owned. Roles include operator, quality reviewer, EHS reviewer,
regulatory lead, auditor, and admin. Approval privileges are intentionally
narrower than create/update privileges.

The assistant surface supports:

- formula-release guidance
- quality hold triage
- submission assembly help
- document instruction management

Document and instruction intake produces governed CRUD previews. Mutations are
restricted to owned tables and require human confirmation. This satisfies the
agent/chatbot document-instruction CRUD requirement without crossing package
boundaries.

## Release Evidence, Seed Data, And Tests

`release_evidence.py` and `RELEASE_EVIDENCE.md` capture schema, services,
events, handlers, workbench surfaces, governance, and assistant CRUD support.
`seed_data.py` now describes realistic demo seed records for SDS, hazardous
material, formula, batch, and document instruction artifacts.

Focused tests cover:

- metadata and contract shape
- formula release gates
- batch, quality, and hold flow
- governed document-instruction CRUD
- route dispatch and workbench surfaces
- event handler idempotency and dead-letter behavior

## Manifest Traceability Appendix

The PBC assistant contributes the `chemical_batch_compliance_skills` skill namespace for document/instruction intake, governed CRUD mutation previews, batch review help, formula release guidance, quality hold triage, and regulatory dossier assembly.

- tables: chemical_formula, batch_record, sds_document, hazardous_material,
  regulatory_submission, quality_test, compliance_hold,
  chemical_batch_compliance_policy_rule,
  chemical_batch_compliance_runtime_parameter,
  chemical_batch_compliance_schema_extension,
  chemical_batch_compliance_control_assertion,
  chemical_batch_compliance_governed_model
- apis: `POST /chemical-formulas`, `POST /batch-records`,
  `POST /sds-documents`, `POST /hazardous-materials`,
  `POST /regulatory-submissions`,
  `GET /chemical-batch-compliance-workbench`
- emits: `ChemicalBatchComplianceCreated`,
  `ChemicalBatchComplianceUpdated`,
  `ChemicalBatchComplianceApproved`,
  `ChemicalBatchComplianceExceptionOpened`
- consumes: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- ui fragments: `ChemicalBatchComplianceWorkbench`,
  `ChemicalBatchComplianceDetail`,
  `ChemicalBatchComplianceAssistantPanel`
- permissions: `chemical_batch_compliance.read`,
  `chemical_batch_compliance.create`,
  `chemical_batch_compliance.update`,
  `chemical_batch_compliance.approve`,
  `chemical_batch_compliance.admin`
- configuration: `CHEMICAL_BATCH_COMPLIANCE_DATABASE_URL`,
  `CHEMICAL_BATCH_COMPLIANCE_EVENT_TOPIC`,
  `CHEMICAL_BATCH_COMPLIANCE_RETRY_LIMIT`,
  `CHEMICAL_BATCH_COMPLIANCE_DEFAULT_POLICY`
- standard features: schema/migrations/models, service/api contracts,
  AppGen-X events, idempotent handlers, retry/dead-letter evidence, RBAC,
  parameters, rules, workbench, governed assistant CRUD, release evidence
- standard features exact manifest values: chemical_formula_management,
  chemical_batch_compliance_workflow,
  chemical_batch_compliance_analytics, configuration_schema, rule_engine,
  parameter_engine, owned_schema_migrations_models,
  appgen_x_outbox_inbox_eventing, idempotent_handlers,
  retry_dead_letter_evidence, permissions, seed_data, workbench,
  agentic_document_instruction_intake, governed_datastore_crud,
  ai_agent_task_assistance, configuration_workbench,
  continuous_release_assurance
- advanced capabilities: event-sourced history, multi-tenant isolation,
  schema evolution resilience, anomaly detection, semantic document
  understanding, predictive risk scoring, counterfactual assessment,
  cryptographic audit proofs, continuous control testing, sustainability
  awareness, cross-PBC event federation, governed AI execution
- advanced capabilities exact manifest values:
  chemical_batch_compliance_event_sourced_operational_history,
  chemical_batch_compliance_multi_tenant_policy_isolation,
  chemical_batch_compliance_schema_evolution_resilience,
  chemical_batch_compliance_autonomous_anomaly_detection,
  chemical_batch_compliance_semantic_document_instruction_understanding,
  chemical_batch_compliance_predictive_risk_scoring,
  chemical_batch_compliance_counterfactual_scenario_simulation,
  chemical_batch_compliance_cryptographic_audit_proofs,
  chemical_batch_compliance_continuous_control_testing,
  chemical_batch_compliance_carbon_and_sustainability_awareness,
  chemical_batch_compliance_cross_pbc_event_federation,
  chemical_batch_compliance_governed_ai_agent_execution
