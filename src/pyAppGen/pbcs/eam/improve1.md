# Enterprise Asset Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `eam`. The items are specific to enterprise asset management: equipment registry, asset hierarchy, locations, criticality, warranties, preventive and predictive maintenance, condition monitoring, meters, work requests, work orders, scheduling, mobile execution, safety permits, lockout/isolation, spare usage, labor assignment, downtime, failure analysis, vendor service, reliability analytics, rules, parameters, configuration, AppGen-X event reliability, UI workbenches, and agent-assisted maintenance operations.

## Current Domain Evidence Used

- Domain purpose: `eam` owns maintainable equipment, asset hierarchy, maintenance strategies, preventive plans, condition monitoring, work requests, work orders, scheduling, safety controls, spare usage, labor execution, downtime, reliability analytics, compliance evidence, warranties, service-vendor performance, rules, parameters, configuration, and workbench UI fragments.
- Owned boundary: equipment, maintenance plans, work orders, spare part usage, condition readings, meter readings, failure events, maintenance schedules, service vendor events, safety permits, maintenance rules, maintenance parameters, maintenance configuration, outbox, inbox, and dead-letter evidence.
- Existing command/query surface: runtime configuration, parameter/rule/schema-extension registration, equipment registration, maintenance plan creation, condition and meter readings, safety permits, work orders, scheduling, spare issue, work-order completion, event inbox, workbench, schema/service/release evidence, permissions, UI binding, and boundary verification.
- Existing events and dependencies: emits `EquipmentRegistered`, `MaintenancePlanReleased`, `ConditionReadingRecorded`, `MeterReadingRecorded`, `SafetyPermitApproved`, `WorkOrderCreated`, `WorkOrderScheduled`, `SparePartUsed`, `MaintenanceCompleted`, and `VendorPerformanceUpdated`; consumes `DowntimeCaptured`, `NonConformanceRaised`, `InventoryReservationConfirmed`, `PurchaseOrderAcknowledged`, and `AssetLifecycleUpdated`; composes with production, quality, inventory, procurement, asset lifecycle, audit, and analytics only through declared APIs/events/projections.

## 50 Better-Than-World-Class Improvements

### 1. Equipment readiness gate

**Justification:** Maintenance work is unsafe and unreliable when equipment identity, hierarchy, location, criticality, warranty, meter, safety, and maintainability data are incomplete.

**Improvement:** Add an equipment readiness gate that validates equipment class, site, location, parent/child hierarchy, status, criticality, maintainability state, meter setup, warranty references, safety requirements, and lifecycle projection freshness before equipment can be released for maintenance planning.

### 2. Asset hierarchy integrity model

**Justification:** Incorrect parent-child relationships create bad downtime rollups, spare applicability errors, and incomplete safety isolation.

**Improvement:** Enforce hierarchy invariants for acyclic parentage, effective dates, site compatibility, location inheritance, criticality rollup, meter inheritance, failure aggregation, and isolation impact mapping.

### 3. Location and maintainability state tracking

**Justification:** Equipment moves, temporary installations, decommissioning, and unavailable states change what work can be planned or executed.

**Improvement:** Track location history, installation state, operating state, maintainability state, mobility, access restrictions, effective dates, and source event lineage, then expose as-of asset position in the workbench.

### 4. Criticality and consequence model

**Justification:** Work priority should reflect safety, environmental, production, quality, service, and cost consequences rather than static labels.

**Improvement:** Add criticality scoring with weighted consequence dimensions, redundancy, failure detectability, downtime cost, safety exposure, regulatory class, customer impact, and explainable priority derivation.

### 5. Warranty and recovery governance

**Justification:** Warranty leakage happens when maintenance work, failures, vendor events, and spare usage are not checked against coverage.

**Improvement:** Add warranty eligibility checks, claim windows, covered failure modes, excluded conditions, required evidence, vendor notification, recovery amount estimate, claim status, and closure evidence.

### 6. Maintenance strategy portfolio

**Justification:** Assets need a mix of run-to-failure, preventive, predictive, condition-based, statutory, calibration, warranty, and shutdown strategies.

**Improvement:** Model strategy portfolios per equipment class and asset with trigger type, risk rationale, expected benefit, cost, compliance basis, override rules, and review cadence.

### 7. Preventive maintenance plan readiness

**Justification:** Preventive plans fail when intervals, task lists, spares, labor, permits, and release rules are incomplete.

**Improvement:** Validate interval, calendar, site, work type, task steps, labor skills, spare requirements, safety permit class, predecessor plans, downtime expectation, and release approvals before `MaintenancePlanReleased`.

### 8. Meter-based maintenance triggers

**Justification:** Usage-driven assets require maintenance based on runtime, cycles, mileage, throughput, or condition counters.

**Improvement:** Add meter trigger definitions with unit, rollover handling, reading confidence, due-at threshold, forecasted due date, stale-reading policy, and generated work-order proposal evidence.

### 9. Predictive maintenance signal catalog

**Justification:** Predictive maintenance requires controlled signals, not ad hoc sensor or condition readings.

**Improvement:** Register signal definitions for vibration, temperature, pressure, oil analysis, electrical load, acoustic data, process drift, and operator observations with units, thresholds, sampling cadence, and asset applicability.

### 10. Condition reading validation

**Justification:** Bad condition readings can trigger unnecessary maintenance or miss imminent failures.

**Improvement:** Validate reading source, timestamp, unit, device identity, equipment state, outlier range, duplicate readings, stale readings, manual override reason, and confidence score before risk scoring.

### 11. Work request intake triage

**Justification:** Maintenance demand often starts as vague operator reports, alarms, quality findings, or downtime records.

**Improvement:** Add intake triage for symptom, asset, location, severity, safety concern, production impact, evidence attachments, reporter, duplicate detection, recommended work type, and conversion to planned work order.

### 12. Work order lifecycle state machine

**Justification:** Work orders need controlled transitions from request through planning, approval, scheduling, execution, completion, technical closure, and financial closure.

**Improvement:** Implement state transitions with idempotency key, actor, timestamp, reason, required fields, allowed next states, emitted event expectations, and policy explanations for invalid transitions.

### 13. Work planning package

**Justification:** Execution quality depends on having job steps, skills, spares, tools, permits, procedures, drawings, and acceptance criteria ready before scheduling.

**Improvement:** Add work package readiness with task list, craft requirements, estimated duration, spare reservations, tool requirements, safety permits, isolation plan, documents, quality checks, and supervisor approval.

### 14. Maintenance scheduling optimizer

**Justification:** Maintenance schedules must balance risk, production availability, labor, spares, permits, vendor windows, and downtime constraints.

**Improvement:** Add scheduling optimization that scores candidate windows by failure risk, production impact, craft capacity, spare availability, permit readiness, vendor SLA, planned downtime, and carbon-aware preferences.

### 15. Dispatch and mobile execution controls

**Justification:** Technicians need a controlled field workflow that works under intermittent connectivity and preserves audit evidence.

**Improvement:** Add mobile execution states for accepted, en route, on site, started, paused, blocked, completed, and synced with offline queue, evidence capture, job-step checklist, time booking, spares, photos, signatures, and retry proof.

### 16. Skill-based labor assignment

**Justification:** Work quality and safety depend on matching craft, certification, location access, shift, fatigue exposure, and availability.

**Improvement:** Add labor assignment checks for skill, certification expiry, crew size, shift schedule, overtime exposure, site access, safety qualification, conflict, travel time, and assignment rationale.

### 17. Tool and equipment requirement matching

**Justification:** Jobs fail or are delayed when specialized tools, test equipment, lifts, or calibrated devices are unavailable.

**Improvement:** Add job-tool requirements, availability windows, calibration readiness, reservation, checkout/checkin, substitute tool rules, and blocked-work alerts for missing tools.

### 18. Safety permit readiness gate

**Justification:** Hazardous maintenance requires permits, lockout, isolation, gas tests, confined-space controls, hot-work controls, and risk acceptance.

**Improvement:** Validate permit type, hazards, controls, isolations, approvers, effective window, affected equipment hierarchy, required tests, worker acknowledgements, and emergency rollback before `SafetyPermitApproved`.

### 19. Lockout and isolation map

**Justification:** Safe maintenance requires knowing every energy source and adjacent asset affected by isolation.

**Improvement:** Model isolation points, energy types, lock ownership, verification steps, affected equipment tree, conflict with running production, permit links, and release sequence.

### 20. Spare reservation and issue governance

**Justification:** Spare shortages delay critical work, while uncontrolled issues distort inventory and cost.

**Improvement:** Add reservation projection checks, substitute rules, kitting, issue approval, consumption reason, serial/lot capture, return handling, cost attribution, and `SparePartUsed` event evidence.

### 21. Repairable spare lifecycle

**Justification:** Rotables and repairables require removal, inspection, refurbishment, quarantine, warranty, and return-to-stock tracking.

**Improvement:** Add repairable spare workflows with removed-from-asset, condition, repair vendor, warranty claim, refurbishment result, certification, quarantine, installed-on-asset, and cost history.

### 22. Downtime and production impact linkage

**Justification:** Maintenance decisions need reliable linkage between failures, downtime, work orders, and production impact.

**Improvement:** Project `DowntimeCaptured` events into equipment downtime records with reason, duration, production impact, planned/unplanned flag, linked work order, restoration evidence, and MTTR calculation inputs.

### 23. Failure event classification

**Justification:** Reliability improvement depends on consistent failure modes, mechanisms, causes, effects, and detection methods.

**Improvement:** Add failure coding with equipment class taxonomy, failure mode, mechanism, cause, effect, detection method, severity, recurrence group, evidence, and required root-cause trigger.

### 24. Root-cause and corrective action workflow

**Justification:** Recurrent failures persist when root cause and corrective actions are disconnected from work execution.

**Improvement:** Add RCA methods, hypothesis evidence, cause validation, corrective actions, owner, due date, effectiveness check, recurrence monitoring, and linkage to failure events and work orders.

### 25. Reliability analytics dashboard

**Justification:** Maintenance leaders need actionable reliability metrics, not raw work-order lists.

**Improvement:** Add MTBF, MTTR, availability, backlog age, schedule compliance, wrench time, emergency work ratio, repeat failure, PM compliance, overdue statutory work, and cost-risk drilldowns by asset, class, site, and period.

### 26. Failure forecasting

**Justification:** World-class asset management shifts from reactive work to risk-based intervention.

**Improvement:** Forecast failure probability, downtime exposure, safety exposure, spare demand, and maintenance due dates using condition readings, meter trends, failure history, operating context, and plan compliance.

### 27. Counterfactual strategy simulation

**Justification:** Planners need to compare maintenance intervals and condition triggers before changing a strategy.

**Improvement:** Simulate alternative intervals, thresholds, shutdown windows, labor plans, spare policies, and vendor strategies with predicted failures avoided, cost, downtime, safety risk, and backlog impact.

### 28. Maintenance backlog risk scoring

**Justification:** Backlog should be prioritized by risk and consequence, not just age or manually assigned priority.

**Improvement:** Score backlog items by criticality, failure forecast, safety exposure, compliance deadline, production impact, spare availability, vendor lead time, and schedule opportunity.

### 29. Statutory and compliance maintenance proof

**Justification:** Regulated assets require evidence that inspections, tests, permits, and maintenance were completed on time by qualified people.

**Improvement:** Generate compliance proof packets with plan, work order, permit, technician qualifications, calibration/tool evidence, readings, completion notes, timestamps, signatures, and immutable event references.

### 30. Service vendor performance management

**Justification:** External maintenance vendors influence uptime, cost, warranty, safety, and compliance.

**Improvement:** Track vendor events, SLA commitments, response time, first-time fix, rework, safety incidents, warranty recovery, cost variance, documentation quality, and performance score updates.

### 31. Vendor dispatch and acknowledgement workflow

**Justification:** Contractor work needs auditable assignment, site access, permit acknowledgement, arrival, execution, and completion evidence.

**Improvement:** Add vendor dispatch states, acknowledgement, expected arrival, credential checks, permit requirements, work evidence, completion review, dispute capture, and `VendorPerformanceUpdated` event output.

### 32. Asset lifecycle handoff integration

**Justification:** Commissioning, transfer, refurbishment, and retirement affect maintenance plans, warranties, meters, and spares.

**Improvement:** Consume `AssetLifecycleUpdated` into package-local projections that update maintainability state, plan eligibility, hierarchy changes, warranty state, and open-work exceptions without shared-table access.

### 33. Quality and nonconformance integration

**Justification:** Quality findings can require equipment inspection, calibration, repair, or production hold support.

**Improvement:** Project `NonConformanceRaised` into maintenance review queues with affected equipment, suspected cause, quality severity, required inspection, linked work order, and closure feedback.

### 34. Inventory and procurement projection controls

**Justification:** Spare reservations and vendor orders must rely on declared projections instead of direct access to inventory or procurement tables.

**Improvement:** Validate `InventoryReservationConfirmed` and `PurchaseOrderAcknowledged` projections for freshness, quantity, part identity, vendor, due date, and idempotency before scheduling or issuing spares.

### 35. AppGen-X inbox reliability

**Justification:** Consumed downtime, quality, inventory, procurement, and lifecycle events materially change maintenance priority and execution readiness.

**Improvement:** Add inbox schema validation, idempotency, retry evidence, unsupported-event rejection, dead-letter promotion, projection rebuild, stale dependency alerts, and workbench replay/quarantine controls.

### 36. AppGen-X outbox delivery assurance

**Justification:** Equipment, plan, reading, permit, work-order, spare, completion, and vendor events must be reliably visible to composed applications.

**Improvement:** Add outbox state, ordering group, payload hash, retry count, next attempt, delivery proof, dead-letter linkage, and replay controls for every emitted EAM event.

### 37. Owned-boundary proof

**Justification:** EAM must compose through APIs/events/projections and never share source tables with production, quality, inventory, procurement, asset lifecycle, audit, or analytics.

**Improvement:** Add release evidence that scans schema descriptors, services, routes, agent plans, and generated DSL for foreign table reads or writes, failing the audit on violations.

### 38. Maintenance workbench coverage

**Justification:** The UI must surface the complete EAM domain, not just equipment and work-order CRUD.

**Improvement:** Expand workbench navigation for equipment registry, hierarchy map, plans, condition monitoring, meters, requests, work orders, scheduler, mobile execution, spares, safety, reliability, vendors, rules, parameters, configuration, events, and release evidence.

### 39. Technician cockpit

**Justification:** Technicians need a focused execution surface that reduces paperwork while preserving safety and evidence.

**Improvement:** Add a cockpit with assigned jobs, route/travel context, permit status, job steps, tools, spares, readings, photos, notes, time capture, blockers, completion checklist, and offline synchronization status.

### 40. Planner and scheduler cockpit

**Justification:** Planners need visibility into readiness blockers before work reaches the field.

**Improvement:** Add queues for unplanned requests, incomplete packages, missing spares, missing tools, permit blockers, labor conflicts, vendor dependencies, overdue PMs, risk-ranked backlog, and optimized schedule proposals.

### 41. Agent-safe maintenance planning

**Justification:** AI assistance can save maintenance time only if it cannot bypass safety, permits, inventory, or approval controls.

**Improvement:** Require the EAM agent to produce side-effect-free plans naming command, permission, owned tables, idempotency key, expected event, safety gates, rollback limits, and human confirmation for equipment, plan, work order, permit, spare, reading, and completion actions.

### 42. Maintenance document and instruction intake

**Justification:** Maintenance facts arrive through manuals, technician notes, inspection sheets, vendor reports, permits, and failure photos.

**Improvement:** Extract candidate facts for equipment, plans, readings, work orders, permits, spares, and vendor events with confidence, evidence links, missing fields, rule checks, and governed mutation previews.

### 43. Semantic maintenance instruction parsing

**Justification:** Work request and task text must become structured work steps, hazards, spares, tools, skills, and completion criteria.

**Improvement:** Parse instructions into proposed task lists, safety controls, spare requirements, labor skills, tools, readings, acceptance criteria, and quality checks with planner review.

### 44. Maintenance anomaly detection

**Justification:** Abnormal work patterns can indicate asset degradation, poor planning, missing spares, or unsafe execution.

**Improvement:** Detect anomalies in readings, meter jumps, repeat failures, emergency work, spare usage, labor time, vendor response, safety permits, completion notes, and event replay behavior with explanations.

### 45. Governed reliability model evidence

**Justification:** Predictive maintenance models affect safety, downtime, vendor spend, spare stock, and technician workload.

**Improvement:** Track model purpose, training window, asset coverage, feature lineage, validation metrics, drift, false-negative exposure, approval status, rollback, and explainability evidence.

### 46. Decentralized equipment identity

**Justification:** High-control asset networks need trustworthy equipment, meter, tool, and vendor identities.

**Improvement:** Add credential references, issuer, verification status, expiry, revocation, proof hash, and trust level for equipment identity, meters, calibrated tools, vendor credentials, and compliance packets.

### 47. Maintenance resilience drills

**Justification:** Maintenance operations must remain safe when mobile devices, projections, outbox delivery, vendor channels, or scheduler services fail.

**Improvement:** Add drills for duplicate lifecycle events, offline mobile completion, spare projection delay, permit approval outage, outbox dead letter, vendor acknowledgement failure, and hierarchy rebuild.

### 48. Continuous maintenance control testing

**Justification:** Controls should be proven continuously across planning, scheduling, execution, safety, spares, vendors, and events.

**Improvement:** Add assertions for work without permit, completion without required reading, spare issue without reservation, overdue statutory PM, expired certification, stale projection, foreign-table access, dead-letter aging, and agent-preview bypass.

### 49. EAM readiness score

**Justification:** Users need an evidence-backed view of whether `eam` is ready for controlled asset operations.

**Improvement:** Compute readiness from equipment completeness, hierarchy integrity, plan coverage, condition/meter setup, work-order lifecycle, safety permits, spares, labor, vendor controls, reliability analytics, event reliability, UI coverage, model governance, and agent safety.

### 50. End-to-end maintenance execution proof

**Justification:** A complete EAM PBC must prove it can run the full lifecycle from equipment registration to completed maintenance event.

**Improvement:** Add an executable proof scenario covering equipment registration, hierarchy, maintenance plan release, condition/meter trigger, work request, work package, permit, spare reservation/issue, labor assignment, schedule, mobile execution, completion, reliability metrics, emitted events, UI evidence, boundary proof, controls, and agent explanation.
