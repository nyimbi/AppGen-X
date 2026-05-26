# Returns and Reverse Logistics PBC

## Purpose

The Returns and Reverse Logistics PBC owns return authorizations, RMAs, return
eligibility, return labels, carrier handoff, receipt and inspection evidence,
disposition routing, restock/refurbish/scrap routing, credit adjustments,
refund and ledger handoff, fraud and abuse screening, runtime control
evidence, and the returns workbench. It integrates with order, payment,
inventory, ledger, identity, and platform event infrastructure through APIs,
AppGen-X events, and read-only federated projections.

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
- `returns_reverse_logistics_outbox`, `returns_reverse_logistics_inbox`, and
  `returns_reverse_logistics_dead_letter`: AppGen-X event contract tables for
  idempotent handlers, retry evidence, and dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB only.

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

## Public APIs

- `POST /returns`
- `POST /labels`
- `POST /inspection-grades`

## Events

Emitted events:

- `ReturnAuthorized`
- `CreditAdjustmentIssued`

Consumed events:

- `OrderShipped`
- `PaymentCaptured`

Handlers are idempotent by
`returns_reverse_logistics:{event_type}:{event_id}`, retry at least three
times, and write exhausted failures to
`returns_reverse_logistics_dead_letter`.

## UI and Workbench

The UI exposes a returns workbench, return authorization console, eligibility
screening panel, return label console, carrier handoff board, inspection and
disposition workbench, credit adjustment console, refund/ledger handoff panel,
fraud signal panel, topology graph, return exception board, rule studio,
parameter console, configuration panel, and AppGen-X eventing monitor. The
workbench renders configuration/rule/parameter binding evidence directly from
package-owned runtime state.

## Release Evidence

Release readiness requires passing package-local runtime smoke, API/event
contract evidence, AppGen-X inbox/outbox/dead-letter evidence, deterministic
rule compilation, bounded parameter validation, workbench render evidence,
tenant isolation checks, focused unit tests, and restricted legacy-name scans
over the package write scope.
