# Legal Matter Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `legal_matter_management`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.
- Representative owned tables: `legal_matter_management_legal_matter`, `legal_matter_management_matter_party`, `legal_matter_management_matter_counsel`, `legal_matter_management_matter_budget`, `legal_matter_management_matter_budget_line`, `legal_matter_management_legal_hold`, `legal_matter_management_hold_custodian`, `legal_matter_management_matter_deadline`, `legal_matter_management_filing_record`, `legal_matter_management_matter_document`, `legal_matter_management_document_privilege_review`, `legal_matter_management_outside_counsel_invoice`, ...
- Representative operations/APIs: `open_legal_matter`, `register_matter_party`, `assign_counsel`, `create_matter_budget`, `capture_budget_line`, `issue_legal_hold`, `register_hold_custodian`, `track_matter_deadline`, `record_filing`, `attach_matter_document`, `review_document_privilege`, `ingest_counsel_invoice`, ...
- Representative events: `LegalMatterOpened`, `LegalHoldIssued`, `MatterDeadlineTracked`, `FilingRecorded`, `MatterRiskChanged`, `MatterClosed`.
- Representative advanced capabilities: `legal deadline risk prediction`, `semantic document privilege triage`, `case exposure simulation`, `outside counsel spend intelligence`, `cryptographic hold evidence`, `policy-aware settlement routing`.

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `legal_matter_management_legal_matter`

**Justification:** This owned table is part of the Legal Matter Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.

**Improvement:** Extend `legal_matter_management_legal_matter` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `legal_matter_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `legal_matter_management_matter_party`

**Justification:** This owned table is part of the Legal Matter Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.

**Improvement:** Extend `legal_matter_management_matter_party` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `legal_matter_management_workflow`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `legal_matter_management_matter_counsel`

**Justification:** This owned table is part of the Legal Matter Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.

**Improvement:** Extend `legal_matter_management_matter_counsel` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `legal_matter_management_analytics`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `legal_matter_management_matter_budget`

**Justification:** This owned table is part of the Legal Matter Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.

**Improvement:** Extend `legal_matter_management_matter_budget` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `configuration_schema`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `legal_matter_management_matter_budget_line`

**Justification:** This owned table is part of the Legal Matter Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.

**Improvement:** Extend `legal_matter_management_matter_budget_line` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `rule_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `legal_matter_management_legal_hold`

**Justification:** This owned table is part of the Legal Matter Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.

**Improvement:** Extend `legal_matter_management_legal_hold` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `parameter_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `legal_matter_management_hold_custodian`

**Justification:** This owned table is part of the Legal Matter Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.

**Improvement:** Extend `legal_matter_management_hold_custodian` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `owned_schema_migrations_models`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `legal_matter_management_matter_deadline`

**Justification:** This owned table is part of the Legal Matter Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.

**Improvement:** Extend `legal_matter_management_matter_deadline` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `appgen_x_outbox_inbox_eventing`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `legal_matter_management_filing_record`

**Justification:** This owned table is part of the Legal Matter Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.

**Improvement:** Extend `legal_matter_management_filing_record` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `idempotent_handlers`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `legal_matter_management_matter_document`

**Justification:** This owned table is part of the Legal Matter Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.

**Improvement:** Extend `legal_matter_management_matter_document` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `retry_dead_letter_evidence`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `open_legal_matter` a complete command lifecycle

**Justification:** High-value users need `open_legal_matter` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `open_legal_matter` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `LegalMatterOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `register_matter_party` a complete command lifecycle

**Justification:** High-value users need `register_matter_party` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `register_matter_party` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `LegalHoldIssued`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `assign_counsel` a complete command lifecycle

**Justification:** High-value users need `assign_counsel` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `assign_counsel` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MatterDeadlineTracked`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `create_matter_budget` a complete command lifecycle

**Justification:** High-value users need `create_matter_budget` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_matter_budget` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `FilingRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `capture_budget_line` a complete command lifecycle

**Justification:** High-value users need `capture_budget_line` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `capture_budget_line` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MatterRiskChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `issue_legal_hold` a complete command lifecycle

**Justification:** High-value users need `issue_legal_hold` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `issue_legal_hold` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MatterClosed`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `register_hold_custodian` a complete command lifecycle

**Justification:** High-value users need `register_hold_custodian` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `register_hold_custodian` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `LegalMatterOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `track_matter_deadline` a complete command lifecycle

**Justification:** High-value users need `track_matter_deadline` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `track_matter_deadline` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `LegalHoldIssued`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `record_filing` a complete command lifecycle

**Justification:** High-value users need `record_filing` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `record_filing` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MatterDeadlineTracked`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `attach_matter_document` a complete command lifecycle

**Justification:** High-value users need `attach_matter_document` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `attach_matter_document` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `FilingRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `legal deadline risk prediction` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Legal Matter Management and measurably improves legal matter management risk score without hiding assumptions.

**Improvement:** Promote `legal deadline risk prediction` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `legal_matter_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `semantic document privilege triage` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Legal Matter Management and measurably improves legal matter management workbench metric without hiding assumptions.

**Improvement:** Promote `semantic document privilege triage` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `legal_matter_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `case exposure simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Legal Matter Management and measurably improves legal matter management risk score without hiding assumptions.

**Improvement:** Promote `case exposure simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `legal_matter_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `outside counsel spend intelligence` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Legal Matter Management and measurably improves legal matter management workbench metric without hiding assumptions.

**Improvement:** Promote `outside counsel spend intelligence` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `legal_matter_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `cryptographic hold evidence` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Legal Matter Management and measurably improves legal matter management risk score without hiding assumptions.

**Improvement:** Promote `cryptographic hold evidence` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `legal_matter_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `policy-aware settlement routing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Legal Matter Management and measurably improves legal matter management workbench metric without hiding assumptions.

**Improvement:** Promote `policy-aware settlement routing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `legal_matter_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `legal deadline risk prediction` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Legal Matter Management and measurably improves legal matter management risk score without hiding assumptions.

**Improvement:** Promote `legal deadline risk prediction` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `legal_matter_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `semantic document privilege triage` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Legal Matter Management and measurably improves legal matter management workbench metric without hiding assumptions.

**Improvement:** Promote `semantic document privilege triage` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `legal_matter_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `case exposure simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Legal Matter Management and measurably improves legal matter management risk score without hiding assumptions.

**Improvement:** Promote `case exposure simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `legal_matter_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `outside counsel spend intelligence` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Legal Matter Management and measurably improves legal matter management workbench metric without hiding assumptions.

**Improvement:** Promote `outside counsel spend intelligence` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `legal_matter_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `matter_intake_policy` and `deadline_warning_days`

**Justification:** Complete Legal Matter Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `matter_intake_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `deadline_warning_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `hold_policy` and `budget_warning_percent`

**Justification:** Complete Legal Matter Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `hold_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `budget_warning_percent` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `deadline_escalation_policy` and `privilege_review_sla_hours`

**Justification:** Complete Legal Matter Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `deadline_escalation_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `privilege_review_sla_hours` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `privilege_review_policy` and `settlement_approval_limit`

**Justification:** Complete Legal Matter Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `privilege_review_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `settlement_approval_limit` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `budget_policy` and `hold_review_days`

**Justification:** Complete Legal Matter Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `budget_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `hold_review_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `legal matter workbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Legal Matter Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `legal matter workbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `matter timeline` into a full specialist command center

**Justification:** The PBC UI must expose the complete Legal Matter Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `matter timeline` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `legal hold console` into a full specialist command center

**Justification:** The PBC UI must expose the complete Legal Matter Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `legal hold console` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `deadline calendar` into a full specialist command center

**Justification:** The PBC UI must expose the complete Legal Matter Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `deadline calendar` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `document privilege queue` into a full specialist command center

**Justification:** The PBC UI must expose the complete Legal Matter Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `document privilege queue` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /legal-matters` and `SupplierQualified`

**Justification:** Legal Matter Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /legal-matters` and consumed event `SupplierQualified` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /outside-counsel` and `InvoiceCaptured`

**Justification:** Legal Matter Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /outside-counsel` and consumed event `InvoiceCaptured` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /matter-budgets` and `PolicyChanged`

**Justification:** Legal Matter Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /matter-budgets` and consumed event `PolicyChanged` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /legal-holds` and `AuditProofGenerated`

**Justification:** Legal Matter Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /legal-holds` and consumed event `AuditProofGenerated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Legal Matter Management

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Legal Matter Management

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Legal Matter Management

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Legal Matter Management

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Legal Matter Management

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Legal Matter Management

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
