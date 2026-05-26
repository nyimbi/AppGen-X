# Product Catalog PIM PBC Specification

## Scope

`product_catalog_pim` owns package-local product catalog and product
information management behavior for AppGen-X applications. The package governs
product masters, families, variants, taxonomies, categories, assortments,
attribute schemas, localized content, media evidence, pricing metadata,
approval and lifecycle evidence, publication readiness, syndication evidence,
rules, parameters, configuration, API descriptors, permissions, UI/workbench
bindings, and AppGen-X event evidence.

The package integrates with commerce, pricing, inventory, tax, content, and
search through AppGen-X events, API descriptors, and read-only projections
only. It must not read or write shared tables from other PBCs.

Source registration entrypoint: `implementation_contract()`.

Package-local contract builders:

- `product_catalog_pim_build_schema_contract()`
- `product_catalog_pim_build_service_contract()`
- `product_catalog_pim_build_release_evidence()`

## Owned Boundary

### Owned tables

Core master-data tables:

- `product`
- `product_family`
- `product_variant`
- `product_variant_option`
- `product_variant_member`
- `product_taxonomy`
- `taxonomy_node`
- `taxonomy_relationship`
- `product_category`
- `category_assignment`

Attribute, content, and media tables:

- `product_attribute_schema`
- `product_attribute`
- `product_attribute_validation_rule`
- `product_attribute_value_option`
- `product_locale_content`
- `product_localization_memory`
- `product_seo_metadata`
- `product_media`
- `product_enrichment_task`

Pricing, lifecycle, approval, and publication tables:

- `product_price`
- `product_channel_price`
- `product_compliance_claim`
- `product_lifecycle_stage`
- `product_approval_workflow`
- `product_approval_decision`
- `catalog_publication`
- `catalog_channel_projection`
- `catalog_channel_policy`
- `catalog_syndication_feed`
- `catalog_syndication_delivery`

Assortment, quality, graph, governance, and advanced evidence tables:

- `product_assortment`
- `product_assortment_assignment`
- `product_data_quality_score`
- `product_data_quality_issue`
- `product_bundle_definition`
- `product_relationship`
- `product_identity_credential`
- `product_graph_projection`
- `product_semantic_embedding`
- `product_readiness_forecast`
- `product_risk_model`
- `product_policy_screening`
- `product_publication_proof`
- `product_audit_trace`
- `product_schema_extension`
- `product_control_assertion`
- `product_governed_model`
- `product_seed_data`
- `product_rule`
- `product_parameter`
- `product_configuration`

### Runtime tables

- `product_catalog_pim_appgen_outbox_event`
- `product_catalog_pim_appgen_inbox_event`
- `product_catalog_pim_dead_letter_event`

### Datastore and eventing constraints

- Allowed relational backends: PostgreSQL, MySQL, MariaDB.
- Required event contract: `AppGen-X`.
- Required event topic: `appgen.product.events`.
- Stream-engine selection is not user-configurable.
- No stream picker, stream-engine picker, or user eventing choice surface may be
  exposed.
- Shared table access must remain `false`.

## Standard Capabilities

The package-local standard feature contract covers:

- Product master records, family modeling, variant modeling, and SKU
  governance.
- Taxonomy assignment, taxonomy hierarchy, category management, and assortment
  management.
- Attribute schemas, validation rules, value options, and enrichment tasking.
- Localized content, localization memory, SEO metadata, and media-rights
  evidence.
- Channel pricing, channel projections, channel policy, publication, and
  syndication.
- Lifecycle evidence, approval workflow evidence, compliance claims, and
  restricted-region screening.
- Data-quality scoring, product relationships, bundle definitions, rules,
  parameters, configuration, owned-table boundary validation, AppGen-X
  outbox/inbox eventing, idempotent handlers, retry/dead-letter evidence,
  permissions, UI/workbench evidence, and release evidence.

## Advanced Runtime Capabilities

Advanced runtime evidence must cover:

- Event-sourced product lifecycle with immutable hash chaining.
- Graph-relational product topology across families, variants, taxonomies,
  categories, attributes, channels, locales, and compliance artifacts.
- Counterfactual publication simulation and temporal sellability forecasting.
- Semantic instruction parsing, predictive readiness risk, and anomaly
  detection.
- Publication-route failover, publication proofs, resilience drills,
  cryptographic epoch rotation, and carbon-aware publication.
- Mathematical optimization, mechanism-design channel allocation, stochastic
  exposure modeling, federated views, decentralized identity evidence, and
  governed model evidence.

`product_catalog_pim_runtime_smoke()` must exercise every advanced capability
key and return `ok: true`.

## Configuration, Rules, and Parameters

### Supported configuration fields

- `database_backend`
- `event_topic`
- `retry_limit`
- `allowed_channels`
- `allowed_locales`
- `allowed_media_roles`
- `allowed_regions`
- `default_timezone`
- `workbench_limit`

Configuration rules:

- Reject backends outside PostgreSQL, MySQL, and MariaDB.
- Reject any stream-engine, stream picker, or user-selectable eventing fields.
- Require the exact AppGen-X topic `appgen.product.events`.
- Record `event_contract: AppGen-X`.
- Record owned-table evidence and hidden stream-picker evidence.

### Supported parameters

- `minimum_completeness`
- `minimum_margin`
- `max_missing_required_attributes`
- `content_quality_threshold`
- `publication_batch_size`
- `retention_days`
- `workbench_limit`

### Rule registration requirements

- `rule_id`
- `tenant`
- `rule_type`
- `allowed_channels`
- `allowed_locales`
- `required_attributes`
- `required_media_roles`
- `restricted_regions`
- `status`

Rules compile into deterministic hashes and retain compile evidence.

## Schema Contract

`product_catalog_pim_build_schema_contract()` must declare:

- Every owned table with generated field metadata.
- Runtime table descriptors for outbox, inbox, and dead-letter evidence.
- Owned-table relationships across product, variant, schema, publication,
  assortment, and approval structures.
- Generated migration descriptors for every owned table under
  `pbcs/product_catalog_pim/migrations/`.
- Generated model descriptors for every owned table under
  `pbcs/product_catalog_pim/models/`.
- Allowed prefix evidence for `product_`, `catalog_`, `taxonomy_`, and
  `category_` tables.
- `shared_table_access: false`.

The schema contract must prove standard PIM table-stakes plus advanced
semantic, analytics, and governance structures are represented in package-local
metadata.

## Service Contract

`product_catalog_pim_build_service_contract()` must declare:

- Command methods for configuration, rules, parameters, schema extension,
  consumed-event handling, family/product/schema creation, enrichment, pricing,
  compliance, publishing, proofs, screening, resilience, optimization, channel
  allocation, governed-model registration, and boundary verification.
- Query methods for workbench views, simulations, forecasts, semantic parsing,
  risk scoring, recommendations, schema/service/release evidence, permissions,
  binding evidence, federated views, identity evidence, anomaly detection, and
  stochastic exposure modeling.
- Transaction boundary:
  `product_catalog_pim_owned_datastore_plus_appgen_outbox`.
- Idempotent handler evidence for `receive_event`.
- Retry/dead-letter evidence backed by inbox/dead-letter runtime tables.
- Rules/parameters/configuration governance evidence.
- External dependency evidence limited to declared APIs, AppGen-X consumed
  events, and read-model projections.
- `shared_tables: ()`.

## API Contract

`product_catalog_pim_build_api_contract()` must expose package-local descriptors
for:

- `PUT /product-catalog/configuration`
- `POST /product-catalog/rules`
- `POST /product-catalog/parameters`
- `POST /product-catalog/schema-extensions`
- `POST /product-families`
- `POST /products`
- `POST /attribute-schemas`
- `POST /product-attributes`
- `POST /product-media`
- `POST /product-locale-content`
- `POST /product-prices`
- `POST /product-compliance-claims`
- `POST /catalog-publications`
- `POST /product-catalog/events/inbox`
- `GET /product-catalog/workbench`
- `GET /product-catalog/schema-contract`
- `GET /product-catalog/service-contract`
- `GET /product-catalog/release-evidence`

Every route descriptor must carry:

- command or query binding
- owned-table evidence
- emitted or consumed event evidence where applicable
- RBAC permission
- idempotency-key strategy

The API contract must also declare:

- `event_contract: AppGen-X`
- `required_event_topic: appgen.product.events`
- `database_backends: ("postgresql", "mysql", "mariadb")`
- package-local emitted and consumed event descriptors
- runtime table names
- dependency evidence with `shared_tables: ()`
- `shared_table_access: false`
- hidden stream-picker evidence

## Event Contract

### Emitted AppGen-X events

- `ProductClassified`
- `ProductRegistered`
- `AttributeSchemaDefined`
- `ProductEnriched`
- `ProductMediaAttached`
- `ProductPriceReady`
- `ProductComplianceClaimed`
- `ProductPublished`

### Consumed AppGen-X events

- `TaxCalculated`
- `MediaAssetApproved`
- `InventoryPositionUpdated`
- `PricePromotionApproved`
- `SearchIndexRequested`

`receive_event` must be idempotent by explicit `idempotency_key` or the derived
`event_type:event_id` key. It must:

- record inbox evidence on every attempt
- project package-local read evidence only
- avoid duplicate mutation after successful processing
- record retry evidence for unsupported or simulated-failure events
- dead-letter exhausted failures to
  `product_catalog_pim_dead_letter_event`

Outbox evidence must use `product_catalog_pim_appgen_outbox_event` and keep the
AppGen-X contract marker implicit through the package-local API/service/schema
contracts.

## Permissions Contract

The package must declare permissions such as:

- `product_catalog_pim.read`
- `product_catalog_pim.product`
- `product_catalog_pim.enrich`
- `product_catalog_pim.publish`
- `product_catalog_pim.configure`
- `product_catalog_pim.event`
- `product_catalog_pim.audit`

Action-level RBAC must cover:

- configuration, rule, parameter, and schema-extension actions
- product/family/schema/enrichment/publication actions
- `receive_event`
- `build_api_contract`
- `build_schema_contract`
- `build_service_contract`
- `build_release_evidence`
- workbench, render, audit, and boundary actions

## UI And Workbench Binding Evidence

`product_catalog_pim_ui_contract()` and `product_catalog_pim_render_workbench()`
must prove:

- workbench routes for products, families, variants, taxonomy, categories,
  enrichment, localization, media, compliance, lifecycle, assortments,
  publication, syndication, data quality, analytics, rules, parameters, and
  configuration
- fragments for master-data, taxonomy/category, lifecycle/approvals,
  assortments, publication, syndication, data quality, semantic/analytics, and
  governance views
- configuration/rule/parameter fragments bound to owned tables and runtime
  evidence
- outbox, inbox, and dead-letter table names visible to the workbench binding
  contract
- action-level RBAC evidence for visible and locked actions
- `event_contract: AppGen-X`
- `shared_table_access: false`

`product_catalog_pim_build_workbench_view()` must expose tenant-scoped counts,
configuration/rule/parameter evidence, inbox/outbox/dead-letter counts, and
binding evidence.

## Boundary Proof

`product_catalog_pim_verify_owned_table_boundary()` may allow only:

- package-owned tables
- package-emitted and consumed AppGen-X event types
- package runtime tables
- declared API and projection dependencies

It must reject foreign-table references and keep `shared_tables: ()`.

## Release Evidence

`product_catalog_pim_build_release_evidence()` must assemble package-local
evidence for:

- owned schema depth
- one migration descriptor per owned table
- runtime table declaration
- service contract depth
- AppGen-X API contract correctness
- permissions coverage for schema/service/release evidence routes
- UI/workbench binding evidence
- idempotent inbox/outbox/dead-letter evidence
- boundary proof
- backend allowlist proof
- runtime smoke proof

The package-local release contract must remain side-effect free.

## Verification Expectations

Focused verification for this package must prove:

- standard and advanced catalog/PIM workflows execute
- schema/service/release contracts are built package-locally
- rules, parameters, configuration, UI, and workbench bindings remain correct
- schema extensions are limited to owned tables
- API descriptors declare AppGen-X, runtime tables, and no shared-table access
- `receive_event` stays idempotent and produces inbox/retry/dead-letter evidence
- boundary verification rejects foreign references

## Completion Criteria For This Slice

`product_catalog_pim` is complete for this slice only when:

- `implementation_contract()` exposes `schema_contract`,
  `service_contract`, and `release_evidence_contract`
- the schema contract declares comprehensive owned metadata for standard PIM
  table-stakes and advanced governance/analytics structures
- the service contract, API contract, permissions contract, and UI/workbench
  evidence all agree on the fixed AppGen-X topic and hidden stream-picker
  behavior
- focused runtime tests cover the package-local contract builders and runtime
  evidence
- package-local `py_compile` and focused `pytest` succeed

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `product_catalog_pim`
- Mesh: `cx`
- Datastore backend: `None`

### Owned Tables

- `product`
- `product_price`
- `product_media`
- `product_attribute`

### API Routes

- `POST /products`
- `GET /product-read-models`
- `POST /prices`

### Emitted Events

- `ProductClassified`
- `ProductPublished`
- `ForecastUpdated`

### Consumed Events

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
