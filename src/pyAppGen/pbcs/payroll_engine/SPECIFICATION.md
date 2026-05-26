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
- `payroll_period`
- `payroll_pay_group`
- `payroll_legal_entity`
- `payroll_run`
- `payroll_run_worker`
- `payroll_run_approval`
- `payroll_run_lock`
- `worker_projection`
- `worker_pay_profile`
- `worker_bank_instruction`
- `labor_hours`
- `labor_hours_line`
- `earning_code`
- `earning_calculation`
- `overtime_calculation`
- `gross_pay_component`
- `payslip`
- `payslip_line`
- `tax_withholding_projection`
- `deduction`
- `deduction_rule`
- `deduction_arrear`
- `garnishment_order`
- `benefit_allocation`
- `benefit_plan`
- `employer_contribution`
- `net_pay_distribution`
- `payment_instruction`
- `payment_batch_projection`
- `journal_request_projection`
- `tax_wage_base_projection`
- `payroll_filing`
- `payroll_filing_line`
- `payroll_correction`
- `retro_adjustment`
- `off_cycle_payment`
- `payroll_exception`
- `payroll_policy_screening`
- `payroll_audit_trace`
- `payroll_proof`
- `payroll_federation_projection`
- `payroll_carbon_batch_window`
- `payroll_batch_optimization`
- `payroll_cash_allocation`
- `payroll_anomaly_signal`
- `payroll_risk_model`
- `payroll_cash_forecast`
- `payroll_parsed_instruction`
- `payroll_seed_data`
- `payroll_schema_extension`
- `payroll_control_assertion`
- `payroll_governed_model`
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
- Payroll periods, pay groups, legal entities, payroll run rosters, run approvals, and run locks.
- Worker payroll projection from personnel identity evidence.
- Worker pay profiles, bank instructions, pay group eligibility, and country/currency controls.
- Labor-hours ingestion from AppGen-X events or direct package-local command paths.
- Labor-hour lines, earning code catalogs, earning calculations, overtime calculations, and gross-pay components.
- Hourly, salary, overtime, supplemental, and off-cycle gross-pay calculation.
- Tax withholding projection and gross-to-net payslip calculation.
- Payslip lines for earnings, taxes, deductions, benefits, net-pay distributions, and corrections.
- Deduction handling for retirement, garnishment, court, tax, loan, and post-tax deductions with rule-based limits.
- Deduction rules, arrears, and garnishment-order priority evidence.
- Benefit allocation with employer and employee contribution tracking.
- Benefit plans and employer contribution evidence.
- Net pay floor enforcement and payroll precision support.
- Payment instructions, payment-batch projections, and treasury handoff readiness.
- Payslip generation with gross, tax, deduction, benefit, net-pay, risk, currency, and status fields.
- Approval workflow and payroll posting control.
- Filing preparation by jurisdiction and statutory channel.
- Filing lines, filing materiality, and jurisdiction-level filing evidence.
- Treasury payment-batch readiness without treasury table access.
- Ledger journal request readiness without ledger table access.
- Tax wage-base projection handoff without tax table access.
- Retroactive adjustment and off-cycle payroll policy support through rules and parameters.
- Payroll corrections, payroll exceptions, policy screening, audit traces, payroll proofs, federation projections, carbon-aware batch windows, batch optimization, cash allocation, anomaly signals, risk models, cash forecasts, parsed instruction evidence, control assertions, governed model metadata, seed data, and schema extensions.
- Multi-tenant and multi-entity isolation.
- AppGen-X inbox/outbox idempotency and dead-letter evidence.
- RBAC descriptors for run, approval, filing, event, configuration, and audit actions.
- Package-local workbench UI for runs, payslips, deductions, benefits, filings, rules, parameters, configuration, and event evidence.

## Generated Schema, Services, And Release Evidence

`build_schema_contract` emits field definitions, relationships, migration paths
under `pbcs/payroll_engine/migrations/`, generated model names, backend
allowlists, and `shared_table_access: false` for every owned table. The
schema contract covers calendar, period, pay group, legal entity, runs, run
workers, approvals, locks, workers, pay profiles, bank instructions, labor
hours, earning codes, overtime, gross components, payslips, taxes, deductions,
arrears, garnishments, benefits, employer contributions, net distributions,
payment instructions, payment batches, journal requests, tax wage bases,
filings, corrections, retro adjustments, off-cycle payments, exceptions,
policy screening, audit trace, proofs, federation, carbon windows,
optimization, cash allocation, anomaly, risk, forecast, parsed instructions,
seed data, extensions, controls, governed models, rules, parameters,
configuration, outbox, inbox, and dead-letter artifacts.

`build_service_contract` declares the transaction boundary as the Payroll
Engine owned datastore plus the AppGen-X outbox. Commands configure runtime
state, set parameters, register rules and schema extensions, receive events,
maintain worker projections, open payroll runs, ingest labor hours, calculate
payslips, apply deductions, allocate benefits, post payroll, prepare filings,
route payment or filing work, generate payroll proofs, screen policy, federate
payroll views, verify worker identity, run resilience drills, rotate crypto
epochs, schedule carbon-aware batches, optimize payroll batches, allocate cash,
run controls, register governed models, and verify owned-table boundaries.
Query methods cover workbench views, pay-policy simulation, cash forecasting,
semantic instruction parsing, payroll-risk scoring, exception recommendations,
anomaly detection, stochastic exposure, and generated API/schema/release
contracts. External dependencies are declared APIs, consumed AppGen-X events,
and package-local projections only; shared tables are forbidden.

`build_release_evidence` combines schema, service, API, and RBAC evidence into
release checks for owned schema depth, migration coverage, command depth,
fixed AppGen-X eventing, permission coverage for key commands, backend
allowlist, and no shared-table access. A Payroll Engine release is valid only
when all checks pass and `blocking_gaps` is empty.

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

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `payroll_engine`
- Mesh: `hcm`
- Datastore backend: `None`

### Owned Tables

- `payroll_calendar`
- `payroll_period`
- `payroll_pay_group`
- `payroll_legal_entity`
- `payroll_run`
- `payroll_run_worker`
- `payroll_run_approval`
- `payroll_run_lock`
- `worker_projection`
- `worker_pay_profile`
- `worker_bank_instruction`
- `labor_hours`
- `labor_hours_line`
- `earning_code`
- `earning_calculation`
- `overtime_calculation`
- `gross_pay_component`
- `payslip`
- `payslip_line`
- `tax_withholding_projection`
- `deduction`
- `deduction_rule`
- `deduction_arrear`
- `garnishment_order`
- `benefit_allocation`
- `benefit_plan`
- `employer_contribution`
- `net_pay_distribution`
- `payment_instruction`
- `payment_batch_projection`
- `journal_request_projection`
- `tax_wage_base_projection`
- `payroll_filing`
- `payroll_filing_line`
- `payroll_correction`
- `retro_adjustment`
- `off_cycle_payment`
- `payroll_exception`
- `payroll_policy_screening`
- `payroll_audit_trace`
- `payroll_proof`
- `payroll_federation_projection`
- `payroll_carbon_batch_window`
- `payroll_batch_optimization`
- `payroll_cash_allocation`
- `payroll_anomaly_signal`
- `payroll_risk_model`
- `payroll_cash_forecast`
- `payroll_parsed_instruction`
- `payroll_seed_data`
- `payroll_schema_extension`
- `payroll_control_assertion`
- `payroll_governed_model`
- `payroll_rule`
- `payroll_parameter`
- `payroll_configuration`
- `payroll_engine_appgen_outbox_event`
- `payroll_engine_appgen_inbox_event`
- `payroll_engine_dead_letter_event`

### API Routes

- `POST /payroll-runs`
- `POST /payroll-runs/{id}/workers`
- `POST /payroll-runs/{id}/payslips`
- `POST /payslips/{id}/deductions`
- `POST /payslips/{id}/benefits`
- `POST /payroll-runs/{id}/post`
- `POST /payroll-filings`
- `POST /payroll/events/inbox`
- `POST /payroll-rules`
- `POST /payroll-parameters`
- `POST /payroll-configuration`
- `GET /payslips`
- `GET /payroll-workbench`

### Emitted Events

- `PayrollPosted`
- `PayrollFilingPrepared`

### Consumed Events

- `LaborHoursApproved`
- `TaxCalculated`

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
