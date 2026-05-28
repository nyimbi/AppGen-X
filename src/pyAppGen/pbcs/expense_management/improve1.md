# Expense Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `expense_management`. Each item is specific to expense reports, expense lines, receipt artifacts, card transactions, merchant profiles, policy validation, approvals, reimbursements, cash advances, mileage, per diem, audit sampling, duplicate detection, spend controls, employee spend intelligence, agent assistance, and AppGen-X event reliability.

## Current Domain Evidence Used

- Domain purpose: expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence.
- Owned operational surface: expense reports, expense lines, receipt artifacts, card transactions, merchant profiles, expense policies, policy violations, approval tasks, reimbursement batches, reimbursement payments, cash advances, mileage claims, per diem claims, audit samples, duplicate expense signals, exception cases, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X runtime event tables.
- Declared operations: expense report creation, expense line capture, receipt attachment, card transaction ingestion, card/receipt matching, policy validation, policy violation opening, approval routing, report approval, reimbursement batching, reimbursement execution, cash advance recording, mileage calculation, per diem calculation, audit sampling, duplicate detection, exception resolution, and expense rule compilation.
- Declared events and integrations: emits `ExpenseReportCreated`, `ExpensePolicyViolationOpened`, `ExpenseApproved`, `ReimbursementScheduled`, `ExpenseAuditSampled`, and `DuplicateExpenseDetected`; consumes `EmployeeCreated`, `CardTransactionPosted`, `PaymentExecuted`, and `PolicyChanged`; catalog traceability also includes employee, payment, access policy, reimbursement, and fraud-flag events.
- Advanced capability evidence: semantic receipt extraction, probabilistic duplicate detection, counterfactual policy coaching, continuous spend control testing, risk-based audit sampling, carbon-aware travel expense insights, event-sourced operational history, multi-tenant policy isolation, anomaly detection, predictive risk scoring, scenario simulation, cryptographic audit proofs, cross-PBC event federation, and governed agent execution.

## 50 Better-Than-World-Class Improvements

### 1. Expense report readiness gate

**Justification:** Reports submitted with missing employee context, incomplete lines, unmatched card transactions, absent receipts, stale policy, or invalid approver chains create payment delays and audit risk.

**Improvement:** Add a readiness gate that verifies employee projection, report period, currency, business purpose, line completeness, receipt requirements, card match state, policy version, approver eligibility, and exception status before submission.

### 2. Report lifecycle state machine

**Justification:** Expense reports move through draft, submitted, returned, policy review, manager approval, audit review, approved, reimbursement scheduled, paid, rejected, withdrawn, and reopened states.

**Improvement:** Implement a strict lifecycle state machine with allowed transitions, required evidence, owner, timestamp, notification, and reimbursement effects. Release tests should reject reimbursement actions before approval.

### 3. Expense line category intelligence

**Justification:** Correct categorization drives policy rules, tax handling, reimbursement, analytics, carbon estimates, and approval routing.

**Improvement:** Add category intelligence using merchant profile, receipt text, card metadata, location, employee role, project code, and historical patterns. Store confidence, policy implications, and human override rationale.

### 4. Business purpose quality scoring

**Justification:** Weak business-purpose text makes legitimate expenses hard to audit and suspicious expenses hard to challenge.

**Improvement:** Score business purpose for specificity, customer/project linkage, attendee detail, trip linkage, policy-required details, and generic phrasing. The agent should propose stronger purpose text from receipts, calendar/travel projections, and user instructions.

### 5. Receipt artifact evidence chain

**Justification:** Receipts prove spend, but screenshots, email forwards, images, PDFs, and uploads can be duplicated, altered, incomplete, or unrelated.

**Improvement:** Add receipt fingerprints, source metadata, OCR extraction, image/PDF integrity checks, attachment lineage, duplicate artifact detection, and redaction status. Link receipt facts to expense lines with confidence and reviewer notes.

### 6. Semantic receipt extraction

**Justification:** Manual entry is slow and error-prone, while raw OCR does not reliably identify merchant, tax, tip, currency, date, attendees, or line items.

**Improvement:** Extract structured receipt fields with confidence per field, line-item details, tax/tip/service charges, payment method, currency, merchant, date/time, and anomaly flags. Require confirmation for low-confidence or policy-sensitive fields.

### 7. Receipt-to-card matching

**Justification:** Card transactions and receipts often differ due to tips, currency conversion, delayed posting, split payments, and merchant name variation.

**Improvement:** Match receipts to card transactions using amount tolerances, date windows, merchant aliases, currency conversion, location, authorization/posting dates, and tip detection. Store match confidence, alternatives, and mismatch reason.

### 8. Card transaction feed governance

**Justification:** Card feeds may contain duplicates, reversals, pending authorizations, late postings, missing employee links, or disputed transactions.

**Improvement:** Add card-feed controls for idempotency, authorization/posting lifecycle, reversal detection, employee assignment, merchant normalization, dispute flags, and dead-letter handling. UI should separate pending, posted, reversed, and disputed transactions.

### 9. Merchant profile enrichment

**Justification:** Merchant identity affects category, risk, prohibited spend, tax, location, and duplicate detection.

**Improvement:** Maintain merchant profiles with aliases, category codes, risk flags, preferred category, region, tax treatment, policy notes, and historical violation rates. Use profiles in line classification and policy validation.

### 10. Expense policy versioning

**Justification:** Expense policy changes must not retroactively alter previously valid reports unless explicitly migrated.

**Improvement:** Version policies with effective dates, employee groups, regions, categories, thresholds, receipt rules, approval requirements, and compiled hashes. Each report and line should store the policy version evaluated.

### 11. Policy rule compiler

**Justification:** Expense policies are often written in human language with exceptions, thresholds, travel classes, locations, and role-specific rules.

**Improvement:** Compile structured and document-sourced policy rules into executable predicates with test cases, ambiguity flags, effective dates, and approver evidence. The agent should highlight unclear policy wording before activation.

### 12. Counterfactual policy coaching

**Justification:** Employees should learn how to make compliant choices before submitting expenses, not only after violations are opened.

**Improvement:** Add coaching simulations that explain which policy rule would pass, fail, or require receipt/approval under alternative amount, category, merchant, route, or travel-class choices.

### 13. Policy violation lifecycle

**Justification:** Violations require consistent handling across warning, exception request, manager override, audit hold, rejection, reimbursement reduction, or fraud review.

**Improvement:** Add violation states, severity, rule version, impacted amount, approver, exception evidence, employee response, and resolution outcome. Link violations to approval tasks and audit samples.

### 14. Exception request workflow

**Justification:** Some policy exceptions are legitimate due to emergencies, customer needs, accessibility requirements, or preapproved business events.

**Improvement:** Add exception requests with reason taxonomy, supporting evidence, approver role, amount impact, precedent checks, expiration, and audit visibility. The agent should draft exception explanations without bypassing approval.

### 15. Approval routing graph

**Justification:** Expense approvals depend on amount, category, project, cost center, employee level, policy violation, cash advance, and audit risk.

**Improvement:** Build approval routing graphs with manager, project owner, finance, compliance, audit, and executive nodes. Store routing rationale, skipped approvers, delegation, out-of-office handling, and escalation timers.

### 16. Segregation-of-duty controls

**Justification:** Employees should not approve their own expenses, subordinate exceptions where prohibited, or reimbursement batches they influence.

**Improvement:** Add segregation checks for submitter, approver, delegate, card owner, payment preparer, and auditor. Block or escalate conflicted approvals and preserve conflict evidence.

### 17. Approval SLA and escalation

**Justification:** Slow approvals delay reimbursement and obscure close accruals.

**Improvement:** Track approval SLA by policy, employee group, amount, and reimbursement cycle. Auto-escalate overdue tasks, notify owners, and show bottlenecks by approver and category.

### 18. Reimbursement batch readiness

**Justification:** Reimbursements should not be batched until reports are approved, payment details are valid, advances are netted, holds are clear, and employee status is active.

**Improvement:** Add batch readiness checks for approval, duplicate/fraud flags, cash advance offsets, currency, payment projection, employee eligibility, tax treatment, and cutoff period. Generate a batch proof before payment handoff.

### 19. Reimbursement payment reconciliation

**Justification:** Expense reimbursement must reconcile scheduled, executed, failed, reversed, and partially paid payments.

**Improvement:** Consume payment execution events through declared AppGen-X handlers, update reimbursement status, classify failures, support retry, and link payment evidence to reports. Store reconciliation deltas for audit.

### 20. Cash advance lifecycle

**Justification:** Cash advances need issuance, usage, reconciliation, unused balance return, overdue follow-up, and policy exception handling.

**Improvement:** Add advance states, issued amount, expected use, linked reports, applied amounts, returned funds, aging, employee communication, and write-off policy. Block reimbursement where advances must be netted.

### 21. Mileage route validation

**Justification:** Mileage claims are prone to inflated distances, repeated routes, commute inclusion, and incorrect rates.

**Improvement:** Validate mileage using origin/destination, date, business purpose, route distance, commute deduction, rate version, vehicle type, and duplicate route checks. Store route evidence and policy exceptions.

### 22. Per diem eligibility engine

**Justification:** Per diem depends on location, travel dates, partial days, meals provided, role, policy, currency, and local rules.

**Improvement:** Add per diem calculations with location tables, meal deductions, partial-day factors, overnight requirements, employee eligibility, and effective-rate versions. Explain every deduction and generated amount.

### 23. Attendee and hospitality governance

**Justification:** Meals and entertainment often require attendees, business relationship, limits, and compliance checks.

**Improvement:** Add attendee capture with names, organizations, roles, customer/prospect linkage, employee count, per-person spend, prohibited party checks, and purpose evidence. Block incomplete hospitality lines above threshold.

### 24. Travel expense linkage

**Justification:** Travel expenses make more sense when connected to trips, bookings, itineraries, events, and travel-policy approvals.

**Improvement:** Link expense lines to declared travel projections for flights, hotels, rides, meals, and trip approvals. Flag expenses outside travel dates, locations, policy class, or booking source.

### 25. Carbon-aware travel spend insights

**Justification:** Expense data can help organizations understand travel emissions without making employees manually compute them.

**Improvement:** Estimate emissions for mileage, flights, rides, hotels, and travel categories using route and category evidence. Provide carbon summaries, alternatives, and policy coaching where configured.

### 26. Duplicate expense detection

**Justification:** Duplicates occur across receipts, card transactions, reports, cash claims, split bills, and resubmissions.

**Improvement:** Use probabilistic matching on amount, date, merchant, receipt fingerprint, employee, attendees, location, card transaction, and semantic description. Store match candidates, confidence, and reviewer disposition.

### 27. Fraud and abuse signal modeling

**Justification:** Expense abuse includes altered receipts, personal spend, merchant collusion, repeated exceptions, weekend spend, duplicate claims, and category manipulation.

**Improvement:** Add fraud signals with explainable drivers, severity, policy links, employee history, merchant risk, and case routing. Keep model recommendations separate from approved disciplinary actions.

### 28. Risk-based audit sampling

**Justification:** Random sampling misses high-risk behavior while overburdening low-risk employees.

**Improvement:** Sample expenses using amount, category, policy violations, employee history, merchant risk, duplicate signals, receipt confidence, project risk, and statistical coverage requirements. Store sampling rationale and audit outcome feedback.

### 29. Audit sample workbench

**Justification:** Auditors need structured review of receipts, policy, approvals, payments, exceptions, and employee explanations.

**Improvement:** Build an audit workbench with evidence checklist, pass/fail decisions, findings, required corrections, reimbursement impact, employee response, and closure evidence. Track repeat findings and control weaknesses.

### 30. Spend control dashboard

**Justification:** Finance needs visibility into spend trends, policy leakage, reimbursement backlog, merchant concentration, and high-risk categories.

**Improvement:** Add dashboards by employee, department, project, category, merchant, region, policy version, and payment status. Include budget alerts, anomaly trends, and control exceptions.

### 31. Employee spend intelligence

**Justification:** Employees need personalized guidance on policy, missing receipts, upcoming deadlines, rejected items, and reimbursement timing.

**Improvement:** Provide employee-facing intelligence cards for open reports, unmatched card transactions, missing receipts, violations, required approvals, expected reimbursement date, cash advance aging, and coaching suggestions.

### 32. Mobile receipt capture workflow

**Justification:** Receipt capture should happen at spend time, while context is fresh and before receipts are lost.

**Improvement:** Add mobile capture states for offline upload, image quality, duplicate artifact, OCR confidence, card match suggestion, category suggestion, and policy warning. Store upload evidence and sync conflict handling.

### 33. Receipt redaction and privacy

**Justification:** Receipts may contain personal items, health data, card fragments, loyalty IDs, or unrelated customer information.

**Improvement:** Detect sensitive receipt content, suggest redactions, preserve original access controls, and store redacted versions for approvers where allowed. Agent summaries must avoid exposing irrelevant sensitive details.

### 34. Project and cost allocation splitting

**Justification:** One expense may need allocation across projects, grants, departments, customers, or cost centers.

**Improvement:** Add split allocations with percentages/amounts, validation totals, approver routing by split owner, policy rules per segment, and reimbursement/payment neutrality. Store split rationale and audit trail.

### 35. Multi-currency expense controls

**Justification:** International expenses involve transaction currency, reimbursement currency, card settlement currency, FX rates, and rounding.

**Improvement:** Add currency controls for receipt amount, card amount, employee claim amount, reimbursement amount, rate source, rate date, spread, and rounding. Explain differences and flag suspicious FX claims.

### 36. Tax and recoverability capture

**Justification:** Expense receipts may include recoverable taxes or jurisdiction-specific tax evidence.

**Improvement:** Extract tax amounts, tax IDs, jurisdiction, recoverability category, receipt validity, and missing-tax evidence. Provide tax reporting exports through owned tables and declared integrations only.

### 37. Spend accrual readiness

**Justification:** Finance needs visibility into incurred but not reimbursed expenses for close.

**Improvement:** Add accrual views for submitted, approved, unsubmitted card, matched receipt, cash advance, and pending reimbursement expenses. Include confidence levels and cutoff evidence.

### 38. Policy change impact analysis

**Justification:** Changing thresholds, receipt rules, mileage rates, or approval limits can affect employees, controls, and reimbursement timing.

**Improvement:** Simulate policy changes against historical reports and open drafts to estimate violation rate, audit load, reimbursement delay, spend reduction, and employee impact. Require approval for material policy changes.

### 39. Continuous expense control testing

**Justification:** Expense controls should run continuously rather than waiting for manual audits.

**Improvement:** Add controls for missing receipts, expired policy versions, approval conflicts, duplicate signals, card-feed gaps, reimbursement before approval, stale advances, and high-risk merchants. Store assertion results and remediation tasks.

### 40. Expense anomaly detection

**Justification:** Sudden spend spikes, new merchants, repeated exceptions, weekend transactions, and unusual category shifts may indicate misuse or process defects.

**Improvement:** Detect anomalies by employee, merchant, category, project, region, amount, time, and policy version. Route high-risk anomalies to audit samples or exception cases with explainable drivers.

### 41. Exception case workflow

**Justification:** Expense issues such as missing receipt, disputed card charge, duplicate claim, rejected reimbursement, or cash advance shortage require structured resolution.

**Improvement:** Add exception cases with type, severity, owner, SLA, linked report/line/payment, required evidence, employee response, resolution action, and financial impact. Provide agent-prepared resolution plans for approval.

### 42. Cryptographic expense proof

**Justification:** Auditors and employees may need proof that expense reports, receipts, approvals, reimbursements, and policy decisions were not altered.

**Improvement:** Generate hash-chain proofs for report lifecycle, receipt artifacts, policy evaluation, approvals, reimbursement batches, payment reconciliation, and audit samples. Provide redacted verifier exports.

### 43. AppGen-X event reliability proof

**Justification:** Expense management depends on employee, card, payment, and policy events; lost or duplicate events create reimbursement and audit errors.

**Improvement:** Harden event descriptors with schema versions, idempotency keys, ordering assumptions, retry envelopes, dead-letter taxonomy, replay eligibility, and handler evidence. Include tests for duplicate card posts and failed payment callbacks.

### 44. Cross-PBC boundary proof

**Justification:** Expense processing must use employee, card, payment, policy, travel, project, and finance context without direct foreign-table access.

**Improvement:** Generate a boundary proof listing each declared API, projection, event, cached field, staleness policy, and retention rule. Release audits should fail undeclared employee, payment, travel, or project table access.

### 45. Agent-assisted receipt and report creation

**Justification:** Employees benefit from AI help turning receipts, emails, itineraries, and instructions into compliant expense drafts.

**Improvement:** Let the PBC agent extract expense lines, match card transactions, suggest categories, identify missing facts, draft business purposes, and preview policy outcomes. It should require confirmation before creating or submitting reports.

### 46. Agent-assisted approver review

**Justification:** Approvers need concise evidence and policy context without reading every receipt manually.

**Improvement:** Provide approver summaries showing policy status, violations, unusual items, duplicate signals, receipt confidence, history, and recommended questions. The agent must not approve or reject without explicit authorized action.

### 47. UI capability surface proof

**Justification:** A complete Expense Management PBC must expose its domain operations in usable UI surfaces.

**Improvement:** Add release checks proving UI coverage for reports, lines, receipts, card transactions, merchants, policies, violations, approvals, reimbursements, payments, advances, mileage, per diem, audits, duplicates, exceptions, rules, parameters, controls, models, events, analytics, and agent tools.

### 48. Expense resilience drills

**Justification:** Expense operations must recover from card feed outages, receipt extraction failures, payment callback delays, policy deployment errors, and dead-letter surges.

**Improvement:** Add resilience drills for delayed card transactions, duplicate feed replay, failed OCR, invalid policy rollout, payment failure events, reimbursement replay, and dead-letter recovery. Store recovery time, affected reports, and financial exposure.

### 49. Expense readiness score

**Justification:** Operators need a concise signal showing whether the PBC is ready for production expense operations in a composed app.

**Improvement:** Compute readiness from policy coverage, receipt extraction quality, card feed health, approval routing, reimbursement reconciliation, audit controls, event health, UI coverage, boundary proof, and agent safety. Show blocking gaps and remediation actions.

### 50. End-to-end expense release proof

**Justification:** A world-class Expense Management PBC needs one evidence package proving that spend can flow from receipt/card intake through policy, approval, reimbursement, audit, and analytics safely.

**Improvement:** Create an end-to-end proof exercising report creation, line capture, receipt extraction, card ingestion, match, policy validation, violation handling, approval routing, reimbursement batching, payment reconciliation, cash advance, mileage, per diem, duplicate detection, audit sampling, exception resolution, rule compilation, UI coverage, AppGen-X eventing, boundary verification, and agent-safe CRUD planning.
