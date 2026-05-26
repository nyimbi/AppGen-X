# Returns and Reverse Logistics PBC Specification

`returns_reverse_logistics` is the AppGen-X packaged business capability for
RMA and reverse-flow execution. It owns return authorization, eligibility,
labels, receiving, inspection, disposition, refund or exchange settlement,
restocking and repair recovery, carrier claims, fraud and risk evidence,
customer-facing status, exception workflows, and package-local completeness
contracts under `src/pyAppGen/pbcs/returns_reverse_logistics/`.

Implementation entrypoint: `implementation_contract()`.

## Owned Boundary

- **PBC key:** `returns_reverse_logistics`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Required AppGen-X topic:** `appgen.returns.events`
- **Emits:** `ReturnAuthorized`, `CreditAdjustmentIssued`
- **Consumes:** `OrderShipped`, `PaymentCaptured`
- **Shared table access:** forbidden
- **Owned tables:** `return_authorization`, `return_line`,
  `return_eligibility_decision`, `return_policy_snapshot`,
  `reverse_route_graph`, `return_label`, `carrier_handoff`,
  `return_receipt`, `inspection_grade`, `inspection_finding`,
  `disposition_decision`, `refund_exchange_resolution`,
  `restocking_order`, `repair_refurbishment_order`, `carrier_claim`,
  `return_customer_status`, `return_exception_case`,
  `return_exception_task`, `return_fraud_signal`, `credit_adjustment`,
  `refund_ledger_handoff`, `inventory_recovery_projection`,
  `repair_vendor_projection`, `carrier_claim_projection`,
  `customer_notification_projection`, `order_return_projection`,
  `payment_return_projection`, `inventory_return_projection`,
  `ledger_return_projection`, `returns_reverse_logistics_rule`,
  `returns_reverse_logistics_parameter`,
  `returns_reverse_logistics_configuration`,
  `returns_reverse_logistics_schema_extension`, `return_proof`,
  `return_policy_screening`, `return_control_assertion`,
  `return_governed_model`, `return_seed_data`,
  `returns_reverse_logistics_outbox_event`,
  `returns_reverse_logistics_inbox_event`, and
  `returns_reverse_logistics_dead_letter_event`

Boundary validation is executable through
`returns_reverse_logistics_verify_owned_table_boundary(references)`. It allows
only owned tables, declared upstream APIs, declared consumed events, and
declared read-only projections. Schema extensions are accepted only for owned
tables and only for lowercase snake_case field names.

## Standard Table-Stakes

The package completeness contract covers:

1. RMA creation and return authorization.
2. Return eligibility evaluation and decision evidence.
3. Label generation and carrier handoff tracking.
4. Return receiving and receipt evidence.
5. Inspection grading and finding capture.
6. Disposition decisioning for restock, refurbish, or scrap.
7. Refund and exchange resolution metadata.
8. Restocking, repair, and refurbishment recovery records.
9. Carrier claims and downstream claim projections.
10. Fraud and abuse screening with customer-visible status updates.
11. Refund and ledger handoff evidence.
12. Customer status and exception workflow tracking.
13. Rule, parameter, and configuration support.
14. AppGen-X outbox, inbox, retry, and dead-letter evidence.
15. Package-local API, schema, service, permission, and release contracts.
16. Workbench and UI binding evidence without stream-engine selection.

## Advanced Runtime Evidence

The runtime proves the following advanced capabilities:

1. Event-sourced returns lifecycle.
2. Graph-relational reverse logistics topology.
3. Probabilistic eligibility scoring.
4. Counterfactual disposition simulation.
5. Temporal recovery forecasting.
6. Autonomous exception resolution.
7. Semantic return instruction parsing.
8. Predictive return risk.
9. Self-healing carrier and route selection.
10. Cryptographic return proof.
11. Immutable return audit trail.
12. Dynamic return policy screening.
13. Automated control testing.
14. Cross-system order, payment, inventory, and ledger federation.
15. Universal API plus async AppGen-X eventing.
16. Distributed-systems evidence for idempotent handlers.
17. Fraud and abuse screening.
18. Tenant isolation.
19. Chaos-tolerant reverse operations.
20. Crypto agility.
21. Carbon-aware routing.
22. Mathematical recovery optimization.
23. Disposition allocation mechanism design.
24. Return anomaly detection.
25. Stochastic exposure modeling.
26. Governed-model evidence.
27. Permission-governance evidence.

## Rules, Parameters, and Configuration

Rules require `rule_id`, `tenant`, `scope`, `status`,
`eligibility_policy`, `label_policy`, `inspection_policy`, and
`credit_policy`. Runtime compilation emits a deterministic `compiled_hash`
plus rule evidence. Rules reject stream-engine or user-facing eventing fields.

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
The event topic is fixed to `appgen.returns.events`; stream-engine pickers and
user-facing eventing choices are rejected.

## API Contract

The package-local API contract is descriptor-driven and includes configuration,
parameter, rule, schema-extension, return authorization, label generation,
receipt, inspection, disposition, credit, refund or exchange, carrier claim,
customer-status, inbox, workbench, schema-contract, service-contract, and
release-evidence routes.

Every descriptor states:

- route
- command or query
- owned tables touched
- required permission
- idempotency key where mutation occurs
- declared upstream API or event dependencies when external state is involved

The API contract explicitly records:

- `event_contract: AppGen-X`
- `required_event_topic: appgen.returns.events`
- `runtime_tables`
- `dependencies.shared_tables: ()`
- `shared_table_access: false`
- `stream_engine_picker_visible: false`
- `user_eventing_choice: false`

## Schema, Service, and Release Contracts

`returns_reverse_logistics_build_schema_contract()` emits generated table
descriptors, runtime-table descriptors, relationship metadata, migration
descriptors under `pbcs/returns_reverse_logistics/migrations/`, and generated
model descriptors for every owned table.

`returns_reverse_logistics_build_service_contract()` proves that mutations are
bounded to Returns-owned tables and that external state enters only through
declared APIs, events, and projections. It records the transaction boundary,
idempotent inbox handler, retry/dead-letter evidence, command methods for core
reverse-logistics flows, and query methods for forecasting, proof, anomaly,
policy, and release evidence.

`returns_reverse_logistics_build_release_evidence()` is the package-local
release gate. It combines schema depth, migration coverage, service depth,
AppGen-X event contract, permission coverage, duplicate/retry/dead-letter
control evidence, and workbench binding evidence. The package is not complete
unless this contract returns `ok: true`.

## Permissions

Declared permissions:

- `returns_reverse_logistics.authorize`
- `returns_reverse_logistics.label`
- `returns_reverse_logistics.inspect`
- `returns_reverse_logistics.adjust`
- `returns_reverse_logistics.event.consume`
- `returns_reverse_logistics.configure`
- `returns_reverse_logistics.audit`
- `returns_reverse_logistics.exception`
- `returns_reverse_logistics.claim`

Action-permission mappings cover return authorization, labels, receipt and
inspection, disposition and crediting, exchange resolution, carrier claims,
runtime configuration, schema and rule maintenance, workbench and contract
queries, and boundary verification.

## UI and Workbench Binding

The UI contract exposes:

- returns workbench
- return authorization console
- eligibility screening panel
- return label console
- carrier handoff board
- inspection and disposition workbench
- credit adjustment console
- refund/ledger handoff panel
- refund or exchange resolution panel
- restock/repair recovery panel
- carrier claims panel
- customer return status panel
- fraud signal panel
- topology graph
- exception board
- rule studio
- parameter console
- configuration panel
- AppGen-X eventing monitor

Workbench binding evidence includes `owned_tables`, `runtime_tables`, fixed
AppGen-X topic and contract, no shared-table access, and release-query
surfaces for schema, service, and release evidence.

## Release Expectations

Focused validation for this package must include:

- `py_compile` over the package and focused runtime test file
- focused `pytest` for `tests/test_pbc_returns_reverse_logistics_runtime.py`
- release evidence with no blocking gaps
- idempotent duplicate/retry/dead-letter evidence
- package-local checks that no stream-engine picker or user eventing selector
  appears in the package contract surface
