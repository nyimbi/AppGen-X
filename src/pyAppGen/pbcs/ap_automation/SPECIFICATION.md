# Accounts Payable Automation PBC

## Purpose

The Accounts Payable Automation PBC owns vendor onboarding, vendor bank and tax
profiles, purchase-order references, goods-receipt references, invoice capture,
electronic invoice ingestion, two-way and three-way matching, contract
compliance matching, exception handling, approval policy, tax validation,
withholding, payment scheduling, payment batching, payment execution, remittance
advice, discount optimization, vendor statement reconciliation, vendor risk,
and AP workbench evidence. It integrates with GL, treasury, tax, procurement,
workflow, identity, schema registry, audit ledger, and gateway PBCs through
APIs, AppGen-X events, and read-only package-local projections.

## Owned Datastore Boundary

The PBC owns:

- `ap_automation_vendor`: vendor master, beneficial ownership, identity,
  payment terms, risk signals, status, and compliance metadata.
- `ap_automation_vendor_site`: remit-to addresses, operating sites, default
  currency, and site-level status.
- `ap_automation_vendor_bank_account`: tokenized bank account, supported
  payment rail, validation status, and account-verification proof.
- `ap_automation_vendor_tax_profile`: jurisdiction, withholding code,
  exemption status, and proof hash.
- `ap_automation_vendor_risk_signal`: vendor risk observations, score, source,
  and observation timestamp.
- `ap_automation_purchase_order`: PO reference, vendor, currency, committed
  amount, status, and audit proof.
- `ap_automation_purchase_order_line`: PO line item, quantity, unit price,
  account assignment, and matching key.
- `ap_automation_goods_receipt`: receipt evidence, PO reference, receiving
  status, exceptions, and audit proof.
- `ap_automation_goods_receipt_line`: receipt line item, quantity, exception
  code, and receiving reconciliation evidence.
- `ap_automation_invoice`: invoice header, vendor, PO, receipt, tax, contract
  terms, subtotal, total, match state, approval state, and payment state.
- `ap_automation_invoice_line`: invoice line item, account assignment, tax
  code, quantity, unit price, and matching dimensions.
- `ap_automation_invoice_capture_artifact`: OCR/e-invoice/source-document
  artifact, source hash, extraction confidence, and storage reference.
- `ap_automation_invoice_match_result`: probabilistic two-way, three-way, and
  contract-match evidence, confidence, decision, and explanation hash.
- `ap_automation_payment`: scheduled and executed payment records, rail,
  approval evidence, idempotency key, and settlement metadata.
- `ap_automation_payment_batch`: payment batch, rail, currency, scheduled date,
  status, and total amount.
- `ap_automation_payment_rail_decision`: payment-rail candidate score, cost,
  latency, risk, and selected route.
- `ap_automation_discount_opportunity`: discount rate, discount value,
  counterfactual capital cost, net benefit, and decision.
- `ap_automation_vendor_statement`: vendor statement hash, reconciled amount,
  exception count, and status.
- `ap_automation_withholding_tax`: withholding jurisdiction, amount, rate, and
  proof hash.
- `ap_automation_e_invoice_submission`: e-invoice standard, jurisdiction,
  submission hash, acceptance state, and immutable submission proof.
- `ap_automation_exception_case`: match, tax, duplicate, vendor, and liquidity
  exception state with resolution evidence.
- `ap_automation_approval_task`: approver, threshold, decision, and
  segregation-of-duties evidence.
- `ap_automation_cash_forecast_projection`: AppGen-X consumed treasury
  projection snapshot owned locally by AP.
- `ap_automation_policy_rule`, `ap_automation_runtime_parameter`, and
  `ap_automation_schema_extension`: executable rules, bounded parameters, and
  owned schema-on-read extension records.
- `ap_automation_control_assertion`: duplicate, approval, payment, tax, and
  segregation-of-duties control evidence.
- `ap_automation_governed_model`: regulated AP model metadata, feature lineage,
  drift score, and governance status.
- `ap_automation_outbox`, `ap_automation_inbox`, and
  `ap_automation_dead_letter`: AppGen-X event contract tables for exactly-once
  handlers, retries, and dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

The executable `ap_automation_build_schema_contract()` returns at least 30
owned AP tables, one migration descriptor per table, one model descriptor per
table, and owned-only relationships for vendors, sites, bank accounts, tax
profiles, purchase orders, receipts, invoices, invoice lines, match results,
payments, exceptions, and approval tasks. Cross-PBC references are represented
only as declared APIs, AppGen-X events, or package-local projections. Shared
table access is explicitly false.

## Standard Table-Stakes Capabilities

The PBC fully implements vendor master, vendor-site management, vendor bank
validation, vendor tax profile management, vendor onboarding, purchase-order
references, goods-receipt references, receipt-line reconciliation, invoice
capture, OCR extraction, electronic invoice ingestion, invoice validation,
two-way service matching, three-way matching, contract compliance matching,
exception management, approval workflow, segregation-of-duties checks, tax
validation, withholding tax, payment terms, payment scheduling, payment
batching, payment execution, remittance advice, discount management, duplicate
invoice detection, vendor statement reconciliation, bank-rail routing,
payment-rail failover, audit trail, controls, configuration schema, executable
rules, bounded runtime parameters, seed data, permissions, and AP workbench
views.

`ap_automation_build_service_contract()` proves command methods for these
surfaces and binds every mutation to the AP-owned datastore plus AppGen-X outbox
transaction boundary. Query surfaces cover cash forecasting, discount
counterfactuals, vendor risk, fraud information shift, temporal liquidity, and
workbench views.

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

Advanced capability implementation is executable and deterministic:

- invoice lifecycle operations append AppGen-X outbox events and preserve
  immutable audit hashes;
- vendor graph data combines beneficial owners, risk signals, tax profile, and
  payment credentials without sharing external tables;
- liquidity-aware scheduling uses AP-owned cash forecast projections from
  declared treasury events;
- schema extensions are accepted only for AP-owned tables with safe field
  names and versioned extension records;
- three-way matching combines PO amount, invoice amount, receipt quantity, and
  vendor risk into a confidence decision;
- payment routing chooses available rails and records failover evidence;
- discount counterfactuals compare discount value against capital cost;
- exception resolution can self-correct high-evidence missing-receipt cases;
- contract-term extraction derives net terms, discount windows, discount rate,
  and tax jurisdiction from source text;
- vendor risk scoring uses sanction context, payment history, ownership graph,
  and model governance;
- tax validation returns disclosure-minimized proof claims without exposing
  invoice-line payloads;
- e-invoice submission produces immutable jurisdictional submission hashes;
- control testing verifies segregation of duties, approval limits, duplicate
  invoice guards, and payment integrity;
- cross-border payment federation emits ISO-style payment message evidence;
- supply-chain finance integration computes reverse-factoring advance amounts;
- decentralized vendor identity checks DID, issuer, status, and revocation
  posture;
- resilience drills prove rail outage self-healing;
- crypto epochs support algorithm agility for payment authorization;
- carbon-aware settlement selects lower-intensity windows;
- algebraic routing optimizes cost, risk, liquidity, and carbon;
- dynamic discount negotiation clears between buyer bid and vendor ask;
- information-theoretic fraud detection measures distribution shift;
- financial model governance records feature lineage, drift, and explainability
  requirements.

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

Configuration and parameter behavior is executable:

- database backend must be PostgreSQL, MySQL, or MariaDB;
- event topic must be `appgen.ap.events`;
- event-engine picker fields are rejected before configuration is accepted;
- accepted configuration records the fixed AppGen-X event contract,
  non-selectable event surface, backend allowlist, required topic, and payment
  rails;
- parameters are bounded and compiled with hashes;
- rules require `rule_id`, tenant, scope, and status;
- schema extensions must target AP-owned tables and use safe field names.

## Public APIs

- `POST /ap/vendors`
- `POST /ap/vendor-bank-accounts`
- `POST /ap/vendor-tax-profiles`
- `POST /ap/purchase-orders`
- `POST /ap/goods-receipts`
- `POST /ap/invoices`
- `POST /ap/invoices/{invoice_id}/match`
- `POST /ap/exceptions`
- `POST /ap/approval-tasks`
- `POST /ap/payment-schedules`
- `POST /ap/payment-batches`
- `POST /ap/payments`
- `POST /ap/e-invoices`
- `POST /ap/vendor-statements/reconcile`
- `POST /ap/events/inbox`
- `GET /ap/workbench`

The API contract declares each route's command or query, owned-table set,
required permission, idempotency key, emitted or consumed event, backend
allowlist, and AppGen-X event topic. No route grants direct access to GL,
treasury, procurement, tax, identity, audit, workflow, or gateway tables.

## Events

Emitted events:

- `VendorOnboarded`
- `PurchaseOrderIssued`
- `GoodsReceiptRecorded`
- `InvoiceCaptured`
- `PaymentScheduled`
- `PaymentExecuted`
- `InvoiceExceptionResolved`
- `VendorRiskChanged`
- `DiscountOpportunityCaptured`

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

The UI exposes an AP workbench, vendor onboarding console, vendor-bank
validation panel, invoice capture queue, e-invoice ingestion lane, three-way
match board, contract compliance board, exception triage, approval task queue,
payment schedule console, payment batch console, payment execution panel, tax
validation view, withholding view, remittance view, discount optimization view,
vendor statement reconciliation view, vendor-risk panel, AP rule studio, AP
parameter console, and configuration panel. Actions are permission-bound and
rendered from package-owned state.

Workbench binding evidence includes owned tables, outbox/inbox/dead-letter
tables, configuration state, rule count, parameter count, vendor count, invoice
count, open invoice amount, scheduled and executed payment counts, retry and
dead-letter evidence, event topic, visible actions, and locked actions per
principal permission set.

## Release Evidence

Release readiness requires:

- `ap_automation_runtime_smoke()` returning `ok: True` with every advanced
  capability check passing;
- `ap_automation_build_schema_contract()` returning at least 30 owned tables,
  owned relationships, one migration descriptor per table, one model descriptor
  per table, PostgreSQL/MySQL/MariaDB backend allowlist, and no shared-table
  access;
- `ap_automation_build_service_contract()` returning at least 20 command
  methods, owned-datastore transaction boundary, declared API/event/projection
  dependencies, and no shared tables;
- `ap_automation_build_release_evidence()` returning `ok: True` for schema
  depth, migration coverage, service depth, API/event contract, permission
  coverage, backend allowlist, and shared-table rejection;
- package `implementation_contract()` exposing the same owned tables,
  schema/service/release contracts, UI, API, permissions, backend allowlist,
  emitted/consumed event types, and fixed event topic;
- focused tests proving configuration, parameters, rules, schema extension
  validation, vendor onboarding, PO/receipt capture, invoice capture,
  probabilistic matching, payment scheduling, rail failover, payment execution,
  discount analysis, cash forecasting, idempotent inbox handling,
  retry/dead-letter behavior, workbench rendering, permission-bound actions,
  API contracts, and owned-table boundary rejection;
- `pbc_implementation_release_audit(("ap_automation",))`,
  `pbc_implemented_capability_audit(("ap_automation",))`, full
  generation/capability/implementation/catalog audits, and `pbc_release_audit()`
  returning `ok: True`;
- restricted-name scans over the AP package/test/spec files returning clean and
  no stream-engine or non-AppGen-X event picker exposed to ordinary users.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `ap_automation`
- Mesh: `finops`
- Datastore backend: `None`

### Owned Tables

- `vendor`
- `vendor_site`
- `vendor_bank_account`
- `vendor_tax_profile`
- `vendor_risk_signal`
- `purchase_order`
- `purchase_order_line`
- `goods_receipt`
- `goods_receipt_line`
- `invoice`
- `invoice_line`
- `invoice_capture_artifact`
- `invoice_match_result`
- `payment`
- `payment_batch`
- `payment_rail_decision`
- `discount_opportunity`
- `vendor_statement`
- `withholding_tax`
- `e_invoice_submission`
- `exception_case`
- `approval_task`
- `cash_forecast_projection`
- `policy_rule`
- `runtime_parameter`
- `schema_extension`
- `control_assertion`
- `governed_model`

### API Routes

- `POST /ap/vendors`
- `POST /ap/vendor-bank-accounts`
- `POST /ap/vendor-tax-profiles`
- `POST /ap/purchase-orders`
- `POST /ap/goods-receipts`
- `POST /ap/invoices`
- `POST /ap/invoices/{invoice_id}/match`
- `POST /ap/exceptions`
- `POST /ap/approval-tasks`
- `POST /ap/payment-schedules`
- `POST /ap/payment-batches`
- `POST /ap/payments`
- `POST /ap/e-invoices`
- `POST /ap/vendor-statements/reconcile`
- `GET /ap/workbench`

### Emitted Events

- `VendorOnboarded`
- `PurchaseOrderIssued`
- `GoodsReceiptRecorded`
- `InvoiceCaptured`
- `PaymentScheduled`
- `PaymentExecuted`
- `InvoiceExceptionResolved`
- `VendorRiskChanged`
- `DiscountOpportunityCaptured`

### Consumed Events

- `VendorApproved`
- `PurchaseOrderApproved`
- `GoodsReceiptPosted`
- `TaxPolicyChanged`
- `CashForecastUpdated`
- `AccessPolicyChanged`

### UI Fragments

- None declared

### Permissions

- None declared

### Configuration Keys

- None declared

### Standard Features

- None declared

### Advanced Capabilities

- None declared

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->
