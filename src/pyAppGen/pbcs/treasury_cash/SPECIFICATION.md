# Treasury and Cash Management PBC

## Purpose

`treasury_cash` owns enterprise cash visibility, bank connectivity, statement
ingestion, reconciliation, cash positioning, forecasting, liquidity planning,
payment funding, payment-rail routing, cash sweeping, concentration,
intercompany netting, in-house banking, FX exposure, hedge recommendations,
debt facilities, investments, bank fees, counterparty risk, covenant evidence,
working-capital finance, cross-border liquidity, controls, rules, parameters,
configuration, governed models, and treasury workbench evidence.

The package is a composable PBC. It integrates with payables, receivables,
payroll, tax, identity, schema, audit, and gateway capabilities only through
declared APIs, AppGen-X events, and read-only projections. It does not share
tables with other PBCs or bank adapters.

## Owned Datastore Boundary

The runtime owns the following tables. Every table is represented in the
schema contract, has generated migration evidence, and has a generated model:

- `treasury_cash_bank_account`: account, legal entity, bank, country,
  currency, status, and risk score.
- `treasury_cash_bank_account_signatory`: account signatories, roles,
  approval limits, and active state.
- `treasury_cash_bank_counterparty`: bank counterparty master, rating, risk,
  country, and identity proof.
- `treasury_cash_bank_topology`: bank network, accounts, signatories,
  topology hash, and risk context.
- `treasury_cash_balance`: opening, intraday, and closing balances by account,
  value date, currency, kind, and status.
- `treasury_cash_intraday_balance`: observed intraday balances, timestamp,
  source, and currency.
- `treasury_cash_statement`: statement header, account, date, status, and hash
  chain root.
- `treasury_cash_statement_line`: statement amount, narrative, currency, and
  line hash.
- `treasury_cash_reconciliation_match`: statement-to-flow matches, confidence,
  and status.
- `treasury_cash_reconciliation_exception`: unmatched line reason and
  resolution state.
- `treasury_cash_cash_position`: value-date position, currency, available
  cash, restricted cash, and confidence.
- `treasury_cash_cash_forecast`: forecast horizon, currency, confidence, and
  model version.
- `treasury_cash_cash_forecast_line`: period amount and confidence bands.
- `treasury_cash_liquidity_pool`: pool target, available cash, currency, and
  policy state.
- `treasury_cash_liquidity_plan`: target balance, funding source, and
  optimization score.
- `treasury_cash_sweep_instruction`: source/target accounts, amount, and
  sweep state.
- `treasury_cash_concentration_run`: pool concentration date, total swept, and
  run status.
- `treasury_cash_intercompany_netting`: entity pair, amount, currency, and
  settlement status.
- `treasury_cash_in_house_bank_account`: entity-owned internal bank account,
  currency, balance, and status.
- `treasury_cash_payment_funding`: funded payment reference, amount, source,
  and approval state.
- `treasury_cash_payment_rail_route`: selected rail, cost, latency, risk, and
  idempotency key.
- `treasury_cash_fx_exposure`: currency pair, exposure amount, volatility, and
  value date.
- `treasury_cash_hedge_recommendation`: hedge instrument, amount, ratio, and
  linked exposure.
- `treasury_cash_capital_action`: investment, debt, hedge, or funding action
  with amount and approval state.
- `treasury_cash_debt_facility`: facility counterparty, limit, availability,
  rate, and covenant state.
- `treasury_cash_debt_draw`: draw amount, rate, daily interest, and status.
- `treasury_cash_investment`: placed amount, yield, maturity, expected
  interest, and status.
- `treasury_cash_bank_fee`: account fee amount, fee type, and anomaly score.
- `treasury_cash_covenant_proof`: position proof hash, minimum liquidity, and
  covenant result.
- `treasury_cash_cross_border_liquidity`: target country, settlement amount,
  and message evidence.
- `treasury_cash_working_capital_finance`: program, eligible amount, advance
  amount, and counterparty.
- `treasury_cash_counterparty_risk_signal`: risk signal, score, and
  observation time.
- `treasury_cash_policy_rule`: policy rule, scope, status, predicate, and
  compiled hash.
- `treasury_cash_rule`: executable treasury rule, scope, status, predicate,
  and compiled hash.
- `treasury_cash_parameter`: bounded parameter value and compiled hash.
- `treasury_cash_configuration`: database backend, AppGen-X topic, retry
  limit, and default currency.
- `treasury_cash_schema_extension`: owned table extension field and version.
- `treasury_cash_control_assertion`: continuous treasury control result and
  evidence hash.
- `treasury_cash_governed_model`: model lineage, drift score, and governance
  state.
- `treasury_cash_appgen_outbox_event`: emitted AppGen-X event and idempotency
  key.
- `treasury_cash_appgen_inbox_event`: consumed AppGen-X event, attempts, and
  status.
- `treasury_cash_dead_letter_event`: failed event, attempts, and reason.

Supported ordinary backing stores are PostgreSQL, MySQL, and MariaDB. The
runtime rejects other backends.

## Standard Capabilities

The PBC implements the expected treasury and cash table-stakes:

- Bank account master data, bank counterparties, signatory controls, bank
  topology, and counterparty risk.
- Opening, intraday, and value-date balance capture.
- Bank statement ingestion, line hash chains, semantic narrative parsing,
  reconciliation matching, and exception management.
- Cash position by tenant, account, currency, and value date.
- Cash forecast with confidence bands from payables, receivables, payroll, tax,
  FX, and manual projections.
- Liquidity pools, target balances, optimization, sweeps, concentration, cash
  pooling, in-house banking, and intercompany netting.
- Payment funding, release authorization, and payment-rail routing.
- FX exposure capture, hedge recommendation, debt facilities, debt draws,
  investment placement, maturity evidence, and bank fee analysis.
- Covenant proof, working-capital finance, cross-border liquidity, approval
  controls, audit trail, and workbench evidence.
- Executable configuration, rules, parameters, schema extensions, permissions,
  seedable state, AppGen-X inbox/outbox, idempotent handlers, retries, and
  dead-letter evidence.

## Advanced Capabilities

The runtime proves advanced treasury behavior:

- Event-sourced cash lifecycle across accounts, balances, statements,
  positions, forecasts, funding, investments, debt, and capital actions.
- Graph-relational bank topology with signatory and counterparty exposure
  propagation.
- Multi-tenant liquidity isolation with independent policies and workbench
  views.
- Schema-evolution resilient cash schema with owned extension records.
- Probabilistic cash forecasting with confidence intervals.
- Real-time liquidity optimization across cash pools, payment obligations,
  target balances, funding cost, and risk.
- Counterfactual funding analysis and temporal stochastic liquidity modeling.
- Autonomous reconciliation with semantic bank narrative parsing.
- Predictive counterparty liquidity risk and governed model registration.
- Self-healing payment rail routing with rail availability failover.
- Disclosure-minimized covenant proof and immutable bank connectivity audit.
- Dynamic sanction and fraud screening across bank topology.
- Continuous treasury control testing.
- Universal API and AppGen-X asynchronous event contracts.
- Cross-border liquidity federation and working-capital finance integration.
- Decentralized counterparty identity verification.
- Bank-rail resilience drills, crypto-agile treasury authorization,
  carbon-aware liquidity scheduling, algebraic optimization, mechanism-design
  funding allocation, information-shift cash anomaly detection, formal
  invariants, distributed idempotency, probabilistic liquidity-risk models,
  cryptographic proof evidence, mathematical optimization, and financial model
  governance.

## Rules, Parameters, and Configuration

Configuration is validated by `treasury_cash_configure_runtime`. Required
settings include `database_backend`, `event_topic`, `retry_limit`,
`default_currency`, `default_timezone`, allowed payment rails, and workbench
limits. The ordinary event topic is fixed to
`appgen.treasury_cash.events`; user-facing stream-engine selection is rejected.

Parameters are validated by `treasury_cash_set_parameter`. Supported
parameters include `minimum_liquidity_buffer`,
`counterparty_risk_threshold`, `cash_forecast_confidence_floor`,
`funding_approval_limit`, `fx_exposure_threshold`, and `workbench_limit`.

Rules are registered by `treasury_cash_register_rule`. Rule scopes include
liquidity buffers, dual approval, funding authorization, counterparty risk,
payment rail availability, investment limits, debt draw limits, FX hedge
triggers, reconciliation controls, and release gates.

Schema extensions are accepted only for Treasury-owned tables. Foreign table
extensions fail the boundary check.

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
- `POST /treasury/events/inbox`
- `GET /treasury/workbench`

Declared external dependencies are APIs and projections only:

- `GET /identity/policies`
- `POST /audit/contract-events`
- `GET /schema/events`
- `payment_funding_projection`
- `receivable_forecast_projection`
- `payable_payment_projection`
- `payroll_funding_projection`
- `tax_payment_projection`
- `fx_rate_projection`
- `access_policy_projection`

## Events and Handlers

Emitted AppGen-X events:

- `BankAccountRegistered`
- `BankBalanceCaptured`
- `BankStatementIngested`
- `CashPositionBuilt`
- `PaymentFunded`
- `InvestmentPlaced`
- `DebtFacilityDrawn`

Consumed AppGen-X events:

- `PaymentFundingRequested`
- `ReceivableCashForecasted`
- `PayablePaymentScheduled`
- `PayrollFundingRequested`
- `TaxPaymentScheduled`
- `FxRateChanged`
- `AccessPolicyChanged`

Handlers are idempotent by `treasury_cash:{event_type}:{event_id}`. Failures
retry according to configuration and then write to
`treasury_cash_dead_letter_event`. Duplicate processed events return the
existing handler without mutating state.

## UI and Workbench

The UI exposes a treasury cash workbench, bank account console, signatory
panel, counterparty risk view, balance capture board, bank statement
reconciliation board, reconciliation exception queue, cash position view,
forecast workbench, liquidity pool console, sweep and concentration board,
payment funding console, payment-rail routing panel, intercompany netting
view, in-house bank view, FX exposure and hedge panel, debt facility console,
investment placement console, covenant evidence panel, bank fee anomaly panel,
rule studio, parameter console, schema extension panel, inbox/outbox monitor,
dead-letter triage, configuration panel, and release evidence panel.

Every visible action is permission-bound and rendered from Treasury-owned
state plus declared projections.

## Permissions and RBAC

The permission contract covers read, bank, balance, statement, reconcile,
position, forecast, funding, payment, investment, debt, FX, event, configure,
and audit permissions. Release evidence verifies that critical command methods
such as bank-account registration, balance capture, and event inbox processing
are permission-bound.

## Package Metadata and Self-Registration

The package key is `treasury_cash`. Package metadata advertises the
implementation directory, capabilities, standard features, owned tables,
database allowlist, AppGen-X topic, emitted events, consumed events, UI
fragments, API contract, schema contract, service contract, permissions, and
release evidence. Registration plans for external PBCs remain side-effect-free
and may depend on Treasury only through declared APIs, AppGen-X events, or
projections.

## Release Evidence

Release readiness requires:

- `treasury_cash_runtime_smoke()` returns `ok`.
- `implementation_contract()` includes runtime, UI, API, schema, service,
  permissions, topic, events, and release evidence contracts.
- `treasury_cash_build_schema_contract()` proves all owned tables, models,
  relationships, migrations, backend allowlist, and no shared table access.
- `treasury_cash_build_service_contract()` proves command and query services,
  transaction boundary, owned mutations, and declared external dependencies.
- `treasury_cash_build_release_evidence()` proves schema depth, migration
  coverage, service depth, AppGen-X API/event contract, permission coverage,
  backend allowlist, and shared-table isolation.
- Focused Treasury tests pass.
- The global PBC release audit, implementation release audit, implemented
  capability audit, and generation smoke audit pass for the implemented PBC
  set.
- Diff scans contain no banned legacy product or framework names.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `treasury_cash`
- Mesh: `finops`
- Datastore backend: `None`

### Owned Tables

- `bank_account`
- `bank_account_signatory`
- `bank_counterparty`
- `bank_topology`
- `balance`
- `intraday_balance`
- `statement`
- `statement_line`
- `reconciliation_match`
- `reconciliation_exception`
- `cash_position`
- `cash_forecast`
- `cash_forecast_line`
- `liquidity_pool`
- `liquidity_plan`
- `sweep_instruction`
- `concentration_run`
- `intercompany_netting`
- `in_house_bank_account`
- `payment_funding`
- `payment_rail_route`
- `fx_exposure`
- `hedge_recommendation`
- `capital_action`
- `debt_facility`
- `debt_draw`
- `investment`
- `bank_fee`
- `covenant_proof`
- `cross_border_liquidity`
- `working_capital_finance`
- `counterparty_risk_signal`
- `policy_rule`
- `rule`
- `parameter`
- `configuration`
- `schema_extension`
- `control_assertion`
- `governed_model`

### API Routes

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
- `POST /treasury/events/inbox`
- `GET /treasury/workbench`

### Emitted Events

- `BankAccountRegistered`
- `BankBalanceCaptured`
- `BankStatementIngested`
- `CashPositionBuilt`
- `PaymentFunded`
- `InvestmentPlaced`
- `DebtFacilityDrawn`

### Consumed Events

- `PaymentFundingRequested`
- `ReceivableCashForecasted`
- `PayablePaymentScheduled`
- `PayrollFundingRequested`
- `TaxPaymentScheduled`
- `FxRateChanged`
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

## Agent, Chatbot Skills, And Self-Registration Contract

The `treasury_cash` package exposes a first-class PBC agent and chatbot interface through `agent.py`. The composed application imports these capabilities under the `treasury_cash_skills` namespace so a single application assistant can route help, task guidance, document instruction intake, governed datastore CRUD planning, workbench navigation, and policy explanation back to the owning PBC instead of inventing cross-package mutations. The agent contract is scoped to the `Treasury and Cash Management` boundary and must name the command, permission, owned tables, idempotency key, expected AppGen-X event, and human confirmation requirement before any create, update, or delete plan is eligible to execute.

Document and instruction intake is explicit release evidence. The chatbot can accept uploaded documents, operational notes, or user instructions, extract candidate facts for owned tables such as `treasury_cash_bank_account`, `treasury_cash_bank_account_signatory`, `treasury_cash_bank_counterparty`, `treasury_cash_bank_topology`, `treasury_cash_balance`, `treasury_cash_intraday_balance`, validate those facts against package rules, parameters, configuration, and permissions, and return a side-effect-free mutation preview. The preview is not a write. It is a governed plan that references service operations such as , uses AppGen-X event expectations such as `BankAccountRegistered`, `BankBalanceCaptured`, `BankStatementIngested`, `CashPositionBuilt`, rejects foreign tables, and records whether a read-only query or a confirmed command is required. This keeps AI assistance professional, auditable, and bounded to the PBC datastore.

Self-registration is also part of the specification. `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` must produce a side-effect-free discovery and registration plan for `treasury_cash`. Registration metadata identifies the source package directory, required artifacts, owned datastore, AppGen-X event contract, UI fragments, RBAC descriptors, configuration schema, seed data, tests, and release evidence without mutating the global catalog during discovery. Composition tooling may then register the PBC, merge the `treasury_cash_skills` contribution into the single composed assistant, and expose the workbench UI while preserving owned-table boundaries and declared API/event/projection dependencies.

