# Public Sector Case Management Improvement Backlog

## Current Domain Evidence Used

- PBC key from the manifest: `public_sector_case_management`.
- Manifest description: citizen cases, eligibility, benefits, inspections, notices, appeals, service levels, and public outcomes.
- Existing APIs: `POST /citizen-cases`, `POST /eligibility-determinations`, `POST /benefit-decisions`, `POST /inspections`, `POST /notices`, `GET /public-sector-case-management-workbench`.
- Existing workflows: `public_sector_case_management_create_citizen_case_workflow`, `public_sector_case_management_record_eligibility_determination_workflow`.
- Existing tables: `citizen_case`, `eligibility_determination`, `benefit_decision`, `inspection`, `notice`, `appeal`, `service_outcome`, `public_sector_case_management_policy_rule`, `public_sector_case_management_runtime_parameter`, `public_sector_case_management_schema_extension`, `public_sector_case_management_control_assertion`, `public_sector_case_management_governed_model`.
- Existing emitted events: `PublicSectorCaseManagementCreated`, `PublicSectorCaseManagementUpdated`, `PublicSectorCaseManagementApproved`, `PublicSectorCaseManagementExceptionOpened`.
- Existing consumed events: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`.
- Existing UI fragments: `PublicSectorCaseManagementWorkbench`, `PublicSectorCaseManagementDetail`, `PublicSectorCaseManagementAssistantPanel`.
- Existing release artifacts referenced by the manifest: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`.

### 1. Multi-channel intake envelope

**Justification:** Public-sector case work starts before a case exists, and intake often arrives through web forms, walk-in clerks, call-center notes, partner uploads, and scanned paper packets that currently risk becoming inconsistent records.

**Improvement:** Add a canonical intake envelope for every inbound request with source channel, intake worker, submission timestamp, language, program requested, urgency marker, and contactability status before a `citizen_case` is created.

**Acceptance evidence:** Intake fixtures cover portal, call-center, clerk, batch import, and scanned packet paths; the workbench shows the same intake envelope across all entry channels; rejected submissions carry explicit rejection reasons instead of disappearing from queues.

### 2. Applicant, household, and authorized representative model

**Justification:** Eligibility and service decisions commonly depend on household composition and representation authority, not just one named applicant, and weak modeling here creates appealable errors.

**Improvement:** Expand intake and case detail flows to track applicant, household members, caregivers, guardians, interpreters, and authorized representatives with role effective dates and verification status.

**Acceptance evidence:** A case can show multiple parties with independent permissions and dates; household changes trigger recalculation prompts; representative changes are visible in case history and notice generation tests.

### 3. Residency and jurisdiction determination

**Justification:** Residency, service district, and office jurisdiction often decide which rules, calendars, and appeal venues apply, so address data cannot remain a loose text field.

**Improvement:** Normalize residential, mailing, temporary shelter, and confidential addresses; derive jurisdiction, service office, hearing venue, and local program overlays from governed reference data.

**Acceptance evidence:** Address normalization tests show deterministic jurisdiction assignment; confidential address handling suppresses unsafe display locations; routing to office queues changes when jurisdiction changes.

### 4. Front-door program screening

**Justification:** Citizens usually ask for help, not for a specific internal program code, so the system needs guided screening across benefits and services before a worker starts formal eligibility.

**Improvement:** Add a screening layer that can suggest likely programs, missing prerequisites, cross-program incompatibilities, and referral-only services before an `eligibility_determination` is opened.

**Acceptance evidence:** Screening results list candidate programs with reasons and confidence bands; incompatible combinations are flagged before submission; screening can be rerun after new facts are added.

### 5. Eligibility period and retroactivity rules

**Justification:** Public programs frequently hinge on application date, incident date, verification receipt date, and retroactive coverage windows, so date logic must be explicit and auditable.

**Improvement:** Add rule support for effective start date, retroactive start, end date, recertification date, and adverse-action lead time on `eligibility_determination` records.

**Acceptance evidence:** Date-rule fixtures cover timely applications, late verification, retroactive grants, and closed periods; notices display the same date basis used by the decision engine; appeal records preserve the date rules that were applied.

### 6. Missing-information and verification checklist engine

**Justification:** Case delays often come from unstructured follow-up work for missing proofs, and without a checklist engine SLA management and correspondence quality both degrade.

**Improvement:** Generate program-specific verification checklists tied to policy rules, with item status, due date, waiver reason, substituted proof, and worker notes stored against the case.

**Acceptance evidence:** Each checklist item can be satisfied, waived, substituted, or expired; due dates drive reminder notices; checklist completion gates approval paths in workflow tests.

### 7. Evidence-aware document intake

**Justification:** Scanned IDs, pay stubs, rent ledgers, medical forms, and hearing exhibits should enter the domain as evidence objects, not as loose attachments.

**Improvement:** Convert uploaded or scanned documents into typed evidence entries with document class, asserted facts, confidence score, extraction status, page count, and linkage to the exact decision question they support.

**Acceptance evidence:** A worker can see which evidence supports income, identity, disability, residency, or service need; low-confidence extraction routes to manual review; evidence entries remain linked after appeal creation.

### 8. Evidence sufficiency evaluation

**Justification:** Workers need to know whether evidence is merely present or actually sufficient for the specific rule under review, especially in contested or time-sensitive cases.

**Improvement:** Add an evidence sufficiency layer that scores whether the current evidence set satisfies each open rule, identifies contradictions, and proposes the smallest additional proof needed.

**Acceptance evidence:** Rule evaluations show satisfied, insufficient, conflicting, or expired evidence states; contradiction scenarios open explicit exceptions; sufficiency results are included in approval and denial review screens.

### 9. Outbound citizen correspondence orchestration

**Justification:** Public-sector case management fails operationally when notices are late, unclear, or inconsistent with the underlying decision record.

**Improvement:** Turn `notice` into a correspondence orchestration object that supports request-for-information letters, appointment notices, approval notices, denial notices, closure notices, and appeal-rights notices from the same decision facts.

**Acceptance evidence:** Notice templates render different scenarios from one governed data model; every notice stores delivery channel, generated language, and fact snapshot; denied notices include the exact rule citations used in the case.

### 10. Inbound correspondence and response matching

**Justification:** Citizens reply by mail, portal upload, email gateway, or contact-center callback, and the system must match those responses to the exact unresolved request without manual detective work.

**Improvement:** Add inbound correspondence matching with notice ID, barcode, intake envelope, household identity hints, and unresolved checklist item linkage.

**Acceptance evidence:** Returned proofs auto-link to the notice that requested them; ambiguous matches route to review queues; unmatched correspondence is visible in a supervised exception queue instead of being lost.

### 11. Referral creation to external services

**Justification:** Many cases need referrals to housing, behavioral health, workforce, child support, or partner agencies, and referral quality determines whether service plans actually complete.

**Improvement:** Model outbound referrals as first-class records with referral reason, requested service, urgency, eligibility basis, receiving organization, expected response window, and closure requirements.

**Acceptance evidence:** A case can open multiple concurrent referrals with different programs and deadlines; referral packages include only allowed evidence; the workbench distinguishes pending, accepted, declined, and completed referrals.

### 12. Referral loop closure and service outcome capture

**Justification:** A referral is incomplete until the sending agency can prove what happened, whether service was delivered, and whether the citizen needs follow-up action.

**Improvement:** Extend `service_outcome` to capture referral acceptance, first contact, no-show, completed service, partial service, ineligible-on-arrival, and provider-closed outcomes with structured reason codes.

**Acceptance evidence:** Service outcomes can be tied back to the originating referral and case goal; unresolved referrals breach SLA timers; provider closure codes surface in analytics without exposing private narrative text by default.

### 13. Benefit and service package decisioning

**Justification:** Case workers often need to decide both monetary benefits and non-monetary services, and the package must be internally consistent before approval.

**Improvement:** Add a combined package view where `benefit_decision` and `service_outcome` recommendations can be reviewed together for amount, frequency, duration, conditions, and service obligations.

**Acceptance evidence:** Review screens show conflicts between cash benefit rules and service participation requirements; package approval stores one coherent fact snapshot; partial-package approvals are explicitly constrained and tested.

### 14. Change reporting, reductions, and overpayment handling

**Justification:** Public-sector programs face frequent changes in income, household, and compliance, and reductions or overpayments are where notice and appeal defects become most expensive.

**Improvement:** Add change-report workflows that recompute ongoing eligibility, identify reductions or closures, track potential overpayments, and enforce adverse-action notice lead times before final effect.

**Acceptance evidence:** Tests cover income increase, household departure, late change reporting, and overpayment discovery; reduction actions cannot finalize before required notice windows; case history shows which reported change triggered the action.

### 15. Appeal intake validation

**Justification:** Appeals must be accepted or rejected on clear filing rules, because mishandling timeliness or standing creates due-process risk immediately.

**Improvement:** Add an appeal intake validator that checks standing, filing date, appealed action, requested remedy, language needs, and whether the appeal is a continuation-of-benefits request.

**Acceptance evidence:** Appeal submissions record timeliness calculations and filing basis; continuation-of-benefits requests open special review states; rejected appeals preserve a machine-readable rejection reason and review history.

### 16. Issue framing and appeal scope control

**Justification:** Appeal hearings go badly when the contested issue is vague, overly broad, or disconnected from the original decision facts.

**Improvement:** Require each `appeal` to define contested action, contested period, contested rule application, requested remedy, and included evidence scope before hearing preparation begins.

**Acceptance evidence:** Appeal records cannot move to hearing-ready without a scoped issue statement; remand decisions can target only the contested scope; notices and hearing packets reuse the same appeal framing fields.

### 17. Hearing scheduling and participant logistics

**Justification:** Hearings involve officer calendars, worker availability, citizen accessibility needs, interpreters, remote links, and reschedule rules, all of which are case-critical domain data.

**Improvement:** Add hearing scheduling with venue type, accessibility accommodations, interpreter booking, remote participation details, representative attendance, and reschedule reason tracking.

**Acceptance evidence:** Scheduling tests cover in-person, phone, and video hearings; interpreter and accommodation needs block final scheduling until confirmed; reschedules preserve original dates and reasons in the audit trail.

### 18. Hearing packet assembly

**Justification:** Hearing officers need a complete, ordered packet with the action under appeal, supporting evidence, notices, chronology, and rule basis, and packet gaps create remands.

**Improvement:** Build a hearing packet generator that assembles case chronology, adverse action history, evidence index, notice history, policy version, and issue statement into a reviewable bundle.

**Acceptance evidence:** Packet previews show missing components before release; packet generation timestamps and contents are immutable once served; packet exports respect privacy redaction rules by participant role.

### 19. Hearing outcomes, remands, and implementation

**Justification:** The operational burden continues after the hearing, and outcomes must translate into concrete case changes, reopened determinations, or upheld actions.

**Improvement:** Add structured hearing outcomes for affirmed, reversed, modified, remanded, withdrawn, and dismissed results with implementation deadlines and owning queue.

**Acceptance evidence:** A remand opens follow-up work with required issue scope; reversal outcomes regenerate benefits or services using the corrected basis; implementation delays show up in supervisor aging dashboards.

### 20. Evidence chain of custody

**Justification:** Evidence used for eligibility, sanctions, or hearings needs provenance strong enough for audit and appeal review, especially when documents are re-uploaded or redacted later.

**Improvement:** Track evidence receipt source, uploader, scan hash, original filename, derived pages, redaction lineage, and every access or export event for each evidence object.

**Acceptance evidence:** Chain-of-custody views show the full lifecycle of a document; redacted copies remain linked to originals without exposing sealed content; hearing packets can prove which evidence version was served.

### 21. Privacy-safe evidence sharing

**Justification:** Case workers need to share enough evidence to support a decision or referral without disclosing unrelated or legally protected information.

**Improvement:** Add role-based evidence views that can disclose full, partial, redacted, or metadata-only versions depending on whether the audience is an internal worker, provider, hearing officer, or citizen.

**Acceptance evidence:** Export tests prove that protected fields are removed by audience type; provider referral packets exclude unrelated household data; sealed documents cannot be attached to outbound correspondence without override approval.

### 22. SLA clock model for case work

**Justification:** Intake, verification, decision, correspondence, referral, and appeal stages each have different clocks, and one generic due date is not enough to manage public obligations.

**Improvement:** Define separate SLA clocks for intake registration, screening, eligibility determination, notice issuance, referral acknowledgment, appeal intake, hearing scheduling, and post-hearing implementation.

**Acceptance evidence:** Each queue shows its own age and target date; reports distinguish late intake from late notice generation; SLA definitions are parameterized by program and jurisdiction rather than hard-coded.

### 23. Pause, tolling, and resume reasons

**Justification:** Case clocks often pause for citizen response windows, court stays, disaster periods, or pending external verification, and those pauses must be transparent to supervisors and auditors.

**Improvement:** Add governed pause reasons with start and end triggers, actor, supporting evidence, and whether the pause affects only one clock or multiple clocks on the same case.

**Acceptance evidence:** Timeline views show active and paused periods distinctly; pause misuse opens control exceptions; resumed clocks continue from the correct remaining duration instead of resetting silently.

### 24. Purpose-based access and least privilege

**Justification:** Public-sector case records frequently contain health, income, domestic violence, juvenile, or other restricted data that should be visible only for a lawful case-processing purpose.

**Improvement:** Extend permissions beyond coarse CRUD so that viewing, editing, exporting, or discussing a field requires both role authorization and a declared processing purpose tied to the case action.

**Acceptance evidence:** Unauthorized access attempts are denied with auditable reasons; supervisors can review purpose declarations by worker and field; assistant actions are blocked when the active purpose does not permit the requested data use.

### 25. Confidentiality markers and protected populations

**Justification:** Survivors of violence, minors, witnesses, and other protected populations need extra handling across notices, hearing logistics, and workbench visibility.

**Improvement:** Add confidentiality markers for protected address, sealed contact method, restricted party, youth-sensitive record, and witness-protected evidence with downstream UI and export behavior attached to each marker.

**Acceptance evidence:** Confidentiality markers suppress unsafe display elements across case detail, notices, and packet exports; hearing scheduling prevents accidental disclosure of protected locations; role tests confirm correct masking behavior.

### 26. Fraud referral boundary and handoff control

**Justification:** Program integrity work must not contaminate ordinary eligibility processing with unreviewed suspicion signals, and the system needs a clear boundary between case work and fraud referral.

**Improvement:** Model fraud referral as a separate bounded handoff that can receive specific facts, reason codes, and approved evidence excerpts without exposing the ordinary case queue to investigative notes or retaliatory workflow branches.

**Acceptance evidence:** Fraud referral packages include only approved data categories; the originating case shows that a referral occurred without exposing investigative content; case workers cannot see fraud-case notes unless granted separate authority.

### 27. Program rule versioning and effective dating

**Justification:** Public programs change through legislation, emergency directives, budget updates, and local waivers, so decisions must always point to the exact rule set in force at the time.

**Improvement:** Version `public_sector_case_management_policy_rule` with effective start and end dates, emergency supersession flags, jurisdiction overlays, and migration notes for in-flight cases.

**Acceptance evidence:** A worker can inspect the precise rule version used for any eligibility or benefit decision; rule changes can be simulated against open cases before activation; out-of-date rule references fail validation in release checks.

### 28. Human-readable rule explanations

**Justification:** Citizens, workers, and hearing officers need to understand why a rule fired, not just that it fired, especially in adverse decisions.

**Improvement:** Require every program-rule evaluation to produce a plain-language explanation, the governing citation, the decisive facts, and the missing facts that would have changed the outcome.

**Acceptance evidence:** Denial and reduction notices reuse the same explanation text shown in the workbench; explanations are available by language and reading level template; appeal packets include both machine and human-readable rule traces.

### 29. Manual override governance

**Justification:** Overrides are sometimes necessary for hardship, emergency waiver, or data correction scenarios, but they become a control failure if they are informal.

**Improvement:** Add override types with required justification, approver role, expiry, downstream recalculation requirements, and whether the override affects benefits, services, SLA clocks, or correspondence.

**Acceptance evidence:** Override records show who requested, approved, and relied on the override; expired overrides re-open review tasks automatically; reports separate lawful overrides from policy violations.

### 30. Supervisor workbench queue design

**Justification:** Supervisors need to manage backlog by risk, lateness, and citizen impact, not by flat lists of open records.

**Improvement:** Redesign `PublicSectorCaseManagementWorkbench` queues around intake review, pending verification, ready to decide, pending notice, pending referral response, appeal intake, hearing prep, and post-hearing implementation.

**Acceptance evidence:** Queue counts align with underlying state projections; supervisors can filter by program, office, SLA risk, and protected-case handling restrictions; queue definitions are testable and not embedded only in UI code.

### 31. Case detail chronology and decision timeline

**Justification:** Workers and reviewers need one coherent chronology that shows facts, decisions, notices, referrals, appeals, and hearings in causal order.

**Improvement:** Expand `PublicSectorCaseManagementDetail` with a timeline that merges intake events, evidence receipt, rule evaluations, decisions, correspondence, referral milestones, appeal actions, and hearing outcomes.

**Acceptance evidence:** Timeline ordering remains correct under replay and backfill tests; each entry can drill into underlying evidence or policy context; chronology can be exported for quality review without exposing sealed data.

### 32. Correspondence drafting and review UX

**Justification:** Notice quality is often lost in the final drafting step when workers manually rewrite approved facts or paste from prior cases.

**Improvement:** Add a structured correspondence composer that locks factual inserts to governed case data while still allowing controlled narrative sections, translation selection, and supervisor preview.

**Acceptance evidence:** Workers cannot accidentally alter governed facts inside a notice; preview mode shows final citizen-facing language by delivery channel; supervisor review compares the drafted notice against the decision facts and citations.

### 33. Appeal and hearing operator UX

**Justification:** Appeals and hearings involve dense, time-sensitive navigation, and a generic case screen does not support clerk, worker, and hearing-officer needs.

**Improvement:** Add role-specific appeal and hearing views for filing intake, issue framing, packet readiness, hearing logistics, continuance tracking, and outcome implementation.

**Acceptance evidence:** Users with different roles see different default panels and actions; packet completeness indicators are visible without opening each artifact; hearing-day workflows can be executed without using raw attachments or external spreadsheets.

### 34. Agent skill for intake triage

**Justification:** The assistant panel is only useful if it performs bounded case-management work that reduces clerical load without making hidden decisions.

**Improvement:** Add an intake-triage agent skill that summarizes inbound submissions, identifies missing structured fields, proposes likely program screens, and routes the case to the right human queue without auto-approving eligibility.

**Acceptance evidence:** Agent outputs are stored as suggestions with confidence and provenance; the skill cannot commit decisions beyond its authority boundary; low-confidence triage results force human review before any downstream workflow starts.

### 35. Agent skill for correspondence drafting

**Justification:** Notice drafting is repetitive but legally sensitive, making it a good candidate for assisted drafting with strict grounding.

**Improvement:** Add a correspondence agent skill that drafts citizen-facing notices from governed case facts, active rule explanations, and approved templates while preserving citation blocks and plain-language standards.

**Acceptance evidence:** Drafted notices always cite the underlying decision and rule explanation objects; workers can compare draft language to source facts side by side; the agent refuses to invent facts or policy citations not present in the record.

### 36. Agent skill for hearing preparation

**Justification:** Hearing preparation consumes significant staff time and requires fast summarization across chronology, evidence, and contested issues.

**Improvement:** Add a hearing-prep agent skill that assembles a concise issue summary, identifies disputed facts, highlights missing packet elements, and proposes targeted follow-up questions for the assigned worker.

**Acceptance evidence:** Hearing-prep outputs link every statement to case history or evidence; missing packet warnings match the packet-completeness rules; the skill cannot finalize hearing outcomes or alter the appeal scope.

### 37. Agent skill for quality review and coaching

**Justification:** Supervisors need scalable quality review that surfaces explainable defects rather than opaque scores.

**Improvement:** Add a quality-review agent skill that checks for unsupported decisions, missing notices, privacy leaks, stale SLA clocks, weak issue framing, and inconsistent referral closure while generating review notes for supervisors.

**Acceptance evidence:** Quality-review findings can be sampled against human reviewer outcomes; each finding cites the record element that triggered it; false-positive tuning is tracked in release evidence rather than hidden in prompt changes.

### 38. Domain event taxonomy expansion

**Justification:** The current emitted events are too coarse for operational replay, integration, and audit across intake, notices, referrals, appeals, and hearings.

**Improvement:** Add domain events for intake received, screening completed, verification requested, evidence accepted, decision issued, notice delivered, referral opened, referral closed, appeal filed, hearing scheduled, hearing decided, and SLA breached.

**Acceptance evidence:** Event contracts exist for each new domain milestone; consumers can subscribe without reading internal tables; event naming and payload examples are documented in the package release evidence.

### 39. Cross-system event boundaries

**Justification:** The PBC consumes external policy and party updates, but it needs explicit boundaries for what external changes may and may not mutate inside public-sector case processing.

**Improvement:** Define inbound event handlers that can update reference data, party details, or provider qualification status while preventing external systems from silently closing cases, rewriting hearing outcomes, or changing protected evidence.

**Acceptance evidence:** Contract tests show what each consumed event may mutate; prohibited external mutations generate exceptions instead of side effects; lineage views trace every derived case change back to the source event.

### 40. Replay, idempotency, and dead-letter operations

**Justification:** Public agencies need confidence that retried events and batch corrections will not duplicate benefits, notices, or hearing actions.

**Improvement:** Strengthen event processing with domain-level idempotency keys, replay guards for irreversible actions, and dead-letter tooling that explains the case impact of a failed event before retry.

**Acceptance evidence:** Duplicate-event tests prove no duplicate notices or benefit actions occur; dead-letter entries show affected case IDs and blocked milestones; replay tools require role-based approval for irreversible branches.

### 41. Operational analytics for backlog and citizen impact

**Justification:** Leadership needs to see more than throughput; they need aging, timeliness, reversal rates, referral completion, and service outcomes by office and program.

**Improvement:** Build operational analytics that combine queue aging, notice timeliness, appeal rates, hearing reversals, referral completion, and citizen-impact indicators into one governed metric model.

**Acceptance evidence:** Metrics are defined with business meaning and source projections; dashboards can drill from aggregate trend to affected cases; metric calculations are covered by regression fixtures.

### 42. Quality sampling and corrective action tracking

**Justification:** Public-sector quality management requires repeatable sampling, defect classification, coaching, and proof that corrective actions close the same defect class over time.

**Improvement:** Add a quality module that samples cases by risk and program, records defect taxonomy, assigns corrective actions, and measures repeat-defect rates after remediation.

**Acceptance evidence:** Sample plans can target high-risk cases or random cohorts; defect findings connect to policy, workflow, or training causes; repeated defects are visible in supervisor and release evidence views.

### 43. Retention, legal hold, and expungement rules

**Justification:** Case files, hearing materials, and referral records follow different retention schedules, and some records must be held or expunged under law.

**Improvement:** Apply retention schedules by record type and program, support legal holds at case or evidence level, and add expungement workflows that preserve required audit stubs without retaining sealed content.

**Acceptance evidence:** Retention timers can be shown per case artifact; legal holds block deletion and export changes; expungement tests confirm content removal while preserving the required audit trace.

### 44. Release evidence pack for policy and workflow changes

**Justification:** Every rule, template, queue, or agent change can affect eligibility and due process, so the package needs release evidence stronger than a passing unit-test summary.

**Improvement:** Expand `RELEASE_EVIDENCE.md` expectations to require policy diff summaries, affected program inventory, notice regression samples, appeal-impact review, privacy checks, and rollback instructions for every release.

**Acceptance evidence:** Release evidence bundles contain signed policy diffs, notice previews, workflow regression results, and explicit rollback steps; no release is marked ready without completed evidence for rules, templates, and agent behaviors touched.

### 45. Seed data, fixtures, and scenario coverage

**Justification:** Rich domain fixtures are needed to keep the package from regressing back to shallow examples that ignore households, protected cases, appeals, and referrals.

**Improvement:** Expand seed data and test fixtures to cover single-adult, multi-household, emergency, protected-address, reduction, overpayment, appeal, hearing, and multi-referral scenarios.

**Acceptance evidence:** Test fixtures can instantiate realistic end-to-end journeys without manual SQL edits; seed data includes policy versions and office calendars; scenario names match real operational use cases instead of generic placeholders.

### 46. Accessibility, language access, and readability

**Justification:** A public-sector system fails its mission if citizens cannot understand notices or participate in hearings because of language or accessibility gaps.

**Improvement:** Add language preference, interpreter need, alternate-format notice delivery, readability review, and accessibility checks across intake, correspondence, workbench actions, and hearing scheduling.

**Acceptance evidence:** Notices can be rendered in alternate languages and accessible formats; hearing scheduling stores accommodation commitments; accessibility regressions are included in release evidence rather than treated as optional polish.

### 47. Security logging and consent traceability

**Justification:** Supervisors and auditors need to reconstruct who viewed, changed, exported, or discussed sensitive case information and under what authority.

**Improvement:** Add security logging that records user, role, purpose, consent basis, record scope, action type, and export destination for sensitive operations across cases, notices, referrals, and hearings.

**Acceptance evidence:** Sensitive actions appear in searchable audit views; consent-dependent actions fail when consent status is missing or expired; export logs distinguish citizen-authorized sharing from internal processing.

### 48. Duplicate case and cross-program coordination

**Justification:** Agencies routinely receive duplicate applications, separate program enrollments for one household, and cross-program actions that should inform each other without collapsing lawful boundaries.

**Improvement:** Add duplicate detection and coordination rules that can link related cases, share allowed facts across programs, and prevent double-processing while still preserving program-specific rule and appeal boundaries.

**Acceptance evidence:** Potential duplicates are surfaced before decision issue; linked cases share only approved coordination facts; closing one program does not silently close another unless an explicit rule allows it.

### 49. Continuity operations for outages and hearing-day disruption

**Justification:** Public service obligations continue through outages, courthouse closures, and disaster events, so the package needs continuity behavior for critical steps.

**Improvement:** Add continuity procedures for offline intake capture, deferred notice generation, rescheduled hearings, emergency policy overrides, and replay of queued actions after service restoration.

**Acceptance evidence:** Outage simulations show that intake can be captured and reconciled later; hearing disruptions generate citizen-safe reschedule notices; replay after restoration preserves original timestamps and actor attribution.

### 50. Go-live exit criteria and production evidence

**Justification:** A domain-deep backlog needs a concrete definition of done so releases do not ship with unproven due-process, privacy, or operational behavior.

**Improvement:** Define go-live exit criteria for `public_sector_case_management` covering end-to-end scenario pass rates, notice accuracy, SLA instrumentation, privacy controls, fraud referral boundary tests, agent guardrails, event contract validation, and release evidence completeness.

**Acceptance evidence:** The package can present a production-readiness report with scenario coverage, policy version inventory, event contract checks, privacy test results, and signed release evidence referencing the exact build and migration set that is being deployed.
