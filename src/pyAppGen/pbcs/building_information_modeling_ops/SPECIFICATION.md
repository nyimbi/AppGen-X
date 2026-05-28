# Building Information Modeling Operations PBC Specification

## Scope

`building_information_modeling_ops` is a standalone PBC for BIM model operations, federation governance, coordinate assurance, clash and issue management, asset object registration, handover package control, model review, and digital twin linkage. A composed application with only this PBC must be fully usable for a BIM operations team: database-backed forms collect model metadata, wizards guide federation setup and release readiness, controls block unsafe publication, the workbench shows current queues and metrics, services execute all commands, routes expose the API surface, and the agent assistant can help users complete tasks from documents or instructions.

The standard features include bim_model_management, building_information_modeling_ops_workflow, building_information_modeling_ops_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, and continuous_release_assurance. Advanced capabilities include event-sourced operational history, multi-tenant policy isolation, schema evolution resilience, autonomous anomaly detection, semantic document instruction understanding, predictive risk scoring, counterfactual scenario simulation, cryptographic audit proofs, continuous control testing, carbon and sustainability awareness, cross-PBC event federation, and governed AI agent execution.

## Owned Domain Model

The PBC owns the table boundary for bim_model, model_version, clash_issue, asset_object, handover_package, model_review, digital_twin_link, policy rules, runtime parameters, schema extensions, control assertions, and governed model declarations. These owned tables are the authoritative datastore for the package. Other PBCs may reference model identifiers through declared APIs, emitted events, consumed events, or projections, but they must not share or mutate the BIM tables directly. Database portability is constrained to PostgreSQL, MySQL, and MariaDB, and the migration and model artifacts must remain deterministic.

The model registry captures project identity, discipline, authoring system reference, coordinate basis, issue purpose, version lineage, review state, handover readiness, and twin linkage. Relationships are internal to the package: model versions belong to BIM models, clash issues reference versions, asset objects may be attached to versions, handover packages aggregate reviewed model artifacts, and digital twin links point to the approved object baseline.

## Services, APIs, And Workflows

Service commands create BIM models, register model versions, open clash issues, register asset objects, prepare handover packages, record model reviews, and link digital twin objects. Additional federation commands establish project coordinate baselines, register model packages, assemble federations, and produce release evidence. Every command uses a transaction boundary that writes the owned datastore plus the AppGen-X outbox. Query operations return model detail, package status, blocked issue queues, federation health, and workbench metrics.

The API route contract exposes POST /bim-models, POST /model-versions, POST /clash-issues, POST /asset-objects, POST /handover-packages, and GET /building-information-modeling-ops-workbench. Route validation requires idempotency keys for mutations, rejects foreign table writes, and maps each route to a service command or query. Commands are retriable and idempotent so an interrupted model-registration workflow can be safely replayed.

## UI, Wizards, Controls, And Agent

The UI includes BuildingInformationModelingOpsWorkbench, BuildingInformationModelingOpsDetail, and BuildingInformationModelingOpsAssistantPanel. Forms support BIM model intake, model version registration, clash issue creation, asset object registration, handover package preparation, model review, digital twin linking, coordinate baseline capture, and federation assembly. Wizards guide federation setup, package review, issue-purpose publishing, and release evidence review. Controls verify coordinate alignment, discipline completeness, model lineage, unresolved critical clashes, handover package completeness, review approval, RBAC permission, schema extension compatibility, and owned-table boundary compliance.

The PBC agent, assistant, and chatbot provide BIM operational skills. They can read a document or instruction such as an information requirements sheet, model transmittal, clash report, review checklist, or handover note, then propose a CRUD datastore mutation plan. The plan explains created or updated records, required permissions, rule violations, and resulting events before execution. In a larger composed application, these skills are contributed into the single application agent namespace without exposing implementation details or a stream-engine picker.

## Events, Rules, And Resilience

AppGen-X eventing is the only ordinary event model. The PBC emits BuildingInformationModelingOpsCreated, BuildingInformationModelingOpsUpdated, BuildingInformationModelingOpsApproved, and BuildingInformationModelingOpsExceptionOpened. It consumes PolicyChanged, AuditEventSealed, and OperationalKpiChanged. The outbox records domain events; the inbox tracks consumed events; handlers enforce idempotency, retry transient failures, and send unrecoverable payloads to a dead-letter table with evidence available in release audit output.

Rules and parameters govern required model fields, coordinate tolerance, issue-purpose publishing, review quorum, handover completeness, model version naming, twin-link readiness, and assistant mutation limits. Configuration is managed through BUILDING_INFORMATION_MODELING_OPS_DATABASE_URL, BUILDING_INFORMATION_MODELING_OPS_EVENT_TOPIC, BUILDING_INFORMATION_MODELING_OPS_RETRY_LIMIT, and BUILDING_INFORMATION_MODELING_OPS_DEFAULT_POLICY.

## Registration And Release

Package registration, package discovery, and metadata validation are side-effect-free. They register only a plan and metadata manifest. Release evidence must prove schema, migration, model, service, route, event, handler, UI, permission, RBAC, configuration, seed, agent, and test coverage. A single-PBC generation smoke audit must show database-backed forms, wizards, controls, services, routes, workbench cards, and assistant skills.

## Manifest Traceability Appendix

Tables: bim_model, model_version, clash_issue, asset_object, handover_package, model_review, digital_twin_link, building_information_modeling_ops_policy_rule, building_information_modeling_ops_runtime_parameter, building_information_modeling_ops_schema_extension, building_information_modeling_ops_control_assertion, building_information_modeling_ops_governed_model.

APIs: POST /bim-models, POST /model-versions, POST /clash-issues, POST /asset-objects, POST /handover-packages, GET /building-information-modeling-ops-workbench.

Emits: BuildingInformationModelingOpsCreated, BuildingInformationModelingOpsUpdated, BuildingInformationModelingOpsApproved, BuildingInformationModelingOpsExceptionOpened.

Consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged.

UI fragments: BuildingInformationModelingOpsWorkbench, BuildingInformationModelingOpsDetail, BuildingInformationModelingOpsAssistantPanel.

Permissions: building_information_modeling_ops.read, building_information_modeling_ops.create, building_information_modeling_ops.update, building_information_modeling_ops.approve, building_information_modeling_ops.admin.

Configuration: BUILDING_INFORMATION_MODELING_OPS_DATABASE_URL, BUILDING_INFORMATION_MODELING_OPS_EVENT_TOPIC, BUILDING_INFORMATION_MODELING_OPS_RETRY_LIMIT, BUILDING_INFORMATION_MODELING_OPS_DEFAULT_POLICY.

Standard features: bim_model_management, building_information_modeling_ops_workflow, building_information_modeling_ops_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance.

Advanced capabilities: building_information_modeling_ops_event_sourced_operational_history, building_information_modeling_ops_multi_tenant_policy_isolation, building_information_modeling_ops_schema_evolution_resilience, building_information_modeling_ops_autonomous_anomaly_detection, building_information_modeling_ops_semantic_document_instruction_understanding, building_information_modeling_ops_predictive_risk_scoring, building_information_modeling_ops_counterfactual_scenario_simulation, building_information_modeling_ops_cryptographic_audit_proofs, building_information_modeling_ops_continuous_control_testing, building_information_modeling_ops_carbon_and_sustainability_awareness, building_information_modeling_ops_cross_pbc_event_federation, building_information_modeling_ops_governed_ai_agent_execution.
