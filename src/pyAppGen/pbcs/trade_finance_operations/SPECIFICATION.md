# Trade Finance Operations PBC

## Purpose

The `trade_finance_operations` PBC is a world-class packaged business capability for trade-finance issuance, presentation, compliance, discrepancy, finance, settlement, and message-evidence work. It owns letters of credit, guarantees and standby credits, documentary collections, trade bills, trade loans, shipment document intake, sanctions and compliance controls, discrepancy decisions, collateral and margin cover, limit reservations, fee calculations, settlement release, SWIFT-like evidence, package-local governance, and release evidence. It is designed as a composable AppGen-X package, not a thin catalog row. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, rules, parameters, configuration, seed data, standalone app shell, release evidence, and runtime smoke checks.

## Stable Identity

- PBC key: `trade_finance_operations`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/trade_finance_operations`.
- Runtime entrypoint: `trade_finance_operations_runtime_capabilities()`.
- UI entrypoint: `trade_finance_operations_ui_contract()`.
- Standalone app entrypoint: `TradeFinanceOperationsStandaloneApp` in `standalone.py`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox, inbox, and dead-letter contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

The package owns only `trade_finance_operations_` tables. It does not mutate foreign or shared tables. Cross-PBC collaboration must happen through declared APIs, AppGen-X events, or read-only projections. The owned schema covers issuance records, bills, loans, document packages, shipment evidence, sanctions checks, discrepancy cases, collateral and limit records, fee accruals, settlement records, SWIFT-like evidence, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X inbox/outbox/dead-letter tables. The boundary is explicit: if a table reference is foreign, shared, or lacks the `trade_finance_operations_` prefix, the package must reject it.

## Schema, Migrations, and Models

Schema generation is package-local and auditable. `migrations/001_initial.sql` materializes the owned tables required for trade finance operations. `runtime.py`, `models.py`, and `schema_contract.py` expose the owned schema contract, logical model list, backend allowlist, and migration evidence. The schema includes records for letters of credit, bank guarantees and SBLC, documentary collections, trade bills, trade loans, shipment and trade-document packages, sanctions decisions, discrepancy cases, collateral and margin positions, limit reservations, fee accruals, settlements, and SWIFT-like message evidence. Policy, parameter, schema-extension, control-assertion, and governed-model tables keep the PBC self-contained and side-effect-free.

## Services, APIs, and Queries

Service and API contracts are explicit. Command methods cover `configure_runtime`, `set_parameter`, `register_rule`, `register_schema_extension`, `receive_event`, `command_letter_of_credit`, and the trade-domain operations for issuance, collections, bills, loans, shipment documents, sanctions, discrepancies, collateral, limits, fees, settlement, SWIFT-like evidence, amendment simulation, and release-evidence export. Query methods cover workbench, case detail, release evidence pack, advanced assessment, and document instruction parsing. Public API routes include the legacy package routes `POST /letter-of-credits`, `POST /bank-guarantees`, `POST /documentary-collections`, `POST /trade-documents`, `POST /sanctions-checks`, and `GET /trade-finance-operations-workbench`, plus richer package-local routes for trade bills, trade loans, discrepancy decisions, collateral, limits, fees, settlement, and SWIFT-like messages. Every command keeps an idempotency key, stays inside the owned datastore plus outbox transaction boundary, and never exposes a stream-engine picker.

## Events, Outbox, Inbox, Dead-Letter, Idempotency, and Retry

AppGen-X eventing is mandatory. The package emits typed lifecycle events such as creation, update, approval, exception, presentation receipt, discrepancy raise, waiver request, screening block, settlement completion, and SWIFT-evidence creation. It consumes `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`. Event handlers require idempotency keys, ignore duplicates, preserve retry metadata, and route unknown events into the owned dead-letter table. The event contract, handlers, and route metadata all keep the event contract fixed to AppGen-X and keep stream-engine controls hidden. This is a non-negotiable policy for PostgreSQL, MySQL, and MariaDB deployments.

## UI, Workbench, Forms, Wizards, Controls, and RBAC

The UI surface includes the core fragments `TradeFinanceOperationsWorkbench`, `TradeFinanceOperationsDetail`, and `TradeFinanceOperationsAssistantPanel`. The workbench is an operations cockpit with issuance, presentation, sanctions hold, discrepancy, collateral and limit, settlement, and release-evidence queues. Forms cover issuance, guarantees/SBLC, documentary collections, bills, loans, shipment document packages, sanctions review, discrepancy decisions, collateral, limits, fees, settlement, and SWIFT-like message evidence. Wizards orchestrate issuance, guarantee/SBLC setup, documentary collections, presentation examination, trade-loan and settlement workflows, and release-evidence review. Controls provide queue cards, document-matrix comparison, sanctions boundary guardrails, collateral and limit coverage, fee waterfalls, SWIFT evidence consoles, and release gates. RBAC is explicit through `trade_finance_operations.read`, `trade_finance_operations.create`, `trade_finance_operations.update`, `trade_finance_operations.approve`, and `trade_finance_operations.admin`.

## Rules, Parameters, Configuration, and Governance

Rules are first-class artifacts covering letters of credit, guarantees, standby credits, documentary collections, shipment documents, sanctions and compliance, discrepancy resolution, limits and collateral, fees, and settlement release. Parameters are bounded artifacts covering quality, materiality, approval SLA, risk thresholds, workbench limits, sanctions hold SLAs, waiver SLAs, collateral haircuts, and limit buffers. Configuration enforces PostgreSQL/MySQL/MariaDB, the fixed AppGen-X event topic, retry limits, default policy packs, and dual-control requirements. Governance hooks compile rules, evaluate rules, validate configuration, set parameters, and prove that no mutation path bypasses confirmation or owned-table checks.

## Agent, Chatbot, Skills, and Governed Datastore CRUD

The package contributes a single-agent namespace `trade_finance_operations_skills` through `chatbot_interface_contract()` and `composed_agent_contribution()`. The chatbot explicitly includes `governed_datastore_crud`, document instruction intake, mutation preview, sanctions boundary guidance, and release-evidence explanation. Every skill is confirmation-gated for mutation, uses the AppGen-X contract, and rejects foreign tables. The agent can parse document instructions, map them to forms, wizards, and routes, preview governed CRUD actions, suggest discrepancy paths, and explain screening boundaries. It cannot clear a blocked sanctions case by itself and cannot write outside `trade_finance_operations_` tables.

## Standalone One-PBC App Workflow

`standalone.py` composes the package into an executable one-PBC app. A typical journey issues a letter of credit or guarantee, reserves exposure, posts collateral or margin, records shipment documents, runs sanctions and compliance screening, examines the document package, opens or waives discrepancies, assesses fees, settles the case, records SWIFT-like evidence, and generates a release-evidence pack. Documentary collections, trade bills, and trade loans follow the same governed path. Amendment simulation is explicitly non-mutating so operators can compare before-and-after effects on limits, fees, and screening without changing live state. The workbench, detail page, forms, wizards, controls, assistant preview, and release-evidence pack are all package-local and side-effect-free in tests.

## Side-Effect-Free Self-Registration and Release Evidence

The package self-registers through `register_pbc()`, `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()`. Registration is side-effect-free: it validates the manifest, returns a catalog patch, and proves publishability without mutating any shared registry. Release evidence covers schema, services, routes, events, handlers, UI, forms, wizards, controls, RBAC, configuration, rules, parameters, seed data, standalone workflow checks, assistant guardrails, and smoke checks. Tests cover schema/service/release evidence, event contracts, package metadata and discovery, service and route surfaces, governance hooks, idempotent handlers, forms/wizards/controls, capability assurance, and the standalone journey.

## Manifest Traceability Appendix

This appendix preserves traceability to the catalog-backed PBC manifest values used by repo-level audits.

- tables: letter_of_credit, bank_guarantee, documentary_collection, trade_document, sanctions_check, shipment_evidence, trade_settlement, trade_finance_operations_policy_rule, trade_finance_operations_runtime_parameter, trade_finance_operations_schema_extension, trade_finance_operations_control_assertion, trade_finance_operations_governed_model
- apis: POST /letter-of-credits, POST /bank-guarantees, POST /documentary-collections, POST /trade-documents, POST /sanctions-checks, GET /trade-finance-operations-workbench
- emits: TradeFinanceOperationsCreated, TradeFinanceOperationsUpdated, TradeFinanceOperationsApproved, TradeFinanceOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- ui_fragments: TradeFinanceOperationsWorkbench, TradeFinanceOperationsDetail, TradeFinanceOperationsAssistantPanel
- permissions: trade_finance_operations.read, trade_finance_operations.create, trade_finance_operations.update, trade_finance_operations.approve, trade_finance_operations.admin
- configuration: TRADE_FINANCE_OPERATIONS_DATABASE_URL, TRADE_FINANCE_OPERATIONS_EVENT_TOPIC, TRADE_FINANCE_OPERATIONS_RETRY_LIMIT, TRADE_FINANCE_OPERATIONS_DEFAULT_POLICY
- standard_features: letter_of_credit_management, trade_finance_operations_workflow, trade_finance_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: trade_finance_operations_event_sourced_operational_history, trade_finance_operations_multi_tenant_policy_isolation, trade_finance_operations_schema_evolution_resilience, trade_finance_operations_autonomous_anomaly_detection, trade_finance_operations_semantic_document_instruction_understanding, trade_finance_operations_predictive_risk_scoring, trade_finance_operations_counterfactual_scenario_simulation, trade_finance_operations_cryptographic_audit_proofs, trade_finance_operations_continuous_control_testing, trade_finance_operations_carbon_and_sustainability_awareness, trade_finance_operations_cross_pbc_event_federation, trade_finance_operations_governed_ai_agent_execution

## Extended Standalone Surfaces

Beyond the audit appendix above, the package-local standalone app also exposes trade bills, trade loans, discrepancy cases, collateral margins, limit reservations, fee accruals, settlement detail, SWIFT-like evidence, release-evidence review, and amendment simulation. These richer surfaces remain package-local, use the same AppGen-X event contract, and do not require any shared-table or stream-engine exceptions.
