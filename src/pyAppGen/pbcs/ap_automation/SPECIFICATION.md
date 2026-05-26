# Accounts Payable Automation PBC

## Purpose

The Accounts Payable Automation PBC owns vendor onboarding, purchase-order
references, goods-receipt references, invoice capture, three-way matching,
exception handling, approval policy, tax validation, payment scheduling,
payment execution, discount optimization, vendor risk, and AP workbench
evidence. It integrates with GL, treasury, tax, procurement, workflow, identity,
schema registry, audit ledger, and gateway PBCs through APIs, AppGen-X events,
and read-only projections.

## Owned Datastore Boundary

The PBC owns:

- `ap_automation_vendor`: vendor master, beneficial ownership, identity,
  payment terms, risk signals, status, and compliance metadata.
- `ap_automation_purchase_order`: PO reference, vendor, currency, lines,
  committed amount, and status.
- `ap_automation_goods_receipt`: receipt evidence, PO reference, quantities,
  exceptions, and receiving status.
- `ap_automation_invoice`: invoice header, lines, tax, contract terms,
  subtotal, total, match state, approval state, and payment state.
- `ap_automation_payment`: scheduled and executed payment records, rail,
  approval evidence, idempotency key, and settlement metadata.
- `ap_automation_exception_case`: match, tax, duplicate, vendor, and liquidity
  exceptions with resolution evidence.
- `ap_automation_outbox`, `ap_automation_inbox`, and
  `ap_automation_dead_letter`: AppGen-X event contract tables for exactly-once
  handlers, retries, and dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

## Standard Table-Stakes Capabilities

The PBC fully implements vendor master, vendor onboarding, purchase-order
references, goods-receipt references, invoice capture, invoice validation,
three-way matching, exception management, approval workflow, tax validation,
payment terms, payment scheduling, payment execution, discount management,
duplicate invoice detection, vendor statement reconciliation, withholding tax,
bank-rail routing, audit trail, controls, configuration schema, executable
rules, runtime parameters, seed data, permissions, and AP workbench views.

## Advanced Capabilities

The runtime proves event-sourced invoice lifecycle, graph-relational vendor data
modeling, multi-tenant liquidity isolation, schema-evolution resilient invoice
metadata, probabilistic three-way matching, liquidity-aware payment scheduling,
counterfactual discount analysis, temporal cash-flow forecasting, autonomous
exception resolution, semantic contract-to-invoice alignment, predictive vendor
risk scoring, self-healing payment routing, disclosure-minimized tax validation,
immutable electronic invoicing evidence, dynamic vendor-network screening,
automated controls, universal API and asynchronous events, cross-border payment
federation, supply-chain finance network integration, decentralized vendor
identity, payment-rail resilience drills, crypto-agile payment authorization,
carbon-aware settlement scheduling, algebraic payment routing, dynamic discount
mechanism design, fraud information-shift detection, temporal liquidity
forecasting, formal invariants, and governed financial models.

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, status, and
scope-specific predicates such as match threshold, required three-way match,
approval boundaries, tax requirements, and payment-rail policy. Parameters
include `auto_match_threshold`, `payment_approval_limit`,
`discount_capture_floor`, `vendor_risk_threshold`, `liquidity_buffer`, and
`workbench_limit`.

Configuration includes database backend, event topic, retry limit, default
currency, default timezone, allowed payment rails, and workbench limits. Runtime
configuration rejects unsupported databases and exposes the AppGen-X event
contract as the ordinary eventing surface.

## Public APIs

- `POST /ap/vendors`
- `POST /ap/purchase-orders`
- `POST /ap/goods-receipts`
- `POST /ap/invoices`
- `POST /ap/invoices/{id}/match`
- `POST /ap/exceptions`
- `POST /ap/payment-schedules`
- `POST /ap/payments`
- `GET /ap/workbench`

## Events

Emitted events:

- `VendorOnboarded`
- `PurchaseOrderIssued`
- `GoodsReceiptRecorded`
- `InvoiceCaptured`
- `PaymentScheduled`
- `PaymentExecuted`
- `InvoiceExceptionResolved`

Consumed events:

- `VendorApproved`
- `PurchaseOrderApproved`
- `GoodsReceiptPosted`
- `TaxPolicyChanged`
- `CashForecastUpdated`
- `AccessPolicyChanged`

Handlers are idempotent by `ap_automation:{event_type}:{event_id}`, retry at
least three times, and write failures to `ap_automation_dead_letter`.

## UI and Workbench

The UI exposes an AP workbench, vendor onboarding console, invoice capture
queue, three-way match board, exception triage, payment schedule console,
payment execution panel, tax validation view, discount optimization view,
vendor-risk panel, AP rule studio, AP parameter console, and configuration
panel. Actions are permission-bound and rendered from package-owned state.

## Release Evidence

Release readiness requires passing runtime smoke, package-local UI contract,
owned tables, API/event/handler surfaces, AppGen-X event contract evidence,
configuration/rule/parameter execution, generated DSL compatibility, package
metadata, workbench rendering, and focused unit tests.
