# Facilities and Space Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `facilities_space_management`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.
- Representative owned tables: `facilities_space_management_facility_site`, `facilities_space_management_facility_floor`, `facilities_space_management_space_record`, `facilities_space_management_space_type`, `facilities_space_management_occupancy_plan`, `facilities_space_management_occupancy_assignment`, `facilities_space_management_space_reservation`, `facilities_space_management_move_request`, `facilities_space_management_move_task`, `facilities_space_management_maintenance_signal`, `facilities_space_management_space_availability_snapshot`, `facilities_space_management_access_constraint`, ...
- Representative operations/APIs: `create_facility_site`, `define_floor`, `create_space_record`, `classify_space_type`, `create_occupancy_plan`, `assign_occupant`, `reserve_space`, `open_move_request`, `complete_move_task`, `record_maintenance_signal`, `publish_availability_snapshot`, `define_access_constraint`, ...
- Representative events: `FacilityCreated`, `SpaceReserved`, `MoveRequested`, `MaintenanceSignalRecorded`, `SafetyInspectionRecorded`, `CapacityPlanPublished`.
- Representative advanced capabilities: `space demand forecasting`, `reservation conflict optimization`, `occupancy scenario simulation`, `safety-risk scoring`, `maintenance-aware availability`, `hybrid workplace recommendation`.

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `facilities_space_management_facility_site`

**Justification:** This owned table is part of the Facilities and Space Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.

**Improvement:** Extend `facilities_space_management_facility_site` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `facility_site_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `facilities_space_management_facility_floor`

**Justification:** This owned table is part of the Facilities and Space Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.

**Improvement:** Extend `facilities_space_management_facility_floor` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `facilities_space_management_workflow`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `facilities_space_management_space_record`

**Justification:** This owned table is part of the Facilities and Space Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.

**Improvement:** Extend `facilities_space_management_space_record` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `facilities_space_management_analytics`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `facilities_space_management_space_type`

**Justification:** This owned table is part of the Facilities and Space Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.

**Improvement:** Extend `facilities_space_management_space_type` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `configuration_schema`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `facilities_space_management_occupancy_plan`

**Justification:** This owned table is part of the Facilities and Space Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.

**Improvement:** Extend `facilities_space_management_occupancy_plan` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `rule_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `facilities_space_management_occupancy_assignment`

**Justification:** This owned table is part of the Facilities and Space Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.

**Improvement:** Extend `facilities_space_management_occupancy_assignment` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `parameter_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `facilities_space_management_space_reservation`

**Justification:** This owned table is part of the Facilities and Space Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.

**Improvement:** Extend `facilities_space_management_space_reservation` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `owned_schema_migrations_models`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `facilities_space_management_move_request`

**Justification:** This owned table is part of the Facilities and Space Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.

**Improvement:** Extend `facilities_space_management_move_request` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `appgen_x_outbox_inbox_eventing`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `facilities_space_management_move_task`

**Justification:** This owned table is part of the Facilities and Space Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.

**Improvement:** Extend `facilities_space_management_move_task` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `idempotent_handlers`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `facilities_space_management_maintenance_signal`

**Justification:** This owned table is part of the Facilities and Space Management operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.

**Improvement:** Extend `facilities_space_management_maintenance_signal` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `retry_dead_letter_evidence`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `create_facility_site` a complete command lifecycle

**Justification:** High-value users need `create_facility_site` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_facility_site` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `FacilityCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `define_floor` a complete command lifecycle

**Justification:** High-value users need `define_floor` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `define_floor` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `SpaceReserved`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `create_space_record` a complete command lifecycle

**Justification:** High-value users need `create_space_record` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_space_record` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MoveRequested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `classify_space_type` a complete command lifecycle

**Justification:** High-value users need `classify_space_type` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `classify_space_type` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MaintenanceSignalRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `create_occupancy_plan` a complete command lifecycle

**Justification:** High-value users need `create_occupancy_plan` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_occupancy_plan` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `SafetyInspectionRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `assign_occupant` a complete command lifecycle

**Justification:** High-value users need `assign_occupant` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `assign_occupant` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `CapacityPlanPublished`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `reserve_space` a complete command lifecycle

**Justification:** High-value users need `reserve_space` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `reserve_space` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `FacilityCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `open_move_request` a complete command lifecycle

**Justification:** High-value users need `open_move_request` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `open_move_request` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `SpaceReserved`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `complete_move_task` a complete command lifecycle

**Justification:** High-value users need `complete_move_task` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `complete_move_task` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MoveRequested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `record_maintenance_signal` a complete command lifecycle

**Justification:** High-value users need `record_maintenance_signal` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `record_maintenance_signal` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MaintenanceSignalRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `space demand forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Facilities and Space Management and measurably improves facilities space management risk score without hiding assumptions.

**Improvement:** Promote `space demand forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `facilities_space_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `reservation conflict optimization` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Facilities and Space Management and measurably improves facilities space management workbench metric without hiding assumptions.

**Improvement:** Promote `reservation conflict optimization` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `facilities_space_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `occupancy scenario simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Facilities and Space Management and measurably improves facilities space management risk score without hiding assumptions.

**Improvement:** Promote `occupancy scenario simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `facilities_space_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `safety-risk scoring` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Facilities and Space Management and measurably improves facilities space management workbench metric without hiding assumptions.

**Improvement:** Promote `safety-risk scoring` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `facilities_space_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `maintenance-aware availability` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Facilities and Space Management and measurably improves facilities space management risk score without hiding assumptions.

**Improvement:** Promote `maintenance-aware availability` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `facilities_space_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `hybrid workplace recommendation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Facilities and Space Management and measurably improves facilities space management workbench metric without hiding assumptions.

**Improvement:** Promote `hybrid workplace recommendation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `facilities_space_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `space demand forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Facilities and Space Management and measurably improves facilities space management risk score without hiding assumptions.

**Improvement:** Promote `space demand forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `facilities_space_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `reservation conflict optimization` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Facilities and Space Management and measurably improves facilities space management workbench metric without hiding assumptions.

**Improvement:** Promote `reservation conflict optimization` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `facilities_space_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `occupancy scenario simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Facilities and Space Management and measurably improves facilities space management risk score without hiding assumptions.

**Improvement:** Promote `occupancy scenario simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `facilities_space_management_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `safety-risk scoring` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Facilities and Space Management and measurably improves facilities space management workbench metric without hiding assumptions.

**Improvement:** Promote `safety-risk scoring` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `facilities_space_management_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `space_reservation_policy` and `reservation_horizon_days`

**Justification:** Complete Facilities and Space Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `space_reservation_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `reservation_horizon_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `occupancy_policy` and `occupancy_capacity_buffer`

**Justification:** Complete Facilities and Space Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `occupancy_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `occupancy_capacity_buffer` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `move_policy` and `move_sla_days`

**Justification:** Complete Facilities and Space Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `move_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `move_sla_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `maintenance_block_policy` and `utilization_warning_percent`

**Justification:** Complete Facilities and Space Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `maintenance_block_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `utilization_warning_percent` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `safety_policy` and `safety_review_days`

**Justification:** Complete Facilities and Space Management coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `safety_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `safety_review_days` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `facilities workbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Facilities and Space Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `facilities workbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `space map` into a full specialist command center

**Justification:** The PBC UI must expose the complete Facilities and Space Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `space map` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `reservation calendar` into a full specialist command center

**Justification:** The PBC UI must expose the complete Facilities and Space Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `reservation calendar` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `move board` into a full specialist command center

**Justification:** The PBC UI must expose the complete Facilities and Space Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `move board` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `maintenance block panel` into a full specialist command center

**Justification:** The PBC UI must expose the complete Facilities and Space Management surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `maintenance block panel` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /facility-sites` and `EmployeeCreated`

**Justification:** Facilities and Space Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /facility-sites` and consumed event `EmployeeCreated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /buildings` and `WorkOrderCompleted`

**Justification:** Facilities and Space Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /buildings` and consumed event `WorkOrderCompleted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /spaces` and `AccessPolicyChanged`

**Justification:** Facilities and Space Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /spaces` and consumed event `AccessPolicyChanged` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /space-reservations` and `PolicyChanged`

**Justification:** Facilities and Space Management must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /space-reservations` and consumed event `PolicyChanged` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Facilities and Space Management

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Facilities and Space Management

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Facilities and Space Management

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Facilities and Space Management

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Facilities and Space Management

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Facilities and Space Management

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
