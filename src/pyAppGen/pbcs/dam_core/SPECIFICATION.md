# DAM Core PBC

`dam_core` is the AppGen-X Digital Asset Management packaged business capability
for media asset lifecycle, rendition generation, rights enforcement, metadata
governance, asset quality, and commerce/content projection integration. It owns
its schema, service layer, events, handlers, UI workbench, configuration,
parameters, rules, package metadata, tests, and release evidence.

## Stable Identity

- PBC key: `dam_core`.
- Mesh: `content`.
- Package directory: `src/pyAppGen/pbcs/dam_core`.
- Runtime entrypoint: `dam_core_runtime_capabilities()`.
- UI entrypoint: `dam_core_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Default datastore: `dam_core_store`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: AppGen-X event contract on `appgen.dam.events`.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

The PBC owns exactly these tables:

- `asset`: tenant-scoped asset identity, product projection key, file metadata,
  MIME type, size, locale, storage URI, content fingerprint, lifecycle state,
  rights policy reference, rendition references, metadata index, and audit hash.
- `asset_rendition`: rendition request and completion state, profile, target
  MIME type, dimensions, output URI, quality score, duration, retry evidence,
  and audit hash.
- `rights_policy`: license type, allowed markets, blocked markets, expiration,
  attribution requirement, approver, status, policy hash, and enforcement
  evidence.
- `metadata_tag`: asset-bound taxonomy, value, confidence, source, tenant,
  compiled evidence, and governance proof.

No product, commerce, search, or content tables are shared. `ProductPublished`
is consumed into an internal product projection and is represented as the
declared dependency `enterprise_pim.ProductPublished`. The owned-boundary
verifier accepts owned tables, DAM-local event tables, `product_projection`,
catalog DAM APIs, and that declared event dependency; it rejects direct foreign
references such as `product`.

## Standard Table-Stakes Capabilities

The implementation covers the operational surface expected from a production
digital asset management package:

- Asset registration with tenant, product projection, filename, MIME type, size,
  storage URI, binary fingerprint, locale, creator, status, and audit evidence.
- Duplicate and binary fingerprint evidence through content hashes.
- Product projection consumption from `ProductPublished` with idempotent
  handler records.
- Runtime configuration for database backend, event topic, retry limit,
  storage tier, allowed MIME types, rendition profiles, default rights
  decision, metadata taxonomies, locale, and workbench limit.
- Parameter engine for max asset size, quality threshold, rights risk,
  transcode retries, duplicate similarity, rendition cost, carbon cost, usage
  forecast horizon, metadata confidence floor, and workbench limit.
- Rule engine for tenant, governance scope, MIME policy, rights policy,
  rendition policy, metadata policy, status, compiled hash, and policy-engine
  evidence.
- Schema extension for owned tables only.
- Rights policy attachment, rights enforcement, market blocking, use-case
  decisions, and policy evidence.
- Metadata tagging with taxonomy validation and confidence-floor enforcement.
- Rendition request and completion for declared profiles, output URI, quality
  score, duration, status, and AppGen-X outbox events.
- Workbench views for asset counts, ready renditions, rights policies,
  metadata tags, product projections, outbox, dead letters, configuration,
  rules, and parameters.
- API contract descriptors for asset registration, rendition requests, rights
  policies, metadata tags, inbox handling, and workbench queries.
- Permission mapping for asset write, rendition write, rights management,
  rights evaluation, metadata write, event consumption, configuration, and
  audit actions.
- Retry/dead-letter evidence for handler failure.
- Seed evidence for storage tiers, rendition profiles, metadata taxonomies, and
  rights decisions.

## Advanced Capabilities

The runtime exposes evidence for:

- Content-addressed asset lifecycle with immutable event hashes.
- Owned media schema boundary and explicit foreign-table rejection.
- Multi-tenant media isolation.
- Schema-evolution-safe asset, rendition, rights, and metadata extensions.
- Product projection federation through AppGen-X events only.
- Probabilistic asset quality scoring.
- Counterfactual rendition cost and carbon route simulation.
- Temporal asset usage forecasting.
- Autonomous asset exception resolution for missing rights, low quality,
  missing metadata, and failed transcodes.
- Semantic asset instruction parsing for render, tag, and rights actions.
- Predictive governance risk scoring.
- Self-healing transcode route selection and failover.
- Cryptographic asset proof generation with selective disclosure.
- Immutable asset audit trail and hash-chain control tests.
- Dynamic rights and MIME policy screening.
- Automated DAM control testing for hash chain, tenant isolation, rights
  coverage, rendition coverage, and configuration validity.
- Cross-system product, commerce, search, and content federation through
  declared APIs/events.
- AppGen-X outbox/inbox eventing with idempotent handlers.
- Retry and dead-letter evidence.
- Carbon-aware rendition route optimization parameters.
- Governed metadata and model evidence through confidence thresholds and
  compiled rules.

## Commands And Services

The service layer exposes these package-local commands:

- `configure_runtime(configuration)`.
- `set_parameter(name, value)`.
- `register_rule(rule)`.
- `register_schema_extension(table, fields)`.
- `receive_event(envelope, simulate_failure=False)`.
- `register_asset(asset)`.
- `attach_rights_policy(policy)`.
- `add_metadata_tag(tag)`.
- `request_rendition(rendition)`.
- `complete_rendition(rendition_id, result)`.
- `enforce_rights(asset_id, market=..., use_case=...)`.
- `build_api_contract()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references=...)`.

All commands operate on package-local state and return deterministic,
side-effect-free transition payloads suitable for generated apps and release
smoke tests.

## APIs

The package-local API contract exposes:

- `POST /dam/assets` for `register_asset`, writing `asset`, requiring
  `dam_core.asset.write`, and emitting `AssetRegistered`.
- `POST /dam/assets/{asset_id}/renditions` for `request_rendition`, writing
  `asset_rendition`, requiring `dam_core.rendition.write`, and emitting
  `AssetRenditionRequested`.
- `POST /dam/assets/{asset_id}/rights` for `attach_rights_policy`, writing
  `rights_policy`, requiring `dam_core.rights.manage`, and emitting
  `AssetRightsPolicyAttached`.
- `POST /dam/assets/{asset_id}/tags` for `add_metadata_tag`, writing
  `metadata_tag`, requiring `dam_core.metadata.write`, and emitting
  `AssetMetadataTagged`.
- `POST /dam/events/inbox` for `receive_event`, consuming AppGen-X events and
  requiring `dam_core.event.consume`.
- `GET /dam/workbench` for `build_workbench_view`, reading owned DAM state and
  requiring `dam_core.audit`.

The catalog route set remains `POST /assets`, `POST /renditions`, and
`GET /assets`; the package-local API contract includes additional internal
routes needed to fully exercise the runtime.

## Events And Handlers

Consumed events:

- `ProductPublished`, provided by the product/content domain and stored only as
  a DAM product projection.

Emitted events include:

- `AssetRegistered`.
- `AssetRenditionRequested`.
- `AssetRenditionReady`.
- `AssetRightsPolicyAttached`.
- `AssetMetadataTagged`.

Handlers require event IDs and AppGen-X envelopes, deduplicate already handled
messages, write inbox records, maintain dead-letter evidence on simulated
failure, and never expose stream-engine selection.

## UI And Workbench

The workbench exposes:

- Asset registry.
- Rendition pipeline.
- Metadata tag board.
- Rights policy panel.
- Product projection panel.
- Quality and control-test panels.
- Rule studio.
- Parameter console.
- Configuration panel.
- Event outbox.
- Inbox and dead-letter review.

Rendering uses action permissions to calculate visible and locked commands. The
configuration panel exposes only PostgreSQL, MySQL, and MariaDB plus the fixed
AppGen-X event contract.

## Release Evidence

Focused tests prove:

- Runtime capabilities and smoke checks pass.
- Configuration, parameters, rules, schema extensions, event consumption, asset
  registration, rights policy attachment, metadata tagging, rendition request
  and completion, rights enforcement, API contract, workbench rendering, and UI
  contract execute.
- Product dependencies are projections, not shared product tables.
- Boundary validation accepts owned tables and declared dependencies and
  rejects foreign table references.
- Invalid database backends, invalid parameters, non-owned schema extensions,
  and simulated handler failures are rejected or dead-lettered.
- The package participates in all-PBC implementation release and generation
  smoke audits.
