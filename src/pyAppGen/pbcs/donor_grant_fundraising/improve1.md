# Donor Grant Fundraising Improvement Backlog

This backlog is specific to the exact key `donor_grant_fundraising` and is grounded in the current manifest surfaces for donors, campaigns, pledges, gifts, restrictions, grant applications, stewardship, analytics, assistant support, APIs, events, and release evidence.

## Current Domain Evidence Used

- Exact key: `donor_grant_fundraising`
- Manifest label: `Donor Grant and Fundraising`
- Description: `Donors, campaigns, pledges, restrictions, gifts, grant applications, stewardship, and impact reporting`
- Core tables: `donor`, `campaign`, `pledge`, `gift`, `restriction`, `grant_application`, `stewardship_touchpoint`
- Governance tables: `donor_grant_fundraising_policy_rule`, `donor_grant_fundraising_runtime_parameter`, `donor_grant_fundraising_schema_extension`, `donor_grant_fundraising_control_assertion`, `donor_grant_fundraising_governed_model`
- Current APIs: `POST /donors`, `POST /campaigns`, `POST /pledges`, `POST /gifts`, `POST /restrictions`, `GET /donor-grant-fundraising-workbench`
- Current emitted events: `DonorGrantFundraisingCreated`, `DonorGrantFundraisingUpdated`, `DonorGrantFundraisingApproved`, `DonorGrantFundraisingExceptionOpened`
- Current consumed events: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`
- Current UI fragments: `DonorGrantFundraisingWorkbench`, `DonorGrantFundraisingDetail`, `DonorGrantFundraisingAssistantPanel`
- Current workflows: `donor_grant_fundraising_create_donor_workflow`, `donor_grant_fundraising_record_campaign_workflow`
- Current analytics: `donor_grant_fundraising_risk_score`, `donor_grant_fundraising_workbench_metric`
- Current docs: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`
- Current package test entry: `tests/test_contract.py`

### 1. Unified donor profile with fundraising and grant context

**Justification:** Fundraising teams need one governed profile that combines householding, donor intent, giving history, restriction preferences, and grant-maker attributes without forcing staff to piece context together from separate records.

**Improvement:** Expand the `donor` aggregate into a canonical profile that distinguishes individual, household, corporate, and foundation donors; stores relationship stage, preferred channels, funding interests, recognition preferences, and known compliance requirements; and presents this in `DonorGrantFundraisingDetail` and `DonorGrantFundraisingWorkbench`.

**Acceptance evidence:** Donor profile fixtures cover each donor type, the detail view shows recognition and restriction preferences, and release evidence demonstrates create/update flows through `POST /donors` for the `donor_grant_fundraising` key.

### 2. Prospect-to-donor qualification pipeline

**Justification:** High-value fundraising work starts before a donor is fully active, so the package needs a governed pipeline for research, qualification, assignment, and conversion instead of treating every record as already ready for solicitation.

**Improvement:** Add a prospect pipeline on `donor` with stages for identified, researched, qualified, assigned, cultivated, solicitation-ready, and converted, plus owner assignment, next action date, and qualification evidence.

**Acceptance evidence:** Pipeline stage transitions are visible in the workbench, invalid skips are rejected by policy rules, and release evidence shows conversion from qualified prospect to active donor under `donor_grant_fundraising_create_donor_workflow`.

### 3. Campaign hierarchy and goal modeling

**Justification:** Fundraising campaigns often roll up from annual funds, capital appeals, emergency drives, and grant-backed initiatives, so campaign records need structure beyond a flat name and amount target.

**Improvement:** Extend `campaign` to support parent-child campaigns, objective categories, goal amounts, target donor segments, start and end windows, gift counting rules, and linked grant opportunity themes.

**Acceptance evidence:** Campaign hierarchy fixtures roll up correctly in `DonorGrantFundraisingWorkbench`, drill-in views show child totals, and release evidence includes campaign goal calculations sourced from `POST /campaigns`.

### 4. Pledge lifecycle with installment discipline

**Justification:** Pledges are multi-step commitments that can be verbal, written, revised, partially fulfilled, written off, or restructured, and those differences directly affect revenue planning and stewardship.

**Improvement:** Model `pledge` states for draft, pending confirmation, active, partially paid, fulfilled, overdue, amended, cancelled, and written off, with installment schedules, reminder dates, and amendment reasons.

**Acceptance evidence:** Installment schedules appear on the donor detail page, overdue pledges raise exceptions when milestones pass, and tests show lifecycle transitions initiated through `POST /pledges`.

### 5. Gift application against pledges and campaigns

**Justification:** Gift posting is only useful when finance and advancement staff can see exactly which pledge, campaign, appeal, or unrestricted pool received the money.

**Improvement:** Link each `gift` to campaign, pledge, appeal source, restriction usage, receipt status, and posting date, and show remaining pledge balance and campaign progress immediately after gift entry.

**Acceptance evidence:** Gift-to-pledge matching appears in workbench totals, unmatched gifts open review exceptions, and release evidence shows `POST /gifts` updating both campaign progress and pledge balance projections.

### 6. Restriction catalog with usable spending rules

**Justification:** Restricted funds become operationally risky when the package stores only text descriptions rather than machine-checkable spending constraints and release conditions.

**Improvement:** Enrich `restriction` with restriction type, purpose code, geography, time window, beneficiary class, required approvals, release conditions, and sunset logic that can be evaluated by policy rules and assistant actions.

**Acceptance evidence:** Restriction summaries display machine-readable conditions, prohibited gift applications are blocked with explicit reasons, and release evidence includes policy evaluation traces for `POST /restrictions`.

### 7. Grant opportunity pipeline before application

**Justification:** Grant fundraising success depends on disciplined opportunity management long before an application exists, including qualification, fit scoring, deadlines, and relationship readiness.

**Improvement:** Add a pre-application pipeline on `grant_application` for identified, researching, qualified, drafting, internal review, submitted, declined, awarded, and closed, with funder fit, strategic priority, and deadline confidence fields.

**Acceptance evidence:** Opportunity aging and stage metrics appear on the workbench, expiring opportunities trigger alerts, and release evidence demonstrates stage movement and fit scoring for the `donor_grant_fundraising` package.

### 8. Proposal composition workspace

**Justification:** Proposal development requires narrative, budget, attachments, approvals, and submission packaging, which should remain inside the package boundary rather than living in scattered operator notes.

**Improvement:** Give `grant_application` a proposal workspace with sections for narrative status, budget completeness, attachment checklist, reviewer comments, submission package version, and final sign-off.

**Acceptance evidence:** Proposal completeness is visible in `DonorGrantFundraisingDetail`, incomplete submission attempts are blocked, and release evidence includes proposal readiness snapshots for grant opportunities moving to submitted.

### 9. Grant budget versus restriction validation

**Justification:** Grant proposals and awarded funds frequently carry purpose, time, and cost-category limits that must align with restriction rules before submission and before spending.

**Improvement:** Add validation between `grant_application` budgets and `restriction` rules so staff can see when proposed uses violate purpose codes, timing windows, or approval requirements.

**Acceptance evidence:** Budget-rule mismatches create actionable exceptions, reviewers can inspect the exact violated condition, and release evidence shows a compliant proposal passing validation while a conflicting one is rejected.

### 10. Award acceptance and post-award setup

**Justification:** Winning a grant introduces award conditions, reporting obligations, and stewardship expectations that need controlled setup rather than ad hoc operator follow-up.

**Improvement:** Add a post-award checklist on `grant_application` for award letter review, restriction creation or update, reporting cadence, stewardship owner assignment, acknowledgement deadlines, and renewal planning.

**Acceptance evidence:** Awarded applications cannot move to active stewardship until required setup tasks are complete, the workbench shows post-award readiness, and release evidence captures signed-off award setup records.

### 11. Donor acknowledgement orchestration

**Justification:** Acknowledgements are a core donor promise, and missing or delayed receipts damage trust, compliance posture, and renewal likelihood.

**Improvement:** Add acknowledgement workflows for `gift` and `pledge` with templates by donor type, recognition preference, tax-receipt need, and channel, plus due dates and exception routing for missed service targets.

**Acceptance evidence:** Every qualifying gift shows acknowledgement status, overdue acknowledgements appear in the workbench queue, and release evidence contains receipt and acknowledgement completion metrics.

### 12. Stewardship playbooks by donor segment

**Justification:** Major donors, recurring donors, grant makers, and corporate sponsors require different follow-up patterns, evidence, and messaging.

**Improvement:** Extend `stewardship_touchpoint` with playbook type, expected cadence, touchpoint outcome, next ask readiness, and linked donor segment so teams can run structured stewardship instead of free-form logging.

**Acceptance evidence:** Playbook adherence appears as a stewardship score in the workbench, missed cadence targets open exceptions, and release evidence includes touchpoint completion by segment.

### 13. Relationship timeline across gifts, pledges, and grant proposals

**Justification:** Fundraisers need a single relationship timeline to prepare meetings, understand momentum, and avoid duplicate asks or conflicting stewardship actions.

**Improvement:** Build a chronological relationship timeline that merges `gift`, `pledge`, `campaign`, `grant_application`, and `stewardship_touchpoint` activity into one donor-facing operating view.

**Acceptance evidence:** The detail page shows a unified activity stream, timeline entries link back to owned records, and release evidence demonstrates a donor history rendered from only package-owned tables and projections.

### 14. Household and organizational relationship mapping

**Justification:** Giving decisions often involve spouses, family offices, board members, and institutional contacts, so relationship mapping is necessary for accurate asks and acknowledgements.

**Improvement:** Add relationship structures to `donor` for households, organizational affiliations, advisor roles, and decision-maker influence, with controlled visibility and relationship validity dates.

**Acceptance evidence:** Relationship maps display in the detail view, acknowledgement selection respects recognition relationships, and release evidence shows relationship-aware outreach recommendations for `donor_grant_fundraising`.

### 15. Contact role management for grant makers

**Justification:** Foundation and institutional fundraising depends on accurate contacts for program officers, grants managers, finance reviewers, and signatories.

**Improvement:** Model named contact roles on `grant_application` and linked donor records, including role type, contact window, preferred communication channel, and approval authority.

**Acceptance evidence:** Proposal workflows surface required contact gaps, submission packages reference the right signatory and contact roles, and release evidence includes contact-role validation before submission.

### 16. Opportunity scoring and ask strategy

**Justification:** Teams need a defendable way to prioritize donor and grant opportunities based on affinity, capacity, timing, mission fit, and compliance complexity.

**Improvement:** Use `donor_grant_fundraising_risk_score` and package analytics to create an opportunity score that ranks donor asks and grant pursuits by potential value, likelihood, urgency, and delivery risk.

**Acceptance evidence:** Workbench rankings show why an opportunity is prioritized, score changes are auditable, and release evidence includes ranked pipeline snapshots with explanation fields.

### 17. Internal review chain for proposals and large asks

**Justification:** Major solicitations and grant submissions often require program, finance, legal, and executive review before they should move forward.

**Improvement:** Add review stages, reviewer roles, due dates, comments, and approval evidence to `grant_application` and selected major `pledge` or campaign asks, with enforced separation of duties from package permissions.

**Acceptance evidence:** Review blockers prevent submission or approval until required sign-offs exist, reviewers see pending work in the workbench, and release evidence records completed review chains.

### 18. Board and executive briefing packets

**Justification:** Leadership review is faster and less error-prone when the package can assemble current donor, campaign, and grant context into one governed briefing view.

**Improvement:** Create briefing packet outputs from package-owned data for campaign status, major donor readiness, grant pipeline, restricted-fund exposure, and overdue reporting obligations.

**Acceptance evidence:** Briefing views are generated from current projections, packet data links back to source records, and release evidence includes a reproducible leadership briefing snapshot.

### 19. Document intake for donor instructions and grant requirements

**Justification:** Donor letters, grant guidelines, and award notices often contain operational instructions that staff need interpreted consistently and safely.

**Improvement:** Use `agentic_document_instruction_intake` and `donor_grant_fundraising_semantic_document_instruction_understanding` to parse donor correspondence, proposal guidelines, and award notices into structured tasks, restrictions, and review prompts.

**Acceptance evidence:** Parsed document summaries appear in `DonorGrantFundraisingAssistantPanel`, low-confidence extractions require human confirmation, and release evidence includes side-by-side document and extracted instruction traces.

### 20. Assistant skill pack for grant proposal support

**Justification:** Grant teams benefit from guided drafting help only when the assistant stays inside package boundaries, uses current records, and keeps humans in control of final submission.

**Improvement:** Add governed assistant skills that summarize opportunity fit, propose proposal checklists, flag missing attachments, and draft reviewer questions from `grant_application`, `restriction`, and donor history records.

**Acceptance evidence:** Assistant actions are permission-checked, every draft artifact is traceable to package data, and release evidence demonstrates accepted and rejected assistant suggestions for proposal support.

### 21. Assistant skill pack for stewardship drafting

**Justification:** Stewardship messaging should reflect actual gifts, pledges, restrictions, and recent touchpoints rather than generic thank-you text.

**Improvement:** Add governed assistant skills that draft acknowledgement notes, meeting prep briefs, renewal prompts, and impact updates based on `gift`, `pledge`, `stewardship_touchpoint`, and donor preferences.

**Acceptance evidence:** Staff can review generated drafts in `DonorGrantFundraisingAssistantPanel`, assistant output cites supporting records, and release evidence shows approval before any draft becomes an outbound message.

### 22. Guardrails for assistant-triggered mutations

**Justification:** Assistant support becomes unsafe when it can create donors, restrictions, or approvals without explicit policy checks and operator review.

**Improvement:** Require action previews, approval routing, idempotency keys, and policy evaluation before assistant-initiated create or update actions touch `donor`, `pledge`, `gift`, `restriction`, or `grant_application`.

**Acceptance evidence:** Mutation previews display affected fields, denied assistant actions log policy reasons, and release evidence contains approved versus blocked assistant action samples for the `donor_grant_fundraising` key.

### 23. Donor portfolio workbench

**Justification:** Relationship managers need a first-class operating surface for assigned donors, next actions, open pledges, recent gifts, and stewardship gaps.

**Improvement:** Create a portfolio slice in `DonorGrantFundraisingWorkbench` that filters donors by owner, stage, next action, campaign alignment, pledge exposure, and acknowledgement backlog.

**Acceptance evidence:** Portfolio queues load from package projections, managers can sort by next action and risk, and release evidence includes role-based donor portfolio screenshots tied to package data.

### 24. Grant pipeline workbench

**Justification:** Grant teams need one queue for qualification, drafting, reviews, deadlines, submissions, awards, and renewals rather than separate manual trackers.

**Improvement:** Add a grant pipeline workbench slice with deadline buckets, stage counts, reviewer blockers, compliance obligations, and renewal forecast indicators driven from `grant_application`.

**Acceptance evidence:** Deadline risk highlights appear without leaving the package, stage counts reconcile to stored records, and release evidence includes grant pipeline metrics derived from owned projections.

### 25. Campaign performance workbench

**Justification:** Campaign leaders need current progress, donor movement, pledge conversion, gift pace, and segment performance in one operating view.

**Improvement:** Extend `DonorGrantFundraisingWorkbench` with campaign rollups, segment performance, ask conversion, average gift, pledge fulfillment trend, and linked grant-funded campaign indicators.

**Acceptance evidence:** Campaign totals reconcile to underlying gifts and pledges, trends update after new gift posting events, and release evidence shows campaign performance views for multiple campaign types.

### 26. Restriction compliance workbench

**Justification:** Restricted fund oversight needs a dedicated operational surface because violations often arise from timing, purpose, and approval mismatches that are easy to miss in generic queues.

**Improvement:** Add a compliance slice showing active restrictions, pending releases, blocked uses, expiring conditions, overdue approvals, and grant-linked obligations.

**Acceptance evidence:** Restriction exceptions are drillable from the workbench, blocked uses show exact policy failures, and release evidence includes compliance queue exports for auditors and operators.

### 27. Reporting calendar and submission workspace

**Justification:** Grant reporting and donor impact updates are deadline-driven and should be managed as operational work, not as calendar reminders outside the package.

**Improvement:** Create a reporting workspace for `grant_application` and stewardship obligations with report type, period, evidence checklist, owner, review chain, and submission status.

**Acceptance evidence:** Upcoming and overdue reports appear in the workbench, missing evidence blocks submission completion, and release evidence includes report readiness snapshots and submission logs.

### 28. Impact reporting tied to gifts and grants

**Justification:** Donors and grant makers want credible outcome reporting that traces to funded programs, restrictions, and stewardship commitments.

**Improvement:** Link `gift`, `restriction`, and `grant_application` records to impact reporting statements, evidence references, outcome periods, and narrative approval status inside the package.

**Acceptance evidence:** Impact reports show traceability from funding source to reported outcome, incomplete evidence is flagged before publication, and release evidence contains outcome trace reports for sample gifts and grants.

### 29. API boundary for donor profile mutations

**Justification:** The package needs clear contract boundaries so external callers know which mutations belong in package-owned APIs and which data must arrive through consumed events.

**Improvement:** Tighten the `POST /donors` contract with required donor profile fields, source attribution, duplicate checks, and mutation rules that prevent accidental edits to fields owned by other packages.

**Acceptance evidence:** Contract tests reject out-of-bound fields, accepted payloads persist only package-owned data, and release evidence includes API examples and negative cases for `POST /donors`.

### 30. API boundary for campaign, pledge, gift, and restriction writes

**Justification:** Write APIs are safe only when boundaries are explicit about who can create, revise, approve, and reconcile fundraising records.

**Improvement:** Define stricter contracts for `POST /campaigns`, `POST /pledges`, `POST /gifts`, and `POST /restrictions`, including approval prerequisites, idempotency behavior, conflict handling, and source-system attribution.

**Acceptance evidence:** Contract tests cover happy paths and duplicate submissions, the workbench shows source attribution on created records, and release evidence documents idempotent replay behavior for each write API.

### 31. Event boundary and replay discipline

**Justification:** Fundraising and grant operations depend on trustworthy projections, which means emitted and consumed events need clear meaning, replay behavior, and exception handling.

**Improvement:** Document and enforce event semantics for `DonorGrantFundraisingCreated`, `DonorGrantFundraisingUpdated`, `DonorGrantFundraisingApproved`, and `DonorGrantFundraisingExceptionOpened`, plus consumed event effects from `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified`.

**Acceptance evidence:** Event replay tests rebuild core projections without drift, duplicate delivery is handled idempotently, and release evidence includes event flow diagrams and replay checksums for `donor_grant_fundraising`.

### 32. Exception taxonomy for fundraising and grant operations

**Justification:** Operators need to distinguish data quality errors, policy failures, deadline risks, approval gaps, and external dependency problems so remediation is immediate and accurate.

**Improvement:** Add exception types, severity, owner, due date, retryability, linked record, and closure evidence across donor, pledge, gift, restriction, and grant application flows.

**Acceptance evidence:** Exception queues can be filtered by type and severity, closure requires evidence, and release evidence includes exception aging and resolution metrics from the package workbench.

### 33. Duplicate donor and pledge resolution

**Justification:** Duplicate records distort campaign performance, acknowledgement status, and stewardship planning, especially when donors give through multiple channels.

**Improvement:** Add matching and merge workflows for `donor` and duplicate-detection logic for `pledge`, with confidence scoring, operator review, and retained audit history for all merge decisions.

**Acceptance evidence:** Suspected duplicates appear in a governed review queue, merge actions preserve source references, and release evidence demonstrates duplicate handling without losing gift or pledge lineage.

### 34. Renewal forecasting for grants and recurring donors

**Justification:** Forecasting is stronger when the package can distinguish likely renewals, at-risk renewals, and lapsed relationships before teams miss a window.

**Improvement:** Extend package analytics to forecast grant renewal probability, recurring donor retention, and campaign reactivation likelihood using prior stewardship quality, reporting timeliness, and funding history.

**Acceptance evidence:** Forecast outputs are explainable in the workbench, score changes are auditable, and release evidence includes renewal forecast accuracy checks against held-out historical records.

### 35. Counterfactual ask and funding scenarios

**Justification:** Fundraising leaders need to compare ask strategies, campaign pacing, and grant pursuit choices before committing scarce staff time.

**Improvement:** Use `donor_grant_fundraising_counterfactual_scenario_simulation` to simulate outcomes for different ask amounts, donor assignments, campaign timing, reporting delays, and proposal submission mixes.

**Acceptance evidence:** Scenario comparisons show assumptions and projected outcomes side by side, simulation inputs are preserved for review, and release evidence includes approved scenario runs tied to planning decisions.

### 36. Compliance calendar with obligation tracking

**Justification:** Grant terms, restricted gifts, acknowledgement rules, and internal approvals all create time-bound obligations that should be monitored centrally.

**Improvement:** Add a compliance calendar that tracks report due dates, acknowledgement deadlines, approval expirations, stewardship commitments, and restriction sunset dates across package records.

**Acceptance evidence:** Calendar-driven alerts appear in the workbench, overdue items generate exceptions automatically, and release evidence shows compliance coverage for active grants and restricted gifts.

### 37. Policy rule coverage for separation of duties

**Justification:** Sensitive fundraising actions such as approving major gifts, releasing restrictions, and finalizing award setup should not be performed by a single unchecked actor.

**Improvement:** Extend `donor_grant_fundraising_policy_rule` to encode reviewer independence, approval thresholds, large-gift controls, and restricted-fund release approvals tied to package permissions.

**Acceptance evidence:** Policy tests prove blocked self-approval paths, approver roles display in the UI, and release evidence contains separation-of-duties control results for high-risk flows.

### 38. Multi-tenant portfolio isolation

**Justification:** Organizations using the package in shared infrastructure need strict tenant separation for donor relationships, fundraising plans, and grant obligations.

**Improvement:** Apply `donor_grant_fundraising_multi_tenant_policy_isolation` to donor portfolios, campaign analytics, assistant actions, and release evidence access, with tenant-aware configuration and policy enforcement.

**Acceptance evidence:** Cross-tenant access attempts are denied, tenant-scoped workbench views show only local records, and release evidence includes isolation test results for the `donor_grant_fundraising` package.

### 39. Consent, privacy, and recognition preference controls

**Justification:** Donor trust depends on honoring privacy settings, communication consent, anonymous giving requests, and recognition limitations across every downstream workflow.

**Improvement:** Add consent and preference controls to `donor` that influence acknowledgement generation, stewardship prompts, reporting visibility, and assistant draft content.

**Acceptance evidence:** Anonymous donors are suppressed from recognition outputs, blocked channels are respected in follow-up plans, and release evidence includes consent-driven behavior tests in the donor workbench.

### 40. Soft credit and relationship-aware attribution

**Justification:** Campaign reporting and stewardship planning often require recognizing who influenced or facilitated a gift even when legal ownership stays with a different donor record.

**Improvement:** Add soft-credit attribution structures for gifts and pledges so households, board champions, or institutional introducers can be reflected in analytics without corrupting legal donor ownership.

**Acceptance evidence:** Soft-credit totals appear separately from legal totals, attribution changes preserve audit history, and release evidence demonstrates relationship-aware campaign reports.

### 41. Restricted-fund release and amendment workflow

**Justification:** Restrictions change over time through board action, donor approval, or grant amendment, and those changes need controlled workflow rather than silent field edits.

**Improvement:** Add release and amendment workflows for `restriction` with request reason, supporting evidence, approver routing, effective date, and downstream impact preview on gifts and reports.

**Acceptance evidence:** Proposed restriction changes show impact analysis before approval, unauthorized amendments are blocked, and release evidence captures completed release or amendment cases with approval history.

### 42. Grant amendment and rebudgeting workflow

**Justification:** Awarded grants commonly require rebudgeting, no-cost extensions, or scope adjustments, and those changes affect compliance and reporting.

**Improvement:** Add amendment paths on `grant_application` for rebudgeting, extension, scope revision, and reporting cadence changes, with reviewer roles and linked updated restrictions where necessary.

**Acceptance evidence:** Amendment requests preserve previous approved values, downstream reporting calendars update after approval, and release evidence includes amended grant cases with before-and-after comparison views.

### 43. Revenue pacing and cash forecast analytics

**Justification:** Advancement leaders need to distinguish booked pledges, received gifts, restricted balances, and likely grant awards to manage timing and staffing decisions.

**Improvement:** Add analytics that separate committed, received, expected, restricted, and available funding across campaigns, grant opportunities, and donor portfolios using package-owned projections.

**Acceptance evidence:** Forecast tiles reconcile to pledge and gift states, scenario assumptions are visible, and release evidence includes monthly pacing views for campaigns and grants.

### 44. Major donor meeting preparation workspace

**Justification:** Fundraisers prepare better when donor history, recent touchpoints, pending pledges, restrictions, and active opportunities are assembled into one briefing surface.

**Improvement:** Create a meeting-prep view that pulls donor profile, recent gifts, open asks, stewardship notes, proposal status, and recommended next steps into `DonorGrantFundraisingAssistantPanel` and the detail page.

**Acceptance evidence:** Meeting brief generation cites specific package records, stale data warnings are visible before export, and release evidence includes reproducible briefing examples for major donor visits.

### 45. Reporting-quality controls and evidence bundles

**Justification:** Donor and grant reports need defendable evidence packages so reviewers can trust statements before they leave the organization.

**Improvement:** Add evidence bundles for impact reporting and grant reporting that collect supporting records, versioned narrative text, reviewer sign-off, and provenance hashes from package-owned data.

**Acceptance evidence:** Reports cannot move to complete without required evidence attached, reviewer sign-off is stored with timestamps, and `RELEASE_EVIDENCE.md` includes reporting control results for `donor_grant_fundraising`.

### 46. Control testing for fundraising operations

**Justification:** High-value controls should run continuously against live package behavior rather than existing only as release-time checklists.

**Improvement:** Use `donor_grant_fundraising_control_assertion` and `donor_grant_fundraising_continuous_control_testing` to monitor duplicate gifts, overdue acknowledgements, missing report reviews, expired restrictions, and skipped approvals.

**Acceptance evidence:** Control failures raise package exceptions automatically, control results are visible in the workbench, and release evidence includes passing and failing control samples with remediation history.

### 47. Audit-proof approval history

**Justification:** Donor approvals, proposal approvals, restriction releases, and major gift decisions need tamper-evident history to support audits and dispute resolution.

**Improvement:** Apply `donor_grant_fundraising_event_sourced_operational_history` and `donor_grant_fundraising_cryptographic_audit_proofs` to all high-risk approvals and exceptions across core records.

**Acceptance evidence:** Approval history can be replayed in order, proof verification detects tampering, and release evidence includes approval-history verification runs for selected donor and grant workflows.

### 48. Schema extension governance for nonprofit-specific fields

**Justification:** Different organizations will need fields such as constituency tags, fiscal sponsor data, or grant classification details, and those extensions should remain governed.

**Improvement:** Use `donor_grant_fundraising_schema_extension` to allow tenant-scoped schema additions with compatibility checks, migration previews, projection impact review, and assistant-awareness rules.

**Acceptance evidence:** Extension registration requires approval, compatibility tests run before activation, and release evidence shows one extension path added without breaking existing donor or grant projections.

### 49. Domain seed data and contract scenarios

**Justification:** Reliable delivery depends on package-native scenarios that reflect actual nonprofit fundraising and grant operations rather than minimal placeholder examples.

**Improvement:** Expand `seed_data.py` and package tests to include realistic donor profiles, campaigns, pledges, restricted gifts, proposal reviews, awarded grants, stewardship touchpoints, and reporting obligations.

**Acceptance evidence:** Seed data creates a usable demonstration portfolio in `DonorGrantFundraisingWorkbench`, contract tests cover the main write APIs and projections, and release evidence references those package scenarios explicitly.

### 50. Release readiness scorecard for donor and grant operations

**Justification:** The package needs a repeatable go-live view that shows whether fundraising, grant, compliance, assistant, API, and reporting capabilities are ready together.

**Improvement:** Create a release readiness scorecard that summarizes API contract coverage, event replay health, workbench readiness, control status, assistant guardrails, reporting evidence, and unresolved exception counts for `donor_grant_fundraising`.

**Acceptance evidence:** `RELEASE_EVIDENCE.md` contains the scorecard with pass/fail criteria, the scorecard links back to package artifacts and tests, and release evidence demonstrates no unreviewed blocker remains at sign-off.
