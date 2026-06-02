"""Executable improve1 controls for the Telecom Network Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    TELECOM_NETWORK_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    TELECOM_NETWORK_OPERATIONS_CONSUMED_EVENT_TYPES,
    TELECOM_NETWORK_OPERATIONS_OWNED_TABLES,
    TELECOM_NETWORK_OPERATIONS_REQUIRED_EVENT_TOPIC,
    TELECOM_NETWORK_OPERATIONS_RUNTIME_TABLES,
)

PBC_KEY = "telecom_network_operations"
EVENT_CONTRACT = "AppGen-X"
TELECOM_ALLOWED_DATABASE_BACKENDS = TELECOM_NETWORK_OPERATIONS_ALLOWED_DATABASE_BACKENDS
TELECOM_REQUIRED_EVENT_TOPIC = TELECOM_NETWORK_OPERATIONS_REQUIRED_EVENT_TOPIC
TELECOM_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in TELECOM_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in TELECOM_CAPABILITIES}
TELECOM_OWNED_TABLES = tuple(
    dict.fromkeys(
        TELECOM_NETWORK_OPERATIONS_OWNED_TABLES
        + TELECOM_NETWORK_OPERATIONS_RUNTIME_TABLES
        + tuple(f"telecom_network_operations_{capability.slug}_control" for capability in TELECOM_CAPABILITIES)
    )
)
TELECOM_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        TELECOM_NETWORK_OPERATIONS_CONSUMED_EVENT_TYPES
        + (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "AlarmRaised",
            "AlarmCleared",
            "PmCounterChanged",
            "InventoryDiscoveryChanged",
            "FieldEvidenceAttached",
            "DispatchStatusChanged",
            "CustomerNotificationQueued",
            "MaintenanceApprovalChanged",
            "CircuitProtectionSwitched",
            "SlaPolicyChanged",
            "DocumentReceived",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "market_id",
    "site_code",
    "network_element_id",
    "technology_domain",
    "severity",
    "operator_id",
    "evidence_references",
)
_FIELD_ROWS = """
1|site_hierarchy_id,parent_site,latitude,longitude,access_restriction,power_asset,dependent_cell_circuit_set
2|radio_identity_id,bts_id,sector_id,carrier_id,band,pci_psc_bcch,neighbor_relation_set
3|service_path_id,circuit_id,a_end,z_end,vlan_or_pseudowire,protection_group,route_diversity
4|fiber_route_id,cable_id,sheath,tube,strand,closure_id,splice_validation
5|alarm_catalog_id,vendor_code,normalized_family,perceived_severity,probable_cause,object_class,suppressibility_flag
6|correlation_rule_id,parent_cause,child_alarm_set,suppression_count,root_cause_confidence,raw_event_stream,audit_expansion
7|trouble_ticket_id,external_reference,severity,customer_impact,dispatch_status,boundary_state,owned_ticket_field_set
8|maintenance_window_id,planned_work_class,mop_version,rollback_plan,change_owner,freeze_status,dependent_scope
9|outage_lifecycle_id,outage_state,bridge_commander,restoration_eta,impacted_service_set,communication_milestone,reopen_evidence
10|sla_clock_id,clock_state,service_class,pause_reason,exclusion_reason,breach_forecast,audit_position
11|capacity_model_id,capacity_class,installed_capacity,reserved_capacity,used_capacity,forecast_capacity,emergency_headroom
12|kpi_catalog_id,kpi_name,technology,threshold,market_baseline,vendor_baseline,warning_state
13|degradation_warning_id,kpi_trend,minor_alarm_count,ticket_trend,risk_score,operator_feedback,evidence_citation
14|field_boundary_id,work_order_context,site_access_note,safety_prerequisite,equipment_needed,restoration_evidence,external_roster_block
15|inventory_boundary_id,operational_attribute,referenced_asset_id,finance_master_block,vendor_master_block,boundary_rejection
16|noc_queue_id,queue_type,market_filter,site_filter,severity_filter,aging_bucket,degraded_data_state
17|topology_ui_id,map_view,path_trace,fiber_diagram,rack_summary,drilldown_path,accessibility_state
18|site_detail_id,power_alarm,generator_state,battery_autonomy,access_restriction,active_ticket,recent_field_visit
19|war_room_id,commander,timeline,impacted_services,current_hypothesis,field_status,sla_countdown
20|planned_work_calendar_id,freeze_period,overlap_window,shared_circuit_conflict,fiber_activity_conflict,rollback_evidence,approval_state
21|alarm_triage_skill_id,source_alarm_set,correlation_logic,root_cause_draft,incident_draft,confirmation_required,blocked_action
22|ticket_summary_skill_id,ticket_history,recent_alarm_set,impacted_site_set,field_note_set,sla_position,next_action
23|planned_work_reviewer_skill_id,mop_reference,dependency_overlap,rollback_completeness,risky_object_set,mitigation,feedback_capture
24|outage_comms_skill_id,template_type,incident_fact_set,customer_advisory,restoration_update,approval_required,unsupported_claim_block
25|degradation_investigator_skill_id,kpi_drift,low_severity_alarm_set,repeat_ticket_set,recent_planned_work,hypothesis_rank,evidence_span
26|event_taxonomy_id,event_name,schema_version,payload_contract,originating_record,ui_queue_mapping,replay_contract
27|event_replay_id,event_order,duplicate_clear,late_kpi_change,ticket_callback,idempotency_key,snapshot_match
28|operational_timeline_id,timeline_object,event_order,actor,source_system,correction_event,immutable_history
29|impact_propagation_id,fault_object,affected_site_set,affected_cell_set,affected_circuit_set,service_case_set,sla_exposure_set
30|oss_boundary_id,connector_type,source_of_truth,owned_state,external_state,graceful_degradation,write_block
31|restoration_playbook_id,playbook_type,alternate_path,service_priority,operator_decision,sla_update,reroute_evidence
32|fiber_cut_playbook_id,route_segment,closure_candidate,dispatch_prerequisite,splice_step,optical_validation,soak_monitoring
33|power_environment_id,mains_state,generator_state,battery_autonomy,fuel_concern,hvac_alarm,access_denial
34|field_evidence_id,photo_reference,meter_reading,otdr_trace,replaced_part_reference,closure_note,warehouse_mutation_block
35|topology_search_id,query_type,site_result,cell_result,circuit_result,fiber_result,provenance
36|bulk_reconciliation_id,feed_type,missing_object,extra_object,mismatch,operator_decision,approval_audit
37|stale_inventory_control_id,stale_site,orphan_cell,unused_circuit,unreachable_fiber,last_seen,queue_filter
38|release_matrix_id,scenario_id,site_evidence,alarm_evidence,outage_evidence,ui_flow_evidence,event_trace
39|synthetic_incident_id,scenario_type,seed_topology,alarm_sequence,workbench_output,detail_output,replay_log
40|change_governance_id,approval_history,freeze_window,emergency_override,rollback_timeout,post_change_validation,audit_status
41|sla_forecast_id,outage_age,eta_confidence,customer_class,pending_field_step,time_to_breach,escalation_state
42|capacity_forecast_id,active_capacity,reserved_headroom,planned_add,borrowed_capacity,forecast_warning,alert_clearance
43|kpi_anomaly_id,baseline,deviation,market_seasonality,operator_confirmation,feedback_action,threshold_tuning
44|service_view_id,customer_service_class,underlying_fault_path,impact_count,role_visibility,summary_scope,internal_topology_block
45|dead_letter_workbench_id,failed_event_type,replay_state,quarantine_reason,blast_radius,operator_note,recovery_evidence
46|regional_rules_id,market_hierarchy,timezone,holiday_calendar,permit_restriction,response_rule,calendar_pause
47|least_privilege_id,role_name,view_topology,declare_outage,attach_evidence,approve_work,replay_event
48|document_intake_id,document_type,extracted_mop_step,rollback_criterion,rca_finding,field_outcome,source_span
49|dashboard_projection_id,projection_type,major_outage_count,breach_risk,mttr,chronic_market,raw_alarm_redaction
50|manifest_traceability_id,manifest_table,manifest_api,manifest_ui_fragment,manifest_event_contract,release_artifact,blocker_status
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    5: ("AlarmRaised", "AlarmCleared"),
    12: ("OperationalKpiChanged", "PmCounterChanged"),
    14: ("DispatchStatusChanged", "FieldEvidenceAttached"),
    23: ("MaintenanceApprovalChanged",),
    24: ("CustomerNotificationQueued",),
    26: ("AlarmRaised", "AlarmCleared", "OperationalKpiChanged"),
    30: ("InventoryDiscoveryChanged", "DispatchStatusChanged", "CustomerNotificationQueued"),
    31: ("CircuitProtectionSwitched",),
    34: ("FieldEvidenceAttached",),
    36: ("InventoryDiscoveryChanged",),
    40: ("MaintenanceApprovalChanged", "PolicyChanged"),
    41: ("SlaPolicyChanged",),
    48: ("DocumentReceived",),
    50: ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"),
}
_TOPOLOGY_INVENTORY_FEATURES = (1, 2, 3, 4, 11, 14, 15, 17, 18, 29, 30, 35, 36, 37, 44, 46, 49, 50)
_ALARM_OUTAGE_SLA_FEATURES = (5, 6, 7, 9, 10, 12, 13, 16, 19, 21, 22, 24, 25, 26, 27, 28, 41, 43, 45, 50)
_PLANNED_FIELD_RESTORATION_FEATURES = (8, 20, 23, 31, 32, 33, 34, 39, 40, 47, 48, 50)
_GOVERNANCE_RELEASE_FEATURES = (26, 27, 28, 30, 36, 38, 39, 40, 42, 45, 46, 47, 49, 50)
_AGENT_FEATURES = (21, 22, 23, 24, 25, 48, 50)
_HUMAN_CONFIRMATION_FEATURES = (6, 8, 9, 20, 21, 23, 24, 25, 31, 32, 34, 36, 40, 45, 48, 50)
_APPROVAL_REQUIRED_FEATURES = (8, 9, 20, 23, 24, 31, 32, 34, 40, 47, 48, 50)
_NON_MUTATING_FEATURES = (13, 17, 21, 22, 23, 24, 25, 29, 31, 32, 35, 36, 37, 38, 39, 41, 42, 43, 44, 49, 50)
_PROJECTION_ONLY_FEATURES = (14, 30, 34, 44, 49)


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
        "tables": (f"telecom_network_operations_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"TelecomNetworkOperations{_camel(capability.slug)}Panel",
        "route": f"POST /telecom-network-operations/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in TELECOM_CAPABILITIES}


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
        "event_topic": TELECOM_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "topology_inventory_evidence_complete": True,
        "alarm_outage_sla_evidence_complete": True,
        "planned_field_restoration_evidence_complete": True,
        "governance_release_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned telecom model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _TOPOLOGY_INVENTORY_FEATURES and payload.get("topology_inventory_evidence_complete") is not True:
        findings.append("topology and inventory evidence is required for sites, radio, circuits, fiber, capacity, field boundary, inventory boundary, topology UI, site detail, impact propagation, OSS boundaries, search, reconciliation, stale topology, service views, regional rules, dashboards, and manifest proof")
    if number in _ALARM_OUTAGE_SLA_FEATURES and payload.get("alarm_outage_sla_evidence_complete") is not True:
        findings.append("alarm, outage, trouble ticket, KPI, SLA, event ordering, timeline, dead-letter, war room, and telecom assistant evidence is required")
    if number in _PLANNED_FIELD_RESTORATION_FEATURES and payload.get("planned_field_restoration_evidence_complete") is not True:
        findings.append("planned work, field evidence, restoration playbook, fiber cut, power/environment, synthetic incidents, change governance, least privilege, document intake, and manifest proof evidence is required")
    if number in _GOVERNANCE_RELEASE_FEATURES and payload.get("governance_release_evidence_complete") is not True:
        findings.append("telecom event taxonomy, idempotency, timeline, integration boundaries, reconciliation, release matrix, scenario library, change governance, capacity forecast, dead-letter, regional rules, least privilege, dashboards, and manifest traceability require governance release evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("alarm suppression, planned work, outage declaration, agent drafts, reroute, fiber restoration, field evidence, reconciliation, change governance, replay, document intake, and release gates require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-impact NOC actions require separated approval for planned work, outage control, communications, restoration, field evidence, change overrides, least privilege, document intake, and release gates")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("telecom assistant skills must cite alarms, KPIs, tickets, topology, MOP/RCA evidence, show reversible previews, and block direct writes before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("degradation risk, topology views, assistant skills, impact propagation, playbooks, search, reconciliation, stale controls, release matrices, scenario replay, SLA/capacity/KPI forecasts, service views, dashboards, and manifest gates must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("field dispatch, OSS discovery, customer notification, external account, and executive dashboard context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != TELECOM_REQUIRED_EVENT_TOPIC:
        findings.append("telecom network operations eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in TELECOM_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary telecom network operations datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("telecom network operations controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_telecom_network_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in TELECOM_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in TELECOM_DECLARED_DEPENDENCIES)
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
        "required_event_topic": TELECOM_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": TELECOM_ALLOWED_DATABASE_BACKENDS,
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


def improve1_telecom_network_operations_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_telecom_network_operations_control(capability) for capability in TELECOM_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.telecom_network_operations.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": TELECOM_OWNED_TABLES,
        "allowed_database_backends": TELECOM_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": TELECOM_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": TELECOM_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


TELECOM_NETWORK_OPERATIONS_CONTROL_FUNCTIONS = (
    "evaluate_telecom_network_operations_control",
    "improve1_telecom_network_operations_control_contract",
    "sample_payload_for",
)
