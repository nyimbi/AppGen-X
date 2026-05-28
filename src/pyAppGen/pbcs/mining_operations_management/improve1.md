# Mining Operations Management Improvement Backlog

## Current Domain Evidence Used

- PBC key: `mining_operations_management`.
- Manifest description: mine plans, extraction, haulage, fleet, ore quality, safety, stockpiles, and rehabilitation operations.
- Current APIs in manifest: `POST /mine-plans`, `POST /pit-blocks`, `POST /extraction-shifts`, `POST /haulage-cycles`, `POST /fleet-assets`, `GET /mining-operations-management-workbench`.
- Current tables in manifest: `mine_plan`, `pit_block`, `extraction_shift`, `haulage_cycle`, `fleet_asset`, `ore_quality`, `stockpile`, `mining_operations_management_policy_rule`, `mining_operations_management_runtime_parameter`, `mining_operations_management_schema_extension`, `mining_operations_management_control_assertion`, `mining_operations_management_governed_model`.
- Current emitted events in manifest: `MiningOperationsManagementCreated`, `MiningOperationsManagementUpdated`, `MiningOperationsManagementApproved`, `MiningOperationsManagementExceptionOpened`.
- Current consumed events in manifest: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Current UI fragments in manifest: `MiningOperationsManagementWorkbench`, `MiningOperationsManagementDetail`, `MiningOperationsManagementAssistantPanel`.
- Current workflows in manifest: `mining_operations_management_create_mine_plan_workflow` and `mining_operations_management_record_pit_block_workflow`.

### 1. Hierarchical mine plan structure

**Justification:** Open-pit benches and underground stopes must roll up into a planning hierarchy that production, geology, and plant teams can reconcile without manual spreadsheets.

**Improvement:** Extend the planning model so one mine plan can contain period versions, pit phases, pushbacks, benches, stopes, drawpoints, and mining blocks with explicit parent-child relationships, sequencing windows, planned tonnage, planned grade, stripping ratio, and ore destination.

**Acceptance evidence:** Regression tests prove hierarchy creation and edits through the mine-plan workflow, the workbench shows expandable plan trees by phase and mining area, and release evidence includes a sample plan pack with pit and stope rollups.

### 2. Spatial identity for pits, benches, stopes, and drawpoints

**Justification:** Dispatching and ore control break down when operational records do not point to the exact mining location where material was drilled, blasted, loaded, or hauled.

**Improvement:** Add canonical location identifiers and boundary metadata for pit, bench, stope, drawpoint, ore drive, and loading point records, including mine coordinate reference, mining method, active status, and linkage to the owning mine plan period.

**Acceptance evidence:** Validation fixtures reject duplicated or ambiguous location IDs, UI detail pages show location lineage from plan to execution record, and release evidence includes boundary examples for both pit and underground layouts.

### 3. Drill pattern planning

**Justification:** Drill-and-blast performance affects fragmentation, dilution, loader productivity, and downstream crusher throughput, so it needs first-class backlog coverage.

**Improvement:** Introduce drill pattern entities and workflow steps for hole count, hole depth, burden, spacing, sub-drill, explosive type, initiation sequence, powder factor, target fragmentation class, and shift readiness status.

**Acceptance evidence:** Contract tests cover drill pattern submission and approval, the workbench exposes upcoming and overdue patterns by bench or stope, and release evidence includes a signed-off drill pattern example with design assumptions.

### 4. Blast execution and blast clearance control

**Justification:** A mine cannot safely execute blasts without verifying exclusion zones, blast windows, pre-clearance, and post-blast release decisions.

**Improvement:** Add blast execution records tied to drill patterns with blast time, clearance confirmation, exclusion zone checks, misfire flags, re-entry approval, and post-blast inspection outcome.

**Acceptance evidence:** Tests show that blast completion is blocked until clearance conditions are met, UI badges expose blast status and re-entry hold points, and release evidence includes an auditable blast packet from plan through release.

### 5. Dig block and ore parcel definition

**Justification:** Mine planning alone is too coarse for daily mining because equipment operators and ore control geologists need diggable ore parcels with clear destination rules.

**Improvement:** Add dig block or ore parcel records beneath pit blocks and stopes with expected tonnes, expected grade bands, lithology, destination policy, dilution risk, and mining sequence priority.

**Acceptance evidence:** Workflow tests verify ore parcel creation under approved plan structures, the detail view displays parcel-level destination rules, and release evidence includes parcel snapshots used in a daily production cycle.

### 6. Shift target planning

**Justification:** Supervisors need a governed way to convert monthly mine plans into shift-level targets for tonnes, metres, blasts, and equipment hours.

**Improvement:** Add shift target objects for day and night shifts with target ore tonnes, waste tonnes, metres drilled, blasts due, truck loads, plant feed nomination, and critical constraints by mining area.

**Acceptance evidence:** Tests verify target versioning and approval, the workbench compares target versus actual per shift, and release evidence contains one daily target board generated from an approved plan.

### 7. Haul route catalog and route constraints

**Justification:** Haul cycles are not meaningful without route context such as ramp status, one-way sections, queue limits, and maximum gross vehicle mass restrictions.

**Improvement:** Add haul route definitions with from-point, to-point, ramp segment, distance, gradient band, expected cycle time, traffic direction rule, and temporary closure state.

**Acceptance evidence:** Route validation tests prevent impossible route assignments, dispatch UI shows active and blocked routes, and release evidence includes a route-status example affecting daily cycle plans.

### 8. Dispatch assignment engine

**Justification:** Mining operations depend on the daily pairing of loaders, trucks, operators, and active loading points, not just recorded haulage cycles after the fact.

**Improvement:** Add dispatch assignment capabilities that allocate trucks to loaders or stopes, track dispatch board state, capture reassignment reasons, and enforce equipment compatibility by loading point, payload class, and route condition.

**Acceptance evidence:** Scenario tests cover dispatching, reassignment, and blocked allocations, the workbench shows a live dispatch board view, and release evidence includes an assignment log for one full shift.

### 9. Equipment boundary and capability model

**Justification:** Loader, truck, drill, and ancillary assets operate under boundary rules that determine where they may work and what material classes they can handle.

**Improvement:** Extend fleet asset coverage to include equipment class, payload band, approved mining areas, operator certification requirements, fuel type, communication availability, and whether the unit is cleared for pit, underground, or dual-use operation.

**Acceptance evidence:** Tests reject dispatches that cross equipment boundary rules, UI screens show asset capability cards, and release evidence includes a blocked-assignment example caused by an equipment boundary violation.

### 10. Ore control sampling workflow

**Justification:** Grade control depends on sample points, assay turnaround, and local ore-waste decisions that must stay linked to the material that is actually mined.

**Improvement:** Introduce ore control sample records tied to dig blocks, blast polygons, and stopes with sample type, interval, assay status, provisional grade, final grade, and sampling confidence.

**Acceptance evidence:** Assay workflow tests prove status changes and late-result corrections, ore control screens show pending and final samples, and release evidence includes one ore-control chain from sample to dispatch destination change.

### 11. Ore-waste boundary decisions

**Justification:** Mining loses value when ore-waste boundaries are changed informally without traceable grade reasoning or supervisor approval.

**Improvement:** Add boundary decision records that capture dig-line adjustments, visual geology observations, assay references, grade thresholds, destination changes, and who approved the ore or waste call.

**Acceptance evidence:** Tests enforce approval before destination changes take effect, the UI displays before-and-after boundary calls, and release evidence contains a signed boundary adjustment example with grade rationale.

### 12. Dilution and ore loss accounting

**Justification:** Reconciliation is incomplete unless the system can explain where planned ore was lost and where unplanned waste dilution entered the material stream.

**Improvement:** Add dilution and ore-loss events linked to dig blocks, stopes, blasts, and haul cycles, with causal categories such as overbreak, underbreak, backfill contamination, poor dig compliance, and sampling uncertainty.

**Acceptance evidence:** Analytics tests roll dilution and ore-loss measures into reconciliation reports, the workbench shows variance drivers by area, and release evidence includes one reconciled month with documented loss categories.

### 13. Stockpile genealogy

**Justification:** ROM, low-grade, high-grade, and blending stockpiles need genealogy so plant feed decisions can be defended after multiple reclaim and topping events.

**Improvement:** Extend stockpile handling to track build, top-up, reclaim, depletion, moisture adjustment, and source lineage from pit block, stope, or ore parcel into every stockpile movement.

**Acceptance evidence:** Tests prove lineage preservation across multiple stockpile movements, UI views show stockpile genealogy timelines, and release evidence includes a stockpile mass-balance example.

### 14. Stockpile quality estimation

**Justification:** Plant feed planning fails if stockpile tonnes and grade are treated as static values rather than continuously updated estimates with confidence bounds.

**Improvement:** Add estimated tonnes, estimated grade, moisture, density factor, confidence class, last survey date, and last sample date to stockpiles with governed recalculation rules after each movement or survey adjustment.

**Acceptance evidence:** Recalculation tests cover stockpile build and reclaim events, the workbench highlights stale estimates, and release evidence includes before-and-after quality estimates after a survey correction.

### 15. Plant feed nomination and blend planning

**Justification:** The mine-to-plant handoff is where planning, ore control, and stockpile management converge, so it must be explicit in the backlog.

**Improvement:** Add plant feed nominations by shift and day with required tonnes, target grade band, blend components, stockpile draw plan, crusher or mill destination, and fallback feed options if a source becomes unavailable.

**Acceptance evidence:** Tests prove that nominations reference valid available material, UI panels show planned versus achieved plant feed, and release evidence includes one blend plan with contingency options.

### 16. Crusher and ROM pad queue visibility

**Justification:** Dispatch decisions must account for queue buildup at crushers, ore passes, ROM pads, and tipping points to avoid hidden delays and rehandle.

**Improvement:** Add queue state records for crusher pockets, ROM pads, ore passes, and tipping locations with queue length, wait time band, destination availability, and diversion rules.

**Acceptance evidence:** UI tests confirm queue indicators on dispatch and haulage screens, projections show queue-driven delay attribution, and release evidence includes one shift where dispatch changed because of crusher congestion.

### 17. Payload and tonnage adjustment governance

**Justification:** Reconciliation becomes unreliable when survey tonnes, truck payload system tonnes, and belt tonnes drift without a controlled adjustment process.

**Improvement:** Add tonnage adjustment records that compare payload system, truck count, survey, and plant receipt measures, including approved adjustment method, effective period, and material classes affected.

**Acceptance evidence:** Tests cover approval and rollback of tonnage adjustments, reports show adjusted and raw values side by side, and release evidence includes one signed adjustment decision used in month-end reconciliation.

### 18. Grade reconciliation chain

**Justification:** Mining teams need one governed view from reserve model through ore control to stockpile and plant feed to understand grade gain or loss.

**Improvement:** Build reconciliation entities and projections for plan grade, control grade, mined grade, stockpile grade, and plant feed grade, including variance reasons and sign-off stages.

**Acceptance evidence:** Tests prove roll-forward consistency across reconciliation stages, the workbench exposes variance drill-down by area and period, and release evidence includes a complete reconciliation pack for one reporting month.

### 19. Survey and measured volume integration

**Justification:** Measured excavation and stockpile surveys are core evidence for tonnes moved, pit advance, and stope void development.

**Improvement:** Add measured survey capture for excavation progress, stockpile volumes, stope voids, and backfill progress with survey date, source, method, confidence, and linkage to affected production records.

**Acceptance evidence:** Tests verify survey updates trigger dependent recalculations, UI views flag stale or missing surveys, and release evidence contains one survey-based correction pack.

### 20. Geotechnical domain and hazard tagging

**Justification:** Geotechnical hazards such as wall movement, crest risk, brow instability, seismicity, and ground support limits directly affect what can be mined.

**Improvement:** Add geotechnical domain tags and hazard states to pits, benches, stopes, and active work areas with risk rating, monitoring source, mitigation requirement, and expiry time for the current ground condition assessment.

**Acceptance evidence:** Tests block mining actions in hazard-tagged areas without approval, the UI shows geotech overlays and restrictions, and release evidence includes one area closure caused by geotechnical risk.

### 21. Geotechnical exclusion zones and conditional approvals

**Justification:** Operations need clear boundary logic when a geotechnical engineer allows restricted access under monitored conditions rather than a full closure.

**Improvement:** Add exclusion zone rules and conditional approval workflows that specify allowed activity, allowed equipment, monitoring checks, escort requirements, and review interval.

**Acceptance evidence:** Workflow tests verify conditional approvals expire correctly, dispatch screens show area-specific constraints, and release evidence includes one conditional-access record with sign-off history.

### 22. Water, dewatering, and weather constraints

**Justification:** Rain, flooded headings, sump limits, and poor road conditions materially change how mine plans are executed and should be reflected in daily decisions.

**Improvement:** Add operational constraint records for rainfall, dewatering status, road condition, sump capacity, and visibility windows, with logic that can block drilling, blasting, loading, or haulage by area.

**Acceptance evidence:** Tests cover constraint-driven stoppages and resumptions, workbench banners explain active weather or water limits, and release evidence includes one shift exception opened by wet-condition restrictions.

### 23. Maintenance and availability boundary

**Justification:** Fleet availability is not a static attribute; dispatch and shift planning need visibility into planned maintenance, breakdown, and return-to-service readiness.

**Improvement:** Extend fleet assets with availability states, breakdown class, maintenance due windows, workshop queue, and return-to-service release checks that feed directly into dispatch eligibility.

**Acceptance evidence:** Tests reject assignments for unavailable or unreleased equipment, UI panels show maintenance-driven dispatch shortfalls, and release evidence includes one fleet availability summary tied to missed production.

### 24. Shift handover and supervisor notes

**Justification:** Key production context is often lost between shifts unless the PBC captures handover notes, open issues, and required follow-up actions.

**Improvement:** Add structured shift handover records covering active headings, blocked areas, equipment issues, ore destination changes, outstanding blasts, stockpile concerns, and plant feed risks.

**Acceptance evidence:** Tests verify handover completion before shift closure, UI screens present unresolved handover items to the next supervisor, and release evidence includes one linked day-night handover record.

### 25. Delay code taxonomy

**Justification:** Production reporting is weak when lost time is captured as free text instead of governed delay categories that can be trended and improved.

**Improvement:** Add a mine-specific delay taxonomy for drilling, blasting, loading, haulage, ore pass, crusher, geotech, weather, survey, and maintenance interruptions with primary and secondary cause capture.

**Acceptance evidence:** Reporting tests roll delay codes into availability and utilization metrics, the workbench supports delay-code drill-down, and release evidence includes one daily delay report.

### 26. Shift production reporting

**Justification:** A mining operations workbench must provide a governed shift production report rather than relying on downstream manual consolidation.

**Improvement:** Add shift production reports that summarize ore tonnes, waste tonnes, metres drilled, blasts fired, truck loads, stockpile movements, plant feed sent, delays, and safety or geotech exceptions by area.

**Acceptance evidence:** Tests validate report totals against source records, the workbench exports the shift report, and release evidence includes one signed production report with supporting record links.

### 27. Variance explanation workflow

**Justification:** Supervisors and managers need structured explanations when actual production misses plan, not just a red variance number.

**Improvement:** Add variance records for tonnes, grade, metres, blasts, cycle count, and equipment hours with causal categories, supporting evidence, action owner, and whether the variance impacts future plan commitments.

**Acceptance evidence:** Tests require variance completion above configured thresholds, UI views show unresolved variances by period, and release evidence includes one closed variance case with corrective action.

### 28. Rolling forecast update cycle

**Justification:** Mine plans change quickly after geotech events, plant constraints, assay returns, and equipment losses, so the PBC needs a short-cycle forecasting surface.

**Improvement:** Add rolling forecast versions for next shift, next day, and next week with deltas from the approved plan, confidence band, and dependency assumptions for active mining areas and plant feed.

**Acceptance evidence:** Tests show forecast version history and approval flow, the workbench compares forecast versus committed plan, and release evidence includes one forecast revision caused by changed ore availability.

### 29. Underground stope readiness checklist

**Justification:** Underground stopes require readiness checks for development completion, services, support, ventilation, and access that differ from open-pit pushback readiness.

**Improvement:** Add stope readiness checklists with headings for development complete, support installed, ventilation available, services in place, brow condition checked, drawpoint readiness, and backfill status.

**Acceptance evidence:** Tests block stope activation until checklist items are satisfied or waived by approval, the detail page shows readiness status, and release evidence includes one approved stope readiness packet.

### 30. Open-pit phase and pushback readiness checklist

**Justification:** Pushback sequencing needs formal readiness control for access, pre-strip completion, wall monitoring, and haul road readiness.

**Improvement:** Add pit-phase readiness records for access established, dewatering complete, ramp serviceability, wall monitoring active, pre-strip achieved, and first-blast approval.

**Acceptance evidence:** Tests enforce readiness gates before the phase becomes active, the workbench shows incomplete pushback prerequisites, and release evidence includes one approved pit-phase start package.

### 31. Typed operational event model

**Justification:** The current generic events do not give downstream consumers enough mining context to react safely to planning, dispatch, ore control, and reconciliation changes.

**Improvement:** Expand emitted events into typed mining events such as `MinePlanVersionApproved`, `BlastCleared`, `DispatchAssignmentChanged`, `OreBoundaryAdjusted`, `StockpileReconciled`, and `PlantFeedNominated` while preserving lineage to the generic package lifecycle.

**Acceptance evidence:** Event-schema tests validate required mining fields, event examples are added to release evidence, and downstream projection tests consume the new event types without ambiguity.

### 32. Event-sourced operational history views

**Justification:** Root-cause analysis is difficult unless users can reconstruct the exact sequence from plan change to blast, haulage, stockpile movement, and plant feed consequence.

**Improvement:** Build event-backed timelines for plan versions, shift execution, dispatch changes, ore boundary calls, stockpile genealogy, and reconciliation adjustments with actor, reason, and before-after summaries.

**Acceptance evidence:** Replay tests rebuild timelines from events, the UI exposes chronological history filters by pit or stope, and release evidence includes one event replay checksum report.

### 33. Projection freshness and dead-letter handling

**Justification:** A live dispatch or reconciliation board is dangerous if the user cannot see when projections are stale or if critical event handlers have failed.

**Improvement:** Add freshness indicators, dead-letter queues, replay actions, and operator explanations for mining projections that power dispatch, stockpile, and reporting screens.

**Acceptance evidence:** Tests simulate failed projection handlers and successful replay, the UI shows stale-data warnings with affected areas, and release evidence includes dead-letter remediation evidence for one failed event.

### 34. Agent skill for shift planning

**Justification:** A useful assistant in this domain should help supervisors prepare shift plans from mine plan, fleet, geotech, and plant feed context without bypassing approvals.

**Improvement:** Add an agent skill that drafts a shift plan with proposed tonnes, active areas, equipment assignments, blast windows, ore destination changes, and risk notes, all as preview-only until a human confirms.

**Acceptance evidence:** Skill tests prove draft generation uses package APIs and permission checks, the assistant panel shows traceable source data and diff preview, and release evidence includes one approved agent-assisted shift plan.

### 35. Agent skill for blast readiness review

**Justification:** Blast preparation gathers dispersed evidence and is a good candidate for governed assistant support.

**Improvement:** Add an agent skill that summarizes drill completion, clearance status, explosive plan, exclusion zone checks, geotech status, and outstanding blockers for a specific blast area.

**Acceptance evidence:** Tests verify the agent refuses to approve or release blasts directly, the assistant panel cites the exact readiness records used, and release evidence includes one blast-readiness summary generated by the skill.

### 36. Agent skill for ore control and destination advice

**Justification:** Ore control teams need rapid, explainable suggestions when assay returns or visual observations imply a destination change.

**Improvement:** Add an agent skill that proposes ore-waste boundary adjustments, stockpile destinations, or plant feed substitutions based on grade evidence, reconciliation state, and policy thresholds.

**Acceptance evidence:** Tests verify the skill emits suggestions with confidence and rationale, UI review steps require human approval before any destination change, and release evidence includes one accepted and one rejected suggestion case.

### 37. Workbench shift console

**Justification:** Mine supervisors need a single shift console rather than jumping between generic detail forms.

**Improvement:** Create a shift console in `MiningOperationsManagementWorkbench` showing active areas, dispatch board, blast windows, queue states, delays, stockpile movements, plant feed nomination, and unresolved safety or geotech constraints.

**Acceptance evidence:** UI tests cover loading, empty, degraded, and permission-filtered states, the console updates from projections without manual refresh assumptions, and release evidence includes screenshots from a seeded shift scenario.

### 38. Pit and stope detail workspace

**Justification:** Area-specific decisions require one workspace where planning, drilling, blasting, ore control, and geotech evidence are visible together.

**Improvement:** Extend `MiningOperationsManagementDetail` into pit and stope workspaces with tabs for plan, readiness, blast status, ore control, active equipment, delays, and reconciliation history.

**Acceptance evidence:** UI integration tests navigate across pit and stope contexts, the workspace shows different components for open-pit and underground records, and release evidence includes one detail walkthrough for each mining method.

### 39. Stockpile and plant feed board

**Justification:** ROM management and blending decisions need a dedicated board because they combine material quality, quantity, queue state, and plant demand.

**Improvement:** Add a board view for stockpiles and plant feed showing tonnes, grade bands, moisture, reclaim plan, active blend recipes, nomination gaps, and feed risk alerts.

**Acceptance evidence:** Tests verify data joins between stockpile, assay, and plant feed projections, UI screenshots show blend cards and alert states, and release evidence includes one day-of-plant-feed board export.

### 40. Reconciliation workspace

**Justification:** Reconciliation is a distinct operating practice and needs its own guided workflow rather than a static report.

**Improvement:** Add a reconciliation workspace for monthly and weekly close that stages survey updates, tonnage adjustments, grade variances, dilution events, and sign-off tasks from mining, geology, survey, and plant stakeholders.

**Acceptance evidence:** Workflow tests enforce staged sign-off, the UI shows unresolved reconciliation blockers, and release evidence contains one complete close package with signatories and variance commentary.

### 41. Mobile and low-connectivity capture

**Justification:** Field supervisors and ore control teams often work in pits or underground areas with unstable connectivity, but production records still need to be captured promptly.

**Improvement:** Add offline-tolerant capture flows for delay events, sample collection, shift notes, and area readiness checks with local queueing, conflict resolution, and later synchronization through governed APIs.

**Acceptance evidence:** Sync tests cover duplicate prevention and conflict resolution, the UI labels unsynced field records clearly, and release evidence includes one offline capture replay log.

### 42. Mine-specific permissions and approvals

**Justification:** Blast release, destination changes, tonnage adjustments, and month-end reconciliation should not share the same approval semantics.

**Improvement:** Add permission scopes and approval policies for plan approval, blast clearance, ore boundary change, stockpile adjustment, plant feed nomination, and reconciliation sign-off, with thresholds and segregation-of-duties checks.

**Acceptance evidence:** Permission tests prove role-based denial and approval escalation paths, the UI hides or disables restricted actions, and release evidence includes an approval matrix used in test and demo scenarios.

### 43. Scenario simulation for mine-to-plant decisions

**Justification:** Mine planners and plant coordinators need to compare options such as opening another bench, changing blend, or diverting trucks before they commit the operation.

**Improvement:** Add simulation flows for what-if scenarios covering equipment loss, blast slip, geotech closure, stockpile depletion, and altered plant grade targets, with projected impact on tonnes, grade, queues, and backlog.

**Acceptance evidence:** Simulation tests produce non-mutating scenario outputs, the workbench shows side-by-side scenario comparison, and release evidence includes one documented scenario review used in planning.

### 44. Mining anomaly detection

**Justification:** Domain anomalies such as impossible cycle times, plant feed without source material, or stockpile growth without inbound movements should be detected automatically.

**Improvement:** Build anomaly rules and models for improbable haul cycles, grade jumps, inconsistent tonnage flows, dispatch conflicts, unapproved area activation, and reconciliation mismatches.

**Acceptance evidence:** Tests cover known anomaly patterns and false-positive suppression, the UI presents anomaly cards with drill-down links, and release evidence includes one anomaly triage report with disposition outcome.

### 45. Release evidence pack for operations scenarios

**Justification:** This PBC needs evidence that it works across realistic mining flows, not only route-level test output.

**Improvement:** Expand release evidence so it contains scenario packs for open-pit production, underground stope mining, blast release, stockpile management, plant feed nomination, and reconciliation close, each with input data, UI proof, events, and outcome summaries.

**Acceptance evidence:** `RELEASE_EVIDENCE.md` references scenario IDs and generated artifacts, seeded datasets reproduce the same scenarios, and a verification checklist shows the expected evidence for every packaged release.

### 46. Seed data for realistic mine operations

**Justification:** Reviewers cannot assess plan, haulage, ore control, and reconciliation behavior without representative data for pits, stopes, fleets, stockpiles, and feed targets.

**Improvement:** Enrich package seed data with at least one open-pit and one underground mine scenario, including active equipment, drill patterns, blasts, stockpiles, assay results, haul routes, delays, and plant feed targets.

**Acceptance evidence:** Seed-data tests load the scenarios cleanly, workbench screens populate with meaningful records, and release evidence identifies which seeded records drive each demonstration path.

### 47. API surface completeness

**Justification:** The current manifest exposes only a narrow command surface and does not yet reflect the operational queries and actions miners need daily.

**Improvement:** Add governed APIs for dispatch assignments, blast readiness, ore-control samples, stockpile adjustments, plant feed nominations, reconciliation actions, delay capture, and forecast versions, plus read endpoints for area workspaces and boards.

**Acceptance evidence:** Contract tests cover create, update, query, and validation-only flows, route documentation lists request and response shapes for each mining action, and release evidence includes example calls for the expanded API set.

### 48. Mining runbooks and operator guidance

**Justification:** A feature-rich workbench still fails operationally if supervisors, dispatchers, geologists, and plant coordinators do not have package-local guidance.

**Improvement:** Add domain runbooks and assistant help content for shift planning, blast control, dispatch recovery, stockpile correction, plant feed nomination, and reconciliation close, all aligned with package workflows and screens.

**Acceptance evidence:** Documentation checks verify the runbooks are linked from the UI and assistant panel, release evidence references the runbook versions used during verification, and seeded scenarios map to the documented operating steps.

### 49. Test matrix across mining flows

**Justification:** The package needs a test shape that mirrors real mining workflows instead of isolated CRUD checks.

**Improvement:** Add a test matrix that covers open-pit and underground plan setup, drill-and-blast control, dispatching, ore control updates, stockpile genealogy, plant feed nominations, geotech restrictions, and reconciliation close.

**Acceptance evidence:** Test listings show coverage for each flow, failure output identifies the broken mining stage clearly, and release evidence summarizes the executed matrix for the package version.

### 50. Operational readiness gate

**Justification:** The final release decision should depend on mining-domain readiness evidence, not only generic package generation success.

**Improvement:** Add a release gate that requires passing scenario tests, fresh UI snapshots, typed event samples, seed-data reproducibility, reconciliation outputs, and sign-off that dispatch, ore control, stockpile, plant feed, and geotech surfaces all behaved as expected.

**Acceptance evidence:** The package emits a readiness checklist for the release candidate, the release evidence bundle contains every required artifact, and verification output explicitly states that the mining operations gate passed for the target version.
