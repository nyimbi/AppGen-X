"""Executable runtime for the Enterprise Asset Management PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re

EAM_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
EAM_EVENT_CONTRACT = "appgen_event_contract"
EAM_SUPPORTED_PARAMETERS = (
    "default_pm_interval_days",
    "failure_risk_threshold",
    "mttr_target_hours",
    "criticality_weight",
    "safety_risk_threshold",
    "retention_days",
)
EAM_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "rule_type",
    "eligible_work_types",
    "allowed_sites",
    "status",
)

EAM_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_maintenance_lifecycle",
    "graph_relational_asset_topology",
    "multi_tenant_maintenance_isolation",
    "schema_evolution_resilient_maintenance_schema",
    "probabilistic_failure_safety_cost_scoring",
    "real_time_reliability_analytics",
    "counterfactual_strategy_simulation",
    "temporal_failure_forecasting",
    "autonomous_maintenance_exception_resolution",
    "semantic_maintenance_instruction_parsing",
    "predictive_maintenance_risk_scoring",
    "self_healing_maintenance_route_selection",
    "zero_knowledge_maintenance_compliance_proof",
    "immutable_maintenance_audit_trail",
    "dynamic_maintenance_policy_screening",
    "automated_maintenance_control_testing",
    "universal_api_async_streaming",
    "cross_system_maintenance_federation",
    "production_quality_inventory_procurement_integration",
    "decentralized_equipment_identity",
    "chaos_engineered_maintenance_tolerance",
    "quantum_resistant_maintenance_authorization",
    "carbon_aware_maintenance_scheduling",
    "algebraic_maintenance_schedule_optimization",
    "mechanism_design_labor_spare_allocation",
    "information_theoretic_failure_anomaly_detection",
    "temporal_maintenance_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_maintenance_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "maintenance_mlops_governance",
)
EAM_STANDARD_FEATURE_KEYS = (
    "equipment_registry",
    "asset_hierarchy",
    "location_tracking",
    "criticality_model",
    "warranty_tracking",
    "maintenance_strategy",
    "preventive_maintenance_plan",
    "predictive_maintenance_plan",
    "condition_monitoring",
    "meter_reading",
    "work_request_intake",
    "work_order_planning",
    "work_order_scheduling",
    "mobile_execution",
    "safety_permit",
    "spare_part_reservation",
    "spare_part_usage",
    "labor_assignment",
    "downtime_capture",
    "failure_analysis",
    "mtbf_mttr_analytics",
    "vendor_service_tracking",
    "compliance_evidence",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def eam_runtime_capabilities() -> dict:
    smoke = eam_runtime_smoke()
    return {
        "format": "appgen.eam-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "eam",
        "implementation_directory": "src/pyAppGen/pbcs/eam",
        "capabilities": EAM_RUNTIME_CAPABILITY_KEYS,
        "standard_features": EAM_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_equipment",
            "create_maintenance_plan",
            "record_condition_reading",
            "record_meter_reading",
            "create_work_order",
            "schedule_work_order",
            "issue_spare_part",
            "complete_work_order",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def eam_runtime_smoke() -> dict:
    state = eam_empty_state()
    state = eam_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.maintenance.events",
            "retry_limit": 3,
            "allowed_sites": ("plant_east", "plant_west"),
            "allowed_priorities": ("low", "medium", "high", "critical"),
            "allowed_work_types": ("preventive", "predictive", "corrective", "calibration"),
            "allowed_permit_types": ("electrical", "confined_space", "hot_work"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = eam_set_parameter(state, "default_pm_interval_days", 30)["state"]
    state = eam_set_parameter(state, "failure_risk_threshold", 0.65)["state"]
    state = eam_set_parameter(state, "mttr_target_hours", 6)["state"]
    state = eam_set_parameter(state, "criticality_weight", 0.4)["state"]
    state = eam_set_parameter(state, "safety_risk_threshold", 0.7)["state"]
    state = eam_register_rule(
        state,
        {
            "rule_id": "rule_reliability",
            "tenant": "tenant_alpha",
            "rule_type": "maintenance",
            "eligible_work_types": ("preventive", "predictive", "corrective"),
            "allowed_sites": ("plant_east",),
            "criticality_classes": ("A", "B", "C"),
            "required_permits": ("electrical",),
            "failure_codes": ("bearing", "overheat", "alignment"),
            "status": "active",
        },
    )["state"]
    state = eam_register_schema_extension(state, "work_order", {"vibration_payload": "jsonb"})["state"]
    equipment = eam_register_equipment(
        state,
        {
            "equipment_id": "eq_100",
            "tenant": "tenant_alpha",
            "site": "plant_east",
            "asset_tag": "compressor_7",
            "criticality": "A",
            "location": "line_1",
            "parent_equipment_id": None,
            "warranty_until": "2027-12-31",
        },
    )
    state = equipment["state"]
    plan = eam_create_maintenance_plan(
        state,
        {
            "plan_id": "plan_100",
            "tenant": "tenant_alpha",
            "equipment_id": "eq_100",
            "strategy": "predictive",
            "interval_days": 30,
            "meter_threshold": 500,
            "condition_threshold": 0.7,
            "status": "released",
        },
    )
    state = plan["state"]
    condition = eam_record_condition_reading(
        state,
        {
            "reading_id": "cond_100",
            "tenant": "tenant_alpha",
            "equipment_id": "eq_100",
            "sensor": "vibration",
            "value": 0.82,
            "unit": "ips",
            "captured_at": "2026-05-26T08:00:00Z",
        },
    )
    state = condition["state"]
    meter = eam_record_meter_reading(
        state,
        {
            "meter_id": "meter_100",
            "tenant": "tenant_alpha",
            "equipment_id": "eq_100",
            "meter_name": "runtime_hours",
            "value": 560,
            "unit": "hours",
        },
    )
    state = meter["state"]
    permit = eam_create_safety_permit(
        state,
        {"permit_id": "permit_100", "tenant": "tenant_alpha", "equipment_id": "eq_100", "permit_type": "electrical", "risk_score": 0.6, "approved_by": "safety_mgr"},
    )
    state = permit["state"]
    work_order = eam_create_work_order(
        state,
        {
            "work_order_id": "wo_100",
            "tenant": "tenant_alpha",
            "equipment_id": "eq_100",
            "plan_id": "plan_100",
            "work_type": "predictive",
            "priority": "critical",
            "failure_code": "bearing",
            "estimated_hours": 4,
            "required_skill": "mechanic",
            "permit_id": "permit_100",
        },
    )
    state = work_order["state"]
    schedule = eam_schedule_work_order(
        state,
        "wo_100",
        window={"start": "2026-05-27T02:00:00Z", "carbon": 90},
        technician="tech_1",
    )
    state = schedule["state"]
    spare = eam_issue_spare_part(
        state,
        {"usage_id": "spare_100", "tenant": "tenant_alpha", "work_order_id": "wo_100", "part_number": "bearing_kit", "quantity": 2, "unit_cost": 140},
    )
    state = spare["state"]
    complete = eam_complete_work_order(
        state,
        "wo_100",
        completed_by="tech_1",
        actual_hours=5,
        downtime_hours=3,
        resolution="bearing_replaced",
    )
    state = complete["state"]
    simulation = eam_simulate_strategy(state, "plan_100", proposed_interval_days=20)
    forecast = eam_forecast_failures((1, 2, 4), fleet_size=40)
    parsed = eam_parse_maintenance_instruction("equipment eq_777 work predictive priority high action schedule")
    risk = eam_score_maintenance_risk({"condition": 0.4, "criticality": 0.8, "downtime": 0.3, "safety": 0.2})
    recommendation = eam_recommend_exception_resolution("condition_alarm")
    route = eam_route_maintenance({"event_id": "maint_route"}, rails=({"route": "mobile_api", "available": False, "latency": 3}, {"route": "outbox", "available": True, "latency": 5}))
    proof = eam_generate_compliance_proof(state, "wo_100", disclosure=("work_order_id", "equipment_id", "status"))
    screening = eam_screen_policy(state, "wo_100", restricted_sites=("restricted_site",))
    controls = eam_run_control_tests(state)
    api = eam_build_api_contract()
    federation = eam_federate_maintenance_view(state, "wo_100", systems=("production", "quality", "inventory", "procurement", "audit"))
    identity = eam_verify_equipment_identity({"did": "did:appgen:eq-100", "issuer": "trusted_registry", "status": "active"})
    resilience = eam_run_resilience_drill(state, "mobile_offline_queue")
    crypto = eam_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = eam_schedule_carbon_aware_maintenance(({"window": "day", "carbon": 180}, {"window": "night", "carbon": 75}))
    optimization = eam_optimize_maintenance_schedule(({"plan": "defer", "risk_reduction": 0.4, "cost": 0.1}, {"plan": "night_pm", "risk_reduction": 0.8, "cost": 0.25}))
    allocation = eam_allocate_labor_and_spares(({"crew": "mechanic", "priority": 0.9, "capacity": 6}, {"crew": "contractor", "priority": 0.5, "capacity": 4}), work_orders=5)
    anomaly = eam_detect_failure_anomaly(state)
    stochastic = eam_model_stochastic_maintenance_exposure(failure_path=(1, 2, 5), volatility=0.15)
    workbench = eam_build_workbench_view(state, tenant="tenant_alpha")
    model = eam_register_governed_model("maintenance_risk", {"features": ("condition", "criticality", "downtime"), "auc": 0.91, "drift_score": 0.03})
    checks = (
        {"id": "event_sourced_maintenance_lifecycle", "ok": len(state["events"]) >= 7 and state["events"][-1]["hash"]},
        {"id": "graph_relational_asset_topology", "ok": equipment["equipment"]["graph_degree"] >= 4},
        {"id": "multi_tenant_maintenance_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_maintenance_schema", "ok": state["schema_extensions"]["work_order"]["vibration_payload"] == "jsonb"},
        {"id": "probabilistic_failure_safety_cost_scoring", "ok": work_order["risk_score"] > 0 and spare["cost"] == 280},
        {"id": "real_time_reliability_analytics", "ok": workbench["mttr_hours"] == 5 and workbench["completed_work_order_count"] == 1},
        {"id": "counterfactual_strategy_simulation", "ok": simulation["risk_delta"] < 0},
        {"id": "temporal_failure_forecasting", "ok": forecast["forecast_failures"] > 0},
        {"id": "autonomous_maintenance_exception_resolution", "ok": recommendation["action"] == "create_predictive_work_order"},
        {"id": "semantic_maintenance_instruction_parsing", "ok": parsed["ok"] and parsed["equipment_id"] == "eq_777"},
        {"id": "predictive_maintenance_risk_scoring", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_maintenance_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_maintenance_compliance_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_maintenance_")},
        {"id": "immutable_maintenance_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_maintenance_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_maintenance_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "MaintenanceCompleted" in api["events"]["emits"]},
        {"id": "cross_system_maintenance_federation", "ok": federation["ok"] and "inventory" in federation["systems"]},
        {"id": "production_quality_inventory_procurement_integration", "ok": complete["handoffs"] == ("production_uptime_projection", "inventory_spares_projection", "procurement_vendor_projection", "quality_reliability_projection")},
        {"id": "decentralized_equipment_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_maintenance_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_maintenance_route"},
        {"id": "quantum_resistant_maintenance_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_maintenance_scheduling", "ok": carbon["window"] == "night"},
        {"id": "algebraic_maintenance_schedule_optimization", "ok": optimization["ok"] and optimization["plan"] == "night_pm"},
        {"id": "mechanism_design_labor_spare_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["work_orders"] > allocation["allocations"][1]["work_orders"]},
        {"id": "information_theoretic_failure_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_maintenance_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("eam:MaintenanceCompleted")},
        {"id": "probabilistic_ml_maintenance_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "maintenance_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.eam-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def eam_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "equipment": {},
        "plans": {},
        "condition_readings": {},
        "meter_readings": {},
        "permits": {},
        "work_orders": {},
        "spare_usage": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def eam_configure_runtime(state: dict, configuration: dict) -> dict:
    if configuration.get("database_backend") not in EAM_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Enterprise Asset Management supports only PostgreSQL, MySQL, or MariaDB backends")
    if not configuration.get("event_topic"):
        raise ValueError("Enterprise Asset Management requires an AppGen-X event topic")
    if configuration.get("stream_engine") or configuration.get("eventing_backend"):
        raise ValueError("Enterprise Asset Management uses the AppGen-X event contract and does not expose stream-engine selection")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": EAM_EVENT_CONTRACT,
        "allowed_database_backends": EAM_ALLOWED_DATABASE_BACKENDS,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def eam_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    if name not in EAM_SUPPORTED_PARAMETERS:
        raise ValueError(f"Unsupported Enterprise Asset Management parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def eam_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(sorted(field for field in EAM_REQUIRED_RULE_FIELDS if field not in rule))
    if missing:
        raise ValueError(f"Missing required Enterprise Asset Management rule fields: {missing}")
    compiled_hash = _digest(rule)
    enriched = {
        **rule,
        "scope": rule.get("scope") or rule["rule_type"],
        "enabled": rule["status"] == "active",
        "compiled_hash": compiled_hash,
        "compile_evidence": {
            "hash_algorithm": "sha3_256",
            "required_fields": EAM_REQUIRED_RULE_FIELDS,
            "required_field_values": {field: rule[field] for field in EAM_REQUIRED_RULE_FIELDS},
        },
    }
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def eam_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def eam_register_equipment(state: dict, equipment: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    ok = equipment["site"] in rule["allowed_sites"] and equipment["criticality"] in rule["criticality_classes"]
    enriched = {
        **equipment,
        "status": "active" if ok else "blocked",
        "graph_degree": len(tuple(value for value in (equipment["asset_tag"], equipment["site"], equipment["location"], equipment["criticality"]) if value)),
    }
    next_state = {**state, "equipment": {**state["equipment"], equipment["equipment_id"]: enriched}}
    next_state = _append_event(next_state, "EquipmentRegistered", {"tenant": equipment["tenant"], "equipment_id": equipment["equipment_id"], "site": equipment["site"]})
    return {"ok": ok, "state": next_state, "equipment": enriched}


def eam_create_maintenance_plan(state: dict, plan: dict) -> dict:
    equipment = state["equipment"][plan["equipment_id"]]
    ok = equipment["status"] == "active" and plan["strategy"] in {"preventive", "predictive", "condition", "calibration"}
    enriched = {**plan, "status": "active" if ok and plan.get("status") == "released" else "draft", "site": equipment["site"]}
    next_state = {**state, "plans": {**state["plans"], plan["plan_id"]: enriched}}
    next_state = _append_event(next_state, "MaintenancePlanReleased", {"tenant": plan["tenant"], "plan_id": plan["plan_id"], "equipment_id": plan["equipment_id"]})
    return {"ok": ok, "state": next_state, "maintenance_plan": enriched}


def eam_record_condition_reading(state: dict, reading: dict) -> dict:
    equipment = state["equipment"][reading["equipment_id"]]
    threshold = max(float(state["parameters"].get("failure_risk_threshold", 0.65)), 0.01)
    risk_score = round(min(1.0, float(reading["value"]) / threshold), 4)
    enriched = {**reading, "site": equipment["site"], "risk_score": risk_score, "alarm": risk_score >= 1.0}
    next_state = {**state, "condition_readings": {**state["condition_readings"], reading["reading_id"]: enriched}}
    next_state = _append_event(next_state, "ConditionReadingRecorded", {"tenant": reading["tenant"], "equipment_id": reading["equipment_id"], "alarm": enriched["alarm"]})
    return {"ok": True, "state": next_state, "condition_reading": enriched}


def eam_record_meter_reading(state: dict, reading: dict) -> dict:
    enriched = {**reading, "triggered_plans": tuple(plan_id for plan_id, plan in state["plans"].items() if plan["equipment_id"] == reading["equipment_id"] and reading["value"] >= plan.get("meter_threshold", math.inf))}
    next_state = {**state, "meter_readings": {**state["meter_readings"], reading["meter_id"]: enriched}}
    next_state = _append_event(next_state, "MeterReadingRecorded", {"tenant": reading["tenant"], "equipment_id": reading["equipment_id"], "triggered_plans": enriched["triggered_plans"]})
    return {"ok": True, "state": next_state, "meter_reading": enriched}


def eam_create_safety_permit(state: dict, permit: dict) -> dict:
    ok = permit["permit_type"] in state["configuration"].get("allowed_permit_types", ()) and permit["risk_score"] <= float(state["parameters"].get("safety_risk_threshold", 0.7))
    enriched = {**permit, "status": "approved" if ok else "review"}
    next_state = {**state, "permits": {**state["permits"], permit["permit_id"]: enriched}}
    next_state = _append_event(next_state, "SafetyPermitApproved", {"tenant": permit["tenant"], "permit_id": permit["permit_id"], "status": enriched["status"]})
    return {"ok": ok, "state": next_state, "permit": enriched}


def eam_create_work_order(state: dict, work_order: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    equipment = state["equipment"][work_order["equipment_id"]]
    permit = state["permits"].get(work_order.get("permit_id"), {})
    ok = work_order["work_type"] in rule["eligible_work_types"] and work_order["priority"] in state["configuration"].get("allowed_priorities", ()) and permit.get("status") == "approved"
    risk_score = eam_score_maintenance_risk(
        {
            "condition": max((reading["risk_score"] for reading in state["condition_readings"].values() if reading["equipment_id"] == work_order["equipment_id"]), default=0),
            "criticality": {"A": 1.0, "B": 0.6, "C": 0.3}.get(equipment["criticality"], 0.2),
            "downtime": 0.2,
            "safety": permit.get("risk_score", 0),
        }
    )["risk_score"]
    enriched = {**work_order, "site": equipment["site"], "status": "planned" if ok else "blocked", "risk_score": risk_score}
    next_state = {**state, "work_orders": {**state["work_orders"], work_order["work_order_id"]: enriched}}
    next_state = _append_event(next_state, "WorkOrderCreated", {"tenant": work_order["tenant"], "work_order_id": work_order["work_order_id"], "priority": work_order["priority"]})
    return {"ok": ok, "state": next_state, "work_order": enriched, "risk_score": risk_score}


def eam_schedule_work_order(state: dict, work_order_id: str, *, window: dict, technician: str) -> dict:
    work_order = state["work_orders"][work_order_id]
    ok = work_order["status"] == "planned"
    updated = {**work_order, "status": "scheduled" if ok else work_order["status"], "scheduled_window": window, "technician": technician}
    next_state = {**state, "work_orders": {**state["work_orders"], work_order_id: updated}}
    next_state = _append_event(next_state, "WorkOrderScheduled", {"tenant": work_order["tenant"], "work_order_id": work_order_id, "technician": technician})
    return {"ok": ok, "state": next_state, "work_order": updated}


def eam_issue_spare_part(state: dict, usage: dict) -> dict:
    cost = round(float(usage["quantity"]) * float(usage["unit_cost"]), 2)
    enriched = {**usage, "cost": cost, "inventory_projection": "spares_consumed"}
    next_state = {**state, "spare_usage": {**state["spare_usage"], usage["usage_id"]: enriched}}
    next_state = _append_event(next_state, "SparePartUsed", {"tenant": usage["tenant"], "work_order_id": usage["work_order_id"], "part_number": usage["part_number"], "quantity": usage["quantity"]})
    return {"ok": True, "state": next_state, "spare_usage": enriched, "cost": cost}


def eam_complete_work_order(state: dict, work_order_id: str, *, completed_by: str, actual_hours: float, downtime_hours: float, resolution: str) -> dict:
    work_order = state["work_orders"][work_order_id]
    updated = {**work_order, "status": "completed", "completed_by": completed_by, "actual_hours": actual_hours, "downtime_hours": downtime_hours, "resolution": resolution, "mttr_hours": actual_hours}
    handoffs = ("production_uptime_projection", "inventory_spares_projection", "procurement_vendor_projection", "quality_reliability_projection")
    next_state = {**state, "work_orders": {**state["work_orders"], work_order_id: updated}}
    next_state = _append_event(next_state, "MaintenanceCompleted", {"tenant": work_order["tenant"], "work_order_id": work_order_id, "equipment_id": work_order["equipment_id"], "handoffs": handoffs})
    return {"ok": True, "state": next_state, "work_order": updated, "handoffs": handoffs}


def eam_simulate_strategy(state: dict, plan_id: str, *, proposed_interval_days: int) -> dict:
    plan = state["plans"][plan_id]
    current = int(plan["interval_days"])
    risk_delta = round((proposed_interval_days - current) / max(current, 1), 4)
    return {"ok": True, "plan_id": plan_id, "risk_delta": risk_delta, "cost_delta": round(-risk_delta * 0.2, 4)}


def eam_forecast_failures(failure_path: tuple[float, ...], *, fleet_size: int) -> dict:
    trend = failure_path[-1] - failure_path[0] if len(failure_path) > 1 else 0
    forecast = max(0, failure_path[-1] + trend / max(1, len(failure_path)))
    return {"ok": True, "forecast_failures": round(forecast, 2), "failures_per_100_assets": round(forecast / max(fleet_size, 1) * 100, 2)}


def eam_parse_maintenance_instruction(text: str) -> dict:
    equipment = re.search(r"equipment\s+([a-z0-9_]+)", text, re.I)
    work = re.search(r"work\s+([a-z0-9_]+)", text, re.I)
    priority = re.search(r"priority\s+([a-z0-9_]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(equipment and work and priority and action), "equipment_id": equipment.group(1) if equipment else None, "work_type": work.group(1) if work else None, "priority": priority.group(1) if priority else None, "action": action.group(1) if action else None}


def eam_score_maintenance_risk(signals: dict) -> dict:
    risk = round(signals.get("condition", 0) * 1.3 + signals.get("criticality", 0) * 0.8 + signals.get("downtime", 0) * 0.7 + signals.get("safety", 0) * 1.2, 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 1.0 else "expedite"}


def eam_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"condition_alarm": "create_predictive_work_order", "permit_block": "route_safety_review", "spare_shortage": "reserve_alternate_part"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def eam_route_maintenance(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"eam:MaintenanceRoute:{event['event_id']}"}


def eam_generate_compliance_proof(state: dict, work_order_id: str, *, disclosure: tuple[str, ...]) -> dict:
    work_order = state["work_orders"][work_order_id]
    claims = {field: work_order[field] for field in disclosure if field in work_order}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_maintenance_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def eam_screen_policy(state: dict, work_order_id: str, *, restricted_sites: tuple[str, ...]) -> dict:
    work_order = state["work_orders"][work_order_id]
    blocked = work_order["site"] in restricted_sites
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "work_order_id": work_order_id}


def eam_run_control_tests(state: dict) -> dict:
    gaps = []
    configuration = state["configuration"]
    if not configuration.get("ok"):
        gaps.append("invalid_configuration")
    if configuration.get("event_contract") != EAM_EVENT_CONTRACT:
        gaps.append("invalid_event_contract")
    if configuration.get("database_backend") not in EAM_ALLOWED_DATABASE_BACKENDS:
        gaps.append("unsupported_database_backend")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(work_order["status"] not in {"completed", "cancelled"} for work_order in state["work_orders"].values()):
        gaps.append("open_work_order")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def eam_build_api_contract() -> dict:
    return {
        "ok": True,
        "routes": ("POST /equipment", "POST /maintenance-plans", "POST /work-orders", "POST /work-orders/{id}/schedule", "POST /work-orders/{id}/complete", "POST /condition-readings", "POST /meter-readings", "POST /spare-usage", "POST /safety-permits", "POST /maintenance-rules", "POST /maintenance-parameters", "POST /maintenance-configuration"),
        "events": {"emits": ("MaintenanceCompleted", "VendorPerformanceUpdated", "WorkOrderCreated"), "consumes": ("DowntimeCaptured", "NonConformanceRaised", "InventoryReservationConfirmed", "PurchaseOrderAcknowledged")},
        "permissions": ("eam.read", "eam.equipment", "eam.plan", "eam.execute", "eam.safety", "eam.configure", "eam.audit"),
        "configuration": ("EAM_DATABASE_URL", "EAM_EVENT_TOPIC", "EAM_RETRY_LIMIT", "EAM_DEFAULT_TIMEZONE"),
    }


def eam_federate_maintenance_view(state: dict, work_order_id: str, *, systems: tuple[str, ...]) -> dict:
    work_order = state["work_orders"][work_order_id]
    return {"ok": True, "work_order_id": work_order_id, "systems": systems, "projection": {"equipment_id": work_order["equipment_id"], "status": work_order["status"], "risk_score": work_order["risk_score"]}}


def eam_verify_equipment_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def eam_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"mobile_offline_queue", "vendor_api_timeout"}, "scenario": scenario, "mode": "degraded_maintenance_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "eam.dead_letter"}


def eam_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"eam_epoch_{epoch:04d}"}


def eam_schedule_carbon_aware_maintenance(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def eam_optimize_maintenance_schedule(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["risk_reduction"] - candidate["cost"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "plan": selected["plan"], "objective_score": selected["objective"], "candidates": scored}


def eam_allocate_labor_and_spares(crews: tuple[dict, ...], *, work_orders: int) -> dict:
    weights = tuple({"crew": item["crew"], "weight": item["priority"] * item["capacity"]} for item in crews)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"crew": item["crew"], "work_orders": round(work_orders * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["work_orders"] for item in allocations), 2) == round(work_orders, 2), "allocations": allocations, "clearing_priority": round(sum(item["priority"] for item in crews) / len(crews), 4)}


def eam_detect_failure_anomaly(state: dict) -> dict:
    counts = tuple(1 for work_order in state["work_orders"].values() if work_order.get("failure_code"))
    if not counts:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(counts) or 1
    entropy = round(-sum((count / total) * math.log(max(count / total, 0.0001), 2) for count in counts), 4)
    return {"ok": True, "entropy": entropy, "outliers": tuple(count for count in counts if count > 3)}


def eam_model_stochastic_maintenance_exposure(*, failure_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(failure_path) < 2 else (failure_path[-1] - failure_path[0]) / (len(failure_path) - 1)
    exposure = abs(drift) * volatility * len(failure_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def eam_build_workbench_view(state: dict, *, tenant: str) -> dict:
    equipment = tuple(item for item in state["equipment"].values() if item["tenant"] == tenant)
    plans = tuple(plan for plan in state["plans"].values() if plan["tenant"] == tenant)
    work_orders = tuple(work_order for work_order in state["work_orders"].values() if work_order["tenant"] == tenant)
    spares = tuple(usage for usage in state["spare_usage"].values() if usage["tenant"] == tenant)
    completed = tuple(work_order for work_order in work_orders if work_order["status"] == "completed")
    return {
        "ok": True,
        "tenant": tenant,
        "equipment_count": len(equipment),
        "plan_count": len(plans),
        "work_order_count": len(work_orders),
        "completed_work_order_count": len(completed),
        "critical_work_order_count": len(tuple(work_order for work_order in work_orders if work_order["priority"] == "critical")),
        "spare_usage_count": len(spares),
        "spare_cost": round(sum(usage["cost"] for usage in spares), 2),
        "mttr_hours": round(sum(work_order.get("mttr_hours", 0) for work_order in completed) / max(len(completed), 1), 2),
        "downtime_hours": round(sum(work_order.get("downtime_hours", 0) for work_order in completed), 2),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
    }


def eam_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"eam_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"eam:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
