# Land and Real Estate Development Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `land_real_estate_development`.
- Manifest description: parcels, entitlements, zoning, feasibility, permits, development milestones, and land economics.
- Owned tables currently include `land_parcel`, `zoning_case`, `entitlement`, `feasibility_model`, `permit_application`, `development_milestone`, and `land_option`.
- Current APIs include `POST /land-parcels`, `POST /zoning-cases`, `POST /entitlements`, `POST /feasibility-models`, `POST /permit-applications`, and `GET /land-real-estate-development-workbench`.
- Current workflows include land parcel creation and zoning case recording.
- Current UI fragments include `LandRealEstateDevelopmentWorkbench`, `LandRealEstateDevelopmentDetail`, and `LandRealEstateDevelopmentAssistantPanel`.
- Current emitted events include `LandRealEstateDevelopmentCreated`, `LandRealEstateDevelopmentUpdated`, `LandRealEstateDevelopmentApproved`, and `LandRealEstateDevelopmentExceptionOpened`.
- Current consumed events include `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified`.

### 1. Parcel identity and legal description mastering
**Justification:** Land deals fail early when parcel numbers, lot references, metes-and-bounds text, and legal descriptions drift across diligence, entitlement, and closing packets. The current `land_parcel` surface needs a stronger canonical identity model before downstream approvals and economics can be trusted.
**Improvement:** Extend `land_parcel` to store parcel aliases, assessor parcel numbers, recorder references, legal descriptions, survey revision lineage, acreage variants, and source-of-truth ranking so the workbench can show one governed parcel identity with explicit discrepancies.
**Acceptance evidence:** Contract tests proving one canonical parcel can reconcile multiple source identifiers, workbench discrepancy badges for mismatched legal descriptions, and audit entries showing who accepted or rejected a parcel identity merge.

### 2. Assemblage and site-control workflow
**Justification:** Real projects often depend on stitching together contiguous parcels through options, purchase agreements, rights of entry, and exclusivity periods rather than a single acquisition event. Without assemblage logic, feasibility and entitlements will be modeled against land the developer does not fully control.
**Improvement:** Add an assemblage layer above `land_parcel` and `land_option` that tracks target site boundaries, controlling agreements, seller holdouts, drop-dead dates, termination rights, and minimum-control thresholds required to proceed to entitlement submission.
**Acceptance evidence:** Scenario fixtures covering partial assemblage, expiring option windows, and seller holdout cases, plus a workbench map that flags whether the development site has enough controlled acreage to advance.

### 3. Survey, title, and boundary conflict register
**Justification:** Boundary overlaps, unrecorded easements, encroachments, and inconsistent survey calls can destroy site plans long after acquisition underwriting appears complete. These defects belong in the operating model, not in disconnected diligence folders.
**Improvement:** Introduce a parcel-level conflict register that links survey revisions, title exceptions, encroachment findings, boundary disputes, and required cure actions to `land_parcel` records and downstream entitlement blocking rules.
**Acceptance evidence:** Test cases showing a boundary conflict blocking subdivision and permit readiness, plus detail views that expose unresolved survey and title issues with owner, due date, and cure status.

### 4. Title commitment exception triage
**Justification:** Title commitments contain restrictive covenants, reciprocal easement agreements, mineral reservations, access gaps, and lien items that materially change yield and buildability. Treating title review as a generic attachment workflow misses one of the core land-development risks.
**Improvement:** Create structured title-exception entities tied to `land_parcel` and `land_option`, including exception type, burdened acreage, cure path, endorsement dependency, closing condition, and whether the item affects zoning strategy, lenderability, or construction access.
**Acceptance evidence:** Structured examples for liens, access exceptions, and use restrictions, a blocking rule that prevents acquisition approval when uncured fatal exceptions remain, and a workbench panel showing cure progress by parcel.

### 5. Environmental diligence progression
**Justification:** Phase I findings, recognized environmental conditions, historical use, vapor intrusion concerns, wetlands presence, and remediation obligations all change acquisition and entitlement posture. The PBC needs explicit diligence stages instead of a binary clear/not-clear marker.
**Improvement:** Add environmental diligence states and issue types across Phase I, Phase II, remediation planning, agency closure, and post-closing monitoring, with each issue linked to parcel risk, contingency language, and schedule impacts inside `feasibility_model`.
**Acceptance evidence:** Feasibility test fixtures where contamination changes residual land value and go/no-go recommendations, plus workbench evidence that unresolved environmental items automatically open blocking exceptions.

### 6. Geotechnical, floodplain, and subsurface constraints
**Justification:** Deep foundations, unsuitable soils, flood storage requirements, groundwater management, and cut/fill imbalance can move a project from viable to uneconomic. These are feasibility drivers, not merely consultant outputs.
**Improvement:** Model subsurface and physical-site constraints as structured feasibility inputs with cost ranges, severity tiers, affected parcels, and mitigation assumptions so land economics and infrastructure phasing use governed site-condition data.
**Acceptance evidence:** Sensitivity tests showing changed soil or flood assumptions altering infrastructure costs and yield, and a feasibility screen that highlights parcels needing abnormal foundation or drainage treatment.

### 7. Zoning ordinance matrix and permitted-use engine
**Justification:** Entitlement strategy starts with what zoning already allows by right, by special use, by variance, or not at all. A shallow `zoning_case` record cannot support realistic underwriting without ordinance-level development standards.
**Improvement:** Expand `zoning_case` to hold zoning districts, overlay districts, permitted-use categories, density limits, height envelopes, setbacks, parking ratios, open-space requirements, and trigger conditions for discretionary approvals.
**Acceptance evidence:** Rule tests validating a concept program against district standards, workbench comparison tables for by-right versus discretionary scenarios, and ordinance citations stored with each governing standard.

### 8. Entitlement dependency graph
**Justification:** Rezoning, preliminary plat, site plan, conditional use permit, design review, subdivision map, utility approvals, and environmental determinations often depend on each other in strict order. Missing dependency logic leads to impossible schedules and false readiness.
**Improvement:** Build a dependency graph across `zoning_case`, `entitlement`, `permit_application`, and `development_milestone` so each approval path can define prerequisites, parallel tracks, appeal windows, and downstream tasks blocked by unresolved agency action.
**Acceptance evidence:** Graph-based tests that reject impossible submission sequences, workbench critical-path visuals, and milestone projections proving that entitlement dependencies roll up into schedule risk.

### 9. Jurisdiction calendar and hearing cadence management
**Justification:** Planning commission cycles, council hearing calendars, noticing windows, resubmittal cutoffs, and holiday blackouts drive schedule realism more than internal task due dates. Development teams need agency-time visibility, not just task-time visibility.
**Improvement:** Add jurisdiction calendars and hearing cadence metadata to `zoning_case` and `entitlement`, including notice lead times, staff review windows, quorum-dependent hearing dates, and standard deferral outcomes when packets miss cutoff.
**Acceptance evidence:** Calendar simulation tests that move hearing dates when submission packets miss a cutoff, and workbench aging views that separate internal delay from agency-calendar delay.

### 10. Community engagement and political-risk tracking
**Justification:** Neighborhood opposition, council priorities, school-capacity concerns, labor commitments, and traffic objections frequently reshape entitlement conditions. Political feasibility should be explicit in the PBC rather than buried in meeting notes.
**Improvement:** Add a stakeholder and issue ledger tied to `zoning_case` and `entitlement` that records public comments, elected-official positions, neighborhood commitments, issue severity, and mitigation promises that must flow into final approvals.
**Acceptance evidence:** Structured hearing packet summaries, risk scores that rise when opposition themes intensify, and acceptance tests proving that promised mitigations become tracked post-approval obligations.

### 11. Acquisition closing readiness gate
**Justification:** Development teams often let entitlement and design work outrun unresolved title, survey, diligence, lender, and seller-deliverable items. A closing gate prevents the package from presenting premature certainty.
**Improvement:** Introduce an acquisition readiness gate spanning `land_option`, `land_parcel`, and `development_milestone` for executed agreements, deposit status, diligence completion, title cures, survey approvals, entity authority, and closing statement signoff.
**Acceptance evidence:** A checklist-driven approval route that blocks close-ready status until mandatory conditions are satisfied, with test cases for missing seller deliverables and expired contingency periods.

### 12. Land option economics and notice windows
**Justification:** Option premiums, extension payments, exercise deadlines, cure rights, and seller notice mechanics are recurring sources of value leakage. They should be modeled as operational clocks, not static agreement metadata.
**Improvement:** Deepen `land_option` to track option tiers, exercise mechanics, extension rights, notice addresses, default cure windows, refundability, and valuation consequences when a deadline is missed or an extension is elected.
**Acceptance evidence:** Deadline-engine tests for exercise and extension scenarios, automated exception generation for near-term option expirations, and a workbench timer lane showing economic exposure by upcoming notice date.

### 13. Development constraints map for easements and setbacks
**Justification:** Recorded easements, utility corridors, access restrictions, building lines, and offsite dedications reduce net developable area and can invalidate unit counts. Feasibility needs a governed land-constraint representation.
**Improvement:** Add structured developable-area reducers to `land_parcel` so the PBC can distinguish gross acreage, constrained acreage, dedication acreage, and net buildable acreage used by `feasibility_model`.
**Acceptance evidence:** Feasibility calculations that trace unit yield back to parcel constraints, workbench visuals highlighting burdened land area, and rule tests proving building envelopes shrink when new easement data is entered.

### 14. Highest-and-best-use scenario library
**Justification:** Site value depends on program choices such as for-sale residential, multifamily, industrial, mixed use, build-to-rent, or land-banked future phases. The PBC should compare realistic development concepts, not a single pro forma stub.
**Improvement:** Expand `feasibility_model` to support multiple named concept scenarios with program mix, density assumptions, parking strategy, phasing approach, entitlement burden, and infrastructure intensity per scenario.
**Acceptance evidence:** Side-by-side scenario outputs with internal rate, margin, yield, schedule, and risk deltas, plus simulation tests that preserve a non-mutating baseline scenario for board review.

### 15. Feasibility assumption register with source lineage
**Justification:** Development feasibility becomes ungovernable when assumptions about rents, absorption, hard costs, fees, carry, and contingency live in spreadsheets without provenance. Every critical assumption should be attributable and challengeable.
**Improvement:** Add a structured assumption register to `feasibility_model` with source type, source date, owner, confidence band, market basis, jurisdiction basis, and whether the assumption is locked, proposed, or under review.
**Acceptance evidence:** Detail pages showing source lineage for top assumptions, tests that invalidate stale assumptions after a configured age threshold, and change logs that explain who altered a key underwriting input.

### 16. Residual land value and seller-price bridge
**Justification:** Acquisition decisions hinge on the gap between seller expectations and residual land value after all entitlement, infrastructure, and construction burdens are included. That bridge should be visible in the operating system.
**Improvement:** Add a residual land value waterfall to `feasibility_model` that separately shows revenue, vertical costs, infrastructure, soft costs, fees, financing, contingency, developer margin, and resulting land value versus purchase price.
**Acceptance evidence:** Waterfall snapshots for board-ready review, scenario tests that quantify why a site fails hurdle rate, and workbench indicators flagging whether seller pricing exceeds supportable value.

### 17. Infrastructure capacity and will-serve management
**Justification:** Water, sewer, power, gas, telecom, and storm capacity often control whether a site can be phased or built at all. Infrastructure availability belongs in the domain core, not as free-text comments under permits.
**Improvement:** Add infrastructure-capacity records linked to `land_parcel`, `entitlement`, and `permit_application`, capturing provider, available capacity, required upgrades, will-serve letter status, cost responsibility, and expiration of utility commitments.
**Acceptance evidence:** Structured will-serve workflows, alerts when provider letters expire before permit issuance, and feasibility tests that move a project from viable to blocked when utility capacity drops below need.

### 18. Offsite improvement and frontage obligation planning
**Justification:** Road widening, turn lanes, sidewalks, signalization, drainage upgrades, and utility extensions often sit outside the site boundary but dominate early capital planning. These obligations need traceability from approval condition to construction handoff.
**Improvement:** Create offsite-improvement records tied to approvals and milestones, with agency owner, frontage limits, trigger condition, estimated cost, reimbursement potential, and whether the item is prerequisite to vertical permit or certificate of occupancy.
**Acceptance evidence:** Obligation views proving each offsite item rolls from approval condition into budget and milestone tracking, with tests for prerequisite logic before construction release.

### 19. Subdivision, plat, and map sequencing
**Justification:** Many developments need lot splits, replats, condominium maps, dedications, and easement vacations before financing, sale, or construction turnover can occur. The package needs map-level sequencing instead of generic milestone names.
**Improvement:** Add platting and map workflows to `entitlement` and `development_milestone`, including map type, review stage, agency signoff path, recording status, and which parcels or phases become marketable after recordation.
**Acceptance evidence:** Workflow tests showing a sale or building permit cannot proceed before required map recordation, and a workbench lane that tracks agency review versus county recording completion.

### 20. Permit package completeness and drawing-set control
**Justification:** Permit review stalls when civil, landscape, architecture, structural, utility, and consultant sheets are out of sync or missing jurisdiction-required forms. Completeness should be measurable before submittal.
**Improvement:** Expand `permit_application` to manage drawing-set versions, discipline checklists, consultant seals, jurisdiction forms, deferred-submittal items, and completeness scoring prior to official agency intake.
**Acceptance evidence:** Packet-completeness tests for common submittal types, red/yellow/green readiness indicators in the workbench, and immutable version records for each issued plan set.

### 21. Agency comment roundtrip and response quality control
**Justification:** Approval cycles are won or lost in comment responses, condition clarifications, and resubmittal discipline. The PBC should manage the roundtrip as a governed process rather than a document email chain.
**Improvement:** Add agency comment items to `permit_application` and `entitlement` with comment category, originating department, plan sheet reference, proposed response, responsible discipline, due date, and acceptance status after resubmittal.
**Acceptance evidence:** Response-matrix exports, tests proving unresolved high-severity comments block resubmittal approval, and workbench filters by department, severity, and aging.

### 22. Development agreement and condition-of-approval register
**Justification:** Post-approval obligations often live for years and include phasing triggers, public improvements, affordability commitments, school mitigation, art requirements, and reporting duties. If they are not structured at approval time, they disappear before handoff.
**Improvement:** Create an obligations register linked to `entitlement`, `permit_application`, and `development_milestone` for every approval condition, development agreement clause, reporting date, and physical-delivery requirement.
**Acceptance evidence:** Tests showing conditions survive from approval into construction and closeout phases, plus a workbench obligations calendar with owner, trigger, due date, and evidence status.

### 23. Impact fee, exaction, and reimbursement ledger
**Justification:** Fee programs and exactions directly affect land value and release timing, and reimbursement rights can materially improve project returns. The PBC needs structured economic tracking around agency charges and credits.
**Improvement:** Add a ledger for impact fees, in-lieu fees, dedications, exactions, credits, reimbursements, and fee deferrals, linked to parcel phase, permit stage, and agency ordinance basis.
**Acceptance evidence:** Reconciliation tests between modeled fees and approved obligations, visibility into paid versus accrued fee exposure, and workflow evidence for reimbursement claim preparation.

### 24. Affordable housing and public-benefit compliance
**Justification:** Inclusionary requirements, affordability covenants, prevailing wage triggers, local hiring pledges, and community-benefit packages are frequent approval conditions with long tails. They need explicit lifecycle management from entitlement through occupancy.
**Improvement:** Add a compliance module that tracks each affordability or public-benefit obligation, unit counts or spend commitments, trigger dates, monitoring periods, and the handoff of those obligations into operating teams.
**Acceptance evidence:** Tests that affordability commitments flow into sales or lease releases, condition dashboards with expiring reporting deadlines, and evidence packs showing which commitments were satisfied or remain open.

### 25. Construction handoff basis and design-freeze package
**Justification:** The transition from entitlement/design development to procurement and construction often loses assumptions around approved scope, conditions, utility requirements, and owner commitments. Construction should inherit a governed basis package rather than interpretation by memory.
**Improvement:** Add a construction handoff artifact assembled from `feasibility_model`, `permit_application`, `entitlement`, and `development_milestone`, including approved drawings, condition summaries, utility commitments, allowances, alternates, and unresolved risk items.
**Acceptance evidence:** A generated handoff packet with versioned contents, tests proving stale plan sets cannot be used for contractor release, and signoff workflow records from development, design, and preconstruction leads.

### 26. Contractor and supplier qualification linkage
**Justification:** Long-lead infrastructure and sitework packages depend on prequalified contractors and utilities, and the manifest already consumes `SupplierQualified`. The PBC should convert that event into construction-readiness logic.
**Improvement:** Add supplier qualification projections that link `SupplierQualified` events to bid-package eligibility, contractor shortlist composition, insurance requirements, and which infrastructure scopes can move from planning into procurement.
**Acceptance evidence:** Idempotent event-handler tests for `SupplierQualified`, procurement readiness badges in the workbench, and blocking logic when a required trade package lacks qualified bidders.

### 27. Utility relocation and temporary service handoff
**Justification:** Utility relocation, shutdown windows, temporary power, temporary water, and easement access can derail site mobilization even when major permits are issued. These are handoff-critical infrastructure tasks that deserve first-class tracking.
**Improvement:** Add relocation and temporary-service task groups tied to `development_milestone`, including provider owner, outage windows, prerequisite permits, customer notifications, and commissioning dependencies before vertical construction start.
**Acceptance evidence:** Milestone tests that delay mobilization when relocation scopes are incomplete, plus workbench views showing utility-critical path items and confirmed outage windows.

### 28. Financing covenant and draw-condition traceability
**Justification:** Development milestones are frequently constrained by lender conditions precedent, equity release approvals, and inspection-backed draw packages. These obligations sit between feasibility and construction and cannot stay off-system.
**Improvement:** Add draw-condition and covenant records tied to `development_milestone`, `permit_application`, and the construction handoff package so the team can see which approvals, contracts, and third-party reports are required before funding release.
**Acceptance evidence:** Tests showing a milestone cannot achieve finance-ready status without required lender evidence, and dashboards that distinguish agency readiness from funding readiness.

### 29. For-sale release readiness handoff
**Justification:** For-sale projects need map recordation, budget alignment, product definition, model approvals, disclosure packets, and escrow instructions before units or lots can be released. Sales should receive a clean, governed handoff from development.
**Improvement:** Create a sales-release checklist linked to `development_milestone` and approval obligations covering final map status, disclosure package completeness, pricing authorization, model-home approvals, homeowner association setup, and close-of-escrow dependencies.
**Acceptance evidence:** Release gates that prevent sellable status before required approvals and disclosures are complete, plus signoff records from legal, finance, sales, and development owners.

### 30. Lease-up readiness handoff
**Justification:** Multifamily, industrial, office, and retail projects transition into lease-up only after unit or suite readiness, occupancy clearances, amenity availability, and operating assumptions are aligned. Leasing teams need development data with obligation context.
**Improvement:** Build a lease-up handoff flow tied to `development_milestone` for temporary certificate status, unit turn sequencing, common-area readiness, tenant improvement allowances, delivery assumptions, and lease constraint notes derived from approvals.
**Acceptance evidence:** Lease-release tests that verify occupancy and turnover prerequisites, plus a workbench lane showing which spaces are marketable, deliverable, or blocked by remaining conditions.

### 31. Product mix, pricing, and absorption governance
**Justification:** Sales and leasing handoffs break when product mix or target pricing drifts away from the approved feasibility basis without review. The PBC should police the bridge from underwriting assumptions to go-to-market execution.
**Improvement:** Add controlled release baselines in `feasibility_model` for unit mix, suite mix, pricing bands, absorption assumptions, concessions, and phase-by-phase release strategy, with approval workflows for material deviations.
**Acceptance evidence:** Deviation reports comparing active go-to-market settings against approved underwriting, approval-history logs for changed release assumptions, and tests that force review above configured drift thresholds.

### 32. Obligation clock and deadline engine
**Justification:** Development obligations are time-sensitive: notice windows, appeal periods, commencement deadlines, completion deadlines, recording deadlines, and annual reporting dates all carry default risk. The package needs a single obligation clock instead of scattered reminders.
**Improvement:** Implement a deadline engine spanning `land_option`, `entitlement`, `permit_application`, and `development_milestone`, with trigger events, grace logic, escalation ladders, and calendar-aware due-date calculation.
**Acceptance evidence:** Time-based tests for notice periods and permit expirations, visible countdown widgets in the workbench, and exception records automatically opened when mandatory actions cross threshold windows.

### 33. Insurance, bond, and indemnity compliance
**Justification:** Performance bonds, subdivision bonds, general liability, builder's risk, contractor indemnities, and agency-required certificates often gate permits and closeout. These risk-transfer instruments belong in the project operating record.
**Improvement:** Add compliance records for bonds, insurance, and indemnities with carrier, limit, obligee, expiration, endorsement requirements, and the approvals or milestones they support.
**Acceptance evidence:** Tests showing permit issuance or final acceptance blocked by expired coverage, plus workbench summaries of expiring bonds and missing endorsements by phase.

### 34. Project risk heatmap and kill-criteria framework
**Justification:** Land development is a portfolio of uncertain bets, and teams need explicit criteria for pause, reprice, redesign, or abandon decisions. A risk score alone is too shallow for executive steering.
**Improvement:** Build a multi-axis risk heatmap across land control, entitlement probability, infrastructure burden, capital exposure, schedule confidence, community opposition, and execution readiness, with configurable kill criteria for each project stage.
**Acceptance evidence:** Decision-packet exports showing risk movement over time, tests proving projects can be auto-flagged for executive review when kill criteria are crossed, and board-style summaries rendered in the workbench.

### 35. Schedule critical path and long-lead dependency management
**Justification:** Long-lead permits, utility upgrades, environmental closure, agency hearings, and procurement packages often define the real path to revenue. Development teams need critical-path logic anchored in domain dependencies.
**Improvement:** Extend `development_milestone` with predecessor logic, float, long-lead tags, external-owner dependencies, and probabilistic slippage bands driven by permit and entitlement cycle performance.
**Acceptance evidence:** Critical-path calculations that update when upstream approvals slip, visual path summaries in the workbench, and scenario tests showing how long-lead utility work changes first-vertical-start dates.

### 36. Counterfactual redesign and value-engineering simulator
**Justification:** When costs spike or agencies impose new conditions, teams need to compare redesign moves such as density reduction, product shift, parking change, or phasing revisions before reopening negotiations. The package already advertises simulation capability and should apply it directly to development choices.
**Improvement:** Add governed counterfactual simulations to `feasibility_model` and `entitlement` so users can compare redesign alternatives while preserving the approved baseline, assumption lineage, and approval history for each alternative case.
**Acceptance evidence:** Stored what-if scenarios with non-mutating outputs, variance reports showing economic and approval tradeoffs, and access controls that distinguish exploratory scenarios from approved project strategy.

### 37. Approval denial, appeal, and resubmittal playbooks
**Justification:** Denials, conditions too severe to accept, and politically motivated continuances require structured recovery paths. The PBC should help the team choose whether to appeal, redesign, or re-sequence.
**Improvement:** Add denial and appeal workflows to `zoning_case`, `entitlement`, and `permit_application`, including denial basis, cure options, appeal deadlines, rehearing strategy, and whether the project remains financeable under revised conditions.
**Acceptance evidence:** Case fixtures for denial, continuance, and appeal outcomes, deadline enforcement for appeal filings, and workbench playbooks that present recommended next actions by denial type.

### 38. Parcel analyst cockpit in the workbench
**Justification:** Parcel analysts need survey, title, control, diligence, and acquisition readiness in one place; they should not navigate general-purpose screens to reconstruct site status. A domain cockpit improves both speed and decision quality.
**Improvement:** Create a parcel cockpit in `LandRealEstateDevelopmentWorkbench` focused on parcel stack health, site-control coverage, title cure progress, diligence findings, and acquisition gating outcomes.
**Acceptance evidence:** UI route coverage for parcel cockpit states, persona-driven smoke tests, and evidence that parcel anomalies can be triaged without leaving the workbench.

### 39. Entitlement manager cockpit in the workbench
**Justification:** Entitlement teams need hearing calendars, open conditions, public comments, agency comments, and dependency order in a single operational surface. Generic detail pages hide the sequence logic this role depends on.
**Improvement:** Add an entitlement cockpit that combines `zoning_case`, `entitlement`, and `permit_application` timelines, hearing preparation tasks, decision packets, and post-hearing conditions with role-based actions.
**Acceptance evidence:** Workbench tests covering submission, hearing, continuance, approval, and denial states, plus permission-aware actions for analysts, managers, and approvers.

### 40. Feasibility and investment committee cockpit
**Justification:** Investment and development leaders need one view of value, risk, schedule, and control status before approving more spend. The workbench should produce decision-grade summaries instead of raw records.
**Improvement:** Add a feasibility cockpit that surfaces scenario comparisons, residual land value bridge, risk heatmap, capital milestones, and approval readiness with explicit links back to the assumptions and obligations driving each summary number.
**Acceptance evidence:** Decision-view tests showing traceability from executive metrics back to source assumptions, and exportable committee packets generated from the same governed data shown in the cockpit.

### 41. Approvals and permit operations cockpit
**Justification:** Approval operations are queue-heavy and deadline-sensitive, so reviewers need department-level aging, resubmittal readiness, and blocking comment visibility. A dedicated operations view reduces missed cycles.
**Improvement:** Add an approvals cockpit centered on `permit_application` and `development_milestone` with intake queues, completeness scores, agency comment aging, scheduled hearing dates, and pre-submittal versus official-submittal distinctions.
**Acceptance evidence:** Queue-state tests, aging filters by department and project, and operational dashboards proving users can isolate what is blocking the next permit cycle.

### 42. Infrastructure and handoff cockpit
**Justification:** Utility coordination, offsite work, construction turnover, and sales or lease release readiness span multiple domain tables and roles. The PBC needs a cross-functional handoff view rather than scattered milestone records.
**Improvement:** Create an infrastructure and handoff cockpit that consolidates will-serve status, offsite improvements, relocation tasks, construction handoff packets, and downstream sales or leasing readiness by phase.
**Acceptance evidence:** Role-based workflow tests for infrastructure coordinators and handoff owners, plus workbench summaries that show exactly which unresolved items prevent downstream release.

### 43. Document intake for plats, ordinances, staff reports, and agreements
**Justification:** Land development relies on dense documents such as title reports, ordinances, staff reports, utility letters, plats, and development agreements. The assistant surface should extract usable structured facts instead of offering generic summaries.
**Improvement:** Train `LandRealEstateDevelopmentAssistantPanel` flows to parse these documents into draft parcel facts, approval conditions, deadlines, fee obligations, hearing dates, and infrastructure commitments, with source citations attached to each extracted field.
**Acceptance evidence:** Extraction tests using representative land-development documents, confidence thresholds that force human review when fields are uncertain, and source-span links displayed before any governed mutation is allowed.

### 44. Governed agent flow for due-diligence task generation
**Justification:** Assistant automation is most useful when it turns newly discovered risk into concrete, reviewable work without bypassing governance. Due diligence generates many repetitive but high-stakes follow-up tasks.
**Improvement:** Add an agent flow that proposes diligence tasks from survey, title, environmental, and geotechnical findings, then routes each proposed task through policy checks, owner assignment, due-date calculation, and human confirmation.
**Acceptance evidence:** Permission tests proving the agent can draft but not silently assign or close tasks, preview-and-confirm UI flows, and audit logs showing the source evidence behind each generated task.

### 45. Governed agent flow for negotiation memos and redline impact summaries
**Justification:** Purchase agreement changes, option amendments, and development agreement redlines alter economics and obligation posture quickly. Teams need machine assistance that explains the domain impact of proposed edits before approval.
**Improvement:** Add an agent workflow that compares agreement versions, summarizes changed business terms, maps them to affected parcels or obligations, and drafts negotiation memos for human approval inside the workbench.
**Acceptance evidence:** Version-diff tests for option and development agreement changes, redline impact summaries tied to affected obligations, and explicit approval checkpoints before any term change updates governed records.

### 46. Governed agent flow for approval-packet assembly
**Justification:** Hearing and permit packets require coordinated assembly of forms, plans, narratives, studies, and commitments. An agent can help, but only if it operates within strict completeness and provenance controls.
**Improvement:** Add an approval-packet assembly flow that gathers the current governed plan set, studies, consultant signatures, narratives, and jurisdiction forms, then flags missing pieces and drafts a submission packet for reviewer release.
**Acceptance evidence:** Packet assembly tests with intentionally stale or missing inputs, completeness reports visible before submission approval, and immutable packet manifests stored with the resulting `permit_application` or `entitlement`.

### 47. Cross-PBC event response for policy, customer, and supplier changes
**Justification:** The manifest already declares `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified` as consumed events, but the land-development use cases need explicit domain consequences. External changes should reopen the right risks and not create silent drift.
**Improvement:** Implement idempotent handlers that recalculate approval strategy after policy shifts, refresh buyer or tenant assumptions after customer changes, and update procurement readiness after supplier qualification events.
**Acceptance evidence:** Event-handling tests showing deterministic downstream effects, lineage records linking each reopened exception to the triggering source event, and workbench notifications explaining why project posture changed.

### 48. Audit-proof evidence packs for approvals and handoffs
**Justification:** Real estate development disputes often turn on what the team knew, approved, and handed off at a specific moment. The package should be able to produce tamper-evident evidence packs for key approvals and transitions.
**Improvement:** Generate evidence packs for acquisition approval, entitlement approval, permit submission, construction handoff, and sales or lease release, each containing source documents, decision logs, signoffs, assumptions, and condition status with integrity proofs.
**Acceptance evidence:** Evidence-pack generation tests, reproducible manifests for repeated exports, and validation routines that confirm stored integrity proofs still match the referenced approval package.

### 49. Closeout, stabilization, and archive readiness
**Justification:** The development PBC should not stop at construction turnover; it should also capture when obligations are satisfied, inventory is released, and the project can transition into stabilized operations or archived history. Closeout discipline matters for future claims and lessons learned.
**Improvement:** Add closeout states to `development_milestone` and the obligations register for final acceptance, warranty handoff, reporting completion, fee reconciliation, unsold inventory transfer, stabilized occupancy, and archive eligibility.
**Acceptance evidence:** Tests proving a project cannot archive while open obligations remain, closeout dashboards showing remaining post-completion tasks, and immutable archive snapshots of the final project basis and outcomes.

### 50. Portfolio feedback loop and pattern reuse
**Justification:** Land development organizations improve by learning which jurisdictions, site conditions, approval paths, and handoff practices repeatedly create cost or schedule pain. The PBC should retain those lessons in reusable operational form.
**Improvement:** Add a portfolio feedback layer that mines completed `development_milestone`, `entitlement`, `permit_application`, and risk outcomes to recommend default contingencies, schedule buffers, and approval playbooks for new projects in similar contexts.
**Acceptance evidence:** Pattern summaries derived from completed projects, recommendation cards visible in new-project feasibility workflows, and governance controls requiring review before portfolio-learned defaults become active policy.
