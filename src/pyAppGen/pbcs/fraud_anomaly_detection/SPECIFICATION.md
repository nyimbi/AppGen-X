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
- `pbc_implementation_release_audit(("fraud_anomaly_detection",))`,
  `pbc_generation_smoke_audit(...)`, `pbc_implemented_capability_audit(...)`,
  full `pbc_implementation_release_audit(...)`, and `pbc_release_audit()` all
  return `ok: True`.
- Restricted-name scans over the package and tests are clean, and ordinary users
  cannot choose stream engines or non-AppGen-X event contracts.
