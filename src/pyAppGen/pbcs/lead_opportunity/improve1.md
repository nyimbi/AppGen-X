# Lead Opportunity PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `lead_opportunity`. The items are specific to revenue pipeline execution: account hierarchy, lead intake, enrichment, deduplication, scoring, assignment, qualification, opportunities, stage history, pipeline forecasting, quote/proposal handoffs, win/loss outcomes, sales activities, coaching insights, customer segment projections, rules, parameters, configuration, AppGen-X event reliability, UI workbenches, and agent-assisted sales operations.

## Current Domain Evidence Used

- Domain purpose: `lead_opportunity` owns revenue pipeline intake, lead scoring, qualification, account hierarchy management, opportunity execution, sales activity evidence, revenue forecasting, and customer-update publication.
- Owned boundary: leads, enrichment snapshots, dedupe cases, score snapshots, assignments, qualification decisions, opportunities, stage history, forecast snapshots, quote/proposal handoffs, outcomes, account hierarchies, sales activities, coaching insights, audit events, rules, parameters, configuration, governed models, seed data, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: runtime configuration, parameters, rules, schema extensions, event receiving, account hierarchy creation, lead creation/enrichment/qualification, opportunity creation, sales activity recording, stage advancement, quote/proposal handoff, opportunity win/loss, workbench, API/schema/service/release evidence, permissions, UI binding, and boundary verification.
- Existing events and dependencies: emits `LeadQualified`, `OpportunityWon`, `OpportunityLost`, `CustomerUpdated`, and `QuoteProposalRequested`; consumes `CustomerSegmentUpdated`; integrates with customer, segment, billing, territory, marketing, product, quote/proposal, and finance only through declared APIs/events/projections.

## 50 Better-Than-World-Class Improvements

### 1. Account hierarchy readiness gate

**Justification:** Opportunity ownership and forecast rollups are unreliable when account identity, parentage, owner, region, and customer projection evidence are incomplete.

**Improvement:** Add readiness checks for account id, tenant, parent account, customer projection key, region, owner, active status, duplicate account risk, hierarchy depth, and audit proof before account hierarchy creation.

### 2. Account hierarchy integrity controls

**Justification:** Bad account hierarchy creates duplicate selling effort, wrong territory credit, and distorted pipeline forecasts.

**Improvement:** Enforce acyclic parentage, effective dating, parent-child region compatibility, owner inheritance, customer projection freshness, merge/split lineage, and hierarchy rollup recalculation.

### 3. Lead intake readiness gate

**Justification:** Lead capture must verify source, contact, consent, region, currency, account context, and duplicate risk before entering the pipeline.

**Improvement:** Validate source, contact fields, email/domain, tenant, region, currency, estimated value, consent marker, customer/account projection, duplicate candidates, and assignment policy before lead creation.

### 4. Lead lifecycle state machine

**Justification:** Leads move through captured, enriched, dedup_review, scored, assigned, qualified, disqualified, converted, stale, and archived states.

**Improvement:** Implement lead transitions with actor, timestamp, reason, score snapshot, assignment evidence, qualification decision, emitted event expectations, and invalid-transition explanations.

### 5. Lead enrichment snapshot governance

**Justification:** Enrichment changes firmographic, contact, segment, value, and fit evidence used for qualification.

**Improvement:** Store enrichment source, fields changed, confidence, freshness, consent status, segment fit, account match, value estimate, rejected enrichments, and audit hash.

### 6. Lead dedupe case workflow

**Justification:** Duplicate leads fragment pipeline ownership and inflate funnel metrics.

**Improvement:** Add dedupe cases with candidate leads, matching factors, confidence, owner conflicts, merge/suppress/keep decisions, reviewer, account impact, and downstream score recalculation.

### 7. Lead score snapshot model

**Justification:** Qualification and assignment need explainable scoring rather than opaque totals.

**Improvement:** Record source weight, segment fit, engagement score, account fit, estimated value, region fit, stale activity, negative signals, score version, confidence, and threshold comparison.

### 8. Assignment engine governance

**Justification:** Lead assignment affects response time, fairness, territory rules, and quota credit.

**Improvement:** Add assignment rules for territory, segment, account owner, workload, skill, language, value, round-robin, named account, and fallback owner with assignment rationale.

### 9. Qualification decision evidence

**Justification:** Qualified leads trigger opportunity creation and must be auditably justified.

**Improvement:** Store threshold, score, missing data, disqualifying factors, reviewer override, decision reason, valid-through date, and `LeadQualified` event evidence.

### 10. Open opportunity limit controls

**Justification:** Excess open opportunities per account or owner can distort forecasts and reduce execution quality.

**Improvement:** Enforce configurable limits by account, customer, owner, segment, and region with exception workflow and assignment/reassignment recommendations.

### 11. Opportunity creation readiness

**Justification:** Opportunities should be created only from qualified leads or explicit account expansion with value, stage, owner, and close-date evidence.

**Improvement:** Validate qualified lead, account hierarchy, amount, currency, stage, close date, owner, win probability, forecast amount, risk score, and quote/proposal eligibility.

### 12. Opportunity lifecycle state machine

**Justification:** Opportunities require controlled progression through pipeline stages, forecast changes, quote handoffs, win/loss, and closure.

**Improvement:** Implement states for open, qualified, discovery, proposal, negotiation, commit, won, lost, stalled, slipped, and archived with transition rules and audit events.

### 13. Stage history integrity

**Justification:** Stage velocity, slippage, and forecast accuracy depend on accurate stage history.

**Improvement:** Record prior/new stage, timestamp, owner, reason, required fields, probability change, expected close-date change, stale activity warning, and forecast snapshot linkage.

### 14. Pipeline forecast snapshot engine

**Justification:** Forecasts must be reproducible by time, stage, probability, owner, region, and confidence.

**Improvement:** Generate snapshots with open amount, weighted amount, commit/best-case/pipeline views, probability, close-date distribution, slippage risk, confidence, and source opportunity list.

### 15. Deal slippage detection

**Justification:** Slipped opportunities degrade forecast trust and need early intervention.

**Improvement:** Detect close-date pushes, stale activity, stage stagnation, negative sentiment, missing next step, quote delay, and low engagement with slippage risk score and recommended action.

### 16. Win probability calibration

**Justification:** Static stage probabilities rarely reflect actual deal quality.

**Improvement:** Calibrate win probability from stage, activity sentiment, account fit, segment fit, deal age, owner history, quote status, competitor/risk notes, and historical outcomes.

### 17. Quote/proposal handoff governance

**Justification:** Quote handoffs should include enough opportunity, customer, pricing, and approval context without sharing quote tables.

**Improvement:** Store handoff id, opportunity id, requested products/services, amount, currency, customer/account projection, required approvals, deadline, idempotency key, and `QuoteProposalRequested` evidence.

### 18. Opportunity outcome capture

**Justification:** Win/loss outcomes feed forecasting, coaching, customer updates, and product/pricing feedback.

**Improvement:** Capture outcome type, reason, competitor, amount, close date, sales cycle, lost stage, customer feedback, next opportunity flag, and downstream event evidence.

### 19. Win handoff controls

**Justification:** Won opportunities trigger customer updates and downstream revenue activity.

**Improvement:** Gate `OpportunityWon` and `CustomerUpdated` on final stage, amount/currency validation, account/customer projection freshness, quote/proposal status, owner approval, and duplicate-win prevention.

### 20. Loss analysis workflow

**Justification:** Losses need structured reasons and coaching feedback to improve future pipeline quality.

**Improvement:** Add loss categories, competitor, price/product/fit reason, engagement pattern, stage lost, late-stage risk flags, coaching insight, and forecast model feedback.

### 21. Sales activity evidence model

**Justification:** Activity history drives next-best action, forecast confidence, and coaching.

**Improvement:** Store activity type, subject, timestamp, owner, channel, sentiment, participants, outcome, next step, follow-up date, opportunity link, and immutable proof.

### 22. Sentiment and intent extraction

**Justification:** Activity notes can reveal budget, authority, need, timing, risk, and objections.

**Improvement:** Extract structured sentiment, intent, objections, buying signals, timeline, decision makers, competitor mentions, and next-best action candidates with reviewer confidence.

### 23. Next-best-action engine

**Justification:** Sellers need prioritized actions that improve conversion and deal velocity.

**Improvement:** Recommend actions based on stage, stale activity, sentiment, missing stakeholders, quote delay, close-date risk, buyer objections, and segment fit with rationale and expected impact.

### 24. Sales coaching insight lifecycle

**Justification:** Coaching should be actionable, accepted or dismissed, and measured against outcomes.

**Improvement:** Add insight states, source activity, recommendation, owner, manager review, accepted/dismissed reason, follow-up evidence, and outcome correlation.

### 25. Customer segment projection handling

**Justification:** Lead and opportunity scoring depends on customer-segment context that must remain projection-only.

**Improvement:** Consume `CustomerSegmentUpdated` into package-local projections with segment id, version, freshness, confidence, allowed use, tenant, event id, and retry/dead-letter evidence.

### 26. Territory projection controls

**Justification:** Assignment and forecast rollups require territory context without direct territory-table access.

**Improvement:** Store territory projection freshness, owner mapping, region compatibility, override reason, assignment impact, and boundary evidence for territory-dependent decisions.

### 27. Billing projection controls

**Justification:** Existing customer billing health influences expansion opportunities, churn risk, and qualification.

**Improvement:** Track billing projection status, unpaid balance band, payment health, renewal timing, expansion eligibility, projection freshness, and use in scoring explanations.

### 28. Revenue policy screening

**Justification:** Pipeline rules vary by region, currency, segment, opportunity type, open opportunity count, and owner assignment.

**Improvement:** Compile deterministic policies for lead qualification, assignment, opportunity creation, stage advancement, quote handoff, win/loss, forecast inclusion, and customer updates.

### 29. Runtime parameter governance

**Justification:** Qualification thresholds, win probability, stale activity days, forecast floor, and source/segment weights materially affect pipeline outcomes.

**Improvement:** Add parameter bounds, impact simulation, approval workflow, effective dating, tenant/region overrides, rollback, and release evidence.

### 30. Schema extension governance

**Justification:** Sales teams need custom lead/opportunity fields while preserving owned boundaries and auditability.

**Improvement:** Allow extensions only on owned lead/opportunity tables with field validation, sensitivity classification, migration preview, UI binding preview, API exposure review, and release-audit evidence.

### 31. AppGen-X inbox reliability

**Justification:** Segment events directly affect lead score, assignment, and opportunity risk.

**Improvement:** Add inbox validation, idempotency, duplicate suppression, retry evidence, unsupported-event rejection, dead-letter promotion, projection rebuild, and workbench replay/quarantine controls.

### 32. AppGen-X outbox delivery assurance

**Justification:** Lead and opportunity events drive customer, quote, billing, analytics, and audit flows.

**Improvement:** Add outbox state, ordering group, payload hash, retry attempts, next retry, delivery proof, dead-letter linkage, and replay controls for emitted pipeline events.

### 33. Cross-PBC boundary proof

**Justification:** Lead Opportunity must not directly read customer, segment, billing, territory, marketing, product, quote, or finance tables.

**Improvement:** Add release evidence scanning schema descriptors, services, routes, DSL, workbench bindings, and agent plans for foreign table access, proving dependencies are APIs, events, or projections only.

### 34. Pipeline audit trail

**Justification:** Revenue audits and disputes require reconstructing lead, assignment, qualification, stage, forecast, activity, and outcome decisions.

**Improvement:** Hash-chain leads, enrichments, dedupe cases, score snapshots, assignments, qualification decisions, opportunities, activities, forecasts, handoffs, outcomes, and event deliveries.

### 35. Cryptographic pipeline proof

**Justification:** Leadership and downstream consumers may need proof of pipeline state without exposing sensitive deal details.

**Improvement:** Generate selective-disclosure proofs for qualified leads, forecast snapshots, stage history, opportunity outcome, quote handoff, and customer-update publication.

### 36. Pipeline anomaly detection

**Justification:** Abnormal pipeline patterns can indicate bad data, sandbagging, duplicate leads, assignment defects, or forecast manipulation.

**Improvement:** Detect anomalies in lead velocity, duplicate rate, score jumps, assignment skew, stage aging, close-date pushes, forecast changes, win/loss patterns, and dead-letter spikes.

### 37. Stochastic revenue exposure model

**Justification:** Pipeline risk spans deal loss, slippage, forecast miss, assignment overload, stale activity, and customer health.

**Improvement:** Model exposure by opportunity, owner, region, segment, stage, close period, amount, activity health, and projection freshness with mitigation actions.

### 38. Governed revenue model evidence

**Justification:** Lead scoring, win probability, next-best action, and forecast models influence customer treatment and revenue decisions.

**Improvement:** Track model purpose, training window, feature lineage, validation metrics, drift, fairness/segment impact, approval status, rollback, and explainability evidence.

### 39. Counterfactual pipeline simulation

**Justification:** Sales leaders need to test assignment, qualification, stage probability, and activity policies before changing live operations.

**Improvement:** Simulate thresholds, owner assignment modes, stage probabilities, stale activity rules, forecast confidence floors, and max open opportunities with pipeline and conversion effects.

### 40. Semantic sales instruction parsing

**Justification:** Sellers and managers often request pipeline updates in natural language.

**Improvement:** Parse instructions into safe query or command previews with target lead/opportunity, action, stage, amount, date, owner, reason, policy checks, and no mutation until confirmed.

### 41. Agent-safe revenue plans

**Justification:** The sales chatbot must not silently qualify leads, move stages, request quotes, or close deals.

**Improvement:** Require side-effect-free plans naming command, permission, owned tables, idempotency key, expected event, forecast impact, customer impact, rollback limits, and human confirmation.

### 42. Lead inbox workbench coverage

**Justification:** Sales operations need complete lead triage, not raw lead rows.

**Improvement:** Expand lead inbox with source, enrichment gaps, duplicate risk, score factors, assignment status, qualification decision, stale warnings, and safe actions.

### 43. Opportunity pipeline workbench coverage

**Justification:** Sellers and leaders need full deal execution visibility.

**Improvement:** Add stage board, stage history, amount, probability, close-date risk, activities, quote handoffs, forecasts, outcomes, coaching, and customer update evidence.

### 44. Forecast rollup cockpit

**Justification:** Forecast review needs explainable rollups and risk flags.

**Improvement:** Add views by owner, region, segment, stage, close period, commit/best-case/pipeline, slippage risk, stale activity, confidence, and changed-since-last-forecast.

### 45. Dedupe and enrichment console

**Justification:** Lead quality teams need focused queues for duplicates and enrichment gaps.

**Improvement:** Add queues for duplicate candidates, incomplete enrichment, stale segment projection, missing account match, invalid contact, and owner conflicts with review actions.

### 46. Continuous revenue control testing

**Justification:** Pipeline controls must run continuously across leads, opportunities, forecasts, events, and agent plans.

**Improvement:** Add assertions for opportunity without qualified lead, win without final stage, quote handoff without opportunity, stale segment scoring, duplicate lead unresolved, foreign-table access, dead-letter aging, and agent-preview bypass.

### 47. Revenue resilience drills

**Justification:** Revenue operations must degrade safely through duplicate events, projection failures, assignment conflicts, and outbox failures.

**Improvement:** Add drills for duplicate segment event, projection delay, assignment fallback, stage update conflict, quote handoff outbox failure, win event replay, and workbench degraded mode.

### 48. Customer update governance

**Justification:** Won opportunities can update customer projections and must be controlled.

**Improvement:** Gate `CustomerUpdated` on won outcome, account/customer projection freshness, amount/currency, owner approval, duplicate prevention, payload version, and delivery proof.

### 49. Lead Opportunity readiness score

**Justification:** Users need an evidence-backed view of whether `lead_opportunity` is ready for live revenue pipeline execution.

**Improvement:** Compute readiness from account hierarchy, lead capture, enrichment, dedupe, scoring, assignment, qualification, opportunities, stage history, forecasting, activities, handoffs, outcomes, event reliability, UI coverage, model governance, boundary proof, controls, and agent safety.

### 50. End-to-end revenue pipeline proof

**Justification:** A complete Lead Opportunity PBC must prove it can execute the full lifecycle from lead capture to won/lost outcome and customer update.

**Improvement:** Add an executable proof scenario covering account hierarchy, segment event intake, lead capture, enrichment, dedupe, scoring, assignment, qualification, opportunity creation, activity, stage advancement, quote handoff, forecast snapshot, win/loss outcome, emitted events, UI evidence, boundary proof, controls, and agent explanation.
