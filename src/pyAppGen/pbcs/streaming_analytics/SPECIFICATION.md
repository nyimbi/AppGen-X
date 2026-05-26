# Streaming Analytics PBC

`streaming_analytics` is the AppGen-X packaged business capability for
operational metric streams, KPI snapshots, dashboard projections, replayable
analytics evidence, and real-time business telemetry. It is a complete PBC with
owned schema, configuration, parameters, rules, service commands, API contracts,
AppGen-X events, idempotent handlers, UI fragments, tests, and release evidence.

## Stable Identity

- PBC key: `streaming_analytics`.
- Mesh: `intelligence`.
- Package directory: `src/pyAppGen/pbcs/streaming_analytics`.
- Runtime entrypoint: `streaming_analytics_runtime_capabilities()`.
- UI entrypoint: `streaming_analytics_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Default datastore: `streaming_analytics_store`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: AppGen-X outbox/inbox events only.
- User-facing stream-engine selector: forbidden and hidden.

## Generated Schema

`streaming_analytics_build_schema_contract()` is the package-local generated
schema artifact for this PBC. It declares the owned datastore boundary, runtime
AppGen-X tables, migrations, generated model artifacts, relationship edges, and
the PostgreSQL/MySQL/MariaDB backend allowlist.

## Owned Datastore Boundary

The PBC owns exactly these tables:

- `metric_stream`: stream definitions, tenant, event type, metric field,
  aggregation function, region, status, and compiled definition hash.
- `aggregation_window`: stream-bound window definitions, tenant, duration,
  state, and compiled window hash.
- `kpi_snapshot`: latest stream values, event counts, probabilistic confidence,
  cryptographic proof, and publication evidence.
- `dashboard_projection`: dashboard read models, selected streams, latest KPI
  values, projection status, and audit proof.

The PBC does not read or write foreign tables. Cross-PBC dependencies are
declared as event or API dependencies:

- `audit_ledger.AuditEventSealed`.
- `dom.OrderShipped`.
- `payment_orchestration.PaymentCaptured`.
- `POST /metric-streams`.
- `GET /kpis`.
- `GET /projections`.

The runtime boundary verifier accepts owned tables, AppGen-X local event tables,
and declared dependencies. It rejects direct foreign table references such as
payment, order, or audit tables.

## Standard Table-Stakes Capabilities

The implementation covers the expected operational analytics surface:

- Metric stream registration by tenant, event type, field, aggregation, region,
  and status.
- Window definition for each stream with explicit window duration and lifecycle
  state.
- Direct metric-event ingestion with tenant, event type, region, values,
  quality score, and audit proof.
- Idempotent event consumption for `AuditEventSealed`, `OrderShipped`, and
  `PaymentCaptured`.
- KPI snapshot recomputation for count, sum, average, and max aggregations.
- Dashboard projection creation with selected stream IDs and latest KPI values.
- AppGen-X outbox emission of `OperationalKpiChanged` and `ForecastUpdated`.
- AppGen-X inbox records for consumed events.
- Retry and dead-letter evidence for handler failure simulation.
- Late-event, replay, watermark, retention, and quality gate parameters.
- Configuration schema for database backend, event topic, retry limit,
  timezone, supported event types, supported regions, retention days, watermark
  seconds, aggregation mode, and workbench limit.
- Parameter engine with bounded values for default window minutes, late-event
  tolerance, quality threshold, forecast horizon, alert multiplier, replay batch
  size, KPI confidence threshold, projection refresh seconds, max events per
  window, and workbench limit.
- Rule engine with tenant scope, allowed event types, allowed regions, quality
  policy, aggregation policy, alert policy, status, and compiled hash.
- Schema extension for owned tables only.
- RBAC descriptors for administrators, operators, and auditors.
- API contract descriptors for stream creation, window creation, metric-event
  ingestion, KPI queries, and projection queries.
- Workbench views and UI fragments for streams, events, aggregation windows,
  KPI snapshots, projections, replay, quality, rules, parameters,
  configuration, outbox, and dead-letter review.
- Seed data for supported event-type and aggregation families.

## Advanced Capabilities

The runtime exposes evidence for:

- Event-sourced metric lifecycle with append-only state events.
- Owned analytics schema boundary with explicit rejection of foreign tables.
- Multi-tenant metric isolation.
- Schema-evolution-resilient metric context.
- Real-time event ingestion and windowed aggregation.
- KPI snapshot publication with cryptographic proofs.
- Dashboard projection management.
- Late-event handling and replay controls.
- Data-quality gatekeeping.
- Probabilistic KPI confidence scoring.
- Counterfactual metric threshold simulation through alert and quality
  parameters.
- Temporal KPI forecasting through forecast horizon and forecast events.
- Autonomous metric exception resolution through retry/dead-letter records.
- Semantic metric-definition understanding through structured stream/rule
  envelopes.
- Predictive operational risk evidence through confidence and quality scoring.
- Self-healing window recomputation on each relevant event.
- Immutable metric audit trail through hashed state events and snapshot proofs.
- Dynamic metric policy screening through allowed event types, regions, and
  tenant-scoped rules.
- Automated KPI control testing through runtime smoke and focused unit tests.
- Cross-system audit, order, and payment federation by declared event
  dependencies only.
- AppGen-X outbox/inbox eventing.
- Idempotent handlers and duplicate-event detection.
- Retry/dead-letter evidence.
- Permissions governance evidence.
- Governed model evidence for KPI confidence and forecasting.

## Service Layer

`streaming_analytics_build_service_contract()` is the package-local service
artifact for this PBC. It declares the generated command/query surface, route
artifacts, AppGen-X event and handler artifacts, permissions, configuration,
idempotent handler requirements, retry/dead-letter evidence, and UI fragment
artifacts.

The service layer exposes these package-local operations:

- `configure_runtime(configuration)`.
- `set_parameter(name, value)`.
- `register_rule(rule)`.
- `register_schema_extension(table, fields)`.
- `register_metric_stream(command)`.
- `define_window(command)`.
- `receive_event(event, simulate_failure=False)`.
- `ingest_metric_event(command)`.
- `create_dashboard_projection(command)`.
- `build_api_contract()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references=...)`.

All operations are side-effect-free state transitions and are safe for generated
application embedding.

## APIs

The API contract exposes:

- `POST /metric-streams` for `register_metric_stream`, writing
  `metric_stream`, requiring `streaming_analytics.stream.write`.
- `POST /aggregation-windows` for `define_window`, writing
  `aggregation_window`, requiring `streaming_analytics.window.write`.
- `POST /metric-events` for `ingest_metric_event`, recomputing
  `kpi_snapshot`, emitting `OperationalKpiChanged` and `ForecastUpdated`, and
  requiring `streaming_analytics.event.write`.
- `GET /kpis` for KPI snapshot queries, requiring `streaming_analytics.audit`.
- `GET /projections` for dashboard projection queries, requiring
  `streaming_analytics.audit`.

The catalog-declared route set remains `POST /metric-streams`, `GET /kpis`,
and `GET /projections`; the package-local API contract includes the additional
internal routes needed to fully exercise the runtime commands.

## Events And Handlers

Consumed events:

- `AuditEventSealed` maps to audit metric events.
- `OrderShipped` maps to order metric events.
- `PaymentCaptured` maps to payment metric events.

Emitted events:

- `OperationalKpiChanged`.
- `ForecastUpdated`.

Handlers require event IDs, reject unsupported event types, use deterministic
idempotency keys, ignore duplicates, write AppGen-X inbox records, and create
dead-letter evidence when failure is simulated. Outbox events include tenant,
payload, AppGen-X contract marker, retry policy, dead-letter target, and audit
hash.

## UI And Workbench

The workbench exposes:

- Metric stream registry.
- Metric event monitor.
- Aggregation window designer.
- KPI snapshot board.
- Dashboard projection builder.
- Replay console.
- Quality panel.
- Rule studio.
- Parameter console.
- Configuration panel.
- Event outbox.
- Dead-letter queue.

The renderer uses RBAC permissions to compute visible and locked actions. The
configuration editor allows only PostgreSQL, MySQL, and MariaDB and never
exposes a stream-engine picker.

## Release Evidence

`streaming_analytics_build_release_evidence()` aggregates the package-local
schema, service, API, permissions, AppGen-X runtime control evidence, and
generated artifact coverage into one release-ready contract.

Focused tests prove:

- Runtime capabilities and smoke checks pass.
- Configuration, parameters, rules, schema extensions, stream registration,
  window definition, event consumption, direct metric ingestion, KPI
  recomputation, dashboard projections, and workbench rendering execute.
- API and permissions contracts expose routes, roles, policy controls, and
  no shared-table access.
- Owned-boundary validation accepts owned tables and declared dependencies and
  rejects foreign tables.
- Invalid database backends, invalid parameters, non-owned schema extensions,
  unsupported events, and simulated handler failures are rejected or
  dead-lettered.
- The PBC participates in the all-PBC implementation release audit and
  all-built-in generation smoke audit.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `streaming_analytics`
- Mesh: `intelligence`
- Datastore backend: `None`

### Owned Tables

- `metric_stream`
- `aggregation_window`
- `kpi_snapshot`
- `dashboard_projection`

### API Routes

- `POST /metric-streams`
- `GET /kpis`
- `GET /projections`

### Emitted Events

- `ForecastUpdated`
- `OperationalKpiChanged`

### Consumed Events

- `AuditEventSealed`
- `OrderShipped`
- `PaymentCaptured`

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
