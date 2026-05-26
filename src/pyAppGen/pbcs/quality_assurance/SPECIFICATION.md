# Quality Assurance PBC Specification

## Purpose

`quality_assurance` owns inspection planning, sampling, lot and batch quality
state, inspection tests, measurement series, nonconformance, CAPA, holds,
release evidence, calibration, procedures, supplier quality, customer quality,
audit packets, rule and parameter governance, configuration, AppGen-X event
evidence, and release-readiness proof for manufacturing and supply operations.

The package composes with production, inventory, procurement, returns,
maintenance, customer, and audit capabilities only through declared APIs,
AppGen-X events, and package-local projections. It does not share source tables
with adjacent PBCs.

## Owned Datastore Boundary

The runtime owns these tables and emits generated model and migration
descriptors for each:

- `inspection_plan`: inspection plan master, revision, source, and sampling mode.
- `sampling_scheme`: sample size, acceptance method, AQL, and rejection gate.
- `lot_batch_profile`: lot or batch identity, supplier, manufacture, and expiry.
- `inspection_test_definition`: governed inspection or measurement definition.
- `inspection_result`: executed inspection result, decision, and inspector proof.
- `inspection_measurement_series`: SPC-ready measurement aggregates and Cpk evidence.
- `quality_hold`: hold, quarantine, severity, lot, and site isolation record.
- `non_conformance`: defect class, severity, root cause, and exception state.
- `quality_capa`: corrective and preventive action evidence.
- `quality_release`: approved release or disposition evidence.
- `calibration_asset`: gauges, tools, and metrology asset identity.
- `calibration_schedule`: due-date, window, and completion status for calibration.
- `procedure_revision`: controlled inspection or calibration procedure revision.
- `supplier_quality_profile`: supplier quality score, PPM, and audit state.
- `supplier_quality_incident`: supplier defect or escape evidence.
- `customer_quality_case`: customer complaint or field-quality case.
- `audit_evidence_packet`: disclosure-minimized audit proof package.
- `quality_rule`: compiled runtime rule evidence.
- `quality_parameter`: bounded numeric runtime parameter.
- `quality_configuration`: backend, topic, retry, and runtime installation state.
- `quality_compliance_package`: package-level compliance and release package.
- `quality_seed_data`: seeded quality vocabularies and lookup values.
- `quality_governed_model`: governed model registration and drift evidence.
- `quality_control_assertion`: continuous control proof.
- `quality_schema_extension`: package-local schema extension catalog.
- `quality_assurance_appgen_outbox_event`: emitted AppGen-X event evidence.
- `quality_assurance_appgen_inbox_event`: consumed AppGen-X event evidence.
- `quality_assurance_dead_letter_event`: exhausted retry and dead-letter evidence.

Supported ordinary backends are PostgreSQL, MySQL, and MariaDB only.

## Standard Capabilities

The package implements:

- Inspection plan authoring, revisioning, and release.
- Sampling schemes for fixed, percentage, and risk-informed inspection.
- Lot and batch quality traceability.
- Inspection test and measurement definitions.
- Inspection result recording with measurement series and SPC evidence.
- Quality holds and hold release.
- Nonconformance capture, disposition, and CAPA evidence.
- Release evidence and compliance package generation.
- Calibration asset and calibration schedule metadata.
- Controlled procedure revision metadata.
- Supplier quality and customer quality case evidence.
- Audit packets, rules, parameters, configuration, seed data, and workbench views.
- Idempotent AppGen-X inbox, outbox, retry, and dead-letter handling.

## Advanced Capabilities

The runtime proves deterministic evidence for:

- Event-sourced quality lifecycle and immutable audit history.
- Graph-relational quality topology across plans, tests, results, holds, CAPA,
  releases, suppliers, customers, and audit packets.
- Multi-tenant isolation and schema evolution.
- Probabilistic defect, escape, and compliance risk scoring.
- SPC analytics and defect forecasting.
- Counterfactual sampling simulation and autonomous exception recommendations.
- Semantic inspection instruction parsing.
- Self-healing route selection across API and outbox rails.
- Zero-knowledge quality proof generation.
- Dynamic policy screening and automated control testing.
- Universal API and AppGen-X event contracts.
- Cross-system federation across production, inventory, procurement, and audit.
- Decentralized lot identity verification.
- Resilience drills, crypto agility, carbon-aware scheduling, optimization,
  allocation, anomaly detection, stochastic exposure modeling, and governed
  model evidence.

## Rules, Parameters, and Configuration

`quality_assurance_configure_runtime()` accepts only:

- `database_backend`
- `event_topic`
- `retry_limit`
- `allowed_sites`
- `allowed_inspection_sources`
- `allowed_hold_reasons`
- `allowed_dispositions`
- `default_timezone`
- `workbench_limit`

The runtime event topic is fixed to `appgen.quality.events`, the event contract
is fixed to `AppGen-X`, and no stream-engine or user-selectable eventing picker
is exposed.

`quality_assurance_set_parameter()` supports package-local numeric parameters:

- `default_sample_size`
- `defect_threshold`
- `cpk_minimum`
- `hold_severity_threshold`
- `capa_due_days`
- `retention_days`
- `release_approval_threshold`

`quality_assurance_register_rule()` requires deterministic rule compile inputs:

- `rule_id`
- `tenant`
- `rule_type`
- `eligible_sources`
- `allowed_sites`
- `sampling_methods`
- `required_measurements`
- `critical_defect_classes`
- `release_dispositions`
- `status`

Rule registration emits normalized compile evidence and a stable compiled hash.
Schema extensions remain package-local and may target only Quality Assurance
owned tables.

## APIs and Dependencies

Package-local API descriptors cover:

- `PUT /quality/configuration`
- `POST /quality/parameters`
- `POST /quality/rules`
- `POST /quality/schema-extensions`
- `POST /quality/inspection-plans`
- `POST /quality/inspection-results`
- `POST /quality/holds`
- `POST /quality/non-conformances`
- `POST /quality/non-conformances/{id}/disposition`
- `POST /quality/holds/{id}/release`
- `POST /quality/events/inbox`
- `GET /quality/workbench`
- `GET /quality/schema-contract`
- `GET /quality/service-contract`
- `GET /quality/release-evidence`
- `GET /quality/ui-binding`

Declared external dependencies are APIs, events, and projections only:

- APIs: `GET /production/orders/{id}`, `GET /inventory/lots/{id}`,
  `GET /procurement/suppliers/{id}/quality-score`, `GET /returns/cases/{id}`,
  `GET /maintenance/assets/{id}`, `GET /crm/customers/{id}/quality-profile`,
  `POST /audit/quality-events`
- Projections: `production_completion_projection`,
  `goods_receipt_projection`, `inventory_lot_projection`,
  `supplier_score_projection`
- Consumed events: `ProductionCompleted`, `GoodsReceiptPosted`,
  `InventoryLotMoved`, `SupplierScoreChanged`

## Events and Handlers

Emitted AppGen-X events:

- `InspectionPlanCreated`
- `InspectionResultRecorded`
- `QualityHoldCreated`
- `NonConformanceRaised`
- `NonConformanceDispositioned`
- `QualityHoldReleased`

Consumed AppGen-X events:

- `ProductionCompleted`
- `GoodsReceiptPosted`
- `InventoryLotMoved`
- `SupplierScoreChanged`

`quality_assurance_receive_event()` records inbox evidence, enforces
idempotency by event id or idempotency key, updates package-local projections,
records retry evidence for failed or unsupported events, and writes exhausted
events to dead-letter evidence.

## Schema, Service, UI, and Release Contracts

The package exposes executable contract builders:

- `quality_assurance_build_schema_contract()`
- `quality_assurance_build_service_contract()`
- `quality_assurance_build_release_evidence()`
- `quality_assurance_ui_binding_contract()`

`quality_assurance_build_schema_contract()` proves:

- owned tables and runtime tables
- relationship metadata
- migration descriptors
- model descriptors
- backend allowlist
- no shared-table access

`quality_assurance_build_service_contract()` proves:

- command and query methods for standard QA operations and advanced analytics
- transaction boundary as the Quality Assurance owned datastore plus AppGen-X
  outbox
- idempotent inbox handling
- retry and dead-letter evidence surfaces
- declared external dependencies

`quality_assurance_ui_binding_contract()` proves:

- workbench route
- owned table binding
- runtime inbox/outbox/dead-letter binding
- shared-table isolation

`implementation_contract()` publishes runtime, UI, API, schema, service,
release-evidence, permissions, boundary, topic, emitted events, consumed
events, and package-local UI-binding evidence.

## Permissions and Workbench

The permission contract covers read, inspect, hold, disposition, configure,
audit, and event actions. Audit permissions also gate schema, service, release,
and UI-binding evidence queries.

The workbench exposes plans, sampling, results, SPC, holds, nonconformances,
CAPA, calibration, procedures, supplier quality, customer quality, audit
evidence, rules, parameters, configuration, and release evidence surfaces. UI
binding evidence must show owned tables, runtime tables, RBAC mappings, event
topic lock, and dead-letter visibility.

## Release Readiness

Completion requires:

- `quality_assurance_runtime_smoke()` returns `ok`.
- `implementation_contract()` exposes schema, service, release-evidence, and
  UI-binding contracts in addition to runtime, UI, API, permissions, topic, and
  boundary metadata.
- `quality_assurance_build_schema_contract()` covers all owned tables with one
  migration descriptor and one model descriptor each.
- `quality_assurance_build_service_contract()` covers standard commands,
  advanced query capabilities, idempotent inbox handling, and retry/dead-letter
  evidence.
- `quality_assurance_build_release_evidence()` proves schema depth, service
  depth, fixed AppGen-X contract, permission coverage, UI binding evidence, and
  duplicate plus dead-letter control evidence.
- Focused Quality Assurance tests pass.
