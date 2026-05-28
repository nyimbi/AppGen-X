# Permitting Licensing and Inspections Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `permitting_licensing_inspections`.
- Manifest description: applications, reviews, permits, licenses, fees, inspections, violations, renewals, and citizen workflows.
- Current owned tables: `application`, `permit`, `license`, `review_task`, `fee_assessment`, `inspection`, and `violation`.
- Current APIs: `POST /applications`, `POST /permits`, `POST /licenses`, `POST /review-tasks`, `POST /fee-assessments`, and `GET /permitting-licensing-inspections-workbench`.
- Current emitted events: `PermittingLicensingInspectionsCreated`, `PermittingLicensingInspectionsUpdated`, `PermittingLicensingInspectionsApproved`, and `PermittingLicensingInspectionsExceptionOpened`.
- Current consumed events: `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified`.
- Current UI fragments: `PermittingLicensingInspectionsWorkbench`, `PermittingLicensingInspectionsDetail`, and `PermittingLicensingInspectionsAssistantPanel`.
- Current docs: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

### 1. Application intake package completeness

**Justification:** Permit and license intake fails early when the system treats every submission as a generic record instead of a package with forms, plans, declarations, signatures, and supporting attachments. A domain backlog should start by making incomplete submittals visible before staff spend review time.

**Improvement:** Add intake package rules that classify application type, required documents, required attestations, required responsible parties, and required parcel or address data before an `application` can enter active review. Distinguish new applications, revisions, amendments, transfers, renewals, and complaint-triggered cases.

**Acceptance evidence:** Scenario fixtures show accepted and rejected intake packages by application type, the workbench exposes a submission completeness checklist, and `RELEASE_EVIDENCE.md` links each intake rule to UI screenshots, API examples, and failing-to-passing tests.

### 2. Application identity, parcel, and party normalization

**Justification:** Permitting and licensing records become unreliable when applicant names, parcel identifiers, contractor numbers, and site addresses drift across submissions. Normalization is a domain control, not a cosmetic cleanup.

**Improvement:** Normalize applicant, owner, contractor, business, parcel, and site identity fields at intake, and preserve both the submitted values and the canonicalized values on the case. Add duplicate and near-duplicate detection for the same site or party combination.

**Acceptance evidence:** Test data covers duplicate parcel submissions, changed business names, and alternate address formats; case detail UI shows canonical and source values; release evidence includes duplicate-detection outcomes and operator override traces.

### 3. Pre-application consultation tracking

**Justification:** Many jurisdictions use early consultations to steer applicants before formal submission, but the current PBC evidence does not show a first-class place for advisory conversations, preliminary flags, or concept-stage requirements. Without this, the system loses context that explains later review decisions.

**Improvement:** Introduce a pre-application record tied to `application` intake that captures advisory notes, likely review disciplines, known code or ordinance issues, expected fees, and likely public notice or hearing obligations. Promote the record into a formal application without rekeying core facts.

**Acceptance evidence:** Seed scenarios show conversion from consultation to application, the workbench timeline preserves advisory history, and release evidence includes a no-retyping conversion test with retained notes and actors.

### 4. Plan set version control

**Justification:** Plan review is impossible to audit if reviewers cannot tell which plan sheets, drawings, or narratives were in force for a given comment cycle. Version drift is a primary cause of dispute in construction permitting and technical licensing cases.

**Improvement:** Treat each plan upload as a governed plan-set version with sheet inventory, revision dates, resubmittal reason, reviewer comparison notes, and supersession links. Bind review comments and approvals to a specific plan-set version rather than a loose document collection.

**Acceptance evidence:** Case detail UI shows plan-set version history, review comments resolve against a specific version, and release evidence includes side-by-side version diffs and a superseded-plan regression test.

### 5. Multi-discipline plan review routing

**Justification:** Plan review rarely belongs to one reviewer; zoning, structural, fire, utilities, accessibility, environmental, and business-license disciplines often run in parallel or sequence. Generic task routing hides discipline-specific dependencies and approval order.

**Improvement:** Expand `review_task` into discipline-aware review routing with dependency graphs, concurrency rules, lead reviewer assignment, and discipline-specific comment templates. Support both sequential gating and parallel review packages.

**Acceptance evidence:** Tests cover sequential and parallel routing paths, the workbench shows discipline swimlanes with blockers, and release evidence includes a review matrix proving the correct order for each application type.

### 6. Correction cycle and resubmittal governance

**Justification:** The domain lives on correction loops; a case can move through multiple review rounds before approval, denial, or abandonment. The PBC needs explicit correction cycles rather than silent overwrites of comments and plans.

**Improvement:** Add correction-round records that link reviewer comments, applicant responses, revised plan sets, due dates, and staff acceptance of each resubmittal. Separate open corrections, accepted corrections, waived corrections, and unresolved corrections.

**Acceptance evidence:** Scenario tests show multi-round review with carried-forward comments, the detail UI groups comments by correction cycle, and release evidence includes overdue-correction alerts and accepted-resubmittal proofs.

### 7. Fee assessment boundary and cashiering handoff

**Justification:** Fee assessment belongs inside this PBC, but payment posting, treasury reconciliation, and ledger settlement often do not. The boundary must be explicit so the package owns fee logic without quietly absorbing cashiering responsibilities.

**Improvement:** Define `fee_assessment` as the authoritative domain for fee calculation, waivers, credits, and refund eligibility while publishing a clear outbound handoff for payment request, payment confirmation, refund execution, and accounting reconciliation. Record payment status as an external dependency instead of an owned financial ledger.

**Acceptance evidence:** Architecture and API evidence show the boundary between assessed fees and posted payments, events prove outbound handoff and inbound confirmation behavior, and release evidence includes tests that block permit issuance when payment confirmation is missing.

### 8. Fee schedules, waivers, credits, and refunds

**Justification:** Fee logic is not a single formula; it depends on use type, valuation, square footage, occupancy, urgency, renewal status, reinspection counts, public-hearing fees, and hardship waivers. A shallow fee table will not survive real permitting operations.

**Improvement:** Add rule-driven fee schedules with effective dates, jurisdiction scope, discretionary waivers, fee credits, refund eligibility, and rework charges. Track who approved a waiver, why it was allowed, and whether the waiver changes downstream review or enforcement behavior.

**Acceptance evidence:** Fee simulations cover new, revised, renewal, reinspection, and hearing scenarios; the workbench displays line-level fee explanations; and release evidence includes waiver approval trails and refund-eligibility tests.

### 9. Permit issuance readiness gate

**Justification:** Permit issuance should be a deliberate domain milestone, not the last save after a reviewer clicks approve. Issuance must prove that plan review, fee readiness, conditions, and dependency checks are complete.

**Improvement:** Add an issuance gate that requires all mandatory reviews closed, all blocking corrections resolved, all required fees confirmed, all permit conditions assembled, and all public notice or hearing outcomes recorded before a `permit` can move to issued status. Support issuance holds with explicit reasons.

**Acceptance evidence:** Issuance blockers appear in the workbench and detail UI, integration tests prove that unresolved dependencies prevent issuance, and release evidence includes a full readiness checklist trace for each permit type.

### 10. License qualification and operating conditions

**Justification:** A license is more than an approval flag; it usually carries qualifications, scope limits, operating conditions, expiration rules, and disciplinary history. The backlog should make those domain facts first-class.

**Improvement:** Extend `license` records to capture qualified activities, allowed locations, capacity or occupancy limits, staffing requirements, training or insurance proofs, and special operating conditions. Make conditions machine-readable so inspections and renewals can test them automatically.

**Acceptance evidence:** License detail UI shows structured conditions, inspection scenarios can evaluate those conditions, and release evidence includes qualification-rule tests plus condition-driven enforcement examples.

### 11. Temporary permits and provisional licenses

**Justification:** Jurisdictions often issue temporary occupancy approvals, phased permits, event permits, and provisional licenses while full review or corrective work remains open. These are high-risk instruments and need separate rules from permanent approvals.

**Improvement:** Model temporary permits and provisional licenses with explicit term limits, missing-item lists, auto-expiration behavior, and follow-up review checkpoints. Prevent silent conversion into permanent approval without satisfying remaining conditions.

**Acceptance evidence:** Seed data includes temporary and provisional cases, the system auto-flags approaching expiration, and release evidence includes tests that prevent permanent status conversion without documented completion.

### 12. Inspection type matrix and scheduling

**Justification:** Inspections are not interchangeable; rough-in, final, complaint, renewal, compliance, and follow-up inspections have different prerequisites, windows, and inspectors. A strong PBC should encode those distinctions directly.

**Improvement:** Add an inspection type matrix that defines prerequisites, allowed outcomes, required evidence, reinspection rules, and default scheduling windows for each `inspection` type. Support route-based scheduling and inspector capacity constraints.

**Acceptance evidence:** Scheduling tests cover prerequisite failures and route assignment, the workbench shows inspection queues by type and aging, and release evidence includes capacity and window calculations for multiple inspection classes.

### 13. Mobile inspection evidence capture

**Justification:** Field inspectors need to record evidence where the work occurs, not after returning to a desk. If the package does not treat photos, notes, signatures, measurements, and geotags as first-class evidence, later enforcement will be weak.

**Improvement:** Add mobile-friendly capture for inspection observations, photos, annotated plan references, signatures, geolocation, timestamped measurements, and witness notes. Preserve the chain of custody for each evidence item and link it to the exact inspection outcome.

**Acceptance evidence:** Mobile UI flows are demonstrated in release evidence, evidence objects show actor, time, and location lineage, and regression tests prove that captured media and notes remain attached after sync and correction events.

### 14. Failed inspection corrections and reinspections

**Justification:** Failed inspections drive correction work, reinspections, and fee consequences. The system should separate an initial failed inspection from the later corrective work and any subsequent reinspection decisions.

**Improvement:** When an inspection fails, automatically open a correction package with failed items, code references, due dates, reinspection eligibility, and reinspection fee triggers. Track whether the next visit is a full reinspection, a partial verification, or an administrative closure.

**Acceptance evidence:** Failed-inspection scenarios produce linked correction notices and reinspection tasks, the workbench shows open failed items by site and inspector, and release evidence includes a reinspection-fee trigger test.

### 15. Violation taxonomy and severity scoring

**Justification:** Enforcement quality depends on a consistent violation vocabulary. Without a clear taxonomy, the same behavior can be under-classified in one case and over-classified in another.

**Improvement:** Introduce a violation taxonomy for life safety, operational, documentation, occupancy, nuisance, environmental, licensing, and repeat-offender violations with severity, imminence, recurrence, and remedy type. Use the taxonomy to drive notice templates, hearing eligibility, and enforcement ladders.

**Acceptance evidence:** Violation creation tests verify taxonomy-driven defaults, analytics group cases by severity and type, and release evidence includes examples showing how taxonomy changes downstream notice and hearing behavior.

### 16. Enforcement ladder and stop-work authority

**Justification:** Enforcement is rarely a single step; it typically moves from warning to citation to suspension, stop-work, revocation, or referral. The system should encode the ladder and the authority needed for each escalation.

**Improvement:** Add an enforcement ladder with explicit escalation steps, approval authority, emergency powers, and mandatory evidence for each step. Include stop-work order issuance, service, release, and appeal handling as a controlled workflow.

**Acceptance evidence:** Enforcement scenarios prove that the right authority is required for each step, stop-work orders generate service records and release checks, and release evidence includes escalation matrices and blocked-override tests.

### 17. Notice of violation and due-process timeline

**Justification:** A violation case is defective if the package cannot prove when notice was created, served, acknowledged, cured, or escalated. Due-process dates are central domain facts.

**Improvement:** Create a notice workflow that records notice generation, delivery channel, service confirmation, cure deadline, extension decisions, and escalation dates. Automatically compute the next legally allowed step based on service status and deadlines.

**Acceptance evidence:** Timeline views show notice-to-cure-to-escalation progression, tests cover service failures and deadline extensions, and release evidence includes notice artifacts and statutory clock calculations.

### 18. Public notice publication ledger

**Justification:** Some permits, licenses, variances, and hearings require public notice, publication windows, and proof that the notice actually ran. This is often omitted until late in implementation and then handled out of band.

**Improvement:** Add a public notice ledger that stores notice text, publication channel, posting dates, mailing lists, site-posting evidence, affidavits of publication, and comment windows. Link notice obligations to application, permit, license, and hearing milestones.

**Acceptance evidence:** Cases that require notice cannot advance without publication proof, the detail UI shows notice windows and artifacts, and release evidence includes publication-ledger entries with linked affidavits and comment periods.

### 19. Hearing docket, exhibits, and outcomes

**Justification:** Hearings are a specialized domain stage with scheduling, exhibit packets, testimony, continuances, and formal outcomes. Treating them as a generic task would erase key procedural facts.

**Improvement:** Model hearings with docket numbers, hearing type, notice basis, continuance history, hearing exhibits, participant roles, board or hearing-officer outcomes, and remand or condition results. Tie hearing outcomes back into permit, license, and violation state changes.

**Acceptance evidence:** Hearing scenarios show scheduling through outcome, exhibit packets are visible in case detail, and release evidence includes a continued hearing example plus a decision-to-case-state transition test.

### 20. Renewal calendars and outreach

**Justification:** Renewals are predictable workload and should not depend on staff remembering expiration dates. Strong renewal handling reduces lapses, unlicensed activity, and urgent last-minute queues.

**Improvement:** Create renewal calendars with advance notice cadence, grace-period messaging, missing-document reminders, and role-based queues for expiring permits and licenses. Support high-volume seasonal renewal campaigns without collapsing case history into batch notes.

**Acceptance evidence:** Renewal jobs create the correct notices at the correct lead times, workbench dashboards show expiring populations by window, and release evidence includes campaign results and notice audit logs.

### 21. Renewal eligibility and continuing conditions

**Justification:** Renewal is not automatic; the case must prove that ongoing qualifications, inspections, fees, and enforcement history support renewal. Otherwise the system becomes a passive expiration tracker instead of a licensing authority.

**Improvement:** Add renewal eligibility rules that evaluate continuing education, active violations, unresolved failed inspections, unpaid assessed fees, insurance or bond status, and required attestations. Distinguish full renewal, conditional renewal, denied renewal, and renewal hold.

**Acceptance evidence:** Renewal decision tests cover eligible, conditional, denied, and held cases, case detail displays the rule outcomes that drove the decision, and release evidence includes a denied-renewal packet with rule citations.

### 22. Expiration, grace, suspension, and reinstatement

**Justification:** The period between active and revoked status often determines whether the public sees fair treatment or arbitrary administration. Expiration and reinstatement rules need their own lifecycle semantics.

**Improvement:** Expand permit and license lifecycle states to cover expired, grace, suspended, reinstatement pending, reinstated, and revoked. Track the event, reason, authority, and required conditions for each status change.

**Acceptance evidence:** State-transition tests prove illegal jumps are blocked, the workbench separates expired from suspended populations, and release evidence includes reinstatement scenarios with required-condition verification.

### 23. Citizen portal intake and self-service

**Justification:** Citizen portals are a primary domain surface for applicants, residents, and businesses. If self-service stops at basic form upload, the package still leaves high-friction work to staff.

**Improvement:** Add a citizen-facing portal for account creation, guided application intake, document upload, fee estimate preview, status inquiries, correction responses, complaint filing, and hearing participation details. Separate portal permissions for applicants, owners, contractors, and complainants.

**Acceptance evidence:** Portal flows are covered in end-to-end tests, role-restricted views show only the right cases and actions, and release evidence includes screenshots for intake, correction response, and complaint submission.

### 24. Citizen portal status, transparency, and correspondence

**Justification:** Applicants and residents need to know what is happening without calling the office for every update. Transparent case status reduces manual inquiry workload and improves trust.

**Improvement:** Publish stage-based status explanations, outstanding items, next-step guidance, upcoming deadlines, and official correspondence history in the citizen portal. Show which review disciplines are complete, which corrections remain open, and whether a hearing or public notice stage is active.

**Acceptance evidence:** Portal UI tests confirm stage explanations and correspondence history, usability scenarios show users locating outstanding items without staff help, and release evidence includes portal screenshots and localized message examples.

### 25. Internal workbench queue and dashboard design

**Justification:** `PermittingLicensingInspectionsWorkbench` should reflect how permitting offices actually work: intake, plan review, issuance, inspections, renewals, hearings, and enforcement are different operational lanes. One generic queue hides real priorities.

**Improvement:** Redesign the workbench with lane-specific queues, aging buckets, discipline filters, inspection route views, renewal campaigns, and enforcement dashboards. Add saved views for intake staff, reviewers, inspectors, supervisors, and hearing clerks.

**Acceptance evidence:** UI acceptance tests cover each saved view, performance evidence shows large queue loads remain usable, and release evidence includes role-based screenshots plus queue-count reconciliation against seeded cases.

### 26. Record detail timeline and evidence graph

**Justification:** `PermittingLicensingInspectionsDetail` should tell the procedural story of a case. Staff should not need to inspect tables or log streams to reconstruct plan revisions, notices, hearings, or enforcement actions.

**Improvement:** Build a timeline and evidence graph that shows application events, review cycles, plan-set versions, fee milestones, issuance, inspections, violations, public notices, hearings, renewals, and correspondence in one traceable view. Link every action to the actor, source event, and attached evidence.

**Acceptance evidence:** Detail-page UI tests confirm timeline ordering and evidence linking, event lineage is visible for every major milestone, and release evidence includes screenshots of a case spanning intake through enforcement closure.

### 27. Documents, stamped plans, and attachment governance

**Justification:** Permitting decisions depend on controlled documents such as stamped plans, certificates, letters, proofs of publication, and hearing exhibits. The package should govern those artifacts directly rather than treating them as loose files.

**Improvement:** Add document classes, retention tags, stamp status, supersession rules, signed-copy indicators, and document-to-case-role links. Distinguish working drafts, accepted submittals, approved stamp sets, and public-facing versions.

**Acceptance evidence:** Attachment tests prove document classes and supersession behavior, the detail UI shows which plan set is current and stamped, and release evidence includes a document-governance matrix with sample artifacts.

### 28. Cross-agency referrals and sign-offs

**Justification:** Many permits and licenses depend on outside sign-offs such as fire, health, utilities, zoning, environmental, or legal review. Those dependencies should be explicit instead of buried in comment text.

**Improvement:** Add referral objects with requested review scope, due dates, returned conditions, blocking status, and stale-dependency rules. Support both internal cross-department referrals and external agency acknowledgments.

**Acceptance evidence:** Referral scenarios show blocking and non-blocking referrals, stale referrals appear in workbench exception queues, and release evidence includes turnaround tracking and returned-condition capture.

### 29. Event catalog expansion for domain milestones

**Justification:** The current emitted events are too generic to explain real permitting behavior to downstream consumers. Domain milestones such as plan review completion, permit issuance, failed inspection, violation notice served, public notice posted, hearing decided, and renewal denied need typed events.

**Improvement:** Expand the event catalog with explicit milestone events and structured payloads for applications, plan review, fee assessment, permit and license lifecycle changes, inspections, violations, corrections, renewals, public notices, hearings, and enforcement actions. Preserve event lineage to the case, actor, and triggering rule.

**Acceptance evidence:** Event schema examples exist for each major milestone, event replay tests prove downstream projections can rebuild case history, and `RELEASE_EVIDENCE.md` maps each user-facing stage to its emitted and consumed events.

### 30. Outbound notices, letters, and templates

**Justification:** Permitting offices produce a large volume of official correspondence. If notice generation stays ad hoc, the package cannot guarantee consistent language, deadlines, or service records.

**Improvement:** Add governed templates for application deficiency letters, review comments, correction notices, permit issuance letters, renewal notices, inspection results, violation notices, hearing notices, and enforcement orders. Support jurisdiction-level wording overrides with version history.

**Acceptance evidence:** Template tests render the correct data into each letter type, service channels are logged for each notice, and release evidence includes approved samples plus versioned template history.

### 31. Corrections, amendments, and supersessions

**Justification:** Case history must distinguish a correction to an existing record from a new application or a replacement permit. Without that distinction, analytics and legal review become unreliable.

**Improvement:** Model corrections, amendments, revisions, transfers, and supersessions as explicit relationships across `application`, `permit`, and `license` records. Preserve the original issuance or filing record while making the currently effective record obvious.

**Acceptance evidence:** Relationship tests cover revised permits and amended licenses, UI badges identify the active superseding record, and release evidence includes a scenario proving historical links remain intact after correction.

### 32. Appeals, reconsiderations, and variance workflows

**Justification:** Permit denials, license actions, and enforcement outcomes often trigger appeals or variance requests. The domain needs a structured path for reconsideration instead of forcing staff to improvise outside the system.

**Improvement:** Add appeal and variance case types with filing deadlines, record-locking behavior, hearing requirements, evidence packet assembly, and outcome effects on the underlying case. Distinguish administrative reconsideration from formal appeal.

**Acceptance evidence:** Appeal scenarios verify deadline enforcement and outcome propagation, hearing packets attach automatically to the appeal record, and release evidence includes a denial-to-appeal-to-remand example.

### 33. Role-based delegation and override controls

**Justification:** Permitting work frequently requires delegated sign-off and emergency override, but those actions must be visible and constrained. Hidden delegation is a governance failure.

**Improvement:** Add explicit delegation records, acting-on-behalf-of markers, override reasons, duration limits, and supervisor review for high-impact actions such as permit issuance, stop-work orders, waivers, and license suspension. Enforce finer permissions than the current broad approve and admin grants.

**Acceptance evidence:** Permission tests show that only authorized delegates can act, UI displays delegated authority and override rationale, and release evidence includes expired-delegation and blocked-override scenarios.

### 34. Agent skill for application intake triage

**Justification:** `PermittingLicensingInspectionsAssistantPanel` should help staff classify and prepare intake work, not just summarize text. Intake triage is a high-value, low-risk place for governed assistance.

**Improvement:** Add an agent skill that reviews a submission package, identifies missing items, proposes application type, flags likely hearing or public-notice obligations, and drafts the intake completeness checklist for staff confirmation. Keep the agent in suggest-only mode unless a human confirms the draft record.

**Acceptance evidence:** Skill evaluations show correct triage suggestions across seeded applications, the assistant cites source documents for each recommendation, and release evidence includes accepted and rejected assistant drafts with audit trails.

### 35. Agent skill for plan review summarization

**Justification:** Reviewers need help consolidating long correction narratives, repeated comment cycles, and discipline conflicts. A domain-tuned skill can reduce review friction without taking away decision authority.

**Improvement:** Add an agent skill that summarizes plan-set changes, groups comments by discipline and code topic, highlights unresolved items across resubmittals, and drafts applicant-facing correction summaries. Require reviewer confirmation before any comment set is issued.

**Acceptance evidence:** Summary quality tests compare agent output to reviewer-approved examples, the assistant references exact plan sheets or comments, and release evidence includes multi-cycle review examples with human confirmation logs.

### 36. Agent skill for inspection preparation and field assistance

**Justification:** Inspectors benefit from a concise case brief before arriving onsite and a structured way to turn findings into complete records afterward. Domain assistance should shorten field time while improving evidence quality.

**Improvement:** Add an agent skill that prepares an inspection brief from approved plans, prior inspections, active conditions, open violations, and prior corrections, then helps convert field notes into a structured inspection record. Keep final outcomes and enforcement choices under inspector control.

**Acceptance evidence:** Field scenarios show the assistant producing accurate pre-visit briefs and post-visit structured drafts, inspectors can accept or reject suggestions item by item, and release evidence includes comparison of raw notes to final recorded findings.

### 37. Agent skill for violation drafting and enforcement recommendations

**Justification:** Violation and enforcement work is text-heavy and deadline-sensitive. A governed skill can help produce consistent notices and escalation recommendations while leaving legal and supervisory authority with humans.

**Improvement:** Add an agent skill that classifies observed violations, drafts notices, suggests cure deadlines, recommends escalation based on recurrence and severity, and assembles the evidence packet for review. Record the rule basis and source evidence for every recommendation.

**Acceptance evidence:** Draft notices generated by the assistant are compared against approved templates and human outcomes, recommendation logs show cited facts and rules, and release evidence includes blocked cases where the agent lacked sufficient evidence.

### 38. Geospatial, zoning, and address validation

**Justification:** Many permitting and licensing decisions depend on parcel boundaries, zoning districts, overlays, frontage, flood or hazard zones, and jurisdiction limits. The PBC should not accept site data without geospatial validation.

**Improvement:** Add geospatial validation for parcel-to-address matching, zoning district lookup, jurisdiction boundary checks, and overlay-triggered review requirements. Store the geospatial evidence used for each decision so later appeals can reconstruct the basis.

**Acceptance evidence:** Tests cover valid and invalid site locations, the UI shows zoning and overlay context on case detail, and release evidence includes geospatial lookup artifacts tied to review-routing decisions.

### 39. Contractor, business, and responsible-party registry synchronization

**Justification:** Permits and licenses often depend on active contractor credentials, business registrations, and designated responsible parties. The current manifest shows consumed events, but the backlog should sharpen how those dependencies affect case progress.

**Improvement:** Tie `CustomerUpdated` and `SupplierQualified` style dependencies to contractor license validity, business standing, insurance or bond status, and responsible-party changes. Open exceptions when dependent registry information becomes stale or disqualifying.

**Acceptance evidence:** Consumed-event tests prove that stale or disqualifying registry changes open visible exceptions, case detail shows dependency freshness, and release evidence includes a suspended-contractor scenario that blocks permit progress.

### 40. SLA calendars, workload balancing, and escalation

**Justification:** Review timeliness matters in permitting, especially when statutes or published service targets apply. Queue metrics alone are not enough without calendar-aware clocks and escalation rules.

**Improvement:** Add SLA calendars for intake screening, plan review, inspection response, correction review, renewal processing, hearing preparation, and enforcement follow-up. Support pause rules for applicant waiting periods and escalation when internal deadlines are missed.

**Acceptance evidence:** SLA timers respect business calendars and pause states, the workbench highlights at-risk and breached work, and release evidence includes tests for clock start, pause, resume, and escalation behavior.

### 41. Analytics for throughput, aging, and compliance

**Justification:** A domain workbench should answer operational questions such as where reviews stall, which inspection types re-fail most often, and how long renewals stay in grace. Better analytics make policy and staffing choices defensible.

**Improvement:** Expand analytics to cover intake completeness rates, discipline review turnaround, correction cycle counts, issuance latency, inspection failure rates, violation cure performance, hearing outcomes, renewal conversion, and enforcement escalation patterns. Separate staff workload views from public-service outcomes.

**Acceptance evidence:** Metrics definitions are published, dashboards reconcile with seeded scenarios and event counts, and release evidence includes screenshots and numeric checks for each major lifecycle stage.

### 42. Release evidence matrix and traceability

**Justification:** The backlog should not stop at ideas; it should force proof. `RELEASE_EVIDENCE.md` should be able to show which requirement, test, UI screen, event, and scenario demonstrates each domain capability.

**Improvement:** Build a release evidence matrix that maps every major domain area in this backlog to APIs, events, UI fragments, tests, seed data, and operator walkthroughs. Flag gaps where a claimed capability lacks executable evidence or visible UI coverage.

**Acceptance evidence:** `RELEASE_EVIDENCE.md` contains a trace table keyed by backlog section, missing evidence fails the release gate, and release packages include direct links to tests, screenshots, event payloads, and scenario outputs.

### 43. Seed scenarios and regression packs

**Justification:** Domain regressions often hide in rare but critical case shapes such as appealed denials, continued hearings, reinspections after corrections, and provisional approvals. Seed scenarios should mirror the real lifecycle, not only happy paths.

**Improvement:** Add end-to-end seeded cases for standard permit review, phased permit issuance, complaint-led inspection, violation escalation, hearing continuance, renewal denial, reinstatement, public notice, and refund-eligible fee reversal. Use the scenarios for demos, regression tests, and release proof.

**Acceptance evidence:** Seed packs can be loaded repeatedly without divergence, regression tests run against those packs, and release evidence includes named scenario traces from intake through final disposition.

### 44. Audit trail, chain of custody, and public records

**Justification:** Permitting records may be requested in audits, litigation, public-records responses, and appeals. Auditability requires both procedural history and evidence integrity.

**Improvement:** Strengthen audit trails with immutable event lineage, document custody tracking, redaction metadata, public-records export views, and separation between confidential and releasable artifacts. Keep service proofs, hearing exhibits, and field evidence traceable from creation to disclosure.

**Acceptance evidence:** Audit exports preserve chronology and redaction state, custody history is visible per artifact, and release evidence includes a public-records export walkthrough with confidential material correctly withheld.

### 45. Multi-tenant ordinance and policy parameterization

**Justification:** Different jurisdictions apply different ordinances, fee schedules, notice rules, and hearing thresholds. A reusable PBC must vary local policy without forking the core lifecycle.

**Improvement:** Expand `permitting_licensing_inspections_policy_rule` and runtime parameters so each tenant can configure review disciplines, fee formulas, notice windows, hearing triggers, inspection cadences, renewal periods, and enforcement steps. Preserve default patterns while allowing local overrides with effective dates.

**Acceptance evidence:** Tenant-specific scenarios produce different but explainable outcomes from the same baseline case, configuration history is visible in the workbench, and release evidence includes cross-tenant comparison packs with no policy leakage.

### 46. Accessibility, language access, and digital equity

**Justification:** Citizen-facing permitting software fails the public if it assumes English-only, desktop-only, or expert-only users. Accessibility and language access are domain requirements for public service delivery.

**Improvement:** Make the citizen portal and internal UI support accessible workflows, plain-language stage explanations, translated notices, mobile-responsive intake, and assisted channels for users who cannot complete a digital application alone. Track preferred language and accommodation needs on the case.

**Acceptance evidence:** Accessibility checks pass on portal and workbench flows, translated templates render correctly with case data, and release evidence includes screen-reader, keyboard-only, and mobile-device walkthroughs.

### 47. Offline field operations and sync recovery

**Justification:** Inspectors and enforcement officers often work in areas with weak connectivity. The package should let them capture findings safely offline and then reconcile without losing evidentiary integrity.

**Improvement:** Add offline capture for inspections, notices served in the field, signatures, photos, and follow-up tasks with conflict-aware sync when the device reconnects. Preserve the original offline timestamps and device actor identity when records are merged.

**Acceptance evidence:** Offline-to-sync scenarios show no lost observations or media, conflict cases are surfaced for human review, and release evidence includes field-mode screenshots and sync reconciliation logs.

### 48. Operational runbooks, dead letters, and exception recovery

**Justification:** Real permitting systems fail in production through stuck events, duplicate notifications, stale dependencies, and malformed submissions. Recovery needs domain-aware runbooks, not just infrastructure retries.

**Improvement:** Build operational runbooks for intake failures, event dead letters, failed correspondence, stale payment confirmations, hearing reschedules, and registry-sync exceptions. Tie each runbook to a visible exception type, recovery action, and required evidence after recovery.

**Acceptance evidence:** Exception dashboards expose domain-specific recovery actions, dead-letter scenarios can be replayed safely, and release evidence includes operator runbook walkthroughs plus before-and-after exception state proofs.

### 49. Training assets and operator readiness

**Justification:** A deep domain PBC still fails if staff cannot learn the intended lifecycle and controls. Release readiness should include role-based operator guidance, not only technical artifacts.

**Improvement:** Produce role-specific walkthroughs for intake staff, reviewers, inspectors, supervisors, hearing clerks, and enforcement staff that use seeded cases and the actual UI. Include guidance for assistant usage, override rules, and evidence expectations.

**Acceptance evidence:** Training packs reference seeded scenarios and live UI states, operator signoff is recorded against each role track, and release evidence includes walkthrough completion records and feedback-based revisions.

### 50. Go-live readiness and post-release evidence

**Justification:** The package should only declare readiness when it can prove the domain lifecycle works in practice across applications, plan review, fees, issuance, licenses, inspections, violations, renewals, public notices, hearings, enforcement, citizen portals, UI, agent skills, and events. Go-live is a domain evidence problem, not a purely technical deploy step.

**Improvement:** Create a go-live gate that requires verified scenarios, queue dashboards, notice templates, event schemas, assistant guardrails, public portal checks, and rollback plans for the full permitting and licensing lifecycle. Extend post-release evidence to show first-run production health, exception rates, and any capability gaps discovered after launch.

**Acceptance evidence:** The release gate fails if any major domain lane lacks executable proof, `RELEASE_EVIDENCE.md` includes pre-release and post-release sections with linked artifacts, and the final evidence pack shows path-by-path verification for each backlog area in this file.
