# Travel Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `travel_management`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.
- Representative owned tables: `travel_management_trip_request`, `travel_management_traveler_profile`, `travel_management_travel_policy`, `travel_management_travel_approval_task`, `travel_management_booking_intent`, `travel_management_air_booking`, `travel_management_hotel_booking`, `travel_management_ground_booking`, `travel_management_itinerary_item`, `travel_management_duty_of_care_alert`, `travel_management_travel_disruption`, `travel_management_unused_ticket`, ...
- Representative operations/APIs: `create_trip_request`, `validate_travel_policy`, `route_travel_approval`, `create_booking_intent`, `record_air_booking`, `record_hotel_booking`, `record_ground_booking`, `build_itinerary`, `screen_duty_of_care`, `open_travel_disruption`, `track_unused_ticket`, `link_travel_expense`, ...
- Representative events: `TripRequested`, `TravelApproved`, `ItineraryBuilt`, `DutyOfCareAlertOpened`, `TravelDisruptionOpened`, `UnusedTicketRecorded`.
- Representative advanced capabilities: `traveler-aware policy guidance`, `disruption counterfactual routing`, `semantic itinerary ingestion`, `duty-of-care risk intelligence`, `unused-ticket optimization`, `carbon-aware booking comparison`.

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `travel_management_trip_request`

**Justification:** This owned table is part of the Travel Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.

**Improvement:** Extend `travel_management_trip_request` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `travel_request_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `travel_management_traveler_profile`

**Justification:** This owned table is part of the Travel Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.

**Improvement:** Extend `travel_management_traveler_profile` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `travel_management_workflow`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `travel_management_travel_policy`

**Justification:** This owned table is part of the Travel Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.

**Improvement:** Extend `travel_management_travel_policy` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `travel_management_analytics`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `travel_management_travel_approval_task`

**Justification:** This owned table is part of the Travel Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.

**Improvement:** Extend `travel_management_travel_approval_task` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `configuration_schema`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `travel_management_booking_intent`

**Justification:** This owned table is part of the Travel Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.

**Improvement:** Extend `travel_management_booking_intent` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `rule_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `travel_management_air_booking`

**Justification:** This owned table is part of the Travel Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.

**Improvement:** Extend `travel_management_air_booking` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `parameter_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `travel_management_hotel_booking`

**Justification:** This owned table is part of the Travel Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.

**Improvement:** Extend `travel_management_hotel_booking` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `owned_schema_migrations_models`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `travel_management_ground_booking`

**Justification:** This owned table is part of the Travel Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.

**Improvement:** Extend `travel_management_ground_booking` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `appgen_x_outbox_inbox_eventing`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `travel_management_itinerary_item`

**Justification:** This owned table is part of the Travel Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.

**Improvement:** Extend `travel_management_itinerary_item` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `idempotent_handlers`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `travel_management_duty_of_care_alert`

**Justification:** This owned table is part of the Travel Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance.

**Improvement:** Extend `travel_management_duty_of_care_alert` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `retry_dead_letter_evidence`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `create_trip_request` a complete command lifecycle

**Justification:** High-value users need `create_trip_request` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_trip_request` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TripRequested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `validate_travel_policy` a complete command lifecycle

**Justification:** High-value users need `validate_travel_policy` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `validate_travel_policy` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TravelApproved`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `route_travel_approval` a complete command lifecycle

**Justification:** High-value users need `route_travel_approval` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `route_travel_approval` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ItineraryBuilt`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `create_booking_intent` a complete command lifecycle

**Justification:** High-value users need `create_booking_intent` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_booking_intent` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DutyOfCareAlertOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `record_air_booking` a complete command lifecycle

**Justification:** High-value users need `record_air_booking` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `record_air_booking` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TravelDisruptionOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `record_hotel_booking` a complete command lifecycle

**Justification:** High-value users need `record_hotel_booking` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `record_hotel_booking` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `UnusedTicketRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `record_ground_booking` a complete command lifecycle

**Justification:** High-value users need `record_ground_booking` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `record_ground_booking` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TripRequested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `build_itinerary` a complete command lifecycle

**Justification:** High-value users need `build_itinerary` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `build_itinerary` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `TravelApproved`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `screen_duty_of_care` a complete command lifecycle

**Justification:** High-value users need `screen_duty_of_care` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `screen_duty_of_care` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ItineraryBuilt`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `open_travel_disruption` a complete command lifecycle

**Justification:** High-value users need `open_travel_disruption` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `open_travel_disruption` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DutyOfCareAlertOpened`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `traveler-aware policy guidance` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Travel Management and measurably improves travel management risk score without hiding assumptions.

**Improvement:** Promote `traveler-aware policy guidance` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `travel_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `disruption counterfactual routing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Travel Management and measurably improves travel management workbench metric without hiding assumptions.

**Improvement:** Promote `disruption counterfactual routing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `travel_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `semantic itinerary ingestion` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Travel Management and measurably improves travel management risk score without hiding assumptions.

**Improvement:** Promote `semantic itinerary ingestion` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `travel_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `duty-of-care risk intelligence` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Travel Management and measurably improves travel management workbench metric without hiding assumptions.

**Improvement:** Promote `duty-of-care risk intelligence` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `travel_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `unused-ticket optimization` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Travel Management and measurably improves travel management risk score without hiding assumptions.

**Improvement:** Promote `unused-ticket optimization` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `travel_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `carbon-aware booking comparison` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Travel Management and measurably improves travel management workbench metric without hiding assumptions.

**Improvement:** Promote `carbon-aware booking comparison` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `travel_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `traveler-aware policy guidance` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Travel Management and measurably improves travel management risk score without hiding assumptions.

**Improvement:** Promote `traveler-aware policy guidance` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `travel_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `disruption counterfactual routing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Travel Management and measurably improves travel management workbench metric without hiding assumptions.

**Improvement:** Promote `disruption counterfactual routing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `travel_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `semantic itinerary ingestion` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Travel Management and measurably improves travel management risk score without hiding assumptions.

**Improvement:** Promote `semantic itinerary ingestion` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `travel_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `duty-of-care risk intelligence` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Travel Management and measurably improves travel management workbench metric without hiding assumptions.

**Improvement:** Promote `duty-of-care risk intelligence` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `travel_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `travel_approval_policy` and `advance_booking_days`

**Justification:** Complete Travel Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `travel_approval_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `advance_booking_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `fare_class_policy` and `hotel_rate_limit`

**Justification:** Complete Travel Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `fare_class_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `hotel_rate_limit` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `hotel_rate_policy` and `risk_alert_threshold`

**Justification:** Complete Travel Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `hotel_rate_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `risk_alert_threshold` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `duty_of_care_policy` and `unused_ticket_warning_days`

**Justification:** Complete Travel Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `duty_of_care_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `unused_ticket_warning_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `unused_ticket_policy` and `approval_amount_limit`

**Justification:** Complete Travel Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `unused_ticket_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `approval_amount_limit` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `travel workbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Travel Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `travel workbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `trip request board` into a full specialist command center

**Justification:** The PBC UI must expose the complete Travel Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `trip request board` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `booking intent console` into a full specialist command center

**Justification:** The PBC UI must expose the complete Travel Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `booking intent console` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `itinerary timeline` into a full specialist command center

**Justification:** The PBC UI must expose the complete Travel Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `itinerary timeline` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `duty of care map` into a full specialist command center

**Justification:** The PBC UI must expose the complete Travel Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `duty of care map` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /travel-requests` and `EmployeeCreated`

**Justification:** Travel Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /travel-requests` and consumed event `EmployeeCreated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /travel-bookings` and `ExpenseReportCreated`

**Justification:** Travel Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /travel-bookings` and consumed event `ExpenseReportCreated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /itineraries` and `PolicyChanged`

**Justification:** Travel Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /itineraries` and consumed event `PolicyChanged` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /policy-checks` and `PaymentExecuted`

**Justification:** Travel Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /policy-checks` and consumed event `PaymentExecuted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Travel Management

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Travel Management

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Travel Management

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Travel Management

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Travel Management

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Travel Management

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
