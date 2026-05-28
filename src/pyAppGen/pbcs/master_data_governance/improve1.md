# Master Data Governance PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `master_data_governance`. Each item is specific to the domain surface currently declared by the PBC and is intended to move the package beyond world-class breadth toward complete specialist-grade coverage.

## Current Domain Evidence Used

- Domain purpose: Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.
- Representative owned tables: `master_data_governance_master_record`, `master_data_governance_master_domain`, `master_data_governance_source_record_link`, `master_data_governance_match_candidate`, `master_data_governance_match_decision`, `master_data_governance_survivorship_rule`, `master_data_governance_survivorship_decision`, `master_data_governance_golden_record_version`, `master_data_governance_hierarchy_node`, `master_data_governance_hierarchy_relationship`, `master_data_governance_data_quality_rule`, `master_data_governance_data_quality_observation`, ...
- Representative operations/APIs: `create_master_record`, `register_master_domain`, `link_source_record`, `generate_match_candidate`, `record_match_decision`, `define_survivorship_rule`, `apply_survivorship`, `publish_golden_version`, `create_hierarchy_node`, `link_hierarchy_relationship`, `define_quality_rule`, `observe_data_quality`, ...
- Representative events: `MasterRecordCreated`, `MatchCandidateGenerated`, `GoldenRecordPublished`, `HierarchyChanged`, `DataQualityChanged`, `MasterDataPublished`.
- Representative advanced capabilities: `probabilistic entity resolution`, `explainable survivorship`, `hierarchy impact simulation`, `quality anomaly detection`, `stewardship workload optimization`, `cryptographic golden record proof`.

## 50 Better-Than-World-Class Improvements

### 1. Deep specialist lifecycle semantics for `master_data_governance_master_record`

**Justification:** This owned table is part of the Master Data Governance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.

**Improvement:** Extend `master_data_governance_master_record` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `master_record_management`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 2. Deep specialist lifecycle semantics for `master_data_governance_master_domain`

**Justification:** This owned table is part of the Master Data Governance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.

**Improvement:** Extend `master_data_governance_master_domain` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `master_data_governance_workflow`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 3. Deep specialist lifecycle semantics for `master_data_governance_source_record_link`

**Justification:** This owned table is part of the Master Data Governance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.

**Improvement:** Extend `master_data_governance_source_record_link` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `master_data_governance_analytics`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 4. Deep specialist lifecycle semantics for `master_data_governance_match_candidate`

**Justification:** This owned table is part of the Master Data Governance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.

**Improvement:** Extend `master_data_governance_match_candidate` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `configuration_schema`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 5. Deep specialist lifecycle semantics for `master_data_governance_match_decision`

**Justification:** This owned table is part of the Master Data Governance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.

**Improvement:** Extend `master_data_governance_match_decision` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `rule_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 6. Deep specialist lifecycle semantics for `master_data_governance_survivorship_rule`

**Justification:** This owned table is part of the Master Data Governance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.

**Improvement:** Extend `master_data_governance_survivorship_rule` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `parameter_engine`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 7. Deep specialist lifecycle semantics for `master_data_governance_survivorship_decision`

**Justification:** This owned table is part of the Master Data Governance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.

**Improvement:** Extend `master_data_governance_survivorship_decision` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `owned_schema_migrations_models`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 8. Deep specialist lifecycle semantics for `master_data_governance_golden_record_version`

**Justification:** This owned table is part of the Master Data Governance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.

**Improvement:** Extend `master_data_governance_golden_record_version` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `appgen_x_outbox_inbox_eventing`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 9. Deep specialist lifecycle semantics for `master_data_governance_hierarchy_node`

**Justification:** This owned table is part of the Master Data Governance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.

**Improvement:** Extend `master_data_governance_hierarchy_node` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `idempotent_handlers`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 10. Deep specialist lifecycle semantics for `master_data_governance_hierarchy_relationship`

**Justification:** This owned table is part of the Master Data Governance operating core; if it remains a generic record, specialists cannot model the real states, exceptions, evidence, and controls implied by Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.

**Improvement:** Extend `master_data_governance_hierarchy_relationship` with domain-specific status values, subtype fields, temporal validity, provenance, quality/control flags, exception reasons, and relationship invariants for `retry_dead_letter_evidence`. Pair the schema with migration DDL, typed model descriptors, command/query services, role-aware UI panels, release tests, and agent-safe CRUD previews so the full lifecycle is explicit and auditable inside the PBC boundary.

### 11. Make `create_master_record` a complete command lifecycle

**Justification:** High-value users need `create_master_record` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_master_record` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MasterRecordCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 12. Make `register_master_domain` a complete command lifecycle

**Justification:** High-value users need `register_master_domain` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `register_master_domain` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MatchCandidateGenerated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 13. Make `link_source_record` a complete command lifecycle

**Justification:** High-value users need `link_source_record` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `link_source_record` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GoldenRecordPublished`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 14. Make `generate_match_candidate` a complete command lifecycle

**Justification:** High-value users need `generate_match_candidate` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `generate_match_candidate` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `HierarchyChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 15. Make `record_match_decision` a complete command lifecycle

**Justification:** High-value users need `record_match_decision` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `record_match_decision` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `DataQualityChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 16. Make `define_survivorship_rule` a complete command lifecycle

**Justification:** High-value users need `define_survivorship_rule` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `define_survivorship_rule` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MasterDataPublished`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 17. Make `apply_survivorship` a complete command lifecycle

**Justification:** High-value users need `apply_survivorship` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `apply_survivorship` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MasterRecordCreated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 18. Make `publish_golden_version` a complete command lifecycle

**Justification:** High-value users need `publish_golden_version` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `publish_golden_version` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `MatchCandidateGenerated`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 19. Make `create_hierarchy_node` a complete command lifecycle

**Justification:** High-value users need `create_hierarchy_node` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `create_hierarchy_node` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `GoldenRecordPublished`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 20. Make `link_hierarchy_relationship` a complete command lifecycle

**Justification:** High-value users need `link_hierarchy_relationship` to cover intake, validation, approval, execution, amendment, cancellation, audit, and exception recovery rather than a happy-path transaction.

**Improvement:** Implement `link_hierarchy_relationship` with idempotency, preflight simulation, permission checks, typed validation, rule evaluation, policy explanations, AppGen-X outbox emission through `HierarchyChanged`, retry/dead-letter evidence, and UI actions for draft, submit, approve, reject, amend, cancel, replay, and evidence export. The PBC agent should preview the mutation, explain risks, and require human confirmation.

### 21. Operationalize `probabilistic entity resolution` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Master Data Governance and measurably improves master data governance risk score without hiding assumptions.

**Improvement:** Promote `probabilistic entity resolution` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `master_data_governance_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 22. Operationalize `explainable survivorship` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Master Data Governance and measurably improves master data governance workbench metric without hiding assumptions.

**Improvement:** Promote `explainable survivorship` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `master_data_governance_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 23. Operationalize `hierarchy impact simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Master Data Governance and measurably improves master data governance risk score without hiding assumptions.

**Improvement:** Promote `hierarchy impact simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `master_data_governance_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 24. Operationalize `quality anomaly detection` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Master Data Governance and measurably improves master data governance workbench metric without hiding assumptions.

**Improvement:** Promote `quality anomaly detection` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `master_data_governance_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 25. Operationalize `stewardship workload optimization` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Master Data Governance and measurably improves master data governance risk score without hiding assumptions.

**Improvement:** Promote `stewardship workload optimization` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `master_data_governance_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 26. Operationalize `cryptographic golden record proof` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Master Data Governance and measurably improves master data governance workbench metric without hiding assumptions.

**Improvement:** Promote `cryptographic golden record proof` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `master_data_governance_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 27. Operationalize `probabilistic entity resolution` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Master Data Governance and measurably improves master data governance risk score without hiding assumptions.

**Improvement:** Promote `probabilistic entity resolution` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `master_data_governance_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 28. Operationalize `explainable survivorship` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Master Data Governance and measurably improves master data governance workbench metric without hiding assumptions.

**Improvement:** Promote `explainable survivorship` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `master_data_governance_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 29. Operationalize `hierarchy impact simulation` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Master Data Governance and measurably improves master data governance risk score without hiding assumptions.

**Improvement:** Promote `hierarchy impact simulation` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `master_data_governance_risk_score`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 30. Operationalize `quality anomaly detection` as a governed decision system

**Justification:** The capability only creates value when it changes specialist decisions inside Master Data Governance and measurably improves master data governance workbench metric without hiding assumptions.

**Improvement:** Promote `quality anomaly detection` into an executable subsystem with model/version metadata, deterministic fallbacks, confidence bands, counterfactual comparisons, drift checks, policy constraints, and user-visible evidence. Surface it as a workbench panel tied to `master_data_governance_workbench_metric`, with drilldowns from recommendation to source records, rules, events, model inputs, approval requirements, and agent rationale.

### 31. Create simulation-grade governance for `matching_policy` and `match_confidence_threshold`

**Justification:** Complete Master Data Governance coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `matching_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `match_confidence_threshold` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 32. Create simulation-grade governance for `survivorship_policy` and `quality_score_floor`

**Justification:** Complete Master Data Governance coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `survivorship_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `quality_score_floor` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 33. Create simulation-grade governance for `quality_threshold_policy` and `stewardship_sla_hours`

**Justification:** Complete Master Data Governance coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `quality_threshold_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `stewardship_sla_hours` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 34. Create simulation-grade governance for `stewardship_policy` and `publication_batch_size`

**Justification:** Complete Master Data Governance coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `stewardship_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `publication_batch_size` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 35. Create simulation-grade governance for `hierarchy_change_policy` and `hierarchy_depth_limit`

**Justification:** Complete Master Data Governance coverage requires specialists to tune policy safely without code changes while preserving explainability, approvals, and tenant isolation.

**Improvement:** Add a policy cockpit where `hierarchy_change_policy` can be versioned, tested against historical cases, simulated against open work, approved, rolled back, and monitored. Bind `hierarchy_depth_limit` to typed ranges, defaults, impact analysis, release notes, control evidence, and agent explanations showing exactly which records, events, queues, and UI decisions will change.

### 36. Upgrade `master data workbench` into a full specialist command center

**Justification:** The PBC UI must expose the complete Master Data Governance surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `master data workbench` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 37. Upgrade `match review queue` into a full specialist command center

**Justification:** The PBC UI must expose the complete Master Data Governance surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `match review queue` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 38. Upgrade `survivorship studio` into a full specialist command center

**Justification:** The PBC UI must expose the complete Master Data Governance surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `survivorship studio` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 39. Upgrade `golden record detail` into a full specialist command center

**Justification:** The PBC UI must expose the complete Master Data Governance surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `golden record detail` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 40. Upgrade `hierarchy manager` into a full specialist command center

**Justification:** The PBC UI must expose the complete Master Data Governance surface so experts can operate queues, exceptions, analytics, rules, and automations without leaving the package.

**Improvement:** Expand `hierarchy manager` with role-specific queues, record timelines, state-transition actions, inline policy explanations, exception triage, projection freshness, event replay, agent guidance, release-evidence status, saved views, and audit breadcrumbs. Every operation, rule, parameter, owned-table browser, advanced capability, and edge-case queue should be permission-aware and directly reachable.

### 41. Prove cross-PBC federation for `POST /master-records` and `CustomerUpdated`

**Justification:** Master Data Governance must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /master-records` and consumed event `CustomerUpdated` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 42. Prove cross-PBC federation for `POST /match-candidates` and `SupplierQualified`

**Justification:** Master Data Governance must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /match-candidates` and consumed event `SupplierQualified` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 43. Prove cross-PBC federation for `POST /merge-decisions` and `ProductPublished`

**Justification:** Master Data Governance must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /merge-decisions` and consumed event `ProductPublished` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 44. Prove cross-PBC federation for `POST /stewardship-tasks` and `PolicyChanged`

**Justification:** Master Data Governance must compose through APIs, events, and projections instead of shared tables; integration failures usually emerge at schema evolution, idempotency, replay, or stale-data boundaries.

**Improvement:** Add compatibility tests and workbench evidence for `POST /stewardship-tasks` and consumed event `PolicyChanged` covering version negotiation, payload validation, idempotent replay, dead-letter triage, stale projection warnings, authorization failures, and dependency health. Operators should be able to inspect payload lineage and safely replay or quarantine messages.

### 45. Temporal reconstruction and bitemporal audit for Master Data Governance

**Justification:** Regulated and operationally complex domains need to answer what was known, valid, processed, and visible at any point in time.

**Improvement:** Add transaction-time, valid-time, and processing-time fields to core records, temporal query APIs, projection rebuild tooling, and UI time travel so specialists can reconstruct decisions, reports, and automation outcomes.

### 46. Bulk operations and migration-grade controls for Master Data Governance

**Justification:** World-class deployments must handle imports, mass corrections, high-volume operating days, and cutovers without bypassing governance.

**Improvement:** Add staged bulk upload, duplicate detection, chunked validation, approval sampling, partial failure handling, retry dashboards, reconciliation summaries, and agent-generated remediation plans for large batches.

### 47. Specialist edge-case playbooks for Master Data Governance

**Justification:** Rare cases often carry the highest financial, legal, safety, service, or compliance risk.

**Improvement:** Create a playbook catalog with detection rules, required evidence, escalation paths, fallback actions, owner roles, and release-audited tests for high-severity edge cases and exception queues.

### 48. Pre-mutation simulation and blast-radius analysis for Master Data Governance

**Justification:** Users should understand consequences before committing irreversible, customer-visible, operationally disruptive, or financially material changes.

**Improvement:** Add what-if simulation for every material command, showing impacted records, emitted events, dependent projections, rule outcomes, approvals, downstream PBC dependencies, and rollback limits.

### 49. Continuous control testing and operational assurance for Master Data Governance

**Justification:** Better-than-world-class PBCs prove controls continuously, not only at release or during periodic audits.

**Improvement:** Add executable control assertions, sampled evidence checks, anomaly thresholds, control-owner dashboards, breach/recovery events, and release gates that fail when domain controls lose evidence.

### 50. Human-in-the-loop domain agent execution for Master Data Governance

**Justification:** The PBC chatbot must help specialists perform real work while preventing unsafe autonomous mutation.

**Improvement:** Add domain-specific skills, document parsing, task planning, CRUD previews, confidence/risk scoring, confirmation gates, redaction, policy explanations, and post-action evidence packets for every supported command and query.
