# Tax Compliance and Localization PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `tax_localization`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.
- Representative owned tables: `tax_localization_tax_jurisdiction`, `tax_localization_tax_jurisdiction_topology`, `tax_localization_tax_authority_channel`, `tax_localization_tax_authority_submission`, `tax_localization_tax_filing_calendar`, `tax_localization_tax_nexus_profile`, `tax_localization_tax_rule`, `tax_localization_tax_rule_version`, `tax_localization_tax_rule_impact_analysis`, `tax_localization_product_taxability`, `tax_localization_counterparty_tax_profile`, `tax_localization_tax_exemption_review`, ...
- Representative operations/APIs: `command_tax_jurisdictions`, `command_tax_rules`, `command_tax_quotes`, `command_tax_invoices_id_tax_records`, `command_tax_filings`, `command_tax_events_inbox`, `query_tax_workbench`.
- Representative events: `TaxJurisdictionRegistered`, `TaxRuleActivated`, `TaxCalculated`, `InvoiceTaxRecorded`, `TaxFilingPrepared`.
- Representative advanced capabilities: `event_sourced_tax_lifecycle`, `graph_relational_jurisdiction_topology`, `multi_tenant_compliance_isolation`, `schema_evolution_resilient_tax_schema`, `probabilistic_taxability_classification`, `real_time_tax_quote_convergence`, `counterfactual_tax_policy_simulation`, `temporal_tax_liability_forecasting`, `autonomous_filing_reconciliation`, `semantic_tax_document_parsing`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `tax_localization_tax_jurisdiction`

**Justification:** This owned table is part of the Tax Compliance and Localization operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.

**Improvement:** Extend `tax_localization_tax_jurisdiction` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `jurisdiction_master`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `tax_localization_tax_jurisdiction_topology`

**Justification:** This owned table is part of the Tax Compliance and Localization operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.

**Improvement:** Extend `tax_localization_tax_jurisdiction_topology` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `jurisdiction_topology`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `tax_localization_tax_authority_channel`

**Justification:** This owned table is part of the Tax Compliance and Localization operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.

**Improvement:** Extend `tax_localization_tax_authority_channel` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `authority_channel`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `tax_localization_tax_authority_submission`

**Justification:** This owned table is part of the Tax Compliance and Localization operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.

**Improvement:** Extend `tax_localization_tax_authority_submission` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `authority_submission`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `tax_localization_tax_filing_calendar`

**Justification:** This owned table is part of the Tax Compliance and Localization operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.

**Improvement:** Extend `tax_localization_tax_filing_calendar` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `filing_calendar`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `tax_localization_tax_nexus_profile`

**Justification:** This owned table is part of the Tax Compliance and Localization operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.

**Improvement:** Extend `tax_localization_tax_nexus_profile` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `nexus_profile`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `tax_localization_tax_rule`

**Justification:** This owned table is part of the Tax Compliance and Localization operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.

**Improvement:** Extend `tax_localization_tax_rule` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `tax_rule_authoring`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `tax_localization_tax_rule_version`

**Justification:** This owned table is part of the Tax Compliance and Localization operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.

**Improvement:** Extend `tax_localization_tax_rule_version` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `tax_rule_impact_analysis`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `tax_localization_tax_rule_impact_analysis`

**Justification:** This owned table is part of the Tax Compliance and Localization operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.

**Improvement:** Extend `tax_localization_tax_rule_impact_analysis` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `product_taxability`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `tax_localization_product_taxability`

**Justification:** This owned table is part of the Tax Compliance and Localization operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Regional tax, product taxability, nexus, quote calculation, invoice tax, exemptions, duties, filings, remittance, and tax controls.

**Improvement:** Extend `tax_localization_product_taxability` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `counterparty_tax_profile`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `command_tax_jurisdictions` a complete command lifecycle

**Justification:** High-value users need `command_tax_jurisdictions` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_tax_jurisdictions` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TaxJurisdictionRegistered`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `command_tax_rules` a complete command lifecycle

**Justification:** High-value users need `command_tax_rules` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_tax_rules` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TaxRuleActivated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `command_tax_quotes` a complete command lifecycle

**Justification:** High-value users need `command_tax_quotes` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_tax_quotes` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TaxCalculated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `command_tax_invoices_id_tax_records` a complete command lifecycle

**Justification:** High-value users need `command_tax_invoices_id_tax_records` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_tax_invoices_id_tax_records` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `InvoiceTaxRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `command_tax_filings` a complete command lifecycle

**Justification:** High-value users need `command_tax_filings` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_tax_filings` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TaxFilingPrepared`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `command_tax_events_inbox` a complete command lifecycle

**Justification:** High-value users need `command_tax_events_inbox` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_tax_events_inbox` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TaxJurisdictionRegistered`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Turn `query_tax_workbench` into an expert read-model experience

**Justification:** Domain experts rely on `query_tax_workbench` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_tax_workbench` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `TaxRuleActivated` last changed the projection, and where uncertainty or missing data affects confidence.

### 18. Make `command_tax_jurisdictions` a complete command lifecycle

**Justification:** High-value users need `command_tax_jurisdictions` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_tax_jurisdictions` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TaxCalculated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `command_tax_rules` a complete command lifecycle

**Justification:** High-value users need `command_tax_rules` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_tax_rules` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `InvoiceTaxRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `command_tax_quotes` a complete command lifecycle

**Justification:** High-value users need `command_tax_quotes` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_tax_quotes` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TaxFilingPrepared`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_tax_lifecycle` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Tax Compliance and Localization and measurably improves accuracy rate without hiding assumptions.

**Improvement:** Promote `event_sourced_tax_lifecycle` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `accuracy_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `graph_relational_jurisdiction_topology` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Tax Compliance and Localization and measurably improves close cycle time without hiding assumptions.

**Improvement:** Promote `graph_relational_jurisdiction_topology` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `close_cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `multi_tenant_compliance_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Tax Compliance and Localization and measurably improves cash impact without hiding assumptions.

**Improvement:** Promote `multi_tenant_compliance_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cash_impact`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `schema_evolution_resilient_tax_schema` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Tax Compliance and Localization and measurably improves compliance exceptions without hiding assumptions.

**Improvement:** Promote `schema_evolution_resilient_tax_schema` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `compliance_exceptions`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `probabilistic_taxability_classification` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Tax Compliance and Localization and measurably improves tax jurisdiction registered throughput without hiding assumptions.

**Improvement:** Promote `probabilistic_taxability_classification` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `tax_jurisdiction_registered_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `real_time_tax_quote_convergence` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Tax Compliance and Localization and measurably improves tax rule activated throughput without hiding assumptions.

**Improvement:** Promote `real_time_tax_quote_convergence` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `tax_rule_activated_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `counterfactual_tax_policy_simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Tax Compliance and Localization and measurably improves accuracy rate without hiding assumptions.

**Improvement:** Promote `counterfactual_tax_policy_simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `accuracy_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `temporal_tax_liability_forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Tax Compliance and Localization and measurably improves close cycle time without hiding assumptions.

**Improvement:** Promote `temporal_tax_liability_forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `close_cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `autonomous_filing_reconciliation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Tax Compliance and Localization and measurably improves cash impact without hiding assumptions.

**Improvement:** Promote `autonomous_filing_reconciliation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cash_impact`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic_tax_document_parsing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Tax Compliance and Localization and measurably improves compliance exceptions without hiding assumptions.

**Improvement:** Promote `semantic_tax_document_parsing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `compliance_exceptions`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `TAX_LOCALIZATION_DATABASE_URL` and `TAX_LOCALIZATION_DATABASE_URL`

**Justification:** Complete Tax Compliance and Localization coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `TAX_LOCALIZATION_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `TAX_LOCALIZATION_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `TAX_LOCALIZATION_EVENT_TOPIC` and `TAX_LOCALIZATION_EVENT_TOPIC`

**Justification:** Complete Tax Compliance and Localization coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `TAX_LOCALIZATION_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `TAX_LOCALIZATION_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `TAX_LOCALIZATION_RETRY_LIMIT` and `TAX_LOCALIZATION_RETRY_LIMIT`

**Justification:** Complete Tax Compliance and Localization coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `TAX_LOCALIZATION_RETRY_LIMIT` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `TAX_LOCALIZATION_RETRY_LIMIT` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `TAX_LOCALIZATION_DATABASE_URL` and `TAX_LOCALIZATION_DATABASE_URL`

**Justification:** Complete Tax Compliance and Localization coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `TAX_LOCALIZATION_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `TAX_LOCALIZATION_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `TAX_LOCALIZATION_EVENT_TOPIC` and `TAX_LOCALIZATION_EVENT_TOPIC`

**Justification:** Complete Tax Compliance and Localization coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `TAX_LOCALIZATION_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `TAX_LOCALIZATION_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `TaxLocalizationWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Tax Compliance and Localization surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `TaxLocalizationWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `TaxLocalizationDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Tax Compliance and Localization surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `TaxLocalizationDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `TaxLocalizationWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Tax Compliance and Localization surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `TaxLocalizationWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `TaxLocalizationDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Tax Compliance and Localization surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `TaxLocalizationDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `TaxLocalizationWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Tax Compliance and Localization surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `TaxLocalizationWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /tax/jurisdictions` and `ProductClassified`

**Justification:** Tax Compliance and Localization must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /tax/jurisdictions` and consumed event `ProductClassified` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /tax/rules` and `InvoiceIssued`

**Justification:** Tax Compliance and Localization must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /tax/rules` and consumed event `InvoiceIssued` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /tax/quotes` and `OrderPriced`

**Justification:** Tax Compliance and Localization must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /tax/quotes` and consumed event `OrderPriced` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /tax/invoices/{id}/tax-records` and `PaymentCollected`

**Justification:** Tax Compliance and Localization must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /tax/invoices/{id}/tax-records` and consumed event `PaymentCollected` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Tax Compliance and Localization

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Tax Compliance and Localization

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Tax Compliance and Localization

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Tax Compliance and Localization

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Tax Compliance and Localization

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Tax Compliance and Localization

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
