# Accounts Payable Automation PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `ap_automation`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Vendor obligations, OCR intake, invoice matching, approval, and withholding.
- Representative owned tables: `ap_automation_vendor`, `ap_automation_vendor_site`, `ap_automation_vendor_bank_account`, `ap_automation_vendor_tax_profile`, `ap_automation_vendor_risk_signal`, `ap_automation_purchase_order`, `ap_automation_purchase_order_line`, `ap_automation_goods_receipt`, `ap_automation_goods_receipt_line`, `ap_automation_invoice`, `ap_automation_invoice_line`, `ap_automation_invoice_capture_artifact`, ...
- Representative operations/APIs: `command_ap_vendors`, `command_ap_vendor_bank_accounts`, `command_ap_vendor_tax_profiles`, `command_ap_purchase_orders`, `command_ap_goods_receipts`, `command_ap_invoices`, `command_ap_invoices_invoice_id_match`, `command_ap_exceptions`, `command_ap_approval_tasks`, `command_ap_payment_schedules`, `command_ap_payment_batches`, `command_ap_payments`, ...
- Representative events: `VendorOnboarded`, `PurchaseOrderIssued`, `GoodsReceiptRecorded`, `InvoiceCaptured`, `PaymentScheduled`, `PaymentExecuted`, `InvoiceExceptionResolved`, `VendorRiskChanged`, `DiscountOpportunityCaptured`.
- Representative advanced capabilities: `event_sourced_invoice_lifecycle`, `graph_relational_vendor_data_model`, `multi_tenant_liquidity_isolation`, `schema_evolution_resilient_invoice_schema`, `probabilistic_three_way_matching`, `real_time_liquidity_aware_payment_scheduling`, `counterfactual_discount_analysis`, `temporal_cash_flow_forecasting`, `autonomous_exception_resolution`, `semantic_contract_to_invoice_alignment`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `ap_automation_vendor`

**Justification:** This owned table is part of the Accounts Payable Automation operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Vendor obligations, OCR intake, invoice matching, approval, and withholding.

**Improvement:** Extend `ap_automation_vendor` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `configuration_schema`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `ap_automation_vendor_site`

**Justification:** This owned table is part of the Accounts Payable Automation operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Vendor obligations, OCR intake, invoice matching, approval, and withholding.

**Improvement:** Extend `ap_automation_vendor_site` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `rule_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `ap_automation_vendor_bank_account`

**Justification:** This owned table is part of the Accounts Payable Automation operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Vendor obligations, OCR intake, invoice matching, approval, and withholding.

**Improvement:** Extend `ap_automation_vendor_bank_account` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `parameter_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `ap_automation_vendor_tax_profile`

**Justification:** This owned table is part of the Accounts Payable Automation operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Vendor obligations, OCR intake, invoice matching, approval, and withholding.

**Improvement:** Extend `ap_automation_vendor_tax_profile` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `vendor_master`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `ap_automation_vendor_risk_signal`

**Justification:** This owned table is part of the Accounts Payable Automation operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Vendor obligations, OCR intake, invoice matching, approval, and withholding.

**Improvement:** Extend `ap_automation_vendor_risk_signal` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `vendor_onboarding`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `ap_automation_purchase_order`

**Justification:** This owned table is part of the Accounts Payable Automation operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Vendor obligations, OCR intake, invoice matching, approval, and withholding.

**Improvement:** Extend `ap_automation_purchase_order` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `purchase_order_reference`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `ap_automation_purchase_order_line`

**Justification:** This owned table is part of the Accounts Payable Automation operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Vendor obligations, OCR intake, invoice matching, approval, and withholding.

**Improvement:** Extend `ap_automation_purchase_order_line` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `goods_receipt_reference`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `ap_automation_goods_receipt`

**Justification:** This owned table is part of the Accounts Payable Automation operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Vendor obligations, OCR intake, invoice matching, approval, and withholding.

**Improvement:** Extend `ap_automation_goods_receipt` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `receipt_line_reconciliation`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `ap_automation_goods_receipt_line`

**Justification:** This owned table is part of the Accounts Payable Automation operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Vendor obligations, OCR intake, invoice matching, approval, and withholding.

**Improvement:** Extend `ap_automation_goods_receipt_line` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `invoice_capture`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `ap_automation_invoice`

**Justification:** This owned table is part of the Accounts Payable Automation operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Vendor obligations, OCR intake, invoice matching, approval, and withholding.

**Improvement:** Extend `ap_automation_invoice` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `ocr_extraction`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `command_ap_vendors` a complete command lifecycle

**Justification:** High-value users need `command_ap_vendors` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ap_vendors` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `VendorOnboarded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `command_ap_vendor_bank_accounts` a complete command lifecycle

**Justification:** High-value users need `command_ap_vendor_bank_accounts` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ap_vendor_bank_accounts` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PurchaseOrderIssued`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `command_ap_vendor_tax_profiles` a complete command lifecycle

**Justification:** High-value users need `command_ap_vendor_tax_profiles` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ap_vendor_tax_profiles` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GoodsReceiptRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `command_ap_purchase_orders` a complete command lifecycle

**Justification:** High-value users need `command_ap_purchase_orders` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ap_purchase_orders` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `InvoiceCaptured`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `command_ap_goods_receipts` a complete command lifecycle

**Justification:** High-value users need `command_ap_goods_receipts` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ap_goods_receipts` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PaymentScheduled`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `command_ap_invoices` a complete command lifecycle

**Justification:** High-value users need `command_ap_invoices` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ap_invoices` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PaymentExecuted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `command_ap_invoices_invoice_id_match` a complete command lifecycle

**Justification:** High-value users need `command_ap_invoices_invoice_id_match` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ap_invoices_invoice_id_match` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `InvoiceExceptionResolved`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `command_ap_exceptions` a complete command lifecycle

**Justification:** High-value users need `command_ap_exceptions` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ap_exceptions` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `VendorRiskChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `command_ap_approval_tasks` a complete command lifecycle

**Justification:** High-value users need `command_ap_approval_tasks` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ap_approval_tasks` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DiscountOpportunityCaptured`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `command_ap_payment_schedules` a complete command lifecycle

**Justification:** High-value users need `command_ap_payment_schedules` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_ap_payment_schedules` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `VendorOnboarded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_invoice_lifecycle` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Accounts Payable Automation and measurably improves accuracy rate without hiding assumptions.

**Improvement:** Promote `event_sourced_invoice_lifecycle` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `accuracy_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `graph_relational_vendor_data_model` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Accounts Payable Automation and measurably improves close cycle time without hiding assumptions.

**Improvement:** Promote `graph_relational_vendor_data_model` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `close_cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `multi_tenant_liquidity_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Accounts Payable Automation and measurably improves cash impact without hiding assumptions.

**Improvement:** Promote `multi_tenant_liquidity_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cash_impact`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `schema_evolution_resilient_invoice_schema` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Accounts Payable Automation and measurably improves compliance exceptions without hiding assumptions.

**Improvement:** Promote `schema_evolution_resilient_invoice_schema` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `compliance_exceptions`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `probabilistic_three_way_matching` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Accounts Payable Automation and measurably improves vendor onboarded throughput without hiding assumptions.

**Improvement:** Promote `probabilistic_three_way_matching` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `vendor_onboarded_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `real_time_liquidity_aware_payment_scheduling` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Accounts Payable Automation and measurably improves purchase order issued throughput without hiding assumptions.

**Improvement:** Promote `real_time_liquidity_aware_payment_scheduling` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `purchase_order_issued_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `counterfactual_discount_analysis` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Accounts Payable Automation and measurably improves accuracy rate without hiding assumptions.

**Improvement:** Promote `counterfactual_discount_analysis` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `accuracy_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `temporal_cash_flow_forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Accounts Payable Automation and measurably improves close cycle time without hiding assumptions.

**Improvement:** Promote `temporal_cash_flow_forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `close_cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `autonomous_exception_resolution` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Accounts Payable Automation and measurably improves cash impact without hiding assumptions.

**Improvement:** Promote `autonomous_exception_resolution` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cash_impact`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic_contract_to_invoice_alignment` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Accounts Payable Automation and measurably improves compliance exceptions without hiding assumptions.

**Improvement:** Promote `semantic_contract_to_invoice_alignment` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `compliance_exceptions`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `AP_AUTOMATION_DATABASE_URL` and `AP_AUTOMATION_DATABASE_URL`

**Justification:** Complete Accounts Payable Automation coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `AP_AUTOMATION_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `AP_AUTOMATION_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `AP_AUTOMATION_EVENT_TOPIC` and `AP_AUTOMATION_EVENT_TOPIC`

**Justification:** Complete Accounts Payable Automation coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `AP_AUTOMATION_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `AP_AUTOMATION_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `AP_AUTOMATION_RETRY_LIMIT` and `AP_AUTOMATION_RETRY_LIMIT`

**Justification:** Complete Accounts Payable Automation coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `AP_AUTOMATION_RETRY_LIMIT` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `AP_AUTOMATION_RETRY_LIMIT` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `AP_AUTOMATION_DATABASE_URL` and `AP_AUTOMATION_DATABASE_URL`

**Justification:** Complete Accounts Payable Automation coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `AP_AUTOMATION_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `AP_AUTOMATION_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `AP_AUTOMATION_EVENT_TOPIC` and `AP_AUTOMATION_EVENT_TOPIC`

**Justification:** Complete Accounts Payable Automation coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `AP_AUTOMATION_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `AP_AUTOMATION_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `ApAutomationWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Accounts Payable Automation surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `ApAutomationWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `ApAutomationDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Accounts Payable Automation surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `ApAutomationDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `ApAutomationWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Accounts Payable Automation surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `ApAutomationWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `ApAutomationDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Accounts Payable Automation surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `ApAutomationDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `ApAutomationWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Accounts Payable Automation surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `ApAutomationWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /ap/vendors` and `VendorApproved`

**Justification:** Accounts Payable Automation must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /ap/vendors` and consumed event `VendorApproved` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /ap/vendor-bank-accounts` and `PurchaseOrderApproved`

**Justification:** Accounts Payable Automation must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /ap/vendor-bank-accounts` and consumed event `PurchaseOrderApproved` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /ap/vendor-tax-profiles` and `GoodsReceiptPosted`

**Justification:** Accounts Payable Automation must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /ap/vendor-tax-profiles` and consumed event `GoodsReceiptPosted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /ap/purchase-orders` and `TaxPolicyChanged`

**Justification:** Accounts Payable Automation must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /ap/purchase-orders` and consumed event `TaxPolicyChanged` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Accounts Payable Automation

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Accounts Payable Automation

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Accounts Payable Automation

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Accounts Payable Automation

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Accounts Payable Automation

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Accounts Payable Automation

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
