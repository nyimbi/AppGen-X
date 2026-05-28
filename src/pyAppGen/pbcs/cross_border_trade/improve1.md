# Cross-Border Trade and Customs Compliance PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `cross_border_trade`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: HS code assignment, landed cost, export controls, and customs declarations.
- Representative owned tables: `cross_border_trade_hs_classification`, `cross_border_trade_landed_cost_quote`, `cross_border_trade_export_control_check`, `cross_border_trade_customs_declaration`, `cross_border_trade_denied_party_screening`, `cross_border_trade_trade_document_packet`, `cross_border_trade_broker_handoff`, `cross_border_trade_carrier_handoff`, `cross_border_trade_trade_compliance_hold`, `cross_border_trade_country_restriction_policy`, `cross_border_trade_trade_audit_evidence`.
- Representative operations/APIs: `command_landed_cost`, `command_export_checks`, `command_declarations`, `query_cross_border_trade_workbench`, `command_denied_party_screenings`, `command_document_packets`, `command_broker_handoffs`, `command_carrier_handoffs`, `command_compliance_holds`, `command_hold_resolutions`, `command_country_restrictions`, `command_declaration_releases`.
- Representative events: `CustomsDeclarationPrepared`, `LandedCostCalculated`, `DeniedPartyScreened`, `TradeDocumentPacketPrepared`, `BrokerHandoffQueued`, `CarrierHandoffPrepared`, `TradeComplianceHoldOpened`, `TradeComplianceHoldResolved`, `CountryRestrictionPolicyRegistered`, `CustomsDeclarationReleased`.
- Representative advanced capabilities: `event_sourced_trade_lifecycle`, `owned_trade_schema_boundary`, `graph_relational_trade_topology`, `multi_tenant_trade_isolation`, `schema_evolution_resilient_trade_schema`, `probabilistic_hs_classification_scoring`, `counterfactual_landed_cost_simulation`, `temporal_duty_tax_exposure_forecasting`, `autonomous_trade_exception_resolution`, `semantic_trade_document_understanding`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `cross_border_trade_hs_classification`

**Justification:** This owned table is part of the Cross-Border Trade and Customs Compliance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by HS code assignment, landed cost, export controls, and customs declarations.

**Improvement:** Extend `cross_border_trade_hs_classification` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `hs_classification`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `cross_border_trade_landed_cost_quote`

**Justification:** This owned table is part of the Cross-Border Trade and Customs Compliance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by HS code assignment, landed cost, export controls, and customs declarations.

**Improvement:** Extend `cross_border_trade_landed_cost_quote` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `landed_cost_quote`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `cross_border_trade_export_control_check`

**Justification:** This owned table is part of the Cross-Border Trade and Customs Compliance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by HS code assignment, landed cost, export controls, and customs declarations.

**Improvement:** Extend `cross_border_trade_export_control_check` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `export_control_check`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `cross_border_trade_customs_declaration`

**Justification:** This owned table is part of the Cross-Border Trade and Customs Compliance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by HS code assignment, landed cost, export controls, and customs declarations.

**Improvement:** Extend `cross_border_trade_customs_declaration` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `customs_declaration`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `cross_border_trade_denied_party_screening`

**Justification:** This owned table is part of the Cross-Border Trade and Customs Compliance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by HS code assignment, landed cost, export controls, and customs declarations.

**Improvement:** Extend `cross_border_trade_denied_party_screening` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `country_of_origin`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `cross_border_trade_trade_document_packet`

**Justification:** This owned table is part of the Cross-Border Trade and Customs Compliance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by HS code assignment, landed cost, export controls, and customs declarations.

**Improvement:** Extend `cross_border_trade_trade_document_packet` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `duty_tax_fee_calculation`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `cross_border_trade_broker_handoff`

**Justification:** This owned table is part of the Cross-Border Trade and Customs Compliance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by HS code assignment, landed cost, export controls, and customs declarations.

**Improvement:** Extend `cross_border_trade_broker_handoff` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `restricted_party_and_sanctions_screening`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `cross_border_trade_carrier_handoff`

**Justification:** This owned table is part of the Cross-Border Trade and Customs Compliance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by HS code assignment, landed cost, export controls, and customs declarations.

**Improvement:** Extend `cross_border_trade_carrier_handoff` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `license_requirement_detection`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `cross_border_trade_trade_compliance_hold`

**Justification:** This owned table is part of the Cross-Border Trade and Customs Compliance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by HS code assignment, landed cost, export controls, and customs declarations.

**Improvement:** Extend `cross_border_trade_trade_compliance_hold` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `incoterm_support`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `cross_border_trade_country_restriction_policy`

**Justification:** This owned table is part of the Cross-Border Trade and Customs Compliance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by HS code assignment, landed cost, export controls, and customs declarations.

**Improvement:** Extend `cross_border_trade_country_restriction_policy` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `broker_submission_handoff`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `command_landed_cost` a complete command lifecycle

**Justification:** High-value users need `command_landed_cost` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_landed_cost` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CustomsDeclarationPrepared`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `command_export_checks` a complete command lifecycle

**Justification:** High-value users need `command_export_checks` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_export_checks` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `LandedCostCalculated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `command_declarations` a complete command lifecycle

**Justification:** High-value users need `command_declarations` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_declarations` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DeniedPartyScreened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Turn `query_cross_border_trade_workbench` into an expert read-model experience

**Justification:** Domain experts rely on `query_cross_border_trade_workbench` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_cross_border_trade_workbench` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `TradeDocumentPacketPrepared` last changed the projection, and where uncertainty or missing data affects confidence.

### 15. Make `command_denied_party_screenings` a complete command lifecycle

**Justification:** High-value users need `command_denied_party_screenings` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_denied_party_screenings` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `BrokerHandoffQueued`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `command_document_packets` a complete command lifecycle

**Justification:** High-value users need `command_document_packets` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_document_packets` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CarrierHandoffPrepared`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `command_broker_handoffs` a complete command lifecycle

**Justification:** High-value users need `command_broker_handoffs` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_broker_handoffs` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TradeComplianceHoldOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `command_carrier_handoffs` a complete command lifecycle

**Justification:** High-value users need `command_carrier_handoffs` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_carrier_handoffs` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TradeComplianceHoldResolved`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `command_compliance_holds` a complete command lifecycle

**Justification:** High-value users need `command_compliance_holds` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_compliance_holds` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CountryRestrictionPolicyRegistered`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `command_hold_resolutions` a complete command lifecycle

**Justification:** High-value users need `command_hold_resolutions` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_hold_resolutions` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CustomsDeclarationReleased`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_trade_lifecycle` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Cross-Border Trade and Customs Compliance and measurably improves authorization rate without hiding assumptions.

**Improvement:** Promote `event_sourced_trade_lifecycle` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `authorization_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `owned_trade_schema_boundary` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Cross-Border Trade and Customs Compliance and measurably improves route margin without hiding assumptions.

**Improvement:** Promote `owned_trade_schema_boundary` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `route_margin`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `graph_relational_trade_topology` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Cross-Border Trade and Customs Compliance and measurably improves return cycle time without hiding assumptions.

**Improvement:** Promote `graph_relational_trade_topology` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `return_cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `multi_tenant_trade_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Cross-Border Trade and Customs Compliance and measurably improves landed cost accuracy without hiding assumptions.

**Improvement:** Promote `multi_tenant_trade_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `landed_cost_accuracy`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `schema_evolution_resilient_trade_schema` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Cross-Border Trade and Customs Compliance and measurably improves customs declaration prepared throughput without hiding assumptions.

**Improvement:** Promote `schema_evolution_resilient_trade_schema` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `customs_declaration_prepared_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `probabilistic_hs_classification_scoring` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Cross-Border Trade and Customs Compliance and measurably improves landed cost calculated throughput without hiding assumptions.

**Improvement:** Promote `probabilistic_hs_classification_scoring` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `landed_cost_calculated_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `counterfactual_landed_cost_simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Cross-Border Trade and Customs Compliance and measurably improves authorization rate without hiding assumptions.

**Improvement:** Promote `counterfactual_landed_cost_simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `authorization_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `temporal_duty_tax_exposure_forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Cross-Border Trade and Customs Compliance and measurably improves route margin without hiding assumptions.

**Improvement:** Promote `temporal_duty_tax_exposure_forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `route_margin`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `autonomous_trade_exception_resolution` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Cross-Border Trade and Customs Compliance and measurably improves return cycle time without hiding assumptions.

**Improvement:** Promote `autonomous_trade_exception_resolution` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `return_cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic_trade_document_understanding` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Cross-Border Trade and Customs Compliance and measurably improves landed cost accuracy without hiding assumptions.

**Improvement:** Promote `semantic_trade_document_understanding` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `landed_cost_accuracy`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `CROSS_BORDER_TRADE_DATABASE_URL` and `CROSS_BORDER_TRADE_DATABASE_URL`

**Justification:** Complete Cross-Border Trade and Customs Compliance coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `CROSS_BORDER_TRADE_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `CROSS_BORDER_TRADE_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `CROSS_BORDER_TRADE_EVENT_TOPIC` and `CROSS_BORDER_TRADE_EVENT_TOPIC`

**Justification:** Complete Cross-Border Trade and Customs Compliance coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `CROSS_BORDER_TRADE_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `CROSS_BORDER_TRADE_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `CROSS_BORDER_TRADE_RETRY_LIMIT` and `CROSS_BORDER_TRADE_RETRY_LIMIT`

**Justification:** Complete Cross-Border Trade and Customs Compliance coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `CROSS_BORDER_TRADE_RETRY_LIMIT` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `CROSS_BORDER_TRADE_RETRY_LIMIT` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `CROSS_BORDER_TRADE_DATABASE_URL` and `CROSS_BORDER_TRADE_DATABASE_URL`

**Justification:** Complete Cross-Border Trade and Customs Compliance coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `CROSS_BORDER_TRADE_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `CROSS_BORDER_TRADE_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `CROSS_BORDER_TRADE_EVENT_TOPIC` and `CROSS_BORDER_TRADE_EVENT_TOPIC`

**Justification:** Complete Cross-Border Trade and Customs Compliance coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `CROSS_BORDER_TRADE_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `CROSS_BORDER_TRADE_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `CrossBorderTradeWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Cross-Border Trade and Customs Compliance surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `CrossBorderTradeWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `CrossBorderTradeDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Cross-Border Trade and Customs Compliance surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `CrossBorderTradeDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `CrossBorderTradeWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Cross-Border Trade and Customs Compliance surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `CrossBorderTradeWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `CrossBorderTradeDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Cross-Border Trade and Customs Compliance surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `CrossBorderTradeDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `CrossBorderTradeWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Cross-Border Trade and Customs Compliance surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `CrossBorderTradeWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /landed-cost` and `ProductClassified`

**Justification:** Cross-Border Trade and Customs Compliance must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /landed-cost` and consumed event `ProductClassified` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /export-checks` and `OrderPriced`

**Justification:** Cross-Border Trade and Customs Compliance must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /export-checks` and consumed event `OrderPriced` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /declarations` and `ProductClassified`

**Justification:** Cross-Border Trade and Customs Compliance must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /declarations` and consumed event `ProductClassified` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `GET /cross-border-trade-workbench` and `OrderPriced`

**Justification:** Cross-Border Trade and Customs Compliance must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `GET /cross-border-trade-workbench` and consumed event `OrderPriced` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Cross-Border Trade and Customs Compliance

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Cross-Border Trade and Customs Compliance

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Cross-Border Trade and Customs Compliance

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Cross-Border Trade and Customs Compliance

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Cross-Border Trade and Customs Compliance

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Cross-Border Trade and Customs Compliance

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
