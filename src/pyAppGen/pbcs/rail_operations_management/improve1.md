# Rail Operations Management Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `rail_operations_management`.
- Manifest description: train plans, consists, track windows, yards, crews, incidents, and rail service performance.
- Existing APIs in scope: `POST /train-plans`, `POST /consists`, `POST /track-windows`, `POST /yard-moves`, `POST /crew-assignments`, and `GET /rail-operations-management-workbench`.
- Existing tables in scope: `train_plan`, `consist`, `track_window`, `yard_move`, `crew_assignment`, `rail_incident`, `service_performance`, `rail_operations_management_policy_rule`, `rail_operations_management_runtime_parameter`, `rail_operations_management_schema_extension`, `rail_operations_management_control_assertion`, and `rail_operations_management_governed_model`.
- Existing emitted events in scope: `RailOperationsManagementCreated`, `RailOperationsManagementUpdated`, `RailOperationsManagementApproved`, and `RailOperationsManagementExceptionOpened`.
- Existing consumed events in scope: `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Existing UI fragments in scope: `RailOperationsManagementWorkbench`, `RailOperationsManagementDetail`, and `RailOperationsManagementAssistantPanel`.

### 1. Train graph and pathing baseline
**Justification:** A train plan is only operationally credible if every planned movement is anchored to a line, direction, junction path, and allowable route rather than a loose origin-destination record.
**Improvement:** Extend `train_plan` to store route graph references, line segments, running direction, ruling gradients, loop availability, and alternative paths so planners can distinguish preferred paths from diversionary paths before the day-of-operation.
**Acceptance evidence:** Schema and API examples show route graph identifiers on `POST /train-plans`, validation rejects impossible segment orderings, and the workbench renders the planned path with primary and fallback routes.

### 2. Public timetable versus operating timetable separation
**Justification:** Passenger service recovery and freight prioritization break down when the same timetable field is used for public promises, internal pathing, and control-office working times.
**Improvement:** Add distinct timetable layers for published times, working timetable times, and control-adjusted times, including validity dates, service class, and reason codes for divergence between what passengers see and what dispatch uses.
**Acceptance evidence:** `train_plan` examples carry all three timetable layers, UI views let operators compare them side by side, and tests prove public times cannot be silently overwritten by control edits.

### 3. Headway and junction conflict validation
**Justification:** Train planning without headway rules, overlap clearance, and junction sequencing checks produces plans that look valid in CRUD terms but fail in real signaling territory.
**Improvement:** Add timetable validation rules that enforce minimum headway by signaling section, junction margins, platform reoccupation intervals, and single-line token occupancy so planners see conflicts before approval.
**Acceptance evidence:** Conflict fixtures demonstrate rejected overtakes, flat-junction clashes, and single-line meets, with the assistant and workbench showing exact blocking sections and conflict times.

### 4. Rolling stock consist version history
**Justification:** Consists change because of failures, late arrivals, and short formations, and operators need a durable history of what formation was planned, accepted, and actually dispatched.
**Improvement:** Turn `consist` into a versioned structure that records locomotive class, vehicle order, brake type, coupler compatibility, and change reason for each formation revision.
**Acceptance evidence:** `POST /consists` examples show explicit revision numbers, the detail page shows side-by-side formation diffs, and audit history reconstructs the consist active at departure time.

### 5. Rolling stock restriction matching
**Justification:** A valid consist must be compatible with route electrification, axle load, platform length, train protection equipment, and loading gauge, not just with the service code.
**Improvement:** Add rule-engine checks that match each consist against traction availability, train heating or shore supply needs, ETCS or ATP fitment, maximum trailing load, and route class restrictions.
**Acceptance evidence:** Validation evidence shows rejected diesel-on-electric-only paths, overlength passenger formations, and overweight freight consists, with rule outputs pointing to the exact restriction that failed.

### 6. Crew district and boundary handoff model
**Justification:** Crew assignments are domain-deep only when the system understands depots, signing-on points, route knowledge districts, and mandatory relief boundaries.
**Improvement:** Expand `crew_assignment` to model driver and conductor districts, handover stations, taxi or van links, relief windows, and which crew leg owns the train between each boundary point.
**Acceptance evidence:** A sample service crossing multiple districts shows legal handoffs in the UI, the API rejects assignments that cross a route-knowledge boundary without relief, and evidence traces the owning crew by segment.

### 7. Hours-of-service and fatigue legality
**Justification:** Crew legality is a safety boundary, and rail control cannot rely on manual spreadsheets to catch excessive duty lengths, missed rest, or night-shift accumulation.
**Improvement:** Add rules for sign-on, preparation time, route time, relief time, maximum continuous driving, minimum rest, meal break handling, and fatigue escalation thresholds by crew role.
**Acceptance evidence:** Tests cover late-running extensions, rescue duties, and relief failures, while the workbench shows remaining legal time and blocks new assignments once thresholds are crossed.

### 8. Dispatch movement authority board
**Justification:** Dispatchers need a single operational board that shows which trains are planned, ready, signaled, departed, delayed, held, or terminated instead of hunting across separate train and incident records.
**Improvement:** Build a dispatch board projection that combines `train_plan`, `consist`, `crew_assignment`, `track_window`, and `rail_incident` into movement authority states with train-ready checks and hold reasons.
**Acceptance evidence:** `GET /rail-operations-management-workbench` returns dispatch-board data, state transitions are evented, and UI filters allow controllers to view trains awaiting path, crew, stock, or possession clearance.

### 9. Track possession and engineering window integration
**Justification:** A train plan is not executable unless it knows where engineering possessions, line blocks, and worksite limits intersect the path and planned passage times.
**Improvement:** Expand `track_window` from a generic window table into possession records carrying section limits, blocked tracks, worksite authority, isolation status, pilotman requirements, and affected timetable paths.
**Acceptance evidence:** Possession examples show exact milepost or signal limits, planning validation flags trains through blocked sections, and the workbench can list every affected service by possession window.

### 10. Temporary speed restriction handling
**Justification:** Control offices recover service differently when delay comes from a possession closure versus a temporary speed restriction, so the timetable model must represent both.
**Improvement:** Add temporary speed restriction objects tied to route sections, effective times, maximum allowed speed, and reason codes, then use them to recompute section running times and knock-on delay exposure.
**Acceptance evidence:** Scenario tests show revised running times under TSRs, dispatch views highlight trains affected in the next operating horizon, and release evidence contains rule outputs for recalculated timings.

### 11. Signaling and block occupancy constraints
**Justification:** Dispatch decisions must respect block section occupancy, overlap release, approach locking, and single-line staff or token rules, not just timetable arithmetic.
**Improvement:** Introduce signaling-constraint metadata in planning and dispatch projections so a controller sees when a planned move is blocked by occupied sections, overlap protection, or direction-of-traffic restrictions.
**Acceptance evidence:** Simulations demonstrate blocked dispatch where signaling clearance is impossible, UI cards cite the signaling constraint, and event history captures when the block condition cleared.

### 12. Station call and skip-stop modeling
**Justification:** Passenger recovery frequently depends on adding, dropping, or reordering station calls, and freight services may have crew or traffic stops that should not be treated like public station calls.
**Improvement:** Model each station call with arrival, departure, dwell, call type, platform preference, commercial stop flag, operational stop flag, and skip-stop authority so dispatch and passenger service views stay aligned.
**Acceptance evidence:** The plan detail shows ordered station calls with reasons for omitted stops, validation catches impossible dwell or turn-round times, and service-recovery actions can selectively skip calls with audit evidence.

### 13. Platform occupation and turnback logic
**Justification:** Terminal congestion and turnback failures are major sources of delay, and platform conflicts must be surfaced before controllers improvise unsafe or unworkable reversals.
**Improvement:** Add platform occupation intervals, minimum platform reoccupation gaps, shunt release times, cleaning or catering windows, and turnback dependencies between arriving and departing services.
**Acceptance evidence:** Conflict fixtures show terminal throat and platform clashes, the workbench timeline displays overlapping occupations, and recovery simulations prove revised turnbacks remain feasible.

### 14. Yard move route and authority control
**Justification:** Yard moves are not generic logistics steps; they involve shunt routes, hand points, protected zones, and limits of authority that differ from mainline dispatch.
**Improvement:** Expand `yard_move` to capture origin track, destination track, route path, foul-point protection, point-set requirements, propelling movement status, and supervising signaller or yardmaster.
**Acceptance evidence:** Yard-move records show route detail rather than free text, conflict checks reject simultaneous occupation of the same ladder or neck, and the yard UI displays active shunts with authority limits.

### 15. Last-mile shunt safety controls
**Justification:** Low-speed yard work still creates high-severity risk because of hand signals, personnel on track, and rolling stock split or join operations.
**Improvement:** Add safety checklists for ground staff confirmation, radio channel assignment, hand-signaller presence, brake continuity confirmation, and propelling movement limits before a yard move can start.
**Acceptance evidence:** Safety-critical `yard_move` commands require explicit confirmations, failed confirmations open `RailOperationsManagementExceptionOpened`, and release evidence includes completed checklist samples.

### 16. Freight train make-up and tonnage balance
**Justification:** Freight recovery depends on knowing trailing tonnage, brake force, hazardous load position, wagon order, and route limits, not just whether a train number exists.
**Improvement:** Add freight-specific consist logic for wagon order, tonnage by vehicle, hazardous commodity segregation, brake percentage, train length, trailing load by route section, and load-ready status.
**Acceptance evidence:** Freight consist scenarios reject overweight and badly marshalled trains, the UI shows tonnage and brake summaries, and incident review can reconstruct the exact make-up at departure.

### 17. Passenger formation swap management
**Justification:** Passenger fleets often swap formations at short notice, and the system must track capacity loss, dooring differences, accessibility impacts, and platform fit.
**Improvement:** Add passenger-formation swap workflows that preserve seat count, accessibility spaces, selective door operation needs, and dispatch consequences when a planned unit or coach set is replaced.
**Acceptance evidence:** Formation swap events link old and new consists, passenger impact appears on service detail pages, and acceptance tests show accurate capacity and platform-fit recalculation.

### 18. Passenger service recovery playbooks
**Justification:** Passenger disruption handling needs structured playbooks for short turns, skip-stops, split routes, and bus bridges rather than ad hoc notes in incident records.
**Improvement:** Add recovery templates tied to `rail_incident` and `train_plan` that can generate revised service patterns, passenger-facing call changes, alternative stock plans, and required approvals.
**Acceptance evidence:** Recovery scenarios show a controller selecting a playbook and producing revised train plans, call changes, and approval evidence, with every generated action traceable in event history.

### 19. Freight service recovery and path re-slotting
**Justification:** Freight recovery has different priorities from passenger recovery, including terminal slots, customer cut-offs, wagon connections, and pathing around passenger peaks.
**Improvement:** Add freight re-slotting tools that score alternative departure paths, yard hold options, re-marshalling needs, and customer-impact windows when a freight service misses its planned slot.
**Acceptance evidence:** Simulated late-freight cases produce ranked alternatives, the decision record shows why a path was selected, and service-performance projections capture cut-off protection or breach.

### 20. Delay attribution taxonomy
**Justification:** Delay data is only useful if planners can separate primary cause, reactionary cause, and shared-contributor effects across infrastructure, operator, rolling stock, crew, and external events.
**Improvement:** Extend `service_performance` and `rail_incident` with attribution categories, subcodes, reactionary links, causation confidence, and source evidence down to station-call or section-run granularity.
**Acceptance evidence:** Delay reports can roll up by category and subcode, linked incidents show primary versus reactionary delay, and audit evidence traces each attribution decision back to operational facts.

### 21. Incident command timeline
**Justification:** Major incidents evolve through reports, site protection, service decisions, and recovery milestones, and operators need one authoritative chronology rather than scattered comments.
**Improvement:** Turn `rail_incident` into a command timeline with detection time, first protection, control escalation, site attendance, recovery estimate, partial reopening, and full closure milestones.
**Acceptance evidence:** Incident detail pages show ordered milestone cards, replay tests reconstruct the same timeline from events, and unresolved milestones stay visible on the dispatch board until cleared.

### 22. Safety-critical near-miss evidence
**Justification:** Near misses, SPAD-adjacent cases, wrong-route events, and worker-protection breaches demand stronger evidence preservation than ordinary service delays.
**Improvement:** Add a safety-critical incident subtype with protected attachments, witness roles, signal or route identifiers, affected trains, track-worker protection status, and mandatory review workflow.
**Acceptance evidence:** Safety incidents require higher permissions, the system records sealed evidence references after `AuditEventSealed`, and release evidence demonstrates immutable handling of sensitive incident data.

### 23. Weather and environmental operating restrictions
**Justification:** Heat, flooding, leaf fall, wind, and visibility restrictions change safe speeds, traction limits, and route availability, so they belong inside operations planning instead of outside memos.
**Improvement:** Add environmental restriction records that can lower line speeds, ban specific rolling stock, require pilot working, or cap train length or weight by route and time band.
**Acceptance evidence:** Weather-driven restrictions feed planning validation, dispatch views show active environmental controls, and scenario tests prove train timing and route eligibility adjust when restrictions apply.

### 24. Resource triage across stock, crew, and infrastructure
**Justification:** Dispatchers need to see which shortage is constraining service recovery: no stock, no legal crew, no route, no platform, or no path.
**Improvement:** Build a triage view that scores each planned service on route availability, consist readiness, crew legality, station platform availability, and possession conflict so the bottleneck is explicit.
**Acceptance evidence:** The workbench ranks constrained services by bottleneck type, triage scores update after relevant events, and tests show the top blocker changes correctly as constraints clear.

### 25. Level crossing and line block coordination
**Justification:** Certain routes depend on local crossing attendants, manual block releases, or line block clearances that are operationally different from pure signaling logic.
**Improvement:** Add route constraints for attended crossings, manual release points, line-block authorities, and local protection dependencies that must be satisfied before a dispatch move can proceed.
**Acceptance evidence:** Dispatch simulations reject moves lacking crossing or line-block clearance, the detail page shows which local authority is outstanding, and event evidence records when the clearance was granted.

### 26. Terminal throat and platform-capacity management
**Justification:** Busy terminals fail first at throats, scissors crossovers, and platform groups, so service planning must include these choke points explicitly.
**Improvement:** Add terminal-capacity models for throat occupancy, crossover conflicts, platform groups, and approach-release sequencing to prevent infeasible turnbacks and stacked arrivals.
**Acceptance evidence:** Capacity warnings appear before approval, terminal views show throat and platform contention windows, and recovery simulations demonstrate whether proposed resequencing actually fits.

### 27. Maintenance-window negotiation
**Justification:** Engineering access and traffic flow compete for the same infrastructure, and the package should support negotiated possessions rather than all-or-nothing closures.
**Improvement:** Extend `track_window` with negotiation states, partial-section availability, handback milestones, and conditional release rules so engineering and operations can stage work around train priorities.
**Acceptance evidence:** Possession records show requested, negotiated, confirmed, and handed-back states, conflict reports list trains affected by each negotiation option, and approvals capture who accepted the compromise.

### 28. Interline and cross-boundary handover
**Justification:** Rail services often cross operator, region, or control-area boundaries, and handover quality determines whether downstream controllers inherit good data or surprises.
**Improvement:** Add control-boundary handover packets covering train state, consist state, delay status, incident context, and outstanding restrictions whenever a service passes to another desk or operator.
**Acceptance evidence:** Handover records are evented, the receiving boundary can acknowledge or reject incomplete packets, and the audit trail shows the full train state handed over at each boundary.

### 29. Event-sourced train movement history
**Justification:** Performance analysis and incident review require a durable record of planned, actual, and amended movement times at each operational point.
**Improvement:** Add event-sourced train movement records for departures, arrivals, passing times, platform changes, station-call amendments, and train-graph path changes linked back to `train_plan`.
**Acceptance evidence:** Replay tests reconstruct a train's actual journey, service-performance reports derive from event history instead of mutable columns alone, and operators can view every timing change by event order.

### 30. Predictive late running and missed-connection risk
**Justification:** Controllers need forward-looking risk, not just current delay minutes, especially where passenger connections or freight terminal slots are fragile.
**Improvement:** Use `service_performance`, station-call history, environmental restrictions, and active incidents to forecast late running, missed passenger connections, and terminal slot breaches over the next operating horizon.
**Acceptance evidence:** Risk cards show predicted delay bands and key drivers, model outputs are calibrated against recent events, and controllers can trace each prediction back to observable operating inputs.

### 31. Counterfactual dispatch simulation
**Justification:** Service recovery choices should be tested before they are committed, especially when alternatives involve rerouting, skip-stopping, short-turning, or holding freight.
**Improvement:** Add simulation tools that compare multiple dispatch interventions against line capacity, crew legality, station occupancy, passenger call coverage, and freight cut-off impact.
**Acceptance evidence:** A controller can run side-by-side scenarios without mutating live records, each scenario returns quantified impacts, and accepted decisions link the chosen scenario to the resulting live changes.

### 32. Station operations timeline UI
**Justification:** Platform staff and passenger operations teams need a local view of arriving, dwelling, departing, and platform-changed services at each station.
**Improvement:** Create a station timeline in `RailOperationsManagementWorkbench` showing station calls, platform allocations, dwell variance, missed calls, crowd-risk flags, and immediate turnaround dependencies.
**Acceptance evidence:** Station views filter by location and time horizon, platform changes and skipped calls are highlighted, and UI tests confirm operators can trace a disrupted platform sequence without opening raw records.

### 33. Corridor dispatcher UI
**Justification:** Dispatchers need a corridor-first operational picture rather than a generic list page if they are to manage junctions, headways, and possessions effectively.
**Improvement:** Add a corridor board with line diagrams, active train order, conflicting movements, possession overlays, and train-ready blockers so corridor dispatch can work directly from the package.
**Acceptance evidence:** Workbench routes support corridor selection, live corridor cards explain why a train cannot yet move, and screenshot evidence shows line diagrams aligned with current train sequence data.

### 34. Yardmaster UI
**Justification:** Yard operations have different mental models from mainline dispatch and need track occupancy, rake position, and shunt conflict visibility.
**Improvement:** Add a yardmaster workspace that shows receiving roads, departure roads, locomotive positions, planned shunts, blocked points, and unsafe route conflicts for each yard area.
**Acceptance evidence:** Yard screens show track occupancy by road, active shunt authority by movement, and validation prevents two planned moves from fouling the same road at the same time.

### 35. Incident commander UI
**Justification:** Incident handling needs dedicated views for chronology, impacted services, protection state, and recovery options rather than overloading the generic detail screen.
**Improvement:** Build an incident command view with milestone timeline, affected train list, service recovery candidates, possession implications, attachment inventory, and escalation status.
**Acceptance evidence:** Incident detail routes show command-specific widgets, major incidents list all impacted trains and restrictions, and UI tests prove no critical incident action is hidden behind generic forms.

### 36. Release evidence for safe timetable and dispatch changes
**Justification:** Rail operations changes need release proof that rules, simulations, and regressions were checked before new planning or dispatch logic reaches users.
**Improvement:** Expand `RELEASE_EVIDENCE.md` expectations to include timetable-conflict regression results, signaling constraint tests, possession overlap checks, yard safety checklist verification, and incident replay integrity.
**Acceptance evidence:** Release packages contain explicit rail-operational test outputs, evidence links to event schemas and UI screenshots, and a reviewer can prove the release covered planning, dispatch, yard, and incident paths.

### 37. Agent skill for timetable amendment intake
**Justification:** Control offices receive amendment instructions in notices, circulars, and free text, and the assistant should convert them into safe draft timetable changes instead of plain summaries.
**Improvement:** Add an assistant skill that extracts amended times, affected trains, station-call changes, route restrictions, and validity windows from documents and prepares draft `train_plan` amendments with citations.
**Acceptance evidence:** Assistant previews show source spans for every proposed change, low-confidence extractions stay in review, and accepted drafts become governed commands rather than direct database edits.

### 38. Agent skill for consist repair suggestions
**Justification:** When rolling stock fails, operators need practical recovery options such as short formation, stock swap, or train cancellation support under time pressure.
**Improvement:** Add a skill that analyzes unavailable vehicles, depot stock, route restrictions, and service obligations to propose valid consist substitutions and downstream passenger or freight impact.
**Acceptance evidence:** Skill outputs rank alternatives with operational tradeoffs, blocked options cite the restriction that failed, and accepted proposals generate auditable consist revisions.

### 39. Agent skill for incident summarization and handover
**Justification:** Shift handover quality falls when incident summaries are manual and inconsistent, especially across long disruptions with multiple partial recoveries.
**Improvement:** Add a handover skill that produces structured incident summaries covering chronology, protection state, trains still affected, next decision points, and unresolved safety conditions.
**Acceptance evidence:** Shift handover summaries reference event and attachment sources, supervisors can compare outgoing and incoming handover packets, and no summary is sent without human review when safety-critical flags are present.

### 40. Expanded rail-operational event catalog
**Justification:** The current generic event names do not convey whether the package approved a timetable change, opened a safety incident, or reassigned a consist.
**Improvement:** Add typed emitted events for train-plan validated, station-call changed, consist revised, crew handoff blocked, possession confirmed, yard move authorized, incident escalated, and recovery plan accepted.
**Acceptance evidence:** Event schemas and examples are published beside the package, consumers can subscribe to specific operational changes without payload guessing, and compatibility tests protect older subscribers.

### 41. Consumed-event handling and freshness checks
**Justification:** External policy and KPI events should change rail behavior only through traceable, idempotent handlers with explicit staleness detection.
**Improvement:** Use `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` to refresh planning rules, seal evidence states, and update service-performance thresholds while recording source event lineage and freshness age.
**Acceptance evidence:** Duplicate and out-of-order event tests pass, stale-source warnings are visible in the workbench, and every derived change links back to the consumed event that triggered it.

### 42. Release evidence for safety-critical incident handling
**Justification:** Incident workflows deserve their own release proof because service-delay tests alone do not show that safety-sensitive branches still behave correctly.
**Improvement:** Require release evidence for safety-critical incident creation, escalation, evidence sealing, restricted-permission viewing, and closure with retained chronology.
**Acceptance evidence:** Release artifacts include incident workflow traces, permission test output, sealed evidence references, and regression results for major-incident UI and event replay paths.

### 43. Synthetic scenario test pack
**Justification:** Rail operations quality improves when the package is tested against plausible operating days, not just isolated unit records.
**Improvement:** Add packaged scenarios for commuter peak disruption, freight path squeeze, station overrun, failed unit swap, overrun possession, terminal congestion, and wrong-side crew relief.
**Acceptance evidence:** The scenario suite runs end to end, each scenario exercises multiple tables and events, and outputs show whether planning, dispatch, yard, and incident projections remain internally consistent.

### 44. Policy and parameter workbench for rail rules
**Justification:** Controllers and planners need to see which operational rules are active without reading raw policy tables or code.
**Improvement:** Build a policy workbench for `rail_operations_management_policy_rule` and `rail_operations_management_runtime_parameter` covering headway thresholds, dispatch priorities, fatigue rules, possession margins, and recovery approval gates.
**Acceptance evidence:** Users can inspect active rule versions and effective dates, change previews show operational impact before approval, and audit history records who changed each live rule and why.

### 45. Richer rail data model primitives
**Justification:** Domain depth depends on naming the real objects of operation such as train IDs, service IDs, block sections, platforms, depots, yards, and control areas.
**Improvement:** Expand schemas with first-class identifiers for reporting number, service code, consist code, control area, route section, platform, yard road, depot, and incident location so records stop relying on ambiguous text fields.
**Acceptance evidence:** API payloads use typed identifiers, search and filtering work on those primitives, and migration evidence shows legacy free text mapped into controlled fields without data loss.

### 46. Multi-tenant operating rule isolation
**Justification:** Different rail operators, infrastructure managers, and control regions may share software but not dispatch rules, crew limits, or evidence access.
**Improvement:** Enforce tenant-scoped rule sets, route maps, rolling-stock catalogs, control areas, and evidence retention policies so no operator can see or execute another operator's rail decisions.
**Acceptance evidence:** Isolation tests prove tenant-specific views and rules, cross-tenant access is denied for incidents and dispatch boards, and release evidence includes negative tests for tenant leakage.

### 47. Dead-letter, replay, and operational recovery tooling
**Justification:** Event failures are operational incidents when they hide train-state, possession, or incident changes from the workbench.
**Improvement:** Add dead-letter queues and replay tools with domain-specific explanations so operators can distinguish harmless duplicates from missing movement, crew, or incident updates.
**Acceptance evidence:** The workbench exposes dead-letter reason, replay eligibility, and impacted train or incident context, with test fixtures proving safe replay and poison-message quarantine behavior.

### 48. Carbon and energy-aware dispatch choices
**Justification:** The manifest already signals carbon awareness, and rail control should use that capability in ways that respect punctuality, safety, and freight or passenger commitments.
**Improvement:** Add optional energy and carbon scoring for pathing and recovery decisions, including diesel substitution, empty-stock balancing, regenerative-braking opportunity, and unnecessary yard repositioning.
**Acceptance evidence:** Dispatch simulations can compare energy and punctuality tradeoffs, the scoring model is visible but not mandatory for safety-critical moves, and release evidence shows the feature never bypasses operational rules.

### 49. Continuous control testing for safety boundaries
**Justification:** Rail safety and control boundaries should be monitored continuously, not only during audits or after a bad dispatch decision.
**Improvement:** Use `rail_operations_management_control_assertion` to run continuous checks for crew legality, route restriction breaches, unauthorized timetable edits, possession overlap, missing evidence seals, and unreviewed safety incidents.
**Acceptance evidence:** Failing controls raise visible exceptions, control histories show pass or fail over time, and release evidence includes the latest control-run results for the modified package version.

### 50. Go-live readiness scorecard
**Justification:** A rail package should not be considered ready on the strength of CRUD completeness alone; it needs explicit proof across planning, dispatch, recovery, safety, UI, and eventing.
**Improvement:** Add a readiness scorecard that gates release on train-plan validation coverage, dispatch-board fidelity, consist and crew legality, possession integration, incident chronology completeness, agent-skill guardrails, and event-contract verification.
**Acceptance evidence:** The package ships with a scored release checklist, each score links to concrete evidence artifacts, and the final release report states whether `rail_operations_management` is fit for controlled rollout.
