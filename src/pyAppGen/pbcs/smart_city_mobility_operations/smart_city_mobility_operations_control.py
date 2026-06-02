"""Executable improve1 controls for the Smart City Mobility Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    SMART_CITY_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    SMART_CITY_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES,
    SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES,
    SMART_CITY_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC,
    SMART_CITY_MOBILITY_OPERATIONS_RUNTIME_TABLES,
)

PBC_KEY = "smart_city_mobility_operations"
EVENT_CONTRACT = "AppGen-X"
MOBILITY_ALLOWED_DATABASE_BACKENDS = SMART_CITY_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS
MOBILITY_REQUIRED_EVENT_TOPIC = SMART_CITY_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC
MOBILITY_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in MOBILITY_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in MOBILITY_CAPABILITIES}
MOBILITY_OWNED_TABLES = tuple(
    dict.fromkeys(
        SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES
        + SMART_CITY_MOBILITY_OPERATIONS_RUNTIME_TABLES
        + tuple(f"smart_city_mobility_operations_{capability.slug}_control" for capability in MOBILITY_CAPABILITIES)
    )
)
MOBILITY_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        SMART_CITY_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES
        + (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "TransitVehiclePositionUpdated",
            "TransitServiceDisrupted",
            "ParkingOccupancyObserved",
            "CurbSensorObserved",
            "SignalControllerStatusChanged",
            "EmergencyVehiclePreemptionRequested",
            "MicromobilityOperatorFeedUpdated",
            "WeatherAlertIssued",
            "PublicAlertDeliveryStatusChanged",
            "MajorEventSchedulePublished",
            "ConstructionPermitChanged",
            "SchoolCalendarChanged",
            "FreightPermitChanged",
            "AccessibilityAssetOutageReported",
            "EnvironmentalSensorObserved",
            "PrivacyPolicyChanged",
            "AgencyDataSharingAgreementChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "agency_id",
    "district_id",
    "corridor_id",
    "jurisdiction_id",
    "policy_version",
    "operating_window",
    "evidence_references",
)
_FIELD_ROWS = """
1|corridor_registry_id,directional_segment,functional_class,target_operating_objective,linked_transit_service,linked_signal_plan,orphan_segment_check
2|baseline_id,weekday_pattern,peak_window,event_window,weather_regime,kpi_name,baseline_value
3|intersection_registry_id,approach_id,movement_id,lane_group,ped_crossing,bike_crossing,control_type
4|timing_version_id,cycle_length,phase_split,offset,clearance_interval,pedestrian_timing,engineer_signoff
5|tsp_rule_pack_id,eligible_route,lateness_threshold,occupancy_threshold,green_extension_limit,blackout_condition,simulation_result
6|preemption_policy_id,preemption_event_id,conflict_resolution_order,pedestrian_phase_rule,railroad_preemption_rule,recovery_plan,trace_classification
7|accessibility_timing_id,walk_interval,flashing_clearance,leading_ped_interval,audible_status,tactile_confirmation,detour_instruction
8|micromobility_geofence_id,slow_zone,no_ride_zone,no_parking_zone,sidewalk_conflict_zone,parking_corral,revision_status
9|bike_conflict_monitor_id,bike_crossing_movement,turn_phase,curb_loading_window,near_miss_incident,hotspot_score,remediation_task
10|curb_inventory_id,block_face_id,zone_use_type,time_band,user_class,restriction_set,overlap_check
11|dynamic_curb_window_id,effective_date,time_band,recurrence_pattern,event_override,fallback_mode,transition_preview
12|loading_compliance_id,planned_dwell,observed_dwell,vehicle_class,block_face_occupancy,repeat_violator,obstruction_mode
13|parking_turnover_id,asset_type,occupancy_rate,turnover_rate,overstay_count,payment_compliance,spillover_zone
14|accessible_parking_control_id,designated_space_count,field_status,obstruction_incident,permit_restriction,availability_result,exception_state
15|parking_guidance_id,destination_context,occupancy_filter,curb_restriction_filter,event_closure_filter,accessibility_filter,recommendation_result
16|incident_taxonomy_id,taxonomy_code,response_playbook,severity_mapping,legacy_category_map,kpi_rollup_code,approval_state
17|incident_lifecycle_id,detected_at,verified_at,dispatched_at,mitigated_at,lane_cleared_at,post_review_outcome
18|planned_disruption_id,disruption_type,affected_corridor_set,linked_signal_change,linked_curb_change,public_alert_plan,rollback_test
19|congestion_heatmap_id,direction,time_window,travel_time_metric,queue_metric,reliability_metric,sensor_gap_flag
20|bottleneck_correlation_id,delay_spike,signal_contributor,curb_contributor,parking_contributor,incident_contributor,evidence_rank
21|feed_registry_id,feed_type,feed_owner,cadence,schema_version,freshness_sla,failure_impact
22|feed_quality_id,freshness_score,completeness_score,schema_conformity,geospatial_plausibility,clock_skew,quarantine_decision
23|sensor_fusion_id,source_sensor_set,derived_metric,provenance_set,confidence_score,degraded_source_set,fusion_result
24|stop_congestion_id,route_id,stop_id,boarding_delay,blocked_boarding_flag,lift_deployment_issue,disruption_explanation
25|headway_recovery_id,route_id,planned_headway,live_spacing,bunching_threshold,recommended_intervention,approval_state
26|school_zone_policy_id,school_calendar_state,crossing_window,loading_restriction,speed_display_rule,parent_pickup_spillover,override_result
27|freight_governance_id,preferred_loading_window,restricted_turn,oversized_vehicle_constraint,curb_reservation,peak_period_rule,simulation_impact
28|accessibility_disruption_id,path_outage_type,alternative_path,public_alert_reference,closure_exemption,assistant_summary,closeout_evidence
29|emissions_estimate_id,vehicle_class,speed_profile,delay_seconds,dwell_seconds,queue_length,emissions_delta
30|spillback_detection_id,low_speed_duration,upstream_intersection,stop_blockage,loading_obstruction,estimated_duration,likely_source
31|alert_template_id,template_type,language_code,channel_type,severity_rule,length_rule,approval_history
32|alert_trigger_id,trigger_geography,route_or_stop,confidence_threshold,feed_quality_state,false_positive_suppression,send_decision
33|command_view_id,pinned_corridor,layout_mode,issue_badge_set,permission_scope,map_to_record_navigation,drilldown_state
34|intersection_detail_id,active_timing_plan,detector_health,recent_override,ped_accessibility_setting,nearby_incident,recovery_action
35|incident_playbook_skill_id,playbook_type,cited_incident,cited_signal_plan,cited_transit_service,detour_message,approval_flow
36|retiming_review_skill_id,parameter_diff,corridor_goal_assessment,accessibility_constraint,queue_risk,transit_priority_interaction,required_approver
37|event_taxonomy_id,domain_event_type,schema_version,event_example,legacy_compatibility,replay_category,outbox_test
38|projection_replay_id,projection_name,replay_run_id,drift_threshold,corrupted_fixture,drift_result,exception_reference
39|parameter_set_id,jurisdiction_scope,season_scope,event_profile,corridor_class,staged_rollout_state,rollback_token
40|modal_priority_rule_id,competing_mode_set,precedence_rule,ped_delay_guardrail,bike_protection_guardrail,bus_reliability_target,winning_rule
41|scenario_simulation_id,event_type,attendance_surge,road_closure_set,temporary_transit_plan,alert_plan,kpi_delta
42|weather_playbook_id,weather_trigger,threshold_value,response_task,alert_template,escalation_criteria,clear_down_criteria
43|shift_handoff_id,handoff_timestamp,active_corridor_summary,unresolved_incident_set,fragile_feed_set,pending_approval_set,watchlist_closure_state
44|equity_lens_id,geography_segment,vulnerability_marker,delay_delta,parking_pressure_delta,safety_conflict_delta,policy_simulation_result
45|privacy_control_id,identifier_classification,hashing_policy,retention_rule,masking_rule,export_permission,purge_result
46|tenant_isolation_id,agency_scope,district_scope,record_isolation_result,projection_isolation_result,assistant_permission_scope,shared_event_metadata
47|continuous_control_id,control_family,signal_approval_check,accessibility_field_check,feed_quarantine_check,replay_integrity_check,exception_created
48|release_pack_id,change_class,planned_scope,approval_set,simulation_result,rollback_plan,post_release_window
49|observation_rollback_id,change_type,observation_window,success_threshold,rollback_threshold,outcome_state,rollback_readiness
50|go_live_scorecard_id,feed_readiness_score,control_status_score,assistant_evaluation_score,ui_completeness_score,event_schema_score,evidence_completeness_score
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    2: ("OperationalKpiChanged", "WeatherAlertIssued"),
    5: ("TransitVehiclePositionUpdated",),
    6: ("EmergencyVehiclePreemptionRequested",),
    8: ("MicromobilityOperatorFeedUpdated",),
    12: ("CurbSensorObserved",),
    13: ("ParkingOccupancyObserved",),
    15: ("ParkingOccupancyObserved",),
    18: ("MajorEventSchedulePublished", "ConstructionPermitChanged"),
    21: ("TransitVehiclePositionUpdated", "ParkingOccupancyObserved", "SignalControllerStatusChanged"),
    26: ("SchoolCalendarChanged",),
    27: ("FreightPermitChanged",),
    28: ("AccessibilityAssetOutageReported",),
    29: ("EnvironmentalSensorObserved",),
    31: ("PolicyChanged",),
    32: ("PublicAlertDeliveryStatusChanged",),
    34: ("SignalControllerStatusChanged",),
    37: ("AuditEventSealed",),
    42: ("WeatherAlertIssued",),
    45: ("PrivacyPolicyChanged",),
    46: ("AgencyDataSharingAgreementChanged",),
}
_CORRIDOR_SIGNAL_FEATURES = (1, 2, 3, 4, 5, 6, 7, 19, 20, 25, 33, 34, 36, 40, 48, 49, 50)
_CURB_PARKING_FEATURES = (8, 10, 11, 12, 13, 14, 15, 27, 30, 48, 49, 50)
_INCIDENT_ALERT_FEATURES = (16, 17, 18, 28, 31, 32, 35, 42, 43, 47, 48, 49, 50)
_DATA_FEED_FEATURES = (21, 22, 23, 24, 29, 30, 37, 38, 47, 50)
_GOVERNANCE_FEATURES = (4, 5, 6, 7, 11, 14, 18, 25, 26, 27, 28, 31, 36, 39, 40, 41, 44, 45, 46, 47, 48, 49, 50)
_ASSISTANT_FEATURES = (9, 20, 25, 28, 35, 36, 41, 42, 44, 50)
_HUMAN_CONFIRMATION_FEATURES = (4, 5, 6, 7, 11, 14, 18, 25, 26, 27, 28, 31, 35, 36, 40, 41, 42, 45, 47, 48, 49, 50)
_APPROVAL_REQUIRED_FEATURES = (4, 5, 6, 7, 11, 14, 18, 25, 26, 27, 31, 36, 39, 40, 41, 45, 46, 48, 49, 50)
_NON_MUTATING_FEATURES = (2, 5, 9, 15, 19, 20, 22, 23, 25, 29, 30, 32, 35, 36, 38, 40, 41, 44, 47, 48, 49, 50)
_PROJECTION_ONLY_FEATURES = (2, 5, 6, 8, 12, 13, 15, 18, 21, 22, 23, 26, 27, 28, 29, 32, 34, 42, 45, 46)


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
        "tables": (f"smart_city_mobility_operations_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"SmartCityMobilityOperations{_camel(capability.slug)}Panel",
        "route": f"POST /smart-city-mobility-operations/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in MOBILITY_CAPABILITIES}


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
        "event_topic": MOBILITY_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "corridor_signal_evidence_complete": True,
        "curb_parking_evidence_complete": True,
        "incident_alert_evidence_complete": True,
        "data_feed_evidence_complete": True,
        "governance_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned mobility model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _CORRIDOR_SIGNAL_FEATURES and payload.get("corridor_signal_evidence_complete") is not True:
        findings.append("corridor registry, baselines, intersections, timing, priority, preemption, accessibility timing, congestion, bottlenecks, headways, command views, retiming review, modal priority, release packs, rollback, and go-live scorecards require corridor signal evidence")
    if number in _CURB_PARKING_FEATURES and payload.get("curb_parking_evidence_complete") is not True:
        findings.append("micromobility geofences, curb inventory, dynamic windows, loading dwell, parking turnover, accessible parking, guidance, freight routes, spillback, release packs, rollback, and go-live scorecards require curb parking evidence")
    if number in _INCIDENT_ALERT_FEATURES and payload.get("incident_alert_evidence_complete") is not True:
        findings.append("incident taxonomy, clearance lifecycle, planned events, accessibility outages, alert templates, alert triggers, incident playbooks, weather playbooks, handoffs, controls, release packs, rollback, and scorecards require incident alert evidence")
    if number in _DATA_FEED_FEATURES and payload.get("data_feed_evidence_complete") is not True:
        findings.append("feed registry, feed quality, sensor fusion, stop congestion, emissions, spillback, event taxonomy, replay drift, controls, and scorecards require data feed evidence")
    if number in _GOVERNANCE_FEATURES and payload.get("governance_evidence_complete") is not True:
        findings.append("signal approvals, priority guardrails, preemption, accessibility, curb windows, parking integrity, planned disruptions, headway interventions, school/freight/accessibility policies, alerts, retiming, parameters, modal priorities, scenarios, equity, privacy, tenancy, controls, release packs, rollback, and go-live scorecards require governance evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("safety-critical timing, priority, preemption, accessibility, curb changes, parking availability, planned events, headway interventions, school/freight/accessibility disruptions, alerts, assistant recommendations, scenarios, privacy, controls, release packs, rollback, and go-live require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk mobility changes require separated approval for signal timing, transit priority, preemption, accessibility, dynamic curb windows, parking integrity, planned events, headway controls, school/freight rules, alerts, retiming review, parameters, modal priorities, scenarios, privacy, tenant isolation, release packs, rollback, and go-live gates")
    if number in _ASSISTANT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("mobility assistant skills must cite operational records, preview impacts, prepare governed updates only, and remain approval-gated before CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("baselines, simulations, heatmaps, correlation, feed quality, fusion, headway, emissions, spillback, alerts, assistant reviews, replay, modal priority, scenarios, equity, controls, release packs, rollback, and scorecards must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("transit, parking, curb, signal, emergency, micromobility, weather, event, construction, school, freight, accessibility, environmental, privacy, agency, audit, and KPI facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != MOBILITY_REQUIRED_EVENT_TOPIC:
        findings.append("smart city mobility eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in MOBILITY_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary smart city mobility datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("smart city mobility controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_smart_city_mobility_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in MOBILITY_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in MOBILITY_DECLARED_DEPENDENCIES)
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
        "required_event_topic": MOBILITY_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": MOBILITY_ALLOWED_DATABASE_BACKENDS,
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


def improve1_smart_city_mobility_operations_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_smart_city_mobility_operations_control(capability) for capability in MOBILITY_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.smart-city-mobility-operations-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": MOBILITY_OWNED_TABLES,
        "declared_dependencies": MOBILITY_DECLARED_DEPENDENCIES,
        "allowed_database_backends": MOBILITY_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": MOBILITY_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


SMART_CITY_MOBILITY_OPERATIONS_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_smart_city_mobility_operations_control(slug, payload))
    for capability in MOBILITY_CAPABILITIES
}
