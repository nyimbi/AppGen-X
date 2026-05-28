# General Ledger Core PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `gl_core`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Immutable financial truth, journal orchestration, chart of accounts, and balances.
- Representative owned tables: `gl_core_ledger_event_log`, `gl_core_journal_entry`, `gl_core_journal_line`, `gl_core_ledger_account`, `gl_core_accounting_period`, `gl_core_ledger_projection`, `gl_core_consensus_replica`, `gl_core_schema_extension`, `gl_core_tenant_ledger_partition`, `gl_core_probabilistic_posting`, `gl_core_close_snapshot`, `gl_core_causal_scenario`, ...
- Representative operations/APIs: `command_journals`, `query_trial_balance`, `query_chart_of_accounts`, `query_ledger_events`, `command_ledger_projections`, `command_consensus_commits`, `command_schema_extensions`, `query_temporal_ledger`, `command_probabilistic_postings`, `command_continuous_close_snapshots`, `command_causal_scenarios`, `command_reconciliation_cases`, ...
- Representative events: `JournalPosted`, `PeriodClosed`, `TrialBalanceCalculated`, `LedgerEventAppended`, `ConsensusCommitted`, `LedgerProjectionRebuilt`, `ContinuousCloseSnapshotCreated`, `ReconciliationSuggested`, `AuditProofGenerated`, `RegulatoryRuleCompiled`, ...
- Representative advanced capabilities: `event_sourced_ledger_core`, `distributed_consensus_protocol`, `schema_on_read_extensibility`, `multi_tenant_isolation`, `real_time_olap_oltp_convergence`, `probabilistic_accounting_primitives`, `continuous_close_architecture`, `causal_inference_engine`, `autonomous_reconciliation`, `semantic_transaction_understanding`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `gl_core_ledger_event_log`

**Justification:** This owned table is part of the General Ledger Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Immutable financial truth, journal orchestration, chart of accounts, and balances.

**Improvement:** Extend `gl_core_ledger_event_log` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `configuration_schema`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `gl_core_journal_entry`

**Justification:** This owned table is part of the General Ledger Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Immutable financial truth, journal orchestration, chart of accounts, and balances.

**Improvement:** Extend `gl_core_journal_entry` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `rule_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `gl_core_journal_line`

**Justification:** This owned table is part of the General Ledger Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Immutable financial truth, journal orchestration, chart of accounts, and balances.

**Improvement:** Extend `gl_core_journal_line` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `parameter_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `gl_core_ledger_account`

**Justification:** This owned table is part of the General Ledger Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Immutable financial truth, journal orchestration, chart of accounts, and balances.

**Improvement:** Extend `gl_core_ledger_account` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `chart_of_accounts`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `gl_core_accounting_period`

**Justification:** This owned table is part of the General Ledger Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Immutable financial truth, journal orchestration, chart of accounts, and balances.

**Improvement:** Extend `gl_core_accounting_period` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `journal_entry`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `gl_core_ledger_projection`

**Justification:** This owned table is part of the General Ledger Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Immutable financial truth, journal orchestration, chart of accounts, and balances.

**Improvement:** Extend `gl_core_ledger_projection` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `journal_line_balancing`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `gl_core_consensus_replica`

**Justification:** This owned table is part of the General Ledger Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Immutable financial truth, journal orchestration, chart of accounts, and balances.

**Improvement:** Extend `gl_core_consensus_replica` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `posting_periods`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `gl_core_schema_extension`

**Justification:** This owned table is part of the General Ledger Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Immutable financial truth, journal orchestration, chart of accounts, and balances.

**Improvement:** Extend `gl_core_schema_extension` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `trial_balance`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `gl_core_tenant_ledger_partition`

**Justification:** This owned table is part of the General Ledger Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Immutable financial truth, journal orchestration, chart of accounts, and balances.

**Improvement:** Extend `gl_core_tenant_ledger_partition` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `ledger_projection`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `gl_core_probabilistic_posting`

**Justification:** This owned table is part of the General Ledger Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Immutable financial truth, journal orchestration, chart of accounts, and balances.

**Improvement:** Extend `gl_core_probabilistic_posting` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `account_reconciliation`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `command_journals` a complete command lifecycle

**Justification:** High-value users need `command_journals` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_journals` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `JournalPosted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Turn `query_trial_balance` into an expert read-model experience

**Justification:** Domain experts rely on `query_trial_balance` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_trial_balance` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `PeriodClosed` last changed the projection, and where uncertainty or missing data affects confidence.

### 13. Turn `query_chart_of_accounts` into an expert read-model experience

**Justification:** Domain experts rely on `query_chart_of_accounts` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_chart_of_accounts` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `TrialBalanceCalculated` last changed the projection, and where uncertainty or missing data affects confidence.

### 14. Turn `query_ledger_events` into an expert read-model experience

**Justification:** Domain experts rely on `query_ledger_events` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_ledger_events` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `LedgerEventAppended` last changed the projection, and where uncertainty or missing data affects confidence.

### 15. Make `command_ledger_projections` a complete command lifecycle

**Justification:** High-value users need `command_ledger_projections` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ledger_projections` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ConsensusCommitted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `command_consensus_commits` a complete command lifecycle

**Justification:** High-value users need `command_consensus_commits` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_consensus_commits` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `LedgerProjectionRebuilt`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `command_schema_extensions` a complete command lifecycle

**Justification:** High-value users need `command_schema_extensions` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_schema_extensions` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ContinuousCloseSnapshotCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Turn `query_temporal_ledger` into an expert read-model experience

**Justification:** Domain experts rely on `query_temporal_ledger` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_temporal_ledger` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `ReconciliationSuggested` last changed the projection, and where uncertainty or missing data affects confidence.

### 19. Make `command_probabilistic_postings` a complete command lifecycle

**Justification:** High-value users need `command_probabilistic_postings` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_probabilistic_postings` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `AuditProofGenerated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `command_continuous_close_snapshots` a complete command lifecycle

**Justification:** High-value users need `command_continuous_close_snapshots` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_continuous_close_snapshots` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `RegulatoryRuleCompiled`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_ledger_core` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside General Ledger Core and measurably improves accuracy rate without hiding assumptions.

**Improvement:** Promote `event_sourced_ledger_core` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `accuracy_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `distributed_consensus_protocol` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside General Ledger Core and measurably improves close cycle time without hiding assumptions.

**Improvement:** Promote `distributed_consensus_protocol` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `close_cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `schema_on_read_extensibility` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside General Ledger Core and measurably improves cash impact without hiding assumptions.

**Improvement:** Promote `schema_on_read_extensibility` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cash_impact`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `multi_tenant_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside General Ledger Core and measurably improves compliance exceptions without hiding assumptions.

**Improvement:** Promote `multi_tenant_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `compliance_exceptions`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `real_time_olap_oltp_convergence` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside General Ledger Core and measurably improves journal posted throughput without hiding assumptions.

**Improvement:** Promote `real_time_olap_oltp_convergence` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `journal_posted_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `probabilistic_accounting_primitives` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside General Ledger Core and measurably improves period closed throughput without hiding assumptions.

**Improvement:** Promote `probabilistic_accounting_primitives` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `period_closed_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `continuous_close_architecture` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside General Ledger Core and measurably improves accuracy rate without hiding assumptions.

**Improvement:** Promote `continuous_close_architecture` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `accuracy_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `causal_inference_engine` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside General Ledger Core and measurably improves close cycle time without hiding assumptions.

**Improvement:** Promote `causal_inference_engine` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `close_cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `autonomous_reconciliation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside General Ledger Core and measurably improves cash impact without hiding assumptions.

**Improvement:** Promote `autonomous_reconciliation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cash_impact`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic_transaction_understanding` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside General Ledger Core and measurably improves compliance exceptions without hiding assumptions.

**Improvement:** Promote `semantic_transaction_understanding` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `compliance_exceptions`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `GL_CORE_DATABASE_URL` and `GL_CORE_DATABASE_URL`

**Justification:** Complete General Ledger Core coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `GL_CORE_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `GL_CORE_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `GL_CORE_EVENT_TOPIC` and `GL_CORE_EVENT_TOPIC`

**Justification:** Complete General Ledger Core coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `GL_CORE_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `GL_CORE_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `GL_CORE_RETRY_LIMIT` and `GL_CORE_RETRY_LIMIT`

**Justification:** Complete General Ledger Core coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `GL_CORE_RETRY_LIMIT` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `GL_CORE_RETRY_LIMIT` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `GL_CORE_DATABASE_URL` and `GL_CORE_DATABASE_URL`

**Justification:** Complete General Ledger Core coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `GL_CORE_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `GL_CORE_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `GL_CORE_EVENT_TOPIC` and `GL_CORE_EVENT_TOPIC`

**Justification:** Complete General Ledger Core coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `GL_CORE_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `GL_CORE_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `GlCoreWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete General Ledger Core surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `GlCoreWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `GlCoreDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete General Ledger Core surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `GlCoreDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `GlCoreWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete General Ledger Core surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `GlCoreWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `GlCoreDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete General Ledger Core surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `GlCoreDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `GlCoreWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete General Ledger Core surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `GlCoreWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /journals` and `InvoiceApproved`

**Justification:** General Ledger Core must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /journals` and consumed event `InvoiceApproved` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `GET /trial-balance` and `PaymentCaptured`

**Justification:** General Ledger Core must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `GET /trial-balance` and consumed event `PaymentCaptured` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `GET /chart-of-accounts` and `DepreciationCalculated`

**Justification:** General Ledger Core must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `GET /chart-of-accounts` and consumed event `DepreciationCalculated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `GET /ledger-events` and `OrderShipped`

**Justification:** General Ledger Core must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `GET /ledger-events` and consumed event `OrderShipped` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for General Ledger Core

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for General Ledger Core

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for General Ledger Core

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for General Ledger Core

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for General Ledger Core

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for General Ledger Core

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
