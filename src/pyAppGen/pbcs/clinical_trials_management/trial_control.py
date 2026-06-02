"""Executable clinical trial controls for improve1 execution.

This module provides side-effect-free proof objects for every clinical trials
management improve1 capability. Each control binds domain evidence to an owned
trial table, AppGen-X event metadata, UI/service surfaces, agent skill exposure,
configuration handles, retry/dead-letter evidence, and release-audit artifacts.
"""

from __future__ import annotations

from datetime import date, datetime
import hashlib
import json
from typing import Callable, Mapping

PBC_KEY = "clinical_trials_management"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = (
    "clinical_trials_management_trial_protocol",
    "clinical_trials_management_study_site",
    "clinical_trials_management_subject",
    "clinical_trials_management_consent_record",
    "clinical_trials_management_visit_schedule",
    "clinical_trials_management_adverse_event",
    "clinical_trials_management_monitoring_finding",
    "clinical_trials_management_clinical_trials_management_policy_rule",
    "clinical_trials_management_clinical_trials_management_runtime_parameter",
    "clinical_trials_management_clinical_trials_management_schema_extension",
    "clinical_trials_management_clinical_trials_management_control_assertion",
    "clinical_trials_management_clinical_trials_management_governed_model",
    "clinical_trials_management_appgen_outbox_event",
    "clinical_trials_management_appgen_inbox_event",
    "clinical_trials_management_appgen_dead_letter_event",
)
TRIAL_CONTROL_CAPABILITIES = (
    "protocol_version_governance",
    "eligibility_criteria_engine",
    "screening_and_enrollment_lifecycle",
    "informed_consent_version_control",
    "site_activation_checklist",
    "delegation_of_authority",
    "visit_schedule_windowing",
    "assessment_and_procedure_checklist",
    "randomization_and_blinding_controls",
    "investigational_product_accountability",
    "adverse_event_intake",
    "serious_event_reporting",
    "protocol_deviation_management",
    "monitoring_visit_planning",
    "source_data_verification_strategy",
    "data_query_lifecycle",
    "electronic_case_report_form_governance",
    "endpoint_and_outcome_traceability",
    "subject_retention_and_visit_adherence",
    "site_performance_scorecards",
    "recruitment_funnel_tracking",
    "diversity_and_representativeness_monitoring",
    "ethics_and_regulatory_approval_tracking",
    "training_compliance",
    "trial_supply_and_lab_kit_readiness",
    "sample_collection_dependency",
    "safety_signal_review",
    "risk_based_monitoring_model_governance",
    "trial_master_file_evidence",
    "audit_and_inspection_readiness",
    "data_lock_readiness",
    "consent_aware_data_use",
    "privacy_safe_subject_views",
    "trial_agent_evidence_summaries",
    "governed_agent_crud_commands",
    "protocol_amendment_impact_simulation",
    "cross_pbc_boundary_proofs",
    "trial_timeline_projection",
    "deviation_root_cause_analytics",
    "carbon_and_participant_burden_awareness",
    "multi_country_localization",
    "continuous_control_assertions",
    "dead_letter_and_retry_operations",
    "cryptographic_trial_evidence_proofs",
    "seeded_trial_scenario_library",
    "trial_operations_workbench",
    "subject_discontinuation_and_follow_up",
    "full_clinical_trial_release_simulation",
    "package_overlap_guardrails",
    "composition_dsl_and_unified_agent_exposure",
)
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "protocol_version_governance": ("protocol_version", "target_state", "amendment_rationale", "effective_date", "impact_scope"),
    "eligibility_criteria_engine": ("criteria_set", "source_evidence", "thresholds", "reviewer", "decision_trace"),
    "screening_and_enrollment_lifecycle": ("subject_state", "consent_status", "eligibility_status", "cohort", "audit_history"),
    "informed_consent_version_control": ("consent_version", "protocol_version", "language", "signer_role", "source_document_evidence"),
    "site_activation_checklist": ("activation_checklist", "ethics_approval", "contract_status", "training_completion", "activation_date"),
    "delegation_of_authority": ("staff_role", "task_scope", "training_status", "start_date", "revocation_state"),
    "visit_schedule_windowing": ("visit_type", "target_day", "allowed_window", "actual_day", "deviation_link"),
    "assessment_and_procedure_checklist": ("required_procedures", "completed_procedures", "performer", "source_evidence", "waiver_reason"),
    "randomization_and_blinding_controls": ("randomization_event", "arm_assignment", "stratification_factors", "blinded_role", "unblinding_reason"),
    "investigational_product_accountability": ("product_lot", "kit_id", "dispense_record", "return_record", "pharmacist_signoff"),
    "adverse_event_intake": ("event_term", "onset", "grade", "seriousness", "relatedness"),
    "serious_event_reporting": ("seriousness", "recipient", "initial_deadline", "submission_proof", "narrative"),
    "protocol_deviation_management": ("deviation_type", "severity", "impacted_subject", "root_cause", "corrective_action"),
    "monitoring_visit_planning": ("monitoring_type", "site_risk", "planned_date", "documents_reviewed", "finding_plan"),
    "source_data_verification_strategy": ("field", "criticality", "risk_tier", "verification_state", "approval_evidence"),
    "data_query_lifecycle": ("query_reason", "data_field", "assignee", "response_state", "lock_impact"),
    "electronic_case_report_form_governance": ("form_version", "field_definitions", "edit_checks", "activation_date", "migration_impact"),
    "endpoint_and_outcome_traceability": ("endpoint_definition", "source_visit", "derivation_rule", "adjudication_state", "lock_status"),
    "subject_retention_and_visit_adherence": ("retention_risk", "missed_contact_pattern", "outreach_task", "barrier_category", "contact_preference"),
    "site_performance_scorecards": ("activation_metric", "enrollment_pace", "query_aging", "deviation_rate", "freshness"),
    "recruitment_funnel_tracking": ("funnel_stage", "referral_source", "outreach_consent", "screen_fail_reason", "enrollment_forecast"),
    "diversity_and_representativeness_monitoring": ("demographic_projection", "target_cohort", "representation_gap", "site_contribution", "recruitment_action"),
    "ethics_and_regulatory_approval_tracking": ("approval_body", "submission_package", "approval_date", "expiry", "amendment_linkage"),
    "training_compliance": ("curriculum", "required_role", "completion", "expiry", "authorization_linkage"),
    "trial_supply_and_lab_kit_readiness": ("kit_inventory", "site_supply_level", "expiry", "shipment_status", "visit_readiness"),
    "sample_collection_dependency": ("sample_requirement", "collection_window", "processing_requirement", "shipment_tracking", "receipt_status"),
    "safety_signal_review": ("signal_candidate", "frequency", "seriousness_mix", "committee_status", "action_recommendation"),
    "risk_based_monitoring_model_governance": ("model_version", "features", "evaluation_evidence", "thresholds", "drift_check"),
    "trial_master_file_evidence": ("evidence_category", "required_artifacts", "missing_artifacts", "owner", "inspection_readiness_score"),
    "audit_and_inspection_readiness": ("inspection_scope", "evidence_room", "finding", "corrective_action", "closeout_proof"),
    "data_lock_readiness": ("lock_checklist", "blocking_issue", "owner", "waiver", "approval"),
    "consent_aware_data_use": ("consent_scope", "data_use", "withdrawal_restrictions", "optional_sample", "future_research_use"),
    "privacy_safe_subject_views": ("viewer_role", "identifier_redaction", "clinical_redaction", "safety_redaction", "dashboard_scope"),
    "trial_agent_evidence_summaries": ("summary_type", "citations", "source_records", "human_approval", "regulatory_text_flag"),
    "governed_agent_crud_commands": ("intent", "entity", "protocol_version", "source_evidence", "confirmation"),
    "protocol_amendment_impact_simulation": ("amendment", "affected_subjects", "affected_sites", "reconsent_needs", "training_impact"),
    "cross_pbc_boundary_proofs": ("external_system", "dependency_contract", "projection_mode", "event_mode", "foreign_table_check"),
    "trial_timeline_projection": ("event_type", "actor", "source", "linked_entity", "protocol_version"),
    "deviation_root_cause_analytics": ("root_cause_category", "site_attribution", "training_gap", "process_gap", "effectiveness"),
    "carbon_and_participant_burden_awareness": ("travel_burden", "remote_visit_eligibility", "travel_support", "shipment_consolidation", "safety_override"),
    "multi_country_localization": ("jurisdiction", "consent_rule", "safety_reporting_rule", "privacy_rule", "policy_version"),
    "continuous_control_assertions": ("threshold", "population", "failing_records", "owner", "remediation"),
    "dead_letter_and_retry_operations": ("dead_letter_reason", "risk", "retry_count", "idempotency_key", "replay_checkpoint"),
    "cryptographic_trial_evidence_proofs": ("consent_hash", "eligibility_hash", "randomization_hash", "visit_hash", "data_lock_hash"),
    "seeded_trial_scenario_library": ("protocol_seed", "site_activation_seed", "subject_enrollment_seed", "serious_event_seed", "data_lock_seed"),
    "trial_operations_workbench": ("protocol_queue", "site_activation_queue", "screening_queue", "safety_queue", "lock_blocker_queue"),
    "subject_discontinuation_and_follow_up": ("discontinuation_reason", "treatment_status", "follow_up_requirement", "safety_contact_plan", "data_use_consent"),
    "full_clinical_trial_release_simulation": ("protocol_activation", "site_open", "subject_consent", "adverse_event", "lock_readiness"),
    "package_overlap_guardrails": ("ehr_dependency", "lab_dependency", "device_dependency", "finance_dependency", "submission_dependency"),
    "composition_dsl_and_unified_agent_exposure": ("models", "routes", "services", "event_contracts", "assistant_skills"),
}
CAPABILITY_TABLES = {
    "protocol_version_governance": OWNED_TABLES[0],
    "eligibility_criteria_engine": OWNED_TABLES[2],
    "screening_and_enrollment_lifecycle": OWNED_TABLES[2],
    "informed_consent_version_control": OWNED_TABLES[3],
    "site_activation_checklist": OWNED_TABLES[1],
    "delegation_of_authority": OWNED_TABLES[1],
    "visit_schedule_windowing": OWNED_TABLES[4],
    "assessment_and_procedure_checklist": OWNED_TABLES[4],
    "randomization_and_blinding_controls": OWNED_TABLES[2],
    "investigational_product_accountability": OWNED_TABLES[10],
    "adverse_event_intake": OWNED_TABLES[5],
    "serious_event_reporting": OWNED_TABLES[5],
    "protocol_deviation_management": OWNED_TABLES[10],
    "monitoring_visit_planning": OWNED_TABLES[6],
    "source_data_verification_strategy": OWNED_TABLES[6],
    "data_query_lifecycle": OWNED_TABLES[10],
    "electronic_case_report_form_governance": OWNED_TABLES[9],
    "endpoint_and_outcome_traceability": OWNED_TABLES[10],
    "subject_retention_and_visit_adherence": OWNED_TABLES[2],
    "site_performance_scorecards": OWNED_TABLES[1],
    "recruitment_funnel_tracking": OWNED_TABLES[2],
    "diversity_and_representativeness_monitoring": OWNED_TABLES[10],
    "ethics_and_regulatory_approval_tracking": OWNED_TABLES[1],
    "training_compliance": OWNED_TABLES[1],
    "trial_supply_and_lab_kit_readiness": OWNED_TABLES[10],
    "sample_collection_dependency": OWNED_TABLES[4],
    "safety_signal_review": OWNED_TABLES[5],
    "risk_based_monitoring_model_governance": OWNED_TABLES[11],
    "trial_master_file_evidence": OWNED_TABLES[10],
    "audit_and_inspection_readiness": OWNED_TABLES[10],
    "data_lock_readiness": OWNED_TABLES[10],
    "consent_aware_data_use": OWNED_TABLES[3],
    "privacy_safe_subject_views": OWNED_TABLES[10],
    "trial_agent_evidence_summaries": OWNED_TABLES[11],
    "governed_agent_crud_commands": OWNED_TABLES[11],
    "protocol_amendment_impact_simulation": OWNED_TABLES[0],
    "cross_pbc_boundary_proofs": OWNED_TABLES[10],
    "trial_timeline_projection": OWNED_TABLES[12],
    "deviation_root_cause_analytics": OWNED_TABLES[10],
    "carbon_and_participant_burden_awareness": OWNED_TABLES[10],
    "multi_country_localization": OWNED_TABLES[7],
    "continuous_control_assertions": OWNED_TABLES[10],
    "dead_letter_and_retry_operations": OWNED_TABLES[14],
    "cryptographic_trial_evidence_proofs": OWNED_TABLES[10],
    "seeded_trial_scenario_library": OWNED_TABLES[10],
    "trial_operations_workbench": OWNED_TABLES[10],
    "subject_discontinuation_and_follow_up": OWNED_TABLES[2],
    "full_clinical_trial_release_simulation": OWNED_TABLES[10],
    "package_overlap_guardrails": OWNED_TABLES[10],
    "composition_dsl_and_unified_agent_exposure": OWNED_TABLES[11],
}
CAPABILITY_EVENTS = {
    capability: "ClinicalTrials" + "".join(part.capitalize() for part in capability.split("_"))
    for capability in TRIAL_CONTROL_CAPABILITIES
}
ALLOWED_PROTOCOL_STATES = {"draft", "approved", "active", "amended", "superseded", "paused", "closed", "archived"}
ALLOWED_SUBJECT_STATES = {"prescreening", "consented", "screening", "randomized", "treatment", "follow_up", "withdrawn", "completed", "screen_failed"}
ALLOWED_VISIT_WINDOWS = {"on_window", "early", "late", "missed", "skipped", "rescheduled"}
AUTHORIZED_TASK_ROLES = {"investigator", "coordinator", "pharmacist", "lab_staff", "monitor", "data_manager"}
DECLARED_DEPENDENCY_MODES = {"api", "event", "projection", "package_metadata"}


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
    if capability == "protocol_version_governance" and payload.get("target_state") not in ALLOWED_PROTOCOL_STATES:
        findings.append("invalid_protocol_version_state")
    if capability == "eligibility_criteria_engine" and payload.get("conflicting_evidence") is True:
        findings.append("eligibility_conflict_requires_review")
    if capability == "screening_and_enrollment_lifecycle":
        if payload.get("subject_state") not in ALLOWED_SUBJECT_STATES:
            findings.append("invalid_subject_state")
        if payload.get("subject_state") in {"randomized", "treatment"} and (payload.get("consent_status") != "valid" or payload.get("eligibility_status") != "eligible"):
            findings.append("enrollment_blocked_without_valid_consent_and_eligibility")
    if capability == "informed_consent_version_control":
        if payload.get("consent_status") in {"missing", "expired", "withdrawn"}:
            findings.append("consent_not_active")
        if payload.get("protocol_version") != payload.get("consent_protocol_version", payload.get("protocol_version")):
            findings.append("consent_protocol_version_mismatch")
    if capability == "site_activation_checklist" and payload.get("checklist_complete") is False:
        findings.append("site_activation_blocked_by_missing_checklist")
    if capability == "delegation_of_authority" and payload.get("staff_role") not in AUTHORIZED_TASK_ROLES:
        findings.append("unauthorized_trial_task_role")
    if capability == "visit_schedule_windowing" and payload.get("window_classification") not in (None, *ALLOWED_VISIT_WINDOWS):
        findings.append("invalid_visit_window_classification")
    if capability == "assessment_and_procedure_checklist" and payload.get("required_open"):
        findings.append("visit_closure_blocked_by_required_procedure")
    if capability == "randomization_and_blinding_controls" and payload.get("blinded_role") is True and payload.get("arm_assignment_visible") is True:
        findings.append("blinding_violation")
    if capability == "investigational_product_accountability" and payload.get("reconciliation_variance"):
        findings.append("investigational_product_variance_unresolved")
    if capability == "serious_event_reporting" and payload.get("seriousness") == "serious":
        age = _age_hours(payload.get("initial_deadline"))
        if age is not None and not payload.get("submission_proof"):
            findings.append("serious_event_reporting_overdue")
    if capability == "data_query_lifecycle" and payload.get("response_state") == "open" and payload.get("lock_impact") == "blocks_lock":
        findings.append("data_lock_blocked_by_open_query")
    if capability == "data_lock_readiness" and payload.get("blocking_issue") not in {"none", "waived"}:
        findings.append("data_lock_blocked")
    if capability == "consent_aware_data_use" and payload.get("data_use") not in str(payload.get("consent_scope")):
        findings.append("data_use_outside_consent_scope")
    if capability == "privacy_safe_subject_views" and payload.get("viewer_role") == "sponsor" and payload.get("identifier_redaction") is False:
        findings.append("sponsor_view_requires_identifier_redaction")
    if capability == "trial_agent_evidence_summaries" and (not payload.get("citations") or payload.get("human_approval") is not True):
        findings.append("agent_summary_requires_citations_and_human_approval")
    if capability == "governed_agent_crud_commands" and payload.get("confirmation") is not True:
        findings.append("agent_crud_requires_confirmation")
    if capability == "risk_based_monitoring_model_governance":
        if payload.get("evaluation_evidence") == "missing" or payload.get("drift_check") == "stale":
            findings.append("monitoring_model_governance_not_current")
    if capability == "cross_pbc_boundary_proofs":
        if payload.get("dependency_contract") not in DECLARED_DEPENDENCY_MODES:
            findings.append("undeclared_dependency_contract")
        if payload.get("foreign_table_check") == "foreign_table_access":
            findings.append("foreign_table_access_blocked")
    if capability == "package_overlap_guardrails" and any(str(payload.get(key, "")).endswith("_table") for key in REQUIRED_FIELDS[capability]):
        findings.append("overlap_guardrail_blocks_foreign_ownership")
    return tuple(findings)


def evaluate_trial_control(capability: str, payload: Mapping[str, object] | None = None) -> dict:
    if capability not in TRIAL_CONTROL_CAPABILITIES:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_trial_control", "side_effects": ()}
    payload = dict(payload or {})
    base_ok, missing, invalid = _base_checks(capability, payload)
    findings = _domain_findings(capability, payload)
    table = CAPABILITY_TABLES[capability]
    requires_review = bool(
        findings
        or "agent" in capability
        or "safety" in capability
        or "serious_event" in capability
        or "unblinding" in str(payload)
        or payload.get("requires_review")
    )
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
            "inbox_table": "clinical_trials_management_appgen_inbox_event",
            "dead_letter_table": "clinical_trials_management_appgen_dead_letter_event",
            "max_attempts": 5,
        },
        "release_evidence": {
            "code_artifact": "clinical_trials_management/trial_control.py",
            "ui_artifact": "clinical_trials_management/ui.py",
            "service_artifact": "clinical_trials_management/runtime.py",
            "test_artifact": "clinical_trials_management/tests/test_domain_behavior.py",
            "traceability": "clinical_trials_management/IMPROVE1_TRACEABILITY.md",
        },
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def sample_payload_for(capability: str) -> dict:
    if capability not in TRIAL_CONTROL_CAPABILITIES:
        raise KeyError(capability)
    payload = {field: f"{field}_evidence" for field in REQUIRED_FIELDS[capability]}
    payload["referenced_tables"] = (CAPABILITY_TABLES[capability],)
    if capability == "protocol_version_governance":
        payload["target_state"] = "active"
    if capability == "screening_and_enrollment_lifecycle":
        payload.update({"subject_state": "randomized", "consent_status": "valid", "eligibility_status": "eligible"})
    if capability == "informed_consent_version_control":
        payload.update({"consent_status": "active", "protocol_version": "v2", "consent_protocol_version": "v2"})
    if capability == "site_activation_checklist":
        payload["checklist_complete"] = True
    if capability == "delegation_of_authority":
        payload["staff_role"] = "coordinator"
    if capability == "visit_schedule_windowing":
        payload["window_classification"] = "on_window"
    if capability == "assessment_and_procedure_checklist":
        payload["required_open"] = False
    if capability == "randomization_and_blinding_controls":
        payload.update({"blinded_role": True, "arm_assignment_visible": False})
    if capability == "investigational_product_accountability":
        payload["reconciliation_variance"] = False
    if capability == "serious_event_reporting":
        payload.update({"seriousness": "serious", "initial_deadline": "2026-05-30T00:00:00", "submission_proof": "submitted"})
    if capability == "data_query_lifecycle":
        payload.update({"response_state": "resolved", "lock_impact": "none"})
    if capability == "data_lock_readiness":
        payload["blocking_issue"] = "none"
    if capability == "consent_aware_data_use":
        payload.update({"consent_scope": "main_study optional_sample future_research_use", "data_use": "main_study"})
    if capability == "privacy_safe_subject_views":
        payload.update({"viewer_role": "sponsor", "identifier_redaction": True})
    if capability == "trial_agent_evidence_summaries":
        payload.update({"citations": ("source-1",), "human_approval": True})
    if capability == "governed_agent_crud_commands":
        payload["confirmation"] = True
    if capability == "risk_based_monitoring_model_governance":
        payload.update({"evaluation_evidence": "approved", "drift_check": "current"})
    if capability == "cross_pbc_boundary_proofs":
        payload.update({"dependency_contract": "event", "foreign_table_check": "declared_projection"})
    return payload


def _make_runner(capability: str) -> Callable[[Mapping[str, object] | None], dict]:
    def runner(payload: Mapping[str, object] | None = None) -> dict:
        return evaluate_trial_control(capability, payload)

    runner.__name__ = f"run_{capability}"
    return runner


for _capability in TRIAL_CONTROL_CAPABILITIES:
    globals()[f"run_{_capability}"] = _make_runner(_capability)

TRIAL_CONTROL_FUNCTIONS: Mapping[str, Callable[[Mapping[str, object] | None], dict]] = {
    capability: globals()[f"run_{capability}"] for capability in TRIAL_CONTROL_CAPABILITIES
}


def improve1_trial_control_contract() -> dict:
    samples = tuple(TRIAL_CONTROL_FUNCTIONS[capability](sample_payload_for(capability)) for capability in TRIAL_CONTROL_CAPABILITIES)
    return {
        "format": "appgen.clinical-trials-management.improve1-trial-control.v1",
        "ok": len(samples) == 50 and all(item["ok"] for item in samples),
        "pbc": PBC_KEY,
        "capability_count": len(TRIAL_CONTROL_CAPABILITIES),
        "capabilities": TRIAL_CONTROL_CAPABILITIES,
        "owned_tables": OWNED_TABLES,
        "event_contract": EVENT_CONTRACT,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "samples": samples,
        "side_effects": (),
    }
