# Master Data Governance PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `master_data_governance`. Each item is specific to master data management and governance: master domains, golden records, source links, entity resolution, match decisions, survivorship, hierarchy management, data quality, stewardship, approvals, publication, downstream synchronization, exception handling, lineage, auditability, and governed lifecycle automation. The intent is complete domain coverage for a better-than-world-class MDM PBC while preserving AppGen-X package boundaries.

## Current Domain Evidence Used

- Domain purpose: owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation.
- Owned tables include master record, master domain, source record link, match candidate, match decision, survivorship rule, survivorship decision, golden record version, hierarchy node, hierarchy relationship, data quality rule, quality observation, stewardship task, master data approval, publication batch, publication event, exception case, policy rule, runtime parameter, schema extension, control assertion, governed model, outbox, inbox, and dead-letter evidence.
- Operations include `create_master_record`, `register_master_domain`, `link_source_record`, `generate_match_candidate`, `record_match_decision`, `define_survivorship_rule`, `apply_survivorship`, `publish_golden_version`, `create_hierarchy_node`, `link_hierarchy_relationship`, `define_quality_rule`, `observe_data_quality`, `open_stewardship_task`, `approve_master_change`, `create_publication_batch`, `publish_master_event`, `resolve_master_exception`, `compile_mdm_rule`, and `simulate_survivorship_impact`.
- Events include `MasterRecordCreated`, `MatchCandidateGenerated`, `GoldenRecordPublished`, `HierarchyChanged`, `DataQualityChanged`, and `MasterDataPublished`; consumed events include customer, supplier, product, and policy changes.
- Existing advanced claims include probabilistic entity resolution, explainable survivorship, hierarchy impact simulation, quality anomaly detection, stewardship workload optimization, and cryptographic golden record proof.

## 50 Better-Than-World-Class Improvements

### 1. Master Domain Modeling and Domain Policy

**Justification:** Customer, supplier, product, asset, location, employee, chart, and reference-data domains have different identity keys, quality rules, survivorship policies, hierarchies, and publication requirements. A generic master domain cannot provide complete MDM coverage.

**Improvement:** Expand `register_master_domain` with domain type, business purpose, authoritative source ranking, identity keys, survivorship strategy, quality rule set, hierarchy model, stewardship team, publication scope, and sensitivity classification. Require each domain to carry policy versions and release evidence before activation.

### 2. Golden Record Lifecycle State Machine

**Justification:** Golden records need explicit lifecycle states: proposed, pending match, pending survivorship, draft golden, approved, published, quarantined, deprecated, merged, split, and retired. Simple active/inactive state hides governance work.

**Improvement:** Add a configurable master record lifecycle that gates transitions on match decisions, quality observations, steward approvals, survivorship evidence, hierarchy validity, and publication readiness. Emit AppGen-X events only after policy-compliant transitions.

### 3. Source Record Provenance and Trust Ranking

**Justification:** Golden-record quality depends on knowing which sources contributed which attributes, when they were captured, and how trustworthy each source is for each field.

**Improvement:** Upgrade `link_source_record` with source PBC, external id, source timestamp, capture method, trust score, authoritative fields, freshness, contradiction flags, and lineage hash. Show field-level provenance on the golden record detail page.

### 4. Domain-Specific Identity Keys

**Justification:** Entity resolution cannot rely on one matching approach across domains. Customers, suppliers, products, and locations use different identifiers, aliases, addresses, legal names, SKUs, and regulatory ids.

**Improvement:** Add domain identity key definitions with required/optional keys, normalization, phonetic rules, tokenization, hierarchy-aware keys, locale handling, and validation. Use these keys in match candidate generation and steward explanations.

### 5. Probabilistic Entity Resolution Workbench

**Justification:** Match decisions require explainable probabilities, field comparisons, contradictions, source trust, historic decisions, and steward feedback. A match score alone is not enough.

**Improvement:** Expand `generate_match_candidate` with candidate pairs/clusters, feature-level similarity, confidence, threshold band, contradiction evidence, recommended action, and reviewer queue. The workbench should visualize why records match, maybe match, or should remain separate.

### 6. Match Decision Governance

**Justification:** Match, no-match, merge, split, and defer decisions can permanently affect downstream systems. Decisions need authority, rationale, and appeal/reversal paths.

**Improvement:** Upgrade `record_match_decision` with decision type, steward role, evidence reviewed, override reason, confidence, effective date, reversal eligibility, and downstream impact. Require dual review for high-impact merges or splits.

### 7. Merge, Split, and Unmerge Operations

**Justification:** MDM systems must support safe correction of false merges and missed matches. Without split/unmerge, bad decisions contaminate golden records indefinitely.

**Improvement:** Add explicit merge, split, and unmerge workflows with affected source records, prior golden versions, downstream publications, rollback limits, consumer notifications, and cryptographic evidence. Simulate impact before applying high-risk changes.

### 8. Survivorship Rule Studio

**Justification:** Survivorship is domain- and field-specific: legal name, billing address, tax id, phone, classification, hierarchy parent, and status may come from different authoritative sources.

**Improvement:** Expand `define_survivorship_rule` into a rule studio with field-level source priority, recency, confidence, manual override, null handling, conflict handling, jurisdiction, and test cases. Simulate rules against historical records before activation.

### 9. Explainable Survivorship Decisions

**Justification:** Stewards and consumers must understand why each golden attribute won over competing source values. Black-box survivorship reduces trust.

**Improvement:** Upgrade `apply_survivorship` with field-by-field winner/loser values, rule version, source trust, freshness, steward override, conflict reason, and confidence. Store decision explanations on each golden record version.

### 10. Golden Record Versioning and Time Travel

**Justification:** Downstream consumers, auditors, and analysts need to know what the golden record looked like at prior publication times, not just current state.

**Improvement:** Expand `publish_golden_version` with transaction time, valid time, publication time, source snapshot, survivorship decision ids, quality score, approval evidence, and rollback linkage. Provide as-of queries and UI time travel.

### 11. Hierarchy Type and Relationship Governance

**Justification:** Hierarchies differ: legal ownership, reporting, buying group, geography, product category, bill-to/ship-to, parent-child, and operational rollups. Generic edges are insufficient.

**Improvement:** Upgrade hierarchy nodes and relationships with hierarchy type, relationship role, effective dates, ownership percentage, rollup rules, cycle prevention, cardinality constraints, and steward approvals.

### 12. Hierarchy Impact Simulation

**Justification:** Changing a parent, category, buying group, or location hierarchy can alter pricing, reporting, risk, access, tax, and downstream analytics.

**Improvement:** Add hierarchy simulation that shows affected golden records, consumers, publications, reports, access policies, and dependent PBC projections before a relationship change is approved.

### 13. Reference Data and Code Set Governance

**Justification:** Master data includes controlled values such as statuses, categories, countries, tax types, industry codes, and product attributes. Poor reference data creates inconsistent records.

**Improvement:** Add reference-data domain support with code sets, translations, deprecations, aliases, mappings, effective dates, and publication rules. Validate master records against active code-set versions.

### 14. Data Quality Rule Library

**Justification:** Master data quality spans completeness, validity, uniqueness, consistency, accuracy, conformity, timeliness, and referential integrity. One quality score hides specific remediations.

**Improvement:** Expand `define_quality_rule` with quality dimension, target fields, threshold, source scope, domain, severity, remediation owner, sampling method, and release tests. Link each rule to stewardship tasks and publication gates.

### 15. Quality Observation Root Cause

**Justification:** Quality observations are useful only when they reveal source-system defects, process gaps, stale data, bad transformations, or steward errors.

**Improvement:** Upgrade `observe_data_quality` with source, rule, affected records, anomaly cluster, root cause, recurrence, source owner, remediation action, and downstream impact. Emit `DataQualityChanged` when quality affects publication.

### 16. Quality Firewall Before Publication

**Justification:** Publishing low-quality golden records propagates errors to every consuming PBC. Publication needs a quality gate.

**Improvement:** Add publication-blocking quality firewalls by domain, field, consumer tier, and use case. Require exception approval for records below the quality score floor and include quality evidence in publication events.

### 17. Stewardship Task Prioritization

**Justification:** Steward queues can become unmanageable when every match, quality issue, or exception has equal priority. High-impact records need attention first.

**Improvement:** Expand `open_stewardship_task` with priority based on downstream dependency, data quality severity, financial exposure, customer impact, publication blocker, and SLA. Provide workload balancing and aging views.

### 18. Steward Skill and Workload Routing

**Justification:** Some stewardship tasks require domain, region, language, legal, supplier, product, or privacy expertise. Generic assignment causes slow and inaccurate decisions.

**Improvement:** Add steward skill profiles, domain responsibility, workload, escalation authority, and independence constraints. Route tasks using skill, availability, priority, and conflict rules.

### 19. Approval Matrix for Master Data Changes

**Justification:** High-impact master changes, such as legal name, tax id, bank-like identifiers, product classification, or hierarchy parent, need appropriate approvals.

**Improvement:** Upgrade `approve_master_change` with field-level approval policies, risk scoring, dual control, source evidence, segregation checks, emergency paths, and expiry. Store approval rationale with the affected golden version.

### 20. Sensitive Attribute Change Controls

**Justification:** Some attributes create fraud, compliance, or financial risk if changed incorrectly. They need stronger validation and monitoring.

**Improvement:** Add sensitive attribute definitions, change risk scoring, required evidence, manual review, notification rules, and post-change monitoring. Support domain-specific sensitive fields through policy rather than code changes.

### 21. Publication Batch Planning

**Justification:** Publication should consider record readiness, consumer windows, event volume, dependency ordering, and rollback. Naive batch publishing creates downstream instability.

**Improvement:** Expand `create_publication_batch` with batch scope, consumer targets, dependency order, cutover window, size limit, quality readiness, rollback plan, and expected event volume. Simulate publication load before execution.

### 22. Publication Event Contract Governance

**Justification:** Downstream PBCs depend on stable master-data events. Schema drift or missing fields breaks consumers.

**Improvement:** Upgrade `publish_master_event` with event schema version, contract compatibility, consumer subscriptions, replay eligibility, idempotency, and evidence hashes. Block incompatible publication events without migration support.

### 23. Downstream Consumer Dependency Mapping

**Justification:** Master data changes affect customer, supplier, product, pricing, order, finance, analytics, and risk domains. Stewards need consumer impact visibility.

**Improvement:** Add dependency records from subscriptions, event acknowledgements, and declared projections. Show affected consumers for merge, split, hierarchy, survivorship, and publication changes.

### 24. Duplicate Prevention at Intake

**Justification:** Duplicate records are cheaper to prevent than to resolve after they spread downstream. Intake should screen before new master records are created.

**Improvement:** Add pre-create duplicate checks using domain identity keys, existing match candidates, source history, and similarity thresholds. Require steward review before creating records that overlap high-confidence existing masters.

### 25. Bulk Load and Migration Governance

**Justification:** MDM deployments and acquisitions require high-volume imports, deduplication, quality checks, stewardship sampling, and controlled publication.

**Improvement:** Add staged bulk load workflows with file/source profiling, duplicate analysis, rule simulation, batch validation, steward sampling, partial failure handling, and publication readiness dashboards.

### 26. Cross-Domain Relationship Management

**Justification:** Customer-to-supplier, product-to-vendor, location-to-customer, employee-to-cost-center, and account-to-entity relationships often matter as much as individual records.

**Improvement:** Add governed cross-domain relationship records with type, source, effective dates, confidence, ownership, and publication rules. Preserve PBC boundaries by using identifiers and projections, not foreign-table writes.

### 27. Address, Name, and Identifier Standardization

**Justification:** Matching quality depends on normalization of names, addresses, phone numbers, tax ids, SKUs, emails, and locale-specific identifiers.

**Improvement:** Add standardization pipelines with parsing, transliteration, casing, punctuation, country rules, alias dictionaries, validation, and confidence. Store original and standardized values with provenance.

### 28. Multilingual and Multi-Script Entity Resolution

**Justification:** Global master data includes accents, transliterations, non-Latin scripts, local legal suffixes, and regional address formats. English-only matching misses duplicates.

**Improvement:** Add locale-aware matching, transliteration, script normalization, local legal entity suffixes, regional address rules, and multilingual steward explanations.

### 29. Golden Record Confidence Score

**Justification:** Consumers need to know whether a golden record is high-confidence, contested, stale, or incomplete before using it in operations.

**Improvement:** Add confidence scoring based on source agreement, quality rules, steward decisions, survivorship conflicts, freshness, and downstream issue history. Publish confidence with golden versions.

### 30. Staleness and Recertification Cadence

**Justification:** Master records decay when names, addresses, categories, ownership, and relationships change. Static golden records become liabilities.

**Improvement:** Add recertification schedules by domain and risk tier, stale attribute detection, owner reminders, source refresh checks, and publication blocking for overdue high-risk records.

### 31. Master Data Exception Workflow

**Justification:** Exceptions such as unresolved duplicates, policy violations, missing source proof, publication failures, and quality waivers require controlled resolution.

**Improvement:** Upgrade `resolve_master_exception` with exception type, affected records, severity, policy basis, owner, expiry, compensating controls, downstream impact, and closure evidence.

### 32. Conflict and Contradiction Workbench

**Justification:** Source systems often disagree on legal name, address, status, category, or hierarchy. Stewards need a dedicated conflict view.

**Improvement:** Add conflict clusters that show competing values, source trust, freshness, downstream usage, prior decisions, and recommended resolution. Link conflicts to survivorship decisions and quality observations.

### 33. MDM Policy and Parameter Studio

**Justification:** Matching thresholds, survivorship policies, quality floors, hierarchy limits, publication sizes, and stewardship SLAs need governed configuration.

**Improvement:** Expand `compile_mdm_rule` into a policy studio with versioning, simulation, approval workflow, effective dates, rollback, test cases, and impact analysis across match candidates, golden versions, and publications.

### 34. Matching Model Governance

**Justification:** Probabilistic matching can merge or split important entities incorrectly. Models need validation, drift monitoring, bias checks, and steward feedback loops.

**Improvement:** Add governed model records for matching algorithms, training/evaluation sets, precision/recall, false-merge risk, false-split risk, drift, approval, limitations, and rollback.

### 35. Stewardship Quality Metrics

**Justification:** MDM quality depends on steward decisions. Teams need visibility into decision accuracy, backlog, cycle time, reversals, and domain complexity.

**Improvement:** Add metrics for task age, decision consistency, false merge reversals, override rate, quality improvement, publication blockers removed, and workload by domain. Use metrics for coaching and capacity planning.

### 36. Golden Record Cryptographic Proof

**Justification:** Consumers and auditors may need proof of the sources, rules, decisions, and approvals that produced a golden record.

**Improvement:** Generate cryptographic proof packets with source hashes, match decisions, survivorship rule versions, quality observations, approvals, publication event ids, and golden version hashes.

### 37. Master Data Lineage Graph

**Justification:** A golden record's lineage spans sources, transformations, match clusters, survivorship, approvals, and publications. Without graph lineage, decisions are hard to trust.

**Improvement:** Build a lineage graph from source links through match and survivorship decisions to golden versions and publication events. Provide upstream and downstream views in the workbench.

### 38. Publication Replay and Recovery

**Justification:** Downstream publication can fail, duplicate, or need replay. Master data sync must be reliable and auditable.

**Improvement:** Add publication replay controls with idempotency keys, batch membership, consumer acknowledgements, dead-letter reasons, replay eligibility, and reconciliation status.

### 39. Downstream Reconciliation

**Justification:** Publishing a golden record does not prove consumers applied it. Reconciliation is needed for trusted synchronization.

**Improvement:** Add consumer acknowledgement records, projection freshness, applied version, mismatch detection, and reconciliation tasks. Alert stewards when critical consumers lag or diverge.

### 40. Privacy and Consent-Aware Mastering

**Justification:** Person and customer mastering may involve privacy, consent, purpose limitation, deletion, and subject-rights constraints.

**Improvement:** Add privacy basis, consent projection, minimization flags, deletion restrictions, suppression state, and subject-rights compatibility checks. Ensure publication respects privacy and consent projections.

### 41. Hierarchy Cycle and Orphan Detection

**Justification:** Bad hierarchy edges create cycles, orphan nodes, broken rollups, and invalid reporting. These defects can spread widely.

**Improvement:** Add continuous hierarchy controls for cycle detection, orphan detection, invalid parent type, excessive depth, effective-date overlap, and missing root nodes. Generate stewardship tasks for violations.

### 42. Master Data Sandbox and What-If

**Justification:** Stewards need to test merges, survivorship, hierarchy changes, and publications before affecting production golden records.

**Improvement:** Add sandbox scenarios with isolated match clusters, proposed survivorship, proposed hierarchy changes, publication simulation, quality impact, and consumer impact. Promote only approved scenarios.

### 43. Agent-Assisted Stewardship

**Justification:** Stewards review documents, source records, duplicate candidates, quality observations, and policy text. The agent can reduce work only if it stays grounded and confirmable.

**Improvement:** Give the PBC agent skills to summarize candidates, explain survivorship, propose stewardship tasks, draft merge/split recommendations, and create CRUD plans with citations, confidence, affected tables, event plans, and human confirmation.

### 44. Semantic Document Intake for Master Updates

**Justification:** Master updates often arrive via certificates, contracts, emails, onboarding forms, regulatory filings, or product sheets. Manual extraction is slow and inconsistent.

**Improvement:** Add document extraction workflows for legal names, addresses, identifiers, product attributes, certificates, hierarchy relationships, and effective dates. Require steward review and source evidence before applying updates.

### 45. Cross-PBC Boundary Proofs

**Justification:** MDM consumes customer, supplier, product, policy, and other domain signals but must own its own golden-record logic. Shared mutation would break composition.

**Improvement:** Add explicit projection contracts and tests proving services mutate only `master_data_governance_` tables plus AppGen-X runtime tables. External context must flow through APIs, events, or read-only projections.

### 46. Master Data Release Evidence Packs

**Justification:** MDM affects many downstream operations. Releases must prove schema, matching, survivorship, quality, approvals, publication, and event reliability.

**Improvement:** Generate release evidence packs with schema hashes, migration manifests, service contracts, event schemas, handler idempotency proofs, retry/dead-letter tests, match simulations, survivorship tests, publication smoke runs, UI coverage, and agent manifests.

### 47. Audit-Ready Master Change Narrative

**Justification:** Auditors and business users need a plain-language explanation of who changed what, why, based on which source, under which rule, and where it was published.

**Improvement:** Add generated change narratives tied to source records, steward actions, approvals, quality checks, survivorship decisions, and publication events. Require citations and role-based redaction.

### 48. Domain-Specific Workbenches

**Justification:** Customer, supplier, product, location, and reference-data stewards need different fields, rules, hierarchy views, and quality checks.

**Improvement:** Expand the UI into domain-specific workbenches with tailored match review, golden detail, quality console, hierarchy manager, stewardship queue, approvals, publication monitor, and agent panel.

### 49. MDM Dead-Letter and Event Replay Operations

**Justification:** Source updates and publication events can arrive late, duplicate, malformed, or fail. MDM needs safe replay and quarantine.

**Improvement:** Add operations views for inbox, outbox, dead letters, retry, quarantine, payload lineage, idempotency keys, source event freshness, and replay. Unknown events should never mutate master state.

### 50. Complete Master Data Governance Workbench Coverage

**Justification:** MDM leaders, data stewards, domain owners, approvers, integration owners, auditors, and downstream consumers need full operational visibility. Hidden APIs are not enough.

**Improvement:** Expand the workbench to cover domains, source links, master records, match clusters, merge/split, survivorship, golden versions, hierarchies, quality, stewardship tasks, approvals, publications, exceptions, policies, simulations, evidence, agent actions, and release status.
