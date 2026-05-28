# Actuarial Pricing and Reserving PBC Better-Than-World-Class Improvement Backlog

## Purpose

This file identifies, justifies, and describes 50 high-impact improvements for `actuarial_pricing_reserving`. The backlog is specific to rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls and is intended to move the PBC from release-auditable scaffolding toward complete, specialist-grade domain coverage.

## Current Domain Evidence Used

- Stable PBC key: `actuarial_pricing_reserving`.
- Domain purpose: Rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls.
- Owned domain tables: `rating_model`, `actuarial_assumption`, `experience_study`, `reserve_estimate`, `loss_triangle`, `capital_scenario`, `model_validation`, `actuarial_pricing_reserving_policy_rule`, `actuarial_pricing_reserving_runtime_parameter`, `actuarial_pricing_reserving_schema_extension`, `actuarial_pricing_reserving_control_assertion`, `actuarial_pricing_reserving_governed_model`.
- Public APIs: `POST /rating-models`, `POST /actuarial-assumptions`, `POST /experience-studys`, `POST /reserve-estimates`, `POST /loss-triangles`, `GET /actuarial-pricing-reserving-workbench`.
- Emitted AppGen-X events: `ActuarialPricingReservingCreated`, `ActuarialPricingReservingUpdated`, `ActuarialPricingReservingApproved`, `ActuarialPricingReservingExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Current standard surfaces include: `rating_model_management`, `actuarial_pricing_reserving_workflow`, `actuarial_pricing_reserving_analytics`, `configuration_schema`, `rule_engine`, `parameter_engine`, `owned_schema_migrations_models`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `retry_dead_letter_evidence`.
- Current advanced surfaces include: `actuarial_pricing_reserving_event_sourced_operational_history`, `actuarial_pricing_reserving_multi_tenant_policy_isolation`, `actuarial_pricing_reserving_schema_evolution_resilience`, `actuarial_pricing_reserving_autonomous_anomaly_detection`, `actuarial_pricing_reserving_semantic_document_instruction_understanding`, `actuarial_pricing_reserving_predictive_risk_scoring`, `actuarial_pricing_reserving_counterfactual_scenario_simulation`, `actuarial_pricing_reserving_cryptographic_audit_proofs`.

## 50 High-Impact Improvements

### 1. Canonical lifecycle state model for Rating Model

**Justification:** This closes shallow CRUD gaps by making every actuarial pricing and reserving transition explainable and testable instead of implicit in free-form status values.

**Improvement:** Define a complete state machine for `rating_model` with explicit draft, validated, blocked, approved, active, suspended, corrected, closed, archived, and reopened states. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** State-transition tests, invalid-transition fixtures, workbench state badges, and emitted AppGen-X transition events for ActuarialPricingReservingCreated, ActuarialPricingReservingUpdated, ActuarialPricingReservingApproved. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 2. Domain intake and normalization for Actuarial Assumption

**Justification:** The PBC cannot reach complete domain coverage unless it handles the messy front door of rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls, not only already-clean records.

**Improvement:** Build a typed intake pipeline for `actuarial_assumption` that accepts structured API payloads, document-derived instructions, batch loads, and assistant-generated drafts while normalizing identifiers, dates, units, parties, and jurisdictional context. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Golden intake fixtures, rejected-record queues, field-level normalization evidence, and assistant previews before governed datastore mutation. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 3. Specialist validation rules for Experience Study

**Justification:** World-class Actuarial Pricing and Reserving requires rules that domain experts can reason about, version, test, and roll back without code edits.

**Improvement:** Add a domain rule compiler for `experience_study` that supports threshold rules, eligibility rules, dependency rules, temporal windows, conflicting-instruction detection, and override justification. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Rule simulation tests, versioned rule manifests, rule impact reports, and UI rule editors linked to `ACTUARIAL_PRICING_RESERVING_DATABASE_URL, ACTUARIAL_PRICING_RESERVING_EVENT_TOPIC, ACTUARIAL_PRICING_RESERVING_RETRY_LIMIT`. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 4. Parameter governance and tuning for Reserve Estimate

**Justification:** Parameters are where operations teams tune actuarial pricing and reserving; unbounded constants would make the PBC brittle and unsafe in real deployments.

**Improvement:** Expose bounded runtime parameters for `reserve_estimate` covering risk thresholds, SLA windows, confidence floors, escalation cutoffs, batch sizes, retry limits, and human-confirmation requirements. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Parameter schema validation, tenant overrides, approval history, rollback controls, and workbench diff views. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 5. Deep owned schema expansion for Loss Triangle

**Justification:** A single payload column cannot express the full surface of rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls or prove cross-PBC boundaries are respected.

**Improvement:** Extend the owned schema around `loss_triangle` with normalized child tables for line-level evidence, party roles, approvals, attachments, comments, metrics, exception reasons, and control assertions. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Migrations, models, relationship tests, schema contract snapshots, and no shared-table access outside the `actuarial_pricing_reserving_` namespace. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 6. Event-sourced operational history for Capital Scenario

**Justification:** Temporal reconstruction is essential for better-than-world-class auditability and dispute resolution in actuarial pricing and reserving.

**Improvement:** Capture every material mutation of `capital_scenario` as immutable AppGen-X events with actor, tenant, command, policy version, idempotency key, before/after summary, and projection checkpoint. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Replay tests, projection checksums, event ordering evidence, and point-in-time workbench views. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 7. Projection and read-model strategy for Model Validation

**Justification:** The workbench should not force users to infer domain truth from raw tables; each projection should answer a real operating question.

**Improvement:** Create purpose-built projections for `model_validation`: operational queue, executive KPI rollup, exception aging, compliance evidence, agent task context, and external dependency health. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Projection contracts, freshness SLAs, backfill tests, and visible stale-projection warnings. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 8. Exception taxonomy and remediation for Actuarial Pricing Reserving Policy Rule

**Justification:** High-value PBCs win on exception throughput; generic “failed” states hide the details operators need.

**Improvement:** Model the full exception taxonomy for `actuarial_pricing_reserving_policy_rule`, including severity, root cause, blocking dependency, remediation owner, due date, retry eligibility, escalation path, and closure evidence. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Exception queues, aging metrics, remediation playbooks, dead-letter linkage, and closure test fixtures for sanctions or fraud holds. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 9. Predictive risk scoring for Actuarial Pricing Reserving Runtime Parameter

**Justification:** The package should warn users before actuarial pricing and reserving work fails, breaches policy, or creates downstream cost.

**Improvement:** Add predictive risk scoring for `actuarial_pricing_reserving_runtime_parameter` using domain features from owned tables, consumed events PolicyChanged, AuditEventSealed, OperationalKpiChanged, rule outcomes, aging, anomaly signals, and historical corrections. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Feature manifests, score explanations, calibration reports, drift alerts, and tests for low/medium/high-risk scenarios. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 10. Counterfactual simulation for Actuarial Pricing Reserving Schema Extension

**Justification:** Advanced users need to ask “what would happen if” before committing changes to live rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls operations.

**Improvement:** Provide scenario simulation for `actuarial_pricing_reserving_schema_extension`: policy change, capacity constraint, deadline shift, price/rate change, eligibility change, disruption, and manual override outcomes. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Simulation APIs, non-mutating sandbox state, comparison reports, and workbench side-by-side scenario panels. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 11. Autonomous anomaly triage for Actuarial Pricing Reserving Control Assertion

**Justification:** A world-class PBC should reduce analyst burden without hiding the reasoning behind automated triage.

**Improvement:** Implement anomaly detection for `actuarial_pricing_reserving_control_assertion` that identifies outliers, duplicate submissions, impossible sequences, stale dependencies, unusual amounts/counts/durations, and contradictory fields. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Explainable anomaly cards, reviewer feedback loops, false-positive tracking, and suppression governance. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 12. Semantic document understanding for Actuarial Pricing Reserving Governed Model

**Justification:** Document-heavy work in Actuarial Pricing and Reserving cannot be complete if the assistant only answers questions and cannot prepare accurate governed changes.

**Improvement:** Train the package assistant to parse domain documents and instructions for `actuarial_pricing_reserving_governed_model`, extract obligations, dates, parties, quantities, identifiers, and exceptions, then map them to safe draft mutations. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Document extraction tests, confidence thresholds, redaction handling, source span citations, and human confirmation workflows. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 13. Agent-safe CRUD execution for Rating Model

**Justification:** The PBC agent must be a first-class operator but never a hidden bypass around RBAC, rules, or owned datastore boundaries.

**Improvement:** Add a professional chatbot skill for `rating_model` that can create, update, correct, close, and annotate records only through policy-checked commands, approval gates, and previewed diffs. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Skill manifests, permission tests, preview/confirm flows, blocked-action evidence, and audit events for every assistant mutation. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 14. Workbench persona coverage for Actuarial Assumption

**Justification:** A generic detail page underserves the domain; each role needs the exact controls and evidence they use daily.

**Improvement:** Design dedicated workbench panels for `actuarial_assumption`: operator queue, supervisor approvals, analyst exceptions, auditor evidence, configuration owner, and agent-assistance review. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** UI contract entries, route tests, empty/error/loading states, and permission-aware action availability. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 15. Cross-PBC dependency contracts for Experience Study

**Justification:** Composable packages fail when hidden table coupling enters the domain model.

**Improvement:** Represent dependencies for `experience_study` through declared APIs, consumed events PolicyChanged, AuditEventSealed, OperationalKpiChanged, and projections rather than shared tables, with explicit freshness, ownership, and fallback behavior. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Dependency manifests, contract tests, stale dependency alerts, and no foreign-table references in generated artifacts. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 16. API completeness and versioning for Reserve Estimate

**Justification:** Complete domain coverage requires both command and query surfaces, not only happy-path create endpoints.

**Improvement:** Expand APIs beyond POST /rating-models, POST /actuarial-assumptions, POST /experience-studys to cover search, validation-only commands, simulation, bulk intake, exception closure, evidence export, projection reads, and idempotent corrections. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** OpenAPI-style route manifests, backward-compatible version tests, deprecation metadata, and idempotency assertions. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 17. Typed emitted-event expansion for Loss Triangle

**Justification:** Consumers should understand what happened in Actuarial Pricing and Reserving without parsing opaque payloads.

**Improvement:** Replace generic lifecycle emissions with typed events for each meaningful `loss_triangle` transition, exception, approval, correction, simulation result, and downstream handoff. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Event schema tests, event examples, compatibility checks, and emitted-event coverage in release evidence. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 18. Consumed-event handlers for Capital Scenario

**Justification:** A PBC is composable only when incoming events affect its own domain state predictably and safely.

**Improvement:** Implement idempotent handlers for consumed events PolicyChanged, AuditEventSealed, OperationalKpiChanged that update projections, open dependency exceptions, recalculate risk, and preserve source event lineage. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Duplicate-event tests, handler side-effect boundaries, dead-letter fixtures, and lineage links back to source events. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 19. Retry and dead-letter operations for Model Validation

**Justification:** Dead letters are not just plumbing; they are domain work queues that can block rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls.

**Improvement:** Create operational tools for retrying, quarantining, explaining, and resolving dead-lettered `model_validation` events with max-attempt policy, poison-message detection, and replay safety. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Dead-letter workbench, retry eligibility tests, replay audit proof, and operator action logs. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 20. RBAC and attribute policy for Actuarial Pricing Reserving Policy Rule

**Justification:** High-impact domain operations need finer controls than generic RBAC grants.

**Improvement:** Extend permissions for `actuarial_pricing_reserving_policy_rule` from coarse read/create/update/admin to action-level and attribute-aware policies based on role, tenant, jurisdiction, monetary/materiality threshold, and exception severity. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Permission matrix docs, ABAC policy tests, denied-action UI states, and assistant skill permission checks. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 21. Continuous control testing for Actuarial Pricing Reserving Runtime Parameter

**Justification:** Controls should run during operations, not only during release audit or manual review.

**Improvement:** Embed control assertions for `actuarial_pricing_reserving_runtime_parameter` that continuously test segregation of duties, required approvals, stale exceptions, policy drift, duplicate records, and boundary violations. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Control dashboards, failing-control events, test fixtures, and release evidence tied to `actuarial_pricing_reserving_control_assertion` records. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 22. Cryptographic audit proofing for Actuarial Pricing Reserving Schema Extension

**Justification:** Better-than-world-class auditability requires proof of integrity, not merely logs stored in mutable tables.

**Improvement:** Hash-chain material `actuarial_pricing_reserving_schema_extension` decisions, documents, emitted events, and release-evidence snapshots to make tampering visible without exposing sensitive payloads. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Proof manifests, verification APIs, redacted proof exports, and audit-ledger handoff events. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 23. Privacy, consent, and secrecy controls for Actuarial Pricing Reserving Control Assertion

**Justification:** Complete domain coverage must account for protected data and restricted operational evidence.

**Improvement:** Add field-level privacy classifications for `actuarial_pricing_reserving_control_assertion`, consent checks, masking rules, retention schedules, legal holds, and assistant redaction policies. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Retention tests, masked UI snapshots, consent-blocked mutation fixtures, and export controls. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 24. Multi-tenant operating model for Actuarial Pricing Reserving Governed Model

**Justification:** The PBC should scale across organizations while preserving independent policy and compliance boundaries.

**Improvement:** Support tenant-specific `actuarial_pricing_reserving_governed_model` rules, data residency, encryption context, configuration, seed data, and release evidence without allowing cross-tenant leakage. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Tenant isolation tests, tenant-scoped parameters, key-rotation evidence, and cross-tenant negative fixtures. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 25. Schema evolution and extension registry for Rating Model

**Justification:** Domain teams will add fields; the PBC must evolve without breaking APIs, events, or workbench projections.

**Improvement:** Make schema extensions for `rating_model` first-class with compatibility checks, migration previews, projection backfills, field ownership, and rollback metadata. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Extension registry UI, compatibility tests, migration dry-runs, and backfill release evidence. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 26. Master data quality gates for Actuarial Assumption

**Justification:** Many actuarial pricing and reserving errors begin as bad reference data; the PBC should catch them before workflow execution.

**Improvement:** Define reference-data contracts for `actuarial_assumption`: canonical codes, parties, locations, classifications, calendars, units, currencies, products, assets, or service categories as relevant to the domain. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Reference validation fixtures, stale-code warnings, mapping tables, and dependency freshness indicators. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 27. Bulk operations and correction workflows for Experience Study

**Justification:** Enterprise-scale Actuarial Pricing and Reserving users cannot operate one record at a time.

**Improvement:** Add bulk load, bulk validate, bulk approve, and bulk correction workflows for `experience_study` with partial success, row-level errors, resumability, and rollback. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** CSV/API batch fixtures, resumable job state, row-level audit evidence, and assistant-generated correction suggestions. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 28. Lifecycle collaboration and tasking for Reserve Estimate

**Justification:** Domain collaboration should live inside the PBC boundary and remain auditable with the record it affects.

**Improvement:** Attach tasks, comments, ownership, due dates, handoffs, and escalation threads to `reserve_estimate` without leaking into external shared task tables. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Task tables, comment audit history, notification events, escalation SLAs, and role-specific task queues. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 29. SLA and service-level governance for Loss Triangle

**Justification:** Users need to know when rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls is late, blocked, or at risk before customer or regulator impact.

**Improvement:** Define SLAs for `loss_triangle` across intake, validation, approval, exception resolution, event handling, downstream projection refresh, and release-evidence generation. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** SLA breach events, timers, configurable calendars, workbench aging buckets, and tests for pause/resume behavior. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 30. Operational analytics cockpit for Capital Scenario

**Justification:** World-class operations require leading indicators, not only record counts.

**Improvement:** Build analytics for `capital_scenario`: throughput, backlog, aging, approval latency, exception rate, risk distribution, automation acceptance, correction rate, and downstream dependency health. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Metric definitions, projection tests, drill-through routes, export APIs, and anomaly overlays. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 31. Decision intelligence and recommendations for Model Validation

**Justification:** The PBC should help expert users decide faster while showing evidence and uncertainty.

**Improvement:** Generate ranked recommendations for `model_validation` such as next best action, likely resolution, required evidence, policy adjustment, staffing/capacity response, or downstream handoff. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Recommendation explanations, confidence intervals, feedback capture, model governance records, and rejection reasons. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 32. Quality and completeness scoring for Actuarial Pricing Reserving Policy Rule

**Justification:** Operators should see whether a record is truly ready, not just technically saved.

**Improvement:** Score each `actuarial_pricing_reserving_policy_rule` record for completeness, consistency, policy readiness, dependency readiness, evidence sufficiency, and downstream composability. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Scoring rules, missing-evidence lists, readiness badges, and blocking criteria in command handlers. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 33. End-to-end scenario library for Actuarial Pricing Reserving Runtime Parameter

**Justification:** Release evidence is stronger when every important actuarial pricing and reserving behavior has executable examples.

**Improvement:** Create seeded scenarios for `actuarial_pricing_reserving_runtime_parameter`: normal flow, urgent path, exception path, corrected path, duplicate path, late event path, and audit export path. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Scenario seed data, runtime smoke coverage, generated-app fixtures, and story-level workbench screenshots/contracts. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 34. Domain ontology and terminology model for Actuarial Pricing Reserving Schema Extension

**Justification:** Precise vocabulary prevents the PBC from misclassifying specialist documents or user instructions.

**Improvement:** Add an ontology for `actuarial_pricing_reserving_schema_extension` terms, synonyms, classifications, relationships, allowed values, and phrase mappings used by the assistant and UI. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Ontology files, assistant parsing tests, UI glossary, and mapping evidence for domain-specific abbreviations. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 35. Advanced search and investigation for Actuarial Pricing Reserving Control Assertion

**Justification:** Investigators and operators need fast, explainable retrieval across the whole domain surface.

**Improvement:** Provide search across `actuarial_pricing_reserving_control_assertion` records, events, documents, exceptions, tasks, comments, and audit proofs with filters for tenant, status, risk, date, party, and dependency. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Search index contracts, result provenance, permission-filtered queries, and stale-index warnings. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 36. Reconciliation and closure controls for Actuarial Pricing Reserving Governed Model

**Justification:** Closure is not complete until the PBC can prove no material domain work remains unresolved.

**Improvement:** Add reconciliation workflows that compare `actuarial_pricing_reserving_governed_model` state against consumed events, external projections, expected totals/counts, approvals, and release evidence before closure. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Reconciliation reports, variance thresholds, closure blockers, and AppGen-X closure events. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 37. Regulatory and policy reporting for Rating Model

**Justification:** World-class PBCs turn operational evidence into credible reporting without spreadsheet reconstruction.

**Improvement:** Generate domain reporting packs for `rating_model` covering statutory, contractual, operational, board, customer, or regulator evidence depending on monetary integrity, funds movement controls, counterparty risk, regulatory evidence, settlement finality, fraud prevention, and financial reconciliation. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Report schemas, redaction rules, traceable metric sources, and approval/export audit events. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 38. Carbon and resource awareness for Actuarial Assumption

**Justification:** Sustainability evidence should be embedded in operations instead of treated as an after-the-fact report.

**Improvement:** Where relevant, attach carbon, energy, water, travel, capacity, compute, or resource-footprint metadata to `actuarial_assumption` decisions and batch operations. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Footprint fields, scheduling parameters, exception rules, and dashboards that expose operational tradeoffs. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 39. Resilience and offline behavior for Experience Study

**Justification:** Real operations keep moving during outages; the PBC must preserve correctness when dependencies are unavailable.

**Improvement:** Define resilience modes for `experience_study`: degraded dependency mode, offline draft capture, delayed event replay, conflict detection, and safe recovery after partial failure. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Offline fixtures, replay tests, conflict queues, recovery logs, and user-visible degraded-mode warnings. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 40. Human-in-the-loop automation for Reserve Estimate

**Justification:** Automation should accelerate rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls while preserving accountability for high-risk decisions.

**Improvement:** Set explicit automation boundaries for `reserve_estimate`: auto-approve, auto-reject, suggest-only, require-review, and block-until-evidence states with policy-based routing. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Automation policy tests, reviewer queues, override reasons, and assistant action audit trails. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 41. Package discovery and fit scoring for Loss Triangle

**Justification:** Users selecting PBCs need transparent fit reasoning, especially when domains are adjacent but not overlapping.

**Improvement:** Improve package metadata so composition can explain when `actuarial_pricing_reserving` fits a prompt, what entities it owns, what APIs/events it exposes, and what adjacent PBCs it depends on. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Discovery manifests, prompt-selection tests, overlap rationale links, and composition DSL examples. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 42. Configuration deployment pipeline for Capital Scenario

**Justification:** Configuration changes can materially alter actuarial pricing and reserving; they need the same discipline as code releases.

**Improvement:** Add configuration promotion for `capital_scenario` across draft, test, approved, active, deprecated, and rollback states with impact analysis before activation. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Config diff views, approval workflows, simulation before activation, and rollback tests. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 43. Workbench command completeness for Model Validation

**Justification:** A PBC does not fully surface its capabilities if users must call hidden APIs for core work.

**Improvement:** Expose every high-value operation for `model_validation` in the UI: create, validate, approve, simulate, correct, assign, export, retry, close, and audit-proof verification. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** UI action coverage tests, permission-aware disabled states, keyboard paths, and assistant handoff links. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 44. Document packet and evidence vault for Actuarial Pricing Reserving Policy Rule

**Justification:** Documents often carry the legal or operational truth behind rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls.

**Improvement:** Create a governed evidence vault for `actuarial_pricing_reserving_policy_rule` documents, attachments, source spans, extracted fields, signatures, approvals, and retention labels. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Evidence models, source-to-field lineage, signature validation, retention policies, and proof exports. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 45. Data correction and amendment history for Actuarial Pricing Reserving Runtime Parameter

**Justification:** World-class systems correct mistakes without rewriting history or confusing downstream consumers.

**Improvement:** Support formal amendments for `actuarial_pricing_reserving_runtime_parameter` that preserve original values, correction reason, approving actor, effective date, downstream event impacts, and replay behavior. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Amendment tables, correction events, projection replay tests, and side-by-side before/after UI. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 46. External participant collaboration for Actuarial Pricing Reserving Schema Extension

**Justification:** Many actuarial pricing and reserving workflows require outside parties, but they must not gain direct access to internal tables.

**Improvement:** Add controlled collaboration portals or API views for external participants related to `actuarial_pricing_reserving_schema_extension`, limited to scoped evidence submission, status checks, comments, and dispute responses. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Participant role policies, scoped tokens, submission audit trails, and inbound evidence validation. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 47. Advanced dependency freshness scoring for Actuarial Pricing Reserving Control Assertion

**Justification:** A record may be valid locally but unsafe if dependency evidence is stale or incomplete.

**Improvement:** Score freshness and reliability of dependencies used by `actuarial_pricing_reserving_control_assertion`, including consumed events PolicyChanged, AuditEventSealed, OperationalKpiChanged, referenced projections, configuration versions, and external submissions. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Freshness indicators, blocking rules, stale-event simulations, and workbench dependency health panels. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 48. Model governance and explainability for Actuarial Pricing Reserving Governed Model

**Justification:** Governed AI is mandatory for professional-grade automation in Actuarial Pricing and Reserving.

**Improvement:** For every predictive or agentic feature around `actuarial_pricing_reserving_governed_model`, record model version, prompt or ruleset version, training/evaluation evidence, confidence, explanation, and human feedback. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Model cards, prompt/version manifests, feedback loops, drift tests, and audit proof for recommendations. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 49. High-scale partitioning and archival for Rating Model

**Justification:** Better-than-world-class packages must remain operable after years of high-volume domain history.

**Improvement:** Plan scale behavior for `rating_model`: tenant partitioning, archival policies, cold storage, retention-aware search, projection compaction, and large-batch replay. Tie the behavior to `actuarial_pricing_reserving_create_rating_model_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Partition tests, archive/retrieve fixtures, retention enforcement, and replay benchmarks. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.

### 50. Release gate expansion for Actuarial Assumption

**Justification:** The PBC should not claim domain coverage unless release evidence proves the claim end to end.

**Improvement:** Expand release gates for `actuarial_pricing_reserving` so every schema, service, API, event, handler, UI, rule, parameter, agent skill, seed scenario, and improvement backlog item maps to executable evidence. Tie the behavior to `actuarial_pricing_reserving_record_actuarial_assumption_workflow` where applicable, and make it visible in `ActuarialPricingReservingWorkbench` so operators do not need hidden scripts or raw table access.

**Acceptance evidence:** Release audit checks, manifest traceability, generated-app smoke tests, and missing-capability blockers. The evidence should be package-local in `src/pyAppGen/pbcs/actuarial_pricing_reserving` and should preserve PostgreSQL, MySQL, and MariaDB backend compatibility.
