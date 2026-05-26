# Loyalty Rewards PBC

`loyalty_rewards` owns member enrollment, reward accounts, earning rules, a points ledger, redemptions, tier qualification, referral and partner accrual evidence, expiration handling, liability controls, and reward-governance proof for AppGen-X generated applications.

## Owned Boundary

- Owned tables: `reward_account`, `points_ledger`, `earning_rule`, `redemption`.
- Integration boundary: declared APIs, AppGen-X outbox/inbox events, and projections only.
- Datastore backends: PostgreSQL, MySQL, or MariaDB.
- Eventing: AppGen-X event contract on `appgen.loyalty_rewards.events`; no user-facing stream-engine selection.

## Standard Capabilities

- Member enrollment, reward accounts, wallet balances, and tier state.
- Points earn, adjustment, expiration, partner accrual, referral, promotion, and redemption ledger entries.
- Earning rules, redemption policies, tier policies, liability reserve controls, and fraud review thresholds.
- Idempotent consumption of `PaymentCaptured` and `PromotionApplied`.
- Emission of `RewardBalanceChanged` and `CustomerSegmentUpdated` through the AppGen-X outbox.
- Retry/dead-letter evidence, RBAC descriptors, configuration schema, parameter engine, rule engine, seed data, and workbench views.

## Advanced Capabilities

- Event-sourced rewards lifecycle and immutable rewards audit trail.
- Probabilistic breakage, customer value, churn, and fraud scoring evidence.
- Counterfactual offer simulation and temporal rewards-liability forecasting.
- Autonomous loyalty exception resolution and semantic rewards-rule understanding.
- Dynamic policy screening, automated liability control testing, and self-healing balance reconciliation.
- Cross-system payment, promotion, and segment federation through declared APIs/events only.
- Governed model evidence and cryptographic reward-balance proofs.

## UI

The workbench exposes reward account registry, points ledger panel, earning rule studio, redemption console, tier qualification board, referral and partner panel, expiration and liability panel, fraud review queue, rule studio, parameter console, configuration panel, outbox, and dead-letter queue fragments.
