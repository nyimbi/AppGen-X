# Price Promotion Engine PBC

`price_promotion_engine` is the AppGen-X packaged business capability for
standard pricing, promotion governance, quote optimization, margin control, and
release-evidence generation. The package is self-contained under
`src/pyAppGen/pbcs/price_promotion_engine` and exposes executable runtime,
schema, service, API, permission, UI, and release contracts through
package-local functions and `implementation_contract()`.

## Stable Identity

- PBC key: `price_promotion_engine`
- Mesh: commerce
- Package directory: `src/pyAppGen/pbcs/price_promotion_engine`
- Runtime entrypoint: `price_promotion_engine_runtime_capabilities()`
- UI entrypoint: `price_promotion_engine_ui_contract()`
- Source registration entrypoint: `implementation_contract()`
- Allowed database backends: PostgreSQL, MySQL, MariaDB
- Event contract: fixed `AppGen-X`
- Required event topic: `appgen.price_promotion.events`
- User stream-engine choice: forbidden and hidden

## Package-Local Builders

The package exposes the hardened complete-PBC builder surface:

- `price_promotion_engine_build_schema_contract()`
- `price_promotion_engine_build_service_contract()`
- `price_promotion_engine_build_release_evidence()`
- `price_promotion_engine_build_api_contract()`
- `price_promotion_engine_permissions_contract()`
- `price_promotion_engine_binding_evidence()`

`implementation_contract()` includes:

- `advanced_runtime`
- `ui_contract`
- `api_contract`
- `schema_contract`
- `service_contract`
- `release_evidence_contract`
- `permissions_contract`
- `owned_tables`
- `runtime_tables`
- `required_event_topic`
- `event_contract`
- `consumes`
- `emits`

## Owned Datastore Boundary

The package owns these business tables:

- `price_configuration`
- `price_parameter`
- `price_policy_rule`
- `price_schema_extension`
- `price_list`
- `price_book`
- `price_book_entry`
- `price_rule`
- `customer_price`
- `channel_price`
- `currency_price`
- `promotion`
- `promotion_rule`
- `coupon`
- `promotion_eligibility`
- `promotion_stacking_policy`
- `promotion_exclusion`
- `campaign_budget`
- `promotion_approval`
- `loyalty_tier`
- `price_simulation`
- `price_margin_guardrail`
- `price_decision`
- `price_audit_trace`
- `price_performance_telemetry`

The package also owns these AppGen-X runtime tables:

- `price_promotion_engine_appgen_outbox_event`
- `price_promotion_engine_appgen_inbox_event`
- `price_promotion_engine_dead_letter_event`

No shared tables are accessed. External context is allowed only through
declared APIs, projections, and consumed AppGen-X events:

- APIs:
  `POST /customer-segment-projections/resolve`,
  `POST /forecast-projections/resolve`,
  `POST /checkout-projections/price-context`,
  `GET /currency-rate-projections/{currency}`
- Projections:
  `customer_segment_projection`,
  `forecast_projection`,
  `checkout_projection`,
  `currency_rate_projection`
- Consumed events:
  `CustomerSegmentUpdated`,
  `ForecastUpdated`

`price_promotion_engine_verify_owned_table_boundary()` accepts only owned
tables, runtime tables, declared events, and declared dependencies. Foreign
references such as `customer_segment` are rejected.

## Standard Table-Stakes Coverage

The complete package covers:

- price lists, price books, and price-book entries
- customer-, channel-, and currency-specific price records
- governed pricing rules with margin, stacking, exclusion, approval, and budget
  policy evidence
- promotion rules, coupons, eligibility, stacking, exclusions, budgets, and
  approvals
- loyalty-tier pricing
- quote decisions with counterfactual simulations
- margin guardrails and review routing
- audit traces and performance telemetry
- package-local configuration, parameter, and schema-extension support
- AppGen-X outbox, inbox, idempotency, retry, and dead-letter evidence
- workbench/UI binding evidence for pricing, promotion, approval, simulation,
  telemetry, and governance surfaces

## Runtime Behavior

`price_promotion_engine_runtime_capabilities()` reports:

- the full owned-table and runtime-table boundary
- fixed AppGen-X topic and contract metadata
- emitted and consumed event types
- standard pricing/promotion features
- advanced optimization and governance capability keys
- executable smoke evidence from `price_promotion_engine_runtime_smoke()`

The runtime supports these commands:

- `configure_runtime(configuration)`
- `set_parameter(name, value)`
- `register_rule(rule)`
- `register_schema_extension(table, fields)`
- `register_price_rule(command)`
- `register_promotion(command)`
- `register_loyalty_tier(command)`
- `receive_event(event, simulate_failure=False)`
- `quote_price(command)`
- `apply_promotion(decision_id, promotion_id)`

Quote generation performs:

- tenant-aware rule selection
- customer/channel/currency price resolution
- volume-break evaluation
- promotion eligibility checks
- stacking and exclusion enforcement
- budget and approval gating
- loyalty-tier discounting
- forecast adjustment
- margin/risk scoring
- decision, simulation, guardrail, audit-trace, telemetry, and outbox evidence

Promotion application performs:

- eligibility verification against the stored decision
- applied-promotion persistence on the owned decision
- campaign-budget consumption updates
- audit and telemetry evidence
- `PromotionApplied` outbox emission

## Schema Contract Expectations

`price_promotion_engine_build_schema_contract()` returns:

- one generated table descriptor per owned table
- one generated migration descriptor per owned table
- one generated model descriptor per owned table
- runtime-table descriptors for outbox, inbox, and dead-letter evidence
- explicit relationships between price books, price rules, promotions,
  approvals, budgets, decisions, simulations, guardrails, audit traces, and
  telemetry
- backend allowlist evidence
- fixed AppGen-X eventing evidence
- declared dependency evidence with `shared_tables: ()`

## Service Contract Expectations

`price_promotion_engine_build_service_contract()` declares:

- command methods for pricing, promotion, configuration, event handling, and
  boundary verification
- query methods for workbench binding, API/schema/service/release evidence, and
  permissions
- transaction boundary:
  `price_promotion_engine_owned_datastore_plus_appgen_outbox`
- mutation scope limited to owned and runtime tables
- idempotent handler evidence for `receive_event`
- retry/dead-letter table evidence tied to `price_configuration.retry_limit`
- fixed AppGen-X eventing with no stream-engine picker or user eventing choice

## API Contract Expectations

`price_promotion_engine_build_api_contract()` exposes descriptors for:

- `PUT /price-promotion/configuration`
- `POST /price-promotion/rules`
- `POST /price-promotion/parameters`
- `POST /price-promotion/schema-extensions`
- `POST /price-rules`
- `POST /promotions`
- `POST /loyalty-tiers`
- `POST /price-quotes`
- `POST /promotion-applications`
- `POST /price-promotion/events/inbox`
- `GET /price-promotion/workbench`
- `GET /price-promotion/schema-contract`
- `GET /price-promotion/service-contract`
- `GET /price-promotion/release-evidence`

The API contract must also include:

- emitted and consumed event descriptors
- required event topic and AppGen-X contract
- runtime table evidence for outbox/inbox/dead-letter processing
- database backend allowlist
- permission list
- dependency evidence with `shared_table_access: False`

## Permissions

`price_promotion_engine_permissions_contract()` governs:

- `price_promotion_engine.price.write`
- `price_promotion_engine.promotion.write`
- `price_promotion_engine.quote`
- `price_promotion_engine.event.consume`
- `price_promotion_engine.configure`
- `price_promotion_engine.audit`

Release/audit permissions must cover:

- `build_api_contract`
- `build_schema_contract`
- `build_service_contract`
- `build_release_evidence`
- `build_workbench_view`
- `render_workbench`
- `verify_owned_table_boundary`

## UI And Workbench

The UI contract includes fragments for:

- price list/book management
- price rules
- promotions and coupons
- campaign budgets and approvals
- quote simulations
- margin guardrails
- forecast and segment inputs
- decision ledger and telemetry
- governance/configuration/parameters
- AppGen-X outbox and dead-letter visibility

The rendered workbench must prove:

- tenant-filtered counts for price books, promotions, approvals, simulations,
  decisions, telemetry, outbox, and dead letters
- configuration/rule/parameter binding
- event contract and runtime-table binding evidence
- permission-based visible and locked actions

## Release Evidence

`price_promotion_engine_build_release_evidence()` combines:

- schema contract
- service contract
- API contract
- permissions contract
- UI contract
- rendered workbench evidence
- boundary verification
- runtime smoke evidence

Release checks must prove:

- owned schema depth equals the owned-table list
- migration descriptors exist for every owned table
- runtime tables are declared exactly
- service queries include `build_release_evidence`
- API event contract and topic remain fixed
- permissions cover release queries
- UI/workbench bindings include AppGen-X event evidence
- inbox/outbox/dead-letter idempotency evidence exists
- standard table-stakes counts exist for books, coupons, budgets, approvals,
  simulations, and telemetry
- database backends remain limited to PostgreSQL, MySQL, and MariaDB

## Validation

Focused validation for this completeness slice is expected to include:

- `py_compile` over the package-local files and focused test file
- focused `pytest` for `tests/test_pbc_price_promotion_engine_runtime.py`
- assertions that `implementation_contract()` now exposes schema, service, and
  release evidence contracts through the package-local registration surface

## Seed And Release Evidence

Release evidence includes package-local seed data for price books, discount
families, promotion states, eligibility reason codes, guardrail bands, and
approval queues. The package validates those seeds with schema, migration,
model, service, route, event, handler, UI, RBAC, configuration, and release
contracts.
