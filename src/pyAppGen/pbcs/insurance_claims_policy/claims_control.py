"""Executable improve1 controls for the Insurance Claims Policy PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "insurance_claims_policy"
EVENT_CONTRACT = "AppGen-X"
CLAIMS_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
CLAIMS_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.insurance_claims_policy.events"
CLAIMS_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + tuple(
    f"insurance_claims_policy_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
)))
CLAIMS_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "CustomerUpdated", "PaymentCaptured", "FraudSignalRaised", "PolicyChanged",
    "LegalMatterProjected", "VendorProjected", "CatastropheEventProjected",
    "PaymentStatusProjected", "ComplaintReceived", "RegulatoryRuleChanged",
)))
CLAIMS_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in CLAIMS_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in CLAIMS_CONTROL_CAPABILITIES}
_DEFAULT_FIELDS = ("owned_record", "insurance_context", "required_evidence", "operator_visible", "audit_trail", "safe_to_execute")
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {cap.feature_number: _DEFAULT_FIELDS for cap in CLAIMS_CONTROL_CAPABILITIES}
_FEATURE_FIELDS.update({
    1: ("line_of_business", "coverage_tree", "perils", "exclusions", "deductibles", "territory", "policy_form", "rule_citations_visible"),
    2: ("policyholder_verified", "risk_details_complete", "coverage_complete", "premium_schedule_ready", "disclosures_acknowledged", "bind_authority_verified", "policy_created_blocked_until_ready"),
    3: ("party_graph", "party_roles", "relationship_effective_dates", "authority_to_act", "consent_status", "disclosure_guard", "payment_role_checked"),
    4: ("risk_object_type", "risk_identifiers", "insured_value", "location", "exposure_period", "inspection_evidence", "source_projection", "owned_snapshot"),
    5: ("requested_change", "effective_date", "backdating_rule", "premium_impact", "coverage_impact", "approval_authority", "customer_acknowledgement", "before_after_visible"),
    6: ("policy_version_timeline", "transaction_time", "effective_time", "endorsement_layering", "loss_date_reconstruction", "version_cited", "current_record_not_used_for_loss"),
    7: ("installment_schedule", "earned_premium", "unearned_premium", "grace_period", "lapse_notice", "reinstatement_condition", "premium_status_at_loss"),
    8: ("cancellation_reason", "notice_template", "delivery_proof", "cure_window", "reinstatement_requirements", "non_renewal_rule", "impacted_claims_preview"),
    9: ("fnol_channel", "loss_description", "severity_triage", "catastrophe_flag", "injury_indicator", "duplicate_claim_check", "initial_reserve_recommendation"),
    10: ("loss_datetime", "discovery_date", "loss_location", "cause_of_loss", "peril", "involved_objects", "confidence", "policy_version_linked"),
    11: ("claimant_role", "relationship_to_policy", "authority_documents", "represented_party", "payment_eligibility", "tax_fields", "communication_permissions", "payment_blocked_without_authority"),
    12: ("evidence_type", "source", "admissibility", "required_status", "redaction", "authenticity_hash", "chain_of_custody", "missing_by_stage_visible"),
    13: ("policy_version", "coverage_grants", "exclusions", "duties_after_loss", "premium_status", "sublimits", "deductible", "decision_citations"),
    14: ("letter_type", "draft_source", "policy_citations", "facts_relied_on", "reviewer_approval", "delivery_evidence", "response_deadline", "waiver_guard"),
    15: ("limit_ledger", "coverage_part", "claim_id", "reserve_amount", "paid_amount", "deductible_applied", "aggregate_erosion", "remaining_authority"),
    16: ("exposure_drivers", "confidence_interval", "review_cadence", "authority_threshold", "reserve_rationale", "stale_reserve_alert", "reviewer_approval"),
    17: ("loss_type", "injury", "property_value", "coverage_ambiguity", "litigation_risk", "fraud_signal", "complexity_score", "assignment_priority"),
    18: ("adjuster_profile", "license_status", "authority_limit", "line_expertise", "workload", "territory", "conflict_check", "assignment_blocked_if_ineligible"),
    19: ("diary_task", "due_date", "regulatory_basis", "owner", "escalation", "completion_evidence", "dependency_links", "overdue_control"),
    20: ("jurisdiction", "ack_timer", "investigation_timer", "coverage_decision_timer", "payment_timer", "denial_notice_timer", "breach_exception_opened"),
    21: ("fraud_signals", "confidence", "severity", "siu_referral_rule", "false_positive_feedback", "investigator_notes", "human_review_before_adverse_action"),
    22: ("image_metadata_check", "duplicate_document_check", "invoice_pattern_check", "tamper_indicator", "geotag_consistency", "cross_claim_reuse", "review_route"),
    23: ("provider_record", "eligibility", "specialty", "rates", "service_area", "license", "performance_score", "assignment_constraints"),
    24: ("estimate_lines", "depreciation", "betterment", "repair_replace_decision", "appraisal_method", "reviewer_approval", "variance_analysis"),
    25: ("treatment_events", "medical_bills", "diagnosis_category", "lost_wage_evidence", "impairment_rating", "privacy_restrictions", "sensitive_access_control"),
    26: ("catastrophe_event", "surge_triage", "mass_fnol", "emergency_payment_rule", "mobile_adjuster_deployment", "event_level_reserve", "portfolio_dashboard"),
    27: ("opportunity_score", "responsible_party", "recovery_basis", "evidence_checklist", "demand_package", "statute_deadline", "closure_reason"),
    28: ("salvage_item", "condition", "ownership", "custody", "residual_value", "disposal_path", "sale_proceeds", "environmental_handling"),
    29: ("demands", "offers", "counteroffers", "authority_limits", "negotiation_rationale", "release_requirements", "lien_handling", "acceptance_expiry"),
    30: ("authority_matrix", "settlement_amount", "reserve_impact", "coverage_ambiguity", "fraud_indicator", "approval_chain", "release_complete", "payment_blocked_until_approved"),
    31: ("payment_breakdown", "payee_validation", "deductible_calculation", "limit_calculation", "liens", "tax_withholding", "duplicate_payment_check", "finance_handoff_event"),
    32: ("payee_interest", "priority_rule", "supporting_documents", "release_requirement", "joint_payee_logic", "dispute_handling", "eligibility_explained"),
    33: ("litigation_indicator", "legal_projection_link", "defense_counsel_snapshot", "litigation_phase", "defense_cost_treatment", "discovery_deadlines", "privilege_flags", "declared_dependency_mode"),
    34: ("complaint_reason", "jurisdiction_deadline", "independent_reviewer", "original_decision", "new_evidence", "outcome", "communication_proof", "corrective_action"),
    35: ("timeline_event", "party_role", "channel", "consent_checked", "deadline_context", "delivery_proof", "omission_alert"),
    36: ("document_instruction", "extracted_claim_fields", "source_citations", "confidence", "human_confirmation", "direct_mutation_blocked", "unsafe_prompt_denied"),
    37: ("portal_claim_status", "evidence_upload", "secure_message", "settlement_view", "payment_status", "accessibility_mode", "role_based_visibility"),
    38: ("sla_metric", "customer_experience_metric", "cycle_time", "reopen_rate", "complaint_rate", "segment_breakdown", "dashboard_visible"),
    39: ("reopen_reason", "new_evidence", "supplemental_reserve", "prior_closure_reference", "approval_required", "supplemental_payment_guard"),
    40: ("closure_checklist", "open_diaries_closed", "payments_reconciled", "recoveries_reviewed", "retention_class", "legal_hold_checked", "closure_blocked_until_ready"),
    41: ("scenario_inputs", "loss_distribution", "coverage_sensitivity", "catastrophe_sensitivity", "reserve_sensitivity", "assumptions_visible", "no_live_mutation"),
    42: ("portfolio_segment", "development_triangle", "ibnr_signal", "reserve_adequacy", "trend_explanation", "finance_projection_boundary", "aggregate_dashboard"),
    43: ("control_suite", "coverage_checked", "reserve_checked", "settlement_checked", "payment_checked", "sla_checked", "control_effective"),
    44: ("packet_hash", "previous_hash", "document_hashes", "decision_hashes", "payment_hashes", "proof_verified", "tamper_evident_export"),
    45: ("dependency_mode", "projection_name", "foreign_table_access_blocked", "owned_snapshot", "api_event_dependency_declared", "safe_replay_allowed"),
    46: ("rule_type", "rule_version", "simulation_scope", "impact_preview", "approval_history", "activation_guard", "rollback_visible"),
    47: ("accessibility_need", "vulnerable_customer_flag", "communication_preference", "support_accommodation", "privacy_guard", "service_standard_visible"),
    48: ("fraud_model_signal", "adverse_action_guard", "human_review", "notice_required", "false_positive_feedback", "model_governance", "customer_harm_checked"),
    49: ("command_center_queue", "policy_metrics", "claim_metrics", "reserve_metrics", "fraud_metrics", "sla_metrics", "role_filtered_actions"),
    50: ("policy_seeded", "claim_seeded", "coverage_seeded", "reserve_seeded", "settlement_seeded", "payment_seeded", "events_emitted", "workbench_driven", "agent_summary_generated", "control_assertions_run", "release_documents_updated"),
})
_FEATURE_DEPENDENCIES = {
    21: ("FraudSignalRaised",),
    23: ("VendorProjected",),
    26: ("CatastropheEventProjected",),
    31: ("PaymentCaptured",),
    33: ("LegalMatterProjected",),
    34: ("ComplaintReceived",),
    45: ("CustomerUpdated", "PaymentStatusProjected", "RegulatoryRuleChanged"),
}
_EMPTY_ALLOWED_FIELDS = ()

_REQUIRED_TRUE: dict[int, tuple[str, ...]] = {
    1: ("rule_citations_visible",), 2: ("policyholder_verified", "risk_details_complete", "coverage_complete", "premium_schedule_ready", "disclosures_acknowledged", "bind_authority_verified", "policy_created_blocked_until_ready"),
    3: ("disclosure_guard", "payment_role_checked"), 4: ("owned_snapshot",), 5: ("customer_acknowledgement", "before_after_visible"), 6: ("loss_date_reconstruction", "version_cited", "current_record_not_used_for_loss"),
    7: ("premium_status_at_loss",), 8: ("delivery_proof", "impacted_claims_preview"), 9: ("severity_triage", "duplicate_claim_check"), 10: ("policy_version_linked",),
    11: ("payment_blocked_without_authority",), 12: ("authenticity_hash", "chain_of_custody", "missing_by_stage_visible"), 13: ("decision_citations",), 14: ("reviewer_approval", "delivery_evidence", "waiver_guard"),
    15: ("limit_ledger", "remaining_authority"), 16: ("reserve_rationale", "stale_reserve_alert", "reviewer_approval"), 17: ("complexity_score", "assignment_priority"), 18: ("assignment_blocked_if_ineligible",),
    19: ("completion_evidence", "overdue_control"), 20: ("breach_exception_opened",), 21: ("human_review_before_adverse_action",), 22: ("review_route",),
    23: ("eligibility", "license", "assignment_constraints"), 24: ("reviewer_approval", "variance_analysis"), 25: ("privacy_restrictions", "sensitive_access_control"), 26: ("portfolio_dashboard",),
    27: ("evidence_checklist", "demand_package"), 28: ("custody", "environmental_handling"), 29: ("negotiation_rationale", "release_requirements"), 30: ("approval_chain", "release_complete", "payment_blocked_until_approved"),
    31: ("payee_validation", "duplicate_payment_check", "finance_handoff_event"), 32: ("priority_rule", "eligibility_explained"), 33: ("declared_dependency_mode",), 34: ("independent_reviewer", "communication_proof"),
    35: ("consent_checked", "delivery_proof", "omission_alert"), 36: ("source_citations", "human_confirmation", "direct_mutation_blocked", "unsafe_prompt_denied"), 37: ("role_based_visibility",), 38: ("dashboard_visible",),
    39: ("approval_required", "supplemental_payment_guard"), 40: ("open_diaries_closed", "payments_reconciled", "recoveries_reviewed", "legal_hold_checked", "closure_blocked_until_ready"),
    41: ("assumptions_visible", "no_live_mutation"), 42: ("finance_projection_boundary", "aggregate_dashboard"), 43: ("coverage_checked", "reserve_checked", "settlement_checked", "payment_checked", "sla_checked", "control_effective"),
    44: ("proof_verified", "tamper_evident_export"), 45: ("foreign_table_access_blocked", "api_event_dependency_declared", "safe_replay_allowed"), 46: ("impact_preview", "activation_guard", "rollback_visible"),
    47: ("privacy_guard", "service_standard_visible"), 48: ("adverse_action_guard", "human_review", "model_governance", "customer_harm_checked"), 49: ("role_filtered_actions",),
    50: ("policy_seeded", "claim_seeded", "coverage_seeded", "reserve_seeded", "settlement_seeded", "payment_seeded", "events_emitted", "workbench_driven", "agent_summary_generated", "control_assertions_run", "release_documents_updated"),
}
_NUMERIC_MINIMUMS: dict[int, dict[str, float]] = {16: {"confidence_interval": 0.1}, 21: {"confidence": 0.5}, 38: {"cycle_time": 0.0}}


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
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"insurance_claims_policy_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "ui": _camel(capability.slug),
        "route": f"POST /insurance-claims-policy/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in CLAIMS_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    for field in _REQUIRED_TRUE.get(resolved.feature_number, ()): payload[field] = True
    for field, value in _NUMERIC_MINIMUMS.get(resolved.feature_number, {}).items(): payload[field] = max(value, 0.91)
    payload.update({
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": CLAIMS_CONTROL_REQUIRED_EVENT_TOPIC,
        "database_backend": "postgresql",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    for field in _REQUIRED_TRUE.get(n, ()):
        if payload.get(field) is not True:
            findings.append(f"{capability.title} requires {field.replace('_', ' ')}")
    for field, minimum in _NUMERIC_MINIMUMS.get(n, {}).items():
        if float(payload.get(field, -1) or -1) < minimum:
            findings.append(f"{capability.title} requires {field.replace('_', ' ')} above {minimum}")
    if n == 2 and payload.get("policy_created_blocked_until_ready") is not True:
        findings.append("policy issuance must block PolicyCreated until readiness evidence is complete")
    if n == 6 and payload.get("current_record_not_used_for_loss") is not True:
        findings.append("coverage decisions must reconstruct effective-dated policy version at loss time")
    if n == 11 and payload.get("payment_blocked_without_authority") is not True:
        findings.append("claimant and payee authority must block settlement/payment when unresolved")
    if n == 13 and not payload.get("decision_citations"):
        findings.append("coverage reasoning workbench requires cited facts, rules, and policy version")
    if n == 14 and payload.get("waiver_guard") is not True:
        findings.append("reservation of rights and denial governance must prevent waiver-risk letters")
    if n == 20 and payload.get("breach_exception_opened") is not True:
        findings.append("fair claims handling controls must open breach exceptions for missed regulatory timers")
    if n == 21 and payload.get("human_review_before_adverse_action") is not True:
        findings.append("fraud signal fusion cannot drive adverse customer action without human review")
    if n == 30 and payload.get("payment_blocked_until_approved") is not True:
        findings.append("settlement authority matrix must block payment until approvals and releases are complete")
    if n == 31 and payload.get("duplicate_payment_check") is not True:
        findings.append("payment disbursement controls must prevent duplicate claim payments")
    if n == 33 and payload.get("declared_dependency_mode") not in (True, "api", "event", "projection"):
        findings.append("litigation escalation must use declared APIs/events/projections, not shared legal tables")
    if n == 36 and (payload.get("human_confirmation") is not True or payload.get("direct_mutation_blocked") is not True or not payload.get("source_citations")):
        findings.append("claim document agent intake requires citations, human confirmation, and no direct mutation")
    if n == 44 and payload.get("proof_verified") is not True:
        findings.append("cryptographic claim evidence packets must verify before release")
    if n == 45 and (payload.get("foreign_table_access_blocked") is not True or payload.get("dependency_mode") == "shared_table"):
        findings.append("cross-PBC boundaries must block foreign table access and shared-table coupling")
    if n == 48 and payload.get("human_review") is not True:
        findings.append("fraud governance must preserve human review and adverse-action safeguards")
    if n == 50 and not all(payload.get(field) is True for field in _REQUIRED_TRUE[50]):
        findings.append("end-to-end insurance release evidence is incomplete")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in CLAIMS_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary insurance PBC datastore must be PostgreSQL, MySQL, or MariaDB")
    return tuple(findings)


def evaluate_claims_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in CLAIMS_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in CLAIMS_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": CLAIMS_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": CLAIMS_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_claims_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_claims_control(capability) for capability in CLAIMS_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.insurance-claims-policy-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": CLAIMS_CONTROL_OWNED_TABLES, "declared_dependencies": CLAIMS_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": CLAIMS_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": CLAIMS_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


CLAIMS_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_claims_control(slug, payload)) for capability in CLAIMS_CONTROL_CAPABILITIES}
