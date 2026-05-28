# Banking Core Accounts PBC Specification

## Scope

`banking_core_accounts` is a standalone PBC for deposit account operations. A generated application that contains only this PBC must still let an operations team open, approve, activate, restrict, reopen, service, and close accounts without relying on shared foreign tables. The package owns its datastore boundary, service layer, API route layer, AppGen-X event contract, forms, wizards, controls, workbench, RBAC permission set, agent assistant, seed data, configuration schema, runtime parameters, release evidence, and tests.

The standard capability surface covers deposit account management, available and ledger balance tracking, account holds, interest accrual, fee assessment, statement cycle readiness, service cases, lifecycle state transitions, maker-checker approval, operational exceptions, and audit-ready account history. The advanced capability surface adds event-sourced operational history, multi-tenant policy isolation, schema evolution resilience, autonomous anomaly detection, semantic document instruction understanding, predictive risk scoring, counterfactual scenario simulation, cryptographic audit proofs, continuous control testing, carbon and sustainability awareness, cross-PBC event federation, and governed AI agent execution.

## Owned Boundary

The PBC owns every table required to operate the domain: deposit accounts, balance snapshots, holds, interest accrual, fee assessment, statements, service cases, policy rules, runtime parameter records, schema extension declarations, control assertions, and governed model metadata. Other PBCs may consume its APIs, projections, or emitted events, but they cannot write these owned tables directly. Cross-PBC dependencies are represented as API commands, queries, AppGen-X outbox messages, inbox messages, and projections rather than shared table joins. The generated schema, migration, and model artifacts are therefore sufficient for a one-PBC app backed by PostgreSQL, MySQL, or MariaDB.

## Functional Workflows

The primary account-opening wizard captures product, party reference, currency, account purpose, source of funds, opening channel, required documents, initial restrictions, and risk flags. The service validates rule configuration and parameter thresholds, creates the account in pending state, records an outbox event, and exposes the record in the workbench. The approval workflow requires an operator with the approve permission, verifies all mandatory controls, emits an approved event, and activates the account. Lifecycle commands restrict, dormancy-mark, close, and reopen accounts with reason codes, effective dates, and idempotency keys.

Balance workflows record ledger balance, available balance, holds, interest, and fees with explicit transaction boundaries. Hold forms capture amount, expiration, legal basis, and release rule. Interest and fee services calculate postings from configured rules but leave posting into external ledgers to declared API/event dependencies. Query APIs return account detail, workbench queues, risk indicators, and control exceptions. Mutations are routed through the service layer so that every command is auditable, retryable, and protected from duplicate execution.

## UI, Controls, And Agent

The generated UI must include a BankingCoreAccountsWorkbench for queues and metrics, BankingCoreAccountsDetail for lifecycle and financial state, and BankingCoreAccountsAssistantPanel for professional help. Forms cover account opening, balance adjustment, hold placement, fee assessment, interest accrual, statement readiness, and service-case creation. Wizards guide account opening and lifecycle approval. Controls surface maker-checker separation, duplicate request detection, policy rule violations, stale document checks, negative available balance prevention, restriction override review, dormant account governance, and owned-table boundary enforcement.

The agent, assistant, and chatbot expose skills for document instruction intake, guided CRUD datastore mutation, account-opening help, lifecycle guidance, exception explanation, and composition into the application-wide single agent. The agent can parse onboarding documents or operator instructions, propose a side-effect-free plan, show required permissions, and execute create, update, approve, or query actions only through governed service commands.

## Events And Resilience

Ordinary eventing uses the AppGen-X contract only. There is no user-visible stream picker. The PBC writes emitted events to its outbox and consumes declared events through its inbox. Idempotent handlers enforce idempotency_key semantics, retry failed policy/audit/operational messages, and route unrecoverable messages to the dead-letter table. Release evidence must show the outbox, inbox, retry policy, and dead-letter path for every command and consumed event.

## Configuration And Registration

Configuration includes database URL, event topic, retry limit, and default policy. The rule engine compiles deposit-account lifecycle rules, hold release rules, approval requirements, risk score thresholds, dormancy parameters, and assistant mutation policies. Runtime parameters are editable through governed configuration workbench controls. Package registration is side-effect-free: discovery, metadata validation, and registration plan generation must not mutate the datastore or call external services.

## Release Requirements

The package is releasable only when schema, migration, model, service, API route, event, handler, UI, permission, configuration, seed, registration, agent, and release tests pass. A generation smoke test must prove the single-PBC app includes database-backed forms, wizards, controls, workbench views, service commands, route contracts, agent skills, and AppGen-X event evidence.

## Manifest Traceability Appendix

Tables: deposit_account, account_balance, account_hold, interest_accrual, fee_assessment, statement_cycle, account_service_case, banking_core_accounts_policy_rule, banking_core_accounts_runtime_parameter, banking_core_accounts_schema_extension, banking_core_accounts_control_assertion, banking_core_accounts_governed_model.

APIs: POST /deposit-accounts, POST /account-balances, POST /account-holds, POST /interest-accruals, POST /fee-assessments, GET /banking-core-accounts-workbench.

Emits: BankingCoreAccountsCreated, BankingCoreAccountsUpdated, BankingCoreAccountsApproved, BankingCoreAccountsExceptionOpened.

Consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged.

UI fragments: BankingCoreAccountsWorkbench, BankingCoreAccountsDetail, BankingCoreAccountsAssistantPanel.

Permissions: banking_core_accounts.read, banking_core_accounts.create, banking_core_accounts.update, banking_core_accounts.approve, banking_core_accounts.admin.

Configuration: BANKING_CORE_ACCOUNTS_DATABASE_URL, BANKING_CORE_ACCOUNTS_EVENT_TOPIC, BANKING_CORE_ACCOUNTS_RETRY_LIMIT, BANKING_CORE_ACCOUNTS_DEFAULT_POLICY.

Standard features: deposit_account_management, banking_core_accounts_workflow, banking_core_accounts_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance.

Advanced capabilities: banking_core_accounts_event_sourced_operational_history, banking_core_accounts_multi_tenant_policy_isolation, banking_core_accounts_schema_evolution_resilience, banking_core_accounts_autonomous_anomaly_detection, banking_core_accounts_semantic_document_instruction_understanding, banking_core_accounts_predictive_risk_scoring, banking_core_accounts_counterfactual_scenario_simulation, banking_core_accounts_cryptographic_audit_proofs, banking_core_accounts_continuous_control_testing, banking_core_accounts_carbon_and_sustainability_awareness, banking_core_accounts_cross_pbc_event_federation, banking_core_accounts_governed_ai_agent_execution.
