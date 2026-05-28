# Customer Success Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `customer_success_management`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.
- Representative owned tables: `customer_success_management_customer_success_account`, `customer_success_management_success_plan`, `customer_success_management_onboarding_milestone`, `customer_success_management_adoption_signal`, `customer_success_management_health_score`, `customer_success_management_health_score_component`, `customer_success_management_success_playbook`, `customer_success_management_playbook_task`, `customer_success_management_customer_escalation`, `customer_success_management_renewal_motion`, `customer_success_management_expansion_opportunity`, `customer_success_management_executive_business_review`, ...
- Representative operations/APIs: `create_success_account`, `create_success_plan`, `track_onboarding_milestone`, `ingest_adoption_signal`, `calculate_health_score`, `explain_health_component`, `launch_playbook`, `complete_playbook_task`, `open_customer_escalation`, `start_renewal_motion`, `identify_expansion_opportunity`, `prepare_executive_review`, ...
- Representative events: `SuccessAccountCreated`, `HealthScoreChanged`, `PlaybookLaunched`, `CustomerEscalationOpened`, `RenewalMotionStarted`, `ChurnRiskChanged`.
- Representative advanced capabilities: `causal health scoring`, `AI playbook recommendation`, `renewal outcome simulation`, `semantic account plan extraction`, `value realization forecasting`, `customer journey graph intelligence`.

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `customer_success_management_customer_success_account`

**Justification:** This owned table is part of the Customer Success Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.

**Improvement:** Extend `customer_success_management_customer_success_account` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `customer_success_account_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `customer_success_management_success_plan`

**Justification:** This owned table is part of the Customer Success Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.

**Improvement:** Extend `customer_success_management_success_plan` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `customer_success_management_workflow`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `customer_success_management_onboarding_milestone`

**Justification:** This owned table is part of the Customer Success Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.

**Improvement:** Extend `customer_success_management_onboarding_milestone` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `customer_success_management_analytics`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `customer_success_management_adoption_signal`

**Justification:** This owned table is part of the Customer Success Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.

**Improvement:** Extend `customer_success_management_adoption_signal` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `configuration_schema`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `customer_success_management_health_score`

**Justification:** This owned table is part of the Customer Success Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.

**Improvement:** Extend `customer_success_management_health_score` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `rule_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `customer_success_management_health_score_component`

**Justification:** This owned table is part of the Customer Success Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.

**Improvement:** Extend `customer_success_management_health_score_component` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `parameter_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `customer_success_management_success_playbook`

**Justification:** This owned table is part of the Customer Success Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.

**Improvement:** Extend `customer_success_management_success_playbook` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `owned_schema_migrations_models`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `customer_success_management_playbook_task`

**Justification:** This owned table is part of the Customer Success Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.

**Improvement:** Extend `customer_success_management_playbook_task` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `appgen_x_outbox_inbox_eventing`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `customer_success_management_customer_escalation`

**Justification:** This owned table is part of the Customer Success Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.

**Improvement:** Extend `customer_success_management_customer_escalation` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `idempotent_handlers`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `customer_success_management_renewal_motion`

**Justification:** This owned table is part of the Customer Success Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns customer success accounts, onboarding, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence.

**Improvement:** Extend `customer_success_management_renewal_motion` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `retry_dead_letter_evidence`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `create_success_account` a complete command lifecycle

**Justification:** High-value users need `create_success_account` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_success_account` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `SuccessAccountCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `create_success_plan` a complete command lifecycle

**Justification:** High-value users need `create_success_plan` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_success_plan` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `HealthScoreChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `track_onboarding_milestone` a complete command lifecycle

**Justification:** High-value users need `track_onboarding_milestone` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `track_onboarding_milestone` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PlaybookLaunched`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `ingest_adoption_signal` a complete command lifecycle

**Justification:** High-value users need `ingest_adoption_signal` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `ingest_adoption_signal` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CustomerEscalationOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `calculate_health_score` a complete command lifecycle

**Justification:** High-value users need `calculate_health_score` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `calculate_health_score` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `RenewalMotionStarted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `explain_health_component` a complete command lifecycle

**Justification:** High-value users need `explain_health_component` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `explain_health_component` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ChurnRiskChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `launch_playbook` a complete command lifecycle

**Justification:** High-value users need `launch_playbook` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `launch_playbook` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `SuccessAccountCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `complete_playbook_task` a complete command lifecycle

**Justification:** High-value users need `complete_playbook_task` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `complete_playbook_task` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `HealthScoreChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `open_customer_escalation` a complete command lifecycle

**Justification:** High-value users need `open_customer_escalation` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `open_customer_escalation` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PlaybookLaunched`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `start_renewal_motion` a complete command lifecycle

**Justification:** High-value users need `start_renewal_motion` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `start_renewal_motion` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CustomerEscalationOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `causal health scoring` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer Success Management and measurably improves customer success management risk score without hiding assumptions.

**Improvement:** Promote `causal health scoring` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_success_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `AI playbook recommendation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer Success Management and measurably improves customer success management workbench metric without hiding assumptions.

**Improvement:** Promote `AI playbook recommendation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_success_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `renewal outcome simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer Success Management and measurably improves customer success management risk score without hiding assumptions.

**Improvement:** Promote `renewal outcome simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_success_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `semantic account plan extraction` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer Success Management and measurably improves customer success management workbench metric without hiding assumptions.

**Improvement:** Promote `semantic account plan extraction` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_success_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `value realization forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer Success Management and measurably improves customer success management risk score without hiding assumptions.

**Improvement:** Promote `value realization forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_success_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `customer journey graph intelligence` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer Success Management and measurably improves customer success management workbench metric without hiding assumptions.

**Improvement:** Promote `customer journey graph intelligence` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_success_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `causal health scoring` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer Success Management and measurably improves customer success management risk score without hiding assumptions.

**Improvement:** Promote `causal health scoring` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_success_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `AI playbook recommendation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer Success Management and measurably improves customer success management workbench metric without hiding assumptions.

**Improvement:** Promote `AI playbook recommendation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_success_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `renewal outcome simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer Success Management and measurably improves customer success management risk score without hiding assumptions.

**Improvement:** Promote `renewal outcome simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_success_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic account plan extraction` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Customer Success Management and measurably improves customer success management workbench metric without hiding assumptions.

**Improvement:** Promote `semantic account plan extraction` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customer_success_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `health_score_policy` and `churn_risk_threshold`

**Justification:** Complete Customer Success Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `health_score_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `churn_risk_threshold` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `playbook_trigger_policy` and `onboarding_sla_days`

**Justification:** Complete Customer Success Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `playbook_trigger_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `onboarding_sla_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `renewal_risk_policy` and `health_warning_score`

**Justification:** Complete Customer Success Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `renewal_risk_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `health_warning_score` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `escalation_policy` and `renewal_notice_days`

**Justification:** Complete Customer Success Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `escalation_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `renewal_notice_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `value_realization_policy` and `playbook_task_sla_hours`

**Justification:** Complete Customer Success Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `value_realization_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `playbook_task_sla_hours` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `customer success workbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Customer Success Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `customer success workbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `health cockpit` into a full specialist command center

**Justification:** The PBC UI must expose the complete Customer Success Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `health cockpit` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `onboarding tracker` into a full specialist command center

**Justification:** The PBC UI must expose the complete Customer Success Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `onboarding tracker` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `playbook board` into a full specialist command center

**Justification:** The PBC UI must expose the complete Customer Success Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `playbook board` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `renewal room` into a full specialist command center

**Justification:** The PBC UI must expose the complete Customer Success Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `renewal room` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /success-accounts` and `CustomerUpdated`

**Justification:** Customer Success Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /success-accounts` and consumed event `CustomerUpdated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /health-scores` and `SubscriptionActivated`

**Justification:** Customer Success Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /health-scores` and consumed event `SubscriptionActivated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /onboarding-plans` and `TicketClosed`

**Justification:** Customer Success Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /onboarding-plans` and consumed event `TicketClosed` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /renewal-plans` and `PaymentFailed`

**Justification:** Customer Success Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /renewal-plans` and consumed event `PaymentFailed` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Customer Success Management

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Customer Success Management

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Customer Success Management

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Customer Success Management

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Customer Success Management

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Customer Success Management

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
