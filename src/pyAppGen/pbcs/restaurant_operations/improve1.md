# Restaurant Operations Improvement Backlog

## Current Domain Evidence Used

- PBC key: `restaurant_operations`
- Manifest description: menus, recipes, kitchen production, reservations, food cost, labor, waste, and service execution
- Current owned tables: `menu_item`, `recipe`, `kitchen_ticket`, `reservation`, `inventory_prep`, `food_waste`, `labor_shift`
- Current APIs: `POST /menu-items`, `POST /recipes`, `POST /kitchen-tickets`, `POST /reservations`, `POST /inventory-preps`, `GET /restaurant-operations-workbench`
- Current UI fragments: `RestaurantOperationsWorkbench`, `RestaurantOperationsDetail`, `RestaurantOperationsAssistantPanel`
- Current emitted events: `RestaurantOperationsCreated`, `RestaurantOperationsUpdated`, `RestaurantOperationsApproved`, `RestaurantOperationsExceptionOpened`
- Current consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`

### 1. Menu lifecycle by store and daypart
**Justification:** Restaurants do not operate one global menu. Breakfast, lunch, dinner, late night, holiday, and site-specific availability must be explicit or operators will hide critical business rules in notes and workarounds.

**Improvement:** Add a canonical menu lifecycle that separates concept approval from store rollout. A menu item should carry draft, test kitchen, approved, scheduled, active, suspended, and retired states with effective windows by site, channel, and daypart.

**Acceptance evidence:** Store and daypart activation tests, a workbench timeline that shows future activations, and release evidence proving scheduled menu changes publish without editing recipe history.

### 2. Menu version sets and rollback
**Justification:** Operators need to roll a whole menu set forward or backward when pricing, supplier availability, or promotion plans change close to service.

**Improvement:** Introduce menu version sets that group items, prices, modifier rules, and availability into one reversible deployment unit per site or brand. Support preview and atomic rollback for a failed rollout.

**Acceptance evidence:** Version-set diff views, rollback integration tests, and evidence that an aborted deployment restores the prior active menu without orphaning kitchen or reservation references.

### 3. Modifier group modeling
**Justification:** Restaurant orders break down when modifier logic is shallow. Required sides, optional add-ons, substitutions, half-and-half choices, and nested preparation instructions all affect kitchen execution and check accuracy.

**Improvement:** Model modifier groups with min and max selection rules, nesting, default values, price deltas, allergen implications, and channel-specific visibility. Keep the kitchen-facing instruction separate from the guest-facing label.

**Acceptance evidence:** Contract tests for required and nested modifiers, UI validation for over-selection, and kitchen ticket evidence showing clean modifier rendering with no free-text ambiguity.

### 4. Allergen and dietary labeling on menus
**Justification:** Menu data is unsafe if dietary claims are only descriptive text. Guests and staff need structured allergen, vegan, halal, gluten-free, and spicy metadata that follows the item through ordering and preparation.

**Improvement:** Attach structured dietary flags, allergen declarations, and caution notes to menu items and modifiers. Track whether the claim is recipe-derived, manually attested, or blocked because of cross-contact risk.

**Acceptance evidence:** Validation tests for missing allergen declarations, workbench badges for dietary claims, and audit evidence showing who approved or changed each guest-facing label.

### 5. Recipe versioning and yield control
**Justification:** A menu item is not operationally real unless its recipe version, yield, and portion assumptions are stable enough to drive prep, depletion, and food cost.

**Improvement:** Add recipe versioning with effective dates, target yield, portion size, unit conversions, prep method notes, and store overrides. Lock historical orders and waste records to the exact recipe version used at service time.

**Acceptance evidence:** Recipe version history tests, yield recalculation fixtures, and release evidence proving historical tickets remain reproducible after a recipe amendment.

### 6. Recipe-to-menu binding rules
**Justification:** One menu item may depend on multiple recipes or prep components, and one recipe may support multiple menu items. That relationship needs explicit governance or substitutions and food cost will drift.

**Improvement:** Support recipe bundles and optional prep components per menu item, including plating-only items, shared sauces, and seasonal garnishes. Enforce validation so an active menu item cannot point to incomplete or expired recipe dependencies.

**Acceptance evidence:** Referential integrity tests between `menu_item` and `recipe`, dependency warnings in the workbench, and scenario evidence for activating a menu item with one missing prep component.

### 7. Prep list generation from forecast and reservations
**Justification:** Prep should reflect expected covers and order mix, not yesterday's intuition. Reservations, walk-in patterns, and delivery surges must feed prep decisions before service begins.

**Improvement:** Generate prep recommendations from reservation covers, historical mix, channel weighting, and current menu availability. Separate suggested prep from approved prep so operators can tune batches before committing.

**Acceptance evidence:** Prep suggestion traces, scenario tests for quiet and peak periods, and UI evidence showing how reservation changes revise recommended prep quantities.

### 8. Batch prep traceability and hold times
**Justification:** Prep batches are where food safety, waste, and throughput meet. The system must know when a batch was made, by whom, how much remains, and when it must be discarded.

**Improvement:** Extend `inventory_prep` to capture batch identifier, production time, expiration time, holding method, station assignment, and discard reason. Make prep batches first-class dependencies for kitchen tickets and waste events.

**Acceptance evidence:** Batch traceability tests, hold-time countdowns in the UI, and evidence that an expired batch blocks new ticket allocation until replaced or formally overridden.

### 9. Mise en place readiness checks
**Justification:** Service quality degrades before the first order if stations are missing prep, tools, labels, or allergen controls. Pre-service readiness is operational data, not a paper checklist.

**Improvement:** Add station readiness workflows that confirm required prep, utensils, labels, and sanitizer status before a shift or daypart opens. Allow site-specific readiness templates by concept and menu complexity.

**Acceptance evidence:** Ready-not-ready checklists, blocked service-opening scenarios, and release evidence showing that missing prep or missing labels creates visible exceptions in the workbench.

### 10. Kitchen display ticket state machine
**Justification:** Kitchen display logic is central to restaurant operations. Print-and-pray tickets cannot handle coursing, expo coordination, and delivery timing at scale.

**Improvement:** Give `kitchen_ticket` explicit states such as queued, acknowledged, firing, held, plated, expo-ready, handed-off, recalled, and closed. Preserve timestamps and actor identity for each transition.

**Acceptance evidence:** KDS state-transition tests, event traces for out-of-order transitions, and screenshots showing the current state model on kitchen display views.

### 11. Course pacing and fire timing
**Justification:** Restaurants need to pace appetizers, entrees, desserts, and delivery prep differently. Without explicit fire rules, the system cannot support real table service or coordinated handoff.

**Improvement:** Add course groups, fire offsets, hold instructions, and synchronizing rules so tickets can be paced by seat, table, or fulfillment promise. Include expo overrides with mandatory reason capture.

**Acceptance evidence:** Multi-course order scenarios, timing variance analytics, and workbench evidence that a delayed appetizer changes downstream fire recommendations instead of silently drifting.

### 12. Expo and pass management
**Justification:** The pass is where kitchen completion becomes service execution. Missing expo controls lead to cold food, wrong table delivery, and poor accountability.

**Improvement:** Add an expo board that verifies plate completeness, modifier fulfillment, allergen markings, and handoff destination before a ticket can leave the line. Support re-fire and return-to-line workflows.

**Acceptance evidence:** Expo confirmation events, rejection and refire scenarios, and UI evidence that incomplete plates cannot be marked handed-off without an override trail.

### 13. Table map and service ownership
**Justification:** Dining room operations depend on table state, section ownership, and turnover progress. Reservations alone do not capture live table service reality.

**Improvement:** Add a table map model with table status, party size, service phase, assigned server, and turn timers. Link open tickets and reservations to the active table occupancy record rather than relying on free text.

**Acceptance evidence:** Table-state transitions, server assignment tests, and screenshots showing occupied, cleaning, ready, and seated states mapped to active orders.

### 14. Reservation pacing against real table inventory
**Justification:** Overbooking and underutilization both come from treating reservations as abstract rows instead of promises against finite tables, turn times, and service constraints.

**Improvement:** Extend `reservation` logic to allocate against actual table inventory, combinable tables, accessibility constraints, and configurable turn assumptions by daypart and party size.

**Acceptance evidence:** Reservation pacing simulations, no-double-booking tests, and workbench evidence that a blocked reservation explains whether the limit is tables, turn time, or staff capacity.

### 15. Waitlist and walk-in management
**Justification:** Walk-ins compete with reservations for the same dining room capacity. A serious restaurant operations backlog must cover quoted wait, party sequencing, and table reassignment rules.

**Improvement:** Add waitlist records with quoted time, actual seat time, party preferences, text-ready state, and escalation when quoted waits are repeatedly missed. Allow staff to convert a walk-in to a seated table without re-entering guest details.

**Acceptance evidence:** Waitlist queue tests, quote-accuracy metrics, and UI evidence showing party promotion from waitlist to seated state with full audit history.

### 16. Unified order lifecycle across channels
**Justification:** Dine-in, takeout, curbside, and delivery orders differ operationally but should still share a canonical order lifecycle for reporting, kitchen execution, and exception handling.

**Improvement:** Define a unified order state model that covers intake, acceptance, firing, ready, packed, handed-off, delivered, canceled, refunded, and reconciled states while keeping channel-specific steps explicit.

**Acceptance evidence:** Channel-by-channel state diagrams, integration tests for dine-in and off-premise flows, and evidence that canceled orders stop downstream prep and waste attribution correctly.

### 17. Modifier propagation to kitchen execution
**Justification:** Modifier detail often degrades between ordering and the line. If the kitchen sees flattened or ambiguous instructions, the platform is not truly restaurant-grade.

**Improvement:** Preserve modifier semantics end to end so the guest UI, server UI, KDS, expo board, and waste analytics all understand the difference between "no onion," "sauce on side," and "substitute gluten-free bun."

**Acceptance evidence:** End-to-end modifier fixtures, kitchen display rendering snapshots, and tests that confirm price changes, allergens, and prep instructions all stay aligned.

### 18. 86 logic and substitution rules
**Justification:** Item outages happen constantly. Operators need structured 86 behavior that protects guest expectations, kitchen load, and delivery marketplace accuracy.

**Improvement:** Add 86 states for menu items, modifiers, and prep components with scope by site, channel, and time window. Support approved substitutions and guest-facing messaging when only part of an item is unavailable.

**Acceptance evidence:** 86 activation tests, substitute suggestion scenarios, and evidence that third-party channels and the in-house UI reflect the same outage within the same release window.

### 19. Inventory boundary ownership
**Justification:** Restaurant operations must know ingredient availability, but it should not own full inventory valuation or procurement. The boundary needs to be explicit to avoid duplicate stock truth.

**Improvement:** Treat on-hand ingredient position as consumed evidence from an inventory-adjacent PBC while `restaurant_operations` owns prep intent, kitchen demand, and service impact. Store only the minimum operational snapshot needed for decisions and trace the source system for the canonical quantity.

**Acceptance evidence:** Boundary documentation, contract tests proving no direct inventory writes, and event traces showing stock snapshots are consumed rather than mutated locally.

### 20. Depletion requests from recipe and prep usage
**Justification:** Orders and prep must create demand against ingredients, but restaurant operations should emit consumption intent instead of silently adjusting inventory tables.

**Improvement:** Emit structured depletion and reservation events from recipe usage, prep batches, waste, and voided food. Distinguish theoretical usage from confirmed usage and correction events so adjacent inventory services can reconcile cleanly.

**Acceptance evidence:** Event schema examples, replay tests for corrected depletion, and evidence that voided tickets reverse demand with explicit causal linkage.

### 21. Food safety temperature monitoring
**Justification:** Safe service requires continuous attention to hot hold, cold hold, cooking, and cooling thresholds. Free-text notes are not acceptable evidence for food safety controls.

**Improvement:** Add temperature check records linked to prep batches, stations, and equipment zones. Support manual entry, device ingestion, threshold breaches, and immediate operational actions such as discard, reheat, or manager review.

**Acceptance evidence:** Threshold-breach scenarios, line-check audit trails, and UI alerts showing open food safety exceptions with required disposition.

### 22. Allergen cross-contact handling
**Justification:** Ingredient declarations alone are insufficient when the actual risk comes from shared fryers, cutting boards, glove changes, or mislabeled prep bins.

**Improvement:** Model cross-contact controls at recipe, station, and ticket level, including required tool changes, dedicated prep zones, and manager confirmation for high-risk tickets. Let the system block unsafe routing to a station that cannot meet the request.

**Acceptance evidence:** Cross-contact routing tests, blocked-assignment evidence, and ticket-level audit history that shows how an allergen-sensitive order was handled.

### 23. Cooling, reheating, and discard workflows
**Justification:** Prep safety is not just about initial cook. Restaurants need evidence around cooling curves, reheating limits, and discard enforcement for reheated or expired product.

**Improvement:** Track cooling start and end, reheating attempts, maximum reuse counts, and mandatory discard states for prep batches. Surface overdue cooling and reheating violations in the manager workbench.

**Acceptance evidence:** Safety lifecycle tests for a prep batch, overdue countdowns, and release evidence showing that unsafe batches cannot be assigned to new tickets.

### 24. Waste taxonomy and root cause capture
**Justification:** Waste data is useless if every loss is logged as a generic discard. Restaurants need to separate overproduction, spoilage, line error, guest return, dropped plate, and expired hold.

**Improvement:** Expand `food_waste` with a controlled reason taxonomy, station, shift, menu item or prep batch linkage, and responsible phase such as prep, cook, expo, or service. Support both quantity and estimated cost impact.

**Acceptance evidence:** Waste reason validation tests, analytics by cause and station, and evidence that the UI prevents uncategorized waste closure.

### 25. Theoretical versus actual yield analytics
**Justification:** Recipe engineering depends on understanding where cost and portion drift occur. The system should expose when theoretical yield and actual output diverge materially.

**Improvement:** Compare recipe target yield, approved prep quantity, sold quantity, and recorded waste to highlight overportioning, trim loss, and mis-prep. Allow managers to investigate by item, station, shift, and recipe version.

**Acceptance evidence:** Yield variance dashboards, drift alerts, and seeded scenarios proving the system can distinguish waste from portion inflation.

### 26. Comp and void governance
**Justification:** Comps and voids are both guest-service tools and abuse vectors. They must be operationally fast while remaining tightly governed.

**Improvement:** Create separate workflows for pre-fire void, post-fire void, manager comp, and hospitality comp with reason codes, approval thresholds, and attachment of service-recovery context. Keep check impact and kitchen impact distinct.

**Acceptance evidence:** Approval-path tests by amount and role, comp and void audit reports, and evidence that post-fire voids can still trigger waste or remake workflows.

### 27. Distinguishing discount, comp, and waste
**Justification:** Restaurants often blend commercial decisions and operational losses. That destroys margin analysis and can hide control failures.

**Improvement:** Enforce separate ledgers and event types for promotional discounts, service-recovery comps, order voids, and physical waste. Each path should preserve its own approval logic, root cause, and reporting destination.

**Acceptance evidence:** Reporting snapshots that keep categories separate, reconciliation tests across the four paths, and evidence that the UI prevents a manager from using a comp code to hide spoiled food.

### 28. Delivery channel menu publishing
**Justification:** Off-premise demand fails when third-party channels drift from the in-house menu. Restaurants need explicit publication state and timing controls per channel.

**Improvement:** Add delivery-channel publication status, mapped item identifiers, mapped modifier availability, lead times, pickup windows, and site-specific throttles. Support preview before a menu sync is released.

**Acceptance evidence:** Channel mapping tests, publication diff views, and evidence that an unpublished or failed sync is visible in the workbench before service begins.

### 29. Delivery order ingestion and outage handling
**Justification:** Channel orders arrive through brittle integrations. The restaurant side needs clean recovery when a marketplace retries, delays, or duplicates an order.

**Improvement:** Add idempotent intake for delivery orders with marketplace identifier, promised time, handoff type, and failure recovery path. Support duplicate detection, late accept decisions, and graceful fallback during integration outages.

**Acceptance evidence:** Duplicate-order fixtures, delayed-ingestion scenarios, and event traces proving a recovered marketplace order does not create a second kitchen ticket.

### 30. Labor boundary ownership
**Justification:** Restaurant operations depends on staffing, but it should not own payroll, tax, or full HR records. The labor boundary must be as clear as the inventory boundary.

**Improvement:** Treat `labor_shift` as an operational staffing surface with demand, assignment, and service impact data while consuming official worker, schedule, and payroll truth from a labor-adjacent domain. Keep labor cost assumptions explicit and local only where needed for service decisions.

**Acceptance evidence:** Boundary tests showing no payroll mutation, dependency contracts for staffing feeds, and workbench evidence that missing labor data raises a dependency exception instead of creating local shadow records.

### 31. Staffing demand from reservations and order mix
**Justification:** Labor should respond to expected covers, prep load, and delivery volume rather than only fixed schedules. Restaurants need forward-looking demand signals inside the PBC.

**Improvement:** Generate staffing pressure indicators from reservations, forecasted order mix, prep intensity, and channel mix. Separate front-of-house, line, expo, and prep demand so managers can see where the pinch point is.

**Acceptance evidence:** Demand forecast traces, side-by-side staffing pressure views, and scenario evidence for a reservation spike, delivery surge, and large-party seating event.

### 32. Station assignment and skill coverage
**Justification:** Not every worker can cover every station, and service quality collapses when the system ignores station skill requirements or break coverage.

**Improvement:** Model station skills, certifications, and temporary assignment changes inside operational labor views. Highlight uncovered stations, break overlap risk, and high-risk setups such as the same person covering expo and allergy-sensitive fry station.

**Acceptance evidence:** Skill-coverage tests, uncovered-station alerts, and UI evidence showing which station assignment risk is blocking an opening checklist or service plan.

### 33. Table service recovery workflow
**Justification:** Front-of-house recovery is a major operational domain. Late food, wrong modifiers, cold plates, and missed birthday requests all need structured handling tied to the original order.

**Improvement:** Add guest issue records linked to table, seat, order line, and server action. Support remake, comp request, manager visit, priority refire, and promised follow-up with timestamps and resolution evidence.

**Acceptance evidence:** Service recovery scenarios, linked comp and refire events, and workbench evidence that unresolved guest issues stay visible until formally closed.

### 34. Seat-level ordering and shared-item logic
**Justification:** Real tables include shared appetizers, split checks, and seat-specific modifiers. Without seat-level structure, the kitchen and service staff cannot reliably coordinate.

**Improvement:** Add seat assignment, shareable item flags, split responsibility, and guest note routing so line items can be prepared and delivered accurately while still rolling up to the right check and table context.

**Acceptance evidence:** Multi-seat order fixtures, shared-item kitchen rendering tests, and UI evidence showing seat-specific delivery without duplicating the item on the expo board.

### 35. Server and handheld UI flow
**Justification:** Table service depends on a fast and mistake-resistant UI. Servers need guided entry that minimizes modifier misses, wrong seat assignment, and delayed fire timing.

**Improvement:** Rework the front-of-house UI around service flow: seat the table, start order, add modifiers, course items, hold fire, request guest note review, and send in one obvious sequence. Make high-risk actions such as void after fire require explicit escalation.

**Acceptance evidence:** UI interaction tests, keyboard and handheld acceptance paths, and screenshots demonstrating that service-critical actions are available without navigating away from the active table.

### 36. Kitchen display and expo UI flow
**Justification:** Kitchen display usability is part of the domain model. If cooks and expo cannot interpret the board instantly, the underlying data design has failed.

**Improvement:** Design role-specific KDS views for grill, pantry, expo, and pack stations with lane grouping, urgent badges, modifier prominence, allergen markers, and promised-time countdowns. Keep view logic driven by structured ticket state and station routing.

**Acceptance evidence:** Role-based UI contracts, screenshot evidence for each station view, and usability checks that show critical modifier and timing data stays visible under peak load.

### 37. Manager workbench for operational exceptions
**Justification:** Managers need one place to see reservations, kitchen backlog, food safety issues, comps, staffing gaps, and delivery delays together. Fragmented dashboards weaken operational control.

**Improvement:** Turn `GET /restaurant-operations-workbench` into an exception-first cockpit with widgets for dining room pacing, KDS backlog, expiring prep, open guest recoveries, waste spikes, and blocked delivery channels.

**Acceptance evidence:** Workbench route tests, widget contract snapshots, and evidence that each high-severity exception links directly to the underlying operational record and remediation action.

### 38. Agent skill for menu engineering
**Justification:** Restaurant teams need guided help when creating or updating menu items, but agent assistance must stay within policy and avoid inventing operational facts.

**Improvement:** Add an assistant skill that drafts menu items, daypart assignments, modifier sets, and rollout plans from a manager prompt, then shows a governed preview before any mutation. Require citations to existing menu and recipe data where possible.

**Acceptance evidence:** Skill prompt fixtures, permission-checked preview flows, and audit evidence that the assistant cannot activate a menu change without the same approvals as a human user.

### 39. Agent skill for prep, waste, and 86 coaching
**Justification:** Managers need help interpreting prep pressure and waste patterns quickly during service, not generic analytics after the shift ends.

**Improvement:** Add an assistant skill that explains likely prep shortfalls, recommends controlled 86 actions, identifies waste root causes, and suggests batch-size changes based on reservation, order, and waste evidence.

**Acceptance evidence:** Explainability traces for recommendations, accepted and rejected suggestion logs, and tests proving the assistant stays suggestion-only when the configured policy forbids autonomous changes.

### 40. Agent skill for reservation and table optimization
**Justification:** Reservation teams need fast what-if reasoning around table combinations, no-shows, pacing, and walk-in insertion. This is a high-value assistant use case if it stays grounded in actual table inventory.

**Improvement:** Add an assistant skill that proposes seating plans, quote adjustments, and reseating actions using live table status, turn assumptions, and reservation priority rules. Surface the exact constraints behind each suggestion.

**Acceptance evidence:** Simulation fixtures for no-show and walk-in pressure, side-by-side assistant recommendations, and audit trails showing accepted suggestions changed only the intended reservation or table records.

### 41. Domain event taxonomy for service operations
**Justification:** The current generic events are too broad for serious operational replay, analytics, and integration. Restaurant operations needs typed events that describe what actually happened.

**Improvement:** Define typed events for menu activation, recipe revision, prep batch started, prep batch expired, reservation seated, table turned, ticket fired, item refired, order packed, comp approved, and waste recorded. Keep causal links between related events.

**Acceptance evidence:** Event catalog documentation, schema tests, and replay evidence showing projections rebuild correctly from typed service events alone.

### 42. Event ingestion and dependency health
**Justification:** The PBC already consumes `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`, but the operational effect of those events should be visible and testable.

**Improvement:** Build idempotent handlers that update policy readiness, audit proof state, and KPI-driven alerts without mutating unrelated domain records. Surface dependency freshness and last-processed offsets in the workbench.

**Acceptance evidence:** Duplicate-event tests, handler health dashboards, and evidence that a stale dependency raises an actionable exception instead of silently aging out.

### 43. Permissions by role, site, and action
**Justification:** Restaurant control failures often come from overbroad permissions. A cashier, server, chef, sous chef, and general manager should not share the same action surface.

**Improvement:** Expand permission checks to action level by site, station, and monetary or safety threshold. Make high-risk actions such as post-fire voids, allergy overrides, and manual ticket state correction require stronger approval paths.

**Acceptance evidence:** Permission matrix tests, denied-action UI states, and release evidence showing role-specific access for service, kitchen, and management personas.

### 44. Offline and degraded-mode operations
**Justification:** Restaurants still have to serve guests when the network or one integration fails. The backlog should cover degraded operation instead of assuming perfect connectivity.

**Improvement:** Add offline-safe capture for table service actions, queued kitchen updates, deferred delivery acknowledgments, and clear reconciliation once connectivity returns. Mark degraded records visibly so staff know what still needs sync or review.

**Acceptance evidence:** Offline recovery scenarios, conflict-resolution traces, and UI evidence that staff can distinguish unsynced changes from fully confirmed operational state.

### 45. Multi-location concept governance
**Justification:** Chain restaurants need local variation without losing brand control. One site may run brunch, another may not; one city may require different allergen text or service flow.

**Improvement:** Support hierarchical configuration for brand, concept, region, and site covering menu rollout, reservation rules, prep templates, KDS routing, and food safety checklists. Keep inheritance and override reasoning explicit.

**Acceptance evidence:** Multi-site override tests, inheritance diff views, and evidence that local changes do not leak across tenants or unrelated sites.

### 46. Release evidence for rush and edge-case scenarios
**Justification:** Release confidence in restaurant operations comes from realistic service scenarios, not just CRUD tests. Peak periods and operational edge cases reveal the real defects.

**Improvement:** Build executable release scenarios for lunch rush, modifier-heavy large party, reservation no-show wave, third-party delivery burst, 86 event, food safety discard, and post-fire comp. Tie each scenario to the exact APIs, UI flows, and events exercised.

**Acceptance evidence:** Scenario manifests, smoke test outputs, and a release evidence index that shows pass or fail for each high-risk restaurant operation.

### 47. Delivery SLA and handoff proof
**Justification:** Off-premise service quality depends on the handoff boundary from kitchen to courier. Without evidence of promised versus actual ready times, channel disputes are hard to resolve.

**Improvement:** Track ready time, packed time, courier arrival, courier handoff, and late reason codes for delivery orders. Separate restaurant-caused delay from courier-caused delay for analytics and dispute support.

**Acceptance evidence:** SLA metrics by channel, handoff timestamp tests, and evidence exports that support a late-order investigation without querying external systems directly.

### 48. Cross-PBC boundary documentation and contracts
**Justification:** The package touches adjacent domains such as inventory, labor, audit, and policy. Those seams need hard contracts or the implementation will drift toward hidden coupling.

**Improvement:** Document and test every cross-PBC contract used by restaurant operations, especially stock snapshots, staffing signals, policy updates, and sealed audit evidence. Keep local ownership limited to restaurant decision state and operational execution.

**Acceptance evidence:** Contract test suite results, boundary diagrams, and release evidence showing no shared-table dependency outside the package's owned schema.

### 49. Operational KPI definitions and explainability
**Justification:** Restaurants need metrics they can act on in the moment. Throughput, turn time, ticket time, quote accuracy, waste, and comp rate all need stable definitions or teams will argue about the numbers.

**Improvement:** Define canonical KPIs for dining room, kitchen, off-premise, safety, waste, and labor pressure with calculation windows, exclusions, and drill-through paths back to raw operational records and events.

**Acceptance evidence:** KPI definition catalog, projection validation tests, and workbench drill-through evidence that explains exactly why a metric moved.

### 50. Release gate traceability to every operational surface
**Justification:** The backlog is only useful if release evidence proves the package now covers the restaurant domain end to end. Menus, recipes, prep, reservations, table service, KDS, orders, modifiers, boundaries, safety, waste, comps, delivery, UI, agent skills, and events must all be tied to executable proof.

**Improvement:** Build a release gate matrix that maps every major restaurant operations surface to schema, API, event, UI, assistant skill, scenario, and audit evidence. Block release when any critical surface lacks evidence or has stale evidence.

**Acceptance evidence:** A traceability matrix in `RELEASE_EVIDENCE.md`, automated checks that fail on missing coverage, and final validation that the package can demonstrate end-to-end evidence for each major restaurant operations workflow.
