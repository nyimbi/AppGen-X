# Grant and Fund Accounting PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `grant_fund_accounting`. Each item is specific to grant awards, fund restrictions, grant budgets, allowable costs, cost transactions, allocations, drawdowns, receipts, match requirements, match contributions, funder reporting, milestones, compliance evidence, closeout, grant exceptions, funder-ready controls, agent assistance, and AppGen-X event reliability.

## Current Domain Evidence Used

- Domain purpose: grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls.
- Owned operational surface: grant awards, grant funds, fund restrictions, grant budgets, budget lines, allowable cost rules, cost transactions, cost allocations, drawdown requests, drawdown receipts, match requirements, match contributions, funder reports, reporting milestones, compliance evidence, grant closeouts, exception cases, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X runtime event tables.
- Declared operations: grant award creation, fund restriction definition, grant budget opening, budget line capture, allowable cost rule registration, grant cost recording, cost allocation, drawdown request preparation, drawdown receipt recording, match requirement tracking, match contribution recording, funder report building, reporting milestone tracking, compliance evidence attachment, grant closeout, exception resolution, grant rule compilation, and funding shortfall simulation.
- Declared events and integrations: emits `GrantAwardCreated`, `GrantBudgetApproved`, `GrantCostRecorded`, `DrawdownRequested`, `FunderReportSubmitted`, and `GrantExceptionOpened`; consumes `JournalPosted`, `PaymentExecuted`, `PolicyChanged`, and `AuditProofGenerated`; catalog traceability also includes expense, payment, restriction, reimbursement, compliance, and audit events.
- Advanced capability evidence: restriction-aware cost validation, drawdown cash simulation, semantic award document extraction, continuous funder compliance testing, cryptographic evidence packets, multi-funder portfolio forecasting, event-sourced operational history, multi-tenant policy isolation, anomaly detection, predictive risk scoring, scenario simulation, continuous control testing, cross-PBC event federation, and governed agent execution.

## 50 Better-Than-World-Class Improvements

### 1. Grant award intake gate

**Justification:** Award setup errors can cascade into unallowable costs, missed reports, failed draws, match shortfalls, and funder findings.

**Improvement:** Add an award intake gate validating funder, award number, period of performance, funding amount, assistance listing, restrictions, budget categories, reporting schedule, match terms, indirect cost rules, closeout terms, and source-document evidence before activation.

### 2. Semantic award document extraction

**Justification:** Grant requirements are embedded in award letters, notices, contracts, amendments, terms, and funder guidance.

**Improvement:** Let the agent extract restrictions, budgets, allowable costs, reporting milestones, match obligations, draw rules, indirect cost terms, procurement clauses, and closeout requirements with source citations and confidence before humans approve owned records.

### 3. Award lifecycle state machine

**Justification:** Awards move through pre-award, awarded, active, amended, suspended, closeout, closed, terminated, and archived states with different spending and reporting rules.

**Improvement:** Implement strict lifecycle transitions with required evidence, spending effects, drawdown eligibility, reporting obligations, closeout tasks, and audit proof. Block cost recording where award status forbids activity.

### 4. Award amendment governance

**Justification:** Amendments can change funding, period, restrictions, match, reporting, budget lines, and closeout obligations.

**Improvement:** Add amendment versioning with changed terms, effective date, impacted budgets, affected costs, drawdown changes, reporting schedule updates, and approval evidence. Show before/after compliance impact.

### 5. Fund restriction taxonomy

**Justification:** Restrictions can be time-based, purpose-based, program-based, geography-based, donor-imposed, statutory, matching, or reporting-driven.

**Improvement:** Model restriction type, source clause, effective period, affected funds/budgets/costs, release criteria, and reporting treatment. Cost validation should reference explicit restriction records rather than generic policy flags.

### 6. Restriction-aware cost validation

**Justification:** Costs may be generally valid but unallowable for a specific fund, period, program, or award condition.

**Improvement:** Validate costs against award period, budget category, fund restriction, allowable cost rule, procurement requirement, match eligibility, prior approval, indirect cost rule, and remaining budget. Store all pass/fail reasons and required remediation.

### 7. Grant fund lifecycle controls

**Justification:** Grant funds require controlled creation, funding, obligation, spend, draw, release, transfer, and closeout treatment.

**Improvement:** Add fund states with award link, restriction scope, available balance, obligated balance, spent balance, drawn balance, matched balance, and closeout readiness. Provide fund balance rollforwards and audit traces.

### 8. Grant budget versioning

**Justification:** Grant budgets often change through amendments, rebudgeting authority, funder approvals, and internal revisions.

**Improvement:** Version grant budgets with approved amounts, categories, effective dates, funder approval requirement, rebudget thresholds, prior version comparison, and locked periods. Every cost should reference the active budget version evaluated.

### 9. Budget line burn-rate analytics

**Justification:** Under-spend, over-spend, and end-of-award spending spikes are common grant risks.

**Improvement:** Track burn rate by budget line, category, fund, period, and award with projected exhaustion, underspend risk, overspend risk, and recommended rebudget or draw actions. Surface warnings before violations occur.

### 10. Allowable cost rule compiler

**Justification:** Allowability rules are nuanced across funder, program, cost category, period, procurement, prior approval, and documentation.

**Improvement:** Compile allowable cost policies from structured configuration and award documents into executable rules with examples, ambiguity flags, clause citations, test cases, and approval workflow.

### 11. Cost transaction evidence model

**Justification:** Grant costs need source journal, payment, expense, payroll, procurement, vendor, period, and support-document evidence.

**Improvement:** Store cost transactions with source projection, cost category, incurred date, paid date, accounting period, documentation status, allowability result, budget impact, draw eligibility, and audit evidence.

### 12. Journal and payment reconciliation

**Justification:** Grant ledgers must reconcile journal postings, payments, draw receipts, reimbursements, and reported costs.

**Improvement:** Reconcile consumed `JournalPosted` and `PaymentExecuted` events to owned cost transactions, drawdown receipts, and fund balances with duplicate detection, late-posting flags, and unmatched item queues.

### 13. Cost transfer governance

**Justification:** Moving costs between grants is high risk and often subject to timing, documentation, and approval restrictions.

**Improvement:** Add cost transfer requests with original grant, target grant, reason, timing, evidence, allowability check, budget impact, approver, and audit trail. Flag late or frequent transfers for review.

### 14. Cost allocation rule versioning

**Justification:** Shared costs require defensible allocation bases, periods, and approvals.

**Improvement:** Version allocation rules with source pool, target awards, allocation basis, excluded costs, effective period, documentation, and approval. Allocation runs should store input pool, basis values, output lines, and reconciliation.

### 15. Allocation run traceability

**Justification:** Funders may challenge allocated costs unless the basis and calculations are transparent.

**Improvement:** Store allocation traces showing source costs, basis metrics, target percentages, rounding, residuals, excluded awards, and resulting grant cost transactions. Provide exportable calculation evidence.

### 16. Drawdown readiness gate

**Justification:** Drawdowns should only request reimbursable, allowable, documented, paid or eligible costs according to funder rules.

**Improvement:** Add readiness checks for cost allowability, payment status, documentation, budget availability, prior draw status, match status, funder limits, reporting currency, and cash timing before a draw request can be submitted.

### 17. Drawdown cash simulation

**Justification:** Organizations need to forecast cash needs and funder reimbursement timing.

**Improvement:** Simulate drawdown timing using eligible costs, payment schedules, funder processing days, advance/reimbursement method, holdbacks, pending exceptions, and cash balance assumptions. Show cash shortfall risk and recommended draw timing.

### 18. Drawdown receipt reconciliation

**Justification:** Received cash may differ from requested draws due to funder adjustments, partial approvals, timing, or rejected costs.

**Improvement:** Reconcile drawdown receipts to requests by amount, date, funder reference, rejected lines, pending lines, and cash account projection. Create exception cases for unmatched or short-paid receipts.

### 19. Match requirement schedule

**Justification:** Match obligations often vary by award period, category, source, cash/in-kind type, and percentage.

**Improvement:** Model match requirements with schedule, basis, source restrictions, eligible contribution types, valuation rules, due dates, and shortfall thresholds. Track progress and forecast shortfalls.

### 20. Match contribution evidence

**Justification:** Match contributions must be documented, eligible, valued correctly, and not double-counted.

**Improvement:** Store contribution source, cash/in-kind type, valuation method, donor/source, documentation, eligibility, award linkage, date, and double-count checks. Provide contribution-level audit evidence.

### 21. In-kind contribution valuation controls

**Justification:** In-kind services, donated goods, facilities, and volunteer time require defensible valuation.

**Improvement:** Add valuation methods, rate sources, market evidence, approver, donor restrictions, and documentation requirements for in-kind contributions. Flag unsupported valuations and expired rate evidence.

### 22. Funder reporting calendar

**Justification:** Missing financial, programmatic, draw, compliance, or closeout reports can jeopardize funding.

**Improvement:** Create a milestone calendar with report type, due date, submission window, owner, data cutoff, dependencies, required attachments, funder portal status, and escalation rules.

### 23. Funder report builder

**Justification:** Funder reports must tie costs, budgets, draws, match, restrictions, compliance, and narrative evidence together.

**Improvement:** Build reports from owned costs, budgets, drawdowns, match, compliance evidence, and milestones with reconciliations, variance explanations, attachments, approval workflow, and submitted version proof.

### 24. Report-to-ledger reconciliation

**Justification:** Reported costs must reconcile to grant cost transactions, fund balances, and drawdown history.

**Improvement:** Add reconciliation between report lines, cost transactions, budget categories, draw requests, and receipts. Block submission where report totals do not match approved ledger evidence or explainable adjustments.

### 25. Compliance evidence room

**Justification:** Grant compliance requires organized evidence for eligibility, procurement, reporting, controls, audits, and closeout.

**Improvement:** Add evidence packets with document type, award link, cost link, restriction link, report link, retention period, source, reviewer, redaction state, and cryptographic proof. UI should show missing evidence by obligation.

### 26. Continuous funder compliance testing

**Justification:** Waiting for audits to find compliance gaps is too late.

**Improvement:** Run controls for unallowable costs, late reports, expired evidence, match shortfalls, budget overages, draw mismatches, procurement gaps, cost transfer timing, and closeout readiness. Store assertion results and remediation tasks.

### 27. Procurement and subaward compliance hooks

**Justification:** Grant costs often require procurement method, vendor eligibility, competition, subrecipient monitoring, or debarment evidence.

**Improvement:** Add compliance fields for procurement method, required quotes, sole-source justification, vendor eligibility, subaward status, monitoring requirements, and evidence links through declared projections.

### 28. Indirect cost rate governance

**Justification:** Indirect cost recovery depends on negotiated rates, base definitions, exclusions, caps, and effective periods.

**Improvement:** Model indirect cost rates with base, rate, effective dates, exclusions, funder caps, approval evidence, and calculation trace. Validate indirect cost lines and draw eligibility against the active rate.

### 29. Program income tracking

**Justification:** Program income may need to be deducted, added, cost-shared, or reported depending on award terms.

**Improvement:** Add program income records with source, period, award link, treatment method, restriction, budget impact, report inclusion, and audit evidence. Include income in draw and report readiness checks.

### 30. Fund balance rollforward

**Justification:** Funders and auditors need beginning balance, awards, costs, draws, match, transfers, adjustments, and ending balance.

**Improvement:** Generate rollforwards by award, fund, restriction, budget category, and period with drilldowns to transactions and reports. Reconcile rollforward totals to draw and report evidence.

### 31. Multi-funder portfolio forecasting

**Justification:** Organizations manage overlapping awards with different periods, restrictions, and cash timing.

**Improvement:** Forecast portfolio funding, spend, draw cash, match exposure, report workload, closeout workload, and shortfall risk by funder, program, award, and period. Show confidence and assumptions.

### 32. Funding shortfall simulation

**Justification:** Shortfalls can arise from delayed draws, unallowable costs, match gaps, award underspend, or funder withholding.

**Improvement:** Simulate shortfall scenarios with draw delays, rejected costs, match gaps, budget changes, and spending pace. Recommend mitigation through rebudget, cost transfer, bridge funding, or funder communication.

### 33. Grant exception case workflow

**Justification:** Grant exceptions such as unallowable cost, late report, missing evidence, match shortfall, or draw rejection need structured resolution.

**Improvement:** Add exception cases with type, severity, award, fund, cost/report link, owner, due date, required evidence, financial exposure, resolution action, and closure proof.

### 34. Closeout readiness checklist

**Justification:** Grant closeout requires final costs, draws, reports, match, property, equipment, program income, evidence retention, and funder acceptance.

**Improvement:** Add a closeout checklist with required milestones, final reconciliation, unliquidated obligations, match completion, report submissions, draw receipts, property disposition, evidence packet, and approval.

### 35. Closeout adjustment governance

**Justification:** Late costs, refunds, draw corrections, and funder adjustments after closeout can affect reports and balances.

**Improvement:** Add post-closeout adjustment workflows with approval, materiality, funder notification, report amendment, draw correction, and audit trail. Block casual edits to closed awards.

### 36. Retention and audit readiness

**Justification:** Grant evidence has retention rules that may vary by funder, award, litigation, audit status, and closeout date.

**Improvement:** Add retention schedules, legal hold, audit hold, destruction eligibility, evidence completeness, and export packages. Surface evidence nearing retention review and block premature deletion.

### 37. Cryptographic evidence packet

**Justification:** Funder-ready evidence should be tamper-evident across awards, budgets, costs, draws, match, reports, and closeout.

**Improvement:** Generate cryptographic packets with hash-chain proofs, redacted payload fingerprints, source event hashes, report versions, and verifier exports for auditors and funders.

### 38. Grant policy impact analysis

**Justification:** Policy changes can affect allowability, draw timing, match, reporting, and closeout controls.

**Improvement:** Simulate policy changes against active awards and recent costs to identify affected transactions, reports, draw requests, exception cases, and required remediation.

### 39. Predictive grant risk scoring

**Justification:** Grant managers need early warning for awards likely to miss reports, overspend, underspend, violate restrictions, or fail match.

**Improvement:** Score awards using burn rate, reporting workload, match progress, draw delays, exception history, evidence completeness, staff workload, and funder behavior. Show drivers and recommended actions.

### 40. Grant anomaly detection

**Justification:** Unusual costs, draws, allocations, match contributions, budget changes, or report adjustments may indicate compliance or data issues.

**Improvement:** Detect anomalies by award, fund, cost category, vendor, period, draw request, match source, allocation basis, and report line. Route high-risk anomalies to exception cases.

### 41. AppGen-X event reliability proof

**Justification:** Grant accounting depends on journal, payment, policy, expense, and audit events; lost or duplicated events can misstate fund balances.

**Improvement:** Harden event descriptors with schema versions, idempotency keys, ordering assumptions, retry envelopes, dead-letter taxonomy, replay eligibility, and handler evidence. Include duplicate journal and late payment scenarios.

### 42. Cross-PBC boundary proof

**Justification:** Grant accounting needs journal, payment, expense, procurement, audit, and finance context without direct foreign-table access.

**Improvement:** Generate a boundary proof enumerating every declared API, projection, consumed event, cached field, staleness policy, and retention rule. Release audits should fail undeclared ledger, payment, expense, or procurement table access.

### 43. Agent-assisted award setup

**Justification:** Award setup is document-heavy and error-prone, making it a strong fit for governed AI assistance.

**Improvement:** Let the agent parse award packages, propose restrictions, budgets, reports, match, draw rules, and compliance tasks, then present a side-effect-free setup plan with citations and confidence for approval.

### 44. Agent-assisted cost allowability review

**Justification:** Accountants need fast explanations of why a cost is allowable, questionable, or disallowed.

**Improvement:** Let the agent analyze cost evidence, award terms, budget category, period, restriction, procurement evidence, and match rules. It should recommend remediation without approving or recording costs without confirmation.

### 45. Grant accounting workbench cockpit

**Justification:** Grant managers need a live surface for award status, budgets, restrictions, costs, draws, match, reports, exceptions, controls, and closeout.

**Improvement:** Build cockpit panels with award health, burn rate, draw readiness, match progress, report deadlines, evidence gaps, exception queues, dead letters, and control assertions. Every action should map to permissioned service commands.

### 46. UI capability surface proof

**Justification:** A complete Grant and Fund Accounting PBC must expose all domain capabilities through dedicated UI surfaces.

**Improvement:** Add release checks proving UI coverage for awards, funds, restrictions, budgets, allowable rules, costs, allocations, drawdowns, receipts, match, reports, milestones, compliance evidence, closeout, exceptions, policies, parameters, controls, models, events, and agent tools.

### 47. Grant control testing library

**Justification:** Grant accounting needs repeatable controls over allowability, budget, draws, match, reports, closeout, and evidence retention.

**Improvement:** Ship controls for costs outside period, budget overages, missing evidence, draw before payment, duplicate draws, match shortfall, late reports, unresolved exceptions, and closed-award edits. Store owners, cadence, results, and remediation.

### 48. Grant resilience drills

**Justification:** Grant operations must recover from event backlogs, bad policy releases, draw rejections, report deadline surges, and evidence store outages.

**Improvement:** Add drills for duplicate journal replay, payment delay, draw rejection batch, policy rollback, report rebuild, evidence packet recovery, and dead-letter surge. Store recovery time, affected awards, and financial exposure.

### 49. Grant readiness score

**Justification:** Operators need a concise signal showing whether the PBC is production-ready for funder-facing grant accounting.

**Improvement:** Compute readiness from award setup completeness, restriction coverage, budget controls, allowability rules, draw readiness, match progress, reporting calendar, evidence completeness, event health, UI coverage, boundary proof, and agent safety.

### 50. End-to-end grant release proof

**Justification:** A world-class Grant and Fund Accounting PBC needs one evidence package proving that awards can flow from setup through costs, draws, reports, compliance, and closeout safely.

**Improvement:** Create an end-to-end proof exercising award document intake, award creation, fund restriction, budget approval, allowable cost rule, cost recording, allocation, drawdown request, receipt reconciliation, match tracking, report building, compliance evidence, closeout, exception resolution, policy compilation, UI coverage, AppGen-X eventing, boundary verification, and agent-safe CRUD planning.
