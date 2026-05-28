# Case and Knowledge Management PBC

## Purpose

The `case_knowledge_management` PBC is a world-class packaged business capability for Owns support case intake, classification, queues, SLAs, escalations, resolution, knowledge articles, article quality, feedback, and support intelligence. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `case_knowledge_management_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `case_knowledge_management_support_case`: owns support case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_contact`: owns case contact lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_classification`: owns case classification lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_queue`: owns case queue lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_assignment`: owns case assignment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_sla`: owns case sla lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_sla_timer_event`: owns sla timer event lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_interaction`: owns case interaction lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_escalation`: owns case escalation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_resolution`: owns case resolution lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_knowledge_article`: owns knowledge article lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_article_version`: owns article version lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_article_feedback`: owns article feedback lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_article_quality_score`: owns article quality score lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_root_cause`: owns root cause lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_duplicate_link`: owns case duplicate link lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_exception_case`: owns case exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_policy_rule`: owns case policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_runtime_parameter`: owns case runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_schema_extension`: owns case schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_control_assertion`: owns case control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_case_governed_model`: owns case governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `case_knowledge_management_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `case_knowledge_management_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `case_knowledge_management_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for cases: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_support_case`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `classify_case`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `route_case_queue`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `assign_case`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `start_sla_timer`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_case_interaction`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_case_escalation`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_case`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `publish_knowledge_article`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `version_article`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_article_feedback`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `score_article_quality`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `identify_root_cause`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `link_duplicate_case`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_case_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_case_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `recommend_next_best_resolution`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- semantic case classification: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- next-best-resolution assistant: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- knowledge gap detection: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- duplicate case graphing: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- SLA breach prediction: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- article quality drift monitoring: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `case_routing_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `sla_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `escalation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `knowledge_publish_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `duplicate_detection_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `article_retirement_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `sla_warning_minutes`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `duplicate_similarity_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `article_quality_floor`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `escalation_age_hours`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `queue_capacity_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `case_knowledge_management_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `CaseCreated`
- `CaseAssigned`
- `SlaRiskChanged`
- `CaseEscalated`
- `CaseResolved`
- `KnowledgeArticlePublished`

Consumed events:

- `CustomerUpdated`
- `ProductPublished`
- `PolicyChanged`
- `WorkflowTaskCompleted`

Handlers use idempotency keys of the form `case_knowledge_management:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- case workbench.
- queue board.
- SLA timer console.
- escalation room.
- knowledge studio.
- article quality panel.
- root cause analytics.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `case_knowledge_management_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: support_case, case_contact, case_classification, case_queue, case_assignment, case_sla, sla_timer_event, case_interaction, case_escalation, case_resolution, knowledge_article, article_version, article_feedback, article_quality_score, root_cause, case_duplicate_link, case_exception_case, case_policy_rule, case_runtime_parameter, case_schema_extension, case_control_assertion, case_governed_model
- operations: create_support_case, classify_case, route_case_queue, assign_case, start_sla_timer, record_case_interaction, open_case_escalation, resolve_case, publish_knowledge_article, version_article, capture_article_feedback, score_article_quality, identify_root_cause, link_duplicate_case, resolve_case_exception, compile_case_rule, recommend_next_best_resolution
- emits: CaseCreated, CaseAssigned, SlaRiskChanged, CaseEscalated, CaseResolved, KnowledgeArticlePublished
- consumes: CustomerUpdated, ProductPublished, PolicyChanged, WorkflowTaskCompleted
- rules: case_routing_policy, sla_policy, escalation_policy, knowledge_publish_policy, duplicate_detection_policy, article_retirement_policy
- parameters: sla_warning_minutes, duplicate_similarity_threshold, article_quality_floor, escalation_age_hours, queue_capacity_limit, workbench_limit
- advanced_capabilities: semantic case classification, next-best-resolution assistant, knowledge gap detection, duplicate case graphing, SLA breach prediction, article quality drift monitoring
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: support_case, knowledge_article, article_version, semantic_knowledge_index, case_deflection_event, knowledge_approval, content_freshness_signal, agent_assist_recommendation
- apis: POST /support-cases, POST /knowledge-articles, POST /article-approvals, POST /case-deflections, GET /knowledge-workbench
- emits: KnowledgeArticlePublished, CaseDeflected, AgentAssistRecommended, ContentFreshnessFlagged
- consumes: ServiceTicketOpened, CustomerUpdated, SearchIndexRefreshed
- ui_fragments: CaseKnowledgeManagementWorkbench, CaseKnowledgeManagementDetail, CaseKnowledgeManagementAssistantPanel
- permissions: case_knowledge_management.read, case_knowledge_management.create, case_knowledge_management.update, case_knowledge_management.approve, case_knowledge_management.admin
- configuration: CASE_KNOWLEDGE_MANAGEMENT_DATABASE_URL, CASE_KNOWLEDGE_MANAGEMENT_EVENT_TOPIC, CASE_KNOWLEDGE_MANAGEMENT_RETRY_LIMIT, CASE_KNOWLEDGE_MANAGEMENT_DEFAULT_POLICY
- standard_features: support_case_management, case_knowledge_management_workflow, case_knowledge_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud
- advanced_capabilities: case_knowledge_management_event_sourced_operational_history, case_knowledge_management_multi_tenant_policy_isolation, case_knowledge_management_schema_evolution_resilience, case_knowledge_management_autonomous_anomaly_detection, case_knowledge_management_semantic_document_instruction_understanding, case_knowledge_management_predictive_risk_scoring, case_knowledge_management_counterfactual_scenario_simulation, case_knowledge_management_cryptographic_audit_proofs, case_knowledge_management_continuous_control_testing, case_knowledge_management_carbon_and_sustainability_awareness, case_knowledge_management_cross_pbc_event_federation, case_knowledge_management_governed_ai_agent_execution
