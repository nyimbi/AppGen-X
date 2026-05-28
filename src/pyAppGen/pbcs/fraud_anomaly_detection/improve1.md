# Anomalous Activity and Fraud Detection PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `fraud_anomaly_detection`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.
- Representative owned tables: `fraud_anomaly_detection_risk_signal`, `fraud_anomaly_detection_anomaly_score`, `fraud_anomaly_detection_fraud_rule`, `fraud_anomaly_detection_risk_case`, `fraud_anomaly_detection_identity_link`, `fraud_anomaly_detection_behavior_baseline`, `fraud_anomaly_detection_device_fingerprint`, `fraud_anomaly_detection_network_indicator`, `fraud_anomaly_detection_velocity_window`, `fraud_anomaly_detection_decision_explanation`, `fraud_anomaly_detection_loss_exposure`, `fraud_anomaly_detection_analyst_queue_item`, ...
- Representative operations/APIs: `configure_runtime`, `set_parameter`, `register_rule`, `register_schema_extension`, `register_fraud_rule`, `ingest_risk_signal`, `score_anomaly`, `open_risk_case`, `receive_event`, `build_workbench_view`.
- Representative events: `FraudRiskScored`, `RiskCaseOpened`.
- Representative advanced capabilities: `event_sourced_risk_signal_lifecycle`, `owned_fraud_schema_boundary`, `multi_tenant_risk_isolation`, `schema_evolution_resilient_risk_context`, `checkout_and_payment_event_ingestion`, `access_policy_change_intelligence`, `behavior_baseline_anomaly_scoring`, `fraud_rule_compilation_and_execution`, `risk_case_management_and_escalation`, `graph_identity_link_analysis`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `fraud_anomaly_detection_risk_signal`

**Justification:** This owned table is part of the Anomalous Activity and Fraud Detection operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.

**Improvement:** Extend `fraud_anomaly_detection_risk_signal` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `risk_signal_ingestion`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `fraud_anomaly_detection_anomaly_score`

**Justification:** This owned table is part of the Anomalous Activity and Fraud Detection operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.

**Improvement:** Extend `fraud_anomaly_detection_anomaly_score` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `anomaly_scoring`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `fraud_anomaly_detection_fraud_rule`

**Justification:** This owned table is part of the Anomalous Activity and Fraud Detection operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.

**Improvement:** Extend `fraud_anomaly_detection_fraud_rule` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `fraud_rule_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `fraud_anomaly_detection_risk_case`

**Justification:** This owned table is part of the Anomalous Activity and Fraud Detection operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.

**Improvement:** Extend `fraud_anomaly_detection_risk_case` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `risk_case_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `fraud_anomaly_detection_identity_link`

**Justification:** This owned table is part of the Anomalous Activity and Fraud Detection operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.

**Improvement:** Extend `fraud_anomaly_detection_identity_link` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `checkout_projection`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `fraud_anomaly_detection_behavior_baseline`

**Justification:** This owned table is part of the Anomalous Activity and Fraud Detection operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.

**Improvement:** Extend `fraud_anomaly_detection_behavior_baseline` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `payment_projection`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `fraud_anomaly_detection_device_fingerprint`

**Justification:** This owned table is part of the Anomalous Activity and Fraud Detection operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.

**Improvement:** Extend `fraud_anomaly_detection_device_fingerprint` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `access_policy_projection`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `fraud_anomaly_detection_network_indicator`

**Justification:** This owned table is part of the Anomalous Activity and Fraud Detection operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.

**Improvement:** Extend `fraud_anomaly_detection_network_indicator` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `identity_link_analysis`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `fraud_anomaly_detection_velocity_window`

**Justification:** This owned table is part of the Anomalous Activity and Fraud Detection operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.

**Improvement:** Extend `fraud_anomaly_detection_velocity_window` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `velocity_checks`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `fraud_anomaly_detection_decision_explanation`

**Justification:** This owned table is part of the Anomalous Activity and Fraud Detection operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Behavior baselines, identity graph risk, anomaly scores, fraud rules, decision explanations, loss exposure, analyst queues, and operational risk flags for checkout, payment, and access-policy activity.

**Improvement:** Extend `fraud_anomaly_detection_decision_explanation` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `device_and_network_indicators`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `configure_runtime` a complete command lifecycle

**Justification:** High-value users need `configure_runtime` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `configure_runtime` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `FraudRiskScored`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `set_parameter` a complete command lifecycle

**Justification:** High-value users need `set_parameter` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `set_parameter` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `RiskCaseOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `register_rule` a complete command lifecycle

**Justification:** High-value users need `register_rule` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `register_rule` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `FraudRiskScored`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `register_schema_extension` a complete command lifecycle

**Justification:** High-value users need `register_schema_extension` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `register_schema_extension` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `RiskCaseOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `register_fraud_rule` a complete command lifecycle

**Justification:** High-value users need `register_fraud_rule` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `register_fraud_rule` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `FraudRiskScored`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `ingest_risk_signal` a complete command lifecycle

**Justification:** High-value users need `ingest_risk_signal` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `ingest_risk_signal` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `RiskCaseOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `score_anomaly` a complete command lifecycle

**Justification:** High-value users need `score_anomaly` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `score_anomaly` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `FraudRiskScored`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `open_risk_case` a complete command lifecycle

**Justification:** High-value users need `open_risk_case` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `open_risk_case` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `RiskCaseOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `receive_event` a complete command lifecycle

**Justification:** High-value users need `receive_event` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `receive_event` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `FraudRiskScored`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `build_workbench_view` a complete command lifecycle

**Justification:** High-value users need `build_workbench_view` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `build_workbench_view` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `RiskCaseOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_risk_signal_lifecycle` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Anomalous Activity and Fraud Detection and measurably improves risk precision without hiding assumptions.

**Improvement:** Promote `event_sourced_risk_signal_lifecycle` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `risk_precision`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `owned_fraud_schema_boundary` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Anomalous Activity and Fraud Detection and measurably improves risk recall without hiding assumptions.

**Improvement:** Promote `owned_fraud_schema_boundary` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `risk_recall`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `multi_tenant_risk_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Anomalous Activity and Fraud Detection and measurably improves case open rate without hiding assumptions.

**Improvement:** Promote `multi_tenant_risk_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `case_open_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `schema_evolution_resilient_risk_context` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Anomalous Activity and Fraud Detection and measurably improves false positive rate without hiding assumptions.

**Improvement:** Promote `schema_evolution_resilient_risk_context` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `false_positive_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `checkout_and_payment_event_ingestion` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Anomalous Activity and Fraud Detection and measurably improves decision latency without hiding assumptions.

**Improvement:** Promote `checkout_and_payment_event_ingestion` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `decision_latency`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `access_policy_change_intelligence` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Anomalous Activity and Fraud Detection and measurably improves loss exposure without hiding assumptions.

**Improvement:** Promote `access_policy_change_intelligence` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `loss_exposure`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `behavior_baseline_anomaly_scoring` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Anomalous Activity and Fraud Detection and measurably improves drift score without hiding assumptions.

**Improvement:** Promote `behavior_baseline_anomaly_scoring` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `drift_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `fraud_rule_compilation_and_execution` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Anomalous Activity and Fraud Detection and measurably improves identity link density without hiding assumptions.

**Improvement:** Promote `fraud_rule_compilation_and_execution` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `identity_link_density`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `risk_case_management_and_escalation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Anomalous Activity and Fraud Detection and measurably improves velocity alert rate without hiding assumptions.

**Improvement:** Promote `risk_case_management_and_escalation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `velocity_alert_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `graph_identity_link_analysis` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Anomalous Activity and Fraud Detection and measurably improves fraud risk scored throughput without hiding assumptions.

**Improvement:** Promote `graph_identity_link_analysis` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `fraud_risk_scored_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `database_backend` and `database_backend`

**Justification:** Complete Anomalous Activity and Fraud Detection coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `database_backend` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `database_backend` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `event_topic` and `event_topic`

**Justification:** Complete Anomalous Activity and Fraud Detection coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `event_topic` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `event_topic` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `retry_limit` and `retry_limit`

**Justification:** Complete Anomalous Activity and Fraud Detection coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `retry_limit` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `retry_limit` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `default_region` and `default_region`

**Justification:** Complete Anomalous Activity and Fraud Detection coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `default_region` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `default_region` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `supported_regions` and `supported_regions`

**Justification:** Complete Anomalous Activity and Fraud Detection coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `supported_regions` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `supported_regions` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `FraudAnomalyDetectionWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Anomalous Activity and Fraud Detection surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `FraudAnomalyDetectionWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `RiskSignalMonitor` into a full specialist command center

**Justification:** The PBC UI must expose the complete Anomalous Activity and Fraud Detection surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `RiskSignalMonitor` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `AnomalyScoreBoard` into a full specialist command center

**Justification:** The PBC UI must expose the complete Anomalous Activity and Fraud Detection surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `AnomalyScoreBoard` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `FraudRuleStudio` into a full specialist command center

**Justification:** The PBC UI must expose the complete Anomalous Activity and Fraud Detection surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `FraudRuleStudio` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `RiskCaseConsole` into a full specialist command center

**Justification:** The PBC UI must expose the complete Anomalous Activity and Fraud Detection surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `RiskCaseConsole` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /risk-events` and `CheckoutCompleted`

**Justification:** Anomalous Activity and Fraud Detection must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /risk-events` and consumed event `CheckoutCompleted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /fraud-checks` and `PaymentCaptured`

**Justification:** Anomalous Activity and Fraud Detection must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /fraud-checks` and consumed event `PaymentCaptured` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `GET /risk-cases` and `AccessPolicyChanged`

**Justification:** Anomalous Activity and Fraud Detection must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `GET /risk-cases` and consumed event `AccessPolicyChanged` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `GET /risk-workbench` and `CheckoutCompleted`

**Justification:** Anomalous Activity and Fraud Detection must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `GET /risk-workbench` and consumed event `CheckoutCompleted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Anomalous Activity and Fraud Detection

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Anomalous Activity and Fraud Detection

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Anomalous Activity and Fraud Detection

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Anomalous Activity and Fraud Detection

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Anomalous Activity and Fraud Detection

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Anomalous Activity and Fraud Detection

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
