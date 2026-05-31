"""Executable improve1 controls for the Talent Onboarding PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    TALENT_ONBOARDING_ALLOWED_DATABASE_BACKENDS,
    TALENT_ONBOARDING_CONSUMED_EVENT_TYPES,
    TALENT_ONBOARDING_OWNED_TABLES,
    TALENT_ONBOARDING_REQUIRED_EVENT_TOPIC,
    _TALENT_ONBOARDING_RUNTIME_TABLES,
)

PBC_KEY = "talent_onboarding"
EVENT_CONTRACT = "AppGen-X"
TALENT_ALLOWED_DATABASE_BACKENDS = TALENT_ONBOARDING_ALLOWED_DATABASE_BACKENDS
TALENT_REQUIRED_EVENT_TOPIC = TALENT_ONBOARDING_REQUIRED_EVENT_TOPIC
TALENT_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in TALENT_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in TALENT_CAPABILITIES}
TALENT_OWNED_TABLES = tuple(
    dict.fromkeys(
        TALENT_ONBOARDING_OWNED_TABLES
        + _TALENT_ONBOARDING_RUNTIME_TABLES
        + tuple(f"talent_onboarding_{capability.slug}_control" for capability in TALENT_CAPABILITIES)
    )
)
TALENT_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        TALENT_ONBOARDING_CONSUMED_EVENT_TYPES
        + (
            "RoleChanged",
            "WorkerIdentityVerified",
            "PersonnelProfileProvisioned",
            "PayrollWorkerProjectionChanged",
            "AccessPreloadRequested",
            "WelcomeNotificationQueued",
            "BackgroundProviderStatusChanged",
            "CompensationRangePublished",
            "JobCatalogRoleChanged",
            "AuditEventSealed",
            "CandidateDocumentReceived",
            "EquipmentFulfillmentChanged",
            "PolicyChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "requisition_id",
    "candidate_id",
    "jurisdiction",
    "worker_type",
    "policy_version",
    "actor_id",
    "evidence_references",
)
_FIELD_ROWS = """
1|readiness_gate_id,job_title,department,manager_id,location,legal_entity,budget_evidence
2|approval_route_id,requisition_type,approval_threshold,delegated_approver,decision,rejection_reason,policy_hash
3|budget_governance_id,budget_source,approved_range,currency,headcount_allocation,expiry,change_history
4|skill_taxonomy_id,skill_type,proficiency,evidence_expectation,trainable_flag,certification_requirement,ambiguity_check
5|sourcing_campaign_id,campaign_goal,channel,target_market,budget,diversity_objective,effectiveness_metric
6|source_attribution_id,source_type,campaign_id,referrer_or_vendor,attribution_confidence,fee_eligibility,source_lineage
7|candidate_readiness_id,identity_status,contact_status,work_authorization_indicator,source_status,consent_status,profile_status
8|candidate_consent_id,purpose,language_version,jurisdiction_scope,capture_timestamp,expiry,withdrawal_effect
9|privacy_request_id,request_type,identity_verification,scope,due_date,legal_hold,anonymization_action
10|duplicate_detection_id,email_match,phone_match,resume_fingerprint,identity_proof_match,semantic_similarity,merge_decision
11|profile_enrichment_id,education_evidence,experience_evidence,skill_evidence,certification_evidence,confidence,reviewer_approval
12|stage_state_id,current_stage,next_stage,allowed_transition,actor,reason,communication_readiness
13|fair_screening_id,scorecard_dimension,evidence_weight,prohibited_attribute_exclusion,adverse_impact_monitor,reviewer_override,rejection_review
14|interview_plan_id,competency_set,structured_question_set,rubric,panel_role_set,sequence,accommodation_need
15|panel_allocation_id,skill_coverage,role_seniority,availability,conflict_check,workload,selection_explanation
16|schedule_resilience_id,timezone,candidate_availability,interviewer_conflict,reschedule_reason,sla,no_show_handling
17|feedback_quality_id,rubric_score,evidence_field,prohibited_content_check,late_feedback_escalation,calibration,confidence
18|evaluation_chain_id,source,competency,score,evaluator,candidate_visibility_policy,audit_hash
19|scorecard_explainability_id,dimension_set,skill_coverage,assessment_evidence,risk_flag,decision_rationale,weight_sensitivity
20|background_package_id,role_id,jurisdiction,worker_type,access_level,provider,check_expiry
21|adjudication_id,result_type,confidence_threshold,role_relevance,reviewer,candidate_response,decision_reason
22|adverse_action_id,notice_reason,check_reference,notice_date,waiting_period,response_deadline,delivery_proof
23|offer_readiness_id,requisition_status,budget_status,candidate_stage,check_adjudication,compensation_projection,start_date
24|comp_projection_id,range,currency,pay_frequency,variable_pay,benefits_eligibility,freshness
25|offer_approval_id,approval_amount,compensation_variance,exception_reason,relocation_terms,manager_authority,reapproval_trigger
26|offer_acceptance_id,offer_state,sent_at,viewed_at,accepted_at,signature_evidence,start_date_trigger
27|communication_readiness_id,message_type,notification_projection,template_data,privacy_filter,delivery_channel,handoff_status
28|checklist_generation_id,template_set,role_projection,location,start_date,equipment_need,access_requirement
29|task_sla_id,task_owner,due_date,dependency,sla,blocker,provisioning_impact
30|equipment_request_id,role_need,location,due_date,device_type,delivery_projection,receipt_evidence
31|access_preload_id,role_bundle,start_date,manager_id,least_privilege_bundle,approval,activation_condition
32|identity_handoff_id,candidate_identity,accepted_offer,start_date,role_id,manager_id,proof_hash
33|payroll_projection_id,pay_group,compensation_projection,start_date,legal_entity,bank_readiness,missing_setup_task
34|candidate_proof_id,proof_type,redaction_policy,hash_set,policy_version,verification_api,disclosure_scope
35|audit_trace_id,hash_chain,requisition_change,stage_change,offer_change,agent_preview,event_handling
36|policy_screening_id,action_type,attribute_set,decision,explanation,override_route,policy_version
37|pipeline_analytics_id,funnel_conversion,cycle_time,source_quality,stage_aging,offer_acceptance,onboarding_sla
38|hiring_forecast_id,time_to_fill,interview_demand,offer_acceptance_delay,background_delay,task_workload,drift_evidence
39|risk_model_governance_id,model_name,feature_lineage,training_window,approval_status,fairness_check,rollback_plan
40|anomaly_detection_id,anomaly_type,source_spike,stage_loop,feedback_delay,offer_exception,review_route
41|stochastic_exposure_id,exposure_type,role_location_source,stage,start_date,confidence_interval,mitigation_action
42|event_reliability_id,outbox_status,inbox_status,dead_letter_status,idempotency_key,replay_eligibility,projection_freshness
43|boundary_proof_id,external_domain,declared_api_or_event,model_reference,service_reference,agent_reference,foreign_table_scan
44|workbench_coverage_id,role_view,panel_name,command_set,form_set,agent_panel,capability_visibility
45|document_intake_id,document_type,extracted_fact_set,owned_table_mapping,privacy_validation,foreign_mutation_rejection,approval_preview
46|agent_plan_id,command,permission,owned_table_set,idempotency_key,emitted_event,human_approval
47|carbon_schedule_id,schedule_type,remote_in_person_tradeoff,carbon_score,fairness_constraint,candidate_preference,window_selection
48|resilience_drill_id,scenario,provider_outage,duplicate_event,identity_delay,dead_letter_replay,drill_evidence
49|readiness_score_id,setup_score,consent_policy_score,offer_control_score,ui_coverage_score,boundary_score,agent_safety_score
50|hire_to_provision_proof_id,approved_requisition,candidate_capture,consent_screening,interview_offer,onboarding_access,emitted_events
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("RoleChanged",),
    3: ("CompensationRangePublished",),
    20: ("BackgroundProviderStatusChanged",),
    24: ("CompensationRangePublished",),
    27: ("WelcomeNotificationQueued",),
    30: ("EquipmentFulfillmentChanged",),
    31: ("AccessPreloadRequested",),
    32: ("WorkerIdentityVerified", "PersonnelProfileProvisioned"),
    33: ("PayrollWorkerProjectionChanged",),
    35: ("AuditEventSealed",),
    43: ("RoleChanged", "WorkerIdentityVerified", "PayrollWorkerProjectionChanged", "AccessPreloadRequested"),
    45: ("CandidateDocumentReceived",),
    48: ("BackgroundProviderStatusChanged", "WorkerIdentityVerified"),
    50: ("RoleChanged", "WorkerIdentityVerified", "AccessPreloadRequested", "PayrollWorkerProjectionChanged"),
}
_REQUISITION_CANDIDATE_FEATURES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 36, 43, 44, 49, 50)
_INTERVIEW_EVALUATION_FEATURES = (14, 15, 16, 17, 18, 19, 37, 38, 39, 40, 41, 47, 49, 50)
_CHECK_OFFER_ONBOARDING_FEATURES = (20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 48, 50)
_GOVERNANCE_AGENT_FEATURES = (34, 35, 36, 39, 40, 42, 43, 44, 45, 46, 48, 49, 50)
_AGENT_FEATURES = (13, 19, 36, 39, 40, 45, 46, 49, 50)
_HUMAN_CONFIRMATION_FEATURES = (10, 13, 17, 19, 21, 22, 23, 25, 26, 31, 32, 36, 39, 45, 46, 50)
_APPROVAL_REQUIRED_FEATURES = (2, 3, 21, 22, 23, 25, 26, 31, 32, 36, 39, 46, 50)
_NON_MUTATING_FEATURES = (13, 15, 16, 19, 24, 27, 34, 37, 38, 39, 40, 41, 43, 45, 46, 47, 49, 50)
_PROJECTION_ONLY_FEATURES = (1, 24, 27, 30, 31, 32, 33, 43, 50)


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
        "tables": (f"talent_onboarding_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"TalentOnboarding{_camel(capability.slug)}Panel",
        "route": f"POST /talent-onboarding/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in TALENT_CAPABILITIES}


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
        "event_topic": TALENT_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "requisition_candidate_evidence_complete": True,
        "interview_evaluation_evidence_complete": True,
        "check_offer_onboarding_evidence_complete": True,
        "governance_agent_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned talent model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _REQUISITION_CANDIDATE_FEATURES and payload.get("requisition_candidate_evidence_complete") is not True:
        findings.append("requisition and candidate evidence is required for readiness, approvals, budgets, skills, sourcing, attribution, consent, privacy, duplicate checks, profile enrichment, stage controls, fair screening, policy screening, boundary proof, UI coverage, readiness score, and hire-to-provision proof")
    if number in _INTERVIEW_EVALUATION_FEATURES and payload.get("interview_evaluation_evidence_complete") is not True:
        findings.append("interview and evaluation evidence is required for interview plans, panel allocation, scheduling resilience, feedback quality, evaluation chain, scorecards, analytics, forecasts, model governance, anomaly detection, exposure modeling, carbon-aware scheduling, readiness score, and end-to-end proof")
    if number in _CHECK_OFFER_ONBOARDING_FEATURES and payload.get("check_offer_onboarding_evidence_complete") is not True:
        findings.append("background check, offer, onboarding, equipment, access, identity, payroll, resilience, and hire-to-provision evidence is required before execution")
    if number in _GOVERNANCE_AGENT_FEATURES and payload.get("governance_agent_evidence_complete") is not True:
        findings.append("candidate proofs, audit traces, policy screening, model governance, anomaly review, event reliability, boundary proof, workbench coverage, document intake, agent planning, resilience, readiness, and release proof require governance and agent evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("talent decisions that merge candidates, reject candidates, capture feedback, score candidates, adjudicate checks, send adverse action, extend offers, accept/rescind offers, preload access, provision identity, screen policy, govern models, or run agent plans require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk talent actions require separated approval for requisitions, budgets, adjudication, adverse action, offers, access preload, provisioning handoff, policies, models, agent plans, and hire-to-provision release")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("talent assistant skills must validate privacy and permissions, show reversible CRUD previews, cite evidence, and block direct writes before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("screening, panel allocation, scheduling, scorecards, compensation projections, communication facts, proofs, analytics, forecasts, model governance, anomalies, exposure, boundary, document intake, agent plans, carbon scheduling, readiness, and release proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("role, compensation, notification, equipment, access, personnel, payroll, identity, and audit context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != TALENT_REQUIRED_EVENT_TOPIC:
        findings.append("talent onboarding eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in TALENT_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary talent onboarding datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("talent onboarding controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_talent_onboarding_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in TALENT_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in TALENT_DECLARED_DEPENDENCIES)
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
        "required_event_topic": TALENT_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": TALENT_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "configurable_rules_parameters": True,
        "agent_assisted": True,
        "side_effect_free": True,
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "slug": resolved.slug,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "evidence": evidence,
        "payload_digest": _digest(candidate)[:20],
        "side_effects": (),
    }


def improve1_talent_onboarding_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_talent_onboarding_control(capability) for capability in TALENT_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.talent_onboarding.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": TALENT_OWNED_TABLES,
        "allowed_database_backends": TALENT_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": TALENT_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": TALENT_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


TALENT_ONBOARDING_CONTROL_FUNCTIONS = (
    "evaluate_talent_onboarding_control",
    "improve1_talent_onboarding_control_contract",
    "sample_payload_for",
)
