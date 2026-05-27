# Enterprise Asset Management PBC Specification

## Scope

`eam` owns the complete enterprise asset management domain for AppGen-X generated
applications. It manages maintainable equipment, asset hierarchy, maintenance
strategies, preventive plans, condition monitoring, work requests, work orders,
scheduling, safety controls, spare usage, labor execution, downtime, reliability
analytics, compliance evidence, warranties, service-vendor performance, rules,
parameters, configuration, and workbench UI fragments.

The PBC composes with production, quality, inventory, procurement, asset
lifecycle, audit, and analytics PBCs only through APIs, AppGen-X events, and
read-model projections. It never shares tables with those PBCs.

## Owned Boundary

Owned tables:

- `equipment`
- `maintenance_plan`
- `work_order`
- `spare_part_usage`
- `condition_reading`
- `meter_reading`
- `failure_event`
- `maintenance_schedule`
- `service_vendor_event`
- `safety_permit`
- `maintenance_rule`
- `maintenance_parameter`
- `maintenance_configuration`
- `maintenance_outbox`
- `maintenance_inbox`
- `maintenance_dead_letter`

Allowed datastore backends are PostgreSQL, MySQL, and MariaDB. Ordinary eventing
uses the AppGen-X outbox/inbox event contract.

Executable runtime guarantees for this package are strict:

- Runtime configuration rejects any backend outside PostgreSQL, MySQL, and
  MariaDB.
- Runtime configuration requires an AppGen-X event topic, stamps the
  AppGen-X event contract, and does not expose any user-facing stream-engine
  or eventing-backend picker.
- Parameters are bounded to the package-owned maintenance controls:
  `default_pm_interval_days`, `failure_risk_threshold`,
  `mttr_target_hours`, `criticality_weight`, `safety_risk_threshold`, and
  `retention_days`.
- Rules must include `rule_id`, `tenant`, `rule_type`,
  `eligible_work_types`, `allowed_sites`, and `status`; compiled rule
  evidence is deterministic and hash-based.
- Workbench/runtime evidence must expose configuration, rule, and parameter
  bindings for the active tenant view.

## Standard Capabilities

- Equipment master data, hierarchy, criticality, location, warranty, and
  maintainability state.
- Preventive, predictive, condition-based, calibration, statutory, and warranty
  maintenance strategies.
- Maintenance plan creation, release, revisioning, interval control, meter
  control, and trigger evaluation.
- Work request intake, triage, approval, planning, work-order creation,
  assignment, scheduling, dispatch, mobile execution, completion, and closure.
- Spare part reservation, issue, return, consumption costing, and inventory
  projection handoff.
- Labor skill matching, craft capacity checks, shift assignment, and overtime
  exposure scoring.
- Safety permit, lockout/tagout, hazard, isolation, and risk-acceptance gates.
- Downtime capture, failure coding, root-cause capture, corrective action, MTBF,
  MTTR, backlog, schedule compliance, wrench-time, and reliability analytics.
- Contractor/vendor service events, SLA compliance, warranty recovery, and
  procurement/service-performance handoffs.
- Rule execution, parameter management, runtime configuration, permissions,
  seed data, UI workbench fragments, idempotent handlers, retry/dead-letter
  evidence, and release audit evidence.

## Advanced Capabilities

- Event-sourced maintenance lifecycle with immutable hash-chained history.
- Graph-relational asset topology spanning equipment, locations, meters,
  plans, work orders, permits, spares, vendors, and reliability events.
- Tenant-isolated reliability operations with independent configuration,
  parameters, rules, and crypto epochs.
- Schema evolution through governed JSON-style extension registration.
- Probabilistic failure, downtime, safety, and cost exposure scoring.
- Real-time reliability analytics over work orders, failure events, downtime,
  MTBF, MTTR, backlog, and schedule compliance.
- Counterfactual maintenance strategy simulation for interval and condition
  triggers.
- Temporal failure forecasting and risk-weighted work prioritization.
- Autonomous maintenance exception recommendation with auditable rationale.
- Semantic maintenance instruction parsing for work requests and planning text.
- Predictive maintenance risk scoring and route selection across workbench API,
  mobile offline queue, outbox, and vendor service channels.
- Cryptographic maintenance-compliance proofs, immutable regulatory trails,
  dynamic policy screening, and continuous maintenance-control testing.
- Universal API and AppGen-X event contracts, federation views, decentralized
  equipment identity checks, resilience drills, crypto agility, carbon-aware
  scheduling, mathematical optimization, mechanism-design labor/spare
  allocation, anomaly detection, stochastic exposure modeling, and governed
  reliability models.

## APIs

- `POST /equipment`
- `POST /maintenance-plans`
- `POST /work-orders`
- `POST /work-orders/{id}/schedule`
- `POST /work-orders/{id}/complete`
- `POST /condition-readings`
- `POST /meter-readings`
- `POST /spare-usage`
- `POST /safety-permits`
- `GET /maintenance-workbench`
- `POST /maintenance-rules`
- `POST /maintenance-parameters`
- `POST /maintenance-configuration`

## Events

Emitted:

- `EquipmentRegistered`
- `MaintenancePlanReleased`
- `ConditionReadingRecorded`
- `MeterReadingRecorded`
- `SafetyPermitApproved`
- `WorkOrderCreated`
- `WorkOrderScheduled`
- `SparePartUsed`
- `MaintenanceCompleted`
- `VendorPerformanceUpdated`

Consumed:

- `DowntimeCaptured`
- `NonConformanceRaised`
- `InventoryReservationConfirmed`
- `PurchaseOrderAcknowledged`
- `AssetLifecycleUpdated`

Handlers are idempotent through `eam:<EventType>:<event_id>` keys, retry through
the AppGen-X outbox adapter, and route exhausted failures to
`eam.dead_letter`.

## UI

The package exports a workbench UI contract with fragments for equipment,
maintenance plans, work orders, scheduling, reliability analytics, safety,
spares, vendor service, rules, parameters, and configuration.

The configuration editor exposes only datastore and AppGen-X event topic
controls. The workbench must surface configuration binding status, bound rule
identifiers, and bound parameter identifiers without presenting a stream-engine
selector or alternative user-facing eventing mode.

## Schema, Service, And Release Evidence

The implementation directory is `src/pyAppGen/pbcs/eam`, and the package
exports side-effect-free registration through `implementation_contract()`.
`eam_build_schema_contract()` emits owned schema descriptors, generated
migration descriptors, generated model descriptors, and owned relationships for
equipment, meters, maintenance plans, work orders, safety permits, spare usage,
service-vendor events, reliability signals, and AppGen-X runtime tables.

`eam_build_service_contract()` proves command and query methods for runtime
configuration, rule and parameter registration, schema extension ownership,
equipment registration, plan release, work-order scheduling and completion,
condition/meter readings, spare usage, service-vendor evidence, event inbox
handling, UI/workbench reads, API descriptors, permissions, boundary checks,
and release evidence. The owned boundary rejects shared or foreign tables and
allows cross-PBC dependencies only through declared APIs, AppGen-X events, and
package-local projections.

Release evidence includes package-local seed data for maintenance priorities,
work-order states, meter units, safety permit classes, spare-usage reasons,
vendor service classes, and reliability risk bands. Focused tests validate the
seed descriptors together with schema, migration, model, service, route, event,
handler, UI, RBAC, configuration, and release contracts.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `eam`
- Mesh: `opsmfg`
- Datastore backend: `postgresql`

### Owned Tables

- `equipment`
- `maintenance_plan`
- `work_order`
- `spare_part_usage`
- `condition_reading`
- `meter_reading`
- `failure_event`
- `maintenance_schedule`
- `service_vendor_event`
- `safety_permit`
- `maintenance_rule`
- `maintenance_parameter`
- `maintenance_configuration`
- `maintenance_outbox`
- `maintenance_inbox`
- `maintenance_dead_letter`

### API Routes

- `POST /equipment`
- `POST /maintenance-plans`
- `POST /work-orders`
- `POST /work-orders/{id}/schedule`
- `POST /work-orders/{id}/complete`
- `POST /condition-readings`
- `POST /meter-readings`
- `POST /spare-usage`
- `POST /safety-permits`
- `GET /maintenance-workbench`
- `POST /maintenance-rules`
- `POST /maintenance-parameters`
- `POST /maintenance-configuration`

### Emitted Events

- `EquipmentRegistered`
- `MaintenancePlanReleased`
- `ConditionReadingRecorded`
- `MeterReadingRecorded`
- `SafetyPermitApproved`
- `WorkOrderCreated`
- `WorkOrderScheduled`
- `SparePartUsed`
- `MaintenanceCompleted`
- `VendorPerformanceUpdated`

### Consumed Events

- `DowntimeCaptured`
- `NonConformanceRaised`
- `InventoryReservationConfirmed`
- `PurchaseOrderAcknowledged`
- `AssetLifecycleUpdated`

### UI Fragments

- `MaintenanceWorkbench`
- `EquipmentRegistry`
- `AssetHierarchyMap`
- `MaintenancePlanConsole`
- `ConditionMonitoringPanel`
- `WorkOrderBoard`
- `MaintenanceScheduler`
- `SpareUsageConsole`
- `SafetyPermitConsole`
- `ReliabilityDashboard`
- `VendorServicePanel`
- `MaintenanceRuleStudio`
- `MaintenanceParameterConsole`
- `MaintenanceConfigurationPanel`

### Permissions

- `eam.read`
- `eam.equipment`
- `eam.plan`
- `eam.execute`
- `eam.safety`
- `eam.configure`
- `eam.audit`

### Configuration Keys

- `database_backend`
- `event_topic`
- `retry_limit`
- `allowed_sites`
- `allowed_priorities`
- `allowed_work_types`
- `allowed_permit_types`
- `default_timezone`
- `workbench_limit`

### Standard Features

- `equipment_registry`
- `asset_hierarchy`
- `location_tracking`
- `criticality_model`
- `warranty_tracking`
- `maintenance_strategy`
- `preventive_maintenance_plan`
- `predictive_maintenance_plan`
- `condition_monitoring`
- `meter_reading`
- `work_request_intake`
- `work_order_planning`
- `work_order_scheduling`
- `mobile_execution`
- `safety_permit`
- `spare_part_reservation`
- `spare_part_usage`
- `labor_assignment`
- `downtime_capture`
- `failure_analysis`
- `mtbf_mttr_analytics`
- `vendor_service_tracking`
- `compliance_evidence`
- `idempotent_handlers`
- `permissions`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `seed_data`
- `workbench`

### Advanced Capabilities

- `event_sourced_maintenance_lifecycle`
- `graph_relational_asset_topology`
- `multi_tenant_maintenance_isolation`
- `schema_evolution_resilient_maintenance_schema`
- `probabilistic_failure_safety_cost_scoring`
- `real_time_reliability_analytics`
- `counterfactual_strategy_simulation`
- `temporal_failure_forecasting`
- `autonomous_maintenance_exception_resolution`
- `semantic_maintenance_instruction_parsing`
- `predictive_maintenance_risk_scoring`
- `self_healing_maintenance_route_selection`
- `zero_knowledge_maintenance_compliance_proof`
- `immutable_maintenance_audit_trail`
- `dynamic_maintenance_policy_screening`
- `automated_maintenance_control_testing`
- `universal_api_async_streaming`
- `cross_system_maintenance_federation`
- `production_quality_inventory_procurement_integration`
- `decentralized_equipment_identity`
- `chaos_engineered_maintenance_tolerance`
- `quantum_resistant_maintenance_authorization`
- `carbon_aware_maintenance_scheduling`
- `algebraic_maintenance_schedule_optimization`
- `mechanism_design_labor_spare_allocation`
- `information_theoretic_failure_anomaly_detection`
- `temporal_maintenance_exposure_stochastic_modeling`
- `distributed_systems_engineering`
- `probabilistic_ml_maintenance_risk`
- `cryptographic_engineering`
- `mathematical_optimization`
- `maintenance_mlops_governance`

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->

## Agent, Chatbot Skills, And Self-Registration Contract

The `eam` package exposes a first-class PBC agent and chatbot interface through `agent.py`. The composed application imports these capabilities under the `eam_skills` namespace so a single application assistant can route help, task guidance, document instruction intake, governed datastore CRUD planning, workbench navigation, and policy explanation back to the owning PBC instead of inventing cross-package mutations. The agent contract is scoped to the `Enterprise Asset Management` boundary and must name the command, permission, owned tables, idempotency key, expected AppGen-X event, and human confirmation requirement before any create, update, or delete plan is eligible to execute.

Document and instruction intake is explicit release evidence. The chatbot can accept uploaded documents, operational notes, or user instructions, extract candidate facts for owned tables such as `eam_equipment`, `eam_maintenance_plan`, `eam_work_order`, `eam_spare_part_usage`, `eam_condition_reading`, `eam_meter_reading`, validate those facts against package rules, parameters, configuration, and permissions, and return a side-effect-free mutation preview. The preview is not a write. It is a governed plan that references service operations such as , uses AppGen-X event expectations such as `EquipmentRegistered`, `MaintenancePlanReleased`, `ConditionReadingRecorded`, `MeterReadingRecorded`, rejects foreign tables, and records whether a read-only query or a confirmed command is required. This keeps AI assistance professional, auditable, and bounded to the PBC datastore.

Self-registration is also part of the specification. `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` must produce a side-effect-free discovery and registration plan for `eam`. Registration metadata identifies the source package directory, required artifacts, owned datastore, AppGen-X event contract, UI fragments, RBAC descriptors, configuration schema, seed data, tests, and release evidence without mutating the global catalog during discovery. Composition tooling may then register the PBC, merge the `eam_skills` contribution into the single composed assistant, and expose the workbench UI while preserving owned-table boundaries and declared API/event/projection dependencies.

