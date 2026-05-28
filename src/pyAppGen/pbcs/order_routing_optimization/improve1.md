# Order Routing Optimization PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `order_routing_optimization`. The items are specific to distributed order routing: routing plans, plan legs, node topology, node calendars, services, capacity, constraints, cost components, promises, split shipments, inventory/transport/service inputs, route candidates, capacity snapshots, routing decisions, reservations, simulations, optimization runs, exceptions, approvals, feedback, policy screening, federation, carbon-aware scheduling, network optimization, capacity allocation, anomaly detection, exposure modeling, forecasts, parsed requests, rules, parameters, configuration, AppGen-X event reliability, UI workbenches, and agent-assisted routing operations.

## Current Domain Evidence Used

- Domain purpose: `order_routing_optimization` owns optimized fulfillment route selection across orders, regions, nodes, capacity, costs, promises, tax, inventory, transportation, service inputs, split shipments, approvals, feedback, and routing evidence.
- Owned boundary: routing plans and legs, nodes, node calendars, node services, node capacity, routing constraints, cost components, promises, split shipments and legs, inventory/transport/service input projections, route candidates, capacity snapshots, decisions, node reservations, simulations, optimization runs, exceptions and resolutions, approvals, feedback, policy screening, audit traces, federation projections, carbon schedules, network optimization, capacity allocation, anomaly signals, exposure models, forecasts, parsed requests, seed data, schema extensions, control assertions, governed models, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: configuration, parameters, rules, schema extensions, event handling, capacity snapshot intake, route candidate upsert, order routing, node capacity reservation, simulations, capacity forecasts, exception recommendations, request parsing, fulfillment-risk scoring, self-healing route selection, routing proofs, policy screening, control tests, federation, resilience drills, crypto rotation, carbon-aware scheduling, network optimization, capacity auctions, anomaly detection, stochastic exposure, governed model registration, workbench, schema/service/release evidence, permissions, UI binding, and boundary verification.
- Existing events and dependencies: emits `FulfillmentRouteSelected` and `NodeCapacityReserved`; consumes `OrderVerified`, `AvailabilityProjected`, and `TaxCalculated`; integrates with order, inventory, tax, WMS, transportation, DOM, approval, and feedback capabilities only through declared APIs/events/projections.

## 50 Better-Than-World-Class Improvements

### 1. Routing request readiness gate

**Justification:** Route selection is unsafe when order verification, availability, tax, destination, service level, item restrictions, and promise requirements are incomplete.

**Improvement:** Add a readiness gate validating order projection, destination, items, quantities, service commitment, channel, customer priority, availability projection freshness, tax projection freshness, regional restrictions, split policy, substitution mode, and approval requirements before routing begins.

### 2. Routing plan lifecycle state machine

**Justification:** Routing plans move through draft, candidate collection, optimization, policy review, approval, reservation, selected, superseded, failed, and cancelled states.

**Improvement:** Implement plan state transitions with actor, timestamp, reason, idempotency key, required evidence, allowed next states, emitted event expectations, and invalid-transition explanations.

### 3. Plan leg modeling

**Justification:** Multi-leg fulfillment can include node pick, pack, handoff, carrier movement, consolidation, cross-dock, pickup, and final delivery.

**Improvement:** Model each leg with sequence, origin, destination, service, carrier, cutoff, expected duration, cost, capacity, risk, carbon, dependency, and proof of inclusion in the selected route.

### 4. Routing node readiness

**Justification:** Nodes cannot be selected unless calendars, services, capacity, inventory, restrictions, and operating status are current.

**Improvement:** Add node readiness checks for status, calendar, cutoff, service coverage, capacity snapshot freshness, supported fulfillment modes, inventory projection, tax region, transport options, carbon profile, and exception state.

### 5. Node calendar and cutoff intelligence

**Justification:** Promises fail when routing ignores holidays, shift calendars, processing cutoffs, blackout windows, and carrier pickup times.

**Improvement:** Add calendar logic for node operating windows, regional holidays, carrier cutoffs, processing lead time, blackout periods, surge exceptions, and promise feasibility calculations.

### 6. Node service capability catalog

**Justification:** Nodes differ by pick, pack, ship, pickup, return, hazmat, cold chain, oversized, custom handling, and marketplace capabilities.

**Improvement:** Model node services with eligibility, item constraints, channel constraints, throughput, service-level support, required equipment, compliance flags, and route-candidate compatibility checks.

### 7. Capacity snapshot integrity

**Justification:** Routing decisions rely on capacity signals that may be stale, duplicated, or inconsistent with reservations.

**Improvement:** Validate capacity snapshots by node, service, date/time bucket, capacity type, available quantity, reserved quantity, source timestamp, freshness SLA, confidence, and prior reservation effects.

### 8. Node capacity reservation lifecycle

**Justification:** Capacity must be reserved, confirmed, released, expired, or rebalanced without double-booking nodes.

**Improvement:** Implement reservation states with hold minutes, quantity, service bucket, order reference, route plan, expiration, release reason, confirmation, conflict detection, and `NodeCapacityReserved` evidence.

### 9. Routing constraint compiler

**Justification:** Constraints such as blocked nodes, regions, item restrictions, split limits, service levels, and carbon budgets must be deterministic and explainable.

**Improvement:** Compile routing constraints from rules into hash-backed predicates with eligible nodes, regions, capacity floors, split policy, substitution mode, status, effective dates, and human-readable decision explanations.

### 10. Cost component traceability

**Justification:** Routing cost is a composite of fulfillment, handling, shipping, tax, split, delay, exception, carbon, and service-failure risk.

**Improvement:** Record cost components per candidate and selected route with source, currency, formula, confidence, tax projection reference, carbon cost, risk adjustment, and counterfactual comparison.

### 11. Delivery promise evidence

**Justification:** Selected routes must prove how the promised date, service level, and confidence were derived.

**Improvement:** Store promise evidence with cutoff, processing time, carrier service, transit time, destination, calendar, capacity, tax constraints, freshness, confidence, and customer-facing promise text.

### 12. Split-shipment governance

**Justification:** Splits improve availability but increase cost, complexity, emissions, customer friction, and failure risk.

**Improvement:** Add split eligibility, max split count, item grouping, shipment leg evidence, incremental cost, promise impact, carbon impact, customer policy, approval threshold, and split-suppression rationale.

### 13. Inventory input projection controls

**Justification:** Routing must not directly read inventory tables and must trust only declared availability projections.

**Improvement:** Validate inventory input projections for item, quantity, node, channel, freshness, confidence, ATP/CTP mode, reservation compatibility, and idempotent `AvailabilityProjected` lineage.

### 14. Transport input projection controls

**Justification:** Carrier and service options can change by lane, cutoff, capacity, disruption, cost, and compliance.

**Improvement:** Normalize transport inputs by carrier, service, origin, destination, lane, cutoff, ETA, cost, capacity, disruption flag, carbon estimate, and eligibility constraints.

### 15. Service input projection controls

**Justification:** Service promises depend on customer tier, channel policy, subscription promise, delivery window, and handling requirements.

**Improvement:** Normalize service inputs into customer/service level, time window, channel rule, handling requirement, substitution allowance, split preference, promise penalty, and approval policy.

### 16. Route candidate completeness scoring

**Justification:** Candidates are not comparable unless costs, capacity, promises, risk, carbon, constraints, and dependencies are complete.

**Improvement:** Score candidate completeness and block selection when required fields, projection freshness, node readiness, cost evidence, promise evidence, or policy screening evidence are missing.

### 17. Multi-objective route scoring

**Justification:** The best route is not always cheapest or fastest; it must balance SLA, cost, capacity, risk, tax, carbon, and customer experience.

**Improvement:** Add weighted scoring with configurable cost, SLA, capacity, risk, carbon, split, margin, customer priority, and confidence weights plus an explanation of tradeoffs.

### 18. Probabilistic promise confidence

**Justification:** Deterministic promise dates hide uncertainty from stale availability, transport disruption, capacity variance, and node performance.

**Improvement:** Compute confidence intervals for delivery promise, capacity availability, split success, cost estimate, and route completion using projection freshness and historical performance.

### 19. Fulfillment risk score

**Justification:** Route decisions should surface likely failures before an order is promised.

**Improvement:** Score fulfillment risk by node capacity, node reliability, inventory freshness, transport disruption, tax confidence, split complexity, weather/service disruptions, and exception history.

### 20. Counterfactual simulation lab

**Justification:** Operators need to understand what would happen if a different node, split policy, carrier, or carbon weight were used.

**Improvement:** Add simulations comparing alternate nodes, service modes, split limits, substitution modes, capacity reservations, carbon weights, and approval policies with cost, SLA, risk, and capacity outcomes.

### 21. Network optimization runs

**Justification:** Route optimization must operate at network scale, not only one order at a time.

**Improvement:** Add optimization runs over order batches, nodes, service buckets, constraints, carbon windows, and capacity limits with candidate rankings, objective values, infeasibility reasons, and reproducible inputs.

### 22. Capacity allocation auction

**Justification:** Scarce node capacity may need principled allocation across channels, customers, service levels, and order values.

**Improvement:** Add capacity allocation mechanisms with demand bids, priority classes, fairness constraints, reserve prices, allocation proof, losing-bid explanation, and override governance.

### 23. Carbon-aware routing schedule

**Justification:** Routing can reduce emissions when lower-carbon nodes or lanes still meet promise constraints.

**Improvement:** Add carbon schedules using node carbon profile, lane emissions, service guardrails, cost tradeoff, promise confidence, approval thresholds, and customer/channel carbon policy.

### 24. Dynamic routing policy screening

**Justification:** Some routes must be blocked due to geography, tax, item restrictions, capacity floor, customer promises, compliance, or carbon budgets.

**Improvement:** Add policy screening with allow/block/review outcomes, violated rule references, override eligibility, approval queue, evidence requirements, and selected-route impact.

### 25. Routing approval workflow

**Justification:** High-risk routes, high-cost splits, customer-impacting substitutions, and carbon/cost overrides need controlled approval.

**Improvement:** Add approval states, approver role, threshold, policy reason, route evidence packet, escalation, expiry, denial reason, and audit trace before route finalization.

### 26. Routing feedback ledger

**Justification:** Optimization improves only when selected routes are compared with fulfillment outcomes.

**Improvement:** Capture feedback for actual ship node, ship time, delivery date, cost variance, service failure, customer complaint, split success, capacity accuracy, and model training eligibility.

### 27. Exception resolution workflow

**Justification:** Nodes go offline, capacity disappears, projections go stale, tax changes, and carriers fail after route planning.

**Improvement:** Add exception cases with category, severity, affected order/plan, stale dependency, recommended reroute, approval requirement, customer impact, replay option, and closure evidence.

### 28. Self-healing route selection

**Justification:** Routing should recover safely when a selected node becomes unavailable before fulfillment execution.

**Improvement:** Add self-healing that detects capacity loss, node outage, stale availability, rejected reservation, or transport disruption, then proposes safe reroute candidates with human approval for material impacts.

### 29. Capacity forecast engine

**Justification:** Future routing decisions need forecasted node capacity and saturation risk.

**Improvement:** Forecast capacity by node, service, calendar bucket, channel, demand class, planned labor, transportation constraints, current reservations, and historical throughput.

### 30. Demand surge protection

**Justification:** Promotions, holidays, regional spikes, and marketplace events can overwhelm normal routing policies.

**Improvement:** Add surge detection, capacity buffers, channel throttles, split controls, priority protection, promise confidence downgrade, and automatic escalation.

### 31. Natural-language route request parsing

**Justification:** Users ask routing questions in operational language such as "find the lowest-risk route that avoids node X."

**Improvement:** Parse route requests into safe query/simulation inputs with item, region, service level, forbidden nodes, carbon preference, split policy, confidence floor, and no mutation unless confirmed.

### 32. Agent-safe routing plans

**Justification:** AI assistance must not silently select routes, reserve capacity, or change rules.

**Improvement:** Require side-effect-free agent plans for route selection, capacity reservation, simulation, rule changes, approvals, exceptions, and feedback, naming permission, owned tables, idempotency key, expected event, risks, and human confirmation.

### 33. Document and instruction intake

**Justification:** Routing constraints arrive through customer instructions, carrier notices, regional restrictions, approval notes, and operational playbooks.

**Improvement:** Extract candidate constraints, node restrictions, service preferences, carbon requirements, split instructions, approval needs, and exception facts with confidence, evidence links, and governed mutation previews.

### 34. AppGen-X inbox reliability

**Justification:** Order, availability, and tax events are foundational inputs to routing decisions.

**Improvement:** Add inbox idempotency, schema-version checks, payload validation, retry evidence, unsupported-event rejection, projection rebuild, dead-letter promotion, and workbench replay/quarantine controls.

### 35. AppGen-X outbox delivery assurance

**Justification:** Fulfillment route and node-capacity events must reliably reach downstream execution and orchestration capabilities.

**Improvement:** Add outbox state, ordering group, payload hash, delivery attempts, next retry, delivery proof, dead-letter linkage, and replay controls for `FulfillmentRouteSelected` and `NodeCapacityReserved`.

### 36. Cross-PBC dependency boundary proof

**Justification:** Routing must not bypass composition by reading checkout, order, inventory, tax, transportation, WMS, DOM, approval, or feedback tables.

**Improvement:** Add release evidence scanning schema descriptors, services, routes, DSL, and agent plans for foreign table access, proving dependencies are only APIs, AppGen-X events, or package-local projections.

### 37. Routing federation view

**Justification:** Operations need one view of routing state across orders, nodes, capacity, promises, approvals, exceptions, and feedback.

**Improvement:** Build a federation projection with source lineage, freshness, authorization, version compatibility, projection lag, and drilldowns into each package-owned routing artifact.

### 38. Routing anomaly detection

**Justification:** Abnormal routing decisions may indicate bad data, model drift, capacity feed failures, or policy misconfiguration.

**Improvement:** Detect anomalies in route cost, split frequency, node selection, capacity consumption, promise failures, carbon cost, approval overrides, duplicate events, and feedback variance.

### 39. Stochastic exposure model

**Justification:** Routing risk spans delivery failure, cost overruns, capacity shortfalls, service penalties, carbon exposure, and customer dissatisfaction.

**Improvement:** Model exposure distributions by route, node, region, service level, channel, item class, and time bucket with mitigation recommendations and confidence intervals.

### 40. Governed optimization model evidence

**Justification:** Routing models influence customer promises, revenue, cost, capacity, and emissions.

**Improvement:** Track model purpose, training window, feature lineage, objective function, constraints, validation metrics, drift, fairness/service impact, approval, rollback, and explainability evidence.

### 41. Crypto-agile routing proof

**Justification:** High-value routing decisions may need proof of policy compliance without exposing costs or customer details.

**Improvement:** Generate selective-disclosure routing proofs with route hash, policy hash, timestamp, proof type, verifier, crypto epoch, key rotation evidence, expiry, and revocation.

### 42. Route audit trail time travel

**Justification:** Disputes require reconstructing what projections, constraints, costs, and approvals were visible at route decision time.

**Improvement:** Add temporal query support over routing plans, candidates, capacity snapshots, decisions, reservations, approvals, events, and policy versions using transaction, valid, and processing times.

### 43. Runtime parameter impact controls

**Justification:** Weights and thresholds directly change fulfillment decisions and customer promises.

**Improvement:** Add parameter bounds, impact simulation, approval workflow, effective dating, rollback, tenant/region overrides, and release evidence for cost, SLA, capacity, risk, carbon, split, forecast, and confidence parameters.

### 44. Schema extension governance

**Justification:** Routing implementations need custom node, carrier, region, item, and customer attributes without breaking package ownership.

**Improvement:** Allow extensions only on owned routing tables with field validation, migration preview, UI binding preview, API exposure review, and release-audit evidence.

### 45. Workbench coverage

**Justification:** Route operators need a full command center instead of scattered tables.

**Improvement:** Expand workbench surfaces for plans, legs, nodes, calendars, services, capacity, constraints, costs, promises, splits, inputs, candidates, decisions, reservations, simulations, optimizations, exceptions, approvals, feedback, events, rules, parameters, configuration, and release evidence.

### 46. Routing decision explanation UI

**Justification:** Users need to understand why a route was chosen, rejected, approved, or blocked.

**Improvement:** Add explainability panels showing candidate ranking, constraints, costs, SLA, capacity, inventory freshness, tax, carbon, risk, split rationale, approval status, and counterfactual alternatives.

### 47. Continuous routing control testing

**Justification:** Better-than-world-class routing proves controls continuously, not just in release tests.

**Improvement:** Add assertions for route without verified order, stale availability, stale tax, capacity over-reservation, blocked-node selection, split above max, missing approval, foreign-table access, dead-letter aging, and agent-preview bypass.

### 48. Routing resilience drills

**Justification:** Route selection must degrade safely when nodes, projections, optimization, or event delivery fail.

**Improvement:** Add drills for duplicate order event, stale availability, tax projection delay, node outage, optimization timeout, reservation conflict, outbox dead letter, and workbench degraded mode.

### 49. Order Routing readiness score

**Justification:** Users need an evidence-backed view of whether `order_routing_optimization` is ready to select fulfillment routes.

**Improvement:** Compute readiness from order/availability/tax inputs, node topology, capacity, candidates, constraints, cost and promise evidence, simulations, approvals, feedback, event reliability, UI coverage, model governance, controls, and agent safety.

### 50. End-to-end route selection proof

**Justification:** A complete Order Routing Optimization PBC must prove it can route an order through all controlled decision steps.

**Improvement:** Add an executable proof scenario covering `OrderVerified`, `AvailabilityProjected`, `TaxCalculated`, node readiness, capacity snapshot, route candidate intake, scoring, policy screening, split decision, approval if needed, capacity reservation, selected route event, workbench evidence, boundary proof, controls, and agent explanation.
