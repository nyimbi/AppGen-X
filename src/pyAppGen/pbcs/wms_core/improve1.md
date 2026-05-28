# Warehouse Management Core PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `wms_core`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Putaway, picking, packing, cross-docking, and warehouse edge workflows.
- Representative owned tables: `wms_core_warehouse`, `wms_core_warehouse_zone`, `wms_core_bin_location`, `wms_core_inbound_receipt`, `wms_core_inbound_receipt_line`, `wms_core_dock_door`, `wms_core_dock_appointment`, `wms_core_putaway_task`, `wms_core_pick_wave`, `wms_core_pick_task`, `wms_core_pack_task`, `wms_core_shipment_confirmation`, ...
- Representative operations/APIs: `command_wms_warehouses`, `command_wms_inbound`, `command_wms_putaway`, `command_wms_pick_waves`, `command_wms_pack_tasks`, `command_wms_shipments`, `query_wms_workbench`.
- Representative events: `WarehouseRegistered`, `BinRegistered`, `GoodsReceiptPosted`, `PutawayTaskCreated`, `PutawayConfirmed`, `PickWaveReleased`, `Picked`, `PackTaskCreated`, `Packed`, `OrderShipped`.
- Representative advanced capabilities: `event_sourced_warehouse_lifecycle`, `graph_relational_warehouse_topology`, `multi_tenant_warehouse_isolation`, `schema_evolution_resilient_warehouse_schema`, `probabilistic_putaway_pick_estimation`, `real_time_warehouse_execution_analytics`, `counterfactual_wave_labor_simulation`, `temporal_throughput_dock_forecasting`, `autonomous_exception_resolution`, `semantic_warehouse_event_parsing`, ...

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `wms_core_warehouse`

**Justification:** This owned table is part of the Warehouse Management Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Putaway, picking, packing, cross-docking, and warehouse edge workflows.

**Improvement:** Extend `wms_core_warehouse` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `warehouse_master`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `wms_core_warehouse_zone`

**Justification:** This owned table is part of the Warehouse Management Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Putaway, picking, packing, cross-docking, and warehouse edge workflows.

**Improvement:** Extend `wms_core_warehouse_zone` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `warehouse_zone_master`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `wms_core_bin_location`

**Justification:** This owned table is part of the Warehouse Management Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Putaway, picking, packing, cross-docking, and warehouse edge workflows.

**Improvement:** Extend `wms_core_bin_location` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `warehouse_calendar`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `wms_core_inbound_receipt`

**Justification:** This owned table is part of the Warehouse Management Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Putaway, picking, packing, cross-docking, and warehouse edge workflows.

**Improvement:** Extend `wms_core_inbound_receipt` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `warehouse_identity`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `wms_core_inbound_receipt_line`

**Justification:** This owned table is part of the Warehouse Management Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Putaway, picking, packing, cross-docking, and warehouse edge workflows.

**Improvement:** Extend `wms_core_inbound_receipt_line` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `bin_location_master`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `wms_core_dock_door`

**Justification:** This owned table is part of the Warehouse Management Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Putaway, picking, packing, cross-docking, and warehouse edge workflows.

**Improvement:** Extend `wms_core_dock_door` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `bin_attributes`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `wms_core_dock_appointment`

**Justification:** This owned table is part of the Warehouse Management Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Putaway, picking, packing, cross-docking, and warehouse edge workflows.

**Improvement:** Extend `wms_core_dock_appointment` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `bin_capacity_snapshots`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `wms_core_putaway_task`

**Justification:** This owned table is part of the Warehouse Management Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Putaway, picking, packing, cross-docking, and warehouse edge workflows.

**Improvement:** Extend `wms_core_putaway_task` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `inbound_receipt`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `wms_core_pick_wave`

**Justification:** This owned table is part of the Warehouse Management Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Putaway, picking, packing, cross-docking, and warehouse edge workflows.

**Improvement:** Extend `wms_core_pick_wave` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `receipt_lines`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `wms_core_pick_task`

**Justification:** This owned table is part of the Warehouse Management Core operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Putaway, picking, packing, cross-docking, and warehouse edge workflows.

**Improvement:** Extend `wms_core_pick_task` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `dock_door_registration`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `command_wms_warehouses` a complete command lifecycle

**Justification:** High-value users need `command_wms_warehouses` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_wms_warehouses` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `WarehouseRegistered`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `command_wms_inbound` a complete command lifecycle

**Justification:** High-value users need `command_wms_inbound` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_wms_inbound` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `BinRegistered`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `command_wms_putaway` a complete command lifecycle

**Justification:** High-value users need `command_wms_putaway` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_wms_putaway` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GoodsReceiptPosted`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `command_wms_pick_waves` a complete command lifecycle

**Justification:** High-value users need `command_wms_pick_waves` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_wms_pick_waves` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PutawayTaskCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `command_wms_pack_tasks` a complete command lifecycle

**Justification:** High-value users need `command_wms_pack_tasks` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_wms_pack_tasks` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PutawayConfirmed`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `command_wms_shipments` a complete command lifecycle

**Justification:** High-value users need `command_wms_shipments` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_wms_shipments` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PickWaveReleased`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Turn `query_wms_workbench` into an expert read-model experience

**Justification:** Domain experts rely on `query_wms_workbench` for operational decisions; a world-class read path must be explainable, filterable, temporally accurate, and safe under stale projections.

**Improvement:** Build `query_wms_workbench` as a dedicated query contract with projection freshness, filter validation, pagination, saved views, temporal/as-of reads, row-level permissions, traceable source records, and UI drilldowns. Add agent explanations for how the answer was produced, what events like `Picked` last changed the projection, and where uncertainty or missing data affects confidence.

### 18. Make `command_wms_warehouses` a complete command lifecycle

**Justification:** High-value users need `command_wms_warehouses` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_wms_warehouses` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `PackTaskCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `command_wms_inbound` a complete command lifecycle

**Justification:** High-value users need `command_wms_inbound` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_wms_inbound` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `Packed`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `command_wms_putaway` a complete command lifecycle

**Justification:** High-value users need `command_wms_putaway` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `command_wms_putaway` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `OrderShipped`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `event_sourced_warehouse_lifecycle` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Warehouse Management Core and measurably improves availability accuracy without hiding assumptions.

**Improvement:** Promote `event_sourced_warehouse_lifecycle` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `availability_accuracy`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `graph_relational_warehouse_topology` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Warehouse Management Core and measurably improves cycle time without hiding assumptions.

**Improvement:** Promote `graph_relational_warehouse_topology` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `multi_tenant_warehouse_isolation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Warehouse Management Core and measurably improves service level without hiding assumptions.

**Improvement:** Promote `multi_tenant_warehouse_isolation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `service_level`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `schema_evolution_resilient_warehouse_schema` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Warehouse Management Core and measurably improves exception backlog without hiding assumptions.

**Improvement:** Promote `schema_evolution_resilient_warehouse_schema` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `exception_backlog`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `probabilistic_putaway_pick_estimation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Warehouse Management Core and measurably improves warehouse registered throughput without hiding assumptions.

**Improvement:** Promote `probabilistic_putaway_pick_estimation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `warehouse_registered_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `real_time_warehouse_execution_analytics` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Warehouse Management Core and measurably improves bin registered throughput without hiding assumptions.

**Improvement:** Promote `real_time_warehouse_execution_analytics` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `bin_registered_throughput`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `counterfactual_wave_labor_simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Warehouse Management Core and measurably improves availability accuracy without hiding assumptions.

**Improvement:** Promote `counterfactual_wave_labor_simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `availability_accuracy`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `temporal_throughput_dock_forecasting` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Warehouse Management Core and measurably improves cycle time without hiding assumptions.

**Improvement:** Promote `temporal_throughput_dock_forecasting` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `cycle_time`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `autonomous_exception_resolution` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Warehouse Management Core and measurably improves service level without hiding assumptions.

**Improvement:** Promote `autonomous_exception_resolution` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `service_level`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `semantic_warehouse_event_parsing` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Warehouse Management Core and measurably improves exception backlog without hiding assumptions.

**Improvement:** Promote `semantic_warehouse_event_parsing` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `exception_backlog`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `WMS_CORE_DATABASE_URL` and `WMS_CORE_DATABASE_URL`

**Justification:** Complete Warehouse Management Core coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `WMS_CORE_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `WMS_CORE_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `WMS_CORE_EVENT_TOPIC` and `WMS_CORE_EVENT_TOPIC`

**Justification:** Complete Warehouse Management Core coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `WMS_CORE_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `WMS_CORE_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `WMS_CORE_RETRY_LIMIT` and `WMS_CORE_RETRY_LIMIT`

**Justification:** Complete Warehouse Management Core coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `WMS_CORE_RETRY_LIMIT` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `WMS_CORE_RETRY_LIMIT` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `WMS_CORE_DATABASE_URL` and `WMS_CORE_DATABASE_URL`

**Justification:** Complete Warehouse Management Core coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `WMS_CORE_DATABASE_URL` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `WMS_CORE_DATABASE_URL` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `WMS_CORE_EVENT_TOPIC` and `WMS_CORE_EVENT_TOPIC`

**Justification:** Complete Warehouse Management Core coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `WMS_CORE_EVENT_TOPIC` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `WMS_CORE_EVENT_TOPIC` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `WmsCoreWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Warehouse Management Core surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `WmsCoreWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `WmsCoreDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Warehouse Management Core surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `WmsCoreDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `WmsCoreWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Warehouse Management Core surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `WmsCoreWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `WmsCoreDetail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Warehouse Management Core surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `WmsCoreDetail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `WmsCoreWorkbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Warehouse Management Core surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `WmsCoreWorkbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /wms/warehouses` and `InventoryAllocated`

**Justification:** Warehouse Management Core must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /wms/warehouses` and consumed event `InventoryAllocated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /wms/inbound` and `InboundArrived`

**Justification:** Warehouse Management Core must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /wms/inbound` and consumed event `InboundArrived` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /wms/putaway` and `QualityHoldReleased`

**Justification:** Warehouse Management Core must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /wms/putaway` and consumed event `QualityHoldReleased` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /wms/pick-waves` and `CarrierBooked`

**Justification:** Warehouse Management Core must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /wms/pick-waves` and consumed event `CarrierBooked` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Warehouse Management Core

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Warehouse Management Core

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Warehouse Management Core

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Warehouse Management Core

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Warehouse Management Core

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Warehouse Management Core

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
