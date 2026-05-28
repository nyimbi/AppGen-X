# Customer 360 and Engagement Registry PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `customer_360`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Profiles, touchpoints, preferences, channel history, and customer read models.
- Representative owned tables: `customer_360_customer_profile`, `customer_360_engagement_event`, `customer_360_communication_preference`, `customer_360_touchpoint`.
- Representative operations/APIs: `command_profiles`, `command_touchpoints`, `query_customer_timeline`.
- Representative events: `CustomerUpdated`, `PreferenceChanged`.
- Representative advanced capabilities: `event_sourced_customer_lifecycle`, `graph_relational_customer_topology`, `multi_tenant_customer_isolation`, `schema_evolution_resilient_customer_schema`, `probabilistic_identity_consent_engagement_scoring`, `real_time_customer_timeline_analytics`, `counterfactual_preference_segment_simulation`, `temporal_customer_value_churn_forecasting`, `autonomous_customer_data_exception_resolution`, `semantic_customer_instruction_parsing`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `customer_360_customer_profile`

**Justification:** This owned table is part of the Customer 360 and Engagement Registry operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Profiles, touchpoints, preferences, channel history, and customer read models.

**Improvement:** Extend `customer_360_customer_profile` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `customer_profile`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `customer_360_engagement_event`

**Justification:** This owned table is part of the Customer 360 and Engagement Registry operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Profiles, touchpoints, preferences, channel history, and customer read models.

**Improvement:** Extend `customer_360_engagement_event` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `profile_versioning`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `customer_360_communication_preference`

**Justification:** This owned table is part of the Customer 360 and Engagement Registry operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Profiles, touchpoints, preferences, channel history, and customer read models.

**Improvement:** Extend `customer_360_communication_preference` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `profile_attribute_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `customer_360_touchpoint`

**Justification:** This owned table is part of the Customer 360 and Engagement Registry operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Profiles, touchpoints, preferences, channel history, and customer read models.

**Improvement:** Extend `customer_360_touchpoint` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `identity_resolution`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `customer_360_customer_profile`

**Justification:** This owned table is part of the Customer 360 and Engagement Registry operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Profiles, touchpoints, preferences, channel history, and customer read models.

**Improvement:** Extend `customer_360_customer_profile` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `identity_evidence`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `customer_360_engagement_event`

**Justification:** This owned table is part of the Customer 360 and Engagement Registry operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Profiles, touchpoints, preferences, channel history, and customer read models.

**Improvement:** Extend `customer_360_engagement_event` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `identity_match_review`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `customer_360_communication_preference`

**Justification:** This owned table is part of the Customer 360 and Engagement Registry operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Profiles, touchpoints, preferences, channel history, and customer read models.

**Improvement:** Extend `customer_360_communication_preference` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `survivorship_rules`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `customer_360_touchpoint`

**Justification:** This owned table is part of the Customer 360 and Engagement Registry operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Profiles, touchpoints, preferences, channel history, and customer read models.

**Improvement:** Extend `customer_360_touchpoint` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `relationship_graph`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `customer_360_customer_profile`

**Justification:** This owned table is part of the Customer 360 and Engagement Registry operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Profiles, touchpoints, preferences, channel history, and customer read models.

**Improvement:** Extend `customer_360_customer_profile` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `households`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `customer_360_engagement_event`

**Justification:** This owned table is part of the Customer 360 and Engagement Registry operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Profiles, touchpoints, preferences, channel history, and customer read models.

**Improvement:** Extend `customer_360_engagement_event` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `profile_merge_case`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `command_profiles` a complete command lifecycle

**Justification:** High-value users need `command_profiles` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_profiles` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CustomerUpdated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `command_touchpoints` a complete command lifecycle

**Justification:** High-value users need `command_touchpoints` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_touchpoints` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PreferenceChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Turn `query_customer_timeline` into an expert read-model experience

**Justification:** Domain experts rely on `query_customer_timeline` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_customer_timeline` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `CustomerUpdated` last changed the projection, and where uncertainty or missing data affects confidence.

### 14. Make `command_profiles` a complete command lifecycle

**Justification:** High-value users need `command_profiles` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_profiles` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PreferenceChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `command_touchpoints` a complete command lifecycle

**Justification:** High-value users need `command_touchpoints` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_touchpoints` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CustomerUpdated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Turn `query_customer_timeline` into an expert read-model experience

**Justification:** Domain experts rely on `query_customer_timeline` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_customer_timeline` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `PreferenceChanged` last changed the projection, and where uncertainty or missing data affects confidence.

### 17. Make `command_profiles` a complete command lifecycle

**Justification:** High-value users need `command_profiles` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_profiles` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CustomerUpdated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `command_touchpoints` a complete command lifecycle

**Justification:** High-value users need `command_touchpoints` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_touchpoints` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PreferenceChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Turn `query_customer_timeline` into an expert read-model experience

**Justification:** Domain experts rely on `query_customer_timeline` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_customer_timeline` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `CustomerUpdated` last changed the projection, and where uncertainty or missing data affects confidence.

### 20. Make `command_profiles` a complete command lifecycle

**Justification:** High-value users need `command_profiles` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_profiles` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PreferenceChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_customer_lifecycle` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer 360 and Engagement Registry and measurably improves conversion quality without hiding assumptions.

**Improvement:** Promote `event_sourced_customer_lifecycle` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `conversion_quality`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `graph_relational_customer_topology` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer 360 and Engagement Registry and measurably improves fulfillment accuracy without hiding assumptions.

**Improvement:** Promote `graph_relational_customer_topology` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `fulfillment_accuracy`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `multi_tenant_customer_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer 360 and Engagement Registry and measurably improves customer health without hiding assumptions.

**Improvement:** Promote `multi_tenant_customer_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_health`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `schema_evolution_resilient_customer_schema` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer 360 and Engagement Registry and measurably improves margin impact without hiding assumptions.

**Improvement:** Promote `schema_evolution_resilient_customer_schema` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `margin_impact`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `probabilistic_identity_consent_engagement_scoring` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer 360 and Engagement Registry and measurably improves customer updated throughput without hiding assumptions.

**Improvement:** Promote `probabilistic_identity_consent_engagement_scoring` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_updated_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `real_time_customer_timeline_analytics` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer 360 and Engagement Registry and measurably improves preference changed throughput without hiding assumptions.

**Improvement:** Promote `real_time_customer_timeline_analytics` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `preference_changed_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `counterfactual_preference_segment_simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer 360 and Engagement Registry and measurably improves conversion quality without hiding assumptions.

**Improvement:** Promote `counterfactual_preference_segment_simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `conversion_quality`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `temporal_customer_value_churn_forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer 360 and Engagement Registry and measurably improves fulfillment accuracy without hiding assumptions.

**Improvement:** Promote `temporal_customer_value_churn_forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `fulfillment_accuracy`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `autonomous_customer_data_exception_resolution` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer 360 and Engagement Registry and measurably improves customer health without hiding assumptions.

**Improvement:** Promote `autonomous_customer_data_exception_resolution` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_health`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic_customer_instruction_parsing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer 360 and Engagement Registry and measurably improves margin impact without hiding assumptions.

**Improvement:** Promote `semantic_customer_instruction_parsing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `margin_impact`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `CUSTOMER_360_DATABASE_URL` and `CUSTOMER_360_DATABASE_URL`

**Justification:** Complete Customer 360 and Engagement Registry coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `CUSTOMER_360_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `CUSTOMER_360_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `CUSTOMER_360_EVENT_TOPIC` and `CUSTOMER_360_EVENT_TOPIC`

**Justification:** Complete Customer 360 and Engagement Registry coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `CUSTOMER_360_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `CUSTOMER_360_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `CUSTOMER_360_RETRY_LIMIT` and `CUSTOMER_360_RETRY_LIMIT`

**Justification:** Complete Customer 360 and Engagement Registry coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `CUSTOMER_360_RETRY_LIMIT` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `CUSTOMER_360_RETRY_LIMIT` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `CUSTOMER_360_DATABASE_URL` and `CUSTOMER_360_DATABASE_URL`

**Justification:** Complete Customer 360 and Engagement Registry coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `CUSTOMER_360_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `CUSTOMER_360_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `CUSTOMER_360_EVENT_TOPIC` and `CUSTOMER_360_EVENT_TOPIC`

**Justification:** Complete Customer 360 and Engagement Registry coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `CUSTOMER_360_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `CUSTOMER_360_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `Customer360Workbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Customer 360 and Engagement Registry surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `Customer360Workbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `Customer360Detail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Customer 360 and Engagement Registry surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `Customer360Detail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `Customer360Workbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Customer 360 and Engagement Registry surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `Customer360Workbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `Customer360Detail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Customer 360 and Engagement Registry surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `Customer360Detail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `Customer360Workbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Customer 360 and Engagement Registry surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `Customer360Workbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /profiles` and `InvoiceIssued`

**Justification:** Customer 360 and Engagement Registry must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /profiles` and consumed event `InvoiceIssued` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /touchpoints` and `PaymentCaptured`

**Justification:** Customer 360 and Engagement Registry must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /touchpoints` and consumed event `PaymentCaptured` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `GET /customer-timeline` and `CandidateHired`

**Justification:** Customer 360 and Engagement Registry must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `GET /customer-timeline` and consumed event `CandidateHired` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /profiles` and `InvoiceIssued`

**Justification:** Customer 360 and Engagement Registry must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /profiles` and consumed event `InvoiceIssued` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Customer 360 and Engagement Registry

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Customer 360 and Engagement Registry

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Customer 360 and Engagement Registry

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Customer 360 and Engagement Registry

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Customer 360 and Engagement Registry

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Customer 360 and Engagement Registry

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
