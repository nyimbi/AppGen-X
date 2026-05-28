# Customer 360 and Engagement Registry PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `customer_360`. The items are specific to customer data management: unified profiles, identities, account/contact relationships, consent, communication preferences, touchpoints, engagement events, timelines, segmentation projections, merge evidence, privacy controls, customer value and health signals, event reliability, workbench coverage, and agent-assisted customer operations.

## Current Domain Evidence Used

- Domain purpose: unified customer profile and engagement registry for customer identities, profile attributes, account and contact relationships, consent, communication preferences, touchpoints, engagement events, customer timelines, lifecycle state, loyalty and service signals, segmentation projections, merge evidence, privacy controls, rules, parameters, configuration, and workbench fragments.
- Owned boundary: customer profiles, identities, relationships, engagement events, communication preferences, touchpoints, consent records, timelines, segment projections, profile merge cases, rules, parameters, configuration, inbox/outbox, and dead-letter evidence; generated schema evidence also covers identity evidence, survivorship, households, value snapshots, health signals, churn forecasts, exception remediation, cryptographic proofs, policy screenings, controls, federation views, resilience drills, crypto epochs, carbon windows, optimization artifacts, anomaly signals, exposure forecasts, governed models, and seed data.
- Existing command/query surface: profile creation, identity linking, consent recording, preference updates, touchpoint capture, engagement ingestion, merge case open/resolve, AppGen-X inbox handling, timeline queries, workbench, schema extensions, rules, parameters, configuration, boundary checks, UI contracts, and release evidence.
- Existing events and dependencies: emits `CustomerUpdated`, `CustomerIdentityLinked`, `PreferenceChanged`, `ConsentRecorded`, `TouchpointCaptured`, `CustomerSegmentUpdated`, `ProfileMergeCaseOpened`, and `ProfileMergeResolved`; consumes billing, payment, order, service, loyalty, and hiring events through declared APIs/projections only.

## 50 Better-Than-World-Class Improvements

### 1. Customer profile identity spine

**Justification:** A Customer 360 profile must anchor all downstream engagement, service, order, billing, loyalty, notification, and analytics projections without duplicating customers.

**Improvement:** Add an identity spine with stable profile ID, tenant/entity, lifecycle state, source lineage, primary identity, confidence, profile type, effective dates, and immutable creation evidence. Every update should preserve source and survivorship decisions.

### 2. Profile lifecycle state machine

**Justification:** Customer records move through prospect, active, dormant, restricted, deleted, anonymized, merged, and archived states with different legal and operational effects.

**Improvement:** Implement lifecycle transitions with allowed commands, permissions, reasons, consent impact, retention effect, emitted events, and audit trace. Block engagement actions when lifecycle state forbids them.

### 3. Profile attribute governance

**Justification:** Demographic, firmographic, household, value, and service attributes have different provenance, sensitivity, and survivorship requirements.

**Improvement:** Model attributes with source, confidence, verified/unverified status, sensitivity, effective dates, jurisdiction, retention class, and survivorship priority. UI should distinguish owned values, projections, and inferred values.

### 4. Identity resolution evidence model

**Justification:** Linking email, phone, device, external IDs, loyalty IDs, and verified credentials without evidence creates privacy and service risks.

**Improvement:** Store identity evidence with type, normalized value, verifier, confidence, source event, expiry, consent basis, conflict status, and match rationale. Identity links should be explainable and reversible through merge governance.

### 5. Probabilistic identity matching

**Justification:** Customer identity is often uncertain because of shared devices, reused phones, misspellings, family accounts, and stale external IDs.

**Improvement:** Add probabilistic matching with thresholds, feature explanations, candidate profiles, false-positive risk, false-negative risk, and review queues. Auto-link only above policy confidence and route ambiguous matches to humans.

### 6. Duplicate detection and merge case workflow

**Justification:** Duplicate profiles fragment consent, preferences, orders, service context, value metrics, and customer experience.

**Improvement:** Add merge cases with candidate profiles, evidence, survivorship proposal, affected identities, consent conflicts, relationship impact, downstream event effects, approver, decision, rollback constraints, and emitted `ProfileMergeResolved` evidence.

### 7. Survivorship rule compiler

**Justification:** Profile merges and updates need deterministic rules for which data wins under conflicts.

**Improvement:** Compile survivorship rules by attribute type, source trust, recency, verification, consent, jurisdiction, and manual override. Store rule hash and show field-level survivorship explanations during merge.

### 8. Account, household, and contact relationship graph

**Justification:** Customer understanding requires relationships: households, businesses, contacts, dependents, employees, agents, billing accounts, and service accounts.

**Improvement:** Model relationship types, direction, role, authority, effective dates, confidence, privacy constraints, and allowed use cases. Timeline and workbench views should show relationship context without leaking restricted data.

### 9. Consent record lifecycle

**Justification:** Consent must be specific, provable, revocable, jurisdiction-aware, and linked to channel and purpose.

**Improvement:** Model consent with purpose, channel, lawful basis, jurisdiction, capture source, evidence, timestamp, expiry, withdrawal, versioned language, and downstream eligibility. Emit `ConsentRecorded` with idempotent evidence.

### 10. Communication preference center

**Justification:** Preferences are not simple flags; they combine opt-in/out, channel, topic, frequency, quiet hours, language, and legal constraints.

**Improvement:** Add preference records for channel, topic, frequency, locale, quiet hours, priority, jurisdiction, consent dependency, source, and effective dates. Preference changes should emit `PreferenceChanged` and update timeline projections.

### 11. Privacy policy screening

**Justification:** Customer actions must comply with consent, jurisdiction, retention, lifecycle state, sensitivity, and purpose limits.

**Improvement:** Screen profile updates, identity links, consent changes, touchpoint capture, engagement ingestion, merge resolution, segment projection, and export actions. Store policy version, attributes evaluated, decision, explanation, and override path.

### 12. Data subject request workflow

**Justification:** Customers may request access, correction, deletion, restriction, portability, or opt-out, and those requests need governed handling.

**Improvement:** Add request lifecycle with identity verification, request type, scope, jurisdiction, due date, impacted records, allowed actions, proof package, exception reasons, and completion evidence.

### 13. Touchpoint capture normalization

**Justification:** Touchpoints from web, mobile, store, email, service, order, payment, support, and field channels have inconsistent metadata.

**Improvement:** Normalize touchpoints with channel, journey stage, device/source, location granularity, actor, purpose, timestamp confidence, consent applicability, and source payload hash. Reject or quarantine touchpoints that violate policy.

### 14. Engagement event ingestion taxonomy

**Justification:** Engagement events drive timeline, segmentation, value, and churn, so event semantics must be precise.

**Improvement:** Define event types, channel, direction, intent, sentiment, outcome, campaign/service/order reference projection, source trust, timestamp, deduplication key, and replay behavior. Unsupported events should create retry/dead-letter evidence.

### 15. Customer timeline reconstruction

**Justification:** Customer-facing teams need a chronological, explainable view of profile, consent, preference, engagement, order, billing, service, and loyalty context.

**Improvement:** Build timeline read models with source, event type, projection freshness, sensitivity filters, relationship context, actor, confidence, and redaction rules. Support as-of timeline reconstruction for audits and disputes.

### 16. Recency, frequency, and value metrics

**Justification:** Customer value and engagement health need consistent operational metrics derived from events and projections.

**Improvement:** Add RFM metrics with calculation window, source projections, currency/value assumptions, channel filters, confidence, and stale-state warnings. Store metric versions so segments and decisions can be reproduced.

### 17. Customer health signal model

**Justification:** Service, payment, order, loyalty, and engagement events reveal satisfaction, churn, retention, and support risk.

**Improvement:** Compute health signals from service closures, order verification, payment capture, loyalty earn, engagement decay, sentiment, complaints, and lifecycle state. Provide reason codes and recommended follow-up actions.

### 18. Churn and engagement forecasting

**Justification:** Customer teams need proactive retention signals instead of only historical timelines.

**Improvement:** Forecast churn and engagement decline by segment, channel, lifecycle, value tier, recent events, service outcomes, and preference constraints. Include confidence, drift, feature lineage, and recommended interventions.

### 19. Segment projection governance

**Justification:** Segment membership affects campaigns, personalization, service, eligibility, and analytics, so stale or opaque segments are risky.

**Improvement:** Store segment projections with source, rule/model version, membership confidence, effective dates, purpose, consent dependency, exclusion reason, and freshness. Emit `CustomerSegmentUpdated` when owned segment evidence changes.

### 20. Counterfactual segmentation simulation

**Justification:** Teams need to understand who would enter or leave a segment before changing rules.

**Improvement:** Simulate segment and preference rule changes against current profiles, showing membership deltas, consent blockers, channel reach, value impact, privacy risk, and workload without mutating state.

### 21. Customer value snapshot

**Justification:** Value is temporal and cross-domain; Customer 360 should provide a governed read model without owning billing or order tables.

**Improvement:** Build value snapshots from declared billing, payment, order, and loyalty projections with freshness, window, currency, value type, confidence, and exclusions. Mark projections distinctly from owned profile facts.

### 22. Service and loyalty signal integration

**Justification:** Customer experience depends on service outcomes and loyalty activity as much as profile data.

**Improvement:** Project `ServiceTicketClosed` and `LoyaltyRewardEarned` events into service satisfaction, issue resolution, loyalty engagement, reward recency, and health signals. Preserve event lineage and stale projection warnings.

### 23. Candidate-to-customer continuity

**Justification:** Hiring or candidate events may create relationships that later affect customer or employee-facing contexts.

**Improvement:** Ingest `CandidateHired` as a bounded projection with identity confidence, relationship type, privacy scope, and allowed downstream use. Prevent inappropriate marketing or service use when purpose is restricted.

### 24. Preference conflict resolution

**Justification:** Preferences can conflict across channels, topics, jurisdictions, accounts, households, and source systems.

**Improvement:** Add conflict detection, precedence rules, human review, source trust, customer-confirmation requirement, and effective communication eligibility. Timeline should show why a preference wins.

### 25. Consent confidence scoring

**Justification:** Old, imported, ambiguous, or unsupported consent evidence may not be safe enough for customer actions.

**Improvement:** Score consent confidence from evidence quality, source, language version, age, jurisdiction, capture method, identity match confidence, and withdrawal history. Block actions below `minimum_consent_confidence`.

### 26. Customer communication eligibility view

**Justification:** Notifications and engagement packages need a safe customer-facing eligibility projection.

**Improvement:** Produce eligibility read models by profile, channel, topic, purpose, locale, quiet hours, preference, consent, lifecycle state, and policy result. Keep notifications integration projection-based.

### 27. Engagement attribution lineage

**Justification:** Engagement events often originate from campaigns, service cases, orders, support sessions, and loyalty actions, and attribution affects value analysis.

**Improvement:** Track attribution source, campaign/service/order projection reference, first/last-touch semantics, confidence, and channel contribution. Analytics should cite attribution lineage.

### 28. Sentiment and intent enrichment governance

**Justification:** Sentiment and intent are useful but uncertain, subjective, and sensitive.

**Improvement:** Store sentiment/intent with model version, source text reference, confidence, reviewer override, sensitivity flag, and allowed use. Avoid using low-confidence sentiment for automated adverse decisions.

### 29. Customer anomaly detection

**Justification:** Sudden profile changes, identity churn, preference flips, event spikes, and value drops can indicate fraud, integration defects, or privacy issues.

**Improvement:** Detect anomalies in identities, profile attributes, consent changes, touchpoints, engagement frequency, segment membership, merge cases, and projection updates. Route anomalies to review with explanations.

### 30. Stochastic customer exposure model

**Justification:** Customer risk spans churn, privacy, consent, engagement, value, service dissatisfaction, merge uncertainty, and projection staleness.

**Improvement:** Model exposure distributions by profile, segment, channel, lifecycle, region, and relationship graph. Provide mitigation suggestions and confidence, not binary labels.

### 31. Customer MLOps governance

**Justification:** Identity, churn, health, sentiment, segmentation, and anomaly models affect customer treatment and fairness.

**Improvement:** Add governed model evidence with feature lineage, training windows, approval status, explainability, drift monitoring, fairness checks, rollback, and release evidence for every customer model.

### 32. Cryptographic customer proof

**Justification:** Internal or external parties may need proof of consent, preference, identity link, or merge decision without seeing sensitive profile data.

**Improvement:** Generate redacted proofs for consent, preference, identity evidence, merge decisions, and timeline snapshots with hash, policy version, timestamp, and verification API.

### 33. Immutable customer audit trace

**Justification:** Customer profile and consent changes are high-risk and must be reconstructable.

**Improvement:** Hash-chain profile updates, identity links, consent changes, preference changes, touchpoints, engagement ingestion, merge cases, rule changes, agent previews, and event handling. Support temporal audit in the workbench.

### 34. AppGen-X event reliability cockpit

**Justification:** Customer 360 relies on consumed billing, payment, order, service, loyalty, and hiring events plus emitted customer lifecycle events.

**Improvement:** Add inbox/outbox/dead-letter views for idempotency, duplicates, retries, handler version, payload lineage, projection freshness, replay eligibility, and downstream event effects. Warn when stale projections affect timeline or eligibility.

### 35. Boundary proof for customer ownership

**Justification:** Customer 360 must integrate with order, billing, service, loyalty, notifications, identity, audit, and analytics without shared tables.

**Improvement:** Add static/runtime checks proving commands touch only Customer 360-owned tables plus AppGen-X runtime tables. Include failing fixtures for direct order, billing, service, loyalty, notification, and analytics table access.

### 36. Multi-tenant and regional privacy isolation

**Justification:** Customer data is sensitive and subject to tenant, entity, region, jurisdiction, and purpose constraints.

**Improvement:** Enforce isolation in profiles, identities, consents, preferences, touchpoints, timelines, segments, merge cases, events, UI filters, saved views, and agent previews with release evidence.

### 37. Schema extension governance for profiles

**Justification:** Customer attributes vary by industry, but uncontrolled extensions create privacy and integration risk.

**Improvement:** Require extension metadata for owned table, field name, sensitivity, purpose, retention, allowed regions, validation, and UI exposure. Reject malformed names and foreign table extensions.

### 38. Customer workbench coverage

**Justification:** Operators, analysts, and auditors need the full Customer 360 surface in UI, not only backend commands.

**Improvement:** Expand UI into profile registry, identity resolution, relationship graph, consent center, preference center, touchpoint capture, engagement ingestion, timeline, merge review, segment dashboard, value/health views, privacy requests, anomalies, controls, rules, parameters, configuration, events, and agent panels.

### 39. Agent-safe customer document intake

**Justification:** The Customer 360 chatbot should parse contact-center notes, preference instructions, consent forms, profile updates, and merge evidence without unsafe writes.

**Improvement:** Add intake skills that extract candidate customer facts, map them to owned tables, validate rules/permissions/privacy, reject foreign-table mutations, and produce side-effect-free previews with confidence, risks, confirmations, and expected AppGen-X events.

### 40. Agent-safe profile and consent actions

**Justification:** AI assistance around customer data can create privacy violations if it mutates records without controls.

**Improvement:** Require agent plans for profile updates, identity links, consent records, preference changes, touchpoint capture, merge resolution, and data subject requests to list command, permission, owned tables, idempotency key, emitted event, privacy basis, rollback limits, and human approval.

### 41. Customer federation views

**Justification:** Business users need a unified view enriched with order, billing, service, loyalty, notification, and analytics signals without shared datastore access.

**Improvement:** Build federated views using declared projections with freshness, source event, confidence, purpose limit, and boundary evidence. UI should mark projected data distinctly from Customer 360-owned data.

### 42. Channel allocation optimization

**Justification:** Engagement channels should be allocated based on consent, preference, value, urgency, fatigue, and fairness.

**Improvement:** Add optimization for next-best eligible channel with frequency caps, quiet hours, consent confidence, expected value, customer fatigue, service urgency, and fairness constraints. Keep execution in downstream communication packages.

### 43. Carbon-aware customer processing

**Justification:** Large customer workloads, batch enrichment, and analytics can have operational energy impact.

**Improvement:** Add carbon-aware scheduling windows for non-urgent enrichment, segmentation rebuilds, embedding generation, and analytics refresh while preserving urgent consent/privacy actions.

### 44. Rule and parameter simulation

**Justification:** Changing identity thresholds, churn thresholds, consent confidence, engagement decay, or retention periods materially changes customer operations.

**Improvement:** Simulate changes against current and historical profiles, showing match changes, merge workload, consent eligibility, segment deltas, churn alerts, retention actions, dead-letter volume, and privacy risk.

### 45. Data retention and minimization controls

**Justification:** Customer 360 must retain enough history for service and audit while minimizing unnecessary personal data.

**Improvement:** Add retention schedules by record type, purpose, jurisdiction, consent, lifecycle state, legal hold, and anonymization policy. Workbench should show records approaching purge or anonymization.

### 46. Resilience drills for customer data routes

**Justification:** Customer projections and events can arrive late, duplicate, malformed, or unavailable.

**Improvement:** Add drills for duplicate events, unsupported events, dead-letter replay, projection outage, identity conflict, consent withdrawal during processing, and merge rollback. Store drill evidence in release gates.

### 47. Continuous customer control testing

**Justification:** Customer controls should run continuously across identity, consent, preferences, privacy, merges, timelines, and event handling.

**Improvement:** Add assertions for low-confidence identity auto-link, missing consent evidence, preference conflict, restricted lifecycle engagement, cross-tenant leakage, stale projection use, merge without approval, dead-letter aging, and agent-preview bypass.

### 48. Customer timeline quality score

**Justification:** A timeline can look complete while missing key sources, stale projections, or sensitive redactions.

**Improvement:** Score timeline quality from source coverage, projection freshness, event ordering, deduplication, consent filtering, redaction completeness, relationship context, and unresolved exceptions. Show gaps by profile.

### 49. Customer 360 readiness score

**Justification:** Users need an evidence-backed view of whether Customer 360 is ready for production customer operations.

**Improvement:** Compute readiness from profile schema, identity confidence, consent policy, preferences, touchpoint coverage, timeline quality, merge governance, privacy workflows, event reliability, UI coverage, boundary proof, control assertions, model governance, and agent safety.

### 50. End-to-end customer profile proof

**Justification:** A complete Customer 360 PBC must prove it can manage the full customer lifecycle with privacy and boundary controls.

**Improvement:** Add an executable proof scenario covering profile creation, identity link, consent record, preference change, touchpoint capture, engagement ingestion, timeline projection, merge review, segment update, emitted events, privacy proof, UI evidence, controls, and agent explanation.
