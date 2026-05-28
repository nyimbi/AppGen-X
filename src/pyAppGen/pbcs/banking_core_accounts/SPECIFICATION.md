# Banking Core Accounts PBC

## Purpose

The `banking_core_accounts` PBC is a packaged business capability for Deposit accounts, balances, holds, interest, fees, statements, customer account servicing, and account controls. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `banking_core_accounts`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/banking_core_accounts`.
- Runtime entrypoint: `banking_core_accounts_runtime_capabilities()`.
- UI entrypoint: `banking_core_accounts_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `banking_core_accounts_deposit_account`: owns deposit account lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_account_balance`: owns account balance lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_account_hold`: owns account hold lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_interest_accrual`: owns interest accrual lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_fee_assessment`: owns fee assessment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_statement_cycle`: owns statement cycle lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_account_service_case`: owns account service case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_banking_core_accounts_policy_rule`: owns banking core accounts policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_banking_core_accounts_runtime_parameter`: owns banking core accounts runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_banking_core_accounts_schema_extension`: owns banking core accounts schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_banking_core_accounts_control_assertion`: owns banking core accounts control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `banking_core_accounts_banking_core_accounts_governed_model`: owns banking core accounts governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `banking_core_accounts_appgen_outbox_event`, `banking_core_accounts_appgen_inbox_event`, and `banking_core_accounts_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /deposit-accounts', 'POST /account-balances', 'POST /account-holds', 'POST /interest-accruals', 'POST /fee-assessments', 'GET /banking-core-accounts-workbench').

## Executable Domain Operations

- `create_deposit_account`: validates policy, writes owned `banking_core_accounts_deposit_account` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_account_balance`: validates policy, writes owned `banking_core_accounts_account_balance` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_account_hold`: validates policy, writes owned `banking_core_accounts_account_hold` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_interest_accrual`: validates policy, writes owned `banking_core_accounts_interest_accrual` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_fee_assessment`: validates policy, writes owned `banking_core_accounts_fee_assessment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_statement_cycle`: validates policy, writes owned `banking_core_accounts_statement_cycle` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_account_service_case`: validates policy, writes owned `banking_core_accounts_account_service_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_banking_core_accounts_policy_rule`: validates policy, writes owned `banking_core_accounts_banking_core_accounts_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_banking_core_accounts_runtime_parameter`: validates policy, writes owned `banking_core_accounts_banking_core_accounts_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_banking_core_accounts_schema_extension`: validates policy, writes owned `banking_core_accounts_banking_core_accounts_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_banking_core_accounts_control_assertion`: validates policy, writes owned `banking_core_accounts_banking_core_accounts_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_banking_core_accounts_governed_model`: validates policy, writes owned `banking_core_accounts_banking_core_accounts_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_banking_core_accounts_13`: validates policy, writes owned `banking_core_accounts_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_banking_core_accounts_14`: validates policy, writes owned `banking_core_accounts_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_banking_core_accounts_15`: validates policy, writes owned `banking_core_accounts_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_banking_core_accounts_16`: validates policy, writes owned `banking_core_accounts_deposit_account` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_banking_core_accounts_17`: validates policy, writes owned `banking_core_accounts_account_balance` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_banking_core_accounts_18`: validates policy, writes owned `banking_core_accounts_account_hold` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Banking Core Accounts domain records.
- Multi-tenant policy isolation with owned table boundaries.
- Schema evolution resilience through package-local schema extensions.
- Autonomous anomaly detection and specialist exception triage.
- Semantic document and instruction understanding for professional intake.
- Predictive risk scoring and confidence-ranked recommendations.
- Counterfactual scenario simulation for policy and operational choices.
- Cryptographic audit proofs for high-value records and decisions.
- Continuous control testing over domain lifecycle events.
- Carbon and sustainability awareness where operational decisions affect footprint.
- Cross-PBC event federation through AppGen-X only.
- Governed AI agent execution with human confirmation for mutations.

## Rules, Parameters, and Configuration

Rules are first-class artifacts: ('deposit_account_policy', 'account_balance_policy', 'account_hold_policy', 'interest_accrual_policy', 'fee_assessment_policy', 'statement_cycle_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /deposit-accounts', 'POST /account-balances', 'POST /account-holds', 'POST /interest-accruals', 'POST /fee-assessments', 'GET /banking-core-accounts-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `banking_core_accounts_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('BankingCoreAccountsCreated', 'BankingCoreAccountsUpdated', 'BankingCoreAccountsApproved', 'BankingCoreAccountsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('deposit account board', 'account balance board', 'account hold board', 'interest accrual board', 'fee assessment board', 'statement cycle board', 'account service case board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `banking_core_accounts_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: deposit_account, account_balance, account_hold, interest_accrual, fee_assessment, statement_cycle, account_service_case, banking_core_accounts_policy_rule, banking_core_accounts_runtime_parameter, banking_core_accounts_schema_extension, banking_core_accounts_control_assertion, banking_core_accounts_governed_model
- operations: create_deposit_account, record_account_balance, review_account_hold, approve_interest_accrual, simulate_fee_assessment, create_statement_cycle, record_account_service_case, review_banking_core_accounts_policy_rule, approve_banking_core_accounts_runtime_parameter, simulate_banking_core_accounts_schema_extension, create_banking_core_accounts_control_assertion, record_banking_core_accounts_governed_model, operate_banking_core_accounts_13, operate_banking_core_accounts_14, operate_banking_core_accounts_15, operate_banking_core_accounts_16, operate_banking_core_accounts_17, operate_banking_core_accounts_18
- emits: BankingCoreAccountsCreated, BankingCoreAccountsUpdated, BankingCoreAccountsApproved, BankingCoreAccountsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: deposit_account_policy, account_balance_policy, account_hold_policy, interest_accrual_policy, fee_assessment_policy, statement_cycle_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: BankingCoreAccountsWorkbench, BankingCoreAccountsDetail, BankingCoreAccountsAssistantPanel
- permissions: banking_core_accounts.read, banking_core_accounts.create, banking_core_accounts.update, banking_core_accounts.approve, banking_core_accounts.admin
- configuration: BANKING_CORE_ACCOUNTS_DATABASE_URL, BANKING_CORE_ACCOUNTS_EVENT_TOPIC, BANKING_CORE_ACCOUNTS_RETRY_LIMIT, BANKING_CORE_ACCOUNTS_DEFAULT_POLICY
- standard_features: deposit_account_management, banking_core_accounts_workflow, banking_core_accounts_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: banking_core_accounts_event_sourced_operational_history, banking_core_accounts_multi_tenant_policy_isolation, banking_core_accounts_schema_evolution_resilience, banking_core_accounts_autonomous_anomaly_detection, banking_core_accounts_semantic_document_instruction_understanding, banking_core_accounts_predictive_risk_scoring, banking_core_accounts_counterfactual_scenario_simulation, banking_core_accounts_cryptographic_audit_proofs, banking_core_accounts_continuous_control_testing, banking_core_accounts_carbon_and_sustainability_awareness, banking_core_accounts_cross_pbc_event_federation, banking_core_accounts_governed_ai_agent_execution
