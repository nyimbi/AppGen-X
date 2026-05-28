# Airport Operations Management PBC Improvement Backlog

This backlog is a hand-curated improvement set for `airport_operations_management`. It is grounded in the current manifest surfaces and focused on airport operations realities: gates, stands, runway and taxiway availability, turnaround control, ground handlers, baggage belts, passenger flows, deicing, disruption response, and airport operations center decision-making.

## Current Domain Evidence Used

- Exact PBC key: `airport_operations_management`
- Label: `Airport Operations Management`
- Description: gates, stands, slots, turnaround, baggage, passenger flows, disruptions, and airport coordination
- Owned tables: `gate_assignment`, `stand_allocation`, `slot`, `turndown_task`, `baggage_belt`, `passenger_flow`, `airport_disruption`, `airport_operations_management_policy_rule`, `airport_operations_management_runtime_parameter`, `airport_operations_management_schema_extension`, `airport_operations_management_control_assertion`, `airport_operations_management_governed_model`
- Existing APIs: `POST /gate-assignments`, `POST /stand-allocations`, `POST /slots`, `POST /turndown-tasks`, `POST /baggage-belts`, `GET /airport-operations-management-workbench`
- Existing workflows: `airport_operations_management_create_gate_assignment_workflow`, `airport_operations_management_record_stand_allocation_workflow`
- Existing UI fragments: `AirportOperationsManagementWorkbench`, `AirportOperationsManagementDetail`, `AirportOperationsManagementAssistantPanel`
- Existing emitted events: `AirportOperationsManagementCreated`, `AirportOperationsManagementUpdated`, `AirportOperationsManagementApproved`, `AirportOperationsManagementExceptionOpened`
- Existing consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- Existing advanced capabilities already declared in the manifest include event-sourced operational history, predictive risk scoring, counterfactual simulation, continuous control testing, and governed AI agent execution

### 1. Gate and stand compatibility matrix with operational constraints
**Justification:** Gate assignment quality depends on more than aircraft size. Contact stand fit, wingtip clearance, jet bridge geometry, customs segregation, Schengen or non-Schengen handling, towbarless pushback compatibility, and overnight parking rules all affect whether an assignment is operationally valid.
**Improvement:** Model a first-class compatibility matrix across `gate_assignment` and `stand_allocation` for aircraft family, wingspan code, domestic or international processing, bussing requirements, hydrant fuel access, PCA or GPU availability, and adjacent stand shadow restrictions.
**Acceptance evidence:** Rule fixtures covering narrowbody, widebody, remote-stand, and international-arrival scenarios; rejected assignments with machine-readable reasons; workbench views that show why a stand is usable, blocked, or conditionally available.

### 2. Turnaround milestone graph instead of flat task tracking
**Justification:** A turnaround is a dependency network, not a checklist. Boarding, fuelling, catering, cabin cleaning, baggage offload, load sheet completion, and pushback readiness each block different downstream steps.
**Improvement:** Upgrade `turndown_task` into a turnaround milestone graph with planned, estimated, actual, and predicted timestamps for on-block, first bag, fuelling complete, cleaning complete, boarding start, doors closed, and off-block.
**Acceptance evidence:** Dependency-chain tests for short-haul and long-haul turns; critical-path highlighting in `AirportOperationsManagementWorkbench`; exception cards showing which milestone is driving estimated departure delay.

### 3. Runway and taxiway availability as decision inputs for stand and gate plans
**Justification:** Gate and stand plans become misleading when runway closures, taxiway work, reduced visibility procedures, or hot-spot restrictions are not reflected in the same operating view.
**Improvement:** Add a runway and taxiway status model that feeds arrival sequencing, expected taxi-in or taxi-out times, preferred stand zones, and departure release risk into the `airport_operations_management` workbench.
**Acceptance evidence:** Simulated runway closure and taxiway restriction scenarios that alter stand recommendations; visible status timeline for open, constrained, and closed surfaces; replay evidence linking a stand decision to the surface state in effect at decision time.

### 4. Remote stand bussing orchestration
**Justification:** Remote stands are only usable if bus capacity, gate lounge readiness, and dispatch timing all line up. Without that coupling, the system can claim capacity that does not exist.
**Improvement:** Extend `stand_allocation` to account for bussing demand, bus fleet assignment windows, passenger boarding gate pairing, and minimum dispatch lead times for remote operations.
**Acceptance evidence:** Allocation tests showing remote-stand rejection when buses are exhausted; paired gate-to-stand visual links in the workbench; release evidence for bus scheduling conflicts detected before dispatch.

### 5. Multi-aircraft ramp system and swing-gate handling
**Justification:** Many airports rely on MARS stands and swing gates that can host one widebody or multiple narrowbodies depending on adjacent occupancy. Static one-aircraft-per-stand logic leaves revenue and resilience on the table.
**Improvement:** Support conditional split and merge behavior for MARS stands, swing gates, and dual boarding bridge layouts, including adjacency rules and turnaround overlap constraints.
**Acceptance evidence:** Scenario tests for one-widebody versus two-narrowbody stand usage; live occupancy visualization of merge and split states; audit trail entries that show when a stand topology changed and why.

### 6. Deicing queue, pad, and fluid capacity control
**Justification:** Winter operations fail first at the edges: deicing pad saturation, Type I or Type IV fluid shortage, queue length, and holdover window expiry. Departure planning needs those facts, not separate spreadsheets.
**Improvement:** Add deicing resources to the `airport_disruption` and turnaround model, including pad assignments, queue position, fluid inventory thresholds, holdover countdowns, and return-for-repeat-deicing workflows.
**Acceptance evidence:** Winter-ops simulations that force deicing queue formation; alerts when predicted holdover time expires before takeoff; resource dashboards showing pad occupancy and fluid burn versus stock on hand.

### 7. Apron works, stand closures, and maintenance possession management
**Justification:** Stand availability often changes hour by hour because of pavement work, lighting defects, FOD cleanup, or equipment maintenance. A static availability flag is not credible for live allocation.
**Improvement:** Add time-bounded stand closure windows, partial apron possession zones, and degraded-capacity states to `stand_allocation`, with effectivity times and operational notes that propagate to assignment logic.
**Acceptance evidence:** Time-windowed tests where a stand is valid before works start and blocked after; map or list rendering of closure periods in the workbench; event history showing when capacity was reduced, restored, or overridden.

### 8. Ground handler capability and roster awareness
**Justification:** A turnaround can be technically assigned yet operationally impossible if the contracted handler lacks trained staff, required equipment, or active roster coverage for that aircraft type and service package.
**Improvement:** Model handler capability by airline, aircraft type, service scope, shift, and ramp zone so that `turndown_task` planning reflects who can actually perform fuelling coordination, loading, cleaning, PRM service, and dispatch support.
**Acceptance evidence:** Assignment tests that fail when a handler is out of scope or off shift; queue views grouped by handler load; operational reports showing unserved turns prevented before aircraft arrival.

### 9. Baggage make-up and reclaim synchronization
**Justification:** Belt planning is two-sided. Departure make-up belts and arrival reclaim belts compete for conveyor and pier capacity, and changes on one side can starve the other.
**Improvement:** Deepen `baggage_belt` to model make-up position, reclaim belt allocation, early-bag storage dependency, odd-size belt routing, and belt-to-flight sequencing across arrival and departure waves.
**Acceptance evidence:** Conflict tests for overlapping reclaim and make-up demand; belt occupancy timelines; visible reroute recommendations when a belt outage or overflow condition occurs.

### 10. Passenger flow segmentation across terminal processes
**Justification:** Passenger flow is not one queue. Originating, transfer, transit, international arrival, domestic arrival, crew, and PRM travelers consume different resources and can bottleneck different parts of the terminal.
**Improvement:** Expand `passenger_flow` to represent check-in, bag drop, security, outbound immigration, transfer security, inbound immigration, reclaim, customs, arrivals hall, and gate holdroom populations separately.
**Acceptance evidence:** Segment-specific throughput and dwell metrics; forecasts that highlight which process will breach capacity first; evidence that gate changes update downstream passenger routing assumptions.

### 11. Holdroom saturation and boarding readiness controls
**Justification:** Gate selection is poor if it ignores holdroom size, nearby restroom capacity, family-travel demand, or the likelihood of spillback into a concourse during a delay.
**Improvement:** Add holdroom occupancy forecasts and boarding readiness status to gate planning so the system can avoid assigning a full long-haul departure to an undersized lounge at the same time as nearby departures.
**Acceptance evidence:** Boarding-bank simulations with capacity warnings; workbench badges for low, medium, and critical holdroom congestion; post-event replay showing whether predicted saturation matched actual counts.

### 12. PRM, unaccompanied minor, and special assistance routing
**Justification:** Special-assistance flows are safety and service commitments, not optional annotations. Gate changes, bussing, remote stands, and late connections can all break those commitments.
**Improvement:** Add assisted-travel indicators to `passenger_flow` and `turndown_task` so that gate and stand decisions account for wheelchair transfer time, lift availability, escort staffing, and minimum handoff windows.
**Acceptance evidence:** Cases where remote-stand assignment is blocked for insufficient assisted-travel support; queue views of open assistance obligations; exception evidence tied to missed or delayed PRM handoffs.

### 13. Aircraft towing and reposition planning
**Justification:** Stand utilization improves only if towing moves are planned with tug availability, licensed driver coverage, push or pull route restrictions, and occupancy windows in mind.
**Improvement:** Add tow-leg entities and route feasibility checks to `stand_allocation`, including pre-tow readiness, tug assignment, tow corridor restrictions, and post-tow stand release timing.
**Acceptance evidence:** Towed-turn scenarios that free contact stands for later departures; alerts for impossible tow chains; workbench playback showing whether the system protected the tow path from conflicting stand use.

### 14. Fuel, GPU, PCA, and hydrant service compatibility
**Justification:** A stand may appear open but still be unsuitable if it lacks fuel hydrant access, fixed electrical power, pre-conditioned air, or safe hose routing for the assigned aircraft and turnaround duration.
**Improvement:** Extend gate and stand rules to include hydrant service, tanker-only access, GPU and PCA availability, and equipment conflicts that affect boarding comfort, fuel timing, and engine start readiness.
**Acceptance evidence:** Compatibility decisions exposed alongside stand recommendations; rejected assignments for missing services; turnaround timelines showing service deficiencies as direct delay causes.

### 15. Cleaning, catering, water, lavatory, and waste sequencing
**Justification:** These services compete for door access, equipment position, and ramp clearance. Modeling them independently misses the resource choreography that drives actual turn performance.
**Improvement:** Represent service windows, mutually exclusive tasks, and service-vehicle access constraints inside `turndown_task`, with configurable sequencing rules by aircraft type and airline handling standard.
**Acceptance evidence:** Critical-path calculations that change when one service slips; workbench swimlanes for service-provider activity; operational evidence for blocked turns caused by incompatible task overlap.

### 16. Slot, TOBT, TSAT, CTOT, and A-CDM reconciliation
**Justification:** Departure predictability depends on keeping local turnaround facts aligned with network slot constraints and collaborative decision-making milestones.
**Improvement:** Upgrade `slot` handling to reconcile scheduled off-block, target off-block, target start-up approval, and calculated takeoff constraints, with explicit mismatch reasons and resynchronization actions.
**Acceptance evidence:** Scenarios where a late inbound changes TOBT and cascades to TSAT or CTOT; mismatch dashboards in the workbench; release evidence showing reduced manual phone coordination during peak banks.

### 17. Diversion, air return, and recovery playbooks
**Justification:** Diversions and return-to-stand events are where airport operations systems either prove themselves or collapse into ad hoc coordination.
**Improvement:** Add structured playbooks in `airport_disruption` for diversion acceptance, stand recovery, passenger containment, baggage intercept, crew transport, and terminal resource reassignment.
**Acceptance evidence:** Replayable disruption timelines for diversion and air-return events; checklists completed in sequence; measured recovery time from event open to stable stand plan.

### 18. Safety inspection and FOD evidence capture
**Justification:** Stand availability decisions are only defensible if apron inspections, FOD findings, lighting defects, and stand-entry restrictions can be tied directly to the operational state.
**Improvement:** Add safety inspection records and evidence attachments to `airport_operations_management_control_assertion`, linking each stand or ramp-zone clearance state to the inspection that justified it.
**Acceptance evidence:** Inspection-to-stand traceability; rejected assignments when inspection validity expires; mobile-friendly evidence capture with timestamp, location, and inspector identity preserved in the audit trail.

### 19. Weather, lightning, wind, and low-visibility operating states
**Justification:** Weather disrupts different resources in different ways. Lightning stops ramp work, strong wind removes stairs or bridge usage options, and low visibility changes taxi spacing and stand preferences.
**Improvement:** Add weather-triggered operating states that affect ground handling, deicing demand, pushback timing, remote-stand viability, and terminal processing assumptions across the workbench.
**Acceptance evidence:** Test cases for lightning stop, strong crosswind, and LVP conditions; operational cards that explain which actions are blocked and for how long; replay evidence showing state changes during weather events.

### 20. Winter readiness with deicing stock and crew visibility
**Justification:** Knowing that deicing is required is not enough. Airports need to know whether the trained crews, trucks, pads, and fluid stocks exist to meet the demand curve.
**Improvement:** Add winter-readiness views to `AirportOperationsManagementWorkbench` showing fluid inventory, truck availability, crew shifts, predicted deicing demand by wave, and recovery posture after overnight weather.
**Acceptance evidence:** Pre-peak readiness snapshots; threshold alerts for low stock or insufficient crews; historical evidence comparing forecast versus actual deicing demand during a weather event.

### 21. Gate change impact visualization
**Justification:** A gate change is never just a gate change. It affects passengers already walking, airlines printing updates, baggage tug routes, PRM escorts, lounge staffing, and nearby departures.
**Improvement:** Add an impact panel that shows immediate and downstream consequences of a proposed `gate_assignment` change before it is approved.
**Acceptance evidence:** Decision previews with affected flights, belts, passenger counts, and service tasks; after-action evidence confirming whether the approved gate change reduced or increased disruption spread.

### 22. Aircraft substitution propagation
**Justification:** Last-minute aircraft swaps break assumptions about stand fit, fuel, boarding bridges, baggage volume, and cleaning duration. The system needs to re-evaluate everything that depended on the original aircraft.
**Improvement:** Add substitution handling that recalculates gate compatibility, turnaround milestones, baggage capacity, and passenger process demand when the inbound or outbound aircraft type changes.
**Acceptance evidence:** Swap scenarios for narrowbody-to-widebody and widebody-to-narrowbody substitutions; automatic reopening of dependent checks; visible before and after comparisons in the detail view.

### 23. Late-inbound recovery engine for turnaround resilience
**Justification:** Most departure delay minutes start with a late arrival. Recovery quality depends on quickly identifying which tasks can compress, which cannot, and when a gate or stand move becomes the better option.
**Improvement:** Add recovery suggestions for `turndown_task` that estimate schedule regain from task resequencing, stand moves, bus boarding, handler reassignment, or selective service reductions approved by policy.
**Acceptance evidence:** Recovery recommendations ranked by minutes saved and operational risk; measured comparison between suggested versus actual recovery outcomes; explicit policy blocks on unsafe compression options.

### 24. Airport operations center command board
**Justification:** Airport coordination needs one shared command view. Separate screens for stands, gates, belts, and disruptions force operators to reconstruct the situation manually.
**Improvement:** Expand `GET /airport-operations-management-workbench` into an airport operations center board with stand occupancy, runway state, departure bank health, belt status, top disruptions, and action-needed queues.
**Acceptance evidence:** Persona-based views for stand planner, turnaround controller, terminal duty manager, and supervisor; latency and freshness indicators on each panel; acceptance sessions with real operating scenarios.

### 25. Stand and gate conflict simulation before approval
**Justification:** Conflicts are easier to prevent than to unwind. Operators need pre-approval simulation that sees adjacency, towing dependencies, downstream baggage consequences, and passenger routing impacts.
**Improvement:** Add non-mutating simulation around `gate_assignment` and `stand_allocation` changes so planners can test proposed reallocations without disturbing the live operational picture.
**Acceptance evidence:** Side-by-side plan comparison for current versus proposed allocations; conflict counts with severity; evidence that simulated conflicts match actual rules enforced at approval time.

### 26. Belt outage and baggage contingency routing
**Justification:** Conveyor and reclaim failures are common high-impact events. The system should help operators preserve service and safety while minimizing passenger confusion and bag misroutes.
**Improvement:** Add contingency routing for `baggage_belt` failures, including alternate reclaim belts, delayed-bag holding, make-up relocation, and customer-information triggers when reclaim points change.
**Acceptance evidence:** Outage drills where bags are rerouted without orphaned records; reclaim-change notifications visible in the workbench; post-event replay showing belt outage duration and recovery actions.

### 27. Arrival and departure bank heatmaps
**Justification:** Wave pressure is easier to manage when peaks are visible. Operators need to see where gate scarcity, baggage stress, immigration crowding, and turnaround overlap will converge.
**Improvement:** Add time-phased heatmaps for stands, gates, belts, passenger processes, and handler load across the day, with drill-through to the records driving each hotspot.
**Acceptance evidence:** Forecast-versus-actual overlays for one operating day; hotspot drill-downs that lead to the responsible flights and resources; release evidence that planners used the heatmaps to preempt at least one conflict class.

### 28. Terminal resource closure and queue redirection planning
**Justification:** Security lane, immigration desk, check-in island, or corridor closures can invalidate otherwise sound gate and stand plans by changing where passengers can actually flow.
**Improvement:** Expand `passenger_flow` and disruption handling to represent terminal resource outages and the redirection logic needed to keep passengers moving to the correct process points.
**Acceptance evidence:** Queue model tests for partial terminal closures; visible reroute plans by passenger segment; evidence that gate and boarding timing recommendations change when terminal resources are constrained.

### 29. Landside to airside dependency view
**Justification:** Missed departures often start landside with bag-drop congestion, road access disruption, or check-in staffing shortfalls, not at the aircraft. The workbench should expose that chain.
**Improvement:** Add dependency views linking landside arrival pressure, check-in throughput, bag-drop backlog, security queue length, and gate readiness so controllers can see whether a late departure is terminal-driven or stand-driven.
**Acceptance evidence:** Cases where the primary delay driver is correctly attributed to landside pressure; cross-panel indicators in the workbench; historical reports showing recurrent weak points by process.

### 30. Airline and ground-handler SLA scoreboard
**Justification:** Airports need objective visibility into whether airlines and handlers are meeting turnaround, baggage, dispatch, and recovery obligations by station, wave, and aircraft type.
**Improvement:** Add SLA measurement across `turndown_task`, `baggage_belt`, and disruption workflows, including on-time service starts, completion against planned windows, exception aging, and recovery responsiveness.
**Acceptance evidence:** Scorecards by handler and airline; drill-down from SLA breach to task-level evidence; release evidence showing repeated breach patterns detected without manual spreadsheet compilation.

### 31. Delay code capture with evidence and causal hierarchy
**Justification:** Delay coding is often low quality because it happens after the fact. Reliable reporting requires evidence captured close to the event and a consistent causal model.
**Improvement:** Add structured delay-cause capture to `airport_disruption` and turnaround records, with primary and contributing causes, supporting timestamps, and links to the tasks or resource constraints that drove the delay.
**Acceptance evidence:** Delay records with evidentiary timestamps and linked milestones; validation rules preventing contradictory codes; reports that roll delay minutes up by root cause and contributing factor.

### 32. Event boundary hardening for airport operations integrations
**Justification:** Airport operations touches AODB, RMS, baggage systems, common-use platforms, and collaborative decision-making feeds. Boundary confusion creates duplicate updates and ownership disputes.
**Improvement:** Define explicit command, read-model, and event boundaries for `airport_operations_management`, including which changes are authoritative locally, which are mirrored, and which must be consumed as external facts.
**Acceptance evidence:** Event contracts that distinguish internal lifecycle events from imported status changes; idempotency tests on repeated inbound messages; architectural evidence that no shared external table is treated as owned state.

### 33. API expansion for search, simulation, and recovery operations
**Justification:** The current API set is creation-heavy. Real airport users also need search, availability checks, validation-only calls, simulation endpoints, and operational recovery commands.
**Improvement:** Extend the public surface around `POST /gate-assignments`, `POST /stand-allocations`, `POST /slots`, `POST /turndown-tasks`, and `POST /baggage-belts` with query, simulation, conflict-check, and resolution endpoints that support live control-room work.
**Acceptance evidence:** Route contracts for validation-only and simulation modes; example payloads for search and recovery actions; acceptance tests showing that non-mutating requests produce the same rule outcomes as mutating approvals.

### 34. Idempotent inbound feed handling for operational updates
**Justification:** Flight updates arrive repeatedly, out of order, and from multiple feeds. Without disciplined idempotency and ordering rules, controllers lose trust in the operational picture.
**Improvement:** Strengthen inbound update handling so that repeated stand, slot, belt, and disruption messages can be safely deduplicated, sequenced, quarantined, or replayed without corrupting the domain state.
**Acceptance evidence:** Duplicate and out-of-order message tests; dead-letter visibility for malformed updates; replay proofs that the same feed produces the same final state after reprocessing.

### 35. Assistant skill for disruption brief generation
**Justification:** During irregular operations, supervisors need fast, accurate narrative briefs for the current situation, likely next bottlenecks, and recommended containment actions.
**Improvement:** Add a governed skill in `AirportOperationsManagementAssistantPanel` that summarizes active `airport_disruption` records, stand congestion, belt outages, weather constraints, and recovery priorities for the next operating window.
**Acceptance evidence:** Briefs that cite the underlying records and timestamps; blocked responses when confidence is too low; reviewer feedback showing the skill is useful without inventing facts.

### 36. Assistant skill for gate and stand decision rationale
**Justification:** Operators should be able to ask why a gate or stand was chosen or rejected and get an answer tied to actual rules, resource states, and policy constraints.
**Improvement:** Add an explanatory skill that answers allocation questions using `gate_assignment`, `stand_allocation`, rule results, runway status, passenger-flow load, and adjacent-stand constraints.
**Acceptance evidence:** Question-and-answer cases where the assistant cites precise rule outcomes and current resource states; refusal behavior for unsupported claims; audit trail entries for all assisted decision explanations.

### 37. Assistant skill for turnaround readiness checks
**Justification:** Frontline controllers need a quick way to ask what is still blocking departure and whether an intervention is likely to help.
**Improvement:** Add a readiness-check skill that inspects the turnaround milestone graph, handler tasks, deicing status, slot alignment, and stand readiness, then produces a concise blocker list and recommended next action.
**Acceptance evidence:** Readiness summaries validated against live test fixtures; blocker ordering that matches the actual critical path; feedback evidence from controllers that the summaries reduce manual cross-checking.

### 38. Agent guardrails for safety, authority, and escalation
**Justification:** Airport operations assistants must never suggest unsafe ramp actions, bypass authority boundaries, or hide uncertainty when flight-critical decisions are involved.
**Improvement:** Define agent guardrails around stand closures, PRM handling, deicing, weather holds, and safety inspections so the assistant can advise, draft, and explain, but escalates appropriately on high-risk actions.
**Acceptance evidence:** Policy tests that block unsafe suggestions; escalation prompts for high-severity cases; release evidence showing the assistant stays within allowed decision support boundaries.

### 39. Persona-specific airport operations workbench views
**Justification:** Stand planners, terminal duty managers, baggage supervisors, and turnaround controllers need different slices of the same truth. One generic page increases cognitive load.
**Improvement:** Refine `AirportOperationsManagementWorkbench` and `AirportOperationsManagementDetail` into role-aware views with specialized filters, alerts, and action panels for gate planning, baggage control, terminal flow, and disruption management.
**Acceptance evidence:** Permission-aware route and panel tests; side-by-side persona demonstrations; reduced-click evidence for common tasks such as approving a stand move or reviewing belt overload risk.

### 40. Mobile-first apron inspection and turnaround evidence capture
**Justification:** Many critical observations happen on the ramp, not at a desk. Controllers need a reliable way to capture evidence from mobile devices without losing context.
**Improvement:** Add mobile-friendly flows for safety inspections, stand condition notes, turnaround milestone confirmations, and equipment-readiness evidence tied directly to the affected airport operations records.
**Acceptance evidence:** Mobile capture tests with offline or delayed-upload handling; time, actor, and location preserved in the audit trail; field evidence visible in desktop workbench views without manual transcription.

### 41. Event-sourced operational history and replay for peak periods
**Justification:** When an airport day goes wrong, the operations team must be able to reconstruct what was known, when it was known, and which decision followed from it.
**Improvement:** Deepen the declared event-sourced history capability so that gate, stand, slot, belt, passenger-flow, and disruption changes can be replayed minute by minute across a peak operating window.
**Acceptance evidence:** Deterministic replay for a disrupted day; point-in-time reconstruction of the workbench view; ability to compare the original decision with a counterfactual better decision after the fact.

### 42. Predictive risk scoring for missed departure and stand conflict
**Justification:** Risk scoring is only valuable if it predicts operational pain that controllers can still influence before it happens.
**Improvement:** Focus predictive risk on missed off-block, stand conflict probability, baggage reclaim overload, passenger queue breach, and deicing-induced departure miss, using the declared `airport_operations_management_predictive_risk_scoring` capability.
**Acceptance evidence:** Calibrated risk bands with outcome tracking; explanation panels that identify the top contributing operational factors; evidence that high-risk items surface early in workbench queues.

### 43. Counterfactual scenario simulation for disruption containment
**Justification:** The declared counterfactual capability should answer live airport questions such as whether towing an aircraft, switching to a remote stand, or delaying boarding would have reduced disruption spread.
**Improvement:** Add scenario simulation for runway closure, belt outage, stand closure, aircraft swap, handler shortage, and terminal congestion, with outcome comparisons on departure performance and passenger impact.
**Acceptance evidence:** Saved scenario runs with explicit assumptions; side-by-side comparison of actual versus simulated outcomes; evidence that simulation uses the same domain rules as live execution.

### 44. Continuous control testing for approvals and overrides
**Justification:** Airport operations depends on fast overrides, but fast overrides become unsafe unless control assertions continuously test whether the right people approved the right deviations with the right evidence.
**Improvement:** Add continuous checks in `airport_operations_management_control_assertion` for stand override authority, expired inspection evidence, unapproved gate changes, missing disruption closure notes, and agent actions without required confirmation.
**Acceptance evidence:** Control failures generated during test scenarios; workbench panels for open control breaches; release evidence showing controls run during operations rather than only in periodic audit exercises.

### 45. Release evidence pack for airport operations readiness
**Justification:** Airport domains require more than unit tests before release. Operators need proof that the system behaves correctly across peak, disrupted, and safety-sensitive conditions.
**Improvement:** Expand release evidence to include scenario packs for morning bank, diversion wave, runway closure, belt outage, deicing event, PRM-heavy departure, and terminal resource failure.
**Acceptance evidence:** `RELEASE_EVIDENCE.md` entries tied to named operational scenarios; screenshots or snapshots from the workbench; replay outputs and API traces proving the package handled each scenario end to end.

### 46. Dead-letter, replay, and quarantine console for airport ops feeds
**Justification:** Feed failures are operational events. Controllers and support engineers need a safe way to understand whether a missed update is blocking a stand release, slot refresh, or belt change.
**Improvement:** Add a console for quarantined inbound messages, replayable handler runs, failure classification, and operator-visible impact assessment when an inbound feed stops updating airport operations state.
**Acceptance evidence:** Drill scenarios where a broken feed is quarantined and replayed; visibility into affected flights and resources; evidence that replay cannot silently bypass current policy checks.

### 47. Tenant and operator policy isolation
**Justification:** Shared platforms may serve different airport operators, terminals, or airline communities with different stand policies, deicing rules, passenger-flow assumptions, and approval structures.
**Improvement:** Use the declared multi-tenant policy isolation capability so that operator-specific rules, service calendars, and thresholds remain isolated while sharing the same `airport_operations_management` package footprint.
**Acceptance evidence:** Cross-tenant negative tests for stand and rule leakage; separate policy views and parameter histories by tenant; release evidence showing one tenant can tighten controls without changing another tenant's behavior.

### 48. Schema extension governance for local airport rules
**Justification:** Every airport has local variations such as gate naming conventions, runway crossing procedures, bussing zones, and customs segregation layouts. Those differences should be extensible without breaking the core package.
**Improvement:** Make `airport_operations_management_schema_extension` a governed path for adding local fields, rules, and views for airport-specific stand, gate, and terminal nuances while preserving compatibility with the core APIs and events.
**Acceptance evidence:** Approved extension examples for local naming or process rules; compatibility checks for existing endpoints and event contracts; evidence that extensions appear in the workbench without forking core logic.

### 49. Rule and model explainability for controllers and auditors
**Justification:** Allocation and disruption decisions must be explainable to operations leaders, auditors, and frontline teams under time pressure. Black-box recommendations will not earn operational trust.
**Improvement:** Add explainability surfaces for rules, predictive scores, and agent recommendations, showing which facts, thresholds, policies, and historical patterns drove each recommendation or rejection.
**Acceptance evidence:** Decision cards that cite the source facts and policies used; explanation exports for audit review; acceptance sessions showing operators can understand and challenge automated recommendations.

### 50. Go-live operational drill scorecard
**Justification:** A package can look complete in code yet still be unready for live operations. Airports need rehearsal-based evidence that people, workflows, APIs, events, UI, and agent skills all work together.
**Improvement:** Add a go-live drill scorecard covering stand allocation, gate change control, turnaround recovery, baggage contingency, deicing coordination, disruption command, and assistant-supported decision review.
**Acceptance evidence:** Signed drill outcomes with pass or fail criteria, unresolved gap tracking, and release evidence that every critical airport operations path was rehearsed before production rollout.
