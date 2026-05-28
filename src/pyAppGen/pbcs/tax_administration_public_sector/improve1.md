# Public Sector Tax Administration PBC Better-Than-World-Class Improvement Backlog

## Purpose

This file identifies, justifies, and describes 50 high-impact improvements for `tax_administration_public_sector`. The backlog is specific to taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration and is intended to move the PBC from release-auditable scaffolding toward complete, specialist-grade domain coverage.

## Current Domain Evidence Used

- Stable PBC key: `tax_administration_public_sector`.
- Domain purpose: Taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration.
- Owned domain tables: `taxpayer_account`, `tax_filing`, `assessment`, `audit_case`, `collection_action`, `appeal`, `tax_notice`, `tax_administration_public_sector_policy_rule`, `tax_administration_public_sector_runtime_parameter`, `tax_administration_public_sector_schema_extension`, `tax_administration_public_sector_control_assertion`, `tax_administration_public_sector_governed_model`.
- Public APIs: `POST /taxpayer-accounts`, `POST /tax-filings`, `POST /assessments`, `POST /audit-cases`, `POST /collection-actions`, `GET /tax-administration-public-sector-workbench`.
- Emitted AppGen-X events: `TaxAdministrationPublicSectorCreated`, `TaxAdministrationPublicSectorUpdated`, `TaxAdministrationPublicSectorApproved`, `TaxAdministrationPublicSectorExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Current standard surfaces include: `taxpayer_account_management`, `tax_administration_public_sector_workflow`, `tax_administration_public_sector_analytics`, `configuration_schema`, `rule_engine`, `parameter_engine`, `owned_schema_migrations_models`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `retry_dead_letter_evidence`.
- Current advanced surfaces include: `tax_administration_public_sector_event_sourced_operational_history`, `tax_administration_public_sector_multi_tenant_policy_isolation`, `tax_administration_public_sector_schema_evolution_resilience`, `tax_administration_public_sector_autonomous_anomaly_detection`, `tax_administration_public_sector_semantic_document_instruction_understanding`, `tax_administration_public_sector_predictive_risk_scoring`, `tax_administration_public_sector_counterfactual_scenario_simulation`, `tax_administration_public_sector_cryptographic_audit_proofs`.

## 50 High-Impact Improvements

### 1. Canonical lifecycle state model for Taxpayer Account

**Justification:** This closes shallow CRUD gaps by making every public sector tax administration transition explainable and testable instead of implicit in free-form status values.

**Improvement:** Define a complete state machine for `taxpayer_account` with explicit draft, validated, blocked, approved, active, suspended, corrected, closed, archived, and reopened states. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** State-transition tests, invalid-transition fixtures, workbench state badges, and emitted AppGen-X transition events for TaxAdministrationPublicSectorCreated, TaxAdministrationPublicSectorUpdated, TaxAdministrationPublicSectorApproved. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 2. Domain intake and normalization for Tax Filing

**Justification:** The PBC cannot reach complete domain coverage unless it handles the messy front door of taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration, not only already-clean records.

**Improvement:** Build a typed intake pipeline for `tax_filing` that accepts structured API payloads, document-derived instructions, batch loads, and assistant-generated drafts while normalizing identifiers, dates, units, parties, and jurisdictional context. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Golden intake fixtures, rejected-record queues, field-level normalization evidence, and assistant previews before governed datastore mutation. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 3. Specialist validation rules for Assessment

**Justification:** World-class Public Sector Tax Administration requires rules that domain experts can reason about, version, test, and roll back without code edits.

**Improvement:** Add a domain rule compiler for `assessment` that supports threshold rules, eligibility rules, dependency rules, temporal windows, conflicting-instruction detection, and override justification. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Rule simulation tests, versioned rule manifests, rule impact reports, and UI rule editors linked to `TAX_ADMINISTRATION_PUBLIC_SECTOR_DATABASE_URL, TAX_ADMINISTRATION_PUBLIC_SECTOR_EVENT_TOPIC, TAX_ADMINISTRATION_PUBLIC_SECTOR_RETRY_LIMIT`. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 4. Parameter governance and tuning for Audit Case

**Justification:** Parameters are where operations teams tune public sector tax administration; unbounded constants would make the PBC brittle and unsafe in real deployments.

**Improvement:** Expose bounded runtime parameters for `audit_case` covering risk thresholds, SLA windows, confidence floors, escalation cutoffs, batch sizes, retry limits, and human-confirmation requirements. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Parameter schema validation, tenant overrides, approval history, rollback controls, and workbench diff views. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 5. Deep owned schema expansion for Collection Action

**Justification:** A single payload column cannot express the full surface of taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration or prove cross-PBC boundaries are respected.

**Improvement:** Extend the owned schema around `collection_action` with normalized child tables for line-level evidence, party roles, approvals, attachments, comments, metrics, exception reasons, and control assertions. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Migrations, models, relationship tests, schema contract snapshots, and no shared-table access outside the `tax_administration_public_sector_` namespace. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 6. Event-sourced operational history for Appeal

**Justification:** Temporal reconstruction is essential for better-than-world-class auditability and dispute resolution in public sector tax administration.

**Improvement:** Capture every material mutation of `appeal` as immutable AppGen-X events with actor, tenant, command, policy version, idempotency key, before/after summary, and projection checkpoint. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Replay tests, projection checksums, event ordering evidence, and point-in-time workbench views. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 7. Projection and read-model strategy for Tax Notice

**Justification:** The workbench should not force users to infer domain truth from raw tables; each projection should answer a real operating question.

**Improvement:** Create purpose-built projections for `tax_notice`: operational queue, executive KPI rollup, exception aging, compliance evidence, agent task context, and external dependency health. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Projection contracts, freshness SLAs, backfill tests, and visible stale-projection warnings. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 8. Exception taxonomy and remediation for Tax Administration Public Sector Policy Rule

**Justification:** High-value PBCs win on exception throughput; generic “failed” states hide the details operators need.

**Improvement:** Model the full exception taxonomy for `tax_administration_public_sector_policy_rule`, including severity, root cause, blocking dependency, remediation owner, due date, retry eligibility, escalation path, and closure evidence. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Exception queues, aging metrics, remediation playbooks, dead-letter linkage, and closure test fixtures for schedule slippage. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 9. Predictive risk scoring for Tax Administration Public Sector Runtime Parameter

**Justification:** The package should warn users before public sector tax administration work fails, breaches policy, or creates downstream cost.

**Improvement:** Add predictive risk scoring for `tax_administration_public_sector_runtime_parameter` using domain features from owned tables, consumed events PolicyChanged, AuditEventSealed, OperationalKpiChanged, rule outcomes, aging, anomaly signals, and historical corrections. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Feature manifests, score explanations, calibration reports, drift alerts, and tests for low/medium/high-risk scenarios. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 10. Counterfactual simulation for Tax Administration Public Sector Schema Extension

**Justification:** Advanced users need to ask “what would happen if” before committing changes to live taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration operations.

**Improvement:** Provide scenario simulation for `tax_administration_public_sector_schema_extension`: policy change, capacity constraint, deadline shift, price/rate change, eligibility change, disruption, and manual override outcomes. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Simulation APIs, non-mutating sandbox state, comparison reports, and workbench side-by-side scenario panels. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 11. Autonomous anomaly triage for Tax Administration Public Sector Control Assertion

**Justification:** A world-class PBC should reduce analyst burden without hiding the reasoning behind automated triage.

**Improvement:** Implement anomaly detection for `tax_administration_public_sector_control_assertion` that identifies outliers, duplicate submissions, impossible sequences, stale dependencies, unusual amounts/counts/durations, and contradictory fields. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Explainable anomaly cards, reviewer feedback loops, false-positive tracking, and suppression governance. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 12. Semantic document understanding for Tax Administration Public Sector Governed Model

**Justification:** Document-heavy work in Public Sector Tax Administration cannot be complete if the assistant only answers questions and cannot prepare accurate governed changes.

**Improvement:** Train the package assistant to parse domain documents and instructions for `tax_administration_public_sector_governed_model`, extract obligations, dates, parties, quantities, identifiers, and exceptions, then map them to safe draft mutations. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Document extraction tests, confidence thresholds, redaction handling, source span citations, and human confirmation workflows. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 13. Agent-safe CRUD execution for Taxpayer Account

**Justification:** The PBC agent must be a first-class operator but never a hidden bypass around RBAC, rules, or owned datastore boundaries.

**Improvement:** Add a professional chatbot skill for `taxpayer_account` that can create, update, correct, close, and annotate records only through policy-checked commands, approval gates, and previewed diffs. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Skill manifests, permission tests, preview/confirm flows, blocked-action evidence, and audit events for every assistant mutation. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 14. Workbench persona coverage for Tax Filing

**Justification:** A generic detail page underserves the domain; each role needs the exact controls and evidence they use daily.

**Improvement:** Design dedicated workbench panels for `tax_filing`: operator queue, supervisor approvals, analyst exceptions, auditor evidence, configuration owner, and agent-assistance review. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** UI contract entries, route tests, empty/error/loading states, and permission-aware action availability. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 15. Cross-PBC dependency contracts for Assessment

**Justification:** Composable packages fail when hidden table coupling enters the domain model.

**Improvement:** Represent dependencies for `assessment` through declared APIs, consumed events PolicyChanged, AuditEventSealed, OperationalKpiChanged, and projections rather than shared tables, with explicit freshness, ownership, and fallback behavior. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Dependency manifests, contract tests, stale dependency alerts, and no foreign-table references in generated artifacts. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 16. API completeness and versioning for Audit Case

**Justification:** Complete domain coverage requires both command and query surfaces, not only happy-path create endpoints.

**Improvement:** Expand APIs beyond POST /taxpayer-accounts, POST /tax-filings, POST /assessments to cover search, validation-only commands, simulation, bulk intake, exception closure, evidence export, projection reads, and idempotent corrections. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** OpenAPI-style route manifests, backward-compatible version tests, deprecation metadata, and idempotency assertions. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 17. Typed emitted-event expansion for Collection Action

**Justification:** Consumers should understand what happened in Public Sector Tax Administration without parsing opaque payloads.

**Improvement:** Replace generic lifecycle emissions with typed events for each meaningful `collection_action` transition, exception, approval, correction, simulation result, and downstream handoff. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Event schema tests, event examples, compatibility checks, and emitted-event coverage in release evidence. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 18. Consumed-event handlers for Appeal

**Justification:** A PBC is composable only when incoming events affect its own domain state predictably and safely.

**Improvement:** Implement idempotent handlers for consumed events PolicyChanged, AuditEventSealed, OperationalKpiChanged that update projections, open dependency exceptions, recalculate risk, and preserve source event lineage. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Duplicate-event tests, handler side-effect boundaries, dead-letter fixtures, and lineage links back to source events. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 19. Retry and dead-letter operations for Tax Notice

**Justification:** Dead letters are not just plumbing; they are domain work queues that can block taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration.

**Improvement:** Create operational tools for retrying, quarantining, explaining, and resolving dead-lettered `tax_notice` events with max-attempt policy, poison-message detection, and replay safety. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Dead-letter workbench, retry eligibility tests, replay audit proof, and operator action logs. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 20. RBAC and attribute policy for Tax Administration Public Sector Policy Rule

**Justification:** High-impact domain operations need finer controls than generic RBAC grants.

**Improvement:** Extend permissions for `tax_administration_public_sector_policy_rule` from coarse read/create/update/admin to action-level and attribute-aware policies based on role, tenant, jurisdiction, monetary/materiality threshold, and exception severity. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Permission matrix docs, ABAC policy tests, denied-action UI states, and assistant skill permission checks. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 21. Continuous control testing for Tax Administration Public Sector Runtime Parameter

**Justification:** Controls should run during operations, not only during release audit or manual review.

**Improvement:** Embed control assertions for `tax_administration_public_sector_runtime_parameter` that continuously test segregation of duties, required approvals, stale exceptions, policy drift, duplicate records, and boundary violations. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Control dashboards, failing-control events, test fixtures, and release evidence tied to `tax_administration_public_sector_control_assertion` records. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 22. Cryptographic audit proofing for Tax Administration Public Sector Schema Extension

**Justification:** Better-than-world-class auditability requires proof of integrity, not merely logs stored in mutable tables.

**Improvement:** Hash-chain material `tax_administration_public_sector_schema_extension` decisions, documents, emitted events, and release-evidence snapshots to make tampering visible without exposing sensitive payloads. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Proof manifests, verification APIs, redacted proof exports, and audit-ledger handoff events. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 23. Privacy, consent, and secrecy controls for Tax Administration Public Sector Control Assertion

**Justification:** Complete domain coverage must account for protected data and restricted operational evidence.

**Improvement:** Add field-level privacy classifications for `tax_administration_public_sector_control_assertion`, consent checks, masking rules, retention schedules, legal holds, and assistant redaction policies. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Retention tests, masked UI snapshots, consent-blocked mutation fixtures, and export controls. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 24. Multi-tenant operating model for Tax Administration Public Sector Governed Model

**Justification:** The PBC should scale across organizations while preserving independent policy and compliance boundaries.

**Improvement:** Support tenant-specific `tax_administration_public_sector_governed_model` rules, data residency, encryption context, configuration, seed data, and release evidence without allowing cross-tenant leakage. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Tenant isolation tests, tenant-scoped parameters, key-rotation evidence, and cross-tenant negative fixtures. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 25. Schema evolution and extension registry for Taxpayer Account

**Justification:** Domain teams will add fields; the PBC must evolve without breaking APIs, events, or workbench projections.

**Improvement:** Make schema extensions for `taxpayer_account` first-class with compatibility checks, migration previews, projection backfills, field ownership, and rollback metadata. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Extension registry UI, compatibility tests, migration dry-runs, and backfill release evidence. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 26. Master data quality gates for Tax Filing

**Justification:** Many public sector tax administration errors begin as bad reference data; the PBC should catch them before workflow execution.

**Improvement:** Define reference-data contracts for `tax_filing`: canonical codes, parties, locations, classifications, calendars, units, currencies, products, assets, or service categories as relevant to the domain. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Reference validation fixtures, stale-code warnings, mapping tables, and dependency freshness indicators. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 27. Bulk operations and correction workflows for Assessment

**Justification:** Enterprise-scale Public Sector Tax Administration users cannot operate one record at a time.

**Improvement:** Add bulk load, bulk validate, bulk approve, and bulk correction workflows for `assessment` with partial success, row-level errors, resumability, and rollback. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** CSV/API batch fixtures, resumable job state, row-level audit evidence, and assistant-generated correction suggestions. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 28. Lifecycle collaboration and tasking for Audit Case

**Justification:** Domain collaboration should live inside the PBC boundary and remain auditable with the record it affects.

**Improvement:** Attach tasks, comments, ownership, due dates, handoffs, and escalation threads to `audit_case` without leaking into external shared task tables. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Task tables, comment audit history, notification events, escalation SLAs, and role-specific task queues. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 29. SLA and service-level governance for Collection Action

**Justification:** Users need to know when taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration is late, blocked, or at risk before customer or regulator impact.

**Improvement:** Define SLAs for `collection_action` across intake, validation, approval, exception resolution, event handling, downstream projection refresh, and release-evidence generation. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** SLA breach events, timers, configurable calendars, workbench aging buckets, and tests for pause/resume behavior. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 30. Operational analytics cockpit for Appeal

**Justification:** World-class operations require leading indicators, not only record counts.

**Improvement:** Build analytics for `appeal`: throughput, backlog, aging, approval latency, exception rate, risk distribution, automation acceptance, correction rate, and downstream dependency health. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Metric definitions, projection tests, drill-through routes, export APIs, and anomaly overlays. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 31. Decision intelligence and recommendations for Tax Notice

**Justification:** The PBC should help expert users decide faster while showing evidence and uncertainty.

**Improvement:** Generate ranked recommendations for `tax_notice` such as next best action, likely resolution, required evidence, policy adjustment, staffing/capacity response, or downstream handoff. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Recommendation explanations, confidence intervals, feedback capture, model governance records, and rejection reasons. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 32. Quality and completeness scoring for Tax Administration Public Sector Policy Rule

**Justification:** Operators should see whether a record is truly ready, not just technically saved.

**Improvement:** Score each `tax_administration_public_sector_policy_rule` record for completeness, consistency, policy readiness, dependency readiness, evidence sufficiency, and downstream composability. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Scoring rules, missing-evidence lists, readiness badges, and blocking criteria in command handlers. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 33. End-to-end scenario library for Tax Administration Public Sector Runtime Parameter

**Justification:** Release evidence is stronger when every important public sector tax administration behavior has executable examples.

**Improvement:** Create seeded scenarios for `tax_administration_public_sector_runtime_parameter`: normal flow, urgent path, exception path, corrected path, duplicate path, late event path, and audit export path. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Scenario seed data, runtime smoke coverage, generated-app fixtures, and story-level workbench screenshots/contracts. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 34. Domain ontology and terminology model for Tax Administration Public Sector Schema Extension

**Justification:** Precise vocabulary prevents the PBC from misclassifying specialist documents or user instructions.

**Improvement:** Add an ontology for `tax_administration_public_sector_schema_extension` terms, synonyms, classifications, relationships, allowed values, and phrase mappings used by the assistant and UI. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Ontology files, assistant parsing tests, UI glossary, and mapping evidence for domain-specific abbreviations. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 35. Advanced search and investigation for Tax Administration Public Sector Control Assertion

**Justification:** Investigators and operators need fast, explainable retrieval across the whole domain surface.

**Improvement:** Provide search across `tax_administration_public_sector_control_assertion` records, events, documents, exceptions, tasks, comments, and audit proofs with filters for tenant, status, risk, date, party, and dependency. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Search index contracts, result provenance, permission-filtered queries, and stale-index warnings. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 36. Reconciliation and closure controls for Tax Administration Public Sector Governed Model

**Justification:** Closure is not complete until the PBC can prove no material domain work remains unresolved.

**Improvement:** Add reconciliation workflows that compare `tax_administration_public_sector_governed_model` state against consumed events, external projections, expected totals/counts, approvals, and release evidence before closure. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Reconciliation reports, variance thresholds, closure blockers, and AppGen-X closure events. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 37. Regulatory and policy reporting for Taxpayer Account

**Justification:** World-class PBCs turn operational evidence into credible reporting without spreadsheet reconstruction.

**Improvement:** Generate domain reporting packs for `taxpayer_account` covering statutory, contractual, operational, board, customer, or regulator evidence depending on contractual obligations, site progress evidence, physical asset state, commercial controls, safety constraints, change events, and long-horizon lifecycle accountability. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Report schemas, redaction rules, traceable metric sources, and approval/export audit events. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 38. Carbon and resource awareness for Tax Filing

**Justification:** Sustainability evidence should be embedded in operations instead of treated as an after-the-fact report.

**Improvement:** Where relevant, attach carbon, energy, water, travel, capacity, compute, or resource-footprint metadata to `tax_filing` decisions and batch operations. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Footprint fields, scheduling parameters, exception rules, and dashboards that expose operational tradeoffs. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 39. Resilience and offline behavior for Assessment

**Justification:** Real operations keep moving during outages; the PBC must preserve correctness when dependencies are unavailable.

**Improvement:** Define resilience modes for `assessment`: degraded dependency mode, offline draft capture, delayed event replay, conflict detection, and safe recovery after partial failure. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Offline fixtures, replay tests, conflict queues, recovery logs, and user-visible degraded-mode warnings. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 40. Human-in-the-loop automation for Audit Case

**Justification:** Automation should accelerate taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration while preserving accountability for high-risk decisions.

**Improvement:** Set explicit automation boundaries for `audit_case`: auto-approve, auto-reject, suggest-only, require-review, and block-until-evidence states with policy-based routing. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Automation policy tests, reviewer queues, override reasons, and assistant action audit trails. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 41. Package discovery and fit scoring for Collection Action

**Justification:** Users selecting PBCs need transparent fit reasoning, especially when domains are adjacent but not overlapping.

**Improvement:** Improve package metadata so composition can explain when `tax_administration_public_sector` fits a prompt, what entities it owns, what APIs/events it exposes, and what adjacent PBCs it depends on. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Discovery manifests, prompt-selection tests, overlap rationale links, and composition DSL examples. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 42. Configuration deployment pipeline for Appeal

**Justification:** Configuration changes can materially alter public sector tax administration; they need the same discipline as code releases.

**Improvement:** Add configuration promotion for `appeal` across draft, test, approved, active, deprecated, and rollback states with impact analysis before activation. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Config diff views, approval workflows, simulation before activation, and rollback tests. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 43. Workbench command completeness for Tax Notice

**Justification:** A PBC does not fully surface its capabilities if users must call hidden APIs for core work.

**Improvement:** Expose every high-value operation for `tax_notice` in the UI: create, validate, approve, simulate, correct, assign, export, retry, close, and audit-proof verification. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** UI action coverage tests, permission-aware disabled states, keyboard paths, and assistant handoff links. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 44. Document packet and evidence vault for Tax Administration Public Sector Policy Rule

**Justification:** Documents often carry the legal or operational truth behind taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration.

**Improvement:** Create a governed evidence vault for `tax_administration_public_sector_policy_rule` documents, attachments, source spans, extracted fields, signatures, approvals, and retention labels. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Evidence models, source-to-field lineage, signature validation, retention policies, and proof exports. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 45. Data correction and amendment history for Tax Administration Public Sector Runtime Parameter

**Justification:** World-class systems correct mistakes without rewriting history or confusing downstream consumers.

**Improvement:** Support formal amendments for `tax_administration_public_sector_runtime_parameter` that preserve original values, correction reason, approving actor, effective date, downstream event impacts, and replay behavior. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Amendment tables, correction events, projection replay tests, and side-by-side before/after UI. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 46. External participant collaboration for Tax Administration Public Sector Schema Extension

**Justification:** Many public sector tax administration workflows require outside parties, but they must not gain direct access to internal tables.

**Improvement:** Add controlled collaboration portals or API views for external participants related to `tax_administration_public_sector_schema_extension`, limited to scoped evidence submission, status checks, comments, and dispute responses. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Participant role policies, scoped tokens, submission audit trails, and inbound evidence validation. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 47. Advanced dependency freshness scoring for Tax Administration Public Sector Control Assertion

**Justification:** A record may be valid locally but unsafe if dependency evidence is stale or incomplete.

**Improvement:** Score freshness and reliability of dependencies used by `tax_administration_public_sector_control_assertion`, including consumed events PolicyChanged, AuditEventSealed, OperationalKpiChanged, referenced projections, configuration versions, and external submissions. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Freshness indicators, blocking rules, stale-event simulations, and workbench dependency health panels. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 48. Model governance and explainability for Tax Administration Public Sector Governed Model

**Justification:** Governed AI is mandatory for professional-grade automation in Public Sector Tax Administration.

**Improvement:** For every predictive or agentic feature around `tax_administration_public_sector_governed_model`, record model version, prompt or ruleset version, training/evaluation evidence, confidence, explanation, and human feedback. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Model cards, prompt/version manifests, feedback loops, drift tests, and audit proof for recommendations. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 49. High-scale partitioning and archival for Taxpayer Account

**Justification:** Better-than-world-class packages must remain operable after years of high-volume domain history.

**Improvement:** Plan scale behavior for `taxpayer_account`: tenant partitioning, archival policies, cold storage, retention-aware search, projection compaction, and large-batch replay. Tie the behavior to `tax_administration_public_sector_create_taxpayer_account_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Partition tests, archive/retrieve fixtures, retention enforcement, and replay benchmarks. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 50. Release gate expansion for Tax Filing

**Justification:** The PBC should not claim domain coverage unless release evidence proves the claim end to end.

**Improvement:** Expand release gates for `tax_administration_public_sector` so every schema, service, API, event, handler, UI, rule, parameter, agent skill, seed scenario, and improvement backlog item maps to executable evidence. Tie the behavior to `tax_administration_public_sector_record_tax_filing_workflow` where applicable, and make it visible in `TaxAdministrationPublicSectorWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Release audit checks, manifest traceability, generated-app smoke tests, and missing-capability blockers. The evidence should be package-local in `src/pyAppGen/pbcs/tax_administration_public_sector` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.
