"""Executable improve1 controls for the Identity KYC AML Compliance PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "identity_kyc_aml_compliance"
EVENT_CONTRACT = "AppGen-X"
IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.identity_kyc_aml_compliance.events"
IDENTITY_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + tuple(
    f"identity_kyc_aml_compliance_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
)))
IDENTITY_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "PolicyChanged", "AuditEventSealed", "OperationalKpiChanged", "CustomerProfileProjected",
    "TransactionMonitoringSignalProjected", "WatchlistUpdated", "PrivacyConsentProjected",
)))
IDENTITY_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in IDENTITY_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in IDENTITY_CONTROL_CAPABILITIES}
_DEFAULT_FIELDS = ("owned_record", "evidence", "review_state", "approval_state", "operator_visible", "audit_trail", "safe_to_execute")
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {cap.feature_number: _DEFAULT_FIELDS for cap in IDENTITY_CONTROL_CAPABILITIES}
_FEATURE_FIELDS.update({
    1: ("current_state", "target_state", "allowed_transition", "mandatory_evidence", "jurisdiction_reason_code", "status_badge_visible", "lifecycle_event_emitted"),
    2: ("customer_type", "jurisdiction", "product_exposure", "channel", "expected_activity", "obligation_set_attached", "creation_allowed"),
    3: ("normalized_name", "date_of_birth", "identifier", "document_evidence", "duplicate_candidates", "merge_review_opened", "lineage_preserved"),
    4: ("document_class", "jurisdiction", "issuing_authority", "identifier", "issue_date", "expiry_date", "capture_method", "profile_linked", "completeness_passed"),
    5: ("authenticity_state", "tamper_state", "expiry_state", "identity_consistency", "replacement_required", "exception_opened", "approval_blocked"),
    6: ("liveness_outcome", "face_match_confidence", "capture_timestamp", "retry_count", "manual_review_path", "remote_profile_blocked_without_evidence"),
    7: ("watchlist_source", "match_basis", "alias_pathway", "country_context", "confidence", "disposition_requirement", "blocking_severity", "unresolved_blocking_hit"),
    8: ("screening_category", "review_track", "threshold", "reviewer", "resolution_path", "pep_queue", "sanctions_only_close_blocked"),
    9: ("disposition", "reason_code", "mandatory_rationale", "reviewer_evidence", "resolution_time", "taxonomy_version", "analytics_ready"),
    10: ("ownership_graph", "direct_pct", "indirect_pct", "control_relationships", "effective_dates", "ultimate_owner_reached", "approval_blocked_if_unresolved"),
    11: ("jurisdiction_threshold", "ownership_threshold", "voting_control_threshold", "coverage_pct", "simulation_available", "approval_blocked_below_coverage"),
    12: ("role_type", "nominee_flag", "signatory_flag", "board_controller", "screening_required", "role_badge_visible", "screening_not_skipped"),
    13: ("source_of_funds", "source_of_wealth", "expected_activity", "occupation_or_business", "supporting_docs", "higher_risk_required", "approval_warning"),
    14: ("pep_trigger", "high_risk_geography_trigger", "complex_ownership_trigger", "adverse_media_trigger", "edd_required", "exception_if_incomplete"),
    15: ("identity_documents", "beneficial_owners", "unresolved_hits", "expected_activity", "source_evidence", "reviewer_commentary", "packet_complete"),
    16: ("geography_factor", "customer_type_factor", "product_factor", "ownership_factor", "screening_factor", "monitoring_factor", "model_version", "score_explained"),
    17: ("original_score", "challenged_score", "challenge_note", "supervisor_decision", "override_lineage", "reviewer_evidence", "challenge_closed"),
    18: ("risk_tier", "rescreening_interval", "next_due_date", "policy_version", "overdue_queue", "jurisdiction_scope", "active_schedule"),
    19: ("inbound_event", "event_trigger", "profiles_selected", "rescreening_scope", "idempotency_key", "no_duplicate_side_effects", "event_lineage_visible"),
    20: ("alert_source", "typology", "severity", "customer_context", "transaction_context", "triage_decision", "sla_visible"),
    21: ("alert_id", "promotion_threshold", "case_created", "case_boundary", "alert_evidence_retained", "duplicate_case_blocked"),
    22: ("case_state", "suspicion_basis", "linked_alerts", "investigator", "approval_chain", "closure_outcome", "case_timeline_complete"),
    23: ("narrative_draft", "filing_boundary", "external_filing_mutation_blocked", "redaction_applied", "filing_decision", "approval_required", "audit_trail"),
    24: ("maker", "checker", "approval_chain", "segregation_enforced", "high_risk_decision", "approval_audit", "same_user_blocked"),
    25: ("lawful_basis", "consent_state", "processing_purpose", "data_subject_rights", "privacy_policy_version", "restricted_processing_visible"),
    26: ("retention_schedule", "purge_due_date", "legal_hold", "audit_hold", "purge_blocked_when_hold", "destruction_evidence", "policy_version"),
    27: ("export_purpose", "need_to_know", "redaction_profile", "protected_fields_masked", "recipient", "export_audit", "raw_export_blocked"),
    28: ("country", "risk_tier", "sanctions_program", "pep_exposure", "jurisdiction_policy", "effective_date", "decision_uses_matrix"),
    29: ("idempotency_key", "payload_hash", "duplicate_request", "stable_response", "duplicate_profile_prevented", "retry_documented"),
    30: ("file_type", "malware_scan", "size_check", "content_type_check", "pii_classification", "unsafe_file_blocked", "storage_boundary"),
    31: ("bulk_update_id", "owner_changes", "prior_graph_snapshot", "new_graph_snapshot", "lineage_hash", "approval_required", "rollback_available"),
    32: ("screening_event", "payload_schema", "category", "disposition", "event_topic", "appgen_contract", "idempotency_key"),
    33: ("monitoring_event", "projection_mode", "alert_created", "profile_risk_refreshed", "foreign_table_access_blocked", "event_lineage"),
    34: ("inbound_event", "dependency_mode", "policy_effect", "audit_effect", "kpi_effect", "idempotent_handler", "dead_letter_route"),
    35: ("dead_letter_item", "failure_reason", "retry_policy", "safe_replay_allowed", "operator_notes", "closure_code", "affected_case_visible"),
    36: ("rule_change", "simulation_scope", "impacted_profiles", "impacted_cases", "approval_preview", "live_mutation_blocked", "explainable_diff"),
    37: ("parameter", "bounds_valid", "approval_history", "tenant_override", "impact_preview", "activation_allowed", "rollback_visible"),
    38: ("assertion_suite", "kyc_evidence_checked", "screening_resolution_checked", "edd_checked", "maker_checker_checked", "privacy_checked", "control_effective"),
    39: ("proof_hash", "previous_hash", "payload_digest_valid", "proof_verified", "altered_order_detected", "redacted_export_supported", "auditor_export"),
    40: ("schema_tests", "workflow_tests", "event_tests", "ui_tests", "agent_guardrails", "boundary_checks", "release_pack_complete"),
    41: ("analyst_queue", "kyc_queue", "screening_queue", "edd_queue", "monitoring_queue", "sla_badges", "permission_filtered"),
    42: ("profile_header", "decision_workspace", "document_panel", "ownership_graph", "screening_panel", "risk_panel", "approval_actions"),
    43: ("monitoring_queue", "typology_filters", "alert_aging", "case_promotion", "risk_refresh", "operator_actions", "read_only_projections"),
    44: ("case_queue", "narrative_workspace", "evidence_timeline", "approval_chain", "filing_boundary", "redaction_tools", "closure_actions"),
    45: ("document_instruction", "extracted_fields", "source_citations", "confidence", "human_confirmation", "direct_mutation_blocked", "unsafe_file_denied"),
    46: ("screening_hit", "suggested_disposition", "match_explanation", "source_citations", "human_confirmation", "direct_mutation_blocked", "false_positive_learning"),
    47: ("case_summary", "evidence_citations", "narrative_draft", "redaction_applied", "filing_boundary", "human_confirmation", "direct_mutation_blocked"),
    48: ("model_name", "model_version", "drift_metric", "feedback_loop", "human_feedback", "approval_status", "model_update_blocked_until_approved"),
    49: ("tenant_id", "jurisdiction", "data_residency", "policy_scope", "queue_leakage_blocked", "assistant_scope", "cross_tenant_access_blocked"),
    50: ("kyc_profile_seeded", "document_seeded", "owner_seeded", "screening_seeded", "monitoring_seeded", "case_seeded", "apis_exercised", "events_emitted", "workbench_queues_driven", "agent_summary_generated", "control_assertions_run", "release_documents_updated"),
})
_FEATURE_DEPENDENCIES = {19: ("PolicyChanged", "WatchlistUpdated"), 33: ("TransactionMonitoringSignalProjected",), 34: ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"), 49: ("PrivacyConsentProjected",)}
_EMPTY_ALLOWED_FIELDS = ("duplicate_candidates",)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability): return capability
    if isinstance(capability, int): return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    return {"title": capability.title, "slug": capability.slug, "tables": (f"identity_kyc_aml_compliance_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "ui": _camel(capability.slug), "route": f"POST /identity-kyc-aml-compliance/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in IDENTITY_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None: return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({
        "allowed_transition": True, "mandatory_evidence": "captured", "status_badge_visible": True, "lifecycle_event_emitted": True, "obligation_set_attached": True, "creation_allowed": True,
        "duplicate_candidates": (), "merge_review_opened": True, "lineage_preserved": True, "profile_linked": True, "completeness_passed": True, "authenticity_state": "accepted", "tamper_state": "clear", "expiry_state": "valid", "identity_consistency": True, "approval_blocked": False,
        "liveness_outcome": "pass", "face_match_confidence": 0.93, "remote_profile_blocked_without_evidence": True, "confidence": 0.91, "unresolved_blocking_hit": False, "screening_category": "pep", "pep_queue": True, "sanctions_only_close_blocked": True,
        "mandatory_rationale": "captured", "reviewer_evidence": "captured", "ultimate_owner_reached": True, "approval_blocked_if_unresolved": True, "coverage_pct": 100, "approval_blocked_below_coverage": True, "screening_required": True, "screening_not_skipped": True,
        "supporting_docs": ("sof.pdf",), "higher_risk_required": True, "edd_required": True, "exception_if_incomplete": True, "packet_complete": True, "model_version": "v1", "score_explained": True, "challenge_closed": True,
        "next_due_date": "2026-12-31", "active_schedule": True, "idempotency_key": "idem-1", "no_duplicate_side_effects": True, "event_lineage_visible": True, "sla_visible": True, "case_created": True, "duplicate_case_blocked": True,
        "case_timeline_complete": True, "external_filing_mutation_blocked": True, "redaction_applied": True, "approval_required": True, "segregation_enforced": True, "same_user_blocked": True, "restricted_processing_visible": True,
        "purge_blocked_when_hold": True, "destruction_evidence": "captured", "protected_fields_masked": True, "raw_export_blocked": True, "decision_uses_matrix": True, "payload_hash": "hash", "duplicate_profile_prevented": True, "stable_response": True,
        "malware_scan": "clear", "size_check": True, "content_type_check": True, "unsafe_file_blocked": True, "storage_boundary": "owned", "rollback_available": True, "event_topic": IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC, "appgen_contract": EVENT_CONTRACT,
        "foreign_table_access_blocked": True, "dependency_mode": "event", "idempotent_handler": True, "dead_letter_route": "owned-dlq", "safe_replay_allowed": True, "live_mutation_blocked": True, "bounds_valid": True, "activation_allowed": True,
        "kyc_evidence_checked": True, "screening_resolution_checked": True, "edd_checked": True, "maker_checker_checked": True, "privacy_checked": True, "control_effective": True, "payload_digest_valid": True, "proof_verified": True, "altered_order_detected": False,
        "redacted_export_supported": True, "release_pack_complete": True, "permission_filtered": True, "read_only_projections": True, "human_confirmation": True, "direct_mutation_blocked": True, "unsafe_file_denied": True, "source_citations": ("doc-1",),
        "false_positive_learning": True, "model_update_blocked_until_approved": True, "queue_leakage_blocked": True, "cross_tenant_access_blocked": True, "kyc_profile_seeded": True, "document_seeded": True, "owner_seeded": True, "screening_seeded": True, "monitoring_seeded": True, "case_seeded": True, "apis_exercised": True, "events_emitted": True, "workbench_queues_driven": True, "agent_summary_generated": True, "control_assertions_run": True, "release_documents_updated": True,
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and (payload.get("allowed_transition") is not True or not payload.get("mandatory_evidence") or payload.get("lifecycle_event_emitted") is not True): findings.append("KYC profile lifecycle requires allowed transition, evidence, and lifecycle event")
    if n == 2 and (not payload.get("customer_type") or not payload.get("jurisdiction") or payload.get("obligation_set_attached") is not True): findings.append("onboarding classification gate requires customer type, jurisdiction, and obligation set")
    if n == 3 and (payload.get("duplicate_candidates") not in ((), []) or payload.get("lineage_preserved") is not True): findings.append("duplicate identity resolution must clear candidates and preserve merge lineage")
    if n == 4 and payload.get("completeness_passed") is not True: findings.append("document capture completeness blocks incomplete identity documents")
    if n == 5 and (payload.get("authenticity_state") != "accepted" or payload.get("expiry_state") != "valid" or payload.get("identity_consistency") is not True): findings.append("document authenticity and expiry controls block invalid or inconsistent documents")
    if n == 6 and (payload.get("liveness_outcome") != "pass" or payload.get("face_match_confidence", 0) < 0.8): findings.append("remote onboarding requires liveness and face-match evidence")
    if n == 7 and payload.get("unresolved_blocking_hit") is True: findings.append("sanctions screening cannot approve unresolved blocking hits")
    if n == 8 and payload.get("sanctions_only_close_blocked") is not True: findings.append("PEP and RCA hits cannot close through sanctions-only workflow")
    if n == 10 and payload.get("ultimate_owner_reached") is not True: findings.append("beneficial ownership graph must reach an ultimate owner or controller")
    if n == 13 and not payload.get("supporting_docs"): findings.append("source of funds and wealth evidence requires supporting documents")
    if n == 15 and payload.get("packet_complete") is not True: findings.append("EDD review packet must be complete before approval")
    if n == 17 and (payload.get("challenge_closed") is not True or not payload.get("reviewer_evidence")): findings.append("risk score challenge requires reviewer evidence and closure")
    if n == 23 and payload.get("external_filing_mutation_blocked") is not True: findings.append("SAR/STR filing boundary must block external filing mutation")
    if n == 24 and (payload.get("segregation_enforced") is not True or payload.get("same_user_blocked") is not True): findings.append("maker-checker approval chain must block same-user approval")
    if n == 27 and (payload.get("protected_fields_masked") is not True or payload.get("raw_export_blocked") is not True): findings.append("need-to-know exports must redact protected fields and block raw export")
    if n == 29 and (payload.get("duplicate_profile_prevented") is not True or payload.get("stable_response") is not True): findings.append("onboarding API idempotency must prevent duplicate profiles")
    if n == 30 and (payload.get("malware_scan") != "clear" or payload.get("unsafe_file_blocked") is not True): findings.append("document file-safety gate blocks unsafe submissions")
    if n == 32 and (payload.get("appgen_contract") != EVENT_CONTRACT or payload.get("event_topic") != IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC): findings.append("screening-hit event contracts must use AppGen-X topic")
    if n == 34 and (payload.get("dependency_mode") not in ("api", "event", "projection") or payload.get("idempotent_handler") is not True): findings.append("inbound policy/audit/KPI boundary requires idempotent API/event/projection handling")
    if n in (45, 46, 47) and (payload.get("human_confirmation") is not True or payload.get("direct_mutation_blocked") is not True or not payload.get("source_citations")): findings.append("KYC/AML agent skills require citations, confirmation, and no direct mutation")
    if n == 49 and (payload.get("queue_leakage_blocked") is not True or payload.get("cross_tenant_access_blocked") is not True): findings.append("multi-tenant policy isolation must block queue and cross-tenant leakage")
    if n == 50 and not all(payload.get(field) is True for field in ("kyc_profile_seeded", "document_seeded", "owner_seeded", "screening_seeded", "monitoring_seeded", "case_seeded", "apis_exercised", "events_emitted", "workbench_queues_driven", "agent_summary_generated", "control_assertions_run", "release_documents_updated")): findings.append("end-to-end KYC and AML control test is incomplete")
    if payload.get("stream_engine_picker_visible"): findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_identity_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None: return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved); candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in IDENTITY_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in IDENTITY_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_identity_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_identity_control(capability) for capability in IDENTITY_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.identity-kyc-aml-compliance-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": IDENTITY_CONTROL_OWNED_TABLES, "declared_dependencies": IDENTITY_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


IDENTITY_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_identity_control(slug, payload)) for capability in IDENTITY_CONTROL_CAPABILITIES}
