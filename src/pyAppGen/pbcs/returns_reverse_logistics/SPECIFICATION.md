# Returns and Reverse Logistics PBC

## Purpose

The Returns and Reverse Logistics PBC owns return authorizations, RMAs, return
eligibility, return labels, carrier handoff, receipt and inspection evidence,
disposition routing, restock/refurbish/scrap routing, credit adjustments,
refund and ledger handoff, fraud and abuse screening, runtime control
evidence, and the returns workbench. It integrates with order, payment,
inventory, ledger, identity, and platform event infrastructure through APIs,
AppGen-X events, and read-only federated projections.

Implementation entrypoint: `implementation_contract()`.

## Owned Datastore Boundary

The PBC owns:

- `return_authorization`: RMA, order/payment/customer references, eligibility,
  fraud score, lifecycle status, and graph topology evidence.
- `return_label`: carrier route selection, label status, handoff state,
  tracking, and carbon-aware route evidence.
- `inspection_grade`: receipt, inspection grade, disposition recommendation,
  recovery estimate, and inspection notes.
- `credit_adjustment`: refund/credit amount, disposition-adjusted recovery,
  refund handoff, ledger handoff, and immutable issuance evidence.
- `returns_reverse_logistics_outbox_event`,
  `returns_reverse_logistics_inbox_event`, and
  `returns_reverse_logistics_dead_letter_event`: AppGen-X event contract tables for
  idempotent handlers, retry evidence, and dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB only.
Schema extensions are accepted only for owned tables and reject non-owned or
invalid field names.

Boundary validation is package-local and executable through
`returns_reverse_logistics_verify_owned_table_boundary(references)`. It accepts
only owned tables plus declared API/event dependencies and rejects shared-table
access.

## Standard Table-Stakes Capabilities

The PBC fully implements return authorizations and RMAs, return eligibility,
return labels, carrier handoff, receipt and inspection, disposition routing,
restock/refurbish/scrap routing, credit adjustments, refund and ledger
handoff, fraud and abuse screening, tenant isolation, idempotent handlers,
AppGen-X outbox/inbox eventing, retry/dead-letter evidence, permissions,
configuration schema, executable rules, bounded runtime parameters, seed-data
surfaces, immutable audit evidence, and package-owned workbench views.

## Advanced Capabilities

The runtime proves event-sourced returns lifecycle, graph-relational reverse
logistics topology, probabilistic return eligibility and fraud scoring,
counterfactual disposition simulation, temporal return-rate and recovery
forecasting, autonomous return exception resolution, semantic return
instruction parsing, predictive return risk, self-healing label and carrier
route selection, cryptographic return proof, immutable return audit trail,
dynamic return policy screening, automated control testing, cross-system
order/payment/inventory/ledger federation, universal API plus asynchronous
streaming, distributed systems evidence, chaos tolerance, crypto agility,
carbon-aware return routing, mathematical recovery optimization, disposition
allocation mechanism design, anomaly detection, stochastic return exposure
modeling, and governed ML model evidence.

## Rules, Parameters, and Configuration

Rules are executable records with required fields `rule_id`, `tenant`, `scope`,
`status`, `eligibility_policy`, `label_policy`, `inspection_policy`, and
`credit_policy`. Runtime compilation produces a deterministic `compiled_hash`
and structured rule evidence. Rules reject hidden stream-engine or user-facing
eventing choices.

Supported parameters are bounded to:

- `eligibility_window_days`
- `fraud_threshold`
- `recovery_floor`
- `carrier_handoff_hours`
- `carbon_weight`
- `route_switch_threshold`
- `forecast_horizon_days`
- `anomaly_zscore_threshold`
- `workbench_limit`

Configuration requires `database_backend`, `event_topic`, `retry_limit`,
`default_currency`, `supported_carriers`, and `supported_dispositions`.
Runtime requires the AppGen-X topic `appgen.returns.events`, rejects stream
engine pickers or user-facing eventing choices, and accepts only PostgreSQL,
MySQL, or MariaDB backends.

Implementation metadata exports:

- `allowed_database_backends`
- `owned_tables`
- `api_contract`
- `permissions_contract`
- `shared_table_access = false`

## Public APIs

- `POST /returns`
- `POST /labels`
- `POST /inspection-grades`
- `POST /credit-adjustments`
- `POST /returns-reverse-logistics/events/inbox`
- `GET /returns-reverse-logistics-workbench`

The package-local API contract records owned tables touched per command,
declared upstream dependencies, required permissions, idempotency keys, fixed
AppGen-X eventing, and the absence of any stream-engine picker.

## Permissions Contract

Declared permissions:

- `returns_reverse_logistics.authorize`
- `returns_reverse_logistics.label`
- `returns_reverse_logistics.inspect`
- `returns_reverse_logistics.adjust`
- `returns_reverse_logistics.event.consume`
- `returns_reverse_logistics.configure`
- `returns_reverse_logistics.audit`

The action-permission mapping covers runtime configuration, rule and schema
registration, event consumption, return authorization, label generation,
inspection capture, credit adjustment, workbench rendering, and boundary
verification.

## Events

Emitted events:

- `ReturnAuthorized`
- `CreditAdjustmentIssued`

Consumed events:

- `OrderShipped`
- `PaymentCaptured`

Handlers are idempotent by
`returns_reverse_logistics:{event_type}:{event_id}`, retry at least three
times, write retry evidence into package-owned runtime state, and write
exhausted failures to `returns_reverse_logistics_dead_letter_event`.

## UI and Workbench

The UI exposes a returns workbench, return authorization console, eligibility
screening panel, return label console, carrier handoff board, inspection and
disposition workbench, credit adjustment console, refund/ledger handoff panel,
fraud signal panel, topology graph, return exception board, rule studio,
parameter console, configuration panel, and AppGen-X eventing monitor. The
workbench renders configuration/rule/parameter binding evidence directly from
package-owned runtime state, including owned-table binding evidence for inbox,
outbox, and dead-letter surfaces.

## Release Evidence

Release readiness requires passing package-local runtime smoke, API/event
contract evidence, AppGen-X inbox/outbox/dead-letter evidence, deterministic
rule compilation, bounded parameter validation, workbench render evidence,
tenant isolation checks, focused unit tests, and restricted legacy-name scans
over the package write scope.
