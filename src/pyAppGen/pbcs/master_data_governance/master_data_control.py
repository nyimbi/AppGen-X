"""Executable improve1 controls for the Master Data Governance PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "master_data_governance"
EVENT_CONTRACT = "AppGen-X"
MASTER_DATA_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
MASTER_DATA_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.master_data_governance.events"
_BASE_OWNED_TABLES = (
    "master_data_governance_master_record",
    "master_data_governance_golden_record",
    "master_data_governance_match_candidate",
    "master_data_governance_merge_decision",
    "master_data_governance_survivorship_rule",
    "master_data_governance_data_quality_rule",
    "master_data_governance_stewardship_task",
    "master_data_governance_downstream_sync_event",
    "master_data_governance_appgen_outbox_event",
    "master_data_governance_appgen_inbox_event",
    "master_data_governance_appgen_dead_letter_event",
)
MASTER_DATA_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(
    _BASE_OWNED_TABLES + tuple(f"master_data_governance_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)
))
MASTER_DATA_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys((
    "CustomerUpdated",
    "SupplierQualified",
    "ProductPublished",
    "PolicyChanged",
    "ConsentChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)))
MASTER_DATA_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in MASTER_DATA_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in MASTER_DATA_CONTROL_CAPABILITIES}
_BASE_FIELDS = (
    "tenant_id",
    "domain_id",
    "master_record_id",
    "golden_record_id",
    "source_record_id",
    "policy_version",
    "audit_trail",
    "evidence_references",
)
_PRIMARY_PROOF_FIELDS: dict[int, str] = {
    1: 'domain_policy_activated',
    2: 'lifecycle_transition_gated',
    3: 'source_provenance_trust_ranked',
    4: 'identity_keys_normalized',
    5: 'entity_resolution_explainable',
    6: 'match_decision_dual_reviewed',
    7: 'merge_split_unmerge_simulated',
    8: 'survivorship_rule_tested',
    9: 'survivorship_decision_explained',
    10: 'golden_version_time_travel_ready',
    11: 'hierarchy_relationship_governed',
    12: 'hierarchy_impact_simulated',
    13: 'reference_code_set_versioned',
    14: 'quality_rule_dimensioned',
    15: 'quality_root_cause_recorded',
    16: 'publication_quality_firewall_passed',
    17: 'stewardship_priority_scored',
    18: 'steward_skill_routing_enforced',
    19: 'approval_matrix_satisfied',
    20: 'sensitive_attribute_controls_applied',
    21: 'publication_batch_simulated',
    22: 'publication_event_contract_compatible',
    23: 'consumer_dependency_mapped',
    24: 'duplicate_prevention_screened',
    25: 'bulk_load_governance_sampled',
    26: 'cross_domain_relationship_projected',
    27: 'standardization_pipeline_applied',
    28: 'multilingual_resolution_explained',
    29: 'golden_record_confidence_published',
    30: 'recertification_cadence_enforced',
    31: 'exception_workflow_closed_with_evidence',
    32: 'conflict_cluster_resolved',
    33: 'mdm_policy_parameter_version_approved',
    34: 'matching_model_governed',
    35: 'stewardship_metrics_reconciled',
    36: 'golden_record_proof_packet_sealed',
    37: 'lineage_graph_complete',
    38: 'publication_replay_idempotent',
    39: 'downstream_reconciliation_current',
    40: 'privacy_consent_projection_respected',
    41: 'hierarchy_cycle_orphan_controls_clean',
    42: 'sandbox_scenario_approved',
    43: 'agent_stewardship_human_confirmed',
    44: 'semantic_document_intake_cited',
    45: 'cross_pbc_boundary_proven',
    46: 'release_evidence_pack_complete',
    47: 'change_narrative_cited',
    48: 'domain_workbench_surface_complete',
    49: 'dead_letter_replay_quarantined',
    50: 'complete_workbench_coverage_visible',
}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {
    feature_number: _BASE_FIELDS + (primary_proof,)
    for feature_number, primary_proof in _PRIMARY_PROOF_FIELDS.items()
}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    3: ('CustomerUpdated', 'SupplierQualified', 'ProductPublished'),
    22: ('PolicyChanged',),
    23: ('CustomerUpdated', 'SupplierQualified', 'ProductPublished'),
    26: ('CustomerUpdated', 'SupplierQualified', 'ProductPublished'),
    39: ('CustomerUpdated', 'SupplierQualified', 'ProductPublished'),
    40: ('ConsentChanged',),
    45: ('CustomerUpdated', 'SupplierQualified', 'ProductPublished', 'PolicyChanged'),
    49: ('CustomerUpdated', 'SupplierQualified', 'ProductPublished'),
}
_DOMAIN_MESSAGES: dict[int, str] = {
    1: 'master domains must define domain type, purpose, authoritative sources, identity keys, survivorship, quality, hierarchy, stewardship, publication, sensitivity, policy version, and release proof',
    2: 'golden records must move through proposed, matching, survivorship, approval, publication, quarantine, merge, split, deprecation, and retirement only through governed gates',
    3: 'source links must retain source PBC, external id, timestamp, capture method, trust score, authoritative fields, freshness, contradictions, and lineage hash',
    4: 'identity keys must be domain-specific with required and optional keys, normalization, phonetics, tokenization, hierarchy awareness, locale rules, and validation',
    5: 'entity resolution must expose candidate clusters, field similarity, confidence bands, contradictions, source trust, historic decisions, recommendation, and steward queue',
    6: 'match decisions must record type, steward authority, reviewed evidence, override reason, confidence, effective date, reversal eligibility, appeal, and downstream impact',
    7: 'merge, split, and unmerge must simulate affected sources, prior golden versions, publications, rollback limits, consumer notifications, and proof before mutation',
    8: 'survivorship rules must test field priority, recency, confidence, manual override, null handling, conflicts, jurisdiction, historical records, and activation impact',
    9: 'survivorship decisions must explain winner and loser values, rule version, trust, freshness, override, conflict reason, confidence, and golden-version linkage',
    10: 'golden versions must preserve transaction, valid, and publication time, source snapshot, survivorship decisions, quality score, approvals, rollback, and as-of query support',
    11: 'hierarchy relationships must carry hierarchy type, role, dates, ownership percent, rollup rules, cycle prevention, cardinality, and steward approval',
    12: 'hierarchy simulation must show affected records, consumers, publications, reports, access, pricing, risk, tax, and dependent projections before approval',
    13: 'reference data must govern code sets, translations, aliases, mappings, deprecations, effective dates, publication rules, and active-version validation',
    14: 'quality rules must define dimension, target fields, threshold, source scope, domain, severity, remediation owner, sampling, release tests, and publication gates',
    15: 'quality observations must expose source, rule, affected records, anomaly cluster, root cause, recurrence, owner, remediation, and downstream impact',
    16: 'publication firewalls must block low-quality records by domain, field, consumer tier, use case, quality floor, exception approval, and event evidence',
    17: 'stewardship priority must rank work by downstream dependency, quality severity, financial exposure, customer impact, publication blocker, SLA, aging, and workload balance',
    18: 'steward routing must enforce domain, region, language, legal, supplier, product, privacy, availability, independence, priority, and escalation constraints',
    19: 'approval matrices must satisfy field-level policy, risk score, dual control, source evidence, segregation, emergency path, expiry, and rationale on golden version',
    20: 'sensitive attributes must apply definitions, risk scoring, required evidence, manual review, notification, monitoring, and domain policy without code changes',
    21: 'publication batches must simulate scope, consumers, dependency order, cutover window, size limit, readiness, rollback, and event-volume impact',
    22: 'publication events must validate schema version, compatibility, subscriptions, replay eligibility, idempotency, migration support, and evidence hashes',
    23: 'consumer dependencies must be mapped from subscriptions, acknowledgements, projections, merge/split, hierarchy, survivorship, and publication impacts',
    24: 'intake must prevent duplicates through identity keys, existing candidates, source history, similarity threshold, and steward review before create',
    25: 'bulk loads must profile sources, analyze duplicates, simulate rules, validate batches, sample steward decisions, handle partial failure, and prove publication readiness',
    26: 'cross-domain relationships must use identifiers and projections for type, source, dates, confidence, ownership, and publication without foreign-table mutation',
    27: 'standardization must parse and preserve original plus standardized names, addresses, phones, tax ids, SKUs, emails, locale rules, aliases, and confidence',
    28: 'multilingual resolution must handle accents, transliteration, non-Latin scripts, legal suffixes, regional addresses, locale-aware matching, and steward explanation',
    29: 'confidence scoring must publish source agreement, quality, steward decisions, survivorship conflicts, freshness, downstream issues, and contested/stale indicators',
    30: 'recertification must enforce schedules by domain and risk tier, stale detection, reminders, source refresh, and publication blocking for overdue records',
    31: 'exceptions must track type, records, severity, policy basis, owner, expiry, compensating controls, downstream impact, and closure evidence',
    32: 'conflict workbenches must show competing values, trust, freshness, usage, prior decisions, recommended resolution, survivorship links, and quality observations',
    33: 'policy studios must version thresholds, survivorship, quality floors, hierarchy limits, publication sizes, SLAs, tests, simulations, approvals, rollback, and impact',
    34: 'matching models must govern training sets, evaluation, precision, recall, false-merge risk, false-split risk, drift, feedback, approval, limitation, and rollback',
    35: 'steward metrics must reconcile age, consistency, false-merge reversals, override rate, quality improvement, publication blockers removed, workload, and coaching',
    36: 'golden-record proof packets must seal source hashes, match decisions, survivorship versions, quality observations, approvals, publication ids, and golden hashes',
    37: 'lineage graphs must connect sources, transformations, match clusters, survivorship, approvals, golden versions, publication events, upstream, and downstream views',
    38: 'publication replay must enforce idempotency keys, batch membership, acknowledgements, dead-letter reasons, replay eligibility, and reconciliation status',
    39: 'downstream reconciliation must track acknowledgements, projection freshness, applied versions, mismatches, critical consumer lag, divergence, and stewardship tasks',
    40: 'privacy-aware mastering must respect legal basis, consent projections, minimization, deletion restrictions, suppression, subject rights, and publication limits',
    41: 'hierarchy controls must detect cycles, orphans, invalid parent types, excessive depth, effective-date overlaps, missing roots, and steward tasks',
    42: 'sandbox what-if scenarios must isolate match clusters, survivorship, hierarchy changes, publication simulations, quality impact, consumer impact, and promotion approval',
    43: 'agent stewardship must summarize candidates, explain survivorship, propose tasks and merge/split plans with citations, confidence, affected tables, events, and confirmation',
    44: 'semantic document intake must extract names, addresses, identifiers, product attributes, certificates, relationships, dates, citations, evidence, and steward review',
    45: 'boundary proofs must show services mutate only owned master-data tables and AppGen-X runtime tables while external context flows through APIs/events/projections',
    46: 'release packs must prove schema, migrations, services, events, idempotency, retries, matching, survivorship, publication, UI coverage, agents, and smoke runs',
    47: 'change narratives must explain who changed what, why, from which source, under which rule, where it was published, with citations and redaction',
    48: 'domain workbenches must tailor customer, supplier, product, location, and reference-data match review, golden detail, quality, hierarchy, stewardship, approvals, publication, and agent panels',
    49: 'event replay operations must quarantine unknown events and expose inbox, outbox, dead letters, retry, payload lineage, idempotency, freshness, and safe replay',
    50: 'complete workbench coverage must expose domains, sources, masters, matches, merge/split, survivorship, golden versions, hierarchies, quality, stewardship, approvals, publications, exceptions, policies, simulations, evidence, agents, and release status',
}
_HUMAN_CONFIRMATION_FEATURES = (43, 44)
_PROJECTION_ONLY_FEATURES = (3, 23, 26, 39, 40, 45)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    proof = _PRIMARY_PROOF_FIELDS[capability.feature_number]
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"master_data_governance_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": proof,
        "ui": f"MasterDataGovernance{_camel(capability.slug)}Panel",
        "route": f"POST /master-data-governance/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in MASTER_DATA_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({
        "database_backend": "postgresql",
        "event_contract": EVENT_CONTRACT,
        "event_topic": MASTER_DATA_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    feature_number = capability.feature_number
    spec = CONTROL_SPECS[feature_number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[feature_number])
    if feature_number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("master-data agents must propose and cite changes; steward approval is required before governed mutation")
    if feature_number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("external customer, supplier, product, privacy, and policy context must use APIs, events, or read-only projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != MASTER_DATA_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("master data eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in MASTER_DATA_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary master data datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("master data controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_master_data_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in MASTER_DATA_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in MASTER_DATA_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "primary_proof": spec["primary_proof"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": MASTER_DATA_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": MASTER_DATA_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "slug": resolved.slug,
        "title": resolved.title,
        "capability": resolved.as_traceability_row(),
        "payload": candidate,
        "evidence": evidence,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "side_effects": (),
    }


def improve1_master_data_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_master_data_control(capability) for capability in MASTER_DATA_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.master-data-governance-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": MASTER_DATA_CONTROL_OWNED_TABLES,
        "declared_dependencies": MASTER_DATA_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": MASTER_DATA_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": MASTER_DATA_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


MASTER_DATA_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_master_data_control(slug, payload))
    for capability in MASTER_DATA_CONTROL_CAPABILITIES
}
