# Port Terminal Operations Improvement Backlog

## Current Domain Evidence Used

- PBC key: `port_terminal_operations`.
- Manifest description: vessel calls, berths, yard moves, containers, equipment, customs handoffs, and terminal productivity.
- Current tables: `vessel_call`, `berth_plan`, `container_move`, `yard_slot`, `gate_transaction`, `terminal_equipment`, `customs_handoff`, `port_terminal_operations_policy_rule`, `port_terminal_operations_runtime_parameter`, `port_terminal_operations_schema_extension`, `port_terminal_operations_control_assertion`, `port_terminal_operations_governed_model`.
- Current APIs: `POST /vessel-calls`, `POST /berth-plans`, `POST /container-moves`, `POST /yard-slots`, `POST /gate-transactions`, `GET /port-terminal-operations-workbench`.
- Current emitted events: `PortTerminalOperationsCreated`, `PortTerminalOperationsUpdated`, `PortTerminalOperationsApproved`, `PortTerminalOperationsExceptionOpened`.
- Current consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Current workflows and UI fragments: `port_terminal_operations_create_vessel_call_workflow`, `port_terminal_operations_record_berth_plan_workflow`, `PortTerminalOperationsWorkbench`, `PortTerminalOperationsDetail`, `PortTerminalOperationsAssistantPanel`.

### 1. Vessel ETA Confidence and Berth Nomination
**Justification:** Berth planning fails early when ETA changes arrive as free text and the terminal cannot distinguish a stable arrival forecast from a speculative line update.

**Improvement:** Add a vessel-arrival model that stores last advised ETA, pilot-ready ETA, tide-feasible ETA, and confidence band, then requires berth nominations to carry source, update time, and revision reason before they can influence quay plans.

**Acceptance evidence:** A berth nomination record shows ETA revisions with source lineage, conflict flags when confidence drops below threshold, and tests cover early arrival, late arrival, and repeated ETA churn.

### 2. Berth Window Conflict Resolution
**Justification:** Two vessels can appear schedulable on paper while still conflicting on LOA, beam, draft, bollard reach, tidal window, or adjacent-crane envelope.

**Improvement:** Extend berth planning to evaluate berth windows against vessel dimensions, tide constraints, neighboring vessel interference, and marine service availability before a berth plan is accepted.

**Acceptance evidence:** Simulation fixtures prove the plan rejects impossible overlaps, explains the blocking constraint, and offers the next feasible berth window or alternate berth.

### 3. Berth Readiness Checklist
**Justification:** A vessel marked "alongside" without readiness evidence hides missing pilotage, tug confirmation, gang assignment, customs pre-clearance, or crane availability.

**Improvement:** Introduce a berth-readiness checklist that gates berthing on marine services, labor shift coverage, crane allocation, yard receiving space, and customs status for the intended move profile.

**Acceptance evidence:** A vessel cannot transition to ready-to-berth without all checklist items resolved, blocked items surface on the workbench, and audit history shows who cleared each dependency.

### 4. Quay Crane Assignment by Bay Plan
**Justification:** Terminal productivity drops when crane allocation is disconnected from hatch distribution, move density, twin-lift eligibility, and crane travel interference.

**Improvement:** Model quay crane assignment per vessel call using bay-level move counts, hatch grouping, crane split zones, crane crossing restrictions, and crane travel time between assigned spans.

**Acceptance evidence:** The berth plan shows crane-to-bay assignments, warns on crane crossing conflicts, and replay tests confirm reassignment after crane outage or late vessel shift.

### 5. Crane Intensity and Shift Alignment
**Justification:** A crane plan is not operational if it ignores gang start times, meal breaks, maintenance windows, and night-shift labor limits.

**Improvement:** Add crane intensity planning that aligns planned gross moves per hour with labor rosters, maintenance windows, and approved work-hour limits, then throttles the plan when staffing cannot support the requested intensity.

**Acceptance evidence:** Shift-aware crane plans show planned versus feasible intensity, reject unsupported peaks, and produce evidence for supervisor override when temporary extra gangs are approved.

### 6. Bay Sequence and Hatch Cover Dependencies
**Justification:** Move instructions that ignore hatch cover sequencing and lashing release create unsafe crane time assumptions and avoidable delays.

**Improvement:** Track bay sequence dependencies, including hatch cover open and close order, lashing status, and bay access readiness, so crane schedules only expose executable move sets.

**Acceptance evidence:** Vessel work plans block moves behind unopened hatches, record lashing completion events, and highlight downstream delay if hatch cover handling slips.

### 7. Restow Control and Avoidable Rehandles
**Justification:** Restows consume crane time and berth window capacity, yet many are preventable when stow mismatches are detected before discharge starts.

**Improvement:** Flag planned and emerging restows by comparing expected discharge and load sequence against bay stack geometry, destination mix, and container priority, then surface a "preventable restow" queue.

**Acceptance evidence:** The system quantifies planned restows by vessel call, records operator justification for accepted restows, and shows reduced avoidable restow count after corrective sequencing.

### 8. Container Move Instruction Lifecycle
**Justification:** Container work becomes irreconcilable when a move can jump from request to completion without visible dispatch, acknowledgment, execution, and exception states.

**Improvement:** Give each container move a lifecycle of planned, dispatched, accepted, in-progress, completed, reversed, canceled, or exception, with actor, equipment, location, and timestamp captured at each transition.

**Acceptance evidence:** Move history for a single box reconstructs who instructed, who executed, what equipment was used, and why a reversal or cancellation occurred.

### 9. Twin-Lift, Tandem, and Dual-Cycle Eligibility
**Justification:** Crane productivity assumptions are misleading if high-productivity move modes are planned on boxes, bays, or cargo mixes that cannot support them.

**Improvement:** Encode eligibility rules for twin-lift, tandem lift, and dual-cycle operations based on container size mix, weight spread, dangerous-goods restrictions, and vessel bay geometry.

**Acceptance evidence:** Productivity models show when advanced lift modes are permitted, exceptions explain the disqualifying factor, and crane plans recalculate when lift mode eligibility changes.

### 10. Yard Block Allocation by Flow
**Justification:** Yard congestion rises when import, export, transshipment, hazardous, empty, reefer, and customs-held containers compete for the same blocks without policy.

**Improvement:** Introduce yard planning rules that allocate blocks by cargo flow, onward mode, service string, destination cluster, and special handling class, then protect reserved capacity for imminent vessel work.

**Acceptance evidence:** Yard-slot projections show reserved versus consumed capacity by flow type, and tests cover high-import surge, export stack buildup, and transshipment peaking.

### 11. Rehandle Hotspot Prediction
**Justification:** The terminal usually knows where unproductive rehandles will occur before the yard reaches crisis state, but that signal is lost without stack-level forecasting.

**Improvement:** Score yard slots for rehandle risk using stack height, due time, box priority, truck appointment demand, vessel cut-off, and expected crane feeding sequence.

**Acceptance evidence:** The workbench highlights hotspot stacks before the shift starts, planners can compare proposed relocations, and actual rehandle counts are tracked against forecast.

### 12. Stack Discipline for Weight and Segregation
**Justification:** Unsafe stacks arise when heavy-over-light, hazardous segregation, OOG placement, and line-specific placement rules are enforced only through local memory.

**Improvement:** Add yard-slot validation for stack weight ordering, dangerous-goods segregation, out-of-gauge geometry, line allocation, and reefer plug proximity before a move is accepted.

**Acceptance evidence:** Invalid stack placements are blocked with a domain reason, exception overrides require named approval, and tests prove segregation rules across neighboring slots.

### 13. Misposition and Lost-Box Search
**Justification:** A container marked present but not found in the expected slot disrupts vessel work, gate release, and customs inspection queues.

**Improvement:** Build a misposition workflow that triangulates last confirmed move, equipment breadcrumb, OCR sightings, neighboring slot anomalies, and manual search results to locate missing containers fast.

**Acceptance evidence:** Search cases retain search trail evidence, candidate locations are ranked, and closure requires either physical confirmation or a reconciled correction move.

### 14. Gate Appointment Capacity by Hour and Lane
**Justification:** Gate congestion is created upstream when appointment limits ignore lane count, clerk staffing, OCR uptime, and yard receiving capacity.

**Improvement:** Support hourly appointment quotas by gate lane, transaction type, trucking segment, and yard destination so import pickup, export drop-off, empty return, and reefer service flows can be shaped independently.

**Acceptance evidence:** Appointment calendars show remaining capacity by hour, overbooking rules are explicit, and turn-time results improve after quota adjustments.

### 15. Truck Turn-Time Exception Loop
**Justification:** Median turn time hides the operational causes of failure such as missing release, OCR mismatch, no booking, late customs hold, or yard retrieval delay.

**Improvement:** Add an exception loop for gate transactions that classifies delay cause at entry, processing, yard handoff, and exit, then routes the case to the owning team with a due clock.

**Acceptance evidence:** Gate dashboards break down turn-time loss by cause code, each long-turn case shows routed ownership, and repeat causes are traceable to equipment, appointment, or release failures.

### 16. Empty Pickup and Return Balancing
**Justification:** Empty inventory can consume prime gate and yard capacity when release orders, depot allocations, and line return windows are handled outside the core operating model.

**Improvement:** Add empty-container policies for pickup and return that consider line ownership, depot target, gate slot pressure, yard dwell, and reposition priorities.

**Acceptance evidence:** Empty stock by line and depot is visible, invalid returns are blocked before gate arrival, and planners can see the impact of changing return instructions.

### 17. Customs Boundary Release Gating
**Justification:** A box should not flow from terminal custody to truck or vessel if the customs boundary is represented only as a note or offline email.

**Improvement:** Model customs release as a first-class gate on container and gate workflows, with release state, inspection requirement, scan result, and expiry timestamp carried into move and gate decisions.

**Acceptance evidence:** Containers under customs restriction cannot be dispatched or gated out, release expiry is enforced, and every release decision retains source message evidence.

### 18. Hold Taxonomy and Precedence Rules
**Justification:** Operations teams lose time when "on hold" does not distinguish line hold, customs hold, terminal safety hold, documentation hold, or reefer technical hold.

**Improvement:** Create a hold model with type, issuer, effective time, expiry rule, precedence, override authority, and operational impact so multiple holds can coexist without ambiguity.

**Acceptance evidence:** A container or vessel view shows all active holds in precedence order, actions are blocked according to the highest-precedence hold, and release history shows which hold was cleared.

### 19. Customs Exam and Scan Routing
**Justification:** Inspection flow breaks down when exam yard staging, scanner queueing, and return-to-stack instructions are tracked outside the move lifecycle.

**Improvement:** Add customs exam routing that reserves staging positions, scan appointments, escort steps, and return instructions, with explicit ownership for failed scan, missed exam, or non-intrusive inspection retry.

**Acceptance evidence:** Exam cases show current stage, next appointment, and return path, and missed inspection windows produce recoverable exceptions rather than silent dwell growth.

### 20. Dangerous Goods Segregation and IMDG Checks
**Justification:** Dangerous-goods safety cannot rely on manual memory when stack neighbors, vessel stow plans, and gate acceptance decisions all depend on the same classification logic.

**Improvement:** Enforce IMDG-aware rules across yard slots, gate acceptance, vessel loading, and reefer plug allocation, including class, subsidiary risk, flashpoint, segregation group, and documentation completeness.

**Acceptance evidence:** DG validation blocks unsafe adjacency, vessel load plans flag incompatible neighbors, and the audit trail shows the exact DG rule that drove the decision.

### 21. Reefer Plug Allocation
**Justification:** Reefer service failures start when the terminal treats plug points as generic yard capacity instead of a monitored, constrained resource.

**Improvement:** Track reefer sockets, power status, cable reach, genset dependency, and priority class, then reserve plug positions based on arrival pattern, dwell risk, and vessel cut-off.

**Acceptance evidence:** The yard plan shows plug occupancy and reserve margin, reefer moves cannot target unpowered slots, and allocation tests cover import surge and transshipment reefers.

### 22. Reefer Temperature and Power Excursion Workflow
**Justification:** A reefer alarm is only useful if it drives timely action before cargo quality is at risk or release is blocked.

**Improvement:** Add a reefer-monitoring workflow for temperature deviation, power loss, unplug event, and manual inspection result, with escalation rules by commodity sensitivity and remaining tolerance window.

**Acceptance evidence:** Every reefer alarm opens a timed case, inspection notes and corrective actions are linked to the container, and unresolved power loss remains visible until closure.

### 23. Demurrage and Dwell-Risk Watchlist
**Justification:** Dwell pain is often predictable from holds, missing documents, customs exam backlog, and failed appointments before invoices or complaints arrive.

**Improvement:** Build a dwell-risk watchlist that scores containers by free-time expiry, hold status, customs stage, appointment availability, line release, and storage location accessibility.

**Acceptance evidence:** The workbench ranks at-risk boxes by hours remaining, planners can filter by root cause, and historical evidence shows whether intervention reduced late pickups.

### 24. Free-Time Exception Evidence
**Justification:** Waivers and storage disputes become unresolvable when free-time adjustments are not tied to named causes and terminal evidence.

**Improvement:** Record demurrage and storage exception grounds such as customs stop, system outage, weather closure, terminal-caused misposition, or reefer technical issue, then attach supporting event and approval evidence.

**Acceptance evidence:** Every free-time adjustment shows cause, approver, time range, and supporting event references, and exportable evidence exists for dispute handling.

### 25. Transshipment Connection Protection
**Justification:** Transshipment promises fail when incoming vessel delay, yard position, and outgoing cut-off are not evaluated together.

**Improvement:** Add transshipment protection logic that pairs inbound ETA confidence, discharge sequence, yard transfer path, and outbound load cut-off to identify boxes likely to miss the connection.

**Acceptance evidence:** At-risk transshipment boxes are visible before discharge completes, the system recommends rescue moves or roll decisions, and completed cases show saved versus missed connections.

### 26. Intermodal Cut-Off Coordination
**Justification:** Port terminals often hand cargo to rail, barge, and truck legs that each have different closure times and staging needs.

**Improvement:** Track onward-mode cut-offs, transfer staging, documentation readiness, and late-gate tolerances so the yard plan and gate appointment logic can respect downstream departure windows.

**Acceptance evidence:** A container view shows the active onward-mode deadline, missed cut-offs produce explicit exceptions, and planners can see cutoff breaches by mode and carrier.

### 27. Marine Services Dependency Board
**Justification:** Berth plans are operationally incomplete when tug, pilot, mooring crew, and launch availability sit outside the same exception surface as vessel work.

**Improvement:** Add marine-services dependencies to vessel calls, including requested service time, confirmed service time, provider acknowledgment, and slippage reason, then feed that into berth and sailing readiness.

**Acceptance evidence:** Vessel calls display dependency readiness at a glance, missed marine service slots automatically threaten the berth window, and replans are logged with cause.

### 28. Equipment Health and Fallback Dispatch
**Justification:** Yard and quay plans degrade quickly if RTGs, RMGs, terminal tractors, top handlers, and reach stackers are assumed healthy until they fail.

**Improvement:** Extend terminal-equipment records with operating state, fault category, maintenance hold, battery or fuel state, and fallback equipment pool so dispatch can reassign work before queues collapse.

**Acceptance evidence:** Equipment outages trigger task rerouting, planners can see the productivity hit of each outage, and dispatch history shows which moves were reassigned.

### 29. Vessel Work Completion Reconciliation
**Justification:** A vessel should not sail on the strength of move counts alone when unlanded boxes, short-shipped exports, and late bay corrections may still exist.

**Improvement:** Reconcile actual discharge and load execution against planned move lists, bay completion, hatch closure, and final stow confirmation before the vessel call can close.

**Acceptance evidence:** Closure requires zero unresolved move discrepancies or approved exceptions, and the final reconciliation report shows shortages, overages, and corrected last-minute changes.

### 30. EDI Ingest for Vessel and Container Messages
**Justification:** Port operations depend on external messages, and poor normalization of line and vessel EDI creates repeated manual repair work.

**Improvement:** Add structured ingest and validation for operational messages such as BAPLIE, MOVINS, CODECO, COARRI, and COPARN, mapping them to vessel call, move, gate, and customs-release workflows with source retention.

**Acceptance evidence:** Each inbound message can be replayed idempotently, parser rejects are explainable at segment level, and normalized events retain original message identifiers.

### 31. Operational Event Timestamp Fidelity
**Justification:** Sequence disputes arise when the system cannot distinguish event occurrence time, device capture time, ingest time, and correction time.

**Improvement:** Store multi-clock timestamps for gate, move, reefer, customs, and crane events, then use an explicit ordering policy for projections and audit reconstruction.

**Acceptance evidence:** Event views show all relevant timestamps, replay logic remains deterministic with late-arriving messages, and audit exports explain why a corrected event was reordered.

### 32. Idempotent Replay and Late-Message Handling
**Justification:** External line, customs, and gate systems will resend or delay messages; without replay discipline, the terminal creates phantom moves and duplicate releases.

**Improvement:** Add idempotency keys and late-message policies for all inbound operational events so duplicates are suppressed, superseded messages are tracked, and harmless replays can rebuild projections safely.

**Acceptance evidence:** Duplicate message tests do not create extra work, stale messages are quarantined with reason, and replay from a known checkpoint reproduces the same operational state.

### 33. Customs Handoff Audit Chain
**Justification:** Customs handoff is the legal boundary between cargo restriction and permitted flow, so every state change must be provable after the fact.

**Improvement:** Expand customs handoff records with request, response, officer or system source, document reference, validity period, and linked container actions that were enabled or blocked by that handoff.

**Acceptance evidence:** A single customs case can be reconstructed end to end, from request to release or rejection, and container actions cite the governing customs decision.

### 34. Live Berth, Yard, and Gate Workbench
**Justification:** Operators need one operating picture that connects quay work, yard pressure, and gate demand rather than three disconnected status pages.

**Improvement:** Redesign the workbench into synchronized berth, yard, and gate boards with shared filters for vessel, service, container, block, gate lane, hold type, and exception owner.

**Acceptance evidence:** Filters applied on one board propagate to the others, drill-through preserves context, and operators can move from vessel delay to affected yard and gate impacts in one flow.

### 35. Yard Visual Heatmap and Stack Profile UI
**Justification:** Yard planners need spatial visibility into congestion, reefer density, DG clustering, and rehandle hotspots that cannot be inferred from flat tables.

**Improvement:** Add a yard heatmap that shows occupancy, dwell pressure, plug usage, DG concentration, and predicted rehandle risk, with stack profiles visible at block, row, bay, and tier level.

**Acceptance evidence:** Clicking a hotspot reveals the underlying boxes and risk reasons, planners can compare before and after a re-slot scenario, and the UI handles large yards without losing responsiveness.

### 36. Exception Cockpit with Aging and SLA Views
**Justification:** Exception queues become noise when berth conflicts, missed appointments, DG blocks, reefer alarms, and customs holds are mixed without urgency and ownership.

**Improvement:** Build an exception cockpit that groups operational issues by domain stream, severity, aging bucket, SLA breach risk, and current owner, with explicit next action and escalation path.

**Acceptance evidence:** Operators can filter to breach-imminent cases, each case shows time remaining and owner, and completed exceptions preserve closure evidence and cause coding.

### 37. Evidence Panel for Holds and Releases
**Justification:** Operators waste time hunting across logs, emails, and screens to verify why a container is blocked or released.

**Improvement:** Add an evidence panel on detail pages that assembles holds, release messages, customs actions, gate attempts, reefer alarms, and recent moves in time order with source links.

**Acceptance evidence:** A blocked container view shows all governing evidence without leaving the detail page, and exported evidence packs retain source timestamps and identifiers.

### 38. Operator Task and Shift Handover Log
**Justification:** Port operations are shift-based, and unresolved issues are often lost during handover even though the system already knows the pending risks.

**Improvement:** Attach shift handover notes, active risks, pending approvals, and priority actions to berth, yard, gate, reefer, and customs queues so incoming supervisors inherit the live problem list.

**Acceptance evidence:** Shift close requires unresolved cases to be handed over or acknowledged, handover logs are searchable by workstream, and reopened cases show the missed handover link.

### 39. Agent Skill for Vessel Operations Coordination
**Justification:** The assistant should help with berth and vessel-work coordination without becoming an ungoverned shortcut around marine or cargo controls.

**Improvement:** Add a vessel-ops agent skill that can summarize ETA shifts, berth conflicts, crane assignment impacts, and sail-readiness gaps, then prepare but not silently apply corrective plans.

**Acceptance evidence:** The assistant produces cited vessel coordination summaries, every proposed change is previewed before approval, and blocked actions explain the governing policy.

### 40. Agent Skill for Yard Planning
**Justification:** Yard planners need rapid what-if support on stack allocation, rehandle reduction, transshipment rescue, and reefer placement.

**Improvement:** Add a yard-planner agent skill that can compare block-allocation scenarios, recommend re-slots, identify misposition search paths, and explain the tradeoff between dwell relief and crane feeding efficiency.

**Acceptance evidence:** Scenario outputs include the source slots and predicted impact, accepted recommendations create visible drafts, and rejected recommendations capture planner feedback for improvement.

### 41. Agent Skill for Gate Supervision
**Justification:** Gate supervisors need help spotting appointment oversubscription, release failures, OCR outages, and truck turn-time spikes before queues spill outside the terminal.

**Improvement:** Add a gate-supervisor agent skill that monitors appointment utilization, long-turn root causes, lane outages, and release blocks, then suggests quota adjustments or manual recovery actions.

**Acceptance evidence:** The assistant can explain current gate pressure with cited cases, suggested quota changes are tied to capacity assumptions, and no agent action bypasses appointment or release rules.

### 42. Agent Skill for Customs and Release Desk
**Justification:** Release desks spend time correlating holds, releases, scan results, and carrier instructions across multiple systems and messages.

**Improvement:** Add a customs-and-release agent skill that assembles the current release posture for a container, shows active holds and precedence, and drafts the next permissible action or escalation.

**Acceptance evidence:** Desk users can request a release summary with linked evidence, the skill refuses unsafe release recommendations, and every desk action remains attributable to a named user approval.

### 43. Agent Skill for Reefer Operations
**Justification:** Reefer teams need fast triage during power loss, alarm storms, and plug-capacity pressure, but the assistant must stay grounded in live equipment and container state.

**Improvement:** Add a reefer-operations agent skill that summarizes active alarms, plug saturation, high-value cargo exposure, and recommended inspection sequence based on risk and time remaining.

**Acceptance evidence:** Alarm triage summaries cite the current reefer cases, inspection order can be compared with manual prioritization, and corrective actions require explicit operator confirmation.

### 44. Agent Governance and Preview-Confirm Discipline
**Justification:** Helpful agent skills become operational risk if they can issue live commands without explaining impact on holds, customs, cranes, or gate capacity.

**Improvement:** Require every assistant-generated mutation to show preview diffs, affected containers or vessel calls, policy checks, and downstream impacts before a human with the right permission confirms it.

**Acceptance evidence:** Audit history records the preview, approver, and final applied command, and tests prove the assistant cannot commit state changes through hidden side paths.

### 45. Scenario Simulation for Delay and Outage Cases
**Justification:** Terminal leaders need to compare response options when weather closes the berth, a crane trips, customs scanning backs up, or gate OCR goes down.

**Improvement:** Add scenario simulation for berth delay, crane outage, yard block closure, customs inspection surge, reefer plug shortage, and gate lane failure, with impact projected onto vessel completion, dwell, and truck turn time.

**Acceptance evidence:** Scenario runs show baseline versus simulated KPIs, assumptions are explicit, and accepted response plans can be promoted into governed operational drafts.

### 46. Release Evidence Pack for Operational Readiness
**Justification:** A terminal-facing release is not ready on the strength of unit tests alone; it needs proof that domain controls, queues, and event flows are behaving.

**Improvement:** Produce a release evidence pack that includes berth-planning cases, yard-pressure cases, DG and reefer cases, customs-release cases, gate congestion cases, and replayed EDI/event traces.

**Acceptance evidence:** The package contains named scenarios, expected outcomes, captured screenshots or logs, and sign-off fields for operations, controls, and support owners.

### 47. Realistic Test Data for Vessel Calls and Container Populations
**Justification:** Thin seed data hides sequence and congestion defects that only appear when a vessel call carries realistic bay counts, discharge waves, and mixed cargo classes.

**Improvement:** Build scenario data sets for feeder, mainline, transshipment-heavy, reefer-heavy, and DG-heavy calls, with corresponding yard occupancy, gate demand, and customs-release variation.

**Acceptance evidence:** Test fixtures reproduce realistic congestion patterns, move counts and cut-off windows are plausible, and regression suites use the data to validate planning and exception behavior.

### 48. Operational KPI Baselines and Thresholds
**Justification:** The PBC should know what "good", "at risk", and "failed" look like for berth productivity, gate turn time, dwell, reefer response, and customs cycle time.

**Improvement:** Define KPI baselines and alert thresholds for berth waiting time, gross moves per hour, rehandle ratio, gate turn time, customs-release aging, reefer alarm response, and transshipment miss rate.

**Acceptance evidence:** KPI definitions are visible in the workbench, thresholds are configurable with approval history, and alerts trigger when the live metric crosses the defined boundary.

### 49. Terminal-Specific Policy Variants Under Tenant Isolation
**Justification:** Different terminals can have different tide constraints, DG rules, gate hours, customs processes, and reefer capacity, yet must stay inside the same package boundary safely.

**Improvement:** Support tenant-specific operational policies, parameter sets, and UI defaults for berth, yard, gate, customs, DG, and reefer workflows without allowing one terminal's rules or data to leak into another's.

**Acceptance evidence:** Tenant policy sets can be compared and versioned independently, cross-tenant access tests fail closed, and release evidence proves rule changes only affect the intended terminal.

### 50. Cutover, Rollback, and Recovery Drills
**Justification:** Port operations cannot accept a release that has never been tested against replay, rollback, and degraded-mode recovery under live-like pressure.

**Improvement:** Define cutover and rollback drills for EDI ingest failure, projection rebuild, crane telemetry loss, reefer alarm backlog, customs-message delay, and gate appointment overload, with explicit degraded-mode procedures.

**Acceptance evidence:** Recovery drills are executed against representative data, restore times and data-loss windows are recorded, and the release report includes unresolved recovery gaps before go-live.
