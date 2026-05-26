# Asset Lifecycle PBC Specification

## Purpose

`asset_lifecycle` is the AppGen-X packaged business capability for fixed asset
operations from acquisition intent through capitalization, componentization,
placed-in-service control, depreciation, transfer, revaluation, impairment,
maintenance-life adjustments, verification, insurance, warranty, retirement,
and disposal evidence. The package is deliberately self-contained: it owns its
schema, models, services, events, handlers, workbench fragments, permissions,
rules, parameters, configuration, tests, and release evidence under this
directory. External finance, procurement, maintenance, insurance, tax, identity,
and ledger interactions are represented only by AppGen-X APIs, events, and
projections; this PBC never reaches into another PBC table.

The package supports the ordinary enterprise asset lifecycle table stakes and
adds advanced runtime surfaces for temporal valuation, probabilistic useful-life
estimation, policy screening, cryptographic evidence, optimization, and
resilience. The implementation is executable in `runtime.py`, renderable through
`ui.py`, exportable through `__init__.py`, and proven by
`tests/test_pbc_asset_lifecycle_runtime.py`.

## Owned Datastore Boundary

The owned tables are:

- `fixed_asset`: asset identity, tenant, legal entity, description, category,
  cost, residual value, currency, book, useful life, status, current book value,
  accumulated depreciation, location, custodian, cost center, service date,
  disposal state, and cryptographic asset identity.
- `asset_component`: parent-child component hierarchy, component names,
  replacement metadata, capitalization split, lifecycle overrides, and topology
  degree evidence.
- `asset_book`: depreciation book definition, default method, calendar, book
  currency, tenant policy, and statutory or management purpose.
- `asset_depreciation_schedule`: generated schedule header, method, book,
  lines, period amounts, residual value guard, and schedule version evidence.
- `asset_depreciation_run`: run header, period, posted journal rows,
  idempotency key, retry status, posting route, and close evidence.
- `asset_transfer`: location, cost center, custodian, legal entity, book move,
  approval, effective date, and policy screening evidence.
- `asset_valuation_adjustment`: revaluation, impairment, reversal, fair value,
  recoverable amount, market indicator, approver, and valuation proof.
- `asset_maintenance_adjustment`: maintenance event linkage, useful-life delta,
  evidence, risk effect, and projection update.
- `asset_insurance_warranty`: policy, coverage, warranty term, insured value,
  carrier projection key, and exception status.
- `asset_retirement`: retirement method, proceeds, gain or loss, final status,
  disposal approval, and audit evidence.
- `asset_physical_verification`: verification campaigns, scanned evidence,
  exception status, location confirmation, and control results.
- `asset_rule`, `asset_parameter`, and `asset_configuration`: executable
  package rules, runtime parameters, and validated configuration.

Runtime event tables are
`asset_lifecycle_appgen_outbox_event`, `asset_lifecycle_appgen_inbox_event`,
and `asset_lifecycle_dead_letter_event`. They are package-owned AppGen-X
contract tables, not user-selectable stream infrastructure. Supported ordinary
backends are exactly PostgreSQL, MySQL, and MariaDB.

## Standard Business Capabilities

The package implements fixed asset master data, register search, acquisition
capture, capitalization thresholds, component assets, placed-in-service
workflow, asset book assignment, depreciation schedule generation, depreciation
run posting, asset transfer, custodian and cost center assignment, revaluation,
impairment, maintenance-driven useful-life adjustment, insurance and warranty
metadata, physical verification, retirement, sale, scrapping, disposal gain/loss
calculation, audit trail, approval controls, rule administration, parameter
administration, configuration administration, package metadata, workbench
rendering, and release-gate evidence.

Standard accounting behavior includes cost, residual value, useful life, book
value, accumulated depreciation, service date, retirement proceeds, gain or
loss, period depreciation journals, valuation adjustments, and immutable event
history. Standard control behavior includes required approval metadata for
transfers, valuation changes, impairments, and retirements; configuration
validation; threshold parameters; rule activation; and permission-bound actions.

## Advanced Capabilities

The runtime includes event-sourced lifecycle history with hash chaining,
graph-relational component topology, multi-tenant book isolation,
schema-on-read extensions for owned tables, probabilistic useful-life
estimation, real-time valuation projections, counterfactual repair/replace/
retain optimization, temporal value-at-risk forecasting, autonomous impairment
recommendation, semantic capitalization parsing, predictive maintenance-linked
risk scoring, self-healing depreciation journal routing, zero-knowledge-style
asset audit proofs, immutable regulatory trail controls, dynamic policy
screening, automated control tests, universal API and event descriptors,
cross-system federation projections, insurance and warranty integration,
decentralized asset identity verification, resilience drills, crypto epoch
rotation, carbon-aware utilization scheduling, portfolio optimization,
mechanism-design shared asset allocation, information-theoretic anomaly
detection, stochastic valuation evidence, regulated model governance, and
formal invariant checks.

These capabilities are implemented as deterministic package-local functions so
the release audit can prove the surfaces without requiring external services.
External systems may later attach to the API and event contracts, but the
package contract does not depend on side effects outside its boundary.

## Rules, Parameters, and Configuration

Rules are executable dictionaries with `rule_id`, `tenant`, `scope`, and
`status`. Scopes include capitalization, depreciation, transfer, valuation,
retirement, verification, and release gate behavior. Scope-specific predicates
may define capitalization thresholds, approval requirements, depreciation book
policy, transfer limits, impairment indicators, physical verification cadence,
retirement approval limits, or release-blocking controls.

Parameters are constrained to known asset lifecycle knobs:
`capitalization_threshold`, `impairment_indicator_threshold`,
`physical_verification_interval_days`, `depreciation_batch_size`,
`retirement_approval_limit`, and `workbench_limit`. Unknown parameters are
rejected, including attempts to smuggle stream selection through parameter
names.

Configuration requires an allowed database backend, the fixed AppGen-X event
topic `appgen.asset.events`, retry limit, default currency, default timezone,
and optionally a default book and workbench limit. Configuration enriches state
with `event_contract: AppGen-X`, the fixed topic, allowed database backends,
owned tables, outbox table, inbox table, dead-letter table, and
`stream_engine_picker_visible: false`. Any user-facing stream-engine picker or
alternate eventing field is rejected.

## APIs, Events, and Handlers

The descriptor API contract exposes command routes for registering assets,
placing assets in service, building depreciation schedules, running
depreciation, transferring assets, revaluing assets, impairing assets,
recording maintenance adjustments, retiring assets, and receiving AppGen-X
events. Query routes expose the register and risk projections. Every route is a
descriptor with a command or query, owned table, and permission. The contract
declares `shared_table_access: false`, the owned tables, runtime tables,
allowed backends, emitted events, consumed events, dependency projections, and a
hidden stream picker.

Emitted events are `AssetRegistered`, `AssetPlacedInService`,
`DepreciationCalculated`, `AssetTransferred`, `AssetRevalued`, `AssetImpaired`,
`MaintenanceAdjustedAssetLife`, and `AssetRetired`.

Consumed events are `PurchaseReceiptCapitalized`, `MaintenanceCompleted`,
`InsurancePolicyChanged`, `TaxBookChanged`, and `AccessPolicyChanged`.
`receive_event` is idempotent by `event_id`, records processed inbox entries,
stores handler evidence, and updates consumed-event projections:
purchase receipts, maintenance completions, insurance policies, tax books, and
access policies. Unsupported or malformed events produce retry evidence and are
dead-lettered after the configured retry limit.

## Permissions and Workbench

The permissions contract maps each action to an AppGen-X permission such as
`asset_lifecycle.register`, `asset_lifecycle.depreciation`,
`asset_lifecycle.valuation`, `asset_lifecycle.retirement`,
`asset_lifecycle.event`, `asset_lifecycle.audit`, and
`asset_lifecycle.configure`. Roles include admin, accountant, operator, and
auditor. ABAC attributes include tenant, legal entity, book, location, cost
center, and asset category.

The UI contract exposes the asset lifecycle workbench, register console,
capitalization queue, service board, depreciation schedule view, depreciation
run console, transfer board, revaluation and impairment panel, maintenance
adjustment view, insurance and warranty panel, physical verification console,
retirement console, risk panel, rule studio, parameter console, and
configuration panel. Workbench render evidence includes visible and locked
actions, configuration binding, rules, parameters, outbox count, inbox count,
dead-letter count, owned tables, event configuration, and RBAC bindings.

## Boundary and Release Evidence

`verify_owned_table_boundary` accepts only package-owned tables, package runtime
tables, declared consumed events, declared dependency projections, declared API
dependencies, and names prefixed with `asset_lifecycle_`. Foreign table names
are reported as violations. This proves cross-PBC dependency representation
through APIs, events, and projections instead of shared tables.

Release evidence requires runtime smoke success, standard feature coverage,
advanced capability coverage, package-local source contract, descriptor API
contract, permissions contract, UI contract, owned table evidence, AppGen-X
configuration, idempotent handler tests, retry/dead-letter tests, boundary
tests, and focused unit tests. The package remains side-effect free: registration
and composition can inspect the package and build plans without mutating
external state.
