# Asset Lifecycle PBC Specification

## Purpose

`asset_lifecycle` owns fixed-asset master data, capitalization, componentization,
depreciation, impairment, revaluation, transfers, maintenance integration,
retirement, disposal, audit evidence, and asset-related journal events. It
integrates with ledger, procurement, maintenance, treasury, tax, and insurance
through APIs, projections, and events only; it never shares tables.

## Standard Table-Stakes Capabilities

- Fixed asset master and asset register.
- Acquisition, capitalization, and placed-in-service workflows.
- Component asset and parent-child asset hierarchy.
- Asset location, custodian, cost center, and legal-entity assignment.
- Book, tax, statutory, and management depreciation books.
- Straight-line, declining-balance, units-of-production, and manual methods.
- Depreciation schedule generation and depreciation run posting.
- Asset transfer between cost centers, locations, legal entities, and books.
- Asset revaluation, impairment, and reversal controls.
- Maintenance and useful-life adjustment evidence.
- Insurance, warranty, and compliance metadata.
- Lease, right-of-use, and financed asset descriptors.
- Asset retirement, sale, scrapping, and disposal gain/loss calculation.
- Journal event emission for capitalization, depreciation, impairment,
  revaluation, transfer, and retirement.
- Physical verification, audit trail, attachments, and source-document links.
- Segregation-of-duties and approval controls.
- Asset workbench views for register, depreciation, risk, exceptions, and close.
- Configuration for books, calendars, useful lives, residual values, and
  thresholds.
- Executable rules, runtime parameters, permission descriptors, seed data, and
  package-local UI fragments for every operator-facing asset flow.

## Advanced Capabilities

- Event-sourced asset lifecycle as the primary persistence model.
- Graph-relational asset topology with parent, component, location, custodian,
  maintenance, and insurance relationships.
- Multi-tenant asset book isolation with independent calendars and policies.
- Schema-evolution resilient asset attributes for regulatory and industry
  extensions.
- Probabilistic useful-life and residual-value estimation.
- Real-time depreciation and valuation projections.
- Counterfactual lifecycle optimization across repair, transfer, replace, sell,
  and scrap scenarios.
- Temporal asset value and risk forecasting.
- Autonomous impairment and revaluation recommendation.
- Semantic source-document parsing for capitalization and componentization.
- Predictive maintenance-linked asset risk scoring.
- Self-healing depreciation-run routing and idempotent journal emission.
- Zero-knowledge asset audit proof over sensitive asset metadata.
- Immutable asset event and regulatory trail.
- Dynamic policy and compliance screening for asset moves and disposals.
- Automated fixed-asset control testing.
- Universal API and async event contract for asset lifecycle actions.
- Cross-system asset federation with maintenance, procurement, and ledger
  projections.
- Insurance and warranty network integration.
- Decentralized asset identity for high-value or regulated assets.
- Chaos-engineered depreciation and journal replay tolerance.
- Crypto-agile asset authorization and evidence signing.
- Carbon-aware asset utilization and retirement scheduling.
- Algebraic asset portfolio optimization.
- Mechanism-design allocation for scarce shared assets.
- Information-theoretic asset anomaly detection.
- Temporal asset valuation stochastic modeling.
- Distributed systems engineering for idempotent asset events.
- Probabilistic ML for asset risk, useful life, and impairment.
- Cryptographic engineering for audit proofs and signatures.
- Mathematical optimization for depreciation, replacement, and disposal.
- Financial MLOps governance for regulated asset models.

## Owned Runtime Boundary

All executable source for this PBC lives in this directory. Runtime state,
standard feature coverage, advanced capability smoke evidence, and package
registration metadata are owned by `asset_lifecycle`.

## Owned Datastore Boundary

The PBC owns:

- `asset_lifecycle_asset`: fixed-asset master, acquisition metadata, category,
  cost, residual value, book, useful life, currency, legal entity, status,
  identity, and source evidence.
- `asset_lifecycle_component`: component hierarchy, parent-child relationships,
  capitalization split, useful-life overrides, and replacement evidence.
- `asset_lifecycle_assignment`: location, custodian, cost center, legal entity,
  book, transfer evidence, approval trail, and effective dates.
- `asset_lifecycle_depreciation_schedule`: book, method, period lines,
  depreciation basis, residual value, and schedule version.
- `asset_lifecycle_depreciation_run`: run header, period, journals,
  idempotency key, posting status, retry evidence, and journal route.
- `asset_lifecycle_valuation_event`: revaluation, impairment, reversal,
  recoverable amount, fair value, market indicator, and approval evidence.
- `asset_lifecycle_retirement`: sale, scrap, disposal proceeds, gain/loss,
  retirement method, and final authorization.
- `asset_lifecycle_outbox`, `asset_lifecycle_inbox`, and
  `asset_lifecycle_dead_letter`: AppGen-X event contract tables for
  exactly-once handlers, retries, and dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, status, and
scope-specific predicates such as capitalization threshold, approval
requirements, depreciation book policy, transfer controls, impairment
indicators, retirement approval limit, physical-verification cadence, and
release-gate constraints.

Parameters include `capitalization_threshold`,
`impairment_indicator_threshold`, `physical_verification_interval_days`,
`depreciation_batch_size`, `retirement_approval_limit`, and `workbench_limit`.

Configuration includes database backend, event topic, retry limit, default
currency, default timezone, default book, and workbench limits. Runtime
configuration rejects unsupported databases and exposes the AppGen-X event
contract as the ordinary eventing surface.

## Public APIs

- `POST /assets`
- `POST /assets/{id}/place-in-service`
- `POST /assets/{id}/depreciation-schedules`
- `POST /assets/depreciation-runs`
- `POST /assets/{id}/transfers`
- `POST /assets/{id}/revaluations`
- `POST /assets/{id}/impairments`
- `POST /assets/{id}/maintenance-adjustments`
- `POST /assets/{id}/retirements`
- `GET /assets/register`
- `GET /assets/{id}/valuation`
- `GET /assets/workbench`

## Events

Emitted events:

- `AssetRegistered`
- `AssetPlacedInService`
- `DepreciationCalculated`
- `AssetTransferred`
- `AssetRevalued`
- `AssetImpaired`
- `MaintenanceAdjustedAssetLife`
- `AssetRetired`

Consumed events:

- `PurchaseReceiptCapitalized`
- `MaintenanceCompleted`
- `InsurancePolicyChanged`
- `TaxBookChanged`
- `LegalEntityChanged`
- `AccessPolicyChanged`

Handlers are idempotent by `asset_lifecycle:{event_type}:{event_id}`, retry at
least three times, and write failures to `asset_lifecycle_dead_letter`.

## UI and Workbench

The UI exposes an asset lifecycle workbench, asset register console,
capitalization queue, placed-in-service board, depreciation schedule view,
depreciation run console, transfer board, revaluation and impairment panel,
maintenance adjustment view, insurance and warranty panel, physical
verification console, retirement console, asset risk panel, asset rule studio,
asset parameter console, and configuration panel. Actions are permission-bound
and rendered from package-owned state.

## Release Evidence

Release readiness requires passing runtime smoke, package-local UI contract,
owned tables, API/event/handler surfaces, AppGen-X event contract evidence,
configuration/rule/parameter execution, generated DSL compatibility, package
metadata, workbench rendering, and focused unit tests.
