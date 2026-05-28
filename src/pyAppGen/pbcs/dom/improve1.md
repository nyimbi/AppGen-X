# Distributed Order Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `dom`. The items are specific to distributed order management: order capture, order lines, channel context, holds, verification, customer/tax/payment projections, fraud screening, pricing handoff, allocation orchestration, fulfillment planning, node selection, split shipments, backorders, substitutions, cancellations, shipment projections, order exceptions, promise forecasting, carbon-aware fulfillment, policy simulation, event reliability, UI workbenches, and agent-assisted order orchestration.

## Current Domain Evidence Used

- Domain purpose: order capture, verification, pricing handoff, tax and customer projection use, fraud screening, sourcing, allocation orchestration, fulfillment planning, shipment confirmation projection, exception handling, and order lifecycle visibility.
- Owned boundary: sales orders, order lines, statuses, notes, holds, promises, channel context, payment projections, customer projections, customer identity projections, tax projections, fraud screens and signals, order verification, price components, discount projections, inventory allocation projections, inventory node projections, payment authorization projections, fulfillment plans and lines, node candidates, reservation projections, split shipments, backorders, substitutions, cancellation requests, shipment projections, shipment-status projections, order exceptions, route selections, risk scores, promise demand forecasts, fulfillment policy simulations, route replay, verification proofs, policy screenings, audit traces, federation projections, carbon fulfillment, fulfillment optimization, node allocation, anomaly signals, fulfillment exposure models, parsed events, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: order capture, tax projection, fraud screening, verification, pricing, allocation, fulfillment plan creation, shipment projection, AppGen-X inbox handling, workbench, rules, parameters, schema extensions, runtime configuration, boundary checks, and release evidence.
- Existing events and dependencies: emits `OrderCaptured`, `TaxProjectionApplied`, `FraudScreened`, `OrderVerified`, `OrderPriced`, `InventoryAllocationProjected`, `FulfillmentPlanCreated`, and `OrderShipped`; consumes inventory, tax, customer, payment, and shipment events through declared APIs/projections only.

## 50 Better-Than-World-Class Improvements

### 1. Order capture readiness gate

**Justification:** Incomplete captured orders create downstream verification failures, allocation churn, fraud ambiguity, tax errors, and fulfillment exceptions.

**Improvement:** Add order readiness checks for customer projection freshness, channel, currency, destination, line completeness, requested service level, payment projection, tax readiness, fraud prerequisites, source references, and tenant/entity context. Orders that fail readiness should remain draft or held with clear remediation.

### 2. Channel context normalization

**Justification:** Marketplace, ecommerce, call center, EDI-style, subscription, store, and service-channel orders carry different promises, constraints, and references.

**Improvement:** Normalize channel context into governed fields for channel type, source system, order intent, customer promise, cutoff, marketplace rules, cancellation rights, return policy, service level, and source reference lineage. Verification and fulfillment planning should cite channel context.

### 3. Order line integrity engine

**Justification:** Line-level errors in item, quantity, UOM, service level, ship-to, bundle, customization, or eligibility drive costly order exceptions.

**Improvement:** Validate each order line for item projection eligibility, quantity/UOM, destination restrictions, promised service, bundle/component behavior, substitution allowance, tax readiness, fulfillment constraints, and cancellation/return policy. Store rejected-line reasons explicitly.

### 4. Order status state machine

**Justification:** DOM needs deterministic lifecycle transitions across capture, hold, verification, priced, allocated, planned, shipped, backordered, cancelled, and exception states.

**Improvement:** Implement a state machine with allowed transitions, command/event source, timestamp, actor, reason, idempotency key, rollback/compensation constraints, and UI-visible status history. Invalid transitions should fail with policy explanations.

### 5. Hold and release governance

**Justification:** Orders can be held for fraud, payment, customer status, tax readiness, inventory confidence, address issues, restricted goods, or manual review.

**Improvement:** Add typed holds with owner, severity, source, release criteria, SLA, expiry, override permission, downstream blocks, and audit evidence. Fulfillment planning should not proceed through blocking holds.

### 6. Customer projection confidence

**Justification:** DOM relies on customer facts without owning the customer master, so stale or incomplete projections are operational risk.

**Improvement:** Track projection freshness, source event id, customer status, identity confidence, address confidence, restrictions, credit/service eligibility, and privacy flags. Verification should warn or hold when customer projection confidence is below policy.

### 7. Customer identity reconciliation

**Justification:** Duplicate, ambiguous, or low-confidence customer identities affect fraud, tax, payment, loyalty, and fulfillment decisions.

**Improvement:** Add identity projection reconciliation with match confidence, competing identities, verified attributes, consent/privacy indicators, and decision impact. The agent should ask for human confirmation before merging or relying on ambiguous identity evidence.

### 8. Tax projection gating

**Justification:** Orders should not be verified or priced as complete when tax calculation is missing, stale, or incompatible with destination and line data.

**Improvement:** Add tax-ready gates for jurisdiction, address, taxable lines, exemption projection, tax amount, calculation timestamp, source event, and recalculation triggers. Emit tax projection evidence only through DOM-owned records.

### 9. Payment authorization projection handling

**Justification:** Payment authorization changes fulfillment eligibility, fraud posture, cancellation behavior, and release timing.

**Improvement:** Track authorization amount, currency, expiry, capture window, partial authorization, payment hold, source event id, stale status, and risk flags. Fulfillment plans should respect authorization validity and warn before expiry.

### 10. Fraud signal fusion

**Justification:** Fraud decisions require multiple signals: customer identity, payment, address mismatch, velocity, device/channel hints, high-risk goods, and fulfillment route.

**Improvement:** Fuse fraud signals into explainable screens with score, reason codes, confidence, source projection freshness, review queue, decision evidence, and downstream hold/release actions. Avoid opaque auto-rejection for low-confidence cases.

### 11. Fraud review workflow

**Justification:** Manual fraud review must be fast, fair, auditable, and connected to order release or cancellation.

**Improvement:** Add review states, analyst notes, requested evidence, customer contact outcome, escalation, decision reason, policy version, and release/cancel event effects. UI should show why the order is blocked and what action resolves it.

### 12. Order verification proof

**Justification:** Verification is the key control that an order is valid enough to continue orchestration.

**Improvement:** Generate a verification proof containing customer, tax, payment, line, fraud, channel, policy, and status checks with pass/fail evidence, projection versions, and hash. Emit `OrderVerified` only when all required gates pass or approved exceptions are present.

### 13. Price component trace

**Justification:** DOM must show price, discount, surcharge, tax handoff, and channel promotions without owning every upstream pricing source.

**Improvement:** Store price components with source projection, line/order scope, currency, effective date, discount eligibility, override reason, rounding, and event lineage. `OrderPriced` should include a traceable component summary.

### 14. Discount and promotion projection governance

**Justification:** Promotions can conflict with channel rules, customer eligibility, margin thresholds, and fulfillment constraints.

**Improvement:** Track discount projection source, eligibility, exclusions, stacking rules, margin impact, expiry, and stale status. Hold pricing when projection evidence contradicts order line or channel context.

### 15. Allocation confidence model

**Justification:** Allocation projections from inventory may be uncertain because of reservations, holds, in-transit stock, node capacity, or stale events.

**Improvement:** Store allocation confidence by line, node, lot/serial where applicable, reservation, freshness, and risk. Fulfillment planning should distinguish hard allocation, soft promise, and tentative availability.

### 16. Inventory node candidate scoring

**Justification:** Fulfillment node choice drives cost, speed, carbon, customer promise, split shipments, and stockout risk.

**Improvement:** Score node candidates by allocation confidence, distance, service level, capacity, cutoff, carrier availability projection, margin, carbon, risk, inventory freshness, and channel policy. Explain rejected nodes.

### 17. Fulfillment policy compiler

**Justification:** Fulfillment decisions combine many policies: sourcing priority, split eligibility, substitutions, backorders, cancellation, service level, margin, and customer promise.

**Improvement:** Compile fulfillment rules into deterministic policy versions with eligibility checks, ranking formulas, override routes, and simulation support. Fulfillment plans should cite the policy hash.

### 18. Split shipment governance

**Justification:** Split shipments can save promises but increase freight cost, carbon, customer friction, and exception risk.

**Improvement:** Add split shipment rules for maximum splits, line compatibility, customer/channel permission, cost threshold, service promise, carbon impact, packaging constraints, and approval requirements. UI should show split tradeoffs before confirmation.

### 19. Backorder lifecycle

**Justification:** Backorders require active management, customer visibility, allocation refresh, cancellation rules, and promise updates.

**Improvement:** Model backorder states, reason, expected supply projection, refresh cadence, customer notification projection, cancellation eligibility, partial release, substitution offers, and aging escalation. Backorders should not be passive notes.

### 20. Substitution eligibility engine

**Justification:** Substitutions can satisfy demand but may violate customer preference, product compatibility, compliance, margin, or channel rules.

**Improvement:** Add substitution eligibility with equivalent items, customer/channel consent, price impact, tax impact, fulfillment feasibility, risk, and approval path. The order workbench should show why each substitute is accepted or rejected.

### 21. Cancellation request workflow

**Justification:** Cancellation depends on order status, payment authorization, allocation, fulfillment progress, shipment state, customer rights, and channel policy.

**Improvement:** Add cancellation request states, eligibility checks, line/partial cancellation, reversal events, refund/payment projection requirements, fulfillment stop signal, reason codes, and customer-impact evidence.

### 22. Promise date governance

**Justification:** Promise dates are customer-facing commitments built from inventory, node, carrier, calendar, and policy assumptions.

**Improvement:** Store promise date derivation with allocation, node, cutoff, service level, route projection, calendar, uncertainty, and customer/channel terms. Recalculate and explain promise changes when projections update.

### 23. Demand and promise forecasting

**Justification:** DOM should anticipate promise pressure, not only react after allocation fails.

**Improvement:** Forecast demand and promise risk by channel, item, node, region, service level, promotion, and seasonality. Use forecasts to warn about future backorders, split pressure, and fulfillment exposure.

### 24. Fulfillment plan lifecycle

**Justification:** Fulfillment plans evolve as allocation, payment, customer, shipment, and inventory projections change.

**Improvement:** Model plan states from proposed to committed, partially released, replanned, shipped, failed, cancelled, and closed. Store plan line dependencies, node candidate evidence, reservation projection, route selection, and replan reason.

### 25. Route selection replay

**Justification:** DOM decisions must be reconstructable when routing, node selection, or shipment projection changes.

**Improvement:** Add route replay that rebuilds fulfillment decisions from the same projections and policy versions, showing deterministic versus changed outcomes. Use replay for audits, model drift, and exception diagnosis.

### 26. Shipment projection reconciliation

**Justification:** DOM does not own transportation state but must understand shipment progress and customer impact.

**Improvement:** Reconcile `ShipmentDelivered` and shipment status projections to order lines, split shipments, promises, exceptions, and close criteria. Flag delivered-with-exception, partial delivery, stale status, and missing proof.

### 27. Order exception taxonomy

**Justification:** Generic exceptions hide root causes and make automation unsafe.

**Improvement:** Define order exceptions for missing projection, failed verification, fraud review, payment expiry, tax mismatch, allocation gap, node infeasible, split rejected, backorder aging, substitution conflict, cancellation conflict, shipment delay, and delivery discrepancy. Each should define owner, SLA, severity, recovery action, and closure evidence.

### 28. Exception resolution recommender

**Justification:** Order orchestration teams need recommended next actions that are safe and explainable.

**Improvement:** Generate recommendations such as refresh projection, release hold, reprice, request payment reauthorization, reallocate, split, substitute, backorder, cancel, or escalate. Each recommendation should show confidence, risk, event effects, and required permission.

### 29. Order anomaly detection

**Justification:** Unusual order behavior can indicate fraud, integration defects, pricing errors, abuse, or operational failure.

**Improvement:** Detect anomalies in order velocity, line mix, price components, repeated cancellations, projection churn, allocation failures, status loops, manual overrides, and channel patterns. Route anomalies to review with non-accusatory explanations.

### 30. Stochastic fulfillment exposure

**Justification:** Order risk is probabilistic across fraud, payment, allocation, fulfillment, shipment, cancellation, and delivery.

**Improvement:** Model fulfillment exposure distributions by order, line, channel, node, region, service level, and customer segment. Surface likely cost, promise, cancellation, and exception exposure with mitigation options.

### 31. Carbon-aware fulfillment planning

**Justification:** Order fulfillment choices affect distance, packaging, split shipments, carrier mode, inventory positioning, and returns risk.

**Improvement:** Add carbon metrics to node selection, split decisions, backorder/substitution options, and route selection. Show service-cost-carbon tradeoffs rather than silently optimizing emissions.

### 32. Fulfillment optimization with constraints

**Justification:** DOM must optimize across customer promise, availability, margin, cost, carbon, risk, channel policy, and operational capacity.

**Improvement:** Implement optimization with hard constraints, soft preferences, sensitivity analysis, fallback plans, and explanation. Users should see why a plan is best and which constraint is binding.

### 33. Mechanism-design allocation across channels

**Justification:** Scarce inventory allocation can unfairly favor one channel, customer type, or region if the mechanism is hidden.

**Improvement:** Add allocation mechanisms for fairness, service priority, margin, customer tier, contractual commitments, emergency demand, and channel protection. Simulate allocation outcomes and explain tradeoffs.

### 34. Order federation without shared tables

**Justification:** DOM composes with commerce, customer, tax, payment, inventory, WMS, transportation, finance, and audit packages but must not read their tables.

**Improvement:** Add federation projections with freshness and boundary evidence for all external facts. Static and runtime checks should reject direct foreign-table access and prove projection-only dependencies.

### 35. AppGen-X event reliability cockpit

**Justification:** DOM decisions depend on consumed inventory, tax, customer, payment, and shipment events and emitted order lifecycle events.

**Improvement:** Add inbox/outbox/dead-letter panels with idempotency keys, duplicates, retry schedule, handler version, payload lineage, projection freshness, replay eligibility, and downstream event effects. Warn users when stale projections affect decisions.

### 36. Order audit trace and hash chain

**Justification:** Orders require reconstruction across customer-facing, financial, fraud, fulfillment, and shipment decisions.

**Improvement:** Hash-chain capture, projection updates, fraud screens, verification, pricing, allocation, plans, holds, exceptions, cancellations, shipment projection, agent previews, and emitted events. UI timelines should support temporal audit.

### 37. Zero-knowledge order verification proof

**Justification:** Internal or external parties may need proof that an order passed controls without seeing customer, payment, or fraud details.

**Improvement:** Generate cryptographic verification proofs for required order controls and projection freshness. Provide verification APIs that prove pass/fail status and timestamp while redacting protected payload fields.

### 38. Dynamic order policy screening

**Justification:** Order acceptance and fulfillment depend on policies for channel, customer, goods, destination, payment, fraud, tax, and fulfillment risk.

**Improvement:** Screen capture, verify, price, allocate, plan, cancel, ship projection, and exception closure actions. Store policy version, attributes evaluated, decision, explanation, and override path.

### 39. Rule and parameter simulation

**Justification:** Fraud thresholds, split limits, allocation confidence, partial fulfillment, promise horizon, and exception SLAs materially alter order behavior.

**Improvement:** Simulate rule and parameter changes against historical and active orders, showing conversion, holds, fraud reviews, allocation gaps, split shipments, backorders, cancellations, carbon, exceptions, and dead-letter volume.

### 40. Order MLOps governance

**Justification:** Fraud, cancellation, allocation confidence, promise risk, and anomaly models influence customer outcomes and operational fairness.

**Improvement:** Add model registry, feature lineage, training windows, approval status, explainability, drift monitoring, fairness checks, rollback, and release evidence for every model used in order decisions.

### 41. Multi-channel and tenant isolation

**Justification:** DOM handles sensitive customer, payment projection, fraud, price, and fulfillment data across tenants, entities, brands, and channels.

**Improvement:** Enforce isolation in orders, projections, plans, exceptions, events, UI filters, saved views, and agent previews. Release evidence should prove no cross-tenant projection leakage.

### 42. Order workbench coverage

**Justification:** Operations teams need full UI access to the order orchestration surface, not hidden backend commands.

**Improvement:** Expand UI into capture queue, validation board, projection freshness, fraud review, verification proof, pricing trace, allocation board, fulfillment planner, split/backorder/substitution console, cancellation queue, shipment projection, exceptions, simulations, controls, rules, parameters, configuration, event reliability, and agent panels.

### 43. Agent-safe order document intake

**Justification:** The DOM chatbot should parse customer instructions, order imports, marketplace messages, cancellation notes, and exception documents without unsafe writes.

**Improvement:** Add intake skills that extract candidate order facts, map them to DOM-owned tables, validate permissions/rules/projections, reject foreign-table mutations, and produce side-effect-free previews with confidence, risks, confirmations, and expected AppGen-X events.

### 44. Agent-safe orchestration planning

**Justification:** AI can help resolve order problems only if it respects state, projection freshness, and human confirmation gates.

**Improvement:** Require agent plans for verify, price, allocate, fulfill, split, substitute, backorder, cancel, and exception closure to list command, permission, owned tables, idempotency key, emitted event, affected lines, rollback limits, customer impact, and human approval.

### 45. Customer communication readiness

**Justification:** DOM decisions often require customer-facing communication, but the PBC must separate orchestration from external messaging ownership.

**Improvement:** Generate communication-ready evidence for promise changes, backorders, substitutions, cancellations, fraud review, and delivery exceptions with approved facts, confidence, and channel constraints. Emit or expose this as a projection, not direct foreign messaging table writes.

### 46. Chaos-engineered orchestration tolerance

**Justification:** Order orchestration must survive missing projections, duplicate events, stale payments, failed tax calculations, delayed inventory allocation, and shipment event replay.

**Improvement:** Add resilience drills for projection outage, duplicate event, dead-letter replay, payment expiry, tax delay, allocation reversal, fulfillment replan, and shipment correction. Store drill evidence in release gates.

### 47. Continuous order control testing

**Justification:** Controls should run continuously across capture, verification, pricing, allocation, fulfillment, cancellation, shipment projection, and event handling.

**Improvement:** Add assertions for unverified fulfillment, stale tax projection, expired payment authorization, fraud hold bypass, invalid status transition, over-split order, unapproved substitution, unauthorized cancellation, dead-letter aging, and agent-preview bypass.

### 48. Order close and lifecycle completeness

**Justification:** Orders should close only when all lines, payments, shipments, exceptions, cancellations, and projections reconcile to a final state.

**Improvement:** Add close criteria for shipped/delivered lines, cancelled lines, backorder resolution, payment projection status, shipment projection, open exceptions, emitted events, and audit trace completeness. Workbench should surface orders stuck before close.

### 49. DOM readiness score

**Justification:** Users need an evidence-backed view of whether DOM is ready for production order orchestration.

**Improvement:** Compute readiness from channel setup, status policies, projection freshness, fraud controls, verification proof, price trace, allocation confidence, fulfillment rules, exception workflows, UI coverage, event reliability, boundary proof, control assertions, model governance, and agent safety.

### 50. End-to-end order orchestration proof

**Justification:** A complete DOM PBC must prove it can coordinate the full order lifecycle while respecting package boundaries.

**Improvement:** Add an executable proof scenario covering order capture, customer/tax/payment projections, fraud screen, verification proof, pricing, inventory allocation projection, fulfillment plan, split/backorder decision where applicable, shipment projection, emitted `OrderShipped`, audit trace, UI evidence, controls, and agent explanation.
