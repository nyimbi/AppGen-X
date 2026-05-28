# Production Scheduling and Floor Control PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `production_control`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.
- Representative owned tables: `production_control_work_center`, `production_control_production_order`, `production_control_routing_step`, `production_control_production_schedule`, `production_control_dispatch_list`, `production_control_operation_confirmation`, `production_control_downtime_event`, `production_control_material_consumption`, `production_control_wip_inventory`, `production_control_labor_time_booking`, `production_control_machine_time_booking`, `production_control_quality_gate_result`, ...
- Representative operations/APIs: `command_production_orders`, `command_downtime`, `record_execution_records`, `query_schedule`.
- Representative events: `ProductionCompleted`, `AssetPlacedInService`, `DowntimeCaptured`, `MaterialConsumptionRecorded`, `LaborTimeBooked`, `MachineTimeBooked`, `QualityGateRecorded`, `ScrapReworkCaptured`.
- Representative advanced capabilities: `event_sourced_production_lifecycle`, `graph_relational_routing_work_center_topology`, `multi_tenant_site_execution_isolation`, `schema_evolution_resilient_production_schema`, `probabilistic_downtime_yield_schedule_risk_scoring`, `real_time_oee_execution_analytics`, `counterfactual_dispatch_capacity_simulation`, `temporal_throughput_downtime_forecasting`, `autonomous_production_exception_resolution`, `semantic_shop_floor_instruction_parsing`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `production_control_work_center`

**Justification:** This owned table is part of the Production Scheduling and Floor Control operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.

**Improvement:** Extend `production_control_work_center` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `work_center_master`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `production_control_production_order`

**Justification:** This owned table is part of the Production Scheduling and Floor Control operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.

**Improvement:** Extend `production_control_production_order` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `routing_step_definition`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `production_control_routing_step`

**Justification:** This owned table is part of the Production Scheduling and Floor Control operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.

**Improvement:** Extend `production_control_routing_step` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `production_order_creation`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `production_control_production_schedule`

**Justification:** This owned table is part of the Production Scheduling and Floor Control operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.

**Improvement:** Extend `production_control_production_schedule` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `finite_capacity_scheduling`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `production_control_dispatch_list`

**Justification:** This owned table is part of the Production Scheduling and Floor Control operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.

**Improvement:** Extend `production_control_dispatch_list` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `dispatch_list`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `production_control_operation_confirmation`

**Justification:** This owned table is part of the Production Scheduling and Floor Control operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.

**Improvement:** Extend `production_control_operation_confirmation` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `operation_sequencing`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `production_control_downtime_event`

**Justification:** This owned table is part of the Production Scheduling and Floor Control operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.

**Improvement:** Extend `production_control_downtime_event` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `production_start`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `production_control_material_consumption`

**Justification:** This owned table is part of the Production Scheduling and Floor Control operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.

**Improvement:** Extend `production_control_material_consumption` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `operation_confirmation`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `production_control_wip_inventory`

**Justification:** This owned table is part of the Production Scheduling and Floor Control operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.

**Improvement:** Extend `production_control_wip_inventory` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `production_completion`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `production_control_labor_time_booking`

**Justification:** This owned table is part of the Production Scheduling and Floor Control operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Routings, work centers, capacity, assembly sequencing, OEE, downtime, execution records, and completion evidence.

**Improvement:** Extend `production_control_labor_time_booking` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `downtime_capture`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `command_production_orders` a complete command lifecycle

**Justification:** High-value users need `command_production_orders` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_production_orders` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ProductionCompleted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `command_downtime` a complete command lifecycle

**Justification:** High-value users need `command_downtime` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_downtime` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `AssetPlacedInService`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `record_execution_records` a complete command lifecycle

**Justification:** High-value users need `record_execution_records` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `record_execution_records` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DowntimeCaptured`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Turn `query_schedule` into an expert read-model experience

**Justification:** Domain experts rely on `query_schedule` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_schedule` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `MaterialConsumptionRecorded` last changed the projection, and where uncertainty or missing data affects confidence.

### 15. Make `command_production_orders` a complete command lifecycle

**Justification:** High-value users need `command_production_orders` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_production_orders` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `LaborTimeBooked`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `command_downtime` a complete command lifecycle

**Justification:** High-value users need `command_downtime` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_downtime` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MachineTimeBooked`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `record_execution_records` a complete command lifecycle

**Justification:** High-value users need `record_execution_records` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `record_execution_records` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `QualityGateRecorded`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Turn `query_schedule` into an expert read-model experience

**Justification:** Domain experts rely on `query_schedule` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_schedule` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `ScrapReworkCaptured` last changed the projection, and where uncertainty or missing data affects confidence.

### 19. Make `command_production_orders` a complete command lifecycle

**Justification:** High-value users need `command_production_orders` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_production_orders` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `ProductionCompleted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `command_downtime` a complete command lifecycle

**Justification:** High-value users need `command_downtime` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_downtime` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `AssetPlacedInService`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_production_lifecycle` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Production Scheduling and Floor Control and measurably improves plan adherence without hiding assumptions.

**Improvement:** Promote `event_sourced_production_lifecycle` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `plan_adherence`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `graph_relational_routing_work_center_topology` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Production Scheduling and Floor Control and measurably improves yield rate without hiding assumptions.

**Improvement:** Promote `graph_relational_routing_work_center_topology` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `yield_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `multi_tenant_site_execution_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Production Scheduling and Floor Control and measurably improves downtime minutes without hiding assumptions.

**Improvement:** Promote `multi_tenant_site_execution_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `downtime_minutes`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `schema_evolution_resilient_production_schema` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Production Scheduling and Floor Control and measurably improves quality escape rate without hiding assumptions.

**Improvement:** Promote `schema_evolution_resilient_production_schema` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `quality_escape_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `probabilistic_downtime_yield_schedule_risk_scoring` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Production Scheduling and Floor Control and measurably improves production completed throughput without hiding assumptions.

**Improvement:** Promote `probabilistic_downtime_yield_schedule_risk_scoring` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `production_completed_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `real_time_oee_execution_analytics` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Production Scheduling and Floor Control and measurably improves asset placed in service throughput without hiding assumptions.

**Improvement:** Promote `real_time_oee_execution_analytics` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `asset_placed_in_service_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `counterfactual_dispatch_capacity_simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Production Scheduling and Floor Control and measurably improves plan adherence without hiding assumptions.

**Improvement:** Promote `counterfactual_dispatch_capacity_simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `plan_adherence`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `temporal_throughput_downtime_forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Production Scheduling and Floor Control and measurably improves yield rate without hiding assumptions.

**Improvement:** Promote `temporal_throughput_downtime_forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `yield_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `autonomous_production_exception_resolution` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Production Scheduling and Floor Control and measurably improves downtime minutes without hiding assumptions.

**Improvement:** Promote `autonomous_production_exception_resolution` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `downtime_minutes`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic_shop_floor_instruction_parsing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Production Scheduling and Floor Control and measurably improves quality escape rate without hiding assumptions.

**Improvement:** Promote `semantic_shop_floor_instruction_parsing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `quality_escape_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `PRODUCTION_CONTROL_DATABASE_URL` and `PRODUCTION_CONTROL_DATABASE_URL`

**Justification:** Complete Production Scheduling and Floor Control coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `PRODUCTION_CONTROL_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `PRODUCTION_CONTROL_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `PRODUCTION_CONTROL_EVENT_TOPIC` and `PRODUCTION_CONTROL_EVENT_TOPIC`

**Justification:** Complete Production Scheduling and Floor Control coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `PRODUCTION_CONTROL_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `PRODUCTION_CONTROL_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `PRODUCTION_CONTROL_RETRY_LIMIT` and `PRODUCTION_CONTROL_RETRY_LIMIT`

**Justification:** Complete Production Scheduling and Floor Control coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `PRODUCTION_CONTROL_RETRY_LIMIT` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `PRODUCTION_CONTROL_RETRY_LIMIT` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `PRODUCTION_CONTROL_DATABASE_URL` and `PRODUCTION_CONTROL_DATABASE_URL`

**Justification:** Complete Production Scheduling and Floor Control coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `PRODUCTION_CONTROL_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `PRODUCTION_CONTROL_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `PRODUCTION_CONTROL_EVENT_TOPIC` and `PRODUCTION_CONTROL_EVENT_TOPIC`

**Justification:** Complete Production Scheduling and Floor Control coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `PRODUCTION_CONTROL_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `PRODUCTION_CONTROL_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `ProductionControlWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Production Scheduling and Floor Control surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `ProductionControlWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `ProductionControlDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Production Scheduling and Floor Control surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `ProductionControlDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `ProductionExecutionLedger` into a full specialist command center

**Justification:** The PBC UI must expose the complete Production Scheduling and Floor Control surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `ProductionExecutionLedger` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `ProductionQualityConsole` into a full specialist command center

**Justification:** The PBC UI must expose the complete Production Scheduling and Floor Control surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `ProductionQualityConsole` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `ProductionControlWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Production Scheduling and Floor Control surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `ProductionControlWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /production-orders` and `PlannedOrderReleased`

**Justification:** Production Scheduling and Floor Control must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /production-orders` and consumed event `PlannedOrderReleased` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /downtime` and `MaintenanceCompleted`

**Justification:** Production Scheduling and Floor Control must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /downtime` and consumed event `MaintenanceCompleted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /material-consumptions` and `PlannedOrderReleased`

**Justification:** Production Scheduling and Floor Control must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /material-consumptions` and consumed event `PlannedOrderReleased` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /labor-time` and `MaintenanceCompleted`

**Justification:** Production Scheduling and Floor Control must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /labor-time` and consumed event `MaintenanceCompleted` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Production Scheduling and Floor Control

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Production Scheduling and Floor Control

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Production Scheduling and Floor Control

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Production Scheduling and Floor Control

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Production Scheduling and Floor Control

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Production Scheduling and Floor Control

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
