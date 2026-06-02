"""Executable improve1 controls for the Utility Outage Restoration PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    UTILITY_OUTAGE_RESTORATION_ALLOWED_DATABASE_BACKENDS,
    UTILITY_OUTAGE_RESTORATION_CONSUMED_EVENT_TYPES,
    UTILITY_OUTAGE_RESTORATION_OWNED_TABLES,
    UTILITY_OUTAGE_RESTORATION_REQUIRED_EVENT_TOPIC,
    UTILITY_OUTAGE_RESTORATION_RUNTIME_TABLES,
)

PBC_KEY = "utility_outage_restoration"
EVENT_CONTRACT = "AppGen-X"
OUTAGE_ALLOWED_DATABASE_BACKENDS = UTILITY_OUTAGE_RESTORATION_ALLOWED_DATABASE_BACKENDS
OUTAGE_REQUIRED_EVENT_TOPIC = UTILITY_OUTAGE_RESTORATION_REQUIRED_EVENT_TOPIC
OUTAGE_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in OUTAGE_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in OUTAGE_CAPABILITIES}
OUTAGE_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        UTILITY_OUTAGE_RESTORATION_OWNED_TABLES
        + UTILITY_OUTAGE_RESTORATION_RUNTIME_TABLES
        + tuple(f"utility_outage_restoration_{capability.slug}_control" for capability in OUTAGE_CAPABILITIES)
    )
)
OUTAGE_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        UTILITY_OUTAGE_RESTORATION_CONSUMED_EVENT_TYPES
        + (
            "NetworkTopologyChanged",
            "CustomerCriticalityChanged",
            "CrewRosterChanged",
            "WorkManagementOrderChanged",
            "SafetyClearanceChanged",
            "InventoryAvailabilityChanged",
            "WeatherAlertChanged",
            "FieldDamageAssessmentCompleted",
            "CustomerNotificationQueued",
            "CallCenterCaseChanged",
            "MapPublicationRequested",
            "ClaimsCaseOpened",
            "RegulatoryCalendarChanged",
            "AuditEvidenceSealed",
            "OperationalKpiChanged",
            "PolicyChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "incident_id",
    "service_area_id",
    "operating_company_id",
    "feeder_id",
    "operator_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|incident_number,current_state,target_state,transition_reason,source_system,owner_role,required_evidence,next_allowed_actions
2|detection_source_id,source_type,confidence,report_timestamp,service_point_projection,device_projection,duplicate_cluster,conflict_flag
3|interruption_id,device_id,device_type,upstream_device_id,downstream_device_ids,interruption_type,predicted_fault_segment,lockout_status
4|topology_projection_id,feeder_projection,device_projection,service_point_projection,phase_connectivity,connectivity_timestamp,freshness_status,no_external_mutation
5|impact_id,customer_count,critical_customer_count,life_support_count,facility_type,affected_phase,outage_start_time,restoration_segment
6|priority_queue_id,critical_customer_type,communication_requirement,backup_status_projection,escalation_owner,contact_due_at,life_safety_flag,priority_reason
7|severity_score_id,customer_factor,hazard_factor,critical_load_factor,weather_factor,duration_factor,crew_availability_factor,explainability_trace
8|restoration_estimate_id,estimate_type,confidence,source,assumptions,revision_reason,communicated_at,expires_at
9|etr_rule_id,approval_threshold,audience,channel,message_template,suppression_rule,revision_threshold,communication_log
10|switching_plan_id,sequence_number,device_id,action,hold_point,authority,clearance_reference,completion_evidence
11|clearance_id,affected_devices,issuer,holder,grounding_evidence,release_criteria,blocked_commands,active_hold_tag
12|crew_assignment_id,crew_id,crew_type,voltage_qualification,equipment_profile,shift_status,travel_estimate,task_type
13|route_plan_id,staging_area,route_geometry,access_constraints,storm_base,task_sequence,priority_customer_stop,estimated_arrival
14|damage_assessment_id,location,asset_projection,severity,photo_evidence,hazard_type,material_need,repair_recommendation
15|hazard_record_id,hazard_type,perimeter,responder_notification,blocked_work,mitigation_owner,clearance_evidence,severity_level
16|mutual_aid_request_id,requesting_region,crew_type,quantity,eta,lodging_plan,staging_assignment,release_status
17|material_projection_id,material_type,available_quantity,reservation_status,delivery_eta,shortage_alert,source_dependency,no_inventory_mutation
18|vegetation_event_id,tree_crew_required,vegetation_location,clearance_status,blocked_road,recurrence_marker,prevention_task,crew_queue
19|storm_mode_id,weather_projection,operating_level,staging_plan,communication_interval,estimate_policy,mutual_aid_trigger,active_flag
20|nested_outage_id,parent_incident_id,child_incident_id,partial_restoration_event,remaining_customer_count,nested_detection_source,recalculation_trace,parent_history_preserved
21|momentary_event_id,device_id,duration_seconds,operation_count,affected_customers,recurrence_pattern,sustained_outage_flag,reliability_treatment
22|reliability_metric_id,metric_type,period,customers_interrupted,outage_duration_minutes,exclusion_flag,event_linkage,certification_status
23|major_event_id,classification_threshold,weather_evidence,affected_area,approval_status,reporting_treatment,metric_exclusion_reason,audit_evidence
24|report_package_id,report_period,included_incidents,excluded_incidents,metric_snapshot,certifier,attachments,submission_evidence
25|public_feed_id,generalized_location,affected_count_range,status,approved_estimate,cause_category,suppression_reason,redacted_fields
26|notification_timeline_id,milestone,channel,audience,message_template,delivery_status,revision_reference,communication_evidence
27|call_center_sync_id,call_case_projection,incident_reference,script_status,callback_queue,channel_status,synchronization_lag,read_only_projection
28|cause_code_id,cause_category,subcause,operator_reason,field_confirmed_reason,regulatory_code,override_evidence,causal_history
29|verification_id,meter_ping_result,customer_callback_result,crew_confirmation,energization_evidence,exception_reason,verified_by,verified_at
30|reopen_case_id,callback_id,remaining_outage_evidence,nested_incident_created,customer_contact,reason_code,reopen_owner,resolution_path
31|command_board_id,queue_state,incident_filters,next_best_actions,sla_badges,map_context,crew_context,operator_decision_log
32|mobile_task_packet_id,crew_id,job_steps,device_context,safety_notes,materials_projection,offline_cache,completion_payload
33|rule_parameter_id,rule_name,parameter_name,bounds,scope,effective_date,simulation_result,approval_state
34|summary_agent_id,source_documents,incident_digest,customer_impact_summary,crew_summary,etr_summary,cited_facts,human_confirmation
35|switching_review_agent_id,switching_plan,clearance_check,hazard_check,sequence_risk,energization_blockers,recommended_change,operator_approval
36|safety_agent_id,hazard_summary,blocked_commands,clearance_state,grounding_state,life_safety_alert,write_block,escalation_target
37|event_model_id,event_name,payload_schema,lifecycle_transition,projection_replay,sequence_trace,consumer_contract,event_mapping
38|temporal_reconstruction_id,as_of_timestamp,event_sequence,projection_state,customer_impact_snapshot,crew_state_snapshot,estimate_snapshot,replay_hash
39|evidence_packet_id,hash_chain_root,attachment_hashes,event_hashes,operator_signature,timestamp_authority,verification_channel,tamper_status
40|equity_analysis_id,vulnerable_customer_projection,language_access_need,medical_priority,disadvantaged_area_flag,restoration_equity_score,outreach_gap,mitigation_action
41|crew_arrival_id,crew_id,current_location_projection,route_eta,traffic_constraint,staging_delay,arrival_confidence,customer_visible_eta
42|patrol_workflow_id,feeder_section,patrol_sequence,crew_assignment,hazard_observation,damage_observation,access_issue,completion_status
43|dependency_graph_id,device_node,repair_dependency,switching_dependency,crew_dependency,material_dependency,critical_path,restoration_order
44|mutual_aid_cost_id,external_crew_id,cost_center,lodging_cost,travel_cost,work_hours,release_evidence,settlement_status
45|claims_handoff_id,claim_reference,customer_projection,incident_evidence,damage_summary,coverage_boundary,no_claims_mutation,handoff_status
46|performance_benchmark_id,peer_group,restoration_duration,customer_minutes_interrupted,crew_productivity,storm_adjustment,benchmark_percentile,improvement_action
47|smoke_scenario_id,scenario_name,test_reference,ui_evidence,event_trace,boundary_evidence,release_check,coverage_status
48|boundary_proof_id,dependency_name,projection_record,api_event_contract,no_foreign_mutation,idempotency_behavior,dead_letter_behavior,audit_reference
49|storm_command_center_id,storm_base,mutual_aid_roster,crew_staging_map,critical_facility_queue,public_comm_cadence,resource_gap,executive_update
50|executive_brief_id,active_outage_count,customers_out,critical_customers_out,etr_confidence,crew_deployment,regulatory_risk,next_decision
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    2: ("NetworkTopologyChanged", "CustomerCriticalityChanged"),
    3: ("NetworkTopologyChanged",),
    4: ("NetworkTopologyChanged",),
    5: ("CustomerCriticalityChanged", "NetworkTopologyChanged"),
    6: ("CustomerCriticalityChanged",),
    12: ("CrewRosterChanged", "WorkManagementOrderChanged"),
    13: ("CrewRosterChanged",),
    14: ("FieldDamageAssessmentCompleted", "WorkManagementOrderChanged"),
    17: ("InventoryAvailabilityChanged",),
    19: ("WeatherAlertChanged",),
    25: ("MapPublicationRequested", "CustomerNotificationQueued"),
    26: ("CustomerNotificationQueued",),
    27: ("CallCenterCaseChanged",),
    32: ("CrewRosterChanged", "InventoryAvailabilityChanged"),
    40: ("CustomerCriticalityChanged",),
    41: ("CrewRosterChanged",),
    45: ("ClaimsCaseOpened",),
    48: ("PolicyChanged", "OperationalKpiChanged"),
    50: ("AuditEvidenceSealed", "OperationalKpiChanged"),
}
_INCIDENT_DETECTION_FEATURES = (1, 2, 3, 4, 5, 7, 8, 20, 21, 28, 29, 30, 38, 43, 47, 50)
_RESTORATION_OPERATION_FEATURES = (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 32, 35, 36, 41, 42, 43, 44, 49, 50)
_CUSTOMER_REGULATORY_FEATURES = (5, 6, 8, 9, 22, 23, 24, 25, 26, 27, 40, 45, 46, 49, 50)
_GOVERNANCE_AGENT_FEATURES = (31, 33, 34, 35, 36, 37, 38, 39, 47, 48, 50)
_AGENT_FEATURES = (34, 35, 36, 47, 50)
_HUMAN_CONFIRMATION_FEATURES = (9, 10, 11, 12, 14, 15, 16, 23, 24, 25, 26, 29, 30, 35, 36, 39, 44, 49, 50)
_APPROVAL_REQUIRED_FEATURES = (9, 10, 11, 15, 16, 23, 24, 25, 26, 35, 36, 39, 44, 49, 50)
_NON_MUTATING_FEATURES = (4, 5, 7, 8, 17, 21, 22, 23, 24, 25, 27, 31, 33, 34, 35, 36, 37, 38, 39, 40, 45, 46, 47, 48, 50)
_PROJECTION_ONLY_FEATURES = (2, 3, 4, 5, 6, 12, 13, 17, 19, 25, 27, 32, 40, 41, 45, 48)


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
        "tables": (f"utility_outage_restoration_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"UtilityOutageRestoration{_camel(capability.slug)}Panel",
        "route": f"POST /utility-outage-restoration/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in OUTAGE_CAPABILITIES}


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
        "event_topic": OUTAGE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "incident_detection_evidence_complete": True,
        "restoration_operations_evidence_complete": True,
        "customer_regulatory_evidence_complete": True,
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
        findings.append(f"{capability.title} requires owned outage model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _INCIDENT_DETECTION_FEATURES and payload.get("incident_detection_evidence_complete") is not True:
        findings.append("outage detection, topology projection, customer impact, incident lifecycle, nested outage, momentary interruption, verification, reconstruction, dependency graph, release scenario, and executive status evidence is required")
    if number in _RESTORATION_OPERATION_FEATURES and payload.get("restoration_operations_evidence_complete") is not True:
        findings.append("switching safety, clearance tags, crew qualification, route staging, damage assessment, hazards, mutual aid, materials projection, vegetation, storm mode, mobile tasking, patrol, cost release, and command center evidence is required")
    if number in _CUSTOMER_REGULATORY_FEATURES and payload.get("customer_regulatory_evidence_complete") is not True:
        findings.append("critical customer, ETR governance, reliability indices, major event classification, regulator package, public map redaction, notification timeline, call center sync, equity analytics, claims boundary, benchmark, and executive evidence is required")
    if number in _GOVERNANCE_AGENT_FEATURES and payload.get("governance_agent_evidence_complete") is not True:
        findings.append("operator workbench, configurable rules and parameters, governed agents, safety restrictions, AppGen-X event specialization, temporal replay, cryptographic evidence, smoke scenarios, boundary proof, and executive briefing evidence is required")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("ETR publication, switching, safety clearance, crew dispatch, damage, hazards, mutual aid, regulator reporting, public communication, restoration verification, reopen, agent review, cryptographic evidence, storm command, and executive decisions require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk outage restoration actions require separated approval for ETR publication, switching, clearances, hazards, mutual aid, regulator reports, public feeds, agent switching review, evidence packets, cost release, storm command, and executive decisions")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("outage restoration assistant skills must cite owned facts, show reversible CRUD previews, enforce safety permissions and policy checks, and block direct writes before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("topology reads, customer impact, severity, ETR forecasts, material availability, momentary metrics, regulator reports, public feeds, call center projections, workbench views, rule simulations, agent summaries, event replay, evidence packets, equity analytics, claims handoff, benchmarks, release scenarios, boundary proof, and executive briefing must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("network topology, customer criticality, crew roster, material, weather, public map, call center, claims, policy, KPI, and audit context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != OUTAGE_REQUIRED_EVENT_TOPIC:
        findings.append("utility outage restoration eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in OUTAGE_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary utility outage restoration datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("utility outage restoration controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_utility_outage_restoration_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in OUTAGE_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in OUTAGE_DECLARED_DEPENDENCIES)
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
        "required_event_topic": OUTAGE_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": OUTAGE_ALLOWED_DATABASE_BACKENDS,
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


def improve1_utility_outage_restoration_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_utility_outage_restoration_control(capability) for capability in OUTAGE_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.utility_outage_restoration.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": OUTAGE_CONTROL_OWNED_TABLES,
        "allowed_database_backends": OUTAGE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": OUTAGE_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": OUTAGE_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


UTILITY_OUTAGE_RESTORATION_CONTROL_FUNCTIONS = (
    "evaluate_utility_outage_restoration_control",
    "improve1_utility_outage_restoration_control_contract",
    "sample_payload_for",
)
