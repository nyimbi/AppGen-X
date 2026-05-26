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
