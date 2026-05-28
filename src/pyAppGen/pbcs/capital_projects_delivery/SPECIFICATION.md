# Capital Projects Delivery PBC Specification

## Scope

`capital_projects_delivery` is a standalone PBC for capital project governance, engineering-procurement-construction package management, permit milestone control, physical progress measurement, commissioning systems, project risk, turnover packages, stage-gate approvals, and delivery workbench operations. A generated application that includes only this PBC must be able to run the domain: it needs database-backed forms, lifecycle wizards, controls, service commands, API routes, AppGen-X eventing, an agent assistant, RBAC permission enforcement, seed data, configuration, and release evidence.

The standard capability surface covers capital_project_management, capital_projects_delivery_workflow, capital_projects_delivery_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, and continuous_release_assurance. Advanced capabilities include event-sourced operational history, multi-tenant policy isolation, schema evolution resilience, autonomous anomaly detection, semantic document instruction understanding, predictive risk scoring, counterfactual scenario simulation, cryptographic audit proofs, continuous control testing, carbon and sustainability awareness, cross-PBC event federation, and governed AI agent execution.

## Owned Boundary And Datastore

The PBC owns the capital_project, epc_package, permit_milestone, progress_measurement, commissioning_system, project_risk, turnover_package, capital_projects_delivery_policy_rule, capital_projects_delivery_runtime_parameter, capital_projects_delivery_schema_extension, capital_projects_delivery_control_assertion, and capital_projects_delivery_governed_model tables. No shared foreign table is required for core operation. Integration with portfolio, finance, procurement, assets, or workforce PBCs happens through API calls, consumed events, emitted events, or projections. The schema, migration, and model artifacts must be portable across PostgreSQL, MySQL, and MariaDB.

The owned model captures project identity, authorization, baseline dates, budget envelope references, delivery stage, EPC package scope, permit authority, percent complete, earned progress, commissioning boundary, risk exposure, turnover readiness, policy rule evaluation, configuration parameters, schema extensions, control assertions, and governed AI model metadata.

## Workflows And Commands

The create-capital-project workflow captures project charter, sponsor, site, phase, approval class, target dates, budget reference, and risk category. The gate checklist wizard records required deliverables and evidence for concept, definition, execution, commissioning, turnover, and closeout. Gate approval commands verify checklist completion, RBAC authority, maker-checker separation, policy rules, risk conditions, permit status, and commissioning readiness before changing lifecycle state. Rejection and rollback commands preserve event-sourced history and require reason codes.

EPC package workflows create package scope, contractor reference, planned dates, procurement readiness, interface risks, and acceptance criteria. Permit milestone workflows track authority, application, review, approval, expiry, and blocking status. Progress measurement commands record physical quantities, earned value references, percent complete, exceptions, and evidence attachments. Commissioning system commands track subsystem boundaries, test packs, punch items, energization status, and turnover packages. Query operations serve project detail, stage-gate readiness, permit constraints, progress exceptions, commissioning readiness, risk heatmaps, and the workbench queue.

## UI, Controls, And Agent

The UI includes CapitalProjectsDeliveryWorkbench, CapitalProjectsDeliveryDetail, and CapitalProjectsDeliveryAssistantPanel. Forms cover project creation, EPC package setup, permit milestone update, progress measurement, commissioning system readiness, project risk entry, turnover package creation, policy rule editing, and parameter update. Wizards cover capital project gate approval, lifecycle transition review, commissioning readiness, and turnover acceptance. Controls verify required deliverables, schedule slippage, risk exposure, permit blockers, progress evidence, commissioning punch items, rule compliance, approval authority, RBAC permission, duplicate idempotency keys, and owned-table boundary protection.

The PBC agent, assistant, and chatbot expose skills for project intake, document instruction parsing, checklist generation, CRUD datastore mutation, risk explanation, gate readiness guidance, and workbench triage. The assistant can read a project charter, engineering package note, permit correspondence, progress report, or commissioning checklist, build a side-effect-free mutation plan, explain rule and parameter impacts, and execute approved service commands. In a composed app, these skills integrate into the single application agent rather than a separate disconnected bot.

## Events, Handlers, And Resilience

Ordinary eventing uses the AppGen-X contract only. The package emits CapitalProjectsDeliveryCreated, CapitalProjectsDeliveryUpdated, CapitalProjectsDeliveryApproved, and CapitalProjectsDeliveryExceptionOpened. It consumes PolicyChanged, AuditEventSealed, and OperationalKpiChanged. Outbox events are written inside the same service transaction as owned table changes. Inbox handlers process consumed events with idempotency_key checks, retry policy evidence, and dead-letter routing for malformed or unrecoverable payloads. There is no stream-engine picker in user-facing configuration.

## Rules, Parameters, And Configuration

Rules evaluate gate deliverable completeness, minimum approval authority, permit blocking status, risk thresholds, commissioning acceptance, turnover evidence, and assistant mutation policy. Parameters define retry limit, default policy, stage gate thresholds, risk appetite, required review quorum, and stale evidence limits. Configuration is surfaced through CAPITAL_PROJECTS_DELIVERY_DATABASE_URL, CAPITAL_PROJECTS_DELIVERY_EVENT_TOPIC, CAPITAL_PROJECTS_DELIVERY_RETRY_LIMIT, and CAPITAL_PROJECTS_DELIVERY_DEFAULT_POLICY.

## Registration And Release

Package registration, discovery, metadata validation, and composition planning are side-effect-free. Release evidence must prove migration, schema, model, services, API routes, events, handlers, UI, workbench, permission/RBAC, configuration, seed data, agent skills, tests, and generation smoke behavior. A one-PBC app is releasable only if it can create and approve a capital project, record EPC and permit work, measure progress, review commissioning, and show actionable controls without any external package.

## Manifest Traceability Appendix

Tables: capital_project, epc_package, permit_milestone, progress_measurement, commissioning_system, project_risk, turnover_package, capital_projects_delivery_policy_rule, capital_projects_delivery_runtime_parameter, capital_projects_delivery_schema_extension, capital_projects_delivery_control_assertion, capital_projects_delivery_governed_model.

APIs: POST /capital-projects, POST /epc-packages, POST /permit-milestones, POST /progress-measurements, POST /commissioning-systems, GET /capital-projects-delivery-workbench.

Emits: CapitalProjectsDeliveryCreated, CapitalProjectsDeliveryUpdated, CapitalProjectsDeliveryApproved, CapitalProjectsDeliveryExceptionOpened.

Consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged.

UI fragments: CapitalProjectsDeliveryWorkbench, CapitalProjectsDeliveryDetail, CapitalProjectsDeliveryAssistantPanel.

Permissions: capital_projects_delivery.read, capital_projects_delivery.create, capital_projects_delivery.update, capital_projects_delivery.approve, capital_projects_delivery.admin.

Configuration: CAPITAL_PROJECTS_DELIVERY_DATABASE_URL, CAPITAL_PROJECTS_DELIVERY_EVENT_TOPIC, CAPITAL_PROJECTS_DELIVERY_RETRY_LIMIT, CAPITAL_PROJECTS_DELIVERY_DEFAULT_POLICY.

Standard features: capital_project_management, capital_projects_delivery_workflow, capital_projects_delivery_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance.

Advanced capabilities: capital_projects_delivery_event_sourced_operational_history, capital_projects_delivery_multi_tenant_policy_isolation, capital_projects_delivery_schema_evolution_resilience, capital_projects_delivery_autonomous_anomaly_detection, capital_projects_delivery_semantic_document_instruction_understanding, capital_projects_delivery_predictive_risk_scoring, capital_projects_delivery_counterfactual_scenario_simulation, capital_projects_delivery_cryptographic_audit_proofs, capital_projects_delivery_continuous_control_testing, capital_projects_delivery_carbon_and_sustainability_awareness, capital_projects_delivery_cross_pbc_event_federation, capital_projects_delivery_governed_ai_agent_execution.
