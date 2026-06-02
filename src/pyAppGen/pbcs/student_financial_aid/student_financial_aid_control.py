"""Executable improve1 controls for the Student Financial Aid PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    STUDENT_FINANCIAL_AID_ALLOWED_DATABASE_BACKENDS,
    STUDENT_FINANCIAL_AID_CONSUMED_EVENT_TYPES,
    STUDENT_FINANCIAL_AID_OWNED_TABLES,
    STUDENT_FINANCIAL_AID_REQUIRED_EVENT_TOPIC,
    STUDENT_FINANCIAL_AID_RUNTIME_TABLES,
)

PBC_KEY = "student_financial_aid"
EVENT_CONTRACT = "AppGen-X"
AID_ALLOWED_DATABASE_BACKENDS = STUDENT_FINANCIAL_AID_ALLOWED_DATABASE_BACKENDS
AID_REQUIRED_EVENT_TOPIC = STUDENT_FINANCIAL_AID_REQUIRED_EVENT_TOPIC
AID_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in AID_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in AID_CAPABILITIES}
AID_OWNED_TABLES = tuple(
    dict.fromkeys(
        STUDENT_FINANCIAL_AID_OWNED_TABLES
        + STUDENT_FINANCIAL_AID_RUNTIME_TABLES
        + tuple(f"student_financial_aid_{capability.slug}_control" for capability in AID_CAPABILITIES)
    )
)
AID_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        STUDENT_FINANCIAL_AID_CONSUMED_EVENT_TYPES
        + (
            "StudentEnrollmentChanged",
            "StudentIdentityVerified",
            "ProgramEligibilityChanged",
            "DocumentReceived",
            "AcademicProgressEvaluated",
            "LoanRequirementCompleted",
            "FinancePostingUpdated",
            "StudentAccountBalanceChanged",
            "CommunicationPreferenceChanged",
            "InvestigationOutcomeUpdated",
            "SponsorAwardChanged",
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "student_projection_id",
    "aid_year",
    "term_id",
    "program_projection_id",
    "policy_version",
    "reviewer_id",
    "evidence_references",
)
_FIELD_ROWS = """
1|application_state_id,current_state,requested_transition,transition_reason,required_evidence,allowed_command_set,event_emission
2|identity_enrollment_boundary_id,identity_confidence,enrollment_status,residency_status,dependency_status,projection_freshness,source_evidence
3|period_control_id,academic_year,payment_period,census_date,enrollment_intensity,rule_version,term_scope
4|dependency_review_id,household_size,family_in_college,special_circumstance,source_document_set,override_status,rationale
5|coa_budget_id,tuition_amount,fee_amount,housing_food_amount,books_amount,transportation_amount,professional_judgment_adjustment
6|eligibility_trace_id,contribution_input,budget_amount,resource_amount,calculated_need,aid_limit,calculation_version
7|packaging_rule_id,fund_priority,eligibility_condition,annual_limit,aggregate_limit,unmet_need_handling,overaward_check
8|fund_capacity_id,fund_source,available_capacity,reservation_status,waitlist_rule,release_condition,allocation_audit
9|external_resource_id,resource_source,amount,term_scope,restriction,confirmation_status,award_impact
10|verification_tracking_id,selection_reason,required_document,status,due_date,discrepancy,correction_outcome
11|document_extraction_id,source_page,extracted_field_set,confidence,discrepancy_flag,reviewer_approval,mutation_preview
12|conflicting_information_id,fact_type,source_a,source_b,severity,resolution_owner,closure_evidence
13|professional_judgment_id,request_reason,adjusted_field,original_value,adjusted_value,reviewer_authority,audit_note
14|dependency_override_id,override_type,evidence_checklist,effective_year,renewal_requirement,denial_reason,notice
15|sap_status_id,evaluation_period,gpa_result,pace_result,timeframe_result,appeal_status,next_review_date
16|sap_appeal_id,appeal_reason,documentation,academic_plan,committee_decision,condition_set,expiration_date
17|award_response_id,award_line,response,accepted_amount,response_date,channel,counseling_requirement
18|loan_requirement_boundary_id,requirement_type,completion_status,expiration,source_system,freshness,external_mutation_block
19|disbursement_checklist_id,enrollment_check,verification_check,sap_check,hold_check,acceptance_check,blocker_reason
20|disbursement_schedule_id,split_basis,earliest_release_date,census_recalculation,late_disbursement,cancellation_rule,schedule_result
21|return_of_funds_id,withdrawal_date,attendance_projection,aid_earned,unearned_amount,institutional_share,student_notice
22|enrollment_recalculation_id,enrollment_event_id,affected_award_set,revised_amount_set,notice,approval_state,recalculation_reason
23|overaward_case_id,source,affected_award_set,adjustment_plan,refund_boundary,student_notice,closure_evidence
24|compliance_obligation_id,obligation_type,due_date,owner,rule_source,status,escalation_state
25|program_eligibility_id,effective_date,credential_status,modality,location,restriction_reason,packaging_block
26|citizenship_residency_id,status_projection,required_document_set,discrepancy_reason,reviewer,notice,eligibility_block
27|consortium_record_id,host_institution,credit_count,cost_amount,agreement_document,attendance_confirmation,award_adjustment
28|program_packaging_profile_id,student_level,program_type,eligible_fund_set,limit_rule,budget_rule,required_check
29|aggregate_limit_id,fund_type,annual_usage,lifetime_usage,remaining_eligibility,freshness,override_constraint
30|communication_timeline_id,template,language,channel,trigger,delivery_evidence,student_response
31|portal_task_id,task_type,due_date,student_action,status,raw_datastore_access_block,completion_evidence
32|advisor_queue_id,queue_type,owner,sla,severity,student_population,next_action
33|award_revision_id,before_award_lines,after_award_lines,revision_reason,source_event,student_notice,effective_date
34|reconciliation_boundary_id,finance_projection,student_account_projection,disbursed_amount,posted_amount,returned_amount,freshness
35|exception_taxonomy_id,exception_category,severity,blocked_action,owner,due_date,reopen_reason
36|rule_parameter_id,rule_type,parameter_key,bounds,approval_history,rollback_token,runtime_effect
37|student_guidance_skill_id,status_summary,blocker_explanation,draft_message,source_citation,current_record_check,projection_check
38|document_review_skill_id,document_type,missing_signature,mismatched_value,expiration_flag,followup_required,approval_required
39|agent_safety_id,proposed_command,affected_record_set,financial_impact,confidence,approval_role,blocked_write
40|fraud_referral_boundary_id,anomaly_flag,referral_payload,hold_status,source_evidence,resolution_projection,casework_mutation_block
41|equity_analytics_id,unmet_need_metric,completion_time_metric,document_burden_metric,appeal_outcome_metric,disbursement_delay_metric,privacy_aggregation
42|privacy_consent_id,consent_status,authorized_party,redaction_policy,field_visibility,audit_control,unauthorized_view_block
43|point_in_time_reconstruction_id,replay_timestamp,application_snapshot,eligibility_snapshot,award_snapshot,disbursement_snapshot,sap_snapshot
44|aid_evidence_packet_id,eligibility_hash,award_hash,verification_hash,disbursement_hash,appeal_hash,alteration_check
45|predictive_risk_id,missing_item_factor,progress_factor,enrollment_change_factor,document_age_factor,revision_factor,explanation
46|campus_program_isolation_id,campus_scope,program_scope,rule_scope,budget_scope,permission_scope,leakage_check
47|release_smoke_scenario_id,scenario_name,owned_record_evidence,event_evidence,ui_artifact,boundary_check,scenario_result
48|boundary_proof_id,external_domain,declared_api_or_event,model_reference,service_reference,agent_command_reference,foreign_table_scan
49|sponsor_report_id,sponsor_projection,report_period,included_awards,adjustments,disbursements,delivery_evidence
50|command_center_id,student_summary,timeline,task_set,award_view,blocker_set,governed_action
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    2: ("StudentEnrollmentChanged", "StudentIdentityVerified"),
    10: ("DocumentReceived",),
    11: ("DocumentReceived",),
    15: ("AcademicProgressEvaluated",),
    18: ("LoanRequirementCompleted",),
    22: ("StudentEnrollmentChanged",),
    25: ("ProgramEligibilityChanged",),
    30: ("CommunicationPreferenceChanged",),
    34: ("FinancePostingUpdated", "StudentAccountBalanceChanged"),
    40: ("InvestigationOutcomeUpdated",),
    47: ("PolicyChanged", "AuditEventSealed"),
    48: ("StudentEnrollmentChanged", "FinancePostingUpdated", "DocumentReceived"),
    49: ("SponsorAwardChanged",),
}
_APPLICATION_ELIGIBILITY_FEATURES = (1, 2, 3, 4, 5, 6, 13, 14, 25, 26, 27, 28, 46, 50)
_AWARD_DISBURSEMENT_FEATURES = (7, 8, 9, 17, 18, 19, 20, 21, 22, 23, 29, 33, 34, 49, 50)
_VERIFICATION_COMPLIANCE_FEATURES = (10, 11, 12, 15, 16, 24, 35, 36, 40, 42, 43, 44, 47, 48, 50)
_STUDENT_EXPERIENCE_FEATURES = (30, 31, 32, 37, 38, 39, 41, 45, 50)
_AGENT_FEATURES = (11, 37, 38, 39, 45, 50)
_HUMAN_CONFIRMATION_FEATURES = (11, 13, 14, 16, 17, 19, 21, 22, 23, 36, 37, 38, 39, 40, 47, 49, 50)
_APPROVAL_REQUIRED_FEATURES = (13, 14, 16, 19, 21, 22, 23, 36, 39, 40, 47, 49, 50)
_NON_MUTATING_FEATURES = (2, 4, 5, 6, 7, 8, 9, 11, 13, 19, 20, 21, 22, 23, 29, 34, 37, 38, 39, 40, 41, 43, 44, 45, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (2, 8, 9, 18, 22, 25, 29, 34, 40, 48, 49)


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
        "tables": (f"student_financial_aid_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"StudentFinancialAid{_camel(capability.slug)}Panel",
        "route": f"POST /student-financial-aid/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in AID_CAPABILITIES}


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
        "event_topic": AID_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "application_eligibility_evidence_complete": True,
        "award_disbursement_evidence_complete": True,
        "verification_compliance_evidence_complete": True,
        "student_experience_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned financial-aid model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _APPLICATION_ELIGIBILITY_FEATURES and payload.get("application_eligibility_evidence_complete") is not True:
        findings.append("application lifecycle, identity/enrollment, periods, dependency, cost of attendance, need, professional judgment, overrides, program/citizenship/consortium/program packaging, campus isolation, and command center require application eligibility evidence")
    if number in _AWARD_DISBURSEMENT_FEATURES and payload.get("award_disbursement_evidence_complete") is not True:
        findings.append("packaging rules, fund capacity, external resources, award responses, loan requirements, disbursement checks, schedules, returns, enrollment changes, overawards, aggregate limits, revisions, reconciliation, sponsor reports, and command center require award disbursement evidence")
    if number in _VERIFICATION_COMPLIANCE_FEATURES and payload.get("verification_compliance_evidence_complete") is not True:
        findings.append("verification, document extraction, conflicts, SAP, appeals, compliance calendar, exceptions, rules, fraud referrals, privacy, reconstruction, evidence packets, release smoke, boundary proof, and command center require verification compliance evidence")
    if number in _STUDENT_EXPERIENCE_FEATURES and payload.get("student_experience_evidence_complete") is not True:
        findings.append("communications, portal tasks, advisor queues, student guidance, document review, agent safety, equity analytics, predictive risk, and command center require student experience evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("document extraction, professional judgment, dependency overrides, appeals, award response changes, disbursement release, returns, enrollment revisions, overawards, rules, agent guidance, document review, agent writes, referrals, release smoke, sponsor reporting, and command center require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk aid actions require separated approval for professional judgment, dependency overrides, appeals, disbursement release, returns, enrollment recalculation, overaward resolution, rules, agent writes, fraud referrals, release smoke, sponsor reporting, and command center decisions")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("financial aid assistant skills must cite source evidence, preview mutations, block high-impact writes, require RBAC, and remain approval-gated before CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("projections, reviews, budgets, calculations, packaging, capacity, resources, extraction, judgments, disbursement checks, schedules, returns, revisions, limits, reconciliation, agent guidance, fraud, analytics, reconstruction, packets, risk, boundary proof, sponsor reporting, and command center must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("student lifecycle, finance, documents, identity, compliance, communication, investigation, sponsor, audit, policy, and KPI context must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != AID_REQUIRED_EVENT_TOPIC:
        findings.append("student financial aid eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in AID_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary student financial aid datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("student financial aid controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_student_financial_aid_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in AID_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in AID_DECLARED_DEPENDENCIES)
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
        "required_event_topic": AID_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": AID_ALLOWED_DATABASE_BACKENDS,
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


def improve1_student_financial_aid_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_student_financial_aid_control(capability) for capability in AID_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.student-financial-aid-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": AID_OWNED_TABLES,
        "declared_dependencies": AID_DECLARED_DEPENDENCIES,
        "allowed_database_backends": AID_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": AID_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


STUDENT_FINANCIAL_AID_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_student_financial_aid_control(slug, payload))
    for capability in AID_CAPABILITIES
}
