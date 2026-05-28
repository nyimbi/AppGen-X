# Lending Origination and Servicing Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `lending_origination_servicing`.
- Label and description: Lending Origination and Servicing covering loan applications, underwriting, offers, disbursement, repayment, servicing, collections, and covenant monitoring.
- Owned tables named in the manifest: `loan_application`, `borrower_profile`, `underwriting_decision`, `loan_offer`, `disbursement`, `repayment_schedule`, `servicing_case`, `lending_origination_servicing_policy_rule`, `lending_origination_servicing_runtime_parameter`, `lending_origination_servicing_schema_extension`, `lending_origination_servicing_control_assertion`, and `lending_origination_servicing_governed_model`.
- Published APIs named in the manifest: `POST /loan-applications`, `POST /borrower-profiles`, `POST /underwriting-decisions`, `POST /loan-offers`, `POST /disbursements`, and `GET /lending-origination-servicing-workbench`.
- Event mesh contracts already declared: emitted `LendingOriginationServicingCreated`, `LendingOriginationServicingUpdated`, `LendingOriginationServicingApproved`, `LendingOriginationServicingExceptionOpened`; consumed `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- UI fragments already declared: `LendingOriginationServicingWorkbench`, `LendingOriginationServicingDetail`, `LendingOriginationServicingAssistantPanel`.
- Advanced capability anchors already declared: event-sourced operational history, multi-tenant policy isolation, schema evolution resilience, anomaly detection, semantic document understanding, predictive risk scoring, counterfactual simulation, cryptographic audit proofs, continuous control testing, and governed AI agent execution.

### 1. Borrower And Application Intake Normalization
**Justification:** `loan_application` and `borrower_profile` are present in the manifest, but real lending intake is not one shape. Consumer, SME, refinance, secured, and co-borrower requests all carry different mandatory facts, and weak intake normalization creates avoidable underwriting churn.

**Improvement:** Build a canonical intake contract that captures borrower role, product request, purpose, occupancy or business use, requested amount, term preference, channel, and consent artifacts before any decisioning begins. Normalize applicant, co-borrower, guarantor, and beneficial-owner roles so downstream rules do not infer them from free text.

**Acceptance evidence:** Payload fixtures for individual and joint borrowers, validation cases for missing consent or unsupported role combinations, and workbench screenshots showing the normalized party structure before the record reaches underwriting.

### 2. Document Stipulation Checklist Management
**Justification:** Lending files rarely move from application to funding with complete documentation on first pass. Missing bank statements, tax returns, formation documents, or insurance binders directly affect cycle time and approval quality.

**Improvement:** Add a stipulation model tied to `loan_application` that tracks requested document, source, owner, due date, received date, verification result, and waiver rationale. Separate pre-underwriting stipulations from pre-funding stipulations so the queue reflects the actual stage of work.

**Acceptance evidence:** Tests proving incomplete stipulations block the correct stage, UI evidence of aged stipulations grouped by owner, and audit entries linking each waived item to an approver and reason.

### 3. Income And Cash-Flow Verification
**Justification:** Underwriting depends on verified repayment capacity, not just declared income. The current manifest surfaces underwriting but does not yet imply domain-specific verification for salaried, self-employed, and seasonal borrowers.

**Improvement:** Introduce verification routines for paystubs, payroll deposits, tax returns, business statements, rent rolls, and recurring obligation offsets. Store gross, net, stable, and excluded income components separately so debt-service logic can explain the final number used in decisioning.

**Acceptance evidence:** Calculation fixtures for wage earners and self-employed borrowers, variance flags when declared income diverges from verified income, and detail views showing how each component rolled into the approved repayment capacity.

### 4. Identity, Fraud, And KYC Gating
**Justification:** Fraud loss often enters before underwriting through synthetic identities, account takeover, altered documents, or mismatched beneficial ownership. A lending package needs explicit front-door gates rather than after-the-fact exception cleanup.

**Improvement:** Add identity verification and fraud review checkpoints covering name-date-of-birth mismatches, document tampering signals, duplicate tax identifiers, watchlist hits, device anomalies, and beneficial-owner screening. Route hard fails into `servicing_case` only when the file has already advanced; otherwise hold the origination record in a pre-decision queue.

**Acceptance evidence:** Negative fixtures for watchlist and duplicate identity scenarios, escalation routing tests, and dashboard evidence that separates fraud review queues from ordinary underwriting backlog.

### 5. Credit Bureau Ingestion And Dispute Handling
**Justification:** Credit pull data is foundational to underwriting and pricing, yet disputes, freezes, thin files, and bureau discrepancies are common and require explicit handling instead of one opaque score field.

**Improvement:** Model bureau pulls, tradeline snapshots, inquiry counts, freeze status, and dispute flags as first-class underwriting evidence. Allow the underwriter to choose which bureau set was used, when re-pull is required, and whether disputed tradelines were excluded from policy calculations.

**Acceptance evidence:** Fixtures for frozen-file retries, multi-bureau mismatch handling, and decision screens that show the exact bureau snapshot and exclusions used for a final approval or decline.

### 6. Collateral, Appraisal, And Lien Data Capture
**Justification:** Secured lending cannot be governed well if collateral facts are stuffed into narrative notes. Asset identity, valuation source, lien position, and title conditions all change the credit and boarding path.

**Improvement:** Extend the domain model to capture collateral type, identifier, valuation date, valuation source, haircut policy, lien position, title status, insurance requirement, and pending condition. Link these facts to `underwriting_decision` and `loan_offer` so loan structure reflects collateral reality.

**Acceptance evidence:** Schema and contract tests for secured-loan collateral payloads, pricing cases that change based on lien position or haircut, and boarding evidence confirming the collateral terms approved are the terms booked.

### 7. Affordability And Debt-Service Calculation Engine
**Justification:** Decisioning quality depends on consistent affordability math. Debt-to-income, debt-service-coverage, residual-income, and global-cash-flow ratios should be reproducible from stored facts and policy versions.

**Improvement:** Implement a calculation engine that stores ratio inputs, inclusions, exclusions, stress assumptions, and rounding rules with the resulting affordability metrics. Support consumer and commercial variants without burying one inside custom rule code for the other.

**Acceptance evidence:** Golden tests for DTI, DSCR, and residual-income scenarios, policy-version snapshots attached to each calculation, and UI drill-down showing why a file passed or failed the affordability thresholds.

### 8. Underwriting Rule Versioning And Decision Policy Lineage
**Justification:** `underwriting_decision` exists, but regulated lending requires the institution to explain which policy version, threshold set, and override chain produced that decision on that date.

**Improvement:** Version every underwriting policy package in `lending_origination_servicing_policy_rule` with effective dates, target products, risk tiers, override authority, and supersession links. Persist the exact rule bundle and runtime parameter values used for each decision so later reviews do not reconstruct policy from memory.

**Acceptance evidence:** Simulation tests across two policy versions, immutable lineage links from decision to policy package, and release evidence showing who approved a policy change and when it became effective.

### 9. Decision Explanation And Adverse Action Support
**Justification:** A decline or counteroffer is not operationally complete until the institution can articulate the decision basis in borrower-facing and auditor-facing language. Unexplained models create compliance and reputation risk.

**Improvement:** Generate structured decision explanations from rule outcomes, affordability results, collateral findings, and fraud dispositions. Support decline, conditional approval, reduced amount, shorter term, and pricing counteroffer explanations, including adverse-action reason mapping where the file is declined.

**Acceptance evidence:** Test cases covering decline and counteroffer reason generation, rendered notice previews with mapped reason codes, and audit exports showing the exact evidence points behind each explanation.

### 10. Offer Construction, Pricing, And Expiration Control
**Justification:** `loan_offer` is named in the manifest, but a lending offer is more than amount and rate. Product fit, pricing exceptions, lock expiration, and required conditions must stay aligned with approved risk posture.

**Improvement:** Expand offer modeling to include term, amortization method, pricing index or fixed-rate basis, fees, lock date, expiration date, conditions precedent, and permitted variance from the approved structure. Require second review when pricing deviates from policy or when the approved amount is increased after underwriting.

**Acceptance evidence:** Offer-assembly tests for fixed and variable products, expiration behavior validated in the workbench, and approval records for any pricing or amount exception.

### 11. Closing Conditions And Approval-To-Fund Orchestration
**Justification:** Many losses and customer escalations happen between approval and funding because the institution lacks a precise control layer for closing conditions, final verification, and readiness to fund.

**Improvement:** Add an approval-to-fund checklist spanning executed documents, funding instructions, fraud re-check, lien perfection prerequisites, insurance evidence, and final approval expiry. Distinguish advisory items from hard funding blockers so operations knows exactly what prevents disbursement.

**Acceptance evidence:** Tests showing hard blockers stop `POST /disbursements`, stage-aware UI badges for unresolved conditions, and trace logs connecting the funding decision to the last completed verification step.

### 12. Loan Boarding Completeness Gate
**Justification:** A file can be approved and funded yet still board incorrectly because note terms, balances, due dates, and fee settings were not reconciled before the servicing account was created.

**Improvement:** Introduce a boarding gate that compares approved offer terms, executed contract terms, and funded amounts before the servicing record becomes active. Require explicit resolution for mismatched first payment date, payment frequency, interest basis, escrow requirement, or late-fee setup.

**Acceptance evidence:** Boarding comparison reports, tests for mismatched note-to-system fields, and evidence that no active servicing account is created until all hard discrepancies are cleared.

### 13. Executed Contract And Note Version Linkage
**Justification:** Lending operations need to know which executed paper or electronic package governs the loan after funding. Without version linkage, later servicing and payoff actions can drift from the actual note.

**Improvement:** Link every boarded loan to the definitive signed note, disclosure package, modification agreement, and rider set with execution timestamps and signature completion status. Preserve prior versions so the system can show what changed between original closing and later modifications.

**Acceptance evidence:** Document lineage tests, UI evidence that the active contract version is visible in `LendingOriginationServicingDetail`, and audit records showing when a superseding agreement replaced an earlier one.

### 14. Funding Disbursement And Settlement Reconciliation
**Justification:** `disbursement` is present, but the domain needs more than a send-funds command. Warehouse funding, escrow netting, fee withholding, and settlement corrections require explicit reconciliation.

**Improvement:** Model gross funded amount, net borrower proceeds, payoffs to prior lenders, reserve holds, fee deductions, and settlement account references. Add reconciliation steps that confirm outbound funding instructions match booked balances and settlement acknowledgments.

**Acceptance evidence:** Disbursement tests covering refinance and purchase scenarios, exception queues for unmatched settlement acknowledgments, and reconciliation reports showing gross-to-net funding math.

### 15. Amortization Method Library
**Justification:** A servicing platform cannot rely on one repayment schedule shape. Standard installment, interest-only, balloon, step-rate, and irregular first-period loans all need distinct amortization behavior.

**Improvement:** Extend `repayment_schedule` to support multiple amortization methods with explicit rules for payment amount calculation, schedule generation, balloon balance, and curtailment effects. Store method metadata with the schedule so payoff, modification, and delinquency logic use the same canonical source.

**Acceptance evidence:** Schedule fixtures for level-pay, interest-only, balloon, and step-rate products, comparison tests against known amortization outputs, and UI evidence showing the selected method on the loan detail screen.

### 16. Interest Accrual Basis And Fee Accrual Controls
**Justification:** Loans that appear similar can accrue differently based on day-count convention, accrual start date, compounding treatment, and fee capitalization rules. Misstating these rules creates servicing defects and payoff errors.

**Improvement:** Store interest basis, accrual start rule, non-business-day handling, fee accrual treatment, and capitalization policy as explicit boarded terms. Ensure the schedule engine, delinquency engine, and payoff quote logic all reference the same accrual metadata.

**Acceptance evidence:** Tests for 30/360 and actual-day conventions, cross-checks between accrual ledger and payoff quote outputs, and exception alerts when boarded accrual settings differ from executed note terms.

### 17. Escrow Setup, Analysis, And Shortage Handling
**Justification:** The manifest already covers repayment and servicing, but escrow is a distinct operational domain with its own funding, analysis, shortage, surplus, and disbursement rules.

**Improvement:** Add escrow sub-ledgers for tax, insurance, and special assessment buckets with payment due dates, cushion settings, annual analysis rules, shortage spread options, and borrower-notice requirements. Treat escrow setup as part of boarding completeness, not as a later manual correction.

**Acceptance evidence:** Escrow analysis fixtures for surplus and shortage cases, UI evidence of bucket-level balances and next disbursement dates, and notice-generation tests for shortage or surplus outcomes.

### 18. Payment Allocation Waterfall
**Justification:** Servicing accuracy depends on a clear allocation hierarchy. Institutions differ on how they apply borrower funds across principal, interest, escrow, fees, suspense, and recoveries.

**Improvement:** Define configurable allocation waterfalls in `lending_origination_servicing_runtime_parameter` by product and delinquency status. Support exact payment, partial payment, extra principal, payoff remittance, and restricted funds without letting operations hand-edit balances.

**Acceptance evidence:** Allocation tests for current and delinquent accounts, evidence that unapplied funds enter suspense when required, and servicing detail views showing how each payment posted across components.

### 19. Returned Payments, Reversals, And Unapplied Funds
**Justification:** NSF returns, payment reversals, duplicate payments, and unidentified remittances are common servicing events that change delinquency posture and fee treatment.

**Improvement:** Add explicit reversal workflows that unwind principal, interest, escrow, and fee postings while preserving the original transaction lineage. Separate true unapplied funds from suspense balances created by policy, and force a reason code for every manual resolution.

**Acceptance evidence:** End-to-end fixtures for NSF and duplicate-payment reversal, lineage views showing original transaction and reversal pairings, and queue evidence for aged unidentified funds.

### 20. Delinquency Bucket Progression And Collections Strategy
**Justification:** A generic `servicing_case` is not enough for collections. Delinquency handling needs deterministic bucket movement, contact strategy, and escalation rules tied to days past due and product type.

**Improvement:** Build bucket logic for current, grace, early delinquency, late-stage delinquency, default, and workout statuses. Associate each bucket with required notices, contact cadence, eligible loss-mitigation paths, and supervisor approvals for unusual actions.

**Acceptance evidence:** Aging tests that move loans between buckets based on posting dates and due dates, collections queue views segmented by severity, and evidence that required notices are created at the correct thresholds.

### 21. Promise-To-Pay And Workout Commitment Tracking
**Justification:** Collections teams need more than note fields. Promise-to-pay commitments, broken arrangements, and borrower contact outcomes directly change next-action strategy and supervisory oversight.

**Improvement:** Add commitment records with promised amount, due date, channel, collector, success criteria, and breach outcome. When the promise fails, automatically reopen the collections strategy with the right contact history and delinquency context attached.

**Acceptance evidence:** Tests for kept and broken commitments, queue evidence showing promise dates and status, and audit entries proving the next collections step was system-selected after a breach.

### 22. Late Charges, Grace Periods, And Cure Reinstatement
**Justification:** Late-fee handling affects customer fairness, compliance, and balance integrity. Grace days, waiver rules, and reinstatement logic cannot remain implicit if the platform will generate payoffs and modification terms correctly.

**Improvement:** Store late-charge basis, one-time versus recurring assessment, grace-period treatment, cure reversal behavior, and fee-waiver authority on each boarded loan. Ensure reinstatement after cure removes or preserves fees according to policy rather than operator judgment.

**Acceptance evidence:** Fee-assessment fixtures for current, delinquent, and cured loans, evidence of waiver approvals by role, and statement previews showing fee treatment after reinstatement.

### 23. Hardship Modification Intake And Trial Plan Workflow
**Justification:** Borrowers in distress often enter through hardship channels rather than ordinary collections. Modification work needs a full intake path, not a one-off note against the loan.

**Improvement:** Add hardship intake capturing cause, duration, requested relief, supporting documents, occupancy or business status, and prior workout history. Support trial-plan creation, scheduled review milestones, and conversion rules from trial to permanent modification.

**Acceptance evidence:** Test journeys for hardship intake through permanent modification, timeline evidence of trial milestones, and decision records showing why a trial succeeded, failed, or was canceled.

### 24. Capitalization, Re-Aging, And Modification Accounting Controls
**Justification:** A modification changes balances, amortization, delinquency status, and regulatory reporting. Capitalizing arrears or re-aging a loan without clear controls can mask risk and corrupt later payoff or charge-off calculations.

**Improvement:** Make modification accounting explicit: capitalized interest, capitalized fees, deferred principal, forgiven amounts, re-age authority, and post-modification delinquency reset rules. Require an approval path distinct from ordinary servicing actions when the modification changes principal balance or schedule structure.

**Acceptance evidence:** Accounting fixtures for capitalize, defer, and forgive scenarios, approval logs for re-aging decisions, and balance snapshots showing pre- and post-modification states with no unexplained delta.

### 25. Payoff Quote Generation And Per-Diem Accuracy
**Justification:** Payoff requests are high-risk customer moments. A wrong per-diem or omitted fee creates legal exposure, borrower complaints, and settlement defects.

**Improvement:** Build payoff quote generation that calculates unpaid principal, accrued interest, escrow surplus or shortage, recoverable fees, prepayment charges where allowed, and good-through date treatment. Preserve the quote assumptions so later disputes can reproduce the exact number given.

**Acceptance evidence:** Quote fixtures across current, delinquent, and modified loans, cross-checks between payoff quote and accrual engine, and closure evidence when the remittance differs from the quoted amount.

### 26. Satisfaction, Lien Release, And Account Closure Evidence
**Justification:** A loan is not operationally finished when the balance reaches zero. The institution still owes title release, lien satisfaction, statement closure, and archival evidence.

**Improvement:** Add a payoff completion workflow that tracks final funds receipt, pending refunds, lien release preparation, document dispatch, and account closure hold periods. Keep closure blocked if unresolved disputes, reversals, or escrow refunds remain open.

**Acceptance evidence:** Tests for payoff-to-closure progression, evidence that release actions are generated only after final reconciliation, and detail views showing the closed-loan evidence pack attached to the account.

### 27. Charge-Off, Recovery, And Post-Charge-Off Servicing
**Justification:** Charge-off is not the end of servicing. Recoveries, settlements, external placement, and borrower communication restrictions still need governed behavior.

**Improvement:** Model charge-off trigger date, charged-off components, post-charge-off fee policy, recovery allocation, settlement authority, and referral status. Separate accounting posture from legal or customer-contact posture so the platform can represent charged-off loans that remain actively managed.

**Acceptance evidence:** Fixtures for charge-off and recovery posting, dashboards showing gross charge-off and net recovery movement, and audit records for settlement approvals.

### 28. Bankruptcy, Deceased Borrower, And Legal Hold Servicing
**Justification:** Certain servicing scenarios require strict treatment changes that ordinary delinquency workflows cannot safely handle. Bankruptcy stays, probate, and legal holds need hard operational boundaries.

**Improvement:** Add special-status flags and workflow branches for bankruptcy chapter, filing date, stay restrictions, counsel information, deceased-borrower handling, probate representative, and litigation hold scope. Prevent prohibited notices, automated calls, and fee actions while these statuses are active.

**Acceptance evidence:** Negative tests proving blocked actions during stay or hold status, special-case servicing screens with status banners, and evidence logs for court- or estate-related document handling.

### 29. Insurance, Tax, And Escrow Exception Servicing
**Justification:** Escrow operations do not end with annual analysis. Lapsed insurance, delinquent taxes, force-placed coverage, and shortage cures are daily servicing problems that need structured exception handling.

**Improvement:** Build exception flows for missing insurance proof, force-placement timing, tax delinquency notices, escrow advances, and repayment-plan setup for shortages. Link these exceptions to both the servicing balance view and the borrower communication timeline.

**Acceptance evidence:** Exception fixtures for lapsed coverage and tax delinquency, alerts showing the next required action, and account timelines proving notices and advances were recorded in order.

### 30. Customer Complaints, Disputes, And Regulatory Clocks
**Justification:** Complaints and payment disputes create deadline-driven work distinct from normal servicing. Institutions need a clock, owner, and evidence trail from intake through response.

**Improvement:** Add complaint and dispute cases within `servicing_case` with intake channel, alleged issue, requested remedy, assigned owner, response due date, and final disposition. Route complaints about payoff, escrow, credit reporting, or collections into the correct specialist queue automatically.

**Acceptance evidence:** Clock tests for due-date calculation, case-routing evidence by complaint type, and exported response packets showing the facts reviewed before closure.

### 31. Compliance Rules For Disclosures And Notices
**Justification:** Lending origination and servicing both depend on timely, accurate disclosures. Missing a pre-closing notice, delinquency letter, escrow analysis notice, or payoff communication can turn an operational defect into a regulatory issue.

**Improvement:** Catalog disclosure and notice obligations by product, lifecycle stage, borrower state or segment, and triggering event. Store notice template version, generation date, delivery channel, and suppression rule with the governed record so the platform can prove exactly what was sent.

**Acceptance evidence:** Notice-generation fixtures for origination, delinquency, escrow, modification, and payoff stages, suppression tests for prohibited contact scenarios, and release evidence that maps each notice path to its governing rule.

### 32. Fair Lending And Adverse-Impact Monitoring
**Justification:** Underwriting and pricing need post-decision surveillance, not just front-end rules. A lending package should surface whether policy or model behavior is producing unexplained disparities across protected or monitored groups.

**Improvement:** Add monitoring views that compare approval rate, counteroffer rate, exception usage, pricing outcome, and modification relief outcome across defined segments. Treat this as a compliance and governance surface rather than a hidden analytics notebook.

**Acceptance evidence:** Drift and disparity reports built from `lending_origination_servicing_risk_score` and decision outcomes, threshold alerts when monitored gaps widen, and documented review actions by the governance owner.

### 33. Covenant Monitoring And Breach Workflows
**Justification:** The manifest description explicitly includes covenant monitoring. Commercial and structured products need covenant schedules, reporting obligations, and breach escalation inside the same package that owns the loan lifecycle.

**Improvement:** Add covenant records for financial reporting due dates, leverage thresholds, liquidity requirements, collateral tests, and reporting receipt status. Open a governed breach workflow when a covenant is missed or violated, with cure period tracking and approval gates for waivers.

**Acceptance evidence:** Covenant calendar fixtures, breach escalation tests, and workbench evidence showing open covenant exceptions alongside core servicing queues.

### 34. Servicing Fee Authorization And Fee-Waiver Governance
**Justification:** Fees often become the flashpoint in complaints, payoffs, and collections audits. Servicing needs precise controls over who can assess, waive, reverse, or capitalize each fee type.

**Improvement:** Create a fee catalog with allowable triggers, cap rules, waiver authority, refund logic, and statement presentation rules. Prevent ad hoc fee mutations by forcing all fee actions through governed commands with reason codes.

**Acceptance evidence:** Authorization tests by role and fee type, balance-change evidence for fee reversal and waiver, and UI history showing who changed a fee and under which policy authority.

### 35. Overrides, Exceptions, And Second-Review Controls
**Justification:** High-value lending operations always contain exceptions, but unmanaged override culture erodes risk discipline. The platform should distinguish allowed judgment from silent policy drift.

**Improvement:** Require structured override reasons, evidence attachments, approval thresholds, and expiry handling for underwriting, pricing, boarding, modification, and payoff exceptions. Add second-review requirements when the exception touches policy-critical fields such as amount, rate, collateral value, or delinquency reset.

**Acceptance evidence:** Tests that block privileged actions without the required approval chain, queue evidence for pending second review, and monthly override reports grouped by rule family and approver.

### 36. Multi-Tenant Policy Isolation And Configuration
**Justification:** The manifest already names multi-tenant isolation and runtime parameters. Lending operators need tenant-specific products, policies, notice packs, fee rules, and approval limits without data leakage or accidental cross-tenant rule reuse.

**Improvement:** Scope policy rules, runtime parameters, template sets, and governed models to tenant and product family. Add safe defaults for tenant onboarding while preventing one tenant from inheriting another tenant's disclosures, covenant packs, or loss-mitigation settings.

**Acceptance evidence:** Isolation tests for policy and template retrieval, negative fixtures for cross-tenant access, and configuration screens that display tenant scoping for every mutable rule or notice set.

### 37. Event-Sourced Loan Timeline And Replayability
**Justification:** The manifest includes event-sourced operational history, which is particularly valuable in lending where the institution must reconstruct the full path from application through payoff or charge-off.

**Improvement:** Emit domain-specific events for intake, decisioning, offer acceptance, funding, boarding, payment posting, delinquency movement, modification approval, payoff, and closure. Expose a replayable loan timeline so support, audit, and engineering can explain current state from immutable events rather than inferred snapshots.

**Acceptance evidence:** Event schema tests, timeline reconstruction tests for a full loan life cycle, and UI evidence that a user can inspect event order, actor, and resulting state from within the detail view.

### 38. Cross-PBC Event Contracts And Downstream Handoffs
**Justification:** Lending rarely lives alone. Policy, audit, and KPI events are already declared as consumed contracts, and funding or accounting consumers will also depend on precise event payloads.

**Improvement:** Harden event contracts around `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`, and add downstream handoff events for booked-loan activation, escrow setup, charge-off status change, and payoff completion. Each event should carry enough context to support dependent packages without exposing internal-only detail.

**Acceptance evidence:** Contract tests for emitted and consumed event versions, idempotency checks on repeated deliveries, and release notes showing exactly which downstream consumers were validated against the new payloads.

### 39. Workbench Queue And Persona-Specific UI
**Justification:** `LendingOriginationServicingWorkbench` exists in the manifest, but lending operations are queue-driven. Underwriters, closers, servicing specialists, collectors, and compliance reviewers do not need the same landing page.

**Improvement:** Split the workbench into persona-specific queues with saved filters, aging buckets, SLA indicators, exception severity, and quick actions appropriate to each role. Prioritize the queues that correspond to application review, stipulation chase, funding readiness, delinquency, complaints, and modification review.

**Acceptance evidence:** UI contract coverage for each persona queue, role-based action availability tests, and screenshots showing stage-appropriate columns and badges rather than one generic list.

### 40. Application Detail UI With Underwriting Evidence
**Justification:** `LendingOriginationServicingDetail` should make the approval rationale obvious. An underwriter or reviewer should not have to navigate across five tabs to reconstruct borrower facts, policy results, and conditions.

**Improvement:** Build an origination detail layout that presents borrower parties, verified income, bureau pulls, collateral summary, affordability ratios, decision reasons, and outstanding conditions in one coherent narrative. Surface the rule version and risk score used for decisioning beside the evidence that drove them.

**Acceptance evidence:** View-model tests for the detail screen, screenshots showing the evidence layout for approved and declined files, and usability evidence that condition status and decision rationale remain visible without extra drilling.

### 41. Servicing Detail UI With Timeline And Balances
**Justification:** Servicing specialists need one place to see unpaid principal, accrued interest, escrow position, delinquency state, recent payments, and pending exceptions. Fragmented views slow down collections, payoff work, and complaint response.

**Improvement:** Build a servicing detail experience that combines balance snapshot, transaction history, next due breakdown, escrow buckets, delinquency posture, active cases, and payoff readiness. Make the event timeline a first-class sidebar so recent actions and notices are visible in context.

**Acceptance evidence:** Screen contracts for current, delinquent, and modified loans, component tests for balance and timeline widgets, and visual proof that the key servicing facts fit within the primary view hierarchy.

### 42. Collections And Delinquency UI Tooling
**Justification:** Collections work is interaction-heavy. Agents need rapid access to contact history, payment commitments, hardship path eligibility, and prohibited-action warnings without leaving the queue.

**Improvement:** Add a collections workspace inside `LendingOriginationServicingAssistantPanel` that shows contact log, call outcome, promise-to-pay status, available workout options, and compliance warnings for stay, cease-contact, or complaint hold scenarios. Optimize keyboard-driven queue progression for high-volume collectors.

**Acceptance evidence:** UI interaction tests for collector workflows, accessibility checks on quick-action controls, and screenshots showing compliance warnings pinned next to available next steps.

### 43. Agent Skill For Origination Intake Assistant
**Justification:** The manifest already includes agentic document intake and AI task assistance. Origination benefits from a guided assistant that helps assemble complete files without mutating governed data blindly.

**Improvement:** Create an intake skill that drafts borrower and application records from uploaded documents and structured prompts, highlights missing fields, proposes stipulations, and requests confirmation before writing anything to governed tables. The skill should understand borrower role assignment, purpose, product fit, and document sufficiency.

**Acceptance evidence:** Skill prompts and test conversations that produce draft-but-not-posted changes, citation spans back to source documents, and permission tests proving the assistant cannot bypass required confirmations.

### 44. Agent Skill For Underwriter Copilot
**Justification:** Underwriters need acceleration, not automation theater. A useful copilot summarizes evidence, identifies policy tensions, and prepares decision rationales while leaving the credit judgment with the authorized reviewer.

**Improvement:** Build an underwriting assistant that assembles income, bureau, collateral, affordability, and exception facts into a structured recommendation with explicit uncertainty markers. Include simulation support so the underwriter can ask how amount, term, or collateral haircut changes would alter the decision.

**Acceptance evidence:** Conversation traces showing evidence-backed recommendations, simulation outputs tied to policy versions, and reviewer feedback capture on whether the assistant's proposed rationale was accepted, edited, or rejected.

### 45. Agent Skill For Servicing And Modification Assistant
**Justification:** Servicing staff spend large amounts of time reconstructing account status before answering one question. An assistant can reduce handling time only if it understands balances, delinquency, escrow, promises, and modification history.

**Improvement:** Add a servicing skill that can summarize account posture, explain recent balance movement, prepare payoff checklists, outline hardship options, and draft modification comparison views. Keep the skill read-first and approval-gated for any action that would affect balance, delinquency status, or borrower communication.

**Acceptance evidence:** Evaluated conversations for payoff, delinquency, and hardship scenarios, evidence of blocked attempts to take privileged actions without approval, and operator ratings on answer usefulness and factual accuracy.

### 46. Agent Skill For Compliance And Audit Evidence Assembly
**Justification:** Audit preparation is expensive when evidence lives in many records and event streams. The package already names cryptographic proofs and continuous control testing; the assistant should help assemble those artifacts, not invent them.

**Improvement:** Build a compliance skill that gathers policy version, decision lineage, notice history, override approvals, control results, and sealed audit references into a review packet for a specified loan, period, or rule family. The skill should point to existing evidence rather than narrate unsupported conclusions.

**Acceptance evidence:** Skill runs that produce auditable evidence packets for underwriting review and servicing complaint review, citation links to the underlying records and events, and tests showing that unsupported claims are withheld when evidence is incomplete.

### 47. Release Evidence Pack And Traceability Matrix
**Justification:** The manifest includes `RELEASE_EVIDENCE.md`, but lending changes require more than a generic release note. Teams need traceability from rule change or UI change to tests, approvals, and impacted lifecycle stages.

**Improvement:** Create a release evidence structure that maps every change to affected APIs, tables, events, notices, controls, UI fragments, and agent skills. Include explicit coverage for origination, decisioning, boarding, servicing, delinquency, modification, escrow, and payoff flows so no critical stage is omitted from signoff.

**Acceptance evidence:** A traceability matrix generated for a sample release, signoff records by product owner and compliance reviewer, and proof that each changed surface has linked verification artifacts.

### 48. Continuous Control Testing And Sealed Audit Proofs
**Justification:** The advanced capabilities already call out continuous control testing and cryptographic audit proofs. Lending benefits when segregation-of-duties, approval, notice, and balance-integrity checks run continuously instead of waiting for a quarterly review.

**Improvement:** Add control assertions for approval authority, override limits, boarding completeness, notice delivery, payment allocation integrity, escrow analysis timing, and payoff closure steps. Seal the resulting evidence so later audits can verify that the test results were not altered after the fact.

**Acceptance evidence:** Passing and intentionally failing control runs stored against `lending_origination_servicing_control_assertion`, sealed proof verification for a sampled control set, and dashboards showing open control breaks by severity.

### 49. Synthetic Test Portfolios And Operational Dashboards
**Justification:** Lending quality is best proven on realistic portfolios, not only isolated unit cases. Operations also need a supervisory layer that turns raw events into throughput, risk, and aging insight.

**Improvement:** Build synthetic portfolios that cover prime consumer loans, thin-file applicants, secured collateralized loans, modified hardship loans, escrowed mortgages, delinquent accounts, charged-off accounts, and payoff requests. Use those portfolios to drive `lending_origination_servicing_workbench_metric` dashboards for volume, turn time, delinquency migration, modification outcomes, complaint aging, and queue health.

**Acceptance evidence:** Reusable seeded scenarios, dashboard tests built from the synthetic portfolio data, and KPI evidence showing the package can report lifecycle performance without manual spreadsheet assembly.

### 50. Release Readiness, Cutover, And Post-Release Verification
**Justification:** Lending changes touch balances, notices, and customer outcomes. Production readiness needs explicit cutover criteria, rollback posture, and early-life monitoring rather than a generic deploy checklist.

**Improvement:** Define release gates for migration readiness, policy effective-date alignment, queue backfill completion, user training, notice-template approval, and dashboard baselines. Add post-release verification for sample application decisions, funded-loan boarding, payment posting, delinquency movement, escrow analysis, modification booking, and payoff closure during the first operating window after release.

**Acceptance evidence:** A signed readiness checklist, cutover validation logs, post-release sample review results across the major lifecycle stages, and a documented rollback decision path if any verification step fails.
