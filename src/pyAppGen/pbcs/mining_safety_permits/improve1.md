# Mining Safety and Permits Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `mining_safety_permits`.
- Label: Mining Safety and Permits.
- Domain description: mine permits, shifts, blasts, inspections, incidents, safety controls, and regulatory evidence.
- APIs in scope: `POST /mine-permits`, `POST /shift-rosters`, `POST /blast-plans`, `POST /safety-inspections`, `POST /incident-reports`, `GET /mining-safety-permits-workbench`.
- Core tables in scope: `mine_permit`, `shift_roster`, `blast_plan`, `safety_inspection`, `incident_report`, `regulatory_submission`, `control_action`.
- Events currently emitted: `MiningSafetyPermitsCreated`, `MiningSafetyPermitsUpdated`, `MiningSafetyPermitsApproved`, `MiningSafetyPermitsExceptionOpened`.
- Events currently consumed: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- UI fragments named in the manifest: `MiningSafetyPermitsWorkbench`, `MiningSafetyPermitsDetail`, `MiningSafetyPermitsAssistantPanel`.
- Docs already expected by the PBC: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

### 1. Canonical permit-to-work register
**Justification:** Mine sites usually run many permit types in parallel, and a single generic permit record does not distinguish excavation, hot work, electrical isolation, confined space, working at height, lifting, blasting, or radiation-related controls.
**Improvement:** Expand the permit model so every permit-to-work carries permit class, work area, start and expiry windows, simultaneous operations flags, issuing authority, performing crew, affected assets, and mandatory control bundles. Include permit-type-specific rules for underground, open-pit, plant, tailings, laboratory, and workshop work.
**Acceptance evidence:** Schema fields and tests show each permit class can be created with its own required fields, and the workbench displays permit type, status, expiry, and conflicting work indicators.

### 2. Permit lifecycle with mining-specific hold points
**Justification:** Mining permits often require more than draft and approval; they need suspension, revalidation, extension, closure, and post-job verification states when conditions change underground or in the pit.
**Improvement:** Define a state machine for permit draft, supervisor review, safety review, active, suspended, extended, closed, canceled, and expired states with explicit reasons and actor attribution. Require renewed checks before returning a suspended permit to active status.
**Acceptance evidence:** State-transition tests reject illegal jumps, audit history records each transition reason, and UI badges show whether a permit is awaiting review, active, suspended, or overdue for closure.

### 3. Isolation and lockout verification
**Justification:** Permit safety fails quickly when isolations are recorded as free text and not tied to energy sources, lock points, and verification steps.
**Improvement:** Add a structured isolation module capturing electrical, hydraulic, pneumatic, mechanical, gravity, pressure, and stored-energy sources; isolation points; lock and tag IDs; applied-by and verified-by roles; and zero-energy confirmation before work starts.
**Acceptance evidence:** Permit records cannot be approved when required isolation points are incomplete, zero-energy checks are stored in evidence, and regression tests prove multi-point isolation scenarios work.

### 4. Isolation boundary change control
**Justification:** Mine plant layouts and work fronts change during a shift, so an approved isolation can become unsafe if a boundary is altered without re-review.
**Improvement:** Track isolation boundary revisions with versioned diagrams, added or removed lock points, reason for change, and compulsory re-acceptance by the permit issuer and the field supervisor.
**Acceptance evidence:** Edited isolation boundaries create a new version, active permits enter revalidation state, and the event stream records who changed the boundary and who reapproved it.

### 5. Confined space inventory and classification
**Justification:** Confined spaces in mining range from tanks and sumps to ore passes, hoppers, ducts, and raise-bore chambers, each with different entry constraints.
**Improvement:** Maintain a classified confined-space inventory linked to permit records, including space type, dimensions, access points, ventilation arrangements, engulfment hazards, adjacent energy hazards, rescue method, and standby requirements.
**Acceptance evidence:** Confined-space permits can only reference registered spaces or approved temporary spaces, and tests confirm space classification drives the right control checklist.

### 6. Gas testing sequence and validity logic
**Justification:** Underground and enclosed mining work depends on current atmospheric readings, not on a single checkbox saying “gas tested.”
**Improvement:** Model gas testing as a structured sequence with instrument ID, bump-test status, tester competency, reading timestamp, gases measured, permissible limits, retest interval, and invalidation triggers such as blasting, ventilation interruption, or elapsed time.
**Acceptance evidence:** A confined-space or hot-work permit cannot activate without valid atmospheric readings, expiry timers force retesting when the validity window lapses, and evidence exports show the full reading history.

### 7. Ventilation and atmospheric dependency checks
**Justification:** Gas conditions in mines depend on ventilation circuits, fans, regulators, and stoppings, so permit safety needs live ventilation context.
**Improvement:** Introduce ventilation dependency fields for working area, primary and secondary airflow, critical fans, known dead zones, and gas-monitoring points. Add rules that suspend permits when ventilation status is degraded or readings trend toward alarm thresholds.
**Acceptance evidence:** Simulation and rule tests show a ventilation failure moves impacted permits into hold, and the workbench identifies which permits depend on the affected circuit.

### 8. Ground control pre-start assessment
**Justification:** Ground falls and rockbursts remain high-consequence mining hazards, and permits need a direct link to local ground conditions rather than a generic “area safe” statement.
**Improvement:** Add ground control assessments to relevant permits, capturing support type, last scaling date, geotechnical inspection status, seismicity alerts, water ingress observations, brow condition, and unsupported span risk.
**Acceptance evidence:** Permit approvals are blocked when required ground control fields are missing, inspection evidence can be attached to the permit, and tests verify underground and pit-wall scenarios separately.

### 9. Ground support defect escalation
**Justification:** A permit process that records defects without escalating them still allows crews into unsafe headings or unstable benches.
**Improvement:** Create a defect workflow for missing bolts, failed mesh, damaged props, loose ground, crest cracks, berm failures, and shotcrete delamination, with severity, barricade status, corrective owner, and return-to-service criteria.
**Acceptance evidence:** High-severity defects automatically open exceptions, affected permits are paused, and dashboards show unresolved ground support issues by area and shift.

### 10. Explosives permit prerequisites
**Justification:** Blasting and explosives handling need a higher control threshold than ordinary work because errors affect people, ventilation, adjacent workings, and production sequencing.
**Improvement:** Expand blast-plan and explosives permit data to include shotfirer authorization, magazine issue reconciliation, blast-hole readiness, exclusion zone design, firing windows, firing circuit checks, misfire response plan, and blast clearance authority.
**Acceptance evidence:** Explosives-related permits cannot pass approval without all prerequisite fields, and test cases cover routine production blasts, secondary breakage, and misfire contingencies.

### 11. Blast clearance and re-entry control
**Justification:** The permit system must govern the period after detonation as tightly as the period before it.
**Improvement:** Add post-blast checks for fumes clearance, re-entry gas tests, geotechnical inspection, brow and crest inspection, misfire confirmation, and signed release for adjacent crews and mobile equipment.
**Acceptance evidence:** Post-blast permits remain closed to re-entry until all release steps are complete, re-entry evidence is visible in the workbench, and events show who cleared the area.

### 12. Simultaneous operations conflict detection
**Justification:** Mining work often overlaps in the same area, and permits need to identify when one activity invalidates another.
**Improvement:** Build a conflict engine that checks overlapping permits for blasting near confined-space work, energization during maintenance, hot work near hydrocarbons, mobile equipment near suspended loads, and work beneath unsupported ground.
**Acceptance evidence:** Conflict checks run before approval and at activation time, blocking conflicts appear in the UI with resolution guidance, and test fixtures prove conflict detection across permit classes.

### 13. Shift handover permit continuity
**Justification:** Many permit failures happen during shift change when outgoing crews know the hazards but incoming crews inherit only a permit number.
**Improvement:** Add structured handover records with active permits, outstanding isolations, changed conditions, incomplete controls, open exceptions, atmospheric status, pending re-tests, and supervisor signoff from both outgoing and incoming shifts.
**Acceptance evidence:** Shift handover cannot be closed with unresolved active-permit items, the workbench shows unaccepted handovers, and evidence exports include the handover acknowledgement chain.

### 14. Crew competency and authorization checks
**Justification:** Permit validity depends on whether the assigned people are trained and authorized for the specific work, not only whether a supervisor approved the task.
**Improvement:** Introduce competency matching for permit issuer, permit receiver, gas tester, standby person, isolator, electrician, rigger, shotfirer, and geotechnical examiner roles. Validate license dates, medical restrictions, induction status, and area-specific authorizations.
**Acceptance evidence:** Assignment rules reject workers missing required competencies, expired authorizations trigger clear errors, and tests prove role-based competency checks across multiple permit types.

### 15. Contractor verification for high-risk tasks
**Justification:** Contractors often perform specialized mining work, but their documentation quality and site familiarity vary widely.
**Improvement:** Add contractor readiness checks for insurance, scope authorization, inductions, supervisor nomination, equipment compliance, rescue arrangements, and approved work method statements for the specific permit type.
**Acceptance evidence:** Contractors cannot be attached to high-risk permits without passing readiness checks, the detail view shows missing contractor prerequisites, and audit evidence links the contractor package to the permit.

### 16. Fatigue, fit-for-work, and roster exceptions
**Justification:** Mining shifts are long and often remote, so fatigue and fitness issues materially change the risk of work authorization.
**Improvement:** Connect shift-roster records to permit approval checks that flag excessive hours, insufficient rest, unplanned overtime, and medically restricted assignments for safety-critical tasks.
**Acceptance evidence:** Safety-critical permits warn or block on roster risk conditions, exception logic requires supervisor justification, and analytics show how many permits were impacted by fatigue-related rules.

### 17. Hazard control library aligned to mining work
**Justification:** Generic hazard checklists do not capture mine-specific controls such as barricading brows, scaling loose ground, testing for toxic gases, or verifying refuge access.
**Improvement:** Build a control library for ground control, ventilation, explosives, mobile equipment interaction, energy isolation, water management, confined space, working at height, lifting, and hazardous substances. Allow permit templates to require specific controls by work type and area.
**Acceptance evidence:** Permit templates resolve to concrete control lists, closed permits retain the exact controls applied, and tests verify that omitted mandatory controls are detected.

### 18. Critical control verification before work starts
**Justification:** A control listed on a permit is not enough unless someone confirms it was physically implemented in the field.
**Improvement:** Require field verification for selected critical controls with timestamp, verifier identity, evidence attachment, and periodic recheck logic. Examples include barricades in place, ventilation on, scaling completed, gas readings acceptable, and lock points intact.
**Acceptance evidence:** Active status is blocked until critical controls are verified, recheck reminders are generated when needed, and evidence packs show both planned controls and verified controls.

### 19. Water ingress and inundation risk checks
**Justification:** Unexpected water is a distinct mining hazard that can invalidate permits even when other controls look adequate.
**Improvement:** Add water-related assessments for nearby workings, dewatering status, sump capacity, bund integrity, rainfall triggers for surface operations, and known old-workings proximity before permits are approved in exposed areas.
**Acceptance evidence:** Water-risk conditions can stop approval or trigger extra controls, the workbench highlights permits affected by inundation triggers, and scenario tests cover both underground and surface settings.

### 20. Mobile equipment interaction controls
**Justification:** Many mine incidents involve collisions between work crews and haul trucks, loaders, drills, or light vehicles operating in the same zone.
**Improvement:** Add traffic-management fields to permits for equipment exclusion zones, spotters, radio channel, one-way restrictions, parking boundaries, and immobilization checks when maintenance occurs near operating plant or haul roads.
**Acceptance evidence:** Maintenance and field-work permits capture equipment interaction controls, missing traffic-management controls block approval, and UI maps show equipment-related exclusion areas.

### 21. Incident precursor and near-miss capture
**Justification:** A mining safety system should learn from weak signals before they become injuries, blast incidents, falls of ground, or environmental releases.
**Improvement:** Extend incident reporting so near misses, unsafe conditions, permit breaches, gas exceedances, and control failures can be logged quickly and linked to the relevant permit, shift, area, and crew.
**Acceptance evidence:** Near-miss events appear in incident analytics, linked permits display precursor history, and tests prove precursor records can escalate into formal investigations when severity increases.

### 22. Incident prevention feedback loop
**Justification:** Capturing incidents without feeding the lessons back into permits and controls leaves the same exposure in place.
**Improvement:** Add a prevention loop that proposes new controls, template changes, training needs, and policy updates based on incident classifications such as fall of ground, energy release, explosives misfire, atmospheric hazard, vehicle interaction, or procedural breach.
**Acceptance evidence:** Closed incident records can generate tracked control actions, policy changes emit traceable events, and dashboards show whether corrective actions reduced repeat events.

### 23. High-potential event escalation workflow
**Justification:** Potentially catastrophic events need tighter governance even when no injury occurred.
**Improvement:** Introduce a dedicated high-potential pathway for events with blast misfires, serious gas exceedances, ground collapse indicators, uncontrolled energy release, or major permit violations, including immediate area holds, senior review, and evidence preservation.
**Acceptance evidence:** High-potential incidents trigger accelerated notifications and permit holds, evidence retention is enforced, and tests validate escalation timing and closure requirements.

### 24. Regulatory evidence pack assembly
**Justification:** Regulators and internal auditors often ask for the entire evidence trail around a job, not a single permit snapshot.
**Improvement:** Build exportable evidence packs that gather permit forms, approvals, gas tests, isolation records, handovers, inspections, incident links, control verifications, and event history into a reproducible package.
**Acceptance evidence:** Evidence exports are consistent across repeated runs, export manifests show every included artifact, and sample packs exist for confined-space, blasting, and ground-control jobs.

### 25. Jurisdiction and site rule overlay support
**Justification:** Mining organizations often operate across sites with different legal duties, standards, and local operating procedures.
**Improvement:** Add a rule overlay model allowing site, country, commodity, and operation-type variations for permit fields, retention periods, explosives controls, atmospheric limits, and mandatory evidence.
**Acceptance evidence:** Site-specific rules can change validation outcomes without code edits, policy version is stored with each permit, and tests prove one site can require controls that another site does not.

### 26. Workbench area control board
**Justification:** Supervisors need to see active work by area, not only a list of permits sorted by creation time.
**Improvement:** Redesign the workbench with an area control board showing current permits, isolations, confined-space entries, blasting windows, open hazards, incidents, and shift ownership by mining area.
**Acceptance evidence:** The UI renders area-level summaries with live status counts, conflict indicators, and overdue items, and route tests cover empty, populated, and degraded-data states.

### 27. Permit detail view optimized for field decision-making
**Justification:** Permit detail screens often bury the highest-risk facts below general metadata, slowing field decisions.
**Improvement:** Rework the detail panel so hazard controls, atmospheric status, isolations, handover notes, competency gaps, and stop-work conditions appear ahead of less critical metadata. Include a clear “why blocked” section when a permit cannot proceed.
**Acceptance evidence:** UX tests confirm critical fields are visible without scrolling through unrelated data, and snapshots show distinct layouts for active, blocked, and expired permits.

### 28. Assistant skill for permit drafting from site language
**Justification:** Supervisors often describe work in operational language, and the system should help translate that into a valid permit without inventing data.
**Improvement:** Add an agent skill that converts user instructions such as “pump change in decline sump after isolating panel and testing air” into a draft permit with proposed type, work area, controls, and missing-information prompts.
**Acceptance evidence:** Prompt-to-draft fixtures show the assistant extracts the right permit class and hazards, uncertain fields remain explicitly unresolved, and all mutations require user confirmation before save.

### 29. Assistant skill for incident and handover summarization
**Justification:** Shift leaders and safety coordinators need fast summaries of what changed without reading every raw note.
**Improvement:** Add a governed summarization skill that composes shift handover briefs, open-permit digests, and incident summaries with explicit source citations to permits, inspections, gas readings, and control actions.
**Acceptance evidence:** Summaries show source references, omission tests verify no unsupported claims are inserted, and users can drill from every summary statement to the underlying record.

### 30. Assistant refusal and escalation rules for unsafe requests
**Justification:** A mining assistant must never normalize bypassing safety controls or approving permits without evidence.
**Improvement:** Define refusal logic for requests such as approving without gas tests, closing incidents without findings, ignoring competency gaps, or reactivating suspended permits without rechecks. Escalate such requests to named human roles with a preserved audit trail.
**Acceptance evidence:** Safety-violation prompt tests show the assistant refuses and explains the missing controls, escalations are recorded, and no prohibited command reaches the datastore.

### 31. Event model expanded to domain milestones
**Justification:** Generic create and update events do not tell downstream systems which mining safety step actually occurred.
**Improvement:** Emit typed domain events for permit issued, permit suspended, isolation verified, confined-space entry started, gas test failed, blast cleared, handover accepted, incident classified, and regulatory pack exported.
**Acceptance evidence:** Event schema tests cover each new domain milestone, example payloads exist for consumers, and release evidence includes emitted-event inventories.

### 32. Event-sourced reconstruction of safety decisions
**Justification:** Investigations often require replaying who knew what at a given time, especially after incidents or regulator questions.
**Improvement:** Capture immutable decision events with actor, role, shift, area, source record, prior state, new state, and justification for approvals, suspensions, overrides, and closures across permits and incidents.
**Acceptance evidence:** Replay tests reconstruct the timeline of a complex permit with handover and suspension events, and investigators can retrieve point-in-time views from the audit history.

### 33. Operational anomaly detection for permit misuse
**Justification:** Repeated short-cuts such as fast approvals, missing evidence, and unusual after-hours activity should surface before they lead to incidents.
**Improvement:** Add anomaly scoring for patterns such as permits approved too quickly, recurrent use of the same override reason, repeated late gas tests, unusual explosives activity windows, and repeated suspensions in one area.
**Acceptance evidence:** Anomaly cards appear in the workbench with contributing signals, review actions can confirm or dismiss the anomaly, and feedback changes future scoring behavior.

### 34. Continuous control testing of safety rules
**Justification:** A release can pass and still fail operationally if policy enforcement quietly drifts.
**Improvement:** Create automated control assertions that continuously test for expired permits still marked active, confined-space entries lacking current gas tests, blasting permits without exclusion evidence, and closed incidents missing corrective-action closure.
**Acceptance evidence:** Failing control assertions open exceptions automatically, dashboards show pass and fail rates by control family, and tests prove assertions run against realistic data.

### 35. Policy rule workbench for safety governance
**Justification:** Safety teams need to change thresholds and checklists with traceability, not by editing code or undocumented data.
**Improvement:** Add a governance UI for rule creation, approval, activation date, supersession, and rollback of permit, gas-testing, competency, ground-control, and explosives rules.
**Acceptance evidence:** Rule changes require approval, previous versions remain inspectable, and simulation outputs show the effect of a pending rule before activation.

### 36. Runtime parameter controls for operational thresholds
**Justification:** Some thresholds change operationally, such as retest intervals, escalation timers, and dashboard warning windows.
**Improvement:** Separate policy rules from runtime parameters and manage parameters for gas-test validity, handover reminder timing, incident escalation windows, evidence export retention, and stale-permit warnings with approval and rollback support.
**Acceptance evidence:** Parameter edits are audited, invalid values are rejected, and the system shows which permits or dashboards depend on each parameter.

### 37. Offline-capable field capture for inspections and gas tests
**Justification:** Mines often have poor connectivity underground or at remote pits, but inspections and gas readings still need accurate capture.
**Improvement:** Support offline entry of inspections, gas tests, control verifications, and permit acknowledgements with local timestamps, device identity, later synchronization, and conflict resolution rules.
**Acceptance evidence:** Offline submissions sync successfully when connectivity returns, conflicts are surfaced for human review, and tests cover duplicate or delayed sync events.

### 38. Attachment and evidence provenance handling
**Justification:** Photos, sketches, permits, and analyzer screenshots lose value if the system cannot prove where they came from or what record they support.
**Improvement:** Add attachment provenance fields for device, uploader, captured-at time, related area, evidence type, and tamper-evident hashing. Link each artifact to permit steps, inspections, incidents, or regulatory submissions.
**Acceptance evidence:** Evidence objects retain provenance metadata, export packs include hashes and source linkage, and the UI differentiates required evidence from optional reference material.

### 39. Rescue readiness checks for confined-space and high-risk work
**Justification:** Confined-space entry and certain underground tasks are unsafe if rescue arrangements are assumed rather than confirmed.
**Improvement:** Require rescue planning fields for standby person, communication method, retrieval equipment, route to casualty, emergency response team availability, and nearest refuge or muster location where applicable.
**Acceptance evidence:** High-risk permits cannot activate until rescue readiness is complete, rescue plan evidence is visible in the detail view, and tests cover unavailable-rescue-team scenarios.

### 40. Stop-work authority and rapid suspension controls
**Justification:** The system should make it easy to stop unsafe work immediately when conditions change.
**Improvement:** Add a stop-work action that any authorized supervisor or safety role can use to suspend active permits, capture the trigger reason, notify affected crews, and require formal revalidation before restart.
**Acceptance evidence:** Stop-work actions are available from active permit views, notifications and events are emitted immediately, and suspended permits remain blocked until revalidation evidence is complete.

### 41. Cross-shift analytics for recurring hazards
**Justification:** Hazard patterns become visible only when the system compares multiple shifts, areas, and crews over time.
**Improvement:** Add analytics for repeated gas exceedances, recurring ground defects, repeated permit extensions, incident concentration by area, unresolved corrective actions, and frequent handover breakdowns.
**Acceptance evidence:** The analytics workbench exposes trend lines and drill-downs, queries are backed by tested projections, and operational KPI change events update the right panels.

### 42. Scenario simulation for permit and blasting decisions
**Justification:** Supervisors need a safe way to explore “what if we delay the blast” or “what if ventilation is down for two hours” before changing live work.
**Improvement:** Provide simulation tools for blast rescheduling, permit extension, shift reduction, area closure, and ventilation degradation that estimate conflicts, expired gas tests, handover impact, and productivity disruption.
**Acceptance evidence:** Simulations run without mutating live data, comparison outputs show impacted permits and controls, and regression tests verify core scenarios produce stable results.

### 43. Dead-letter and retry handling for safety events
**Justification:** Lost or stuck events can hide a suspended permit, a failed control assertion, or a missing regulatory export.
**Improvement:** Build an operational console for failed event deliveries with reason, retry count, payload summary, affected record, and safe replay controls for safety-critical event types.
**Acceptance evidence:** Dead-letter records are visible in the workbench, replay operations are audited, and tests confirm idempotent processing after retry.

### 44. Multi-tenant and site isolation of safety data
**Justification:** Shared platforms for multiple mines or contractors must prevent one tenant from seeing another tenant’s permits, incidents, or rule sets.
**Improvement:** Enforce tenant and site scoping across records, queries, events, assistant context, analytics, and exports, with explicit policy separation for local rule overlays and release evidence.
**Acceptance evidence:** Negative-access tests fail across tenant boundaries, event consumers receive only authorized tenant data, and UI filters do not leak cross-tenant counts.

### 45. Competency-driven approval routing
**Justification:** Approval chains should reflect the risk of the work, the area, and the permit class rather than a single fixed reviewer list.
**Improvement:** Route approvals dynamically based on hazard profile so that electrical isolation may need an authorized electrician, a blast permit requires a shotfirer or blasting engineer, and a ground-control deviation requires geotechnical review.
**Acceptance evidence:** Routing tests show different permit types produce different approval chains, routing decisions are explained in the UI, and overrides require recorded justification.

### 46. Formal release evidence for safety-critical changes
**Justification:** Changes to permit workflows, rules, or control logic need stronger release proof than ordinary CRUD features.
**Improvement:** Expand `RELEASE_EVIDENCE.md` expectations to include rule-diff summaries, high-risk workflow test results, event compatibility checks, UI evidence for blocked unsafe actions, and sample regulatory pack exports.
**Acceptance evidence:** Release evidence artifacts include the mandated sections for a mining-safety change, and a release checklist fails when those artifacts are missing.

### 47. Safety-focused contract and integration tests
**Justification:** Mining-specific logic is brittle if tests only cover endpoint success and generic validation failures.
**Improvement:** Add contract tests for permit APIs, integration tests for shift handover plus active permits, scenario tests for gas-test expiry, and end-to-end tests for confined-space, blasting, and isolation workflows.
**Acceptance evidence:** Test suites explicitly name mining scenarios, failing cases prove unsafe transitions are blocked, and CI output demonstrates the safety-critical paths are exercised.

### 48. Audit proof chain for evidence integrity
**Justification:** When evidence is challenged, the system should prove that attachments, readings, and approvals were not altered after the fact.
**Improvement:** Hash and chain critical evidence artifacts and decision events so exported proof manifests can show integrity for permit approvals, gas tests, blast clearances, and incident closures without exposing unnecessary content.
**Acceptance evidence:** Proof verification succeeds for unchanged records, tampering tests fail as expected, and exported manifests list the chained artifacts included in the proof set.

### 49. Domain training sandbox and seeded walkthroughs
**Justification:** Safety systems are only effective when supervisors, safety officers, and planners can learn the workflows without touching live operations.
**Improvement:** Provide seeded scenarios covering a confined-space pump repair, a highwall scaling job, an underground electrical isolation, a production blast, and an incident investigation, each with realistic data and guided assistant prompts.
**Acceptance evidence:** Seeded walkthroughs load reproducibly, trainees can complete scenario-specific tasks, and the sandbox remains isolated from production records and analytics.

### 50. Operational readiness review before go-live
**Justification:** A mining permit platform is not ready when code passes alone; it must prove that controls, people, evidence, and support processes are ready for live use.
**Improvement:** Define a go-live readiness gate covering configured rule sets, validated site overlays, trained approvers, tested event handlers, reviewed dashboards, approved release evidence, and incident-response ownership for the PBC.
**Acceptance evidence:** A readiness checklist can be completed from package artifacts, unresolved readiness gaps block release, and final signoff records identify who approved the production launch of the PBC.
