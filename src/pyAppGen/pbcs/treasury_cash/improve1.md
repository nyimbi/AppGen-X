# Treasury and Cash Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `treasury_cash`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.
- Representative owned tables: `treasury_cash_bank_account`, `treasury_cash_bank_account_signatory`, `treasury_cash_bank_counterparty`, `treasury_cash_bank_topology`, `treasury_cash_balance`, `treasury_cash_intraday_balance`, `treasury_cash_statement`, `treasury_cash_statement_line`, `treasury_cash_reconciliation_match`, `treasury_cash_reconciliation_exception`, `treasury_cash_cash_position`, `treasury_cash_cash_forecast`, ...
- Representative operations/APIs: `command_treasury_bank_accounts`, `command_treasury_balances`, `command_treasury_statements`, `command_treasury_statements_id_reconcile`, `query_treasury_cash_position`, `command_treasury_forecasts`, `command_treasury_liquidity_optimize`, `command_treasury_payment_rails_route`, `command_treasury_investments`, `command_treasury_debt_draws`, `command_treasury_fx_hedge_recommendations`, `command_treasury_events_inbox`, ...
- Representative events: `BankAccountRegistered`, `BankBalanceCaptured`, `BankStatementIngested`, `CashPositionBuilt`, `PaymentFunded`, `InvestmentPlaced`, `DebtFacilityDrawn`.
- Representative advanced capabilities: `event_sourced_cash_lifecycle`, `graph_relational_bank_topology`, `multi_tenant_liquidity_isolation`, `schema_evolution_resilient_cash_schema`, `probabilistic_cash_forecasting`, `real_time_liquidity_optimization`, `counterfactual_funding_analysis`, `temporal_cash_flow_stochastic_modeling`, `autonomous_bank_reconciliation`, `semantic_bank_narrative_parsing`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `treasury_cash_bank_account`

**Justification:** This owned table is part of the Treasury and Cash Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.

**Improvement:** Extend `treasury_cash_bank_account` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `configuration_schema`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `treasury_cash_bank_account_signatory`

**Justification:** This owned table is part of the Treasury and Cash Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.

**Improvement:** Extend `treasury_cash_bank_account_signatory` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `rule_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `treasury_cash_bank_counterparty`

**Justification:** This owned table is part of the Treasury and Cash Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.

**Improvement:** Extend `treasury_cash_bank_counterparty` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `parameter_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `treasury_cash_bank_topology`

**Justification:** This owned table is part of the Treasury and Cash Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.

**Improvement:** Extend `treasury_cash_bank_topology` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `bank_account_master`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `treasury_cash_balance`

**Justification:** This owned table is part of the Treasury and Cash Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.

**Improvement:** Extend `treasury_cash_balance` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `bank_signatory_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `treasury_cash_intraday_balance`

**Justification:** This owned table is part of the Treasury and Cash Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.

**Improvement:** Extend `treasury_cash_intraday_balance` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `counterparty_master`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `treasury_cash_statement`

**Justification:** This owned table is part of the Treasury and Cash Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.

**Improvement:** Extend `treasury_cash_statement` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `bank_topology`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `treasury_cash_statement_line`

**Justification:** This owned table is part of the Treasury and Cash Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.

**Improvement:** Extend `treasury_cash_statement_line` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `opening_balance_capture`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `treasury_cash_reconciliation_match`

**Justification:** This owned table is part of the Treasury and Cash Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.

**Improvement:** Extend `treasury_cash_reconciliation_match` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `intraday_balance_capture`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `treasury_cash_reconciliation_exception`

**Justification:** This owned table is part of the Treasury and Cash Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Multi-currency cash, bank connectivity, liquidity planning, funding, investments, debt, FX exposure, and treasury controls.

**Improvement:** Extend `treasury_cash_reconciliation_exception` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `cash_position`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `command_treasury_bank_accounts` a complete command lifecycle

**Justification:** High-value users need `command_treasury_bank_accounts` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_treasury_bank_accounts` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `BankAccountRegistered`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `command_treasury_balances` a complete command lifecycle

**Justification:** High-value users need `command_treasury_balances` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_treasury_balances` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `BankBalanceCaptured`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `command_treasury_statements` a complete command lifecycle

**Justification:** High-value users need `command_treasury_statements` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_treasury_statements` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `BankStatementIngested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `command_treasury_statements_id_reconcile` a complete command lifecycle

**Justification:** High-value users need `command_treasury_statements_id_reconcile` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_treasury_statements_id_reconcile` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CashPositionBuilt`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Turn `query_treasury_cash_position` into an expert read-model experience

**Justification:** Domain experts rely on `query_treasury_cash_position` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_treasury_cash_position` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `PaymentFunded` last changed the projection, and where uncertainty or missing data affects confidence.

### 16. Make `command_treasury_forecasts` a complete command lifecycle

**Justification:** High-value users need `command_treasury_forecasts` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_treasury_forecasts` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `InvestmentPlaced`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `command_treasury_liquidity_optimize` a complete command lifecycle

**Justification:** High-value users need `command_treasury_liquidity_optimize` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_treasury_liquidity_optimize` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DebtFacilityDrawn`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `command_treasury_payment_rails_route` a complete command lifecycle

**Justification:** High-value users need `command_treasury_payment_rails_route` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_treasury_payment_rails_route` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `BankAccountRegistered`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `command_treasury_investments` a complete command lifecycle

**Justification:** High-value users need `command_treasury_investments` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_treasury_investments` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `BankBalanceCaptured`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `command_treasury_debt_draws` a complete command lifecycle

**Justification:** High-value users need `command_treasury_debt_draws` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_treasury_debt_draws` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `BankStatementIngested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_cash_lifecycle` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Treasury and Cash Management and measurably improves accuracy rate without hiding assumptions.

**Improvement:** Promote `event_sourced_cash_lifecycle` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `accuracy_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `graph_relational_bank_topology` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Treasury and Cash Management and measurably improves close cycle time without hiding assumptions.

**Improvement:** Promote `graph_relational_bank_topology` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `close_cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `multi_tenant_liquidity_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Treasury and Cash Management and measurably improves cash impact without hiding assumptions.

**Improvement:** Promote `multi_tenant_liquidity_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cash_impact`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `schema_evolution_resilient_cash_schema` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Treasury and Cash Management and measurably improves compliance exceptions without hiding assumptions.

**Improvement:** Promote `schema_evolution_resilient_cash_schema` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `compliance_exceptions`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `probabilistic_cash_forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Treasury and Cash Management and measurably improves bank account registered throughput without hiding assumptions.

**Improvement:** Promote `probabilistic_cash_forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `bank_account_registered_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `real_time_liquidity_optimization` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Treasury and Cash Management and measurably improves bank balance captured throughput without hiding assumptions.

**Improvement:** Promote `real_time_liquidity_optimization` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `bank_balance_captured_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `counterfactual_funding_analysis` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Treasury and Cash Management and measurably improves accuracy rate without hiding assumptions.

**Improvement:** Promote `counterfactual_funding_analysis` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `accuracy_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `temporal_cash_flow_stochastic_modeling` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Treasury and Cash Management and measurably improves close cycle time without hiding assumptions.

**Improvement:** Promote `temporal_cash_flow_stochastic_modeling` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `close_cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `autonomous_bank_reconciliation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Treasury and Cash Management and measurably improves cash impact without hiding assumptions.

**Improvement:** Promote `autonomous_bank_reconciliation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cash_impact`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic_bank_narrative_parsing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Treasury and Cash Management and measurably improves compliance exceptions without hiding assumptions.

**Improvement:** Promote `semantic_bank_narrative_parsing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `compliance_exceptions`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `TREASURY_CASH_DATABASE_URL` and `TREASURY_CASH_DATABASE_URL`

**Justification:** Complete Treasury and Cash Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `TREASURY_CASH_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `TREASURY_CASH_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `TREASURY_CASH_EVENT_TOPIC` and `TREASURY_CASH_EVENT_TOPIC`

**Justification:** Complete Treasury and Cash Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `TREASURY_CASH_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `TREASURY_CASH_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `TREASURY_CASH_RETRY_LIMIT` and `TREASURY_CASH_RETRY_LIMIT`

**Justification:** Complete Treasury and Cash Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `TREASURY_CASH_RETRY_LIMIT` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `TREASURY_CASH_RETRY_LIMIT` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `TREASURY_CASH_DATABASE_URL` and `TREASURY_CASH_DATABASE_URL`

**Justification:** Complete Treasury and Cash Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `TREASURY_CASH_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `TREASURY_CASH_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `TREASURY_CASH_EVENT_TOPIC` and `TREASURY_CASH_EVENT_TOPIC`

**Justification:** Complete Treasury and Cash Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `TREASURY_CASH_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `TREASURY_CASH_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `TreasuryCashWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Treasury and Cash Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `TreasuryCashWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `TreasuryCashDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Treasury and Cash Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `TreasuryCashDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `TreasuryCashWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Treasury and Cash Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `TreasuryCashWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `TreasuryCashDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Treasury and Cash Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `TreasuryCashDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `TreasuryCashWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Treasury and Cash Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `TreasuryCashWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /treasury/bank-accounts` and `PaymentFundingRequested`

**Justification:** Treasury and Cash Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /treasury/bank-accounts` and consumed event `PaymentFundingRequested` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /treasury/balances` and `ReceivableCashForecasted`

**Justification:** Treasury and Cash Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /treasury/balances` and consumed event `ReceivableCashForecasted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /treasury/statements` and `PayablePaymentScheduled`

**Justification:** Treasury and Cash Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /treasury/statements` and consumed event `PayablePaymentScheduled` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /treasury/statements/{id}/reconcile` and `PayrollFundingRequested`

**Justification:** Treasury and Cash Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /treasury/statements/{id}/reconcile` and consumed event `PayrollFundingRequested` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Treasury and Cash Management

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Treasury and Cash Management

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Treasury and Cash Management

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Treasury and Cash Management

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Treasury and Cash Management

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Treasury and Cash Management

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
