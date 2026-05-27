# Service Ticketing PBC

`service_ticketing` is the AppGen-X packaged business capability for service
operations, ticket lifecycle management, SLA governance, assignment and
handoff orchestration, customer update delivery, resolution evidence, CSAT
readiness, auditability, and automation insights. The package owns its
runtime, schema contract, service contract, release evidence, API descriptors,
permission descriptors, UI workbench bindings, and focused tests.

## Stable Identity

- PBC key: `service_ticketing`.
- Package directory: `src/pyAppGen/pbcs/service_ticketing`.
- Runtime entrypoint: `service_ticketing_runtime_capabilities()`.
- UI entrypoint: `service_ticketing_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Event contract: fixed AppGen-X contract on
  `appgen.service_ticketing.events`.
- User-selectable event contracts: not allowed.
- Stream-engine selector exposure: forbidden and hidden.

## Owned Datastore Boundary

The package owns these operational tables and no foreign business tables:

- `support_ticket`
- `service_queue`
- `sla_policy`
- `service_priority`
- `case_assignment`
- `escalation_event`
- `ticket_interaction`
- `knowledge_suggestion`
- `entitlement_snapshot`
- `case_lifecycle_state`
- `field_service_handoff`
- `customer_update`
- `resolution_record`
- `csat_response`
- `ticket_audit_log`
- `automation_insight`
- `service_rule`
- `service_parameter`
- `service_configuration`

Package-local runtime event tables provide idempotent event evidence:

- `service_ticketing_appgen_outbox_event`
- `service_ticketing_appgen_inbox_event`
- `service_ticketing_dead_letter_event`

The boundary verifier accepts only:

- owned tables
- package-local runtime event tables
- declared consumed events
- declared API dependencies
- declared read-only projections

It rejects undeclared foreign references such as `customer_profile`.

## Declared External Dependencies

The package consumes only declared integrations, not shared tables:

- APIs:
  `GET /customer-context/{customer_id}`,
  `GET /knowledge/suggestions`,
  `GET /entitlements/{customer_id}`,
  `POST /customer-updates`,
  `POST /field-service/handoffs`
- API projections:
  `customer_context_projection`,
  `preference_projection`,
  `entitlement_projection`,
  `knowledge_projection`
- Consumed events:
  `CustomerUpdated`,
  `PreferenceChanged`,
  `EntitlementUpdated`,
  `KnowledgeSuggested`

## Standard Table-Stakes Coverage

The completeness slice covers the ordinary service-ticketing expectations:

- tickets and case lifecycle
- queues and priority catalogs
- SLA policies
- assignment scoring and ownership
- escalations
- ticket interactions
- knowledge suggestions
- entitlement snapshots
- field/service handoffs
- customer updates
- resolution records
- CSAT follow-up evidence
- audit logs
- automation insights
- rule, parameter, and configuration governance
- AppGen-X inbox, outbox, and dead-letter evidence
- workbench and UI binding evidence

## Runtime Configuration And Policy

Runtime configuration supports:

- `database_backend`
- `event_topic`
- `retry_limit`
- `default_region`
- `supported_regions`
- `channels`
- `priority_levels`
- `default_timezone`
- `assignment_mode`
- `workbench_limit`

Parameter support includes:

- SLA breach threshold
- auto-escalation threshold
- sentiment weighting
- priority weighting
- customer-tier weighting
- queue-load weighting
- first-response minutes
- resolution target hours
- maximum open cases per owner
- workbench limit

Rule support includes:

- tenant and scope
- active status
- allowed regions, channels, and priorities
- assignment policy
- escalation policy
- compiled-hash evidence

## Service Contract

The package-local service contract is exposed by
`service_ticketing_build_service_contract()` and included in
`implementation_contract()`.

Command methods:

- `configure_runtime`
- `set_parameter`
- `register_rule`
- `register_schema_extension`
- `receive_event`
- `create_sla_policy`
- `open_ticket`
- `assign_ticket`
- `record_escalation`
- `resolve_ticket`
- `run_control_tests`
- `verify_owned_table_boundary`

Query and release methods:

- `build_workbench_view`
- `build_api_contract`
- `permissions_contract`
- `ui_binding_contract`
- `build_schema_contract`
- `build_service_contract`
- `build_release_evidence`

The service contract proves:

- mutation stays inside owned tables
- runtime event tables are package-local
- event contract is fixed to AppGen-X
- retry/dead-letter policy is defined
- idempotent inbox handling uses `event_type:event_id`
- no shared-table access exists

## Schema Contract

`service_ticketing_build_schema_contract()` emits generated descriptors for:

- every owned table
- migration path per owned table
- model path per owned table
- runtime event table descriptors
- tenant isolation requirements
- schema-extension rules for owned tables only
- declared dependencies and relationships

This contract is exposed through `implementation_contract()` as
`schema_contract`.

## API Contract

`service_ticketing_build_api_contract()` emits route descriptors for:

- `PUT /service-ticketing/configuration`
- `POST /service-ticketing/parameters`
- `POST /service-ticketing/rules`
- `POST /sla-policies`
- `POST /tickets`
- `POST /assignments`
- `POST /ticket-interactions`
- `POST /customer-updates`
- `POST /field-service-handoffs`
- `POST /escalations`
- `POST /resolutions`
- `POST /csat-responses`
- `POST /tickets/reopen`
- `POST /tickets/close`
- `POST /service-ticketing/events/inbox`
- `GET /service-ticketing/workbench`
- `GET /service-ticketing/schema-contract`
- `GET /service-ticketing/service-contract`
- `GET /service-ticketing/release-evidence`

The API contract declares:

- required permissions
- owned-table mutation scope
- emitted and consumed events
- idempotency keys
- fixed required event topic
- hidden stream-engine picker state

## Events And Idempotency

Consumed events:

- `CustomerUpdated`
- `PreferenceChanged`
- `EntitlementUpdated`
- `KnowledgeSuggested`

Emitted events:

- `SupportCaseOpened`
- `TicketAssigned`
- `FieldServiceHandoffPrepared`
- `TicketInteractionRecorded`
- `CustomerUpdateSent`
- `SlaBreached`
- `ResolutionRecorded`
- `CsatSurveyRequested`
- `CsatResponseRecorded`
- `SupportCaseReopened`
- `SupportCaseClosed`
- `CustomerUpdated`

Handlers require `event_id`, record inbox evidence, deduplicate already
handled events, and push simulated failures to the package-local dead-letter
table.

## UI And Workbench

UI surfaces include:

- workbench
- ticket inbox
- queue manager
- SLA designer
- priority matrix
- assignment board
- escalation center
- interaction timeline
- knowledge suggestion panel
- entitlement snapshot panel
- field-service handoff panel
- customer update panel
- resolution console
- CSAT survey panel
- audit trail
- automation insight panel
- governance panels for rules, parameters, and configuration
- outbox, inbox, and dead-letter event panels

Workbench evidence includes:

- ticket, queue, priority, SLA, assignment, escalation, interaction,
  knowledge, entitlement, handoff, customer-update, resolution, CSAT, audit,
  and automation counts
- runtime event table bindings
- AppGen-X eventing metadata
- permission-gated visible and locked actions

## Release Evidence

`service_ticketing_build_release_evidence()` proves:

- owned schema depth matches the expanded table set
- every owned table has migration and model descriptors
- runtime tables are declared
- service contract includes release methods
- AppGen-X event contract and topic are fixed
- permissions cover schema/service/release builders
- UI and workbench bindings point to package-local runtime tables
- handled and dead-letter event evidence is present
- boundary contract forbids shared tables
- backend allowlist remains PostgreSQL, MySQL, and MariaDB
- control tests pass
- table-stakes records are populated across tickets, queues, SLAs,
  priorities, assignments, escalations, interactions, knowledge suggestions,
  entitlements, lifecycle, handoffs, customer updates, resolutions, CSAT,
  audit, automation, rules, parameters, and configuration

## Package Exposure

`implementation_contract()` exposes:

- `advanced_runtime`
- `api_contract`
- `schema_contract`
- `service_contract`
- `release_evidence_contract`
- `permissions_contract`
- `ui_contract`
- `ui_binding_contract`
- `boundary_contract`
- required event topic, emitted events, consumed events, owned tables, runtime
  tables, and backend allowlist

## Seed And Release Evidence

Release evidence includes package-local seed data for ticket severities,
priority bands, queues, SLA policies, resolution reasons, escalation reasons,
and knowledge-link classes. Generated applications validate those seed
descriptors with schema, migration, model, service, route, event, handler, UI,
RBAC, configuration, and release contracts.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `service_ticketing`
- Mesh: `relationship`
- Datastore backend: `postgresql`

### Owned Tables

- `support_ticket`
- `service_queue`
- `sla_policy`
- `service_priority`
- `case_assignment`
- `escalation_event`
- `ticket_interaction`
- `knowledge_suggestion`
- `entitlement_snapshot`
- `case_lifecycle_state`
- `field_service_handoff`
- `customer_update`
- `resolution_record`
- `csat_response`
- `ticket_audit_log`
- `automation_insight`
- `service_rule`
- `service_parameter`
- `service_configuration`

### API Routes

- `PUT /service-ticketing/configuration`
- `POST /service-ticketing/parameters`
- `POST /service-ticketing/rules`
- `POST /sla-policies`
- `POST /tickets`
- `POST /assignments`
- `POST /ticket-interactions`
- `POST /customer-updates`
- `POST /field-service-handoffs`
- `POST /escalations`
- `POST /resolutions`
- `POST /csat-responses`
- `POST /tickets/reopen`
- `POST /tickets/close`
- `POST /service-ticketing/events/inbox`
- `GET /service-ticketing/workbench`
- `GET /service-ticketing/schema-contract`
- `GET /service-ticketing/service-contract`
- `GET /service-ticketing/release-evidence`

### Emitted Events

- `SupportCaseOpened`
- `TicketAssigned`
- `FieldServiceHandoffPrepared`
- `TicketInteractionRecorded`
- `CustomerUpdateSent`
- `SlaBreached`
- `ResolutionRecorded`
- `CsatSurveyRequested`
- `CsatResponseRecorded`
- `SupportCaseReopened`
- `SupportCaseClosed`
- `CustomerUpdated`

### Consumed Events

- `CustomerUpdated`
- `PreferenceChanged`
- `EntitlementUpdated`
- `KnowledgeSuggested`

### UI Fragments

- `ServiceTicketingWorkbench`
- `TicketInbox`
- `ServiceQueueManager`
- `SlaPolicyDesigner`
- `PriorityMatrixPanel`
- `AssignmentQueueBoard`
- `EscalationCommandCenter`
- `TicketInteractionTimeline`
- `KnowledgeSuggestionPanel`
- `EntitlementSnapshotPanel`
- `FieldServiceHandoffPanel`
- `CustomerUpdatePanel`
- `ResolutionConsole`
- `CsatSurveyPanel`
- `ServiceAuditTrail`
- `AutomationInsightPanel`
- `ServiceRuleStudio`
- `ServiceParameterConsole`
- `ServiceConfigurationPanel`
- `ServiceEventOutbox`
- `ServiceEventInbox`
- `ServiceDeadLetterQueue`

### Permissions

- `service_ticketing.ticket.write`
- `service_ticketing.queue.manage`
- `service_ticketing.assignment.write`
- `service_ticketing.escalation.write`
- `service_ticketing.customer.update`
- `service_ticketing.event.consume`
- `service_ticketing.configure`
- `service_ticketing.audit`

### Configuration Keys

- `SERVICE_TICKETING_DATABASE_URL`
- `SERVICE_TICKETING_EVENT_TOPIC`
- `SERVICE_TICKETING_RETRY_LIMIT`
- `SERVICE_TICKETING_DEFAULT_REGION`
- `SERVICE_TICKETING_DEFAULT_TIMEZONE`
- `SERVICE_TICKETING_ASSIGNMENT_MODE`

### Standard Features

- `ticket_management`
- `queue_management`
- `sla_policy`
- `priority_management`
- `case_assignment`
- `escalation_event`
- `interaction_timeline`
- `knowledge_suggestion`
- `entitlement_snapshot`
- `case_lifecycle`
- `field_service_handoff`
- `customer_update`
- `resolution_tracking`
- `csat_tracking`
- `audit_log`
- `automation_insight`
- `customer_context_projection`
- `preference_projection`
- `tenant_isolation`
- `appgen_x_outbox`
- `appgen_x_inbox`
- `idempotent_handlers`
- `retry_dead_letter_evidence`
- `permissions`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `seed_data`
- `workbench`

### Advanced Capabilities

- `event_sourced_case_lifecycle`
- `owned_service_schema_boundary`
- `multi_tenant_case_isolation`
- `schema_evolution_resilient_case_context`
- `omnichannel_case_intake`
- `queue_and_priority_catalog_management`
- `customer_context_projection_handling`
- `preference_projection_handling`
- `entitlement_snapshot_handling`
- `sla_policy_management`
- `skill_based_case_assignment`
- `field_service_handoff_evidence`
- `case_escalation_orchestration`
- `knowledge_suggestion_evidence`
- `customer_update_orchestration`
- `resolution_and_csat_evidence`
- `probabilistic_sla_breach_scoring`
- `counterfactual_assignment_simulation`
- `temporal_backlog_forecasting`
- `autonomous_next_best_response`
- `semantic_case_understanding`
- `predictive_customer_escalation_risk`
- `self_healing_queue_assignment`
- `cryptographic_case_proof`
- `immutable_case_audit_trail`
- `dynamic_service_policy_screening`
- `automated_service_control_testing`
- `automation_insight_evidence`
- `cross_system_customer_preference_workflow_federation`
- `appgen_x_outbox_inbox_eventing`
- `idempotent_handlers`
- `retry_dead_letter_evidence`
- `permissions_governance_evidence`
- `configuration_schema`
- `parameter_engine`
- `rule_engine`
- `seed_data`
- `workbench_ui`
- `governed_model_evidence`

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->
