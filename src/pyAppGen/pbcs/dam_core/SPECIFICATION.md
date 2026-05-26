# DAM Core PBC

`dam_core` is the AppGen-X Digital Asset Management Core packaged business capability. It owns the media asset lifecycle, rendition pipeline, metadata tags, rights policies, and AppGen-X event contracts needed to compose commerce and content applications without sharing tables across PBC boundaries.

## Owned Boundary

- Owned tables: `asset`, `asset_rendition`, `rights_policy`, `metadata_tag`.
- External dependencies are represented only as API/event projections. `ProductPublished` is consumed into an internal `product_projection`; no product table is shared.
- Allowed database backends are PostgreSQL, MySQL, and MariaDB.
- Eventing is fixed to the AppGen-X contract on `appgen.dam.events`; users are not given stream-engine picker fields.

## Runtime Capabilities

- Register content-addressed media assets with tenant isolation, binary fingerprint evidence, product projection dependency evidence, and immutable lifecycle events.
- Request and complete renditions/transcoding for named profiles with quality scores and retry/dead-letter evidence.
- Attach rights policies, enforce market/use-case decisions, block restricted use, and emit policy evidence.
- Add governed metadata tags with confidence floors and taxonomy validation.
- Configure runtime fields, bounded parameters, and compiled rule evidence for asset governance, rights, rendition, and metadata policies.
- Consume `ProductPublished` idempotently, record duplicate detection, and route invalid or failed messages to the dead-letter evidence queue.
- Produce workbench/UI contracts for assets, renditions, metadata, rights, product projections, rules, parameters, configuration, outbox, inbox, and dead letters.

## Release Evidence

The package exposes:

- `dam_core_runtime_capabilities()`
- `dam_core_runtime_smoke()`
- `dam_core_ui_contract()`
- `dam_core_render_workbench()`
- `implementation_contract()`

The smoke audit executes configuration, parameter/rule setup, schema extension, product event handling, duplicate idempotency, dead-letter handling, asset registration, rights policy enforcement, metadata tagging, rendition completion, control tests, and UI/workbench evidence.
