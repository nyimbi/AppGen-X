# Hospitality Property Operations PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces generic roadmap material for `hospitality_property_operations` with a hand-curated hotel operations roadmap. The scope is the owned operating core for rooms, reservations, guest stays, housekeeping, guest requests, occupancy snapshots, rate controls, governed rules, agent assistance, and release evidence, without turning this context into the source of truth for guest master data, staffing systems, supplier master data, or external payment ledgers.

## Current Domain Evidence Used

- Stable PBC key: `hospitality_property_operations`.
- Domain purpose: rooms, reservations, housekeeping, guest service, occupancy, revenue controls, and property operations.
- Owned domain tables: `room_inventory`, `reservation`, `guest_stay`, `housekeeping_task`, `guest_request`, `occupancy_snapshot`, `rate_plan`, `hospitality_property_operations_policy_rule`, `hospitality_property_operations_runtime_parameter`, `hospitality_property_operations_schema_extension`, `hospitality_property_operations_control_assertion`, `hospitality_property_operations_governed_model`.
- Public APIs: `POST /room-inventorys`, `POST /reservations`, `POST /guest-stays`, `POST /housekeeping-tasks`, `POST /guest-requests`, `GET /hospitality-property-operations-workbench`.
- Workbench and assistant surfaces: `HospitalityPropertyOperationsWorkbench`, `HospitalityPropertyOperationsDetail`, `HospitalityPropertyOperationsAssistantPanel`.
- Workflow and governance capabilities: `room_inventory_management`, `hospitality_property_operations_workflow`, `hospitality_property_operations_analytics`, `rule_engine`, `parameter_engine`, `configuration_workbench`, `ai_agent_task_assistance`, `agentic_document_instruction_intake`, `continuous_release_assurance`.
- Advanced capabilities already declared: `hospitality_property_operations_event_sourced_operational_history`, `hospitality_property_operations_multi_tenant_policy_isolation`, `hospitality_property_operations_schema_evolution_resilience`, `hospitality_property_operations_autonomous_anomaly_detection`, `hospitality_property_operations_predictive_risk_scoring`, `hospitality_property_operations_counterfactual_scenario_simulation`, `hospitality_property_operations_cryptographic_audit_proofs`, `hospitality_property_operations_continuous_control_testing`, `hospitality_property_operations_cross_pbc_event_federation`, `hospitality_property_operations_governed_ai_agent_execution`.
- Emitted events: `HospitalityPropertyOperationsCreated`, `HospitalityPropertyOperationsUpdated`, `HospitalityPropertyOperationsApproved`, `HospitalityPropertyOperationsExceptionOpened`.
- Consumed events: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`.
- Release documentation surfaces: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`.

## 50 High-Impact Improvements

### 1. Sellable room state model

**Exact key:** `room_inventory`

**Current Domain Evidence Used:** `room_inventory`, `room_inventory_management`, `POST /room-inventorys`, `HospitalityPropertyOperationsWorkbench`.

**Justification:** Front desk, housekeeping, and maintenance need one authoritative definition of vacant, occupied, inspected, dirty, blocked, out-of-order, and sellable rooms.

**Improvement:** Expand room lifecycle handling so each room tracks operational status, housekeeping status, inspection status, maintenance hold status, and sellable state with explicit transition rules and timestamps.

**Acceptance evidence:** Transition tests reject impossible room-state combinations, room timeline views show each material change, and workbench counts reconcile to the same sellable-room total by property and shift.

### 2. Room attributes, accessibility, and amenity readiness

**Exact key:** `room_inventory_management`

**Current Domain Evidence Used:** `room_inventory`, `room_inventory_management`, `HospitalityPropertyOperationsDetail`.

**Justification:** Room assignment quality depends on bed type, accessibility features, connecting-room relationships, view class, and amenity readiness, not just a room number.

**Improvement:** Extend room inventory to capture room class, bed configuration, accessibility flags, adjoining-room links, amenity kit readiness, minibar status, crib/rollaway compatibility, and inspection prerequisites for resale.

**Acceptance evidence:** Assignment tests match reservations only to compatible rooms, accessible-room protections cannot be bypassed without documented override, and detail views show the attribute set the assignment engine used.

### 3. Reservation lifecycle and guarantee controls

**Exact key:** `reservation`

**Current Domain Evidence Used:** `reservation`, `POST /reservations`, `hospitality_property_operations_workflow`.

**Justification:** Reservations move through inquiry, quoted, booked, guaranteed, modified, canceled, no-show, waitlisted, and reinstated states that drive downstream room and labor commitments.

**Improvement:** Model reservation state with guarantee status, deposit or card-hold evidence, cancellation window, source channel, arrival window, special requests, and reinstatement rules.

**Acceptance evidence:** Workflow tests enforce cutoff and cancellation rules, no-show transitions preserve the original arrival promise, and reservation state changes appear in operational queues without manual refresh.

### 4. Arrival pickup and overbooking projections

**Exact key:** `POST /reservations`

**Current Domain Evidence Used:** `reservation`, `POST /reservations`, `occupancy_snapshot`, `hospitality_property_operations_analytics`.

**Justification:** Hotel revenue control depends on projecting arrivals, wash, no-shows, early departures, and out-of-order rooms before the front desk reaches a sellout crisis.

**Improvement:** Add reservation pickup curves, no-show expectations, arrival-hour projections, oversell thresholds, and walk-risk forecasts that combine reservation status with occupancy and room-availability constraints.

**Acceptance evidence:** Projection tests produce stable forecasts for sellout and shoulder-night scenarios, daily pacing views explain the forecast inputs, and alert thresholds trigger before oversell risk becomes unavoidable.

### 5. Guest stay lifecycle for check-in, moves, and departures

**Exact key:** `guest_stay`

**Current Domain Evidence Used:** `guest_stay`, `POST /guest-stays`, `HospitalityPropertyOperationsDetail`.

**Justification:** Once a guest checks in, the operating problem changes from reservation promise management to in-house service, room moves, stay extensions, and departure readiness.

**Improvement:** Expand guest stay handling with checked-in, in-house, room-moved, extended, late-checkout, early-departure, checked-out, and post-departure review states plus linked stay notes and service flags.

**Acceptance evidence:** Tests preserve room history through moves and extensions, departure logic releases room availability only when stay closure is complete, and stay detail shows the full in-house operational timeline.

### 6. Out-of-order and out-of-service maintenance holds

**Exact key:** `room_inventory`

**Current Domain Evidence Used:** `room_inventory`, `housekeeping_task`, `occupancy_snapshot`, `HospitalityPropertyOperationsWorkbench`.

**Justification:** Property operations need a disciplined way to remove rooms from sale for maintenance, deep clean, pest control, or safety issues without losing forecast visibility.

**Improvement:** Add maintenance hold types, severity, expected return time, engineering owner, guest-impact flags, and recovery steps so blocked rooms remain operationally visible but not sellable.

**Acceptance evidence:** Room-hold tests reduce sellable inventory in occupancy views, reopening a room requires completed recovery evidence, and dashboards separate guest-occupied issues from vacant room blocks.

### 7. Housekeeping task board by zone, shift, and priority

**Exact key:** `housekeeping_task`

**Current Domain Evidence Used:** `housekeeping_task`, `POST /housekeeping-tasks`, `HospitalityPropertyOperationsWorkbench`.

**Justification:** Housekeeping teams work from boards organized by zone, room status, arrival priority, stayover commitment, and checkout turnaround pressure.

**Improvement:** Expand housekeeping tasks with room zone, attendant assignment, due window, task type, arrival dependency, expedite flag, and completion blockers so supervisors can sequence work by real hotel pressure.

**Acceptance evidence:** Task board tests sort rooms correctly for arrival-critical cleaning, overdue tasks surface by shift and zone, and supervisor reassignments preserve previous ownership and timestamps.

### 8. Room inspection and cleaning quality loops

**Exact key:** `housekeeping_task`

**Current Domain Evidence Used:** `housekeeping_task`, `hospitality_property_operations_control_assertion`, `HospitalityPropertyOperationsDetail`.

**Justification:** Marking a room clean is not enough when high-turnover floors, VIP arrivals, and repeat defects require inspection evidence and rework tracking.

**Improvement:** Add inspection-required flags, inspector identity, defect categories, rework counts, photo or note evidence, and pass-fail scoring tied to room release decisions.

**Acceptance evidence:** Inspection tests prevent resale when required checks fail, repeated defect trends appear in quality views, and room release events reference the inspection that cleared the room.

### 9. Guest request intake, SLA, and service recovery

**Exact key:** `guest_request`

**Current Domain Evidence Used:** `guest_request`, `POST /guest-requests`, `HospitalityPropertyOperationsWorkbench`.

**Justification:** Guest requests range from towels and amenities to room moves and urgent complaints, and the hotel needs one service queue with clear SLA ownership.

**Improvement:** Expand guest requests with category, urgency, promised-by time, fulfillment team, guest impact, service recovery flag, and closeout evidence for completion or failure.

**Acceptance evidence:** SLA tests route urgent requests ahead of routine amenities, breach timers pause and resume correctly on guest-dependent waits, and closeout records show whether the guest confirmed resolution.

### 10. Occupancy snapshot grain for same-day turns

**Exact key:** `occupancy_snapshot`

**Current Domain Evidence Used:** `occupancy_snapshot`, `guest_stay`, `reservation`, `hospitality_property_operations_analytics`.

**Justification:** Hotels need occupancy visibility at a finer grain than nightly totals because same-day checkouts, arrivals, stayovers, and room blocks collide throughout the day.

**Improvement:** Add snapshot dimensions for stay date, time bucket, room status mix, arrivals pending, departures pending, stayovers, out-of-service count, and same-day-turn pressure.

**Acceptance evidence:** Snapshot tests reconcile against reservations, stays, and blocked rooms, intraday occupancy views update consistently, and same-day-turn metrics explain why rooms are unavailable even before night audit.

### 11. Rate plan fences linked to operational readiness

**Exact key:** `rate_plan`

**Current Domain Evidence Used:** `rate_plan`, `occupancy_snapshot`, `room_inventory`, `hospitality_property_operations_analytics`.

**Justification:** Rate plans should react to room availability quality, not just raw occupancy percentage, because dirty rooms and blocked rooms cannot support aggressive yield decisions.

**Improvement:** Extend rate plans with room-class applicability, length-of-stay fences, closed-to-arrival rules, shoulder-night controls, amenity package promises, and housekeeping-aware sell thresholds.

**Acceptance evidence:** Pricing-control tests show rate closure when operationally ready inventory falls below threshold, plan logic preserves contractual restrictions, and analytics explain which fence drove the decision.

### 12. Group blocks and allotment pickup workflow

**Exact key:** `hospitality_property_operations_workflow`

**Current Domain Evidence Used:** `reservation`, `rate_plan`, `hospitality_property_operations_workflow`, `HospitalityPropertyOperationsWorkbench`.

**Justification:** Group blocks create distinct hotel operations pressure because pickup pace, cut dates, rooming lists, and release rules can change the availability picture overnight.

**Improvement:** Add workflow support for group blocks, allotments, rooming-list intake, pickup monitoring, attrition warnings, and block release decisions tied back to reservation and occupancy projections.

**Acceptance evidence:** Group scenarios show block pickup against sellable inventory, cut-date actions reopen unused inventory automatically when approved, and workbench queues separate group risk from transient risk.

### 13. Reservation pace, wash, and occupancy forecasting cockpit

**Exact key:** `hospitality_property_operations_analytics`

**Current Domain Evidence Used:** `hospitality_property_operations_analytics`, `reservation`, `occupancy_snapshot`, `rate_plan`.

**Justification:** Revenue and operations teams need a shared forecasting view that connects booking pace with the actual state of rooms and service capacity.

**Improvement:** Build analytics for pace, wash, pickup, length-of-stay mix, same-day arrivals, turn pressure, room-class sellout risk, and rate-plan exposure by property and date.

**Acceptance evidence:** Forecast views drill from a property summary into the room-class drivers, backtests compare projected and realized occupancy, and anomaly markers highlight abrupt pace changes.

### 14. Front desk shift handover workflow

**Exact key:** `hospitality_property_operations_workflow`

**Current Domain Evidence Used:** `guest_stay`, `guest_request`, `housekeeping_task`, `HospitalityPropertyOperationsWorkbench`.

**Justification:** Shift change is a recurring operational failure point when arrivals, unresolved requests, blocked rooms, and VIP notes live in scattered queues.

**Improvement:** Add a front desk handover workflow that bundles unresolved arrivals, room moves, payment-hold follow-ups, maintenance blocks, and guest recovery actions into one sign-off packet.

**Acceptance evidence:** Handover tests show no open item is dropped between shifts, sign-off requires acknowledging critical exceptions, and the incoming shift can filter directly from the packet into live workboards.

### 15. Policy rules for room blocking, VIP handling, and stay exceptions

**Exact key:** `hospitality_property_operations_policy_rule`

**Current Domain Evidence Used:** `hospitality_property_operations_policy_rule`, `rule_engine`, `reservation`, `guest_stay`.

**Justification:** Hotels need explicit policies for complimentary upgrades, late checkout approval, VIP room holds, inaccessible-room protection, and emergency room moves.

**Improvement:** Expand policy rules so operators can manage room-blocking criteria, service-recovery thresholds, stay exception approvals, and room-move requirements without code changes.

**Acceptance evidence:** Rule tests show policy evaluation by property and role, override paths require justification when configured, and applied rules are visible from reservation and stay timelines.

### 16. Runtime parameters for turn-time and service windows

**Exact key:** `hospitality_property_operations_runtime_parameter`

**Current Domain Evidence Used:** `hospitality_property_operations_runtime_parameter`, `parameter_engine`, `housekeeping_task`, `guest_request`.

**Justification:** Cleanup buffers, inspection thresholds, amenity replenishment times, and service windows vary by property type and season.

**Improvement:** Add governed parameters for checkout-to-clean target, inspection delay, arrival rush thresholds, housekeeping batch size, guest request SLAs, and late-night escalation windows.

**Acceptance evidence:** Parameter validation rejects out-of-bounds values, simulation previews show operational impact before activation, and audits preserve who changed service windows and why.

### 17. Front desk operations workbench lanes

**Exact key:** `HospitalityPropertyOperationsWorkbench`

**Current Domain Evidence Used:** `HospitalityPropertyOperationsWorkbench`, `reservation`, `guest_stay`, `occupancy_snapshot`.

**Justification:** Front desk teams need one operational surface for arrivals, departures, room-ready gaps, room moves, VIPs, and service recovery, not generic record lists.

**Improvement:** Split the workbench into arrival, in-house, departure, room-ready, exception, and service-recovery lanes with property, room-class, and shift filters.

**Acceptance evidence:** Route and UI tests show each lane with dedicated counts, filters persist across refreshes, and operators can open a room or stay action directly from the queue they use.

### 18. Room detail workbench with operational evidence

**Exact key:** `HospitalityPropertyOperationsDetail`

**Current Domain Evidence Used:** `HospitalityPropertyOperationsDetail`, `room_inventory`, `housekeeping_task`, `guest_request`.

**Justification:** Supervisors need a room-centric view of status, cleaning history, inspection results, maintenance blocks, and active guest-facing issues during recovery decisions.

**Improvement:** Turn detail pages into room workbenches that combine room status, current stay link, last cleaned time, open tasks, defect history, and readiness evidence in one place.

**Acceptance evidence:** Detail tests show consistent room history after moves and blocks, related tasks load without cross-table leakage, and decision evidence is visible before a room is returned to sale.

### 19. Assistant panel for hotel operations roles

**Exact key:** `HospitalityPropertyOperationsAssistantPanel`

**Current Domain Evidence Used:** `HospitalityPropertyOperationsAssistantPanel`, `ai_agent_task_assistance`, `HospitalityPropertyOperationsWorkbench`.

**Justification:** Front desk agents, housekeeping supervisors, and managers need guided actions and summaries tuned to hotel work rather than generic chatbot responses.

**Improvement:** Add assistant panels for arrival prep, room-ready triage, guest request summaries, inspection follow-up, oversell risk explanation, and handover recap generation.

**Acceptance evidence:** Assistant flows show role-specific prompts, blocked actions explain missing permissions or evidence, and generated summaries link back to the source records they rely on.

### 20. Actionable agent skills for task boards

**Exact key:** `ai_agent_task_assistance`

**Current Domain Evidence Used:** `ai_agent_task_assistance`, `guest_request`, `housekeeping_task`, `permissions`.

**Justification:** The assistant should help dispatch and explain work, but it cannot become a hidden bypass around approvals, service promises, or room-status controls.

**Improvement:** Add agent skills for assigning attendants, reprioritizing service queues, drafting room-move plans, summarizing arrival risk, and preparing exception notes through governed commands only.

**Acceptance evidence:** Skill tests require preview and confirm steps for material actions, denied actions surface the policy reason, and every accepted assistant action writes audit-ready evidence.

### 21. Document intake for rooming lists and guest instructions

**Exact key:** `agentic_document_instruction_intake`

**Current Domain Evidence Used:** `agentic_document_instruction_intake`, `reservation`, `guest_request`, `POST /reservations`.

**Justification:** Group business and concierge-style service often arrive as rooming lists, event sheets, arrival memos, and special instruction documents that need structured handling.

**Improvement:** Add document intake that extracts rooming-list details, arrival notes, amenity requests, accessible-room needs, and service timing promises into draft reservations and task queues.

**Acceptance evidence:** Intake tests show extracted fields with confidence and source spans, risky changes stay in draft until confirmed, and rejected document rows are routed to review queues.

### 22. Event history for rooms, stays, and service work

**Exact key:** `hospitality_property_operations_event_sourced_operational_history`

**Current Domain Evidence Used:** `hospitality_property_operations_event_sourced_operational_history`, `room_inventory`, `guest_stay`, `guest_request`.

**Justification:** Disputes about whether a room was ready, a guest requested help, or a late checkout was approved depend on precise event order and replayable history.

**Improvement:** Store immutable operational history for room status changes, reservation edits, stay lifecycle events, housekeeping completions, inspection failures, and guest-request escalations.

**Acceptance evidence:** Replay tests rebuild room and stay timelines exactly, point-in-time views match stored projections, and the audit trail shows actor, source command, and property scope for each event.

### 23. Idempotent intake and correction handling

**Exact key:** `idempotent_handlers`

**Current Domain Evidence Used:** `idempotent_handlers`, `POST /reservations`, `POST /guest-stays`, `POST /guest-requests`.

**Justification:** Channel retries, duplicate front desk clicks, and repeated guest-service submissions should not create double arrivals, duplicate stays, or duplicate room-service work.

**Improvement:** Add idempotency keys and correction semantics for reservation intake, check-in commands, room moves, housekeeping updates, and guest-request creation.

**Acceptance evidence:** Duplicate-command tests preserve one business outcome, corrections show before-and-after lineage, and retry-safe behavior holds across process restarts and queue replays.

### 24. Boundary-safe event projections

**Exact key:** `appgen_x_outbox_inbox_eventing`

**Current Domain Evidence Used:** `appgen_x_outbox_inbox_eventing`, `occupancy_snapshot`, `HospitalityPropertyOperationsWorkbench`, `hospitality_property_operations_cross_pbc_event_federation`.

**Justification:** Hotel operations need near-real-time projections, but those views must stay on declared events and APIs rather than direct reads into other domains.

**Improvement:** Build projection pipelines for arrivals, departures, room-ready status, and guest-service health using declared event contracts and inbox-outbox patterns only.

**Acceptance evidence:** Contract tests fail on undeclared external table access, projections stay fresh under replay, and workbench health panels show lag and recovery state for each read model.

### 25. Retry and dead-letter workbench for operational queues

**Exact key:** `retry_dead_letter_evidence`

**Current Domain Evidence Used:** `retry_dead_letter_evidence`, `guest_request`, `housekeeping_task`, `HospitalityPropertyOperationsWorkbench`.

**Justification:** When queue handlers fail, hotels still need to see which requests, room updates, and occupancy projections are stuck before they affect guests.

**Improvement:** Add a dead-letter operations board for failed room, stay, housekeeping, and guest-request messages with retry eligibility, root-cause notes, and replay safety checks.

**Acceptance evidence:** Failure tests route poison messages to quarantine, authorized retries preserve idempotency, and the workbench links each dead letter to the business item it delayed.

### 26. Declared cross-domain boundaries for guest and supplier data

**Exact key:** `hospitality_property_operations_cross_pbc_event_federation`

**Current Domain Evidence Used:** `hospitality_property_operations_cross_pbc_event_federation`, `CustomerUpdated`, `SupplierQualified`, `PolicyChanged`.

**Justification:** This context needs guest-profile freshness, supplier qualification, and policy updates, but it should not silently absorb ownership of those upstream systems.

**Improvement:** Formalize event and API boundaries for guest identity changes, outsourced service vendor readiness, and policy updates with freshness indicators and fallback behavior.

**Acceptance evidence:** Boundary tests prove hotel operations can continue in degraded mode using declared projections, stale upstream data is surfaced explicitly, and no hidden foreign-table dependency appears in generated artifacts.

### 27. Predictive risk scoring for arrivals and room readiness

**Exact key:** `hospitality_property_operations_predictive_risk_scoring`

**Current Domain Evidence Used:** `hospitality_property_operations_predictive_risk_scoring`, `reservation`, `housekeeping_task`, `occupancy_snapshot`.

**Justification:** Managers need early warning when a high-value arrival is likely to miss room-ready time because of blocked inventory, inspection failures, or staff pressure.

**Improvement:** Add explainable risk models for room-not-ready arrivals, oversell exposure, guest-request breach risk, amenity shortfall, and maintenance recovery delay.

**Acceptance evidence:** Risk tests generate low, medium, and high alerts with feature explanations, feedback loops capture whether the alert was useful, and action cards open the exact queue that can reduce the risk.

### 28. Counterfactual simulation for sellout and disruption days

**Exact key:** `hospitality_property_operations_counterfactual_scenario_simulation`

**Current Domain Evidence Used:** `hospitality_property_operations_counterfactual_scenario_simulation`, `reservation`, `occupancy_snapshot`, `rate_plan`.

**Justification:** Hotel leaders need to compare what happens if they accept another group block, lose ten rooms to maintenance, or shorten checkout buffers on a compressed day.

**Improvement:** Add non-mutating scenario simulation for sellout nights, storm disruptions, housekeeping shortages, group cancellations, room-block recovery, and late-checkout surges.

**Acceptance evidence:** Simulation tests preserve production data immutability, scenario reports compare occupancy and service outcomes side by side, and chosen assumptions are visible to reviewers.

### 29. Autonomous anomaly detection for room-state contradictions

**Exact key:** `hospitality_property_operations_autonomous_anomaly_detection`

**Current Domain Evidence Used:** `hospitality_property_operations_autonomous_anomaly_detection`, `room_inventory`, `guest_stay`, `occupancy_snapshot`.

**Justification:** The most costly hotel mistakes are often contradictions such as occupied rooms marked vacant, cleaned rooms failing inspection, or arrivals assigned to blocked rooms.

**Improvement:** Add anomaly checks for impossible room-state combinations, duplicate active stays, repeated room moves, stuck housekeeping tasks, and occupancy spikes that do not match reservation behavior.

**Acceptance evidence:** Anomaly tests surface contradictions with clear reasons, suppression rules are auditable, and operational dashboards show anomaly age and closure status.

### 30. Continuous control testing for operational integrity

**Exact key:** `hospitality_property_operations_continuous_control_testing`

**Current Domain Evidence Used:** `hospitality_property_operations_continuous_control_testing`, `hospitality_property_operations_control_assertion`, `permissions`.

**Justification:** Property operations need recurring control checks because the biggest failures come from drift, skipped inspections, unapproved room returns, and manual queue shortcuts.

**Improvement:** Add continuous controls for occupied-clean mismatch, room released without inspection, guest-request closure without evidence, unauthorized override, and stale blocked-room recovery.

**Acceptance evidence:** Control tests emit failures with business context, daily evidence snapshots show pass and fail counts by property, and unresolved control failures stay visible in workbench exception lanes.

### 31. Cryptographic proof for inspection and release evidence

**Exact key:** `hospitality_property_operations_cryptographic_audit_proofs`

**Current Domain Evidence Used:** `hospitality_property_operations_cryptographic_audit_proofs`, `hospitality_property_operations_control_assertion`, `RELEASE_EVIDENCE.md`.

**Justification:** Inspection results, room-release approvals, and release audit packets should be tamper-evident when they support disputes or internal assurance.

**Improvement:** Hash-chain critical inspection, exception, approval, and release artifacts so exported evidence packets can be verified without exposing sensitive guest details.

**Acceptance evidence:** Proof-verification tests detect altered evidence, export flows include proof manifests, and release packets show which hotel operations records are covered by each proof chain.

### 32. Release evidence expansion for hotel operations flows

**Exact key:** `continuous_release_assurance`

**Current Domain Evidence Used:** `continuous_release_assurance`, `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`.

**Justification:** A release should prove the hotel operating surfaces work for rooms, stays, housekeeping, and service recovery instead of only proving files exist.

**Improvement:** Expand release evidence so it covers arrival readiness, same-day turns, guest-request SLA flows, blocked-room recovery, forecast calculations, and assistant guardrails.

**Acceptance evidence:** Release checks fail when any named operating path lacks evidence, the evidence packet links back to specification clauses, and generated smoke runs include hotel-specific scenarios rather than generic CRUD checks.

### 33. Governed AI execution for front desk and housekeeping roles

**Exact key:** `hospitality_property_operations_governed_ai_agent_execution`

**Current Domain Evidence Used:** `hospitality_property_operations_governed_ai_agent_execution`, `ai_agent_task_assistance`, `permissions`.

**Justification:** Hotel staff can benefit from agent help, but room assignment, upgrade, move, and compensation decisions must remain policy-governed and reviewable.

**Improvement:** Add governed execution policies for front desk agent skills, housekeeping dispatch skills, and manager exception skills with approval thresholds, safe-read defaults, and escalation requirements.

**Acceptance evidence:** Policy tests show which actions can run automatically, which require human confirmation, and which are blocked entirely, and every assistant action writes structured governance evidence.

### 34. Multi-property and tenant isolation

**Exact key:** `hospitality_property_operations_multi_tenant_policy_isolation`

**Current Domain Evidence Used:** `hospitality_property_operations_multi_tenant_policy_isolation`, `permissions`, `configuration_workbench`.

**Justification:** Hotel groups need strict isolation across brands and properties while still allowing consistent operating templates where policy permits.

**Improvement:** Add tenant-scoped and property-scoped policies for room rules, service windows, dashboard visibility, and assistant behaviors with no cross-property leakage.

**Acceptance evidence:** Isolation tests block cross-tenant reads and writes, approved template rollout preserves property overrides, and admin views cannot mix one property's service evidence into another's queues.

### 35. Schema extension registry for property-specific room taxonomies

**Exact key:** `hospitality_property_operations_schema_evolution_resilience`

**Current Domain Evidence Used:** `hospitality_property_operations_schema_evolution_resilience`, `hospitality_property_operations_schema_extension`, `room_inventory`.

**Justification:** Resort, city hotel, extended-stay, and serviced-apartment operations need different room and amenity fields without destabilizing the core model.

**Improvement:** Add governed schema extensions for property-specific room classes, amenity bundles, inspection checklists, and service programs with compatibility checks and migration previews.

**Acceptance evidence:** Extension tests protect existing APIs and projections, preview tools show downstream impact before activation, and rollback evidence exists for rejected or superseded extensions.

### 36. Governed model registry for forecasting and recommendation logic

**Exact key:** `hospitality_property_operations_governed_model`

**Current Domain Evidence Used:** `hospitality_property_operations_governed_model`, `hospitality_property_operations_predictive_risk_scoring`, `rate_plan`.

**Justification:** Forecasting and recommendation logic changes business behavior, so model versions need their own governance trail inside hotel operations.

**Improvement:** Add a governed model registry for arrival-risk scoring, room-ready recommendations, overbooking alerts, and staffing-pressure predictions with version, training window, owner, and retirement state.

**Acceptance evidence:** Model-governance tests require approval before activation, model cards show supported use cases and known limits, and decision traces identify the model version that influenced the recommendation.

### 37. Configuration workbench for property calendars and standards

**Exact key:** `configuration_workbench`

**Current Domain Evidence Used:** `configuration_workbench`, `hospitality_property_operations_runtime_parameter`, `HospitalityPropertyOperationsWorkbench`.

**Justification:** Operators need a safe place to manage service windows, holiday calendars, room-clean standards, and amenity defaults without editing raw configuration values.

**Improvement:** Add configuration workbench screens for property calendars, room-status defaults, inspection programs, amenity-restock standards, and service-hour policies.

**Acceptance evidence:** UI tests show editable but governed configuration forms, diff views explain pending changes before activation, and rollback restores prior settings without breaking active queues.

### 38. Rule engine for room moves, late checkout, and service recovery

**Exact key:** `rule_engine`

**Current Domain Evidence Used:** `rule_engine`, `guest_stay`, `guest_request`, `rate_plan`.

**Justification:** Frequent hotel exceptions such as late checkout, complimentary upgrade, or room move need consistent rules because they affect both guest experience and room availability.

**Improvement:** Add rule sets for room-move eligibility, late-checkout approval, service-recovery compensation limits, amenity exception approval, and alternate-room selection.

**Acceptance evidence:** Rule tests cover routine and edge-case scenarios, the applied rule path is visible to staff, and overrides cannot close without the configured justification.

### 39. Parameter engine for forecast horizons and labor buffers

**Exact key:** `parameter_engine`

**Current Domain Evidence Used:** `parameter_engine`, `occupancy_snapshot`, `housekeeping_task`, `hospitality_property_operations_analytics`.

**Justification:** Forecast usefulness depends on horizon, smoothing, labor assumptions, and rush-period buffers that differ by operating model and season.

**Improvement:** Add parameter sets for forecast horizon, wash assumptions, room-turn buffers, inspector capacity, guest-request escalation windows, and same-day-turn thresholds.

**Acceptance evidence:** Parameter tests show recalculated outputs after approved changes, invalid combinations are blocked before activation, and analysts can compare prior and proposed settings in one view.

### 40. Permission model by role, shift, and property

**Exact key:** `permissions`

**Current Domain Evidence Used:** `permissions`, `reservation`, `guest_stay`, `housekeeping_task`.

**Justification:** A front desk agent, housekeeping supervisor, room inspector, and operations manager should not have the same ability to move rooms, close tasks, or approve overrides.

**Improvement:** Extend permissions to cover role, property, shift, action type, and exception severity for room blocks, stay edits, service recovery, and assistant-triggered commands.

**Acceptance evidence:** Authorization tests block unauthorized actions, disabled UI controls explain why access is denied, and assistant flows inherit the same permission outcomes as direct user actions.

### 41. Guest request API completeness and query surfaces

**Exact key:** `POST /guest-requests`

**Current Domain Evidence Used:** `POST /guest-requests`, `guest_request`, `GET /hospitality-property-operations-workbench`.

**Justification:** Service teams need more than create-only request APIs because they must triage, assign, escalate, fulfill, and analyze request patterns in real time.

**Improvement:** Expand the guest-request API set to include list, search, SLA status, escalation, fulfillment evidence, reopen, and export operations with clear versioning.

**Acceptance evidence:** API contract tests cover request lifecycle commands and queries, idempotent reopen behavior is enforced, and client examples show how service workboards consume the new surfaces.

### 42. Housekeeping task bulk assignment and mobile-safe updates

**Exact key:** `POST /housekeeping-tasks`

**Current Domain Evidence Used:** `POST /housekeeping-tasks`, `housekeeping_task`, `HospitalityPropertyOperationsWorkbench`.

**Justification:** Supervisors often need to rebalance dozens of rooms at once during rush periods, and attendants may update task state from constrained devices on the floor.

**Improvement:** Add bulk assign, bulk reprioritize, offline-tolerant completion updates, inspection handoff commands, and room-ready publish operations for housekeeping tasks.

**Acceptance evidence:** Bulk-operation tests preserve per-room audit trails, retry behavior does not duplicate completions, and offline replay surfaces conflicts for review instead of silently overwriting them.

### 43. Stay API boundaries for check-in, room move, and checkout

**Exact key:** `POST /guest-stays`

**Current Domain Evidence Used:** `POST /guest-stays`, `guest_stay`, `room_inventory`, `reservation`.

**Justification:** Front desk workflows need explicit commands for check-in, room assignment, room move, extension, early departure, and checkout because each has different validation and side effects.

**Improvement:** Expand stay APIs into separate commands for arrival validation, check-in, assign-room, move-room, extend-stay, checkout, and reopen-post-departure correction with clear payload boundaries.

**Acceptance evidence:** Contract tests show each command's preconditions, side effects on room status are visible and replay-safe, and invalid direct state mutation attempts are rejected.

### 44. Room inventory APIs for blocks, returns, and amenity status

**Exact key:** `POST /room-inventorys`

**Current Domain Evidence Used:** `POST /room-inventorys`, `room_inventory`, `housekeeping_task`, `guest_request`.

**Justification:** Room operations need command surfaces for maintenance blocks, inspection release, amenity readiness updates, and temporary room holds that are distinct from initial room creation.

**Improvement:** Add room commands for place-block, release-block, mark-dirty, mark-clean, fail-inspection, pass-inspection, update-amenity-readiness, and publish-room-ready.

**Acceptance evidence:** API tests prove state guards on every command, duplicate room-ready publishes remain idempotent, and room command history appears consistently across room, stay, and workbench views.

### 45. Consolidated workbench query boundary

**Exact key:** `GET /hospitality-property-operations-workbench`

**Current Domain Evidence Used:** `GET /hospitality-property-operations-workbench`, `HospitalityPropertyOperationsWorkbench`, `occupancy_snapshot`.

**Justification:** Hotel operators need one query surface that joins arrivals, room readiness, housekeeping load, and guest-service pressure without forcing UI code to stitch raw records together.

**Improvement:** Expand the workbench query boundary to deliver consolidated arrival queues, room-ready gaps, same-day-turn risk, guest-request heatmaps, and blocked-room summaries with freshness metadata.

**Acceptance evidence:** Query tests show stable response contracts across filters and time windows, freshness markers are populated for every panel, and the UI renders without additional hidden joins.

### 46. Typed emitted events for hotel operations milestones

**Exact key:** `HospitalityPropertyOperationsCreated`

**Current Domain Evidence Used:** `HospitalityPropertyOperationsCreated`, `HospitalityPropertyOperationsUpdated`, `HospitalityPropertyOperationsApproved`, `HospitalityPropertyOperationsExceptionOpened`.

**Justification:** Generic lifecycle events are not enough when downstream consumers care about room-ready publication, oversell exception opened, guest request breached, or stay moved.

**Improvement:** Add typed emitted events for room blocked, room ready, arrival checked in, stay moved, stay extended, guest request escalated, inspection failed, and sellout risk opened.

**Acceptance evidence:** Event schema tests preserve backward compatibility where required, examples show hotel-specific payload intent, and release evidence includes emitted-event coverage for the named milestones.

### 47. Policy change handlers for operational rule drift

**Exact key:** `PolicyChanged`

**Current Domain Evidence Used:** `PolicyChanged`, `hospitality_property_operations_policy_rule`, `appgen_x_outbox_inbox_eventing`.

**Justification:** When upstream policy changes arrive, hotels need to recalculate room-block rules, service promises, and approval thresholds without silent drift.

**Improvement:** Add handlers that ingest policy changes, identify impacted room, stay, request, and rule projections, and open explicit review work when a change alters live operating behavior.

**Acceptance evidence:** Handler tests show replay-safe recalculation, impacted queues are visible to reviewers, and stale-policy conditions appear in dashboards until the new rules are acknowledged.

### 48. Customer update handlers for guest preference freshness

**Exact key:** `CustomerUpdated`

**Current Domain Evidence Used:** `CustomerUpdated`, `reservation`, `guest_stay`, `guest_request`.

**Justification:** Hotels need guest-profile freshness for accessibility requests, loyalty treatment, and service preferences, but the source guest profile still belongs elsewhere.

**Improvement:** Add customer-update handlers that refresh guest preference projections, flag impacted arrivals or in-house stays, and preserve a freshness indicator on hotel-side copies.

**Acceptance evidence:** Tests show preference updates affect future operational decisions without rewriting historical stay evidence, stale guest-profile data is visible to staff, and no customer-master table coupling is introduced.

### 49. Supplier qualification handlers for outsourced services

**Exact key:** `SupplierQualified`

**Current Domain Evidence Used:** `SupplierQualified`, `housekeeping_task`, `guest_request`, `hospitality_property_operations_cross_pbc_event_federation`.

**Justification:** Hotels often depend on outsourced housekeeping, linen, floral, amenity, or engineering vendors, and qualification loss can immediately change service capacity.

**Improvement:** Add supplier-qualification handlers that update vendor-readiness projections, warn on tasks assigned to unavailable vendors, and open contingency work for affected service lines.

**Acceptance evidence:** Tests show qualification loss creates actionable exceptions, unaffected queues continue normally, and vendor-readiness projections remain traceable to the inbound supplier event.

### 50. End-to-end release proof for arrival-to-room-ready operations

**Exact key:** `RELEASE_EVIDENCE.md`

**Current Domain Evidence Used:** `RELEASE_EVIDENCE.md`, `SPECIFICATION.md`, `HospitalityPropertyOperationsWorkbench`, `HospitalityPropertyOperationsAssistantPanel`.

**Justification:** The strongest release proof for this context is an arrival-to-departure operating story that shows reservations, room readiness, housekeeping, guest service, assistant guardrails, and evidence capture working together.

**Improvement:** Add an end-to-end release scenario that starts with forecasted arrivals, processes a blocked-room exception, reassigns housekeeping work, completes inspection, checks in the guest, resolves a guest request, and closes the stay with preserved evidence.

**Acceptance evidence:** Release artifacts include scenario data, expected workbench states, emitted events, control results, assistant interactions, and reviewer sign-off showing the full hotel operations loop passed.
