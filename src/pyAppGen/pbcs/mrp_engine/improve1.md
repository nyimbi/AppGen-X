# Material Requirements Planning Engine PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `mrp_engine`. The items are specific to material requirements planning: BOMs, revisions, components, alternates, substitutions, item planning profiles, source rules, demand projections, forecasts, sales-order demand, inventory and lot projections, reservations, quality holds, capacity projections, MRP runs, scenarios, plan versions, planned orders, planned purchase suggestions, planned production orders, transfers, shortages, pegging, exceptions, release routes, policy screening, planning proofs, event reliability, UI workbenches, and agent-assisted planning operations.

## Current Domain Evidence Used

- Domain purpose: package-local planning graph that turns demand, supply projections, bill-of-material structure, site policy, capacity signals, lead times, lot sizing, safety stock, scrap, yield, and release rules into executable planned production orders and planned purchase suggestions.
- Owned boundary: BOMs, revisions, components, alternates, substitution rules, item planning profiles, source rules, material demand, demand lines, forecast snapshots, sales-order demand projections, safety stock policies, inventory/lot/reservation projections, quality hold projections, capacity projections and buckets, work-center and production capacity projections, supplier lead-time projections, MRP runs, run items and buckets, scenarios, plan versions, planned orders and components, purchase suggestions, production orders, transfer orders, shortages, shortage pegging, supply-demand pegging, planning exceptions, resolution plans, release routes, policy screening, audit traces, supply proofs, federation projections, carbon planning windows, allocation optimization, capacity allocation, anomaly signals, risk models, shortage forecasts, parsed instructions, seed data, schema extensions, controls, governed models, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: configuration, rules, parameters, schema extensions, event handling, BOM registration, demand and inventory projection ingestion, run creation/calculation, BOM explosion, material plan calculation, planned-order release, supply routing, proofs, screening, federation, identity checks, resilience drills, crypto epochs, carbon batching, allocation optimization, controls, governed models, workbench, simulations, forecasts, parsing, risk scoring, exceptions, anomaly detection, stochastic exposure, and boundary verification.
- Existing events and dependencies: emits `BomRegistered`, `DemandProjectionIngested`, `InventoryProjectionIngested`, `MrpRunStarted`, `MaterialShortageDetected`, and `PlannedOrderReleased`; consumes inventory, order, forecast, production capacity, quality hold, and supplier lead-time events through declared APIs/projections only.

## 50 Better-Than-World-Class Improvements

### 1. BOM master readiness gate

**Justification:** MRP output is only as good as BOM structure, component quantities, units, sites, scrap, yield, and release state.

**Improvement:** Add BOM readiness checks for parent item, site, revision, component completeness, UOM consistency, scrap/yield, alternate links, lifecycle status, and approval. Block planning against unapproved or incomplete BOMs.

### 2. BOM revision effectivity control

**Justification:** Engineering changes and date/lot/serial effectivity can alter requirements materially.

**Improvement:** Model revision effectivity by date, site, lot/serial range, product configuration, approval state, and supersession. MRP runs should cite the revision snapshot used for every explosion.

### 3. BOM component quantity governance

**Justification:** Component quantities, scrap, phantom behavior, and yield assumptions drive shortage and planned order quantities.

**Improvement:** Add component-level UOM, quantity basis, scrap percent, yield, phantom flag, rounding, optionality, and effective dates. Explosion traces should show every quantity transformation.

### 4. Alternate BOM and routing selection

**Justification:** Alternative structures can mitigate shortages, capacity constraints, or site-specific production rules.

**Improvement:** Add alternate BOM selection policies by site, demand type, capacity, component availability, cost, quality hold, and approval. Simulate alternate selection before changing active planning rules.

### 5. Substitution rule engine

**Justification:** Substitutes can resolve shortages but may violate quality, regulatory, customer, or engineering rules.

**Improvement:** Model substitutions with eligibility, priority, equivalence quantity, site/channel/customer restrictions, quality status, expiry, and approval. Shortage recommendations should explain substitute acceptance or rejection.

### 6. Item planning profile completeness

**Justification:** Lead time, lot sizing, safety stock, sourcing method, make/buy, and planning fence settings determine correct MRP behavior.

**Improvement:** Add profile readiness checks for make/buy, source rule, lead time, lot-size policy, min/max, safety stock, scrap factor, planning fence, time bucket, and planner ownership.

### 7. Source rule governance

**Justification:** Planned orders must know whether to buy, make, transfer, subcontract, or defer.

**Improvement:** Define source rules by item, site, supplier/source site, effective dates, capacity, lead time, minimum quantity, priority, cost, and release route. Planned order release should cite source rule evidence.

### 8. Demand projection normalization

**Justification:** Forecasts, verified orders, dependent demand, and manual planning demand have different priority and reliability.

**Improvement:** Normalize demand with source type, item, site, quantity, due date, priority, confidence, consumption policy, event lineage, and stale status. MRP should preserve source demand identity for pegging.

### 9. Forecast snapshot versioning

**Justification:** Forecast changes can swing planned supply and must be reproducible.

**Improvement:** Store forecast snapshots with version, horizon, bucket, model/source, confidence, override reason, and supersession. Scenario runs should compare forecast versions.

### 10. Sales-order demand pegging

**Justification:** Planners need to know which customer or order demand drives each shortage or planned order without reading order tables.

**Improvement:** Store sales-order demand projections with source event, due date, priority, promised date, quantity, and projection freshness. Peg planned supply and shortages back to these projections.

### 11. Inventory projection freshness

**Justification:** MRP should not rely on stale or incomplete inventory availability.

**Improvement:** Track inventory projection source, position timestamp, available quantity, reservations, in-transit, quality holds, confidence, and freshness. Warn or hold runs when critical projections are stale.

### 12. Lot and reservation-aware planning

**Justification:** Lots, reservations, expiry, and holds materially change usable supply.

**Improvement:** Include lot attributes, expiry, reservation status, hold state, FEFO policy, and allocation confidence in supply netting. Planned orders should not consume projected supply that is not planning-eligible.

### 13. Quality hold projection integration

**Justification:** Quality holds can make apparent inventory unusable for planning.

**Improvement:** Project quality holds with affected item/site/lot, status, release confidence, expected release date, and reason. Planning should include conditional supply only when policy allows.

### 14. Capacity bucket modeling

**Justification:** Material plans that ignore capacity create infeasible production orders.

**Improvement:** Model capacity buckets by work center/site/date, available hours, constraints, load, downtime projection, confidence, and bottleneck status. Planned production orders should show capacity feasibility.

### 15. Supplier lead-time projection governance

**Justification:** Purchase suggestions depend on supplier lead times that vary by item, site, season, risk, and performance.

**Improvement:** Store supplier lead-time projection with source, confidence, minimum/expected/worst-case days, supplier/source rule, validity, and risk. Purchase suggestions should include lead-time confidence.

### 16. Planning horizon and time bucket strategy

**Justification:** Horizon and bucket size affect nervousness, performance, and decision quality.

**Improvement:** Add horizon/bucket policies by item class, site, demand type, and planner. Simulate changes to show shortage, planned-order count, and release workload impact.

### 17. MRP run lifecycle state machine

**Justification:** Planning runs need controlled states for draft, queued, running, calculated, reviewed, partially released, released, superseded, and archived.

**Improvement:** Add run transitions with planner, scenario, input snapshot hashes, rule/parameter versions, start/end time, exception count, approval state, and audit trace.

### 18. Input snapshot freeze

**Justification:** Reproducible planning requires freezing demand, supply, BOM, capacity, and policy inputs at run start.

**Improvement:** Create immutable run snapshots for BOM revisions, demand, inventory, reservations, quality holds, capacity, lead times, rules, and parameters. Recalculation should create a new plan version.

### 19. Multi-scenario planning

**Justification:** Planners need compare-and-choose behavior for demand upside, supplier delay, capacity outage, and policy changes.

**Improvement:** Add scenarios with input deltas, assumptions, owner, status, comparison metrics, and recommended action. Workbench should compare shortages, supply orders, capacity load, cost, and carbon.

### 20. Plan version control

**Justification:** Plans evolve as inputs change, but decisions must remain traceable.

**Improvement:** Version MRP plans with parent run, scenario, input snapshots, calculation algorithm, changed orders, supersession, and release status. Pegging and approvals should reference plan version.

### 21. Supply and demand netting trace

**Justification:** Planners need to explain why MRP created or did not create supply.

**Improvement:** Store netting traces by item/site/bucket showing gross demand, on-hand projection, reservations, scheduled receipts, planned receipts, safety stock, lot size, shortage, and recommended supply.

### 22. Safety stock policy intelligence

**Justification:** Safety stock can protect service or create excess; MRP should make its effect explicit.

**Improvement:** Model safety stock by item/site/bucket, demand variability, service level, lead-time variability, seasonality, and override reason. Show shortages caused solely by safety-stock policy.

### 23. Lot-sizing and rounding engine

**Justification:** Minimum, maximum, fixed, multiple, economic, and supplier pack quantities strongly affect planned order quantities.

**Improvement:** Add lot-sizing policies with minimum, maximum, multiple, fixed order quantity, rounding, source constraints, and cost impact. Planned order traces should show lot-size transformations.

### 24. Planned purchase suggestion lifecycle

**Justification:** Purchase suggestions need review, consolidation, supplier/source rule, release route, and exception handling.

**Improvement:** Model suggestion states, item/site, supplier/source, quantity, due date, lead time, pegged demand, approval, consolidation group, and release evidence to procurement.

### 25. Planned production order lifecycle

**Justification:** Production suggestions must be feasible by BOM, capacity, routing, and material availability.

**Improvement:** Model planned production orders with parent item, site, quantity, start/due date, BOM revision, component requirements, capacity feasibility, release route, and production handoff evidence.

### 26. Planned transfer order lifecycle

**Justification:** Transfers can resolve shortages across sites but affect inventory, transportation, and service constraints.

**Improvement:** Add transfer suggestions with source site, destination site, transit lead time, availability confidence, transportation projection, carbon impact, and release route. Respect site policies and reservations.

### 27. Shortage severity model

**Justification:** Not all shortages are equal; severity depends on due date, demand priority, customer impact, substitute availability, and lead-time risk.

**Improvement:** Score shortages with quantity, days late, demand priority, pegged orders, substitute options, capacity risk, supplier lead time, and customer/service impact. Workbench should rank shortage resolution.

### 28. Pegging graph explorer

**Justification:** Planners must navigate from demand to components, supply, shortages, and release actions.

**Improvement:** Build pegging graph views for demand, BOM levels, supply projections, planned orders, shortages, reservations, and release routes. Support upstream/downstream trace by plan version.

### 29. Exception resolution planning

**Justification:** Shortages, capacity overloads, quality holds, stale projections, and source gaps need actionable resolution plans.

**Improvement:** Generate resolution plans with option type, impacted demand, feasibility, cost, risk, lead time, policy requirements, owner, and expected event effects. Require approval for high-impact actions.

### 30. Planned order release governance

**Justification:** Releasing planned orders creates downstream procurement or production commitments.

**Improvement:** Validate release route, source rule, approval threshold, pegging, quantity, due date, capacity/material feasibility, and stale input status. Emit `PlannedOrderReleased` with idempotent evidence.

### 31. Release route resilience

**Justification:** Procurement and production routes can fail or be temporarily unavailable.

**Improvement:** Add release route health, fallback path, retry policy, dead-letter linkage, and requeue logic. Workbench should show route failures and safe replay options.

### 32. Planning policy screening

**Justification:** MRP must enforce restricted sites, blocked runs, item status, sourcing policy, quality holds, and approval thresholds.

**Improvement:** Screen BOM registration, projection ingestion, run creation, calculation, planned-order release, and exception closure. Store policy version, attributes evaluated, decision, explanation, and override path.

### 33. Material risk forecasting

**Justification:** Shortage risk can be anticipated before demand becomes late.

**Improvement:** Forecast shortage probability by item/site/bucket using demand variability, supplier lead time, inventory confidence, quality holds, capacity, and historical plan stability. Provide mitigation and confidence.

### 34. Capacity allocation mechanism

**Justification:** Scarce capacity must be allocated across items, demand priorities, customers, and sites transparently.

**Improvement:** Add capacity allocation policies for priority, due date, margin/service class, fairness, setup efficiency, and contractual demand. Simulate outcomes before activation.

### 35. Material allocation optimization

**Justification:** Limited supply should be allocated to maximize service while respecting rules and commitments.

**Improvement:** Optimize material allocation across pegged demands, planned orders, substitutions, transfers, and safety stock with explainable constraints and sensitivity analysis.

### 36. Carbon-aware planning windows

**Justification:** Non-urgent planning batches and release timing can account for energy and logistics emissions.

**Improvement:** Add carbon planning windows for batch runs, release timing, transfer choices, and production suggestions. Show cost/service/carbon tradeoffs rather than silently delaying supply.

### 37. Supply availability proof

**Justification:** Planners and downstream consumers may need proof of projected supply without exposing all inventory or supplier details.

**Improvement:** Generate redacted proofs for availability, shortage, pegging, input freshness, and planned supply with hash, plan version, and verification API.

### 38. Immutable planning audit trace

**Justification:** MRP decisions affect procurement, production, customer promises, and cash.

**Improvement:** Hash-chain BOM changes, projection ingestion, run snapshots, netting, planned orders, shortages, exceptions, releases, agent previews, and event handling. Support temporal reconstruction.

### 39. AppGen-X event reliability cockpit

**Justification:** MRP depends on consumed inventory, order, forecast, capacity, quality, and supplier events and emitted planning events.

**Improvement:** Add inbox/outbox/dead-letter views for idempotency, duplicates, retries, handler version, payload lineage, projection freshness, replay eligibility, and downstream release effects.

### 40. Boundary proof for MRP ownership

**Justification:** MRP must compose with inventory, order, forecast, procurement, production, quality, supplier, and audit packages without shared tables.

**Improvement:** Add static/runtime checks proving commands touch only MRP-owned tables plus AppGen-X runtime tables. Include failing fixtures for direct inventory balance, customer order, supplier, production, quality, and audit table access.

### 41. MRP workbench coverage

**Justification:** Planners need the full planning surface, not hidden backend commands.

**Improvement:** Expand UI into BOM explorer, revision control, demand console, forecast snapshots, inventory projections, capacity board, run control, scenario comparison, shortage board, pegging graph, planned order board, release queue, exception resolution, rules, parameters, configuration, events, and agent panels.

### 42. Agent-safe planning instruction intake

**Justification:** The MRP chatbot should parse planning notes, BOM change requests, demand overrides, and shortage instructions without unsafe writes.

**Improvement:** Add intake skills that extract candidate planning facts, map them to owned MRP tables, validate rules/permissions/projections, reject foreign-table mutations, and produce side-effect-free previews with confidence, risks, approvals, and expected AppGen-X events.

### 43. Agent-safe release and exception planning

**Justification:** AI planning actions can create supply commitments and must be human-governed.

**Improvement:** Require agent plans for BOM registration, projection ingestion, run calculation, planned-order release, substitution, transfer, and exception closure to list command, permission, owned tables, idempotency key, emitted event, affected demand, rollback limits, and human approval.

### 44. Counterfactual planning-policy simulation

**Justification:** Changing safety stock, lead time, lot size, capacity threshold, or release rules can materially change supply commitments.

**Improvement:** Simulate parameter and rule changes against historical and active runs, showing shortages, planned orders, inventory exposure, capacity load, release volume, carbon, and dead-letter volume.

### 45. Semantic BOM and demand parsing

**Justification:** Planners often receive BOM notes, demand changes, supplier updates, and expedite instructions in unstructured form.

**Improvement:** Parse instructions into candidate BOM components, demand deltas, lead-time updates, substitution proposals, and exception notes with confidence, validation results, and reviewer approval.

### 46. Shortage anomaly detection

**Justification:** Sudden or unusual shortages may indicate bad projections, BOM errors, supplier disruption, or demand spikes.

**Improvement:** Detect anomalies in demand changes, component usage, lead time, inventory projection drops, quality holds, capacity changes, and release failures. Route findings to planners with explanations.

### 47. Planning MLOps governance

**Justification:** Shortage, forecast, risk, anomaly, and optimization models influence supply commitments.

**Improvement:** Add model registry, feature lineage, training windows, approval status, drift monitoring, explainability, fairness/coverage checks, rollback, and release evidence for every planning model.

### 48. Continuous MRP control testing

**Justification:** Planning controls should run continuously across BOMs, projections, runs, netting, releases, and events.

**Improvement:** Add assertions for inactive BOM planning, stale inventory projections, negative component demand, lot-size violations, release without pegging, blocked quality supply use, dead-letter aging, direct foreign-table access, and agent-preview bypass.

### 49. MRP readiness score

**Justification:** Users need an evidence-backed view of whether MRP is ready for production planning.

**Improvement:** Compute readiness from BOM completeness, planning profiles, demand projections, inventory freshness, capacity coverage, source rules, parameter validation, event reliability, UI coverage, boundary proof, controls, model governance, and agent safety.

### 50. End-to-end material plan proof

**Justification:** A complete MRP PBC must prove it can convert demand and supply projections into governed planned orders.

**Improvement:** Add an executable proof scenario covering BOM registration, demand projection ingestion, inventory projection ingestion, capacity projection, MRP run, BOM explosion, netting, shortage detection, pegging, planned purchase and production suggestions, release route, emitted events, UI evidence, controls, and agent explanation.
