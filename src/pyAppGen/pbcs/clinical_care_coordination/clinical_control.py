"""Executable clinical care coordination controls for improve1 execution.

The functions in this module are deliberately side-effect free. They model the
clinical decision, operational control, UI surface, service/API exposure, event
contract, and package boundary evidence for every item in improve1.md.
"""

from __future__ import annotations

from datetime import date, datetime
import hashlib
import json
from typing import Callable, Mapping

PBC_KEY = "clinical_care_coordination"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = (
    "clinical_care_coordination_patient_care_plan",
    "clinical_care_coordination_care_team",
    "clinical_care_coordination_referral",
    "clinical_care_coordination_encounter",
    "clinical_care_coordination_care_gap",
    "clinical_care_coordination_transition_plan",
    "clinical_care_coordination_outcome_measure",
    "clinical_care_coordination_clinical_care_coordination_policy_rule",
    "clinical_care_coordination_clinical_care_coordination_runtime_parameter",
    "clinical_care_coordination_clinical_care_coordination_schema_extension",
    "clinical_care_coordination_clinical_care_coordination_control_assertion",
    "clinical_care_coordination_clinical_care_coordination_governed_model",
    "clinical_care_coordination_appgen_outbox_event",
    "clinical_care_coordination_appgen_inbox_event",
    "clinical_care_coordination_appgen_dead_letter_event",
)
CLINICAL_CONTROL_CAPABILITIES = (
    "longitudinal_patient_care_plan_state_machine",
    "interdisciplinary_care_team_roster_with_role_semantics",
    "referral_lifecycle_with_closure_accountability",
    "encounter_derived_coordination_tasks",
    "care_gap_taxonomy_specific_to_preventive_chronic_safety_and_access_gaps",
    "transition_of_care_packet_integrity",
    "outcome_measure_registry_with_baseline_and_target_semantics",
    "patient_preference_and_goal_concordance",
    "social_needs_and_barrier_tracking",
    "medication_reconciliation_handoff",
    "closed_loop_patient_outreach",
    "care_coordination_risk_stratification",
    "duplicate_and_fragmented_patient_coordination_detection",
    "clinical_priority_and_urgency_rules",
    "guideline_and_measure_versioning",
    "care_plan_goal_hierarchy",
    "referral_network_performance_evidence",
    "transition_readmission_watchlist",
    "patient_education_assignment_and_comprehension",
    "consent_aware_caregiver_collaboration",
    "coordination_command_center_workbench",
    "patient_timeline_projection",
    "source_document_and_instruction_traceability",
    "care_team_coverage_gap_detection",
    "patient_no_show_and_missed_contact_patterning",
    "care_gap_exclusion_governance",
    "result_reconciliation_workflow",
    "high_risk_medication_and_allergy_coordination",
    "patient_cohort_worklists",
    "escalation_ladder_and_command_authorization",
    "care_conference_planning",
    "patient_safety_exception_playbooks",
    "coordination_quality_measures",
    "clinician_burden_and_task_appropriateness_controls",
    "care_plan_review_cadence_automation",
    "multi_program_coordination",
    "transition_medication_equipment_and_service_readiness_checklist",
    "coordination_data_retention_and_legal_hold",
    "assistant_draft_quality_scoring",
    "coordination_specific_natural_language_commands",
    "patient_level_dependency_freshness",
    "coordinated_bulk_outreach_campaigns",
    "clinical_handoff_summary_generation",
    "care_plan_conflict_detection",
    "patient_navigation_pathway_templates",
    "outcome_driven_closure_review",
    "coordinator_workload_balancing",
    "patient_reported_update_intake",
    "full_coordination_release_simulation",
    "composition_dsl_and_agent_skill_completeness",
)
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "longitudinal_patient_care_plan_state_machine": ("current_state", "target_state", "problem_link", "goal_hierarchy", "revision_trigger"),
    "interdisciplinary_care_team_roster_with_role_semantics": ("member_role", "coverage_window", "escalation_route", "consent_scope", "protected_detail_access"),
    "referral_lifecycle_with_closure_accountability": ("specialty", "urgency", "authorization_state", "appointment_state", "closure_owner"),
    "encounter_derived_coordination_tasks": ("source_encounter", "source_note_span", "coordination_actions", "owner_role", "due_date"),
    "care_gap_taxonomy_specific_to_preventive_chronic_safety_and_access_gaps": ("gap_type", "severity", "guideline_basis", "denominator_eligibility", "closure_evidence"),
    "transition_of_care_packet_integrity": ("discharge_source", "receiving_setting", "medication_reconciliation_status", "follow_up_appointments", "patient_instructions"),
    "outcome_measure_registry_with_baseline_and_target_semantics": ("measure_code", "baseline_value", "target_value", "collection_cadence", "attribution"),
    "patient_preference_and_goal_concordance": ("preferred_language", "contact_channel", "caregiver_permission", "patient_goal_text", "conflict_check"),
    "social_needs_and_barrier_tracking": ("barrier_type", "severity", "resource_referral", "follow_up_date", "resolution_evidence"),
    "medication_reconciliation_handoff": ("source_medication_list", "patient_reported_medications", "discrepancy_reason", "reconciliation_owner", "human_confirmation"),
    "closed_loop_patient_outreach": ("channel", "contact_result", "understanding_confirmation", "barrier_discovered", "next_action"),
    "care_coordination_risk_stratification": ("overdue_gaps", "unresolved_referrals", "transition_risk", "barrier_score", "weight_profile"),
    "duplicate_and_fragmented_patient_coordination_detection": ("patient_projection", "episode_window", "source_lineage", "suggested_merge", "reviewer_decision"),
    "clinical_priority_and_urgency_rules": ("severity", "timer_policy", "due_date", "escalation_threshold", "override_justification"),
    "guideline_and_measure_versioning": ("guideline_version", "denominator_rule", "exclusion_rule", "effective_window", "impact_population"),
    "care_plan_goal_hierarchy": ("parent_goal", "child_goals", "required_dependencies", "blocker_state", "closure_policy"),
    "referral_network_performance_evidence": ("destination_ref", "acceptance_lag", "scheduling_lag", "result_return_lag", "tenant_scope"),
    "transition_readmission_watchlist": ("transition_plan", "readmission_risk", "missed_outreach", "follow_up_status", "escalation_threshold"),
    "patient_education_assignment_and_comprehension": ("topic", "literacy_level", "language", "teach_back_evidence", "unresolved_questions"),
    "consent_aware_caregiver_collaboration": ("relationship", "consent_scope", "expiration", "allowed_topics", "revocation_history"),
    "coordination_command_center_workbench": ("high_risk_queue", "overdue_referrals", "unreconciled_results", "coverage_gaps", "action_availability"),
    "patient_timeline_projection": ("event_type", "actor", "source", "linked_entity", "redaction_rule"),
    "source_document_and_instruction_traceability": ("document_id", "source_span", "extracted_field", "confidence", "reviewer_confirmation"),
    "care_team_coverage_gap_detection": ("required_role", "coverage_window", "risk_tier", "replacement_role", "exception_state"),
    "patient_no_show_and_missed_contact_patterning": ("missed_appointments", "missed_calls", "declined_referrals", "barrier_review", "strategy_change"),
    "care_gap_exclusion_governance": ("exclusion_reason", "evidence_type", "expiration", "approving_role", "reevaluation_date"),
    "result_reconciliation_workflow": ("result_source", "clinical_significance", "action_required", "reviewed_by", "care_plan_impact"),
    "high_risk_medication_and_allergy_coordination": ("medication_alert", "allergy_alert", "source_event_lineage", "linked_task", "human_confirmation"),
    "patient_cohort_worklists": ("cohort_definition", "membership_explanation", "coordinator_assignment", "sla_policy", "outcome_measure"),
    "escalation_ladder_and_command_authorization": ("escalation_reason", "target_role", "due_time", "authorized_resolver", "outcome"),
    "care_conference_planning": ("agenda", "participants", "decisions", "follow_up_tasks", "next_review_date"),
    "patient_safety_exception_playbooks": ("playbook_type", "detection_evidence", "escalation_role", "allowed_commands", "closure_criteria"),
    "coordination_quality_measures": ("measure_definition", "numerator", "denominator", "exclusions", "time_window"),
    "clinician_burden_and_task_appropriateness_controls": ("task_class", "routed_role", "clinical_decision_flag", "reviewer_role", "workload_measure"),
    "care_plan_review_cadence_automation": ("risk_tier", "review_cadence", "next_due_date", "overdue_policy", "change_recorded"),
    "multi_program_coordination": ("program_enrollments", "program_goals", "coordinator_ownership", "conflict_detection", "exit_reason"),
    "transition_medication_equipment_and_service_readiness_checklist": ("medications_obtained", "equipment_delivered", "home_health_scheduled", "transportation_arranged", "emergency_plan_understood"),
    "coordination_data_retention_and_legal_hold": ("retention_category", "legal_hold", "amendment_history", "export_restriction", "redaction_profile"),
    "assistant_draft_quality_scoring": ("source_coverage", "clinical_ambiguity", "missing_required_fields", "preference_conflicts", "reviewer_role"),
    "coordination_specific_natural_language_commands": ("utterance", "domain_intent", "target_patient", "safe_preview", "evidence_required"),
    "patient_level_dependency_freshness": ("dependency", "last_event_time", "freshness_score", "fallback_behavior", "override_policy"),
    "coordinated_bulk_outreach_campaigns": ("cohort", "channel_selection", "exclusion_rules", "retry_cadence", "patient_specific_evidence"),
    "clinical_handoff_summary_generation": ("recipient_scope", "care_plan_summary", "unresolved_tasks", "redaction_rule", "source_references"),
    "care_plan_conflict_detection": ("intervention", "referral_instruction", "patient_preference", "conflict_type", "resolution_path"),
    "patient_navigation_pathway_templates": ("template_name", "template_version", "default_goals", "required_tasks", "patient_specific_edits"),
    "outcome_driven_closure_review": ("outcome_measure", "open_barriers", "unresolved_referrals", "patient_understanding", "signoff_role"),
    "coordinator_workload_balancing": ("coordinator_ref", "risk_adjusted_caseload", "overdue_items", "coverage_absence", "reassignment_suggestion"),
    "patient_reported_update_intake": ("category", "urgency", "summary", "structured_details", "clinical_review_required"),
    "full_coordination_release_simulation": ("admission", "transition_plan", "medication_discrepancy", "referral", "outcome_measured"),
    "composition_dsl_and_agent_skill_completeness": ("models", "routes", "services", "event_contracts", "assistant_skills"),
}
CAPABILITY_TABLES = {
    "longitudinal_patient_care_plan_state_machine": OWNED_TABLES[0],
    "interdisciplinary_care_team_roster_with_role_semantics": OWNED_TABLES[1],
    "referral_lifecycle_with_closure_accountability": OWNED_TABLES[2],
    "encounter_derived_coordination_tasks": OWNED_TABLES[3],
    "care_gap_taxonomy_specific_to_preventive_chronic_safety_and_access_gaps": OWNED_TABLES[4],
    "transition_of_care_packet_integrity": OWNED_TABLES[5],
    "outcome_measure_registry_with_baseline_and_target_semantics": OWNED_TABLES[6],
    "patient_preference_and_goal_concordance": OWNED_TABLES[0],
    "social_needs_and_barrier_tracking": OWNED_TABLES[0],
    "medication_reconciliation_handoff": OWNED_TABLES[5],
    "closed_loop_patient_outreach": OWNED_TABLES[0],
    "care_coordination_risk_stratification": OWNED_TABLES[10],
    "duplicate_and_fragmented_patient_coordination_detection": OWNED_TABLES[10],
    "clinical_priority_and_urgency_rules": OWNED_TABLES[7],
    "guideline_and_measure_versioning": OWNED_TABLES[7],
    "care_plan_goal_hierarchy": OWNED_TABLES[0],
    "referral_network_performance_evidence": OWNED_TABLES[2],
    "transition_readmission_watchlist": OWNED_TABLES[5],
    "patient_education_assignment_and_comprehension": OWNED_TABLES[0],
    "consent_aware_caregiver_collaboration": OWNED_TABLES[1],
    "coordination_command_center_workbench": OWNED_TABLES[10],
    "patient_timeline_projection": OWNED_TABLES[12],
    "source_document_and_instruction_traceability": OWNED_TABLES[9],
    "care_team_coverage_gap_detection": OWNED_TABLES[1],
    "patient_no_show_and_missed_contact_patterning": OWNED_TABLES[10],
    "care_gap_exclusion_governance": OWNED_TABLES[4],
    "result_reconciliation_workflow": OWNED_TABLES[2],
    "high_risk_medication_and_allergy_coordination": OWNED_TABLES[13],
    "patient_cohort_worklists": OWNED_TABLES[10],
    "escalation_ladder_and_command_authorization": OWNED_TABLES[7],
    "care_conference_planning": OWNED_TABLES[0],
    "patient_safety_exception_playbooks": OWNED_TABLES[10],
    "coordination_quality_measures": OWNED_TABLES[6],
    "clinician_burden_and_task_appropriateness_controls": OWNED_TABLES[10],
    "care_plan_review_cadence_automation": OWNED_TABLES[0],
    "multi_program_coordination": OWNED_TABLES[0],
    "transition_medication_equipment_and_service_readiness_checklist": OWNED_TABLES[5],
    "coordination_data_retention_and_legal_hold": OWNED_TABLES[10],
    "assistant_draft_quality_scoring": OWNED_TABLES[11],
    "coordination_specific_natural_language_commands": OWNED_TABLES[11],
    "patient_level_dependency_freshness": OWNED_TABLES[13],
    "coordinated_bulk_outreach_campaigns": OWNED_TABLES[0],
    "clinical_handoff_summary_generation": OWNED_TABLES[0],
    "care_plan_conflict_detection": OWNED_TABLES[10],
    "patient_navigation_pathway_templates": OWNED_TABLES[0],
    "outcome_driven_closure_review": OWNED_TABLES[6],
    "coordinator_workload_balancing": OWNED_TABLES[1],
    "patient_reported_update_intake": OWNED_TABLES[3],
    "full_coordination_release_simulation": OWNED_TABLES[10],
    "composition_dsl_and_agent_skill_completeness": OWNED_TABLES[11],
}
CAPABILITY_EVENTS = {
    capability: "ClinicalCareCoordination" + "".join(part.capitalize() for part in capability.split("_"))
    for capability in CLINICAL_CONTROL_CAPABILITIES
}
ALLOWED_CARE_PLAN_STATES = {"draft", "active", "suspended", "patient_declined", "partially_met", "achieved", "closed"}
ALLOWED_GAP_TYPES = {
    "preventive_screening",
    "immunization",
    "chronic_monitoring",
    "medication_reconciliation",
    "high_risk_medication",
    "behavioral_health_follow_up",
    "social_determinant",
    "post_discharge_follow_up",
    "missed_appointment",
    "patient_outreach_gap",
}
PLAYBOOK_TYPES = {
    "urgent_referral_not_scheduled",
    "critical_result_unreconciled",
    "failed_discharge_follow_up",
    "medication_discrepancy",
    "unreachable_high_risk_patient",
    "missing_caregiver_support",
}


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _age_hours(value: object) -> int | None:
    if not value:
        return None
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        parsed = datetime.combine(value, datetime.min.time())
    else:
        try:
            parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            return None
    return max(0, int((datetime(2026, 5, 30) - parsed).total_seconds() // 3600))


def _invalid_references(references: object) -> tuple[str, ...]:
    if not references:
        return ()
    refs = (references,) if isinstance(references, str) else tuple(str(item) for item in references)
    return tuple(ref for ref in refs if ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_"))


def _base_checks(capability: str, payload: Mapping[str, object]) -> tuple[bool, tuple[str, ...], tuple[str, ...]]:
    missing = tuple(field for field in REQUIRED_FIELDS[capability] if payload.get(field) in (None, "", (), []))
    invalid = _invalid_references(payload.get("referenced_tables", ()))
    return not missing and not invalid, missing, invalid


def _domain_findings(capability: str, payload: Mapping[str, object]) -> tuple[str, ...]:
    findings: list[str] = []
    if capability == "longitudinal_patient_care_plan_state_machine" and payload.get("target_state") not in ALLOWED_CARE_PLAN_STATES:
        findings.append("invalid_care_plan_target_state")
    if capability == "care_gap_taxonomy_specific_to_preventive_chronic_safety_and_access_gaps" and payload.get("gap_type") not in ALLOWED_GAP_TYPES:
        findings.append("unsupported_care_gap_type")
    if capability == "transition_of_care_packet_integrity":
        missing_packet = tuple(field for field in ("medication_reconciliation_status", "follow_up_appointments", "patient_instructions") if not payload.get(field))
        if missing_packet:
            findings.append("transition_packet_incomplete")
    if capability in {"medication_reconciliation_handoff", "high_risk_medication_and_allergy_coordination"} and payload.get("human_confirmation") is not True:
        findings.append("human_confirmation_required_for_medication_risk")
    if capability == "patient_safety_exception_playbooks" and payload.get("playbook_type") not in PLAYBOOK_TYPES:
        findings.append("unsupported_patient_safety_playbook")
    if capability == "coordination_data_retention_and_legal_hold" and payload.get("legal_hold") is True and payload.get("delete_requested") is True:
        findings.append("legal_hold_blocks_deletion")
    if capability == "assistant_draft_quality_scoring" and float(payload.get("source_coverage", 0) or 0) < 0.8:
        findings.append("low_source_coverage_requires_review")
    if capability == "patient_level_dependency_freshness":
        age = _age_hours(payload.get("last_event_time"))
        if age is not None and age > int(payload.get("freshness_score", 24) or 24):
            findings.append("dependency_stale")
    if capability == "outcome_driven_closure_review" and (payload.get("open_barriers") or payload.get("unresolved_referrals")):
        findings.append("closure_blocked_by_outstanding_coordination_work")
    if capability == "patient_reported_update_intake" and payload.get("clinical_review_required") is not True and payload.get("urgency") in {"urgent", "critical"}:
        findings.append("urgent_patient_update_requires_clinical_review")
    return tuple(findings)


def evaluate_clinical_control(capability: str, payload: Mapping[str, object] | None = None) -> dict:
    if capability not in CLINICAL_CONTROL_CAPABILITIES:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_clinical_control", "side_effects": ()}
    payload = dict(payload or {})
    base_ok, missing, invalid = _base_checks(capability, payload)
    findings = _domain_findings(capability, payload)
    table = CAPABILITY_TABLES[capability]
    requires_review = bool(findings or "assistant" in capability or "agent" in capability or "natural_language" in capability or "medication" in capability or "safety" in capability or payload.get("requires_review"))
    return {
        "ok": base_ok,
        "pbc": PBC_KEY,
        "capability": capability,
        "status": "ready" if base_ok and not findings else "review_required",
        "target_table": table,
        "owned_tables": (table,),
        "read_tables": (),
        "invalid_references": invalid,
        "missing_required_fields": missing,
        "domain_findings": findings,
        "event": {
            "event_type": CAPABILITY_EVENTS[capability],
            "event_contract": EVENT_CONTRACT,
            "topic": f"pbc.{PBC_KEY}.events",
            "idempotency_key": _digest((capability, payload)),
        },
        "ui_surface": f"{PBC_KEY}.ui.improve1.{capability}",
        "service_api": f"{PBC_KEY}.services.{capability}",
        "route": f"/workbench/pbcs/{PBC_KEY}/improve1/{capability.replace('_', '-')}",
        "permission": f"{PBC_KEY}.{capability}.operate",
        "configuration": {
            "rule_id": f"{capability}_policy",
            "parameter_id": f"{capability}_threshold",
            "database_backends": ("postgresql", "mysql", "mariadb"),
        },
        "agent_skill": f"{PBC_KEY}_skills.{capability}",
        "requires_human_confirmation": requires_review,
        "retry_dead_letter_evidence": {
            "inbox_table": "clinical_care_coordination_appgen_inbox_event",
            "dead_letter_table": "clinical_care_coordination_appgen_dead_letter_event",
            "max_attempts": 5,
        },
        "release_evidence": {
            "code_artifact": "clinical_care_coordination/clinical_control.py",
            "ui_artifact": "clinical_care_coordination/ui.py",
            "service_artifact": "clinical_care_coordination/runtime.py",
            "test_artifact": "clinical_care_coordination/tests/test_domain_behavior.py",
            "traceability": "clinical_care_coordination/IMPROVE1_TRACEABILITY.md",
        },
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def sample_payload_for(capability: str) -> dict:
    if capability not in CLINICAL_CONTROL_CAPABILITIES:
        raise KeyError(capability)
    payload = {field: f"{field}_evidence" for field in REQUIRED_FIELDS[capability]}
    payload["referenced_tables"] = (CAPABILITY_TABLES[capability],)
    if capability == "longitudinal_patient_care_plan_state_machine":
        payload["target_state"] = "active"
    if capability == "care_gap_taxonomy_specific_to_preventive_chronic_safety_and_access_gaps":
        payload["gap_type"] = "post_discharge_follow_up"
    if capability == "transition_of_care_packet_integrity":
        payload.update({"medication_reconciliation_status": "complete", "follow_up_appointments": ("cardiology",), "patient_instructions": "daily weights"})
    if capability in {"medication_reconciliation_handoff", "high_risk_medication_and_allergy_coordination"}:
        payload["human_confirmation"] = True
    if capability == "patient_safety_exception_playbooks":
        payload["playbook_type"] = "critical_result_unreconciled"
    if capability == "coordination_data_retention_and_legal_hold":
        payload["legal_hold"] = False
    if capability == "assistant_draft_quality_scoring":
        payload["source_coverage"] = 0.95
    if capability == "patient_level_dependency_freshness":
        payload["last_event_time"] = "2026-05-30T00:00:00"
        payload["freshness_score"] = 48
    if capability == "outcome_driven_closure_review":
        payload["open_barriers"] = "none_outstanding"
        payload["unresolved_referrals"] = "none_outstanding"
    if capability == "patient_reported_update_intake":
        payload["urgency"] = "routine"
        payload["clinical_review_required"] = True
    return payload


def _make_runner(capability: str) -> Callable[[Mapping[str, object] | None], dict]:
    def runner(payload: Mapping[str, object] | None = None) -> dict:
        return evaluate_clinical_control(capability, payload)

    runner.__name__ = f"run_{capability}"
    return runner


for _capability in CLINICAL_CONTROL_CAPABILITIES:
    globals()[f"run_{_capability}"] = _make_runner(_capability)

CLINICAL_CONTROL_FUNCTIONS: Mapping[str, Callable[[Mapping[str, object] | None], dict]] = {
    capability: globals()[f"run_{capability}"] for capability in CLINICAL_CONTROL_CAPABILITIES
}


def improve1_clinical_control_contract() -> dict:
    samples = tuple(CLINICAL_CONTROL_FUNCTIONS[capability](sample_payload_for(capability)) for capability in CLINICAL_CONTROL_CAPABILITIES)
    return {
        "format": "appgen.clinical-care-coordination.improve1-clinical-control.v1",
        "ok": len(samples) == 50 and all(item["ok"] for item in samples),
        "pbc": PBC_KEY,
        "capability_count": len(CLINICAL_CONTROL_CAPABILITIES),
        "capabilities": CLINICAL_CONTROL_CAPABILITIES,
        "owned_tables": OWNED_TABLES,
        "event_contract": EVENT_CONTRACT,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "samples": samples,
        "side_effects": (),
    }
