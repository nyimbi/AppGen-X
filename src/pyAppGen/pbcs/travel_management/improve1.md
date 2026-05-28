# Travel Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `travel_management`. Each item is specific to trip requests, traveler profiles, travel policy, approval routing, booking intents, air/hotel/ground bookings, itineraries, duty-of-care, disruptions, unused tickets, travel-expense handoffs, supplier offers, risk assessment, traveler assistance, agent guidance, and AppGen-X event reliability.

## Current Domain Evidence Used

- Domain purpose: trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.
- Owned operational surface: trip requests, traveler profiles, travel policies, approval tasks, booking intents, air bookings, hotel bookings, ground bookings, itinerary items, duty-of-care alerts, travel disruptions, unused tickets, travel-expense links, risk assessments, supplier offers, exception cases, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X runtime event tables.
- Declared operations: trip request creation, travel policy validation, approval routing, booking intent creation, air/hotel/ground booking recording, itinerary building, duty-of-care screening, disruption opening, unused ticket tracking, expense linking, travel risk scoring, supplier offer comparison, exception resolution, travel rule compilation, and disruption impact simulation.
- Declared events and integrations: emits `TripRequested`, `TravelApproved`, `ItineraryBuilt`, `DutyOfCareAlertOpened`, `TravelDisruptionOpened`, and `UnusedTicketRecorded`; consumes `EmployeeCreated`, `ExpenseReportCreated`, `PolicyChanged`, and `PaymentExecuted`; catalog traceability also covers employee, expense, supplier, booking, duty-of-care, and expense-handoff events.
- Advanced capability evidence: traveler-aware policy guidance, disruption counterfactual routing, semantic itinerary ingestion, duty-of-care risk intelligence, unused-ticket optimization, carbon-aware booking comparison, event-sourced operational history, multi-tenant policy isolation, anomaly detection, predictive risk scoring, scenario simulation, cryptographic audit proofs, continuous control testing, cross-PBC event federation, and governed agent execution.

## 50 Better-Than-World-Class Improvements

### 1. Trip request readiness gate

**Justification:** Travel requests without traveler, destination, business purpose, dates, risk, budget, and policy evidence lead to unsafe bookings and approval rework.

**Improvement:** Add a readiness gate that verifies traveler projection, trip purpose, destination, dates, cost estimate, risk level, policy version, required approvals, visa/passport needs, and duty-of-care prerequisites before a request can proceed.

### 2. Trip lifecycle state machine

**Justification:** Trips move through draft, submitted, approved, booking, booked, in-trip, disrupted, completed, cancelled, expensed, and archived states with different policy and assistance actions.

**Improvement:** Implement a strict state machine with allowed transitions, required evidence, owner, notifications, booking effects, expense handoff eligibility, and audit proofs. Release tests should reject bookings and expense links in invalid states.

### 3. Traveler profile completeness scoring

**Justification:** Traveler profiles need contact, emergency, document, preference, accessibility, loyalty, region, and risk information to support bookings and duty-of-care.

**Improvement:** Score profile completeness for contact methods, emergency contacts, identity documents, home region, preferred language, accessibility requirements, loyalty identifiers, notification preferences, and risk consent. Surface missing items before approval or travel.

### 4. Traveler preference and accessibility handling

**Justification:** Travel management must respect seat, meal, accessibility, schedule, lodging, language, and communication needs without exposing sensitive information unnecessarily.

**Improvement:** Add preference categories, sensitivity levels, booking applicability, consent state, visibility controls, and override rules. Booking intent comparisons should explain which preferences were satisfied, unavailable, or policy-blocked.

### 5. Travel policy versioning

**Justification:** Fare class, hotel rate, advance booking, approval thresholds, supplier rules, and risk policies change over time and by employee group.

**Improvement:** Version policies by effective interval, region, employee level, business unit, trip type, supplier category, fare class, hotel cap, ground rules, and exception paths. Store the policy version on every validation and approval decision.

### 6. Travel policy rule compiler

**Justification:** Travel policies often live in documents with nested exceptions, role-specific thresholds, emergency overrides, and supplier preferences.

**Improvement:** Compile travel policy documents into executable predicates with ambiguity flags, examples, test cases, approvers, and effective dates. The agent should request clarification for unclear rules before activation.

### 7. Pre-trip policy coaching

**Justification:** Travelers need guidance before selecting expensive or noncompliant options, not after expenses are submitted.

**Improvement:** Add counterfactual coaching that compares compliant alternatives by fare class, booking window, hotel rate, preferred supplier, route, carbon, and traveler constraints. Show why options pass, warn, or require exception approval.

### 8. Approval routing graph

**Justification:** Travel approvals depend on cost, destination risk, traveler role, advance notice, policy exceptions, project, budget owner, and duty-of-care escalation.

**Improvement:** Build approval graphs with manager, budget owner, risk/security, HR, finance, and executive nodes. Store route rationale, skipped approvers, delegation, escalation timers, and approval evidence.

### 9. Emergency and exception approval lane

**Justification:** Urgent travel may require rapid approval without bypassing duty-of-care and spend controls.

**Improvement:** Add emergency approval states with reason, risk screen, post-approval review, time-boxed authorization, and exception evidence. UI should distinguish emergency policy overrides from normal approval paths.

### 10. Booking intent lifecycle

**Justification:** Booking intent is the bridge between approved need and actual air, hotel, and ground reservations.

**Improvement:** Model intents with purpose, traveler, policy constraints, preferred suppliers, budget, travel window, risk constraints, booking deadline, and option comparison. Track draft, compared, selected, held, booked, expired, and cancelled states.

### 11. Supplier offer normalization

**Justification:** Offers from airlines, hotels, ground providers, agencies, and supplier feeds vary in fare rules, restrictions, fees, cancellation terms, and carbon data.

**Improvement:** Normalize offers into comparable structures with base price, taxes, fees, restrictions, refundability, loyalty accrual, baggage, cancellation, supplier rating, risk, and carbon estimate. Preserve source payload hashes.

### 12. Air booking controls

**Justification:** Air bookings require fare class, routing, layover, refundability, baggage, change fees, ticketing deadlines, and unused ticket implications.

**Improvement:** Add air-specific validation for fare class policy, connection risk, travel time, ticket deadline, seat/accessibility needs, cancellation rules, and unused-ticket eligibility. Store ticket numbers, status, and change history.

### 13. Hotel booking controls

**Justification:** Hotel bookings depend on nightly rate caps, location safety, tax/fee transparency, cancellation windows, traveler accessibility, and preferred supplier status.

**Improvement:** Validate hotels by location, rate cap, total stay cost, cancellation terms, safety rating, accessibility, check-in/out, preferred supplier, and policy exceptions. Surface rate-cap overages and safer alternatives.

### 14. Ground transport controls

**Justification:** Ground transport includes rail, rental car, rideshare, taxi, shuttle, and personal vehicle with distinct policy and safety rules.

**Improvement:** Add ground booking validation for mode eligibility, distance, rate, class, insurance, driver eligibility, pickup/dropoff timing, safety, and carbon. Link personal vehicle use to mileage policy and expense handoff.

### 15. Semantic itinerary ingestion

**Justification:** Itineraries arrive as emails, PDFs, calendar invites, agency feeds, and supplier confirmations with inconsistent formats.

**Improvement:** Parse itinerary documents into air, hotel, ground, meeting, and risk-relevant items with time zones, confirmation numbers, supplier, location, and status. The agent should flag uncertain fields and require confirmation before writing itinerary records.

### 16. Itinerary integrity timeline

**Justification:** A traveler itinerary must reflect current booking state, time zones, disruptions, cancellations, and manual changes.

**Improvement:** Build an itinerary timeline with item dependencies, local times, confirmation status, source evidence, conflict detection, gaps, and change history. UI should highlight impossible connections and missing accommodation nights.

### 17. Duty-of-care risk assessment

**Justification:** Travel risk changes by destination, time, traveler profile, geopolitical events, health advisories, weather, and local operations.

**Improvement:** Score trip risk using destination, itinerary, traveler profile, emergency contact, alert feeds, time proximity, transport modes, and company policy. Store risk drivers, confidence, and required mitigation.

### 18. Duty-of-care alert workflow

**Justification:** Alerts must move from detection to traveler contact, acknowledgement, escalation, assistance, and closure.

**Improvement:** Add alert states, severity, affected travelers, contact attempts, acknowledgment, escalation owner, assistance actions, and closure proof. Track missed contact attempts and unresolved high-risk travelers.

### 19. Traveler location confidence

**Justification:** Duty-of-care actions need to know where the traveler likely is without overclaiming certainty.

**Improvement:** Estimate location confidence from itinerary, check-ins, expense links, traveler updates, and declared projections. Show current, planned, stale, and unknown location states with privacy controls.

### 20. Disruption detection and triage

**Justification:** Flight cancellations, delays, hotel closures, strikes, weather, security incidents, and supplier failures require fast triage.

**Improvement:** Add disruption records with source, affected itinerary items, severity, traveler impact, options, policy implications, duty-of-care risk, and expense impact. Route severe cases to assistance queues.

### 21. Disruption counterfactual routing

**Justification:** During disruption, teams need to compare rebooking options by time, cost, policy, traveler safety, carbon, and downstream meetings.

**Improvement:** Simulate alternatives with cost, arrival time, connection risk, cancellation penalties, unused ticket use, hotel impact, traveler preference, and duty-of-care score. Store selected and rejected route rationale.

### 22. Traveler assistance case workflow

**Justification:** Assistance requests can involve safety, lost documents, medical issues, missed flights, hotel problems, and emergency repatriation.

**Improvement:** Add assistance cases with category, severity, location, contact method, owner, actions, supplier interactions, policy exceptions, cost estimate, and closure evidence. Keep sensitive details access-controlled.

### 23. Unused ticket inventory optimization

**Justification:** Unused tickets represent recoverable value that is often lost due to expiration, traveler mismatch, supplier rules, or poor visibility.

**Improvement:** Track unused tickets with value, currency, traveler, supplier, expiration, transferability, fare rules, residual value, and reuse eligibility. Recommend reuse during booking-intent comparison and warn before expiration.

### 24. Unused ticket expiration controls

**Justification:** Tickets can expire silently without operational ownership or traveler awareness.

**Improvement:** Add expiration alerts, owner assignment, reuse campaigns, exception handling, write-off evidence, and recovered-value analytics. Include unused-ticket status in travel readiness dashboards.

### 25. Travel expense handoff readiness

**Justification:** Expense handoff should connect approved trips, bookings, itineraries, receipts, and reimbursement context without sharing foreign tables.

**Improvement:** Generate travel-expense links with trip, itinerary, policy, approved budget, booking references, expected categories, per diem eligibility, mileage eligibility, and source evidence. Emit handoff events through AppGen-X only.

### 26. Settlement and payment reconciliation

**Justification:** Travel bookings can be prepaid, centrally billed, reimbursed, cancelled, refunded, or settled through supplier statements.

**Improvement:** Reconcile payment execution, supplier charges, cancellations, refunds, unused ticket credits, and traveler expenses through declared events/projections. Store settlement status and exception reasons.

### 27. Supplier performance scorecard

**Justification:** Supplier choices should reflect reliability, traveler experience, policy compliance, disruption handling, cost, carbon, and duty-of-care support.

**Improvement:** Score suppliers by booking success, disruption rate, refund behavior, safety incidents, traveler feedback, preferred status, cost variance, and carbon data completeness. Use scorecards in offer comparison.

### 28. Preferred supplier compliance

**Justification:** Travel programs negotiate preferred suppliers, but exceptions may be justified by safety, availability, accessibility, or cost.

**Improvement:** Validate supplier selections against preferred-supplier rules, exception reasons, negotiated rates, traveler needs, and disruption conditions. Store compliance or exception evidence for sourcing analytics.

### 29. Carbon-aware booking comparison

**Justification:** Travel programs increasingly need to compare emissions alongside cost, time, safety, and policy.

**Improvement:** Add carbon estimates for air, hotel, ground, and route alternatives with assumptions, data source, confidence, and tradeoffs. Allow carbon-aware recommendations subject to traveler safety and business constraints.

### 30. Traveler wellbeing controls

**Justification:** Overly aggressive travel plans can create fatigue, safety issues, and poor performance even when policy-compliant.

**Improvement:** Add controls for red-eye frequency, minimum rest, long layovers, excessive trip density, time-zone burden, and accessibility needs. Surface wellbeing warnings and approval requirements.

### 31. Visa and document readiness

**Justification:** International travel can fail if passports, visas, entry permits, health documents, or traveler identity records are incomplete.

**Improvement:** Add document readiness checks with expiration, destination requirements, lead times, traveler nationality, document sensitivity, and reminders. Block booking finalization where mandatory documents are missing.

### 32. Travel risk exception governance

**Justification:** High-risk destinations may require extra approval, mitigation, security briefing, tracking, or prohibition.

**Improvement:** Add risk exception workflows with destination category, traveler rationale, mitigation plan, approvers, emergency contacts, insurance, and travel restrictions. Store approval and traveler acknowledgement.

### 33. Trip budget and cost forecast

**Justification:** Travel costs should be estimated before approval and compared against actual bookings and expenses.

**Improvement:** Forecast trip cost across air, hotel, ground, per diem, fees, taxes, unused-ticket offsets, and expected expense categories. Compare approved budget, booked cost, settled cost, and expensed cost.

### 34. Travel anomaly detection

**Justification:** Unusual routes, high hotel rates, repeated late booking, excessive cancellations, and supplier anomalies can signal waste or risk.

**Improvement:** Detect anomalies by traveler, route, supplier, booking window, fare class, cancellation rate, destination risk, and cost variance. Route high-risk patterns to exception or audit queues.

### 35. Travel policy impact analysis

**Justification:** Changing booking windows, hotel caps, fare class rules, or approval thresholds affects cost, traveler experience, and compliance load.

**Improvement:** Simulate policy changes against historical trips and pending intents to estimate savings, exceptions, approval volume, traveler impact, carbon impact, and duty-of-care consequences.

### 36. Continuous travel control testing

**Justification:** Travel controls need continuous assurance across policy, approvals, bookings, duty-of-care, unused tickets, settlement, and expense handoffs.

**Improvement:** Add controls for unapproved bookings, missing risk screens, policy exceptions, stale itinerary items, unused-ticket leakage, missing expense handoffs, and unresolved disruptions. Store assertion results and remediation tasks.

### 37. Travel exception case workflow

**Justification:** Travel exceptions such as policy override, supplier failure, refund dispute, traveler emergency, or missing documents need structured resolution.

**Improvement:** Add exception cases with type, severity, owner, affected trip/bookings, required evidence, financial exposure, traveler impact, resolution action, and closure proof.

### 38. Cryptographic travel audit proof

**Justification:** Travel approvals, bookings, risk checks, and expense handoffs may be audited for policy, safety, and spend governance.

**Improvement:** Generate hash-chain proofs for trip requests, approvals, policy evaluations, bookings, itinerary changes, duty-of-care alerts, disruptions, unused tickets, and expense handoffs. Provide redacted verifier exports.

### 39. AppGen-X event reliability proof

**Justification:** Travel management depends on employee, policy, payment, expense, and supplier events; lost or duplicate events can break booking and care flows.

**Improvement:** Harden event descriptors with schema versions, idempotency keys, ordering assumptions, retry envelopes, dead-letter taxonomy, replay eligibility, and handler evidence. Add tests for duplicate employee events and late payment callbacks.

### 40. Cross-PBC boundary proof

**Justification:** Travel needs employee, expense, payment, supplier, policy, and risk context without direct foreign-table access.

**Improvement:** Generate a boundary proof enumerating every declared API, projection, consumed event, cached field, staleness policy, and retention rule. Release audits should fail undeclared employee, expense, payment, or supplier table references.

### 41. Agent-assisted trip planning

**Justification:** Travelers need help turning business goals, meeting locations, policy constraints, and personal needs into compliant trip plans.

**Improvement:** Let the agent draft trip requests, compare compliant options, explain policy, identify missing traveler profile data, and prepare approval-ready plans. It must not book or submit without explicit confirmation.

### 42. Agent-assisted disruption recovery

**Justification:** Disruptions require fast, reasoned choices under uncertainty.

**Improvement:** Let the agent summarize disruption impact, compare rebooking alternatives, check duty-of-care risk, estimate cost and carbon, propose traveler messages, and prepare safe service commands for approval.

### 43. Agent-assisted itinerary ingestion

**Justification:** Users often forward confirmations or upload documents instead of manually entering itinerary items.

**Improvement:** Let the agent extract itinerary items, confirmation numbers, supplier contacts, locations, time zones, cancellation windows, and expense hints from documents. It should surface uncertainty and require review before CRUD.

### 44. Traveler communication center

**Justification:** Travel operations need controlled communication for approvals, booking changes, risk alerts, disruption assistance, and unused-ticket reminders.

**Improvement:** Add communication templates, preference-aware delivery plans, message history, acknowledgement tracking, and escalation for unanswered critical alerts. Integrate only through declared notification events/projections.

### 45. Travel operations cockpit

**Justification:** Managers need a unified view of pending trips, approvals, bookings, disruptions, duty-of-care alerts, unused tickets, exceptions, and supplier issues.

**Improvement:** Build cockpit panels with filters by traveler, region, destination risk, trip state, policy exception, supplier, cost, and alert severity. Include safe bulk actions for reminders, escalation, and evidence export.

### 46. UI capability surface proof

**Justification:** A complete Travel Management PBC must expose all travel capabilities, not hide advanced operations in generic records.

**Improvement:** Add release checks proving UI coverage for trip requests, traveler profiles, policies, approvals, booking intents, air/hotel/ground bookings, itineraries, duty-of-care alerts, disruptions, unused tickets, expense links, risk assessments, supplier offers, exceptions, rules, parameters, controls, models, events, and agent tools.

### 47. Travel resilience drills

**Justification:** Travel systems must recover from supplier feed outages, itinerary ingestion failures, payment callback delays, policy mistakes, and duty-of-care event floods.

**Improvement:** Add drills for supplier outage, duplicate booking replay, itinerary parser failure, policy rollback, risk-alert surge, unused-ticket expiration backlog, and dead-letter recovery. Store recovery time, affected travelers, and cost exposure.

### 48. Travel readiness score

**Justification:** Operators need a concise signal showing whether the PBC is production-ready for managed travel in a composed application.

**Improvement:** Compute readiness from traveler profile completeness, policy coverage, approval routing, supplier offer quality, booking controls, duty-of-care health, unused-ticket controls, expense handoff readiness, event health, UI coverage, and agent safety.

### 49. Traveler data privacy and retention

**Justification:** Travel records include location, identity documents, accessibility needs, emergency contacts, and risk details that require careful handling.

**Improvement:** Add privacy classifications, retention rules, access scopes, redaction support, purpose constraints, and audit for sensitive traveler fields. Agent summaries should avoid exposing unnecessary sensitive profile details.

### 50. End-to-end travel release proof

**Justification:** A world-class Travel Management PBC needs one evidence package proving that travel can flow from request through approval, booking, itinerary, care, disruption, unused ticket, settlement, expense handoff, and assistance safely.

**Improvement:** Create an end-to-end proof exercising trip request readiness, traveler profile, policy compilation, approval routing, booking intent, supplier offer comparison, air/hotel/ground booking, itinerary ingestion, duty-of-care screening, disruption simulation, unused ticket tracking, expense handoff, settlement reconciliation, exception resolution, UI coverage, AppGen-X eventing, boundary verification, and agent-safe CRUD planning.
