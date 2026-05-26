# Subscription Billing PBC

`subscription_billing` is the AppGen-X packaged business capability for recurring
revenue, usage rating, invoice approval, renewals, dunning, and revenue handoff.
It is a composable business package, not a shared module: it owns its schema,
runtime state, service commands, AppGen-X event contracts, workbench fragments,
rules, configuration, parameters, tests, and release evidence.

## Stable Identity

- PBC key: `subscription_billing`.
- Mesh: `commerce`.
- Package directory: `src/pyAppGen/pbcs/subscription_billing`.
- Runtime entrypoint: `subscription_billing_runtime_capabilities()`.
- UI entrypoint: `subscription_billing_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Default datastore: `subscription_billing_store`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: AppGen-X outbox/inbox contract only. The UI and
  configuration contract keep stream-engine selection hidden.

## Owned Datastore Boundary

The PBC owns these core domain tables:

- `subscription`: customer subscription identity, plan binding, tenant, region,
  currency, lifecycle state, renewal confidence, churn risk, MRR, and audit proof.
- `usage_meter`: rated usage events, billable units, effective usage rate, rated
  amount, currency, status, and audit proof.
- `billing_schedule`: next invoice date, billing period, schedule state, and
  lifecycle timing used for renewals and invoice generation.
- `dunning_notice`: open collection notices, reason, retry policy, risk score,
  customer reference, and dead-letter evidence.

The executable schema contract also covers package-local support and evidence
tables:

- `plan_catalog`, `invoice`, `billing_rule`, `billing_parameter`,
  `billing_configuration`, and `billing_schema_extension`.
- AppGen-X evidence tables: `subscription_billing_appgen_outbox_event`,
  `subscription_billing_appgen_inbox_event`, and
  `subscription_billing_dead_letter_event`.

Cross-PBC dependencies are represented only through API calls, events, and
projections. The runtime boundary verifier accepts owned tables plus declared
dependencies such as `payment_orchestration.PaymentCaptured`,
`price_promotion_engine.PriceOptimized`, `tax_localization.POST /tax-quotes`,
`gl_core.POST /journals`, `customer_projection`, and
`entitlement_projection`; direct access to foreign tables is rejected.

## Standard Table-Stakes Capabilities

The implementation covers the ordinary subscription-management surface expected
from a production recurring-revenue system:

- Plan catalog, rate schedules, currencies, supported regions, billing periods,
  base prices, included units, and usage rates.
- Subscription lifecycle: activation, schedule creation, active state,
  renewal review, renewal approval, customer binding, tenant isolation, and
  audit-proof generation.
- Usage metering: quantity capture, included-unit calculation, effective-rate
  selection, rounding precision, rated amount, and `UsageRated` outbox events.
- Invoice generation: period invoices, base plus usage amount, approval
  threshold enforcement, deferred-revenue schedule, tax handoff marker,
  ledger handoff marker, entitlement handoff marker, and invoice audit proof.
- Renewal management: confidence thresholds, churn-risk evaluation, renewal
  count, and review state when thresholds are not met.
- Dunning management: notice creation, reason tracking, risk scoring, retry
  policy, dead-letter target, and workbench visibility.
- Payment handoff: idempotent `PaymentCaptured` handler that marks known
  invoices paid and records inbound event evidence.
- Price handoff: idempotent `PriceOptimized` handler with discount guardrails
  and effective-rate calculation.
- Configuration schema: database backend, AppGen-X event topic, retry limit,
  default currency, supported currencies, supported regions, billing calendars,
  timezone, approval mode, and workbench limit.
- Rule engine: tenant, rule type, plan-family allowlist, currency allowlist,
  region allowlist, renewal policy, invoice policy, status, compiled hash, and
  policy-engine metadata.
- Parameter engine: renewal confidence, churn risk, dunning risk, usage rating
  precision, proration precision, retry limit, carbon-aware batch window,
  discount guardrail, approval threshold, and workbench limit with bounds.
- Schema extension: zero-shared-table extension registration for owned
  subscription, usage, schedule, and dunning tables.
- RBAC descriptors: admin, operator, and auditor roles plus explicit
  permissions for configuration, subscription, usage, invoice, renewal,
  dunning, event, and audit operations.
- UI fragments: subscription registry, plan designer, usage console, invoice
  approval workbench, renewal console, dunning board, entitlement panel, rule
  studio, parameter console, configuration panel, event outbox, and dead-letter
  queue.
- Seed data: billing calendars and dunning reasons used by runtime smoke tests.

## Advanced Capabilities

The runtime exposes advanced evidence for:

- Event-sourced subscription lifecycle with append-only state events and
  AppGen-X outbox records.
- Graph-relational subscription topology across subscriptions, schedules,
  usage meters, invoices, dunning notices, and declared event dependencies.
- Tenant-isolated subscription operations with tenant filters in commands and
  workbench views.
- Schema-evolution-safe owned extensions.
- Probabilistic churn, payment, and revenue scoring.
- Counterfactual plan and proration simulation hooks through parameterized
  rating precision, optimized rates, and discount guardrails.
- Temporal MRR, ARR, renewal, and exposure forecasting evidence.
- Autonomous billing exception resolution through retry/dead-letter handling.
- Semantic billing instruction parsing readiness through compiled rules and
  typed command envelopes.
- Predictive billing risk for invoices, dunning, and renewal review.
- Self-healing billing-route evidence through idempotent handlers and retry
  policies.
- Cryptographic billing proofs and immutable billing audit hashes.
- Dynamic billing policy screening through tenant, plan, currency, region,
  approval, and event-idempotency controls.
- Automated billing control testing through runtime smoke and focused tests.
- Cross-system federation with payment, pricing, tax, ledger, entitlement, and
  customer projections.
- Chaos-tolerant AppGen-X eventing with duplicate detection and simulated
  handler failure.
- Crypto agility via hash-based audit proofs that can be rotated by package
  policy.
- Carbon-aware invoice batch scheduling parameters.
- Mathematical revenue optimization and discount allocation guardrails.
- Billing anomaly detection and stochastic revenue exposure evidence.
- Governed model evidence for risk and pricing decisions.
- Universal API plus asynchronous event surface.
- Distributed-systems engineering through owned state, idempotency keys,
  transaction boundaries, and outbox/inbox separation.

## Commands And Services

The service layer exposes these package-local command methods:

- `configure_runtime(configuration)`.
- `set_parameter(name, value)`.
- `register_rule(rule)`.
- `register_schema_extension(table, fields)`.
- `register_plan(plan)`.
- `create_subscription(command)`.
- `record_usage(usage)`.
- `generate_invoice(subscription_id, period=...)`.
- `renew_subscription(subscription_id)`.
- `create_dunning_notice(subscription_id, reason=...)`.
- `receive_event(event, simulate_failure=False)`.
- `run_control_tests(state)`.
- `simulate_proration_quote(subscription_id, target_seats=..., remaining_ratio=...)`.
- `score_revenue_exposure(subscription_id)`.
- `build_api_contract()`.
- `build_schema_contract()`.
- `build_service_contract()`.
- `build_release_evidence()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references)`.

All commands work on package-local runtime state and return side-effect-free
state transitions suitable for generated-app embedding and release smoke tests.

## APIs

The package declares these catalog routes and expands them into executable API
contract entries:

- `POST /subscriptions` maps to `create_subscription`, owns `subscription` and
  `billing_schedule`, and emits `SubscriptionActivated`.
- `POST /usage` maps to `record_usage`, owns `usage_meter`, and emits
  `UsageRated`.
- `POST /renewals` maps to `renew_subscription`, owns `subscription` and
  `billing_schedule`, and emits `SubscriptionRenewed`.
- `POST /invoices` maps to `generate_invoice`, uses owned schedule state, and
  emits `InvoiceApproved` or `InvoiceApprovalRequested`.
- `POST /dunning-notices` maps to `create_dunning_notice`, owns
  `dunning_notice`, and emits `DunningNoticeCreated`.
- `POST /subscription-billing/events/inbox` maps to `receive_event`, consumes
  AppGen-X events with event ID idempotency.
- `GET /subscription-billing/workbench` maps to `build_workbench_view` and
  returns package-local UI/workbench binding evidence.

## Events And Handlers

Emitted events use AppGen-X outbox records with event IDs, event types, tenant,
payload, idempotency key, retry policy, dead-letter target, and audit hash.

- Emitted: `SubscriptionActivated`, `SubscriptionRenewed`, `UsageRated`,
  `InvoiceApproved`, `InvoiceApprovalRequested`, and `DunningNoticeCreated`.
- Catalog emitted: `SubscriptionActivated`, `SubscriptionRenewed`,
  `UsageRated`, `InvoiceApproved`, `InvoiceApprovalRequested`, and
  `DunningNoticeCreated`.
- Consumed: `PaymentCaptured` and `PriceOptimized`.
- Handler behavior: unsupported event types are rejected, missing event IDs are
  rejected, duplicate event IDs are idempotently ignored, simulated failures
  first produce retry evidence and then dead-letter records once the retry
  limit is exhausted, and successful events are recorded in the inbox.

## Workbench

The UI contract exposes route-backed fragments for subscription operations,
usage, invoice approval, renewals, dunning, entitlement handoff, rules,
parameters, configuration, event outbox, inbox, and dead-letter review.
Rendering uses RBAC permissions to calculate visible and locked actions and
returns explicit workbench binding evidence for owned tables, AppGen-X runtime
tables, panel bindings, configuration, rules, and parameters. The configuration
editor exposes only the AppGen-X event contract and supported SQL backends.

## Release Evidence

Focused tests prove:

- Runtime capabilities and smoke checks pass.
- Package-local `build_schema_contract()`, `build_service_contract()`, and
  `build_release_evidence()` expose executable implementation evidence.
- Configuration, rules, parameters, schema extensions, plan registration,
  subscriptions, usage, invoices, payment events, dunning, and workbench
  rendering execute.
- API, UI binding, and permission contracts are exposed.
- Owned-table boundary validation accepts declared dependencies and rejects
  foreign tables.
- Invalid database backends, invalid parameters, non-owned schema extensions,
  duplicate events, retry transitions, and handler dead-letter failures are
  all evidenced.
- The package participates in `pbc_implementation_release_audit()` and the
  all-PBC generation smoke audit through central exports.
