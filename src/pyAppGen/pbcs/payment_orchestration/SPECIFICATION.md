# Payment Orchestration PBC Specification

## Scope

`payment_orchestration` owns payment intent lifecycle, gateway routing, payment
token governance, fraud handoff, settlement evidence, refund/void commands, and
payment workbench operations for AppGen-X composable applications.

The PBC composes with checkout, subscription billing, fraud, treasury, general
ledger, and customer PBCs through APIs, AppGen-X events, and read-model
projections only. It does not share tables with other PBCs.

## Owned Boundary

Owned tables:

- `payment_gateway`
- `payment_intent`
- `payment_token`
- `fraud_check`
- `payment_event`
- `payment_outbox`
- `payment_inbox`
- `payment_dead_letter`
- `payment_rule`
- `payment_parameter`
- `payment_configuration`

Allowed datastore backends are PostgreSQL, MySQL, and MariaDB. Runtime
configuration requires an AppGen-X event topic and never exposes user-facing
stream-engine or alternate event-contract selection.

## Standard Capabilities

- Gateway registry, health, routing priority, settlement currency, and region
  eligibility.
- Tokenized payment methods with issuer, network, wallet, and vault metadata.
- Payment intents for authorization, capture, refund, void, failure, and
  settlement handoff.
- Fraud checks, risk outcomes, challenge/deny decisions, and retry evidence.
- Provider routing with cost, latency, authorization-rate, risk, and capacity
  scoring.
- Checkout and fraud consumed-event handling with idempotent inbox state.
- AppGen-X outbox events for payment capture, payment failure, and fraud-check
  requests.
- Retry/dead-letter evidence, tenant isolation, permissions, seed/config/rules,
  bounded parameters, and workbench UI fragments.

## Advanced Capabilities

- Event-sourced payment lifecycle with hash-chained payment events.
- Graph-relational topology across gateways, tokens, intents, fraud checks,
  settlement handoffs, customers, checkout sessions, and ledger projections.
- Probabilistic authorization, fraud, and settlement scoring.
- Counterfactual provider-routing simulation.
- Temporal authorization-rate and settlement-risk forecasting.
- Autonomous payment exception resolution.
- Semantic payment instruction parsing.
- Predictive payment risk scoring and self-healing gateway route selection.
- Cryptographic payment proof and immutable audit trail.
- Dynamic payment policy screening and continuous control testing.
- Cross-system checkout, billing, ledger, treasury, and fraud federation.
- Chaos-tolerant AppGen-X eventing, crypto agility, carbon-aware settlement
  windows, mathematical provider optimization, provider allocation mechanisms,
  anomaly detection, stochastic exposure modeling, governed ML evidence,
  universal API/async contracts, and distributed-systems evidence.

## APIs and Events

APIs:

- `POST /payment-intents`
- `POST /gateway-routes`
- `POST /tokens`
- `POST /payment-captures`
- `POST /payment-refunds`
- `GET /payment-workbench`

Emitted events:

- `PaymentCaptured`
- `PaymentFailed`
- `FraudCheckRequested`

Consumed events:

- `CheckoutCompleted`
- `FraudRiskScored`

Handlers are idempotent through `payment_orchestration:<EventType>:<event_id>`
keys, retry through the AppGen-X event contract, and route exhausted failures to
`payment_orchestration.dead_letter`.

## Rules, Parameters, and Configuration

Rules require tenant, status, scope, gateway, risk, currency, region, and
capture-policy evidence. Rules compile into deterministic SHA3 hashes with
normalized inputs. Parameters are bounded to authorization, risk, settlement,
retry, routing, fee, latency, and workbench controls.

Configuration rejects backends outside PostgreSQL, MySQL, and MariaDB, requires
an AppGen-X event topic, and records that stream-engine selection is not
user-facing. Workbench views surface configuration, rule, parameter, outbox,
inbox, and dead-letter bindings.

## UI Contract

The package exports a workbench UI contract with fragments for payment intents,
gateway routing, token vault state, fraud checks, capture/refund actions,
settlement evidence, rules, parameters, configuration, outbox, inbox, and
dead-letter evidence.
