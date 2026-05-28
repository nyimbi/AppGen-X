# Warehouse Management Core PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `wms_core`. The items are specific to warehouse execution: warehouse topology, docks, inbound receiving, putaway, replenishment, picking, wave planning, packing, cartonization, staging, shipping, cross-docking, cycle counting, labor, edge devices, exceptions, traceability, controls, rules, parameters, configuration, UI workbenches, and agent-assisted warehouse operations.

## Current Domain Evidence Used

- Domain purpose: warehouse execution for receiving, putaway, replenishment, picking, packing, staging, shipping, cross-docking, cycle counting, labor assignment, edge-device orchestration, warehouse exception handling, and package-local AppGen-X event handling.
- Owned boundary: warehouse masters, zones, calendars, warehouse identity, bin locations, bin attributes, bin capacity snapshots, inbound receipts and lines, dock doors, dock appointments, putaway tasks and confirmations, replenishment tasks and triggers, pick waves, pick tasks, pick exceptions, pack tasks, cartons, label evidence, pack stations, staging lanes, shipment confirmations and labels, cross-dock flows, cycle counts, warehouse exceptions, labor tasks and assignments, edge-device commands/events/replay, policy screenings, traceability events, shipment proofs, federation projections, carbon waves, pick-path optimization, labor allocation, anomaly signals, risk models, seed data, schema extensions, control assertions, governed models, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: warehouse registration, bin registration, inbound receiving, putaway, pick-wave release, pick execution, pack tasks, shipments, AppGen-X inbox handling, workbench, rules, parameters, schema extensions, configuration, boundary checks, and release evidence.
- Existing events and dependencies: emits `WarehouseRegistered`, `BinRegistered`, `GoodsReceiptPosted`, `PutawayTaskCreated`, `PutawayConfirmed`, `PickWaveReleased`, `Picked`, `PackTaskCreated`, `Packed`, and `OrderShipped`; consumes inventory, inbound arrival, quality release, carrier booking, and access-policy events through declared APIs/projections only.

## 50 Better-Than-World-Class Improvements

### 1. Warehouse topology digital twin

**Justification:** WMS execution depends on the real physical layout of warehouses, zones, aisles, bays, levels, bins, docks, conveyors, pack stations, staging lanes, and restricted areas.

**Improvement:** Build a graph-backed topology model that records coordinates, adjacency, travel cost, congestion sensitivity, temperature/hazard constraints, labor access, automation equipment, and temporal closures. Putaway, picking, replenishment, cross-dock, and staging decisions should cite the topology version used.

### 2. Warehouse master readiness gate

**Justification:** Incomplete warehouse setup causes unsafe receiving, invalid bin assignments, blocked wave release, and untraceable shipping.

**Improvement:** Add readiness checks for calendar, timezone, zones, dock doors, bin statuses, pack stations, label formats, edge-device modes, permissions, seed data, rules, parameters, and AppGen-X event configuration. Block operational commands when mandatory setup evidence is missing.

### 3. Zone capability and restriction engine

**Justification:** Zones carry specialist constraints such as cold chain, hazardous goods, high value cages, quarantine, automation-only areas, and controlled substance storage.

**Improvement:** Model zone capabilities, restrictions, access policies, environmental tolerances, compatibility matrices, and exception approvals. Putaway, pick, replenish, and count workflows should reject tasks that violate zone constraints unless an authorized override is recorded.

### 4. Bin lifecycle and capacity governance

**Justification:** Bins are execution-critical assets; capacity, status, damage, lockout, measurement unit, and slotting class must be accurate.

**Improvement:** Add bin lifecycle states from proposed to active, blocked, maintenance, cycle-count locked, automation reserved, damaged, retired, and archived. Store volumetric, weight, pallet, case, each, and temperature capacity with tolerances and enforce them during putaway and replenishment.

### 5. Dynamic slotting optimization

**Justification:** Static slotting creates travel waste, replenishment churn, congestion, and picker fatigue when demand, item velocity, seasonality, and labor mix change.

**Improvement:** Add slotting recommendations using velocity, affinity, hazard/temperature constraints, cube movement, pick path, replenishment burden, demand seasonality, and ergonomic risk. The workbench should compare current versus proposed slotting before move tasks are generated.

### 6. Dock appointment intelligence

**Justification:** Dock dwell, missed appointments, trailer congestion, labor readiness, and carrier variability drive warehouse throughput.

**Improvement:** Add appointment scoring with expected arrival confidence, unload duration, trailer type, door compatibility, labor demand, yard congestion, inbound priority, detention risk, and quality inspection needs. Dock boards should recommend door assignments and recovery actions.

### 7. Yard-to-dock receiving orchestration

**Justification:** Inbound work begins before goods are scanned at a dock; trailers, seals, appointments, yard moves, and unloading readiness matter.

**Improvement:** Add inbound arrival projections, seal capture, trailer check-in, yard location, door move instructions, unload start/finish, discrepancy capture, detention timers, and proof evidence while keeping transportation state as declared projections.

### 8. Receipt discrepancy and overage workflow

**Justification:** Receiving exceptions such as shorts, overages, wrong item, wrong lot, damage, missing documents, and temperature excursions require governed decisions.

**Improvement:** Add discrepancy reason taxonomy, tolerance rules, photo/document evidence, supplier/carrier projection references, quarantine routing, approval paths, and downstream event evidence. Receipt lines should not silently normalize differences.

### 9. Quality-aware receiving and putaway

**Justification:** Goods cannot be put away or picked until quality and compliance status is understood for regulated or high-risk products.

**Improvement:** Integrate declared quality-release projections into receiving, putaway, and pick eligibility. Model quarantine lanes, sample pulls, inspection waits, conditional release, blocked status, and post-release putaway prioritization with clear operator prompts.

### 10. Putaway decision compiler

**Justification:** Putaway decisions balance capacity, proximity, compatibility, demand, replenishment, cross-dock opportunity, and equipment availability.

**Improvement:** Compile putaway rules into explainable ranking: eligible bins, rejected bins, capacity fit, hazard/temperature compatibility, velocity fit, travel impact, replenishment effect, and override risk. Confirmations should prove scan, operator, bin, item, quantity, and rule version.

### 11. Directed replenishment lifecycle

**Justification:** Forward pick locations fail when replenishment is reactive, poorly prioritized, or detached from active waves.

**Improvement:** Add replenishment triggers for min/max, wave demand, urgent short risk, expiring stock, lane congestion, and equipment availability. Replenishment tasks should include source bin, destination bin, quantity, priority, dependency, expected wave impact, and exception closure.

### 12. Wave planning strategy library

**Justification:** Different warehouses need different release strategies: batch, cluster, zone, order priority, carrier cutoff, temperature, hazard, automation, or labor-balanced waves.

**Improvement:** Implement a wave strategy library with rule parameters, eligibility filters, capacity checks, cutoffs, fairness constraints, and simulation results. Users should preview travel, labor, service risk, carrier risk, and short-pick exposure before release.

### 13. Pick path optimization with constraints

**Justification:** Lowest distance is not always best; congestion, one-way aisles, equipment, ergonomic risk, hazardous zones, and automation interfaces change the route.

**Improvement:** Add path optimization that considers topology, congestion, operator equipment, bin access level, temperature dwell, product separation, pick sequence, and pack-station balancing. Every pick task should carry a route explanation and fallback path.

### 14. Scan validation and anti-bypass controls

**Justification:** Warehouse errors often come from bypassed scans, wrong bin scans, reused labels, blind confirmation, and stale device sessions.

**Improvement:** Add scan-token validation for operator, device, task, bin, item, lot, serial, carton, and timestamp. Record exceptions for manual entry, offline mode, duplicate scans, stale tasks, and supervisor overrides.

### 15. Short-pick resolution workflow

**Justification:** Short picks affect customer promises, inventory accuracy, replenishment, substitutions, and fulfillment priority.

**Improvement:** Add short-pick workflows with alternate bin lookup, substitute proposal, replenishment request, count request, allocation release signal, customer impact projection, and exception reason. The system should distinguish true shortage from inaccessible stock or blocked locations.

### 16. Lot and serial execution controls

**Justification:** Warehouse operators must preserve lot, expiry, FEFO, serial, recall, and custody requirements without owning inventory truth.

**Improvement:** Enforce lot/serial capture from declared allocation and inventory projections during receive, putaway, pick, pack, and ship. Provide trace evidence, rejected-scan reasons, expiry warnings, and recall-block prompts without reading inventory-owned tables.

### 17. Cartonization intelligence

**Justification:** Packing quality affects freight cost, damage, labor, sustainability, and customer experience.

**Improvement:** Add carton recommendation using dimensions, weight, fragility, temperature, hazard separation, carrier constraints, void-fill preference, label placement, sustainability, and cost. Pack stations should show why a carton is selected and when repack is required.

### 18. Pack station workbench completeness

**Justification:** Packers need all operational evidence at the point of work: items, scans, carton, labels, documents, exceptions, weight, and shipping readiness.

**Improvement:** Build a pack station view for task queue, item checklist, scan capture, carton selection, scale reading, label print, document attachment, hazmat/temperature warnings, exception escalation, and final pack proof.

### 19. Label and document proof chain

**Justification:** Missing, duplicated, wrong, or unverified labels create carrier failures and compliance exposure.

**Improvement:** Store label format version, print job, printer identity, reprint reason, scan verification, carrier service, document bundle, and label evidence hash. Reprints should require reason codes and preserve the original proof chain.

### 20. Staging lane and carrier cutoff orchestration

**Justification:** Packed orders can still miss shipment because staging lanes, dock doors, carrier cutoffs, and load sequence are poorly coordinated.

**Improvement:** Add staging lane capacity, carrier/service compatibility, route cutoff, load sequence, dwell risk, temperature exposure, and trailer assignment. The ship queue should rank work by cutoff risk and lane congestion.

### 21. Ship confirmation integrity

**Justification:** Shipping closes the warehouse execution lifecycle and must prove what left, when, by whom, from where, and under which carrier booking.

**Improvement:** Require shipment confirmation evidence for carton IDs, labels, scans, staging lane, dock door, carrier projection, seal/trailer where applicable, operator, timestamp, exceptions, and emitted `OrderShipped` event idempotency.

### 22. Cross-dock eligibility and execution

**Justification:** Cross-docking reduces handling but can violate quality, allocation, routing, or timing constraints if naively applied.

**Improvement:** Add cross-dock eligibility scoring for inbound confidence, outbound demand, dock proximity, quality status, carrier cutoff, handling constraints, and inventory allocation projection. Track direct inbound-to-outbound movement with proof and fallback putaway path.

### 23. Cycle count strategy engine

**Justification:** Counting should target risk and operational value, not only fixed schedules.

**Improvement:** Generate count tasks from velocity, variance history, high-value items, short-picks, blocked bins, stale positions, recent adjustments, new operators, automation faults, and compliance needs. Count tasks should lock or warn on conflicting warehouse work.

### 24. Count variance investigation

**Justification:** A count variance is an operational signal, not just a quantity difference.

**Improvement:** Add variance workflow with recount policy, scan history, recent picks, putaways, replenishments, damages, adjustments, operator/device evidence, likely root cause, inventory event recommendation, and approval requirements.

### 25. Warehouse exception taxonomy

**Justification:** Generic exception buckets hide systemic problems and make automation unsafe.

**Improvement:** Define specialist exceptions for blocked bin, inaccessible aisle, damaged goods, missing stock, scan mismatch, printer failure, conveyor jam, carrier delay, dock no-show, label rejection, pack weight mismatch, temperature excursion, and labor no-show. Each exception should define severity, owner, SLA, recovery action, and release evidence.

### 26. Labor skill and certification assignment

**Justification:** WMS must assign work based on skills, certifications, equipment authorization, shift availability, ergonomics, and safety constraints.

**Improvement:** Add labor skill profiles, certification checks, forklift or equipment eligibility, restricted-zone authorization, fatigue limits, task priority, and fair workload assignment. The system should explain why a worker is or is not eligible.

### 27. Labor productivity with context

**Justification:** Productivity metrics are misleading unless adjusted for travel, congestion, task type, item handling difficulty, device failures, and exception burden.

**Improvement:** Store contextual productivity measures by operator, zone, wave, task type, equipment, shift, exception rate, and congestion. Use these metrics for planning while preventing punitive or opaque automation decisions.

### 28. Mechanism-design task allocation

**Justification:** Pure efficiency optimization can overload skilled workers, starve low-priority tasks, or create unsafe incentives.

**Improvement:** Add task allocation policies with fairness, fatigue, service priority, skill scarcity, queue aging, travel minimization, and safety constraints. Simulate task distribution before releasing major waves or replenishment bursts.

### 29. Edge-device command governance

**Justification:** Scanners, printers, scales, conveyors, and sorters are operational actors that can create or corrupt evidence.

**Improvement:** Add device registry, capability matrix, firmware/version evidence, command authorization, heartbeat, offline mode, retry, command result, replay, and tamper detection. Device commands should be auditable and idempotent.

### 30. Offline and degraded-mode execution

**Justification:** Warehouses cannot always stop when networks, scanners, printers, or external projections fail.

**Improvement:** Define degraded modes for receiving, picking, packing, shipping, and counting with local task cache, bounded offline scans, conflict reconciliation, supervisor approval, and automatic event replay once connectivity returns.

### 31. Conveyor and automation event reconciliation

**Justification:** Automated material handling creates high-volume events that must reconcile to tasks, cartons, bins, and exceptions.

**Improvement:** Add event correlation for conveyor scans, sorter diverts, weight checks, chute assignments, jams, reject lanes, and manual removals. Reconcile automation events to owned tasks and mark orphaned or contradictory events for triage.

### 32. Warehouse traceability timeline

**Justification:** Operators and auditors need to reconstruct warehouse execution from receipt to shipment without cross-table leakage.

**Improvement:** Build a warehouse-owned trace timeline for receipts, putaway, replenishment, picks, packs, labels, staging, shipment, counts, exceptions, edge events, and emitted AppGen-X events. Link external context only through declared projections.

### 33. Zero-knowledge shipment proof

**Justification:** Customers, carriers, or auditors may need shipment integrity evidence without exposing sensitive order, item, or operator details.

**Improvement:** Generate cryptographic shipment proofs from carton, label, scan, staging, dock, carrier, and ship-confirmation evidence. Provide verification APIs that prove integrity and timing while redacting protected payload fields.

### 34. Policy screening for restricted warehouse actions

**Justification:** Restricted bins, high-value stock, hazardous goods, cold chain, blocked carriers, and sensitive operators require dynamic controls.

**Improvement:** Add policy screening before receive, putaway, pick, pack, ship, count, override, and edge replay actions. The screening record should include policy version, attributes evaluated, decision, explanation, override route, and audit evidence.

### 35. Carbon-aware warehouse execution

**Justification:** Warehouse execution choices affect energy, travel, packaging, carrier staging, and refrigeration loads.

**Improvement:** Add carbon-aware wave, pack, and staging recommendations that consider travel, equipment, refrigeration windows, carton choice, carrier cutoff, and renewable-energy schedules. Show operational tradeoffs instead of silently optimizing for emissions.

### 36. Congestion and dock-dwell forecasting

**Justification:** Congestion causes missed cutoffs, overtime, unsafe aisles, and poor utilization.

**Improvement:** Forecast congestion by zone, aisle, dock, pack station, staging lane, and labor group using open tasks, appointments, waves, automation health, and historical throughput. Surface intervention recommendations with confidence and expected impact.

### 37. Predictive damage and exception risk

**Justification:** Damage and exception risk can be mitigated before work is executed.

**Improvement:** Score tasks for damage, short-pick, scan mismatch, label failure, pack weight mismatch, and carrier rejection risk using item handling attributes, zone history, operator context, device health, and timing pressure. Require explainable, monitored models.

### 38. Warehouse MLOps governance

**Justification:** WMS automation influences safety, service, and labor outcomes, so models require governance.

**Improvement:** Add feature lineage, training data windows, drift detection, bias/fairness checks for labor allocation, explainability, approval status, rollback, and model-specific release evidence for putaway, wave, labor, congestion, and anomaly models.

### 39. Rule and parameter simulation

**Justification:** Changing wave size, putaway tolerance, replenishment thresholds, scan tolerance, or dock dwell targets can disrupt the whole warehouse.

**Improvement:** Simulate rule and parameter changes against historical and open work to show effects on travel, throughput, labor load, late shipments, exceptions, replenishment, congestion, and dead-letter volume before activation.

### 40. AppGen-X event reliability cockpit

**Justification:** Warehouse operations depend on declared consumed events and emitted events; retries and dead letters must be operationally visible.

**Improvement:** Add workbench panels for inbox status, outbox status, duplicate detection, retry schedule, dead-letter reasons, handler version, payload lineage, replay eligibility, and projection freshness for inventory, carrier, quality, inbound, and access-policy events.

### 41. Boundary proof for warehouse-only ownership

**Justification:** WMS must not bypass inventory, transportation, quality, order, identity, or finance packages by reading their tables.

**Improvement:** Add static and runtime checks proving WMS commands touch only WMS-owned tables plus AppGen-X inbox/outbox/dead-letter tables. Include failing fixtures for direct inventory balance, carrier table, customer table, and finance table access.

### 42. Workbench coverage for all WMS capabilities

**Justification:** World-class WMS cannot hide specialist functionality behind backend-only commands.

**Improvement:** Expand UI fragments into warehouse setup, topology map, dock board, receiving console, putaway queue, replenishment board, wave planner, pick monitor, pack station, staging board, ship queue, cross-dock view, cycle count, labor console, edge replay, exceptions, controls, rules, parameters, configuration, and agent panels.

### 43. Operator guidance and next-best action

**Justification:** Warehouse users work under time pressure and need concise, role-aware guidance at each station.

**Improvement:** Add next-best-action guidance for receiver, putaway operator, picker, packer, ship clerk, supervisor, maintenance, and auditor roles. Guidance should explain required scans, blocked actions, exception recovery, and safety warnings.

### 44. Agent-safe document and instruction intake

**Justification:** The WMS chatbot should process ASN notes, dock schedules, pack instructions, carrier messages, and exception photos without unsafe writes.

**Improvement:** Add document intake skills that extract candidate warehouse facts, map them to owned tables, validate rules/permissions, reject foreign-table mutations, and produce side-effect-free CRUD previews with confidence, risks, required confirmations, and expected AppGen-X events.

### 45. Agent-safe task execution planning

**Justification:** AI assistance can improve warehouse throughput only if it respects physical constraints and human confirmation gates.

**Improvement:** Require the agent to generate execution plans for receiving, putaway, wave release, packing, shipping, counting, and exception recovery that list command, permission, owned tables, idempotency key, event outcome, affected tasks, rollback limits, and human approval.

### 46. Continuous warehouse control testing

**Justification:** Controls should run throughout operations, not only at release or period audits.

**Improvement:** Add executable assertions for blocked-bin picks, over-capacity putaway, stale waves, orphaned cartons, duplicate labels, unshipped packed orders, dead-letter aging, unauthorized overrides, scan bypasses, and unreconciled edge events.

### 47. Warehouse close and shift handover

**Justification:** Warehouses need operational closure by shift, wave, dock, and day to prevent hidden work and accountability gaps.

**Improvement:** Add close and handover workflows for open receipts, unfinished putaway, replenishment blockers, partial waves, pack exceptions, staged-not-shipped cartons, count variances, device faults, and dead-letter events. Produce shift evidence packets.

### 48. Multi-site federation without shared tables

**Justification:** Enterprises operate multiple warehouses and external fulfillment nodes while keeping each package boundary clean.

**Improvement:** Add federation projections for site capacity, operational status, cutoff risk, cross-site transfer readiness, and exception signals. The WMS should answer network execution questions using declared projections rather than foreign operational tables.

### 49. Warehouse readiness score

**Justification:** Users need a concise, evidence-backed view of whether WMS is production-ready for a warehouse or tenant.

**Improvement:** Compute readiness from setup completeness, topology quality, bin capacity coverage, dock readiness, rule activation, parameter validation, event reliability, UI coverage, edge health, labor permissions, control assertions, boundary proof, and agent safety.

### 50. End-to-end execution proof

**Justification:** A complete WMS PBC must prove it can run the full physical flow from inbound arrival to shipped order.

**Improvement:** Add an executable proof scenario covering inbound arrival projection, receipt, discrepancy handling, putaway, replenishment, allocation projection, wave release, pick, pack, label, staging, ship confirmation, emitted `OrderShipped`, trace timeline, UI evidence, controls, and agent explanation.
