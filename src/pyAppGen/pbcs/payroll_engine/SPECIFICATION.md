# Payroll Engine

Package-local implementation contract for the Payroll Engine PBC. The package owns gross-to-net payroll execution, worker payroll projections, labor-hour intake, payslips, deductions, benefits, payroll postings, filing preparation, event evidence, rules, parameters, configuration, UI fragments, and release validation.

## Stable Identity

- PBC key: `payroll_engine`.
- Mesh: people/HCM.
- Implementation directory: `src/pyAppGen/pbcs/payroll_engine`.
- Runtime module: `runtime.py`.
- UI module: `ui.py`.
- Test module: `tests/test_pbc_payroll_engine_runtime.py`.
- Event topic: `appgen.payroll.events`.
- Event contract: AppGen-X.
- Supported relational backends: PostgreSQL, MySQL, and MariaDB.
- User-facing stream-engine selection is not exposed.

## Owned Boundary

Owned tables and generated model artifacts:

- `payroll_calendar`
- `payroll_run`
- `worker_projection`
- `labor_hours`
- `payslip`
- `deduction`
- `benefit_allocation`
- `payroll_filing`
- `payroll_rule`
- `payroll_parameter`
- `payroll_configuration`
- `payroll_engine_appgen_outbox_event`
- `payroll_engine_appgen_inbox_event`
- `payroll_engine_dead_letter_event`

The PBC does not share personnel, time/labor, tax, treasury, ledger, or audit tables. Cross-PBC integration is represented only by declared APIs, events, or projections:

- Consumed events: `LaborHoursApproved`, `TaxCalculated`.
- API dependencies: `GET /workers`, `GET /labor-hours`, `GET /tax-rates`, `POST /payment-batches`, `POST /journal-requests`.
- Projections and handoffs: `personnel_identity_projection`, `time_labor_projection`, `tax_wage_base_projection`, `treasury_payment_batch`, `ledger_journal_request`, and `audit_ledger_projection`.
- Emitted events: `PayrollPosted`, `PayrollFilingPrepared`.

## Standard Capabilities

- Payroll calendar and payroll run creation by tenant, legal entity, country, period, currency, and run type.
- Worker payroll projection from personnel identity evidence.
- Labor-hours ingestion from AppGen-X events or direct package-local command paths.
- Hourly, salary, overtime, supplemental, and off-cycle gross-pay calculation.
- Tax withholding projection and gross-to-net payslip calculation.
- Deduction handling for retirement, garnishment, court, tax, loan, and post-tax deductions with rule-based limits.
- Benefit allocation with employer and employee contribution tracking.
- Net pay floor enforcement and payroll precision support.
- Payslip generation with gross, tax, deduction, benefit, net-pay, risk, currency, and status fields.
- Approval workflow and payroll posting control.
- Filing preparation by jurisdiction and statutory channel.
- Treasury payment-batch readiness without treasury table access.
- Ledger journal request readiness without ledger table access.
- Tax wage-base projection handoff without tax table access.
- Retroactive adjustment and off-cycle payroll policy support through rules and parameters.
- Multi-tenant and multi-entity isolation.
- AppGen-X inbox/outbox idempotency and dead-letter evidence.
- RBAC descriptors for run, approval, filing, event, configuration, and audit actions.
- Package-local workbench UI for runs, payslips, deductions, benefits, filings, rules, parameters, configuration, and event evidence.

## Advanced Capabilities

- Event-sourced payroll lifecycle with immutable hash-chain audit trail.
- Graph-relational compensation topology across worker, run, payslip, deduction, benefit, tax, and posting projections.
- Probabilistic payroll anomaly and compliance risk scoring.
- Real-time gross-to-net analytics in the workbench.
- Counterfactual pay-policy simulation for overtime and projected gross pay.
- Temporal payroll cash forecasting and stochastic payroll exposure modeling.
- Autonomous payroll exception recommendations for negative net, missing tax, and payment failure.
- Semantic payroll instruction parsing.
- Predictive payroll compliance and liquidity risk scoring.
- Self-healing payment and filing route selection.
- Zero-knowledge payroll proof generation for limited disclosure of payslip facts.
- Dynamic policy screening by jurisdiction and status.
- Automated payroll control testing for configuration, rules, parameters, net-pay floor, and hash-chain integrity.
- Universal API and AppGen-X event contracts.
- Cross-system payroll federation through declared projections.
- Treasury, tax, and ledger integration through handoff artifacts.
- Decentralized worker-pay identity verification using DID-like identity evidence.
- Chaos-engineered payment and filing route tolerance.
- Quantum-resistant authorization simulation through crypto-agile epoch rotation.
- Carbon-aware payroll batch scheduling.
- Algebraic payroll batch optimization.
- Mechanism-design cash allocation across payroll and statutory claims.
- Information-theoretic payroll anomaly detection.
- Governed payroll model registration with feature lineage, drift, and explainability controls.

## Runtime Services

- `configure_runtime` validates backend, exact AppGen-X event topic, retry limit, currency, country, payment-rail, filing-channel, precision, workbench, and stream-picker absence.
- `set_parameter` accepts only supported payroll parameters.
- `register_rule` validates rule identity, tenant, status, and pay-rule scope and stores deterministic compiled evidence.
- `register_schema_extension` accepts only owned-table schema extensions.
- `receive_event` idempotently handles `LaborHoursApproved` and `TaxCalculated`, records inbox evidence, schedules retries, and dead-letters exhausted failures.
- `upsert_worker_projection` owns worker payroll projection.
- `create_payroll_run` opens a payroll run if country and rule policy allow it.
- `ingest_labor_hours` records approved labor hours.
- `calculate_payslip` computes gross pay, tax withholding, net pay, risk score, and payslip state.
- `apply_deduction` enforces deduction limits and updates net pay.
- `allocate_benefit` validates benefit class and updates employee/employer benefit totals.
- `post_payroll_run` posts approved runs and emits treasury, ledger, and tax handoff evidence.
- `prepare_payroll_filing` creates statutory filing artifacts and emits `PayrollFilingPrepared`.
- `build_api_contract` emits descriptor-level route, permission, idempotency, event, dependency, and owned-table evidence.
- `permissions_contract` maps runtime commands to RBAC permissions.
- `verify_owned_table_boundary` accepts owned tables and declared API/event/projection dependencies, then reports direct foreign-table violations.
- `build_workbench_view` exposes operational and release evidence.

## API Contract

- `POST /payroll-runs` maps to `create_payroll_run`.
- `POST /payroll-runs/{id}/payslips` maps to `calculate_payslip`.
- `POST /payslips/{id}/deductions` maps to `apply_deduction`.
- `POST /payslips/{id}/benefits` maps to `allocate_benefit`.
- `POST /payroll-runs/{id}/post` maps to `post_payroll_run`.
- `POST /payroll-filings` maps to `prepare_payroll_filing`.
- `POST /payroll/events/inbox` maps to `receive_event`.
- `GET /payslips` maps to `build_workbench_view`.
- `GET /payroll-workbench` maps to `build_workbench_view`.

Every route descriptor includes owned tables, command or query binding, idempotency key where applicable, required permission, emitted events, consumed events, and dependency evidence.

## Events And Handlers

Emitted events:

- `PayrollPosted`
- `PayrollFilingPrepared`

Consumed events:

- `LaborHoursApproved`
- `TaxCalculated`

Handlers are idempotent by idempotency key or event type and event id. Duplicate processed events do not create duplicate state changes. Failed events record retry evidence until the configured retry limit and then produce dead-letter records.

## Rules, Parameters, And Configuration

Rules cover pay eligibility, worker type, allowed countries, deduction limit percentage, benefit classes, filing channels, garnishment priority, off-cycle eligibility, approval requirements, and status.

Parameters include:

- `standard_period_hours`
- `overtime_multiplier`
- `supplemental_rate`
- `rounding_precision`
- `net_pay_floor`
- `filing_materiality_threshold`
- `approval_amount_threshold`
- `off_cycle_approval_threshold`
- `retro_lookback_periods`
- `workbench_limit`

Configuration includes database backend, event topic, retry limit, default currency, allowed countries, allowed payment rails, allowed filing channels, payroll precision, and workbench limit. Runtime configuration records `event_contract: AppGen-X`, allowed relational backends, hidden stream-engine picker evidence, non-selectable event-contract evidence, and owned tables.

## UI And Workbench

UI fragments:

- `PayrollEngineWorkbench`
- `PayrollRunConsole`
- `PayslipReviewBoard`
- `DeductionEditor`
- `BenefitAllocationPanel`
- `PayrollFilingConsole`
- `PayrollRuleStudio`
- `PayrollParameterConsole`
- `PayrollConfigurationPanel`

The workbench exposes payroll-run, payslip, deduction, benefit, filing, inbox, outbox, dead-letter, configuration, rule, parameter, and owned-boundary evidence. Visible actions are RBAC-filtered by payroll run, approval, filing, event, configuration, and audit permissions.

## Release Evidence

The focused test suite proves:

- Runtime smoke covers every declared standard and advanced capability key.
- The package declares owned tables, allowed relational backends, fixed AppGen-X eventing, descriptor APIs, and action-level RBAC.
- Configuration, parameters, rules, schema extensions, event handling, worker projection, labor intake, payslip calculation, deductions, benefits, posting, filing, UI, and workbench evidence execute.
- Boundary validation accepts owned tables and declared API/event/projection dependencies, then rejects direct foreign-table references.
- Invalid backend, stream-picker configuration, unsupported parameters, non-owned schema extensions, idempotent duplicates, retries, and dead letters are verified.
