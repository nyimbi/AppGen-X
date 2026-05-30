"""Executable improve1 controls for the Port Terminal Operations PBC."""
from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    PORT_TERMINAL_OPERATIONS_OWNED_TABLES,
    PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
)

PBC_KEY = "port_terminal_operations"
EVENT_CONTRACT = "AppGen-X"
PORT_CONTROL_ALLOWED_DATABASE_BACKENDS = PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS
PORT_CONTROL_REQUIRED_EVENT_TOPIC = PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC
PORT_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(PORT_TERMINAL_OPERATIONS_OWNED_TABLES + tuple(f"port_terminal_operations_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
PORT_CONTROL_DECLARED_DEPENDENCIES = (
    "LineVesselScheduleUpdated",
    "MarineServiceConfirmed",
    "LaborRosterChanged",
    "CraneTelemetryChanged",
    "GateAppointmentChanged",
    "CustomsReleaseChanged",
    "CarrierReleaseChanged",
    "RailBargeCutoffChanged",
    "EquipmentHealthChanged",
    "ReeferAlarmChanged",
    "DangerousGoodsRuleChanged",
    "WeatherClosureChanged",
    "EdiMessageReceived",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "PolicyChanged",
)
PORT_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in PORT_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in PORT_CONTROL_CAPABILITIES}
_BASE_FIELDS = (
    "tenant_id",
    "terminal_id",
    "vessel_call_id",
    "container_id",
    "berth_plan_id",
    "yard_slot_id",
    "gate_transaction_id",
    "equipment_id",
    "customs_handoff_id",
    "actor_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|arrival_model_id,last_advised_eta,pilot_ready_eta,tide_feasible_eta,confidence_band,revision_reason
2|berth_conflict_id,loa,beam,draft,bollard_reach,next_feasible_window
3|readiness_checklist_id,pilotage_status,tug_status,gang_assignment,customs_preclearance,crane_availability
4|crane_assignment_id,bay_plan_ref,hatch_group,crane_split_zone,crossing_restriction,travel_time
5|crane_intensity_id,planned_gmph,feasible_gmph,labor_roster_ref,maintenance_window,supervisor_override
6|bay_sequence_id,hatch_cover_order,lashing_status,bay_access_readiness,blocked_move_set,delay_projection
7|restow_case_id,planned_restows,preventable_restows,stack_geometry,destination_mix,operator_justification
8|move_lifecycle_id,move_state,dispatch_actor,execution_equipment,location_timestamp,reversal_reason
9|lift_mode_id,twin_lift_eligible,tandem_eligible,dual_cycle_eligible,weight_spread,dg_restriction
10|yard_allocation_id,cargo_flow,onward_mode,service_string,special_handling_class,reserved_capacity
11|rehandle_hotspot_id,stack_height,due_time,box_priority,truck_demand,relocation_scenario
12|stack_discipline_id,weight_ordering,dg_segregation,oog_geometry,line_allocation,override_approval
13|misposition_case_id,last_confirmed_move,equipment_breadcrumb,ocr_sighting,candidate_location,closure_confirmation
14|appointment_capacity_id,hour_bucket,lane_id,transaction_type,trucking_segment,overbooking_rule
15|turn_time_case_id,delay_stage,cause_code,owning_team,due_clock,repeat_cause
16|empty_balance_id,line_owner,depot_target,return_window,yard_dwell,reposition_priority
17|customs_release_gate_id,release_state,inspection_requirement,scan_result,expiry_timestamp,source_message
18|hold_model_id,hold_type,issuer,effective_time,precedence,override_authority
19|customs_exam_id,staging_position,scan_appointment,escort_step,return_instruction,retry_reason
20|imdg_check_id,imdg_class,subsidiary_risk,flashpoint,segregation_group,documentation_completeness
21|reefer_plug_id,socket_id,power_status,cable_reach,genset_dependency,reserve_margin
22|reefer_alarm_id,temperature_deviation,power_loss,unplug_event,commodity_sensitivity,tolerance_window
23|dwell_watchlist_id,free_time_expiry,hold_status,customs_stage,appointment_availability,root_cause
24|free_time_exception_id,exception_ground,approver,time_range,supporting_event,dispute_export
25|transshipment_protection_id,inbound_eta_confidence,discharge_sequence,outbound_cutoff,rescue_move,roll_decision
26|intermodal_cutoff_id,onward_mode,departure_cutoff,staging_need,late_gate_tolerance,carrier
27|marine_dependency_id,service_type,requested_time,confirmed_time,provider_ack,slippage_reason
28|equipment_health_id,operating_state,fault_category,maintenance_hold,battery_fuel_state,fallback_pool
29|vessel_reconciliation_id,planned_move_count,actual_move_count,bay_completion,hatch_closure,final_stow_confirmation
30|edi_ingest_id,message_type,source_message_id,segment_error,normalized_event,replay_checkpoint
31|timestamp_fidelity_id,occurrence_time,capture_time,ingest_time,correction_time,ordering_policy
32|replay_policy_id,idempotency_key,late_message_policy,superseded_message,quarantine_reason,checkpoint_hash
33|customs_audit_chain_id,request_ref,response_ref,source_officer,document_ref,enabled_action
34|live_workbench_id,berth_board_filter,yard_board_filter,gate_board_filter,shared_context,drillthrough_target
35|yard_heatmap_id,occupancy,dwell_pressure,plug_usage,dg_concentration,rehandle_risk
36|exception_cockpit_id,domain_stream,severity,aging_bucket,sla_breach_risk,escalation_path
37|evidence_panel_id,hold_timeline,release_messages,customs_actions,gate_attempts,source_links
38|handover_log_id,shift_id,active_risks,pending_approvals,priority_actions,acknowledgement
39|vessel_agent_skill_id,eta_shift_summary,berth_conflict_summary,crane_impact,sail_readiness_gap,corrective_plan_preview
40|yard_agent_skill_id,scenario_source_slots,re_slot_recommendation,predicted_impact,dwell_tradeoff,planner_feedback
41|gate_agent_skill_id,appointment_utilization,long_turn_root_cause,lane_outage,quota_adjustment,capacity_assumption
42|customs_agent_skill_id,release_posture,active_holds,hold_precedence,permissible_action,named_user_approval
43|reefer_agent_skill_id,active_alarm_summary,plug_saturation,cargo_exposure,inspection_sequence,operator_confirmation
44|agent_governance_id,preview_diff,affected_assets,policy_checks,downstream_impacts,approver
45|scenario_simulation_id,delay_case,baseline_kpi,simulated_kpi,assumptions,response_plan
46|release_evidence_pack_id,berth_case,yard_case,dg_reefer_case,customs_gate_case,edi_replay_trace
47|test_data_id,vessel_profile,bay_count,cargo_mix,yard_occupancy,gate_demand
48|kpi_baseline_id,kpi_name,good_threshold,at_risk_threshold,failed_threshold,approval_history
49|tenant_policy_variant_id,tide_constraint_set,dg_rule_set,gate_hours,customs_process,reefer_capacity
50|recovery_drill_id,failure_mode,degraded_mode,restore_time,data_loss_window,unresolved_gap
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {n: f"{CAPABILITY_BY_NUMBER[n].slug}_verified" for n in range(1, 51)}
_FEATURE_FIELDS = {n: _BASE_FIELDS + _DOMAIN_FIELDS[n] + (_PRIMARY_PROOF_FIELDS[n],) for n in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("LineVesselScheduleUpdated",),
    3: ("MarineServiceConfirmed", "LaborRosterChanged", "CustomsReleaseChanged"),
    4: ("CraneTelemetryChanged",),
    5: ("LaborRosterChanged", "CraneTelemetryChanged"),
    14: ("GateAppointmentChanged",),
    17: ("CustomsReleaseChanged", "CarrierReleaseChanged"),
    19: ("CustomsReleaseChanged",),
    20: ("DangerousGoodsRuleChanged",),
    22: ("ReeferAlarmChanged",),
    26: ("RailBargeCutoffChanged",),
    27: ("MarineServiceConfirmed",),
    28: ("EquipmentHealthChanged",),
    30: ("EdiMessageReceived",),
    32: ("EdiMessageReceived",),
    33: ("CustomsReleaseChanged", "AuditEventSealed"),
    45: ("WeatherClosureChanged", "EquipmentHealthChanged", "CustomsReleaseChanged"),
    48: ("OperationalKpiChanged",),
    49: ("PolicyChanged",),
    50: ("EdiMessageReceived", "AuditEventSealed"),
}
_HUMAN_CONFIRMATION_FEATURES = (2, 3, 5, 7, 12, 17, 18, 20, 24, 25, 28, 29, 34, 38, 39, 40, 41, 42, 43, 44, 45, 46, 49, 50)
_PROJECTION_ONLY_FEATURES = (1, 3, 4, 5, 14, 17, 19, 20, 22, 26, 27, 28, 30, 32, 33, 45, 48, 49, 50)
_AGENT_PREVIEW_FEATURES = (39, 40, 41, 42, 43, 44)
_NON_MUTATING_FEATURES = (2, 11, 13, 23, 24, 25, 31, 32, 34, 35, 36, 37, 39, 40, 41, 42, 43, 45, 46, 48, 50)
_PORT_RISK_FEATURES = (1, 2, 3, 4, 5, 6, 7, 9, 12, 15, 17, 18, 19, 20, 21, 22, 24, 25, 27, 28, 29, 32, 33, 36, 38, 44, 45, 46, 49, 50)


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
        "tables": (f"port_terminal_operations_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"PortTerminalOperations{_camel(capability.slug)}Panel",
        "route": f"POST /port-terminal-operations/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in PORT_CONTROL_CAPABILITIES}


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
        "event_topic": PORT_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "port_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires port-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _PORT_RISK_FEATURES and payload.get("port_risk_evidence_complete") is not True:
        findings.append("berth, crane, yard, gate, customs, DG, reefer, EDI, replay, handover, agent, release, tenant, and recovery decisions require complete port operations risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("berth conflicts, readiness, intensity, restow, override, release, holds, DG, free-time, transshipment, equipment, closure, boards, handover, agent, simulation, release, tenant, and recovery decisions require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("port agent skills must produce cited, permission-checked, side-effect-free previews before confirmed operations changes")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("conflict resolution, hotspot prediction, search, dwell, free-time evidence, transshipment, timestamp replay, workbench, heatmap, cockpit, evidence panel, agents, scenarios, release packs, KPI baselines, and recovery drills must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("line, marine, labor, crane, gate, customs, carrier, rail, equipment, reefer, DG, weather, EDI, audit, KPI, and policy facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != PORT_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("port terminal eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in PORT_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary port terminal datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("port controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_port_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in PORT_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in PORT_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": PORT_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PORT_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_port_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_port_control(capability) for capability in PORT_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.port-terminal-operations-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": PORT_CONTROL_OWNED_TABLES,
        "declared_dependencies": PORT_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": PORT_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": PORT_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


PORT_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_port_control(slug, payload)) for capability in PORT_CONTROL_CAPABILITIES}
