# Enterprise Product Catalog and PIM PBC Specification

## Scope

`product_catalog_pim` owns package-local product information management for
AppGen-X composable applications. It manages product masters, product families,
variant metadata, attribute schemas, localized content, media references,
publication readiness, compliance claims, catalog publication evidence, rules,
parameters, runtime configuration, UI workbench fragments, and AppGen-X
outbox/inbox operational evidence.

The package composes with commerce, pricing, inventory, tax, content, and
search through APIs, AppGen-X events, and read-model projections only. It does
not read or write shared tables from other PBCs.

## Owned Boundary

Owned tables:

- `product`
- `product_family`
- `product_variant`
- `product_attribute_schema`
- `product_attribute`
- `product_price`
- `product_media`
- `product_locale_content`
- `product_compliance_claim`
- `catalog_publication`
- `catalog_channel_projection`
- `product_rule`
- `product_parameter`
- `product_configuration`

Runtime tables:

- `product_catalog_pim_appgen_outbox_event`
- `product_catalog_pim_appgen_inbox_event`
- `product_catalog_pim_dead_letter_event`

Allowed datastore backends are PostgreSQL, MySQL, and MariaDB. Configuration is
bound to the fixed AppGen-X event topic `appgen.product.events`. Stream-engine
selection is not user-configurable and no stream-picker surface is exposed.

## Standard Capabilities

- Product family creation, product registration, SKU governance, lifecycle
  management, and tenant isolation.
- Attribute schema definition, typed attribute assignment, required-field
  validation, and owned-table schema extension governance.
- Localized content approval, media-rights validation, price readiness, and
  compliance-claim screening.
- Catalog publication orchestration with completeness scoring, channel gating,
  handoff evidence, and workbench visibility.
- Rules, parameters, runtime configuration, owned-table boundary checks,
  idempotent AppGen-X inbox handling, retry evidence, dead-letter evidence, API
  contracts, permissions contracts, and UI contract evidence.

## Advanced Capabilities

- Event-sourced product lifecycle with immutable hash chaining.
- Graph-relational topology across families, products, attributes, media,
  channels, locales, prices, and compliance evidence.
- Counterfactual publication simulation and temporal sellability forecasting.
- Predictive readiness risk scoring, policy screening, and exception
  recommendation.
- Publication route failover, cryptographic publication proof, resilience drill
  evidence, carbon-aware scheduling, mathematical allocation, anomaly
  detection, stochastic exposure modeling, and governed readiness models.

## Configuration, Rules, and Parameters

`configure_runtime` accepts only these configuration fields:

- `database_backend`
- `event_topic`
- `retry_limit`
- `allowed_channels`
- `allowed_locales`
- `allowed_media_roles`
- `allowed_regions`
- `default_timezone`
- `workbench_limit`

Runtime configuration must:

- reject backends outside PostgreSQL, MySQL, and MariaDB
- reject stream-engine and user-selectable eventing fields
- require the exact AppGen-X topic `appgen.product.events`
- record `event_contract: AppGen-X`
- record owned tables and hidden stream-picker evidence

Supported parameters are:

- `minimum_completeness`
- `minimum_margin`
- `max_missing_required_attributes`
- `content_quality_threshold`
- `publication_batch_size`
- `retention_days`
- `workbench_limit`

Rule registration requires:

- `rule_id`
- `tenant`
- `rule_type`
- `allowed_channels`
- `allowed_locales`
- `required_attributes`
- `required_media_roles`
- `restricted_regions`
- `status`

Rules compile into deterministic hashes and preserve compile evidence.

## Schema Extensions and Boundary Proof

`register_schema_extension` accepts only owned tables. Any schema extension
target outside `product_catalog_pim` owned tables is rejected.

`verify_owned_table_boundary` accepts only:

- product-catalog-owned tables
- declared AppGen-X consumed event types
- product-catalog runtime tables
- declared API or projection dependencies

The boundary proof reports direct violations and declares
`shared_table_access: false`.

## API Contract

The package-local API contract includes:

- `POST /product-families` -> `create_product_family`
- `POST /products` -> `register_product`
- `POST /attribute-schemas` -> `define_attribute_schema`
- `POST /product-attributes` -> `set_product_attribute`
- `POST /product-media` -> `attach_product_media`
- `POST /product-locale-content` -> `add_localized_content`
- `POST /product-prices` -> `add_price_metadata`
- `POST /product-compliance-claims` -> `add_compliance_claim`
- `POST /catalog-publications` -> `publish_product`
- `POST /product-catalog/events/inbox` -> `receive_event`
- `GET /product-catalog/workbench` -> `build_workbench_view`

Every route descriptor includes owned tables, command or query binding, RBAC
permission, emitted or consumed events where applicable, and an idempotency-key
strategy. The API contract declares:

- `event_contract: AppGen-X`
- allowed relational backends only
- `shared_table_access: false`
- hidden stream-engine picker evidence

## Event Contract

Emitted:

- `ProductClassified`
- `ProductRegistered`
- `AttributeSchemaDefined`
- `ProductEnriched`
- `ProductMediaAttached`
- `ProductPriceReady`
- `ProductComplianceClaimed`
- `ProductPublished`

Consumed:

- `TaxCalculated`
- `MediaAssetApproved`
- `InventoryPositionUpdated`
- `PricePromotionApproved`
- `SearchIndexRequested`

`receive_event` is idempotent by explicit `idempotency_key` or
`event_type:event_id`. It must:

- record inbox evidence for each processing attempt
- reject unsupported or simulated-failure events with retry evidence
- dead-letter exhausted failures into `product_catalog_pim_dead_letter_event`
- avoid duplicate state mutation after successful processing
- project only package-local read evidence; never access shared tables

## Permissions Contract

The package declares action-level RBAC for:

- `create_product_family`
- `register_product`
- `define_attribute_schema`
- `set_product_attribute`
- `add_localized_content`
- `attach_product_media`
- `add_price_metadata`
- `add_compliance_claim`
- `publish_product`
- `receive_event`
- `register_rule`
- `register_schema_extension`
- `set_parameter`
- `configure_runtime`
- `run_control_tests`
- `build_workbench_view`
- `verify_owned_table_boundary`

Representative permissions are:

- `product_catalog_pim.read`
- `product_catalog_pim.product`
- `product_catalog_pim.enrich`
- `product_catalog_pim.publish`
- `product_catalog_pim.configure`
- `product_catalog_pim.event`
- `product_catalog_pim.audit`

## UI Contract

The package-local UI contract exposes workbench fragments for product master
operations, enrichment, publication, rules, parameters, and configuration.

If the package-local UI is present, it must surface:

- configuration, rule, and parameter bindings
- outbox, inbox, and dead-letter evidence
- runtime-table names for UI bindings
- action-level RBAC evidence for visible and locked actions
- `event_contract: AppGen-X` and hidden stream-picker evidence

## Verification Expectations

Focused runtime verification must prove:

- standard and advanced product catalog workflows execute
- configuration, rules, parameters, and UI contracts bind correctly
- schema extensions are limited to owned tables
- API and permissions contracts declare AppGen-X and no shared-table access
- `receive_event` is idempotent with inbox, retry, and dead-letter evidence
- boundary verification rejects foreign-table references
