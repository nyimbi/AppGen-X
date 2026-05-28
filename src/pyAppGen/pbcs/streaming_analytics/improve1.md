# Streaming Analytics PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `streaming_analytics`. Each improvement is specific to real-time metric ingestion, event-time processing, aggregation windows, KPI snapshots, dashboard projections, replay, watermarks, quality gates, alerts, forecasting, operational risk scoring, metric governance, and telemetry operations so the PBC can move toward complete specialist-grade domain coverage.

## Current Domain Evidence Used

- Domain scope: operational metric streams, metric events, aggregation windows, KPI snapshots, dashboard projections, ingestion checkpoints, data quality results, replay jobs, watermarks, retention policies, threshold alerts, metric forecasts, operational risk scores, metric exceptions, window recomputations, control assertions, snapshot proofs, policy screenings, audit entries, federation views, and governed analytics models.
- Owned analytics surface: `metric_stream`, `aggregation_window`, `kpi_snapshot`, `dashboard_projection`, `metric_event`, `ingestion_checkpoint`, `data_quality_result`, `replay_job`, `watermark_state`, `retention_policy`, `threshold_alert`, `metric_forecast`, `operational_risk_score`, `metric_exception`, `window_recomputation`, `kpi_control_assertion`, `kpi_snapshot_proof`, `metric_policy_screening`, `analytics_audit_entry`, `analytics_federation_view`, and `analytics_governed_model`.
- Declared operations: stream registration, window definition, event receipt, metric ingestion, dashboard projection creation, checkpoint recording, quality evaluation, replay job opening, watermark advancement, retention application, threshold alerts, metric forecasting, operational risk scoring, exception resolution, window recomputation, KPI controls, snapshot proofs, policy screening, federation views, governed model registration, workbench views, and owned-table boundary verification.
- Declared integrations: consumed `AuditEventSealed`, `OrderShipped`, and `PaymentCaptured` events plus emitted `OperationalKpiChanged` and `ForecastUpdated` through the AppGen-X event contract.
- Declared advanced posture: event-sourced metric lifecycle, real-time ingestion, windowed aggregation, late-event handling, replay controls, data-quality gatekeeping, probabilistic KPI confidence, temporal forecasting, self-healing recomputation, immutable audit trails, dynamic policy screening, governed models, idempotent handlers, retry/dead-letter evidence, UI fragments, rules, parameters, and release audits.

## 50 Better-Than-World-Class Improvements

### 1. Metric stream semantic contract registry

**Justification:** A metric stream is operationally useful only when its event type, metric field, aggregation semantics, dimensions, freshness expectation, and business meaning are unambiguous.

**Improvement:** Expand `metric_stream` into a versioned semantic contract with metric definition, unit, dimensional keys, allowed aggregations, owner, consumer list, freshness SLA, compatibility policy, deprecation state, and generated API documentation. Stream registration should reject ambiguous or incompatible metric definitions before ingestion begins.

### 2. Event-time processing model

**Justification:** Real-time analytics becomes misleading when processing-time arrival order is confused with event time, especially for delayed orders, payments, and audit events.

**Improvement:** Add event-time semantics to `metric_event`, `aggregation_window`, and `watermark_state`, including event timestamp, ingestion timestamp, processing timestamp, allowed lateness, time-zone normalization, and clock-skew evidence. KPI snapshots should expose whether values are final, provisional, corrected, or late-adjusted.

### 3. Window taxonomy and lifecycle governance

**Justification:** Tumbling, sliding, session, cumulative, business-calendar, and custom fiscal windows have different correctness and recomputation behavior.

**Improvement:** Extend `aggregation_window` with window type, alignment rule, duration, slide interval, session gap, calendar source, finalization policy, backfill policy, and lifecycle state. The UI should show window coverage, open windows, closed windows, late-adjusted windows, and recomputation eligibility.

### 4. High-cardinality dimension controls

**Justification:** Unbounded dimensions can explode storage, increase latency, create privacy leakage, and make dashboards unusable.

**Improvement:** Add dimension cardinality policies with allowed keys, maximum distinct count, top-k retention, bucketing, suppression, privacy thresholds, and exception workflows. Data quality checks should quarantine streams that exceed dimensional limits.

### 5. Metric event identity and idempotency ledger

**Justification:** Duplicate, retried, corrected, and replayed events can corrupt aggregates unless identity and supersession are explicit.

**Improvement:** Add metric-event identity fields for source event ID, AppGen-X event ID, business key, sequence number, correction marker, superseded event ID, deduplication hash, and idempotency result. Workbench views should explain exactly why an event was accepted, ignored, corrected, or dead-lettered.

### 6. Ingestion backpressure and overload policy

**Justification:** Analytics systems must degrade predictably under event bursts rather than silently dropping events or producing stale dashboards.

**Improvement:** Add overload state, queue depth, ingestion lag, throttling policy, priority class, shedding strategy, and recovery evidence to `ingestion_checkpoint`. Operators should see which streams are lagging, which tenants are throttled, and which KPIs are stale because of backpressure.

### 7. Source freshness and completeness scoring

**Justification:** KPI confidence depends on whether all expected event sources have reported within their freshness windows.

**Improvement:** Add source completeness metrics by stream, tenant, event type, region, source system, and window. KPI snapshots should include expected source count, received source count, missing source list, freshness score, and confidence reduction when sources are stale.

### 8. Data quality rule library

**Justification:** Generic quality scores are insufficient for streaming metrics that need type checks, range checks, monotonicity, referential projections, unit consistency, and anomaly gates.

**Improvement:** Expand `data_quality_result` with rule type, evaluated field, expected range, observed value, severity, disposition, remediation owner, and effect on aggregates. The rule studio should let operators compose quality checks without exposing stream-engine choices.

### 9. Late event impact analysis

**Justification:** Late events may have no material effect, may change a dashboard, or may require downstream KPI republication.

**Improvement:** Add late-event impact calculation that identifies affected windows, snapshots, projections, alerts, forecasts, and emitted events. The UI should show whether the event will be ignored, applied prospectively, applied retroactively, or require controlled replay.

### 10. Watermark drift diagnostics

**Justification:** Watermarks can stall or move too aggressively, causing incorrect finality or unbounded provisional state.

**Improvement:** Extend `watermark_state` with source-specific watermark lag, drift reason, clock-skew estimate, stalled-source evidence, advancement policy, and override approvals. Operators should be able to diagnose why a stream cannot finalize windows.

### 11. Replay planning and dry-run simulation

**Justification:** Replay can repair analytics but can also duplicate alerts, overwrite dashboards, or alter historical evidence if not planned safely.

**Improvement:** Extend `replay_job` with source range, target windows, expected event count, dry-run delta, affected snapshots, alert suppression policy, emitted-event strategy, and rollback evidence. Replay commands should require a preview before execution.

### 12. Deterministic recomputation proofs

**Justification:** Recomputed windows must be provably equivalent to replaying the accepted event history under a specific stream definition and rule version.

**Improvement:** Add recomputation proofs that hash input event IDs, stream contract version, window definition, quality rules, aggregation code version, and output snapshot. `window_recomputation` should expose deterministic equality or explain divergence.

### 13. KPI snapshot finality states

**Justification:** Dashboards need to distinguish provisional, late-adjusted, replayed, certified, and superseded KPI values.

**Improvement:** Extend `kpi_snapshot` with finality state, completeness score, supersession link, certification proof, late adjustment amount, replay marker, and publication policy. APIs should return finality metadata with every KPI value.

### 14. Metric lineage graph

**Justification:** Users need to trace a KPI from dashboard number back to stream, window, events, quality decisions, replay jobs, and policy screens.

**Improvement:** Add a lineage graph linking `dashboard_projection`, `kpi_snapshot`, `aggregation_window`, `metric_stream`, `metric_event`, `data_quality_result`, `watermark_state`, `replay_job`, and `kpi_snapshot_proof`. The workbench should support drill-down and evidence export for any KPI.

### 15. Dashboard projection dependency management

**Justification:** Dashboards can break or mislead when upstream streams change, retire, lag, or alter semantics.

**Improvement:** Extend `dashboard_projection` with stream dependencies, compatibility requirements, freshness SLA, projection owner, consumer impact, refresh policy, and change alerts. Stream contract changes should list every affected dashboard before activation.

### 16. Projection personalization and permission safety

**Justification:** Real-time dashboards often expose sensitive operational, payment, and audit metrics that should vary by role, tenant, region, and purpose.

**Improvement:** Add projection-level permission filters, aggregation thresholds, masked dimensions, tenant/region partitions, and purpose tags. The UI should prove that users see only authorized KPI slices and that suppressed values cannot be inferred through low-count breakdowns.

### 17. Alert fatigue and threshold governance

**Justification:** Threshold alerts lose value when thresholds are noisy, duplicated, unowned, or disconnected from action.

**Improvement:** Expand `threshold_alert` with threshold rationale, hysteresis, cooldown, suppression, escalation path, owner, action playbook, false-positive outcome, and alert quality score. Alert policies should be backtested before activation.

### 18. Dynamic baseline and seasonality-aware alerts

**Justification:** Static thresholds fail for seasonal, weekly, daily, promotional, or operational cycle patterns.

**Improvement:** Add dynamic baselines using historical window profiles, seasonality, daypart, region, tenant, event type, and calendar context. Alerts should explain whether a value is abnormal relative to the correct seasonal baseline, not just an absolute limit.

### 19. Metric anomaly triage workflow

**Justification:** Spikes, drops, missing events, duplicated sources, schema shifts, fraud patterns, and operational incidents require different responses.

**Improvement:** Add `metric_exception` categories for spike, drop, flatline, missing source, duplicate surge, quality failure, schema drift, threshold breach, forecast miss, and policy violation. Each exception should include owner, severity, evidence, remediation steps, and closure proof.

### 20. Operational risk scoring explainability

**Justification:** Risk scores based on metrics can drive urgent operational action and must be explainable and auditable.

**Improvement:** Extend `operational_risk_score` with contributing metrics, weights, baseline, trend, anomaly contribution, quality penalty, confidence, recommended action, and model evidence. UI should let users inspect why risk changed and what action is expected.

### 21. Metric forecast horizon governance

**Justification:** Forecasts over streaming metrics have different reliability at seconds, minutes, hours, days, and planning horizons.

**Improvement:** Extend `metric_forecast` with horizon type, model family, training window, forecast quantiles, calibration evidence, prediction interval, and validity limits. Forecast outputs should clearly mark when a horizon is too long for the selected stream.

### 22. Forecast-versus-actual backtesting

**Justification:** Forecasted KPIs and operational risks need continuous accuracy monitoring before users trust generated forecasts.

**Improvement:** Add backtests by stream, window, horizon, model version, tenant, and event type, with error metrics, bias, interval coverage, and drift evidence. Governed model records should fail release checks when forecast backtesting is missing.

### 23. Metric policy screening before publication

**Justification:** Some KPIs should not be published because of privacy, sensitivity, tenant, region, low-count, or policy restrictions.

**Improvement:** Expand `metric_policy_screening` with screening reason, matched rule, affected dimensions, publication decision, masking strategy, waiver workflow, and expiry. Dashboard and API publication should require policy screening for sensitive metrics.

### 24. Retention policy impact simulator

**Justification:** Retention changes can affect replay capability, audit reconstruction, forecasting, compliance, and storage cost.

**Improvement:** Add retention simulations that calculate affected streams, historical window coverage, replay loss, audit risk, forecast training impact, storage savings, and required approvals. Retention policies should not activate until impact is reviewed.

### 25. Privacy-safe low-count suppression

**Justification:** Real-time operational metrics can leak sensitive individual or customer information through small slices.

**Improvement:** Add low-count and rare-dimension suppression rules with configurable thresholds, aggregation fallback, noise policy, and proof of suppression. KPI APIs should return suppression metadata rather than raw sensitive values.

### 26. Multi-tenant isolation proofs

**Justification:** Streaming analytics often aggregates high-volume events where tenant leakage can be hard to detect after the fact.

**Improvement:** Add isolation proofs that hash tenant partitions, stream definitions, event IDs, snapshots, and projections. Release audits should prove every command and query includes tenant scope and no cross-tenant aggregate can be emitted without explicit policy.

### 27. Cross-PBC federation contracts

**Justification:** Streaming analytics depends on audit, order, payment, and operational events while preserving boundaries and avoiding shared tables.

**Improvement:** Add federation contract descriptors for every consumed external event and projection, including schema version, semantic mapping, freshness SLA, quality expectations, and failure mode. Boundary tests should reject direct references to order, payment, audit, or source PBC tables.

### 28. Schema evolution compatibility testing

**Justification:** Event payloads and metric definitions evolve; analytics must detect breaking changes before dashboards silently change meaning.

**Improvement:** Add compatibility tests for event schema additions, removals, type changes, renamed fields, unit changes, and semantic meaning changes. Stream contracts should require migration plans and consumer impact reports for breaking changes.

### 29. Metric unit and currency normalization

**Justification:** KPI aggregates become invalid when values with different units, currencies, precision, or scale are combined.

**Improvement:** Add unit/currency metadata, conversion policies, precision rules, rounding evidence, and normalization audit fields to metric events and snapshots. Quality checks should reject or quarantine incompatible units before aggregation.

### 30. Derived metric dependency graph

**Justification:** Dashboards often depend on derived KPIs such as conversion rate, revenue per order, payment success rate, or risk-adjusted throughput.

**Improvement:** Add derived metric definitions with numerator/denominator dependencies, calculation formula, null/zero handling, finality rules, freshness propagation, and lineage. Derived metrics should recompute when any base stream changes or is replayed.

### 31. Incremental materialized projection strategy

**Justification:** Recomputing full dashboard projections for every event is inefficient and can create latency spikes.

**Improvement:** Add projection refresh strategies for incremental update, full rebuild, scheduled refresh, event-triggered refresh, and degraded refresh. Store refresh cost, freshness, affected snapshots, and fallback state in `dashboard_projection`.

### 32. Query latency and freshness SLA monitoring

**Justification:** Real-time analytics must prove dashboards and KPI APIs meet latency and freshness commitments.

**Improvement:** Add SLA measurements for ingestion latency, window finalization, snapshot publication, projection refresh, query response, and alert delivery. Workbench views should show breaches, trends, owners, and remediation tasks.

### 33. Analytics cost and storage governance

**Justification:** High-volume metric events, replay windows, dimensions, and snapshots can grow without business value.

**Improvement:** Add storage usage, compute cost, event volume, query cost, replay cost, dashboard usage, and value scoring by stream. Operators should be able to retire, aggregate, sample, or archive low-value expensive streams with impact evidence.

### 34. Sampling and approximation controls

**Justification:** Some high-volume metrics require approximate algorithms, but users need to know accuracy, error bounds, and when approximation is unacceptable.

**Improvement:** Add sampling policies and approximate aggregation descriptors for cardinality, percentiles, quantiles, and top-k metrics with error bounds, confidence, and eligibility rules. KPI snapshots should disclose approximation status and uncertainty.

### 35. Percentile and distribution metrics

**Justification:** Count, sum, average, and max are insufficient for latency, risk, payment processing, fulfillment performance, and operational quality.

**Improvement:** Add percentile, histogram, distribution, unique-count, rate, ratio, and change-point aggregations with validation and UI rendering. Stream definitions should specify which advanced aggregations are mathematically valid for each metric.

### 36. Data replay audit narrative

**Justification:** Replays can materially change historical KPIs, so users need a clear narrative of why the replay occurred and what changed.

**Improvement:** Add replay narratives with cause, authorizer, data range, affected streams, before/after snapshots, downstream events, suppressed alerts, and validation results. The agent should draft narratives from replay evidence for audit review.

### 37. Immutable analytics audit ledger

**Justification:** Metric definitions, quality decisions, replays, retention changes, alerts, and KPI publications require tamper-evident auditability.

**Improvement:** Expand `analytics_audit_entry` with chained hashes, actor, command, affected objects, policy version, before/after evidence, and verification API. Snapshot proof generation should include audit entry hashes.

### 38. Cryptographic KPI proof packets

**Justification:** Operational KPIs can drive executive, financial, customer, and regulatory decisions and must be independently verifiable.

**Improvement:** Extend `kpi_snapshot_proof` into sealed proof packets containing stream contract hashes, window hashes, accepted event hashes, quality decisions, replay references, policy screens, snapshot values, and publication signatures. Provide verification APIs for auditors and consuming PBCs.

### 39. Control assertion automation for KPIs

**Justification:** KPI pipelines need controls over ingestion completeness, quality rules, finality, replay, policy screening, and dashboard publication.

**Improvement:** Expand `kpi_control_assertion` with control objective, stream scope, test method, sample window, failure evidence, owner, remediation, and next run. Release audits should require executable controls for material streams.

### 40. Governed model lifecycle for analytics intelligence

**Justification:** Forecast, anomaly, risk, and confidence models affect operational decisions and require model governance.

**Improvement:** Expand `analytics_governed_model` with purpose, stream scope, features, training data range, evaluation metrics, drift checks, calibration, approval state, challenger model, rollback plan, and usage constraints. Model output should carry model-version evidence.

### 41. Self-healing recomputation playbooks

**Justification:** Window recomputation should be controlled by explicit playbooks instead of ad hoc operator actions.

**Improvement:** Add playbooks for late events, failed quality rules, schema changes, replay correction, missing source recovery, and watermark repair. Each playbook should define trigger, dry run, approval need, recomputation steps, validation, and publication behavior.

### 42. Incident-aware analytics degradation

**Justification:** During source outages or event floods, analytics should make degradation visible rather than presenting stale metrics as healthy.

**Improvement:** Add degradation states for streams, windows, projections, and dashboards, with reason, start time, affected consumers, confidence impact, and recovery condition. APIs should return degradation metadata alongside KPI values.

### 43. Metric exception collaboration workflow

**Justification:** Resolving metric exceptions may require source owners, analysts, auditors, operations, and consuming PBC teams.

**Improvement:** Add collaboration fields to `metric_exception` for participants, comments, tasks, decisions, handoffs, SLA, escalation, and closure evidence. Agent summaries should separate evidence, assumptions, proposed fixes, and unresolved owners.

### 44. Real-time metric catalog and discovery

**Justification:** Users need to find trustworthy streams, understand meaning, see owners, and avoid duplicating metrics.

**Improvement:** Build a metric catalog UI with stream definitions, owners, freshness, quality score, usage, dashboards, lineage, certified status, sensitivity, and examples. The agent should recommend existing streams before allowing duplicate stream creation.

### 45. Natural-language metric definition assistant

**Justification:** Business users can describe desired KPIs in natural language, but the PBC must convert them into safe, typed, governed stream definitions.

**Improvement:** Add agent skills that parse KPI requests into metric stream proposals, dimensions, windows, aggregations, quality rules, policy screens, and dashboard projections. The assistant must preview generated contracts, highlight ambiguity, and require approval.

### 46. Dashboard storytelling with evidence

**Justification:** Dashboards need concise operational explanations, not just charts, when KPIs change materially.

**Improvement:** Add evidence-cited narrative generation for KPI movement, threshold breaches, forecast changes, replay adjustments, quality failures, and risk score shifts. Narratives should distinguish measured facts, provisional values, forecasts, and recommendations.

### 47. Operator command center

**Justification:** Streaming analytics operators need a single surface for lag, quality, replay, watermarks, alerts, exceptions, dead letters, projections, and controls.

**Improvement:** Build an operator command center that aggregates stream health, ingestion lag, watermark status, data-quality failures, replay jobs, projection freshness, alert noise, control failures, and dead-letter queues. Every panel should link to safe remediation commands and agent guidance.

### 48. Consumer impact and contract-change workflow

**Justification:** Metric changes can break executive dashboards, downstream PBC decisions, forecasts, alerts, and audit reports.

**Improvement:** Add consumer impact analysis for stream and KPI changes with affected projections, APIs, events, alerts, forecasts, models, and PBC consumers. Contract changes should require notification, compatibility evidence, and controlled activation.

### 49. Streaming analytics agent command skills

**Justification:** The PBC agent should safely execute operational analytics work, not merely explain dashboards.

**Improvement:** Define first-class skills for stream creation, quality-rule drafting, replay planning, watermark diagnosis, alert tuning, KPI proof generation, exception triage, forecast explanation, projection impact review, and retention impact simulation. Each skill should use typed previews, RBAC checks, human confirmation, and audit evidence.

### 50. End-to-end streaming analytics release evidence matrix

**Justification:** A world-class PBC must prove every streaming analytics capability has schema, services, APIs, events, handlers, UI, agent skills, rules, parameters, tests, and boundary evidence.

**Improvement:** Add a release evidence matrix mapping every Streaming Analytics capability to owned tables, commands, routes, AppGen-X event contracts, idempotent handlers, workbench panels, agent skills, permissions, smoke tests, and cross-PBC boundary checks. Release audits should fail whenever a claimed analytics capability lacks executable proof.
