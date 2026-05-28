# Expense Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `expense_management`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.
- Representative owned tables: `expense_management_expense_report`, `expense_management_expense_line`, `expense_management_receipt_artifact`, `expense_management_card_transaction`, `expense_management_merchant_profile`, `expense_management_expense_policy`, `expense_management_policy_violation`, `expense_management_expense_approval_task`, `expense_management_reimbursement_batch`, `expense_management_reimbursement_payment`, `expense_management_cash_advance`, `expense_management_mileage_claim`, ...
- Representative operations/APIs: `create_expense_report`, `capture_expense_line`, `attach_receipt`, `ingest_card_transaction`, `match_card_receipt`, `validate_expense_policy`, `open_policy_violation`, `route_expense_approval`, `approve_expense_report`, `create_reimbursement_batch`, `execute_reimbursement`, `record_cash_advance`, ...
- Representative events: `ExpenseReportCreated`, `ExpensePolicyViolationOpened`, `ExpenseApproved`, `ReimbursementScheduled`, `ExpenseAuditSampled`, `DuplicateExpenseDetected`.
- Representative advanced capabilities: `semantic receipt extraction`, `probabilistic duplicate detection`, `counterfactual policy coaching`, `continuous spend control testing`, `risk-based audit sampling`, `carbon-aware travel expense insights`.

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `expense_management_expense_report`

**Justification:** This owned table is part of the Expense Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.

**Improvement:** Extend `expense_management_expense_report` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `expense_report_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `expense_management_expense_line`

**Justification:** This owned table is part of the Expense Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.

**Improvement:** Extend `expense_management_expense_line` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `expense_management_workflow`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `expense_management_receipt_artifact`

**Justification:** This owned table is part of the Expense Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.

**Improvement:** Extend `expense_management_receipt_artifact` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `expense_management_analytics`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `expense_management_card_transaction`

**Justification:** This owned table is part of the Expense Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.

**Improvement:** Extend `expense_management_card_transaction` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `configuration_schema`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `expense_management_merchant_profile`

**Justification:** This owned table is part of the Expense Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.

**Improvement:** Extend `expense_management_merchant_profile` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `rule_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `expense_management_expense_policy`

**Justification:** This owned table is part of the Expense Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.

**Improvement:** Extend `expense_management_expense_policy` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `parameter_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `expense_management_policy_violation`

**Justification:** This owned table is part of the Expense Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.

**Improvement:** Extend `expense_management_policy_violation` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `owned_schema_migrations_models`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `expense_management_expense_approval_task`

**Justification:** This owned table is part of the Expense Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.

**Improvement:** Extend `expense_management_expense_approval_task` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `appgen_x_outbox_inbox_eventing`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `expense_management_reimbursement_batch`

**Justification:** This owned table is part of the Expense Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.

**Improvement:** Extend `expense_management_reimbursement_batch` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `idempotent_handlers`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `expense_management_reimbursement_payment`

**Justification:** This owned table is part of the Expense Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.

**Improvement:** Extend `expense_management_reimbursement_payment` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `retry_dead_letter_evidence`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `create_expense_report` a complete command lifecycle

**Justification:** High-value users need `create_expense_report` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_expense_report` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ExpenseReportCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `capture_expense_line` a complete command lifecycle

**Justification:** High-value users need `capture_expense_line` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `capture_expense_line` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ExpensePolicyViolationOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `attach_receipt` a complete command lifecycle

**Justification:** High-value users need `attach_receipt` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `attach_receipt` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ExpenseApproved`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `ingest_card_transaction` a complete command lifecycle

**Justification:** High-value users need `ingest_card_transaction` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `ingest_card_transaction` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ReimbursementScheduled`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `match_card_receipt` a complete command lifecycle

**Justification:** High-value users need `match_card_receipt` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `match_card_receipt` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ExpenseAuditSampled`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `validate_expense_policy` a complete command lifecycle

**Justification:** High-value users need `validate_expense_policy` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `validate_expense_policy` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DuplicateExpenseDetected`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `open_policy_violation` a complete command lifecycle

**Justification:** High-value users need `open_policy_violation` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `open_policy_violation` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ExpenseReportCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `route_expense_approval` a complete command lifecycle

**Justification:** High-value users need `route_expense_approval` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `route_expense_approval` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ExpensePolicyViolationOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `approve_expense_report` a complete command lifecycle

**Justification:** High-value users need `approve_expense_report` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `approve_expense_report` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ExpenseApproved`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `create_reimbursement_batch` a complete command lifecycle

**Justification:** High-value users need `create_reimbursement_batch` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_reimbursement_batch` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ReimbursementScheduled`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `semantic receipt extraction` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Expense Management and measurably improves expense management risk score without hiding assumptions.

**Improvement:** Promote `semantic receipt extraction` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `expense_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `probabilistic duplicate detection` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Expense Management and measurably improves expense management workbench metric without hiding assumptions.

**Improvement:** Promote `probabilistic duplicate detection` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `expense_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `counterfactual policy coaching` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Expense Management and measurably improves expense management risk score without hiding assumptions.

**Improvement:** Promote `counterfactual policy coaching` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `expense_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `continuous spend control testing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Expense Management and measurably improves expense management workbench metric without hiding assumptions.

**Improvement:** Promote `continuous spend control testing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `expense_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `risk-based audit sampling` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Expense Management and measurably improves expense management risk score without hiding assumptions.

**Improvement:** Promote `risk-based audit sampling` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `expense_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `carbon-aware travel expense insights` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Expense Management and measurably improves expense management workbench metric without hiding assumptions.

**Improvement:** Promote `carbon-aware travel expense insights` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `expense_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `semantic receipt extraction` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Expense Management and measurably improves expense management risk score without hiding assumptions.

**Improvement:** Promote `semantic receipt extraction` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `expense_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `probabilistic duplicate detection` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Expense Management and measurably improves expense management workbench metric without hiding assumptions.

**Improvement:** Promote `probabilistic duplicate detection` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `expense_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `counterfactual policy coaching` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Expense Management and measurably improves expense management risk score without hiding assumptions.

**Improvement:** Promote `counterfactual policy coaching` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `expense_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `continuous spend control testing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Expense Management and measurably improves expense management workbench metric without hiding assumptions.

**Improvement:** Promote `continuous spend control testing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `expense_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `receipt_required_policy` and `receipt_required_amount`

**Justification:** Complete Expense Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `receipt_required_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `receipt_required_amount` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `merchant_category_policy` and `auto_approval_limit`

**Justification:** Complete Expense Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `merchant_category_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `auto_approval_limit` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `approval_limit_policy` and `duplicate_similarity_threshold`

**Justification:** Complete Expense Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `approval_limit_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `duplicate_similarity_threshold` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `duplicate_detection_policy` and `mileage_rate`

**Justification:** Complete Expense Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `duplicate_detection_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `mileage_rate` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `reimbursement_policy` and `audit_sample_rate`

**Justification:** Complete Expense Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `reimbursement_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `audit_sample_rate` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `expense workbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Expense Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `expense workbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `receipt inbox` into a full specialist command center

**Justification:** The PBC UI must expose the complete Expense Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `receipt inbox` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `policy violation queue` into a full specialist command center

**Justification:** The PBC UI must expose the complete Expense Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `policy violation queue` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `approval board` into a full specialist command center

**Justification:** The PBC UI must expose the complete Expense Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `approval board` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `reimbursement console` into a full specialist command center

**Justification:** The PBC UI must expose the complete Expense Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `reimbursement console` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /expense-reports` and `EmployeeCreated`

**Justification:** Expense Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /expense-reports` and consumed event `EmployeeCreated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /expense-lines` and `CardTransactionPosted`

**Justification:** Expense Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /expense-lines` and consumed event `CardTransactionPosted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /receipt-documents` and `PaymentExecuted`

**Justification:** Expense Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /receipt-documents` and consumed event `PaymentExecuted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /expense-approvals` and `PolicyChanged`

**Justification:** Expense Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /expense-approvals` and consumed event `PolicyChanged` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Expense Management

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Expense Management

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Expense Management

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Expense Management

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Expense Management

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Expense Management

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
