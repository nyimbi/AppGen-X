# Accounts Receivable and Credit PBC

## Purpose

The Accounts Receivable and Credit PBC owns customer credit, invoice issue,
delivery confirmation, receivable subledger state, cash application, unapplied
cash, disputes, credit memos, refunds, write-offs, aging, dunning,
collections, customer statements, revenue schedules, and receivables workbench
evidence. It integrates with GL, treasury, tax, order, identity, workflow,
schema registry, audit ledger, and gateway PBCs through APIs, AppGen-X events,
and read-only projections.

## Owned Datastore Boundary

The PBC owns:

- `ar_credit_customer`: customer master, credit terms, identity, beneficial
  ownership, risk signals, topology, status, and compliance metadata.
- `ar_credit_invoice`: invoice header, lines, tax, performance obligations,
  due date, open amount, lifecycle state, and revenue evidence.
- `ar_credit_delivery`: fulfillment confirmation evidence referenced by
  receivable validation and revenue scheduling.
- `ar_credit_receipt`: received cash, remittance parse result, bank reference,
  application confidence, and cash-pool assignment.
- `ar_credit_unapplied_cash`: receipts that cannot be matched, triage status,
  reason, and resolution trail.
- `ar_credit_adjustment`: credit memo, refund, write-off, dispute resolution,
  approval evidence, and customer impact.
- `ar_credit_collection_action`: dunning notices, collection channel, schedule,
  idempotency key, and outcome evidence.
- `ar_credit_outbox`, `ar_credit_inbox`, and `ar_credit_dead_letter`:
  AppGen-X event contract tables for exactly-once handlers, retries, and
  dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

## Standard Table-Stakes Capabilities

The PBC fully implements customer master, customer onboarding, credit terms,
invoice generation, invoice validation, delivery confirmation, cash
application, partial payment, unapplied cash, credit memo, write-off, refund,
aging, dunning, collection action scheduling, customer statements, revenue
schedule recognition, credit-limit decisions, dispute management, audit trail,
controls, configuration schema, executable rules, runtime parameters, seed
data, permissions, and AR workbench views.

## Advanced Capabilities

The runtime proves event-sourced receivable lifecycle, graph-relational
customer topology, multi-tenant cash application isolation, schema-evolution
resilient receivable metadata, probabilistic cash application, liquidity-aware
credit extension, counterfactual collection strategy optimization, temporal
revenue-to-cash forecasting, autonomous dispute resolution, semantic
remittance parsing, predictive customer default scoring, self-healing
collection routing, disclosure-minimized revenue verification, immutable
electronic invoicing tax evidence, dynamic sanction and fraud screening,
automated controls, universal API and asynchronous events, cross-border
receivable federation, invoice-finance network integration, decentralized
customer identity, payment-rail resilience drills, crypto-agile payment
authorization, carbon-aware collection scheduling, algebraic collection
optimization, payment-term mechanism design, information-shift cash anomaly
detection, temporal receivable stochastic modeling, formal invariants, and
governed financial models.

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, status, and
scope-specific predicates such as cash application threshold, required delivery
confirmation, credit buffer, collection threshold, dispute auto-resolution
criteria, write-off approval, refund approval, and release-gate constraints.

Parameters include `auto_cash_threshold`, `credit_limit_buffer`,
`collection_risk_threshold`, `dunning_grace_days`, `write_off_approval_limit`,
and `workbench_limit`.

Configuration includes database backend, event topic, retry limit, default
currency, default timezone, allowed collection channels, and workbench limits.
Runtime configuration rejects unsupported databases and exposes the AppGen-X
event contract as the ordinary eventing surface.

## Public APIs

- `POST /ar/customers`
- `POST /ar/invoices`
- `POST /ar/deliveries`
- `POST /ar/remittances/parse`
- `POST /ar/cash-applications`
- `POST /ar/unapplied-cash`
- `POST /ar/credit-memos`
- `POST /ar/write-offs`
- `POST /ar/refunds`
- `POST /ar/collections`
- `GET /ar/aging`
- `GET /ar/statements/{customer_id}`
- `GET /ar/workbench`

## Events

Emitted events:

- `CustomerOnboarded`
- `InvoiceIssued`
- `DeliveryConfirmed`
- `PaymentReceived`
- `UnappliedCashRecorded`
- `CreditMemoIssued`
- `ReceivableWrittenOff`
- `CustomerRefundScheduled`
- `CollectionActionScheduled`

Consumed events:

- `CustomerIdentityVerified`
- `DeliveryConfirmed`
- `TaxPolicyChanged`
- `CashForecastUpdated`
- `AccessPolicyChanged`
- `CollectionPolicyChanged`

Handlers are idempotent by `ar_credit:{event_type}:{event_id}`, retry at
least three times, and write failures to `ar_credit_dead_letter`.

## UI and Workbench

The UI exposes an AR workbench, customer credit console, invoice issue queue,
delivery confirmation board, cash application workbench, unapplied-cash triage,
dispute resolution board, credit memo console, dunning and collections console,
customer statement view, revenue schedule view, customer risk panel, AR rule
studio, AR parameter console, and configuration panel. Actions are
permission-bound and rendered from package-owned state.

## Release Evidence

Release readiness requires passing runtime smoke, package-local UI contract,
owned tables, API/event/handler surfaces, AppGen-X event contract evidence,
configuration/rule/parameter execution, generated DSL compatibility, package
metadata, workbench rendering, and focused unit tests.
