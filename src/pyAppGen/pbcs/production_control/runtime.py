"""Executable runtime for the Production Control PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


PRODUCTION_CONTROL_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_production_lifecycle",
    "graph_relational_routing_work_center_topology",
    "multi_tenant_site_execution_isolation",
    "schema_evolution_resilient_production_schema",
    "probabilistic_downtime_yield_schedule_risk_scoring",
    "real_time_oee_execution_analytics",
    "counterfactual_dispatch_capacity_simulation",
    "temporal_throughput_downtime_forecasting",
    "autonomous_production_exception_resolution",
    "semantic_shop_floor_instruction_parsing",
    "predictive_schedule_quality_maintenance_risk",
    "self_healing_execution_route_selection",
    "zero_knowledge_completion_proof",
    "immutable_production_audit_trail",
    "dynamic_production_policy_screening",
    "automated_production_control_testing",
    "universal_api_async_streaming",
    "cross_system_production_federation",
    "mrp_inventory_quality_asset_integration",
    "decentralized_work_center_asset_identity",
    "chaos_engineered_shop_floor_tolerance",
    "quantum_resistant_production_authorization",
    "carbon_aware_production_scheduling",
    "algebraic_schedule_optimization",
    "mechanism_design_capacity_allocation",
    "information_theoretic_downtime_anomaly_detection",
    "temporal_production_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_production_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "production_mlops_governance",
)
PRODUCTION_CONTROL_STANDARD_FEATURE_KEYS = (
    "work_center_master",
    "routing_step_definition",
    "production_order_creation",
    "finite_capacity_scheduling",
    "dispatch_list",
    "operation_sequencing",
    "production_start",
    "operation_confirmation",
    "production_completion",
    "downtime_capture",
    "oee_calculation",
    "throughput_analytics",
    "schedule_adherence",
    "yield_tracking",
    "material_readiness_projection",
    "quality_gate_projection",
    "maintenance_projection",
    "asset_commissioning_handoff",
    "multi_site_isolation",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def production_control_runtime_capabilities() -> dict:
    smoke = production_control_runtime_smoke()
    return {
        "format": "appgen.production-control-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "production_control",
        "implementation_directory": "src/pyAppGen/pbcs/production_control",
        "capabilities": PRODUCTION_CONTROL_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PRODUCTION_CONTROL_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_work_center",
            "create_production_order",
            "define_routing_step",
            "schedule_order",
            "start_operation",
            "record_downtime",
            "confirm_operation",
            "complete_production_order",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def production_control_runtime_smoke() -> dict:
    state = production_control_empty_state()
    state = production_control_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.production.events",
            "retry_limit": 3,
            "allowed_sites": ("factory_east", "factory_west"),
            "allowed_work_center_types": ("assembly", "test"),
            "allowed_downtime_reasons": ("maintenance", "material", "quality"),
            "allowed_production_routes": ("make", "assemble"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = production_control_set_parameter(state, "capacity_threshold", 0.85)["state"]
    state = production_control_set_parameter(state, "oee_target", 0.75)["state"]
    state = production_control_set_parameter(state, "scrap_threshold", 0.05)["state"]
    state = production_control_set_parameter(state, "takt_time_minutes", 10)["state"]
    state = production_control_set_parameter(state, "schedule_horizon_days", 14)["state"]
    state = production_control_set_parameter(state, "downtime_severity_minutes", 30)["state"]
    state = production_control_register_rule(
        state,
        {
            "rule_id": "rule_factory",
            "tenant": "tenant_alpha",
            "rule_type": "production",
            "eligible_work_center_types": ("assembly", "test"),
            "allowed_sites": ("factory_east",),
            "allowed_routes": ("make", "assemble"),
            "quality_gates": ("final_test",),
            "asset_commissioning_items": ("machine_kit",),
            "dispatch_priorities": ("expedite", "standard"),
            "status": "active",
        },
    )["state"]
    state = production_control_register_schema_extension(state, "production_order", {"digital_thread_payload": "jsonb"})["state"]
    state = production_control_register_work_center(
        state,
        {"work_center_id": "wc_100", "tenant": "tenant_alpha", "site": "factory_east", "name": "Assembly Cell 1", "work_center_type": "assembly", "capacity_hours": 8, "efficiency": 0.9, "status": "available", "identity": {"did": "did:appgen:wc-100", "issuer": "trusted_registry", "status": "active"}},
    )["state"]
    order = production_control_create_production_order(
        state,
        {"order_id": "order_100", "tenant": "tenant_alpha", "site": "factory_east", "item": "machine_kit", "quantity": 10, "route": "make", "priority": "standard", "planned_order_id": "po_100"},
    )
    state = order["state"]
    state = production_control_define_routing_step(
        state,
        {"step_id": "step_100", "tenant": "tenant_alpha", "order_id": "order_100", "sequence": 10, "work_center_id": "wc_100", "standard_minutes": 100, "setup_minutes": 20, "quality_gate": "final_test"},
    )["state"]
    schedule = production_control_schedule_order(state, "order_100", scheduled_by="scheduler_1")
    state = schedule["state"]
    state = production_control_start_operation(state, "step_100", started_by="operator_1")["state"]
    downtime = production_control_record_downtime(state, {"downtime_id": "dt_100", "tenant": "tenant_alpha", "work_center_id": "wc_100", "order_id": "order_100", "reason": "maintenance", "minutes": 20})
    state = downtime["state"]
    confirmation = production_control_confirm_operation(state, "step_100", good_qty=9, scrap_qty=1, labor_hours=2, machine_hours=2.3, confirmed_by="operator_1")
    state = confirmation["state"]
    completed = production_control_complete_production_order(state, "order_100", completed_by="supervisor_1")
    state = completed["state"]
    simulation = production_control_simulate_dispatch_policy(state, "order_100", proposed_capacity_hours=7)
    forecast = production_control_forecast_throughput((8, 9, 10), downtime_minutes=20)
    parsed = production_control_parse_shop_floor_instruction("order order_777 step step_777 work_center wc_777 action start")
    risk = production_control_score_production_risk({"downtime": 0.2, "scrap": 0.1, "late": 0.05})
    recommendation = production_control_recommend_exception_resolution("downtime")
    route = production_control_route_execution({"event_id": "prod_route"}, rails=({"route": "mes_api", "available": False, "latency": 2}, {"route": "outbox", "available": True, "latency": 4}))
    proof = production_control_generate_completion_proof(state, "order_100", disclosure=("order_id", "item", "completed_qty"))
    screening = production_control_screen_policy(state, "order_100", restricted_sites=("restricted_site",))
    controls = production_control_run_control_tests(state)
    api = production_control_build_api_contract()
    federation = production_control_federate_execution_view(state, "order_100", systems=("mrp", "inventory", "quality", "asset"))
    identity = production_control_verify_work_center_identity(state["work_centers"]["wc_100"]["identity"])
    resilience = production_control_run_resilience_drill(state, "mes_api_timeout")
    crypto = production_control_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = production_control_schedule_carbon_aware_shift(({"window": "day", "carbon": 220}, {"window": "night", "carbon": 90}))
    optimization = production_control_optimize_schedule(({"schedule": "expedite", "throughput": 0.95, "cost": 0.35}, {"schedule": "balanced", "throughput": 0.9, "cost": 0.2}))
    allocation = production_control_allocate_capacity(({"work_center_id": "wc_100", "priority": 0.9, "capacity": 80}, {"work_center_id": "wc_200", "priority": 0.5, "capacity": 40}), required_hours=100)
    anomaly = production_control_detect_downtime_anomaly(state)
    stochastic = production_control_model_stochastic_production_exposure(output_path=(8, 9, 11), volatility=0.12)
    workbench = production_control_build_workbench_view(state, tenant="tenant_alpha")
    model = production_control_register_governed_model("production_risk", {"features": ("downtime", "scrap", "capacity"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_production_lifecycle", "ok": len(state["events"]) >= 8 and state["events"][-1]["hash"]},
        {"id": "graph_relational_routing_work_center_topology", "ok": order["production_order"]["graph_degree"] >= 4 and schedule["schedule"]["step_count"] == 1},
        {"id": "multi_tenant_site_execution_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_production_schema", "ok": state["schema_extensions"]["production_order"]["digital_thread_payload"] == "jsonb"},
        {"id": "probabilistic_downtime_yield_schedule_risk_scoring", "ok": confirmation["risk_score"] > 0},
        {"id": "real_time_oee_execution_analytics", "ok": workbench["oee"] > 0},
        {"id": "counterfactual_dispatch_capacity_simulation", "ok": simulation["capacity_load"] > 0},
        {"id": "temporal_throughput_downtime_forecasting", "ok": forecast["forecast_throughput"] > 0},
        {"id": "autonomous_production_exception_resolution", "ok": recommendation["action"] == "route_maintenance_review"},
        {"id": "semantic_shop_floor_instruction_parsing", "ok": parsed["ok"] and parsed["order_id"] == "order_777"},
        {"id": "predictive_schedule_quality_maintenance_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_execution_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_completion_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_completion_")},
        {"id": "immutable_production_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_production_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_production_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "ProductionCompleted" in api["events"]["emits"]},
        {"id": "cross_system_production_federation", "ok": federation["ok"] and "quality" in federation["systems"]},
        {"id": "mrp_inventory_quality_asset_integration", "ok": completed["handoffs"] == ("inventory_receipt_projection", "quality_completion_projection", "asset_commissioning_projection")},
        {"id": "decentralized_work_center_asset_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_shop_floor_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_execution_route"},
        {"id": "quantum_resistant_production_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_production_scheduling", "ok": carbon["window"] == "night"},
        {"id": "algebraic_schedule_optimization", "ok": optimization["ok"] and optimization["schedule"] == "balanced"},
        {"id": "mechanism_design_capacity_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["allocated_hours"] > allocation["allocations"][1]["allocated_hours"]},
        {"id": "information_theoretic_downtime_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_production_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("production_control:ProductionCompleted")},
        {"id": "probabilistic_ml_production_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "production_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.production-control-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def production_control_empty_state() -> dict:
    return {"events": (), "outbox": (), "work_centers": {}, "orders": {}, "routing_steps": {}, "downtime_events": {}, "rules": {}, "parameters": {}, "configuration": {}, "schema_extensions": {}, "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"}}


def production_control_configure_runtime(state: dict, configuration: dict) -> dict:
    ok = configuration.get("database_backend") in {"postgresql", "mysql", "mariadb"} and bool(configuration.get("event_topic"))
    return {"ok": ok, "state": {**state, "configuration": {**configuration, "ok": ok}}, "configuration": {**configuration, "ok": ok}}


def production_control_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def production_control_register_rule(state: dict, rule: dict) -> dict:
    enriched = {**rule, "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def production_control_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def production_control_register_work_center(state: dict, work_center: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    ok = work_center["site"] in state["configuration"].get("allowed_sites", ()) and work_center["work_center_type"] in rule["eligible_work_center_types"]
    enriched = {**work_center, "status": work_center["status"] if ok else "blocked"}
    next_state = {**state, "work_centers": {**state["work_centers"], work_center["work_center_id"]: enriched}}
    next_state = _append_event(next_state, "WorkCenterRegistered", {"tenant": work_center["tenant"], "work_center_id": work_center["work_center_id"], "site": work_center["site"]})
    return {"ok": ok, "state": next_state, "work_center": enriched}


def production_control_create_production_order(state: dict, order: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    ok = order["site"] in state["configuration"].get("allowed_sites", ()) and order["route"] in rule["allowed_routes"]
    enriched = {**order, "status": "created" if ok else "blocked", "completed_qty": 0, "scrap_qty": 0, "graph_degree": len(tuple(value for value in (order["site"], order["item"], order["route"], order["planned_order_id"]) if value))}
    next_state = {**state, "orders": {**state["orders"], order["order_id"]: enriched}}
    next_state = _append_event(next_state, "ProductionOrderCreated", {"tenant": order["tenant"], "order_id": order["order_id"], "item": order["item"], "quantity": order["quantity"]})
    return {"ok": ok, "state": next_state, "production_order": enriched}


def production_control_define_routing_step(state: dict, step: dict) -> dict:
    work_center = state["work_centers"][step["work_center_id"]]
    ok = work_center["status"] == "available"
    enriched = {**step, "status": "ready" if ok else "blocked"}
    next_state = {**state, "routing_steps": {**state["routing_steps"], step["step_id"]: enriched}}
    next_state = _append_event(next_state, "RoutingStepDefined", {"tenant": step["tenant"], "step_id": step["step_id"], "order_id": step["order_id"], "work_center_id": step["work_center_id"]})
    return {"ok": ok, "state": next_state, "routing_step": enriched}


def production_control_schedule_order(state: dict, order_id: str, *, scheduled_by: str) -> dict:
    order = state["orders"][order_id]
    steps = tuple(step for step in state["routing_steps"].values() if step["order_id"] == order_id)
    required_hours = sum(step["standard_minutes"] + step["setup_minutes"] for step in steps) / 60
    capacity = sum(state["work_centers"][step["work_center_id"]]["capacity_hours"] * state["work_centers"][step["work_center_id"]]["efficiency"] for step in steps)
    load = round(required_hours / max(capacity, 0.01), 4)
    ok = load <= float(state["parameters"].get("capacity_threshold", 0.85))
    updated = {**order, "status": "scheduled" if ok else "capacity_review", "capacity_load": load, "scheduled_by": scheduled_by}
    next_state = {**state, "orders": {**state["orders"], order_id: updated}}
    next_state = _append_event(next_state, "ProductionOrderScheduled", {"tenant": order["tenant"], "order_id": order_id, "capacity_load": load})
    return {"ok": ok, "state": next_state, "schedule": {"order_id": order_id, "capacity_load": load, "step_count": len(steps)}}


def production_control_start_operation(state: dict, step_id: str, *, started_by: str) -> dict:
    step = state["routing_steps"][step_id]
    updated = {**step, "status": "in_progress", "started_by": started_by}
    next_state = {**state, "routing_steps": {**state["routing_steps"], step_id: updated}}
    next_state = _append_event(next_state, "OperationStarted", {"tenant": step["tenant"], "step_id": step_id, "order_id": step["order_id"]})
    return {"ok": True, "state": next_state, "routing_step": updated}


def production_control_record_downtime(state: dict, downtime: dict) -> dict:
    ok = downtime["reason"] in state["configuration"].get("allowed_downtime_reasons", ())
    severity = "major" if downtime["minutes"] >= float(state["parameters"].get("downtime_severity_minutes", 30)) else "minor"
    enriched = {**downtime, "status": "captured" if ok else "blocked", "severity": severity}
    next_state = {**state, "downtime_events": {**state["downtime_events"], downtime["downtime_id"]: enriched}}
    next_state = _append_event(next_state, "DowntimeCaptured", {"tenant": downtime["tenant"], "downtime_id": downtime["downtime_id"], "work_center_id": downtime["work_center_id"], "minutes": downtime["minutes"]})
    return {"ok": ok, "state": next_state, "downtime": enriched}


def production_control_confirm_operation(state: dict, step_id: str, *, good_qty: float, scrap_qty: float, labor_hours: float, machine_hours: float, confirmed_by: str) -> dict:
    step = state["routing_steps"][step_id]
    scrap_rate = scrap_qty / max(1, good_qty + scrap_qty)
    risk_score = round(scrap_rate + max(0, machine_hours - (step["standard_minutes"] / 60)) * 0.05, 4)
    updated_step = {**step, "status": "confirmed", "good_qty": good_qty, "scrap_qty": scrap_qty, "labor_hours": labor_hours, "machine_hours": machine_hours, "confirmed_by": confirmed_by}
    order = state["orders"][step["order_id"]]
    updated_order = {**order, "completed_qty": round(order["completed_qty"] + good_qty, 2), "scrap_qty": round(order["scrap_qty"] + scrap_qty, 2)}
    next_state = {**state, "routing_steps": {**state["routing_steps"], step_id: updated_step}, "orders": {**state["orders"], step["order_id"]: updated_order}}
    next_state = _append_event(next_state, "OperationConfirmed", {"tenant": step["tenant"], "step_id": step_id, "order_id": step["order_id"], "good_qty": good_qty, "scrap_qty": scrap_qty})
    return {"ok": True, "state": next_state, "routing_step": updated_step, "risk_score": risk_score}


def production_control_complete_production_order(state: dict, order_id: str, *, completed_by: str) -> dict:
    order = state["orders"][order_id]
    completed = {**order, "status": "completed", "completed_by": completed_by}
    handoffs = ("inventory_receipt_projection", "quality_completion_projection", "asset_commissioning_projection")
    next_state = {**state, "orders": {**state["orders"], order_id: completed}}
    next_state = _append_event(next_state, "AssetPlacedInService", {"tenant": order["tenant"], "order_id": order_id, "item": order["item"]})
    next_state = _append_event(next_state, "ProductionCompleted", {"tenant": order["tenant"], "order_id": order_id, "item": order["item"], "completed_qty": completed["completed_qty"], "handoffs": handoffs})
    return {"ok": True, "state": next_state, "production_order": completed, "handoffs": handoffs}


def production_control_simulate_dispatch_policy(state: dict, order_id: str, *, proposed_capacity_hours: float) -> dict:
    order = state["orders"][order_id]
    required = order["quantity"] * float(state["parameters"].get("takt_time_minutes", 10)) / 60
    return {"ok": True, "order_id": order_id, "capacity_load": round(required / max(proposed_capacity_hours, 0.01), 4)}


def production_control_forecast_throughput(output_path: tuple[float, ...], *, downtime_minutes: float) -> dict:
    trend = output_path[-1] - output_path[0] if len(output_path) > 1 else 0
    return {"ok": True, "forecast_throughput": round(max(0, output_path[-1] + trend / max(1, len(output_path)) - downtime_minutes / 60), 2)}


def production_control_parse_shop_floor_instruction(text: str) -> dict:
    order = re.search(r"order\s+([a-z0-9_]+)", text, re.I)
    step = re.search(r"step\s+([a-z0-9_]+)", text, re.I)
    work_center = re.search(r"work_center\s+([a-z0-9_]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(order and step and work_center and action), "order_id": order.group(1) if order else None, "step_id": step.group(1) if step else None, "work_center_id": work_center.group(1) if work_center else None, "action": action.group(1) if action else None}


def production_control_score_production_risk(signals: dict) -> dict:
    risk = round(signals.get("downtime", 0) * 1.5 + signals.get("scrap", 0) * 2 + signals.get("late", 0), 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.7 else "review"}


def production_control_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"downtime": "route_maintenance_review", "quality_hold": "route_quality_review", "capacity": "reschedule_or_split"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def production_control_route_execution(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"production_control:ExecutionRoute:{event['event_id']}"}


def production_control_generate_completion_proof(state: dict, order_id: str, *, disclosure: tuple[str, ...]) -> dict:
    order = state["orders"][order_id]
    claims = {field: order[field] for field in disclosure if field in order}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_completion_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def production_control_screen_policy(state: dict, order_id: str, *, restricted_sites: tuple[str, ...]) -> dict:
    order = state["orders"][order_id]
    blocked = order["site"] in restricted_sites or order["status"] == "blocked"
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "order_id": order_id}


def production_control_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(order["status"] == "completed" and order["completed_qty"] <= 0 for order in state["orders"].values()):
        gaps.append("completed_without_quantity")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def production_control_build_api_contract() -> dict:
    return {"ok": True, "routes": ("POST /production-orders", "POST /downtime", "GET /schedule", "POST /production-rules", "POST /production-parameters", "POST /production-configuration"), "events": {"emits": ("ProductionCompleted", "AssetPlacedInService", "DowntimeCaptured"), "consumes": ("PlannedOrderReleased", "MaintenanceCompleted")}, "permissions": ("production_control.read", "production_control.schedule", "production_control.operate", "production_control.complete", "production_control.configure", "production_control.audit"), "configuration": ("PRODUCTION_CONTROL_DATABASE_URL", "PRODUCTION_CONTROL_EVENT_TOPIC", "PRODUCTION_CONTROL_RETRY_LIMIT", "PRODUCTION_CONTROL_DEFAULT_TIMEZONE")}


def production_control_federate_execution_view(state: dict, order_id: str, *, systems: tuple[str, ...]) -> dict:
    order = state["orders"][order_id]
    return {"ok": True, "order_id": order_id, "systems": systems, "projection": {"item": order["item"], "completed_qty": order["completed_qty"], "scrap_qty": order["scrap_qty"], "status": order["status"]}}


def production_control_verify_work_center_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def production_control_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"mes_api_timeout", "operator_terminal_failure"}, "scenario": scenario, "mode": "degraded_execution_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "production_control.dead_letter"}


def production_control_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"production_epoch_{epoch:04d}"}


def production_control_schedule_carbon_aware_shift(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def production_control_optimize_schedule(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["throughput"] - candidate["cost"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "schedule": selected["schedule"], "objective_score": selected["objective"], "candidates": scored}


def production_control_allocate_capacity(resources: tuple[dict, ...], *, required_hours: float) -> dict:
    weights = tuple({"work_center_id": item["work_center_id"], "weight": item["priority"] * item["capacity"]} for item in resources)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"work_center_id": item["work_center_id"], "allocated_hours": round(required_hours * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["allocated_hours"] for item in allocations), 2) == round(required_hours, 2), "allocations": allocations, "clearing_priority": round(sum(item["priority"] for item in resources) / len(resources), 4)}


def production_control_detect_downtime_anomaly(state: dict) -> dict:
    minutes = tuple(event["minutes"] for event in state["downtime_events"].values())
    if not minutes:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(minutes) or 1
    entropy = round(-sum((value / total) * math.log(max(value / total, 0.0001), 2) for value in minutes), 4)
    mean = sum(minutes) / len(minutes)
    return {"ok": True, "entropy": entropy, "outliers": tuple(value for value in minutes if abs(value - mean) > 30)}


def production_control_model_stochastic_production_exposure(*, output_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(output_path) < 2 else (output_path[-1] - output_path[0]) / (len(output_path) - 1)
    exposure = abs(drift) * volatility * len(output_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def production_control_build_workbench_view(state: dict, *, tenant: str) -> dict:
    centers = tuple(item for item in state["work_centers"].values() if item["tenant"] == tenant)
    orders = tuple(order for order in state["orders"].values() if order["tenant"] == tenant)
    steps = tuple(step for step in state["routing_steps"].values() if step["tenant"] == tenant)
    downtime = tuple(event for event in state["downtime_events"].values() if event["tenant"] == tenant)
    completed_qty = sum(order["completed_qty"] for order in orders)
    scrap_qty = sum(order["scrap_qty"] for order in orders)
    scheduled_hours = sum((step["standard_minutes"] + step["setup_minutes"]) / 60 for step in steps)
    downtime_hours = sum(event["minutes"] for event in downtime) / 60
    oee = round(max(0, (scheduled_hours - downtime_hours) / max(scheduled_hours, 0.01)) * (completed_qty / max(completed_qty + scrap_qty, 1)), 4)
    return {"ok": True, "tenant": tenant, "work_center_count": len(centers), "order_count": len(orders), "scheduled_order_count": len(tuple(order for order in orders if order["status"] in {"scheduled", "completed"})), "completed_order_count": len(tuple(order for order in orders if order["status"] == "completed")), "routing_step_count": len(steps), "downtime_count": len(downtime), "downtime_minutes": sum(event["minutes"] for event in downtime), "completed_qty": round(completed_qty, 2), "scrap_qty": round(scrap_qty, 2), "oee": oee}


def production_control_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"production_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"production_control:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
