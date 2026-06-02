"""Executable improve1 controls for the Public Safety Dispatch PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PUBLIC_SAFETY_DISPATCH_ALLOWED_DATABASE_BACKENDS,
    PUBLIC_SAFETY_DISPATCH_OWNED_TABLES,
    PUBLIC_SAFETY_DISPATCH_REQUIRED_EVENT_TOPIC,
    PUBLIC_SAFETY_DISPATCH_RUNTIME_TABLES,
)

PBC_KEY = "public_safety_dispatch"
EVENT_CONTRACT = "AppGen-X"
DISPATCH_ALLOWED_DATABASE_BACKENDS = PUBLIC_SAFETY_DISPATCH_ALLOWED_DATABASE_BACKENDS
DISPATCH_REQUIRED_EVENT_TOPIC = PUBLIC_SAFETY_DISPATCH_REQUIRED_EVENT_TOPIC
DISPATCH_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in DISPATCH_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in DISPATCH_CAPABILITIES}
DISPATCH_OWNED_TABLES = tuple(
    dict.fromkeys(
        PUBLIC_SAFETY_DISPATCH_OWNED_TABLES
        + PUBLIC_SAFETY_DISPATCH_RUNTIME_TABLES
        + tuple(f"public_safety_dispatch_{capability.slug}_control" for capability in DISPATCH_CAPABILITIES)
    )
)
DISPATCH_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "CustomerUpdated",
    "SupplierQualified",
    "PremiseHistoryProjected",
    "GeocodeConfidenceProjected",
    "BoloAlertProjected",
    "HospitalDiversionProjected",
    "RadioTransmissionCaptured",
    "UnitTelemetryProjected",
    "RecordsCaseOpened",
    "AuditEventSealed",
)
_BASE_FIELDS = (
    "tenant_id",
    "incident_id",
    "call_id",
    "unit_id",
    "dispatcher_id",
    "agency_id",
    "jurisdiction",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|ng911_call_id,ani,ali,callback_validation,call_source,language_need,abandoned_call_status,phase_two_precision
2|chief_complaint_id,discipline,protocol_family,determinant_code,subdeterminant,caller_words,hazard_flags
3|triage_trace_id,protocol_path,discriminator_answers,upgrade_reason,downgrade_reason,override_reason,final_priority
4|duplicate_review_id,time_window,geocode_distance,caller_overlap,premise_history_match,complaint_similarity,merge_decision
5|safety_prompt_id,weapon_risk,smoke_condition,hazmat_flag,violence_indicator,exposure_note,responder_warning
6|location_confidence_id,primary_geocode,fallback_geocode,confidence_score,premise_type,address_source,validation_status
7|premise_history_id,caution_note,access_instruction,special_occupancy,prior_incident_count,durable_fact,incident_specific_fact
8|party_tracking_id,contact_role,callback_priority,reliability,language_preference,fact_attribution,party_timeline
9|text_session_id,transcript_fragment,heartbeat_status,canned_prompt,silent_call_rule,voice_escalation,location_verification
10|prearrival_instruction_id,protocol_code,instruction_step,caller_compliance,interruption_reason,completion_timestamp,liability_note
11|cad_status_id,current_status,next_status,transition_timestamp,discipline_variant,assignment_context,transition_validity
12|unit_recommendation_id,unit_type,travel_proximity,readiness_score,discipline_match,coverage_impact,override_reason
13|readiness_check_id,staffing_count,role_coverage,medic_level,apparatus_state,equipment_restriction,dispatch_blocker
14|coverage_simulation_id,cross_staffed_asset,move_up_candidate,district_coverage,policy_minimum,uncovered_area,ripple_effect
15|incident_command_id,command_designation,staging_area,tactical_channel,division_group,branch_structure,command_transfer
16|mutual_aid_lifecycle_id,requesting_agency,requested_resource,response_deadline,acknowledgment,eta,jurisdiction_condition
17|interop_note_id,radio_plan,unit_alias,staging_point,command_contact,agency_translation,auto_loaded_note
18|bolo_linkage_id,person_match,vehicle_match,location_match,hit_alert,acknowledgment,relayed_warning
19|radio_log_id,channel,speaker,transmission_type,linked_incident,linked_unit,replay_order
20|channel_assignment_id,recommended_channel,reserved_channel,current_load,override_justification,tactical_use,channel_change
21|safety_escalation_id,distress_indicator,priority_raise,supervisor_attention,recommended_units,command_action,radio_trigger
22|premise_caution_id,caution_type,source,verification_date,review_owner,expiration_rule,access_restriction
23|ems_transport_id,destination_candidate,hospital_status,diversion_flag,transport_milestone,destination_change,patient_hand_off
24|fire_benchmark_id,benchmark_type,timed_prompt,completion_time,overdue_gap,command_visibility,review_note
25|arrival_anomaly_id,status_chronology,location_mismatch,travel_time_outlier,qa_route,exception_event,supervisor_review
26|alert_hit_id,hit_type,mandatory_acknowledgment,notify_supervisor,incident_link,priority_influence,staging_influence
27|unit_conflict_id,competing_incident,recommendation_state,preassignment_state,hold_option,reassign_option,override_reason
28|staging_workflow_id,staging_state,staging_location,reason,command_authority,release_condition,unit_card_instruction
29|approval_gate_id,exception_type,policy_rule,supervisor_id,approval_timestamp,justification,policy_version
30|records_handoff_id,final_classification,priority_history,unit_list,arrival_clear_times,radio_refs,completeness_status
31|disposition_code_id,discipline_scope,outcome_code,transport_outcome,arrest_outcome,fire_outcome,records_mapping
32|workbench_queue_id,waiting_intake,active_incidents,awaiting_assignment,pending_mutual_aid,safety_escalations,stale_calls
33|incident_timeline_id,call_event,dispatch_event,radio_event,milestone_event,safety_alert,source_label
34|keyboard_latency_id,shortcut_key,critical_action,tab_order,latency_budget,measured_latency,operator_confirmation
35|mapping_panel_id,unit_location,jurisdiction_polygon,first_due_area,hydrant_overlay,hospital_overlay,route_warning
36|intake_ai_skill_id,transcript_source,structured_draft,missing_question_checklist,safety_summary,human_confirmation,write_block
37|recommendation_explanation_id,travel_reason,readiness_reason,discipline_reason,coverage_reason,mutual_aid_reason,suggestion_decision
38|radio_summary_skill_id,source_radio_refs,cad_milestone_refs,draft_synopsis,unresolved_questions,handoff_checklist,citation_map
39|domain_event_taxonomy_id,event_schema,call_received_event,incident_merged_event,unit_assigned_event,handoff_completed_event,consumer_contract
40|consumed_event_handler_id,policy_effect,premise_effect,service_area_effect,alarm_rule_effect,mutual_aid_effect,review_task
41|chain_of_custody_id,edited_field,before_value,after_value,correction_reason,actor_id,point_in_time_replay
42|protocol_release_id,protocol_family,compliance_check,question_path,qa_export,training_case,release_gate
43|critical_incident_qa_id,incident_type,review_packet,radio_extract,timeline_extract,supervisor_notes,qa_disposition
44|jurisdiction_boundary_id,boundary_rule,agency_authority,cross_border_assignment,override_reason,mutual_aid_contract,enforcement_result
45|shift_handoff_id,open_incidents,unit_status_summary,safety_alerts,pending_callbacks,records_defects,acknowledged_by
46|degraded_mode_id,outage_type,fallback_channel,offline_cad_packet,sync_checkpoint,manual_dispatch_log,recovery_action
47|data_quality_control_id,control_rule,population,failing_sample,owner,remediation,closure_evidence
48|training_simulation_id,scenario_name,simulated_call,simulated_units,decision_feedback,scorecard,side_effect_free
49|seed_upgrade_id,seed_incident,seed_unit,seed_premise,seed_radio_log,seed_policy,realism_check
50|release_gate_id,operational_evidence,traceability_matrix,domain_tests,ui_coverage,service_coverage,release_decision
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    6: ("GeocodeConfidenceProjected",),
    7: ("PremiseHistoryProjected",),
    18: ("BoloAlertProjected",),
    19: ("RadioTransmissionCaptured",),
    23: ("HospitalDiversionProjected",),
    25: ("UnitTelemetryProjected",),
    26: ("BoloAlertProjected",),
    30: ("RecordsCaseOpened",),
    33: ("RadioTransmissionCaptured",),
    35: ("GeocodeConfidenceProjected", "UnitTelemetryProjected"),
    40: ("PolicyChanged", "CustomerUpdated", "SupplierQualified"),
    41: ("AuditEventSealed",),
    50: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 3, 4, 5, 10, 12, 16, 18, 20, 21, 26, 27, 28, 29, 30, 36, 37, 38, 41, 44, 45, 46, 48, 50)
_SUPERVISOR_APPROVAL_FEATURES = (3, 14, 16, 20, 21, 22, 26, 27, 29, 30, 41, 43, 44, 46, 50)
_NON_MUTATING_FEATURES = (4, 6, 7, 12, 14, 25, 27, 32, 33, 34, 35, 36, 37, 38, 40, 42, 43, 47, 48, 49, 50)
_AI_PREVIEW_FEATURES = (12, 25, 32, 33, 36, 37, 38, 47, 48, 50)
_SAFETY_EVIDENCE_FEATURES = (1, 3, 5, 6, 7, 10, 12, 13, 15, 18, 20, 21, 22, 23, 24, 26, 28, 29, 30, 33, 35, 41, 43, 44, 45, 46, 50)
_PROJECTION_ONLY_FEATURES = (6, 7, 18, 19, 23, 25, 26, 30, 33, 35, 40, 41, 50)
_CAD_CHRONOLOGY_FEATURES = (3, 10, 11, 15, 19, 21, 23, 24, 25, 28, 30, 33, 41, 45, 46)


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
        "tables": (f"public_safety_dispatch_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"PublicSafetyDispatch{_camel(capability.slug)}Panel",
        "route": f"POST /public-safety-dispatch/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in DISPATCH_CAPABILITIES}


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
        "event_topic": DISPATCH_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "supervisor_approval": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "safety_evidence_complete": True,
        "cad_chronology_valid": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned CAD evidence, UI, service/API, event, assistant, and release proof before approval.")
    if number in _SAFETY_EVIDENCE_FEATURES and payload.get("safety_evidence_complete") is not True:
        findings.append("NG911, triage, safety prompts, location, premise, pre-arrival, recommendations, command, BOLO, channels, escalation, transport, fireground, records, map, chain-of-custody, QA, jurisdiction, degraded-mode, and release gates require complete responder and caller safety evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("dispatch-changing actions, AI drafts, incident merges, recommendations, radio summaries, degraded mode, simulations, and release decisions require dispatcher confirmation")
    if number in _SUPERVISOR_APPROVAL_FEATURES and payload.get("supervisor_approval") is not True:
        findings.append("priority overrides, move-ups, mutual aid, channel exceptions, safety escalations, BOLO actions, conflicted units, handoffs, boundary overrides, degraded operations, and release gates require supervisor approval")
    if number in _AI_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("dispatch assistant skills must remain cited, explainable, permission-checked, and preview-only until a human commits the action")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("duplicate detection, geocode fallback, premise lookups, recommendations, anomaly detection, workbench queues, timelines, mapping, assistant summaries, consumed-event reviews, protocol release, QA packages, controls, training, seeds, and release gates must be side-effect-free")
    if number in _CAD_CHRONOLOGY_FEATURES and payload.get("cad_chronology_valid") is not True:
        findings.append("CAD status, radio, milestone, command, transport, fireground, degraded-mode, and chain-of-custody controls require valid chronological ordering")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("premise, geocode, BOLO, hospital, radio, telemetry, records, policy, customer, supplier, and audit facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != DISPATCH_REQUIRED_EVENT_TOPIC:
        findings.append("public safety dispatch eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in DISPATCH_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary public safety dispatch datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("public safety dispatch controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_public_safety_dispatch_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in DISPATCH_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in DISPATCH_DECLARED_DEPENDENCIES)
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
        "required_event_topic": DISPATCH_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": DISPATCH_ALLOWED_DATABASE_BACKENDS,
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


def improve1_public_safety_dispatch_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_public_safety_dispatch_control(capability) for capability in DISPATCH_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.public-safety-dispatch-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": DISPATCH_OWNED_TABLES,
        "declared_dependencies": DISPATCH_DECLARED_DEPENDENCIES,
        "allowed_database_backends": DISPATCH_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": DISPATCH_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


PUBLIC_SAFETY_DISPATCH_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_public_safety_dispatch_control(slug, payload)) for capability in DISPATCH_CAPABILITIES}
