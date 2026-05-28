# Compensation and Payroll Engine PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `payroll_engine`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.
- Representative owned tables: `payroll_engine_payroll_calendar`, `payroll_engine_payroll_period`, `payroll_engine_payroll_pay_group`, `payroll_engine_payroll_legal_entity`, `payroll_engine_payroll_run`, `payroll_engine_payroll_run_worker`, `payroll_engine_payroll_run_approval`, `payroll_engine_payroll_run_lock`, `payroll_engine_worker_projection`, `payroll_engine_worker_pay_profile`, `payroll_engine_worker_bank_instruction`, `payroll_engine_labor_hours`, ...
- Representative operations/APIs: `command_payroll_runs`, `command_payroll_runs_id_workers`, `command_payroll_runs_id_payslips`, `command_payslips_id_deductions`, `command_payslips_id_benefits`, `command_payroll_runs_id_post`, `command_payroll_filings`, `command_payroll_events_inbox`, `command_payroll_rules`, `command_payroll_parameters`, `command_payroll_configuration`, `query_payslips`, ...
- Representative events: `PayrollPosted`, `PayrollFilingPrepared`.
- Representative advanced capabilities: `event_sourced_payroll_lifecycle`, `graph_relational_compensation_topology`, `multi_tenant_payroll_isolation`, `schema_evolution_resilient_payroll_schema`, `probabilistic_payroll_anomaly_compliance_scoring`, `real_time_gross_to_net_analytics`, `counterfactual_pay_policy_simulation`, `temporal_payroll_cash_forecasting`, `autonomous_payroll_exception_resolution`, `semantic_payroll_instruction_parsing`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `payroll_engine_payroll_calendar`

**Justification:** This owned table is part of the Compensation and Payroll Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.

**Improvement:** Extend `payroll_engine_payroll_calendar` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `payroll_calendar`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `payroll_engine_payroll_period`

**Justification:** This owned table is part of the Compensation and Payroll Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.

**Improvement:** Extend `payroll_engine_payroll_period` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `payroll_period`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `payroll_engine_payroll_pay_group`

**Justification:** This owned table is part of the Compensation and Payroll Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.

**Improvement:** Extend `payroll_engine_payroll_pay_group` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `pay_group_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `payroll_engine_payroll_legal_entity`

**Justification:** This owned table is part of the Compensation and Payroll Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.

**Improvement:** Extend `payroll_engine_payroll_legal_entity` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `legal_entity_payroll`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `payroll_engine_payroll_run`

**Justification:** This owned table is part of the Compensation and Payroll Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.

**Improvement:** Extend `payroll_engine_payroll_run` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `payroll_run_creation`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `payroll_engine_payroll_run_worker`

**Justification:** This owned table is part of the Compensation and Payroll Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.

**Improvement:** Extend `payroll_engine_payroll_run_worker` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `payroll_run_worker_roster`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `payroll_engine_payroll_run_approval`

**Justification:** This owned table is part of the Compensation and Payroll Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.

**Improvement:** Extend `payroll_engine_payroll_run_approval` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `payroll_run_approval`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `payroll_engine_payroll_run_lock`

**Justification:** This owned table is part of the Compensation and Payroll Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.

**Improvement:** Extend `payroll_engine_payroll_run_lock` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `payroll_run_lock`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `payroll_engine_worker_projection`

**Justification:** This owned table is part of the Compensation and Payroll Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.

**Improvement:** Extend `payroll_engine_worker_projection` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `worker_projection`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `payroll_engine_worker_pay_profile`

**Justification:** This owned table is part of the Compensation and Payroll Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Gross-to-net payroll, worker pay profiles, earnings, deductions, benefits, filings, payment and journal handoffs, corrections, controls, and payroll-risk evidence.

**Improvement:** Extend `payroll_engine_worker_pay_profile` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `worker_pay_profile`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `command_payroll_runs` a complete command lifecycle

**Justification:** High-value users need `command_payroll_runs` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_payroll_runs` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PayrollPosted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `command_payroll_runs_id_workers` a complete command lifecycle

**Justification:** High-value users need `command_payroll_runs_id_workers` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_payroll_runs_id_workers` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PayrollFilingPrepared`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `command_payroll_runs_id_payslips` a complete command lifecycle

**Justification:** High-value users need `command_payroll_runs_id_payslips` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_payroll_runs_id_payslips` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PayrollPosted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `command_payslips_id_deductions` a complete command lifecycle

**Justification:** High-value users need `command_payslips_id_deductions` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_payslips_id_deductions` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PayrollFilingPrepared`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `command_payslips_id_benefits` a complete command lifecycle

**Justification:** High-value users need `command_payslips_id_benefits` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_payslips_id_benefits` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PayrollPosted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `command_payroll_runs_id_post` a complete command lifecycle

**Justification:** High-value users need `command_payroll_runs_id_post` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_payroll_runs_id_post` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PayrollFilingPrepared`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `command_payroll_filings` a complete command lifecycle

**Justification:** High-value users need `command_payroll_filings` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_payroll_filings` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PayrollPosted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `command_payroll_events_inbox` a complete command lifecycle

**Justification:** High-value users need `command_payroll_events_inbox` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_payroll_events_inbox` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PayrollFilingPrepared`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `command_payroll_rules` a complete command lifecycle

**Justification:** High-value users need `command_payroll_rules` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_payroll_rules` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PayrollPosted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `command_payroll_parameters` a complete command lifecycle

**Justification:** High-value users need `command_payroll_parameters` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_payroll_parameters` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PayrollFilingPrepared`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_payroll_lifecycle` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Compensation and Payroll Engine and measurably improves cycle time without hiding assumptions.

**Improvement:** Promote `event_sourced_payroll_lifecycle` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `graph_relational_compensation_topology` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Compensation and Payroll Engine and measurably improves policy exceptions without hiding assumptions.

**Improvement:** Promote `graph_relational_compensation_topology` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `policy_exceptions`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `multi_tenant_payroll_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Compensation and Payroll Engine and measurably improves pay accuracy without hiding assumptions.

**Improvement:** Promote `multi_tenant_payroll_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `pay_accuracy`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `schema_evolution_resilient_payroll_schema` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Compensation and Payroll Engine and measurably improves workforce readiness without hiding assumptions.

**Improvement:** Promote `schema_evolution_resilient_payroll_schema` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `workforce_readiness`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `probabilistic_payroll_anomaly_compliance_scoring` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Compensation and Payroll Engine and measurably improves payroll posted throughput without hiding assumptions.

**Improvement:** Promote `probabilistic_payroll_anomaly_compliance_scoring` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `payroll_posted_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `real_time_gross_to_net_analytics` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Compensation and Payroll Engine and measurably improves payroll filing prepared throughput without hiding assumptions.

**Improvement:** Promote `real_time_gross_to_net_analytics` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `payroll_filing_prepared_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `counterfactual_pay_policy_simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Compensation and Payroll Engine and measurably improves cycle time without hiding assumptions.

**Improvement:** Promote `counterfactual_pay_policy_simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `temporal_payroll_cash_forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Compensation and Payroll Engine and measurably improves policy exceptions without hiding assumptions.

**Improvement:** Promote `temporal_payroll_cash_forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `policy_exceptions`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `autonomous_payroll_exception_resolution` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Compensation and Payroll Engine and measurably improves pay accuracy without hiding assumptions.

**Improvement:** Promote `autonomous_payroll_exception_resolution` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `pay_accuracy`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic_payroll_instruction_parsing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Compensation and Payroll Engine and measurably improves workforce readiness without hiding assumptions.

**Improvement:** Promote `semantic_payroll_instruction_parsing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `workforce_readiness`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `PAYROLL_ENGINE_DATABASE_URL` and `PAYROLL_ENGINE_DATABASE_URL`

**Justification:** Complete Compensation and Payroll Engine coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `PAYROLL_ENGINE_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `PAYROLL_ENGINE_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `PAYROLL_ENGINE_EVENT_TOPIC` and `PAYROLL_ENGINE_EVENT_TOPIC`

**Justification:** Complete Compensation and Payroll Engine coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `PAYROLL_ENGINE_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `PAYROLL_ENGINE_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `PAYROLL_ENGINE_RETRY_LIMIT` and `PAYROLL_ENGINE_RETRY_LIMIT`

**Justification:** Complete Compensation and Payroll Engine coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `PAYROLL_ENGINE_RETRY_LIMIT` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `PAYROLL_ENGINE_RETRY_LIMIT` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `PAYROLL_ENGINE_DATABASE_URL` and `PAYROLL_ENGINE_DATABASE_URL`

**Justification:** Complete Compensation and Payroll Engine coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `PAYROLL_ENGINE_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `PAYROLL_ENGINE_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `PAYROLL_ENGINE_EVENT_TOPIC` and `PAYROLL_ENGINE_EVENT_TOPIC`

**Justification:** Complete Compensation and Payroll Engine coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `PAYROLL_ENGINE_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `PAYROLL_ENGINE_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `PayrollEngineWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Compensation and Payroll Engine surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `PayrollEngineWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `PayrollEngineDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Compensation and Payroll Engine surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `PayrollEngineDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `PayrollEngineWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Compensation and Payroll Engine surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `PayrollEngineWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `PayrollEngineDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Compensation and Payroll Engine surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `PayrollEngineDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `PayrollEngineWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Compensation and Payroll Engine surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `PayrollEngineWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /payroll-runs` and `LaborHoursApproved`

**Justification:** Compensation and Payroll Engine must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /payroll-runs` and consumed event `LaborHoursApproved` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /payroll-runs/{id}/workers` and `TaxCalculated`

**Justification:** Compensation and Payroll Engine must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /payroll-runs/{id}/workers` and consumed event `TaxCalculated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /payroll-runs/{id}/payslips` and `LaborHoursApproved`

**Justification:** Compensation and Payroll Engine must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /payroll-runs/{id}/payslips` and consumed event `LaborHoursApproved` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /payslips/{id}/deductions` and `TaxCalculated`

**Justification:** Compensation and Payroll Engine must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /payslips/{id}/deductions` and consumed event `TaxCalculated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Compensation and Payroll Engine

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Compensation and Payroll Engine

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Compensation and Payroll Engine

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Compensation and Payroll Engine

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Compensation and Payroll Engine

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Compensation and Payroll Engine

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
