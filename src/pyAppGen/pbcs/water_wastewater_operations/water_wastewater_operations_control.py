"""Executable improve1 controls for the Water Wastewater Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    WATER_WASTEWATER_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    WATER_WASTEWATER_OPERATIONS_CONSUMED_EVENT_TYPES,
    WATER_WASTEWATER_OPERATIONS_OWNED_TABLES,
    WATER_WASTEWATER_OPERATIONS_REQUIRED_EVENT_TOPIC,
    WATER_WASTEWATER_OPERATIONS_RUNTIME_TABLES,
)

PBC_KEY = "water_wastewater_operations"
EVENT_CONTRACT = "AppGen-X"
WATER_ALLOWED_DATABASE_BACKENDS = WATER_WASTEWATER_OPERATIONS_ALLOWED_DATABASE_BACKENDS
WATER_REQUIRED_EVENT_TOPIC = WATER_WASTEWATER_OPERATIONS_REQUIRED_EVENT_TOPIC
WATER_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in WATER_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in WATER_CAPABILITIES}
WATER_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(WATER_WASTEWATER_OPERATIONS_OWNED_TABLES + WATER_WASTEWATER_OPERATIONS_RUNTIME_TABLES + tuple(f"water_wastewater_operations_{capability.slug}_control" for capability in WATER_CAPABILITIES)))
WATER_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(WATER_WASTEWATER_OPERATIONS_CONSUMED_EVENT_TYPES + ("GisNetworkChanged", "ScadaTelemetryChanged", "LimsResultFinalized", "WorkOrderCompleted", "AssetMaintenanceChanged", "CustomerNotificationQueued", "PermitPolicyChanged", "EnergyKpiChanged", "WeatherEmergencyDeclared", "PublicHealthAdvisoryChanged", "AuditEvidenceSealed", "OperationalKpiChanged", "PolicyChanged")))
_BASE_FIELDS = ("tenant_id", "facility_id", "process_area_id", "permit_id", "service_area_id", "operator_id", "policy_version", "evidence_references")
_FIELD_ROWS = """
1|operating_state_id,current_state,target_state,process_mode,operator_shift,permit_context,allowed_commands,state_evidence
2|process_train_id,treatment_stage,unit_process,capacity,online_status,bypass_status,maintenance_window,configuration_version
3|source_tracking_id,source_type,intake_location,influent_flow,raw_quality_snapshot,weather_context,projection_freshness,boundary_evidence
4|sample_chain_id,sample_id,collector,custody_steps,preservation_method,lab_handoff_time,chain_status,tamper_evidence
5|sampling_plan_id,sample_point,frequency,compliance_category,scheduled_time,collector_assignment,missed_sample_rule,calendar_exception
6|sample_distinction_id,sample_id,compliance_flag,operational_flag,permit_citation,reporting_treatment,substitution_rule,audit_reason
7|permit_limit_id,parameter,limit_value,limit_period,facility_scope,effective_date,excursion_rule,approval_state
8|violation_case_id,exceedance_type,measured_value,limit_value,notification_deadline,corrective_action,regulator_notice,closure_evidence
9|residual_management_id,chlorine_residual,target_range,contact_time,boosting_action,low_residual_zone,operator_response,public_health_flag
10|advisory_id,advisory_type,affected_area,health_basis,approval_state,public_message,customer_notification,effective_window
11|interruption_id,interruption_type,affected_customers,start_time,estimated_restoration,crew_assignment,pressure_impact,status
12|pressure_zone_id,zone,pressure_reading,critical_customer_count,hydraulic_boundary,impact_score,projection_timestamp,mitigation_action
13|pump_asset_id,pump_id,station,operating_hours,condition_status,maintenance_due,criticality,asset_projection
14|lift_station_id,station_id,wet_well_level,pump_status,alarm_state,overflow_risk,telemetry_timestamp,response_action
15|overflow_event_id,overflow_type,location,estimated_volume,receiving_water,notification_required,cleanup_action,regulatory_case
16|field_work_order_id,work_type,crew_id,asset_projection,priority,safety_notes,completion_payload,no_work_order_mutation
17|valve_operation_id,valve_id,isolation_zone,operation_type,turn_count,operator,restoration_condition,evidence_photo
18|hydrant_activity_id,hydrant_id,inspection_result,flush_volume,residual_result,flow_result,defect_found,follow_up_action
19|main_break_id,main_segment,break_type,shutdown_area,repair_material,water_quality_hold,restoration_evidence,customer_notice
20|backup_case_id,blockage_location,customer_impact,cleanup_status,cause_category,crew_action,claim_boundary,closure_reason
21|inspection_boundary_id,cctv_event,asset_segment,defect_grade,media_reference,work_recommendation,no_inspection_mutation,boundary_evidence
22|chemical_dosing_id,chemical,feed_rate,target_residual,calibration_status,operator_adjustment,safety_limit,evidence_trace
23|biosolids_batch_id,sludge_source,stabilization_method,volume,disposal_destination,permit_check,hauler_reference,chain_of_custody
24|industrial_discharge_id,discharger_projection,permit_condition,sample_result,exceedance_flag,enforcement_boundary,pretreatment_action,monitoring_status
25|storm_response_id,storm_event,inflow_signal,bypass_risk,crew_staging,facility_mode,public_update,recovery_status
26|tank_operation_id,tank_id,level,turnover_rate,inspection_status,mixing_status,security_status,operating_action
27|water_loss_signal_id,dma_zone,flow_balance,leak_suspect,non_revenue_estimate,meter_anomaly,priority_score,investigation_action
28|efficiency_metric_id,process_unit,energy_usage,flow_treated,kwh_per_volume,chemical_efficiency,benchmark,optimization_action
29|report_package_id,report_period,permit_scope,included_samples,violations,certifier,attachments,submission_evidence
30|operator_log_id,shift_id,log_entry,equipment_status,process_adjustment,abnormal_condition,review_status,audit_hash
31|telemetry_boundary_id,scada_point,alarm_type,current_value,alarm_state,source_timestamp,no_scada_mutation,boundary_evidence
32|plant_command_board_id,process_status_cards,alarm_queue,compliance_queue,incident_queue,maintenance_queue,kpi_cards,operator_actions
33|mobile_packet_id,crew_id,work_order,asset_context,safety_notes,materials_needed,offline_cache,completion_payload
34|rule_parameter_id,rule_name,parameter_name,bounds,scope,effective_date,simulation_result,approval_state
35|sample_agent_id,sample_result,permit_context,trend_context,recommended_interpretation,cited_limits,human_confirmation,write_block
36|incident_narration_agent_id,incident_facts,operator_log,public_message_draft,regulator_summary,cited_events,human_confirmation,write_block
37|safety_agent_id,safety_summary,blocked_commands,confined_space_flag,chemical_hazard,public_health_risk,escalation_target,write_block
38|event_model_id,event_name,payload_schema,lifecycle_transition,projection_replay,sequence_trace,consumer_contract,event_mapping
39|compliance_reconstruction_id,as_of_timestamp,event_sequence,sample_state,permit_state,incident_state,report_snapshot,replay_hash
40|evidence_packet_id,hash_chain_root,sample_hashes,log_hashes,telemetry_hashes,operator_signature,verification_channel,tamper_status
41|criticality_score_id,asset_id,failure_probability,consequence_score,redundancy,critical_customer_impact,resilience_score,mitigation_plan
42|pm_coordination_id,asset_projection,maintenance_plan,work_order_projection,service_risk,compliance_risk,scheduled_window,boundary_evidence
43|notification_timeline_id,notice_type,audience,channel,message,approval_state,delivery_status,revision_reference
44|lab_reconciliation_id,lab_result_id,field_sample_id,chain_status,parameter_match,unit_check,exception_reason,reconciled_status
45|environmental_impact_id,receiving_water,load_estimate,overflow_volume,chemical_usage,emission_factor,impact_score,mitigation_action
46|emergency_mode_id,emergency_type,activation_reason,incident_commander,resource_plan,public_health_action,mutual_aid_status,deactivation_criteria
47|smoke_scenario_id,scenario_name,test_reference,ui_evidence,event_trace,boundary_evidence,release_check,coverage_status
48|boundary_proof_id,dependency_name,projection_record,api_event_contract,no_foreign_mutation,idempotency_behavior,dead_letter_behavior,audit_reference
49|daily_briefing_id,operator_id,plant_risks,water_quality_risks,field_risks,regulatory_deadlines,resource_gaps,next_decision
50|command_center_id,plant_status,active_incidents,compliance_risk,water_quality_status,field_crew_status,emergency_mode,executive_status
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {3:("GisNetworkChanged","ScadaTelemetryChanged"), 4:("LimsResultFinalized",), 10:("PublicHealthAdvisoryChanged","CustomerNotificationQueued"), 13:("AssetMaintenanceChanged",), 16:("WorkOrderCompleted",), 21:("WorkOrderCompleted",), 24:("PermitPolicyChanged",), 28:("EnergyKpiChanged",), 31:("ScadaTelemetryChanged",), 42:("AssetMaintenanceChanged","WorkOrderCompleted"), 43:("CustomerNotificationQueued",), 44:("LimsResultFinalized",), 46:("WeatherEmergencyDeclared",), 48:("PolicyChanged","OperationalKpiChanged"), 50:("AuditEvidenceSealed","OperationalKpiChanged")}
_PLANT_PROCESS_FEATURES=(1,2,3,9,13,14,22,23,24,26,28,30,31,32,50)
_COMPLIANCE_QUALITY_FEATURES=(4,5,6,7,8,10,15,24,29,35,39,40,43,44,45,47,50)
_FIELD_INCIDENT_FEATURES=(11,12,16,17,18,19,20,21,25,33,37,41,42,46,49,50)
_GOVERNANCE_AGENT_FEATURES=(34,35,36,37,38,39,40,47,48,49,50)
_AGENT_FEATURES=(35,36,37,49,50)
_HUMAN_CONFIRMATION_FEATURES=(8,10,11,15,17,19,20,22,24,29,35,36,37,40,43,46,49,50)
_APPROVAL_REQUIRED_FEATURES=(8,10,15,17,19,20,22,24,29,37,40,43,46,49,50)
_NON_MUTATING_FEATURES=(3,4,5,6,7,12,21,25,27,28,29,31,32,34,35,36,37,38,39,40,41,44,45,47,48,49,50)
_PROJECTION_ONLY_FEATURES=(3,13,14,16,21,24,27,28,31,42,43,44,48)

def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()

def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))

def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability): return capability
    if isinstance(capability, int): return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)

def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    return {"title": capability.title, "slug": capability.slug, "tables": (f"water_wastewater_operations_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number], "ui": f"WaterWastewaterOperations{_camel(capability.slug)}Panel", "route": f"POST /water-wastewater-operations/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}

CONTROL_SPECS={capability.feature_number: _spec_for(capability) for capability in WATER_CAPABILITIES}

def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved=_resolve(capability)
    if resolved is None: return {}
    spec=CONTROL_SPECS[resolved.feature_number]
    payload={field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]]=True
    payload.update({"database_backend":"postgresql","event_contract":EVENT_CONTRACT,"event_topic":WATER_REQUIRED_EVENT_TOPIC,"stream_engine_picker_visible":False,"shared_table_access":False,"dependency_access_mode":"api_event_projection","human_confirmation":True,"approver_separate_from_initiator":True,"agent_preview_only":True,"non_mutating_simulation":True,"plant_process_evidence_complete":True,"compliance_quality_evidence_complete":True,"field_incident_evidence_complete":True,"governance_agent_evidence_complete":True,"side_effects":()})
    return payload

def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings=[]; number=capability.feature_number; spec=CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_',' ')}")
        findings.append(f"{capability.title} requires owned water operations model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _PLANT_PROCESS_FEATURES and payload.get("plant_process_evidence_complete") is not True:
        findings.append("treatment plant state, process trains, source water, residual management, pump and lift station operations, chemical dosing, biosolids, industrial discharge, tanks, energy efficiency, operator logbook, telemetry boundary, plant command board, and command center evidence is required")
    if number in _COMPLIANCE_QUALITY_FEATURES and payload.get("compliance_quality_evidence_complete") is not True:
        findings.append("sample chain of custody, sampling plans, compliance distinctions, permit limits, exceedance workflows, public health advisories, overflow handling, regulatory reports, sample agents, compliance reconstruction, cryptographic packets, notifications, lab reconciliation, environmental impact, release scenarios, and command evidence is required")
    if number in _FIELD_INCIDENT_FEATURES and payload.get("field_incident_evidence_complete") is not True:
        findings.append("service interruption, pressure zones, work orders, valve isolation, hydrants, main breaks, backups, inspections, storm response, mobile crews, safety agents, criticality scoring, preventive maintenance, emergency mode, daily briefing, and command center evidence is required")
    if number in _GOVERNANCE_AGENT_FEATURES and payload.get("governance_agent_evidence_complete") is not True:
        findings.append("rules, parameters, governed sample and incident agents, safety restrictions, AppGen-X event specialization, point-in-time compliance replay, cryptographic evidence, release scenarios, boundary proof, daily briefing, and command center evidence is required")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("violations, advisories, interruptions, overflows, isolation, main breaks, backups, chemical dosing, industrial discharge, reports, agents, evidence packets, public notifications, emergency response, briefings, and command decisions require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk water operations require separated approval for violations, advisories, overflows, valve isolation, main breaks, backups, chemical dosing, industrial discharge, reports, safety agents, evidence packets, notifications, emergency mode, briefing, and command decisions")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("water operations assistant skills must cite owned facts, show reversible CRUD previews, enforce safety and public-health policy checks, and block direct writes before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("source projections, samples, plans, permit libraries, pressure analytics, CCTV boundaries, storm response, water loss, efficiency, reports, telemetry, workbench, rules, agents, events, replay, evidence packets, criticality, lab reconciliation, environmental analytics, release scenarios, boundaries, briefings, and command center must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("GIS network, SCADA, LIMS, work order, asset maintenance, customer notification, permit, energy KPI, emergency, policy, KPI, and audit context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != WATER_REQUIRED_EVENT_TOPIC: findings.append("water wastewater operations eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"): findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in WATER_ALLOWED_DATABASE_BACKENDS: findings.append("ordinary water wastewater operations datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"): findings.append("water wastewater operations controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))

def evaluate_water_wastewater_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved=_resolve(capability)
    if resolved is None: return {"ok":False,"reason":"unknown_capability","side_effects":()}
    spec=CONTROL_SPECS[resolved.feature_number]
    candidate=sample_payload_for(resolved); candidate.update(dict(payload or {}))
    missing_fields=tuple(field for field in spec["fields"] if candidate.get(field) in (None,"",(),[]))
    foreign_tables=tuple(table for table in spec["tables"] if table not in WATER_CONTROL_OWNED_TABLES)
    undeclared_dependencies=tuple(dependency for dependency in spec["dependencies"] if dependency not in WATER_DECLARED_DEPENDENCIES)
    findings=_domain_findings(resolved,candidate)
    evidence={"evidence_id":_digest((PBC_KEY,resolved.feature_number,tuple(sorted(candidate))))[:20],"owned_tables":spec["tables"],"required_fields":spec["fields"],"primary_proof":spec["primary_proof"],"ui_surface":spec["ui"],"service_api":spec["route"],"test":"tests/test_domain_behavior.py","event_contract":EVENT_CONTRACT,"required_event_topic":WATER_REQUIRED_EVENT_TOPIC,"allowed_database_backends":WATER_ALLOWED_DATABASE_BACKENDS,"declared_dependencies":spec["dependencies"],"configurable_rules_parameters":True,"agent_assisted":True,"side_effect_free":True}
    ok=not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok":ok,"pbc":PBC_KEY,"feature_number":resolved.feature_number,"title":resolved.title,"slug":resolved.slug,"missing_fields":missing_fields,"foreign_tables":foreign_tables,"undeclared_dependencies":undeclared_dependencies,"findings":findings,"evidence":evidence,"payload_digest":_digest(candidate)[:20],"side_effects":()}

def improve1_water_wastewater_operations_control_contract() -> dict[str, Any]:
    results=tuple(evaluate_water_wastewater_operations_control(capability) for capability in WATER_CAPABILITIES)
    blocking_gaps=tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {"format":"appgen.water_wastewater_operations.improve1-control-contract.v1","ok":len(results)==50 and all(item["ok"] for item in results),"pbc":PBC_KEY,"capability_count":len(results),"capabilities":results,"owned_tables":WATER_CONTROL_OWNED_TABLES,"allowed_database_backends":WATER_ALLOWED_DATABASE_BACKENDS,"event_contract":EVENT_CONTRACT,"required_event_topic":WATER_REQUIRED_EVENT_TOPIC,"declared_dependencies":WATER_DECLARED_DEPENDENCIES,"stream_engine_picker_visible":False,"blocking_gaps":blocking_gaps,"side_effects":()}

WATER_WASTEWATER_OPERATIONS_CONTROL_FUNCTIONS=("evaluate_water_wastewater_operations_control","improve1_water_wastewater_operations_control_contract","sample_payload_for")
