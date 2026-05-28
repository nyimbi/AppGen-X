# Capital Projects Delivery Improvement Backlog

This backlog is hand-curated for the `capital_projects_delivery` PBC and focuses on capital project lifecycle control, project controls depth, delivery workbench usability, governed event boundaries, and release-auditable execution.

## Current Domain Evidence Used

- PBC key: `capital_projects_delivery`.
- Manifest description: megaproject governance, EPC packages, permits, progress, commissioning, risk, and capital delivery controls.
- Core tables: `capital_project`, `epc_package`, `permit_milestone`, `progress_measurement`, `commissioning_system`, `project_risk`, `turnover_package`, `capital_projects_delivery_policy_rule`, `capital_projects_delivery_runtime_parameter`, `capital_projects_delivery_schema_extension`, `capital_projects_delivery_control_assertion`, `capital_projects_delivery_governed_model`.
- Workflows: `capital_projects_delivery_create_capital_project_workflow`, `capital_projects_delivery_record_epc_package_workflow`.
- APIs: `POST /capital-projects`, `POST /epc-packages`, `POST /permit-milestones`, `POST /progress-measurements`, `POST /commissioning-systems`, `GET /capital-projects-delivery-workbench`.
- UI fragments: `CapitalProjectsDeliveryWorkbench`, `CapitalProjectsDeliveryDetail`, `CapitalProjectsDeliveryAssistantPanel`.
- Emitted events: `CapitalProjectsDeliveryCreated`, `CapitalProjectsDeliveryUpdated`, `CapitalProjectsDeliveryApproved`, `CapitalProjectsDeliveryExceptionOpened`.
- Consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Relevant capabilities already declared in the manifest: `capital_project_management`, `workbench`, `agentic_document_instruction_intake`, `ai_agent_task_assistance`, `continuous_release_assurance`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `retry_dead_letter_evidence`, `configuration_workbench`.

### 1. Stage-gate lifecycle aligned to capital project phases
**Justification:** Capital delivery is governed through gated phases such as concept, definition, execution, commissioning, startup, and closeout. A generic status field cannot protect funding decisions, readiness reviews, or turnover timing.
**Improvement:** Introduce a canonical lifecycle for `capital_project` that distinguishes idea, screening, FEL, approved for execution, active construction, mechanical completion, ready for startup, handover complete, and closeout. Require explicit gate approval records, approver roles, exit criteria, and re-baseline rules when a project moves backward.
**Acceptance evidence:** `CapitalProjectsDeliveryDetail` shows gate status, gate dates, and blocked criteria; invalid phase transitions are rejected; approval records support `CapitalProjectsDeliveryApproved` emission with the gate context attached.

### 2. Work breakdown structure as a governed hierarchy
**Justification:** Cost, schedule, progress, and risk only reconcile when they share the same WBS spine. Without a governed WBS, package updates and field progress become impossible to roll up consistently.
**Improvement:** Add WBS hierarchy management to `capital_project` and `epc_package`, including parent-child validation, control account boundaries, discipline tagging, and area/system splits that can support engineering, procurement, construction, and commissioning reporting.
**Acceptance evidence:** Each package and progress record resolves to an approved WBS node; the workbench can roll up by area, discipline, and control account; orphaned or duplicate WBS nodes are surfaced as exceptions.

### 3. Estimate class and basis-of-estimate control
**Justification:** Capital projects evolve from conceptual ranges to control estimates. Teams need to know whether current cost confidence comes from a screening estimate, sanctioned estimate, or field reforecast.
**Improvement:** Extend `capital_project` with estimate class, estimating basis, quantity source, market check date, contingency philosophy, and assumption lineage. Keep revisions time-bound so the sanctioned basis remains visible after execution changes begin.
**Acceptance evidence:** Estimate history appears in `CapitalProjectsDeliveryDetail`; every revised estimate references its predecessor and justification; release evidence includes the sanctioned estimate basis and latest approved forecast.

### 4. Baseline schedule governance with critical path traceability
**Justification:** A capital project needs more than milestone dates. Delivery leadership must understand critical path movement, float erosion, and near-critical work that can consume contingency.
**Improvement:** Add schedule baseline records to `capital_project` with logic revision history, baseline issue date, total float thresholds, and milestone ownership. Record when an `epc_package` or permit change alters the critical path.
**Acceptance evidence:** The workbench highlights current critical and near-critical paths; schedule variance is tied to a named baseline; approval is required before a new baseline replaces the prior control schedule.

### 5. Milestone library for engineering, procurement, construction, and startup
**Justification:** Capital delivery cannot be managed through ad hoc milestones. Teams need a consistent milestone library spanning design, long-lead procurement, civil, mechanical, electrical, pre-commissioning, commissioning, and handover.
**Improvement:** Expand `permit_milestone` and related scheduling constructs to support standardized milestone types, predecessor relationships, success criteria, hold-point flags, and phase ownership across the full project lifecycle.
**Acceptance evidence:** Milestones can be filtered by phase and owner; every key turnover and startup milestone has explicit entry criteria; late milestones raise `CapitalProjectsDeliveryExceptionOpened` with the impacted path identified.

### 6. Package-level commitment, accrual, and forecast control
**Justification:** Capital project cost control depends on seeing budget, committed value, accruals, actuals, forecast-to-complete, and estimate-at-completion together at the package level.
**Improvement:** Extend `epc_package` and `capital_project` controls to capture original budget, approved budget, awarded value, pending change exposure, accrual timing, forecast final cost, and management reserve usage with clear package ownership.
**Acceptance evidence:** `CapitalProjectsDeliveryWorkbench` can display package cost status by awarded, forecast, and variance views; cost movements require dated explanations; release evidence includes a control account level cost rollup.

### 7. Earned progress rules tied to measurable work
**Justification:** Physical progress in capital construction is often overstated when percentage complete is entered without quantity logic. Progress should be earned against measurable rules, not informal opinion.
**Improvement:** Strengthen `progress_measurement` to support installed quantities, earned quantities, weighted milestones, rules of credit, and discipline-specific progress methods for engineering deliverables, procurement, and field installation.
**Acceptance evidence:** Each progress record shows its earning rule and quantity basis; unsupported manual percentages are blocked; workbench rollups can distinguish weighted progress from direct quantity progress.

### 8. Schedule and cost performance index tracking
**Justification:** Delivery leadership needs early warning, not just raw variance. CPI and SPI style indicators help expose underperformance before monthly review packs are compiled.
**Improvement:** Add analytic rollups for planned value, earned value, actual cost, SPI, CPI, and trend direction at project, area, and package level using existing `capital_projects_delivery_workbench_metric` support.
**Acceptance evidence:** The workbench provides indexed cost and schedule trend cards; thresholds are configurable through `capital_projects_delivery_runtime_parameter`; trend breaches create explainable exceptions rather than silent metric drift.

### 9. Change order pipeline from field cause to approved recovery plan
**Justification:** Change orders are a primary source of capital project overruns and disputes. The PBC should show when a change starts, who owns it, how it affects time and cost, and whether funding is authorized.
**Improvement:** Add change order tracking to `epc_package` and `capital_project` with cause code, originating event, contractor notice date, estimated impact, approved impact, funding status, and schedule entitlement assessment.
**Acceptance evidence:** Every material package change appears with pending, quoted, approved, rejected, or disputed state; time and cost impacts are rolled into package forecast only after approval; the workbench separates pending exposure from approved change.

### 10. Early warning and claims avoidance register
**Justification:** Waiting for formal claims is too late. Capital teams need an auditable early warning register to capture emerging contractor, owner, and interface issues before they harden into disputes.
**Improvement:** Add an early warning workflow linked to `epc_package` and `project_risk`, capturing event date, notifying party, probable entitlement path, mitigation action, and expected cost or schedule consequence.
**Acceptance evidence:** Open early warnings appear beside related change orders and risks; aging warnings trigger exceptions; closed warnings preserve disposition and whether they converted into formal claims.

### 11. Risk register with quantitative exposure and trigger logic
**Justification:** Capital project risk management needs more than high-medium-low scoring. Teams need quantified exposure, trigger conditions, mitigation maturity, and owner accountability.
**Improvement:** Extend `project_risk` with probability distributions, time and cost ranges, trigger events, mitigation due dates, owner role, residual risk state, and quantitative rollup into project contingency views.
**Acceptance evidence:** Risks show current and residual exposure; triggered risks automatically escalate; the workbench can sort by cost risk, schedule risk, and mitigation lateness.

### 12. Opportunity management alongside threats
**Justification:** Delivery controls should preserve upside as well as defend against downside. Recovery ideas, productivity gains, and packaging changes are often lost when the system only models threats.
**Improvement:** Add opportunity handling to `project_risk` or a tightly related governed model so beneficial options can be logged, quantified, approved, and tracked without being mixed into threat-only reporting.
**Acceptance evidence:** Opportunity items have expected benefit, confidence, and owner; approved opportunities appear in forecast commentary; the workbench can distinguish upside capture from threat reduction.

### 13. Permit dependency matrix by authority and workfront
**Justification:** Permit slippage frequently blocks mobilization, energization, heavy lifts, or environmental releases. A capital project needs permit visibility at the workfront level, not only a flat permit list.
**Improvement:** Expand `permit_milestone` to store authority, permit type, submission date, review cycle, resubmission count, tied workfront, expiry, and downstream work constraint so field execution knows exactly what is blocked.
**Acceptance evidence:** Permit views can show upcoming expiries and blocked workfronts; resubmission cycles are visible; permit delays can be traced to affected milestones and packages.

### 14. Long-lead equipment tracking through procurement and site readiness
**Justification:** Major equipment often controls the project finish date. Delivery controls need to show when design release, purchase, manufacturing, inspection, shipment, and site readiness fall out of sync.
**Improvement:** Add long-lead item tracking under `epc_package` with manufacturing milestones, inspection releases, logistics status, receiving dates, preservation requirements, and installation readiness checks.
**Acceptance evidence:** Long-lead items can be viewed on the same path as package milestones; late manufacturing or shipment events flag critical-path risk; receiving without site readiness creates a visible storage exposure exception.

### 15. Contractor package readiness before notice to proceed
**Justification:** Package award does not mean package readiness. Scope gaps, missing drawings, poor interfaces, or incomplete access conditions create immediate downstream loss.
**Improvement:** Add a package readiness checklist to `epc_package` covering scope freeze, IFC maturity, material strategy, access handoff, temporary facilities, owner-furnished items, and interface agreement before field execution starts.
**Acceptance evidence:** Packages cannot move into active field execution without readiness signoff; blocked checklist items remain visible in the workbench; readiness findings link to risks and early warnings.

### 16. Field constraint log tied to package and area
**Justification:** Construction performance is shaped by access, scaffolding, craft availability, weather, vendor support, and preceding work. These constraints need structured capture to explain lost productivity and resequencing.
**Improvement:** Introduce a constraint register linked to `epc_package`, WBS area, and `progress_measurement`, with start date, expected release, responsible party, and quantified impact on crews or milestones.
**Acceptance evidence:** Constraint aging appears next to package progress; repeated unresolved constraints raise escalation; closed constraints retain evidence of how the blockage was removed.

### 17. Interface management across EPC packages
**Justification:** Capital projects fail at interfaces: battery limits, tie-ins, utility dependencies, and vendor-owner-contractor handoffs. These are not secondary details; they are delivery-critical boundaries.
**Improvement:** Add interface records between `epc_package` entities with interface type, required deliverable, due date, owning side, receiving side, and acceptance evidence so unresolved boundaries are actively managed.
**Acceptance evidence:** Each interface has a clear owner and due date; late interfaces are visible in package health views; handoff acceptance closes the interface with dated evidence.

### 18. Mechanical completion by system and subsystem
**Justification:** Commissioning starts from systems, not from package totals. Mechanical completion should be measured at the system and subsystem level so turnover sequencing is credible.
**Improvement:** Extend `commissioning_system` and `turnover_package` to define systems, subsystems, completion boundaries, completion criteria, and package-to-system mappings for construction completion.
**Acceptance evidence:** Mechanical completion can be reported by system; system completion is impossible unless mapped construction work is complete; turnover packages show which systems they enable.

### 19. Punch list severity and closeout thresholds
**Justification:** Projects often declare mechanical completion or handover while critical punch items remain unresolved. Severity and closure standards must be explicit.
**Improvement:** Add punch list severity, system impact, responsible party, due date, and closeout rules tied to `commissioning_system` and `turnover_package`, distinguishing A-punch, B-punch, and cosmetic items.
**Acceptance evidence:** System readiness views show punch counts by severity; critical punch items block readiness; closure evidence is attached to each resolved item.

### 20. Pre-commissioning activity tracking
**Justification:** Cleaning, flushing, loop checks, calibration, and pressure testing are often the hidden drivers of startup readiness. They need their own governed delivery visibility.
**Improvement:** Add pre-commissioning activities beneath `commissioning_system` with test type, procedure reference, planned date, actual completion, fail-retest state, and dependency on construction turnover.
**Acceptance evidence:** Pre-commissioning completion is visible per system; failed activities remain open until passed; the assistant panel can surface all prerequisite gaps before commissioning starts.

### 21. Commissioning sequence and startup window control
**Justification:** Startup windows are narrow and interdependent. Losing a commissioning sequence can trigger major rework, resource standby cost, or commercial delay.
**Improvement:** Model commissioning sequence dependencies across `commissioning_system` entities, including utility availability, vendor attendance, energization approvals, performance test windows, and startup permits.
**Acceptance evidence:** The workbench can display commissioning sequences and blockers; delayed prerequisite utilities or permits automatically flag downstream startup impact; readiness reviews show unmet sequence prerequisites.

### 22. Handover dossier completeness before owner acceptance
**Justification:** Owner handover depends on more than physical completion. As-built drawings, test packs, warranties, spares, training, and operating procedures must be complete and traceable.
**Improvement:** Expand `turnover_package` to carry dossier requirements, document completeness, approved deviations, training completion, spare parts transfer, and asset data handoff status before final acceptance.
**Acceptance evidence:** Handover packages cannot be marked complete without dossier completeness; missing owner documents are visible by package; release evidence includes a turnover completeness snapshot.

### 23. Defect liability and post-handover obligation tracking
**Justification:** Delivery control should continue through the defect liability period so unresolved issues, retention, and warranty obligations are not lost after initial handover.
**Improvement:** Add post-handover obligation tracking to `turnover_package` and `epc_package`, including warranty start, warranty end, retention release, defects outstanding, and final close certificate readiness.
**Acceptance evidence:** Warranty obligations remain queryable after handover; retention release is blocked by unresolved critical defects; closeout views show obligations remaining by package.

### 24. Funding approval and appropriation checkpoints
**Justification:** Capital projects often move through staged funding. Execution should not outrun authorized spend, and forecast changes should show when new appropriation is required.
**Improvement:** Add funding approval checkpoints to `capital_project`, including approved amount, committed amount, forecast overrun, next approval threshold, and submission package status for governance review.
**Acceptance evidence:** The workbench warns when committed plus pending exposure exceeds authorized funding; gate reviews can show funding sufficiency; forecast overruns record the date approval was requested and granted.

### 25. Contingency drawdown discipline
**Justification:** Contingency is frequently consumed without enough transparency. Delivery teams need to know whether drawdown was driven by risk realization, estimate maturity, or scope change.
**Improvement:** Add contingency registers on `capital_project` with source category, approved release, remaining balance, linked risk or change reference, and governance notes on why funds were consumed.
**Acceptance evidence:** Contingency usage can be traced to approved events; drawdown without linked justification is blocked; monthly evidence shows opening, used, and remaining contingency by category.

### 26. Resource and productivity risk tracking
**Justification:** Craft shortages, labor instability, and poor crew productivity materially affect schedule recovery plans. These conditions should be visible before milestone slips become irreversible.
**Improvement:** Extend `project_risk` and `progress_measurement` to capture labor productivity assumptions, crew loading, shift pattern changes, camp or transport constraints, and recovery productivity expectations.
**Acceptance evidence:** Productivity variance can be seen by package or area; resource-driven risks are linked to forecast schedule impact; recovery plans show the productivity delta they assume.

### 27. Weather and seasonal disruption modeling
**Justification:** Weather exposure is a normal part of field execution and must be separated from self-inflicted delay to support realistic forecasts and fair entitlement discussions.
**Improvement:** Add weather delay classification to `project_risk`, package progress commentary, and schedule exception logic so the project can compare actual seasonal disruption against planned weather calendars.
**Acceptance evidence:** Weather-tagged delays are reported separately from controllable slippage; the workbench shows cumulative weather impact by period; entitlement reviews can trace relevant days and workfronts.

### 28. Quality hold-point and release boundary management
**Justification:** Work cannot progress safely through fabrication, installation, and turnover unless inspections and hold points are released in the right order.
**Improvement:** Add quality release boundaries to `epc_package`, `permit_milestone`, and `commissioning_system` so inspection release, test acceptance, and construction release status are visible without collapsing quality records into generic comments.
**Acceptance evidence:** Package and system readiness views show outstanding hold points; blocked work is tied to the exact release boundary; accepted releases clear the corresponding execution block.

### 29. Construction sequence of work visualization in the workbench
**Justification:** Delivery teams need to see how packages progress through areas and systems, not just read tables. Visual sequence context is essential for resequencing and recovery reviews.
**Improvement:** Upgrade `CapitalProjectsDeliveryWorkbench` to show a phase-aware sequence of work view by WBS area, package, and system with current blockers, late predecessors, and nearing turnover boundaries.
**Acceptance evidence:** Users can pivot between package, area, and system views; blocked sequences are visually distinct; the detail panel explains the predecessor or permit causing the block.

### 30. Monthly project review pack generation
**Justification:** Capital projects live on recurring governance packs. Preparing them manually wastes time and introduces inconsistency across cost, schedule, risk, and commissioning narratives.
**Improvement:** Use `continuous_release_assurance` and governed reporting to generate a monthly review pack from `capital_project`, `epc_package`, `project_risk`, `progress_measurement`, and `turnover_package` with a locked evidence snapshot.
**Acceptance evidence:** A review pack can be reproduced for a given cutoff date; the evidence snapshot lists exact record versions used; late adjustments after pack freeze are clearly marked as post-cutoff.

### 31. Release evidence tailored to capital project readiness
**Justification:** Release evidence should prove the PBC is safe to operate for live capital delivery, not just that routes respond. Evidence must show business-critical readiness.
**Improvement:** Expand `RELEASE_EVIDENCE.md` expectations for `capital_projects_delivery` to include lifecycle gates, WBS rollups, change order flow, permit dependency handling, commissioning readiness, and handover dossier completeness.
**Acceptance evidence:** Release evidence includes representative scenarios for sanction, field execution, startup readiness, and handover; scenario outputs reference actual PBC events, APIs, and workbench states.

### 32. Assistant skills for project controls roles
**Justification:** Capital delivery teams work in specialized roles such as project controls lead, scheduler, cost engineer, permit coordinator, package engineer, and commissioning manager. The assistant should support these roles directly.
**Improvement:** Define role-scoped `ai_agent_task_assistance` behaviors for schedule diagnostics, forecast narrative drafting, permit action lists, package readiness summaries, and turnover gap analysis within `CapitalProjectsDeliveryAssistantPanel`.
**Acceptance evidence:** The assistant panel offers role-specific prompts and task outputs; generated actions stay within PBC boundaries; approval is required before agent-generated updates can change governed records.

### 33. Document instruction intake for contractor and owner artifacts
**Justification:** Capital delivery decisions often start in contractor letters, field memos, permit notices, and readiness checklists. The intake path should convert those artifacts into structured tasks and proposed updates.
**Improvement:** Strengthen `agentic_document_instruction_intake` so notices, permits, meeting minutes, and startup procedures can produce structured proposals for `epc_package`, `permit_milestone`, `project_risk`, and `turnover_package`.
**Acceptance evidence:** Intake previews show extracted dates, responsible parties, and affected packages; uncertain fields are flagged for review; accepted proposals produce a dated audit trail linking source artifact and final mutation.

### 34. Event boundary refinement for lifecycle and control decisions
**Justification:** The current emitted events are too coarse for rich downstream consumption. Capital delivery needs downstream consumers to know whether a project was sanctioned, rebaselined, blocked, or handed over.
**Improvement:** Refine event payloads for `CapitalProjectsDeliveryCreated`, `CapitalProjectsDeliveryUpdated`, `CapitalProjectsDeliveryApproved`, and `CapitalProjectsDeliveryExceptionOpened` so they carry lifecycle stage, affected object type, project key, WBS scope, and package or system references.
**Acceptance evidence:** Event contracts show distinct payload fields for project, package, permit, risk, and turnover contexts; subscribers can filter on lifecycle or workfront scope without reading opaque blobs.

### 35. Consumed event handling with explicit capital project effects
**Justification:** `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` should have clear operational meaning in the capital project domain. Otherwise the inbox becomes an audit artifact instead of a working control surface.
**Improvement:** Define explicit handlers for each consumed event so policy updates can re-evaluate active controls, sealed audits can freeze review-pack evidence, and KPI changes can update package or project health thresholds.
**Acceptance evidence:** Consumed event processing shows the records re-evaluated and the resulting actions; no-op events are logged as such; replaying the inbox produces the same project control state.

### 36. API boundary hardening around workbench and mutation routes
**Justification:** Capital project operators need confidence that each route has a clear purpose and cannot be used to bypass business gates. API ambiguity usually leads to hidden side channels and inconsistent control application.
**Improvement:** Clarify route responsibilities for `POST /capital-projects`, `POST /epc-packages`, `POST /permit-milestones`, `POST /progress-measurements`, `POST /commissioning-systems`, and `GET /capital-projects-delivery-workbench`, including required approvals, immutable fields, and versioning expectations.
**Acceptance evidence:** Route contracts distinguish create, revise, approve, and query behaviors; attempting to change sanctioned fields through the wrong boundary is rejected; the workbench only reads from governed projections.

### 37. Idempotent handling for repeated field and document updates
**Justification:** Capital delivery updates often arrive repeatedly from integrations, spreadsheets, and document ingestion. Duplicate handling must be safe or package and progress histories become unreliable.
**Improvement:** Use `idempotent_handlers` with domain-specific keys for package updates, permit revisions, progress imports, and commissioning test results so retries do not create duplicate operational facts.
**Acceptance evidence:** Replaying the same update leaves one effective mutation; duplicate attempts are visible in support diagnostics; downstream metrics remain stable after retry storms.

### 38. Dead-letter triage for operational exceptions
**Justification:** A dead-letter queue that nobody can interpret is operationally useless. Capital project support staff need a domain view of what failed, why it failed, and what business process is now at risk.
**Improvement:** Build `retry_dead_letter_evidence` views that classify failures by project, package, permit, system, and event type, and provide recovery guidance grounded in capital delivery semantics.
**Acceptance evidence:** Dead-letter items can be filtered by object type and operational severity; retry decisions preserve history; workbench support views show which project controls are currently degraded by message failure.

### 39. Configuration workbench for project controls calendars and thresholds
**Justification:** Working day calendars, reporting cutoffs, float alarms, and escalation thresholds vary across projects and regions. Operators need a safe way to configure them without code changes.
**Improvement:** Expand `configuration_workbench` and `capital_projects_delivery_runtime_parameter` to manage holiday calendars, reporting periods, float thresholds, late action SLAs, and commissioning readiness tolerances per tenant or project type.
**Acceptance evidence:** Configuration changes are versioned and approved; affected analytics show when a new threshold took effect; existing data is re-evaluated deterministically after approved parameter changes.

### 40. Policy rule library for capital delivery controls
**Justification:** Capital project controls rely on repeatable governance rules such as sanction before award, permit before workfront release, and dossier completeness before handover. These should be explicit and testable.
**Improvement:** Populate `capital_projects_delivery_policy_rule` with domain rules covering package readiness, funding sufficiency, permit gating, critical punch thresholds, and startup prerequisites, with severity and waiver support.
**Acceptance evidence:** Policy simulations show pass, fail, and waived outcomes; waived rules require named approvers and justification; exceptions reference the exact rule violated.

### 41. Control assertions for monthly and gate review readiness
**Justification:** Governance reviews should not rely on someone remembering whether data is complete. Control assertions can continuously prove whether the project is ready for formal review.
**Improvement:** Expand `capital_projects_delivery_control_assertion` to check stale forecasts, unmapped WBS records, packages without readiness signoff, expired permits, unresolved critical punch items, and missing handover documents.
**Acceptance evidence:** Control assertions run on schedule and on demand; failing assertions are visible before review pack freeze; evidence can be attached directly to gate approval records.

### 42. Schema extension governance for owner-specific fields
**Justification:** Capital projects commonly need owner-specific metadata such as facility codes, funding lines, or regional permit attributes. Those additions must not destabilize the shared control model.
**Improvement:** Use `capital_projects_delivery_schema_extension` to register owner-specific fields with declared purpose, owning team, projection impact, validation rules, and rollout plan before they appear in live forms or APIs.
**Acceptance evidence:** Every extension has approval history and compatibility notes; the workbench identifies extension-derived fields; unsupported extensions cannot leak into emitted events or standard analytics by accident.

### 43. Governed model definitions for package and system semantics
**Justification:** Terms such as package complete, mechanical complete, ready for startup, and handover complete often vary across organizations. The PBC should make those semantics explicit instead of leaving them to tribal interpretation.
**Improvement:** Use `capital_projects_delivery_governed_model` to define canonical domain objects and status semantics for packages, systems, permits, and turnover so downstream analytics and agents use the same vocabulary.
**Acceptance evidence:** Model definitions are queryable from the detail view; analytics can cite the exact governed definition behind a status; agent outputs use canonical terms rather than free-form synonyms.

### 44. Multi-project portfolio rollup with drill-back to delivery drivers
**Justification:** Capital leaders often oversee multiple projects. Portfolio views are only useful if they preserve the ability to drill from top-level red status back to the specific package, permit, or system driving it.
**Improvement:** Add portfolio rollups on top of `capital_project_management` so executives can compare sanctioned budget, forecast variance, milestone health, permit exposure, and startup readiness across projects.
**Acceptance evidence:** Portfolio cards link directly to project, package, and system detail; red portfolio indicators explain their underlying driver; drill-back stays within governed projections rather than ad hoc queries.

### 45. Cross-PBC boundary map for adjacent delivery domains
**Justification:** Capital project delivery touches procurement, document control, maintenance readiness, and financial governance. The PBC should document what it owns and what it only references.
**Improvement:** Define an explicit boundary map in the backlog and downstream implementation notes for package control, permit control, commissioning, turnover, and cost-schedule analytics, including which adjacent capabilities are consumed through events or APIs rather than direct mutation.
**Acceptance evidence:** Boundary notes are reflected in service and schema contracts; outbound and inbound events show which domain owns the source truth; the workbench labels referenced data as external when it is not PBC-owned.

### 46. Startup readiness review workflow
**Justification:** Startup readiness is a formal decision point that combines construction completion, commissioning results, permits, operations training, and risk acceptance. It deserves its own governed workflow.
**Improvement:** Add a startup readiness workflow on `commissioning_system`, `turnover_package`, and `capital_project` that assembles prerequisites, unresolved risks, temporary deviations, and final authorization to introduce energy or feed.
**Acceptance evidence:** Readiness reviews show complete, blocked, or conditional status with explicit blockers; approval emits a lifecycle-aware event; conditional approvals retain follow-up obligations and due dates.

### 47. Handover to operations with training and spare-parts verification
**Justification:** Owner acceptance is fragile when operations teams are not trained or critical spares are missing. Handover should prove operational preparedness, not just construction completion.
**Improvement:** Extend `turnover_package` to confirm operator training, operating procedures, maintenance task seeds, spare-part availability, and vendor support arrangements before the package reaches accepted handover.
**Acceptance evidence:** Handover detail shows training completion percentages and missing spares; accepted turnover requires all mandatory preparedness fields; post-handover defects can be traced back to preparedness gaps.

### 48. Live project onboarding and baseline migration discipline
**Justification:** Many projects will enter the PBC midstream, with partial history and imperfect baseline data. Onboarding needs structure or the system will start from a compromised control position.
**Improvement:** Define onboarding routines for `capital_project`, `epc_package`, `permit_milestone`, `progress_measurement`, and `project_risk` that distinguish imported baseline facts, open exceptions, and unknown historical gaps.
**Acceptance evidence:** Imported projects carry an onboarding status and data confidence note; missing historical fields are explicit rather than silently defaulted; initial release evidence includes migration reconciliation results.

### 49. Continuous release assurance against domain scenarios
**Justification:** For this PBC, release safety depends on proving realistic delivery scenarios, not only route tests. The domain needs scenario assurance around sanction, package control, commissioning, and handover.
**Improvement:** Focus `continuous_release_assurance` on scenario suites covering gate approval, WBS rollup, long-lead slip, permit expiry, change order approval, system completion, startup readiness, and handover dossier closure.
**Acceptance evidence:** Scenario runs produce pass-fail evidence with referenced APIs, events, and workbench states; failed scenarios block release signoff; evidence remains reproducible for the same code and seed state.

### 50. Capital project closeout knowledge capture
**Justification:** Closeout is the point where delivery knowledge is either preserved or lost. The PBC should leave behind auditable lessons on estimate drift, schedule recovery, package performance, and commissioning bottlenecks.
**Improvement:** Add structured closeout capture to `capital_project` with final cost versus sanctioned estimate, milestone slippage root causes, change concentration by package, startup bottlenecks, handover defects, and reusable lessons for future projects.
**Acceptance evidence:** Closeout cannot finish without a lessons summary and variance narrative; portfolio views can compare lessons across completed projects; future project teams can search prior closeout findings by phase, discipline, and package type.
