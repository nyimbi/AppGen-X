# Aviation Maintenance Repair Improvement Backlog for `aviation_maintenance_repair`

## Current Domain Evidence Used

- PBC key from `manifest.py`: `aviation_maintenance_repair`.
- Domain description in the manifest: aircraft maintenance, components, work cards, compliance, airworthiness, deferred defects, and MRO operations.
- Owned tables in scope today: `aircraft`, `component`, `work_card`, `maintenance_visit`, `airworthiness_directive`, `deferred_defect`, and `compliance_release`.
- Public APIs in scope today: `POST /aircrafts`, `POST /components`, `POST /work-cards`, `POST /maintenance-visits`, `POST /airworthiness-directives`, and `GET /aviation-maintenance-repair-workbench`.
- Event surfaces already declared: emitted `AviationMaintenanceRepairCreated`, `AviationMaintenanceRepairUpdated`, `AviationMaintenanceRepairApproved`, `AviationMaintenanceRepairExceptionOpened`; consumed `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- UI fragments already declared: `AviationMaintenanceRepairWorkbench`, `AviationMaintenanceRepairDetail`, and `AviationMaintenanceRepairAssistantPanel`.
- Release artifacts already expected by the PBC: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

## Hand-Curated Improvement Backlog

### 1. Aircraft configuration baseline and effectivity control
**Justification:** Maintenance planning is only trustworthy when each tail has a precise baseline for operator configuration, installed options, engine/APU fit, cabin layout, and effectivity cut-ins that change task applicability.
**Improvement:** Add a governed aircraft configuration baseline that records tail number, manufacturer serial number, fleet subtype, option codes, embodiment status, and task effectivity logic down to ATA chapter and mod standard.
**Acceptance evidence:** A tail-level baseline view shows current configuration, superseded configurations, effectivity-driven task inclusions, and a trace from each active requirement back to the configuration element that made it applicable.

### 2. Aircraft status and utilization synchronization
**Justification:** Line and base maintenance decisions depend on current flight hours, flight cycles, parking status, route assignment, and AOG state, not static aircraft master data.
**Improvement:** Introduce a utilization timeline for each aircraft that synchronizes daily FH/FC accrual, station status, operational interruptions, and maintenance-grounded intervals into one planning surface.
**Acceptance evidence:** Planning screens can explain why a due task moved forward or backward, and each forecast change is traceable to an underlying utilization update rather than a manual spreadsheet adjustment.

### 3. Serialized component hierarchy and as-installed history
**Justification:** Aviation MRO requires a reliable as-installed record for serialized components so engineers can reconstruct where a unit was installed, when it moved, and what maintenance history follows it.
**Improvement:** Model parent-child installation history across aircraft, engine, module, assembly, and rotable component positions with removal reason, install reason, and condition at movement time.
**Acceptance evidence:** For any serialized unit, the system can show full movement history, current position, prior defects carried with the unit, and related work cards that triggered install or removal.

### 4. Time-controlled component and life-limited part tracking
**Justification:** LLPs and other time-controlled parts are safety-critical; missing remaining life or incorrect back-to-birth logic creates direct airworthiness risk.
**Improvement:** Expand component records to carry back-to-birth time, since-new/since-overhaul counters, hard-time limits, soft alerts, and shop visit resets for serialized and batch-controlled parts.
**Acceptance evidence:** The backlog includes alerts for approaching limits, a clear reason when a component is blocked from installation, and release evidence showing remaining life calculations used at signoff.

### 5. Maintenance program versioning and applicability
**Justification:** A maintenance organization needs to know which program revision governed planning at any moment, especially when MPD, operator AMP, escalation approvals, or reliability-driven interval changes diverge.
**Improvement:** Create versioned maintenance program entities that hold task intervals, effectivity, escalation references, bridging logic, and supersession history for each fleet or operator group.
**Acceptance evidence:** A planner can open any forecasted task and see the exact program revision, interval source, escalation approval reference, and superseded revision history that produced it.

### 6. Work card revision, effectivity, and signoff block control
**Justification:** Work cards are not generic tickets; they must preserve the revision of the source data, required signoff blocks, consumables, tooling, and effectivity to the aircraft or component being worked.
**Improvement:** Add work card versioning with revision source, task skill code, access requirements, reference document revision, required signatures, and effectivity rules before execution begins.
**Acceptance evidence:** A technician opening a work card sees the locked revision set, required signoff roles, and a warning if the card was generated against an out-of-date manual or inapplicable effectivity.

### 7. Non-routine work card generation during visit execution
**Justification:** Heavy checks and defect-finding inspections routinely create non-routine work that must stay linked to the originating inspection, zone, panel, and finding evidence.
**Improvement:** Enable controlled generation of non-routine work cards from routine tasks, inspections, and defect findings, with linkage back to originating card, station, zone, and inspection result.
**Acceptance evidence:** Visit control can trace every non-routine card to the triggering finding, see its impact on visit critical path, and confirm whether closure evidence satisfied the originating inspection requirement.

### 8. Defect log model from pilot report to rectification
**Justification:** Defects move through observation, troubleshooting, rectification, deferral, recurrence review, and closure; the backlog should reflect that operating chain instead of treating defects as flat records.
**Improvement:** Rework deferred defect handling into a full defect log that records pilot reports, maintenance observations, troubleshooting steps, rectification attempts, deferral decisions, and closeout statements.
**Acceptance evidence:** Each defect shows a chronological technical narrative with who reported it, what troubleshooting occurred, why it was deferred or cleared, and which maintenance release ultimately closed it.

### 9. MEL/CDL deferment control with countdown management
**Justification:** MEL and CDL items are governed by category limits, operating procedures, placarding, dispatch conditions, and expiration countdowns that require far more control than a generic deferred defect status.
**Improvement:** Add MEL/CDL-specific deferment records with category, expiry basis, operational limitations, maintenance procedures, placard requirements, station limitations, and countdown visibility.
**Acceptance evidence:** Dispatch-facing views show remaining time before expiry, required operational procedures, required maintenance actions, and automatic escalation when a deferment approaches its allowed limit.

### 10. Airworthiness directive applicability and compliance planning
**Justification:** AD control is core to continuous airworthiness; the system must distinguish not-applicable, one-time, repetitive, terminating action, and AMOC-driven compliance paths.
**Improvement:** Extend airworthiness directive records to hold applicability logic, compliance method, repeat interval, terminating action, AMOC references, embodiment evidence, and overdue exposure by aircraft and component.
**Acceptance evidence:** For every AD, the PBC can show applicable population, due status, compliance evidence, open exceptions, and whether the next due is suppressed by terminating action or modified by approved alternative means.

### 11. Service bulletin and OEM campaign decision register
**Justification:** Not every SB is mandatory, but maintenance planning needs a disciplined decision trail for incorporation, deferral, partial embodiment, or rejection.
**Improvement:** Introduce an SB decision register that records technical evaluation, cost and downtime impact, embodiment strategy, affected fleet, required kits, and linkage to work scope when adopted.
**Acceptance evidence:** Engineering can review an SB and see the decision basis, adoption status by tail or component population, embodiment completion, and open exposure where the decision has not yet been executed.

### 12. Engineering order and repair scheme governance
**Justification:** Operators often work through engineering orders, repair drawings, and approved repairs that sit between discovered damage and routine card execution.
**Improvement:** Add controlled engineering order records with repair classification, approval basis, structural or systems effect, serial or tail applicability, and expiry or replacement conditions.
**Acceptance evidence:** A damage or repair record can be traced to the engineering authorization that allowed it, with evidence that the repair was performed on the approved population and within its stated conditions.

### 13. Maintenance visit planning around check packages and ground time
**Justification:** A maintenance visit is a constrained event balancing check package content, slot duration, hangar capacity, labor mix, material readiness, and operational return-to-service date.
**Improvement:** Expand `maintenance_visit` into a visit planning model with planned scope, visit milestones, dock or bay assignment, critical path tasks, access dependencies, and ground-time consumption.
**Acceptance evidence:** Visit dashboards show planned versus actual milestone movement, slipped critical path work cards, material blockers, and the impact of added non-routine scope on the release date.

### 14. Zone, ATA, and inspection campaign orchestration
**Justification:** Inspections are usually organized by zone, ATA system, structural area, or campaign type, and planners need a way to understand where open inspection exposure still sits.
**Improvement:** Introduce inspection campaign objects for zonal inspections, structural programs, corrosion programs, borescope campaigns, and repetitive inspection clusters, all linked to work card generation and findings.
**Acceptance evidence:** Supervisors can filter open inspection findings by zone or ATA, review associated non-routines, and confirm whether a campaign is complete enough to release the aircraft or component.

### 15. Duplicate inspection and critical task enforcement
**Justification:** Certain maintenance tasks require independent inspection or duplicate inspection; missing that second check is a direct compliance failure.
**Improvement:** Add task-level flags for independent inspection, duplicate inspection, and critical task status, with separate authorization checks for performer and inspector and explicit block on self-release.
**Acceptance evidence:** The system prevents invalid self-signoff, records both inspection roles distinctly, and includes duplicate-inspection evidence in release-to-service packages.

### 16. Technician authorization matrix by task family and aircraft type
**Justification:** Signoff rights are constrained by license, type authorization, company authorization, shop qualification, and sometimes special process approval.
**Improvement:** Model technician authorizations by aircraft type, engine type, task family, inspection privilege, shop capability, and authorization validity dates.
**Acceptance evidence:** Before signoff, the workbench can explain whether the selected technician is authorized, which authorization record was used, and why an attempted certification was blocked if it failed.

### 17. Shift handover and unfinished work continuity
**Justification:** Multi-shift maintenance fails when task context, tool status, panel access, and safety precautions disappear between handovers.
**Improvement:** Add structured shift handover records to maintenance visits and work cards that capture open access panels, isolated systems, installed tags, incomplete steps, and outstanding engineering questions.
**Acceptance evidence:** Incoming shifts can open a handover board showing unfinished work, safety-critical precautions still active, and explicit acknowledgement that handover information was reviewed before work resumed.

### 18. Tooling issue, return, and calibration lockout
**Justification:** A released task should not rely on uncalibrated torque tools, expired test equipment, or missing controlled tooling.
**Improvement:** Track controlled tooling assignment to work cards, including issue and return status, calibration expiry, substitute-tool approvals, and special-tool availability during visit planning.
**Acceptance evidence:** Execution screens block work requiring a lapsed tool, and release evidence shows calibrated tools used for tasks that demanded controlled tooling.

### 19. Consumables, shelf-life, and hazardous material checks
**Justification:** Sealants, adhesives, lubricants, and hazardous materials often have shelf-life, mix-life, storage, and disposal constraints that matter to maintenance quality records.
**Improvement:** Add consumable controls for batch identity, expiry, mix start and end time, storage condition, and hazardous handling notes linked to work card execution.
**Acceptance evidence:** Completed work cards can show which consumable batch was used, whether it was within allowed life, and whether special handling or disposal evidence was captured.

### 20. Parts request, kitting, and pick shortage visibility
**Justification:** Work scope slips when cards are released without material readiness; planners need a live view of kit completeness before docking or line execution windows.
**Improvement:** Create a maintenance material board that links work cards to requested parts, kit status, shortages, alternates under evaluation, and expected delivery against visit milestones.
**Acceptance evidence:** Visit control can see which critical path cards are blocked by material, which kits are complete, and which shortages have approved alternates or engineering concessions.

### 21. Parts traceability pack for serialized and life-limited parts
**Justification:** Airworthy installation depends on traceable release documents, serial identity, life status, and authorized source, especially for serialized and life-limited hardware.
**Improvement:** Add a traceability pack to component records holding authorized release certificate data, serial and batch information, life documents, repair history, and source chain before installation.
**Acceptance evidence:** Installation screens can show the full traceability pack, highlight missing or conflicting release data, and prevent installation of a part lacking required authorized release evidence.

### 22. Quarantine flow for suspect, unapproved, or damaged parts
**Justification:** Suspect or damaged material must be segregated immediately so it cannot accidentally re-enter stock or be fitted to an aircraft.
**Improvement:** Introduce quarantine states for parts with damage, traceability gaps, suspected unapproved part indicators, missing release documents, or failed incoming inspection results.
**Acceptance evidence:** Quarantined items are visibly segregated from serviceable material, every release from quarantine requires explicit technical justification, and blocked installations reference the quarantine reason.

### 23. Rotable exchange, repair, and warranty loop visibility
**Justification:** Rotables move through removal, replacement, repair vendor dispatch, return, warranty claim, and re-stock; that loop should stay connected to the originating aircraft event.
**Improvement:** Add rotable lifecycle tracking with removal cause, replacement serial, repair order progress, warranty claim state, and serviceable return disposition.
**Acceptance evidence:** Reliability and planning teams can open a rotable history and see whether repeat removals, repair turnaround delays, or warranty recoveries are affecting fleet availability.

### 24. Cannibalization governance and restoration tracking
**Justification:** Cannibalization is sometimes operationally necessary but creates secondary restoration work and traceability obligations that need close control.
**Improvement:** Add a governed cannibalization process recording donor aircraft, recipient aircraft, urgency basis, restoration due-back, reinspection requirements, and final technical closeout.
**Acceptance evidence:** Every cannibalization action is reversible in the record, restoration tasks remain visible until complete, and fleet controllers can see open donor-aircraft exposure created by the removal.

### 25. Vendor repair station and subcontracted work evidence
**Justification:** MRO organizations frequently rely on outside repair stations, but the operator still needs complete evidence of capability, release, and turn-around performance.
**Improvement:** Extend component and maintenance visit records to capture subcontracted work scope, vendor capability basis, expected return date, received documentation, and technical acceptance checks on return.
**Acceptance evidence:** A returned unit or outsourced work package cannot close until required vendor release evidence is present and accepted by the receiving technical authority.

### 26. NDT, borescope, and photographic evidence capture
**Justification:** Findings from NDT, borescope inspections, and visual damage assessments often depend on media evidence and method details, not just typed remarks.
**Improvement:** Add structured inspection evidence capture for inspection method, inspector qualification, defect location reference, measured result, annotated images, and disposition decision.
**Acceptance evidence:** Engineering can review a finding with its supporting media, qualification context, and measured values, and the release package includes references to accepted inspection evidence where required.

### 27. Release-to-service and certificate of release to service pack
**Justification:** The final release decision needs a complete, auditable bundle proving the aircraft or component met technical, inspection, material, and authorization requirements.
**Improvement:** Build a release-to-service pack around `compliance_release` that assembles completed work cards, required inspections, defect disposition, deferred item status, tooling checks, part traceability, and certifier authorization.
**Acceptance evidence:** Certifying staff can review one release pack showing why the item is eligible for release, and the system blocks release if any mandatory evidence is still missing or contradictory.

### 28. Deferred defect risk board and fleet exposure view
**Justification:** A deferred defect is rarely isolated; fleet-wide exposure matters when the same issue is active across multiple tails or stations.
**Improvement:** Add a defect risk board that ranks open deferred defects by MEL/CDL category, recurrence, route limitations, overdue risk, and fleet concentration.
**Acceptance evidence:** Reliability and maintenance control can see which defects are concentrated across the fleet, which ones are nearing dispatch or interval limits, and which require immediate engineering attention.

### 29. Repeat defect and recurring snag detection
**Justification:** Recurring snags often signal ineffective troubleshooting, unsuitable repairs, or latent design problems; they should be visible without manual spreadsheet work.
**Improvement:** Detect repeats by ATA, symptom pattern, aircraft tail, station, component serial, and elapsed time since last clearance, with thresholds configurable by fleet engineering.
**Acceptance evidence:** A defect card clearly states when it is considered recurrent, references related prior occurrences, and routes repeat events into engineering or reliability review queues.

### 30. Reliability program metrics by ATA, system, and component
**Justification:** Reliability control is a core MRO discipline, and the backlog should support measures such as repeat rates, removals, delay causes, and defect concentration by system.
**Improvement:** Add a reliability analytics layer that computes recurring defect rate, unscheduled removal rate, delay and cancellation contributors, repeat intervals, and top offenders by ATA chapter and component family.
**Acceptance evidence:** Reliability users can drill from a fleet metric into the exact defects, removals, and work cards that produced it, with period-over-period trend comparisons.

### 31. Deferred defect aging versus MEL/CDL interval conflict detection
**Justification:** Aging defects become especially dangerous when planning systems miss the interaction between actual aircraft utilization and deferment category clocks.
**Improvement:** Add a rule set that compares projected aircraft utilization against MEL/CDL expiry logic and warns when an apparently acceptable deferral will breach before the next planned maintenance opportunity.
**Acceptance evidence:** Maintenance control receives forward-looking alerts that explain the forecast breach date, the utilization assumption behind it, and the maintenance options available to avoid non-compliance.

### 32. Maintenance forecast from FH, FC, and calendar projections
**Justification:** Effective planning depends on combining hours, cycles, and calendar limits into a single due list that updates as fleet usage changes.
**Improvement:** Build a forecast engine that projects due tasks and component removals using actual accrual history, planned schedule, buffer rules, and operator planning thresholds.
**Acceptance evidence:** Planners can compare today’s forecast with a prior snapshot, identify what changed, and verify that the due driver for each item is clearly labeled as FH, FC, calendar, or combined logic.

### 33. AOG triage workbench
**Justification:** AOG events compress maintenance decision time and require a different operating surface than routine planning or visit execution.
**Improvement:** Add an AOG workbench focused on immediate defect status, available authorized staff, nearby parts options, open engineering questions, deferred possibilities, and release blockers.
**Acceptance evidence:** Controllers can open a single screen for an AOG event and see technical status, material status, manpower status, and the next decision needed to recover the aircraft.

### 34. Line maintenance execution workbench
**Justification:** Transit and overnight line work relies on short windows, station-specific capability, and rapid signoff, so it needs its own focused UI rather than a generic detail page.
**Improvement:** Create a line maintenance workbench optimized for open defects, due tasks, shift assignment, dispatch-critical limits, and rapid review of release blockers.
**Acceptance evidence:** Line users can move from tail status to due cards, open defects, authorizations, and release readiness within one workflow without traversing visit-oriented screens.

### 35. Base maintenance and heavy check control tower
**Justification:** Heavy checks need dock-level control over zones, trades, materials, non-routines, and critical path progress across many days or weeks.
**Improvement:** Create a base maintenance control tower showing dock occupancy, package progress, open access dependencies, major findings, material blockers, and release-to-service readiness by visit.
**Acceptance evidence:** Visit managers can review progress by zone and trade, identify the true release driver, and see whether late findings are still cascading into downstream task groups.

### 36. Release evidence pack generation for visits and major work scopes
**Justification:** Release evidence should not be assembled manually at the end of a visit; the pack should accumulate throughout execution and expose gaps early.
**Improvement:** Generate a release evidence pack that continuously gathers signed cards, duplicate inspection proof, deferred defect statements, parts traceability, and authorization checks as work progresses.
**Acceptance evidence:** Before final signoff, the visit team can preview the release pack, see missing evidence by category, and export a final package aligned with the PBC’s `RELEASE_EVIDENCE.md` expectation.

### 37. Event boundary hardening for maintenance state changes
**Justification:** MRO state changes should emit technically meaningful events so downstream consumers can react without reading internal tables or reverse-engineering status text.
**Improvement:** Replace generic lifecycle emissions with domain-specific maintenance events for aircraft grounded, work card released, work card signed, defect deferred, AD complied, component installed, and release issued.
**Acceptance evidence:** Event catalogs show clear payload contracts, each event maps to a business action in the UI, and no downstream integration depends on undocumented interpretation of internal statuses.

### 38. API boundary expansion for validation, simulation, and evidence export
**Justification:** The current create-oriented APIs are too thin for serious maintenance planning, operational review, and controlled integration with surrounding systems.
**Improvement:** Add explicit APIs for applicability validation, forecast simulation, evidence export, release pack preview, defect recurrence lookup, and authorization pre-check without bypassing governed workflows.
**Acceptance evidence:** API consumers can validate or simulate decisions before mutation, obtain evidence bundles without scraping UI views, and receive structured failure reasons when a command is blocked.

### 39. Audit trail by aircraft, component, work card, and certifier
**Justification:** Investigations often start from a tail, a serial number, a work card, or a certifier, and the audit story should be reconstructable from any of those entry points.
**Improvement:** Build a cross-linked audit trail that pivots across aircraft, component serial, work card, maintenance visit, defect, and certifying staff actions with exact timestamps and source context.
**Acceptance evidence:** An investigator can start from any one of those entities and reconstruct the full maintenance narrative without separate database forensics.

### 40. Controlled correction and supersession of signed maintenance records
**Justification:** Maintenance records occasionally require correction, but corrections must preserve the original statement and make the superseding rationale explicit.
**Improvement:** Add a controlled correction workflow for signed records that preserves original content, records who requested the correction, why it was needed, and which statement superseded it.
**Acceptance evidence:** Corrected records remain fully visible in audit history, the active statement is clearly marked, and release evidence distinguishes original signoff from authorized correction.

### 41. Technical document intake for AMM, CMM, IPC, AD, and SB revisions
**Justification:** Maintenance execution quality depends on the current technical document set, and document change control should drive task and planning change rather than sit outside the PBC.
**Improvement:** Add controlled ingestion for manual revisions, IPC updates, AD revisions, SB revisions, and shop findings so the PBC can detect affected tasks, cards, or component rules.
**Acceptance evidence:** When a source document changes, planners can see impacted tasks or components, acknowledge the review outcome, and verify whether existing cards must be regenerated or reissued.

### 42. Agent skill for work-scope drafting from planning packages
**Justification:** Agent assistance is useful only if it accelerates real planner work such as drafting visit scope, grouping due tasks, and identifying missing prerequisites from source documents.
**Improvement:** Add an assistant skill that reads maintenance program inputs, AD/SB decisions, open defects, and material status to draft a proposed visit or line package for planner review.
**Acceptance evidence:** The assistant produces a reviewable draft scope with cited source reasons for each proposed task, and planners can accept, reject, or edit each proposal before work cards are generated.

### 43. Agent skill for defect troubleshooting and evidence assembly
**Justification:** Troubleshooting assistance should help technicians and controllers gather evidence and prior history without inventing technical actions or bypassing approved data.
**Improvement:** Add an assistant skill that summarizes similar prior defects, related troubleshooting steps, component movement history, and open engineering references while clearly separating facts from recommendations.
**Acceptance evidence:** Defect users can see the evidence set the assistant used, confirm that proposed next steps came from approved references or prior internal outcomes, and reject unsupported suggestions.

### 44. Agent guardrails around maintenance release and certifying authority
**Justification:** The assistant must never imply certifying authority it does not hold, especially around maintenance release, duplicate inspection, or airworthiness decisions.
**Improvement:** Introduce hard guardrails so assistant actions stop at evidence gathering, draft preparation, and controlled recommendations unless a human with the right authorization completes the certifying step.
**Acceptance evidence:** Attempted assistant actions that would cross certifying boundaries are blocked with explicit rationale, and release packs show only human certifier identities in final signoff fields.

### 45. Reliability-to-planning feedback loop
**Justification:** Reliability findings are valuable only if they influence planning, troubleshooting depth, inspection focus, or component strategy in future work.
**Improvement:** Link reliability findings back into maintenance program reviews, visit planning decisions, repeat defect thresholds, and targeted inspection campaigns for high-failure systems.
**Acceptance evidence:** A reliability trend can be traced to a resulting planning change, extra inspection, engineering review, or component strategy decision instead of remaining a read-only report.

### 46. Fleet configuration drift and embodiment status dashboard
**Justification:** Operators frequently manage mixed embodiment states across a fleet, and missing visibility leads to wrong assumptions about AD, SB, or engineering order applicability.
**Improvement:** Add a configuration drift dashboard showing embodiment status for mods, SBs, repairs, software loads, and cabin or systems differences across the fleet.
**Acceptance evidence:** Engineering and planning can identify which tails remain unembodied, why they differ from the fleet baseline, and what task or compliance exposure that difference creates.

### 47. Lease return and redelivery technical records readiness
**Justification:** Redelivery events put unusual pressure on technical records quality, traceability, and open item closure, so they deserve explicit backlog treatment.
**Improvement:** Add a redelivery readiness mode that assembles aircraft configuration history, major maintenance records, AD status, LLP traceability, repair status, and open defect exposure into one review package.
**Acceptance evidence:** Commercial and technical teams can see a gap list for redelivery readiness, with each missing technical record or unresolved exposure assigned to a specific owner.

### 48. Cabin damage, structural repair, and corrosion campaign management
**Justification:** Corrosion findings, structural repairs, and cabin damage often span multiple visits and require long-lived tracking beyond the card that first detected them.
**Improvement:** Add campaign tracking for corrosion prevention, structural repair follow-up, and cabin damage recovery with recurring inspection requirements, engineering references, and long-term embodiment status.
**Acceptance evidence:** Users can review open corrosion or structural campaigns by aircraft and zone, see prior repairs and follow-up requirements, and confirm whether the next visit must carry forward work.

### 49. Pre-close cross-check gate before visit or line release
**Justification:** Many release escapes happen because open cards, missing tools, unresolved material issues, or authorization gaps are discovered too late.
**Improvement:** Add a pre-close gate that cross-checks open work cards, outstanding defects, overdue inspections, missing tool returns, unresolved part traceability issues, and invalid signoff authority before release.
**Acceptance evidence:** The system produces a release-blocker checklist with explicit pass or fail status for each category, and nothing can progress to final release while blockers remain unresolved.

### 50. Continuous airworthiness executive dashboard
**Justification:** Leadership needs a live view of technical risk, release confidence, and fleet exposure that stays grounded in actual maintenance data rather than after-the-fact spreadsheets.
**Improvement:** Build an executive dashboard showing AD compliance risk, deferred defect exposure, repeat defect pressure, visit release confidence, tooling and material readiness, and certifier capacity across the fleet.
**Acceptance evidence:** Leaders can review a current fleet airworthiness posture, drill into the underlying technical records driving each indicator, and export a defensible summary for release and compliance reviews.
