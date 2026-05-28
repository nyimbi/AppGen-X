# Provider Revenue Cycle PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `provider_revenue_cycle` with a hand-curated provider revenue-cycle roadmap. The PBC owns patient accounts, registration revenue readiness, charge capture, coding workqueues, claim batch preparation, denial cases, payment posting evidence, collections coordination, revenue integrity, governed rules, agent assistance, and release evidence without owning payer adjudication, clinical chart source-of-truth, or general ledger tables.

## Current Domain Evidence Used

- Stable PBC key: `provider_revenue_cycle`.
- Domain purpose: healthcare registration, charge capture, coding, claims, denials, payment posting, collections, and revenue integrity.
- Owned domain tables: `patient_account`, `charge_capture`, `coding_workqueue`, `claim_batch`, `denial_case`, `payment_posting`, `collection_worklist`, `provider_revenue_cycle_policy_rule`, `provider_revenue_cycle_runtime_parameter`, `provider_revenue_cycle_schema_extension`, `provider_revenue_cycle_control_assertion`, `provider_revenue_cycle_governed_model`.
- Public APIs: `POST /patient-accounts`, `POST /charge-captures`, `POST /coding-workqueues`, `POST /claim-batchs`, `POST /denial-cases`, `GET /provider-revenue-cycle-workbench`.
- Emitted AppGen-X events: `ProviderRevenueCycleCreated`, `ProviderRevenueCycleUpdated`, `ProviderRevenueCycleApproved`, `ProviderRevenueCycleExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.

## 50 High-Impact Improvements

### 1. Patient Account Revenue Readiness

**Justification:** A patient account is the revenue-cycle container for registration, coverage, authorization, charges, coding, billing, payment, and collections readiness.

**Improvement:** Add account states for preregistered, registered, eligibility pending, authorization pending, charge pending, coding pending, claim ready, billed, denied, paid, underpaid, patient balance, collections, and closed.

**Acceptance evidence:** Tests must reject invalid account transitions and show missing readiness components before claim batching.

### 2. Registration Quality Controls

**Justification:** Incorrect demographic, guarantor, coverage, accident, and coordination data causes denials and rework.

**Improvement:** Add registration validation for identity confidence, guarantor, coverage priority, subscriber relationship, accident indicators, required consent, and missing financial-class evidence.

**Acceptance evidence:** Tests must open registration deficiencies and block claim-ready state until configured errors are resolved.

### 3. Eligibility and Benefits Projection Boundary

**Justification:** Provider billing depends on eligibility but should not own payer enrollment systems.

**Improvement:** Store eligibility response evidence with payer, plan, effective dates, coverage status, benefit summary, response time, and freshness.

**Acceptance evidence:** Boundary tests must fail on shared eligibility table reads and pass on declared event/API projection usage.

### 4. Authorization Tracking

**Justification:** Missing or mismatched authorization creates avoidable denials.

**Improvement:** Add authorization requirement, submitted date, approved services, units, validity dates, payer reference, remaining balance, and mismatch review.

**Acceptance evidence:** Tests must flag missing, expired, unit-exhausted, and service-mismatched authorizations before billing.

### 5. Charge Capture Completeness

**Justification:** Revenue leakage starts when performed services are never charged.

**Improvement:** Expand `charge_capture` with source encounter/event evidence, charge trigger, service date, department, performing clinician, expected charge, captured charge, variance, and missing-charge case.

**Acceptance evidence:** Tests must detect missing, duplicate, late, and unsupported charges from declared clinical events.

### 6. Charge Description Governance

**Justification:** Charge codes, prices, revenue codes, modifiers, and effective dates require controlled governance.

**Improvement:** Add charge master version evidence, effective windows, billable setting, modifier requirements, price basis, and approval workflow.

**Acceptance evidence:** Tests must price historical charges against the correct version and block inactive charge codes.

### 7. Coding Workqueue Specialization

**Justification:** Coding work differs by inpatient, outpatient, professional, emergency, surgery, and ancillary service lines.

**Improvement:** Add coding case type, required documentation, diagnosis/procedure evidence, coder assignment, query need, coding status, and final code set.

**Acceptance evidence:** Tests must route cases by type and prevent final coding when required documentation is missing.

### 8. Clinical Documentation Query Workflow

**Justification:** Coders need governed queries to clinicians when documentation is unclear, incomplete, or conflicting.

**Improvement:** Add query reason, linked documentation evidence, compliant question text, clinician response, due date, and coding outcome impact.

**Acceptance evidence:** Tests must preserve query history and block leading or unsupported query drafts.

### 9. Claim Scrubbing Rules

**Justification:** Clean claims require edits before submission, not after payer rejection.

**Improvement:** Add scrub rules for demographics, coverage, authorization, coding, modifiers, diagnosis pointers, timely filing, accident data, and payer-specific requirements.

**Acceptance evidence:** Tests must scrub clean, warning, fatal, and override-required claim scenarios.

### 10. Claim Batch Assembly

**Justification:** Batches need payer, format, facility, claim type, submitter, sequence, and transmission evidence.

**Improvement:** Expand `claim_batch` with batch type, payer, clearinghouse route, included accounts, totals, validation status, submission status, acknowledgement, and rejection evidence.

**Acceptance evidence:** Tests must assemble, validate, submit, acknowledge, reject, and resubmit claim batches idempotently.

### 11. Clearinghouse Rejection Handling

**Justification:** Clearinghouse rejections are operational problems before payer adjudication.

**Improvement:** Add rejection reason, affected claim, edit category, owner, correction action, resubmission state, and aging.

**Acceptance evidence:** Tests must correct and resubmit rejected claims without creating duplicate batches.

### 12. Denial Case Taxonomy

**Justification:** Denials require root-cause categories, owner, deadline, appeal likelihood, and prevention feedback.

**Improvement:** Expand `denial_case` with category, payer reason, internal root cause, preventable flag, dollar amount, appeal path, owner, and closure reason.

**Acceptance evidence:** Tests must classify authorization, eligibility, coding, timely filing, medical necessity, duplicate, and coordination denials.

### 13. Denial Appeal Workflows

**Justification:** Provider appeals need evidence packets, deadlines, payer-specific requirements, and follow-up.

**Improvement:** Add appeal level, packet checklist, clinical documents, coding rationale, authorization evidence, deadline, submission proof, decision, and underpayment link.

**Acceptance evidence:** Tests must build appeal packets, enforce deadlines, and update account state on upheld or overturned decisions.

### 14. Payment Posting and Remittance Matching

**Justification:** Provider cash application depends on matching remittances, payments, adjustments, denials, and patient responsibility.

**Improvement:** Add `payment_posting` evidence for remittance source, payer trace, claim lines, allowed amount, payment, adjustment, denial, patient responsibility, and unmatched cash.

**Acceptance evidence:** Tests must auto-post clean remittances and route exceptions for unmatched, partial, and conflicting remittances.

### 15. Contractual Underpayment Detection

**Justification:** Payers may pay less than expected under contracted rates.

**Improvement:** Add expected reimbursement, actual payment, variance reason, contract basis, appeal/rebill action, and recovery status.

**Acceptance evidence:** Tests must identify underpayment, overpayment, expected adjustment, and contract-missing scenarios.

### 16. Patient Balance Segmentation

**Justification:** Patient balances need financial assistance, payment plan, dispute, refund, bad debt, and collections paths.

**Improvement:** Add balance segment, statement status, assistance screening, payment plan, dispute, collection hold, agency referral, and write-off reason.

**Acceptance evidence:** Tests must route balances by segment and prevent collections on active disputes or assistance holds.

### 17. Financial Assistance Screening

**Justification:** Professional revenue-cycle operations must protect eligible patients from inappropriate collections.

**Improvement:** Add assistance eligibility signals, application status, presumptive eligibility, documentation request, approval, denial, discount, and renewal.

**Acceptance evidence:** Tests must apply assistance holds and adjust patient balance only after approval evidence.

### 18. Collections Worklist Governance

**Justification:** Collections must be compliant, fair, documented, and policy-controlled.

**Improvement:** Expand `collection_worklist` with account age, balance, contact restrictions, dispute status, assistance status, agency eligibility, outreach attempts, and closure reason.

**Acceptance evidence:** Tests must block outreach where policy, dispute, consent, or assistance status prohibits it.

### 19. Refund and Credit Balance Handling

**Justification:** Credit balances can indicate overpayment, payer recoupment, or patient refund obligations.

**Improvement:** Add credit source, payer/member amount, refund eligibility, offset policy, approval, refund event, and stale-credit escalation.

**Acceptance evidence:** Tests must route payer and patient credits separately and prevent duplicate refunds.

### 20. Revenue Integrity Audit Cases

**Justification:** Revenue integrity covers charge accuracy, coding compliance, missing revenue, contract variance, and policy adherence.

**Improvement:** Add audit case type, population, finding, financial exposure, responsible department, corrective action, and follow-up measurement.

**Acceptance evidence:** Tests must create revenue integrity cases from charge, denial, underpayment, and audit signals.

### 21. Timely Filing Management

**Justification:** Missed filing windows cause preventable write-offs.

**Improvement:** Add payer deadline, first submission, rejection resubmission clock, appeal deadline, proof of timely filing, and late-risk queue.

**Acceptance evidence:** Tests must escalate accounts near deadline and preserve submission proof.

### 22. Coding Compliance Controls

**Justification:** Coding must be accurate, compliant, and defensible.

**Improvement:** Add coding audit flags, coder quality metrics, unsupported code warnings, modifier risk, diagnosis specificity, and correction tracking.

**Acceptance evidence:** Tests must open compliance exceptions and prevent unsupported code finalization.

### 23. Claim Status Follow-Up

**Justification:** Submitted claims require payer acknowledgement, status checks, follow-up, and escalation.

**Improvement:** Add follow-up schedule, last payer status, no-response escalation, requested information, and owner queue.

**Acceptance evidence:** Tests must create follow-up tasks and close only when payment, denial, rejection, or documented resolution exists.

### 24. Payer Rule Configuration

**Justification:** Payer billing requirements vary and change frequently.

**Improvement:** Add payer-specific billing rules, required fields, attachment rules, timely filing, appeal process, authorization policy, and effective dates.

**Acceptance evidence:** Tests must evaluate the same account differently by payer and rule version.

### 25. Parameter Impact Simulation

**Justification:** Changing scrub rules, appeal thresholds, write-off limits, or collection policies can shift revenue and compliance outcomes.

**Improvement:** Add side-effect-free simulation over accounts, charges, claims, denials, patient balances, and underpayments.

**Acceptance evidence:** Tests must produce impact reports before activating high-risk parameter changes.

### 26. Denial Prevention Feedback Loop

**Justification:** Denial management should prevent recurrence, not just work cases.

**Improvement:** Add root-cause trends, upstream owner, prevention recommendation, education task, rule update candidate, and measured reduction.

**Acceptance evidence:** Tests must tie recurring denial causes to prevention actions and track outcome.

### 27. Missing Charge and Late Charge Workflow

**Justification:** Late charges can delay claims and create rebills.

**Improvement:** Add late charge detection, billing hold, rebill requirement, payer notification need, financial impact, and approval workflow.

**Acceptance evidence:** Tests must route late charges correctly before and after claim submission.

### 28. Bad Debt and Write-Off Governance

**Justification:** Write-offs require authorization, category, policy, recoverability, and audit evidence.

**Improvement:** Add write-off type, threshold, approver, reason, financial class, collection history, and reversal path.

**Acceptance evidence:** Tests must reject unauthorized write-offs and preserve reversal evidence.

### 29. Patient Communication Notices

**Justification:** Statements, assistance notices, payment plans, disputes, and collection warnings require governed communication.

**Improvement:** Add notice templates, language, delivery channel, required inserts, consent restrictions, proof of delivery, and returned-mail handling.

**Acceptance evidence:** Tests must generate notices and block communications when restrictions apply.

### 30. Revenue Cycle Workbench

**Justification:** Users need operational queues by role instead of generic record lists.

**Improvement:** Add views for registration deficiencies, authorization risk, missing charges, coding backlog, claim rejects, denials, underpayments, credit balances, and collections holds.

**Acceptance evidence:** UI tests must prove each queue maps to owned data or declared projections and exposes permission-aware actions.

### 31. Agent-Assisted Account Summaries

**Justification:** Staff need quick explanations of why an account is stalled or at risk.

**Improvement:** Add agent skills for account summary, denial root cause, appeal packet draft, missing charge explanation, underpayment rationale, and patient balance guidance.

**Acceptance evidence:** Tests must require citations for every agent summary and mark inferred recommendations clearly.

### 32. Governed Agent CRUD Commands

**Justification:** The assistant should help update accounts safely without silently changing financial state.

**Improvement:** Add command previews for open denial, assign coder, hold claim, release batch, post payment exception, create collection hold, and draft appeal.

**Acceptance evidence:** Intent tests must require account, action, evidence, preview, confirmation, and audit record.

### 33. Remittance Document and Attachment Ingestion

**Justification:** Remittances, payer letters, medical records, and appeal decisions often arrive as documents.

**Improvement:** Add document extraction with source span, candidate posting, denial reason, appeal outcome, confidence, reviewer, and accepted fields.

**Acceptance evidence:** Tests must block low-confidence document-derived mutations until reviewed.

### 34. Governance of Revenue Models

**Justification:** Denial prediction, underpayment detection, and agent summarization affect financial outcomes.

**Improvement:** Register governed models with use case, version, evaluation set, thresholds, drift checks, and human feedback.

**Acceptance evidence:** Tests must block model-backed recommendations if governance evidence is missing or stale.

### 35. Continuous Controls

**Justification:** Revenue-cycle quality requires ongoing controls for clean claim rate, denial preventability, payment variance, write-offs, and collections compliance.

**Improvement:** Add controls with thresholds, populations, failing samples, owner, remediation, recurrence, and closure evidence.

**Acceptance evidence:** Tests must open control failures and require remediation evidence before closure.

### 36. Dead-Letter and Retry Operations

**Justification:** Eligibility events, charge events, claim acknowledgements, remittances, and payer updates can fail.

**Improvement:** Add retry classification, idempotency key, financial risk, replay checkpoint, remediation action, and dead-letter queue.

**Acceptance evidence:** Tests must replay failed inputs without duplicate charges, claims, postings, or notices.

### 37. Cross-PBC Boundary Proofs

**Justification:** Provider revenue cycle composes with EHR, claims adjudication, finance, notifications, and audit but must not share their tables.

**Improvement:** Add release gates proving all dependencies use declared APIs, events, projections, or package metadata.

**Acceptance evidence:** Tests must fail on undeclared foreign table reads and pass on AppGen-X event/API contracts.

### 38. Net Revenue Forecast

**Justification:** Leaders need predicted reimbursement, denial exposure, cash timing, and write-off risk.

**Improvement:** Add forecast projections by account, payer, service line, claim status, denial probability, expected payment, and confidence.

**Acceptance evidence:** Tests must produce explainable forecasts and compare actual results to prediction.

### 39. Root-Cause Financial Analytics

**Justification:** Revenue losses need actionable attribution.

**Improvement:** Add analytics for registration errors, authorization misses, coding delays, late charges, claim rejects, denials, underpayments, credit balances, and collections leakage.

**Acceptance evidence:** Tests must generate tenant-scoped metrics with source drilldowns.

### 40. Payer Scorecards

**Justification:** Provider organizations need evidence on payer payment speed, denial rate, overturn rate, underpayment rate, and administrative burden.

**Improvement:** Add payer scorecards from claim, denial, appeal, underpayment, and payment-posting evidence with trend and confidence.

**Acceptance evidence:** Tests must calculate scorecards without owning payer master tables beyond local evidence.

### 41. Account Timeline Projection

**Justification:** Users need a full history from registration to cash.

**Improvement:** Build account timeline events for registration, eligibility, authorization, charges, coding, billing, denial, appeal, posting, collections, and closure.

**Acceptance evidence:** Replay tests must reconstruct timelines idempotently and respect redaction by role.

### 42. Cryptographic Revenue Evidence

**Justification:** Financial disputes and audits need tamper-evident account and payment history.

**Improvement:** Add proof chains for charge capture, coding finalization, claim submission, denial appeal, payment posting, write-off, and refund events.

**Acceptance evidence:** Tests must verify proof chains and detect altered payloads or reordered events.

### 43. Compliance and Audit Evidence Room

**Justification:** Auditors need curated evidence, not raw exports.

**Improvement:** Add evidence packets for account readiness, coding decision, claim submission, denial appeal, payment posting, write-off, and collections action.

**Acceptance evidence:** Tests must generate permission-safe evidence packets with source links.

### 44. Patient Dispute Workflow

**Justification:** Patients may dispute balances, insurance handling, coding, or financial assistance decisions.

**Improvement:** Add dispute reason, account hold, evidence requested, investigation owner, resolution, adjustment, communication, and appeal path.

**Acceptance evidence:** Tests must block collections during active disputes and preserve resolution evidence.

### 45. Seeded Revenue Cycle Scenario Library

**Justification:** Release evidence needs realistic provider financial journeys.

**Improvement:** Add seeds for clean claim, registration error, missing authorization, coding query, late charge, denial appeal, underpayment, credit balance, and patient assistance.

**Acceptance evidence:** Scenario tests must load side-effect-free and create expected queues, events, and analytics.

### 46. Role-Based Permission Model

**Justification:** Registrars, coders, billers, collectors, revenue integrity analysts, managers, and compliance users need different authority.

**Improvement:** Add permission descriptors for account edit, charge approve, coding finalize, batch submit, appeal submit, write-off approve, payment post, and collection action.

**Acceptance evidence:** Permission tests must block unauthorized commands and show disabled UI actions.

### 47. Timely Close and Month-End Support

**Justification:** Revenue-cycle operations feed financial close but should not own general ledger posting.

**Improvement:** Add month-end readiness projections for unbilled accounts, late charges, uncoded accounts, unposted remittances, open denials, and unapplied cash.

**Acceptance evidence:** Tests must emit close-readiness events and avoid GL table writes.

### 48. Full Revenue Cycle Release Simulation

**Justification:** A complete PBC must prove account-to-cash behavior end to end.

**Improvement:** Add a simulation where a patient account registers, eligibility is checked, authorization is captured, charges post, coding finalizes, claim batches, denial appeals, payment posts, and balance closes.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, handlers, workbench views, agent skills, permissions, and release evidence.

### 49. Package Boundary and Overlap Proofs

**Justification:** This PBC must not duplicate payer adjudication, clinical chart ownership, or general ledger ownership.

**Improvement:** Add overlap checks showing provider-side evidence boundaries and declared dependency contracts for clinical, payer, finance, notification, and audit interactions.

**Acceptance evidence:** Tests must fail on undeclared external table references and pass on declared AppGen-X contracts.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose revenue-cycle skills through DSL, UI, APIs, and the composed application agent.

**Improvement:** Extend composition metadata for patient accounts, charges, coding, claim batches, denials, postings, collections, workbench views, rules, parameters, controls, and agent skills.

**Acceptance evidence:** DSL tests must prove generated apps include provider revenue-cycle models, routes, services, UI artifacts, event contracts, and assistant skills without stream-engine picker exposure.
