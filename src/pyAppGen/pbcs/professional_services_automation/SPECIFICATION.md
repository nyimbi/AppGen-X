# Professional Services Automation PBC Specification

## Stable Identity

The `professional_services_automation` pbc is a package-owned business capability in the `relationship` mesh. It owns the implementation directory `src/pyAppGen/pbcs/professional_services_automation` and exposes a stable manifest, side-effect-free registration, discovery metadata, release evidence, and package-local tests. The PBC description is: Engagements, scopes, staffing, time, billing milestones, utilization, project margin, and client delivery workflows.

## Owned Boundary

The package owns its datastore boundary and does not mutate shared or foreign tables. All owned table names are generated under the `professional_services_automation_` prefix in schema contracts, models, migrations, service operation contracts, event handlers, UI workbench projections, and agent CRUD plans. Cross-PBC collaboration is represented through APIs, AppGen-X events, and read-only projections rather than shared table writes.

## Schema, Migration, and Models

The schema contract declares every owned table, field set, relationship, migration path, and model descriptor. The migration creates tables for PostgreSQL, MySQL, and MariaDB compatible backends. The model manifest proves that every runtime-owned table has a generated model and that relationships point only to owned tables. Schema extensions are governed by rule and parameter controls.

## Service, API, Command, and Query Contracts

The service layer separates command methods from read-only query methods. Commands use the owned datastore plus outbox transaction boundary. Queries read package projections without emitting events. API route contracts include idempotency keys, route metadata, validation evidence, and dispatch plans. The service contract exposes command, query, workbench, schema, release, configuration, parameter, and rule operations.

## Events and Handlers

Events use the AppGen-X contract with outbox, inbox, idempotency, retry, and dead-letter handling. The package emits typed domain events and consumes declared dependency events. Handlers are idempotent and retryable; unknown events are routed to the dead-letter table with retry evidence. Users do not select eventing engines or stream-engine pickers.

## UI, Workbench, Permissions, Rules, Parameters, and Configuration

The UI exposes workbench fragments for operations, records, rules, agent assistance, and configuration editing. Permissions and RBAC descriptors gate read, create, update, approve, and admin actions. Configuration schemas, rule manifests, parameter manifests, seed data, and governance smoke tests are package-local and executable.

## Agent, Chatbot, Skills, Documents, and CRUD

The PBC contributes first-class agent skills into the composed application single assistant under the `professional_services_automation_skills` namespace. The chatbot helps users accomplish tasks, accepts documents and instructions, proposes governed datastore CRUD mutations, rejects foreign table mutation, requires human confirmation for writes, and emits AppGen-X event plans. Skills are expressible in the DSL through composed assistant tool names.

## Standard and Advanced Capabilities

Standard capabilities cover table-stakes business operations, owned schema generation, service/API/event implementation, UI workbench coverage, configuration, rule, parameter, seed, permission, and release evidence. Advanced capabilities add event-sourced history, multi-tenant isolation, semantic document understanding, predictive scoring, counterfactual simulation, cryptographic audit proof, control testing, carbon awareness, cross-PBC event federation, and governed AI agent execution.

## Release, Tests, Seed, and Registration

Release evidence is materialized in `RELEASE_EVIDENCE.md` and `release_evidence.py`. Tests cover generated schema, service, release evidence, event contracts, handlers, agent chatbot skills, side-effect-free registration, service routes, configuration, permissions, and seed hooks. Registration is side-effect-free: `register_pbc`, `registration_plan`, `package_metadata_manifest`, `validate_package_metadata`, and `package_discovery_plan` return plans and metadata without mutating the catalog.

## Datastore and Event Policy

Ordinary datastore backends are limited to postgresql, mysql, and mariadb. Eventing is AppGen-X. The package includes outbox, inbox, dead-letter, retry, idempotent handler, and release-audit evidence without exposing stream-engine choices to users.

## Manifest Traceability Appendix

- tables: client_engagement, statement_of_work, engagement_staffing, delivery_milestone, billable_time_entry, billing_milestone, utilization_snapshot, engagement_margin
- apis: POST /engagements, POST /statements-of-work, POST /staffing, POST /billing-milestones, GET /services-automation-workbench
- emits: EngagementOpened, BillingMilestoneReady, UtilizationMeasured, EngagementMarginUpdated
- consumes: ContractApproved, TimeSubmitted, InvoiceIssued
- ui_fragments: ProfessionalServicesAutomationWorkbench, ProfessionalServicesAutomationDetail, ProfessionalServicesAutomationAssistantPanel
- permissions: professional_services_automation.read, professional_services_automation.create, professional_services_automation.update, professional_services_automation.approve, professional_services_automation.admin
- configuration: PROFESSIONAL_SERVICES_AUTOMATION_DATABASE_URL, PROFESSIONAL_SERVICES_AUTOMATION_EVENT_TOPIC, PROFESSIONAL_SERVICES_AUTOMATION_RETRY_LIMIT, PROFESSIONAL_SERVICES_AUTOMATION_DEFAULT_POLICY
- standard_features: client_engagement_management, professional_services_automation_workflow, professional_services_automation_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud
- advanced_capabilities: professional_services_automation_event_sourced_operational_history, professional_services_automation_multi_tenant_policy_isolation, professional_services_automation_schema_evolution_resilience, professional_services_automation_autonomous_anomaly_detection, professional_services_automation_semantic_document_instruction_understanding, professional_services_automation_predictive_risk_scoring, professional_services_automation_counterfactual_scenario_simulation, professional_services_automation_cryptographic_audit_proofs, professional_services_automation_continuous_control_testing, professional_services_automation_carbon_and_sustainability_awareness, professional_services_automation_cross_pbc_event_federation, professional_services_automation_governed_ai_agent_execution

## Operational Rulebook and Advanced Execution Scenarios

The `professional_services_automation` package treats rules, parameters, and configuration as runtime-operational artifacts rather than static documentation. Domain teams can register policies for engagement setup, statements of work, staffing, time capture, utilization, project financials, milestones, invoicing, and margin control; each policy is versioned, explainable, and evaluated before command execution. Parameters tune thresholds, approval tiers, retry limits, default ownership, workbench filters, agent confirmation gates, and exception severity without changing generated source. The same rulebook feeds API validation, service command guards, workbench indicators, agent recommendations, release evidence, and generated DSL metadata so composed applications preserve one consistent operating model.

Advanced execution scenarios prove that the PBC is useful beyond catalog presence. The runtime can simulate command impact, emit a governed outbox event, update only owned tables, and produce an evidence payload showing which rules fired, which parameters were read, which permissions were required, and which downstream dependencies receive API or event notifications. Exception flows explicitly route margin leakage, unapproved work, capacity shortfalls, late time, and billing readiness gaps. The agent skill layer can translate uploaded instructions, emails, spreadsheets, policy notes, and document packets into proposed CRUD plans, but it never performs writes without the datastore boundary check and confirmation contract. These scenarios are included so generated applications can compose this PBC into a single assistant, expose professional UI workbenches, and audit every autonomous recommendation back to owned schema, service commands, event contracts, handlers, and release evidence.
