# Gaming and Casino Operations PBC

## Purpose

The `gaming_casino_operations` PBC is a standalone package-local implementation for casino-floor execution. Its stable identity is the `gaming_casino_operations` PBC key, and every package artifact, command, query, API route, event handler, workbench view, release check, and registration entrypoint is anchored to that identity. The package is deliberately scoped to owned operational records for patron enrollment, table operations, slot configuration, wager session evidence, payout approvals, responsible-gaming intervention, compliance command, and governed assistant support. The implementation is side-effect-free for discovery and self-registration and only mutates package-owned tables plus AppGen-X outbox, inbox, and dead-letter records.

## Stable Identity And Boundaries

The package lives in `src/pyAppGen/pbcs/gaming_casino_operations` and self-registers through `register_pbc`, `registration_plan`, `package_metadata_manifest`, `validate_package_metadata`, and `package_discovery_plan`. The PBC does not share or mutate foreign tables. Its owned boundary is explicit: every owned table begins with `gaming_casino_operations_`, every command writes only to those owned tables, and all foreign coordination is done through declared API routes, AppGen-X events, or local projections inside the workbench. Shared or foreign tables are rejected by the owned-boundary guard and by governed CRUD planning helpers.

The owned tables are:

- `gaming_casino_operations_player_profile`
- `gaming_casino_operations_table_game`
- `gaming_casino_operations_slot_machine`
- `gaming_casino_operations_wager_session`
- `gaming_casino_operations_payout`
- `gaming_casino_operations_responsible_gaming_case`
- `gaming_casino_operations_gaming_compliance`
- `gaming_casino_operations_policy_rule`
- `gaming_casino_operations_runtime_parameter`
- `gaming_casino_operations_schema_extension`
- `gaming_casino_operations_control_assertion`
- `gaming_casino_operations_governed_model`
- `gaming_casino_operations_appgen_outbox_event`
- `gaming_casino_operations_appgen_inbox_event`
- `gaming_casino_operations_appgen_dead_letter_event`

## Schema, Migration, And Model Generation

The schema is hand-crafted and aligned across `models.py`, `schema_contract.py`, `runtime.py`, and `migrations/001_initial.sql`. The migration file contains concrete `CREATE TABLE` statements for every owned table. The model layer materializes field-level metadata for each owned table, including primary key, typed fields, descriptions, and the class name exposed through the schema contract. The model alignment smoke test ensures the runtime and release evidence see the same schema, migration, and model generation surface.

The player-profile schema carries identity confidence, age verification, restriction state, duplicate review state, and host context. The table-game schema carries pit, table number, game variant, shift ownership, opening bankroll, current bankroll, and dispute state. The slot-machine schema carries denomination, paytable version, operational state, jurisdiction approval state, fault state, and meter readings. The wager-session schema carries player, asset, session status, rating status, dispute flag, and betting metrics. The payout schema carries payout kind, source, amount, approval state, patron verification level, and suspicious-activity evidence. The responsible-gaming and compliance schemas carry owner, risk, severity, and intervention or case status. Policy rules, runtime parameters, schema extensions, control assertions, and governed models complete the owned governance surface.

## Services, Commands, Queries, And API Routes

The service layer exposes both command and query operations. Command methods include `create_player_profile`, `apply_player_restriction`, `handle_table_game`, `handle_slot_machine`, `handle_wager_session`, `handle_payout`, `open_responsible_gaming_case`, `record_compliance_case`, `request_surveillance_review`, `create_control_assertion`, `register_governed_model`, and the workflow runners. Query methods include `build_workbench_view`, `query_workbench`, `run_advanced_assessment`, and document-intake or CRUD-planning helpers. Every command runs inside the `owned_datastore_plus_outbox` transaction boundary, and every query stays read-only.

The public API route contract includes `POST /player-profiles`, `POST /table-games`, `POST /slot-machines`, `POST /wager-sessions`, `POST /payouts`, and `GET /gaming-casino-operations-workbench`. The standalone route surface extends that with package-local app routes such as `POST /app/gaming-casino-operations/responsible-gaming-cases`, `POST /app/gaming-casino-operations/compliance-cases`, workflow routes for patron enrollment, table shift close, and jackpot hand-pay, and a `GET /app/gaming-casino-operations/workbench` route. Route contracts include service method binding, required permission, idempotency key, stream-engine-picker visibility set to false, and AppGen-X metadata.

## Events, Handlers, Retry, And Dead-Letter Policy

The event contract is AppGen-X only. Emitted events are `GamingCasinoOperationsCreated`, `GamingCasinoOperationsUpdated`, `GamingCasinoOperationsApproved`, and `GamingCasinoOperationsExceptionOpened`. Consumed events are `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified`. The event envelope builder produces an idempotency key, aggregate table, aggregate id, topic, tenant, and reaction metadata. The outbox, inbox, and dead-letter tables are first-class owned records.

Handlers are idempotent. `dispatch_event` records duplicate delivery, enforces a retry policy, and returns a dead-letter table when an unexpected event arrives. Runtime event ingestion also tracks state-local idempotency keys so repeated package discovery, release evidence, tests, and smoke runs remain stable. The dead-letter workbench queue is visible in the standalone UI and is included in release evidence. Retry, idempotency, dead-letter, inbox, and outbox language are all explicit in the package and in the release documentation.

## UI, Workbench, Permissions, And RBAC

The UI contract includes the `GamingCasinoOperationsWorkbench`, `GamingCasinoOperationsDetail`, and `GamingCasinoOperationsAssistantPanel` fragments. The workbench blueprint defines forms, wizards, controls, queues, cards, alerts, and persona-specific views for floor supervisors, cage operations, slot operations, responsible-gaming staff, and compliance command. Forms cover patron enrollment review, slot fault recovery, payout approval, and responsible-gaming intervention. Wizards cover table shift close, jackpot hand-pay, and patron enrollment review. Controls cover restriction override, slot return to service, and payout release.

Permissions and RBAC are package-local. The permission manifest declares `gaming_casino_operations.read`, `gaming_casino_operations.create`, `gaming_casino_operations.update`, `gaming_casino_operations.approve`, and `gaming_casino_operations.admin`. Roles include operator, pit supervisor, cage supervisor, compliance officer, and auditor. Action permissions map each service command or query to a concrete permission, and the workbench UI binds actions to those permissions.

## Rules, Parameters, Configuration, And Workflows

Configuration is explicit and bounded. Supported datastore backends are PostgreSQL, MySQL, and MariaDB, and the event topic is fixed to AppGen-X. Runtime configuration includes property id, jurisdiction, retry limit, default policy, default currency, assistant mutation confirmation, and workbench limit. Parameters include `identity_confidence_floor`, `duplicate_review_threshold`, `table_variance_threshold`, `handpay_approval_threshold`, `suspicious_activity_threshold`, `cooling_off_hours`, and `workbench_limit`. Rules include `player_profile_policy`, `table_inventory_policy`, `slot_machine_policy`, `wager_session_policy`, `payout_approval_policy`, `responsible_gaming_policy`, and `compliance_case_policy`.

Workflow coverage is explicit and executable. `gaming_casino_operations_patron_enrollment_workflow` handles identity evidence and duplicate review. `gaming_casino_operations_table_shift_close_workflow` handles variance review, supervisor signoff, and closure publication. `gaming_casino_operations_slot_fault_recovery_workflow` handles meter snapshot capture and return-to-service approval. `gaming_casino_operations_jackpot_handpay_workflow` handles payout creation, supervisor approval, and cage release. `gaming_casino_operations_responsible_gaming_intervention_workflow` handles risk review, intervention planning, and player restriction sync.

## Agent, Assistant, Chatbot, And CRUD Planning

The package includes a governed agent and assistant surface. `agent_skill_manifest` materializes casino-specific skills for patron identity triage, shift close guidance, jackpot evidence summary, and responsible-gaming intervention support. `chatbot_interface_contract` materializes the package-local chatbot and assistant entrypoint and explicitly keeps the stream engine picker hidden. `document_instruction_plan` parses document or instruction text and recommends the correct workflow, owned table set, and route candidate. `datastore_crud_plan` produces governed CRUD mutation previews for owned datastore tables only, rejects foreign tables, and requires confirmation for create, update, or delete mutation plans. `composed_agent_contribution` exposes the single agent skill namespace.

## Release, Tests, Seed Data, And Standalone Application

Release evidence is package-local and executable. `release_evidence.py` validates schema, service, events, standalone app surface, and documentation artifacts and records blocking gaps or boundary gaps. `RELEASE_EVIDENCE.md` summarizes release checks. Seed data is defined in `seed_data.py`. Contract tests live in `tests/test_contract.py`, and focused standalone package tests live in `tests/test_standalone.py`. The standalone app itself is composed in `standalone.py` through `GamingCasinoOperationsStandaloneApplication`, `gaming_casino_operations_standalone_app_contract`, `gaming_casino_operations_bootstrap_standalone_app`, and `gaming_casino_operations_standalone_app_smoke`.

## Datastore And Event Policy

The datastore policy is fixed: PostgreSQL, MySQL, and MariaDB are the only supported backends, and AppGen-X is the only supported event contract. The package does not expose any stream processor picker, alternate event bus, or shared-table escape hatch. The workbench, commands, queries, routes, agent skills, and release checks all assume this datastore and event policy.

## Manifest Traceability Appendix

- tables: player_profile, table_game, slot_machine, wager_session, payout, responsible_gaming_case, gaming_compliance, policy_rule, runtime_parameter, schema_extension, control_assertion, governed_model
- apis: POST /player-profiles, POST /table-games, POST /slot-machines, POST /wager-sessions, POST /payouts, GET /gaming-casino-operations-workbench
- emits: GamingCasinoOperationsCreated, GamingCasinoOperationsUpdated, GamingCasinoOperationsApproved, GamingCasinoOperationsExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- ui_fragments: GamingCasinoOperationsWorkbench, GamingCasinoOperationsDetail, GamingCasinoOperationsAssistantPanel
- permissions: gaming_casino_operations.read, gaming_casino_operations.create, gaming_casino_operations.update, gaming_casino_operations.approve, gaming_casino_operations.admin
- configuration: GAMING_CASINO_OPERATIONS_DATABASE_URL, GAMING_CASINO_OPERATIONS_EVENT_TOPIC, GAMING_CASINO_OPERATIONS_RETRY_LIMIT, GAMING_CASINO_OPERATIONS_DEFAULT_POLICY, GAMING_CASINO_OPERATIONS_PROPERTY_ID, GAMING_CASINO_OPERATIONS_JURISDICTION
- standard_features: player_profile_management, gaming_casino_operations_workflow, gaming_casino_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: gaming_casino_operations_event_sourced_operational_history, gaming_casino_operations_multi_tenant_policy_isolation, gaming_casino_operations_schema_evolution_resilience, gaming_casino_operations_autonomous_anomaly_detection, gaming_casino_operations_semantic_document_instruction_understanding, gaming_casino_operations_predictive_risk_scoring, gaming_casino_operations_counterfactual_scenario_simulation, gaming_casino_operations_cryptographic_audit_proofs, gaming_casino_operations_continuous_control_testing, gaming_casino_operations_carbon_and_sustainability_awareness, gaming_casino_operations_cross_pbc_event_federation, gaming_casino_operations_governed_ai_agent_execution
