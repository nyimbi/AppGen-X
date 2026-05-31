"""Executable improve1 controls for the Time and Labor PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    TIME_LABOR_ALLOWED_DATABASE_BACKENDS,
    TIME_LABOR_CONSUMED_EVENT_TYPES,
    TIME_LABOR_OWNED_TABLES,
    TIME_LABOR_REQUIRED_EVENT_TOPIC,
    _TIME_LABOR_RUNTIME_TABLES,
)

PBC_KEY = "time_labor"
EVENT_CONTRACT = "AppGen-X"
TIME_ALLOWED_DATABASE_BACKENDS = TIME_LABOR_ALLOWED_DATABASE_BACKENDS
TIME_REQUIRED_EVENT_TOPIC = TIME_LABOR_REQUIRED_EVENT_TOPIC
TIME_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in TIME_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in TIME_CAPABILITIES}
TIME_CONTROL_OWNED_TABLES = tuple(
    dict.fromkeys(
        TIME_LABOR_OWNED_TABLES
        + _TIME_LABOR_RUNTIME_TABLES
        + tuple(f"time_labor_{capability.slug}_control" for capability in TIME_CAPABILITIES)
    )
)
TIME_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        TIME_LABOR_CONSUMED_EVENT_TYPES
        + (
            "EmployeeUpdated",
            "RoleChanged",
            "CertificationUpdated",
            "SiteCalendarChanged",
            "PayrollCutoffOpened",
            "PayrollCutoffClosed",
            "ProjectCostObjectChanged",
            "ManufacturingWorkOrderChanged",
            "WarehouseSiteChanged",
            "AuditEvidenceSealed",
            "DocumentReceived",
            "IdentityVerified",
            "PolicyChanged",
            "WeatherOrSafetyAdvisoryReceived",
            "CarbonWindowChanged",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "legal_entity_id",
    "jurisdiction_id",
    "employee_projection_id",
    "work_site_id",
    "policy_version",
    "actor_id",
    "evidence_references",
)
_FIELD_ROWS = """
1|shift_readiness_id,shift_id,role_id,planned_start,planned_end,time_zone,cost_center,eligibility_status,holiday_context
2|pattern_lifecycle_id,pattern_id,recurrence_rule,effective_start,effective_end,rotation_rule,rest_constraint,activation_simulation
3|assignment_eligibility_id,employee_status,certification_set,availability_window,site_access,rest_gap_hours,overtime_exposure,rejection_explanation
4|schedule_bid_id,bid_window,eligible_employee_set,ranking_rule,seniority_weight,preference_score,award_reason,coverage_preserved
5|shift_swap_id,initiator_employee,receiver_employee,role_site_compatibility,overtime_impact,rest_validation,manager_approval,expiry_state
6|demand_forecast_id,forecast_source,forecast_window,required_hours,role_mix,confidence,assumption_set,realized_variance
7|schedule_optimization_id,hard_constraint_set,soft_preference_set,objective_weight,alternative_rejected,cost_impact,overtime_exposure,human_publish_approval
8|allocation_mechanism_id,seniority_rule,preference_rule,fairness_score,skill_scarcity,emergency_staffing,simulation_outcome,audit_rationale
9|clock_device_id,device_type,firmware_version,site_geofence,trust_level,owner,offline_capability,tamper_status,last_heartbeat
10|clock_route_id,source_priority,source_health,offline_mode,replay_behavior,duplicate_policy,fallback_approval,route_exception
11|geofence_validation_id,clock_event_id,accuracy_radius,device_trust,assignment_match,privacy_basis,location_confidence,override_reason
12|clock_sequence_id,sequence_state,clock_in,clock_out,meal_start,meal_end,break_start,repair_action,typed_exception
13|clock_exception_id,exception_type,owner_role,sla_hours,recovery_action,payroll_impact,root_cause,closure_evidence
14|calculation_trace_id,source_event_set,rounding_rule,break_deduction,shift_differential,overtime_bucket,policy_hash,resulting_line_set
15|rounding_policy_id,rounding_interval,direction,grace_period,scope,effective_date,bias_sample_result,activation_simulation
16|break_compliance_id,break_type,required_break_minutes,paid_status,auto_deduction_eligible,waiver_evidence,missed_break_premium,explanation
17|overtime_bucket_id,bucket_type,accumulation_window,stacking_rule,reset_boundary,rate_multiplier,earning_code,precedence
18|premium_rule_id,premium_trigger,rate_multiplier,flat_amount,earning_code,stackability,approval_required,jurisdiction_scope
19|holiday_calendar_id,region_scope,site_scope,observed_date,eligibility_rule,premium_behavior,blackout_rule,calendar_version
20|absence_entitlement_id,absence_type,accrual_rule,carryover_cap,waiting_period,negative_balance_policy,evidence_required,balance_impact_preview
21|absence_request_id,requested_dates,partial_day,reason_code,balance_impact,coverage_impact,approver,escalation_state,cancellation_rule
22|leave_conflict_id,overlap_set,coverage_gap,skill_gap,demand_forecast_link,holiday_constraint,fairness_impact,approval_recommendation
23|labor_summary_id,period,employee_id,earning_code,exception_state,approval_status,line_count,reject_unresolved_exception
24|summary_approval_id,approver_authority,material_change,exception_clearance,segregation_check,batch_evidence,rejection_reason,approved_event
25|hours_proof_id,summary_line_hash,approval_hash,policy_hash,trace_hash,exception_status,redacted_api,privacy_scope
26|cost_allocation_id,cost_center,project_projection,manufacturing_projection,warehouse_projection,allocation_percent,stale_projection_warning,rejected_reason
27|distribution_audit_id,shift_transfer_set,work_assignment,project_projection,supervisor_approval,payroll_summary_line,late_change_flag,anomaly_reason
28|employee_projection_freshness_id,employee_event,active_status,employment_dates,employee_group,identity_confidence,staleness_minutes,block_decision
29|role_projection_impact_id,role_event,affected_shift_set,affected_entry_set,approval_task_set,premium_eligibility_change,recalculation_required,impact_summary
30|approval_workflow_id,approval_type,approver_role,threshold,escalation_rule,delegation_rule,evidence_required,sla_hours,authorized_action
31|time_correction_id,original_value,proposed_value,reason_code,employee_acknowledgement,supervisor_approval,recalculation_effect,payroll_impact
32|policy_screening_id,action_type,attributes_evaluated,policy_decision,explanation,override_path,policy_version,screening_hash
33|fatigue_risk_id,schedule_density,overtime_signal,night_shift_count,rest_gap_signal,absence_history,privacy_guardrail,recommendation
34|anomaly_detection_id,device_trust_signal,geofence_signal,sequence_signal,correction_history,peer_pattern,source_route_signal,review_explanation
35|labor_exposure_model_id,site_role_period,coverage_shortfall,payroll_error_risk,compliance_breach_risk,fatigue_tail_risk,confidence_interval,mitigation_action
36|mlops_governance_id,model_name,feature_lineage,training_window,approval_status,explainability_evidence,drift_monitoring,rollback_plan
37|event_reliability_id,inbox_state,outbox_state,dead_letter_state,idempotency_key,handler_version,payload_lineage,replay_eligibility,projection_freshness
38|ownership_boundary_proof_id,command_name,owned_table_set,declared_projection_set,forbidden_table_fixture,static_check,runtime_check,boundary_result
39|isolation_control_id,tenant_scope,entity_scope,jurisdiction_scope,union_scope,site_scope,ui_filter,agent_preview_scope,leakage_check
40|workbench_coverage_id,schedule_board,pattern_panel,bid_panel,clock_queue,device_health,calculation_trace,overtime_review,agent_panel
41|document_intake_id,document_type,candidate_time_fact_set,owned_table_mapping,permission_validation,projection_validation,confidence,risk,preview_payload
42|agent_plan_id,planned_command,permission,owned_tables,idempotency_key,emitted_event,payroll_impact,rollback_limit,human_approval
43|overtime_simulation_id,scenario_type,affected_employee_set,premium_impact,coverage_impact,fatigue_impact,labor_cost_delta,pay_impact_preview
44|carbon_schedule_window_id,work_type,site_metadata,calendar_window,carbon_intensity,cost_tradeoff,coverage_tradeoff,fairness_tradeoff
45|resilience_drill_id,drill_type,device_outage,offline_replay,duplicate_punch,route_failover,retry_exhaustion,dead_letter_recovery,release_gate
46|crypto_authorization_id,crypto_epoch,signed_proof_reference,key_rotation_evidence,policy_version,algorithm_agility,migration_readiness,proof_scope
47|continuous_control_id,assertion_name,control_scope,unassigned_clock_check,stale_projection_check,geofence_bypass_check,dead_letter_aging,agent_bypass_check
48|payroll_cutoff_id,period,open_exception_count,missing_approval_count,stale_projection_count,recalculation_needed,late_change_detection,handoff_evidence
49|readiness_score_id,rule_readiness,device_readiness,projection_readiness,calculation_trace_readiness,event_reliability,ui_coverage,boundary_proof,agent_safety
50|end_to_end_proof_id,employee_projection,shift_creation,clock_event_set,exception_resolution,time_entry_calculation,labor_summary_approval,labor_hours_event,hours_proof
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    1: ("EmployeeUpdated", "RoleChanged", "SiteCalendarChanged"),
    3: ("EmployeeUpdated", "RoleChanged", "CertificationUpdated"),
    5: ("RoleChanged",),
    19: ("SiteCalendarChanged",),
    24: ("PayrollCutoffOpened",),
    25: ("PayrollCutoffClosed", "AuditEvidenceSealed"),
    26: ("ProjectCostObjectChanged", "ManufacturingWorkOrderChanged", "WarehouseSiteChanged"),
    28: ("EmployeeUpdated",),
    29: ("RoleChanged",),
    37: ("EmployeeUpdated", "RoleChanged"),
    41: ("DocumentReceived", "IdentityVerified"),
    44: ("CarbonWindowChanged",),
    48: ("PayrollCutoffClosed",),
    50: ("EmployeeUpdated", "RoleChanged", "PayrollCutoffClosed", "AuditEvidenceSealed"),
}
_SCHEDULING_FEATURES = (1, 2, 3, 4, 5, 6, 7, 8, 22, 33, 35, 43, 44, 49, 50)
_CLOCK_CALCULATION_FEATURES = (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 31, 34, 45, 47, 50)
_ABSENCE_PAYROLL_FEATURES = (20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 48, 50)
_GOVERNANCE_AGENT_FEATURES = (32, 36, 37, 38, 39, 40, 41, 42, 46, 47, 49, 50)
_AGENT_FEATURES = (34, 40, 41, 42, 43, 49, 50)
_HUMAN_CONFIRMATION_FEATURES = (5, 7, 8, 21, 24, 30, 31, 42, 43, 48, 50)
_APPROVAL_REQUIRED_FEATURES = (5, 7, 21, 24, 30, 31, 42, 48, 50)
_NON_MUTATING_FEATURES = (2, 3, 4, 6, 7, 8, 15, 22, 25, 27, 28, 29, 32, 33, 34, 35, 36, 38, 41, 42, 43, 44, 47, 49, 50)
_PROJECTION_ONLY_FEATURES = (1, 3, 19, 25, 26, 27, 28, 29, 37, 38, 48, 50)


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
        "tables": (f"time_labor_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"TimeLabor{_camel(capability.slug)}Panel",
        "route": f"POST /time-labor/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in TIME_CAPABILITIES}


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
        "event_topic": TIME_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "scheduling_evidence_complete": True,
        "clock_calculation_evidence_complete": True,
        "absence_payroll_evidence_complete": True,
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
        findings.append(f"{capability.title} requires owned time model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _SCHEDULING_FEATURES and payload.get("scheduling_evidence_complete") is not True:
        findings.append("scheduling evidence is required for shift readiness, patterns, eligibility, bids, swaps, demand forecasts, optimization, allocation, leave coverage, fatigue, labor exposure, overtime simulation, carbon windows, readiness, and end-to-end proof")
    if number in _CLOCK_CALCULATION_FEATURES and payload.get("clock_calculation_evidence_complete") is not True:
        findings.append("clock and calculation evidence is required for devices, routes, geofences, sequence states, exceptions, traces, rounding, breaks, overtime, premiums, holidays, corrections, anomaly review, resilience, continuous controls, and end-to-end proof")
    if number in _ABSENCE_PAYROLL_FEATURES and payload.get("absence_payroll_evidence_complete") is not True:
        findings.append("absence, approval, payroll-proof, cost allocation, projection freshness, role impact, approval workflow, cutoff, and end-to-end payroll handoff evidence is required")
    if number in _GOVERNANCE_AGENT_FEATURES and payload.get("governance_agent_evidence_complete") is not True:
        findings.append("policy screening, model governance, event reliability, ownership boundary, isolation, workbench coverage, document intake, agent plans, crypto authorization, continuous controls, readiness, and end-to-end evidence is required")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("schedule swaps, optimized schedules, allocation, absences, summaries, approval workflows, corrections, agent plans, simulations, payroll cutoff, and end-to-end handoff require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk time and labor actions require separated approval for swaps, schedule publishing, absence approval, labor summary approval, workflow authorization, corrections, agent plans, payroll cutoff, and end-to-end proof")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("time labor assistant skills must cite owned facts, show reversible CRUD previews, enforce permissions and policy checks, and block direct writes before approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("eligibility checks, forecasts, optimizations, audits, proofs, projections, policy screens, risks, anomalies, governance, boundary proof, document intake, agent plans, simulations, carbon windows, continuous controls, readiness, and end-to-end scenarios must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("employee, role, payroll, project, manufacturing, warehouse, finance, audit, and carbon context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != TIME_REQUIRED_EVENT_TOPIC:
        findings.append("time labor eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in TIME_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary time labor datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("time labor controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_time_labor_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in TIME_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in TIME_DECLARED_DEPENDENCIES)
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
        "required_event_topic": TIME_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": TIME_ALLOWED_DATABASE_BACKENDS,
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


def improve1_time_labor_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_time_labor_control(capability) for capability in TIME_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.time_labor.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": TIME_CONTROL_OWNED_TABLES,
        "allowed_database_backends": TIME_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": TIME_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": TIME_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


TIME_LABOR_CONTROL_FUNCTIONS = (
    "evaluate_time_labor_control",
    "improve1_time_labor_control_contract",
    "sample_payload_for",
)
