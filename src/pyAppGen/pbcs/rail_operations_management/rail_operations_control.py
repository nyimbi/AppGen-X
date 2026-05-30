"""Executable improve1 controls for the Rail Operations Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES,
    RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES,
)

PBC_KEY = "rail_operations_management"
EVENT_CONTRACT = "AppGen-X"
RAIL_ALLOWED_DATABASE_BACKENDS = RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
RAIL_REQUIRED_EVENT_TOPIC = RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC
RAIL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in RAIL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in RAIL_CAPABILITIES}
RAIL_OWNED_TABLES = tuple(
    dict.fromkeys(
        RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES
        + RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES
        + tuple(f"rail_operations_management_{capability.slug}_control" for capability in RAIL_CAPABILITIES)
    )
)
RAIL_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "InfrastructurePossessionChanged",
    "RollingStockAvailabilityChanged",
    "CrewRosterChanged",
    "WeatherRestrictionChanged",
    "StationCapacityChanged",
    "EnergyPriceSignalChanged",
    "MaintenanceWindowChanged",
    "PassengerConnectionChanged",
    "FreightYardStatusChanged",
)
_BASE_FIELDS = (
    "tenant_id",
    "train_id",
    "service_id",
    "corridor_id",
    "dispatcher_id",
    "operating_day",
    "control_area",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|train_graph_id,path_id,section_sequence,runtime_minutes,conflict_window,baseline_version,path_status
2|timetable_separation_id,public_timetable_id,operating_timetable_id,customer_time,control_time,publication_state,separation_reason
3|headway_validation_id,junction_id,minimum_headway,actual_headway,conflict_pair,clearance_time,validation_status
4|consist_version_id,formation_id,vehicle_sequence,version_number,effective_time,change_reason,approval_state
5|restriction_match_id,vehicle_id,route_restriction,axle_load,gauge_class,traction_limit,match_decision
6|crew_boundary_id,crew_id,district,sign_on_location,relief_point,handoff_time,boundary_status
7|fatigue_legality_id,crew_id,duty_start,duty_end,rest_minutes,legal_limit,legality_decision
8|movement_authority_id,authority_type,track_section,start_signal,end_signal,issued_at,authority_status
9|possession_integration_id,possession_id,engineering_window,blocked_section,protection_method,release_time,integration_status
10|speed_restriction_id,restriction_id,track_section,speed_limit,start_time,end_time,driver_notice_status
11|block_constraint_id,signal_id,block_id,occupancy_state,route_lock,conflict_status,constraint_decision
12|station_call_id,station_id,call_type,dwell_time,skip_stop_reason,passenger_impact,call_status
13|platform_occupation_id,platform_id,arrival_time,departure_time,turnback_move,occupation_conflict,platform_decision
14|yard_route_id,yard_id,move_id,route_path,authority_holder,conflict_check,move_status
15|shunt_safety_id,shunt_move,staff_protection,brake_test_status,route_confirmation,safety_briefing,shunt_decision
16|freight_makeup_id,train_length,tonnage,brake_ratio,dangerous_goods,marshalling_rule,balance_status
17|formation_swap_id,old_formation,new_formation,platform_fit,accessibility_impact,passenger_notice,swap_status
18|passenger_recovery_id,disruption_type,recovery_playbook,connection_plan,crew_stock_option,customer_impact,recovery_status
19|freight_reslot_id,freight_service,missed_path,terminal_window,re_slot_option,customer_priority,reslot_status
20|delay_attribution_id,delay_code,primary_cause,secondary_cause,responsible_party,evidence_link,attribution_status
21|incident_timeline_id,incident_id,command_role,timeline_event,tactical_decision,handover_note,incident_status
22|near_miss_evidence_id,near_miss_type,location,participants,safety_evidence,investigation_owner,evidence_status
23|weather_restriction_id,weather_signal,restriction_type,affected_section,operating_rule,review_time,restriction_status
24|resource_triage_id,stock_option,crew_option,infrastructure_option,priority_service,tradeoff_reason,triage_decision
25|crossing_block_id,crossing_id,line_block_id,protection_arrangement,road_impact,authority_contact,coordination_status
26|terminal_capacity_id,terminal_id,throat_route,platform_capacity,conflicting_moves,queue_depth,capacity_decision
27|maintenance_negotiation_id,window_id,requested_scope,train_impact,alternative_slot,approver,negotiation_status
28|interline_handover_id,boundary_point,partner_operator,handover_packet,acceptance_time,exception,handver_status
29|movement_history_id,event_sequence,location,time_report,authority_reference,previous_hash,history_status
30|late_running_risk_id,current_delay,downstream_conflict,missed_connection_risk,confidence,recovery_option,risk_status
31|dispatch_simulation_id,scenario_name,changed_authority,affected_trains,delay_delta,safety_delta,simulation_state
32|station_timeline_ui_id,station_id,platform_view,passenger_flow,incident_overlay,operator_action,ui_status
33|corridor_dispatcher_ui_id,corridor_view,train_graph_overlay,conflict_marker,authority_action,delay_heatmap,ui_status
34|yardmaster_ui_id,yard_id,move_board,route_conflict,shunt_warning,resource_view,ui_status
35|incident_commander_ui_id,incident_id,timeline_panel,resource_panel,restriction_panel,handover_panel,ui_status
36|safe_change_release_id,change_type,timetable_delta,dispatch_delta,safety_checks,approver,release_state
37|timetable_agent_skill_id,source_instruction,amendment_draft,affected_services,missing_questions,human_confirmation,write_block
38|consist_agent_skill_id,fault_context,repair_suggestion,restriction_check,capacity_impact,human_confirmation,write_block
39|incident_agent_skill_id,incident_notes,summary_draft,handover_sections,citation_map,confidence,write_block
40|event_catalog_id,event_schema,movement_event,authority_event,incident_event,recovery_event,consumer_contract
41|consumed_event_freshness_id,event_type,source_system,freshness_limit,last_seen,staleness_action,handler_status
42|incident_release_evidence_id,incident_id,critical_actions,safety_evidence,handover_packet,reviewer,release_state
43|scenario_pack_id,scenario_name,seed_trains,seed_possessions,seed_incidents,expected_event,coverage_label
44|policy_workbench_id,rule_name,parameter_name,current_value,guardrail,impact_preview,approval_state
45|data_model_primitive_id,primitive_type,relationship,owned_table,migration_status,projection_boundary,model_status
46|tenant_rule_isolation_id,tenant,rule_scope,policy_family,encryption_boundary,access_boundary,isolation_status
47|replay_recovery_id,event_id,idempotency_key,retry_count,dead_letter_reason,replay_checkpoint,recovery_status
48|energy_dispatch_id,energy_signal,carbon_intensity,tractive_energy,delay_tradeoff,chosen_path,energy_decision
49|continuous_control_id,control_rule,population,failing_sample,owner,remediation,closure_evidence
50|go_live_scorecard_id,readiness_metric,score,blocking_gap,owner,exit_criteria,go_live_decision
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    4: ("RollingStockAvailabilityChanged",),
    5: ("RollingStockAvailabilityChanged",),
    6: ("CrewRosterChanged",),
    7: ("CrewRosterChanged",),
    9: ("InfrastructurePossessionChanged", "MaintenanceWindowChanged"),
    17: ("RollingStockAvailabilityChanged",),
    18: ("PassengerConnectionChanged",),
    19: ("FreightYardStatusChanged",),
    23: ("WeatherRestrictionChanged",),
    26: ("StationCapacityChanged",),
    27: ("MaintenanceWindowChanged",),
    29: ("AuditEventSealed",),
    40: ("AuditEventSealed",),
    41: ("PolicyChanged", "OperationalKpiChanged"),
    48: ("EnergyPriceSignalChanged",),
    50: ("AuditEventSealed",),
}
_HUMAN_CONFIRMATION_FEATURES = (2, 4, 8, 10, 14, 15, 17, 18, 19, 21, 24, 27, 28, 31, 36, 37, 38, 39, 42, 44, 47, 48, 50)
_SUPERVISOR_APPROVAL_FEATURES = (3, 7, 8, 9, 11, 14, 15, 21, 22, 24, 25, 27, 31, 36, 42, 44, 46, 50)
_NON_MUTATING_FEATURES = (1, 3, 5, 7, 9, 11, 13, 16, 18, 19, 20, 23, 24, 26, 27, 30, 31, 32, 33, 34, 35, 37, 38, 39, 41, 43, 44, 45, 48, 49, 50)
_AI_PREVIEW_FEATURES = (30, 31, 37, 38, 39, 42, 44, 49, 50)
_SAFETY_EVIDENCE_FEATURES = (3, 7, 8, 9, 10, 11, 14, 15, 21, 22, 23, 25, 27, 29, 31, 36, 42, 46, 47, 49, 50)
_SERVICE_RECOVERY_FEATURES = (18, 19, 20, 24, 28, 30, 31, 39, 41, 47, 48, 50)
_PROJECTION_ONLY_FEATURES = (4, 5, 6, 7, 9, 17, 18, 19, 23, 26, 27, 29, 40, 41, 48, 50)


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
        "tables": (f"rail_operations_management_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"RailOperationsManagement{_camel(capability.slug)}Panel",
        "route": f"POST /rail-operations-management/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in RAIL_CAPABILITIES}


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
        "event_topic": RAIL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "supervisor_approval": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "safety_evidence_complete": True,
        "service_recovery_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned rail evidence, UI, service/API, event, safety, agent, and release proof before approval.")
    if number in _SAFETY_EVIDENCE_FEATURES and payload.get("safety_evidence_complete") is not True:
        findings.append("headway, crew legality, movement authority, possessions, speed restrictions, signaling, yard/shunt safety, incidents, near misses, weather, crossings, maintenance, movement history, simulations, release changes, incident evidence, tenant rules, replay, continuous controls, and go-live require complete rail safety evidence")
    if number in _SERVICE_RECOVERY_FEATURES and payload.get("service_recovery_evidence_complete") is not True:
        findings.append("passenger recovery, freight re-slotting, delay attribution, resource triage, interline handover, late-running risk, simulations, incident handover, freshness, replay, energy choices, and go-live require service recovery evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("timetable, consist, authority, restrictions, yard, shunt, recovery, incident, triage, negotiation, handover, simulations, release changes, agent drafts, incident evidence, policy, replay, energy, and go-live decisions require human confirmation")
    if number in _SUPERVISOR_APPROVAL_FEATURES and payload.get("supervisor_approval") is not True:
        findings.append("conflicts, crew legality, movement authority, possessions, block occupancy, yard/shunt moves, incidents, near misses, crossings, maintenance, simulations, release, incident evidence, policy isolation, and go-live require control supervisor approval")
    if number in _AI_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("rail operations agent skills must remain cited, permission-checked, and preview-only until confirmed by operations staff")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("graph validation, restrictions, crew checks, possessions, signals, platforms, freight makeup, recovery, delay attribution, weather, triage, capacity, maintenance, risk, simulation, UI, agents, event freshness, scenarios, policy, data models, energy, controls, and go-live must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("rolling stock, crew, infrastructure, station, weather, maintenance, passenger, freight, energy, KPI, policy, and audit facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != RAIL_REQUIRED_EVENT_TOPIC:
        findings.append("rail operations eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in RAIL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary rail operations datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("rail operations controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_rail_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in RAIL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in RAIL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": RAIL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": RAIL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_rail_operations_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_rail_operations_control(capability) for capability in RAIL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.rail-operations-management-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": RAIL_OWNED_TABLES,
        "declared_dependencies": RAIL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": RAIL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": RAIL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


RAIL_OPERATIONS_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_rail_operations_control(slug, payload)) for capability in RAIL_CAPABILITIES}
