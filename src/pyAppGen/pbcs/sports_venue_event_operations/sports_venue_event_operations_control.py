"""Executable improve1 controls for the Sports Venue Event Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    SPORTS_VENUE_EVENT_OPERATIONS_CONSUMED_EVENT_TYPES,
    SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES,
    SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC,
    SPORTS_VENUE_EVENT_OPERATIONS_RUNTIME_TABLES,
)

PBC_KEY = "sports_venue_event_operations"
EVENT_CONTRACT = "AppGen-X"
SPORTS_ALLOWED_DATABASE_BACKENDS = SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS
SPORTS_REQUIRED_EVENT_TOPIC = SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC
SPORTS_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in SPORTS_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in SPORTS_CAPABILITIES}
SPORTS_OWNED_TABLES = tuple(
    dict.fromkeys(
        SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES
        + SPORTS_VENUE_EVENT_OPERATIONS_RUNTIME_TABLES
        + tuple(f"sports_venue_event_operations_{capability.slug}_control" for capability in SPORTS_CAPABILITIES)
    )
)
SPORTS_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        SPORTS_VENUE_EVENT_OPERATIONS_CONSUMED_EVENT_TYPES
        + (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "TicketManifestUpdated",
            "CredentialScanReceived",
            "WeatherAlertIssued",
            "PublicSafetyAdvisoryIssued",
            "TransitServiceDisrupted",
            "ParkingInventoryChanged",
            "ConcessionPosOutageReported",
            "MedicalIncidentTransferred",
            "BroadcastScheduleChanged",
            "TeamItineraryChanged",
            "PremiumHospitalityRequestUpdated",
            "VendorArrivalStatusChanged",
            "SettlementVariancePosted",
            "TenantAccessPolicyChanged",
            "CertificationStatusChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "venue_id",
    "event_id",
    "event_day",
    "zone_id",
    "role_owner",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|calendar_hold_id,event_type,promoter_or_team_owner,priority_rank,venue_space_scope,hold_type,cancellation_lineage
2|blackout_window_id,changeover_buffer,curfew_cutoff,crew_rest_period,shutdown_window,unsafe_schedule_block,warning_state
3|competition_conflict_id,league_window,cup_window,broadcast_exclusivity,shared_campus_dependency,alternative_date_set,exception_evidence
4|seating_boundary_id,seat_restriction_type,accessible_inventory_scope,camera_platform_hold,team_hold,commerce_field_rejection,boundary_proof
5|seat_hold_workflow_id,section_row_seat_range,hold_reason,owner,release_deadline,approval_threshold,notification_state
6|accessible_seating_control_id,accessible_classification,companion_pairing_rule,temporary_obstruction,relocation_workflow,supervisor_ack,reduction_approval
7|ingress_zone_id,gate_assignment,open_time,expected_scan_rate,queue_storage_capacity,screening_requirement,fallback_gate
8|egress_route_id,exit_path,lot_release_phase,chokepoint_state,rideshare_zone,bus_dispatch_window,alternate_route_trigger
9|gate_security_boundary_id,gate_task_owner,screening_task_owner,credential_verification_owner,ada_access_owner,queue_management_owner,joint_signoff
10|credential_taxonomy_id,credential_class,zone_access_set,time_window,escort_requirement,revocation_status,template_version
11|credential_scan_id,portal_location,zone_entered,scan_timestamp,exception_reason,escort_linkage,access_window_validation
12|staffing_boundary_id,event_role,post_assignment,shift_timing,certification_status,attendance_status,hr_field_rejection
13|shift_roster_id,checkin_status,no_show_flag,break_window,relief_assignment,standby_pool,replacement_source
14|onboarding_readiness_id,worker_type,id_verification,orientation_completion,rules_acknowledgement,uniform_pickup,deployable_status
15|concession_boundary_id,stand_activation,menu_selection,expected_demand,labor_requirement,alcohol_control,finance_field_rejection
16|stand_outage_id,replenishment_run,outage_type,fallback_menu,pos_degrade_mode,nearby_reroute,closure_state
17|alcohol_control_id,event_cutoff_time,section_restriction,id_check_escalation,intoxication_incident,override_reason,service_lock_state
18|crowd_density_id,area_type,density_value,threshold_level,reverse_flow_risk,intervention_trigger,heatmap_state
19|fan_issue_taxonomy_id,issue_category,severity,location_precision,required_response_team,sla_target,closure_proof
20|incident_command_id,incident_level,commander,scribe,active_objective,resource_request,decision_log
21|medical_response_id,first_aid_room,medic_team,aed_location,stretcher_route,ambulance_ingress,ems_handoff_state
22|evacuation_playbook_id,hazard_type,playbook_type,assembly_zone,message_template,authority_requirement,activation_status
23|field_readiness_id,surface_condition,marking_status,equipment_setup,official_review,locker_room_turnover,required_signoff
24|changeover_phase_id,conversion_type,derig_task,clean_task,seat_reconfiguration,stage_load,critical_path_risk
25|venue_system_readiness_id,system_type,check_status,outage_workflow,fallback_procedure,escalation_path,degraded_mode_decision
26|broadcast_compound_id,truck_arrival_window,dock_assignment,power_requirement,cable_route,camera_position_hold,strike_deadline
27|run_of_show_id,segment_type,owner,target_duration,broadcast_window,contingency_branch,variance_report
28|vip_boundary_id,premium_space,access_scope,catering_readiness,host_contact,incident_handling,billing_field_rejection
29|premium_service_id,arrival_window,dedicated_screening,escort_requirement,suite_stocking_deadline,hospitality_handoff,late_open_escalation
30|transport_staging_id,parking_lot_allocation,rideshare_geofence,vip_curb_zone,bus_parking,media_parking,traffic_release_sequence
31|weather_watch_id,hazard_type,threshold_value,forecast_confidence,watch_state,warning_state,acknowledgement_owner
32|weather_procedure_id,hazard_procedure,player_action,fan_action,staff_role_assignment,message_plan,reentry_criteria
33|weather_settlement_id,delay_duration,overtime_labor,premium_recovery_spend,abandoned_concessions,reschedule_trigger,settlement_link
34|accessibility_wayfinding_id,path_type,elevator_status,ramp_status,sensory_room_status,temporary_closure,alternate_route
35|command_ui_id,persona,event_status,gates_state,staffing_gap,crowd_alert,permissioned_action
36|offline_supervisor_ui_id,device_mode,queued_task,incident_capture_state,gate_state_change,sync_conflict,offline_resolution
37|document_intake_skill_id,source_document_hash,extracted_date,extracted_space,staffing_ask,seat_hold_request,review_diff
38|live_exception_triage_skill_id,issue_group,severity_summary,likely_owner,next_safe_action,duplicate_cluster,permission_block
39|after_action_skill_id,source_log_set,fan_issue_closure_set,staffing_gap_set,weather_milestone_set,unknown_marker,review_state
40|event_catalog_id,domain_event_type,schema_version,idempotency_rule,workflow_mapping,downstream_reliance,event_example
41|consumed_event_contract_id,consumed_event_type,handler_behavior,duplicate_delivery_result,out_of_order_result,reopened_marker,dead_letter_evidence
42|release_evidence_pack_id,api_contract_result,workflow_test_result,ui_capture_result,event_schema_snapshot,permission_proof,scenario_pass
43|drill_evidence_id,drill_type,scenario_definition,participant_role_set,observed_gap,remediation_owner,closure_status
44|certification_control_id,certification_type,expiry_date,post_requirement,qualified_status,blocked_assignment,supervisor_view
45|vendor_load_plan_id,arrival_slot,dock_assignment,freight_path,escort_need,credential_prerequisite,strike_deadline
46|protected_arrival_id,stakeholder_class,secure_parking,tunnel_route,arrival_window,room_readiness,escort_owner
47|housekeeping_readiness_id,service_zone,restroom_check,consumable_replenishment,spill_response,waste_pull_schedule,sla_target
48|settlement_variance_id,staffing_variance,overtime_cost,concession_outage_loss,premium_recovery_spend,damage_claim,closeout_link
49|tenant_isolation_id,calendar_scope,suite_note_scope,credential_scope,incident_scope,redaction_policy,audit_result
50|readiness_gate_id,calendar_score,seating_score,ingress_egress_score,staffing_score,crowd_safety_score,approval_decision
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    3: ("BroadcastScheduleChanged",),
    4: ("TicketManifestUpdated",),
    5: ("TicketManifestUpdated",),
    11: ("CredentialScanReceived",),
    16: ("ConcessionPosOutageReported",),
    21: ("MedicalIncidentTransferred",),
    26: ("BroadcastScheduleChanged",),
    29: ("PremiumHospitalityRequestUpdated",),
    30: ("TransitServiceDisrupted", "ParkingInventoryChanged"),
    31: ("WeatherAlertIssued",),
    32: ("WeatherAlertIssued", "PublicSafetyAdvisoryIssued"),
    33: ("WeatherAlertIssued", "SettlementVariancePosted"),
    41: ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"),
    44: ("CertificationStatusChanged",),
    45: ("VendorArrivalStatusChanged",),
    46: ("TeamItineraryChanged",),
    49: ("TenantAccessPolicyChanged",),
}
_EVENT_CALENDAR_FEATURES = (1, 2, 3, 24, 26, 27, 30, 45, 46, 48, 50)
_SEATING_ACCESS_FEATURES = (4, 5, 6, 10, 11, 28, 29, 34, 49, 50)
_CROWD_SAFETY_FEATURES = (7, 8, 9, 17, 18, 19, 20, 21, 22, 31, 32, 35, 36, 43, 50)
_STAFF_CONCESSION_FEATURES = (12, 13, 14, 15, 16, 17, 44, 47, 48, 50)
_ASSISTANT_FEATURES = (37, 38, 39, 50)
_EVENTING_RELEASE_FEATURES = (40, 41, 42, 43, 48, 49, 50)
_HUMAN_CONFIRMATION_FEATURES = (2, 5, 6, 10, 13, 16, 17, 20, 22, 23, 24, 25, 31, 32, 35, 37, 38, 39, 42, 43, 44, 45, 46, 49, 50)
_APPROVAL_REQUIRED_FEATURES = (2, 5, 6, 10, 17, 20, 22, 23, 24, 25, 31, 32, 42, 43, 44, 45, 46, 49, 50)
_NON_MUTATING_FEATURES = (1, 2, 3, 5, 7, 8, 18, 24, 27, 31, 32, 35, 36, 37, 38, 39, 41, 42, 43, 49, 50)
_PROJECTION_ONLY_FEATURES = (3, 4, 5, 11, 16, 21, 26, 29, 30, 31, 32, 33, 41, 44, 45, 46, 49)


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
        "tables": (f"sports_venue_event_operations_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"SportsVenueEventOperations{_camel(capability.slug)}Panel",
        "route": f"POST /sports-venue-event-operations/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in SPORTS_CAPABILITIES}


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
        "event_topic": SPORTS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "event_calendar_evidence_complete": True,
        "seating_access_evidence_complete": True,
        "crowd_safety_evidence_complete": True,
        "staff_concession_evidence_complete": True,
        "eventing_release_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned venue model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _EVENT_CALENDAR_FEATURES and payload.get("event_calendar_evidence_complete") is not True:
        findings.append("event calendars, blackout/changeover, competition conflicts, changeover phases, broadcast compound, run-of-show, transport staging, vendor load, protected arrivals, settlement, and readiness require event calendar evidence")
    if number in _SEATING_ACCESS_FEATURES and payload.get("seating_access_evidence_complete") is not True:
        findings.append("seating boundaries, seat holds, accessible seating, credentials, credential scans, VIP boundaries, premium service, accessibility wayfinding, tenant confidentiality, and readiness require seating access evidence")
    if number in _CROWD_SAFETY_FEATURES and payload.get("crowd_safety_evidence_complete") is not True:
        findings.append("ingress, egress, gate/security responsibility, alcohol controls, crowd density, fan dispatch, incident command, medical routing, evacuation, weather, command UI, offline supervisor flows, drills, and readiness require crowd safety evidence")
    if number in _STAFF_CONCESSION_FEATURES and payload.get("staff_concession_evidence_complete") is not True:
        findings.append("staffing boundaries, rostering, onboarding, concessions, replenishment/outages, alcohol, certifications, housekeeping, settlement variances, and readiness require staff concession evidence")
    if number in _EVENTING_RELEASE_FEATURES and payload.get("eventing_release_evidence_complete") is not True:
        findings.append("day-of-event catalog, consumed event contracts, release packs, drills, settlement, tenancy, and readiness require eventing release evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("venue scheduling, seating, credentials, staffing, concessions, alcohol, incident command, evacuation, field readiness, changeover, systems, weather, command actions, assistant drafts, release evidence, drills, certifications, vendors, arrivals, tenancy, and readiness require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk venue actions require separated approval for curfews, seat holds, accessibility changes, credentials, alcohol, incident command, evacuation, field readiness, changeovers, systems, weather, release packs, drills, certifications, vendors, arrivals, tenant visibility, and go-live gates")
    if number in _ASSISTANT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("venue assistant skills must cite source records, preserve unknowns, prepare governed drafts only, and remain approval-gated before CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("calendar analysis, changeover warnings, conflict simulation, seat holds, ingress/egress plans, crowd heatmaps, changeover critical path, run-of-show variance, weather scenarios, command UI, offline sync, assistant plans, dependency handling, release evidence, drills, tenant views, and readiness gates must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("ticketing, credentials, weather, safety, transit, parking, concessions, medical, broadcast, team, premium, vendor, settlement, tenant, certification, audit, policy, and KPI context must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != SPORTS_REQUIRED_EVENT_TOPIC:
        findings.append("sports venue eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in SPORTS_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary sports venue datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("sports venue controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_sports_venue_event_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in SPORTS_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in SPORTS_DECLARED_DEPENDENCIES)
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
        "required_event_topic": SPORTS_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": SPORTS_ALLOWED_DATABASE_BACKENDS,
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


def improve1_sports_venue_event_operations_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_sports_venue_event_operations_control(capability) for capability in SPORTS_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.sports-venue-event-operations-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": SPORTS_OWNED_TABLES,
        "declared_dependencies": SPORTS_DECLARED_DEPENDENCIES,
        "allowed_database_backends": SPORTS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": SPORTS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


SPORTS_VENUE_EVENT_OPERATIONS_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_sports_venue_event_operations_control(slug, payload))
    for capability in SPORTS_CAPABILITIES
}
