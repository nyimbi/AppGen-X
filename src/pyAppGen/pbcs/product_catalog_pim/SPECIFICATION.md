# Enterprise Product Catalog and PIM PBC Specification

## Scope

`product_catalog_pim` owns product information management for AppGen-X
composable applications. It manages product masters, families, variant models,
attribute schemas, taxonomy, localized content, enrichment workflow, compliance
claims, digital media references, sellability, publication, catalog read models,
price-list handoff metadata, channel syndication, rules, parameters,
configuration, and workbench UI fragments.

The PBC composes with pricing, commerce, inventory, tax, content, search,
forecasting, order, and customer PBCs through APIs, AppGen-X events, and
read-model projections only. It does not share tables with other PBCs.

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
- `product_outbox`
- `product_inbox`
- `product_dead_letter`

Allowed datastore backends are PostgreSQL, MySQL, and MariaDB. Ordinary eventing
uses the AppGen-X outbox/inbox event contract.

## Standard Capabilities

- Product master registration, family assignment, lifecycle state, ownership,
  uniqueness, and tenant isolation.
- Variant modeling with option axes, parent/child relationships, SKU
  generation, bundle/kit readiness, and sellability constraints.
- Attribute schema governance, typed attribute validation, required attribute
  checks, enrichment completeness, and schema extension control.
- Taxonomy category assignment, merchandising tags, eligibility flags, and
  channel-specific projections.
- Localized names, descriptions, units, dimensions, SEO metadata, compliance
  disclosures, and content approval.
- Media reference registration, role assignment, alt text, rendition metadata,
  rights metadata, and DAM handoff projections.
- Price-list metadata, currency, effective dates, price publication payloads,
  and downstream pricing handoff without owning the pricing engine.
- Compliance claims, restricted-region checks, hazardous or regulated goods
  screening, audit evidence, and release gates.
- Publication workflows, channel syndication, product read models, search
  indexing signals, forecast events, idempotent handlers, retry/dead-letter
  evidence, permissions, seed data, runtime configuration, rules, parameters,
  and UI workbench fragments.

## Advanced Capabilities

- Event-sourced product lifecycle with immutable hash-chained history.
- Graph-relational product topology spanning families, variants, attributes,
  media, channels, locales, prices, compliance, and taxonomy.
- Multi-tenant product isolation with independently configurable rules and
  parameters.
- Schema evolution through governed attribute and extension registration.
- Probabilistic content-quality, sellability, compliance, and demand readiness
  scoring.
- Real-time catalog analytics over completeness, publishability, channel
  readiness, and enrichment backlog.
- Counterfactual publication simulation for channel, locale, attribute, and
  compliance changes.
- Temporal content and sellability risk forecasting.
- Autonomous enrichment exception recommendation with auditable rationale.
- Semantic product instruction parsing for merchandising and enrichment text.
- Predictive product readiness risk scoring and self-healing publication route
  selection.
- Cryptographic catalog publication proofs, immutable audit trails, dynamic
  policy screening, and continuous control testing.
- Universal API and AppGen-X event contracts, federation views, decentralized
  product identity, resilience drills, crypto agility, carbon-aware publication,
  mathematical catalog optimization, channel allocation, anomaly detection,
  stochastic sellability modeling, and governed product intelligence models.

## APIs

- `POST /products`
- `POST /product-families`
- `POST /product-variants`
- `POST /attribute-schemas`
- `POST /product-attributes`
- `POST /product-media`
- `POST /product-locale-content`
- `POST /product-prices`
- `POST /product-compliance-claims`
- `POST /catalog-publications`
- `GET /product-read-models`
- `POST /product-rules`
- `POST /product-parameters`
- `POST /product-configuration`

## Events

Emitted:

- `ProductClassified`
- `ProductEnriched`
- `ProductPublished`
- `ProductPriceReady`
- `ForecastUpdated`

Consumed:

- `TaxCalculated`
- `MediaAssetApproved`
- `InventoryPositionUpdated`
- `PricePromotionApproved`
- `SearchIndexRequested`

Handlers are idempotent through `product_catalog_pim:<EventType>:<event_id>`
keys, retry through the AppGen-X outbox adapter, and route exhausted failures to
`product_catalog_pim.dead_letter`.

## UI

The package exports a workbench UI contract with fragments for product master
data, family and variant modeling, attribute schemas, enrichment, localization,
media, compliance, publication, channel projections, rules, parameters, and
configuration.
