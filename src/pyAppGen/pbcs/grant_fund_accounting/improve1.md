# Grant and Fund Accounting PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `grant_fund_accounting`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.
- Representative owned tables: `grant_fund_accounting_grant_award`, `grant_fund_accounting_grant_fund`, `grant_fund_accounting_fund_restriction`, `grant_fund_accounting_grant_budget`, `grant_fund_accounting_grant_budget_line`, `grant_fund_accounting_allowable_cost_rule`, `grant_fund_accounting_grant_cost_transaction`, `grant_fund_accounting_cost_allocation`, `grant_fund_accounting_drawdown_request`, `grant_fund_accounting_drawdown_receipt`, `grant_fund_accounting_match_requirement`, `grant_fund_accounting_match_contribution`, ...
- Representative operations/APIs: `create_grant_award`, `define_fund_restriction`, `open_grant_budget`, `capture_budget_line`, `register_allowable_cost_rule`, `record_grant_cost`, `run_cost_allocation`, `prepare_drawdown_request`, `record_drawdown_receipt`, `track_match_requirement`, `record_match_contribution`, `build_funder_report`, ...
- Representative events: `GrantAwardCreated`, `GrantBudgetApproved`, `GrantCostRecorded`, `DrawdownRequested`, `FunderReportSubmitted`, `GrantExceptionOpened`.
- Representative advanced capabilities: `restriction-aware cost validation`, `drawdown cash simulation`, `semantic award document extraction`, `continuous funder compliance testing`, `cryptographic evidence packet`, `multi-funder portfolio forecasting`.

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `grant_fund_accounting_grant_award`

**Justification:** This owned table is part of the Grant and Fund Accounting operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.

**Improvement:** Extend `grant_fund_accounting_grant_award` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `grant_award_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `grant_fund_accounting_grant_fund`

**Justification:** This owned table is part of the Grant and Fund Accounting operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.

**Improvement:** Extend `grant_fund_accounting_grant_fund` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `grant_fund_accounting_workflow`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `grant_fund_accounting_fund_restriction`

**Justification:** This owned table is part of the Grant and Fund Accounting operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.

**Improvement:** Extend `grant_fund_accounting_fund_restriction` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `grant_fund_accounting_analytics`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `grant_fund_accounting_grant_budget`

**Justification:** This owned table is part of the Grant and Fund Accounting operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.

**Improvement:** Extend `grant_fund_accounting_grant_budget` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `configuration_schema`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `grant_fund_accounting_grant_budget_line`

**Justification:** This owned table is part of the Grant and Fund Accounting operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.

**Improvement:** Extend `grant_fund_accounting_grant_budget_line` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `rule_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `grant_fund_accounting_allowable_cost_rule`

**Justification:** This owned table is part of the Grant and Fund Accounting operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.

**Improvement:** Extend `grant_fund_accounting_allowable_cost_rule` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `parameter_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `grant_fund_accounting_grant_cost_transaction`

**Justification:** This owned table is part of the Grant and Fund Accounting operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.

**Improvement:** Extend `grant_fund_accounting_grant_cost_transaction` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `owned_schema_migrations_models`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `grant_fund_accounting_cost_allocation`

**Justification:** This owned table is part of the Grant and Fund Accounting operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.

**Improvement:** Extend `grant_fund_accounting_cost_allocation` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `appgen_x_outbox_inbox_eventing`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `grant_fund_accounting_drawdown_request`

**Justification:** This owned table is part of the Grant and Fund Accounting operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.

**Improvement:** Extend `grant_fund_accounting_drawdown_request` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `idempotent_handlers`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `grant_fund_accounting_drawdown_receipt`

**Justification:** This owned table is part of the Grant and Fund Accounting operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.

**Improvement:** Extend `grant_fund_accounting_drawdown_receipt` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `retry_dead_letter_evidence`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `create_grant_award` a complete command lifecycle

**Justification:** High-value users need `create_grant_award` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_grant_award` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GrantAwardCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `define_fund_restriction` a complete command lifecycle

**Justification:** High-value users need `define_fund_restriction` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `define_fund_restriction` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GrantBudgetApproved`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `open_grant_budget` a complete command lifecycle

**Justification:** High-value users need `open_grant_budget` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `open_grant_budget` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GrantCostRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `capture_budget_line` a complete command lifecycle

**Justification:** High-value users need `capture_budget_line` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `capture_budget_line` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DrawdownRequested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `register_allowable_cost_rule` a complete command lifecycle

**Justification:** High-value users need `register_allowable_cost_rule` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `register_allowable_cost_rule` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `FunderReportSubmitted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `record_grant_cost` a complete command lifecycle

**Justification:** High-value users need `record_grant_cost` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `record_grant_cost` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GrantExceptionOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `run_cost_allocation` a complete command lifecycle

**Justification:** High-value users need `run_cost_allocation` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `run_cost_allocation` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GrantAwardCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `prepare_drawdown_request` a complete command lifecycle

**Justification:** High-value users need `prepare_drawdown_request` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `prepare_drawdown_request` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GrantBudgetApproved`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `record_drawdown_receipt` a complete command lifecycle

**Justification:** High-value users need `record_drawdown_receipt` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `record_drawdown_receipt` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GrantCostRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `track_match_requirement` a complete command lifecycle

**Justification:** High-value users need `track_match_requirement` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `track_match_requirement` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DrawdownRequested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `restriction-aware cost validation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Grant and Fund Accounting and measurably improves grant fund accounting risk score without hiding assumptions.

**Improvement:** Promote `restriction-aware cost validation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `grant_fund_accounting_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `drawdown cash simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Grant and Fund Accounting and measurably improves grant fund accounting workbench metric without hiding assumptions.

**Improvement:** Promote `drawdown cash simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `grant_fund_accounting_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `semantic award document extraction` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Grant and Fund Accounting and measurably improves grant fund accounting risk score without hiding assumptions.

**Improvement:** Promote `semantic award document extraction` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `grant_fund_accounting_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `continuous funder compliance testing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Grant and Fund Accounting and measurably improves grant fund accounting workbench metric without hiding assumptions.

**Improvement:** Promote `continuous funder compliance testing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `grant_fund_accounting_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `cryptographic evidence packet` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Grant and Fund Accounting and measurably improves grant fund accounting risk score without hiding assumptions.

**Improvement:** Promote `cryptographic evidence packet` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `grant_fund_accounting_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `multi-funder portfolio forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Grant and Fund Accounting and measurably improves grant fund accounting workbench metric without hiding assumptions.

**Improvement:** Promote `multi-funder portfolio forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `grant_fund_accounting_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `restriction-aware cost validation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Grant and Fund Accounting and measurably improves grant fund accounting risk score without hiding assumptions.

**Improvement:** Promote `restriction-aware cost validation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `grant_fund_accounting_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `drawdown cash simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Grant and Fund Accounting and measurably improves grant fund accounting workbench metric without hiding assumptions.

**Improvement:** Promote `drawdown cash simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `grant_fund_accounting_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `semantic award document extraction` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Grant and Fund Accounting and measurably improves grant fund accounting risk score without hiding assumptions.

**Improvement:** Promote `semantic award document extraction` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `grant_fund_accounting_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `continuous funder compliance testing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Grant and Fund Accounting and measurably improves grant fund accounting workbench metric without hiding assumptions.

**Improvement:** Promote `continuous funder compliance testing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `grant_fund_accounting_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `allowable_cost_policy` and `drawdown_lead_days`

**Justification:** Complete Grant and Fund Accounting coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `allowable_cost_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `drawdown_lead_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `drawdown_policy` and `match_warning_threshold`

**Justification:** Complete Grant and Fund Accounting coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `drawdown_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `match_warning_threshold` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `match_requirement_policy` and `reporting_warning_days`

**Justification:** Complete Grant and Fund Accounting coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `match_requirement_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `reporting_warning_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `reporting_deadline_policy` and `cost_materiality_threshold`

**Justification:** Complete Grant and Fund Accounting coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `reporting_deadline_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `cost_materiality_threshold` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `fund_restriction_policy` and `retention_years`

**Justification:** Complete Grant and Fund Accounting coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `fund_restriction_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `retention_years` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `grant accounting workbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Grant and Fund Accounting surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `grant accounting workbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `fund restriction ledger` into a full specialist command center

**Justification:** The PBC UI must expose the complete Grant and Fund Accounting surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `fund restriction ledger` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `budget control board` into a full specialist command center

**Justification:** The PBC UI must expose the complete Grant and Fund Accounting surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `budget control board` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `drawdown console` into a full specialist command center

**Justification:** The PBC UI must expose the complete Grant and Fund Accounting surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `drawdown console` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `match tracker` into a full specialist command center

**Justification:** The PBC UI must expose the complete Grant and Fund Accounting surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `match tracker` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /grant-awards` and `JournalPosted`

**Justification:** Grant and Fund Accounting must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /grant-awards` and consumed event `JournalPosted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /fund-restrictions` and `PaymentExecuted`

**Justification:** Grant and Fund Accounting must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /fund-restrictions` and consumed event `PaymentExecuted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /grant-budgets` and `PolicyChanged`

**Justification:** Grant and Fund Accounting must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /grant-budgets` and consumed event `PolicyChanged` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /reimbursement-claims` and `AuditProofGenerated`

**Justification:** Grant and Fund Accounting must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /reimbursement-claims` and consumed event `AuditProofGenerated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Grant and Fund Accounting

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Grant and Fund Accounting

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Grant and Fund Accounting

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Grant and Fund Accounting

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Grant and Fund Accounting

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Grant and Fund Accounting

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
