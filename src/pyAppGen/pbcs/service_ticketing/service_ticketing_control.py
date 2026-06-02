"""Executable improve1 controls for the Service Ticketing PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS,
    SERVICE_TICKETING_CONSUMED_EVENT_TYPES,
    SERVICE_TICKETING_OWNED_TABLES,
    SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
    SERVICE_TICKETING_RUNTIME_TABLES,
)

PBC_KEY = "service_ticketing"
EVENT_CONTRACT = "AppGen-X"
SERVICE_ALLOWED_DATABASE_BACKENDS = SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
SERVICE_REQUIRED_EVENT_TOPIC = SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
SERVICE_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in SERVICE_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in SERVICE_CAPABILITIES}
SERVICE_OWNED_TABLES = tuple(
    dict.fromkeys(
        SERVICE_TICKETING_OWNED_TABLES
        + SERVICE_TICKETING_RUNTIME_TABLES
        + tuple(f"service_ticketing_{capability.slug}_control" for capability in SERVICE_CAPABILITIES)
    )
)
SERVICE_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        SERVICE_TICKETING_CONSUMED_EVENT_TYPES
        + (
            "CustomerUpdated",
            "PreferenceChanged",
            "EntitlementUpdated",
            "KnowledgeSuggested",
            "CustomerHealthChanged",
            "FieldServiceHandoffAccepted",
            "FieldServiceOutcomeRecorded",
            "ProductTelemetryIncidentDetected",
            "MajorIncidentStatusChanged",
            "NotificationDeliveryFailed",
            "LegalHoldApplied",
            "DataSubjectRequestOpened",
            "SecurityIncidentLinked",
            "ProductFeedbackCreated",
            "QueueStaffingChanged",
            "AuditEventSealed",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "ticket_id",
    "customer_projection_id",
    "queue_id",
    "case_owner_id",
    "policy_version",
    "service_region",
    "evidence_references",
)
_FIELD_ROWS = """
1|intake_normalization_id,source_channel,source_proof,attachment_set,language_code,sentiment_signal,canonical_idempotency_key
2|readiness_gate_id,identity_confidence,required_field_status,entitlement_state,preferred_contact_channel,severity_evidence,triage_hold_reason
3|taxonomy_version_id,category_path,symptom_code,root_cause_candidate,component_link,severity_mapping,migration_guidance
4|duplicate_detection_id,semantic_similarity_score,external_reference_id,incident_signature,merge_decision,parent_child_link,no_match_rationale
5|lifecycle_state_id,current_state,requested_transition,required_evidence,owner_rule,sla_clock_effect,closure_criteria
6|priority_calibration_id,business_impact,urgency_factor,customer_tier_weight,regulatory_exposure,override_permission,change_reason
7|severity_priority_id,severity_level,priority_level,mapping_policy,customer_visible_language,pressure_only_block,analytics_bucket
8|sla_clock_id,clock_type,business_calendar,entitlement_basis,pause_reason,resume_reason,breach_evidence
9|breach_prediction_id,queue_load_signal,agent_skill_signal,case_age_signal,field_dependency_signal,breach_probability,recommended_action
10|queue_capacity_id,active_agent_capacity,skill_coverage,working_calendar,backlog_age_profile,inflow_forecast,overflow_route
11|assignment_score_id,skill_fit_score,availability_score,language_match,prior_owner_context,rejected_candidate_set,override_rationale
12|fairness_control_id,workload_balance,complexity_weight,after_hours_burden,escalation_share,reassignment_churn,manager_override_evidence
13|handoff_protocol_id,problem_statement,actions_taken,open_question_set,promised_update,SLA_state_snapshot,receiving_acknowledgement
14|escalation_policy_id,compiled_trigger,recipient_set,deadline,customer_update_requirement,deescalation_criteria,resolution_outcome
15|major_incident_link_id,parent_incident_id,impact_scope,bulk_update_batch,individual_sla_preserved,workaround_distribution,detach_reason
16|entitlement_handling_id,entitlement_snapshot_id,coverage_status,authorized_contact_set,supported_product_set,exclusion_reason,approval_requirement
17|preference_update_id,preference_snapshot_id,delivery_channel,language_preference,quiet_hour_window,opt_down_state,unsafe_communication_block
18|promise_tracker_id,promised_update_deadline,promise_owner,delivery_status,next_promised_update,overdue_flag,draft_update_reference
19|interaction_timeline_id,interaction_channel,visibility_flag,author_identity,extracted_action_item,customer_commitment,redaction_status
20|attachment_evidence_id,file_classification,scan_result,retention_policy,redaction_hint,chain_of_custody,relevance_tag
21|knowledge_feedback_id,article_reference,agent_acceptance,customer_visible_use,resolution_contribution,missing_knowledge_flag,article_defect_reason
22|resolution_standard_id,resolution_category,root_cause,fix_action,verification_evidence,customer_confirmation_need,reopen_risk
23|closure_reopen_id,closure_criteria_result,auto_close_timer,reopen_eligibility,reopen_reason,reopen_sla_policy,owner_assignment_rule
24|csat_targeting_id,closure_state,contact_preference,survey_fatigue,language_code,sensitive_issue_suppression,response_correlation
25|sentiment_urgency_id,model_version,sentiment_score,urgency_score,risk_marker_set,confidence,priority_override_policy
26|product_feedback_id,root_cause_candidate,component_attribution,recurrence_evidence,affected_customer_count,workaround_quality,linked_change_request
27|field_handoff_readiness_id,site_location,access_instruction,required_skill_set,tool_part_hint,safety_note,appointment_window
28|field_outcome_reconciliation_id,handoff_outcome_event,outcome_summary,followup_work_required,parts_consumed,sla_recalculation,customer_update_need
29|automation_evidence_id,model_rule_version,input_signal_set,recommendation,confidence,rejected_alternative_set,human_decision
30|reply_draft_id,source_citation_set,redaction_result,tone_control,entitlement_check,promised_update_detection,approval_workflow
31|agent_ticket_creation_id,document_digest,extracted_customer,extracted_product,severity_signal,duplicate_candidate_set,creation_plan
32|troubleshooting_plan_id,diagnostic_step_set,expected_observation,required_permission,customer_safe_question,field_trigger,stop_condition
33|case_summary_id,customer_visible_fact_set,internal_note_summary,open_action_set,blocker_set,sla_state,redaction_result
34|command_center_id,queue_filter,owner_filter,sla_risk_filter,age_filter,bulk_safe_action,export_evidence
35|coaching_insight_id,case_mix_normalization,sla_performance,first_contact_resolution,reopen_rate,sentiment_movement,knowledge_contribution
36|health_signal_handoff_id,issue_category,severity_signal,recurrence_signal,sentiment_signal,sla_outcome,resolution_confidence
37|analytics_forecast_id,forecast_dimension,volume_forecast,backlog_forecast,field_demand_forecast,confidence_interval,scenario_assumption
38|backlog_risk_score_id,customer_tier_factor,priority_factor,severity_factor,sla_clock_factor,duplicate_cluster_factor,score_explanation
39|compliance_legal_hold_id,legal_hold_flag,regulated_issue_flag,security_incident_flag,safety_issue_flag,retention_rule,access_restriction
40|redaction_workflow_id,sensitive_data_type,detection_confidence,redaction_suggestion,field_classification,redaction_audit,leak_prevention_result
41|audit_hash_chain_id,lifecycle_event_hash,assignment_hash,interaction_hash,customer_update_hash,resolution_hash,verifier_export
42|event_reliability_id,event_version,schema_hash,idempotency_key,ordering_assumption,retry_envelope,dead_letter_reason
43|boundary_proof_id,external_projection,api_dependency,consumed_event,cached_field,staleness_policy,foreign_table_scan_result
44|deflection_governance_id,deflection_eligibility,knowledge_confidence,escalation_bypass_rule,sentiment_check,failed_deflection_capture,sla_start_policy
45|proactive_case_id,source_event_evidence,notification_requirement,duplicate_detection_result,entitlement_check,owner_assignment,prevention_outcome
46|service_control_test_id,control_name,sample_case_set,sla_clock_result,assignment_policy_result,customer_update_result,remediation_task
47|resilience_drill_id,drill_type,recovery_time,data_loss_risk,workaround_plan,followup_control,replay_result
48|ui_surface_proof_id,capability_surface,form_reference,wizard_reference,control_reference,agent_tool_reference,coverage_result
49|readiness_score_id,schema_coverage_score,queue_configuration_score,sla_policy_score,event_health_score,agent_safety_score,blocking_gap_link
50|release_proof_id,intake_result,triage_result,assignment_result,field_handoff_result,resolution_csat_result,agent_safe_crud_plan
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("CustomerUpdated", "PreferenceChanged", "EntitlementUpdated"),
    16: ("EntitlementUpdated",),
    17: ("PreferenceChanged",),
    21: ("KnowledgeSuggested",),
    26: ("ProductFeedbackCreated",),
    27: ("EntitlementUpdated",),
    28: ("FieldServiceOutcomeRecorded",),
    36: ("CustomerHealthChanged",),
    39: ("LegalHoldApplied", "DataSubjectRequestOpened", "SecurityIncidentLinked"),
    41: ("AuditEventSealed",),
    42: ("CustomerUpdated", "PreferenceChanged", "EntitlementUpdated", "KnowledgeSuggested"),
    43: ("CustomerUpdated", "PreferenceChanged", "EntitlementUpdated", "KnowledgeSuggested", "FieldServiceHandoffAccepted"),
    45: ("ProductTelemetryIncidentDetected",),
    47: ("NotificationDeliveryFailed", "QueueStaffingChanged"),
}
_CUSTOMER_COMMUNICATION_FEATURES = (1, 17, 18, 19, 24, 30, 33, 36, 40, 44, 45, 50)
_SLA_OPERATION_FEATURES = (2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 27, 28, 34, 37, 38, 46, 47, 49, 50)
_AGENT_FEATURES = (2, 18, 25, 29, 30, 31, 32, 33, 37, 38, 44, 45, 49, 50)
_COMPLIANCE_FEATURES = (20, 22, 23, 39, 40, 41, 42, 43, 46, 47, 48, 49, 50)
_FIELD_SERVICE_FEATURES = (13, 27, 28, 47, 50)
_BOUNDARY_FEATURES = (1, 16, 17, 21, 26, 28, 36, 42, 43, 45, 50)
_HUMAN_CONFIRMATION_FEATURES = (2, 4, 6, 11, 13, 14, 22, 23, 27, 29, 30, 31, 32, 33, 39, 40, 44, 45, 47, 50)
_APPROVAL_REQUIRED_FEATURES = (6, 14, 15, 23, 27, 30, 31, 39, 40, 44, 45, 47, 50)
_NON_MUTATING_FEATURES = (1, 2, 4, 6, 9, 10, 11, 12, 14, 25, 29, 30, 31, 32, 33, 35, 37, 38, 41, 43, 44, 46, 47, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (1, 16, 17, 21, 26, 28, 36, 42, 43, 45)


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
        "tables": (f"service_ticketing_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"ServiceTicketing{_camel(capability.slug)}Panel",
        "route": f"POST /service-ticketing/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in SERVICE_CAPABILITIES}


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
        "event_topic": SERVICE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "customer_communication_evidence_complete": True,
        "sla_operation_evidence_complete": True,
        "compliance_evidence_complete": True,
        "field_service_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned service model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _CUSTOMER_COMMUNICATION_FEATURES and payload.get("customer_communication_evidence_complete") is not True:
        findings.append("intake, preferences, promises, timelines, CSAT, reply drafting, summaries, health handoffs, redaction, deflection, proactive cases, and release proof require customer communication evidence")
    if number in _SLA_OPERATION_FEATURES and payload.get("sla_operation_evidence_complete") is not True:
        findings.append("readiness, lifecycle, priority, severity, SLA clocks, breach prediction, queues, assignment, handoffs, escalation, incidents, field handoffs, command center, forecasting, backlog risk, controls, resilience, readiness, and release proof require SLA operation evidence")
    if number in _COMPLIANCE_FEATURES and payload.get("compliance_evidence_complete") is not True:
        findings.append("attachments, resolution, closure, legal hold, redaction, audit hash chain, event reliability, boundary proof, controls, resilience, UI proof, readiness, and release proof require compliance evidence")
    if number in _FIELD_SERVICE_FEATURES and payload.get("field_service_evidence_complete") is not True:
        findings.append("handoff protocol, field-service readiness, field outcome reconciliation, resilience drills, and release proof require field-service evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("service judgments, duplicate decisions, priority overrides, handoffs, escalations, resolution, closure, field handoffs, automation, agent replies, agent ticket creation, troubleshooting, summaries, compliance, redaction, deflection, proactive cases, resilience, and release proof require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk service actions require separated approval for priority overrides, escalation policy, major incidents, closure/reopen, field dispatch, agent replies, agent ticket creation, compliance/legal holds, redaction, deflection, proactive cases, resilience drills, and release proof")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("service assistant skills must cite ticket evidence, respect visibility and entitlement rules, prepare service commands only, and remain approval-gated before CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("normalization, readiness, duplicate analysis, priority scoring, breach prediction, capacity, assignment, fairness, escalation policy, NLP signals, automation, agent drafts, troubleshooting, summaries, analytics, risk scoring, audit proofs, boundary proofs, deflection, controls, drills, UI proof, readiness, and release proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("customer, preference, entitlement, knowledge, field-service, success, telemetry, legal, security, and audit context must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != SERVICE_REQUIRED_EVENT_TOPIC:
        findings.append("service ticketing eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in SERVICE_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary service ticketing datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("service ticketing controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_service_ticketing_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in SERVICE_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in SERVICE_DECLARED_DEPENDENCIES)
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
        "required_event_topic": SERVICE_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": SERVICE_ALLOWED_DATABASE_BACKENDS,
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


def improve1_service_ticketing_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_service_ticketing_control(capability) for capability in SERVICE_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.service-ticketing-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": SERVICE_OWNED_TABLES,
        "declared_dependencies": SERVICE_DECLARED_DEPENDENCIES,
        "allowed_database_backends": SERVICE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": SERVICE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


SERVICE_TICKETING_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_service_ticketing_control(slug, payload))
    for capability in SERVICE_CAPABILITIES
}
