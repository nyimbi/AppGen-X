# Treasury Cash PBC Specification

## Purpose

`treasury_cash` owns cash positioning, liquidity planning, bank connectivity,
payment funding, FX exposure, intercompany cash movement, investment and debt
operations, treasury controls, and resilience evidence. It is a composable PBC:
it exposes APIs, events, projections, and risk signals, but it does not share
tables with payables, receivables, ledger, or banking adapters.

## Standard Table-Stakes Capabilities

- Bank account master data with account ownership, currency, legal entity, and
  signatory metadata.
- Opening and intraday bank balance capture.
- Cash position projection by tenant, currency, account, and value date.
- Bank statement ingestion and reconciliation.
- Cash forecast from payables, receivables, payroll, tax, and manual flows.
- Liquidity pool management and target balance policy.
- Cash concentration and sweep planning.
- Payment funding proposal and release authorization.
- Intercompany netting and in-house bank settlement.
- FX exposure capture, hedge recommendation, and hedge accounting evidence.
- Debt facility drawdown, repayment, covenant, and interest schedule tracking.
- Short-term investment placement and maturity tracking.
- Bank fee analysis and anomaly detection.
- Signatory, approval, and segregation-of-duties controls.
- Counterparty and bank risk scoring.
- Treasury workbench summary with cash, risk, funding, and exception metrics.
- Audit trail, idempotency keys, retry/dead-letter evidence, and immutable
  event contracts.
- Configuration for currencies, calendars, liquidity thresholds, and risk
  appetite.
- Executable treasury rules, runtime parameters, permission descriptors, seed
  data, and workbench views for every operator-facing flow.

## Advanced Capabilities

- Event-sourced cash lifecycle across balances, forecasts, funding,
  investments, debt, hedges, sweeps, and settlements.
- Graph-relational bank and counterparty topology with exposure propagation.
- Multi-tenant liquidity isolation with independent pools and policies.
- Schema-evolution resilient cash-flow schema for dynamic source attributes.
- Probabilistic cash forecasting with confidence bands.
- Real-time liquidity optimization across available cash, working-capital
  obligations, target balances, and funding cost.
- Counterfactual funding and investment scenario analysis.
- Temporal cash-flow stochastic modeling.
- Autonomous bank-statement reconciliation and exception suggestions.
- Semantic bank narrative parsing for unstructured statement references.
- Predictive counterparty, bank, and liquidity risk scoring.
- Self-healing payment rail and bank-channel routing.
- Zero-knowledge liquidity covenant proof.
- Immutable bank connectivity and regulatory audit trail.
- Dynamic sanction, fraud, and bank-network screening.
- Automated treasury control testing.
- Universal API and async event contracts for cash, funding, hedge, and
  statement flows.
- Cross-border liquidity federation using ISO 20022-style message evidence.
- Supply-chain and working-capital finance integration evidence.
- Decentralized counterparty identity verification.
- Chaos-engineered bank-rail tolerance.
- Crypto-agile payment and treasury authorization.
- Carbon-aware liquidity movement scheduling.
- Algebraic liquidity optimization with multi-objective scoring.
- Mechanism-design funding allocation across entities and counterparties.
- Information-theoretic cash-flow anomaly detection.
- Temporal liquidity stochastic modeling.
- Distributed systems engineering for idempotent multi-region cash state.
- Probabilistic ML for liquidity and counterparty risk.
- Cryptographic engineering for proofs and signatures.
- Mathematical optimization for funding, sweeping, and hedging.
- Financial MLOps governance for regulated treasury models.

## Owned Runtime Boundary

All executable implementation lives in this directory. The catalog may re-export
stable helpers for compatibility, but cash state, runtime smoke evidence,
standard feature inventory, and advanced capability evidence are owned here.

## Owned Datastore Boundary

The PBC owns:

- `treasury_cash_bank_account`: account, legal entity, currency, country, bank
  identifier, signatory metadata, risk signals, identity, and status.
- `treasury_cash_balance`: opening, intraday, and closing balances by value
  date, account, currency, kind, source, and capture status.
- `treasury_cash_statement`: statement header, immutable hash-chain lines,
  narrative parse evidence, reconciliation status, and exception references.
- `treasury_cash_cash_position`: tenant, entity, currency, account, value date,
  available cash, restricted cash, forecast confidence, and source lineage.
- `treasury_cash_liquidity_plan`: target balance, funding source, sweep,
  concentration, intercompany netting, and in-house bank settlement evidence.
- `treasury_cash_capital_action`: investment placement, debt draw, repayment,
  fee analysis, hedge recommendation, approval evidence, and maturity schedule.
- `treasury_cash_outbox`, `treasury_cash_inbox`, and
  `treasury_cash_dead_letter`: AppGen-X event contract tables for exactly-once
  handlers, retries, and dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, status, and
scope-specific predicates such as minimum liquidity buffer, dual approval,
counterparty risk threshold, funding authorization, rail availability,
investment limits, debt draw limits, FX hedge trigger, and release-gate
constraints.

Parameters include `minimum_liquidity_buffer`,
`counterparty_risk_threshold`, `cash_forecast_confidence_floor`,
`funding_approval_limit`, `fx_exposure_threshold`, and `workbench_limit`.

Configuration includes database backend, fixed AppGen-X event topic, retry
limit, default currency, default timezone, allowed payment rails, and workbench
limits. The only valid ordinary event topic is
`appgen.treasury_cash.events`. Runtime configuration rejects unsupported
databases, user-selectable stream engines, alternate event transports, and any
field that would expose an eventing picker to users. The configuration evidence
records `event_contract: AppGen-X`, the PostgreSQL/MySQL/MariaDB backend
allowlist, hidden stream-engine picker state, and the package-owned tables used
by runtime generation.

## Public APIs

- `POST /treasury/bank-accounts`
- `POST /treasury/balances`
- `POST /treasury/statements`
- `POST /treasury/statements/{id}/reconcile`
- `GET /treasury/cash-position`
- `POST /treasury/forecasts`
- `POST /treasury/liquidity/optimize`
- `POST /treasury/payment-rails/route`
- `POST /treasury/investments`
- `POST /treasury/debt-draws`
- `POST /treasury/fx/hedge-recommendations`
- `GET /treasury/workbench`

## Events

Emitted events:

- `BankAccountRegistered`
- `BankBalanceCaptured`
- `BankStatementIngested`
- `CashPositionBuilt`
- `PaymentFunded`
- `InvestmentPlaced`
- `DebtFacilityDrawn`

Consumed events:

- `PaymentFundingRequested`
- `ReceivableCashForecasted`
- `PayablePaymentScheduled`
- `PayrollFundingRequested`
- `TaxPaymentScheduled`
- `FxRateChanged`
- `AccessPolicyChanged`

Handlers are idempotent by `treasury_cash:{event_type}:{event_id}`, retry at
least three times, and write failures to `treasury_cash_dead_letter`.
Consumed events are stored first in `treasury_cash_appgen_inbox_event`, then
projected into package-owned read models:

- `PaymentFundingRequested` creates a payment funding projection for liquidity
  release decisions.
- `ReceivableCashForecasted` creates a receivable forecast projection for cash
  forecasting and confidence-band planning.
- `PayablePaymentScheduled` creates a payable payment projection used for
  near-term funding and bank-rail planning.
- `PayrollFundingRequested` creates a payroll funding projection for protected
  workforce cash needs.
- `TaxPaymentScheduled` creates a tax payment projection for statutory
  liquidity holds.
- `FxRateChanged` creates an FX-rate projection for exposure and hedge
  recommendations.
- `AccessPolicyChanged` creates an access-policy projection for runtime UI and
  API authorization.

Duplicate events return the existing processed handler and do not mutate
state. Unsupported or failing events record retry evidence and move to
`treasury_cash_dead_letter_event` after the configured retry limit.

## API, Permission, and Boundary Contract

The descriptor API contract is generated by the package and lists every route
with command/query name, owned tables, emitted or consumed events, required
permission, and idempotency key where applicable. Routes cover bank account
registration, balance capture, statement ingestion, reconciliation, cash
position, forecasting, liquidity optimization, payment-rail routing,
investments, debt draws, event inbox processing, and workbench reads.

The permission contract binds commands to granular permissions:
`treasury_cash.bank`, `treasury_cash.balance`, `treasury_cash.statement`,
`treasury_cash.reconcile`, `treasury_cash.position`,
`treasury_cash.forecast`, `treasury_cash.funding`,
`treasury_cash.payment`, `treasury_cash.investment`,
`treasury_cash.debt`, `treasury_cash.fx`, `treasury_cash.event`,
`treasury_cash.configure`, and `treasury_cash.audit`.

`verify_owned_table_boundary` proves that runtime references are limited to
Treasury Cash owned tables, AppGen-X runtime event tables, declared consumed
events, or explicitly declared API/projection dependencies. Cross-PBC
integration must use APIs, events, and projections; shared tables are not
allowed.

## UI and Workbench

The UI exposes a treasury cash workbench, bank account console, balance capture
board, bank statement reconciliation board, cash position view, liquidity
forecast workbench, funding optimization console, payment-rail routing panel,
intercompany netting view, FX exposure and hedge panel, debt facility console,
investment placement console, counterparty risk panel, treasury rule studio,
treasury parameter console, and configuration panel. Actions are
permission-bound and rendered from package-owned state.

## Release Evidence

Release readiness requires passing runtime smoke, package-local UI contract,
owned tables, API/event/handler surfaces, AppGen-X event contract evidence,
configuration/rule/parameter execution, generated DSL compatibility, package
metadata, workbench rendering, and focused unit tests.
