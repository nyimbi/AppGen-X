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
- `POST /delivery-attempts`
- `POST /notifications/events/inbox`
- `GET /notifications/contracts/schema`
- `GET /notifications/contracts/service`
- `GET /notifications/release-evidence`
- `GET /notifications-workbench`

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
