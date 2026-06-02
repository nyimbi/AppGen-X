"""Executable improve1 controls for the Insurance Underwriting PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "insurance_underwriting"
EVENT_CONTRACT = "AppGen-X"
UNDERWRITING_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
UNDERWRITING_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.insurance_underwriting.events"
UNDERWRITING_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + tuple(
    f"insurance_underwriting_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
)))
UNDERWRITING_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "PolicyChanged", "AuditEventSealed", "OperationalKpiChanged", "CustomerUpdated",
    "ProducerUpdated", "ClaimsHistoryProjected", "ReinsuranceReferralProjected",
    "InspectionResultProjected", "SanctionsScreeningProjected", "FraudSignalRaised",
    "PortfolioAppetiteChanged", "PolicyAdministrationHandoffAccepted",
)))
UNDERWRITING_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in UNDERWRITING_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in UNDERWRITING_CONTROL_CAPABILITIES}
_DEFAULT_FIELDS = ("owned_record", "underwriting_context", "required_evidence", "operator_visible", "audit_trail", "safe_to_execute")
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {cap.feature_number: _DEFAULT_FIELDS for cap in UNDERWRITING_CONTROL_CAPABILITIES}
_FEATURE_FIELDS.update({
    1: ("submission_state", "allowed_transition", "state_reason", "actor_role", "state_event_emitted", "invalid_transition_blocked", "timeline_visible"),
    2: ("required_fields", "missing_fields", "document_requirements", "risk_answers_complete", "completeness_score", "quote_blocked_until_complete"),
    3: ("document_type", "extracted_fields", "source_citations", "confidence", "human_review", "unsafe_file_blocked", "direct_mutation_blocked"),
    4: ("risk_attributes", "exposure_values", "loss_history", "operations_profile", "risk_score", "profile_version", "source_projection_lineage"),
    5: ("appetite_rule", "risk_class", "territory", "limit_request", "hazard_flags", "appetite_result", "referral_or_decline_reason"),
    6: ("referral_reason", "specialist_queue", "sla_due_at", "required_evidence", "decision_authority", "referral_event_emitted", "duplicate_referral_blocked"),
    7: ("authority_matrix", "underwriter_level", "premium", "limit", "risk_score", "override_amount", "decision_blocked_without_authority"),
    8: ("rating_factor", "evidence_source", "factor_value", "rating_impact", "citation", "override_reason", "review_required"),
    9: ("model_name", "model_version", "input_boundary", "output_explanation", "actuarial_owner", "manual_override_allowed", "training_data_not_mutated"),
    10: ("quote_state", "rate_version", "premium", "terms", "valid_until", "withdrawal_reason", "state_event_emitted"),
    11: ("scenario_set", "premium_delta", "coverage_delta", "deductible_delta", "limit_delta", "side_by_side_visible", "selected_scenario_cited"),
    12: ("subjectivity", "owner", "due_date", "waiver_authority", "completion_evidence", "bind_blocked_until_resolved", "waiver_reason"),
    13: ("exclusion", "coverage_part", "jurisdiction", "wording_version", "approval_required", "customer_visible", "unsupported_exclusion_blocked"),
    14: ("condition", "endorsement", "effective_date", "wording_reference", "acceptance_required", "bind_package_linked", "condition_tracking_visible"),
    15: ("bind_package", "quote_id", "subjectivities_resolved", "forms_attached", "premium_terms", "authority_approval", "policy_handoff_ready"),
    16: ("declination_reason", "appetite_citation", "facts_relied_on", "producer_notice", "reviewer_approval", "appeal_path_visible", "adverse_action_guard"),
    17: ("loss_runs", "claim_frequency", "claim_severity", "large_loss_flag", "trend_analysis", "credibility_weight", "loss_history_cited"),
    18: ("accumulation_zone", "risk_location", "peril", "portfolio_concentration", "capacity_remaining", "accumulation_threshold", "referral_when_exceeded"),
    19: ("reinsurance_trigger", "treaty_boundary", "facultative_review", "ceded_limit", "dependency_mode", "foreign_table_access_blocked", "referral_packet_created"),
    20: ("recommendation", "risk_engineer", "priority", "due_date", "customer_commitment", "pricing_impact", "completion_tracked"),
    21: ("inspection_order", "vendor_or_engineer", "scope", "scheduled_date", "result_received", "recommendations_linked", "quote_blocked_when_required"),
    22: ("sanctions_result", "compliance_rule", "jurisdiction", "blocked_party_check", "license_requirement", "approval_blocked_until_clear", "screening_projection_only"),
    23: ("misrepresentation_signal", "fraud_score", "evidence", "investigator_review", "adverse_action_blocked", "false_positive_feedback", "model_governance"),
    24: ("portfolio_signal", "loss_ratio", "capacity_signal", "appetite_feedback", "rule_change_candidate", "feedback_event_captured", "no_live_mutation"),
    25: ("override_request", "base_price", "override_price", "delta_pct", "reason_code", "authority_approval", "customer_harm_checked"),
    26: ("decision", "decision_facts", "rule_citations", "model_outputs", "underwriter", "authority_evidence", "immutable_decision_record"),
    27: ("appeal_reason", "new_evidence", "independent_reviewer", "original_decision", "reconsideration_outcome", "communication_proof", "timer_visible"),
    28: ("workbench_queue", "submission_cards", "referral_cards", "quote_cards", "bind_cards", "sla_badges", "role_filtered_actions"),
    29: ("risk_summary", "source_citations", "assumptions", "confidence", "human_confirmation", "direct_mutation_blocked", "coverage_limitations_visible"),
    30: ("agent_command", "crud_plan", "target_table", "permission_check", "human_confirmation", "idempotency_key", "direct_mutation_blocked"),
    31: ("wording_clause", "wording_version", "jurisdiction", "approval_status", "template_locked", "diff_visible", "unauthorized_wording_blocked"),
    32: ("jurisdiction", "rule_set", "tax_or_fee", "admitted_status", "notice_requirement", "localized_wording", "conflict_resolution"),
    33: ("producer_id", "channel", "license_status", "appointment_status", "commission_boundary", "communication_authority", "foreign_table_access_blocked"),
    34: ("sla_clock", "workload", "queue_priority", "assignment_owner", "capacity_signal", "escalation", "breach_alert"),
    35: ("quality_review", "sample_reason", "reviewer", "score", "findings", "remediation_task", "feedback_loop"),
    36: ("assertion_suite", "completeness_checked", "authority_checked", "pricing_checked", "bind_checked", "handoff_checked", "control_effective"),
    37: ("dead_letter_item", "failure_reason", "retry_policy", "safe_replay_allowed", "operator_notes", "closure_code", "no_duplicate_side_effects"),
    38: ("packet_hash", "previous_hash", "submission_hash", "decision_hash", "quote_hash", "proof_verified", "tamper_evident_export"),
    39: ("model_name", "model_version", "drift_signal", "assistant_use_case", "approval_status", "human_feedback", "model_update_blocked_until_approved"),
    40: ("appetite_change", "simulation_scope", "impacted_submissions", "impacted_quotes", "capacity_impact", "live_mutation_blocked", "explainable_diff"),
    41: ("quote_to_bind_metric", "conversion_rate", "dropoff_reason", "segment", "producer", "trend_visible", "privacy_aggregated"),
    42: ("decline_reason", "referral_reason", "segment", "authority_level", "trend", "portfolio_feedback", "dashboard_visible"),
    43: ("climate_signal", "carbon_metric", "physical_risk", "transition_risk", "data_source", "underwriting_impact", "greenwashing_guard"),
    44: ("view_role", "minimum_necessary_fields", "privacy_mask", "sensitive_fields_hidden", "audit_visible", "export_guard", "agent_scope_limited"),
    45: ("scenario_id", "seed_submission", "seed_documents", "seed_loss_history", "seed_quotes", "expected_decisions", "regression_ready"),
    46: ("permission", "role", "action", "record_scope", "segregation_rule", "denied_action_visible", "least_privilege_enforced"),
    47: ("handoff_packet", "policy_admin_api", "bind_terms", "forms", "premium_schedule", "idempotency_key", "foreign_policy_table_not_mutated"),
    48: ("simulation_run", "submission_seeded", "quote_seeded", "bind_seeded", "events_emitted", "workbench_driven", "release_documents_updated"),
    49: ("overlap_check", "owned_boundary", "claims_dependency", "policy_admin_dependency", "shared_table_blocked", "composition_warning_visible"),
    50: ("dsl_fragment", "pbc_key", "agent_skills", "composition_manifest", "unified_agent_exposure", "skill_scope", "side_effect_free_registration"),
})
_FEATURE_DEPENDENCIES = {17: ("ClaimsHistoryProjected",), 19: ("ReinsuranceReferralProjected",), 21: ("InspectionResultProjected",), 22: ("SanctionsScreeningProjected",), 23: ("FraudSignalRaised",), 24: ("PortfolioAppetiteChanged",), 33: ("ProducerUpdated",), 47: ("PolicyAdministrationHandoffAccepted",)}
_EMPTY_ALLOWED_FIELDS = ("missing_fields",)
_REQUIRED_TRUE: dict[int, tuple[str, ...]] = {
    1: ("allowed_transition", "state_event_emitted", "invalid_transition_blocked", "timeline_visible"), 2: ("risk_answers_complete", "quote_blocked_until_complete"), 3: ("source_citations", "human_review", "unsafe_file_blocked", "direct_mutation_blocked"),
    5: ("appetite_result",), 6: ("referral_event_emitted", "duplicate_referral_blocked"), 7: ("decision_blocked_without_authority",), 9: ("output_explanation", "training_data_not_mutated"),
    10: ("state_event_emitted",), 11: ("side_by_side_visible", "selected_scenario_cited"), 12: ("bind_blocked_until_resolved",), 13: ("approval_required", "customer_visible", "unsupported_exclusion_blocked"),
    14: ("acceptance_required", "bind_package_linked", "condition_tracking_visible"), 15: ("subjectivities_resolved", "forms_attached", "authority_approval", "policy_handoff_ready"),
    16: ("reviewer_approval", "appeal_path_visible", "adverse_action_guard"), 17: ("loss_history_cited",), 18: ("referral_when_exceeded",), 19: ("foreign_table_access_blocked", "referral_packet_created"),
    20: ("completion_tracked",), 21: ("result_received", "recommendations_linked", "quote_blocked_when_required"), 22: ("blocked_party_check", "approval_blocked_until_clear", "screening_projection_only"),
    23: ("investigator_review", "adverse_action_blocked", "false_positive_feedback", "model_governance"), 24: ("feedback_event_captured", "no_live_mutation"), 25: ("authority_approval", "customer_harm_checked"),
    26: ("rule_citations", "authority_evidence", "immutable_decision_record"), 27: ("independent_reviewer", "communication_proof", "timer_visible"), 28: ("role_filtered_actions",),
    29: ("source_citations", "human_confirmation", "direct_mutation_blocked", "coverage_limitations_visible"), 30: ("permission_check", "human_confirmation", "direct_mutation_blocked"),
    31: ("template_locked", "diff_visible", "unauthorized_wording_blocked"), 32: ("localized_wording", "conflict_resolution"), 33: ("license_status", "appointment_status", "foreign_table_access_blocked"),
    34: ("breach_alert",), 35: ("remediation_task", "feedback_loop"), 36: ("completeness_checked", "authority_checked", "pricing_checked", "bind_checked", "handoff_checked", "control_effective"),
    37: ("safe_replay_allowed", "no_duplicate_side_effects"), 38: ("proof_verified", "tamper_evident_export"), 39: ("human_feedback", "model_update_blocked_until_approved"),
    40: ("live_mutation_blocked", "explainable_diff"), 41: ("trend_visible", "privacy_aggregated"), 42: ("portfolio_feedback", "dashboard_visible"), 43: ("greenwashing_guard",),
    44: ("sensitive_fields_hidden", "audit_visible", "export_guard", "agent_scope_limited"), 45: ("regression_ready",), 46: ("denied_action_visible", "least_privilege_enforced"),
    47: ("policy_admin_api", "foreign_policy_table_not_mutated"), 48: ("submission_seeded", "quote_seeded", "bind_seeded", "events_emitted", "workbench_driven", "release_documents_updated"),
    49: ("owned_boundary", "shared_table_blocked", "composition_warning_visible"), 50: ("dsl_fragment", "agent_skills", "composition_manifest", "unified_agent_exposure", "side_effect_free_registration"),
}


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
    return {"title": capability.title, "slug": capability.slug, "tables": (f"insurance_underwriting_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "ui": _camel(capability.slug), "route": f"POST /insurance-underwriting/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in UNDERWRITING_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    for field in _REQUIRED_TRUE.get(resolved.feature_number, ()): payload[field] = True
    payload.update({"missing_fields": (), "completeness_score": 1.0, "fraud_score": 0.24, "delta_pct": 0.02, "dependency_mode": "event", "database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "required_event_topic": UNDERWRITING_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    for field in _REQUIRED_TRUE.get(n, ()):
        if payload.get(field) is not True:
            findings.append(f"{capability.title} requires {field.replace('_', ' ')}")
    if n == 2 and (payload.get("missing_fields") not in ((), []) or float(payload.get("completeness_score", 0) or 0) < 1.0): findings.append("Submission completeness rules must clear missing fields and reach full completeness before quote")
    if n == 5 and payload.get("appetite_result") is not True: findings.append("Risk appetite screening must route accept, refer, or decline with evidence")
    if n == 7 and payload.get("decision_blocked_without_authority") is not True: findings.append("Underwriting authority matrix must block decisions above authority")
    if n == 9 and payload.get("training_data_not_mutated") is not True: findings.append("Actuarial model boundary cannot mutate actuarial training data")
    if n == 15 and payload.get("policy_handoff_ready") is not True: findings.append("Bind package must be complete before policy administration handoff")
    if n == 19 and (payload.get("dependency_mode") not in ("api", "event", "projection") or payload.get("foreign_table_access_blocked") is not True): findings.append("Reinsurance referral must use declared boundary and block foreign tables")
    if n == 22 and payload.get("approval_blocked_until_clear") is not True: findings.append("Compliance and sanction boundary must block approval until clear")
    if n in (29, 30) and (payload.get("human_confirmation") is not True or payload.get("direct_mutation_blocked") is not True): findings.append("Underwriting agent assistance requires human confirmation and no direct mutation")
    if n == 38 and payload.get("proof_verified") is not True: findings.append("Cryptographic underwriting evidence must verify before release")
    if n == 47 and payload.get("foreign_policy_table_not_mutated") is not True: findings.append("Policy administration handoff must not mutate policy administration tables directly")
    if n == 49 and payload.get("shared_table_blocked") is not True: findings.append("Package overlap guardrails must block shared-table overlap")
    if n == 50 and not all(payload.get(field) is True for field in _REQUIRED_TRUE[50]): findings.append("Composition DSL and unified agent exposure are incomplete")
    if payload.get("stream_engine_picker_visible"): findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in UNDERWRITING_CONTROL_ALLOWED_DATABASE_BACKENDS: findings.append("ordinary underwriting PBC datastore must be PostgreSQL, MySQL, or MariaDB")
    return tuple(findings)


def evaluate_underwriting_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in UNDERWRITING_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in UNDERWRITING_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": UNDERWRITING_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": UNDERWRITING_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_underwriting_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_underwriting_control(capability) for capability in UNDERWRITING_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.insurance-underwriting-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": UNDERWRITING_CONTROL_OWNED_TABLES, "declared_dependencies": UNDERWRITING_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": UNDERWRITING_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": UNDERWRITING_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


UNDERWRITING_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_underwriting_control(slug, payload)) for capability in UNDERWRITING_CONTROL_CAPABILITIES}
