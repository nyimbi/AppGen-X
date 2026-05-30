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
