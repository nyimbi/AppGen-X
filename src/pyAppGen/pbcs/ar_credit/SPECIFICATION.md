# Accounts Receivable and Credit PBC

## Purpose

The Accounts Receivable and Credit PBC owns the quote-to-cash financial
boundary after customer identity and order fulfillment signals are available.
It manages customer credit, sites, payment terms, invoice issue, invoice lines,
tax evidence, delivery confirmation, receivable subledger state, cash receipts,
remittance interpretation, cash application, unapplied cash, disputes, credit
memos, refunds, write-offs, aging, dunning, collection actions, customer
statements, revenue schedules, credit decisions, electronic invoice evidence,
cross-border receivables, invoice-finance programs, controls, rules,
parameters, governed models, and the AR workbench.

The PBC integrates with other AppGen-X capabilities only through declared
APIs, AppGen-X events, and read-only projections. It does not share tables with
GL, treasury, tax, order, identity, workflow, audit, or gateway PBCs.

## Owned Datastore Boundary

The executable runtime declares the following AR-owned tables and migrations.
Every table is owned by `ar_credit`, has a generated model, and is included in
the schema contract:

- `ar_customer`: tenant, customer identity, name, status, default probability,
  credit limit, and audit proof.
- `ar_customer_site`: bill-to and ship-to locations, site status, and customer
  references.
- `ar_customer_graph`: parent entities, beneficial owners, network hashes, and
  risk context.
- `ar_customer_credit_profile`: approved limits, risk grades, approval state,
  and scoring model version.
- `ar_customer_payment_terms`: net days, discount windows, discount rate, and
  terms state.
- `ar_customer_risk_signal`: observed signals, source lineage, score, and
  observation time.
- `ar_invoice`: invoice header, customer, currency, dates, total, open amount,
  and lifecycle state.
- `ar_invoice_line`: SKU, quantity, unit price, account, and tax code.
- `ar_invoice_tax`: jurisdiction, rate, tax amount, and proof hash.
- `ar_invoice_performance_obligation`: allocated obligations, satisfaction
  state, and recognition evidence.
- `ar_delivery_confirmation`: delivery evidence hash and confirmation time.
- `ar_cash_receipt`: received amount, currency, bank reference, and receipt
  timestamp.
- `ar_remittance_advice`: parsed remittance, invoice reference, confidence,
  source hash, and bank reference.
- `ar_cash_application`: receipt-to-invoice application decision, confidence,
  and applied amount.
- `ar_unapplied_cash`: unmatched receipt amount, reason, triage state, and
  resolution trace.
- `ar_credit_memo`: invoice adjustment, amount, reason, and status.
- `ar_write_off`: authorized write-off amount, approver, reason, and status.
- `ar_refund`: refund amount, currency, reason, and schedule state.
- `ar_dispute_case`: disputed invoice amount, reason, decision, and audit
  trace.
- `ar_collection_action`: channel, due date, status, and collection ownership.
- `ar_dunning_notice`: dunning level, channel, days past due, and send time.
- `ar_statement`: customer statement balance, hash, status, and as-of date.
- `ar_revenue_schedule`: recognized and deferred revenue for invoice
  obligations.
- `ar_revenue_schedule_line`: schedule line obligation, amount, and recognition
  state.
- `ar_cash_pool`: currency cash pool, received cash, unapplied cash, and as-of
  view.
- `ar_credit_decision`: recommended limit, risk-adjusted score, and decision.
- `ar_e_invoice_submission`: jurisdiction, standard, submission hash, and
  acceptance state.
- `ar_cross_border_receivable`: target country, settlement amount, and message
  identifier.
- `ar_invoice_finance_program`: financing program, advance amount, and
  counterparty.
- `ar_policy_rule`: executable AR rule, scope, status, predicate, and compiled
  hash.
- `ar_runtime_parameter`: bounded runtime parameter, value, and compiled hash.
- `ar_schema_extension`: table-scoped field extension and version.
- `ar_control_assertion`: continuous control assertion, result, evidence hash,
  and test time.
- `ar_governed_model`: model lineage, drift score, and governance state.
- `ar_credit_appgen_outbox_event`: emitted AppGen-X event, topic, idempotency
  key, and audit hash.
- `ar_credit_appgen_inbox_event`: consumed AppGen-X event, idempotency key,
  attempts, and status.
- `ar_credit_dead_letter_event`: failed event, idempotency key, attempts, and
  dead-letter reason.

Supported backing stores for ordinary AR deployments are PostgreSQL, MySQL,
and MariaDB. The runtime rejects unsupported database backends.

## Standard Capabilities

The PBC implements ordinary AR table-stakes functionality:

- Customer master, customer site maintenance, customer graph ownership, credit
  profile management, identity projection, beneficial-owner risk context, and
  payment terms.
- Invoice issue with lines, taxes, due dates, performance obligations, open
  amount, status transitions, and deterministic invoice totals.
- Delivery confirmation before revenue or cash automation where the active
  rule requires fulfillment evidence.
- Remittance parsing, received cash, probabilistic application, partial
  payment, auto-clear thresholds, cash pool updates, and unapplied cash triage.
- Credit memo, refund, write-off, dispute case, dunning, collection action,
  customer statement, aging, and revenue schedule workflows.
- Credit extension decisions, credit-limit buffers, customer default scoring,
  and collection routing.
- Executable configuration, parameter, rule, schema-extension, permission,
  audit, control, and workbench contracts.
- AppGen-X inbox, outbox, idempotent handlers, retry evidence, and dead-letter
  records.

## Advanced Capabilities

The runtime also proves advanced AR capabilities:

- Event-sourced receivable lifecycle with immutable emitted event evidence and
  projection-friendly state reconstruction.
- Graph-relational customer topology for beneficial-owner, parent, and network
  risk context.
- Multi-tenant cash application isolation with tenant-scoped receipts,
  invoices, rules, and workbench views.
- Schema evolution through owned extension records and schema contract
  migration evidence.
- Probabilistic cash application using confidence thresholds and manual review
  fallbacks.
- Liquidity-aware credit extension using treasury forecast projections without
  treasury table access.
- Counterfactual collection strategy optimization against DSO targets.
- Temporal revenue-to-cash forecasting and stochastic receivable modeling.
- Autonomous dispute resolution with evidence-scored recommendations.
- Semantic remittance parsing for unstructured payment text.
- Predictive customer default scoring and governed model registration.
- Self-healing collection routing with channel availability failover.
- Disclosure-minimized revenue verification using deterministic proof hashes.
- Immutable electronic invoicing and tax audit evidence.
- Dynamic sanction and fraud screening across customer graph context.
- Continuous control testing for event contracts, write-off authorization, and
  open-balance integrity.
- Universal API plus asynchronous AppGen-X events with no user-facing stream
  engine selection.
- Cross-border receivable federation and invoice-finance program integration.
- Decentralized customer identity verification through signed identity
  projections.
- Payment-rail resilience drills, crypto-agile payment authorization,
  carbon-aware collection scheduling, algebraic collection optimization,
  payment-term mechanism design, information-shift cash application anomaly
  detection, formal invariant checks, and financial model governance.

## Rules, Parameters, and Configuration

Configuration is executable and validated by `ar_credit_configure_runtime`.
Required settings include `database_backend`, `event_topic`, `retry_limit`,
`default_currency`, `default_timezone`, allowed collection channels, and
workbench limits. The ordinary event contract is always AppGen-X on
`appgen.ar.events`; users are not exposed to a stream-engine picker.

Runtime parameters are validated by `ar_credit_set_parameter`. Supported
parameters include `auto_cash_threshold`, `credit_limit_buffer`,
`collection_risk_threshold`, `dunning_grace_days`, `write_off_approval_limit`,
and `workbench_limit`.

Rules are registered by `ar_credit_register_rule` and compiled into owned rule
records. Supported rule scopes include cash application, delivery evidence,
credit extension, dunning, collection, dispute resolution, write-off approval,
refund approval, and release gates. Rules and parameters are surfaced in the
workbench and are counted in release smoke evidence.

Schema extensions are accepted only for AR-owned tables. Attempts to extend
foreign tables fail boundary validation.

## Public APIs

The API contract exposes AR commands and queries:

- `POST /ar/customers`
- `POST /ar/invoices`
- `POST /ar/deliveries`
- `POST /ar/remittances/parse`
- `POST /ar/cash-applications`
- `POST /ar/unapplied-cash`
- `POST /ar/credit-memos`
- `POST /ar/write-offs`
- `POST /ar/refunds`
- `POST /ar/disputes`
- `POST /ar/collections`
- `POST /ar/e-invoices`
- `POST /ar/events/inbox`
- `GET /ar/aging`
- `GET /ar/statements/{customer_id}`
- `GET /ar/revenue-schedules/{invoice_id}`
- `GET /ar/workbench`

Declared external dependencies are APIs and projections only:

- `GET /customer_360/customers/{id}/profile`
- `GET /treasury/cash-forecast`
- `POST /tax_localization/quotes`
- `GET /federated_iam/access-policies/{id}`
- `customer_identity_projection`
- `delivery_projection`
- `tax_policy_projection`
- `cash_forecast_projection`
- `access_policy_projection`

## Events and Handlers

Emitted AppGen-X events:

- `CustomerOnboarded`
- `InvoiceIssued`
- `DeliveryConfirmed`
- `PaymentReceived`
- `UnappliedCashRecorded`
- `CreditMemoIssued`
- `ReceivableWrittenOff`
- `CustomerRefundScheduled`
- `CollectionActionScheduled`

Consumed AppGen-X events:

- `CustomerIdentityVerified`
- `DeliveryConfirmed`
- `TaxPolicyChanged`
- `CashForecastUpdated`
- `AccessPolicyChanged`
- `CollectionPolicyChanged`

Handlers are idempotent by `ar_credit:{event_type}:{event_id}`. Processing
failures retry according to configuration and then write to the AR dead-letter
table with the failing event type, idempotency key, attempts, and reason.

## UI and Workbench

The package includes AR UI/workbench fragments for:

- AR workbench summary.
- Customer credit console.
- Customer sites and terms panel.
- Invoice issue queue and invoice detail.
- Delivery confirmation board.
- Cash application workbench and remittance parser.
- Unapplied-cash triage.
- Dispute, credit memo, refund, and write-off boards.
- Aging, dunning, collection, and statement views.
- Revenue schedule view.
- Credit risk, model governance, and anomaly panels.
- Rule studio, parameter console, schema-extension panel, configuration panel,
  inbox/outbox monitor, dead-letter triage, and release evidence panel.

Every visible action is permission-bound and rendered from AR-owned state plus
declared projection inputs.

## Permissions and RBAC

The permission contract includes read, configure, rule, parameter, schema,
customer, invoice, cash, dispute, credit, collection, revenue, event,
workbench, and audit permissions. Command methods require scoped permissions;
release evidence checks that critical actions such as `issue_invoice`,
`apply_cash`, and `receive_event` are covered.

## Package Metadata and Self-Registration

The package key is `ar_credit`. Package metadata advertises the implementation
directory, capabilities, standard features, owned tables, database allowlist,
AppGen-X topic, emitted events, consumed events, UI fragments, API contract,
schema contract, service contract, permissions, and release evidence. External
PBC registration plans must remain side-effect-free and may depend on this PBC
only through APIs, events, or projections.

## Release Evidence

Release readiness requires all of the following evidence to pass:

- `ar_credit_runtime_smoke()` returns `ok`.
- `implementation_contract()` includes runtime, UI, API, schema, service,
  permissions, AppGen-X event topic, and release evidence contracts.
- `ar_credit_build_schema_contract()` proves all owned tables, models,
  relationships, migrations, backend allowlist, and no shared table access.
- `ar_credit_build_service_contract()` proves command and query surfaces,
  transaction boundary, owned mutations, and declared external dependencies.
- `ar_credit_build_release_evidence()` proves schema depth, migration coverage,
  service depth, API/event contract, permission coverage, backend allowlist,
  and shared-table isolation.
- Focused AR tests pass.
- The global PBC release audit, implementation release audit, implemented
  capability audit, and generation smoke audit pass for the implemented PBC
  set.
- Diff scans contain no banned legacy product or framework names.
