# Research Grants Management Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `research_grants_management`.
- Manifest description: research proposals, awards, budgets, compliance, milestones, subawards, effort, and sponsor reporting.
- Owned tables already declared: `grant_proposal`, `research_award`, `sponsor_budget`, `compliance_requirement`, `subaward`, `milestone_report`, `effort_certification`, `research_grants_management_policy_rule`, `research_grants_management_runtime_parameter`, `research_grants_management_schema_extension`, `research_grants_management_control_assertion`, and `research_grants_management_governed_model`.
- Current APIs already declared: `POST /grant-proposals`, `POST /research-awards`, `POST /sponsor-budgets`, `POST /compliance-requirements`, `POST /subawards`, and `GET /research-grants-management-workbench`.
- Current workflows already declared: `research_grants_management_create_grant_proposal_workflow` and `research_grants_management_record_research_award_workflow`.
- Current UI fragments already declared: `ResearchGrantsManagementWorkbench`, `ResearchGrantsManagementDetail`, and `ResearchGrantsManagementAssistantPanel`.
- Current emitted events already declared: `ResearchGrantsManagementCreated`, `ResearchGrantsManagementUpdated`, `ResearchGrantsManagementApproved`, and `ResearchGrantsManagementExceptionOpened`.
- Current consumed events already declared: `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Current evidence documents already declared: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

### 1. Funding opportunity source registry

**Justification:** Proposal quality starts before `grant_proposal` creation. The PBC has proposal and award endpoints, but it does not yet show a first-class place for sponsor announcement version, program code, cycle, or archived opportunity terms that drive the rest of the lifecycle.

**Improvement:** Add an owned funding opportunity registry that stores sponsor program identifier, notice version, internal routing deadline, sponsor deadline, sponsor type, anticipated award type, cost-share expectation, and archived source files. Require proposal creation to reference either a registered opportunity or a justified manual entry path.

**Acceptance evidence:** Schema and API contract for opportunity records, workbench screens that create a proposal from an opportunity, fixtures covering federal, foundation, and industry-style opportunities, and release evidence showing historical opportunity versions remain traceable after sponsor notice updates.

### 2. Opportunity eligibility and institutional fit rules

**Justification:** Opportunity intake is incomplete if the system cannot tell whether the institution, principal investigator, or collaborator set is actually eligible. Early disqualification saves proposal effort and reduces avoidable routing noise.

**Improvement:** Add rules that evaluate sponsor eligibility language against investigator status, organization type, career stage, institutional location, cost-share availability, and limited submission constraints. Record a structured pass, conditional pass, or blocked result before a proposal can enter formal routing.

**Acceptance evidence:** Eligibility rule fixtures for common sponsor scenarios, blocked proposal creation tests, operator override capture with justification, and detail-page evidence showing which specific rule or announcement clause caused the result.

### 3. Limited-submission nomination workflow

**Justification:** Limited submission opportunities require internal competition before proposal work begins. Treating them like ordinary opportunities causes duplicate effort and governance failures.

**Improvement:** Add a nomination workflow that tracks internal call publication, nominee packets, review committee decisions, alternates, and final institutional slot allocation. Prevent more sponsor-bound proposals than the opportunity allows unless an authorized exception is captured.

**Acceptance evidence:** Workflow tests for nomination open, review, selection, and rejection states, UI evidence for ranking nominees, enforcement of sponsor slot limits, and emitted exception events when a proposal attempts to bypass the internal nomination process.

### 4. Opportunity deadline calendar and routing cutoffs

**Justification:** Research administration misses deadlines because sponsor due dates and internal approvals are often managed outside the award system. The PBC needs its own domain calendar logic for proposal readiness.

**Improvement:** Add deadline objects for sponsor submission, institutional routing, compliance review, budget finalization, collaborator packet receipt, and narrative freeze. Display countdowns and dependency-aware warnings in `ResearchGrantsManagementWorkbench`.

**Acceptance evidence:** Calendar projection tests, workbench snapshots with aging buckets, reminder event generation for upcoming cutoffs, and release evidence showing deadline recalculation when sponsor dates change or institutional holidays shift.

### 5. Proposal assembly workspace and section status

**Justification:** A proposal is not a single blob. Operators need a structured view of narrative sections, attachments, approvals, and unresolved gaps before it becomes a sponsor-bound package.

**Improvement:** Extend `grant_proposal` with typed sections for abstract, aims, narrative, budget justification, biosketches, facilities, letters, data plans, and sponsor forms. Track each section as missing, draft, under review, approved, or blocked with owner and due date metadata.

**Acceptance evidence:** Proposal section state transitions, UI evidence for incomplete package detection, attachment integrity checks, and test fixtures proving submission cannot proceed while required sections remain missing or blocked.

### 6. Proposal compliance matrix before submission

**Justification:** Proposal routing is only defensible if every sponsor and institutional requirement has an explicit disposition. Free-text notes do not support audit-ready release evidence.

**Improvement:** Generate a compliance matrix from the funding opportunity, proposal type, participating units, and compliance profile. Include checks for page limits, formatting, mandatory attachments, human subjects language, animal use language, data sharing statements, and collaborator certifications.

**Acceptance evidence:** Matrix generation tests, exported matrix evidence for a routed proposal, UI badges for satisfied versus unresolved checks, and package-level release evidence showing who cleared each compliance item and when.

### 7. Budget template versioning by sponsor mechanism

**Justification:** Budgeting rules differ across sponsor types, award mechanisms, and institutional policy periods. A single static budget template will produce recurring errors.

**Improvement:** Version `sponsor_budget` templates by sponsor, mechanism, budget period structure, currency, and institutional policy era. Preserve effective dates so previously submitted and awarded budgets remain reproducible.

**Acceptance evidence:** Template version registry tests, historical proposal replay showing unchanged totals under the original rule set, UI evidence for template selection at proposal creation, and release evidence that records which template version drove a submitted budget.

### 8. Budget line-item allowability and justification rules

**Justification:** Research grants budgets fail when the system cannot distinguish allowable, conditionally allowable, and prohibited costs. Manual review alone does not scale across volume and sponsor variety.

**Improvement:** Add line-item rules for personnel, fringe, travel, equipment, supplies, participant support, subawards, tuition, publication costs, patient care, and other direct costs. Require an explanation trail when a line is flagged as sponsor-restricted, institutionally sensitive, or requires prior approval.

**Acceptance evidence:** Budget validation fixtures by cost category, rule explanations visible in the UI, blocking behavior for prohibited costs, and release evidence showing which budget lines were auto-cleared versus manually justified.

### 9. Cost share and matching commitment controls

**Justification:** Cost share obligations create long-tail reporting and audit exposure. They must be explicit at proposal stage and carried forward into award execution.

**Improvement:** Add structured cost-share commitments with source account, responsible unit, approval chain, timing expectations, and whether the commitment is mandatory, voluntary committed, or prohibited. Propagate accepted commitments from proposal to award without rekeying.

**Acceptance evidence:** Proposal-to-award carryforward tests, approvals captured from the responsible unit, blocked routing when mandatory cost share lacks backing, and evidence exports that reconcile committed versus delivered match amounts.

### 10. Indirect cost and waiver governance

**Justification:** Facilities and administrative rates drive both pricing and internal policy risk. The PBC needs explicit handling for negotiated rates, de minimis cases, and waiver approvals.

**Improvement:** Add an indirect cost engine that calculates rate base, exclusions, period splits, off-campus treatment, training grant treatment, and approved waivers. Require a waiver record with approver, reason code, effective period, and sponsor citation when a non-standard rate is used.

**Acceptance evidence:** Rate calculation tests across common bases, waiver approval fixtures, UI evidence for rate-base explanation, and release evidence showing how the final indirect cost result was derived for each budget period.

### 11. IRB and ethics boundary classifier

**Justification:** The PBC should govern award readiness without pretending to own protocol review systems. A clear IRB and ethics boundary keeps responsibility precise and prevents false compliance signals.

**Improvement:** Add classification logic in `compliance_requirement` that marks whether a proposal or award implicates IRB, exempt determination, ethics committee review, or no ethics review. Store the dependency, due date, and gating effect without storing full protocol adjudication data owned elsewhere.

**Acceptance evidence:** Boundary tests showing the PBC tracks status dependencies rather than external committee decisions, workbench evidence separating "ethics dependency pending" from "award setup allowed," and release evidence documenting the boundary contract.

### 12. Protocol and approval status boundary integration

**Justification:** Operators still need current protocol status even when the approval system lives outside this PBC. Manual status re-entry creates stale readiness decisions.

**Improvement:** Consume external approval status updates into `compliance_requirement` as read-only boundary facts with source system, status timestamp, expiration date, and exception notes. Make downstream actions depend on these facts rather than ad hoc user statements.

**Acceptance evidence:** Inbound event or API-sync fixtures, stale-status warnings when a source has not refreshed, blocked award setup tests when required approvals are expired, and audit evidence showing the last synchronized status source.

### 13. Conflict of interest and key person disclosure gating

**Justification:** Proposal and award execution both depend on current disclosure status for named investigators. The PBC needs a direct domain link between personnel assignments and disclosure readiness.

**Improvement:** Add key person roster support that checks disclosure completion, training status, and sponsor-specific key person requirements before proposal submission and award activation. Keep the roster versioned so changes after submission remain auditable.

**Acceptance evidence:** Roster change history, blocked-routing tests for expired disclosure, UI warnings on incomplete key person packets, and release evidence showing who was named at submission, award setup, and amendment time.

### 14. Export control and restricted research screening

**Justification:** Research awards can create export control, sanctions, or publication restriction issues that should be surfaced before acceptance. These controls belong inside domain intake, not as post hoc email threads.

**Improvement:** Add restricted research screening for sponsor clauses, foreign participation, controlled technology, publication restrictions, and shipping obligations. Route flagged records to specialized review while preserving the original sponsor language that triggered the flag.

**Acceptance evidence:** Screening fixtures with clause-based flags, routed exception queues, detail-page evidence of the exact triggering language, and release evidence showing resolution before award activation when a restriction applies.

### 15. Sponsor-specific compliance schedule generation

**Justification:** Compliance is not a static checklist. Many awards generate recurring obligations tied to dates, milestones, carryforward thresholds, or participant enrollment.

**Improvement:** Generate recurring and one-time `compliance_requirement` records from sponsor terms, award type, protocol dependencies, and institutional policy. Include due date calculation rules, escalation windows, and owner assignment.

**Acceptance evidence:** Schedule generation tests for annual, quarterly, milestone-driven, and one-time obligations, workbench views that show upcoming deadlines, and release evidence that a newly accepted award creates the expected compliance calendar automatically.

### 16. Award notice extraction and negotiation redlines

**Justification:** Award negotiation depends on the exact terms in the sponsor notice or agreement. The PBC needs to retain both the extracted facts and the unresolved redlines.

**Improvement:** Extend `research_award` intake to capture award amount, project period, obligated amount, options, reporting schedule, publication constraints, data rights, indemnification concerns, governing law concerns, and unresolved negotiation issues. Link extracted terms directly to uploaded notice pages or clauses.

**Acceptance evidence:** Structured extraction fixtures from multiple notice formats, unresolved-redline queues, UI evidence that links terms back to source snippets, and release evidence showing final accepted terms versus initial notice language.

### 17. Award setup readiness checklist

**Justification:** Award acceptance is not the same as operational readiness. Spending, effort, subawards, compliance, and sponsor contacts must be complete before the award should go live.

**Improvement:** Add a readiness checklist to `research_award` covering account setup, budget activation, compliance dependencies, effort allocations, subaward readiness, deliverable schedule, contact roles, and amendment inheritance. Prevent transition to active execution until gating items are complete or explicitly excepted.

**Acceptance evidence:** Checklist completion tests, blocked activation fixtures, workbench readiness score display, and release evidence showing who cleared each readiness gate before the award moved to active.

### 18. Amendment and modification version chain

**Justification:** Awards evolve through supplements, carryforwards, rebudgets, extensions, and term changes. A single mutable award record hides what changed and why.

**Improvement:** Add a versioned amendment model linked to `research_award` that records type, sponsor document, effective date, changed terms, financial impact, compliance impact, and downstream tasks. Preserve a full amendment chain instead of overwriting the award baseline.

**Acceptance evidence:** Amendment sequence tests, UI timeline evidence for superseded versus active terms, replayable event history for amended awards, and release evidence proving the current award state can be reconstructed from the chain.

### 19. Pre-award spending and at-risk cost controls

**Justification:** Institutions often allow spending before the final award arrives, but those transactions carry real financial exposure. The PBC should treat them as governed exceptions, not informal notes.

**Improvement:** Add pre-award spending requests with justification, anticipated sponsor terms, allowable cost window, responsible approvers, and conversion logic if the final award differs from the expectation. Tie approved requests to subsequent award setup and close them automatically when the final award is recorded.

**Acceptance evidence:** Exception approval fixtures, blocked spending tests for expired windows, conversion tests when the award arrives, and release evidence that every pre-award exception resolves to either an award, reversal, or documented loss decision.

### 20. Rebudgeting and prior approval detector

**Justification:** Budget drift is common during execution, and sponsors differ on when rebudgeting is allowed without prior approval. The PBC needs proactive detection before noncompliant spending occurs.

**Improvement:** Compare actual and planned budget movement against sponsor and institutional thresholds for category transfers, scope changes, participant support movement, and salary cap effects. Route detected prior-approval cases into an amendment workflow instead of letting them remain informal.

**Acceptance evidence:** Threshold rule tests, blocked rebudget scenarios, operator-facing explanation of the triggering threshold, and release evidence that prior-approval-required changes cannot be finalized without the related amendment record.

### 21. No-cost extension workflow

**Justification:** No-cost extensions are one of the most common award changes and often require sponsor narrative, unobligated balance analysis, and compliance checks. They deserve a dedicated path rather than a generic amendment note.

**Improvement:** Add a workflow that gathers unobligated balance, scientific justification, revised end date, remaining deliverables, sponsor notice timing, and updated compliance dependencies. Carry approved extensions into reporting schedules, effort windows, and closeout logic.

**Acceptance evidence:** End-date extension tests, sponsor notice packet generation, updated schedule projections, and release evidence that deliverable due dates and closeout windows reflow correctly after an extension.

### 22. Subaward entity profile and risk tiering

**Justification:** `subaward` handling is incomplete without persistent subrecipient profile data. Institutions need risk-based monitoring informed by organization history and documentation quality.

**Improvement:** Add an owned subrecipient profile with legal name history, identifier set, contact roles, audit status, monitoring tier, foreign status, indemnification concerns, and document expiration dates. Use the profile to set initial review depth and monitoring cadence.

**Acceptance evidence:** Profile lifecycle tests, risk-tier assignment fixtures, workbench views showing subrecipient status, and release evidence demonstrating that a high-risk profile produces additional review tasks before subaward issuance.

### 23. Subaward scope, budget, and reconciliation controls

**Justification:** A subaward is not complete if the scope of work, budget, and prime award terms are misaligned. Mismatch at issuance creates downstream invoice and deliverable disputes.

**Improvement:** Add reconciliation checks that compare subaward scope dates, budget categories, indirect cost treatment, reporting dates, and compliance terms against the prime `research_award`. Block issuance when a prime-to-sub mismatch remains unresolved.

**Acceptance evidence:** Prime-to-sub comparison tests, blocked issuance scenarios, UI evidence of specific mismatches, and release evidence proving the executed subaward package matches the active award and amendment chain.

### 24. Subrecipient monitoring cadence and evidence

**Justification:** Monitoring obligations continue after issuance. The PBC needs to track invoice review, technical progress, audit follow-up, and corrective actions over the subaward lifetime.

**Improvement:** Generate monitoring tasks from subrecipient risk tier, invoice pattern, audit results, and sponsor terms. Store monitoring outcomes, overdue actions, and escalations as part of the `subaward` record family.

**Acceptance evidence:** Monitoring schedule tests, overdue escalation events, workbench queues for monitoring tasks, and release evidence that a high-risk subrecipient produces more frequent review checkpoints than a low-risk one.

### 25. Deliverable dependency graph

**Justification:** `milestone_report` should represent more than isolated due dates. Deliverables often depend on protocol approval, recruitment, subcontract milestones, or earlier sponsor submissions.

**Improvement:** Add a dependency graph for technical, financial, and administrative deliverables with predecessor tasks, gating conditions, contingency paths, and owner roles. Surface blocked-versus-ready deliverables in the workbench and detail pages.

**Acceptance evidence:** Dependency graph fixtures, blocked deliverable tests, UI evidence for critical path display, and release evidence showing late upstream tasks automatically reforecast downstream sponsor obligations.

### 26. Technical progress reporting pack

**Justification:** Sponsor progress reports often require a repeatable package of accomplishments, deviations, publications, personnel updates, and future work. Operators need a structured assembly path rather than ad hoc document collection.

**Improvement:** Extend `milestone_report` to assemble technical report packets from award metadata, proposal commitments, deliverable status, publications, participant enrollment, and amendment context. Support draft, review, sponsor-submitted, and sponsor-accepted states.

**Acceptance evidence:** Technical packet generation tests, state transition evidence for draft to submitted, UI evidence of unresolved content gaps, and release evidence including a complete technical report scenario with source traceability.

### 27. Financial sponsor reporting pack

**Justification:** Sponsor financial reporting depends on the same award facts as spending controls, but it has its own timing, format, and reconciliation requirements. It should not be implicit in generic accounting exports.

**Improvement:** Add reporting views that calculate reportable expenditures, commitments, cost share, program income, and unobligated balance by sponsor reporting period. Preserve sponsor-specific reporting basis and line mapping as governed configuration.

**Acceptance evidence:** Period-close report fixtures, reconciliation tests against award and budget totals, UI evidence showing basis and mapping used, and release evidence that a report package can be reproduced after an amendment or late adjustment.

### 28. Effort reporting boundary and certification windows

**Justification:** `effort_certification` belongs in this PBC only to the extent that award commitments, distribution readiness, and certification status affect research award governance. Payroll ownership and payroll edits stay outside the boundary.

**Improvement:** Add effort commitment snapshots, certification periods, named certifiers, exception flags, and certification status tracking tied to active awards and key personnel. Make the boundary explicit: this PBC records award-side obligations and certification results, not payroll source transactions.

**Acceptance evidence:** Boundary documentation in release evidence, certification period tests, workbench warnings for overdue certification, and fixtures proving award activation and closeout logic respond to certification status without mutating external payroll records.

### 29. Payroll-to-award reconciliation exceptions

**Justification:** Even with a clean effort boundary, the PBC still needs to detect when labor charged or distributed against an award conflicts with commitments. Otherwise effort risk stays hidden until audit or certification failure.

**Improvement:** Add exception records that compare inbound labor summaries to planned effort, salary cap rules, and certification windows. Route discrepancies into investigator and administrator queues with required resolution reason codes.

**Acceptance evidence:** Reconciliation exception fixtures, queue views with aging, tests for salary-cap and over-commitment cases, and release evidence showing how an exception is opened, resolved, and reflected in award risk indicators.

### 30. Cost transfer review and late-justification controls

**Justification:** Cost transfers are high-scrutiny events in sponsored research. The PBC should require the documentation trail that explains why the cost was moved and why it was not charged correctly the first time.

**Improvement:** Add a cost transfer object linked to `research_award` and `sponsor_budget` that records transfer date, original charge context, corrected destination, justification narrative, lateness reason, and approvals. Apply stricter routing when the transfer exceeds institutional timeliness thresholds.

**Acceptance evidence:** Late-transfer rule tests, approval chain fixtures, workbench evidence of pending and approved transfers, and release evidence showing that every late transfer carries justification and approver traceability.

### 31. Participant support and stipend restrictions

**Justification:** Participant support, stipends, and trainee-related costs often carry sponsor restrictions that differ from ordinary travel or supplies. These distinctions must be enforced at budget and execution time.

**Improvement:** Add budget and amendment rules that preserve restricted categories, prevent unauthorized rebudgeting, and tag awards that require participant support monitoring. Surface these restrictions in proposal review, budget change requests, and sponsor reporting.

**Acceptance evidence:** Restricted-category fixtures, blocked rebudget tests, UI evidence for sponsor-restricted categories, and release evidence demonstrating that participant support balances remain separately traceable from proposal through closeout.

### 32. Equipment, capital, and fabrication approval boundary

**Justification:** Capital-like purchases often trigger sponsor prior approval, institutional tagging, or fabrication tracking requirements. The PBC should know the grant-facing obligations even if procurement systems own the downstream purchase record.

**Improvement:** Add a compliance and budget rule set for equipment, capitalized items, and fabrication plans that records required sponsor approval, justification, location, and award linkage. Keep the boundary explicit by storing approval obligations and outcomes, not the full procurement transaction lifecycle.

**Acceptance evidence:** Approval requirement fixtures, blocked budget and rebudget scenarios, UI evidence separating grant approval from downstream purchasing, and release evidence documenting the boundary and the linked approval record.

### 33. Human subjects adverse event and protocol deviation linkage

**Justification:** Human subjects awards can encounter deviations or adverse events that materially affect deliverables, reporting, or continued funding. The award system must react without pretending to adjudicate the event itself.

**Improvement:** Add read-only compliance flags and escalation tasks for protocol deviations, suspensions, or adverse event impacts that affect award execution or sponsor reporting. Link the flag to the relevant award, deliverable, or milestone without storing sensitive case detail beyond what the award office needs.

**Acceptance evidence:** Escalation fixtures, blocked deliverable or continuation scenarios, UI evidence of impacted awards, and release evidence showing how a compliance event changed reporting obligations and internal review queues.

### 34. Data use, biosafety, and controlled data obligations

**Justification:** Many research awards carry obligations beyond IRB, including data use terms, biosafety review, controlled data access, and repository submission rules. These need structured representation in `compliance_requirement`.

**Improvement:** Add obligation templates for biosafety approvals, data use agreement dependencies, controlled data handling, repository deposits, and training prerequisites. Track due dates, responsible roles, and whether the obligation gates spending, data access, publication, or closeout.

**Acceptance evidence:** Obligation generation fixtures, UI evidence for obligation type and gating effect, tests showing different gating behavior by obligation, and release evidence that an award’s compliance schedule reflects all active obligations.

### 35. Milestone and amendment timeline UI

**Justification:** Award operators need a single visual timeline to understand proposal submission, award acceptance, amendments, deliverables, compliance deadlines, and closeout. The current declared UI fragments do not yet show that domain storyline.

**Improvement:** Add a timeline view in `ResearchGrantsManagementDetail` that layers proposal events, award versions, amendment effective dates, deliverables, subaward milestones, and compliance due dates. Support zooming from portfolio view to individual record chronology.

**Acceptance evidence:** UI screenshots or snapshots for portfolio and record timelines, event ordering tests, timeline drill-through behavior, and release evidence showing the same amended award before and after a no-cost extension.

### 36. PI, departmental administrator, and central office workbench views

**Justification:** Principal investigators, departmental administrators, and central research offices do not work the same queue. A single undifferentiated workbench hides the actions each role must take.

**Improvement:** Add role-specific queue presets and page layouts in `ResearchGrantsManagementWorkbench` for investigators, department research administrators, and central sponsored programs staff. Each view should prioritize the records, warnings, and actions that matter to that role.

**Acceptance evidence:** Permission-aware UI snapshots, queue composition tests by role, route-level access checks using the declared permissions, and release evidence showing the same record as seen by each role with different actions exposed.

### 37. Calendar, alert, and aging UI

**Justification:** Grants operations lives on dates. Operators need deadline awareness without leaving the PBC for spreadsheets or inbox searches.

**Improvement:** Add calendar, alert, and aging panels that surface proposal deadlines, deliverable due dates, compliance expirations, subaward monitoring tasks, certification windows, and closeout milestones. Support saved filters for sponsor, unit, investigator, and risk tier.

**Acceptance evidence:** UI evidence for calendar and aging panels, alert generation tests, saved-filter behavior, and release evidence showing a portfolio with upcoming deadlines, overdue tasks, and role-specific alerts.

### 38. Assistant skill for funding opportunity triage

**Justification:** The declared assistant panel is most useful when it performs bounded domain work. Opportunity triage is a high-value, low-autonomy task that fits governed assistance well.

**Improvement:** Add an assistant skill that summarizes a funding announcement, extracts eligibility and deadline facts, highlights unusual terms, and proposes an opportunity record draft for human review. Keep the final registration step explicitly user-approved.

**Acceptance evidence:** Prompt-contract fixtures, draft-versus-approved state evidence, UI evidence in `ResearchGrantsManagementAssistantPanel`, and release evidence showing assistant output side by side with the accepted opportunity record.

### 39. Assistant skill for proposal compliance review

**Justification:** Compliance review often requires comparing many attachments and sponsor rules quickly. A guided assistant can accelerate review if every suggestion is traceable.

**Improvement:** Add an assistant skill that inspects proposal sections and attachments, maps them to the proposal compliance matrix, and proposes missing-item findings with clause references. Require users to accept, reject, or edit each finding before it changes official status.

**Acceptance evidence:** Clause-linked assistant review fixtures, human disposition audit trail, UI evidence for accepted and rejected findings, and release evidence that shows assistant suggestions did not become official without user action.

### 40. Assistant skill for budget drafting and rebudget simulation

**Justification:** Budget assembly and rebudget planning benefit from guided calculations and scenario comparison. This is useful only if the assistant is constrained by sponsor and institutional rules already held in the PBC.

**Improvement:** Add an assistant skill that drafts budget periods, estimates fringe and indirect cost, explains flagged categories, and simulates rebudget options against prior-approval rules. Keep all results as drafts until a user commits them to `sponsor_budget`.

**Acceptance evidence:** Draft budget generation fixtures, scenario comparison outputs, UI evidence showing draft status and rule explanations, and release evidence that accepted budget drafts preserve the assistant’s underlying assumptions.

### 41. Assistant skill for award and amendment summarization

**Justification:** Award notices and amendments are dense, and central offices need quick summaries before they route work. Summaries must preserve links back to the authoritative source.

**Improvement:** Add an assistant skill that produces structured summaries of award notices and amendments, including money, period, reporting obligations, subaward implications, and risky clauses. Anchor every extracted fact to a source snippet or uploaded page reference.

**Acceptance evidence:** Summarization fixtures across notice formats, UI evidence for snippet-linked facts, accepted-summary audit trails, and release evidence proving that a summary can be regenerated from the same source document and version.

### 42. Event taxonomy for the grant lifecycle

**Justification:** The current emitted event set is too coarse for proposal, award, amendment, reporting, compliance, and closeout orchestration. Consumers need domain-specific events to build reliable downstream reactions.

**Improvement:** Expand the event catalog with lifecycle events such as opportunity registered, proposal routed, budget validated, compliance obligation created, award activated, amendment recorded, subaward issued, milestone submitted, effort certification overdue, sponsor report filed, and closeout completed. Keep event names stable and explicitly versioned.

**Acceptance evidence:** Event catalog documentation, payload contract tests, outbox entries for representative scenarios, and release evidence demonstrating an end-to-end lifecycle with the expected event sequence and version markers.

### 43. Outbox idempotency and replay evidence for domain events

**Justification:** Richer events only help if they remain safe under retries, duplicate delivery, and projection rebuilds. Research operations cannot tolerate double-issued tasks or phantom sponsor filings.

**Improvement:** Tighten idempotency around proposal, award, subaward, report, and closeout events using deterministic keys, replay-safe handlers, and projection rebuild procedures. Capture replay evidence as a standard part of release validation.

**Acceptance evidence:** Duplicate delivery tests, projection rebuild fixtures, replay logs tied to `AuditEventSealed`, and release evidence showing that repeated event delivery does not create duplicate domain actions.

### 44. Risk scoring with explainable domain drivers

**Justification:** The manifest already declares risk analytics and predictive capabilities, but risk scores are only useful if operators can see the grant-specific reasons behind them. Black-box warnings do not support accountable intervention.

**Improvement:** Add explainable drivers for proposal risk, award execution risk, subaward risk, reporting risk, and closeout risk using overdue obligations, amendment churn, budget volatility, subrecipient issues, unresolved compliance flags, and certification lateness. Show driver history so operators can see why risk changed over time.

**Acceptance evidence:** Risk calculation fixtures, driver explanation UI evidence, trend history tests, and release evidence with one scenario per risk category showing the score and its contributing factors.

### 45. Sponsor communication and correspondence ledger

**Justification:** Many critical grant decisions are made through sponsor correspondence, not just formal notices. The PBC needs a governed record of those communications when they affect proposal, award, or reporting decisions.

**Improvement:** Add a correspondence ledger linked to opportunity, proposal, award, amendment, subaward, and report records. Capture date, sender role, recipient role, topic, commitment made, attached files, and whether the message changed deadlines, budget treatment, or reporting obligations.

**Acceptance evidence:** Correspondence record fixtures, UI evidence showing communication history in context, tests that a correspondence-triggered deadline change updates the related task schedule, and release evidence for an award whose amendment path depended on sponsor email guidance.

### 46. Closeout readiness score

**Justification:** Closeout fails when unresolved deliverables, subawards, financial reports, invention statements, or effort certifications are discovered too late. Operators need an explicit readiness measure well before the end date.

**Improvement:** Add a closeout readiness score that considers final deliverable status, subaward final invoice status, final technical report status, financial reconciliation, invention or patent obligations, certification completion, and record retention flags. Surface the score beginning well before the project end date.

**Acceptance evidence:** Score calculation tests, workbench closeout queue snapshots, scenario fixtures showing readiness improving as tasks close, and release evidence with a near-expiration award that moves from not ready to ready.

### 47. Final technical, financial, and invention closeout pack

**Justification:** Closeout requires a coordinated packet, not isolated final actions. The PBC should assemble the evidence package that proves the award is ready to close.

**Improvement:** Add a closeout pack that gathers final technical report, final financial report, subaward confirmations, equipment disposition notes, invention or patent reporting status, and sponsor correspondence affecting final deliverables. Track each item as draft, under review, submitted, accepted, or waived.

**Acceptance evidence:** Closeout pack assembly tests, UI evidence of item status, sponsor-submitted versus sponsor-accepted state transitions, and release evidence containing a complete closeout scenario with every required artifact linked.

### 48. Retention, audit package, and record freeze

**Justification:** Closed awards still face audits, records requests, and sponsor inquiries. The PBC needs a defensible package and a freeze model that prevents quiet post-closeout mutation.

**Improvement:** Add post-closeout record retention rules, a generated audit package manifest, and a freeze state that permits only controlled corrective amendments with explicit audit trace. Include all core artifacts: proposal, award, amendments, reports, subaward evidence, compliance history, and correspondence ledger entries.

**Acceptance evidence:** Freeze-state mutation tests, audit package manifest exports, corrective-amendment fixtures, and release evidence showing that a closed award can be exported and verified without reopening unrestricted editing.

### 49. Release evidence scenarios and domain fixtures

**Justification:** The manifest already declares `RELEASE_EVIDENCE.md`, but the domain needs evidence that reflects real grant lifecycles rather than generic CRUD checks. Release proof must show the PBC understands research administration.

**Improvement:** Define release evidence scenarios covering opportunity intake, limited submission, proposal routing, budget validation, ethics dependency gating, award setup, amendment handling, subaward issuance, sponsor reporting, effort boundary behavior, and closeout. Back each scenario with stable fixtures and expected events.

**Acceptance evidence:** A scenario index in `RELEASE_EVIDENCE.md`, reproducible fixtures, event-sequence assertions, UI snapshots for critical points, and a release checklist proving every declared scenario passed on the target version.

### 50. Go-live acceptance gates and operating runbooks

**Justification:** A domain-deep backlog still needs a hard operational finish line. The PBC should not ship to active grant administration without explicit proof that proposal, award, reporting, and closeout flows are supportable.

**Improvement:** Add go-live gates for permissions, data migration quality, event replay safety, assistant guardrails, reporting accuracy, closeout readiness behavior, and operator training. Pair the gates with runbooks for deadline misses, sponsor amendment surges, subrecipient monitoring escalation, and release rollback.

**Acceptance evidence:** Go-live checklist results, operator runbook documents, rehearsal evidence for high-risk scenarios, and a signed release evidence section showing the package can support production use for the declared `research_grants_management` scope.
