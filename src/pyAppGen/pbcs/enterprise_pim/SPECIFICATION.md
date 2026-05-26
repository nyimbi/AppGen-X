# Enterprise PIM

Package-local implementation contract for the Enterprise PIM PBC. The package owns enterprise product-information governance for taxonomies, attribute models, localized content, validation workflow, dependency intake, publication readiness, rules, parameters, configuration, UI fragments, and AppGen-X event evidence.

## Stable Identity

- PBC key: `enterprise_pim`.
- Implementation directory: `src/pyAppGen/pbcs/enterprise_pim`.
- Runtime module: `runtime.py`.
- UI module: `ui.py`.
- Test module: `tests/test_pbc_enterprise_pim_runtime.py`.
- Event topic: `appgen.enterprise-pim.events`.
- Event contract: AppGen-X.
- Supported relational backends: PostgreSQL, MySQL, and MariaDB.
- User-facing stream-engine selection is not exposed.

## Owned Boundary

Owned tables and generated model artifacts:

- `product_taxonomy`
- `product_attribute`
- `localized_content`
- `validation_workflow`
- `dependency_schema`
- `dependency_projection`
- `pim_rule`
- `pim_parameter`
- `pim_configuration`
- `enterprise_pim_appgen_outbox_event`
- `enterprise_pim_appgen_inbox_event`
- `enterprise_pim_dead_letter_event`

The PBC does not share product, media, pricing, tax, inventory, search, or commerce tables. Cross-PBC data is represented through:

- Declared dependency schemas.
- AppGen-X events: `MediaAssetApproved`, `PricePromotionApproved`, `TaxCalculated`, `InventoryPositionUpdated`.
- API/projection dependencies: `media_projection`, `pricing_projection`, `tax_projection`, `inventory_projection`, `catalog_projection`, and `search_projection`.
- Published outbox events: `TaxonomyClassified`, `AttributeDefined`, `ContentLocalized`, `ValidationApproved`, and `PimMasterDataReady`.

## Standard Capabilities

- Enterprise taxonomy creation with hierarchy, lineage, parent-child topology, localized names, and status transitions.
- Product attribute definition with data type, required flag, inherited value, localized labels, compiled hash, and active/blocked state.
- Attribute inheritance with configurable maximum depth.
- Localized content upsert with locale validation, default-locale fallback, translation quality scoring, and localized override metadata.
- Validation workflow start and approval with required approver steps, SLA evidence, approval trail, and taxonomy approval propagation.
- Publication readiness evaluation across required locales, required attributes, approved workflow, dependency projections, taxonomy status, and channel configuration.
- Dependency schema acceptance with schema version floors and accepted event validation.
- Dependency projection intake through idempotent AppGen-X inbox handlers.
- Retry and dead-letter evidence for unsupported or failed dependency events.
- Rule engine with deterministic compiled hashes for locale, attribute, validation, dependency, and publication policy.
- Parameter engine for completeness, translation quality, SLA, inheritance depth, retry, schema version floor, anomaly threshold, and workbench limit.
- Configuration schema with backend, event topic, retry limit, default locale, allowed locales, channels, dependency sources, and workbench limit.
- Seed data for default locale and workflow steps.
- Workbench views for taxonomies, attributes, localization, workflows, dependencies, eventing, rules, parameters, configuration, and audit evidence.
- RBAC descriptors for taxonomy, attribute, localization, workflow, approval, integration, configuration, and audit operations.

## Advanced Capabilities

- Event-sourced PIM mutation log with immutable hash-chain audit evidence.
- Graph-relational taxonomy topology and attribute inheritance graph evidence.
- Multi-tenant isolation for taxonomy, attribute, content, workflow, and workbench projections.
- Schema-on-read extension for owned tables with validated field identifiers.
- Multilingual inheritance and locale fallback across taxonomy names, attribute labels, and localized content.
- Probabilistic completeness and translation-quality scoring for publication readiness.
- Counterfactual taxonomy publication simulation across proposed locales.
- Temporal enrichment readiness forecasting for catalog-scale rollout planning.
- Autonomous enrichment exception recommendations for missing locales, attributes, and dependency schemas.
- Semantic PIM instruction parsing for taxonomy, locale, and requested action.
- Predictive validation-risk scoring from missing locale, dependency, and SLA signals.
- Self-healing dependency route selection with failover idempotency.
- Cryptographic master-data proof generation for selective disclosure.
- Dynamic policy screening against restricted taxonomy terms.
- Continuous control tests for configuration, rules, parameters, dependency schemas, taxonomy approval, and hash-chain integrity.
- Cross-system federation through declared catalog, media, pricing, tax, and inventory projections.
- Chaos-tolerant dependency drills with degraded outbox mode and dead-letter topics.
- Crypto-agile epoch rotation.
- Carbon-aware enrichment scheduling.
- Mathematical taxonomy optimization for coverage and complexity.
- Mechanism-design workflow allocation across data-steward and compliance queues.
- PIM content anomaly detection with entropy and outlier evidence.
- Stochastic enrichment exposure modeling.
- Governed model registration with regulated status, explainability, lineage, and approval evidence.

## Runtime Services

- `configure_runtime` validates backend, event topic, retry limits, locale/channel/dependency configuration, and rejects stream-picker fields.
- `set_parameter` accepts only supported parameters and records compiled parameter evidence.
- `register_rule` requires locale, attribute, and validation-policy fields and stores deterministic rule evidence.
- `register_schema_extension` accepts only owned-table schema extensions.
- `accept_dependency_schema` validates dependency source, schema version floor, and consumed AppGen-X event types.
- `receive_event` performs idempotent dependency intake, projection storage, retry handling, and dead-letter recording.
- `create_taxonomy` owns taxonomy hierarchy and emits `TaxonomyClassified`.
- `define_attribute` owns typed attribute definitions and emits `AttributeDefined`.
- `upsert_localized_content` owns localized content and emits `ContentLocalized`.
- `start_validation_workflow` and `approve_validation_workflow` own workflow state and emit `ValidationApproved`.
- `publish_master_data` emits `PimMasterDataReady` only after readiness checks.
- `build_api_contract` emits descriptor-level route, permission, idempotency, event, and dependency evidence.
- `permissions_contract` maps commands to RBAC permissions.
- `verify_owned_table_boundary` accepts owned tables and declared dependencies, then reports direct foreign-table violations.
- `build_workbench_view` exposes operational and release evidence.

## API Contract

- `POST /product-taxonomies` maps to `create_taxonomy`.
- `POST /product-attributes` maps to `define_attribute`.
- `POST /localized-content` maps to `upsert_localized_content`.
- `POST /validation-workflows` maps to `start_validation_workflow`.
- `POST /validation-workflows/{id}/approve` maps to `approve_validation_workflow`.
- `POST /dependency-schemas` maps to `accept_dependency_schema`.
- `POST /pim-events` maps to `receive_event`.
- `POST /pim-publications` maps to `publish_master_data`.
- `GET /pim-workbench` maps to `build_workbench_view`.

Every route descriptor states owned tables, command or query binding, idempotency key, required permission, emitted events, consumed events, and declared API or projection dependencies where applicable.

## Events And Handlers

Emitted events:

- `TaxonomyClassified`
- `AttributeDefined`
- `ContentLocalized`
- `ValidationApproved`
- `PimMasterDataReady`

Consumed events:

- `MediaAssetApproved`
- `PricePromotionApproved`
- `TaxCalculated`
- `InventoryPositionUpdated`

Handlers are idempotent by event id or idempotency key. Unsupported events, failed dependency processing, and exhausted retries produce dead-letter records. The workbench surfaces outbox, inbox, and dead-letter counts.

## Rules, Parameters, And Configuration

Rules require:

- `rule_id`
- `tenant`
- `scope`
- `status`
- `required_locales`
- `required_attributes`
- `validation_policy`

Parameters include:

- `minimum_completeness`
- `minimum_translation_quality`
- `validation_sla_hours`
- `max_inheritance_depth`
- `dead_letter_retry_limit`
- `dependency_schema_version_floor`
- `anomaly_zscore_threshold`
- `workbench_limit`

Configuration includes backend, event topic, retry limit, default locale, allowed locales, allowed channels, dependency sources, and workbench limit. Runtime configuration records `event_contract: AppGen-X`, `allowed_database_backends`, owned tables, and `stream_engine_picker_visible: False`.

## UI And Workbench

UI fragments:

- `EnterprisePimWorkbench`
- `TaxonomyGraphStudio`
- `AttributeDefinitionStudio`
- `AttributeInheritanceInspector`
- `LocalizationWorkbench`
- `ValidationWorkflowBoard`
- `DependencySchemaConsole`
- `PimEventOutbox`
- `PimDeadLetterQueue`
- `PimRuleStudio`
- `PimParameterConsole`
- `PimConfigurationPanel`
- `PimAuditEvidencePanel`

The workbench exposes visible actions based on RBAC, binds to owned tables and event evidence, and includes binding evidence for owned tables, outbox, inbox, and dead-letter artifacts.

## Release Evidence

The focused test suite proves:

- Runtime smoke covers every declared standard and advanced capability key.
- The package declares owned tables, allowed relational backends, AppGen-X eventing, descriptor APIs, and action-level RBAC.
- Configuration, rules, parameters, dependency schemas, schema extensions, events, workflows, and UI contracts execute.
- Publication readiness uses locales, attributes, workflow approval, dependency projections, and channel policy.
- Boundary validation accepts owned tables and declared API/event/projection dependencies while rejecting direct foreign-table references.
- Invalid backend, stream picker fields, unsupported parameters, unsupported dependency events, non-owned schema extensions, and unsupported inbox events fail with evidence.
