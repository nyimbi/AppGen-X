# Asset Lifecycle PBC Specification

## Purpose

`asset_lifecycle` owns fixed asset operations from acquisition intent through
capitalization, componentization, book assignment, placed-in-service control,
depreciation, transfer, revaluation, impairment, maintenance-life adjustment,
insurance, warranty, physical verification, retirement, disposal proceeds,
audit proof, federation, identity evidence, controls, rules, parameters,
configuration, workbench fragments, and release evidence.

External finance, procurement, maintenance, insurance, tax, identity, and
ledger interactions are represented only by declared APIs, AppGen-X events,
and projections. The PBC never reaches into another PBC table.

## Owned Datastore Boundary

The runtime owns these tables, with generated model and migration evidence for
each table:

- `fixed_asset`: asset identity, tenant, legal entity, description, category,
  cost, book value, residual value, status, location, custodian, cost center,
  book, useful life, service date, and identity proof.
- `asset_component`: parent asset components and capitalization split.
- `asset_component_history`: component lifecycle events and evidence hashes.
- `asset_book`: depreciation book, currency, calendar, purpose, and method.
- `asset_book_assignment`: asset-to-book assignment and state.
- `asset_acquisition`: acquisition receipt, amount, and capitalization state.
- `asset_capitalization`: capitalization threshold, approval, and timestamp.
- `asset_lease_right_of_use`: right-of-use asset liability and lease terms.
- `asset_depreciation_schedule`: schedule header, method, book, version, and
  status.
- `asset_depreciation_schedule_line`: period depreciation amount and book
  value.
- `asset_depreciation_run`: run header, period, book, status, and idempotency.
- `asset_depreciation_journal`: run journal line, asset, period, amount, and
  posting route.
- `asset_transfer`: location, cost center, custodian, entity, approval, and
  effective date.
- `asset_valuation_adjustment`: revaluation, impairment, reversal, amount, and
  proof hash.
- `asset_impairment_indicator`: market indicator, recommendation, and
  observation time.
- `asset_maintenance_adjustment`: maintenance evidence and useful-life delta.
- `asset_insurance_warranty`: policy, coverage, warranty term, and exception
  state.
- `asset_claim`: insurance claim amount, policy, and status.
- `asset_retirement`: retirement method, proceeds, gain or loss, approval, and
  audit evidence.
- `asset_disposal_proceeds`: proceeds amount, currency, and receipt time.
- `asset_physical_verification`: scan evidence, location, result, and control
  state.
- `asset_physical_verification_exception`: verification exception and
  resolution state.
- `asset_location_assignment`: location history.
- `asset_custodian_assignment`: custodian history.
- `asset_cost_center_assignment`: cost-center history.
- `asset_policy_screening`: policy decision and evidence hash.
- `asset_audit_proof`: disclosure-minimized audit proof and public claims.
- `asset_cross_system_federation`: external projection hash and target system.
- `asset_identity_credential`: decentralized asset identity credential.
- `asset_carbon_utilization`: carbon-aware utilization window evidence.
- `asset_portfolio_optimization`: portfolio candidates and selected asset.
- `asset_allocation_mechanism`: shared asset allocation and clearing bid.
- `asset_anomaly_signal`: information-shift anomaly signal.
- `asset_risk_model`: asset risk score, model version, and explanations.
- `asset_seed_data`: category, book, method, and useful-life seed records.
- `asset_schema_extension`: owned table extension metadata.
- `asset_control_assertion`: continuous control result and evidence hash.
- `asset_governed_model`: regulated model lineage, drift, and governance.
- `asset_rule`: executable rule, scope, status, predicate, and compiled hash.
- `asset_parameter`: bounded runtime parameter and compiled hash.
- `asset_configuration`: database backend, AppGen-X topic, retry limit, and
  default book.
- `asset_lifecycle_appgen_outbox_event`: emitted AppGen-X event evidence.
- `asset_lifecycle_appgen_inbox_event`: consumed AppGen-X event evidence.
- `asset_lifecycle_dead_letter_event`: failed event and retry evidence.

Supported ordinary backends are PostgreSQL, MySQL, and MariaDB. Runtime
configuration rejects unsupported backends.

## Standard Capabilities

The PBC implements fixed asset master data, register search, acquisition
capture, purchase receipt capitalization, capitalization thresholds, component
assets, component history, book assignment, placed-in-service workflow,
depreciation methods, depreciation schedules, schedule lines, depreciation
runs, depreciation journals, asset transfers, location/custodian/cost-center
assignment, revaluation, impairment, impairment indicators, maintenance-driven
useful-life adjustment, insurance, warranty, insurance claims, lease
right-of-use assets, physical verification, verification exceptions, retirement,
disposal proceeds, disposal gain/loss calculation, approval controls, audit
trail, rule administration, parameter administration, configuration
administration, package metadata, UI/workbench rendering, idempotent handlers,
retry/dead-letter evidence, and release gates.

## Advanced Capabilities

The runtime proves event-sourced lifecycle history with hash chaining,
graph-relational component topology, multi-tenant book isolation, owned schema
extensions, probabilistic useful-life estimation, real-time valuation
projection, counterfactual repair/replace/retain optimization, temporal
value-at-risk forecasting, autonomous impairment recommendation, semantic
capitalization parsing, predictive maintenance-linked risk scoring,
self-healing depreciation journal routing, disclosure-minimized asset audit
proofs, immutable regulatory trail controls, dynamic policy screening,
continuous controls, universal API and AppGen-X events, cross-system federation
projections, insurance and warranty integration, decentralized asset identity,
resilience drills, crypto epoch rotation, carbon-aware utilization scheduling,
portfolio optimization, mechanism-design shared allocation,
information-theoretic anomaly detection, stochastic valuation evidence,
regulated model governance, and formal invariant checks.

## Rules, Parameters, and Configuration

Rules are executable dictionaries with `rule_id`, `tenant`, `scope`, and
`status`. Supported scopes include capitalization, depreciation, transfer,
valuation, impairment, maintenance adjustment, insurance/warranty,
verification, retirement, and release gates.

Parameters are constrained to known asset lifecycle knobs:
`capitalization_threshold`, `impairment_indicator_threshold`,
`physical_verification_interval_days`, `depreciation_batch_size`,
`retirement_approval_limit`, and `workbench_limit`.

Configuration requires an allowed database backend, the fixed AppGen-X event
topic `appgen.asset.events`, retry limit, default currency, default timezone,
default book, and workbench limit. User-facing stream-engine selection and
alternate event transport fields are rejected.

Schema extensions are accepted only for Asset-owned tables. Foreign table
extension attempts fail boundary validation.

## APIs

- `POST /assets`
- `POST /assets/{asset_id}/service`
- `POST /assets/{asset_id}/depreciation-schedules`
- `POST /depreciation-runs`
- `POST /assets/{asset_id}/transfers`
- `POST /assets/{asset_id}/revaluations`
- `POST /assets/{asset_id}/impairments`
- `POST /assets/{asset_id}/maintenance-adjustments`
- `POST /assets/{asset_id}/retirements`
- `POST /assets/events/inbox`
- `GET /assets`
- `GET /assets/{asset_id}/risk`

Declared external dependencies are APIs and projections only:

- `POST /ledger/journals`
- `GET /procurement/receipts`
- `GET /maintenance/work-orders`
- `GET /insurance/policies`
- `GET /tax/books`
- `purchase_receipt_projection`
- `maintenance_completion_projection`
- `insurance_policy_projection`
- `tax_book_projection`
- `access_policy_projection`

## Events and Handlers

Emitted AppGen-X events:

- `AssetRegistered`
- `AssetPlacedInService`
- `DepreciationCalculated`
- `AssetTransferred`
- `AssetRevalued`
- `AssetImpaired`
- `MaintenanceAdjustedAssetLife`
- `AssetRetired`

Consumed AppGen-X events:

- `PurchaseReceiptCapitalized`
- `MaintenanceCompleted`
- `InsurancePolicyChanged`
- `TaxBookChanged`
- `AccessPolicyChanged`

Handlers are idempotent by event id, record inbox evidence, update owned
projections, retry failures according to configuration, and write terminal
failures to `asset_lifecycle_dead_letter_event`.

## UI, Permissions, and Workbench

The UI contract exposes the asset lifecycle workbench, register console,
capitalization queue, service board, component view, book assignment panel,
depreciation schedule view, depreciation run console, transfer board,
revaluation and impairment panel, maintenance adjustment view, insurance and
warranty panel, claims panel, physical verification console, retirement
console, disposal proceeds view, policy screening panel, risk panel, rule
studio, parameter console, schema-extension panel, configuration panel,
inbox/outbox monitor, dead-letter triage, and release evidence panel.

The permissions contract maps actions to AppGen-X permissions such as
`asset_lifecycle.register`, `asset_lifecycle.depreciation`,
`asset_lifecycle.valuation`, `asset_lifecycle.retirement`,
`asset_lifecycle.event`, `asset_lifecycle.audit`, and
`asset_lifecycle.configure`.

## Package Metadata and Release Evidence

The package key is `asset_lifecycle`. Package metadata advertises the
implementation directory, standard features, advanced capabilities, owned
tables, database allowlist, fixed event topic, emitted events, consumed events,
UI fragments, API contract, schema contract, service contract, permissions,
and release evidence.

Release readiness requires:

- `asset_lifecycle_runtime_smoke()` returns `ok`.
- `implementation_contract()` includes runtime, UI, API, schema, service,
  permissions, topic, events, and release evidence contracts.
- `asset_lifecycle_build_schema_contract()` proves all owned tables, models,
  relationships, migrations, backend allowlist, and no shared table access.
- `asset_lifecycle_build_service_contract()` proves command and query services,
  transaction boundary, owned mutations, and declared dependencies.
- `asset_lifecycle_build_release_evidence()` proves schema depth, migration
  coverage, service depth, AppGen-X API/event contract, permission coverage,
  backend allowlist, and shared-table isolation.
- Focused Asset Lifecycle tests pass.
- The global PBC release audit, implementation release audit, implemented
  capability audit, and generation smoke audit pass for the implemented PBC
  set.
- Diff scans contain no banned legacy product or framework names.
