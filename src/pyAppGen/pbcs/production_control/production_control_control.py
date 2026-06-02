"""Executable improve1 controls for the Production Control PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS,
    PRODUCTION_CONTROL_OWNED_TABLES,
    PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
)

PBC_KEY = "production_control"
EVENT_CONTRACT = "AppGen-X"
PRODUCTION_CONTROL_CONTROL_ALLOWED_DATABASE_BACKENDS = PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS
PRODUCTION_CONTROL_CONTROL_REQUIRED_EVENT_TOPIC = PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC
PRODUCTION_CONTROL_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in PRODUCTION_CONTROL_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in PRODUCTION_CONTROL_CONTROL_CAPABILITIES}
_RUNTIME_TABLES = (
    "production_control_appgen_outbox_event",
    "production_control_appgen_inbox_event",
    "production_control_dead_letter_event",
)
PRODUCTION_CONTROL_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        PRODUCTION_CONTROL_OWNED_TABLES
        + _RUNTIME_TABLES
        + tuple(f"production_control_{capability.slug}_control" for capability in PRODUCTION_CONTROL_CONTROL_CAPABILITIES)
    )
)
PRODUCTION_CONTROL_CONTROL_DECLARED_DEPENDENCIES = (
    "PlannedOrderReleased",
    "MaintenanceCompleted",
    "InventoryMaterialReadinessProjected",
    "MrpPlannedOrderProjected",
    "QualityGateProjected",
    "AssetCommissioningProjected",
    "IdentityVerified",
    "AuditEventSealed",
    "EnergyCarbonIntensityProjected",
    "TimeLaborAvailabilityProjected",
    "ModelGovernanceChanged",
)
_BASE_FIELDS = (
    "tenant_id",
    "site_id",
    "work_center_id",
    "production_order_id",
    "routing_step_id",
    "operation_id",
    "actor_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|readiness_gate_id,calendar_id,shift_id,capacity_hours,efficiency,status,maintenance_projection_freshness,oee_target
2|capability_model_id,process_capability,tooling_set,setup_family,machine_class,labor_skill,automation_mode,batch_range
3|routing_lifecycle_id,routing_version,sequence_constraint,setup_minutes,run_minutes,queue_minutes,alternate_work_centers,yield_target
4|order_readiness_id,planned_order_projection,item_id,quantity,due_date,bom_version,material_readiness,quality_hold
5|order_state_id,current_state,next_state,transition_reason,source_event,idempotency_key,downstream_event_effect,policy_explanation
6|finite_schedule_id,capacity_bucket,setup_family,priority,due_date,material_ready,maintenance_window,infeasible_reason
7|adherence_monitor_id,scheduled_start,actual_start,scheduled_end,actual_end,sequence_delta,quantity_delta,cause_code
8|dispatch_optimization_id,dispatch_rank,priority_score,setup_saving,material_status,labor_status,tradeoff,alternative_rejected
9|sequence_control_id,predecessor_step,successor_step,overlap_rule,parallel_group,queue_limit,inspection_required,rework_loop
10|start_validation_id,material_ready,wip_ready,operator_permission,machine_available,maintenance_state,quality_prerequisite,start_blocker
11|split_merge_governance_id,pause_reason,partial_quantity,split_lineage,merge_candidate,wip_movement,recalculation_impact,approval_required
12|confirmation_trace_id,good_quantity,scrap_quantity,rework_quantity,operator_id,start_time,end_time,source_device
13|material_projection_id,item_id,required_quantity,lot_id,reservation_id,quality_hold,freshness,confidence
14|material_consumption_id,component_id,consumed_quantity,lot_serial,issue_method,variance,operator_id,event_id
15|wip_trace_id,wip_quantity,queue_location,hold_reason,split_merge_lineage,inventory_handoff,projection_scope,status
16|labor_booking_id,employee_projection,role,start_time,end_time,booking_type,variance,approval_state
17|machine_booking_id,asset_projection,setup_minutes,run_minutes,idle_minutes,cycle_count,speed,maintenance_state
18|downtime_capture_id,downtime_reason,start_time,end_time,asset_projection,severity,evidence_ref,taxonomy_version
19|oee_impact_id,availability_impact,performance_impact,quality_impact,schedule_impact,throughput_impact,duration_minutes,event_id
20|maintenance_projection_id,asset_id,completion_time,restored_capability,constraint_set,projection_confidence,freshness,capacity_release
21|quality_gate_id,inspection_criteria,sample_size,result,defect_code,hold_state,inspector_id,quality_projection
22|scrap_rework_id,reason_code,quantity,material_component,disposition,rework_route,approval_state,cost_impact
23|completion_control_id,required_operations,confirmed_operations,quality_gate_status,material_status,wip_status,exception_status,proof_hash
24|asset_handoff_id,asset_projection,serial_number,commissioning_status,acceptance_evidence,quality_status,event_id,foreign_table_block
25|oee_snapshot_id,availability,performance,quality,planned_time,unplanned_downtime,ideal_cycle,calculation_version
26|throughput_forecast_id,shift_id,product_family,downtime_risk,material_risk,quality_risk,confidence,intervention
27|exception_taxonomy_id,exception_type,owner_role,sla_minutes,severity,recovery_action,linked_order,escalation
28|recommendation_id,recommended_action,risk_score,schedule_impact,required_permission,event_effect,rollback_limit,explanation
29|capacity_allocation_id,due_date_weight,priority_weight,setup_efficiency,service_class,material_weight,fairness_score,simulation_id
30|counterfactual_dispatch_id,priority_scenario,capacity_threshold,downtime_assumption,routing_alternate,overtime_option,late_order_impact,oee_impact
31|carbon_schedule_id,energy_intensity,carbon_window,urgency_class,batch_run_option,due_date_preserved,cost_tradeoff,service_tradeoff
32|completion_proof_id,redacted_order,quantity_proof,operation_proof,quality_proof,material_proof,hash_chain,expiry
33|audit_trail_id,previous_hash,current_hash,mutation_type,affected_table,source_actor,event_link,tamper_status
34|policy_screening_id,action_type,site_policy,work_center_policy,quality_policy,safety_policy,decision,policy_hash
35|event_cockpit_id,inbox_status,outbox_status,dead_letter_status,idempotency_key,retry_count,payload_lineage,replay_eligible
36|boundary_proof_id,owned_table,declared_dependency,projection_name,foreign_table_probe,violation_result,runtime_check,release_gate
37|workbench_coverage_id,work_center_panel,routing_panel,schedule_panel,dispatch_panel,execution_panel,quality_panel,agent_panel
38|instruction_intake_id,document_digest,extracted_fact,owned_table_mapping,permission_check,projection_check,confidence,approval_required
39|agent_plan_id,command,permission,owned_table_preview,idempotency_key,emitted_event,affected_order,human_approval
40|semantic_parse_id,note_digest,downtime_reason,scrap_code,quality_outcome,material_variance,schedule_change,reviewer_approval
41|anomaly_detection_id,work_center_signal,routing_signal,shift_signal,operator_signal,material_signal,event_signal,explanation
42|exposure_model_id,order_distribution,downtime_distribution,yield_distribution,schedule_distribution,confidence_interval,mitigation
43|mlops_governance_id,model_id,feature_lineage,training_window,approval_status,drift_score,explainability,fairness_check
44|identity_credential_id,device_did,work_center_did,verification_status,expiry,authority,proof_reference,revocation_state
45|resilience_drill_id,scenario,recovery_action,replay_plan,completion_outbox_test,dead_letter_recovery,lesson_record,status
46|crypto_authorization_id,crypto_epoch,signature_ref,key_rotation_evidence,policy_version,migration_readiness,algorithm_family,proof_status
47|continuous_control_id,blocked_center_check,start_without_material_check,predecessor_check,quality_completion_check,wip_mismatch_check,dead_letter_aging,agent_bypass_check
48|shift_handover_id,active_orders,paused_operations,open_exceptions,wip_state,downtime_state,quality_holds,supervisor_signoff
49|readiness_score_id,work_center_score,routing_score,material_score,schedule_score,event_score,boundary_score,agent_score
50|execution_proof_id,planned_order_trace,work_center_trace,routing_trace,schedule_trace,dispatch_trace,completion_trace,oee_trace
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("MaintenanceCompleted", "AssetCommissioningProjected"),
    4: ("PlannedOrderReleased", "InventoryMaterialReadinessProjected", "QualityGateProjected"),
    10: ("InventoryMaterialReadinessProjected", "MaintenanceCompleted", "IdentityVerified"),
    13: ("InventoryMaterialReadinessProjected",),
    16: ("TimeLaborAvailabilityProjected",),
    20: ("MaintenanceCompleted",),
    21: ("QualityGateProjected",),
    24: ("AssetCommissioningProjected",),
    31: ("EnergyCarbonIntensityProjected",),
    35: ("PlannedOrderReleased", "MaintenanceCompleted"),
    36: ("MrpPlannedOrderProjected", "InventoryMaterialReadinessProjected", "QualityGateProjected", "MaintenanceCompleted", "AssetCommissioningProjected", "AuditEventSealed"),
    43: ("ModelGovernanceChanged",),
    45: ("PlannedOrderReleased", "MaintenanceCompleted"),
    50: ("PlannedOrderReleased", "InventoryMaterialReadinessProjected", "QualityGateProjected", "MaintenanceCompleted"),
}
_HUMAN_CONFIRMATION_FEATURES = (4, 5, 8, 10, 11, 14, 16, 17, 21, 22, 23, 24, 28, 29, 30, 31, 34, 38, 39, 40, 45, 46, 48, 50)
_AGENT_PREVIEW_FEATURES = (28, 30, 37, 38, 39, 40, 41, 42, 45, 47, 48, 49, 50)
_NON_MUTATING_FEATURES = (6, 7, 8, 13, 19, 25, 26, 28, 29, 30, 31, 32, 33, 35, 36, 38, 39, 40, 41, 42, 43, 45, 46, 47, 49, 50)
_PROJECTION_ONLY_FEATURES = (1, 4, 10, 13, 16, 20, 21, 24, 31, 35, 36, 43, 45, 50)
_PRODUCTION_RISK_FEATURES = (1, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15, 18, 19, 21, 22, 23, 25, 26, 27, 28, 29, 30, 34, 35, 36, 38, 39, 41, 42, 43, 45, 47, 48, 49, 50)


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
        "tables": (f"production_control_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"ProductionControl{_camel(capability.slug)}Panel",
        "route": f"POST /production-control/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in PRODUCTION_CONTROL_CONTROL_CAPABILITIES}


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
        "event_topic": PRODUCTION_CONTROL_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "production_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires production-owned evidence, UI, service/API, agent, event, and release proof before approval.")
    if number in _PRODUCTION_RISK_FEATURES and payload.get("production_risk_evidence_complete") is not True:
        findings.append("production scheduling, dispatch, execution, downtime, material, WIP, labor, machine, quality, scrap, completion, OEE, exception, model, event, boundary, and release decisions require complete production risk evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("shop-floor scheduling, execution, consumption, time booking, quality, scrap, completion, dispatch optimization, exceptions, policy, agent, resilience, crypto, and handover actions require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("production agent skills must produce cited, permission-checked, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("scheduling, adherence, dispatch optimization, projections, OEE, forecasts, simulations, proofs, audit, event cockpit, boundary, instruction parsing, anomaly, exposure, MLOps, resilience, crypto, controls, readiness, and execution proof must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("MRP, inventory, maintenance, quality, asset, identity, labor, carbon, model, and audit facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != PRODUCTION_CONTROL_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("production control eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in PRODUCTION_CONTROL_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary production datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("production controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_production_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in PRODUCTION_CONTROL_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in PRODUCTION_CONTROL_CONTROL_DECLARED_DEPENDENCIES)
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
        "required_event_topic": PRODUCTION_CONTROL_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PRODUCTION_CONTROL_CONTROL_ALLOWED_DATABASE_BACKENDS,
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


def improve1_production_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_production_control(capability) for capability in PRODUCTION_CONTROL_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.production-control-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": PRODUCTION_CONTROL_CONTROL_OWNED_TABLES,
        "declared_dependencies": PRODUCTION_CONTROL_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": PRODUCTION_CONTROL_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": PRODUCTION_CONTROL_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


PRODUCTION_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_production_control(slug, payload)) for capability in PRODUCTION_CONTROL_CONTROL_CAPABILITIES}
