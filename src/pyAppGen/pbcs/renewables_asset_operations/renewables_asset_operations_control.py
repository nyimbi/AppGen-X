"""Executable improve1 controls for the Renewables Asset Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    RENEWABLES_ASSET_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    RENEWABLES_ASSET_OPERATIONS_CONSUMED_EVENT_TYPES,
    RENEWABLES_ASSET_OPERATIONS_OWNED_TABLES,
    RENEWABLES_ASSET_OPERATIONS_REQUIRED_EVENT_TOPIC,
    RENEWABLES_ASSET_OPERATIONS_RUNTIME_TABLES,
)

PBC_KEY = "renewables_asset_operations"
EVENT_CONTRACT = "AppGen-X"
RENEWABLES_ALLOWED_DATABASE_BACKENDS = RENEWABLES_ASSET_OPERATIONS_ALLOWED_DATABASE_BACKENDS
RENEWABLES_REQUIRED_EVENT_TOPIC = RENEWABLES_ASSET_OPERATIONS_REQUIRED_EVENT_TOPIC
RENEWABLES_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in RENEWABLES_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in RENEWABLES_CAPABILITIES}
RENEWABLES_OWNED_TABLES = tuple(
    dict.fromkeys(
        RENEWABLES_ASSET_OPERATIONS_OWNED_TABLES
        + RENEWABLES_ASSET_OPERATIONS_RUNTIME_TABLES
        + tuple(f"renewables_asset_operations_{capability.slug}_control" for capability in RENEWABLES_CAPABILITIES)
    )
)
RENEWABLES_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        RENEWABLES_ASSET_OPERATIONS_CONSUMED_EVENT_TYPES
        + (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "WeatherResourceUpdated",
            "MarketDispatchInstructionReceived",
            "GridOutageDeclared",
            "ScadaTelemetryCorrected",
            "RevenueMeterTrueUpReceived",
            "WarrantyDocumentStored",
            "OemServiceBulletinPublished",
            "ContractorQualificationUpdated",
            "SparePartAvailabilityChanged",
            "EnvironmentalPermitChanged",
            "PpaSettlementPeriodClosed",
            "SafetyPermitIssued",
            "InspectionMediaStored",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "fleet_id",
    "site_id",
    "asset_id",
    "technology_type",
    "operator_id",
    "operating_interval",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|hierarchy_node_id,parent_asset_id,oem,model,serial_number,commissioning_date,nameplate_capacity
2|availability_view_id,denominator_type,technical_availability,contractual_availability,grid_adjusted_availability,energy_based_availability,exclusion_basis
3|telemetry_boundary_id,signal_name,source_system,rollup_policy,correction_policy,lineage_hash,true_up_version
4|inverter_block_id,irradiance_adjusted_opportunity,actual_ac_output,clipping_loss,soiling_loss,temperature_loss,work_order_link
5|turbine_id,fault_code,power_curve_deviation,yaw_error,icing_suspicion,wake_peer_group,loss_classification
6|storage_unit_id,state_of_energy,dispatch_instruction,charge_mwh,discharge_mwh,cycle_count,degradation_threshold
7|meter_hierarchy_id,check_meter,plant_meter,poi_meter,sub_meter_rollup,tolerance_breach,approved_adjustment
8|curtailment_event_id,initiator,instruction_source,mw_requested,mw_delivered,recoverability,compensation_status
9|exclusion_id,reason_code,attachment_requirement,approver_role,reopen_rule,period_lock_state,monthly_pack_impact
10|ppa_obligation_id,contract_milestone,availability_guarantee,energy_guarantee,notice_period,ld_trigger,settlement_evidence_due
11|warranty_trigger_id,warranty_term,response_obligation,fault_recurrence_count,outage_duration,oem_notification_deadline,claim_bundle
12|work_priority_id,asset_criticality,mw_at_risk,fault_persistence,spares_constraint,weather_window,crew_access_constraint
13|inspection_program_id,inspection_template,photo_capture,defect_classification,geo_stamp,follow_on_action,inspection_packet
14|vegetation_zone_id,growth_survey,mowing_cycle,herbicide_rule,row_access_constraint,shading_loss,production_impact
15|cleaning_strategy_id,soiling_indicator,water_constraint,crew_window,expected_recovery,post_cleaning_verification,defer_reason
16|resource_normalization_id,irradiance,wind_speed,ambient_temperature,weather_quality_flag,expected_output,diagnostic_shift
17|incident_correlation_id,alarm_family,time_window,production_impact,duplicate_alarm_count,incident_case_id,traceability_state
18|interconnect_asset_id,asset_class,outage_class,feeder_id,relay_id,protection_system,maintenance_dependency
19|grid_instruction_id,dispatch_cap,restart_permission,restoration_notice,classification_path,contractual_impact,instruction_evidence
20|spare_readiness_id,critical_spare,repair_depot,cannibalization_decision,long_lead_risk,temporary_restriction,outage_forecast
21|permit_to_work_id,job_hazard_analysis,switching_approval,access_authorization,high_voltage_flag,start_owner,end_owner
22|loto_remote_reset_id,loto_status,remote_reset_restriction,field_presence_indicator,dual_confirmation,restore_asset_id,audit_record
23|contractor_competency_id,contractor_id,training_expiry,authorized_task_class,site_induction,assignment_decision,scope_evidence
24|inspection_media_id,media_type,defect_tag,asset_link,inspection_route,follow_up_work,corrective_action_verification
25|operational_event_id,event_type,idempotency_key,downstream_projection,consumer_contract,replay_key,dead_letter_policy
26|ingestion_id,source_system,event_version,interval_key,merge_rule,malformed_replay_reason,idempotency_result
27|data_quality_scorecard_id,telemetry_completeness,meter_reconciliation_success,inspection_timeliness,exception_age,attachment_completeness,report_block_state
28|performance_ratio_id,weather_deviation,outage_loss,curtailment_loss,clipping_loss,soiling_loss,residual_loss
29|wind_analytics_id,power_curve_reference,yaw_misalignment_score,turbulence_context,icing_probability,peer_rank,corrective_action
30|storage_efficiency_id,charge_acceptance,discharge_delivery,auxiliary_consumption,round_trip_efficiency,market_window,missed_dispatch_code
31|rca_workflow_id,anomaly_id,candidate_cause,excluded_alternative,owner,corrective_action,recovery_verification
32|counterfactual_simulation_id,scenario_name,alternative_dispatch_limit,restoration_assumption,maintenance_timing,energy_delta,compensation_use_case
33|seasonal_plan_id,season,outage_window,vegetation_cycle,blade_campaign,cleaning_campaign,peak_generation_conflict
34|environmental_evidence_id,spill_incident,waste_handling,water_usage,habitat_constraint,ghg_impact,permit_task
35|responsibility_split_id,issue_type,warranty_clause,ltsa_scope,om_scope,owner_capex_flag,notification_deadline
36|financial_exposure_id,lost_energy_mwh,settlement_impact,ppa_ld_exposure,warranty_recovery_value,spare_cost_risk,outage_cost_scenario
37|geospatial_workbench_id,map_layer,map_pin,asset_geometry,road_access,incident_filter,detail_link
38|shift_handover_id,shift_window,alarm_summary,curtailment_summary,grid_instruction_summary,open_hold,acknowledgement_state
39|mobile_offline_id,cached_asset_context,photo_capture,barcode_scan,deferred_sync,conflict_resolution,offline_packet_status
40|assistant_skill_id,diagnosis_preview,curtailment_classification,availability_pack,warranty_packet,spare_suggestion,human_confirmation
41|document_understanding_id,document_type,source_span,maintenance_interval,response_obligation,cure_period,reviewable_task
42|federated_event_id,upstream_event_type,event_version,lineage_trace,downstream_action,workbench_state_change,contract_test
43|release_scenario_id,scenario_type,scenario_stage,owned_schema_evidence,service_event_evidence,ui_agent_evidence,governance_evidence
44|continuous_control_id,control_type,separation_of_duties,required_attachment,period_lock_approval,safety_hold_enforcement,lineage_completeness
45|tenant_segmentation_id,owner_scope,site_calendar,safety_procedure,document_library,approval_chain,isolation_result
46|oem_extension_id,oem_field,typed_definition,compatibility_check,ui_render_rule,event_version_note,audit_scope
47|bulk_correction_id,gap_type,preview_delta,apply_reason,rollback_token,approver_identity,corrected_dataset_hash
48|exception_queue_id,queue_type,sla_hours,owner,age_bucket,closure_evidence,risk_state
49|fixture_catalog_id,fixture_type,scenario_matrix,happy_path,edge_case,verification_surface,release_usage
50|readiness_dashboard_id,telemetry_integrity,event_health,critical_exception_count,safety_control_pass_rate,scenario_coverage,go_live_gate
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    3: ("ScadaTelemetryCorrected", "RevenueMeterTrueUpReceived"),
    7: ("RevenueMeterTrueUpReceived",),
    10: ("PpaSettlementPeriodClosed",),
    11: ("WarrantyDocumentStored", "OemServiceBulletinPublished"),
    12: ("SparePartAvailabilityChanged",),
    16: ("WeatherResourceUpdated",),
    19: ("GridOutageDeclared", "MarketDispatchInstructionReceived"),
    20: ("SparePartAvailabilityChanged",),
    21: ("SafetyPermitIssued",),
    23: ("ContractorQualificationUpdated",),
    24: ("InspectionMediaStored",),
    32: ("MarketDispatchInstructionReceived", "WeatherResourceUpdated"),
    34: ("EnvironmentalPermitChanged",),
    41: ("WarrantyDocumentStored",),
    42: ("WeatherResourceUpdated", "MarketDispatchInstructionReceived", "GridOutageDeclared"),
    46: ("OemServiceBulletinPublished",),
}
_HUMAN_CONFIRMATION_FEATURES = (7, 8, 9, 10, 11, 12, 19, 20, 21, 22, 23, 32, 34, 35, 36, 40, 41, 44, 46, 47, 50)
_APPROVAL_REQUIRED_FEATURES = (2, 7, 8, 9, 10, 11, 19, 21, 22, 23, 32, 34, 35, 36, 44, 45, 46, 47, 50)
_NON_MUTATING_FEATURES = (1, 2, 3, 4, 5, 6, 7, 9, 12, 16, 17, 19, 20, 25, 26, 27, 28, 29, 30, 31, 32, 33, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50)
_AI_PREVIEW_FEATURES = (17, 27, 31, 32, 35, 36, 40, 41, 43, 47, 50)
_SAFETY_CONTROL_FEATURES = (13, 18, 19, 20, 21, 22, 23, 24, 31, 34, 38, 39, 44, 48, 50)
_PERFORMANCE_CONTROL_FEATURES = (2, 4, 5, 6, 7, 8, 14, 15, 16, 28, 29, 30, 31, 32, 36, 49, 50)
_COMMERCIAL_CONTROL_FEATURES = (7, 8, 9, 10, 11, 15, 19, 32, 35, 36, 41, 43, 50)
_PROJECTION_ONLY_FEATURES = (3, 7, 10, 11, 12, 16, 19, 20, 21, 23, 24, 32, 34, 41, 42, 46)


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
        "tables": (f"renewables_asset_operations_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"RenewablesAssetOperations{_camel(capability.slug)}Panel",
        "route": f"POST /renewables-asset-operations/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in RENEWABLES_CAPABILITIES}


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
        "event_topic": RENEWABLES_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "safety_evidence_complete": True,
        "performance_evidence_complete": True,
        "commercial_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned renewables model, UI, service/API, event, agent, test, and release evidence before approval.")
    if number in _SAFETY_CONTROL_FEATURES and payload.get("safety_evidence_complete") is not True:
        findings.append("site inspections, interconnect assets, grid instructions, spares, permit-to-work, lockout/tagout, contractor competency, inspection media, RCA, environmental evidence, handover, mobile field work, controls, queues, and go-live require safety evidence")
    if number in _PERFORMANCE_CONTROL_FEATURES and payload.get("performance_evidence_complete") is not True:
        findings.append("availability, solar, wind, storage, meter reconciliation, curtailment, vegetation, cleaning, normalization, performance ratio, analytics, RCA, simulations, commercial exposure, fixtures, and readiness require performance evidence")
    if number in _COMMERCIAL_CONTROL_FEATURES and payload.get("commercial_evidence_complete") is not True:
        findings.append("meter reconciliation, curtailment, exclusions, PPA obligations, warranty triggers, cleaning economics, grid classification, simulations, responsibility splits, financial exposure, document obligations, release scenarios, and go-live require commercial evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("meter adjustments, curtailment classifications, exclusions, PPA milestones, warranty claims, critical work, grid instructions, spares, permits, remote reset, contractor assignment, simulations, environmental evidence, responsibility splits, financial exposure, assistant actions, document-derived tasks, continuous controls, OEM extensions, bulk corrections, and go-live require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("availability formulas, meter corrections, curtailment, exclusions, PPA settlements, warranties, grid/safety decisions, contractor eligibility, simulations, environmental tasks, responsibility, financial exposure, controls, tenant isolation, OEM extensions, corrections, and readiness require separated approval")
    if number in _AI_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("renewables agent skills must be evidence-cited, permission-checked, and preview-only until confirmed by operations staff")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("asset hierarchy, availability formulas, telemetry boundaries, analytics, reconciliations, planning, scorecards, RCA, simulations, maps, handovers, assistant/document understanding, federation, release evidence, controls, segmentation, schema extensions, corrections, queues, fixtures, and readiness must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("SCADA, revenue meter, PPA, warranty, weather, grid, market, spare, safety, contractor, inspection media, environmental, OEM, audit, policy, and KPI facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != RENEWABLES_REQUIRED_EVENT_TOPIC:
        findings.append("renewables asset operations eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in RENEWABLES_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary renewables datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("renewables controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_renewables_asset_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in RENEWABLES_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in RENEWABLES_DECLARED_DEPENDENCIES)
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
        "required_event_topic": RENEWABLES_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": RENEWABLES_ALLOWED_DATABASE_BACKENDS,
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


def improve1_renewables_asset_operations_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_renewables_asset_operations_control(capability) for capability in RENEWABLES_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.renewables-asset-operations-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": RENEWABLES_OWNED_TABLES,
        "declared_dependencies": RENEWABLES_DECLARED_DEPENDENCIES,
        "allowed_database_backends": RENEWABLES_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": RENEWABLES_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


RENEWABLES_ASSET_OPERATIONS_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_renewables_asset_operations_control(slug, payload))
    for capability in RENEWABLES_CAPABILITIES
}
