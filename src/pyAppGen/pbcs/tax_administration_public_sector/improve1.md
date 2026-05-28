## Current Domain Evidence Used

- Manifest key: `tax_administration_public_sector`.
- Manifest description: taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration.
- Owned tables named in the manifest: `taxpayer_account`, `tax_filing`, `assessment`, `audit_case`, `collection_action`, `appeal`, `tax_notice`, policy-rule, runtime-parameter, schema-extension, control-assertion, and governed-model tables.
- Current command and read surfaces in the manifest: `POST /taxpayer-accounts`, `POST /tax-filings`, `POST /assessments`, `POST /audit-cases`, `POST /collection-actions`, and `GET /tax-administration-public-sector-workbench`.
- Current workflows in the manifest: taxpayer-account creation and tax-filing recording.
- Current UI fragments in the manifest: `TaxAdministrationPublicSectorWorkbench`, `TaxAdministrationPublicSectorDetail`, and `TaxAdministrationPublicSectorAssistantPanel`.
- Current event contract evidence in the manifest: emitted lifecycle events plus consumed `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Current release artifacts named in the manifest: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`, `migrations/001_initial.sql`, and `tests/test_contract.py`.

### 1. Canonical taxpayer identity and TIN lifecycle
**Justification:** Identity defects contaminate registrations, returns, assessments, collections, refunds, and appeals; the package needs one authoritative taxpayer account history instead of ad hoc corrections.
**Improvement:** Extend `taxpayer_account` to track provisional identifiers, final TIN issuance, duplicate detection, merge and split operations, successor liability, deceased or dissolved status, and effective-dated name, address, and contact history.
**Acceptance evidence:** Contract tests for merge, split, and successor scenarios; detail-page timeline showing effective-dated identity changes; event snapshots for account registration, correction, merge, split, suspension, and closure.

### 2. Registration case model by taxpayer role
**Justification:** Public-sector tax administration must distinguish ordinary taxpayers from employers, withholding agents, VAT registrants, excise operators, and exempt entities because each role drives different obligations and controls.
**Improvement:** Add a registration case layer that captures legal form, residency, tax roles, start and cessation dates, supporting documents, approval checkpoints, and registration outcome codes before an account becomes active.
**Acceptance evidence:** Seed scenarios for individual, company, government body, employer, and withholding-agent registrations; approval-path tests; UI queue separating pending, approved, rejected, and ceased registrations.

### 3. Branch, site, and establishment registration
**Justification:** Many liabilities attach to operating locations rather than the head office alone, so one flat account record cannot support inspection, local filing, and collection work.
**Improvement:** Model branch and establishment registrations with parent-child linkage, effective dates, local jurisdiction assignment, closure reason, and filing responsibilities inherited or overridden at site level.
**Acceptance evidence:** Schema and handler tests for branch activation and closure; workbench views that roll liabilities up to the parent while preserving branch detail; audit trail for branch obligation reassignment.

### 4. Filing obligation engine by tax type and status
**Justification:** Filing compliance depends on registration status, tax type, period frequency, threshold changes, and cessation events; missing this engine makes downstream notices and penalties unreliable.
**Improvement:** Create an obligation service that derives monthly, quarterly, annual, event-driven, and nil-return obligations from registration facts, policy rules, and effective dates, then materializes due dates and grace periods.
**Acceptance evidence:** Executable fixtures for VAT, payroll withholding, corporate income, presumptive, and annual information returns; tests for cessation, late registration, and threshold-triggered obligation creation; UI obligation calendar.

### 5. Return intake normalization across channels
**Justification:** Returns arrive through API payloads, keyed forms, uploaded schedules, and agent-assisted drafts; without normalization the package will create inconsistent balances and false audit risk.
**Improvement:** Build a return-intake pipeline for `tax_filing` that standardizes tax period references, currency precision, schedule totals, taxpayer references, preparer details, and document attachments before validation.
**Acceptance evidence:** Golden fixtures for manual, API, bulk-upload, and document-derived return intake; rejected-record queue with field-level reasons; preview step in `TaxAdministrationPublicSectorAssistantPanel` before mutation.

### 6. Return validation for original, nil, late, and amended filings
**Justification:** Public revenue operations depend on period integrity; the package must distinguish original returns, nil returns, replacements, and amendments so assessments and penalties remain defensible.
**Improvement:** Add validation rules for overlapping periods, missing schedules, out-of-range amounts, nil-return eligibility, amendment reason codes, superseded versions, and statutory cutoffs for amendment acceptance.
**Acceptance evidence:** Tests covering duplicate period submissions, nil-return misuse, late amendments, and supersession chains; UI badges for original versus amended status; clear rejection reasons in API responses.

### 7. Assessment engine for self, default, estimated, and adjusted liabilities
**Justification:** Assessment is more than storing a number; public-sector tax administration needs to show why liability exists and how it changed over time.
**Improvement:** Expand `assessment` to support self-assessed, default, estimated, audit-adjusted, additional, reduced, and jeopardy assessments with linked basis, effective dates, tax period references, and statutory authority codes.
**Acceptance evidence:** Assessment-calculation fixtures for each assessment type; audit-proof links from assessment records to return, audit, or policy basis; statement-of-account projection showing reversal and replacement chains.

### 8. Penalty and interest accrual rules
**Justification:** Penalties and interest are core revenue controls and frequent appeal subjects; they cannot remain implicit side effects outside the package.
**Improvement:** Add a rules engine for late-filing penalties, late-payment penalties, interest accrual, suspension, waiver, remission, and recalculation when an assessment is amended or an appeal stays recovery.
**Acceptance evidence:** Rule-version manifests, accrual tests across changing rates and calendars, supervisor override logs, and UI evidence showing how each balance component was computed.

### 9. Statement-of-account and balance reconstruction
**Justification:** Caseworkers, taxpayers, auditors, and courts need one explainable account statement that reconciles obligations, assessments, penalties, credits, refunds, and collection actions.
**Improvement:** Create a taxpayer account statement projection that orders every posting by effective date and posting date, groups by tax type and period, and exposes opening balance, charges, credits, payments, refunds, write-downs, and closing balance.
**Acceptance evidence:** Replay tests that reconstruct balances from events; downloadable statement samples for multiple tax types; workbench drill-through from balance line to source return, assessment, notice, or collection action.

### 10. Payments boundary with treasury and banking channels
**Justification:** The package must own liability, allocation intent, and payment status evidence while avoiding hidden ownership of settlement rails, bank acquiring, or card processing.
**Improvement:** Define an explicit payments boundary where `tax_administration_public_sector` records payment references, receipt evidence, allocation instructions, reversals, and reconciliation results while consuming settlement confirmations from treasury or payment platforms.
**Acceptance evidence:** Boundary contract documenting owned versus external states; idempotent handlers for payment-confirmed, payment-reversed, and reconciliation-failed events; negative tests proving no direct dependency on bank settlement tables.

### 11. Payment allocation and reallocation controls
**Justification:** A single payment often covers several periods or tax types, and poor allocation drives avoidable debt, notices, and refund claims.
**Improvement:** Add allocation rules for oldest debt first, taxpayer-declared reference, legal priority, penalty-first or principal-first treatment, and supervised reallocation with reason codes and approval thresholds.
**Acceptance evidence:** Allocation fixtures spanning single and mixed-tax payments; reallocation approval tests; account detail view showing original allocation and subsequent reallocations with actor attribution.

### 12. Suspense, unapplied cash, and credit balances
**Justification:** Public-sector ledgers accumulate unidentified or excess amounts that must remain visible and controlled until ownership and application are resolved.
**Improvement:** Introduce suspense and credit-balance states for unmatched receipts, overpayments, and misdirected deposits, with work queues for identification, taxpayer confirmation, transfer, offset, or refund.
**Acceptance evidence:** Queue metrics for aged suspense items; offset and clearance tests; release evidence showing suspense items cannot disappear without documented resolution.

### 13. Refund eligibility and fraud screening
**Justification:** Refunds are high-risk cash outflows; the package needs stronger control than a simple negative balance check.
**Improvement:** Model refund claims, automatic eligibility gates, offset-against-debt rules, pre-refund risk scoring, document requirements, bank-detail verification, and maker-checker approvals before a refund instruction is emitted.
**Acceptance evidence:** Seed cases for clean refund, debt-offset refund, duplicate bank account flag, and fraudulent document flag; approval logs; exported refund packet containing liability, offset, and verification evidence.

### 14. Exemptions, waivers, and certificate governance
**Justification:** Exemptions and waivers change obligations, assessments, and collections, so they need first-class lifecycle management with expiry and revocation.
**Improvement:** Add controlled records for statutory exemptions, discretionary waivers, withholding certificates, zero-rate certificates, and remission decisions, including legal basis, effective period, limits, and revocation triggers.
**Acceptance evidence:** Tests for exemption issuance, expiry, renewal, and revocation; obligation recalculation when an exemption changes; UI panel linking certificates to affected liabilities and notices.

### 15. Notice template governance and statutory wording
**Justification:** Notices carry legal consequences; incorrect wording, dates, or citations can void enforcement and weaken appeals defense.
**Improvement:** Create governed notice templates for registration outcomes, return reminders, estimated assessments, debt demands, audit invitations, appeal decisions, and refund decisions with policy versioning and jurisdiction-specific clauses.
**Acceptance evidence:** Template snapshots with version history; rendering tests for each notice type; approval workflow proving only authorized policy owners can publish statutory wording.

### 16. Notice delivery evidence and returned-contact handling
**Justification:** Service of notice is often litigated, so the package must prove when, how, and to which address or channel each notice was delivered or failed.
**Improvement:** Track outbound mail, email, portal publication, SMS summary, delivery attempts, bounce or return status, address quality issues, and re-service actions on `tax_notice`.
**Acceptance evidence:** Delivery-event contracts, returned-mail work queue, address-correction workflow, and appeal packet exports showing service evidence for the contested notice.

### 17. Audit case selection and intake
**Justification:** Audit capacity is limited; case selection must be explainable to supervisors and defensible against bias and arbitrary targeting claims.
**Improvement:** Expand `audit_case` intake to record source trigger, selected risk factors, third-party discrepancy links, random-sample flags, campaign membership, materiality score, and required approval for high-profile or sensitive audits.
**Acceptance evidence:** Risk-trigger fixtures, campaign selection reports, and UI cards showing why a case entered audit; tests ensuring non-selected taxpayers are not exposed in audit queues.

### 18. Audit workpapers and evidence chain
**Justification:** Audit findings fail in objection and appeal if evidence lineage, document handling, and interview notes are incomplete or mutable.
**Improvement:** Add governed workpaper records for evidence requests, field visits, interviews, third-party confirmations, sample tests, computation sheets, and findings, each with source references and tamper-evident history.
**Acceptance evidence:** Workpaper model tests, attachment lineage reports, immutable history checks, and detail-page tabs for evidence, interviews, findings, and supervisor review.

### 19. Audit outcomes and post-audit adjustments
**Justification:** Audit results should flow into assessments, penalties, notices, and collection posture without manual spreadsheet bridges.
**Improvement:** Create audited adjustment flows that post additional assessments, reduce liabilities, close findings with no-change outcomes, and trigger follow-on notices, penalties, or refund reconsideration.
**Acceptance evidence:** End-to-end scenario from audit finding to adjusted assessment and notice issuance; reversal tests when an audit adjustment is overturned; release evidence tying audit outcomes to account balance changes.

### 20. Objection intake and dispute-clock management
**Justification:** Objections are time-bound rights; missing receipt date, grounds, or completeness checks creates avoidable litigation risk.
**Improvement:** Add an objection intake layer that records challenged decision, date served, date received, grounds, requested relief, supporting documents, completeness status, and stay-of-collection effect.
**Acceptance evidence:** Timeliness tests around statutory deadlines; completeness checklist in the assistant panel; queue views for accepted, deficient, withdrawn, and out-of-time objections.

### 21. Appeals lifecycle and external forum handoff
**Justification:** Appeals often move from internal review to tribunal or court, and the package must preserve one continuity chain across those stages.
**Improvement:** Expand `appeal` to cover internal appeal, tribunal appeal, court escalation, remand, consent settlement, and decision implementation, with forum reference numbers and hearing dates.
**Acceptance evidence:** Scenario tests for internal appeal through tribunal remand; calendar integration for hearings; event evidence showing when collections were stayed, resumed, or permanently adjusted.

### 22. Collections strategy ladder
**Justification:** Debt recovery needs ordered, policy-driven escalation rather than isolated collection actions that ignore debt age, dispute status, or taxpayer behavior.
**Improvement:** Add a collections strategy engine that sequences reminder, demand, call task, payment arrangement offer, offset, agency referral, asset action, garnishment request, and write-off recommendation based on debt attributes.
**Acceptance evidence:** Treatment-path fixtures by debt age and risk; supervisor override logs; queue panels showing current strategy stage, next action, and legal blockers.

### 23. Installment plans, hardship relief, and compromise
**Justification:** Public-sector collections must balance recovery with legal relief mechanisms; those decisions need controlled terms and monitoring.
**Improvement:** Model installment agreements, hardship deferrals, settlement offers, and compromise approvals with affordability evidence, broken-plan detection, re-default logic, and linkage to underlying debt items.
**Acceptance evidence:** Tests for plan creation, missed installment, reinstatement, and compromise rejection; balance projection reflecting stayed penalties or resumed accruals; approval evidence for relief decisions.

### 24. Enforcement prerequisites and legal holds
**Justification:** Enforcement taken before notice, appeal, or approval prerequisites are met creates reputational and legal exposure.
**Improvement:** Add hard gating rules so high-impact `collection_action` records cannot proceed unless service evidence, debt certification, appeal status, approval thresholds, and legal-hold checks all pass.
**Acceptance evidence:** Negative tests blocking premature enforcement; UI lock indicators with unmet prerequisites; audit reports listing every enforcement action and its satisfied legal conditions.

### 25. Account holds, freezes, and release controls
**Justification:** Investigations, insolvency, litigation, identity compromise, and policy moratoria all require partial or full holds on taxpayer activity.
**Improvement:** Introduce hold types on `taxpayer_account` for registration change, refund release, enforcement pause, audit hold, appeal stay, and data-correction freeze, each with start, end, reason, and approving actor.
**Acceptance evidence:** Hold-lifecycle tests; detail-page banner showing active holds and blocked actions; event records proving held actions were denied or deferred rather than silently processed.

### 26. Third-party data matching and discrepancy cases
**Justification:** Tax administrations increasingly rely on payroll, customs, land, financial, and procurement feeds to detect under-reporting and non-filing.
**Improvement:** Add discrepancy-case handling that compares returns and account data against third-party statements, flags mismatches, opens cases, and tracks taxpayer explanation, correction, or escalation to audit.
**Acceptance evidence:** Matching-rule fixtures, discrepancy queues by feed type, and case timelines showing source statement, detected variance, taxpayer response, and resolved outcome.

### 27. Risk scoring for compliance and revenue exposure
**Justification:** Risk scoring must support selection, treatment, and approval prioritization without becoming an opaque black box.
**Improvement:** Expand analytics to score non-registration risk, non-filing risk, underpayment risk, refund fraud risk, audit yield potential, and collection recoverability using explainable features from obligations, returns, notices, and historical behavior.
**Acceptance evidence:** Feature manifest, calibration report, and explanation cards on workbench items; supervisor feedback loop for false positives and false negatives; drift alerts in release evidence.

### 28. Debt prioritization and treatment recommendation
**Justification:** Collection teams need recommendations that weigh materiality, collectability, dispute posture, and public-interest sensitivity, not only balance size.
**Improvement:** Add treatment recommendations that rank debts for reminder, arrangement, field visit, offset, enforcement, or hold based on debt age, asset indicators, appeal status, compliance history, and expected recovery.
**Acceptance evidence:** Ranked debt queue with factor explanations; backtesting against historical recovery outcomes; evidence showing recommendations can be accepted, overridden, or rejected with reasons.

### 29. Domain event catalog expansion
**Justification:** The current generic emitted events are too coarse to support downstream consumers that need tax-specific state changes and evidence handoffs.
**Improvement:** Define typed events for registration accepted or ceased, obligation created, return received, assessment raised or amended, payment allocated, refund approved, notice served, audit opened or closed, appeal stayed, and debt treatment changed.
**Acceptance evidence:** Versioned schema snapshots, producer and consumer contract tests, and traceability from each event to the originating record and actor.

### 30. Idempotent commands and duplicate suppression
**Justification:** Duplicate return submissions, repeated payment notifications, and retried notice commands are common in tax operations and will corrupt balances if not controlled.
**Improvement:** Strengthen idempotent handlers around account creation, return receipt, assessment posting, payment allocation, refund initiation, and collection action issuance using natural business keys plus explicit request identifiers.
**Acceptance evidence:** Replay tests with repeated API commands and repeated consumed events; dead-letter entries only for unresolved conflicts; release evidence proving no duplicate postings in seeded scenarios.

### 31. Exception taxonomy and dead-letter remediation
**Justification:** Operators need domain-language failures such as unmatched payment, invalid tax period, missing service evidence, and stayed debt, not generic transport errors.
**Improvement:** Create a tax-specific exception catalog with severity, taxpayer impact, legal impact, retry eligibility, owner role, and remediation playbook for inbound commands, event handlers, notice generation, and risk-scoring jobs.
**Acceptance evidence:** Dead-letter workbench showing domain reasons and next steps; SLA metrics by exception type; closure evidence linking each resolved exception to the corrected record or policy change.

### 32. Workbench queue design by operating function
**Justification:** Registration officers, return reviewers, auditors, collectors, appeals officers, and supervisors each need different queue semantics and evidence density.
**Improvement:** Rework `TaxAdministrationPublicSectorWorkbench` into function-specific queues for registrations, obligations, returns, assessments, refunds, audits, appeals, notices, and collections, each with tailored filters and bulk actions.
**Acceptance evidence:** Route and permission tests for each queue; empty, error, and stale-data states; operator usability evidence showing queues no longer require raw-table lookups.

### 33. Account detail UI with chronology, balances, and linked cases
**Justification:** A tax caseworker should understand the whole taxpayer relationship from one page rather than stitching together separate screens and exports.
**Improvement:** Expand `TaxAdministrationPublicSectorDetail` into an account cockpit showing identity history, active registrations, obligation calendar, account statement, notices, payments, refunds, audits, appeals, and collection actions in one chronological view.
**Acceptance evidence:** Component tests for chronology tabs and balance drill-through; screenshots in release evidence; access-control tests ensuring sensitive panels respect role and hold state.

### 34. Supervisor and policy owner UI for rules and parameters
**Justification:** Penalty rules, filing calendars, treatment thresholds, and assistant policies must be tunable by authorized owners without code edits or undocumented database changes.
**Improvement:** Add governed screens for rule versioning, parameter promotion, impact preview, rollback, and approval of tax policy changes that affect obligations, scoring, notices, and automation boundaries.
**Acceptance evidence:** UI tests for draft, review, approve, activate, and rollback flows; audit logs for every rule or parameter change; comparison view showing before and after operational impact.

### 35. Caseworker assistant skill for taxpayer account operations
**Justification:** Frontline staff benefit from AI assistance only if it is grounded in owned records, constrained by permissions, and explicit about uncertainty.
**Improvement:** Create an assistant skill that summarizes taxpayer posture, highlights overdue obligations and active disputes, drafts next steps, and prepares account notes without bypassing approvals or hidden data access.
**Acceptance evidence:** Skill manifest, permission tests, cited summaries using owned records, and blocked-action evidence when the assistant attempts a restricted operation.

### 36. Registration and return intake assistant skill
**Justification:** Public-sector intake work is document-heavy and repetitive; the assistant should reduce manual data entry while preserving legal accuracy.
**Improvement:** Add a governed intake skill that extracts registration facts, return figures, schedules, and attachment metadata from uploaded documents and prepares drafts with source-span citations for human confirmation.
**Acceptance evidence:** Extraction fixtures for registration forms and return schedules; confidence thresholds and fallback handling; assistant preview in `TaxAdministrationPublicSectorAssistantPanel` before saving.

### 37. Notice drafting and correspondence assistant skill
**Justification:** Notice preparation consumes expert time and errors in dates, periods, or statutory wording create downstream appeal risk.
**Improvement:** Add an assistant skill that drafts notices and internal correspondence from approved templates, pulling period data, balances, due dates, and service channels from governed records while forcing human approval before issue.
**Acceptance evidence:** Prompt and output governance record, rendered-draft tests by notice type, and audit events showing who reviewed and issued each assistant-generated notice.

### 38. Audit and appeals research assistant skill
**Justification:** Officers need fast synthesis of prior adjustments, cited evidence, notice history, and procedural deadlines when preparing audit findings or appeal decisions.
**Improvement:** Create a research skill that compiles chronology, disputed issues, linked evidence, prior decisions, and deadline warnings for a given audit or appeal without generating uncited assertions.
**Acceptance evidence:** Response fixtures with source citations to account, notice, audit, and appeal records; negative tests blocking unsupported claims; user feedback capture on usefulness and accuracy.

### 39. Release evidence traceability from manifest to proof
**Justification:** The package should not claim readiness unless every declared capability, API, table, event, workflow, and UI fragment maps to executable evidence.
**Improvement:** Build a traceability matrix from `manifest.py` entries to tests, scenario seeds, screenshots, API contracts, event contracts, and release checks in `RELEASE_EVIDENCE.md`.
**Acceptance evidence:** Machine-readable trace table, failing release gate when a manifest item lacks proof, and generated report linking each manifest claim to current verification artifacts.

### 40. Seeded taxpayer journey scenarios
**Justification:** Tax administration quality is best proven through whole journeys, not isolated unit tests.
**Improvement:** Add scenario packs for new registration to first return, chronic non-filer to default assessment, matched payment to clearance, refund claim with fraud review, audit adjustment to appeal, and installment-plan breach to enforcement review.
**Acceptance evidence:** Named seed datasets, smoke-test outputs, and release screenshots for each journey; replayable end-to-end logs showing record, event, and UI consistency.

### 41. Jurisdiction and tenant isolation
**Justification:** Public-sector deployments often span multiple jurisdictions or agencies with different forms, rates, notice wording, and secrecy rules.
**Improvement:** Strengthen tenant and jurisdiction partitioning so rules, templates, parameters, risk models, and release evidence are scoped cleanly without cross-jurisdiction leakage.
**Acceptance evidence:** Cross-tenant negative tests, policy-difference fixtures, and workbench views showing jurisdiction-specific wording, calendars, and thresholds from isolated configuration.

### 42. Privacy, secrecy, legal hold, and retention controls
**Justification:** Tax records are among the most sensitive public-sector datasets, and the package must enforce secrecy and retention law as a built-in control.
**Improvement:** Add field classifications, masking rules, export approvals, retention clocks, litigation hold support, and assistant redaction policies across accounts, returns, notices, audits, and appeals.
**Acceptance evidence:** Masked UI snapshots, export-denial tests, retention-expiry jobs with hold exceptions, and release evidence documenting secrecy controls on assistant outputs.

### 43. Filing campaigns, reminders, and compliance outreach
**Justification:** Raising voluntary compliance requires targeted campaigns before liabilities age into enforcement.
**Improvement:** Create campaign management for obligation-based reminders, segmented by tax type, geography, risk band, and filing history, with controlled reminder frequency and channel preference.
**Acceptance evidence:** Campaign seed cases, reminder delivery metrics, opt-out or preference handling where allowed, and evidence that campaign actions feed obligation and notice history rather than separate shadow systems.

### 44. API surface completeness for tax operations
**Justification:** The current manifest exposes create-heavy endpoints but lacks the query, correction, simulation, export, and bulk interfaces needed for real tax administration work.
**Improvement:** Expand the API contract to include search, obligation retrieval, statement retrieval, amendment commands, refund workflow actions, notice issue actions, simulation endpoints, and export endpoints with strict versioning.
**Acceptance evidence:** OpenAPI-style contract snapshots, backward-compatibility tests, idempotency tests for action endpoints, and examples for bulk and query operations tied to seeded journeys.

### 45. Counterfactual simulation for policy and workload changes
**Justification:** Leaders need to know how changing due dates, thresholds, penalty rates, or audit-selection policy would affect revenue, queues, and taxpayer impact before activation.
**Improvement:** Add a simulation workbench that replays obligations, returns, debt treatment, and audit selection under alternate policy parameters without mutating live records.
**Acceptance evidence:** Scenario reports comparing baseline and simulated outcomes; non-mutating test guarantees; supervisor review log for simulation assumptions and chosen policy action.

### 46. Historical migration and balance backfill
**Justification:** Most deployments begin with partial historical data, and inaccurate opening balances will undermine trust in every subsequent action.
**Improvement:** Build migration and reconciliation tooling to import legacy taxpayer accounts, obligations, assessments, and payments, classify unresolved gaps, and establish opening balances with variance explanations.
**Acceptance evidence:** Migration dry-run reports, reconciliation variance thresholds, import idempotency tests, and detail-page evidence distinguishing migrated history from native events.

### 47. Operational metrics and service-level evidence
**Justification:** Tax operations need measurable control over registration turnaround, filing backlog, refund aging, appeal delay, audit cycle time, and debt treatment effectiveness.
**Improvement:** Expand analytics to produce queue age, processing time, breach rates, recovery rate, refund turnaround, objection timeliness, and assistant-acceptance metrics by function and jurisdiction.
**Acceptance evidence:** Metric definitions with data lineage, dashboard tests, SLA breach alerts, and release evidence showing current values against configured thresholds.

### 48. Accessibility, localization, and format correctness
**Justification:** A public-sector tax system must work for diverse taxpayers and officers across languages, disability contexts, and local date, amount, and address formats.
**Improvement:** Improve UI and notice rendering to support keyboard-only workflows, screen readers, locale-specific amounts and dates, multilingual labels, and jurisdiction-specific terminology.
**Acceptance evidence:** Accessibility checks on workbench and detail screens, localized notice snapshots, and automated tests for date, currency, and address formatting by locale.

### 49. Continuous controls and cryptographic audit proof
**Justification:** High-trust public revenue systems need live control monitoring and proof that key evidence was not silently altered after the fact.
**Improvement:** Add continuous assertions for maker-checker separation, stayed-debt enforcement blocks, refund approval thresholds, notice-service completeness, and event-chain integrity, then seal key evidence with hash-linked proofs.
**Acceptance evidence:** Failing-control fixtures, control dashboards, proof-verification scripts, and audit exports showing sealed evidence for selected registration, refund, audit, and collections cases.

### 50. Go-live release gate and rollback evidence
**Justification:** Production promotion should require proof that registrations, obligations, returns, assessments, payments boundary handling, refunds, audits, appeals, notices, collections, UI, agent skills, and events all behave coherently.
**Improvement:** Define a final release gate that blocks deployment unless seeded journeys, API contracts, event contracts, UI checks, assistant-skill checks, control assertions, and rollback rehearsals all pass for the current package version.
**Acceptance evidence:** Signed release checklist, rollback drill output, manifest-to-evidence report, and a failing gate when any declared area of `tax_administration_public_sector` lacks current proof.
