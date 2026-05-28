# Airline Operations Control PBC Improvement Backlog

## Current Domain Evidence Used

- PBC key: `airline_operations_control`.
- Manifest label: `Airline Operations Control`.
- Manifest description: fleet rotations, crew legality, disruptions, passenger reaccommodation, operational control, and recovery planning.
- Owned tables named in the manifest: `flight_leg`, `aircraft_rotation`, `crew_pairing`, `disruption_event`, `reaccommodation_plan`, `operations_decision`, `delay_code`, `airline_operations_control_policy_rule`, `airline_operations_control_runtime_parameter`, `airline_operations_control_schema_extension`, `airline_operations_control_control_assertion`, `airline_operations_control_governed_model`.
- Public routes named in the manifest: `POST /flight-legs`, `POST /aircraft-rotations`, `POST /crew-pairings`, `POST /disruption-events`, `POST /reaccommodation-plans`, `GET /airline-operations-control-workbench`.
- Workflows named in the manifest: `airline_operations_control_create_flight_leg_workflow` and `airline_operations_control_record_aircraft_rotation_workflow`.
- UI fragments named in the manifest: `AirlineOperationsControlWorkbench`, `AirlineOperationsControlDetail`, and `AirlineOperationsControlAssistantPanel`.
- Docs named in the manifest: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.
- Current emitted events: `AirlineOperationsControlCreated`, `AirlineOperationsControlUpdated`, `AirlineOperationsControlApproved`, and `AirlineOperationsControlExceptionOpened`.
- Current consumed events: `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.

### 1. Canonical flight-leg operating timeline

**Justification:** OCC teams cannot explain knock-on delay risk when one flight leg has multiple competing definitions of off-block, airborne, and arrival completion.

**Improvement:** Define one controlled `flight_leg` timeline from schedule publication through gate departure, takeoff, touchdown, on-block, and post-flight closure, with explicit handling for return-to-gate, diversion, and cancellation branches.

**Acceptance evidence:** `RELEASE_EVIDENCE.md` shows planned versus actual timeline traces for on-time, delayed, cancelled, diverted, and ferry-leg scenarios, and the workbench presents one authoritative timeline for each case.

### 2. Tail rotation continuity graph

**Justification:** A late inbound only matters operationally when controllers can see every downstream leg, turn, and overnight dependency attached to that tail.

**Improvement:** Build a rotation graph for each aircraft in `aircraft_rotation` that exposes previous leg, next leg, maintenance stop, spare substitution, and route recovery options across the operating day.

**Acceptance evidence:** Controllers can open a tail and see the full day sequence, a broken turn is highlighted before it becomes a departure delay, and recovery simulations show which later legs are protected or sacrificed.

### 3. Crew legality projection horizon

**Justification:** Crew legality breaches are usually visible hours before departure, but only if the system projects duty, rest, FDP, and connection effects forward rather than evaluating legality at the last minute.

**Improvement:** Add forward-looking legality projections for `crew_pairing` that calculate remaining duty margin, minimum rest exposure, split-duty effects, standby conversion, and deadhead consequences across the rest of the pairing.

**Acceptance evidence:** The workbench displays a legality countdown for each active pairing, projected illegal states are visible before check-in cutoff, and scenario evidence covers delays, swaps, extensions, and reserve activation.

### 4. Aircraft availability with maintenance constraint overlays

**Justification:** An aircraft is not operationally available just because it is on the ground; MEL, CDL, inspections, deferred defects, and parts waits all change what it can legally fly next.

**Improvement:** Extend aircraft availability views so `aircraft_rotation` decisions account for maintenance constraints, route restrictions, dispatch limitations, cabin defects, and upcoming due tasks before assigning the next leg.

**Acceptance evidence:** Tail availability cards show why an aircraft is green, amber, or blocked, and release evidence includes examples where a technical restriction prevents a naive swap.

### 5. Slot and curfew protection controls

**Justification:** Departure recovery that ignores airport slots, curfews, and constrained arrivals can create a worse network outcome than the original delay.

**Improvement:** Add slot-aware controls to `flight_leg` planning so controllers see coordinated slot windows, curfew exposure, night-stop consequences, and refile decisions before committing a revised departure.

**Acceptance evidence:** Scenario packs show constrained-airport departures, missed slot windows, curfew risk at destination, and the resulting decisions recorded with clear rationale.

### 6. ATC, weather, and NOTAM disruption fusion

**Justification:** Irregular ops decisions degrade when ATC restrictions, convective weather, runway closures, and NOTAM impacts arrive as separate unranked alerts.

**Improvement:** Fuse ATC, weather, and NOTAM signals into a single `disruption_event` view that scores relevance by flight leg, station, route, and timing instead of forcing controllers to correlate feeds manually.

**Acceptance evidence:** The OCC workbench shows one disruption card per operational issue with linked affected legs, and examples cover GDP, thunderstorm line, runway closure, and airspace restriction cases.

### 7. Minimum-turn feasibility engine

**Justification:** Published schedules often assume ideal turns; OCC needs a realistic turn view that includes station capability and the current operating context.

**Improvement:** Evaluate each `flight_leg` against minimum turn requirements using aircraft type, gate position, crew change, cleaning, catering, fueling, bags, deplaning, and special-assistance passenger needs.

**Acceptance evidence:** Turn-risk indicators appear before departure control decisions are finalized, and evidence demonstrates feasible, marginal, and impossible turn cases at large and outstation airports.

### 8. Fuel decision guardrails

**Justification:** Fuel choices during disruption recovery affect payload, alternate flexibility, cost, and the ability to protect the next wave of departures.

**Improvement:** Add fuel decision support to `operations_decision` so controllers can compare standard fuel, tanker fuel, extra contingency, alternate changes, payload tradeoffs, and diversion resilience before release.

**Acceptance evidence:** Release evidence includes at least one weather-driven extra fuel case, one tankering tradeoff case, and one payload restriction case with the chosen rationale captured.

### 9. Delay code discipline and hierarchy

**Justification:** Delay codes drive root-cause analysis, cost allocation, and performance conversations, so weak coding destroys the usefulness of post-ops analytics.

**Improvement:** Make `delay_code` assignment controlled, hierarchical, and evidence-backed, with primary cause, contributing causes, coding ownership, and late-change justification when responsibility shifts.

**Acceptance evidence:** The system prevents uncoded closure, exposes code change history, and `RELEASE_EVIDENCE.md` includes examples of reactionary versus root cause coding for multi-factor delays.

### 10. OCC workbench role views

**Justification:** Dispatchers, controllers, crew desk, and passenger reaccommodation teams do not need the same decisions surfaced at the same moment.

**Improvement:** Refine `AirlineOperationsControlWorkbench` into role-specific boards for network control, station control, crew control, maintenance coordination, and customer recovery while preserving one shared operational truth.

**Acceptance evidence:** Workbench screenshots show distinct role views, queue priorities differ by role, and all views reconcile to the same flight, tail, crew, and disruption facts.

### 11. Dispatch release and redispatch gating

**Justification:** Recovery planning remains incomplete if OCC can adjust flight legs without proving that dispatch release conditions are still satisfied.

**Improvement:** Treat dispatch release and redispatch as governed `operations_decision` milestones that check fuel assumptions, alternates, weather, route restrictions, aircraft status, and crew legality before a revised plan becomes active.

**Acceptance evidence:** Decision logs show release, re-release, and hold states, and evidence includes at least one enroute redispatch trigger after a material weather or route change.

### 12. Inbound dependency map for outbound protection

**Justification:** Controllers need to know whether an outbound is waiting on inbound aircraft, inbound crew, inbound bags, or a passenger connection bank before choosing a delay or swap.

**Improvement:** Add a dependency map around `flight_leg` and `aircraft_rotation` that links inbound aircraft, carry-over crew, through passengers, and station constraints to every outbound departure.

**Acceptance evidence:** The workbench can open a departure and show its dependency tree, and evidence covers wait-for-inbound, tail swap, crew split, and passenger-bank protection decisions.

### 13. Reaccommodation boundary rules

**Justification:** Passenger reaccommodation must respect fare, alliance, visa, special-service, and operational promise boundaries or the recovery plan creates downstream exceptions faster than it closes them.

**Improvement:** Define boundary rules for `reaccommodation_plan` covering protected connections, cabin entitlement, special assistance, unaccompanied minors, border constraints, overnight accommodation, and self-transfer exclusions.

**Acceptance evidence:** Recovery scenarios demonstrate when automatic reaccommodation is allowed, when human review is mandatory, and when a proposed plan is blocked for policy or customer-care reasons.

### 14. Aircraft swap simulator

**Justification:** Tail swaps are one of the most powerful recovery levers, but they create hidden consequences across maintenance, seat map, payload, and downstream timing.

**Improvement:** Add a simulation mode for `aircraft_rotation` that compares swap options by tail capability, seat mismatch, cabin defect exposure, maintenance positioning, and the number of protected departures.

**Acceptance evidence:** A controller can compare at least three swap options side by side, and the chosen option records why it outperformed the alternatives.

### 15. Crew swap and standby activation logic

**Justification:** Crew recovery is slower than aircraft recovery when standby, split crew, and base rules are not surfaced quickly enough.

**Improvement:** Extend `crew_pairing` support so OCC can evaluate reserve callout windows, airport standby, deadhead replacement, augmented crew needs, and skill-specific substitutions before a leg goes illegal.

**Acceptance evidence:** Crew desk scenarios show projected illegality, reserve activation timing, and the impact of swaps on later sectors in the same pairing.

### 16. Ferry, reposition, and recovery leg handling

**Justification:** A real airline control system needs to handle non-revenue positioning moves as first-class operational objects, not ad hoc notes around scheduled flying.

**Improvement:** Treat ferry, rescue, and reposition moves as explicit `flight_leg` variants with their own approval path, crew/fuel assumptions, airport permissions, and downstream rotation effects.

**Acceptance evidence:** Recovery cases include a cancelled passenger leg followed by a ferry leg, and the resulting rotation remains coherent in the workbench.

### 17. Cancellation decision packs

**Justification:** Cancelling the wrong leg can destroy an entire wave, while delaying the wrong leg can strand the tail and crew anyway.

**Improvement:** Create a cancellation pack in `operations_decision` that compares delay, cancel, consolidate, downgrade, and ferry alternatives using passenger count, slot impact, downstream recovery value, and crew legality margin.

**Acceptance evidence:** Decision packs are exportable, include the rejected options, and show which network objective the final cancellation protected.

### 18. Diversion and return-to-origin control

**Justification:** Diversions create immediate operational, customer, and maintenance consequences that need structured follow-through once the airborne event ends.

**Improvement:** Expand `disruption_event` handling so diversions and return-to-origin cases capture alternate selection, fuel status, customs implications, onward crew legality, and passenger recovery actions in one linked record.

**Acceptance evidence:** Evidence covers diversion initiation, on-ground stabilization, onward disposition, and the closure of both the airborne event and the ground recovery plan.

### 19. Payload and performance restriction handling

**Justification:** High temperature, short runway, contamination, and altitude constraints can turn an apparently available aircraft into a commercially unusable one.

**Improvement:** Add `flight_leg` checks for payload and performance restrictions so OCC sees seat block, bag offload, cargo cut, and reroute implications when dispatch conditions tighten.

**Acceptance evidence:** Release evidence includes a hot-and-high restriction case and a contaminated-runway case with visible payload or routing decisions.

### 20. Deicing and holdover management

**Justification:** Winter operations fail when deicing starts are tracked without linking them to holdover limits, queue position, and takeoff readiness.

**Improvement:** Model deicing as a timed `disruption_event` with queue state, fluid type assumptions, holdover expiry, and restart logic when a flight misses its departure opportunity.

**Acceptance evidence:** Workbench examples show valid, expiring, and expired holdover situations, and the chosen controller actions are recorded with timestamps.

### 21. Route restriction and alternate compliance

**Justification:** Long-haul and constrained routes can become unavailable because of ETOPS, military airspace closures, volcanic ash, or alternate degradation, not just airport conditions.

**Improvement:** Add route and alternate compliance checks into `operations_decision` so OCC sees when the planned leg is still legal, when a reroute is required, and when the flight should not depart at all.

**Acceptance evidence:** Scenario evidence covers route closure, alternate downgrade, and reroute acceptance with the exact operational reason captured.

### 22. Connection protection strategy

**Justification:** Waiting for connections without a network policy turns a local customer save into a system-wide departure reliability problem.

**Improvement:** Create connection protection rules that balance protected banks, high-value itineraries, minimum connect time, crew legality, slot risk, and downstream aircraft rotation damage before a `flight_leg` is held.

**Acceptance evidence:** Cases show when the system recommends hold, no-hold, or selective passenger reprotection, and the outcome is visible against later network impact.

### 23. Crew rest logistics during irregular ops

**Justification:** Crew legality can fail because of hotel, transport, or rest-environment issues long before it fails because of block-time arithmetic.

**Improvement:** Track hotel assignment, transport status, rest start, wake-up buffer, and immigration exposure around `crew_pairing` during IROPS so later legs reflect operational reality instead of paper assumptions.

**Acceptance evidence:** A disrupted overnight case shows the crew becoming legal or illegal based on actual rest logistics rather than a manual note.

### 24. Interline and codeshare reaccommodation boundaries

**Justification:** Customer recovery crosses commercial boundaries quickly, and OCC needs clear limits on what can be automated versus what must be handed to a commercial or alliance desk.

**Improvement:** Add `reaccommodation_plan` rules for interline, codeshare, alliance, and partner inventory cases, including what data can cross the boundary and which commitments require external confirmation.

**Acceptance evidence:** Evidence includes one own-metal recovery, one alliance recovery, and one blocked plan where the boundary forces manual escalation.

### 25. Maintenance due-clock projection across rotations

**Justification:** An aircraft that is legal now may become unusable after one more sector if the next check or life-limited task is not projected through the day.

**Improvement:** Project maintenance due clocks across `aircraft_rotation` so OCC can see whether continuing the planned sequence burns through inspection thresholds, cycle limits, or deferred-defect tolerances.

**Acceptance evidence:** Tail views show remaining maintenance margin by sector, and at least one recovery plan is rejected because it would breach a due clock later in the day.

### 26. Spare aircraft and standby resource inventory

**Justification:** Recovery options are weak when controllers cannot see the true availability of spare tails, spare crews, or maintenance-ready assets by station and time.

**Improvement:** Add a live availability inventory that brings together spare aircraft status, reserve crews, maintenance release readiness, and station capability to support fast recovery choices.

**Acceptance evidence:** The OCC workbench shows available and unavailable resources by base and outstation, and decision evidence links chosen recovery actions back to that inventory snapshot.

### 27. Station-specific IROPS playbooks

**Justification:** The same disruption should not be handled the same way at a hub, a night-stop outstation, and a slot-constrained international station.

**Improvement:** Create station-aware `disruption_event` playbooks that vary by curfew, crew lodging options, maintenance coverage, customs handling, deicing capability, and passenger volume profile.

**Acceptance evidence:** Playbooks exist for at least a hub, a spoke, and an international station, and operators can show which playbook informed a live decision.

### 28. Operations decision journal with rationale capture

**Justification:** High-tempo control work still needs a durable explanation of who chose what, when, and why, especially when the day is reconstructed after a severe disruption.

**Improvement:** Make `operations_decision` a structured journal of alternatives considered, selected action, assumptions, approvals, and expected downstream effect rather than a free-text summary field.

**Acceptance evidence:** Decision records show rejected alternatives, operator identity, timestamp lineage, and linked disruption or reaccommodation objects for each material recovery step.

### 29. Delay forecast confidence bands

**Justification:** Controllers need to know not just the latest estimate but how likely it is to hold, because unstable estimates trigger bad gate, crew, and customer decisions.

**Improvement:** Add forecast confidence bands to delay predictions using inbound status, station congestion, weather uncertainty, maintenance uncertainty, and crew readiness as explicit drivers.

**Acceptance evidence:** The workbench shows best-case, expected, and worst-case departure outlooks, and forecast quality is measured against actual outcomes in release evidence.

### 30. Event and API boundary contracts

**Justification:** `airline_operations_control` should own operational control decisions without silently absorbing airport, maintenance, crew, or customer-service responsibilities that belong elsewhere.

**Improvement:** Define strict command, query, and event boundaries for `POST /flight-legs`, `POST /aircraft-rotations`, `POST /crew-pairings`, `POST /disruption-events`, `POST /reaccommodation-plans`, and emitted or consumed events so each integration point declares what it owns and what it does not.

**Acceptance evidence:** `SPECIFICATION.md` and `RELEASE_EVIDENCE.md` contain explicit boundary matrices, rejected out-of-scope payload examples, and proof that cross-domain handoffs stay visible rather than implicit.

### 31. Idempotent disruption ingestion and deduplication

**Justification:** ATC and weather feeds often resend the same operational fact with small formatting differences, and duplicate disruption records erode trust quickly.

**Improvement:** Add deduplication logic for `disruption_event` so equivalent ATC, weather, and station updates collapse into one operational issue with preserved source lineage and update history.

**Acceptance evidence:** Replayed feed samples do not create duplicate disruptions, source lineage remains intact, and controllers can see when a disruption card was refreshed rather than recreated.

### 32. Recovery scenario sandbox

**Justification:** OCC teams need a safe place to test alternative recovery waves without contaminating the active network picture.

**Improvement:** Create a non-mutating sandbox around `operations_decision`, `aircraft_rotation`, and `crew_pairing` that lets controllers compare delay, cancel, swap, ferry, and reaccommodation strategies before activating one.

**Acceptance evidence:** Side-by-side scenarios can be opened from the same disruption, only one plan can be promoted, and rejected simulations remain available for later review.

### 33. Agent skills and approval limits

**Justification:** Assistant features in the OCC should accelerate work without creating hidden autonomous decisions that operators cannot challenge.

**Improvement:** Define allowed agent skills in `AirlineOperationsControlAssistantPanel`, such as summarizing disruption impact, drafting recovery options, ranking swaps, and preparing evidence packs, while reserving approvals and certain customer-impacting commitments for humans.

**Acceptance evidence:** Assistant actions show the exact skill used, the human approver where required, and blocked examples where the assistant attempted to exceed its authority.

### 34. Shift handover continuity packs

**Justification:** Many severe control failures happen at shift change because active assumptions and pending decisions are not handed over cleanly.

**Improvement:** Generate handover packs from `operations_decision`, `disruption_event`, open legality risks, and critical rotations so the incoming OCC team inherits the active picture, not just a verbal summary.

**Acceptance evidence:** Handover exports list active risks, unresolved decisions, next trigger points, and owner assignments, and release evidence shows one day-of-ops shift transition.

### 35. Network heatmap and wave-risk view

**Justification:** Local disruptions are easier to overreact to when controllers cannot see how one station issue interacts with bank structure across the network.

**Improvement:** Add a heatmap to `AirlineOperationsControlWorkbench` that groups risk by departure wave, fleet family, station, and tail concentration so OCC can prioritize what threatens the whole schedule.

**Acceptance evidence:** The workbench can pivot between station view and network wave view, and evidence shows one case where a small local delay is deprioritized to protect a larger bank.

### 36. Fuel tankering versus recovery tradeoff analysis

**Justification:** Fuel tankering can save cost but also add weight, reduce payload, and worsen schedule recovery when conditions deteriorate.

**Improvement:** Add an `operations_decision` comparison that weighs tankering benefit against payload loss, extra burn, alternate flexibility, and departure recovery risk by route and day-of-ops conditions.

**Acceptance evidence:** Decision evidence includes one case where tankering is approved and one where it is rejected because it undermines recovery.

### 37. Delay-code-to-cost attribution

**Justification:** Delay codes become strategically useful only when they explain money, not just punctuality.

**Improvement:** Link `delay_code` outcomes to crew overtime, hotel exposure, fuel burn, passenger care, missed slots, and maintenance repositioning cost so post-ops review can target the true drivers.

**Acceptance evidence:** Post-ops reports show operational and financial attribution by delay code family, and a multi-cause event preserves both root cause and downstream cost effects.

### 38. Recovery prioritization policy engine

**Justification:** Airlines recover differently depending on whether they are protecting banks, premium passengers, fleet positioning, or next-day readiness.

**Improvement:** Add policy controls in `airline_operations_control_policy_rule` and `airline_operations_control_runtime_parameter` that let OCC declare the current recovery objective and apply it consistently across swaps, delays, cancellations, and reaccommodation choices.

**Acceptance evidence:** Operators can switch between at least two declared recovery strategies, and identical disruptions lead to measurably different but explainable outcomes under each strategy.

### 39. Technical turnback and return-to-gate handling

**Justification:** Return-to-gate events are operationally distinct from ordinary delays because they reset boarding, maintenance, crew, and passenger commitments all at once.

**Improvement:** Model technical turnbacks as structured `disruption_event` cases with maintenance triage, reaccommodation triggers, crew-duty recalculation, and re-release gating before the flight can resume.

**Acceptance evidence:** Workbench evidence shows the full chain from return-to-gate through either resumed departure, aircraft swap, or cancellation closure.

### 40. Airspace flow restriction and slot revision handling

**Justification:** Flow programs, miles-in-trail restrictions, and revised CTOTs change the economics of holding, cancelling, and rerouting minute by minute.

**Improvement:** Add flow-restriction handling to `flight_leg` control so updated slot times, route windows, and airspace releases automatically refresh the relevant recovery options.

**Acceptance evidence:** A flow-control case shows original and revised slot times, the options OCC considered, and the final decision once the restriction changed.

### 41. Reaccommodation promise tracking

**Justification:** A recovery plan is not credible if the airline cannot prove whether passengers were actually protected onto the flights or services it promised.

**Improvement:** Extend `reaccommodation_plan` so it tracks proposed option, accepted option, ticketing confirmation, uplift outcome, overnight handling, and residual exception status for affected travelers or cohorts.

**Acceptance evidence:** Evidence shows promised versus delivered recovery outcomes for a cancellation event, including unresolved cases that still require manual follow-up.

### 42. Cargo, special loads, and dangerous-goods boundaries

**Justification:** Some recovery options that work for passengers fail operationally because cargo, live animals, special loads, or dangerous goods cannot move the same way.

**Improvement:** Add handling rules so `flight_leg` and `operations_decision` treat cargo and special-load constraints as hard boundaries when rerouting, downgrading aircraft, or reaccommodating mixed passenger and cargo sectors.

**Acceptance evidence:** Recovery scenarios include at least one blocked swap or reroute caused by load restrictions, with the boundary explained in the decision record.

### 43. Release evidence pack for day-of-ops readiness

**Justification:** The package should prove operational readiness with airline-specific evidence, not just route availability and generic happy-path screenshots.

**Improvement:** Make `RELEASE_EVIDENCE.md` show flight-leg control, rotation views, legality projections, disruption fusion, reaccommodation boundaries, delay-code governance, and OCC workbench decisions using realistic airline ops scenarios.

**Acceptance evidence:** The release pack contains named scenarios, linked screenshots or exports, and a traceable mapping from each scenario back to the operational capability it proves.

### 44. Manual override discipline and after-action review

**Justification:** Manual overrides are necessary during severe disruption, but uncontrolled overrides hide whether the system or the process needs to improve.

**Improvement:** Require override reason, expected duration, owner, and post-event review for high-impact `operations_decision` actions such as ignoring legality warnings, relaxing a reaccommodation boundary, or accepting a marginal turn.

**Acceptance evidence:** Override logs can be filtered by type and station, expiring overrides surface in the workbench, and after-action reviews are attached to the originating decision.

### 45. Cross-system handoff visibility

**Justification:** Airline control decisions often depend on airport, maintenance, crew, loyalty, or customer communication systems, and hidden handoffs create false confidence.

**Improvement:** Record explicit handoff states whenever `airline_operations_control` emits or consumes events across adjacent domains, showing requested action, responsible external team or service, response deadline, and returned outcome.

**Acceptance evidence:** At least one end-to-end case traces a disruption from OCC decision through external handoff and back, with no silent status jumps in the middle.

### 46. Flight-leg freeze windows and change arbitration

**Justification:** Not every field on a near-departure flight leg should remain editable once boarding, fueling, loading, or dispatch commitments are underway.

**Improvement:** Introduce controlled freeze windows on `flight_leg` updates so tail changes, departure time shifts, payload adjustments, and cancellation decisions follow stricter arbitration as departure approaches.

**Acceptance evidence:** The system blocks unsafe late edits, allows urgent exceptions through a governed path, and captures who authorized each late change.

### 47. Data freshness service levels for critical feeds

**Justification:** A controller using stale weather, crew, aircraft, or disruption data can make a perfectly reasoned but wrong decision.

**Improvement:** Show freshness SLAs on the critical data feeds that drive `flight_leg`, `aircraft_rotation`, `crew_pairing`, and `disruption_event` decisions, including last update time and the operational consequence of staleness.

**Acceptance evidence:** The workbench marks stale feeds clearly, degraded recommendations are labeled as such, and scenario evidence includes one case where stale data blocks automation.

### 48. Delay-code closure quality checks

**Justification:** Delay-code accuracy usually degrades at closure time, when teams are busy and tempted to choose the nearest acceptable value.

**Improvement:** Add closure checks so a `delay_code` cannot be finalized without supporting operational facts, timing consistency, and confirmation that reactionary codes are not masking a deeper root cause.

**Acceptance evidence:** Closure attempts with missing evidence are rejected, code changes remain auditable, and release evidence includes corrected examples that demonstrate the guardrail.

### 49. Recovery outcome scoring against plan

**Justification:** OCC needs to learn whether its chosen actions actually protected the network, not just whether the immediate issue was closed.

**Improvement:** Score completed `operations_decision` outcomes against the expected network effect, including protected departures, legality avoided, passenger disruption avoided, and cost or delay transferred elsewhere.

**Acceptance evidence:** Post-event scorecards compare expected versus actual recovery outcome and identify where decision heuristics should be tuned.

### 50. Tabletop drills and event-replay regression library

**Justification:** Airline control capability is only credible if the package can repeatedly demonstrate good behavior on known bad days, not just on a clean demo schedule.

**Improvement:** Build a regression library of replayable airline ops cases across weather, ATC flow, technical defects, crew illegality, missed slots, diversions, cancellations, and mass reaccommodation so `airline_operations_control` can be tested against the same severe scenarios release after release.

**Acceptance evidence:** `RELEASE_EVIDENCE.md` references named replay drills, outcomes are reproducible, and regression results show whether recovery quality improved, regressed, or remained stable.
