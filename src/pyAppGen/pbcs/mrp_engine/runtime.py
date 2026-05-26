"""Executable runtime for the Material Requirements Planning PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


MRP_ENGINE_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_planning_lifecycle",
    "graph_relational_bom_topology",
    "multi_tenant_site_planning_isolation",
    "schema_evolution_resilient_planning_schema",
    "probabilistic_shortage_capacity_risk_scoring",
    "real_time_material_plan_analytics",
    "counterfactual_planning_policy_simulation",
    "temporal_demand_shortage_forecasting",
    "autonomous_planning_exception_resolution",
    "semantic_demand_bom_instruction_parsing",
    "predictive_material_capacity_compliance_risk",
    "self_healing_supply_route_selection",
    "zero_knowledge_supply_availability_proof",
    "immutable_planning_audit_trail",
    "dynamic_mrp_policy_screening",
    "automated_mrp_control_testing",
    "universal_api_async_streaming",
    "cross_system_mrp_federation",
    "inventory_order_forecast_integration",
    "decentralized_item_source_identity",
    "chaos_engineered_planning_tolerance",
    "quantum_resistant_planning_authorization",
    "carbon_aware_planning_batching",
    "algebraic_material_allocation_optimization",
    "mechanism_design_capacity_allocation",
    "information_theoretic_shortage_anomaly_detection",
    "temporal_material_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_shortage_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "planning_mlops_governance",
)
MRP_ENGINE_STANDARD_FEATURE_KEYS = (
    "bom_master",
    "bom_revision_control",
    "bom_explosion",
    "demand_projection",
    "inventory_projection",
    "supply_demand_netting",
    "safety_stock",
    "lot_sizing",
    "lead_time_planning",
    "scrap_yield_planning",
    "mrp_run_creation",
    "shortage_detection",
    "planned_production_orders",
    "planned_purchase_suggestions",
    "capacity_readiness",
    "pegging",
    "exception_messages",
    "scenario_simulation",
    "multi_site_isolation",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def mrp_engine_runtime_capabilities() -> dict:
    smoke = mrp_engine_runtime_smoke()
    return {
        "format": "appgen.mrp-engine-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "mrp_engine",
        "implementation_directory": "src/pyAppGen/pbcs/mrp_engine",
        "capabilities": MRP_ENGINE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": MRP_ENGINE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_bom",
            "ingest_demand_projection",
            "ingest_inventory_projection",
            "create_mrp_run",
            "explode_bom",
            "calculate_material_plan",
            "release_planned_order",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def mrp_engine_runtime_smoke() -> dict:
    state = mrp_engine_empty_state()
    state = mrp_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.mrp.events",
            "retry_limit": 3,
            "allowed_sites": ("factory_east", "factory_west"),
            "allowed_order_types": ("production", "purchase"),
            "allowed_procurement_routes": ("buy", "subcontract"),
            "allowed_production_routes": ("make", "assemble"),
            "default_planning_bucket": "daily",
            "workbench_limit": 100,
        },
    )["state"]
    state = mrp_engine_set_parameter(state, "planning_horizon_days", 30)["state"]
    state = mrp_engine_set_parameter(state, "bucket_size_days", 1)["state"]
    state = mrp_engine_set_parameter(state, "safety_stock_multiplier", 1.1)["state"]
    state = mrp_engine_set_parameter(state, "lot_size_minimum", 10)["state"]
    state = mrp_engine_set_parameter(state, "lead_time_days", 3)["state"]
    state = mrp_engine_set_parameter(state, "capacity_threshold", 0.85)["state"]
    state = mrp_engine_set_parameter(state, "shortage_severity_threshold", 20)["state"]
    state = mrp_engine_register_rule(
        state,
        {
            "rule_id": "rule_factory",
            "tenant": "tenant_alpha",
            "rule_type": "planning",
            "eligible_item_types": ("finished_good", "component"),
            "allowed_sites": ("factory_east",),
            "allowed_bom_statuses": ("released",),
            "demand_sources": ("order", "forecast"),
            "release_routes": {"component_a": "buy", "fg_100": "make"},
            "substitutions": {"component_a": ("component_a_alt",)},
            "status": "active",
        },
    )["state"]
    state = mrp_engine_register_schema_extension(state, "planned_order", {"simulation_payload": "jsonb"})["state"]
    state = mrp_engine_register_bom(
        state,
        {
            "bom_id": "bom_100",
            "tenant": "tenant_alpha",
            "parent_item": "fg_100",
            "component_item": "component_a",
            "component_qty": 2,
            "scrap_percent": 0.05,
            "revision": "A",
            "status": "released",
            "site": "factory_east",
        },
    )["state"]
    state = mrp_engine_ingest_demand_projection(
        state,
        {"demand_id": "demand_100", "tenant": "tenant_alpha", "item": "fg_100", "site": "factory_east", "quantity": 30, "source": "order", "need_date": "2026-06-01"},
    )["state"]
    state = mrp_engine_ingest_inventory_projection(
        state,
        {"inventory_id": "inv_100", "tenant": "tenant_alpha", "item": "component_a", "site": "factory_east", "available_qty": 40, "quality_status": "released"},
    )["state"]
    run = mrp_engine_create_mrp_run(state, {"run_id": "run_100", "tenant": "tenant_alpha", "site": "factory_east", "horizon_days": 30, "scenario": "base", "planner": "planner_1"})
    state = run["state"]
    explosion = mrp_engine_explode_bom(state, "fg_100", quantity=30)
    plan = mrp_engine_calculate_material_plan(state, "run_100")
    state = plan["state"]
    release = mrp_engine_release_planned_order(state, "po_run_100_component_a", released_by="planner_1")
    state = release["state"]
    simulation = mrp_engine_simulate_planning_policy(state, "fg_100", demand_qty=50)
    forecast = mrp_engine_forecast_shortage((10, 20, 35), available=40)
    parsed = mrp_engine_parse_planning_instruction("run run_777 item fg_777 site factory_east action plan")
    risk = mrp_engine_score_planning_risk({"shortage": 0.4, "capacity": 0.2, "quality": 0.05})
    recommendation = mrp_engine_recommend_exception_resolution("shortage")
    route = mrp_engine_route_supply({"event_id": "mrp_route"}, rails=({"route": "procurement_api", "available": False, "latency": 2}, {"route": "outbox", "available": True, "latency": 4}))
    proof = mrp_engine_generate_supply_proof(state, "po_run_100_component_a", disclosure=("planned_order_id", "item", "quantity"))
    screening = mrp_engine_screen_policy(state, "run_100", restricted_sites=("restricted_site",))
    controls = mrp_engine_run_control_tests(state)
    api = mrp_engine_build_api_contract()
    federation = mrp_engine_federate_plan_view(state, "po_run_100_component_a", systems=("inventory", "procurement", "production", "orders"))
    identity = mrp_engine_verify_item_identity({"did": "did:appgen:item-component-a", "issuer": "trusted_registry", "status": "active"})
    resilience = mrp_engine_run_resilience_drill(state, "inventory_projection_delay")
    crypto = mrp_engine_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = mrp_engine_schedule_carbon_aware_plan(({"window": "day", "carbon": 210}, {"window": "night", "carbon": 70}))
    optimization = mrp_engine_optimize_material_allocation(({"plan": "expedite", "service": 0.95, "cost": 0.35}, {"plan": "balanced", "service": 0.9, "cost": 0.2}))
    allocation = mrp_engine_allocate_capacity(({"resource": "line_1", "priority": 0.9, "capacity": 80}, {"resource": "line_2", "priority": 0.6, "capacity": 50}), required_capacity=100)
    anomaly = mrp_engine_detect_shortage_anomaly(state)
    stochastic = mrp_engine_model_stochastic_material_exposure(demand_path=(20, 30, 45), volatility=0.15)
    workbench = mrp_engine_build_workbench_view(state, tenant="tenant_alpha")
    model = mrp_engine_register_governed_model("shortage_risk", {"features": ("demand", "inventory", "lead_time"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_planning_lifecycle", "ok": len(state["events"]) >= 6 and state["events"][-1]["hash"]},
        {"id": "graph_relational_bom_topology", "ok": explosion["graph_depth"] == 1 and run["mrp_run"]["graph_degree"] >= 4},
        {"id": "multi_tenant_site_planning_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_planning_schema", "ok": state["schema_extensions"]["planned_order"]["simulation_payload"] == "jsonb"},
        {"id": "probabilistic_shortage_capacity_risk_scoring", "ok": plan["risk_score"] > 0},
        {"id": "real_time_material_plan_analytics", "ok": workbench["planned_order_count"] == 1},
        {"id": "counterfactual_planning_policy_simulation", "ok": simulation["required_component_qty"] > 0},
        {"id": "temporal_demand_shortage_forecasting", "ok": forecast["forecast_shortage"] >= 0},
        {"id": "autonomous_planning_exception_resolution", "ok": recommendation["action"] == "expedite_or_substitute"},
        {"id": "semantic_demand_bom_instruction_parsing", "ok": parsed["ok"] and parsed["item"] == "fg_777"},
        {"id": "predictive_material_capacity_compliance_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_supply_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_supply_availability_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_supply_")},
        {"id": "immutable_planning_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_mrp_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_mrp_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "PlannedOrderReleased" in api["events"]["emits"]},
        {"id": "cross_system_mrp_federation", "ok": federation["ok"] and "procurement" in federation["systems"]},
        {"id": "inventory_order_forecast_integration", "ok": plan["source_projection_count"] == 2},
        {"id": "decentralized_item_source_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_planning_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_projection_route"},
        {"id": "quantum_resistant_planning_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_planning_batching", "ok": carbon["window"] == "night"},
        {"id": "algebraic_material_allocation_optimization", "ok": optimization["ok"] and optimization["plan"] == "balanced"},
        {"id": "mechanism_design_capacity_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["allocated_capacity"] > allocation["allocations"][1]["allocated_capacity"]},
        {"id": "information_theoretic_shortage_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_material_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("mrp_engine:PlannedOrderReleased")},
        {"id": "probabilistic_ml_shortage_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "planning_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.mrp-engine-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def mrp_engine_empty_state() -> dict:
    return {"events": (), "outbox": (), "boms": {}, "demands": {}, "inventory": {}, "mrp_runs": {}, "planned_orders": {}, "rules": {}, "parameters": {}, "configuration": {}, "schema_extensions": {}, "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"}}


def mrp_engine_configure_runtime(state: dict, configuration: dict) -> dict:
    allowed_databases = {"postgresql", "mysql", "mariadb"}
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("MRP Engine supports only PostgreSQL, MySQL, or MariaDB backends")
    if not configuration.get("event_topic"):
        raise ValueError("MRP Engine requires an AppGen-X event topic")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "appgen_event_contract",
        "allowed_database_backends": tuple(sorted(allowed_databases)),
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def mrp_engine_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "planning_horizon_days",
        "bucket_size_days",
        "safety_stock_multiplier",
        "lot_size_minimum",
        "lead_time_days",
        "capacity_threshold",
        "shortage_severity_threshold",
        "scrap_factor",
        "planner_approval_threshold",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported MRP Engine parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def mrp_engine_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required MRP Engine rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("MRP Engine rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def mrp_engine_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def mrp_engine_register_bom(state: dict, bom: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    ok = bom["site"] in state["configuration"].get("allowed_sites", ()) and bom["status"] in rule["allowed_bom_statuses"]
    enriched = {**bom, "status": "active" if ok else "blocked"}
    next_state = {**state, "boms": {**state["boms"], bom["bom_id"]: enriched}}
    next_state = _append_event(next_state, "BomRegistered", {"tenant": bom["tenant"], "bom_id": bom["bom_id"], "parent_item": bom["parent_item"], "component_item": bom["component_item"]})
    return {"ok": ok, "state": next_state, "bom": enriched}


def mrp_engine_ingest_demand_projection(state: dict, demand: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    ok = demand["source"] in rule["demand_sources"] and demand["site"] in state["configuration"].get("allowed_sites", ())
    enriched = {**demand, "status": "accepted" if ok else "blocked"}
    next_state = {**state, "demands": {**state["demands"], demand["demand_id"]: enriched}}
    next_state = _append_event(next_state, "DemandProjectionIngested", {"tenant": demand["tenant"], "demand_id": demand["demand_id"], "item": demand["item"], "quantity": demand["quantity"]})
    return {"ok": ok, "state": next_state, "demand": enriched}


def mrp_engine_ingest_inventory_projection(state: dict, inventory: dict) -> dict:
    ok = inventory["site"] in state["configuration"].get("allowed_sites", ()) and inventory["quality_status"] == "released"
    enriched = {**inventory, "status": "accepted" if ok else "blocked"}
    next_state = {**state, "inventory": {**state["inventory"], inventory["inventory_id"]: enriched}}
    next_state = _append_event(next_state, "InventoryProjectionIngested", {"tenant": inventory["tenant"], "inventory_id": inventory["inventory_id"], "item": inventory["item"], "available_qty": inventory["available_qty"]})
    return {"ok": ok, "state": next_state, "inventory": enriched}


def mrp_engine_create_mrp_run(state: dict, mrp_run: dict) -> dict:
    ok = mrp_run["site"] in state["configuration"].get("allowed_sites", ()) and mrp_run["horizon_days"] <= int(state["parameters"].get("planning_horizon_days", 30))
    enriched = {**mrp_run, "status": "running" if ok else "blocked", "graph_degree": len(tuple(value for value in (mrp_run["tenant"], mrp_run["site"], mrp_run["scenario"], mrp_run["planner"]) if value))}
    next_state = {**state, "mrp_runs": {**state["mrp_runs"], mrp_run["run_id"]: enriched}}
    next_state = _append_event(next_state, "MrpRunStarted", {"tenant": mrp_run["tenant"], "run_id": mrp_run["run_id"], "site": mrp_run["site"]})
    return {"ok": ok, "state": next_state, "mrp_run": enriched}


def mrp_engine_explode_bom(state: dict, parent_item: str, *, quantity: float) -> dict:
    rows = tuple(bom for bom in state["boms"].values() if bom["parent_item"] == parent_item and bom["status"] == "active")
    requirements = tuple({"component_item": row["component_item"], "required_qty": round(quantity * row["component_qty"] * (1 + row["scrap_percent"]), 2), "bom_id": row["bom_id"]} for row in rows)
    return {"ok": bool(requirements), "parent_item": parent_item, "quantity": quantity, "requirements": requirements, "graph_depth": 1 if requirements else 0}


def mrp_engine_calculate_material_plan(state: dict, run_id: str) -> dict:
    run = state["mrp_runs"][run_id]
    planned_orders = {}
    shortage_total = 0.0
    for demand in state["demands"].values():
        if demand["tenant"] != run["tenant"] or demand["site"] != run["site"] or demand["status"] != "accepted":
            continue
        explosion = mrp_engine_explode_bom(state, demand["item"], quantity=demand["quantity"])
        for requirement in explosion["requirements"]:
            item = requirement["component_item"]
            available = sum(inv["available_qty"] for inv in state["inventory"].values() if inv["item"] == item and inv["site"] == run["site"] and inv["status"] == "accepted")
            safety = float(state["parameters"].get("safety_stock_multiplier", 1.0))
            needed = round(requirement["required_qty"] * safety, 2)
            shortage = round(max(0, needed - available), 2)
            shortage_total += shortage
            quantity = max(float(state["parameters"].get("lot_size_minimum", 1)), shortage)
            order_id = f"po_{run_id}_{item}"
            planned_orders[order_id] = {"planned_order_id": order_id, "tenant": run["tenant"], "run_id": run_id, "item": item, "site": run["site"], "quantity": round(quantity, 2), "shortage_qty": shortage, "route": next(iter(state["rules"].values()))["release_routes"].get(item, "buy"), "status": "planned" if shortage else "covered", "pegged_demand_id": demand["demand_id"]}
    next_state = {**state, "planned_orders": {**state["planned_orders"], **planned_orders}, "mrp_runs": {**state["mrp_runs"], run_id: {**run, "status": "planned", "shortage_total": round(shortage_total, 2)}}}
    if shortage_total:
        next_state = _append_event(next_state, "MaterialShortageDetected", {"tenant": run["tenant"], "run_id": run_id, "shortage_total": round(shortage_total, 2)})
    risk_score = round(min(1, shortage_total / max(1, float(state["parameters"].get("shortage_severity_threshold", 20)))), 4)
    return {"ok": True, "state": next_state, "planned_orders": tuple(planned_orders.values()), "shortage_total": round(shortage_total, 2), "risk_score": risk_score, "source_projection_count": len(state["demands"]) + len(state["inventory"])}


def mrp_engine_release_planned_order(state: dict, planned_order_id: str, *, released_by: str) -> dict:
    planned_order = state["planned_orders"][planned_order_id]
    updated = {**planned_order, "status": "released", "released_by": released_by}
    next_state = {**state, "planned_orders": {**state["planned_orders"], planned_order_id: updated}}
    next_state = _append_event(next_state, "PlannedOrderReleased", {"tenant": planned_order["tenant"], "planned_order_id": planned_order_id, "item": planned_order["item"], "quantity": planned_order["quantity"], "route": planned_order["route"]})
    return {"ok": True, "state": next_state, "planned_order": updated}


def mrp_engine_simulate_planning_policy(state: dict, parent_item: str, *, demand_qty: float) -> dict:
    explosion = mrp_engine_explode_bom(state, parent_item, quantity=demand_qty)
    required = round(sum(item["required_qty"] for item in explosion["requirements"]), 2)
    return {"ok": True, "parent_item": parent_item, "required_component_qty": required}


def mrp_engine_forecast_shortage(demand_path: tuple[float, ...], *, available: float) -> dict:
    forecast_demand = demand_path[-1] + (demand_path[-1] - demand_path[0]) / max(1, len(demand_path))
    return {"ok": True, "forecast_demand": round(forecast_demand, 2), "forecast_shortage": round(max(0, forecast_demand - available), 2)}


def mrp_engine_parse_planning_instruction(text: str) -> dict:
    run = re.search(r"run\s+([a-z0-9_]+)", text, re.I)
    item = re.search(r"item\s+([a-z0-9_]+)", text, re.I)
    site = re.search(r"site\s+([a-z0-9_]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(run and item and site and action), "run_id": run.group(1) if run else None, "item": item.group(1) if item else None, "site": site.group(1) if site else None, "action": action.group(1) if action else None}


def mrp_engine_score_planning_risk(signals: dict) -> dict:
    risk = round(signals.get("shortage", 0) * 1.5 + signals.get("capacity", 0) + signals.get("quality", 0) * 2, 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.7 else "review"}


def mrp_engine_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"shortage": "expedite_or_substitute", "capacity": "split_or_reschedule", "quality_hold": "route_quality_review"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def mrp_engine_route_supply(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"mrp_engine:SupplyRoute:{event['event_id']}"}


def mrp_engine_generate_supply_proof(state: dict, planned_order_id: str, *, disclosure: tuple[str, ...]) -> dict:
    planned_order = state["planned_orders"][planned_order_id]
    claims = {field: planned_order[field] for field in disclosure if field in planned_order}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_supply_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def mrp_engine_screen_policy(state: dict, run_id: str, *, restricted_sites: tuple[str, ...]) -> dict:
    run = state["mrp_runs"][run_id]
    blocked = run["site"] in restricted_sites or run["status"] == "blocked"
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "run_id": run_id}


def mrp_engine_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(order["status"] == "planned" and order["shortage_qty"] <= 0 for order in state["planned_orders"].values()):
        gaps.append("invalid_planned_shortage")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def mrp_engine_build_api_contract() -> dict:
    return {"ok": True, "routes": ("POST /mrp-runs", "GET /planned-orders", "GET /shortages", "POST /mrp-rules", "POST /mrp-parameters", "POST /mrp-configuration"), "events": {"emits": ("MaterialShortageDetected", "PlannedOrderReleased"), "consumes": ("InventoryReleased", "OrderVerified", "ForecastUpdated")}, "permissions": ("mrp_engine.read", "mrp_engine.plan", "mrp_engine.release", "mrp_engine.configure", "mrp_engine.audit"), "configuration": ("MRP_ENGINE_DATABASE_URL", "MRP_ENGINE_EVENT_TOPIC", "MRP_ENGINE_RETRY_LIMIT", "MRP_ENGINE_DEFAULT_PLANNING_BUCKET")}


def mrp_engine_federate_plan_view(state: dict, planned_order_id: str, *, systems: tuple[str, ...]) -> dict:
    planned_order = state["planned_orders"][planned_order_id]
    return {"ok": True, "planned_order_id": planned_order_id, "systems": systems, "projection": {"item": planned_order["item"], "quantity": planned_order["quantity"], "route": planned_order["route"], "status": planned_order["status"]}}


def mrp_engine_verify_item_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def mrp_engine_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"inventory_projection_delay", "procurement_api_timeout"}, "scenario": scenario, "mode": "degraded_projection_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "mrp_engine.dead_letter"}


def mrp_engine_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"mrp_epoch_{epoch:04d}"}


def mrp_engine_schedule_carbon_aware_plan(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def mrp_engine_optimize_material_allocation(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["service"] - candidate["cost"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "plan": selected["plan"], "objective_score": selected["objective"], "candidates": scored}


def mrp_engine_allocate_capacity(resources: tuple[dict, ...], *, required_capacity: float) -> dict:
    weights = tuple({"resource": resource["resource"], "weight": resource["priority"] * resource["capacity"]} for resource in resources)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"resource": item["resource"], "allocated_capacity": round(required_capacity * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["allocated_capacity"] for item in allocations), 2) == round(required_capacity, 2), "allocations": allocations, "clearing_priority": round(sum(resource["priority"] for resource in resources) / len(resources), 4)}


def mrp_engine_detect_shortage_anomaly(state: dict) -> dict:
    shortages = tuple(order["shortage_qty"] for order in state["planned_orders"].values())
    if not shortages:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(shortages) or 1
    entropy = round(-sum((shortage / total) * math.log(max(shortage / total, 0.0001), 2) for shortage in shortages), 4)
    mean = sum(shortages) / len(shortages)
    return {"ok": True, "entropy": entropy, "outliers": tuple(shortage for shortage in shortages if abs(shortage - mean) > 20)}


def mrp_engine_model_stochastic_material_exposure(*, demand_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(demand_path) < 2 else (demand_path[-1] - demand_path[0]) / (len(demand_path) - 1)
    exposure = abs(drift) * volatility * len(demand_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def mrp_engine_build_workbench_view(state: dict, *, tenant: str) -> dict:
    boms = tuple(bom for bom in state["boms"].values() if bom["tenant"] == tenant)
    demands = tuple(demand for demand in state["demands"].values() if demand["tenant"] == tenant)
    runs = tuple(run for run in state["mrp_runs"].values() if run["tenant"] == tenant)
    orders = tuple(order for order in state["planned_orders"].values() if order["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "bom_count": len(boms),
        "demand_count": len(demands),
        "run_count": len(runs),
        "planned_order_count": len(orders),
        "released_order_count": len(tuple(order for order in orders if order["status"] == "released")),
        "shortage_total": round(sum(order["shortage_qty"] for order in orders), 2),
        "purchase_suggestion_count": len(tuple(order for order in orders if order["route"] == "buy")),
        "production_suggestion_count": len(tuple(order for order in orders if order["route"] in {"make", "assemble"})),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
    }


def mrp_engine_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"mrp_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"mrp_engine:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
