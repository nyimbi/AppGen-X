# Improvement Backlog for `fleet_mobility_operations`

## Current Domain Evidence Used

- Manifest key: `fleet_mobility_operations`.
- Declared domain description: vehicles, drivers, telematics, routing, maintenance, utilization, fuel, safety, and fleet compliance.
- Owned tables: `vehicle`, `driver_assignment`, `telematics_event`, `route_plan`, `fuel_transaction`, `maintenance_schedule`, `safety_event`, `fleet_mobility_operations_policy_rule`, `fleet_mobility_operations_runtime_parameter`, `fleet_mobility_operations_schema_extension`, `fleet_mobility_operations_control_assertion`, `fleet_mobility_operations_governed_model`.
- Public APIs: `POST /vehicles`, `POST /driver-assignments`, `POST /telematics-events`, `POST /route-plans`, `POST /fuel-transactions`, `GET /fleet-mobility-operations-workbench`.
- Workflows: `fleet_mobility_operations_create_vehicle_workflow`, `fleet_mobility_operations_record_driver_assignment_workflow`.
- UI fragments: `FleetMobilityOperationsWorkbench`, `FleetMobilityOperationsDetail`, `FleetMobilityOperationsAssistantPanel`.
- Emitted events: `FleetMobilityOperationsCreated`, `FleetMobilityOperationsUpdated`, `FleetMobilityOperationsApproved`, `FleetMobilityOperationsExceptionOpened`.
- Consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Advanced capabilities already declared in the manifest include event-sourced operational history, predictive risk scoring, counterfactual scenario simulation, autonomous anomaly detection, cryptographic audit proofs, continuous control testing, cross-PBC event federation, carbon and sustainability awareness, and governed AI agent execution.
- Evidence documents named in the manifest: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

## Backlog

### 1. Vehicle dispatch-readiness ledger

**Justification:** Dispatch needs a single readiness answer before a vehicle is assigned, but the manifest only shows `vehicle`, `maintenance_schedule`, and `safety_event` as separate surfaces.

**Improvement:** Introduce a readiness projection that combines registration status, open maintenance, unresolved safety events, current assignment state, fuel or state-of-charge thresholds, and telematics freshness into one dispatchable verdict per vehicle.

**Acceptance evidence:** Workbench readiness badges on `GET /fleet-mobility-operations-workbench`, projection tests covering ready and blocked cases, and release evidence showing why a blocked vehicle cannot enter a route plan.

### 2. Assignment overlap and rest-window enforcement

**Justification:** `driver_assignment` without overlap, shift, and rest checks will produce unsafe dispatches and unreliable utilization figures.

**Improvement:** Add assignment validation that blocks overlapping shifts, enforces minimum rest windows, flags missing handoff acknowledgements, and records the exact reason an assignment was accepted or refused.

**Acceptance evidence:** API contract tests for `POST /driver-assignments`, rule-evaluation evidence for overlap and rest scenarios, and workbench exception queues showing blocked assignments with operator-resolvable actions.

### 3. Dispatch board for live reallocation

**Justification:** Fleet operators need to rebalance vehicles and drivers when absences, breakdowns, or route slippage occur, and the current manifest exposes only a generic workbench surface.

**Improvement:** Add a dispatch board to `FleetMobilityOperationsWorkbench` that shows unassigned vehicles, unassigned drivers, route-plan gaps, late departures, and one-click reassignment flows with policy checks.

**Acceptance evidence:** UI interaction coverage for drag-and-drop or action-button reassignment, audit events for each reassignment, and release evidence with before-and-after dispatch snapshots.

### 4. Stop-level route ETA projection

**Justification:** `route_plan` is present, but operators also need projected arrival, dwell, delay, and completion risk at each stop rather than only a plan header.

**Improvement:** Build a stop-level projection that combines route plans with the latest telematics event stream to show live ETA drift, missed-stop risk, dwell overrun, and route completion confidence.

**Acceptance evidence:** Projection tests using delayed and on-time telematics samples, workbench timeline views for route progress, and release evidence proving ETA recalculation after new telemetry arrives.

### 5. Telematics quarantine for malformed device traffic

**Justification:** `POST /telematics-events` will receive duplicated, delayed, out-of-order, and malformed messages in production.

**Improvement:** Split telematics ingestion into accept, quarantine, and reject paths with schema validation, device identity checks, timestamp sanity windows, and replay-safe idempotency keys.

**Acceptance evidence:** Ingestion tests for duplicates, future-dated events, stale payloads, and unknown devices; dead-letter evidence for quarantined traffic; and workbench visibility into quarantine backlog size.

### 6. Trip reconstruction from event streams

**Justification:** The manifest declares event-sourced operational history, but fleet investigations also need reconstructed trips, not just raw event logs.

**Improvement:** Derive trip sessions from `telematics_event` so operators can see ignition windows, route deviation, idle segments, excessive dwell, and unscheduled stops for each completed movement.

**Acceptance evidence:** Replay tests that rebuild trip segments from ordered events, detail views that link a trip to its vehicle and assignment, and release evidence showing reconstructed versus planned movement.

### 7. Maintenance readiness horizon

**Justification:** `maintenance_schedule` exists, but dispatchers need forward-looking readiness, not only a list of scheduled services.

**Improvement:** Add a maintenance horizon projection showing services due in the next 7, 14, and 30 days using odometer, engine hours, telematics-derived wear signals, and route commitments.

**Acceptance evidence:** Projection tests for mileage-triggered and date-triggered maintenance, readiness warnings inside the workbench, and release evidence demonstrating that high-risk vehicles are withheld from new assignments.

### 8. Roadside breakdown incident command view

**Justification:** `safety_event` covers incidents, but roadside failures need a coordinated workflow across dispatch, maintenance, and driver support.

**Improvement:** Create an incident command view that records incident location, driver status, towing need, replacement vehicle action, rerouting action, and service return criteria.

**Acceptance evidence:** Incident lifecycle tests, workbench incident drill-down with status transitions, and release evidence linking incident closure to reopened route or replacement dispatch decisions.

### 9. Fuel fraud and abnormal burn detection

**Justification:** `fuel_transaction` alone cannot explain whether fuel spend aligns with telematics distance, idling, or route conditions.

**Improvement:** Add reconciliation between fuel transactions, telematics odometer deltas, idle time, and route-plan distance to detect siphoning, duplicate fills, inefficient burn, and fueling outside approved geofences.

**Acceptance evidence:** Detection tests for duplicate fuel card swipes and abnormal consumption, exception records with investigation notes, and release evidence showing resolved versus unresolved fuel anomalies.

### 10. EV charging readiness planner

**Justification:** The manifest covers fuel transactions but the domain description includes fleet mobility more broadly, which should include electric vehicle dispatch readiness.

**Improvement:** Extend energy management so vehicles can be blocked or prioritized based on state of charge, charger availability, charging-window fit, and route energy requirement.

**Acceptance evidence:** Readiness rules for low-charge scenarios, workbench energy queue views, and release evidence proving that an EV with insufficient charge cannot be dispatched to an energy-intensive route.

### 11. Utilization heatmap by depot, class, and shift

**Justification:** The manifest names utilization in the description, but operators need to see underused and overused assets at a glance.

**Improvement:** Add utilization analytics that break down vehicle active hours, idle hours, route occupancy, assignment gaps, and maintenance downtime by depot, vehicle class, and shift window.

**Acceptance evidence:** Metric definitions behind `fleet_mobility_operations_workbench_metric`, analytical tests for utilization percentages, and workbench heatmaps that drill into the drivers of low utilization.

### 12. Geofence arrival, dwell, and exit controls

**Justification:** Routing and telematics are both declared, and geofencing is the operational boundary that ties them together for dispatch and compliance.

**Improvement:** Add managed geofences for depots, yards, customer sites, fueling stations, no-go zones, and charging sites, with arrival, dwell, and exit events derived from telematics movement.

**Acceptance evidence:** Geofence entry and exit tests, dwell-threshold exceptions in the workbench, and release evidence showing a route deviation triggered by an unauthorized geofence visit.

### 13. Driver license, certification, and medical expiry controls

**Justification:** Fleet compliance is explicitly in scope, and assignment quality depends on driver credentials being current before dispatch.

**Improvement:** Extend `driver_assignment` validation to check license class, endorsements, medical certificate validity, training completion, and jurisdiction-specific compliance before a driver can accept a vehicle or route.

**Acceptance evidence:** Assignment rejection tests for expired credentials, compliance cards in the detail view, and release evidence proving that blocked drivers cannot be scheduled until evidence is refreshed.

### 14. Driver behavior scoring from telematics

**Justification:** Safety outcomes improve when speeding, harsh braking, rapid acceleration, seat-belt gaps, and excessive idle behavior are turned into action, not just stored as raw telemetry.

**Improvement:** Build a driver-behavior score that turns telematics events into coaching queues, route risk alerts, and supervisor review tasks without mutating source telemetry.

**Acceptance evidence:** Scoring model tests with explainable component weights, supervisor workbench views for coaching actions, and release evidence linking score changes to subsequent incident reduction.

### 15. Dispatch exception SLA engine

**Justification:** `FleetMobilityOperationsExceptionOpened` exists, but operators still need timing expectations for assignment, route, maintenance, and safety exceptions.

**Improvement:** Add SLA clocks for unassigned routes, blocked vehicles, overdue incident follow-up, stale telematics feeds, and unresolved compliance gaps, with pause and escalation rules by exception type.

**Acceptance evidence:** Timer tests for pause and resume logic, workbench aging buckets, and release evidence showing automatic escalation when an exception breaches its service window.

### 16. Fleet control tower workbench

**Justification:** One generic workbench page is insufficient for dispatchers managing live vehicle movement, assignment changes, and route risk.

**Improvement:** Turn `FleetMobilityOperationsWorkbench` into a control tower with dispatch board, live route map, blocked-asset queue, telematics freshness indicators, and high-risk exception panels.

**Acceptance evidence:** UI route coverage for control-tower views, permission-aware action controls, and release evidence with screenshots demonstrating the live operational posture in one place.

### 17. Workshop planner workbench

**Justification:** Maintenance teams need a different operational surface from dispatch teams even though both rely on the same `maintenance_schedule` and `vehicle` tables.

**Improvement:** Add a workshop planning view that shows due services, parts readiness, workshop bay capacity, replacement-vehicle need, and service return-to-road decisions.

**Acceptance evidence:** UI coverage for workshop queues, readiness calculations for pending parts and open defects, and release evidence showing a vehicle moving from due-service to cleared-for-dispatch.

### 18. Safety and compliance workbench

**Justification:** `safety_event` and compliance checks need a dedicated operator surface so incidents, driver issues, and audit tasks are not buried in dispatch screens.

**Improvement:** Add a safety and compliance workbench view for incident queues, driver credential gaps, policy breaches, coaching actions, and audit-ready evidence exports.

**Acceptance evidence:** Permission-aware UI tests for safety roles, exception drill-downs tied to source records, and release evidence showing a closed-loop investigation from incident open to evidence export.

### 19. Dispatch replanning agent skill

**Justification:** The manifest declares `ai_agent_task_assistance` and governed AI execution, so the assistant should help dispatch without bypassing fleet controls.

**Improvement:** Add an assistant skill in `FleetMobilityOperationsAssistantPanel` that proposes replacement vehicles, alternative drivers, and revised route priorities after a breakdown or delay, always as previewed actions.

**Acceptance evidence:** Skill tests proving preview-only behavior before approval, audit traces showing user confirmation, and release evidence demonstrating a suggested replan after a route disruption.

### 20. Maintenance triage agent skill

**Justification:** Maintenance planners spend time sorting symptoms, service history, and telematics alerts into repair priorities.

**Improvement:** Add an assistant skill that summarizes fault evidence, proposes repair sequencing, highlights repeat failures, and suggests whether a vehicle should be removed from dispatch rotation.

**Acceptance evidence:** Assistant output with source citations to maintenance and telematics records, approval gates before any status change, and release evidence showing a triage summary used to block a risky vehicle.

### 21. Assignment command boundary expansion

**Justification:** The manifest exposes `POST /driver-assignments`, but production dispatch needs validate, confirm, cancel, handoff, and close commands with explicit intent.

**Improvement:** Expand the assignment API boundary to include validation-only checks, driver acknowledgement capture, reassignment commands, cancellation reasons, and closeout of completed assignments.

**Acceptance evidence:** Route-level contract tests for each command, idempotency checks for repeated calls, and release evidence showing API usage mapped to workbench actions rather than direct table edits.

### 22. Query boundary for route and telematics read models

**Justification:** Operators should not rely on raw table inspection to answer live dispatch questions.

**Improvement:** Add explicit read-model endpoints for route progress, telematics freshness, geofence activity, utilization summaries, and maintenance readiness rather than overloading `GET /fleet-mobility-operations-workbench`.

**Acceptance evidence:** Read-model contract tests, freshness metadata in responses, and release evidence showing UI workbenches served by API projections instead of ad hoc joins.

### 23. Vehicle readiness change event contract

**Justification:** Readiness changes affect dispatch, maintenance, and downstream operations and should be visible through typed events.

**Improvement:** Introduce emitted events for readiness-blocked, readiness-restored, and readiness-risk-raised states so downstream consumers can react without reading fleet tables.

**Acceptance evidence:** Event schema tests, outbox evidence for readiness transitions, and release evidence showing a blocked vehicle state emitted after a critical safety event.

### 24. Route reprojection event contract

**Justification:** ETA drift and route deviation matter beyond the workbench and should be broadcast as operational state changes.

**Improvement:** Emit events when a route is materially reprojected due to telematics delay, reassignment, geofence deviation, or maintenance withdrawal of a planned vehicle.

**Acceptance evidence:** Event emission tests tied to projection changes, event payload examples with old and new ETA windows, and release evidence showing downstream notification triggered by a reprojection event.

### 25. Incident lifecycle event contract

**Justification:** `FleetMobilityOperationsExceptionOpened` is too broad to capture the operational detail of crashes, breakdowns, compliance breaches, and roadside failures.

**Improvement:** Add typed incident events for opened, escalated, contained, reassigned, and closed states, with actor, asset, route, and evidence references.

**Acceptance evidence:** Event schema snapshots, replay tests for incident lifecycle ordering, and release evidence showing an incident closure event linked to restored dispatch readiness.

### 26. Idempotent device-message handling

**Justification:** Device retries and reconnect storms will send the same telematics payload more than once.

**Improvement:** Make telematics ingestion idempotent by device identifier, source timestamp, event hash, and receive window so projections do not double-count movement or violations.

**Acceptance evidence:** Duplicate-message tests proving a single stored effect, dead-letter evidence for conflicting duplicates, and release evidence showing stable trip totals after replay.

### 27. Unified fuel and charging ledger

**Justification:** Mixed fleets need one energy-consumption picture across diesel, petrol, and electric assets.

**Improvement:** Extend `fuel_transaction` handling to support charging sessions, energy units, charger source, charging loss, and cost normalization while preserving a single utilization and cost view.

**Acceptance evidence:** Ledger tests for liquid fuel and charging sessions, workbench filters by energy type, and release evidence showing comparable cost-per-kilometer analytics across vehicle classes.

### 28. Odometer and engine-hour service trigger calibration

**Justification:** Maintenance readiness becomes unreliable when service triggers drift from actual usage.

**Improvement:** Calibrate service triggers using telematics-derived odometer and engine-hour projections so `maintenance_schedule` alerts reflect true wear rather than stale manual updates.

**Acceptance evidence:** Calibration tests for corrected odometer drift, detail views showing trigger source, and release evidence proving that a service due date moved earlier after heavy usage telemetry.

### 29. Shift handoff log for dispatch continuity

**Justification:** Fleet control depends on clear handoff between dispatch teams, especially when vehicles remain active across shifts.

**Improvement:** Add structured shift handoff notes that capture blocked assets, open incidents, at-risk routes, pending reassignment decisions, and telematics gaps inside the workbench.

**Acceptance evidence:** Handoff entry and retrieval tests, audit history by shift owner, and release evidence showing continuity of unresolved issues across dispatcher changeover.

### 30. Dead-letter operations for telematics and fleet events

**Justification:** The manifest already includes retry and dead-letter evidence, but operators need domain-specific recovery workflows for movement and assignment data.

**Improvement:** Create dead-letter views for telematics, route, and assignment events with root-cause tags, replay eligibility, suppression controls, and operator notes.

**Acceptance evidence:** Retry tests for recoverable messages, quarantine behavior for poison messages, and release evidence showing successful replay of delayed telemetry without corrupting projections.

### 31. Route-plan versus actual variance analytics

**Justification:** The declared analytics surface should explain whether routes are performing as planned, not only report generic risk.

**Improvement:** Add route variance analytics for late departures, missed stops, unscheduled dwell, excess distance, geofence detours, and completion reliability by route type and dispatcher.

**Acceptance evidence:** Analytical tests for variance calculations, workbench drill-through to route detail, and release evidence showing a route class with persistent dwell overruns.

### 32. Vehicle downtime and replacement-cost forecasting

**Justification:** Predictive risk scoring should help operators decide when a vehicle is likely to go unavailable and what that will cost.

**Improvement:** Build a forecast using maintenance readiness, incident frequency, utilization intensity, and telematics stress indicators to estimate downtime probability and replacement-dispatch cost.

**Acceptance evidence:** Forecast evaluation on historical vehicle records, explainable factors in the workbench, and release evidence comparing predicted and realized downtime on sampled assets.

### 33. Counterfactual dispatch simulation

**Justification:** The manifest already declares counterfactual scenario simulation, and dispatch teams need it for disruptions before they commit changes.

**Improvement:** Add simulation scenarios for driver absence, depot closure, vehicle breakdown, fuel shortage, charger outage, and traffic-heavy route swaps, returning the projected effect on service coverage and utilization.

**Acceptance evidence:** Simulation test fixtures for each disruption type, side-by-side workbench comparison views, and release evidence proving the simulator does not mutate live assignments or route plans.

### 34. Multi-tenant depot and policy isolation

**Justification:** Multi-tenant policy isolation is declared, but fleet operations also require tenant-safe depots, routes, devices, and evidence handling.

**Improvement:** Enforce tenant scoping across vehicle pools, driver assignments, geofences, telematics devices, maintenance queues, and workbench filters so one tenant cannot infer another tenant's operations.

**Acceptance evidence:** Tenant isolation tests across APIs and read models, negative tests for cross-tenant access, and release evidence showing tenant-specific policy rules applied to the same operational scenario.

### 35. Override reason capture with audit proofs

**Justification:** Dispatch and maintenance supervisors will sometimes override policy, and those decisions need more than a generic update event.

**Improvement:** Require structured override reasons, supporting evidence attachments, approver identity, and cryptographic proof links whenever a blocked vehicle, driver, or route is manually forced through.

**Acceptance evidence:** Approval-path tests for required override fields, proof verification examples tied to `AuditEventSealed`, and release evidence showing an override trail from decision to audit proof.

### 36. Release evidence pack for fleet scenarios

**Justification:** `RELEASE_EVIDENCE.md` is listed in the manifest, so releases should show domain behavior, not only generic test output.

**Improvement:** Produce a release evidence pack that demonstrates dispatch readiness, telematics projection accuracy, route replanning, maintenance blocking, compliance rejection, fuel anomaly detection, and incident closure.

**Acceptance evidence:** Updated `RELEASE_EVIDENCE.md` content expectations captured in the backlog, reproducible scenario outputs for each named flow, and sign-off traces linking evidence to release candidates.

### 37. Configuration workbench for geofences, thresholds, and depot calendars

**Justification:** The manifest includes `configuration_workbench`, but fleet operations require domain-specific runtime controls rather than only generic parameters.

**Improvement:** Add configuration screens for geofence definitions, telematics staleness thresholds, fuel anomaly thresholds, rest-window rules, depot operating calendars, and charging readiness limits.

**Acceptance evidence:** Parameter validation tests, approval history for risky threshold changes, and release evidence showing a controlled threshold update taking effect without redeploying the PBC.

### 38. Policy-change impact preview

**Justification:** The PBC consumes `PolicyChanged`, and operators need to know what changes before a new policy starts blocking live work.

**Improvement:** When a policy update arrives, calculate which vehicles, assignments, routes, maintenance plans, or incidents would become non-compliant and present that preview before enforcement.

**Acceptance evidence:** Event-handler tests for `PolicyChanged`, workbench impact summaries grouped by object type, and release evidence showing a policy change that newly blocks a set of drivers from hazardous assignments.

### 39. Operational KPI-driven reprioritization

**Justification:** The PBC consumes `OperationalKpiChanged`, so fleet queues should react when service-level metrics move materially.

**Improvement:** Reprioritize dispatch, maintenance, and incident queues when KPIs indicate worsening on-time departure, rising downtime, telematics lag, or escalating safety exceptions.

**Acceptance evidence:** Event-consumption tests for KPI-driven queue shifts, workbench ordering changes with rationale, and release evidence showing queue reprioritization after a KPI breach.

### 40. Governed schema extension registry for fleet metadata

**Justification:** Fleet operators will need custom attributes such as depot group, body type, refrigeration status, or charger connector fit without breaking owned boundaries.

**Improvement:** Use `fleet_mobility_operations_schema_extension` to register governed custom fields for vehicles, assignments, routes, and incidents with validation, UI rendering rules, and event compatibility checks.

**Acceptance evidence:** Extension registration tests, projection compatibility checks, and release evidence proving a new fleet-specific attribute appears in the workbench without direct schema surgery.

### 41. Driver acknowledgement and exception handback

**Justification:** Assignment is incomplete until the driver has accepted or rejected the task and explained why.

**Improvement:** Extend assignment flow so drivers can acknowledge, decline, or request clarification on dispatches, with decline reasons feeding back into dispatch replanning and supervisor queues.

**Acceptance evidence:** Assignment lifecycle tests for accept and decline paths, workbench visibility into unacknowledged dispatches, and release evidence showing a declined job automatically reopened for reassignment.

### 42. Idle-time and standby utilization controls

**Justification:** Utilization is not just route occupancy; excessive standby time and depot idling burn cost and energy.

**Improvement:** Add analytics and exception thresholds for excessive idle time, standby time, and engine-on dwell by vehicle, depot, route family, and dispatcher action.

**Acceptance evidence:** Analytical tests for idle ratios, exception cards for excessive idle behavior, and release evidence showing utilization improvement after idle-policy enforcement.

### 43. Seasonal maintenance campaign planning

**Justification:** Fleet readiness often depends on seasonal service bursts such as tire changes, cooling checks, or rainy-season inspections.

**Improvement:** Add campaign planning to `maintenance_schedule` so operators can schedule grouped service windows, reserve workshop capacity, and forecast vehicle availability impact.

**Acceptance evidence:** Campaign scheduling tests, workshop capacity views tied to maintenance demand, and release evidence showing campaign-driven service planning without assignment collisions.

### 44. Depot arrival-to-dispatch turnaround metric

**Justification:** Operations teams need to know how quickly a vehicle returns to ready state after reaching a depot or workshop.

**Improvement:** Measure turnaround from geofence arrival to dispatch-ready clearance, breaking the delay into fueling or charging, inspection, maintenance, documentation, and assignment preparation stages.

**Acceptance evidence:** Metric derivation tests combining geofence events and readiness changes, workbench breakdown charts, and release evidence showing the slowest turnaround stage for a sampled depot.

### 45. Incident root-cause catalog and repeat-failure detection

**Justification:** Safety and roadside events become more valuable when repeat causes are clustered and fed back into policy or maintenance changes.

**Improvement:** Add a controlled catalog for incident root causes, corrective actions, and repeat-failure grouping across vehicles, depots, drivers, and route families.

**Acceptance evidence:** Incident classification tests, repeat-failure analytics in the safety workbench, and release evidence showing a recurring brake-related issue identified across multiple vehicles.

### 46. Offline telematics resilience and freshness warnings

**Justification:** Field connectivity is unreliable, and stale telemetry can silently degrade dispatch decisions if freshness is not surfaced.

**Improvement:** Track device heartbeat freshness, delayed upload windows, and last-known-position age so operators can distinguish truly stationary vehicles from disconnected devices.

**Acceptance evidence:** Freshness tests for connected and disconnected devices, workbench warnings for stale feeds, and release evidence showing dispatch blocked because a vehicle's telemetry was too old to trust.

### 47. Fuel-card versus odometer reconciliation workflow

**Justification:** Fuel controls improve when odometer capture is checked against telematics rather than trusted as entered.

**Improvement:** Add a reconciliation workflow that compares transaction odometer readings to telematics-derived odometer movement and routes suspicious mismatches into investigation.

**Acceptance evidence:** Reconciliation tests with valid and manipulated odometer inputs, investigation queue evidence in the workbench, and release evidence showing a flagged mismatch resolved with operator commentary.

### 48. Charger occupancy and queue projection

**Justification:** Charging readiness depends on charger congestion, not just battery state.

**Improvement:** Model charging-site occupancy, expected wait time, session duration, and route departure commitments so dispatch can choose between charging now, swapping assets, or delaying assignment.

**Acceptance evidence:** Queue-projection tests for overlapping charging sessions, energy workbench views showing charger contention, and release evidence demonstrating a route reassigned because charger wait time would miss departure.

### 49. Carbon and energy intensity reporting

**Justification:** Carbon and sustainability awareness is declared in the manifest, and fleet leaders need route and asset decisions tied to energy intensity.

**Improvement:** Add reporting for fuel burn, charging mix, idle emissions, and route-level energy intensity so dispatch and maintenance decisions can balance cost, readiness, and sustainability.

**Acceptance evidence:** Calculation tests for energy-intensity metrics, workbench views filtered by depot and vehicle class, and release evidence showing how route or charging choices changed the energy profile.

### 50. Release gate for operational proof, not only build proof

**Justification:** Fleet releases should be blocked when domain-critical scenarios cannot be demonstrated, even if the code compiles.

**Improvement:** Define a release gate that requires scenario evidence for vehicle readiness, assignment validation, telematics projection, route variance, maintenance blocking, compliance rejection, incident handling, fuel or charging reconciliation, and event emission integrity.

**Acceptance evidence:** A release checklist linked to `RELEASE_EVIDENCE.md`, automated verification summaries for each required scenario, and a documented fail condition when any fleet-operational proof is missing.
