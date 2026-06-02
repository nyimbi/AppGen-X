"""Capital projects delivery controls for improve1 execution."""
from __future__ import annotations

from datetime import date, datetime, timedelta
import hashlib
import json
from typing import Mapping, Sequence

PBC_KEY = "capital_projects_delivery"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = (
    "capital_projects_delivery_capital_project",
    "capital_projects_delivery_epc_package",
    "capital_projects_delivery_permit_milestone",
    "capital_projects_delivery_progress_measurement",
    "capital_projects_delivery_commissioning_system",
    "capital_projects_delivery_project_risk",
    "capital_projects_delivery_turnover_package",
    "capital_projects_delivery_capital_projects_delivery_policy_rule",
    "capital_projects_delivery_capital_projects_delivery_runtime_parameter",
    "capital_projects_delivery_capital_projects_delivery_schema_extension",
    "capital_projects_delivery_capital_projects_delivery_control_assertion",
    "capital_projects_delivery_capital_projects_delivery_governed_model",
    "capital_projects_delivery_appgen_outbox_event",
    "capital_projects_delivery_appgen_inbox_event",
    "capital_projects_delivery_appgen_dead_letter_event",
)
PROJECT_CONTROL_CAPABILITIES = (
    "stage_gate_lifecycle_capital_project_phases",
    "wbs_governed_hierarchy",
    "estimate_class_basis_control",
    "baseline_schedule_critical_path",
    "epc_startup_milestone_library",
    "package_commitment_accrual_forecast_control",
    "earned_progress_measurable_work_rules",
    "schedule_cost_performance_indices",
    "change_order_recovery_pipeline",
    "early_warning_claims_avoidance_register",
    "quantitative_risk_trigger_register",
    "opportunity_management",
    "permit_dependency_workfront_matrix",
    "long_lead_equipment_site_readiness",
    "contractor_package_readiness_ntp",
    "field_constraint_log",
    "epc_interface_management",
    "mechanical_completion_system_subsystem",
    "punch_list_severity_thresholds",
    "pre_commissioning_activity_tracking",
    "commissioning_sequence_startup_window",
    "handover_dossier_completeness",
    "defect_liability_post_handover_obligations",
    "funding_appropriation_checkpoints",
    "contingency_drawdown_discipline",
    "resource_productivity_risk_tracking",
    "weather_seasonal_disruption_modeling",
    "quality_hold_point_release_boundaries",
    "construction_sequence_workbench_visualization",
    "monthly_project_review_pack_generation",
    "capital_project_readiness_release_evidence",
    "assistant_project_controls_skills",
    "document_instruction_contractor_owner_artifacts",
    "lifecycle_control_event_boundary_refinement",
    "consumed_event_capital_project_effects",
    "api_boundary_workbench_mutation_hardening",
    "idempotent_field_document_updates",
    "dead_letter_operational_triage",
    "configuration_workbench_calendars_thresholds",
    "capital_delivery_policy_rule_library",
    "monthly_gate_review_control_assertions",
    "owner_schema_extension_governance",
    "governed_model_package_system_semantics",
    "multi_project_portfolio_rollup",
    "cross_pbc_delivery_boundary_map",
    "startup_readiness_review_workflow",
    "handover_operations_training_spares",
    "live_project_onboarding_baseline_migration",
    "continuous_release_assurance_domain_scenarios",
    "capital_project_closeout_knowledge_capture",
)
STAGES = ("idea", "screening", "fel", "approved_for_execution", "active_construction", "mechanical_completion", "ready_for_startup", "handover_complete", "closeout")


def _tuple(value: object) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, (list, set)):
        return tuple(value)
    return (value,)


def _date(value: object | None) -> date:
    if value is None:
        return date(2026, 5, 30)
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


def _result(capability: str, table: str, **payload: object) -> dict:
    return {"ok": True, "pbc": PBC_KEY, "capability": capability, "table": table, "event_contract": EVENT_CONTRACT, "stream_engine_picker_visible": False, "shared_table_access": False, "side_effects": (), **payload}


def evaluate_stage_gate(current_stage: str, target_stage: str, criteria: Mapping[str, object], approver_role: str, required_role: str, rebaseline_reason: str | None = None) -> dict:
    direction = "advance" if STAGES.index(target_stage) > STAGES.index(current_stage) else "rollback"
    adjacent = abs(STAGES.index(target_stage) - STAGES.index(current_stage)) == 1
    blocked = tuple(k for k, v in dict(criteria or {}).items() if not v)
    allowed = adjacent and approver_role == required_role and (not blocked if direction == "advance" else bool(rebaseline_reason))
    return _result("stage_gate_lifecycle_capital_project_phases", OWNED_TABLES[0], transition_allowed=allowed, direction=direction, blocked_criteria=blocked, emits="CapitalProjectsDeliveryApproved" if allowed else "CapitalProjectsDeliveryExceptionOpened")


def validate_wbs_hierarchy(nodes: Sequence[Mapping[str, object]]) -> dict:
    ids = {n.get("wbs_id") for n in nodes}
    orphans = tuple(dict(n) for n in nodes if n.get("parent_id") and n.get("parent_id") not in ids)
    duplicates = tuple(x for x in ids if sum(1 for n in nodes if n.get("wbs_id") == x) > 1)
    return _result("wbs_governed_hierarchy", OWNED_TABLES[1], orphaned_nodes=orphans, duplicate_nodes=duplicates, rollup_dimensions=("area", "discipline", "control_account"))


def control_estimate_basis(revisions: Sequence[Mapping[str, object]]) -> dict:
    ordered = tuple(sorted((dict(r) for r in revisions), key=lambda r: str(r.get("effective_at", ""))))
    sanctioned = next((r for r in reversed(ordered) if r.get("status") == "sanctioned"), None)
    lineage_ok = all(i == 0 or ordered[i].get("predecessor_id") == ordered[i-1].get("estimate_id") for i in range(len(ordered)))
    return _result("estimate_class_basis_control", OWNED_TABLES[0], sanctioned_estimate=sanctioned, lineage_ok=lineage_ok, revision_count=len(ordered))


def govern_schedule_baseline(baselines: Sequence[Mapping[str, object]]) -> dict:
    current = next((dict(b) for b in baselines if b.get("current")), None)
    eroded = tuple(dict(b) for b in baselines if float(b.get("total_float_days", 0)) < float(b.get("float_threshold_days", 5)))
    return _result("baseline_schedule_critical_path", OWNED_TABLES[0], current_baseline=current, near_critical_paths=eroded, approval_required_for_rebaseline=True)


def build_milestone_library(milestones: Sequence[Mapping[str, object]]) -> dict:
    invalid = tuple(dict(m) for m in milestones if not m.get("milestone_type") or not m.get("success_criteria"))
    return _result("epc_startup_milestone_library", OWNED_TABLES[2], milestones=tuple(dict(m) for m in milestones), invalid_milestones=invalid, phase_filters=tuple(sorted({m.get("phase") for m in milestones})))


def control_package_cost(packages: Sequence[Mapping[str, object]]) -> dict:
    rollups = []
    for p in packages:
        p = dict(p); variance = float(p.get("forecast_final_cost", 0)) - float(p.get("approved_budget", 0))
        rollups.append({"package_id": p.get("package_id"), "awarded": p.get("awarded_value", 0), "forecast": p.get("forecast_final_cost", 0), "variance": variance})
    return _result("package_commitment_accrual_forecast_control", OWNED_TABLES[1], cost_rollup=tuple(rollups), movements_require_explanation=True)


def earn_progress(measurements: Sequence[Mapping[str, object]]) -> dict:
    earned = tuple({**dict(m), "earned_percent": round(100 * float(m.get("earned_quantity", 0)) / max(1, float(m.get("total_quantity", 1))), 2)} for m in measurements if m.get("rule_of_credit"))
    unsupported = tuple(dict(m) for m in measurements if m.get("manual_percent") and not m.get("rule_of_credit"))
    return _result("earned_progress_measurable_work_rules", OWNED_TABLES[3], earned_records=earned, blocked_manual_percentages=unsupported)


def calculate_performance_indices(values: Mapping[str, object]) -> dict:
    pv, ev, ac = float(values.get("planned_value", 0)), float(values.get("earned_value", 0)), float(values.get("actual_cost", 0))
    return _result("schedule_cost_performance_indices", OWNED_TABLES[3], spi=round(ev / max(1, pv), 4), cpi=round(ev / max(1, ac), 4), trend_direction=values.get("trend", "stable"))


def track_change_order(change: Mapping[str, object]) -> dict:
    c = dict(change or {}); approved = c.get("state") == "approved"
    return _result("change_order_recovery_pipeline", OWNED_TABLES[1], state=c.get("state"), pending_exposure=0 if approved else c.get("estimated_impact", 0), approved_impact=c.get("approved_impact", 0) if approved else 0, schedule_entitlement=c.get("schedule_entitlement"))


def manage_early_warning(warnings: Sequence[Mapping[str, object]], as_of: object | None = None) -> dict:
    today = _date(as_of); aged = tuple({**dict(w), "age_days": (today - _date(w.get("event_date"))).days} for w in warnings)
    escalations = tuple(w for w in aged if w["age_days"] > int(w.get("sla_days", 7)))
    return _result("early_warning_claims_avoidance_register", OWNED_TABLES[5], warnings=aged, escalations=escalations)


def quantify_risks(risks: Sequence[Mapping[str, object]]) -> dict:
    enriched = tuple({**dict(r), "expected_cost": round(float(r.get("probability", 0)) * float(r.get("cost_impact", 0)), 2), "expected_days": round(float(r.get("probability", 0)) * float(r.get("schedule_days", 0)), 2)} for r in risks)
    return _result("quantitative_risk_trigger_register", OWNED_TABLES[5], risks=enriched, triggered=tuple(r for r in enriched if r.get("triggered")))


def manage_opportunities(items: Sequence[Mapping[str, object]]) -> dict:
    approved = tuple(dict(i) for i in items if i.get("status") == "approved")
    benefit = sum(float(i.get("expected_benefit", 0)) * float(i.get("confidence", 1)) for i in approved)
    return _result("opportunity_management", OWNED_TABLES[5], approved_opportunities=approved, weighted_benefit=round(benefit, 2))


def build_permit_dependency_matrix(permits: Sequence[Mapping[str, object]]) -> dict:
    blocked = tuple(dict(p) for p in permits if p.get("status") != "approved" and p.get("tied_workfront"))
    expiring = tuple(dict(p) for p in permits if p.get("expiry") and (_date(p.get("expiry")) - date(2026, 5, 30)).days <= 30)
    return _result("permit_dependency_workfront_matrix", OWNED_TABLES[2], blocked_workfronts=blocked, upcoming_expiries=expiring)


def track_long_lead_equipment(items: Sequence[Mapping[str, object]]) -> dict:
    risks = tuple(dict(i) for i in items if i.get("shipment_status") == "late" or (i.get("received") and not i.get("site_ready")))
    return _result("long_lead_equipment_site_readiness", OWNED_TABLES[1], long_lead_items=tuple(dict(i) for i in items), critical_path_risks=risks)


def evaluate_package_readiness(checklist: Mapping[str, object]) -> dict:
    required = ("scope_freeze", "ifc_maturity", "material_strategy", "access_handoff", "temporary_facilities", "owner_furnished_items", "interface_agreement")
    missing = tuple(k for k in required if not dict(checklist or {}).get(k))
    return _result("contractor_package_readiness_ntp", OWNED_TABLES[1], ready_for_field_execution=not missing, missing_items=missing)


def manage_field_constraints(constraints: Sequence[Mapping[str, object]], as_of: object | None = None) -> dict:
    today = _date(as_of); aged = tuple({**dict(c), "age_days": (today - _date(c.get("start_date"))).days} for c in constraints if c.get("status") != "closed")
    return _result("field_constraint_log", OWNED_TABLES[3], open_constraints=aged, escalations=tuple(c for c in aged if c["age_days"] > c.get("sla_days", 5)))


def manage_interfaces(interfaces: Sequence[Mapping[str, object]]) -> dict:
    late = tuple(dict(i) for i in interfaces if i.get("status") != "accepted" and _date(i.get("due_date")) < date(2026, 5, 30))
    return _result("epc_interface_management", OWNED_TABLES[1], interfaces=tuple(dict(i) for i in interfaces), late_interfaces=late)


def evaluate_mechanical_completion(systems: Sequence[Mapping[str, object]]) -> dict:
    blocked = tuple(dict(s) for s in systems if not s.get("mapped_work_complete") or not s.get("completion_criteria_met"))
    return _result("mechanical_completion_system_subsystem", OWNED_TABLES[4], systems=tuple(dict(s) for s in systems), mechanical_completion_allowed=not blocked, blocked_systems=blocked)


def control_punch_list(items: Sequence[Mapping[str, object]]) -> dict:
    critical = tuple(dict(i) for i in items if i.get("severity") in {"A", "critical"} and i.get("status") != "closed")
    return _result("punch_list_severity_thresholds", OWNED_TABLES[6], open_critical_punch=critical, readiness_blocked=bool(critical))


def track_pre_commissioning(activities: Sequence[Mapping[str, object]]) -> dict:
    failed = tuple(dict(a) for a in activities if a.get("status") in {"failed", "retest_required"})
    complete = sum(1 for a in activities if a.get("status") == "passed")
    return _result("pre_commissioning_activity_tracking", OWNED_TABLES[4], failed_activities=failed, completion_percent=round(100 * complete / max(1, len(tuple(activities))), 2))


def control_commissioning_sequence(systems: Sequence[Mapping[str, object]]) -> dict:
    blockers = tuple(dict(s) for s in systems if not all(s.get(k) for k in ("utility_available", "vendor_attendance", "energization_approved", "startup_permit")))
    return _result("commissioning_sequence_startup_window", OWNED_TABLES[4], sequence_blockers=blockers, startup_window_ready=not blockers)


def validate_handover_dossier(package: Mapping[str, object]) -> dict:
    required = ("as_built_drawings", "test_packs", "warranties", "spares", "training", "operating_procedures", "asset_data")
    missing = tuple(k for k in required if not dict(package or {}).get(k))
    return _result("handover_dossier_completeness", OWNED_TABLES[6], missing_documents=missing, handover_complete=not missing)


def track_post_handover_obligations(obligations: Sequence[Mapping[str, object]]) -> dict:
    unresolved = tuple(dict(o) for o in obligations if o.get("critical") and o.get("status") != "closed")
    return _result("defect_liability_post_handover_obligations", OWNED_TABLES[6], unresolved_critical_defects=unresolved, retention_release_blocked=bool(unresolved))


def check_funding_appropriation(project: Mapping[str, object]) -> dict:
    p = dict(project or {}); exposure = float(p.get("committed_amount", 0)) + float(p.get("pending_exposure", 0))
    over = exposure > float(p.get("approved_amount", 0))
    return _result("funding_appropriation_checkpoints", OWNED_TABLES[0], exposure=exposure, funding_sufficient=not over, approval_request_required=over)


def govern_contingency_drawdown(drawdowns: Sequence[Mapping[str, object]]) -> dict:
    unjustified = tuple(dict(d) for d in drawdowns if not d.get("linked_risk_or_change"))
    used = sum(float(d.get("amount", 0)) for d in drawdowns)
    return _result("contingency_drawdown_discipline", OWNED_TABLES[0], used_contingency=used, unjustified_drawdowns=unjustified)


def track_productivity_risk(records: Sequence[Mapping[str, object]]) -> dict:
    variances = tuple({**dict(r), "productivity_delta": float(r.get("actual_productivity", 0)) - float(r.get("planned_productivity", 0))} for r in records)
    return _result("resource_productivity_risk_tracking", OWNED_TABLES[5], productivity_records=variances, schedule_impact_records=tuple(r for r in variances if r["productivity_delta"] < 0))


def model_weather_disruption(delays: Sequence[Mapping[str, object]]) -> dict:
    weather = tuple(dict(d) for d in delays if d.get("delay_type") == "weather")
    controllable = tuple(dict(d) for d in delays if d.get("delay_type") != "weather")
    return _result("weather_seasonal_disruption_modeling", OWNED_TABLES[5], weather_days=sum(float(d.get("days", 0)) for d in weather), controllable_days=sum(float(d.get("days", 0)) for d in controllable))


def manage_quality_hold_points(points: Sequence[Mapping[str, object]]) -> dict:
    outstanding = tuple(dict(p) for p in points if p.get("status") != "released")
    return _result("quality_hold_point_release_boundaries", OWNED_TABLES[1], outstanding_hold_points=outstanding, execution_blocked=bool(outstanding))


def build_sequence_workbench(packages: Sequence[Mapping[str, object]]) -> dict:
    blocked = tuple(dict(p) for p in packages if p.get("blocker") or p.get("late_predecessor"))
    return _result("construction_sequence_workbench_visualization", OWNED_TABLES[11], sequence_rows=tuple(dict(p) for p in packages), blocked_sequences=blocked, pivots=("package", "area", "system"))


def generate_monthly_review_pack(records: Mapping[str, object]) -> dict:
    required = ("capital_project", "epc_package", "project_risk", "progress_measurement", "turnover_package")
    missing = tuple(k for k in required if not dict(records or {}).get(k))
    return _result("monthly_project_review_pack_generation", OWNED_TABLES[11], pack_id=_digest(records)[:12], missing_sections=missing, frozen_snapshot=not missing)


def build_readiness_release_evidence(scenarios: Mapping[str, object]) -> dict:
    required = ("sanction", "field_execution", "startup_readiness", "handover")
    missing = tuple(k for k in required if not dict(scenarios or {}).get(k))
    return _result("capital_project_readiness_release_evidence", OWNED_TABLES[11], missing_scenarios=missing, release_ready=not missing)


def plan_assistant_project_controls(role: str, prompt: str) -> dict:
    skills = {"scheduler": "schedule_diagnostics", "cost_engineer": "forecast_narrative", "permit_coordinator": "permit_action_list", "package_engineer": "package_readiness_summary", "commissioning_manager": "turnover_gap_analysis"}
    return _result("assistant_project_controls_skills", OWNED_TABLES[11], role=role, skill=skills.get(role, "project_controls_summary"), requires_confirmation="update" in prompt.lower())


def parse_project_document(document: Mapping[str, object], artifact_type: str) -> dict:
    fields = {"notice": ("date", "party", "package"), "permit": ("authority", "expiry", "workfront"), "meeting_minutes": ("actions", "owners"), "startup_procedure": ("system", "prerequisites")}.get(artifact_type, ())
    proposals = {field: dict(document or {}).get(field) for field in fields}
    uncertain = tuple(k for k, v in proposals.items() if v is None)
    return _result("document_instruction_contractor_owner_artifacts", OWNED_TABLES[11], artifact_type=artifact_type, proposals=proposals, uncertain_fields=uncertain, requires_review=True)


def refine_event_boundary(event_context: Mapping[str, object]) -> dict:
    payload = {k: dict(event_context or {}).get(k) for k in ("lifecycle_stage", "affected_object_type", "project_key", "wbs_scope", "package_reference", "system_reference")}
    return _result("lifecycle_control_event_boundary_refinement", OWNED_TABLES[12], payload=payload, filterable_fields=tuple(payload))


def handle_consumed_project_event(event: Mapping[str, object], records: Sequence[Mapping[str, object]]) -> dict:
    action = {"PolicyChanged": "reevaluate_active_controls", "AuditEventSealed": "freeze_review_pack_evidence", "OperationalKpiChanged": "refresh_health_thresholds"}.get(dict(event or {}).get("event_type"), "noop")
    return _result("consumed_event_capital_project_effects", OWNED_TABLES[13], action=action, affected_records=tuple(dict(r) for r in records), replay_deterministic=True)


def harden_api_boundary(route: str, payload: Mapping[str, object]) -> dict:
    immutable_fields = {"sanctioned_estimate", "approved_gate", "baseline_id"}
    attempted = immutable_fields.intersection(set(dict(payload or {}).get("fields_changed", ())))
    return _result("api_boundary_workbench_mutation_hardening", OWNED_TABLES[0], route=route, rejected_fields=tuple(attempted), mutation_allowed=not attempted)


def guard_idempotent_update(channel: str, payload: Mapping[str, object], seen: Sequence[str]) -> dict:
    key = dict(payload or {}).get("idempotency_key") or _digest((channel, payload))
    duplicate = key in set(seen)
    return _result("idempotent_field_document_updates", OWNED_TABLES[13], channel=channel, idempotency_key=key, duplicate=duplicate, effective_mutations=0 if duplicate else 1)


def triage_dead_letter(failure: Mapping[str, object]) -> dict:
    code = dict(failure or {}).get("code", "unknown")
    object_type = dict(failure or {}).get("object_type", "capital_project")
    severity = "high" if object_type in {"permit_milestone", "commissioning_system"} else "medium"
    return _result("dead_letter_operational_triage", OWNED_TABLES[14], object_type=object_type, business_cause=code, severity=severity, retry_guidance="repair_payload_then_replay")


def version_configuration_change(parameter: Mapping[str, object]) -> dict:
    p = dict(parameter or {})
    return _result("configuration_workbench_calendars_thresholds", OWNED_TABLES[8], parameter=p, approved=bool(p.get("approved_by")), effective_at=p.get("effective_at"), re_evaluation_required=True)


def evaluate_policy_rule(rule: Mapping[str, object], context: Mapping[str, object]) -> dict:
    r = dict(rule or {}); waived = bool(r.get("waived_by") and r.get("waiver_reason"))
    passed = bool(dict(context or {}).get(r.get("required_flag", "pass"))) or waived
    return _result("capital_delivery_policy_rule_library", OWNED_TABLES[7], rule_id=r.get("rule_id"), passed=passed, waived=waived, severity=r.get("severity", "medium"))


def run_control_assertions(records: Sequence[Mapping[str, object]]) -> dict:
    failures = tuple(dict(r) for r in records if r.get("stale_forecast") or r.get("unmapped_wbs") or r.get("expired_permit") or r.get("critical_punch") or r.get("missing_handover_docs"))
    return _result("monthly_gate_review_control_assertions", OWNED_TABLES[10], failures=failures, review_ready=not failures)


def register_owner_schema_extension(extension: Mapping[str, object]) -> dict:
    e = dict(extension or {}); required = ("field_name", "purpose", "owning_team", "projection_impact", "validation_rule", "rollout_plan")
    missing = tuple(k for k in required if not e.get(k))
    return _result("owner_schema_extension_governance", OWNED_TABLES[9], valid=not missing and str(e.get("table", OWNED_TABLES[0])).startswith(PBC_KEY), missing_fields=missing)


def define_governed_model_semantics(definitions: Sequence[Mapping[str, object]]) -> dict:
    terms = tuple(dict(d) for d in definitions if d.get("term") and d.get("definition"))
    return _result("governed_model_package_system_semantics", OWNED_TABLES[11], definitions=terms, canonical_terms=tuple(d["term"] for d in terms))


def build_portfolio_rollup(projects: Sequence[Mapping[str, object]]) -> dict:
    rows = tuple({"project_id": p.get("project_id"), "forecast_variance": float(p.get("forecast", 0)) - float(p.get("sanctioned_budget", 0)), "driver": p.get("red_driver")} for p in projects)
    return _result("multi_project_portfolio_rollup", OWNED_TABLES[0], portfolio_rows=rows, drillback_enabled=True)


def map_cross_pbc_boundaries() -> dict:
    return _result("cross_pbc_delivery_boundary_map", OWNED_TABLES[12], owns=("package_control", "permit_control", "commissioning", "turnover", "cost_schedule_analytics"), consumes=("procurement_events", "document_control_apis", "maintenance_readiness_events", "financial_governance_events"), direct_mutation_forbidden=True)


def review_startup_readiness(review: Mapping[str, object]) -> dict:
    required = ("construction_complete", "commissioning_passed", "permits_ready", "training_complete", "risks_accepted", "authorization")
    missing = tuple(k for k in required if not dict(review or {}).get(k))
    return _result("startup_readiness_review_workflow", OWNED_TABLES[4], status="complete" if not missing else "blocked", blockers=missing, conditional_obligations=tuple(_tuple(dict(review or {}).get("conditional_obligations"))))


def verify_operations_handover(package: Mapping[str, object]) -> dict:
    required = ("operator_training", "operating_procedures", "maintenance_task_seeds", "spares_available", "vendor_support")
    missing = tuple(k for k in required if not dict(package or {}).get(k))
    return _result("handover_operations_training_spares", OWNED_TABLES[6], accepted=not missing, missing_preparedness=missing)


def onboard_live_project(imports: Mapping[str, object]) -> dict:
    required = ("capital_project", "epc_package", "permit_milestone", "progress_measurement", "project_risk")
    gaps = tuple(k for k in required if not dict(imports or {}).get(k))
    return _result("live_project_onboarding_baseline_migration", OWNED_TABLES[0], onboarding_status="complete" if not gaps else "exception", historical_gaps=gaps, data_confidence="high" if not gaps else "partial")


def assure_domain_scenarios(scenarios: Mapping[str, object]) -> dict:
    required = ("gate_approval", "wbs_rollup", "long_lead_slip", "permit_expiry", "change_order_approval", "system_completion", "startup_readiness", "handover_dossier")
    missing = tuple(k for k in required if not dict(scenarios or {}).get(k))
    return _result("continuous_release_assurance_domain_scenarios", OWNED_TABLES[11], release_allowed=not missing, missing_scenarios=missing)


def capture_closeout_knowledge(closeout: Mapping[str, object]) -> dict:
    required = ("final_cost_variance", "milestone_slippage_causes", "change_concentration", "startup_bottlenecks", "handover_defects", "lessons_summary")
    missing = tuple(k for k in required if not dict(closeout or {}).get(k))
    return _result("capital_project_closeout_knowledge_capture", OWNED_TABLES[0], closeout_allowed=not missing, missing_fields=missing, searchable_lessons=not missing)


def improve1_project_control_contract() -> dict:
    return _result(
        "improve1_project_control_contract",
        OWNED_TABLES[0],
        capability_count=len(PROJECT_CONTROL_CAPABILITIES),
        capabilities=PROJECT_CONTROL_CAPABILITIES,
        owned_tables=OWNED_TABLES,
        ui_surfaces=tuple(f"{PBC_KEY}.ui.project_control.{capability}" for capability in PROJECT_CONTROL_CAPABILITIES),
        service_surfaces=tuple(f"{PBC_KEY}.service.project_control.{capability}" for capability in PROJECT_CONTROL_CAPABILITIES),
    )
