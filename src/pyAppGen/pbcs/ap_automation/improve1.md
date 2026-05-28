# Accounts Payable Automation PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `ap_automation`. The items are specific to accounts payable operations: vendor onboarding, invoice capture, two-way and three-way matching, tax/withholding, approvals, fraud controls, payment scheduling, discounts, vendor reconciliation, and agent-assisted AP work.

## Current Domain Evidence Used

- Domain purpose: vendor onboarding, vendor bank/tax profiles, PO/receipt references, invoice capture, e-invoice ingestion, matching, contract compliance, exceptions, approval policy, tax validation, withholding, payment scheduling/execution, remittance, discount optimization, vendor statement reconciliation, vendor risk, and AP workbench evidence.
- Owned boundary: vendors, vendor sites, bank accounts, tax profiles, risk signals, purchase orders, PO lines, goods receipts, receipt lines, invoices, invoice lines, capture artifacts, match results, payments, payment batches, rail decisions, discount opportunities, vendor statements, withholding tax, e-invoice submissions, exception cases, approval tasks, cash forecast projections, rules, parameters, schema extensions, controls, governed models, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: vendor, bank, tax, PO, receipt, invoice, invoice match, exception, approval, payment schedule, batch, payment, discount, statement, withholding, e-invoice, configuration, rules, parameters, and workbench operations.
- Existing events and dependencies: emits vendor, PO, receipt, invoice, payment, exception, risk, and discount events; integrates with GL, treasury, tax, procurement, workflow, identity, schema registry, audit ledger, and gateway only through APIs, AppGen-X events, and local projections.

## 50 Better-Than-World-Class Improvements

### 1. Vendor onboarding evidence pack

**Justification:** AP risk starts at vendor setup. A vendor record without ownership, tax, banking, screening, approval, and change evidence is a payment-fraud and compliance weakness.

**Improvement:** Add a vendor onboarding evidence pack with beneficial owner proof, tax profile, bank validation, site verification, sanctions/screening result, payment terms, approver trail, and activation decision. The workbench should block payment-enabled status until mandatory evidence passes.

### 2. Vendor master lifecycle and change control

**Justification:** Vendor changes, especially bank and remit-to changes, are high-risk events requiring stronger controls than ordinary profile edits.

**Improvement:** Model vendor lifecycle states and change requests for name, tax identity, site, terms, bank, remit-to, and hold status. Require reason, independent approval, effective date, duplicate check, and AppGen-X audit evidence for material changes.

### 3. Beneficial ownership and related-party graph

**Justification:** Duplicate vendors, related parties, shell suppliers, and conflicts of interest often hide behind separate vendor records.

**Improvement:** Build a vendor relationship graph over beneficial owners, addresses, bank fingerprints, tax identifiers, contacts, and employee/approver projections. Flag related-party risks and require enhanced approval before invoice payment.

### 4. Vendor bank account validation workflow

**Justification:** Payment fraud frequently occurs through bank account substitution or unverified payment credentials.

**Improvement:** Add bank validation states for submitted, independently verified, micro-test pending, active, suspended, and retired. Store tokenized account evidence, verification method, approver independence, rail compatibility, and last-use proof.

### 5. Payment hold and release governance

**Justification:** AP needs precise holds for vendor risk, invoice dispute, tax failure, duplicate concern, liquidity freeze, or legal instruction.

**Improvement:** Add hold records with scope, reason, owner, expiry, affected invoices/payments, release requirements, and audit trail. Payment scheduling should explain every hold and prevent hidden bypass.

### 6. Vendor tax profile completeness gate

**Justification:** Incorrect tax and withholding setup creates regulatory exposure and rework.

**Improvement:** Validate jurisdiction, registration identifiers, exemption certificate, withholding code, expiry date, treaty basis, and proof hash before invoices can be tax-cleared. Add alerts for expiring or inconsistent certificates.

### 7. E-invoice jurisdiction compliance matrix

**Justification:** E-invoicing rules differ by jurisdiction, format, clearance model, and response state.

**Improvement:** Add jurisdiction matrices for required invoice fields, submission timing, clearance response, cancellation/amendment behavior, archival proof, and tax authority acknowledgement. Block payment for invoices requiring clearance until accepted evidence exists.

### 8. Multi-channel invoice capture normalization

**Justification:** AP receives invoices by portal, email, OCR document, e-invoice network, supplier upload, and API; inconsistent intake creates duplicates and missing evidence.

**Improvement:** Normalize every capture artifact into a canonical invoice intake record with channel, source hash, extraction confidence, original reference, sender identity, duplicate candidates, and document retention policy.

### 9. OCR and extraction confidence governance

**Justification:** Automated extraction must not silently accept low-confidence vendor, amount, tax, PO, or bank fields.

**Improvement:** Track field-level confidence, source coordinates, extraction model version, human corrections, and downstream match impact. Route low-confidence fields to review and use corrections as governed model feedback.

### 10. Semantic invoice-to-contract alignment

**Justification:** Matching only PO and receipt data misses contractual terms, service periods, price escalators, caps, and penalty clauses.

**Improvement:** Add contract-term extraction and alignment for billing period, rate card, discounts, service level credits, tax jurisdiction, and payment terms. Store semantic evidence and exception reasons when invoice terms diverge from contract terms.

### 11. Two-way and three-way match policy compiler

**Justification:** Matching rules vary by vendor, category, amount, service/goods type, tolerance, tax, freight, and receiving status.

**Improvement:** Compile match policies with tolerance bands, quantity/price variance, receipt requirement, service acceptance, tax/freight handling, and exception routing. Each rule version should include fixtures and impact simulation.

### 12. Probabilistic match explanation

**Justification:** Probabilistic matching is only useful if AP specialists can understand why an invoice matched or failed.

**Improvement:** Store candidate PO/receipt lines, match weights, confidence, conflicting evidence, missing fields, and final decision. The UI should show side-by-side invoice, PO, receipt, and contract evidence with suggested resolution.

### 13. Service invoice acceptance workflow

**Justification:** Services often lack goods receipts and need service-period, milestone, timesheet, or deliverable acceptance.

**Improvement:** Add service acceptance records linked to invoice lines, period, approver, deliverable evidence, milestone state, and partial acceptance. Match policies should support two-way, service acceptance, and contract milestone modes.

### 14. Freight, tax, and miscellaneous charge matching

**Justification:** Non-item charges frequently cause exceptions and leakage when not handled by explicit rules.

**Improvement:** Add charge classification, allowed variance, allocation basis, tax treatment, freight terms, and approval policy for non-PO line charges. Route unusual charges to exception cases with suggested account assignment.

### 15. Duplicate invoice detection across weak signals

**Justification:** Duplicate invoices can vary by invoice number formatting, vendor site, amount, date, currency, and capture channel.

**Improvement:** Add duplicate scoring using normalized invoice number, vendor graph, amount, currency, date, PO, source hash, bank account, and line similarity. Require explicit override with reason and approver for high-score duplicates.

### 16. Credit memo and debit memo lifecycle

**Justification:** Payables operations include credits, debit memos, short-pay, overpayment recovery, and supplier adjustments.

**Improvement:** Add memo records with original invoice link, reason, amount, tax impact, open balance, application policy, and GL handoff. Payment scheduling should net eligible credits and explain unapplied memos.

### 17. Invoice exception case management

**Justification:** Exceptions need owner, cause, evidence, SLA, supplier communication, resolution, and close proof, not just a status.

**Improvement:** Expand exception cases with category, root cause, affected invoice lines, owner, supplier contact, required evidence, SLA, escalation, resolution action, and recurrence flag. The agent should draft resolution steps and supplier messages.

### 18. Approval route optimization with SoD

**Justification:** Approval delays hurt discounts and vendor relationships, but approvals must preserve authority and segregation of duties.

**Improvement:** Add approval routing based on amount, account assignment, requester, vendor risk, PO owner, project, cost center, and SoD constraints. Store routing rationale, skipped approvers, delegation, and escalation evidence.

### 19. Delegation and out-of-office handling

**Justification:** AP approvals often stall when approvers are unavailable.

**Improvement:** Add delegation policies with valid dates, scope, limits, SoD checks, and emergency fallback. Approval tasks should reroute before SLA breach while preserving independent approval evidence.

### 20. Dynamic discount capture strategy

**Justification:** Early payment discounts require balancing discount value, cash availability, payment risk, and supplier priority.

**Improvement:** Add discount decisioning that compares discount yield, cash forecast projection, treasury liquidity buffer, payment rail cost, vendor risk, and alternative cash use. Store accepted and rejected opportunities with financial rationale.

### 21. Payment scheduling with liquidity constraints

**Justification:** AP payment plans must respect due dates, discounts, cash forecasts, holds, priority suppliers, and payment limits.

**Improvement:** Build a scheduler that ranks invoices by due date, discount net benefit, vendor criticality, cash projection, currency, rail cutoff, and hold status. Provide what-if scenarios for delaying, accelerating, or batching payments.

### 22. Payment batch approval and release control

**Justification:** Payment batches concentrate financial risk and require control over composition, approval, and release.

**Improvement:** Add batch controls for amount, currency, rail, vendor risk, duplicate checks, approver independence, release window, and settlement proof. UI should show every invoice included, excluded, or held.

### 23. Payment rail selection and failover

**Justification:** Payment route choice affects cost, settlement speed, risk, cutoff times, and resilience.

**Improvement:** Add rail scoring across cost, latency, currency, vendor capability, bank validation, fraud risk, carbon window, and outage state. Store failover decisions and require approval when route changes after batch approval.

### 24. Remittance advice lifecycle

**Justification:** Suppliers need clear remittance details to reconcile payments and reduce disputes.

**Improvement:** Add remittance advice records with payment, invoices, credits, deductions, tax withheld, currency, delivery channel, delivery proof, and supplier acknowledgement. Support regenerated advice with correction evidence.

### 25. Vendor statement reconciliation

**Justification:** Supplier statements reveal missing invoices, unapplied credits, duplicate payments, disputes, and aging errors.

**Improvement:** Add statement ingestion, line matching, missing-document detection, disputed balance cases, aging comparison, and settlement proposals. Workbench should show vendor statement reconciliation by vendor/site/period.

### 26. Withholding tax calculation and certificate expiry

**Justification:** Withholding depends on jurisdiction, vendor status, certificate validity, service type, treaty, and payment date.

**Improvement:** Add withholding decision records with tax profile, rate, base amount, exemption proof, certificate expiry, payment timing, and remittance obligation. Block payment when withholding evidence is missing or expired.

### 27. Tax engine handoff proof

**Justification:** AP should not own tax law globally, but it must prove it asked tax services correctly and applied returned decisions.

**Improvement:** Store tax API request/response digests, schema version, tax decision, line allocation, override, and proof hash. Reconcile invoice tax, withholding, and payment remittance against this evidence.

### 28. GL accrual and liability handoff

**Justification:** AP invoices create liabilities, accruals, expenses, prepaids, and reversals that must be traceable to GL without shared tables.

**Improvement:** Add GL handoff records for invoice accrual, liability recognition, payment clearing, discount taken, tax withheld, and reversal events. Validate account assignments and emit AppGen-X events with idempotency evidence.

### 29. Accrual for received-not-invoiced items

**Justification:** Goods and services received but not invoiced must be accrued for accurate close.

**Improvement:** Add uninvoiced receipt/service accrual proposals with PO/receipt evidence, expected amount, account assignment, reversal policy, and GL handoff. Close workbench should expose unaccrued receipt risk.

### 30. Prepayment and advance management

**Justification:** AP often manages deposits, advances, prepayments, amortization, and application to future invoices.

**Improvement:** Add prepayment records with supplier, purpose, contract/PO link, approval, remaining balance, application rules, amortization schedule, and reconciliation evidence.

### 31. Supplier financing and reverse factoring

**Justification:** AP may offer early payment through financing programs that affect discount economics, supplier cash flow, and treasury exposure.

**Improvement:** Add financing offers, supplier election, funding source, fee, advance amount, settlement date, and accounting handoff. Simulate buyer/supplier benefit and treasury impact before execution.

### 32. Fraud pattern detection

**Justification:** AP is a high-value fraud target through fake vendors, changed bank accounts, duplicate invoices, split invoices, and unusual approval paths.

**Improvement:** Add fraud signals for vendor-bank changes, invoice-number patterns, payment timing, split amounts, approver anomalies, duplicate clusters, and outlier suppliers. Each finding should create an explainable risk signal or payment hold.

### 33. Split invoice and threshold avoidance detection

**Justification:** Fraud or policy avoidance can appear as multiple invoices just below approval thresholds.

**Improvement:** Detect invoice clusters by vendor, requester, PO, date range, amount, account assignment, and approver. Route suspected splits to enhanced approval with evidence.

### 34. Vendor risk scoring governance

**Justification:** Vendor risk scores influence holds and payments, so they must be explainable and controlled.

**Improvement:** Govern risk models with feature lineage, source signals, drift checks, deterministic fallback, override reasons, and review cadence. Display risk contributors and recommended controls in vendor views.

### 35. Supplier communication workspace

**Justification:** AP exceptions and statements require controlled communication with suppliers.

**Improvement:** Add communication records linked to invoices, statements, exceptions, and payments with template, channel, recipient, sent proof, reply summary, and next action. The agent should draft messages from owned evidence.

### 36. Vendor portal task queue

**Justification:** Suppliers can resolve missing tax forms, invoice disputes, statement mismatches, and bank verification without internal AP rework.

**Improvement:** Add supplier-facing task descriptors with evidence request, due date, secure upload, validation status, and AP review outcome. Keep portal state inside AP-owned tables or declared APIs.

### 37. AP close cockpit

**Justification:** Month-end AP close requires open invoice, accrual, payment, tax, statement, and exception visibility.

**Improvement:** Add close dashboards for unmatched invoices, pending approvals, held payments, uninvoiced receipts, withholding exceptions, vendor statement differences, and GL handoff status by period and entity.

### 38. Aging and working-capital analytics

**Justification:** AP affects cash, supplier relationships, and working capital.

**Improvement:** Add aging analytics by vendor, category, entity, due date, discount status, hold reason, and payment priority. Show working-capital impact of payment scenarios and overdue risk.

### 39. Payment recovery and overpayment management

**Justification:** Overpayments, duplicate payments, and credits require recovery workflows.

**Improvement:** Add recovery cases with source invoice/payment, vendor contact, recovery method, expected amount, settlement status, write-off approval, and GL adjustment evidence.

### 40. Cash forecast feedback loop

**Justification:** Treasury forecasts depend on AP schedules, and AP schedules depend on treasury liquidity.

**Improvement:** Publish payment commitments and consume cash forecast projections with freshness checks. Track forecast accuracy by scheduled vs executed payments and expose stale forecast risk.

### 41. Cross-border payment compliance

**Justification:** International payments require currency, beneficiary, bank, sanctions, tax, document, and remittance controls.

**Improvement:** Add cross-border payment requirements by country/currency/rail, including beneficiary validation, documentary proof, FX quote, withholding, sanction check, and settlement trace.

### 42. Payment execution idempotency ledger

**Justification:** Duplicate payment execution is a severe AP failure.

**Improvement:** Add an idempotency ledger for payment schedules, batch release, rail submission, settlement callback, and remittance generation. Duplicate calls should return prior result and never create duplicate payments.

### 43. Dead-letter and payment failure recovery

**Justification:** Failed events or payment callbacks can leave invoices, batches, and GL handoffs inconsistent.

**Improvement:** Build recovery workbench for failed AppGen-X events, rejected payment submissions, settlement mismatches, and stale callbacks. Provide replay simulation, duplicate-payment risk check, and corrective event generation.

### 44. Agent-safe invoice ingestion

**Justification:** The AP chatbot should help ingest invoices and documents, but it must not create payable liabilities blindly.

**Improvement:** Require agent ingestion previews with extracted fields, source citations, confidence, duplicate candidates, tax/match status, suggested coding, and required human review. Low-confidence or high-risk invoices should remain draft.

### 45. Agent-safe payment actions

**Justification:** Payment scheduling and release are financially material actions that require strong confirmation.

**Improvement:** Define agent payment competencies that can analyze, draft, and simulate schedules but require explicit approval for holds, batch creation, release, rail failover, or payment cancellation. Previews should show cash, discount, risk, and duplicate impact.

### 46. AP rules and parameter simulation

**Justification:** Match thresholds, approval limits, discount floors, risk thresholds, and liquidity buffers can materially alter operations.

**Improvement:** Add simulation for rule/parameter changes against historical invoices and open work. Show changes in auto-match rate, exceptions, approval workload, discounts captured, payments delayed, and fraud holds.

### 47. Workbench surface for all AP capabilities

**Justification:** AP specialists need operational views, not hidden backend commands.

**Improvement:** Expand UI into vendor onboarding, bank verification, tax profile, invoice capture, match cockpit, exception board, approval queue, payment scheduler, batch release, discount dashboard, statement reconciliation, close cockpit, fraud/risk panel, and agent assistant.

### 48. Boundary proof for AP-only ownership

**Justification:** AP must integrate with procurement, treasury, tax, GL, workflow, identity, and audit without reading their operational tables.

**Improvement:** Add static/runtime checks proving every AP command touches only AP-owned tables plus declared APIs/events/projections. Include failing fixtures for direct foreign-table references.

### 49. AP release readiness score

**Justification:** Users need a concise but defensible view of whether AP is ready for production use.

**Improvement:** Compute readiness from vendor evidence, bank validation, tax completeness, invoice capture confidence, match automation, exception aging, approval SoD, payment idempotency, GL/tax/treasury handoff, fraud controls, UI coverage, and agent safety.

### 50. End-to-end procure-to-pay trace

**Justification:** AP excellence depends on tracing obligations from purchase order to receipt, invoice, approval, payment, remittance, tax, GL, and vendor statement.

**Improvement:** Build an end-to-end trace view using AP-owned records and declared projections, showing every state transition, event, control, exception, and financial handoff. The agent should answer procure-to-pay status questions from this trace.
