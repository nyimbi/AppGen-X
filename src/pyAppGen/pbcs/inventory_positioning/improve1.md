# Inventory Positioning PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `inventory_positioning`. The items are specific to inventory truth and positioning operations: item governance, node topology, lots, serials, balances, receipts, adjustments, cycle counts, reservations, ATP/CTP, allocations, quality holds, in-transit stock, traceability, backorders, replenishment, reconciliation, channel protection, stock risk, and agent-assisted inventory work.

## Current Domain Evidence Used

- Domain purpose: enterprise inventory truth for item masters, attributes, substitutions, lots, serials, nodes, calendars, capacity, positions, receipts, adjustments, reservations, allocations, releases, quality holds, in-transit projections, traceability, backorders, replenishment, reconciliation, policy screening, stock proofs, federation, carbon fulfillment, competing channel allocation, anomaly signals, stock risk models, rules, parameters, configuration, UI fragments, and release evidence.
- Owned boundary: items, attributes, substitutions, lots, serials, nodes, node calendars/capacity/identity, inventory positions, position snapshots, receipts and receipt lines, adjustments, cycle counts, reservations, allocations and lines, allocation expiry, quality holds/releases, in-transit projections, traceability events, backorders, replenishment signals/plans, reconciliations, policy screenings, stock proofs, cross-node federation, carbon fulfillment, channel allocation, anomaly signals, stock risk models, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: item registration, node registration, receipts, adjustments, availability, allocations, allocation release, quality holds, AppGen-X inbox handling, workbench, rules, parameters, schema extensions, and configuration.
- Existing events and dependencies: emits `ItemRegistered`, `InventoryNodeRegistered`, `GoodsReceiptPosted`, `InventoryAdjusted`, `InventoryAllocated`, `InventoryReleased`, and `QualityHoldApplied`; consumes order, shipment, quality, purchase receipt, demand forecast, and access-policy events through declared APIs/projections only.

## 50 Better-Than-World-Class Improvements

### 1. Item master readiness gate

**Justification:** Inventory accuracy begins with item setup. Items without UOM, tracking flags, substitution rules, shelf-life, hazard, and allocation eligibility create downstream stock errors.

**Improvement:** Add item readiness checks for SKU identity, base UOM, conversion policy, lot/serial tracking, shelf-life, quality policy, substitution group, fulfillment eligibility, and release approval. Block receipts and allocations for incomplete controlled items.

### 2. Unit-of-measure conversion governance

**Justification:** Quantity errors often arise from inconsistent pack, each, case, pallet, weight, or variable-measure conversions.

**Improvement:** Add UOM conversion records with item scope, conversion precision, effective dates, catch-weight behavior, rounding, and validation fixtures. Availability and allocation should cite the conversion rule used.

### 3. Item attribute taxonomy controls

**Justification:** Attributes drive allocation, storage, quality, substitution, tax, shipping, and replenishment decisions.

**Improvement:** Define governed attribute schemas with allowed values, inheritance, validation, sensitivity, and operational use. Workbench views should show missing attributes that block stock movement or allocation.

### 4. Substitution eligibility engine

**Justification:** Substitutions affect customer promise, safety, compliance, margin, and channel rules.

**Improvement:** Add substitution rules with priority, equivalence class, customer/channel eligibility, regulatory restrictions, margin impact, expiration constraints, and approval evidence. ATP should explain when a substitute is proposed or rejected.

### 5. Lot lifecycle governance

**Justification:** Lot-controlled inventory requires manufacture/receipt date, expiry, quarantine, release, recall, and traceability evidence.

**Improvement:** Model lot states from created to received, quarantined, released, blocked, expired, recalled, consumed, and closed. Store shelf-life, potency/grade, supplier lot, quality release, and recall scope.

### 6. Serial custody and uniqueness controls

**Justification:** Serial-controlled goods require one physical unit, one status, one location, and complete custody history.

**Improvement:** Add serial uniqueness checks, current node, lot, custodian, status, reservation link, shipment link, return status, and trace chain. Prevent duplicate on-hand serial positions across nodes.

### 7. Node master operating model

**Justification:** Warehouses, stores, vendors, virtual nodes, in-transit nodes, and cross-docks behave differently.

**Improvement:** Add node types with allowed inventory states, allocation eligibility, receiving rules, shipping cutoff, ownership model, tenant scope, and capacity profile. Workbench views should distinguish physical, virtual, vendor, and in-transit stock.

### 8. Node calendar and cutoff logic

**Justification:** Availability depends on working days, receiving windows, shipping cutoffs, holidays, and carrier handoff times.

**Improvement:** Add calendar policies with local timezone, receiving/shipping windows, holidays, blackout periods, and cutoff handling. ATP/CTP should use calendar evidence to calculate promise dates.

### 9. Node capacity by item and handling class

**Justification:** A node can have units available but no capacity to receive, store, pick, or handle certain stock.

**Improvement:** Add capacity constraints by item class, temperature zone, hazard class, cubic volume, weight, labor window, and receiving dock. Allocation and replenishment should flag capacity conflicts.

### 10. Inventory position invariant engine

**Justification:** Inventory truth depends on on-hand, reserved, allocated, quarantine, in-transit, and available quantities balancing correctly.

**Improvement:** Add invariants proving non-negative balances, state transitions, reservation <= on-hand, allocation <= available, quarantine exclusions, and serial/lot consistency. Store invariant proof with every position mutation.

### 11. Event-sourced stock ledger

**Justification:** Stock positions must be reconstructable from receipts, adjustments, holds, releases, reservations, allocations, shipments, and returns.

**Improvement:** Add stock ledger events with sequence, item, node, lot/serial, quantity delta, state, source, previous hash, and idempotency key. Position snapshots should be rebuildable and verifiable from this ledger.

### 12. Receipt quality and tolerance workflow

**Justification:** Receipts can have overages, shortages, damage, wrong item, unknown lot, expired lot, or quality hold requirements.

**Improvement:** Add receipt validation against purchase receipt projections, expected quantity, tolerance, lot/serial requirements, expiry, quality inspection, and damage codes. Generate exception cases and quality holds where required.

### 13. Putaway eligibility signal

**Justification:** Even if WMS performs physical putaway, inventory positioning must know whether stock is usable, staged, quarantined, or pending receipt.

**Improvement:** Add receipt-to-position states for staged, inspected, accepted, quarantined, available, and rejected. Expose availability only after policy-defined usable state is reached.

### 14. Adjustment reason governance

**Justification:** Adjustments change stock truth and can hide shrink, damage, theft, counting error, or integration failure.

**Improvement:** Add adjustment reason taxonomy, required evidence, approval thresholds, root cause, financial impact, lot/serial impact, and recurrence detection. High-risk adjustments should trigger control assertions.

### 15. Cycle count program design

**Justification:** Inventory accuracy requires risk-based counting, not only ad hoc corrections.

**Improvement:** Add count programs by item velocity, value, shrink risk, location, lot expiry, serial sensitivity, and prior variance. Generate count tasks, blind-count rules, recount thresholds, and approval workflows.

### 16. Count variance resolution

**Justification:** Variances should create auditable corrections and root-cause learning.

**Improvement:** Add variance records with expected quantity, counted quantity, recount result, cause, approver, adjustment linkage, financial impact, and prevention action. Release controls should track unresolved material variances.

### 17. Reservation lifecycle and expiry

**Justification:** Reservations can starve channels if they never expire or are not tied to demand priority.

**Improvement:** Model reservations with demand source, priority, item/node/lot, expiry, renewal rule, partial reservation, substitution allowance, and release reason. Expiry should emit evidence and update availability.

### 18. Allocation policy compiler

**Justification:** Allocation must respect customer priority, channel protection, node eligibility, lot rules, expiration, fulfillment cost, and service levels.

**Improvement:** Compile allocation policies with demand class, node ranking, lot strategy, partial allocation, substitution, safety stock, and override rules. Store policy version and decision trace for every allocation.

### 19. ATP and CTP convergence

**Justification:** Availability-to-promise is incomplete without capacity-to-promise, node calendars, in-transit supply, replenishment, and quality holds.

**Improvement:** Add ATP/CTP calculation traces combining current position, reservations, capacity, calendars, in-transit projections, replenishment plans, and holds. Return promise confidence, earliest date, and limiting constraint.

### 20. Allocation release and reallocation safety

**Justification:** Releasing or reallocating inventory can break orders, channels, or compliance promises.

**Improvement:** Add release workflows with original demand, reason, downstream notification, reallocation candidates, customer impact, and audit proof. Require approval for protected or high-priority demand.

### 21. Quality hold and release governance

**Justification:** Quality holds must remove stock from availability until release evidence is present.

**Improvement:** Add hold categories, source inspection, affected lot/serial/position, release criteria, partial release, expiry, and disposition. Availability must explicitly exclude held stock and explain hold reasons.

### 22. Expiry and FEFO management

**Justification:** Perishable and regulated stock require first-expiry-first-out, minimum shelf life, and expiry risk visibility.

**Improvement:** Add expiry rules by item/customer/channel, minimum remaining shelf life, FEFO allocation strategy, expiry alerts, and disposal/markdown recommendations. ATP should reject lots that violate customer shelf-life rules.

### 23. Recall traceability engine

**Justification:** Lot and serial recalls need rapid forward and backward traceability across receipts, holds, shipments, adjustments, and allocations.

**Improvement:** Build trace queries that show supplier lot, receipt, nodes, current positions, shipped demand, affected customers, open allocations, and quarantine state. Generate recall hold plans and proof bundles.

### 24. In-transit inventory confidence model

**Justification:** In-transit stock can be delayed, damaged, split, or diverted, so it should not be treated like on-hand stock.

**Improvement:** Add in-transit confidence based on carrier milestone, ETA, route risk, ASN quality, receiving capacity, and delay signals. ATP should use confidence bands and distinguish firm versus probable supply.

### 25. Backorder prioritization

**Justification:** Scarce inventory must be assigned to backorders by policy, customer value, SLA, age, margin, and fairness.

**Improvement:** Add backorder queues with priority, promise date, substitution eligibility, split-shipment policy, customer impact, and escalation. Allocation simulations should show who gains and loses under each policy.

### 26. Replenishment signal quality

**Justification:** Replenishment depends on safety stock, forecast, lead time, MOQ, pack size, shelf life, and capacity.

**Improvement:** Add replenishment signals with trigger reason, forecast source, lead-time confidence, supplier/node constraints, MOQ, economic order quantity, expiry risk, and approval status.

### 27. Replenishment plan simulation

**Justification:** Plans can overstock, understock, violate capacity, or miss demand if assumptions are hidden.

**Improvement:** Simulate replenishment plans against demand forecasts, open orders, capacity, in-transit supply, safety stock, and spoilage risk. Persist rejected plans and scenario assumptions.

### 28. Safety stock policy governance

**Justification:** Safety stock is a capital/service-level tradeoff that must be explicit.

**Improvement:** Add safety stock rules by item/node/channel with target service level, demand variability, lead-time variability, seasonality, shelf-life, and override approval. Show working-capital impact.

### 29. Channel protection and fair allocation

**Justification:** Retail, wholesale, ecommerce, marketplace, and strategic customers often compete for constrained inventory.

**Improvement:** Add channel allocation policies with quotas, floors, caps, fairness rules, priority windows, and release conditions. Decision traces should explain channel tradeoffs.

### 30. Negative inventory prevention and recovery

**Justification:** Negative inventory corrupts availability, costing, and fulfillment.

**Improvement:** Add pre-mutation screening for negative positions by item/node/lot/serial, with emergency override, cause, expiry, and recovery plan. Reconciliation should track negative-inventory closure evidence.

### 31. Inventory reconciliation with external projections

**Justification:** Stock truth must reconcile with WMS, order, procurement, quality, transportation, and audit projections without sharing tables.

**Improvement:** Add reconciliation runs comparing owned positions to declared projections, with variance type, stale projection warning, root cause, and correction plan.

### 32. Stock proof for external promises

**Justification:** Partners or customers may need proof that stock was available without seeing full inventory details.

**Improvement:** Generate disclosure-minimized stock proofs with item, quantity, node class, expiry, reservation, and proof hash. Include verifier instructions and expiry time.

### 33. Inventory anomaly taxonomy

**Justification:** Inventory anomalies need domain-specific categories rather than generic risk scores.

**Improvement:** Classify anomalies as shrink spike, receipt variance, allocation churn, reservation hoarding, serial duplication, lot expiry surge, stale in-transit, negative position, quality-hold leakage, or forecast mismatch.

### 34. Stockout and spoilage risk governance

**Justification:** Risk models affect purchasing, allocation, markdown, and customer promise.

**Improvement:** Govern risk models with feature lineage, forecast source, drift, confidence, deterministic fallback, and action thresholds. Workbench recommendations should show risk contributors.

### 35. Carbon-aware fulfillment signals

**Justification:** Inventory positioning can steer demand toward lower-carbon nodes when service and policy permit.

**Improvement:** Add carbon fulfillment records with node energy profile, transport projection, service impact, customer policy, and carbon score. Allocation should show carbon-aware alternatives where eligible.

### 36. Node identity and trust verification

**Justification:** Virtual, vendor-managed, third-party, and in-transit nodes need identity and trust evidence before their stock can be promised.

**Improvement:** Add node credentials with issuer, validity, service scope, revocation, and trust level. ATP should degrade or block stock from untrusted nodes.

### 37. Cross-node federation contracts

**Justification:** Enterprise inventory may include external nodes and partner stock, but direct table access violates PBC boundaries.

**Improvement:** Add federation contracts with source, refresh SLA, trust score, allowed use, quantity confidence, and stale-data behavior. Show federated stock separately from owned confirmed stock.

### 38. Inventory ownership and consignment handling

**Justification:** Stock may be owned, consigned, vendor-owned, customer-owned, or reserved under contract.

**Improvement:** Add ownership status, title transfer rules, consignment terms, billing trigger, and availability eligibility. Prevent owned-stock calculations from including third-party stock incorrectly.

### 39. Kitting and bundle availability

**Justification:** Availability for kits and bundles depends on component stock, substitutions, capacity, and assembly lead time.

**Improvement:** Add kit composition, component availability, substitute components, assembly node, capacity, and promise confidence. ATP should explain bundle bottlenecks.

### 40. Serialized lifecycle trace

**Justification:** High-value serialized goods require exact lifecycle trace from receipt through allocation, shipment, return, repair, and retirement.

**Improvement:** Add serial timeline views with all owned events, projections, status changes, custody, location, quality holds, and customer/order references where declared.

### 41. Inventory close and control cockpit

**Justification:** Period close needs inventory movement, adjustments, counts, holds, negative positions, and reconciliation visibility.

**Improvement:** Add close cockpit panels for unposted receipts, unresolved adjustments, count variances, stale in-transit, negative positions, quality leakage, and reconciliation blockers.

### 42. Agent-safe availability explanation

**Justification:** The inventory chatbot should answer availability questions but avoid overpromising stock.

**Improvement:** Require agent answers to include position freshness, reservations, holds, in-transit confidence, capacity constraints, substitutions, and policy caveats. Low-confidence availability should be marked as tentative.

### 43. Agent-safe allocation planning

**Justification:** Allocations affect customer promises and channel fairness, so AI must not silently move stock.

**Improvement:** Add allocation previews with impacted orders, node choices, lot/serial choices, substitutions, fairness impact, stockout risk, and reversal path. Require human approval for protected stock or low-confidence decisions.

### 44. Agent-safe adjustment and count support

**Justification:** Adjustments change inventory truth and can hide shrink or process failure.

**Improvement:** The agent should draft adjustment/count remediation plans with reason, evidence, expected quantity, variance, financial impact, control risk, and approval route. It should not post material adjustments autonomously.

### 45. Rule and parameter simulation

**Justification:** Safety stock, reservation TTL, partial allocation thresholds, reconciliation tolerance, and stockout risk thresholds materially change operations.

**Improvement:** Simulate rule/parameter changes against historical and open inventory activity, showing availability, stockouts, backorders, allocation churn, replenishment workload, and exception impact.

### 46. Workbench coverage for all inventory capabilities

**Justification:** Inventory specialists need operational access to every lifecycle surface, not hidden backend commands.

**Improvement:** Expand UI into item governance, node topology, position viewer, receipt console, adjustment board, cycle count, availability trace, allocation workbench, holds, traceability, in-transit, backorder, replenishment, reconciliation, anomaly, close, and agent panels.

### 47. Continuous inventory controls

**Justification:** Inventory controls should run continuously across position integrity, reservations, allocations, lots, serials, and reconciliation.

**Improvement:** Add control assertions for negative stock, stale reservations, expired lots, serial duplication, quality-hold leakage, unreconciled projections, count variance aging, and stock proof integrity.

### 48. Boundary proof for inventory-only ownership

**Justification:** Inventory must integrate with order, WMS, procurement, quality, transportation, commerce, identity, schema, and audit without reading their tables.

**Improvement:** Add static/runtime checks proving commands use only inventory-owned tables plus declared APIs/events/projections. Include failing fixtures for direct foreign-table references.

### 49. Inventory readiness score

**Justification:** Users need a concise measure of whether inventory positioning is ready for production stock truth.

**Improvement:** Compute readiness from item completeness, node trust, position invariants, receipt quality, allocation traceability, holds, lot/serial trace, in-transit confidence, reconciliation, UI coverage, boundary proof, and agent safety.

### 50. End-to-end stock trace

**Justification:** Inventory excellence depends on tracing stock from item setup through receipt, status changes, reservation, allocation, release, hold, shipment, adjustment, count, and reconciliation.

**Improvement:** Build an end-to-end stock trace using inventory-owned records and declared projections. The agent should answer stock state questions from this trace with evidence and confidence.
