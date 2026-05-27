# Predictive Demand PBC

`predictive_demand` is the AppGen-X packaged business capability for demand
planning, forecast modeling, inventory coverage analysis, shortage detection,
consensus planning, and governed demand-intelligence workbenches. It is a
complete package-local implementation with owned schema, runtime services, API
descriptors, AppGen-X events, handlers, rules, parameters, configuration, UI
fragments, package metadata, tests, and release-audit evidence.

## Stable Identity

- PBC key: `predictive_demand`.
- Mesh: intelligence.
- Package directory: `src/pyAppGen/pbcs/predictive_demand`.
- Runtime entrypoint: `predictive_demand_runtime_capabilities()`.
- UI entrypoint: `predictive_demand_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X event contract on
  `appgen.predictive_demand.events`.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

The package owns exactly these operational tables:

- `forecast_model`: tenant, SKU, location, algorithm, version, status,
  governance state, compiled hash, and model-registration evidence.
- `forecast_run`: model reference, tenant, SKU, location, horizon, signal set,
  baseline quantity, forecast quantity, inventory coverage, shortage quantity,
  confidence, service-level target, initiator, status, and audit proof.
- `demand_signal`: tenant, signal type, SKU, location, region, quantity,
  signal date, source, payload, driver weight, and signal audit proof.
- `forecast_result`: published forecast, confidence band, recommended supply,
  shortage quantity, planning action, model/run references, and audit proof.
- `planning_horizon`, `forecast_driver`, `consensus_adjustment`,
  `scenario_version`, `shortage_risk`, `replenishment_recommendation`,
  `forecast_exception`, `model_drift_signal`, `planning_rule`,
  `planning_parameter`, `governed_model_evidence`, and
  `forecast_audit_proof`: complete planning governance, causal-driver,
  scenario, shortage, replenishment, exception, drift, rule, parameter,
  model-evidence, and cryptographic audit surfaces.

The PBC does not read or write shared order, inventory, KPI, material, planning,
or finance tables. External information arrives through declared AppGen-X events
or API projections only:

- Consumed events: `OperationalKpiChanged`, `OrderShipped`, and
  `InventoryPoolChanged`.
- API projections: `shipment_projection`, `inventory_pool_projection`, and
  `operational_kpi_projection`.
- Runtime event tables are PBC-local:
  `predictive_demand_appgen_outbox_event`,
  `predictive_demand_appgen_inbox_event`, and
  `predictive_demand_dead_letter_event`.

The owned-boundary verifier accepts only owned tables, declared APIs/events,
declared projections, and PBC-local event tables. It rejects direct references
such as `inventory_pool`.

## Generated Schema

`predictive_demand_build_schema_contract()` is the package-local generated
schema descriptor for Predictive Demand. It publishes:

- Owned tables: `forecast_model`, `forecast_run`, `demand_signal`,
  `forecast_result`, `planning_horizon`, `forecast_driver`,
  `consensus_adjustment`, `scenario_version`, `shortage_risk`,
  `replenishment_recommendation`, `forecast_exception`,
  `model_drift_signal`, `planning_rule`, `planning_parameter`,
  `governed_model_evidence`, and `forecast_audit_proof`.
- Runtime AppGen-X event tables:
  `predictive_demand_appgen_outbox_event`,
  `predictive_demand_appgen_inbox_event`, and
  `predictive_demand_dead_letter_event`.
- Generated migration artifacts in
  `pbcs/predictive_demand/migrations/001_initial.sql` for every owned
  planning table and AppGen-X event table.
- Generated model artifacts under
  `pyAppGen.pbcs.predictive_demand.models.*`.
- Owned-table relationships from `forecast_run.model_id` to
  `forecast_model.model_id` and from `forecast_result.run_id` to
  `forecast_run.run_id`.
- Backend allowlist fixed to PostgreSQL, MySQL, and MariaDB.
- Schema extensions limited to owned tables through
  `register_schema_extension`.

## Standard Table-Stakes Capabilities

The implementation covers the ordinary demand-planning capabilities expected
from a production planning package:

- Forecast model registration with algorithm whitelist, versioning, approval
  state, tenant/SKU/location scope, and compiled governance evidence.
- Runtime configuration for database backend, event topic, retry limit,
  default unit of measure, supported regions, supported signal types, planning
  granularity, timezone, shortage policy, and workbench limit.
- Numeric parameter engine for forecast horizon, history window, service level,
  promotion lift, causal weighting, anomaly threshold, retraining cadence,
  shortage alert window, bias tolerance, and workbench limit.
- Rule engine for tenant, scope, allowed signal types, allowed regions,
  consensus controls, forecast policy, shortage policy, status, compiled hash,
  and policy-engine evidence.
- Schema extension for owned planning tables only, with versioned migration
  evidence.
- Demand signal ingestion for shipments, inventory pools, operational KPIs,
  manual overrides, and promotion signals.
- Idempotent AppGen-X handlers for `OrderShipped`, `OperationalKpiChanged`,
  and `InventoryPoolChanged`.
- Forecast run orchestration that derives baseline demand, daily rate,
  algorithm multipliers, causal pressure, service-level safety stock, inventory
  coverage, shortage quantity, and confidence.
- Forecast result publication with probabilistic confidence bands,
  recommended supply, planning action, and outbox events.
- Planning horizon, causal driver, consensus adjustment, scenario version,
  shortage risk, replenishment recommendation, forecast exception, model drift,
  governed model evidence, and audit proof records are executable command
  surfaces, not only schema declarations.
- Material-shortage detection and emission of `MaterialShortageDetected`.
- Forecast update emission through `ForecastUpdated`.
- Retry/dead-letter evidence for failed consumed-event handling.
- Workbench views for models, signals, runs, results, inventory coverage,
  shortage counts, rules, parameters, configuration, outbox, and dead letters.
- UI fragments for model registry, signal console, run planner, result board,
  consensus studio, shortage risk, inventory coverage, scenario lab, rule
  studio, parameter console, configuration panel, outbox, and dead-letter queue.
- Permission/RBAC descriptors for model, signal, run, result, event,
  configuration, and audit actions.
- Seed data for supported algorithms and signal types.

## Advanced Capabilities

The executable runtime proves the advanced capabilities needed for an
intelligence-grade planning PBC:

- Event-sourced demand signal lifecycle with immutable state-event hashes.
- Owned planning schema boundary enforcement with explicit violation evidence.
- Multi-tenant planning isolation in models, signals, runs, results, and UI
  views.
- Schema-evolution-safe forecast and demand context extensions.
- Governed model registry with algorithm controls and version evidence.
- Event-driven signal projection from orders, inventory, and operational KPIs.
- Probabilistic forecast banding and confidence-aware planning actions.
- Causal-driver modeling using operational signal weights.
- Promotion and planner-override adjustments.
- Temporal replenishment forecasting through configurable horizon and history
  windows.
- Counterfactual planning support through deterministic forecast previews.
- Consensus demand-planning controls and planner override constraints.
- Service-level target and safety-stock guidance.
- Predictive material-constraint risk through shortage quantities and alert
  windows.
- Self-healing retraining cadence controls.
- Cryptographic forecast proofs for models, signals, runs, results, and state
  events.
- Immutable planning audit trail.
- Dynamic policy screening through compiled rules and parameters.
- Automated forecast control testing via smoke checks and release audits.
- Cross-system order, inventory, and operations federation through declared
  APIs/events only.
- AppGen-X outbox/inbox eventing with idempotent handlers.
- Retry/dead-letter evidence.
- Permissions governance evidence.
- Configuration, rule, parameter, seed-data, and workbench evidence.
- Governed model evidence.
- First-class planning table-stakes evidence for every declared planning table:
  horizons, drivers, consensus, scenarios, shortage risk, replenishment,
  exceptions, drift signals, governed model evidence, and sealed audit proofs.

## Service Layer

`predictive_demand_build_service_contract()` is the package-local generated
service descriptor. The service layer exposes these package-local commands:

- `configure_runtime(configuration)`.
- `set_parameter(name, value)`.
- `register_rule(rule)`.
- `register_schema_extension(table, fields)`.
- `register_forecast_model(command)`.
- `receive_event(event, simulate_failure=False)`.
- `ingest_demand_signal(command)`.
- `create_forecast_run(command)`.
- `publish_forecast_result(command)`.
- `register_planning_horizon(command)`.
- `register_forecast_driver(command)`.
- `record_consensus_adjustment(command)`.
- `create_scenario_version(command)`.
- `assess_shortage_risk(command)`.
- `prepare_replenishment_recommendation(command)`.
- `open_forecast_exception(command)`.
- `resolve_forecast_exception(command)`.
- `record_model_drift_signal(command)`.
- `register_governed_model_evidence(command)`.
- `seal_forecast_audit_proof(command)`.
- `build_api_contract()`.
- `build_schema_contract()`.
- `build_service_contract()`.
- `build_release_evidence()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references=...)`.

All commands are deterministic and side-effect-free: they accept explicit state
and return a new state plus evidence payloads suitable for generated apps and
release smoke audits.

The generated service contract also records:

- Fixed AppGen-X eventing on `appgen.predictive_demand.events`.
- Runtime outbox, inbox, and dead-letter tables owned by this PBC.
- Idempotent consumed-event handling through `receive_event`.
- Retry/dead-letter evidence driven by `retry_limit`.
- Generated service, route, event, and handler artifacts derived from the
  package-local runtime.

## APIs

The package-local API contract exposes route descriptors, not just route names:

- `POST /forecast-models` runs `register_forecast_model`, writes
  `forecast_model`, requires `predictive_demand.model.write`, and is
  idempotent by `model_id`.
- `POST /forecast-runs` runs `create_forecast_run`, writes `forecast_run`,
  requires `predictive_demand.run.write`, and is idempotent by `run_id`.
- `POST /demand-signals` runs `ingest_demand_signal`, writes `demand_signal`,
  requires `predictive_demand.signal.write`, and is idempotent by `signal_id`.
- `POST /forecast-results` runs `publish_forecast_result`, writes
  `forecast_result`, requires `predictive_demand.result.write`, and emits
  `ForecastUpdated` and `MaterialShortageDetected`.
- `POST /planning-horizons`, `POST /forecast-drivers`,
  `POST /consensus-adjustments`, `POST /scenario-versions`,
  `POST /shortage-risks`, `POST /replenishment-recommendations`,
  `POST /forecast-exceptions`, `POST /forecast-exceptions/resolve`,
  `POST /model-drift-signals`, `POST /governed-model-evidence`, and
  `POST /forecast-audit-proofs` persist the declared planning, exception,
  drift, governance, and audit-proof records.
- `POST /predictive-demand/events/inbox` runs `receive_event`, consumes the
  declared AppGen-X events, requires `predictive_demand.event.consume`, and is
  idempotent by `event_id`.
- `GET /forecast-results` queries `build_workbench_view`, reads only owned
  Predictive Demand state, and requires `predictive_demand.audit`.

The catalog-facing routes include `POST /forecast-models`,
`POST /forecast-runs`, `POST /demand-signals`, `POST /forecast-results`,
all planning table-stakes command routes, `POST /predictive-demand/events/inbox`,
and `GET /forecast-results`. Release-facing audit routes are package-local:

- `GET /predictive-demand/schema-contract`.
- `GET /predictive-demand/service-contract`.
- `GET /predictive-demand/release-evidence`.

## Events And Handlers

Consumed events:

- `OperationalKpiChanged`.
- `OrderShipped`.
- `InventoryPoolChanged`.

Emitted events:

- `ForecastUpdated`.
- `MaterialShortageDetected`.

Handlers require event IDs, deduplicate already handled messages, record inbox
evidence, translate events into owned demand signals, and send simulated
failures to the dead-letter evidence queue. Users never choose a stream engine.

## UI And Workbench

The UI contract exposes:

- `PredictiveDemandWorkbench`.
- `ForecastModelRegistry`.
- `DemandSignalConsole`.
- `ForecastRunPlanner`.
- `ForecastResultBoard`.
- `ConsensusPlanningStudio`.
- `ShortageRiskPanel`.
- `InventoryCoveragePanel`.
- `ScenarioSimulationLab`.
- `DemandRuleStudio`.
- `DemandParameterConsole`.
- `DemandConfigurationPanel`.
- `DemandEventOutbox`.
- `DemandDeadLetterQueue`.

Rendered workbench output includes tenant-filtered counts, visible/locked
actions from RBAC permissions, owned-table binding evidence, configuration
state, rules, parameters, outbox counts, and dead-letter counts.

## Release Evidence

`predictive_demand_build_release_evidence()` aggregates generated schema,
service, API, permissions, UI, and control evidence for release audits.

Focused tests prove:

- Runtime capability and smoke checks cover every advanced capability key.
- Configuration, rule, parameter, schema-extension, event handling, model
  registration, signal ingestion, forecast run creation, forecast publication,
  shortage detection, outbox emission, UI rendering, API descriptors, RBAC
  descriptors, and workbench evidence execute.
- AppGen-X eventing is fixed and stream-engine picker exposure is false.
- Backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Boundary validation accepts owned tables and declared dependencies and
  rejects direct foreign table references.
- Generated migration, model, service, route, event, handler, and UI artifacts
  are present and aligned with the package-local contract builders.
- Idempotent handlers, retry evidence, and dead-letter evidence are present for
  AppGen-X consumed events.
- Invalid database backends, invalid parameters, non-owned schema extensions,
  and simulated handler failures are rejected or dead-lettered.
- The package participates in all-PBC implementation release and generation
  smoke audits.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `predictive_demand`
- Mesh: `intelligence`
- Datastore backend: `None`

### Owned Tables

- `forecast_model`
- `forecast_run`
- `demand_signal`
- `forecast_result`
- `planning_horizon`
- `forecast_driver`
- `consensus_adjustment`
- `scenario_version`
- `shortage_risk`
- `replenishment_recommendation`
- `forecast_exception`
- `model_drift_signal`
- `planning_rule`
- `planning_parameter`
- `governed_model_evidence`
- `forecast_audit_proof`

### API Routes

- `POST /forecast-models`
- `POST /forecast-runs`
- `POST /demand-signals`
- `POST /forecast-results`
- `POST /planning-horizons`
- `POST /forecast-drivers`
- `POST /consensus-adjustments`
- `POST /scenario-versions`
- `POST /shortage-risks`
- `POST /replenishment-recommendations`
- `POST /forecast-exceptions`
- `POST /forecast-exceptions/resolve`
- `POST /model-drift-signals`
- `POST /governed-model-evidence`
- `POST /forecast-audit-proofs`
- `POST /predictive-demand/events/inbox`
- `GET /forecast-results`
- `GET /predictive-demand/schema-contract`
- `GET /predictive-demand/service-contract`
- `GET /predictive-demand/release-evidence`

### Emitted Events

- `ForecastUpdated`
- `MaterialShortageDetected`

### Consumed Events

- `OperationalKpiChanged`
- `OrderShipped`
- `InventoryPoolChanged`

### UI Fragments

- None declared

### Permissions

- None declared

### Configuration Keys

- None declared

### Standard Features

- None declared

### Advanced Capabilities

- None declared

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->
