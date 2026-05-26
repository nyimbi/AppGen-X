# Tax Localization PBC Specification

## Purpose

`tax_localization` owns tax compliance, localization, indirect tax
calculation, jurisdiction topology, authority connectivity, nexus profiles,
product taxability, counterparty tax profiles, exemption evidence, invoice tax,
cross-border duties, reverse charge, withholding, environmental levies,
filings, remittance, payment evidence, refunds, notices, digital tax
documents, audit proofs, rules, parameters, configuration, UI fragments, and
release evidence.

The PBC integrates with commerce, invoicing, order, payment, identity, schema,
audit, and authority-facing capabilities only through declared APIs, AppGen-X
events, and read-only projections. It does not share tables with other PBCs.

## Owned Datastore Boundary

The runtime owns these tables, each with generated model and migration
evidence:

- `tax_jurisdiction`: country, region, locality, currency, status, and risk.
- `tax_jurisdiction_topology`: parent jurisdiction, authority channel, nexus
  nodes, and topology hash.
- `tax_authority_channel`: authority endpoint, channel type, SLA, and status.
- `tax_authority_submission`: filing submission, channel, status, and
  acknowledgement.
- `tax_filing_calendar`: filing frequency, due day, and holiday policy.
- `tax_nexus_profile`: entity nexus thresholds and active state.
- `tax_rule`: tax type, product class, jurisdiction, rate, and status.
- `tax_rule_version`: effective dates, version, and compiled hash.
- `tax_rule_impact_analysis`: proposed-rate simulation and delta tax.
- `product_taxability`: product class, confidence, and review state.
- `counterparty_tax_profile`: registration, exemption, and nexus state.
- `tax_exemption_review`: certificate decision and expiry.
- `tax_calculation`: quote or invoice calculation header and totals.
- `tax_calculation_line`: taxable amount, tax amount, rule, and rate.
- `invoice_tax_record`: invoice tax recording and status.
- `exemption_certificate`: certificate, jurisdiction, status, and expiry.
- `tax_reverse_charge_rule`: reverse-charge determination rule.
- `tax_withholding_rule`: withholding income type, rate, and treaty code.
- `tax_environmental_levy`: levy basis, product class, and rate.
- `cross_border_duty`: origin, destination, goods value, rate, and duty.
- `tax_duty_classification`: HS classification, origin, and confidence.
- `tax_landed_cost_component`: landed-cost duty/tax component.
- `tax_filing`: period filing liability, approval, and status.
- `tax_filing_line`: calculation-backed filing line.
- `tax_reconciliation`: accrued, collected, remitted, and variance evidence.
- `tax_remittance_batch`: jurisdiction remittance batch and due date.
- `tax_payment_evidence`: remittance payment reference and amount.
- `tax_refund_claim`: refund claim amount, reason, and status.
- `tax_adjustment`: calculation adjustment and approval.
- `tax_notice`: authority notice and resolution state.
- `digital_tax_document`: clearance document and authority status.
- `tax_document_parse`: parsed certificate, rate, and jurisdiction evidence.
- `tax_liability_forecast`: expected liability and tail risk.
- `tax_policy_simulation`: policy simulation and objective score.
- `tax_cross_border_federation`: external tax projection hash.
- `tax_identity_credential`: authority or counterparty tax identity.
- `tax_audit_proof`: disclosure-minimized proof and public claims.
- `tax_allocation`: shared liability allocation and clearing bid.
- `tax_anomaly_signal`: anomaly type, entropy, and observation time.
- `tax_model_registry`: governed model lineage, performance, and drift.
- `tax_seed_data`: jurisdiction pack, tax type, product class, and rate.
- `tax_policy_rule`: executable governance policy rule.
- `tax_parameter`: bounded runtime parameter.
- `tax_configuration`: database backend, AppGen-X topic, retry limit, and
  authority channels.
- `tax_schema_extension`: owned schema extension metadata.
- `tax_control_assertion`: continuous control assertion and evidence hash.
- `tax_governed_model`: regulated model governance state.
- `tax_localization_appgen_outbox_event`: emitted AppGen-X event evidence.
- `tax_localization_appgen_inbox_event`: consumed AppGen-X event evidence.
- `tax_localization_dead_letter_event`: exhausted retry evidence.

Supported ordinary backends are PostgreSQL, MySQL, and MariaDB. Runtime
configuration rejects unsupported backends.

## Standard Capabilities

The PBC implements jurisdiction master data, jurisdiction topology, authority
channels, filing calendars, authority submissions, nexus profiles, tax rule
authoring, tax rule versions, impact analysis, product taxability,
counterparty tax profiles, quote-time calculation, calculation lines, invoice
tax records, exemption certificate validation, exemption reviews,
cross-border duties, duty classification, landed-cost components,
reverse-charge rules, withholding tax, environmental levies, digital tax
documents, document parsing, effective-date compilation, multi-tenant
isolation, tax reconciliation, remittance batches, payment evidence, refund
claims, tax adjustments, notices, approval controls, AppGen-X inbox/outbox,
idempotent handlers, retry/dead-letter evidence, permissions, configuration,
rules, parameters, seed data, and tax workbench views.

## Advanced Capabilities

The runtime proves event-sourced tax lifecycle, graph-relational jurisdiction
topology, multi-tenant compliance isolation, schema-on-read tax extension,
probabilistic taxability classification, real-time quote convergence,
counterfactual tax policy simulation, temporal liability forecasting,
autonomous filing reconciliation, semantic tax document parsing, jurisdiction
risk scoring, self-healing filing route selection, disclosure-minimized tax
audit proofs, immutable regulatory trail, dynamic policy screening, automated
tax controls, universal API and AppGen-X events, cross-border tax federation,
digital document network integration, decentralized tax identity, authority
resilience drills, crypto-agile authorization, carbon-aware filing scheduling,
algebraic remittance optimization, mechanism-design shared tax allocation,
information-theoretic anomaly detection, stochastic exposure modeling,
distributed idempotency, probabilistic ML governance, cryptographic evidence,
mathematical optimization, and tax model governance.

## Rules, Parameters, and Configuration

Configuration is validated by `tax_localization_configure_runtime`. Required
settings include `database_backend`, `event_topic`, `retry_limit`,
`default_currency`, `default_timezone`, authority channels, and workbench
limits. The ordinary topic is fixed to `appgen.tax.events`; user-facing
stream-engine selection is rejected.

Parameters are validated by `tax_localization_set_parameter`. Supported
parameters include `tax_quote_precision`,
`filing_reconciliation_tolerance`, `authority_retry_limit`,
`exemption_expiry_warning_days`, `nexus_sales_threshold`, and
`workbench_limit`.

Executable governance rules are registered by `tax_localization_register_rule`.
Tax calculation rules are registered by `tax_localization_register_tax_rule`
and compiled with effective-date evidence. Rule scopes include filing,
calculation, exemption, cross-border duty, reverse charge, withholding,
authority routing, reconciliation, refund, adjustment, and release gates.

Schema extensions are accepted only for Tax-owned tables. Foreign table
extension attempts fail boundary validation.

## APIs

- `POST /tax/jurisdictions`
- `POST /tax/rules`
- `POST /tax/quotes`
- `POST /tax/invoices/{id}/tax-records`
- `POST /tax/filings`
- `POST /tax/events/inbox`
- `GET /tax/workbench`

Declared external dependencies are APIs and projections only:

- `GET /products/taxability`
- `GET /invoices/{id}`
- `GET /orders/{id}/pricing`
- `GET /identity/policies`
- `POST /audit/tax-events`
- `product_taxability_projection`
- `invoice_tax_projection`
- `order_price_projection`
- `payment_collection_projection`
- `access_policy_projection`
- `authority_acknowledgement_projection`

## Events and Handlers

Emitted AppGen-X events:

- `TaxJurisdictionRegistered`
- `TaxRuleActivated`
- `TaxCalculated`
- `InvoiceTaxRecorded`
- `TaxFilingPrepared`

Consumed AppGen-X events:

- `ProductClassified`
- `InvoiceIssued`
- `OrderPriced`
- `PaymentCollected`
- `AccessPolicyChanged`

Handlers are idempotent by event id, record inbox evidence, update owned
projections, retry failures according to configuration, and write terminal
failures to `tax_localization_dead_letter_event`.

## UI, Permissions, and Workbench

The UI exposes the tax workbench, jurisdiction console, topology view,
authority-channel panel, filing calendar, nexus profile panel, tax rule editor,
rule version view, impact simulation panel, product taxability workbench,
counterparty profile view, quote calculation trace, invoice tax panel,
exemption review queue, duty and landed-cost panel, reverse-charge and
withholding rule panels, digital tax document view, filing monitor,
reconciliation panel, remittance batch view, payment evidence view, refund and
adjustment board, notice queue, document parser, audit proof panel, risk and
model governance panel, rule studio, parameter console, configuration editor,
inbox/outbox monitor, dead-letter triage, and release evidence panel.

The permission contract covers jurisdiction administration, rule
administration, calculation, invoice tax, filing, exemptions, reconciliation,
event handling, configuration, and audit access.

## Package Metadata and Release Evidence

The package key is `tax_localization`. Package metadata advertises the
implementation directory, standard features, advanced capabilities, owned
tables, database allowlist, fixed event topic, emitted events, consumed events,
UI fragments, API contract, schema contract, service contract, permissions,
and release evidence.

Release readiness requires:

- `tax_localization_runtime_smoke()` returns `ok`.
- `implementation_contract()` includes runtime, UI, API, schema, service,
  permissions, topic, events, and release evidence contracts.
- `tax_localization_build_schema_contract()` proves all owned tables, models,
  relationships, migrations, backend allowlist, and no shared table access.
- `tax_localization_build_service_contract()` proves command and query
  services, transaction boundary, owned mutations, and declared dependencies.
- `tax_localization_build_release_evidence()` proves schema depth, migration
  coverage, service depth, AppGen-X API/event contract, permission coverage,
  backend allowlist, and shared-table isolation.
- Focused Tax Localization tests pass.
- The global PBC release audit, implementation release audit, implemented
  capability audit, and generation smoke audit pass for the implemented PBC
  set.
- Diff scans contain no banned legacy product or framework names.
