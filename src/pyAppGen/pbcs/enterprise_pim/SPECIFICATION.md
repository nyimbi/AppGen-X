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
- `taxonomy_node`
- `taxonomy_relationship`
- `taxonomy_publication`
- `taxonomy_classification_candidate`
- `product_attribute`
- `attribute_group`
- `attribute_value_option`
- `attribute_inheritance_rule`
- `attribute_validation_rule`
- `attribute_quality_signal`
- `localized_content`
- `localized_content_version`
- `translation_memory_entry`
- `locale_fallback_rule`
- `content_completeness_score`
- `validation_workflow`
- `validation_workflow_step`
- `approval_decision`
- `publication_readiness_check`
- `dependency_schema`
- `dependency_projection`
- `media_dependency_projection`
- `price_dependency_projection`
- `tax_dependency_projection`
- `inventory_dependency_projection`
- `search_dependency_projection`
- `catalog_publication_projection`
- `channel_publication_policy`
- `product_relationship`
- `product_bundle_definition`
- `product_variant_family`
- `product_variant_member`
- `assortment_assignment`
- `data_steward_assignment`
- `pim_exception`
- `exception_resolution_plan`
- `pim_audit_trace`
- `pim_master_data_proof`
- `pim_policy_screening`
- `pim_federation_projection`
- `carbon_enrichment_window`
- `taxonomy_optimization_plan`
- `workflow_allocation`
- `content_anomaly_signal`
- `enrichment_forecast`
- `enrichment_risk_model`
- `semantic_instruction_parse`
- `pim_schema_extension`
- `pim_control_assertion`
- `pim_governed_model`
- `pim_seed_data`
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
- Attribute group creation with ordered attribute membership and owned taxonomy validation.
- Attribute value-option registration with owned-attribute validation.
- Attribute validation-rule registration with sample-value evaluation and quality-signal evidence.
- Attribute inheritance with configurable maximum depth.
- Localized content upsert with locale validation, default-locale fallback, translation quality scoring, and localized override metadata.
- Translation-memory upsert with source-text hashing, target-locale quality scoring, and approval status.
- Locale fallback-rule registration with configured-locale validation.
- Product relationship modeling for accessory, substitute, compatibility, and bundle-style product graph edges.
- Product bundle definition with component references, component counts, and bundle policy evidence.
- Variant-family and variant-member lifecycle support with required axis validation.
- Assortment assignment by channel and market using configured channel policy.
- Data-steward assignment for explicit ownership and accountability.
- PIM exception open and resolution workflows with resolution-plan evidence.
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
- `create_attribute_group` owns grouped attribute presentation and governance membership.
- `register_attribute_value_option` owns controlled values for enumerated attributes.
- `register_attribute_validation_rule` owns validation logic plus attribute-quality evidence.
- `upsert_localized_content` owns localized content and emits `ContentLocalized`.
- `upsert_translation_memory` owns translation-memory evidence for reusable localized phrases.
- `register_locale_fallback_rule` owns locale fallback policy.
- `start_validation_workflow` and `approve_validation_workflow` own workflow state and emit `ValidationApproved`.
- `create_product_relationship`, `define_product_bundle`, `define_variant_family`, `add_variant_member`, `assign_assortment`, and `assign_data_steward` own relationship, bundling, variant, channel, and stewardship execution.
- `open_pim_exception` and `resolve_pim_exception` own exception lifecycle and resolution-plan evidence.
- `publish_master_data` emits `PimMasterDataReady` only after readiness checks.
- `build_api_contract` emits descriptor-level route, permission, idempotency, event, and dependency evidence.
- `permissions_contract` maps commands to RBAC permissions.
- `verify_owned_table_boundary` accepts owned tables and declared dependencies, then reports direct foreign-table violations.
- `build_workbench_view` exposes operational and release evidence.

## API Contract

- `POST /product-taxonomies` maps to `create_taxonomy`.
- `POST /product-attributes` maps to `define_attribute`.
- `POST /attribute-groups` maps to `create_attribute_group`.
- `POST /attribute-options` maps to `register_attribute_value_option`.
- `POST /attribute-validation-rules` maps to `register_attribute_validation_rule`.
- `POST /localized-content` maps to `upsert_localized_content`.
- `POST /translation-memory` maps to `upsert_translation_memory`.
- `POST /locale-fallback-rules` maps to `register_locale_fallback_rule`.
- `POST /validation-workflows` maps to `start_validation_workflow`.
- `POST /validation-workflows/{id}/approve` maps to `approve_validation_workflow`.
- `POST /dependency-schemas` maps to `accept_dependency_schema`.
- `POST /product-relationships` maps to `create_product_relationship`.
- `POST /product-bundles` maps to `define_product_bundle`.
- `POST /variant-families` maps to `define_variant_family`.
- `POST /variant-members` maps to `add_variant_member`.
- `POST /assortments` maps to `assign_assortment`.
- `POST /data-stewards` maps to `assign_data_steward`.
- `POST /pim-exceptions` maps to `open_pim_exception`.
- `POST /pim-exceptions/{id}/resolve` maps to `resolve_pim_exception`.
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
- `AttributeGroupCreated`
- `AttributeOptionRegistered`
- `AttributeValidationRuleRegistered`
- `TranslationMemoryUpdated`
- `LocaleFallbackRegistered`
- `ProductRelationshipCreated`
- `ProductBundleDefined`
- `VariantFamilyDefined`
- `VariantMemberAdded`
- `AssortmentAssigned`
- `DataStewardAssigned`
- `PimExceptionOpened`
- `PimExceptionResolved`

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

## Generated Schema, Services, And Release Evidence

`enterprise_pim_build_schema_contract` emits generation-ready table, field, relationship, model, and migration descriptors for every owned table. Migration paths are package-local under `pbcs/enterprise_pim/migrations/{sequence}_{table}.sql`, generated models are package-local under `pbcs/enterprise_pim/models/{table}.py`, datastore backends are limited to PostgreSQL, MySQL, and MariaDB, and `shared_table_access` is always false.

`enterprise_pim_build_service_contract` publishes the command and query surface used by generated applications: runtime configuration, parameters, rules, schema extension, dependency-schema acceptance, idempotent inbox handling, taxonomy creation, attribute definition, localized content upsert, workflow start and approval, publication readiness, route failover, selective disclosure proof generation, policy screening, federation, resilience drills, crypto epoch rotation, carbon-aware enrichment, taxonomy optimization, workflow allocation, control testing, governed model registration, and boundary verification.

`enterprise_pim_build_release_evidence` is the package-local release gate. It proves owned schema depth, one migration descriptor per owned table, service command depth, AppGen-X-only API/eventing, permission coverage for core commands, backend allowlist compliance, no shared table access, and UI/workbench evidence.

## Release Evidence

The focused test suite proves:

- Runtime smoke covers every declared standard and advanced capability key.
- The package declares owned tables, allowed relational backends, AppGen-X eventing, descriptor APIs, and action-level RBAC.
- Configuration, rules, parameters, dependency schemas, schema extensions, events, workflows, and UI contracts execute.
- Publication readiness uses locales, attributes, workflow approval, dependency projections, and channel policy.
- Boundary validation accepts owned tables and declared API/event/projection dependencies while rejecting direct foreign-table references.
- Invalid backend, stream picker fields, unsupported parameters, unsupported dependency events, non-owned schema extensions, and unsupported inbox events fail with evidence.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `enterprise_pim`
- Mesh: `content`
- Datastore backend: `None`

### Owned Tables

- `product_taxonomy`
- `taxonomy_node`
- `taxonomy_relationship`
- `product_attribute`
- `attribute_group`
- `attribute_validation_rule`
- `localized_content`
- `localized_content_version`
- `validation_workflow`
- `validation_workflow_step`
- `approval_decision`
- `publication_readiness_check`
- `dependency_schema`
- `dependency_projection`
- `pim_rule`
- `pim_parameter`
- `pim_configuration`

### API Routes

- `POST /product-taxonomies`
- `POST /product-attributes`
- `POST /localized-content`
- `POST /validation-workflows`
- `POST /validation-workflows/{id}/approve`
- `POST /dependency-schemas`
- `POST /pim-events`
- `POST /pim-publications`
- `GET /pim-workbench`

### Emitted Events

- `TaxonomyClassified`
- `AttributeDefined`
- `ContentLocalized`
- `ValidationApproved`
- `PimMasterDataReady`

### Consumed Events

- `InventoryPositionUpdated`
- `MediaAssetApproved`
- `PricePromotionApproved`
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
