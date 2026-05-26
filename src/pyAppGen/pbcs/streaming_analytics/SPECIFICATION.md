# Streaming Analytics PBC

`streaming_analytics` owns metric streams, ingested metric events, aggregation windows, KPI snapshots, dashboard projections, replay evidence, and real-time operational analytics governance for AppGen-X generated applications.

## Owned Boundary

- Owned tables: `metric_stream`, `aggregation_window`, `kpi_snapshot`, `dashboard_projection`.
- Integration boundary: declared APIs, AppGen-X outbox/inbox events, and projections only.
- Datastore backends: PostgreSQL, MySQL, or MariaDB.
- Eventing: AppGen-X event contract on `appgen.streaming_analytics.events`; no user-facing stream-engine selection.

## Standard Capabilities

- Metric stream definition, metric event ingestion, aggregation windows, KPI snapshots, and dashboard projections.
- Threshold alerts, late-event handling, replay evidence, quality checks, retention policy, and dashboard refresh controls.
- Idempotent consumption of `AuditEventSealed`, `OrderShipped`, and `PaymentCaptured`.
- Emission of `ForecastUpdated` and `OperationalKpiChanged` through the AppGen-X outbox.
- Retry/dead-letter evidence, RBAC descriptors, configuration schema, parameter engine, rule engine, seed data, and workbench views.

## Advanced Capabilities

- Event-sourced metric lifecycle and immutable metric audit trail.
- Probabilistic KPI confidence, predictive operational risk, and temporal KPI forecasting.
- Counterfactual threshold simulation and autonomous metric exception resolution.
- Semantic metric-definition understanding and self-healing window recomputation.
- Dynamic metric policy screening, automated KPI control testing, and cryptographic KPI snapshot proofs.
- Cross-system audit, order, and payment federation through declared APIs/events only.

## UI

The workbench exposes metric stream registry, event monitor, aggregation window designer, KPI snapshot board, dashboard projection builder, replay console, quality panel, rule studio, parameter console, configuration panel, outbox, and dead-letter queue fragments.
