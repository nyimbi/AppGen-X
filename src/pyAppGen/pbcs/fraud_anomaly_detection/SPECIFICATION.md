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
- `identity_link`
- `behavior_baseline`
- `device_fingerprint`
- `network_indicator`
- `velocity_window`
- `decision_explanation`
- `loss_exposure`
- `analyst_queue_item`
- `fraud_parameter`
- `fraud_configuration`

Allowed datastore backends are PostgreSQL, MySQL, and MariaDB. Runtime
configuration requires the AppGen-X fraud event topic and never exposes a
stream-engine picker or alternate event-contract selector.

Generated AppGen-X outbox, inbox, retry, idempotency, and dead-letter evidence
remain platform-owned runtime metadata behind the package-local contract.

## Generated Schema

The package-local generated schema contract must enumerate only the owned
domain tables plus AppGen-X runtime evidence tables:

- Domain tables: `risk_signal`, `anomaly_score`, `fraud_rule`,
  `risk_case`, `identity_link`, `behavior_baseline`,
  `device_fingerprint`, `network_indicator`, `velocity_window`,
  `decision_explanation`, `loss_exposure`, `analyst_queue_item`,
  `fraud_parameter`, and `fraud_configuration`
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
- Runtime event handling populates identity links, behavior baselines, device
  fingerprints, network indicators, velocity windows, decision explanations,
  loss exposures, and analyst queue items; these tables are executable state,
  not schema-only descriptors.
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
- `POST /fraud-rules`
- `POST /risk-signals/{id}/score`
- `POST /risk-cases`
- `POST /fraud-configuration`
- `POST /fraud-parameters`

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
ingestion, identity linking, behavior baseline refresh, device/network
indicator capture, velocity calculation, anomaly scoring, decision explanation,
loss projection, analyst queueing, risk-case opening, and AppGen-X event
handling.

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

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `fraud_anomaly_detection`
- Mesh: `intelligence`
- Datastore backend: `postgresql`

### Owned Tables

- `risk_signal`
- `anomaly_score`
- `fraud_rule`
- `risk_case`
- `identity_link`
- `behavior_baseline`
- `device_fingerprint`
- `network_indicator`
- `velocity_window`
- `decision_explanation`
- `loss_exposure`
- `analyst_queue_item`
- `fraud_parameter`
- `fraud_configuration`

### API Routes

- `POST /risk-events`
- `POST /fraud-checks`
- `GET /risk-cases`
- `GET /risk-workbench`
- `POST /fraud-rules`
- `POST /risk-signals/{id}/score`
- `POST /risk-cases`
- `POST /fraud-configuration`
- `POST /fraud-parameters`

### Emitted Events

- `FraudRiskScored`
- `RiskCaseOpened`

### Consumed Events

- `CheckoutCompleted`
- `PaymentCaptured`
- `AccessPolicyChanged`

### UI Fragments

- `FraudAnomalyDetectionWorkbench`
- `RiskSignalMonitor`
- `AnomalyScoreBoard`
- `FraudRuleStudio`
- `RiskCaseConsole`
- `IdentityLinkAnalysisPanel`
- `BehaviorBaselinePanel`
- `DeviceFingerprintPanel`
- `NetworkIndicatorPanel`
- `VelocityWindowPanel`
- `DecisionExplanationConsole`
- `LossExposurePanel`
- `AnalystQueueConsole`
- `FraudParameterConsole`
- `FraudConfigurationPanel`
- `RiskEventInbox`
- `RiskEventOutbox`
- `RiskDeadLetterQueue`

### Permissions

- `fraud_anomaly_detection.read`
- `fraud_anomaly_detection.event.write`
- `fraud_anomaly_detection.anomaly_score.write`
- `fraud_anomaly_detection.fraud_rule.write`
- `fraud_anomaly_detection.risk_case.write`
- `fraud_anomaly_detection.event.consume`
- `fraud_anomaly_detection.configure`
- `fraud_anomaly_detection.audit`

### Configuration Keys

- `database_backend`
- `event_topic`
- `retry_limit`
- `default_region`
- `supported_regions`
- `supported_event_types`
- `identity_dimensions`
- `default_timezone`
- `scoring_mode`
- `workbench_limit`

### Standard Features

- `risk_signal_ingestion`
- `anomaly_scoring`
- `fraud_rule_management`
- `risk_case_management`
- `checkout_projection`
- `payment_projection`
- `access_policy_projection`
- `identity_link_analysis`
- `velocity_checks`
- `device_and_network_indicators`
- `behavior_baselines`
- `loss_exposure_projection`
- `decision_explanations`
- `analyst_queue`
- `tenant_isolation`
- `appgen_x_outbox`
- `appgen_x_inbox`
- `idempotent_handlers`
- `retry_dead_letter_evidence`
- `permissions`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `seed_data`
- `workbench`

### Advanced Capabilities

- `event_sourced_risk_signal_lifecycle`
- `owned_fraud_schema_boundary`
- `multi_tenant_risk_isolation`
- `schema_evolution_resilient_risk_context`
- `checkout_and_payment_event_ingestion`
- `access_policy_change_intelligence`
- `behavior_baseline_anomaly_scoring`
- `fraud_rule_compilation_and_execution`
- `risk_case_management_and_escalation`
- `graph_identity_link_analysis`
- `probabilistic_risk_scoring`
- `counterfactual_rule_simulation`
- `temporal_attack_forecasting`
- `autonomous_triage_recommendations`
- `semantic_signal_interpretation`
- `explainable_risk_decisions`
- `predictive_loss_exposure`
- `self_healing_threshold_tuning`
- `cryptographic_risk_audit_proof`
- `immutable_case_audit_trail`
- `dynamic_policy_screening`
- `automated_model_control_testing`
- `cross_system_checkout_payment_identity_federation`
- `appgen_x_outbox_inbox_eventing`
- `idempotent_handlers`
- `retry_dead_letter_evidence`
- `permissions_governance_evidence`
- `configuration_schema`
- `parameter_engine`
- `rule_engine`
- `seed_data`
- `workbench_ui`
- `governed_model_evidence`

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->

## Agent, Chatbot Skills, And Self-Registration Contract

The `fraud_anomaly_detection` package exposes a first-class PBC agent and chatbot interface through `agent.py`. The composed application imports these capabilities under the `fraud_anomaly_detection_skills` namespace so a single application assistant can route help, task guidance, document instruction intake, governed datastore CRUD planning, workbench navigation, and policy explanation back to the owning PBC instead of inventing cross-package mutations. The agent contract is scoped to the `Anomalous Activity and Fraud Detection` boundary and must name the command, permission, owned tables, idempotency key, expected AppGen-X event, and human confirmation requirement before any create, update, or delete plan is eligible to execute.

Document and instruction intake is explicit release evidence. The chatbot can accept uploaded documents, operational notes, or user instructions, extract candidate facts for owned tables such as `fraud_anomaly_detection_risk_signal`, `fraud_anomaly_detection_anomaly_score`, `fraud_anomaly_detection_fraud_rule`, `fraud_anomaly_detection_risk_case`, `fraud_anomaly_detection_identity_link`, `fraud_anomaly_detection_behavior_baseline`, validate those facts against package rules, parameters, configuration, and permissions, and return a side-effect-free mutation preview. The preview is not a write. It is a governed plan that references service operations such as , uses AppGen-X event expectations such as `FraudRiskScored`, `RiskCaseOpened`, rejects foreign tables, and records whether a read-only query or a confirmed command is required. This keeps AI assistance professional, auditable, and bounded to the PBC datastore.

Self-registration is also part of the specification. `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` must produce a side-effect-free discovery and registration plan for `fraud_anomaly_detection`. Registration metadata identifies the source package directory, required artifacts, owned datastore, AppGen-X event contract, UI fragments, RBAC descriptors, configuration schema, seed data, tests, and release evidence without mutating the global catalog during discovery. Composition tooling may then register the PBC, merge the `fraud_anomaly_detection_skills` contribution into the single composed assistant, and expose the workbench UI while preserving owned-table boundaries and declared API/event/projection dependencies.

