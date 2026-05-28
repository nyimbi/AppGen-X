# Loyalty Rewards PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `loyalty_rewards`. Each item is specific to loyalty member enrollment, rewards wallets, points ledgers, earning rules, redemption reservations, tier qualification, partner accrual, referrals, offer eligibility, liability controls, breakage forecasting, fraud review, policy screening, customer reward intelligence, agent assistance, and AppGen-X event reliability.

## Current Domain Evidence Used

- Domain purpose: loyalty member enrollment, rewards wallets, points ledgers, earning rules, redemptions, tiering, partner accrual, promotional bonuses, liability controls, fraud review, and customer-segment reward intelligence.
- Owned operational surface: reward accounts, points ledger, earning rules, redemptions, reward tiers, tier benefits, referral rewards, partner accruals, offer eligibility, offer simulation, breakage forecasts, expiration schedules, liability snapshots, liability control assertions, fraud reviews, churn risk scores, rewards policy screenings, loyalty exceptions, balance reconciliations, reward balance proofs, audit entries, federation views, governed models, and AppGen-X runtime event tables.
- Declared commands and APIs: runtime configuration, parameter/rule/schema registration, earning-rule registration, member enrollment, event receipt, point issue/adjustment/expiration, redemption creation, tier qualification, referral rewards, partner accruals, offer eligibility, expiration scheduling, liability snapshots, fraud review, churn scoring, breakage forecasting, offer simulation, exception resolution, balance reconciliation, balance proof generation, rewards policy screening, liability controls, federation views, governed model registration, workbench construction, permissions, and owned-boundary verification.
- Declared events and integrations: consumes `PaymentCaptured` and `PromotionApplied`; emits `RewardBalanceChanged` and `CustomerSegmentUpdated`; uses declared payment, promotion, and customer-segment projections without shared-table access.
- Advanced capability evidence: event-sourced rewards lifecycle, owned rewards schema boundary, multi-tenant rewards isolation, schema-evolution-safe reward context, wallet management, points earn/adjust/redeem/expire ledgering, tier qualification and benefits, partner accrual, offer projection, liability controls, probabilistic breakage/customer-value/churn/fraud scoring, counterfactual offer simulation, temporal liability forecasting, exception resolution, semantic rewards-rule understanding, self-healing reconciliation, cryptographic balance proofs, immutable audit trail, dynamic policy screening, AppGen-X eventing, retry/dead-letter evidence, permissions, configuration, seed data, and governed models.

## 50 Better-Than-World-Class Improvements

### 1. Member enrollment eligibility gate

**Justification:** Loyalty programs need controlled enrollment so duplicate accounts, ineligible regions, unsupported currencies, underage customers, employee exclusions, and missing consent do not create invalid wallets or liability.

**Improvement:** Add an enrollment gate that checks customer identity confidence, region, currency, consent, account uniqueness, existing wallet links, fraud risk, partner-program eligibility, and required disclosures. Store eligibility evidence and allow the agent to prepare enrollment plans without creating accounts until approved.

### 2. Reward account lifecycle state machine

**Justification:** Reward accounts move through pending, active, suspended, merged, closed, fraud-hold, deceased/estate, migrated, and archived states with different ledger and redemption rules.

**Improvement:** Implement a strict account state machine with allowed transitions, required approvals, ledger effects, redemption restrictions, customer communication requirements, and audit proof. Release checks should reject point activity on accounts in disallowed states.

### 3. Wallet currency and unit governance

**Justification:** Loyalty balances can represent points, miles, credits, stamps, cashback, or partner units, each with conversion and liability implications.

**Improvement:** Add wallet unit metadata for unit type, precision, base currency, redemption value, liability method, partner conversion rate, rounding policy, and expiration behavior. UI should show both member-facing balance and finance-facing liability values.

### 4. Immutable points ledger controls

**Justification:** The points ledger is the source of truth for member trust and financial liability; direct balance edits are unsafe.

**Improvement:** Enforce append-only ledger entries with entry type, source event, rule version, account state, idempotency key, reversal link, balance-after proof, and liability impact. Provide correction entries instead of mutable point balances.

### 5. Ledger reversal and adjustment governance

**Justification:** Returns, cancellations, fraud, customer goodwill, partner corrections, and operational mistakes require controlled ledger changes.

**Improvement:** Add adjustment and reversal workflows with reason taxonomy, source evidence, approver thresholds, customer visibility, expiration impact, tier impact, and liability recalculation. The agent should show before/after balance, tier, and liability effects.

### 6. Earning rule version control

**Justification:** Earn rates change by campaign, tier, product, region, channel, currency, partner, and time window; historical earnings must remain tied to the active rule version.

**Improvement:** Version earning rules with effective intervals, eligibility predicates, tier multipliers, promotion stacking, partner overrides, rounding, caps, and compiled hashes. Ledger entries should store the exact rule version and calculation trace.

### 7. Earning simulation sandbox

**Justification:** Program managers need to preview how rule changes affect member value, liability, fraud exposure, partner settlement, and customer behavior.

**Improvement:** Add earning simulations over historical payments, promotions, partner events, customer segments, and tier mix. Show expected points issued, incremental liability, impacted members, edge cases, and recommended guardrails before activation.

### 8. Promotion stacking governance

**Justification:** Loyalty earn bonuses can accidentally stack with promotions, referrals, partners, and tier multipliers to create excessive liability or unfair eligibility.

**Improvement:** Add stacking rules, exclusion groups, maximum earn caps, precedence, campaign budgets, and conflict detection. Offer readiness should show which bonuses apply, suppress, or require approval.

### 9. Tier qualification calendar

**Justification:** Tier qualification depends on calendar model, rolling windows, grace periods, soft landings, status matches, lifetime status, and exception handling.

**Improvement:** Model tier calendars with qualification period, benefit period, grace period, downgrade policy, lifetime thresholds, status-match evidence, and tier-freeze rules. Store tier decisions with window, points counted, exclusions, and next-review date.

### 10. Tier benefit entitlement ledger

**Justification:** Benefits such as free shipping, support priority, discounts, upgrades, credits, or exclusive access must be traceable and revocable when tier changes.

**Improvement:** Add a benefit ledger linking tiers to granted, consumed, expired, revoked, and transferred benefits with eligibility, source tier decision, usage evidence, and downstream projection payloads. UI should separate point balance from benefit inventory.

### 11. Tier downgrade fairness controls

**Justification:** Downgrades can harm customer trust when late postings, refunds, exceptional events, or system outages affected qualification.

**Improvement:** Add downgrade review checks for late partner accruals, pending disputes, goodwill policies, outage windows, protected cohorts, and manual exceptions. Generate member communication evidence for downgrades and soft landings.

### 12. Redemption reservation lifecycle

**Justification:** Redemptions need reservation, confirmation, cancellation, expiry, reversal, partial fulfillment, and fraud-hold states to avoid double-spend and customer disputes.

**Improvement:** Implement redemption reservations with hold expiry, points lock, order/reference link, monetary value, confirmation event, reversal policy, partial release, and duplicate protection. The UI should show available, held, and redeemable balances separately.

### 13. Redemption catalog governance

**Justification:** Members need valid redemption options with pricing, stock/capacity, region, tier, partner, expiration, and fulfillment rules.

**Improvement:** Add redemption catalog descriptors for reward type, point cost, cash value, inventory/capacity, fulfillment method, eligible tiers, regions, blackout dates, partner obligations, and policy proof. Block redemptions against retired or exhausted offers.

### 14. Redemption value optimization

**Justification:** Programs must balance member delight, margin, liability, breakage, and partner economics when presenting redemption choices.

**Improvement:** Add recommendation models that rank redemption options by member preference, liability reduction, cost, partner capacity, margin, and fairness constraints. Store why each recommendation was shown and allow deterministic rule-only mode.

### 15. Point expiration fairness workflow

**Justification:** Expiration is financially important but customer-sensitive, especially when members lacked notice or had pending activity.

**Improvement:** Add expiration schedules with notice requirements, rescue offers, grace windows, protected statuses, jurisdiction rules, and late-activity recalculation. Store notification evidence and member-facing explanation for every expired point batch.

### 16. Expiration batch simulation

**Justification:** Before expiring points, operators need to understand balance impact, member sentiment risk, liability release, and customer-service volume.

**Improvement:** Simulate expiration batches by segment, tier, geography, balance size, last activity, notice state, and support-risk score. Provide projected liability release, complaint risk, reactivation opportunity, and recommended exclusions.

### 17. Liability snapshot drilldown

**Justification:** Rewards liability must reconcile outstanding points, redemption value, breakage assumptions, partner obligations, and finance reporting.

**Improvement:** Add liability snapshots with account-level rollups, tier/value bands, expiration schedules, redemption reservations, partner receivables/payables, breakage assumptions, and reconciliation deltas. Provide drilldowns from liability total to ledger entries.

### 18. Liability control assertions

**Justification:** Loyalty liability can materially affect financial statements and requires continuous control evidence.

**Improvement:** Add controls for ledger immutability, balance reconciliation, expiration authorization, redemption holds, partner accrual completeness, breakage model approval, and rule change approvals. Store pass/fail assertions and remediation tasks.

### 19. Breakage forecasting governance

**Justification:** Breakage estimates are sensitive, model-driven, and financially material; unsupported assumptions create audit risk.

**Improvement:** Govern breakage forecasts with cohort definitions, historical redemption behavior, expiry rules, member activity, tier status, promotional effects, model version, confidence intervals, and approval evidence. Provide scenario comparisons and assumption sensitivity.

### 20. Partner accrual reconciliation

**Justification:** Partner earns can arrive late, duplicate, disputed, or valued under different conversion agreements.

**Improvement:** Add partner accrual reconciliation by partner, contract, event source, external reference, conversion rate, settlement period, duplicate status, dispute state, and ledger posting. Surface unmatched and late accruals in a dedicated console.

### 21. Partner settlement evidence

**Justification:** Partner loyalty programs require clear settlement of issued points, redeemed benefits, reversals, breakage, and fees.

**Improvement:** Add settlement statements with partner obligations, customer-visible points, finance liability, invoice/export payloads, exception items, and approval workflow. Keep all settlement data inside owned tables or declared projections.

### 22. Referral fraud controls

**Justification:** Referral programs attract self-referrals, synthetic accounts, collusion, returns abuse, and incentive gaming.

**Improvement:** Score referrals using identity overlap, device/address similarity, purchase quality, return history, velocity, geographic patterns, and reward value. Hold suspicious rewards, generate review cases, and preserve explainable fraud evidence.

### 23. Referral lifecycle management

**Justification:** Referrals need invite, click, signup, qualified action, pending reward, approved reward, rejected reward, reversal, and expiry states.

**Improvement:** Add referral lifecycle tracking with eligibility, qualification criteria, attribution window, source campaign, referrer/referee rules, reward timing, and customer communication state. UI should show referral progress and reasons for pending or rejected rewards.

### 24. Offer eligibility decision traces

**Justification:** Members and operators need to understand why a loyalty offer was shown, hidden, blocked, or expired.

**Improvement:** Store offer eligibility traces with segment projection, tier, balance, purchase history projection, promotion context, consent, region, fraud risk, budget, and rule version. Provide customer-safe and operator-detailed explanations.

### 25. Offer fatigue and fairness controls

**Justification:** Over-targeting loyal members or excluding borderline members can reduce trust and create inequitable outcomes.

**Improvement:** Add offer fatigue caps, diversity constraints, cohort fairness checks, protected-rule restrictions, exposure history, and suppression explanations. Simulations should show overexposed and under-served cohorts.

### 26. Churn-aware reward interventions

**Justification:** Rewards can reduce churn when targeted carefully, but indiscriminate incentives waste liability and train customers to wait for offers.

**Improvement:** Combine churn risk, customer value, tier, breakage, engagement, and offer history to recommend retention rewards with guardrails. Store expected impact, cost, confidence, and ethical-use constraints.

### 27. Fraud review case workflow

**Justification:** Loyalty fraud review needs consistent intake, evidence, investigation, decision, customer communication, and ledger action.

**Improvement:** Add fraud review states, risk drivers, linked accounts, suspicious ledger entries, investigator notes, hold/release actions, reversal actions, and appeal handling. The agent should summarize evidence without exposing unrelated customers.

### 28. Account merge and split workflow

**Justification:** Duplicate loyalty accounts and mistaken merges affect balances, tiers, referrals, redemptions, and liability.

**Improvement:** Add merge/split workflows with identity evidence, ledger consolidation preview, tier recalculation, referral handling, redemption hold review, consent/preference checks, and rollback plan. Require approval for high-value accounts.

### 29. Balance reconciliation automation

**Justification:** Wallet balance must equal ledger-derived balance after earns, adjustments, redemptions, expirations, reversals, and partner events.

**Improvement:** Run reconciliation that recomputes balances, flags mismatches, isolates offending entries, proposes correction entries, and records proof. UI should show reconciled, unreconciled, and corrected accounts.

### 30. Cryptographic reward balance proof

**Justification:** Members, partners, finance, and auditors may need proof that balances and liabilities were computed from untampered ledger entries.

**Improvement:** Generate cryptographic proofs for account balance, tier status, redemption reservations, liability snapshots, and partner accrual statements. Support redacted verifier artifacts that do not reveal unrelated member activity.

### 31. Rewards policy compiler

**Justification:** Program rules are complex and change frequently across regions, products, partners, tiers, and promotions.

**Improvement:** Compile policy from structured rules and natural-language program documents into validated predicates with effective dates, conflict detection, test cases, and approval evidence. The agent should explain ambiguous language and request missing thresholds.

### 32. Rewards rule impact analysis

**Justification:** Changing earning, redemption, tier, expiration, or referral rules can shift liability and member experience at scale.

**Improvement:** Add impact analysis for affected members, point issuance, liability, tier movement, redemption cost, breakage, partner settlement, and complaint risk. Require review for high-impact changes before activation.

### 33. Customer segment synchronization

**Justification:** Loyalty tiers and reward behaviors feed customer segments, while customer segments influence offers and earning rules.

**Improvement:** Define bidirectional but boundary-safe segment synchronization through declared events/projections only. Store projection freshness, segment source, allowed usage, and member-impact evidence for segment-driven loyalty decisions.

### 34. Payment and promotion event hardening

**Justification:** Points issued from payments and promotions must be idempotent, reversible, and explainable despite late captures, refunds, duplicate events, or promotion corrections.

**Improvement:** Harden consumed event handling with schema versions, idempotency keys, source references, reversal detection, promotion stacking evidence, retry envelopes, and dead-letter reason taxonomy. Add generated tests for earn, duplicate, failure, and replay scenarios.

### 35. Return and refund point clawback

**Justification:** Returned purchases should reverse or adjust earned points without unfairly penalizing unrelated balances or confirmed redemptions.

**Improvement:** Add clawback rules for full returns, partial returns, exchanges, refund delays, negative balances, tier impact, and expired points. Store member-facing explanations and fraud-review triggers for suspicious return patterns.

### 36. Negative balance governance

**Justification:** Reversals can create negative point balances, creating disputes and future earn-capture questions.

**Improvement:** Define negative-balance policies by tier, reason, amount, customer status, and jurisdiction. Decide whether to hold redemptions, offset future earns, forgive balances, or create exception reviews with audit evidence.

### 37. Member-facing rewards statement

**Justification:** Members need a clear statement of earns, adjustments, redemptions, expirations, holds, tier progress, and upcoming changes.

**Improvement:** Generate statement views with ledger entries, rule explanations, expiration schedule, pending redemptions, tier progress, benefits, partner accruals, and dispute links. Ensure sensitive internal fraud or policy notes remain hidden.

### 38. Loyalty operations cockpit

**Justification:** Operators need a unified view of balances, liability, fraud reviews, partner accruals, redemptions, expirations, tiers, exceptions, and AppGen-X event health.

**Improvement:** Build cockpit panels for program KPIs, liability movement, high-risk accounts, pending redemptions, partner exceptions, tier movement, expiration batches, fraud queues, dead letters, and controls. Every action should map to a permissioned service command.

### 39. Rewards anomaly detection

**Justification:** Sudden earn spikes, redemption bursts, partner event anomalies, referral rings, or tier jumps can indicate fraud or integration defects.

**Improvement:** Add anomaly detection for ledger velocity, balance jumps, redemption frequency, partner accrual spikes, referral clusters, expiration reversals, and tier movement outliers. Route severe anomalies to fraud review or operational hold.

### 40. Loyalty exception resolution

**Justification:** Programs need controlled handling for disputed points, missing earns, failed redemptions, partner delays, tier appeals, and goodwill adjustments.

**Improvement:** Add exception case types with required evidence, SLA, owner, customer communication, ledger action, partner action, and closure criteria. The agent should prepare exception-resolution plans with balance and liability impact.

### 41. Customer value and reward ROI analytics

**Justification:** Loyalty programs must prove incremental value, not merely issue points.

**Improvement:** Add analytics for incremental revenue, redemption lift, retention impact, tier migration, member engagement, offer ROI, liability cost, breakage, and control cohorts. Store assumptions and confidence intervals to avoid overstating causality.

### 42. Loyalty experiment framework

**Justification:** Earn rates, offers, expiration notices, and tier benefits should be tested with holdouts and controlled cohorts.

**Improvement:** Add experiment cells, holdouts, randomization, eligibility constraints, exposure tracking, outcome capture, and statistical reporting. Tie experiment results to rule versions and future recommendations.

### 43. Agent-assisted loyalty service

**Justification:** Support agents and members need help understanding balances, missing points, redemptions, and tier status without unsafe direct mutation.

**Improvement:** Let the PBC agent answer balance questions, explain ledger entries, find missing earn evidence, draft adjustment requests, and preview redemptions. Any CRUD action should show before/after balance, tier, liability, and policy checks before approval.

### 44. Agent-assisted program design

**Justification:** Loyalty managers often describe desired programs in documents, spreadsheets, or natural-language rules.

**Improvement:** Add agent skills to parse program documents into earning rules, tier calendars, benefit catalogs, redemption policies, expiration rules, and test cases. The agent should surface ambiguity and generate side-effect-free activation plans.

### 45. Privacy and consent-aware rewards

**Justification:** Loyalty operations use customer behavior, segments, and preferences that may be subject to consent, privacy, and purpose restrictions.

**Improvement:** Add consent/purpose checks for offer eligibility, segment use, member statements, partner sharing, and analytics. Store the consent state used and block reward decisions where allowed purpose is missing.

### 46. Multi-tenant program isolation proof

**Justification:** Reward balances, program rules, partner contracts, and liability must never bleed across tenants or brands.

**Improvement:** Generate tenant isolation proofs for accounts, ledgers, rules, redemptions, tiers, partner accruals, liability snapshots, models, events, and UI queries. Release audits should fail any cross-tenant query or undeclared shared table access.

### 47. AppGen-X event reliability proof

**Justification:** Loyalty rewards depend on payment and promotion events and emit balance and segment events; duplication or loss directly affects member trust and liability.

**Improvement:** Add event reliability proof for consumed and emitted schemas, idempotency, ordering, retries, dead letters, replay, and recovery. Include payment duplicate, promotion correction, handler failure, and outbox replay scenarios.

### 48. UI capability surface proof

**Justification:** A complete Loyalty Rewards PBC must expose its domain operations through dedicated UI surfaces, not generic tables.

**Improvement:** Add release checks proving UI coverage for enrollment, accounts, ledger, earning rules, adjustments, redemptions, tiers, benefits, referrals, partners, offers, expiration, liability, fraud, churn, breakage, simulations, exceptions, reconciliation, proofs, policy screening, events, controls, and agent tools.

### 49. Rewards resilience drills

**Justification:** Rewards systems must recover from event backlogs, partner feed outages, bad rule deployments, balance mismatches, fraud spikes, and redemption failures.

**Improvement:** Add resilience drills for payment event replay, promotion rollback, partner outage, invalid rule activation, redemption provider failure, reconciliation mismatch, and dead-letter surge. Store recovery time, duplicate-risk assessment, liability impact, and corrective actions.

### 50. End-to-end loyalty release proof

**Justification:** A world-class Loyalty Rewards PBC needs a single evidence package proving that a member can enroll, earn, adjust, redeem, qualify, receive benefits, handle partner/referral activity, reconcile balances, forecast liability, and operate safely.

**Improvement:** Create an end-to-end proof exercising enrollment, earning rule compilation, payment earn, promotion bonus, adjustment, redemption reservation, tier qualification, benefit grant, referral reward, partner accrual, expiration schedule, liability snapshot, fraud review, breakage forecast, offer simulation, exception resolution, balance reconciliation, cryptographic proof, UI coverage, AppGen-X eventing, boundary verification, and agent-safe CRUD planning.
