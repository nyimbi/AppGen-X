# Water and Wastewater Operations PBC

## Purpose

The `water_wastewater_operations` PBC is a packaged business capability for treatment plants, process units, source water, production, distribution zones, pressure and quality samples, pump and valve operations, sewer collection, lift stations, wastewater treatment, discharge permits, lab compliance, incidents, flushing, hydrants, asset isolation, SCADA projections, workbench controls, and governed operator assistance. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `water_wastewater_operations`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/water_wastewater_operations`.
- Runtime entrypoint: `water_wastewater_operations_runtime_capabilities()`.
- UI entrypoint: `water_wastewater_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

Owned business tables are:

- `water_wastewater_operations_treatment_plant`
- `water_wastewater_operations_process_unit`
- `water_wastewater_operations_source_water_observation`
- `water_wastewater_operations_production_run`
- `water_wastewater_operations_distribution_zone`
- `water_wastewater_operations_pressure_quality_sample`
- `water_wastewater_operations_pump_operation`
- `water_wastewater_operations_valve_operation`
- `water_wastewater_operations_sewer_collection_area`
- `water_wastewater_operations_lift_station`
- `water_wastewater_operations_wastewater_treatment_batch`
- `water_wastewater_operations_discharge_permit`
- `water_wastewater_operations_lab_compliance_case`
- `water_wastewater_operations_operations_incident`
- `water_wastewater_operations_flushing_program`
- `water_wastewater_operations_hydrant_asset`
- `water_wastewater_operations_asset_isolation_plan`
- `water_wastewater_operations_scada_projection`
- `water_wastewater_operations_water_wastewater_operations_policy_rule`
- `water_wastewater_operations_water_wastewater_operations_runtime_parameter`
- `water_wastewater_operations_water_wastewater_operations_schema_extension`
- `water_wastewater_operations_water_wastewater_operations_control_assertion`
- `water_wastewater_operations_water_wastewater_operations_governed_model`

Runtime AppGen-X event tables are `water_wastewater_operations_appgen_outbox_event`, `water_wastewater_operations_appgen_inbox_event`, and `water_wastewater_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. GIS, SCADA historians, lab systems, and customer systems are represented only through projections, work packets, or declared dependencies.

## Schema, Migration, and Model Generation

The package materializes an owned schema contract, migration contract, and model contract from the package directory. Every owned table is represented in `migrations/001_initial.sql`, `schema_contract.py`, and `models.py`. Runtime contracts expose schema evidence without accessing shared generator state. Release evidence links schema, service, UI, agent, and smoke scenarios so package-local tests can prove the generated shape is coherent.

## Service, API, Command, and Query Contracts

Command operations include treatment plant registration, process-unit configuration, source-water observation recording, production-run recording, distribution-zone definition, pressure-quality sampling, pump operations, valve operations, sewer collection registration, lift-station monitoring, wastewater-treatment batch recording, discharge-permit registration, lab-compliance case recording, incident reporting, flushing planning, hydrant inspection, isolation-plan creation, and SCADA projection capture. Query operations include the workbench command center, schema contract, service contract, release evidence, advanced assessment, API contract, and document-instruction parsing.

Public API routes are package-local and AppGen-X aligned. They preserve an `owned_datastore_plus_outbox` transaction boundary, side-effect-free query surfaces, and no stream engine choice. Package tests and release evidence verify service and route execution together.

## Events, Outbox, Inbox, Dead-Letter, Idempotency, and Retry

Emitted events stay on the AppGen-X contract:

- `WaterWastewaterOperationsCreated`
- `WaterWastewaterOperationsUpdated`
- `WaterWastewaterOperationsApproved`
- `WaterWastewaterOperationsExceptionOpened`

Consumed events are:

- `PolicyChanged`
- `AuditEventSealed`
- `OperationalKpiChanged`

The events module also declares domain-event specializations such as `sample_collected`, `limit_exceeded`, `pump_alerted`, `interruption_opened`, `advisory_issued`, `work_completed`, and `report_certified`. These remain payload-level specializations inside the fixed AppGen-X envelope. Handlers enforce idempotency and retry with dead-letter evidence, and package tests verify duplicates and unknown-event routing.

## UI, Workbench, Permission, and RBAC Surface

Workbench fragments remain `WaterWastewaterOperationsWorkbench`, `WaterWastewaterOperationsDetail`, and `WaterWastewaterOperationsAssistantPanel`. The command center exposes sections for treatment, distribution, pressure and quality, pump and valve operations, sewer and lift-station risk, incidents and advisories, flushing and hydrants, asset isolation, SCADA projection health, and release evidence.

Package-local forms include `TreatmentPlantForm`, `ProcessUnitForm`, `PressureQualitySampleForm`, `IncidentReportForm`, `DischargePermitForm`, and `IsolationPlanForm`. Wizards include boil-water advisory, overflow response, hydrant flushing, asset isolation, and lab compliance review. Controls include plant mode, permit risk, pressure alert, pump standby, overflow risk, and governed approval controls. Permissions stay inside the PBC and include read, operate, approve, admin, event, and audit scopes.

## Rules, Parameters, Configuration, and Seed Data

Rules cover treatment-state policy, sampling compliance, pressure response, pump reliability, overflow escalation, hydrant flushing, agent governance, and SCADA freshness. Parameters are bounded and runtime-editable for distribution pressure, residual, turbidity, lift-station risk, hydrant flow, incident notification, SCADA freshness, and workbench limits. Configuration allows only PostgreSQL, MySQL, and MariaDB and fixes the AppGen-X topic. Seed data establishes representative treatment plant, distribution zone, and discharge permit records for release assurance.

## Agent, Assistant, Chatbot, Skill, Document, Instruction, and CRUD Governance

The package contributes confirmation-gated skills for sample interpretation, incident narration, isolation planning, and SCADA projection review. The chatbot interface explicitly advertises `governed_datastore_crud`, mutation preview, sample interpretation, and incident narration. Document and instruction intake stays side-effect-free and returns candidate owned tables plus required confirmation gates. All CRUD plans reject foreign tables, require human confirmation, and preserve the AppGen-X event contract.

## Standard and Advanced Capabilities

Standard capabilities cover treatment plant management, process-unit configuration, source-water monitoring, production and distribution management, pressure-quality sampling, pump and valve operations, sewer collection monitoring, lift-station overflow prevention, wastewater-treatment compliance, discharge-permit management, lab compliance, incidents and advisories, flushing and hydrants, asset isolation, SCADA projection boundaries, configuration, rules, parameters, owned schema, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, permissions, seed data, workbench, governed CRUD, assistant guidance, configuration workbench, and continuous release assurance.

Advanced capabilities cover event-sourced operational history, multi-tenant policy isolation, schema-evolution resilience, autonomous anomaly detection, semantic document understanding, predictive risk scoring, counterfactual simulation, cryptographic audit proofs, continuous control testing, carbon and sustainability awareness, cross-PBC event federation, and governed AI execution.

## Package Release Evidence, Tests, and Side-Effect-Free Registration

Release evidence now includes schema, service, API, UI binding, agent, control summary, and smoke scenarios. Smoke scenarios create treatment, process-unit, sample, pump, incident, isolation, SCADA, permit, and lab-compliance records and prove they appear in the workbench. Package-local tests cover contract function names required by audits, runtime capabilities, operational slice behavior, configuration and parameter bounds, event idempotency, and governed agent behavior. Registration, metadata, and discovery remain side-effect-free.

## Manifest Traceability Appendix

- tables: treatment_plant, water_quality_sample, permit_limit, pump_asset, service_interruption, field_work_order, compliance_sample, process_unit, source_water_observation, production_run, distribution_zone, pressure_quality_sample, pump_operation, valve_operation, sewer_collection_area, lift_station, wastewater_treatment_batch, discharge_permit, lab_compliance_case, operations_incident, flushing_program, hydrant_asset, asset_isolation_plan, scada_projection, water_wastewater_operations_policy_rule, water_wastewater_operations_runtime_parameter, water_wastewater_operations_schema_extension, water_wastewater_operations_control_assertion, water_wastewater_operations_governed_model
- apis: POST /treatment-plants, POST /water-quality-samples, POST /permit-limits, POST /pump-assets, POST /service-interruptions, GET /water-wastewater-operations-workbench, POST /water-ops/treatment-plants, POST /water-ops/process-units, POST /water-ops/source-water, POST /water-ops/production-runs, POST /water-ops/distribution-zones, POST /water-ops/pressure-quality-samples, POST /water-ops/pump-operations, POST /water-ops/valve-operations, POST /water-ops/sewer-collection-areas, POST /water-ops/lift-stations, POST /water-ops/wastewater-treatment-batches, POST /water-ops/discharge-permits, POST /water-ops/lab-compliance-cases, POST /water-ops/incidents, POST /water-ops/flushing-programs, POST /water-ops/hydrants, POST /water-ops/isolation-plans, POST /water-ops/scada-projections, GET /water-ops/workbench, GET /water-ops/release-evidence
- emits: WaterWastewaterOperationsCreated, WaterWastewaterOperationsUpdated, WaterWastewaterOperationsApproved, WaterWastewaterOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- ui_fragments: WaterWastewaterOperationsWorkbench, WaterWastewaterOperationsDetail, WaterWastewaterOperationsAssistantPanel
- permissions: water_wastewater_operations.read, water_wastewater_operations.create, water_wastewater_operations.update, water_wastewater_operations.operate, water_wastewater_operations.approve, water_wastewater_operations.admin, water_wastewater_operations.event, water_wastewater_operations.audit
- configuration: WATER_WASTEWATER_OPERATIONS_DATABASE_URL, WATER_WASTEWATER_OPERATIONS_EVENT_TOPIC, WATER_WASTEWATER_OPERATIONS_RETRY_LIMIT, WATER_WASTEWATER_OPERATIONS_DEFAULT_POLICY
- standard_features: treatment_plant_management, water_wastewater_operations_workflow, water_wastewater_operations_analytics, agentic_document_instruction_intake, process_unit_configuration, source_water_monitoring, production_and_distribution_management, pressure_quality_sampling, pump_valve_operations, sewer_collection_monitoring, lift_station_overflow_prevention, wastewater_treatment_compliance, discharge_permit_management, lab_compliance_and_chain_of_custody, incident_and_advisory_management, flushing_and_hydrant_programs, asset_isolation, scada_projection_boundary, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: water_wastewater_operations_event_sourced_operational_history, water_wastewater_operations_multi_tenant_policy_isolation, water_wastewater_operations_schema_evolution_resilience, water_wastewater_operations_autonomous_anomaly_detection, water_wastewater_operations_semantic_document_instruction_understanding, water_wastewater_operations_predictive_risk_scoring, water_wastewater_operations_counterfactual_scenario_simulation, water_wastewater_operations_cryptographic_audit_proofs, water_wastewater_operations_continuous_control_testing, water_wastewater_operations_carbon_and_sustainability_awareness, water_wastewater_operations_cross_pbc_event_federation, water_wastewater_operations_governed_ai_agent_execution
