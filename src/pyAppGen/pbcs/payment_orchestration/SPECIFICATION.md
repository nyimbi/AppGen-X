# Payment Orchestration

Package-local implementation contract for the Payment Orchestration PBC. The
package owns payment intent lifecycle, provider routing, payment-token custody,
fraud handoff, capture/refund/void execution, settlement and reconciliation
evidence, release validation, UI fragments, and AppGen-X event handling.

## Stable Identity

- PBC key: `payment_orchestration`.
- Mesh: commerce.
- Implementation directory: `src/pyAppGen/pbcs/payment_orchestration`.
- Runtime module: `runtime.py`.
- UI module: `ui.py`.
- Test module: `tests/test_pbc_payment_orchestration_runtime.py`.
- Event topic: `appgen.payment.events`.
- Event contract: AppGen-X.
- Supported relational backends: PostgreSQL, MySQL, and MariaDB.
- User-facing stream-engine selection is not exposed.

## Owned Boundary

Owned tables and generated model artifacts:

- `payment_gateway`
- `payment_token`
- `payment_intent`
- `gateway_route`
- `fraud_check`
- `payment_capture`
- `payment_refund`
- `payment_void`
- `payment_settlement`
- `payment_reconciliation_handoff`
- `payment_exception`
- `payment_audit_trace`
- `payment_proof`
- `payment_federation_projection`
- `payment_carbon_window`
- `payment_gateway_optimization`
- `payment_provider_allocation`
- `payment_anomaly_signal`
- `payment_risk_model`
- `payment_exposure_forecast`
- `payment_instruction_parse`
- `payment_schema_extension`
- `payment_control_assertion`
- `payment_governed_model`
- `payment_rule`
- `payment_parameter`
- `payment_configuration`
- `payment_orchestration_appgen_outbox_event`
- `payment_orchestration_appgen_inbox_event`
- `payment_orchestration_dead_letter_event`

The PBC does not share checkout, billing, fraud, ledger, treasury, customer, or
audit tables. Cross-PBC integration is declared only through APIs, AppGen-X
events, or projections:

- Consumed events: `CheckoutCompleted`, `FraudRiskScored`.
- API dependencies: `GET /checkout/sessions/{id}`, `GET /fraud/cases/{id}`,
  `GET /billing/invoices/{id}`, `POST /ledger/payment-events`,
  `POST /audit/payment-events`.
- Projections and handoffs: `checkout_completion_projection`,
  `fraud_risk_projection`, `ledger_cash_projection`,
  `billing_invoice_projection`.
- Emitted events: `PaymentIntentCreated`, `FraudCheckRequested`,
  `PaymentCaptured`, `PaymentRefunded`, `PaymentVoided`, `PaymentFailed`.

## Standard Capabilities

- Gateway registration with latency, fee, authorization, settlement-risk,
  region, currency, and method evidence.
- Tokenized payment methods with wallet/network metadata and vault references.
- Payment intent creation from checkout evidence with tenant isolation.
- Provider routing with deterministic weight-based objective scoring.
- Fraud handoff, consumed-event inbox evidence, and duplicate-event suppression.
- Capture, refund, and void commands with settlement/reconciliation evidence.
- AppGen-X outbox, inbox, retry, idempotency, and dead-letter evidence.
- Rules, parameters, runtime configuration, schema extensions, control
  assertions, governed model metadata, and package-local workbench UI.

## Generated Schema, Services, And Release Evidence

`build_schema_contract` emits field definitions, relationships, migration paths
under `pbcs/payment_orchestration/migrations/`, generated model names, backend
allowlists, and `shared_table_access: false` for every owned table.

`build_service_contract` declares the transaction boundary as the Payment
Orchestration owned datastore plus the AppGen-X outbox. Command methods cover
runtime configuration, parameters, rules, schema extensions, event intake,
gateway and token registration, intent creation, routing, fraud requests,
capture/refund/void execution, payment proof generation, policy screening,
resilience drills, crypto rotation, carbon-aware settlement, gateway mix
optimization, provider allocation, governed-model registration, control tests,
and owned-boundary verification. Query methods cover workbench views, route
simulation, authorization forecasting, semantic instruction parsing, payment
risk scoring, exception resolution, anomaly detection, stochastic exposure, and
generated API/schema/release contracts.

`build_release_evidence` combines schema, service, API, workbench, and RBAC
evidence into release checks for owned schema depth, migration coverage,
command depth, fixed AppGen-X eventing, permission coverage, backend allowlist,
and no shared-table access.

## Advanced Capabilities

- Event-sourced payment lifecycle with immutable hash-chain evidence.
- Graph-relational topology across gateway, token, intent, route, fraud, and
  settlement artifacts.
- Probabilistic authorization, fraud, and settlement scoring.
- Counterfactual provider-routing simulation.
- Temporal authorization and settlement forecasting.
- Autonomous exception resolution for declines, reviews, settlement delay, and
  token refresh.
- Semantic payment instruction parsing.
- Predictive payment risk scoring and self-healing route selection.
- Cryptographic payment proof generation.
- Dynamic policy screening and automated control testing.
- Cross-system checkout, billing, ledger, and fraud federation.
- Chaos-tolerant AppGen-X eventing, crypto agility, carbon-aware settlement
  windows, mathematical gateway optimization, provider allocation mechanisms,
  anomaly detection, stochastic exposure modeling, and governed ML evidence.

## Runtime Services

- `configure_runtime` validates backend, exact AppGen-X topic, retry limits,
  currency/region/method scope, workbench limit, and stream-picker absence.
- `set_parameter` accepts only supported numeric payment parameters.
- `register_rule` validates rule identity, tenant, routing scope, and stores
  deterministic compiled evidence.
- `register_schema_extension` accepts only owned-table schema extensions.
- `receive_event` idempotently handles `CheckoutCompleted` and
  `FraudRiskScored`, records inbox evidence, schedules retries, and
  dead-letters exhausted failures.
- `register_gateway` owns gateway registry evidence.
- `tokenize_payment_method` owns token/vault metadata.
- `create_payment_intent` owns payment intent creation from checkout evidence.
- `route_gateway` selects provider routes from owned rules and parameters.
- `request_fraud_check` emits AppGen-X fraud-request evidence.
- `capture_payment`, `refund_payment`, and `void_payment` mutate only owned
  payment tables and emit owned events.
- `build_api_contract`, `build_schema_contract`, `build_service_contract`, and
  `build_release_evidence` emit package-local contract evidence.
- `build_workbench_view` exposes operational and release evidence.

## API Contract

- `POST /gateways` maps to `register_gateway`.
- `POST /tokens` maps to `tokenize_payment_method`.
- `POST /payment-intents` maps to `create_payment_intent`.
- `POST /payment-intents/{id}/route` maps to `route_gateway`.
- `POST /payment-intents/{id}/fraud-checks` maps to `request_fraud_check`.
- `POST /payment-intents/{id}/captures` maps to `capture_payment`.
- `POST /payment-intents/{id}/refunds` maps to `refund_payment`.
- `POST /payment-intents/{id}/void` maps to `void_payment`.
- `POST /payment/events/inbox` maps to `receive_event`.
- `GET /payment-workbench` maps to `build_workbench_view`.

Every route descriptor includes owned tables, command/query binding,
idempotency or event evidence, required permission, and API/projection
dependencies.

## Events And Handlers

Emitted events:

- `PaymentIntentCreated`
- `FraudCheckRequested`
- `PaymentCaptured`
- `PaymentRefunded`
- `PaymentVoided`
- `PaymentFailed`

Consumed events:

- `CheckoutCompleted`
- `FraudRiskScored`

Handlers are idempotent by `payment_orchestration:<EventType>:<event_id>` keys.
Duplicate processed events do not create duplicate state changes. Failed events
record retry evidence until the configured retry limit and then produce
dead-letter records in `payment_orchestration_dead_letter_event`.

## Rules, Parameters, And Configuration

Rules cover gateway eligibility, currencies, regions, capture policy, risk
ceiling, tenant, and lifecycle status. Parameters include authorization
thresholds, fraud-review thresholds, capture tolerance, retry limits, route
weights, settlement-risk weight, capture-attempt limits, and workbench limits.

Configuration includes database backend, event topic, retry limit, default
currency, supported currencies, supported regions, supported methods,
settlement windows, default timezone, and workbench limit. Runtime
configuration records `event_contract: AppGen-X`, the relational-backend
allowlist, hidden stream-engine picker evidence, non-selectable event-contract
evidence, and owned tables.

## UI And Workbench

UI fragments:

- `PaymentOrchestrationWorkbench`
- `PaymentIntentConsole`
- `GatewayRoutingBoard`
- `PaymentTokenVault`
- `FraudCheckQueue`
- `CaptureRefundConsole`
- `SettlementEvidencePanel`
- `PaymentRuleStudio`
- `PaymentParameterConsole`
- `PaymentConfigurationPanel`
- `PaymentEventOutbox`
- `PaymentInboxMonitor`
- `PaymentDeadLetterQueue`

The workbench exposes intent, gateway, token, route, fraud, capture, refund,
void, settlement, inbox, outbox, dead-letter, configuration, rule, parameter,
and owned-boundary evidence. Visible actions are RBAC-filtered by payment
intent, capture, refund, event, configuration, and audit permissions.

## Release Evidence

Release is acceptable only when package-local evidence and central PBC audits
prove all of the following:

- `payment_orchestration_runtime_smoke()` returns `ok: True` and covers every
  advanced payment capability key.
- `implementation_contract()` exposes standard features, advanced runtime, UI
  contract, API contract, schema contract, service contract, release evidence
  contract, permissions contract, owned tables, PostgreSQL/MySQL/MariaDB
  backends, consumed/emitted event types, and the fixed AppGen-X event topic.
- Focused runtime tests prove gateway registration, tokenization, payment
  intent creation, routing, fraud handoff, capture, refund, void, idempotent
  consumed events, retry/dead-letter behavior, schema-extension ownership, API
  and permissions contracts, release evidence, workbench binding evidence, and
  foreign-table rejection.
- `pbc_implementation_release_audit(("payment_orchestration",))` returns
  `ok: True`.
- Ordinary users cannot choose stream engines or non-AppGen-X event contracts.
