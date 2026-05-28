# Material Requirements Planning Engine PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `mrp_engine`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.
- Representative owned tables: `mrp_engine_bill_of_material`, `mrp_engine_bom_revision`, `mrp_engine_bom_component`, `mrp_engine_item_planning_profile`, `mrp_engine_material_demand`, `mrp_engine_inventory_projection`, `mrp_engine_capacity_projection`, `mrp_engine_mrp_run`, `mrp_engine_mrp_run_item`, `mrp_engine_planned_order`, `mrp_engine_planned_purchase_suggestion`, `mrp_engine_planned_production_order`, ...
- Representative operations/APIs: `command_mrp_boms`, `command_mrp_demand_projections`, `command_mrp_inventory_projections`, `command_mrp_runs`, `command_mrp_runs_id_calculate`, `command_mrp_planned_orders_id_release`, `command_mrp_events_inbox`, `query_mrp_workbench`.
- Representative events: `BomRegistered`, `DemandProjectionIngested`, `InventoryProjectionIngested`, `MrpRunStarted`, `MaterialShortageDetected`, `PlannedOrderReleased`.
- Representative advanced capabilities: `event_sourced_planning_lifecycle`, `graph_relational_bom_topology`, `multi_tenant_site_planning_isolation`, `schema_evolution_resilient_planning_schema`, `probabilistic_shortage_capacity_risk_scoring`, `real_time_material_plan_analytics`, `counterfactual_planning_policy_simulation`, `temporal_demand_shortage_forecasting`, `autonomous_planning_exception_resolution`, `semantic_demand_bom_instruction_parsing`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `mrp_engine_bill_of_material`

**Justification:** This owned table is part of the Material Requirements Planning Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.

**Improvement:** Extend `mrp_engine_bill_of_material` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `bom_master`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `mrp_engine_bom_revision`

**Justification:** This owned table is part of the Material Requirements Planning Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.

**Improvement:** Extend `mrp_engine_bom_revision` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `bom_revision_control`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `mrp_engine_bom_component`

**Justification:** This owned table is part of the Material Requirements Planning Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.

**Improvement:** Extend `mrp_engine_bom_component` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `bom_component_control`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `mrp_engine_item_planning_profile`

**Justification:** This owned table is part of the Material Requirements Planning Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.

**Improvement:** Extend `mrp_engine_item_planning_profile` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `alternate_bom`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `mrp_engine_material_demand`

**Justification:** This owned table is part of the Material Requirements Planning Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.

**Improvement:** Extend `mrp_engine_material_demand` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `substitution_rule`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `mrp_engine_inventory_projection`

**Justification:** This owned table is part of the Material Requirements Planning Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.

**Improvement:** Extend `mrp_engine_inventory_projection` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `item_planning_profile`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `mrp_engine_capacity_projection`

**Justification:** This owned table is part of the Material Requirements Planning Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.

**Improvement:** Extend `mrp_engine_capacity_projection` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `item_source_rule`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `mrp_engine_mrp_run`

**Justification:** This owned table is part of the Material Requirements Planning Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.

**Improvement:** Extend `mrp_engine_mrp_run` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `bom_explosion`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `mrp_engine_mrp_run_item`

**Justification:** This owned table is part of the Material Requirements Planning Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.

**Improvement:** Extend `mrp_engine_mrp_run_item` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `demand_projection`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `mrp_engine_planned_order`

**Justification:** This owned table is part of the Material Requirements Planning Engine operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by BOM graph analysis, demand/supply/capacity projections, planning runs, shortages, pegging, release routes, and governed material plans.

**Improvement:** Extend `mrp_engine_planned_order` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `demand_projection_lines`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `command_mrp_boms` a complete command lifecycle

**Justification:** High-value users need `command_mrp_boms` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_mrp_boms` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `BomRegistered`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `command_mrp_demand_projections` a complete command lifecycle

**Justification:** High-value users need `command_mrp_demand_projections` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_mrp_demand_projections` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DemandProjectionIngested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `command_mrp_inventory_projections` a complete command lifecycle

**Justification:** High-value users need `command_mrp_inventory_projections` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_mrp_inventory_projections` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `InventoryProjectionIngested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `command_mrp_runs` a complete command lifecycle

**Justification:** High-value users need `command_mrp_runs` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_mrp_runs` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MrpRunStarted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `command_mrp_runs_id_calculate` a complete command lifecycle

**Justification:** High-value users need `command_mrp_runs_id_calculate` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_mrp_runs_id_calculate` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MaterialShortageDetected`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `command_mrp_planned_orders_id_release` a complete command lifecycle

**Justification:** High-value users need `command_mrp_planned_orders_id_release` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_mrp_planned_orders_id_release` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PlannedOrderReleased`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `command_mrp_events_inbox` a complete command lifecycle

**Justification:** High-value users need `command_mrp_events_inbox` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_mrp_events_inbox` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `BomRegistered`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Turn `query_mrp_workbench` into an expert read-model experience

**Justification:** Domain experts rely on `query_mrp_workbench` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_mrp_workbench` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `DemandProjectionIngested` last changed the projection, and where uncertainty or missing data affects confidence.

### 19. Make `command_mrp_boms` a complete command lifecycle

**Justification:** High-value users need `command_mrp_boms` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_mrp_boms` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `InventoryProjectionIngested`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `command_mrp_demand_projections` a complete command lifecycle

**Justification:** High-value users need `command_mrp_demand_projections` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_mrp_demand_projections` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MrpRunStarted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_planning_lifecycle` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Material Requirements Planning Engine and measurably improves plan adherence without hiding assumptions.

**Improvement:** Promote `event_sourced_planning_lifecycle` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `plan_adherence`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `graph_relational_bom_topology` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Material Requirements Planning Engine and measurably improves yield rate without hiding assumptions.

**Improvement:** Promote `graph_relational_bom_topology` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `yield_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `multi_tenant_site_planning_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Material Requirements Planning Engine and measurably improves downtime minutes without hiding assumptions.

**Improvement:** Promote `multi_tenant_site_planning_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `downtime_minutes`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `schema_evolution_resilient_planning_schema` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Material Requirements Planning Engine and measurably improves quality escape rate without hiding assumptions.

**Improvement:** Promote `schema_evolution_resilient_planning_schema` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `quality_escape_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `probabilistic_shortage_capacity_risk_scoring` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Material Requirements Planning Engine and measurably improves bom registered throughput without hiding assumptions.

**Improvement:** Promote `probabilistic_shortage_capacity_risk_scoring` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `bom_registered_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `real_time_material_plan_analytics` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Material Requirements Planning Engine and measurably improves demand projection ingested throughput without hiding assumptions.

**Improvement:** Promote `real_time_material_plan_analytics` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `demand_projection_ingested_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `counterfactual_planning_policy_simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Material Requirements Planning Engine and measurably improves plan adherence without hiding assumptions.

**Improvement:** Promote `counterfactual_planning_policy_simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `plan_adherence`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `temporal_demand_shortage_forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Material Requirements Planning Engine and measurably improves yield rate without hiding assumptions.

**Improvement:** Promote `temporal_demand_shortage_forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `yield_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `autonomous_planning_exception_resolution` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Material Requirements Planning Engine and measurably improves downtime minutes without hiding assumptions.

**Improvement:** Promote `autonomous_planning_exception_resolution` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `downtime_minutes`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic_demand_bom_instruction_parsing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Material Requirements Planning Engine and measurably improves quality escape rate without hiding assumptions.

**Improvement:** Promote `semantic_demand_bom_instruction_parsing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `quality_escape_rate`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `MRP_ENGINE_DATABASE_URL` and `MRP_ENGINE_DATABASE_URL`

**Justification:** Complete Material Requirements Planning Engine coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `MRP_ENGINE_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `MRP_ENGINE_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `MRP_ENGINE_EVENT_TOPIC` and `MRP_ENGINE_EVENT_TOPIC`

**Justification:** Complete Material Requirements Planning Engine coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `MRP_ENGINE_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `MRP_ENGINE_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `MRP_ENGINE_RETRY_LIMIT` and `MRP_ENGINE_RETRY_LIMIT`

**Justification:** Complete Material Requirements Planning Engine coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `MRP_ENGINE_RETRY_LIMIT` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `MRP_ENGINE_RETRY_LIMIT` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `MRP_ENGINE_DATABASE_URL` and `MRP_ENGINE_DATABASE_URL`

**Justification:** Complete Material Requirements Planning Engine coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `MRP_ENGINE_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `MRP_ENGINE_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `MRP_ENGINE_EVENT_TOPIC` and `MRP_ENGINE_EVENT_TOPIC`

**Justification:** Complete Material Requirements Planning Engine coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `MRP_ENGINE_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `MRP_ENGINE_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `MrpEngineWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Material Requirements Planning Engine surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `MrpEngineWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `MrpEngineDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Material Requirements Planning Engine surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `MrpEngineDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `MrpEngineWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Material Requirements Planning Engine surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `MrpEngineWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `MrpEngineDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Material Requirements Planning Engine surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `MrpEngineDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `MrpEngineWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Material Requirements Planning Engine surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `MrpEngineWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /mrp/boms` and `InventoryReleased`

**Justification:** Material Requirements Planning Engine must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /mrp/boms` and consumed event `InventoryReleased` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /mrp/demand-projections` and `OrderVerified`

**Justification:** Material Requirements Planning Engine must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /mrp/demand-projections` and consumed event `OrderVerified` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /mrp/inventory-projections` and `ForecastUpdated`

**Justification:** Material Requirements Planning Engine must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /mrp/inventory-projections` and consumed event `ForecastUpdated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /mrp/runs` and `ProductionCapacityChanged`

**Justification:** Material Requirements Planning Engine must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /mrp/runs` and consumed event `ProductionCapacityChanged` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Material Requirements Planning Engine

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Material Requirements Planning Engine

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Material Requirements Planning Engine

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Material Requirements Planning Engine

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Material Requirements Planning Engine

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Material Requirements Planning Engine

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
