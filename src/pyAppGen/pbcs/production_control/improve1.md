# Production Scheduling and Floor Control PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `production_control`. The items are specific to production scheduling and shop-floor control: work centers, routings, production orders, finite capacity, dispatch lists, operation sequencing, starts, pauses, completions, downtime, OEE, material readiness, material consumption, WIP, labor and machine time, quality gates, scrap/rework, completion proofs, exception cases, release handoffs, event reliability, UI workbenches, and agent-assisted production operations.

## Current Domain Evidence Used

- Domain purpose: production scheduling and shop-floor execution for work centers, routings, production orders, finite capacity, operation sequencing, starts, completions, downtime, OEE, and release handoffs.
- Owned boundary: work centers, production orders, routing steps, production schedules, dispatch lists, operation confirmations, downtime events, material consumption, WIP inventory, labor time booking, machine time booking, quality gate results, completion records, scrap/rework events, OEE snapshots, throughput forecasts, exception cases, policy screening, capacity allocation, completion proofs, audit entries, governed model evidence, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: work-center registration, order creation, routing, scheduling, operation start, material consumption, labor and machine time, downtime, quality gates, scrap/rework, operation confirmation, order completion, OEE snapshots, exception cases, capacity allocation, completion proofs, audit entries, AppGen-X inbox handling, workbench, schema/service/release evidence, rules, parameters, configuration, permissions, and boundary verification.
- Existing events and dependencies: emits `ProductionCompleted`, `AssetPlacedInService`, `DowntimeCaptured`, `MaterialConsumptionRecorded`, `LaborTimeBooked`, `MachineTimeBooked`, `QualityGateRecorded`, and `ScrapReworkCaptured`; consumes `PlannedOrderReleased` and `MaintenanceCompleted`; integrates with MRP, inventory, maintenance, quality, asset lifecycle, and audit only through declared APIs/projections.

## 50 Better-Than-World-Class Improvements

### 1. Work center readiness gate

**Justification:** Production schedules are only feasible when work centers have valid capacity, calendar, shift, equipment, status, and maintenance context.

**Improvement:** Add readiness checks for site, calendar, shift, capacity, efficiency, status, asset projection, allowed operations, operator requirements, maintenance projection freshness, and OEE target. Block scheduling to incomplete or blocked centers.

### 2. Work center capability model

**Justification:** Work centers differ by process capability, tooling, setup, certifications, automation, batch size, and quality gates.

**Improvement:** Model capability, tooling, setup family, machine class, labor skill, automation mode, min/max batch, quality gate, and compatible routing steps. Dispatch should cite capability matching.

### 3. Routing step lifecycle governance

**Justification:** Routing steps define sequence, standard time, setup, quality gates, and work center eligibility; errors create bad schedules and confirmations.

**Improvement:** Add routing step states, sequence constraints, setup/run time, overlap/queue time, alternate work centers, yield, quality gate requirements, and effective dates. Orders should reference routing version snapshots.

### 4. Production order readiness gate

**Justification:** Production orders from planned-order projections require material, routing, capacity, quality, and policy readiness before release to the floor.

**Improvement:** Validate planned-order projection, item, quantity, due date, BOM/routing version, material readiness projection, capacity, quality holds, work center availability, and release policy before order creation.

### 5. Production order lifecycle state machine

**Justification:** Orders need controlled transitions across created, scheduled, dispatched, started, paused, split, merged, completed, closed, and cancelled.

**Improvement:** Implement state transitions with actor, timestamp, source event, reason, idempotency key, allowed next states, and downstream event effects. Invalid transitions should fail with clear policy explanations.

### 6. Finite capacity scheduling engine

**Justification:** Infinite schedules produce infeasible dispatch lists and missed commitments.

**Improvement:** Add finite scheduling by site, work center, shift, capacity bucket, setup family, priority, due date, material readiness, and maintenance projection. Store schedule assumptions and infeasible-order reasons.

### 7. Schedule adherence monitoring

**Justification:** Production control needs to detect when actual starts, completions, downtime, or queues diverge from the plan.

**Improvement:** Compare scheduled versus actual start/end, sequence, quantity, and work center. Surface adherence loss by cause, order, operation, shift, and supervisor.

### 8. Dispatch list optimization

**Justification:** Dispatch order affects setup time, throughput, quality, WIP, and due-date performance.

**Improvement:** Optimize dispatch lists using priority, due date, setup family, material readiness, work center capability, quality gate readiness, labor availability, and downstream constraints. Show tradeoffs and rejected alternatives.

### 9. Operation sequencing controls

**Justification:** Incorrect sequence can create quality failures, rework, WIP confusion, or impossible confirmations.

**Improvement:** Enforce predecessor/successor dependencies, overlap rules, parallel operations, queue time, mandatory inspections, and rework loops. Operation confirmations should validate sequence eligibility.

### 10. Production start validation

**Justification:** Starting production without material, labor, machine availability, or quality readiness causes exceptions.

**Improvement:** Validate material readiness, WIP status, work center state, operator permission, maintenance projection, quality gate prerequisites, and policy screening before starting an operation.

### 11. Pause, resume, split, and merge governance

**Justification:** Shop-floor disruptions require flexible control while preserving traceability.

**Improvement:** Model pause/resume reasons, partial quantities, split order lineage, merge eligibility, WIP movement, affected schedule, and recalculation impact. Require approval for high-risk splits and merges.

### 12. Operation confirmation trace

**Justification:** Confirmations drive inventory, quality, cost, OEE, and downstream completion events.

**Improvement:** Store confirmation evidence for good quantity, scrap, rework, operator, work center, start/end time, machine hours, labor hours, material consumed, quality gate result, and source device/instruction.

### 13. Material readiness projection handling

**Justification:** Production Control does not own inventory but must understand whether material is ready to run.

**Improvement:** Project material readiness from inventory/MRP events with item, quantity, lot, reservation, quality hold, freshness, and confidence. Surface stale or missing material projections before dispatch.

### 14. Material consumption governance

**Justification:** Consumption records affect inventory, yield, cost, and traceability.

**Improvement:** Record consumed material by order, operation, component, quantity, lot/serial where available, scrap factor, issue method, variance, and operator. Emit `MaterialConsumptionRecorded` with idempotent evidence.

### 15. WIP inventory trace

**Justification:** WIP state must be visible between operations without becoming the inventory system of record.

**Improvement:** Track WIP quantity, operation, queue, status, hold reason, location, split/merge lineage, and projection handoff. Distinguish production-owned WIP trace from inventory-owned balances.

### 16. Labor time booking

**Justification:** Labor booking supports cost, productivity, OEE, and time/labor handoff evidence.

**Improvement:** Record labor time by operation, employee/role projection, start/end, direct/indirect, setup/run/rework, approval, and variance. Emit `LaborTimeBooked` with boundary-safe projection data.

### 17. Machine time booking

**Justification:** Machine time determines utilization, maintenance context, OEE, and costing.

**Improvement:** Record machine time by work center/asset projection, setup/run/idle, cycle count, speed, source device, maintenance state, and variance. Emit `MachineTimeBooked` with trace evidence.

### 18. Downtime taxonomy and capture

**Justification:** Downtime needs precise classification to improve OEE and root-cause analysis.

**Improvement:** Define downtime reasons for planned maintenance, unplanned failure, material shortage, quality hold, setup delay, labor shortage, changeover, external outage, and microstop. Capture start/end, asset projection, severity, and evidence.

### 19. Downtime OEE impact model

**Justification:** Downtime affects availability, performance, and quality differently depending on reason and timing.

**Improvement:** Calculate downtime impact on OEE buckets, schedule adherence, throughput, and capacity. Emit `DowntimeCaptured` with work center, duration, reason, and OEE effect.

### 20. Maintenance projection integration

**Justification:** Maintenance completion can release capacity or explain downtime, but maintenance owns its records.

**Improvement:** Project `MaintenanceCompleted` events with asset/work-center, completion time, restored capability, constraints, and confidence. Scheduling and downtime analysis should cite projection freshness.

### 21. Quality gate execution

**Justification:** Quality gates determine whether production can proceed, rework, scrap, or complete.

**Improvement:** Record quality gate results with operation, inspection criteria, sample size, pass/fail, defect codes, hold state, inspector, and quality projection references. Emit `QualityGateRecorded`.

### 22. Scrap and rework lifecycle

**Justification:** Scrap and rework affect yield, cost, schedule, quality, and material planning.

**Improvement:** Model scrap/rework events with reason, quantity, operation, material/component, disposition, rework route, approval, and cost impact. Emit `ScrapReworkCaptured` and link to OEE/yield metrics.

### 23. Production completion controls

**Justification:** Completion closes execution and triggers inventory, quality, asset, and audit consumers.

**Improvement:** Validate all required operations, confirmations, quality gates, material consumption, WIP, scrap/rework, and exceptions before completion. Emit `ProductionCompleted` with proof hash.

### 24. Asset placed-in-service handoff

**Justification:** Some production work commissions assets that asset lifecycle systems must own after completion.

**Improvement:** Generate asset commissioning handoff with production order, serial/asset projection, completion proof, quality status, acceptance evidence, and emitted `AssetPlacedInService` without writing asset tables.

### 25. OEE snapshot governance

**Justification:** OEE metrics can be misleading without clear denominator, time window, and source events.

**Improvement:** Store OEE snapshots with availability, performance, quality, planned time, unplanned downtime, ideal cycle, good/scrap quantities, source events, and calculation version.

### 26. Throughput forecast governance

**Justification:** Supervisors need forecasts for output, late orders, bottlenecks, and staffing decisions.

**Improvement:** Forecast throughput by work center, shift, routing, product family, downtime risk, material readiness, and quality risk. Include confidence, drift, and intervention recommendations.

### 27. Production exception taxonomy

**Justification:** Generic exceptions hide root causes and make floor response slower.

**Improvement:** Define exceptions for missing material, capacity overload, work center blocked, routing mismatch, quality failure, downtime, labor shortage, machine unavailable, WIP mismatch, and late order. Each should define owner, SLA, severity, and recovery action.

### 28. Exception recommendation engine

**Justification:** Supervisors need safe next actions for production disruptions.

**Improvement:** Recommend reschedule, alternate work center, split order, expedite material, wait for maintenance, rework route, quality hold, or cancel operation. Show risk, impact, required permission, and event effects.

### 29. Capacity allocation mechanism

**Justification:** Scarce work-center capacity must be allocated across orders transparently.

**Improvement:** Allocate capacity using due date, priority, setup efficiency, customer/service class, material readiness, quality risk, and fairness. Simulate allocation choices before schedule release.

### 30. Counterfactual dispatch simulation

**Justification:** Dispatch changes can improve one order while harming others.

**Improvement:** Simulate dispatch priority, capacity threshold, downtime assumptions, routing alternates, and overtime scenarios. Show schedule adherence, WIP, throughput, OEE, and late-order impact.

### 31. Carbon-aware production scheduling

**Justification:** Production schedules can account for energy intensity, shift timing, and equipment usage.

**Improvement:** Add carbon-aware schedule windows for non-urgent orders, energy-intensive work centers, and batch runs while preserving due dates and quality constraints. Show service/cost/carbon tradeoffs.

### 32. Completion proof generation

**Justification:** Downstream systems may need proof of production completion without full shop-floor details.

**Improvement:** Generate redacted completion proofs for order, quantity, operations, quality gates, material consumption, timestamps, and hash chain. Provide verification API and proof expiry.

### 33. Immutable production audit trail

**Justification:** Production execution affects inventory, quality, cost, assets, and compliance.

**Improvement:** Hash-chain work center changes, routing, scheduling, dispatch, starts, pauses, confirmations, downtime, material consumption, quality gates, scrap/rework, completion, agent previews, and event handling.

### 34. Policy screening for production actions

**Justification:** Shop-floor actions must respect site, work center, quality, safety, material, operator, and completion policies.

**Improvement:** Screen work center updates, order creation, scheduling, start, consumption, time booking, downtime, quality gates, scrap/rework, completion, and proof generation. Store policy version and decision evidence.

### 35. Shop-floor event reliability cockpit

**Justification:** Production depends on planned-order and maintenance events and emits multiple downstream execution events.

**Improvement:** Add inbox/outbox/dead-letter views for idempotency, duplicates, retries, handler version, payload lineage, projection freshness, replay eligibility, and downstream event effects.

### 36. Boundary proof for production ownership

**Justification:** Production Control must integrate with MRP, inventory, maintenance, quality, asset lifecycle, identity, and audit without shared tables.

**Improvement:** Add static/runtime checks proving commands touch only production-owned tables plus AppGen-X runtime tables. Include failing fixtures for direct MRP, inventory, maintenance, quality, asset, finance, and audit table access.

### 37. Production workbench coverage

**Justification:** Schedulers, supervisors, operators, quality users, maintenance coordinators, and auditors need a complete UI.

**Improvement:** Expand UI into work center console, routing editor, order board, finite schedule, dispatch list, operation control, material/WIP ledger, labor/machine booking, downtime console, quality gates, scrap/rework, completion proof, OEE, exceptions, rules, parameters, configuration, events, and agent panels.

### 38. Agent-safe shop-floor instruction intake

**Justification:** The production_control chatbot should parse work instructions, dispatch notes, downtime notes, quality outcomes, and completion evidence without unsafe writes.

**Improvement:** Add intake skills that extract candidate production facts, map them to owned tables, validate rules/permissions/projections, reject foreign-table mutations, and produce side-effect-free previews with confidence, risks, approvals, and expected AppGen-X events.

### 39. Agent-safe execution planning

**Justification:** AI suggestions on the floor can change production commitments, quality, and safety outcomes.

**Improvement:** Require agent plans for scheduling, dispatch, start, material consumption, time booking, downtime, quality, scrap/rework, completion, and exceptions to list command, permission, owned tables, idempotency key, emitted event, affected order, rollback limits, and human approval.

### 40. Semantic shop-floor parsing

**Justification:** Operators and supervisors often record execution facts in unstructured notes.

**Improvement:** Parse instructions and notes into candidate downtime reasons, scrap codes, quality outcomes, material variances, schedule changes, and exception actions with confidence and reviewer approval.

### 41. Production anomaly detection

**Justification:** Abnormal downtime, scrap, cycle time, OEE, or confirmation patterns can indicate equipment, quality, or data problems.

**Improvement:** Detect anomalies by work center, routing step, product, shift, operator role, material, quality gate, and event stream. Route findings to review with explanations.

### 42. Stochastic production exposure model

**Justification:** Production risk spans downtime, yield, schedule, quality, material, capacity, and completion exposure.

**Improvement:** Model exposure distributions by order, work center, product, shift, operation, and site. Provide mitigation actions and confidence intervals.

### 43. Production MLOps governance

**Justification:** Downtime, yield, scheduling, OEE, and exception models influence operations and labor.

**Improvement:** Add model registry, feature lineage, training windows, approval status, drift monitoring, explainability, fairness/coverage checks, rollback, and release evidence for production models.

### 44. Decentralized work center and asset identity

**Justification:** High-control production needs trusted identities for work centers, equipment, devices, and commissioned assets.

**Improvement:** Add identity credentials, verification status, expiry, authority, proof references, and revocation for work centers/assets. Use identity confidence in scheduling and completion proofs.

### 45. Shop-floor resilience drills

**Justification:** Production routes, device integrations, maintenance projections, and event delivery can fail during active execution.

**Improvement:** Add drills for planned-order duplicate, maintenance projection delay, dispatch route failure, device outage, downtime event replay, completion outbox failure, and dead-letter recovery. Store drill evidence.

### 46. Crypto-agile production authorization

**Justification:** Completion proofs, quality gates, and audit trails need durable cryptographic evidence.

**Improvement:** Add crypto epoch metadata, signed proof references, key rotation evidence, policy version, and migration readiness for future algorithms without tying production logic to one primitive.

### 47. Continuous production control testing

**Justification:** Controls should run continuously across scheduling, dispatch, execution, downtime, quality, completion, and events.

**Improvement:** Add assertions for scheduling blocked work centers, start without material, confirmation before predecessor, completion without quality gate, unexplained downtime, WIP mismatch, direct foreign-table access, dead-letter aging, and agent-preview bypass.

### 48. Production close and shift handover

**Justification:** Shift changes and production close need unresolved work, exceptions, WIP, downtime, and quality context.

**Improvement:** Add close/handover packets with active orders, paused operations, open exceptions, WIP state, downtime, quality holds, expected completions, event failures, and supervisor signoff.

### 49. Production Control readiness score

**Justification:** Users need an evidence-backed view of whether Production Control is ready for shop-floor execution.

**Improvement:** Compute readiness from work center setup, routing coverage, planned-order projections, material readiness, finite scheduling, dispatch controls, operation confirmation, downtime/OEE, quality gates, UI coverage, event reliability, boundary proof, controls, model governance, and agent safety.

### 50. End-to-end production execution proof

**Justification:** A complete Production Control PBC must prove it can execute the full lifecycle from planned order to completion event.

**Improvement:** Add an executable proof scenario covering planned-order projection, work center readiness, routing, finite schedule, dispatch, start, material consumption, labor/machine booking, downtime if applicable, quality gate, scrap/rework, completion, emitted events, OEE snapshot, UI evidence, controls, and agent explanation.
