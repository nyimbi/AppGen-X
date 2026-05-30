# Real Estate Property Management PBC

## Purpose

`real_estate_property_management` is a standalone, single-PBC functional application for portfolio, building, unit, leasing, collections, maintenance, compliance, owner reporting, and governed AI preview workflows.

## Owned Domain Tables

Business tables:
- `real_estate_property_management_portfolio`
- `real_estate_property_management_property`
- `real_estate_property_management_building`
- `real_estate_property_management_unit`
- `real_estate_property_management_tenant`
- `real_estate_property_management_tenant_party`
- `real_estate_property_management_lease`
- `real_estate_property_management_rent_schedule`
- `real_estate_property_management_security_deposit`
- `real_estate_property_management_charge`
- `real_estate_property_management_cam_recovery`
- `real_estate_property_management_maintenance_request`
- `real_estate_property_management_inspection`
- `real_estate_property_management_vacancy`
- `real_estate_property_management_renewal`
- `real_estate_property_management_move_event`
- `real_estate_property_management_delinquency_case`
- `real_estate_property_management_notice`
- `real_estate_property_management_compliance_item`
- `real_estate_property_management_vendor_work_order`
- `real_estate_property_management_owner_statement`
- `real_estate_property_management_asset_performance_snapshot`
- `real_estate_property_management_assistant_artifact`

Support and event tables:
- `real_estate_property_management_policy_rule`
- `real_estate_property_management_runtime_parameter`
- `real_estate_property_management_schema_extension`
- `real_estate_property_management_control_assertion`
- `real_estate_property_management_governed_model`
- `real_estate_property_management_appgen_outbox_event`
- `real_estate_property_management_appgen_inbox_event`
- `real_estate_property_management_appgen_dead_letter_event`

## Canonical Operations

- `create_portfolio` -> `real_estate_property_management_portfolio`
- `create_property` -> `real_estate_property_management_property`
- `create_building` -> `real_estate_property_management_building`
- `create_unit` -> `real_estate_property_management_unit`
- `record_tenant` -> `real_estate_property_management_tenant`
- `create_lease` -> `real_estate_property_management_lease`
- `generate_rent_schedule` -> `real_estate_property_management_rent_schedule`
- `record_security_deposit` -> `real_estate_property_management_security_deposit`
- `post_charge` -> `real_estate_property_management_charge`
- `accrue_cam_recovery` -> `real_estate_property_management_cam_recovery`
- `open_maintenance_request` -> `real_estate_property_management_maintenance_request`
- `create_inspection` -> `real_estate_property_management_inspection`
- `track_vacancy` -> `real_estate_property_management_vacancy`
- `manage_renewal` -> `real_estate_property_management_renewal`
- `record_move_event` -> `real_estate_property_management_move_event`
- `escalate_delinquency` -> `real_estate_property_management_delinquency_case`
- `issue_notice` -> `real_estate_property_management_notice`
- `manage_compliance_case` -> `real_estate_property_management_compliance_item`
- `create_vendor_work_order` -> `real_estate_property_management_vendor_work_order`
- `publish_owner_report` -> `real_estate_property_management_owner_statement`
- `capture_asset_performance` -> `real_estate_property_management_asset_performance_snapshot`
- `preview_assistant_document_instruction` -> `real_estate_property_management_assistant_artifact`

## API Surface

Canonical routes:
- `POST /portfolios`
- `POST /properties`
- `POST /buildings`
- `POST /units`
- `POST /tenants`
- `POST /leases`
- `POST /rent-schedules`
- `POST /security-deposits`
- `POST /charges`
- `POST /cam-recoveries`
- `POST /maintenance-requests`
- `POST /inspections`
- `POST /vacancies`
- `POST /renewals`
- `POST /move-events`
- `POST /delinquencies`
- `POST /notices`
- `POST /compliance-items`
- `POST /vendor-work-orders`
- `POST /owner-reports`
- `POST /asset-performance-snapshots`
- `POST /assistant-previews`
- `GET /real-estate-property-management-workbench`

Compatibility aliases:
- `POST /propertys` -> `POST /properties`

## Workbench

The workbench is queue-centered and exposes:
- portfolio, property, building, unit, lease, collections, maintenance, compliance, owner-reporting, and assistant boards
- KPI cards for occupancy, vacancies, delinquency, notices, compliance, CAM billing, and annualized base rent
- queue rails for vacancies, renewals, delinquencies, maintenance, notices, and compliance
- owner statement and asset-performance panels
- governed assistant preview cards for document/instruction CRUD suggestions

## Governance

- Database backends: `postgresql, mysql, mariadb`
- Event contract: `AppGen-X`
- Stream engine picker: hidden
- Mutation previews require human confirmation
- Owner reporting, collections, maintenance, compliance, and AI review are permissioned separately

## Advanced Capabilities

- `real_estate_property_management_predictive_rent_roll_health`
- `real_estate_property_management_notice_deadline_guidance`
- `real_estate_property_management_vendor_triage_recommendations`
- `real_estate_property_management_owner_statement_lineage`
- `real_estate_property_management_asset_performance_forecasting`
- `real_estate_property_management_governed_ai_document_preview`
- `real_estate_property_management_counterfactual_renewal_scenarios`
- `real_estate_property_management_control_assertion_monitoring`
- `real_estate_property_management_event_sourced_operational_history`
- `real_estate_property_management_multi_tenant_policy_isolation`
- `real_estate_property_management_schema_evolution_resilience`
- `real_estate_property_management_autonomous_anomaly_detection`

## Release Scenarios

- `move_in_flow` covering record_tenant, create_lease, record_move_event, record_security_deposit
- `renewal_and_notice_flow` covering manage_renewal, issue_notice
- `arrears_escalation_flow` covering post_charge, escalate_delinquency
- `maintenance_closeout_flow` covering open_maintenance_request, create_vendor_work_order, create_inspection
- `owner_reporting_flow` covering publish_owner_report, capture_asset_performance
- `assistant_preview_flow` covering preview_assistant_document_instruction


## Manifest Traceability Appendix

The `real_estate_property_management` PBC is a stable PBC package with an owned datastore boundary; it rejects shared or foreign table access and exposes only API, event, and projection dependencies. Schema generation materializes migrations, model contracts, owned table definitions, and release evidence for portfolio, property, building, unit, tenant, tenant_party, lease, rent_schedule, security_deposit, charge, rent_charge, cam_recovery, maintenance_request, inspection, vacancy, renewal, move_event, delinquency_case, notice, compliance_item, vendor_work_order, owner_statement, asset_performance_snapshot, assistant_artifact, real_estate_property_management_policy_rule, real_estate_property_management_runtime_parameter, real_estate_property_management_schema_extension, real_estate_property_management_control_assertion, and real_estate_property_management_governed_model.

The service layer provides command and query APIs through routes including POST /portfolios, POST /properties, POST /buildings, POST /units, POST /tenants, POST /leases, POST /rent-schedules, POST /security-deposits, POST /charges, POST /rent-charges, POST /cam-recoveries, POST /maintenance-requests, POST /inspections, POST /vacancies, POST /renewals, POST /move-events, POST /delinquencies, POST /notices, POST /compliance-items, POST /vendor-work-orders, POST /owner-reports, POST /asset-performance-snapshots, POST /assistant-previews, GET /real-estate-property-management-workbench, and the legacy POST /propertys alias. The event contract uses AppGen-X outbox, inbox, retry, idempotency, and dead-letter handling for RealEstatePropertyManagementCreated, RealEstatePropertyManagementUpdated, RealEstatePropertyManagementApproved, RealEstatePropertyManagementExceptionOpened, PropertyPortfolioRegistered, LeaseLifecycleUpdated, CollectionsEscalated, and OwnerStatementPublished, while consuming PolicyChanged, CustomerUpdated, SupplierQualified, VendorQualified, and DocumentStored.

The UI workbench surfaces RealEstatePropertyManagementWorkbench, RealEstatePropertyManagementDetail, RealEstatePropertyManagementAssistantPanel, and RealEstatePropertyManagementQueueRail with permission/RBAC controls for real_estate_property_management.read, real_estate_property_management.create, real_estate_property_management.update, real_estate_property_management.approve, real_estate_property_management.admin, real_estate_property_management.collections, real_estate_property_management.maintenance, real_estate_property_management.compliance, real_estate_property_management.owner_reporting, and real_estate_property_management.ai_review. Configuration uses REAL_ESTATE_PROPERTY_MANAGEMENT_DATABASE_URL, REAL_ESTATE_PROPERTY_MANAGEMENT_EVENT_TOPIC, REAL_ESTATE_PROPERTY_MANAGEMENT_RETRY_LIMIT, and REAL_ESTATE_PROPERTY_MANAGEMENT_DEFAULT_POLICY; ordinary backends stay limited to PostgreSQL, MySQL, and MariaDB with no stream-engine picker exposed.

Standard capability coverage includes property_management, real_estate_property_management_workflow, real_estate_property_management_analytics, portfolio_and_building_hierarchy, unit_inventory, lease_and_tenant_operations, rent_and_charge_scheduling, cam_recoveries, maintenance_and_inspections, vacancy_and_renewal_management, move_in_move_out, delinquency_and_notice_management, compliance_management, vendor_work_orders, owner_reporting, asset_performance_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, and continuous_release_assurance. Advanced capability coverage includes real_estate_property_management_predictive_rent_roll_health, real_estate_property_management_notice_deadline_guidance, real_estate_property_management_vendor_triage_recommendations, real_estate_property_management_owner_statement_lineage, real_estate_property_management_asset_performance_forecasting, real_estate_property_management_governed_ai_document_preview, real_estate_property_management_counterfactual_renewal_scenarios, real_estate_property_management_control_assertion_monitoring, real_estate_property_management_event_sourced_operational_history, real_estate_property_management_multi_tenant_policy_isolation, real_estate_property_management_schema_evolution_resilience, real_estate_property_management_autonomous_anomaly_detection, real_estate_property_management_semantic_document_instruction_understanding, real_estate_property_management_predictive_risk_scoring, real_estate_property_management_counterfactual_scenario_simulation, real_estate_property_management_cryptographic_audit_proofs, real_estate_property_management_continuous_control_testing, real_estate_property_management_carbon_and_sustainability_awareness, real_estate_property_management_cross_pbc_event_federation, and real_estate_property_management_governed_ai_agent_execution.

Registration is side-effect-free through register/discovery plans, and the package includes tests, seed data, release evidence, rule, parameter, and configuration contracts. The assistant/chatbot contributes skills for document instruction understanding and CRUD datastore mutation previews, with every mutation gated by confirmation and every generated action scoped to owned tables.

This final paragraph exists as explicit release guidance for future maintainers: every property, lease, rent, maintenance, compliance, owner, and assistant pathway must keep owned-table persistence, migration-backed models, command/query service contracts, AppGen-X events, idempotent retryable handlers, RBAC permissions, seed fixtures, release tests, and side-effect-free registration synchronized.
