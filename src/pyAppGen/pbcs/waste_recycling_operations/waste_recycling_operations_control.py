"""Executable improve1 controls for the Waste Recycling Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    WASTE_RECYCLING_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    WASTE_RECYCLING_OPERATIONS_CONSUMED_EVENT_TYPES,
    WASTE_RECYCLING_OPERATIONS_OWNED_TABLES,
    WASTE_RECYCLING_OPERATIONS_REQUIRED_EVENT_TOPIC,
    WASTE_RECYCLING_OPERATIONS_RUNTIME_TABLES,
)

PBC_KEY = "waste_recycling_operations"
EVENT_CONTRACT = "AppGen-X"
WASTE_ALLOWED_DATABASE_BACKENDS = WASTE_RECYCLING_OPERATIONS_ALLOWED_DATABASE_BACKENDS
WASTE_REQUIRED_EVENT_TOPIC = WASTE_RECYCLING_OPERATIONS_REQUIRED_EVENT_TOPIC
WASTE_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in WASTE_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in WASTE_CAPABILITIES}
WASTE_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(WASTE_RECYCLING_OPERATIONS_OWNED_TABLES + WASTE_RECYCLING_OPERATIONS_RUNTIME_TABLES + tuple(f"waste_recycling_operations_{capability.slug}_control" for capability in WASTE_CAPABILITIES)))
WASTE_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(WASTE_RECYCLING_OPERATIONS_CONSUMED_EVENT_TYPES + (
    "FleetVehicleChanged", "CrewRosterChanged", "CustomerServiceRequestChanged", "BillingFeeAssessed",
    "FacilityScaleTicketRecorded", "CommoditySaleCreated", "PermitPolicyChanged", "ContractorRouteCompleted",
    "EnforcementCaseOpened", "AssetMaintenanceCompleted", "WeatherEmergencyDeclared", "AuditEvidenceSealed",
    "OperationalKpiChanged", "PolicyChanged",
)))
_BASE_FIELDS = ("tenant_id", "route_id", "service_area_id", "municipality_id", "material_stream_id", "operator_id", "policy_version", "evidence_references")
_FIELD_ROWS = """
1|route_lifecycle_id,current_state,target_state,service_day,route_type,allowed_commands,transition_reason,service_obligation
2|territory_calendar_id,territory_boundary,holiday_calendar,service_frequency,subscription_class,seasonal_rule,missed_service_cutoff,calendar_exception
3|stop_sequence_id,stop_id,sequence_number,geocode,turn_constraint,service_window,bin_set,optimization_reason
4|vehicle_crew_projection_id,vehicle_id,crew_id,license_class,capacity_projection,shift_status,safety_status,no_fleet_mutation
5|bin_asset_id,serial_number,container_type,capacity,lifecycle_state,assigned_location,rfid_tag,maintenance_status
6|bin_location_id,placement_quality,accessibility_flag,setout_distance,obstruction_status,geofence_confidence,photo_evidence,correction_action
7|pickup_event_id,stop_id,timestamp,gps_point,lift_sensor_evidence,photo_evidence,material_stream,service_result
8|missed_pickup_case_id,reported_by,root_cause,resolution_action,customer_notice,retry_route,fee_credit_boundary,closure_evidence
9|stream_taxonomy_id,stream_code,material_family,accepted_items,prohibited_items,contamination_threshold,facility_destination,education_message
10|contamination_case_id,finding_source,contaminant_type,severity,photo_evidence,notice_required,education_action,repeat_offender_flag
11|yield_record_id,route_id,inbound_weight,recyclable_weight,residue_weight,yield_percent,facility_ticket,trend_indicator
12|disposal_ticket_id,ticket_number,facility_id,gross_weight,tare_weight,net_weight,material_stream,reconciliation_status
13|facility_projection_id,facility_id,facility_type,acceptance_rules,capacity_status,permit_status,scale_status,no_facility_mutation
14|hazmat_exception_id,material_identified,containment_action,crew_safety_instruction,facility_rejection,regulatory_notice,disposal_path,incident_owner
15|bulky_item_request_id,item_type,appointment_window,crew_requirement,fee_boundary,customer_confirmation,capacity_slot,resolution_status
16|organics_quality_id,contamination_level,moisture_level,odor_issue,compost_destination,education_action,batch_quality,diversion_credit
17|commercial_container_service_id,customer_site,container_size,service_frequency,access_constraints,lock_code_policy,extra_pickup_rule,contract_reference
18|roll_off_job_id,job_site,container_type,delivery_window,haul_ticket,construction_debris_type,weight_limit,disposal_destination
19|illegal_dumping_case_id,location,reported_by,material_observed,evidence_photos,enforcement_boundary,cleanup_assignment,case_status
20|public_space_operation_id,operation_type,route_zone,public_bin_id,sweep_frequency,overflow_status,crew_assignment,completion_evidence
21|scale_ingestion_id,scale_ticket_event,facility_id,vehicle_id,material_stream,net_weight,source_timestamp,idempotency_key
22|education_campaign_id,target_route,contamination_theme,audience,channel,materials_sent,behavior_change_metric,follow_up_date
23|enforcement_fee_boundary_id,enforcement_case_projection,fee_code,notice_status,billing_boundary,no_fee_mutation,appeal_window,evidence_packet
24|service_request_boundary_id,request_projection,customer_id,request_type,linked_route_case,status_sync,no_crm_mutation,customer_visibility
25|route_performance_id,planned_stops,completed_stops,missed_stops,route_duration,fuel_usage,overtime_minutes,performance_trend
26|diversion_report_id,report_period,recycled_tons,landfilled_tons,organics_tons,diversion_rate,exclusion_reason,certification_status
27|emissions_estimate_id,vehicle_projection,fuel_type,distance,tons_collected,emission_factor,carbon_estimate,reduction_recommendation
28|safety_observation_id,driver_id,observation_type,severity,near_miss_flag,corrective_action,coach_owner,closure_evidence
29|route_disruption_id,disruption_type,affected_stops,alternate_route,customer_notice,crew_reassignment,recovery_eta,resolution_status
30|emergency_debris_id,event_name,debris_type,zone,crew_staging,contractor_support,facility_capacity,public_update
31|contractor_oversight_id,contractor_id,route_id,service_evidence,missed_stop_count,sla_status,invoice_boundary,corrective_action
32|commodity_sale_boundary_id,commodity_event,material_grade,weight,price_projection,buyer_projection,no_sales_mutation,profitability_view
33|permit_rule_id,permit_type,jurisdiction,facility_rule,material_rule,effective_date,compliance_result,approval_state
34|command_board_id,route_filters,missed_pickup_queue,contamination_queue,disruption_queue,safety_queue,kpi_cards,supervisor_actions
35|bin_service_history_id,bin_asset_id,pickup_history,maintenance_events,damage_reports,relocation_events,capacity_changes,history_digest
36|rule_parameter_id,rule_name,parameter_name,bounds,scope,effective_date,simulation_result,approval_state
37|route_exception_agent_id,exception_digest,route_context,recommended_action,cited_facts,customer_impact,human_confirmation,write_block
38|education_agent_id,contamination_case,photo_summary,material_guidance,draft_message,language_variant,cited_rules,approval_status
39|safety_agent_id,safety_summary,blocked_commands,hazmat_check,crew_risk,public_risk,escalation_target,write_block
40|event_model_id,event_name,payload_schema,lifecycle_transition,projection_replay,sequence_trace,consumer_contract,event_mapping
41|route_reconstruction_id,as_of_timestamp,event_sequence,route_state,pickup_snapshot,crew_projection,facility_ticket_snapshot,replay_hash
42|service_evidence_packet_id,hash_chain_root,photo_hashes,gps_hashes,scale_ticket_hashes,operator_signature,verification_channel,tamper_status
43|profitability_boundary_id,commodity_projection,processing_cost_projection,disposal_cost_projection,revenue_projection,margin_view,no_finance_mutation,boundary_evidence
44|accommodation_id,service_address,accessibility_need,placement_exception,assisted_setout,communication_preference,approval_state,service_instruction
45|capacity_right_sizing_id,bin_asset_id,fill_level_history,overflow_history,underutilization_flag,recommended_capacity,customer_notice,change_evidence
46|qa_sampling_id,sample_plan,route_sample,material_sample,contamination_rate,inspector,corrective_action,certification_evidence
47|smoke_scenario_id,scenario_name,test_reference,ui_evidence,event_trace,boundary_evidence,release_check,coverage_status
48|boundary_proof_id,dependency_name,projection_record,api_event_contract,no_foreign_mutation,idempotency_behavior,dead_letter_behavior,audit_reference
49|daily_briefing_id,supervisor_id,route_risks,missed_service_risks,contamination_hotspots,safety_alerts,resource_gaps,next_decision
50|command_center_id,active_routes,missed_pickups,contamination_rate,diversion_rate,facility_capacity_risk,emergency_mode,executive_status
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {4: ("FleetVehicleChanged", "CrewRosterChanged"), 12: ("FacilityScaleTicketRecorded",), 13: ("FacilityScaleTicketRecorded",), 23: ("EnforcementCaseOpened", "BillingFeeAssessed"), 24: ("CustomerServiceRequestChanged",), 28: ("CrewRosterChanged",), 30: ("WeatherEmergencyDeclared",), 31: ("ContractorRouteCompleted",), 32: ("CommoditySaleCreated",), 35: ("AssetMaintenanceCompleted",), 43: ("CommoditySaleCreated",), 48: ("PolicyChanged", "OperationalKpiChanged"), 50: ("AuditEvidenceSealed", "OperationalKpiChanged")}
_ROUTE_SERVICE_FEATURES = (1,2,3,4,5,6,7,8,15,17,18,19,20,29,30,31,34,35,44,45,49,50)
_MATERIAL_FACILITY_FEATURES = (9,10,11,12,13,14,16,21,22,26,27,32,33,43,46,50)
_COMPLIANCE_SAFETY_FEATURES = (10,12,14,23,24,28,30,31,33,36,39,42,44,48,50)
_GOVERNANCE_AGENT_FEATURES = (36,37,38,39,40,41,42,47,48,49,50)
_AGENT_FEATURES = (37,38,39,49,50)
_HUMAN_CONFIRMATION_FEATURES = (8,10,12,14,15,18,19,23,28,29,30,31,33,37,38,39,42,49,50)
_APPROVAL_REQUIRED_FEATURES = (14,18,23,28,30,31,33,39,42,49,50)
_NON_MUTATING_FEATURES = (4,11,12,13,21,22,23,24,25,26,27,32,34,36,37,38,39,40,41,42,43,45,46,47,48,49,50)
_PROJECTION_ONLY_FEATURES = (4,12,13,23,24,28,30,31,32,35,43,48)


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
    return {"title": capability.title, "slug": capability.slug, "tables": (f"waste_recycling_operations_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number], "ui": f"WasteRecyclingOperations{_camel(capability.slug)}Panel", "route": f"POST /waste-recycling-operations/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in WASTE_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({"database_backend": "postgresql", "event_contract": EVENT_CONTRACT, "event_topic": WASTE_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "shared_table_access": False, "dependency_access_mode": "api_event_projection", "human_confirmation": True, "approver_separate_from_initiator": True, "agent_preview_only": True, "non_mutating_simulation": True, "route_service_evidence_complete": True, "material_facility_evidence_complete": True, "compliance_safety_evidence_complete": True, "governance_agent_evidence_complete": True, "side_effects": ()})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned waste operations model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _ROUTE_SERVICE_FEATURES and payload.get("route_service_evidence_complete") is not True:
        findings.append("route service, territory calendars, stop sequencing, vehicle and crew projections, bin lifecycle, pickup proof, missed pickup resolution, bulky items, commercial containers, roll-off jobs, illegal dumping, public-bin work, disruptions, emergency debris, contractor oversight, bin history, accommodations, right-sizing, daily briefing, and command center evidence is required")
    if number in _MATERIAL_FACILITY_FEATURES and payload.get("material_facility_evidence_complete") is not True:
        findings.append("material streams, contamination workflow, recycling yield, disposal tickets, transfer facility boundary, hazardous material exceptions, organics quality, scale ingestion, education campaigns, diversion reporting, emissions, commodity sale boundary, permit rules, profitability, QA sampling, and command evidence is required")
    if number in _COMPLIANCE_SAFETY_FEATURES and payload.get("compliance_safety_evidence_complete") is not True:
        findings.append("contamination, disposal reconciliation, hazmat, enforcement and fee boundaries, customer-service boundary, driver safety, emergency debris, contractor oversight, compliance permits, rule workbench, safety agent restrictions, cryptographic evidence, accommodations, cross-PBC boundary, and command center evidence is required")
    if number in _GOVERNANCE_AGENT_FEATURES and payload.get("governance_agent_evidence_complete") is not True:
        findings.append("rule parameters, governed route and contamination agents, safety restrictions, AppGen-X events, point-in-time reconstruction, cryptographic service evidence, release scenarios, boundary proof, supervisor briefing, and command center evidence is required")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("missed pickup closure, contamination notices, disposal reconciliation, hazmat, bulky and roll-off scheduling, illegal dumping, enforcement, safety, disruptions, emergency debris, contractor oversight, permit changes, agent recommendations, evidence packets, supervisor briefing, and command decisions require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk waste operations require separated approval for hazmat, roll-off, enforcement fees, safety observations, emergency debris, contractor oversight, permit rules, safety agents, evidence packets, supervisor briefing, and command center decisions")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("waste operations assistant skills must cite owned facts, show reversible CRUD previews, enforce safety permissions and policy checks, and block direct writes before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("vehicle and crew projections, yield analytics, facility projections, scale ingestion, education analysis, boundaries, route analytics, diversion, emissions, commodity sales, command boards, rules, agents, event replay, cryptographic proof, profitability, capacity analysis, QA sampling, release scenarios, boundary proof, briefings, and command center must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("fleet, crew, facility, enforcement, billing, customer-service, emergency, contractor, commodity sale, asset maintenance, policy, KPI, and audit context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != WASTE_REQUIRED_EVENT_TOPIC:
        findings.append("waste recycling operations eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in WASTE_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary waste recycling operations datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("waste recycling operations controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_waste_recycling_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in WASTE_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in WASTE_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "primary_proof": spec["primary_proof"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": WASTE_REQUIRED_EVENT_TOPIC, "allowed_database_backends": WASTE_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "configurable_rules_parameters": True, "agent_assisted": True, "side_effect_free": True}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "title": resolved.title, "slug": resolved.slug, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "evidence": evidence, "payload_digest": _digest(candidate)[:20], "side_effects": ()}


def improve1_waste_recycling_operations_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_waste_recycling_operations_control(capability) for capability in WASTE_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {"format": "appgen.waste_recycling_operations.improve1-control-contract.v1", "ok": len(results) == 50 and all(item["ok"] for item in results), "pbc": PBC_KEY, "capability_count": len(results), "capabilities": results, "owned_tables": WASTE_CONTROL_OWNED_TABLES, "allowed_database_backends": WASTE_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": WASTE_REQUIRED_EVENT_TOPIC, "declared_dependencies": WASTE_DECLARED_DEPENDENCIES, "stream_engine_picker_visible": False, "blocking_gaps": blocking_gaps, "side_effects": ()}


WASTE_RECYCLING_OPERATIONS_CONTROL_FUNCTIONS = ("evaluate_waste_recycling_operations_control", "improve1_waste_recycling_operations_control_contract", "sample_payload_for")
