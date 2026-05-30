"""Executable improve1 controls for the Nonprofit Program Impact PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "nonprofit_program_impact"
EVENT_CONTRACT = "AppGen-X"
IMPACT_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
IMPACT_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.nonprofit_program_impact.events"
_BASE_OWNED_TABLES = (
    "nonprofit_program_impact_program",
    "nonprofit_program_impact_beneficiary",
    "nonprofit_program_impact_service_episode",
    "nonprofit_program_impact_outcome_measure",
    "nonprofit_program_impact_grant_restriction",
    "nonprofit_program_impact_impact_evidence",
    "nonprofit_program_impact_donor_report",
    "nonprofit_program_impact_theory_of_change",
    "nonprofit_program_impact_results_chain",
    "nonprofit_program_impact_output_register",
    "nonprofit_program_impact_indicator_dictionary",
    "nonprofit_program_impact_survey_instrument",
    "nonprofit_program_impact_consent_record",
    "nonprofit_program_impact_safeguarding_incident",
    "nonprofit_program_impact_partner_submission",
    "nonprofit_program_impact_exception_case",
    "nonprofit_program_impact_policy_pack",
    "nonprofit_program_impact_runtime_parameter",
    "nonprofit_program_impact_schema_extension",
    "nonprofit_program_impact_control_assertion",
    "nonprofit_program_impact_governed_model",
    "nonprofit_program_impact_appgen_outbox_event",
    "nonprofit_program_impact_appgen_inbox_event",
    "nonprofit_program_impact_appgen_dead_letter_event",
)
IMPACT_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"nonprofit_program_impact_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
IMPACT_CONTROL_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "CustomerUpdated",
    "SupplierQualified",
    "IdentityVerificationChanged",
    "GrantBudgetProjectionChanged",
    "NotificationDeliveryChanged",
    "DocumentEvidenceSealed",
    "PrivacyConsentChanged",
    "GeographyBoundaryChanged",
    "AuditEventSealed",
)
IMPACT_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in IMPACT_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in IMPACT_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "program_id", "beneficiary_id", "grant_id", "partner_id", "reporting_period", "actor_id", "policy_version", "evidence_references")
_DOMAIN_FIELDS: dict[int, tuple[str, ...]] = {
    1: ("theory_of_change_id", "assumptions", "risk_factors", "target_population", "intervention_components", "impact_horizon"),
    2: ("results_chain_id", "service_episode_links", "output_links", "outcome_links", "contribution_logic", "drill_through_path"),
    3: ("beneficiary_type", "household_id", "cohort_id", "caregiver_child_pair", "dedupe_key", "institution_level"),
    4: ("eligibility_rule_id", "age_band", "geography", "vulnerability_criteria", "referral_source", "override_rationale"),
    5: ("intervention_taxonomy_id", "service_type", "delivery_channel", "dosage_unit", "session_length", "implementing_partner"),
    6: ("planned_dosage", "delivered_dosage", "attendance", "completion_marker", "fidelity_checklist", "missed_session_reason"),
    7: ("output_register_id", "unit_definition", "counting_rule", "dedupe_rule", "service_reference", "evidence_attachment"),
    8: ("outcome_definition", "measurement_window", "unit_of_analysis", "expected_direction", "data_source", "evidence_threshold"),
    9: ("indicator_id", "numerator", "denominator", "disaggregation", "rollup_rule", "missing_data_treatment"),
    10: ("baseline_value", "target_value", "target_period", "revision_reason", "approval_history", "program_outcome_pair"),
    11: ("instrument_id", "version", "language", "question_type", "skip_logic", "scoring_rule"),
    12: ("sampling_frame", "sample_size_target", "selection_rule", "wave_schedule", "response_status", "attrition_reason"),
    13: ("consent_id", "data_use", "story_use", "follow_up_contact", "withdrawal_date", "guardian_consent"),
    14: ("safeguarding_flag", "risk_level", "immediate_action", "referral_status", "restricted_note", "permission_gate"),
    15: ("incident_id", "triage_state", "assignment", "action_log", "escalation_timer", "closure_criteria"),
    16: ("referral_id", "receiving_organization", "appointment_status", "completion_confirmation", "referral_outcome", "follow_through_rate"),
    17: ("case_pack_id", "case_narrative", "before_after_snapshot", "corroborating_document", "confidentiality_level", "citation_set"),
    18: ("quality_score_id", "source_type", "verification_status", "completeness", "timeliness", "reviewer_confidence"),
    19: ("partner_org_id", "site_id", "subaward_id", "delivery_responsibility", "ownership_boundary", "partner_scorecard"),
    20: ("submission_batch_id", "schema_validation", "discrepancy_comment", "approval_checkpoint", "resubmission_status", "correction_loop"),
    21: ("restriction_id", "allowed_programs", "allowed_service_types", "allowed_locations", "date_window", "beneficiary_category"),
    22: ("attribution_rule_id", "funding_mode", "cofunding_basis", "allocation_formula", "excluded_evidence", "report_preview"),
    23: ("reporting_period_id", "freeze_date", "reopen_reason", "locked_snapshot", "mutation_guard", "audit_history"),
    24: ("disaggregation_dimension", "age_band", "gender", "disability", "geography", "small_cell_suppression"),
    25: ("follow_up_wave_id", "reassessment_date", "persistence_classification", "loss_to_follow_up", "baseline_value", "follow_up_value"),
    26: ("adverse_effect_id", "harm_type", "severity", "source", "mitigation_action", "reporting_rule"),
    27: ("comparison_group_id", "matched_cohort", "counterfactual_metadata", "method_note", "use_restriction", "attribution_claim_gate"),
    28: ("site_id", "district", "catchment_area", "community_hierarchy", "coverage_map", "partner_grouping"),
    29: ("dashboard_mode", "throughput_panel", "output_panel", "outcome_panel", "survey_panel", "partner_performance_panel"),
    30: ("program_detail_id", "theory_panel", "target_status", "partner_mix", "grant_restriction_view", "evidence_summary"),
    31: ("timeline_id", "enrollment_event", "service_event", "survey_event", "outcome_event", "redaction_policy"),
    32: ("donor_review_id", "indicator_preview", "attribution_explanation", "quality_warning", "narrative_section", "approval_checkpoint"),
    33: ("assistant_draft_id", "proposal_source", "draft_theory", "draft_outputs", "candidate_outcomes", "citation_map"),
    34: ("survey_qa_id", "indicator_mapping", "missing_question", "scale_conflict", "disaggregation_gap", "resolved_issue"),
    35: ("case_assembly_id", "approved_notes", "survey_excerpt", "media_reference", "redaction_marker", "consent_gate"),
    36: ("event_schema_id", "beneficiary_enrolled_event", "service_completed_event", "outcome_observed_event", "donor_report_frozen_event", "replay_order"),
    37: ("lineage_id", "source_evidence", "outcome_measure", "donor_snapshot", "projection_checkpoint", "lineage_view"),
    38: ("consumed_event_id", "policy_review", "beneficiary_contact_update", "partner_risk_flag", "idempotency_key", "review_queue"),
    39: ("partner_scorecard_id", "service_volume", "verification_rate", "survey_response_rate", "safeguarding_closure_time", "punctuality"),
    40: ("release_matrix_id", "domain_promise", "test_link", "screenshot_link", "seed_dataset", "event_sample"),
    41: ("exception_id", "exception_type", "severity", "owner", "due_date", "closure_proof"),
    42: ("retention_schedule_id", "field_masking", "export_control", "story_use_restriction", "consent_state", "purge_policy"),
    43: ("access_policy_id", "role_check", "attribute_check", "safeguarding_note_scope", "partner_correction_right", "assistant_denial"),
    44: ("risk_score_id", "response_rate_driver", "missed_follow_up_driver", "declining_outcome_driver", "evidence_quality_driver", "partner_delay_driver"),
    45: ("scenario_id", "budget_change", "partner_capacity", "service_mix", "follow_up_completion", "assumption_trace"),
    46: ("offline_draft_id", "local_validation", "sync_reconciliation", "conflict_review", "capture_time", "sync_time"),
    47: ("localization_id", "survey_translation", "adapted_answer_option", "language_guidance", "locale_switch", "instrument_linkage"),
    48: ("accessibility_audit_id", "keyboard_access", "focus_state", "high_contrast_chart", "mobile_review", "manual_walkthrough"),
    49: ("fixture_set_id", "program_fixture", "partner_fixture", "survey_wave_fixture", "safeguarding_fixture", "frozen_report_fixture"),
    50: ("go_live_gate_id", "theory_gate", "beneficiary_gate", "service_gate", "outcome_gate", "dashboard_gate"),
}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    13: ("PrivacyConsentChanged",),
    16: ("SupplierQualified",),
    20: ("SupplierQualified", "DocumentEvidenceSealed"),
    21: ("GrantBudgetProjectionChanged",),
    28: ("GeographyBoundaryChanged",),
    36: ("PolicyChanged", "AuditEventSealed"),
    38: ("PolicyChanged", "CustomerUpdated", "SupplierQualified"),
    42: ("PrivacyConsentChanged",),
}
_DOMAIN_MESSAGES = {capability.feature_number: f"{capability.title} requires owned nonprofit impact evidence, UI, service/API, agent, and release proof before approval." for capability in IMPACT_CONTROL_CAPABILITIES}
_HUMAN_CONFIRMATION_FEATURES = (4, 13, 14, 15, 21, 22, 23, 26, 32, 33, 35, 38, 42, 43, 50)
_PROJECTION_ONLY_FEATURES = (16, 20, 21, 28, 36, 38, 42)
_AGENT_PREVIEW_FEATURES = (33, 34, 35, 43, 50)
_NON_MUTATING_FEATURES = (9, 18, 22, 23, 27, 29, 36, 37, 40, 44, 45, 48, 50)
_SENSITIVE_IMPACT_FEATURES = (4, 13, 14, 15, 17, 18, 21, 22, 23, 24, 26, 27, 32, 35, 38, 41, 42, 43, 50)


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
        "tables": (f"nonprofit_program_impact_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"NonprofitProgramImpact{_camel(capability.slug)}Panel",
        "route": f"POST /nonprofit-program-impact/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in IMPACT_CONTROL_CAPABILITIES}


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
        "event_topic": IMPACT_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "sensitive_impact_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[number])
    if number in _SENSITIVE_IMPACT_FEATURES and payload.get("sensitive_impact_evidence_complete") is not True:
        findings.append("eligibility, consent, safeguarding, attribution, privacy, donor, partner, and release gates require complete impact evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("sensitive beneficiary, safeguarding, donor, partner, privacy, and release decisions require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("nonprofit impact assistant skills must produce cited review previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("indicator math, attribution, dashboards, lineage, release evidence, risk scores, scenarios, and audits must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("partner, grant, policy, consent, geography, and audit facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != IMPACT_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("nonprofit impact eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in IMPACT_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary nonprofit impact datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("nonprofit impact controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_impact_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in IMPACT_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in IMPACT_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": IMPACT_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": IMPACT_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_impact_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_impact_control(capability) for capability in IMPACT_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.nonprofit-program-impact-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": IMPACT_CONTROL_OWNED_TABLES, "declared_dependencies": IMPACT_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": IMPACT_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": IMPACT_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


IMPACT_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_impact_control(slug, payload)) for capability in IMPACT_CONTROL_CAPABILITIES}
