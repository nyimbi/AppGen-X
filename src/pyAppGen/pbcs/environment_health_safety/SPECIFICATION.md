# Environment Health and Safety PBC

## Purpose

`environment_health_safety` is a standalone package-local PBC for EHS incident response, hazard prevention, inspections, permits, corrective actions, training, audit evidence, and regulator-facing governance. The package owns its schema contracts, migration DDL, executable workflows, AppGen-X event contracts, UI/agent surfaces, and release evidence.

## Standalone operational slice

The implemented slice centers on six high-value loops:

1. Serious incident intake, classification, and notification clocks.
2. Investigation dossier completion with closure gating.
3. Near-miss cluster promotion into the hazard register.
4. Permit conflict detection for simultaneous operations.
5. Corrective action effectiveness review and reopen logic.
6. Policy, audit-seal, KPI, and control-assertion governance.

## Owned datastore boundary

Owned business tables:

- `environment_health_safety_ehs_incident`
- `environment_health_safety_hazard`
- `environment_health_safety_inspection`
- `environment_health_safety_permit`
- `environment_health_safety_corrective_action`
- `environment_health_safety_safety_training`
- `environment_health_safety_audit_finding`
- `environment_health_safety_policy_rule`
- `environment_health_safety_runtime_parameter`
- `environment_health_safety_schema_extension`
- `environment_health_safety_control_assertion`
- `environment_health_safety_governed_model`

Event tables:

- `environment_health_safety_appgen_outbox_event`
- `environment_health_safety_appgen_inbox_event`
- `environment_health_safety_appgen_dead_letter_event`

No foreign tables are mutated.

## Lifecycle and governance behavior

- Incident closure is blocked until required investigation fields, corrective action effectiveness, and required regulator notification acknowledgement are complete.
- Fatalities, hospitalizations, major releases, and fire events start jurisdiction-aware reporting clocks.
- Repeated near misses with the same unsafe condition and task create or update a hazard entry with incident lineage.
- Permit conflicts are detected across area, time window, and permit type.
- Consumed governance events are idempotent and either re-evaluate owned records or seal owned evidence bundles.
- Continuous control testing opens exceptions for overdue serious-incident notifications and expired permits.

## Workflow and UX coverage

The workbench exposes incident cards with severity, recordability, notification status, and priority. Forms and wizards cover incident intake, hazard registration, permit issue, inspection sync, dynamic risk assessment, and regulator export preparation. The assistant layer provides preview-only triage, investigation gap detection, hazard promotion explanation, permit conflict checking, and governed CRUD previews.

## Complete Implementation Contract

The Environment Health Safety PBC owns incident, observation, permit, risk assessment, corrective action, inspection, training, exposure, waste manifest, audit, and regulatory obligation tables. Schema, migration, and model artifacts materialize these tables under the environment_health_safety prefix; no shared or foreign table mutation is permitted. Standard functionality includes incident intake, root-cause analysis, action tracking, permit compliance, safety inspections, environmental sampling, waste shipment tracking, training verification, exposure monitoring, regulatory calendar management, and audit evidence. Advanced functionality includes predictive incident risk, semantic permit/document instruction parsing, continuous control testing, carbon and environmental impact awareness, cryptographic audit evidence, and cross-PBC event federation.

Service command methods create and update incidents, observations, permits, inspections, actions, manifests, training records, exposure samples, and regulatory obligations. Query methods surface workbench, control, risk, compliance, and release evidence projections. API route contracts bind each command/query to permission RBAC policies. Event handling uses the AppGen-X contract with outbox, inbox, idempotency keys, retry policy, and dead-letter handling; stream-engine pickers are not exposed. Rules, parameters, and configuration govern severity matrices, permit thresholds, corrective-action SLAs, escalation policies, and accepted datastore backend values of PostgreSQL, MySQL, and MariaDB. The UI workbench exposes forms, wizards, controls, queues, configuration editors, permission-aware actions, and audit panels. The agent/chatbot exposes skills for task guidance, document instruction intake, and governed CRUD datastore mutation previews. Registration and discovery are side-effect-free, with release tests and seed evidence proving single-PBC operability.
## Manifest Traceability Appendix

This appendix maps the executable manifest for `environment_health_safety` to the implemented PBC package so release audits can verify that every declared surface is covered by the specification, code, UI, agent, tests, seed data, and AppGen-X integration evidence.

### tables
- `ehs_incident`
- `hazard`
- `inspection`
- `permit`
- `corrective_action`
- `safety_training`
- `audit_finding`
- `environment_health_safety_policy_rule`
- `environment_health_safety_runtime_parameter`
- `environment_health_safety_schema_extension`
- `environment_health_safety_control_assertion`
- `environment_health_safety_governed_model`

### apis
- `POST /ehs-incidents`
- `POST /hazards`
- `POST /inspections`
- `POST /permits`
- `POST /corrective-actions`
- `GET /environment-health-safety-workbench`

### emits
- `EnvironmentHealthSafetyCreated`
- `EnvironmentHealthSafetyUpdated`
- `EnvironmentHealthSafetyApproved`
- `EnvironmentHealthSafetyExceptionOpened`

### consumes
- `PolicyChanged`
- `AuditEventSealed`
- `OperationalKpiChanged`

### ui_fragments
- `EnvironmentHealthSafetyWorkbench`
- `EnvironmentHealthSafetyDetail`
- `EnvironmentHealthSafetyAssistantPanel`

### permissions
- `environment_health_safety.read`
- `environment_health_safety.create`
- `environment_health_safety.update`
- `environment_health_safety.approve`
- `environment_health_safety.admin`

### configuration
- `ENVIRONMENT_HEALTH_SAFETY_DATABASE_URL`
- `ENVIRONMENT_HEALTH_SAFETY_EVENT_TOPIC`
- `ENVIRONMENT_HEALTH_SAFETY_RETRY_LIMIT`
- `ENVIRONMENT_HEALTH_SAFETY_DEFAULT_POLICY`

### standard_features
- `ehs_incident_management`
- `environment_health_safety_workflow`
- `environment_health_safety_analytics`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `owned_schema_migrations_models`
- `appgen_x_outbox_inbox_eventing`
- `idempotent_handlers`
- `retry_dead_letter_evidence`
- `permissions`
- `seed_data`
- `workbench`
- `agentic_document_instruction_intake`
- `governed_datastore_crud`
- `ai_agent_task_assistance`
- `configuration_workbench`
- `continuous_release_assurance`

### advanced_capabilities
- `environment_health_safety_event_sourced_operational_history`
- `environment_health_safety_multi_tenant_policy_isolation`
- `environment_health_safety_schema_evolution_resilience`
- `environment_health_safety_autonomous_anomaly_detection`
- `environment_health_safety_semantic_document_instruction_understanding`
- `environment_health_safety_predictive_risk_scoring`
- `environment_health_safety_counterfactual_scenario_simulation`
- `environment_health_safety_cryptographic_audit_proofs`
- `environment_health_safety_continuous_control_testing`
- `environment_health_safety_carbon_and_sustainability_awareness`
- `environment_health_safety_cross_pbc_event_federation`
- `environment_health_safety_governed_ai_agent_execution`

The listed tables are owned by the package datastore and are materialized by schema, migration, and model artifacts. The API routes implement service command and query contracts, the emitted and consumed events use AppGen-X outbox, inbox, idempotent retry, and dead-letter handlers, and the UI fragments expose forms, wizards, controls, configuration editors, RBAC permission gates, and agent/chatbot guidance. Configuration keys, standard features, and advanced capabilities are backed by rule, parameter, seed, package registration, discovery, and release evidence. Supported ordinary database backends remain PostgreSQL, MySQL, and MariaDB.
