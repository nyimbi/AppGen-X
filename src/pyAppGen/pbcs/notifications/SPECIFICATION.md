# Notifications PBC

Package-local implementation contract for the Notifications PBC. The package
owns templates, localization variants, channels, recipients, preferences,
consent evidence, schedules, throttling, provider routing, deliveries, retries,
receipts, bounces, campaigns, transactional notifications, audit evidence, and
deliverability analytics. It is a hardened complete-PBC package with executable
schema, service, API, UI, and release-evidence contracts.

## Stable Identity

- PBC key: `notifications`.
- Mesh: relationship.
- Implementation directory: `src/pyAppGen/pbcs/notifications`.
- Runtime module: `runtime.py`.
- UI module: `ui.py`.
- Test module: `tests/test_pbc_notifications_runtime.py`.
- Source registration entrypoint: `implementation_contract()`.
- Supported relational backends: PostgreSQL, MySQL, and MariaDB.
- Event contract: AppGen-X.
- Fixed event topic: `appgen.notifications.events`.
- User-facing stream-engine selection is not exposed.

## Owned Boundary

Owned tables:

- `notification_template`
- `template_locale_variant`
- `delivery_channel`
- `notification_recipient`
- `preference_snapshot`
- `consent_ledger`
- `delivery_schedule`
- `throttle_window`
- `provider_route`
- `message_delivery`
- `delivery_attempt`
- `retry_evidence`
- `delivery_receipt`
- `bounce_event`
- `notification_campaign`
- `campaign_dispatch`
- `transactional_notification`
- `notification_audit_log`
- `deliverability_analytics`
- `notification_rule`
- `notification_parameter`
- `notification_configuration`

Runtime event tables:

- `notifications_appgen_outbox_event`
- `notifications_appgen_inbox_event`
- `notifications_dead_letter_event`

The package does not share customer, workflow, SLA, or profile tables. Cross-PBC
integration is represented only by declared APIs, events, or projections:

- Consumed events: `PreferenceChanged`, `ConsentUpdated`,
  `CampaignScheduled`, `DeliveryReceiptImported`, `BounceRegistered`,
  `SlaBreached`, `WorkflowCompleted`, and
  `TransactionalNotificationRequested`.
- Emitted events: `MessageQueued`, `MessageDelivered`, `MessageFailed`,
  `DeliveryReceiptRecorded`, `BounceRecorded`, `CampaignDispatched`, and
  `TransactionalNotificationDispatched`.
- API dependencies: `GET /recipient-profiles/{recipient_id}`,
  `GET /workflow-events/{workflow_id}`, and `GET /sla-breaches/{breach_id}`.
- Projections: `recipient_projection`, `preference_projection`,
  `consent_projection`, `sla_projection`, `workflow_projection`, and
  `campaign_projection`.

`notifications_verify_owned_table_boundary()` accepts only owned tables, the
runtime event tables, declared AppGen-X events, and the declared API/projection
dependencies above. Direct foreign references such as `customer_profile` are
rejected.

## Standard Capabilities

- Template authoring with required variables, localization variants, and audit
  proof.
- Channel registration for email, SMS, push, and chat with provider health and
  cost evidence.
- Recipient projection, preference snapshots, and consent-ledger evidence from
  inbound AppGen-X events.
- Runtime configuration with fixed AppGen-X topic, database allowlist, retry
  limit, locale set, channel set, timezone, quiet hours, and workbench limit.
- Parameter support for fatigue limits, routing weights, retry limit, TTL,
  campaign batch size, scheduling horizon, and bounce retry window.
- Rule support for consent, delivery, throttling, routing, scheduling, locale,
  and message-type policy.
- Delivery scheduling, quiet-hour enforcement evidence, and provider-route
  selection.
- Message dispatch for campaign and transactional notifications.
- Delivery-attempt, retry, dead-letter, receipt, and bounce evidence.
- Deliverability analytics rollup for deliveries, success rate, failures, and
  bounce totals.
- Audit log evidence for configuration, policy, template, channel, event, send,
  and delivery operations.
- Workbench UI with templates, localization, recipients, preferences, delivery,
  campaigns, transactional flows, analytics, outbox, inbox, and dead letters.

## Advanced Capabilities

- Event-sourced message lifecycle with immutable state-event digests.
- Multi-tenant delivery isolation across templates, channels, recipients,
  preferences, campaigns, deliveries, analytics, and UI.
- Schema-evolution-safe owned-table extensions with package-local migration and
  model descriptors.
- Counterfactual routing, recipient-fatigue scoring, and predictive delivery
  risk evidence.
- Autonomous exception handling through retry and dead-letter evidence.
- Dynamic consent policy screening and self-healing provider routing.
- Deliverability analytics for receipt and bounce evidence.
- AppGen-X outbox/inbox eventing with idempotent handlers and fixed topic.
- Governed model evidence and package-local release auditing.

## Runtime Services

Implemented commands:

- `configure_runtime`
- `set_parameter`
- `register_rule`
- `register_schema_extension`
- `register_template`
- `register_channel`
- `receive_event`
- `send_message`
- `record_delivery_attempt`
- `create_campaign`
- `schedule_notification`
- `create_transactional_notification`
- `route_provider`
- `record_delivery_receipt`
- `record_bounce`
- `record_audit_event`
- `publish_deliverability_analytics`
- `forecast_delivery_window`
- `simulate_channel_routing`
- `recommend_localized_variant`
- `analyze_recipient_fatigue`
- `review_campaign_readiness`
- `review_transactional_history`
- `build_api_contract`
- `build_schema_contract`
- `build_service_contract`
- `build_release_evidence`
- `permissions_contract`
- `build_workbench_view`
- `verify_owned_table_boundary`

`build_service_contract()` additionally declares the broader orchestration
surface used by generated apps:

- campaign creation and dispatch
- transactional notification creation
- provider routing
- delivery receipt and bounce recording
- audit publication
- deliverability analytics publication
- scheduling and simulation queries

## API Contract

Package-local descriptors include:

- `POST /templates`
- `POST /delivery-channels`
- `POST /notifications/rules`
- `POST /notifications/parameters`
- `POST /notifications/configuration`
- `POST /messages`
- `POST /campaigns`
- `POST /delivery-schedules`
- `POST /transactional-notifications`
- `POST /provider-routes`
- `POST /delivery-attempts`
- `POST /delivery-receipts`
- `POST /bounce-events`
- `POST /notification-audit-events`
- `POST /deliverability-analytics/publish`
- `POST /notifications/events/inbox`
- `GET /notifications/contracts/schema`
- `GET /notifications/contracts/service`
- `GET /notifications/release-evidence`
- `GET /notifications-workbench`
- `GET /delivery-window-forecast`
- `GET /channel-routing-simulation`
- `GET /localized-template-recommendation`
- `GET /recipient-fatigue-analysis`
- `GET /campaign-readiness`
- `GET /transactional-history`

Every route descriptor includes owned tables, permission binding, AppGen-X
event-contract evidence, fixed event topic evidence, idempotency evidence where
applicable, and dependency evidence for external projections.

## Schema, Service, And Release Contracts

`notifications_build_schema_contract()` emits:

- generation-ready descriptors for every owned table
- package-local migration paths under `pbcs/notifications/migrations/`
- package-local model descriptors under `pbcs/notifications/models/`
- relationship metadata across templates, recipients, schedules, deliveries,
  campaigns, transactional notifications, receipts, retries, and bounces
- runtime event-table descriptors for outbox, inbox, and dead letters
- backend allowlist evidence, fixed AppGen-X topic evidence, and
  `shared_table_access: False`

`notifications_build_service_contract()` emits:

- standard orchestration for templates, recipients, consent, localization,
  scheduling, routing, throttling, retry/dead-letter handling, receipts,
  bounces, campaigns, transactional notifications, and analytics
- advanced-capability evidence aligned with the runtime capability keys
- idempotent handler evidence
- retry/dead-letter table evidence
- rules/parameters/configuration support evidence
- dependency declarations with no shared-table access

`notifications_build_release_evidence()` is the package-local release gate. It
proves:

- owned-schema depth
- one migration descriptor per owned table
- runtime table declaration for outbox/inbox/dead-letter
- service-contract depth
- fixed AppGen-X API/eventing evidence
- permission coverage for schema/service/release queries
- UI and workbench binding evidence
- boundary validation with zero shared-table access
- backend allowlist compliance

## UI And Workbench

Fragments include:

- `NotificationsWorkbench`
- `TemplateDesigner`
- `LocalizationStudio`
- `DeliveryChannelConsole`
- `RecipientDirectory`
- `PreferenceSnapshotPanel`
- `ConsentLedgerPanel`
- `ScheduleBoard`
- `ThrottlePolicyBoard`
- `ProviderRoutingConsole`
- `MessageComposer`
- `DeliveryStatusBoard`
- `DeliveryReceiptPanel`
- `BounceQueuePanel`
- `CampaignPlanner`
- `TransactionalNotificationConsole`
- `NotificationRuleStudio`
- `NotificationParameterConsole`
- `NotificationConfigurationPanel`
- `NotificationEventOutbox`
- `NotificationDeadLetterQueue`
- `NotificationAuditTrail`
- `DeliverabilityAnalyticsBoard`

Workbench binding evidence includes owned tables, runtime event tables,
permission bindings, fixed AppGen-X configuration evidence, and
deliverability-analytics ownership.

## Verification Targets

Focused runtime tests prove:

- runtime capability coverage for all advanced capability keys
- package `implementation_contract()` exposes schema, service, release,
  required-event-topic, emitted-event, and consumed-event contracts
- schema contract depth, migration/model descriptors, and runtime tables
- service contract depth, idempotent handlers, and orchestration coverage
- API descriptors, permission coverage, and fixed AppGen-X topic evidence
- UI/workbench binding evidence
- configuration, rule, parameter, schema-extension, template, channel, event,
  send, delivery, receipt, bounce, analytics, and dead-letter execution
- boundary enforcement and backend allowlist compliance

## Seed And Release Evidence

Release evidence includes package-local seed data for notification channels,
template categories, consent states, delivery statuses, bounce reasons, and
retry policies. Generated applications validate those seed descriptors with
schema, migration, model, service, route, event, handler, UI, RBAC,
configuration, and release contracts.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `notifications`
- Mesh: `relationship`
- Datastore backend: `postgresql`

### Owned Tables

- `notification_template`
- `template_locale_variant`
- `delivery_channel`
- `notification_recipient`
- `message_delivery`
- `preference_snapshot`
- `consent_ledger`
- `delivery_schedule`
- `throttle_window`
- `provider_route`
- `delivery_attempt`
- `retry_evidence`
- `delivery_receipt`
- `bounce_event`
- `notification_campaign`
- `campaign_dispatch`
- `transactional_notification`
- `notification_audit_log`
- `deliverability_analytics`
- `notification_rule`
- `notification_parameter`
- `notification_configuration`

### API Routes

- `POST /templates`
- `POST /delivery-channels`
- `POST /notifications/rules`
- `POST /notifications/parameters`
- `POST /notifications/configuration`
- `POST /messages`
- `POST /delivery-attempts`
- `POST /notifications/events/inbox`
- `GET /notifications/contracts/schema`
- `GET /notifications/contracts/service`
- `GET /notifications/release-evidence`
- `GET /notifications-workbench`

### Emitted Events

- `MessageQueued`
- `MessageDelivered`
- `MessageFailed`
- `DeliveryReceiptRecorded`
- `BounceRecorded`
- `CampaignDispatched`
- `TransactionalNotificationDispatched`

### Consumed Events

- `PreferenceChanged`
- `ConsentUpdated`
- `CampaignScheduled`
- `DeliveryReceiptImported`
- `BounceRegistered`
- `SlaBreached`
- `WorkflowCompleted`
- `TransactionalNotificationRequested`

### UI Fragments

- `NotificationsWorkbench`
- `TemplateDesigner`
- `LocalizationStudio`
- `DeliveryChannelConsole`
- `RecipientDirectory`
- `PreferenceSnapshotPanel`
- `ConsentLedgerPanel`
- `ScheduleBoard`
- `ThrottlePolicyBoard`
- `ProviderRoutingConsole`
- `MessageComposer`
- `DeliveryStatusBoard`
- `DeliveryReceiptPanel`
- `BounceQueuePanel`
- `CampaignPlanner`
- `TransactionalNotificationConsole`
- `NotificationRuleStudio`
- `NotificationParameterConsole`
- `NotificationConfigurationPanel`
- `NotificationEventOutbox`
- `NotificationDeadLetterQueue`
- `NotificationAuditTrail`
- `DeliverabilityAnalyticsBoard`

### Permissions

- `notifications.analytics.read`
- `notifications.audit`
- `notifications.campaign.write`
- `notifications.channel.write`
- `notifications.configure`
- `notifications.consent.write`
- `notifications.event.consume`
- `notifications.message.send`
- `notifications.recipient.write`
- `notifications.template.write`

### Configuration Keys

- `NOTIFICATIONS_DATABASE_URL`
- `NOTIFICATIONS_EVENT_TOPIC`
- `NOTIFICATIONS_RETRY_LIMIT`
- `NOTIFICATIONS_DEFAULT_LOCALE`
- `NOTIFICATIONS_DEFAULT_TIMEZONE`
- `NOTIFICATIONS_DELIVERY_MODE`

### Standard Features

- `notification_template`
- `template_locale_variant`
- `delivery_channel`
- `notification_recipient`
- `preference_snapshot`
- `consent_ledger`
- `delivery_schedule`
- `throttle_window`
- `provider_route`
- `message_delivery`
- `delivery_attempt`
- `retry_evidence`
- `delivery_receipt`
- `bounce_event`
- `notification_campaign`
- `campaign_dispatch`
- `transactional_notification`
- `notification_audit_log`
- `deliverability_analytics`
- `omnichannel_routing`
- `template_rendering`
- `consent_and_preference_enforcement`
- `scheduling`
- `throttling`
- `localization`
- `campaign_orchestration`
- `transactional_notifications`
- `delivery_status_api`
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
- `schema_contract`
- `service_contract`
- `release_evidence`

### Advanced Capabilities

- `event_sourced_message_lifecycle`
- `owned_notification_schema_boundary`
- `multi_tenant_delivery_isolation`
- `schema_evolution_resilient_template_context`
- `omnichannel_template_management`
- `recipient_profile_projection_handling`
- `preference_snapshot_projection_handling`
- `consent_ledger_evidence`
- `delivery_schedule_and_quiet_hour_forecasting`
- `throttling_and_fatigue_controls`
- `provider_routing_and_failover`
- `template_rendering_and_personalization`
- `delivery_attempt_tracking`
- `delivery_receipt_and_bounce_evidence`
- `campaign_and_transactional_notification_orchestration`
- `localization_variant_management`
- `probabilistic_delivery_risk_scoring`
- `counterfactual_channel_selection_simulation`
- `autonomous_delivery_exception_resolution`
- `semantic_message_instruction_understanding`
- `predictive_recipient_fatigue_risk`
- `self_healing_channel_route_selection`
- `cryptographic_delivery_proof`
- `immutable_delivery_audit_trail`
- `dynamic_consent_policy_screening`
- `automated_communication_control_testing`
- `cross_system_preference_workflow_service_federation`
- `deliverability_analytics_rollup`
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

## Agent, Chatbot Skills, And Self-Registration Contract

The `notifications` package exposes a first-class PBC agent and chatbot interface through `agent.py`. The composed application imports these capabilities under the `notifications_skills` namespace so a single application assistant can route help, task guidance, document instruction intake, governed datastore CRUD planning, workbench navigation, and policy explanation back to the owning PBC instead of inventing cross-package mutations. The agent contract is scoped to the `Omni-Channel Communication and Notifications` boundary and must name the command, permission, owned tables, idempotency key, expected AppGen-X event, and human confirmation requirement before any create, update, or delete plan is eligible to execute.

Document and instruction intake is explicit release evidence. The chatbot can accept uploaded documents, operational notes, or user instructions, extract candidate facts for owned tables such as `notifications_notification_template`, `notifications_template_locale_variant`, `notifications_delivery_channel`, `notifications_notification_recipient`, `notifications_preference_snapshot`, `notifications_consent_ledger`, validate those facts against package rules, parameters, configuration, and permissions, and return a side-effect-free mutation preview. The preview is not a write. It is a governed plan that references service operations such as `configure_runtime`, `set_parameter`, `register_rule`, `register_schema_extension`, `register_template`, `register_channel`, uses AppGen-X event expectations such as `MessageQueued`, `MessageDelivered`, `MessageFailed`, `DeliveryReceiptRecorded`, rejects foreign tables, and records whether a read-only query or a confirmed command is required. This keeps AI assistance professional, auditable, and bounded to the PBC datastore.

Self-registration is also part of the specification. `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` must produce a side-effect-free discovery and registration plan for `notifications`. Registration metadata identifies the source package directory, required artifacts, owned datastore, AppGen-X event contract, UI fragments, RBAC descriptors, configuration schema, seed data, tests, and release evidence without mutating the global catalog during discovery. Composition tooling may then register the PBC, merge the `notifications_skills` contribution into the single composed assistant, and expose the workbench UI while preserving owned-table boundaries and declared API/event/projection dependencies.

