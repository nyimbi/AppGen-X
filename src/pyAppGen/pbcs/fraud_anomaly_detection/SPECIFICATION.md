# Fraud Anomaly Detection PBC Specification

## Scope

`fraud_anomaly_detection` owns behavior-derived risk signals, anomaly scores,
fraud rule execution, risk case management, and fraud/risk workbench operations
for AppGen-X composable applications.

The PBC composes with checkout, payment orchestration, access governance,
identity, and case-management surfaces through APIs, AppGen-X events, and
read-model projections only. It does not share tables with other PBCs.

## Owned Boundary

Owned tables:

- `risk_signal`
- `anomaly_score`
- `fraud_rule`
- `risk_case`

Allowed datastore backends are PostgreSQL, MySQL, and MariaDB. Runtime
configuration requires the AppGen-X fraud event topic and never exposes a
stream-engine picker or alternate event-contract selector.

Generated AppGen-X outbox, inbox, retry, idempotency, and dead-letter evidence
remain platform-owned runtime metadata behind the package-local contract.

## Generated Schema

The package-local generated schema contract must enumerate only the owned
domain tables plus AppGen-X runtime evidence tables:

- Domain tables: `risk_signal`, `anomaly_score`, `fraud_rule`, `risk_case`
- Runtime tables: `fraud_anomaly_detection_appgen_outbox_event`,
  `fraud_anomaly_detection_appgen_inbox_event`,
  `fraud_anomaly_detection_dead_letter_event`

Generated artifacts must include one migration and one model descriptor per
owned table, explicit owned relationships from signals to scores and cases, and
the PostgreSQL/MySQL/MariaDB backend allowlist only. Shared-table access stays
forbidden.

## Standard Capabilities

- Risk signal ingestion for checkout, payment, and access-policy activity.
- Anomaly scoring with explainable outputs and deterministic rule adjustments.
- Fraud rule registration, compilation, and bounded score adjustment controls.
- Risk case opening, queue routing, severity derivation, and analyst workbench
  summaries.
- Identity-link analysis, device/network indicators, velocity checks, behavior
  baselines, and loss-exposure projections.
- Idempotent consumption of `CheckoutCompleted`, `PaymentCaptured`, and
  `AccessPolicyChanged`.
- Emission of `FraudRiskScored` and `RiskCaseOpened` through the AppGen-X
  outbox contract.
- Retry/dead-letter evidence, tenant isolation, permissions, configuration
  schema, bounded parameters, seed data, and workbench UI fragments.

## Advanced Capabilities

- Event-sourced risk signal lifecycle with immutable case and scoring evidence.
- Probabilistic fraud scoring, graph identity-link analysis, and temporal attack
  forecasting.
- Counterfactual rule simulation, explainable risk decisions, and autonomous
  triage recommendations.
- Semantic signal interpretation, predictive loss exposure, and self-healing
  threshold tuning.
- Dynamic policy screening, continuous control testing, cryptographic audit
  proofs, and governed intelligence evidence.
- Cross-system checkout, payment, and identity federation through declared
  APIs/events only.

## APIs and Events

APIs:

- `POST /risk-events`
- `POST /fraud-checks`
- `GET /risk-cases`
- `GET /risk-workbench`

Emitted events:

- `FraudRiskScored`
- `RiskCaseOpened`

Consumed events:

- `CheckoutCompleted`
- `PaymentCaptured`
- `AccessPolicyChanged`

Handlers are idempotent through
`fraud_anomaly_detection:<EventType>:<event_id>` keys, retry through the
AppGen-X event contract, and route exhausted failures to
`fraud_anomaly_detection.dead_letter`.

## Rules, Parameters, and Configuration

Rules require tenant, scope, status, allowed event types, allowed regions,
signal policy, anomaly policy, and case policy evidence. Fraud rules compile
into deterministic hashes with explicit trigger payloads, score adjustments, and
decision intent (`approve`, `review`, or `deny`).

Parameters are bounded to checkout, payment, and access-policy weights; alert
and case-open thresholds; baseline depth; behavior decay; identity-link
influence; analyst override influence; and workbench limits.

Configuration rejects backends outside PostgreSQL, MySQL, and MariaDB, requires
the AppGen-X fraud event topic, records the AppGen-X event contract, and keeps
stream-engine selection hidden. Workbench views surface configuration, policy
rules, fraud rules, parameters, outbox, inbox, and dead-letter bindings.

## Service Layer

The package-local service contract must expose command methods for runtime
configuration, parameter/rule registration, fraud-rule registration, risk-signal
ingestion, anomaly scoring, risk-case opening, and AppGen-X event handling.

Query methods must include workbench, API, schema, service, and release
evidence builders plus owned-boundary verification. Service-layer evidence must
also include:

- Fixed AppGen-X eventing with no stream-engine or event-contract picker
- Explicit outbox/inbox/dead-letter table bindings
- Idempotent `receive_event` handling
- Retry/dead-letter evidence derived from `retry_limit`
- Generated service, route, event, handler, and UI artifact descriptors
- No shared-table dependencies

## UI Contract

The package exports a workbench UI contract with fragments for risk signals,
anomaly scores, fraud rules, risk cases, identity-link analysis, explainability,
loss-exposure monitoring, configuration, parameters, inbox/outbox evidence, and
dead-letter evidence.

## Release Evidence

Release is acceptable only when the package-local evidence and central PBC
audits prove all of the following:

- `fraud_anomaly_detection_runtime_smoke()` returns `ok: True` and covers every
  documented advanced fraud/anomaly capability key.
- `implementation_contract()` exposes standard features, advanced runtime,
  UI contract, API contract, permissions contract, owned tables, allowed
  PostgreSQL/MySQL/MariaDB backends, consumed/emitted event types, and the fixed
  AppGen-X event topic.
- Focused runtime tests prove risk-signal ingestion, fraud-rule registration,
  anomaly scoring, fraud-check decisioning, case opening, idempotent event
  handling, retry/dead-letter behavior, workbench binding evidence, and
  owned-table boundary rejection.
- Package-local schema, service, and release-evidence builders prove owned
  tables, runtime outbox/inbox/dead-letter evidence, generated
  migration/model/service/route/event/handler/UI artifacts, permissions,
  configuration, AppGen-X-only eventing, and the PostgreSQL/MySQL/MariaDB
  backend allowlist.
- `pbc_implementation_release_audit(("fraud_anomaly_detection",))`,
  `pbc_generation_smoke_audit(...)`, `pbc_implemented_capability_audit(...)`,
  full `pbc_implementation_release_audit(...)`, and `pbc_release_audit()` all
  return `ok: True`.
- Restricted-name scans over the package and tests are clean, and ordinary users
  cannot choose stream engines or non-AppGen-X event contracts.
