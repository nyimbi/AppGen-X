# Food Safety Quality Compliance PBC

## Purpose

The `food_safety_quality_compliance` slice owns HACCP plan versions, critical control points, inspections, nonconformances, recall events, supplier audits, quality holds, rules, parameters, governed assistant previews, and release evidence. It does not read or mutate foreign inventory, manufacturing, supplier-master, or customer tables.

## Domain Model

### HACCP Plan Versions

- Plan identity: `plan_code`, `version`, `facility_code`, `product_scope`
- Governance: `approvals`, `effective_from`, `supersedes_plan_id`, `supersession_reason`
- Safety evidence: `process_steps`, `hazard_analysis`, `evidence_hash`
- Approval gate: required hazards with `requires_ccp=true` must be covered by CCP definitions and approvals from food safety, quality, and operations must be present.

### Critical Control Points

- Linkage: `plan_id`, `process_step_code`, `hazard_id`
- Limits: `limit_min`, `limit_max`, `unit`
- Monitoring: `monitoring_method`, `monitoring_frequency_minutes`, `verification_requirement`
- Corrective action: `corrective_action`, `responsible_role`

### Inspections, Nonconformances, and Holds

- Inspections pin `plan_id` and `plan_version` from the active approved plan.
- Critical or allergen/temperature/foreign-material findings open quality holds automatically.
- Major and critical findings also open nonconformances.
- Major or critical nonconformances cannot close without root cause, preventive action, and effectiveness evidence.
- Holds capture affected lots, quantity, location, release criteria, disposition, approvers, and linked HACCP version.

### Supplier Audits

- Supplier audits store supplier projections, commodity, audit type, findings, risk rating, corrective actions, and expiry tracking.
- High-risk, expired, or major-finding audits block approval status.
- Near-expiry audits are surfaced in the workbench.

### Recall Events

- Recall and mock recall flows use `genealogy_projection` and `shipment_projection` inputs only.
- Foreign table access attempts are rejected.
- Mock drills do not mutate live recall state and return evidence packets with elapsed time against the configured target.

### Governed Assistant Previews

- Assistant previews resolve to owned tables only.
- Citations are mandatory.
- Release-impacting previews require explicit release review before approval.
- Approved previews record approver identity and confirmation state.

## Public APIs

- `POST /haccp-plans`
- `POST /critical-control-points`
- `POST /inspections`
- `POST /nonconformances`
- `POST /recall-events`
- `GET /food-safety-quality-compliance-workbench`

## Workbench

- HACCP Approval Queue
- Inspection Escalation Queue
- Open Quality Holds
- Supplier Audit Monitor
- Recall Readiness Board

## Forms And Wizards

- Forms: HACCP plan version intake, CCP definition, inspection review, recall event or mock drill
- Wizards: HACCP authoring and recall response
- Controls: approve HACCP plan, open hold, release hold, run mock recall, approve assistant preview

## Eventing

- Emitted: `FoodSafetyQualityComplianceCreated`, `FoodSafetyQualityComplianceUpdated`, `FoodSafetyQualityComplianceApproved`, `FoodSafetyQualityComplianceExceptionOpened`
- Consumed: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- Idempotency: required for all inbound event handling
- Dead-letter evidence: unexpected events land in `food_safety_quality_compliance_appgen_dead_letter_event`

## Rules And Parameters

### Rules

- `haccp_plan_effectivity_rule`
- `ccp_hazard_mapping_rule`
- `critical_findings_hold_rule`
- `major_nonconformance_closure_rule`
- `supplier_approval_expiry_rule`
- `recall_projection_boundary_rule`
- `assistant_mutation_guardrail_rule`

### Parameters

- `ccp_monitoring_grace_minutes`
- `hold_release_min_approvers`
- `supplier_audit_expiry_warning_days`
- `mock_recall_target_minutes`
- `regulatory_obligation_sla_days`
- `workbench_limit`

## Complete Implementation Contract

The Food Safety Quality Compliance PBC owns HACCP plans, critical control points, inspections, nonconformances, corrective actions, supplier audits, recall events, quality holds, environmental monitoring, allergen controls, sanitation checks, release records, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X event tables. Generated schema, migration, and model artifacts are package-local and preserve the owned boundary; generated services never mutate shared tables. Standard functionality covers HACCP design, CCP monitoring, inspection programs, supplier qualification, lot release, quality holds, nonconformance CAPA, recall mock runs, sanitation verification, allergen cross-contact controls, and audit evidence. Advanced functionality covers predictive quality risk, semantic document instruction understanding, anomaly detection, counterfactual recall simulation, continuous control testing, cryptographic evidence, sustainability/carbon awareness, and governed AI execution.

Service command methods and API route contracts cover plan creation, approval, CCP updates, inspection capture, nonconformance lifecycle, supplier audit review, quality-hold release, recall execution, configuration, parameter, and rule updates. Query methods expose workbench, release evidence, plan detail, recall packet, and compliance projections. Events use the AppGen-X outbox, inbox, idempotent handler, retry policy, and dead-letter contract. UI forms, wizards, controls, RBAC permission gates, rule editors, parameter editors, and configuration surfaces expose the full capability. The PBC chatbot skill set accepts documents/instructions, builds CRUD datastore mutation previews, rejects foreign tables, and contributes skills to the composed single agent. Self-registration and discovery are side-effect-free. Release evidence includes tests, seed data, PostgreSQL, MySQL, and MariaDB policy compliance, and AppGen-X eventing.
## Manifest Traceability Appendix

This appendix maps the executable manifest for `food_safety_quality_compliance` to the implemented PBC package so release audits can verify that every declared surface is covered by the specification, code, UI, agent, tests, seed data, and AppGen-X integration evidence.

### tables
- `haccp_plan`
- `critical_control_point`
- `inspection`
- `nonconformance`
- `recall_event`
- `supplier_audit`
- `quality_hold`
- `food_safety_quality_compliance_policy_rule`
- `food_safety_quality_compliance_runtime_parameter`
- `food_safety_quality_compliance_schema_extension`
- `food_safety_quality_compliance_control_assertion`
- `food_safety_quality_compliance_governed_model`

### apis
- `POST /haccp-plans`
- `POST /critical-control-points`
- `POST /inspections`
- `POST /nonconformances`
- `POST /recall-events`
- `GET /food-safety-quality-compliance-workbench`

### emits
- `FoodSafetyQualityComplianceCreated`
- `FoodSafetyQualityComplianceUpdated`
- `FoodSafetyQualityComplianceApproved`
- `FoodSafetyQualityComplianceExceptionOpened`

### consumes
- `PolicyChanged`
- `AuditEventSealed`
- `OperationalKpiChanged`

### ui_fragments
- `FoodSafetyQualityComplianceWorkbench`
- `FoodSafetyQualityComplianceDetail`
- `FoodSafetyQualityComplianceAssistantPanel`

### permissions
- `food_safety_quality_compliance.read`
- `food_safety_quality_compliance.create`
- `food_safety_quality_compliance.update`
- `food_safety_quality_compliance.approve`
- `food_safety_quality_compliance.admin`

### configuration
- `FOOD_SAFETY_QUALITY_COMPLIANCE_DATABASE_URL`
- `FOOD_SAFETY_QUALITY_COMPLIANCE_EVENT_TOPIC`
- `FOOD_SAFETY_QUALITY_COMPLIANCE_RETRY_LIMIT`
- `FOOD_SAFETY_QUALITY_COMPLIANCE_DEFAULT_POLICY`

### standard_features
- `haccp_plan_management`
- `food_safety_quality_compliance_workflow`
- `food_safety_quality_compliance_analytics`
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
- `food_safety_quality_compliance_event_sourced_operational_history`
- `food_safety_quality_compliance_multi_tenant_policy_isolation`
- `food_safety_quality_compliance_schema_evolution_resilience`
- `food_safety_quality_compliance_autonomous_anomaly_detection`
- `food_safety_quality_compliance_semantic_document_instruction_understanding`
- `food_safety_quality_compliance_predictive_risk_scoring`
- `food_safety_quality_compliance_counterfactual_scenario_simulation`
- `food_safety_quality_compliance_cryptographic_audit_proofs`
- `food_safety_quality_compliance_continuous_control_testing`
- `food_safety_quality_compliance_carbon_and_sustainability_awareness`
- `food_safety_quality_compliance_cross_pbc_event_federation`
- `food_safety_quality_compliance_governed_ai_agent_execution`

The listed tables are owned by the package datastore and are materialized by schema, migration, and model artifacts. The API routes implement service command and query contracts, the emitted and consumed events use AppGen-X outbox, inbox, idempotent retry, and dead-letter handlers, and the UI fragments expose forms, wizards, controls, configuration editors, RBAC permission gates, and agent/chatbot guidance. Configuration keys, standard features, and advanced capabilities are backed by rule, parameter, seed, package registration, discovery, and release evidence. Supported ordinary database backends remain PostgreSQL, MySQL, and MariaDB.
