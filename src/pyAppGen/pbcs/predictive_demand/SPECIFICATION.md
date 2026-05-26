# Predictive Demand PBC

`predictive_demand` owns forecast models, forecast runs, demand signals, forecast results, shortage evidence, and demand-planning workbench logic for AppGen-X generated applications.

## Owned Boundary

- Owned tables: `forecast_model`, `forecast_run`, `demand_signal`, `forecast_result`.
- Integration boundary: declared APIs, AppGen-X outbox/inbox events, and projections only.
- Datastore backends: PostgreSQL, MySQL, or MariaDB.
- Eventing: AppGen-X event contract on `appgen.predictive_demand.events`; no user-facing stream-engine selection.

## Standard Capabilities

- Forecast model registration with governed algorithm/version metadata.
- Demand signal ingestion for shipments, operational KPIs, inventory pools, manual overrides, and promotion signals.
- Forecast run orchestration, result publication, consensus planning controls, and planner override capture.
- Service-level targets, safety-stock guidance, inventory coverage checks, and material-shortage detection.
- Idempotent consumption of `OperationalKpiChanged`, `OrderShipped`, and `InventoryPoolChanged`.
- Emission of `ForecastUpdated` and `MaterialShortageDetected` through the AppGen-X outbox.
- Retry/dead-letter evidence, RBAC descriptors, configuration schema, parameter engine, rule engine, seed data, and workbench views.

## Advanced Capabilities

- Event-sourced demand-signal lifecycle and immutable planning audit trail.
- Probabilistic forecast bands, causal-driver weighting, promotion-lift handling, and temporal replenishment forecasting.
- Counterfactual scenario simulation, autonomous forecast exception resolution, semantic planning-rule understanding, and governed model evidence.
- Predictive material-constraint risk, self-healing retraining cadence controls, cryptographic forecast proofs, and automated planning control testing.
- Cross-system order, inventory, and operational-federation evidence through declared APIs/events only.

## UI

The workbench exposes forecast model registry, demand signal console, forecast run planner, forecast result board, consensus planning studio, shortage risk panel, inventory coverage panel, scenario simulation lab, rule studio, parameter console, configuration panel, outbox, and dead-letter queue fragments.
