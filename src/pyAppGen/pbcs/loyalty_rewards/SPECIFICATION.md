# Loyalty Rewards PBC

`loyalty_rewards` is the AppGen-X packaged business capability for loyalty
member enrollment, rewards wallets, points ledgers, earning rules, redemptions,
tiering, partner accrual, promotional bonuses, liability controls, fraud review,
and customer-segment reward intelligence. It is a complete package-local
implementation with owned schema, runtime services, API descriptors, AppGen-X
events, idempotent handlers, rules, parameters, configuration, UI fragments,
package metadata, tests, and release evidence.

## Stable Identity

- PBC key: `loyalty_rewards`.
- Mesh: relationship.
- Package directory: `src/pyAppGen/pbcs/loyalty_rewards`.
- Runtime entrypoint: `loyalty_rewards_runtime_capabilities()`.
- UI entrypoint: `loyalty_rewards_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X event contract on
  `appgen.loyalty_rewards.events`.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

The package owns exactly these operational tables:

- `reward_account`: tenant, customer, currency, region, tier, status, balance,
  lifetime points, liability amount, and account audit proof.
- `points_ledger`: earn, adjustment, redemption, expiration, referral,
  promotion, and partner accrual entries with source evidence and audit proof.
- `earning_rule`: tenant-scoped earning policy, activity type, points per
  currency unit, tier multipliers, status, and compiled hash.
- `redemption`: reward reservation state, account, order reference, points,
  monetary value, status, and audit proof.

No customer, payment, promotion, segment, commerce, or finance tables are shared
or directly accessed. External information enters through declared AppGen-X
events and API projections only:

- Consumed events: `PaymentCaptured` and `PromotionApplied`.
- API projections: `payment_projection`, `promotion_projection`, and
  `customer_segment_projection`.
- Runtime event tables are PBC-local:
  `loyalty_rewards_appgen_outbox_event`,
  `loyalty_rewards_appgen_inbox_event`, and
  `loyalty_rewards_dead_letter_event`.

The boundary verifier accepts only owned tables, declared APIs/events,
declared projections, and PBC-local event tables. It rejects direct foreign
references such as `customer_account`.

## Standard Table-Stakes Capabilities

The implementation covers the ordinary loyalty capabilities expected from a
production rewards package:

- Member enrollment with tenant, customer, currency, region, tier, status,
  wallet balance, lifetime points, liability, and audit evidence.
- Runtime configuration for database backend, event topic, retry limit,
  default currency, supported currencies, supported regions, tier calendar,
  timezone, liability mode, and workbench limit.
- Parameter engine for base earn rate, tier multipliers, redemption value,
  fraud threshold, liability reserve, expiration days, max daily earn points,
  and workbench limit.
- Rule engine for tenant, scope, currency/region constraints, earning policy,
  redemption policy, tier policy, status, compiled hash, and policy-engine
  evidence.
- Schema extension for owned rewards tables only, with versioned migration
  evidence.
- Earning-rule registration for payment, promotion, referral, and partner
  activity types.
- Points issue, adjustment, redemption debit, expiration, partner accrual, and
  referral-style source tracking through the owned points ledger.
- Tier qualification based on lifetime point thresholds.
- Redemption validation requiring positive covered point balances.
- Liability amount calculation from outstanding reward balance.
- Idempotent AppGen-X handlers for `PaymentCaptured` and `PromotionApplied`.
- Reward balance event emission through `RewardBalanceChanged`.
- Customer segment update emission for qualified tiers through
  `CustomerSegmentUpdated`.
- Retry/dead-letter evidence for failed consumed-event handling.
- Workbench views for accounts, ledger, earning rules, redemptions, balances,
  liabilities, rules, parameters, configuration, outbox, and dead letters.
- UI fragments for account registry, ledger, earning-rule studio, redemption
  console, tier qualification, referral/partner evidence, expiration/liability,
  fraud review, rule studio, parameter console, configuration, outbox, and
  dead-letter queue.
- Permission/RBAC descriptors for account, points, redemption, event,
  configuration, and audit actions.
- Seed data for tiers and activity types.

## Advanced Capabilities

The executable runtime proves the advanced rewards capabilities needed for a
modern relationship PBC:

- Event-sourced rewards lifecycle with immutable state-event hashes.
- Owned rewards schema boundary enforcement with explicit violation evidence.
- Multi-tenant rewards isolation across accounts, ledger, rules, redemptions,
  and UI views.
- Schema-evolution-safe reward context extensions.
- Member enrollment and wallet management.
- Points earn, adjustment, redemption, and expiration ledgering.
- Tier qualification and benefit state.
- Partner accrual and offer projection evidence through declared integrations.
- Expiration and liability controls.
- Probabilistic breakage, customer value, churn, and fraud scoring evidence.
- Counterfactual offer simulation and temporal rewards-liability forecasting.
- Autonomous loyalty exception resolution.
- Semantic rewards-rule understanding.
- Predictive fraud and churn risk evidence.
- Self-healing balance reconciliation through ledger/account recomputation
  evidence.
- Cryptographic reward-balance proofs.
- Immutable rewards audit trail.
- Dynamic rewards policy screening.
- Automated liability control testing.
- Cross-system payment, promotion, and segment federation through declared
  APIs/events only.
- AppGen-X outbox/inbox eventing with idempotent handlers.
- Retry/dead-letter evidence.
- Permissions governance evidence.
- Configuration, rule, parameter, seed-data, and workbench evidence.
- Governed model evidence.

## Generated Schema

`loyalty_rewards_build_schema_contract()` is the package-local generated schema
descriptor for Loyalty Rewards. It proves:

- Every owned table in `LOYALTY_REWARDS_OWNED_TABLES` is present exactly once:
  `reward_account`, `points_ledger`, `earning_rule`, and `redemption`.
- Generated migration artifacts exist for every owned table in
  `pbcs/loyalty_rewards/migrations/{sequence}_{table}.sql`.
- Generated model artifacts exist for every owned table in
  `pyAppGen.pbcs.loyalty_rewards.models.{table}`.
- Runtime AppGen-X eventing evidence remains package-local through
  `loyalty_rewards_appgen_outbox_event`,
  `loyalty_rewards_appgen_inbox_event`, and
  `loyalty_rewards_dead_letter_event`.
- Shared-table access remains forbidden and the datastore allowlist stays
  limited to PostgreSQL, MySQL, and MariaDB.

## Service Layer

`loyalty_rewards_build_service_contract()` is the package-local service
descriptor. It proves the generated service, route, event, handler, UI,
permission, and configuration surfaces for Loyalty Rewards while keeping
ordinary eventing fixed to AppGen-X and stream-engine selection hidden.

The service layer exposes these package-local commands:

- `configure_runtime(configuration)`.
- `set_parameter(name, value)`.
- `register_rule(rule)`.
- `register_schema_extension(table, fields)`.
- `register_earning_rule(command)`.
- `enroll_member(command)`.
- `receive_event(event, simulate_failure=False)`.
- `issue_points(command)`.
- `adjust_points(command)`.
- `create_redemption(command)`.
- `expire_points(account_id, points=...)`.
- `build_api_contract()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references=...)`.

All commands are deterministic and side-effect-free: they accept explicit state
and return new state plus evidence payloads suitable for generated apps and
release smoke audits.

`loyalty_rewards_build_service_contract()` additionally proves:

- Generated service artifacts for every package-local command.
- Generated route artifacts for account, points, redemption, inbox, workbench,
  schema-contract, service-contract, and release-evidence surfaces.
- Generated event and handler artifacts for `PaymentCaptured`,
  `PromotionApplied`, `RewardBalanceChanged`, and
  `CustomerSegmentUpdated`.
- Generated UI artifacts for the owned rewards workbench fragments.
- Idempotent inbox handlers keyed by `event_id` with retry and dead-letter
  evidence bound to the package-local AppGen-X inbox/outbox tables.
- Permission mappings for command, audit, and release-evidence surfaces.
- Configuration schema evidence requiring the fixed AppGen-X topic
  `appgen.loyalty_rewards.events`, PostgreSQL/MySQL/MariaDB only, and no
  stream-engine picker.

## APIs

The package-local API contract exposes route descriptors:

- `POST /reward-accounts` runs `enroll_member`, writes `reward_account`,
  requires `loyalty_rewards.account.write`, and is idempotent by `account_id`.
- `POST /points` runs `issue_points`, writes `points_ledger` and
  `reward_account`, requires `loyalty_rewards.points.write`, emits reward
  events, and is idempotent by `ledger_id`.
- `POST /points/adjustments` runs `adjust_points`, writes `points_ledger` and
  `reward_account`, requires `loyalty_rewards.points.write`, emits reward
  events, and is idempotent by `ledger_id`.
- `POST /redemptions` runs `create_redemption`, writes `redemption`,
  `points_ledger`, and `reward_account`, requires
  `loyalty_rewards.redemption.write`, emits `RewardBalanceChanged`, and is
  idempotent by `redemption_id`.
- `POST /loyalty-rewards/events/inbox` runs `receive_event`, consumes declared
  AppGen-X events, requires `loyalty_rewards.event.consume`, and is idempotent
  by `event_id`.
- `GET /reward-accounts` queries `build_workbench_view`, reads only owned
  Loyalty Rewards state, and requires `loyalty_rewards.audit`.

The catalog-facing route set remains `POST /points`, `POST /redemptions`, and
`GET /reward-accounts`.

## Events And Handlers

Consumed events:

- `PaymentCaptured`.
- `PromotionApplied`.

Emitted events:

- `RewardBalanceChanged`.
- `CustomerSegmentUpdated`.

Handlers require event IDs, deduplicate already handled events, record inbox
evidence, translate payment and promotion events into owned ledger postings,
and send simulated failures to the dead-letter evidence queue. Users never
choose a stream engine.

## UI And Workbench

The UI contract exposes:

- Reward account registry.
- Points ledger panel.
- Earning rule studio.
- Redemption console.
- Tier qualification board.
- Referral and partner panel.
- Expiration and liability panel.
- Fraud review queue.
- Rewards rule studio.
- Rewards parameter console.
- Rewards configuration panel.
- Rewards event outbox.
- Rewards dead-letter queue.

Rendered workbench output includes tenant-filtered account, ledger, earning
rule, redemption, balance, liability, outbox, and dead-letter counts; visible
and locked actions from RBAC permissions; and owned-table binding evidence.

## Release Evidence

`loyalty_rewards_build_release_evidence()` is the package-local release gate.
It combines schema, service, API, and permission evidence and proves:

Focused tests prove:

- Runtime capability and smoke checks cover every advanced capability key.
- Configuration, rule, parameter, schema-extension, earning-rule, enrollment,
  event handling, point issue, point adjustment, redemption, outbox emission,
  UI rendering, API descriptors, RBAC descriptors, and workbench evidence
  execute.
- AppGen-X eventing is fixed and stream-engine picker exposure is false.
- Backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Boundary validation accepts owned tables and declared dependencies and
  rejects direct foreign table references.
- Invalid database backends, invalid parameters, non-owned schema extensions,
  and simulated handler failures are rejected or dead-lettered.
- The package participates in all-PBC implementation release and generation
  smoke audits.
