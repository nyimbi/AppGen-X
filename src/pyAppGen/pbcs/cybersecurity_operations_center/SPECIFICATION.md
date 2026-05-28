# Cybersecurity Operations Center Specification

## Purpose

`cybersecurity_operations_center` is a self-contained AppGen PBC for operating a SOC queue around alerts, incidents, threat intel, playbooks, containment, and evidence. The package owns its schema, runtime logic, AppGen-X events, UI/workbench metadata, assistant planning, tests, and release evidence.

## Ownership Boundary

This package writes only to these owned tables:

- `cybersecurity_operations_center_security_alert`
- `cybersecurity_operations_center_security_incident`
- `cybersecurity_operations_center_asset_exposure`
- `cybersecurity_operations_center_threat_intel`
- `cybersecurity_operations_center_playbook_run`
- `cybersecurity_operations_center_containment_action`
- `cybersecurity_operations_center_response_evidence`
- `cybersecurity_operations_center_cybersecurity_operations_center_policy_rule`
- `cybersecurity_operations_center_cybersecurity_operations_center_runtime_parameter`
- `cybersecurity_operations_center_cybersecurity_operations_center_schema_extension`
- `cybersecurity_operations_center_cybersecurity_operations_center_control_assertion`
- `cybersecurity_operations_center_cybersecurity_operations_center_governed_model`
- `cybersecurity_operations_center_appgen_outbox_event`
- `cybersecurity_operations_center_appgen_inbox_event`
- `cybersecurity_operations_center_appgen_dead_letter_event`

No foreign table writes are allowed. Cross-PBC interaction is limited to declared APIs or AppGen-X consumed events.

## Core Commands

- `command_security_alert`
  - accepts first-class detection context
  - supports validation-only usage
  - applies deduplication/correlation
  - records lineage and emits AppGen-X outbox events
- `transition_alert`
  - enforces the allowed state machine:
    - `new`
    - `deduplicated`
    - `enriched`
    - `triaged`
    - `escalated`
    - `suppressed`
    - `contained`
    - `closed`
    - `reopened`
- `enrich_security_alert`
  - adds structured enrichment facts and provenance
- `suppress_security_alert`
  - stores suppression owner, scope, reason, and review timing
- `record_security_incident`
  - previews and enforces incident promotion thresholds
  - writes explainable severity factors and role ownership
- `review_asset_exposure`
  - projects open alerts/incidents and containment linkage for an asset
- `approve_threat_intel`
  - separates observed fact, assessed relationship, campaign context, and analyst inference
- `simulate_playbook_run`
  - models stage checkpoints and human breakpoints
- `create_containment_action`
  - enforces no-approval, supervisor-approval, and exception-approval paths
- `record_response_evidence`
  - captures checksum, source, storage reference, redaction state, admissibility notes, and chain-of-custody history
- `create_control_assertion`
  - records control-test outcomes and exception evidence
- `record_governed_model`
  - records bounded assistant/AI model usage and guardrails

## Queries and Projections

- `query_workbench`
  - triage lanes: urgent, backlog, watchlist, suppressed
  - incident cards
  - supervisor lane
  - evidence-review lane
  - workbench metrics
- `build_case_detail`
  - timeline
  - evidence list
  - containment actions
  - relationship graph
  - AppGen-X lineage
- `generate_handoff_packet`
  - open questions
  - pending approvals
  - pending evidence
  - cited source records
- `run_advanced_assessment`
  - explainable backlog risk
  - queue pressure and anomaly cards

## API Contract

- `POST /security-alerts`
- `POST /security-alerts/triage`
- `POST /security-alerts/enrich`
- `POST /security-alerts/suppress`
- `POST /security-incidents`
- `POST /security-incidents/promote`
- `POST /asset-exposures`
- `POST /threat-intels`
- `POST /playbook-runs`
- `POST /containment-actions`
- `POST /response-evidence`
- `GET /cybersecurity-operations-center-workbench`
- `GET /cybersecurity-operations-center/case-detail`

## Event Contract

Emitted:

- `CybersecurityOperationsCenterCreated`
- `CybersecurityOperationsCenterUpdated`
- `CybersecurityOperationsCenterApproved`
- `CybersecurityOperationsCenterExceptionOpened`

Consumed:

- `PolicyChanged`
- `AuditEventSealed`
- `OperationalKpiChanged`

Consumed events are idempotent. Unsupported events go to the owned dead-letter table with retry metadata.

## UI / Workbench Contract

Fragments:

- `CybersecurityOperationsCenterWorkbench`
- `CybersecurityOperationsCenterDetail`
- `CybersecurityOperationsCenterAssistantPanel`

Forms:

- alert intake
- incident promotion
- evidence capture
- containment approval

Wizards:

- alert triage
- incident promotion
- playbook run
- shift handoff

Controls:

- severity lane filter
- confidence slider
- event lineage panel
- relationship graph toggle

## Assistant Contract

The assistant can:

- draft triage summaries
- identify missing evidence
- propose threat-intel enrichment previews
- generate shift handoff packets
- parse documents into mutation previews
- build owned-table-only CRUD plans

The assistant cannot mutate foreign tables and requires human confirmation for mutating operations.

## Release Gates

This package maps its local evidence to:

- `pbc_source_artifact_contract`
- `pbc_implementation_release_audit`
- `pbc_generation_smoke_audit`

## Implementation Contract and Traceability Appendix

The `cybersecurity_operations_center` PBC is a side-effect-free registerable package with a stable `pbc` key, a package-local manifest, package discovery metadata, and registration plans that describe the catalog patch without mutating the catalog. Self-registration must remain side-effect-free: loading the package, building discovery evidence, or validating registration cannot open network connections, write shared state, or mutate another PBC.

The owned schema is generated from the package-local model contract and migration artifacts. The schema, migration, and model layer cover security alert, security incident, asset exposure, threat intelligence, playbook run, containment action, response evidence, policy rule, runtime parameter, schema extension, control assertion, governed model, and AppGen-X outbox, inbox, and dead-letter event tables. The PBC never writes foreign or shared tables; any outside context arrives through declared APIs, events, or projections.

The service and API route surface exposes command and query methods for alert intake, triage transition, enrichment, suppression, incident promotion, asset exposure review, threat-intel approval, playbook execution, containment approval, response evidence custody, case detail, workbench queries, handoff packets, runtime configuration, rule compilation, parameter changes, and event intake. Each mutating command has an owned datastore plus AppGen-X outbox boundary; each query is read-only.

The event contract uses AppGen-X outbox, inbox, retry, idempotency, and dead-letter semantics. The ordinary generated application must not expose stream-engine selection. Unsupported events are retried according to package policy and then recorded in `cybersecurity_operations_center_appgen_dead_letter_event`.

The UI and workbench must surface professional SOC operations rather than only record lists. It includes forms for security alert intake, incident promotion, evidence capture, containment approval, asset exposure review, and threat-intel review. It includes wizards for alert triage, staged incident promotion, playbook execution, containment approval, shift handoff, and release evidence review. It includes controls for severity lanes, confidence thresholds, relationship graph inspection, evidence custody, SLA timers, lineage, and RBAC permission-gated actions.

Rules, parameters, and configuration are first-class. Configuration includes `CYBERSECURITY_OPERATIONS_CENTER_DATABASE_URL`, `CYBERSECURITY_OPERATIONS_CENTER_EVENT_TOPIC`, `CYBERSECURITY_OPERATIONS_CENTER_RETRY_LIMIT`, and `CYBERSECURITY_OPERATIONS_CENTER_DEFAULT_POLICY`. Runtime parameters include alert confidence thresholds, severity escalation windows, containment approval requirements, handoff packet depth, and workbench limits. Rules govern deduplication, incident promotion, evidence sufficiency, containment approval, suppression, and event replay.

The assistant exposes skills for task guidance, document instruction intake, governed datastore CRUD mutation previews, alert triage summaries, missing evidence identification, threat-intel enrichment previews, containment recommendation explanation, and shift handoff drafting. Assistant mutations require human confirmation, cite source records, use owned tables only, and preserve AppGen-X event evidence.

The PBC supports standard and advanced SOC capabilities. Standard capabilities include `security_alert_management`, `cybersecurity_operations_center_workflow`, `cybersecurity_operations_center_analytics`, `configuration_schema`, `rule_engine`, `parameter_engine`, `owned_schema_migrations_models`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `retry_dead_letter_evidence`, `permissions`, `seed_data`, `workbench`, `agentic_document_instruction_intake`, `governed_datastore_crud`, `ai_agent_task_assistance`, `configuration_workbench`, and `continuous_release_assurance`. Advanced capabilities include `cybersecurity_operations_center_event_sourced_operational_history`, `cybersecurity_operations_center_multi_tenant_policy_isolation`, `cybersecurity_operations_center_schema_evolution_resilience`, `cybersecurity_operations_center_autonomous_anomaly_detection`, `cybersecurity_operations_center_semantic_document_instruction_understanding`, `cybersecurity_operations_center_predictive_risk_scoring`, `cybersecurity_operations_center_counterfactual_scenario_simulation`, `cybersecurity_operations_center_cryptographic_audit_proofs`, `cybersecurity_operations_center_continuous_control_testing`, `cybersecurity_operations_center_carbon_and_sustainability_awareness`, `cybersecurity_operations_center_cross_pbc_event_federation`, and `cybersecurity_operations_center_governed_ai_agent_execution`.

Release evidence includes generated schema, migration, models, services, routes, events, handlers, UI, RBAC permissions, configuration, seed data, assistant skills, idempotent retry/dead-letter handling, package registration metadata, tests, and smoke audits. The package must validate under PostgreSQL, MySQL, and MariaDB as the only ordinary datastore backends.

## Manifest Traceability Appendix

Permissions:

- `cybersecurity_operations_center.read`
- `cybersecurity_operations_center.create`
- `cybersecurity_operations_center.update`
- `cybersecurity_operations_center.approve`
- `cybersecurity_operations_center.admin`

Configuration:

- `CYBERSECURITY_OPERATIONS_CENTER_DATABASE_URL`
- `CYBERSECURITY_OPERATIONS_CENTER_EVENT_TOPIC`
- `CYBERSECURITY_OPERATIONS_CENTER_RETRY_LIMIT`
- `CYBERSECURITY_OPERATIONS_CENTER_DEFAULT_POLICY`

Standard features:

- `security_alert_management`
- `cybersecurity_operations_center_workflow`
- `cybersecurity_operations_center_analytics`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `owned_schema_migrations_models`
- `appgen_x_outbox_inbox_eventing`
- `idempotent_handlers`
- `retry_dead_letter_evidence`
- `permissions`
- `seed_data`
- `workbench`
- `agentic_document_instruction_intake`
- `governed_datastore_crud`
- `ai_agent_task_assistance`
- `configuration_workbench`
- `continuous_release_assurance`

Advanced capabilities:

- `cybersecurity_operations_center_event_sourced_operational_history`
- `cybersecurity_operations_center_multi_tenant_policy_isolation`
- `cybersecurity_operations_center_schema_evolution_resilience`
- `cybersecurity_operations_center_autonomous_anomaly_detection`
- `cybersecurity_operations_center_semantic_document_instruction_understanding`
- `cybersecurity_operations_center_predictive_risk_scoring`
- `cybersecurity_operations_center_counterfactual_scenario_simulation`
- `cybersecurity_operations_center_cryptographic_audit_proofs`
- `cybersecurity_operations_center_continuous_control_testing`
- `cybersecurity_operations_center_carbon_and_sustainability_awareness`
- `cybersecurity_operations_center_cross_pbc_event_federation`
- `cybersecurity_operations_center_governed_ai_agent_execution`
