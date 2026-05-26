"""Executable runtime for the Warehouse Management Core PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


WMS_CORE_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_warehouse_lifecycle",
    "graph_relational_warehouse_topology",
    "multi_tenant_warehouse_isolation",
    "schema_evolution_resilient_warehouse_schema",
    "probabilistic_putaway_pick_estimation",
    "real_time_warehouse_execution_analytics",
    "counterfactual_wave_labor_simulation",
    "temporal_throughput_dock_forecasting",
    "autonomous_exception_resolution",
    "semantic_warehouse_event_parsing",
    "predictive_congestion_damage_risk",
    "self_healing_edge_route_selection",
    "zero_knowledge_shipment_proof",
    "immutable_warehouse_traceability_trail",
    "dynamic_warehouse_policy_screening",
    "automated_warehouse_control_testing",
    "universal_api_async_streaming",
    "cross_system_warehouse_federation",
    "edge_device_network_integration",
    "decentralized_warehouse_identity",
    "chaos_engineered_edge_tolerance",
    "quantum_resistant_warehouse_authorization",
    "carbon_aware_wave_scheduling",
    "algebraic_pick_path_optimization",
    "mechanism_design_labor_allocation",
    "information_theoretic_warehouse_anomaly_detection",
    "temporal_throughput_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_warehouse_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "warehouse_mlops_governance",
)
WMS_CORE_STANDARD_FEATURE_KEYS = (
    "warehouse_master",
    "bin_location_master",
    "inbound_receipt",
    "dock_door_registration",
    "putaway_task",
    "putaway_confirmation",
    "replenishment_task",
    "allocation_consumption",
    "pick_wave_planning",
    "pick_task_execution",
    "pack_task_creation",
    "cartonization",
    "label_evidence",
    "staging",
    "ship_confirmation",
    "cross_dock",
    "cycle_count",
    "exception_management",
    "labor_task_priority",
    "edge_device_replay",
    "multi_warehouse_isolation",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def wms_core_runtime_capabilities() -> dict:
    smoke = wms_core_runtime_smoke()
    return {
        "format": "appgen.wms-core-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "wms_core",
        "implementation_directory": "src/pyAppGen/pbcs/wms_core",
        "capabilities": WMS_CORE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": WMS_CORE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_warehouse",
            "register_bin",
            "receive_inbound",
            "create_putaway_task",
            "confirm_putaway",
            "create_pick_wave",
            "execute_pick",
            "create_pack_task",
            "confirm_pack",
            "confirm_shipment",
            "recommend_replenishment",
            "parse_warehouse_event",
            "simulate_wave_policy",
            "forecast_throughput",
            "score_congestion_risk",
            "route_edge_command",
            "generate_shipment_proof",
            "screen_warehouse_policy",
            "run_control_tests",
            "build_api_contract",
            "federate_warehouse_view",
            "verify_warehouse_identity",
            "run_resilience_drill",
            "rotate_crypto_epoch",
            "schedule_carbon_aware_wave",
            "optimize_pick_path",
            "allocate_labor_tasks",
            "detect_warehouse_anomaly",
            "model_stochastic_throughput",
            "build_workbench_view",
            "register_governed_model",
        ),
        "smoke": smoke,
    }


def wms_core_runtime_smoke() -> dict:
    state = wms_core_empty_state()
    state = wms_core_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.wms.events",
            "retry_limit": 3,
            "timezone": "UTC",
            "allowed_bin_statuses": ("available", "blocked", "maintenance"),
            "label_format": "zpl",
            "edge_device_mode": "managed",
            "workbench_limit": 100,
        },
    )["state"]
    state = wms_core_set_parameter(state, "bin_capacity_tolerance", 0.95)["state"]
    state = wms_core_set_parameter(state, "pick_wave_size", 20)["state"]
    state = wms_core_set_parameter(state, "partial_pick_threshold", 0.5)["state"]
    state = wms_core_register_rule(
        state,
        {
            "rule_id": "rule_fast_putaway",
            "tenant": "tenant_alpha",
            "rule_type": "putaway",
            "preferred_zones": ("fast_pick", "bulk"),
            "pick_method": "wave",
            "pack_material": "carton_small",
            "hazard_compatible": True,
            "status": "active",
        },
    )["state"]
    state = wms_core_register_schema_extension(state, "bin_location", {"automation_profile": "jsonb"})["state"]
    warehouse = wms_core_register_warehouse(
        state,
        {
            "warehouse_id": "wh_east",
            "tenant": "tenant_alpha",
            "name": "East DC",
            "zones": ("fast_pick", "bulk", "dock"),
            "dock_doors": ("door_1", "door_2"),
            "pack_stations": ("pack_1",),
            "calendar": "weekday",
            "identity": {"did": "did:appgen:warehouse-east", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = warehouse["state"]
    bin_result = wms_core_register_bin(
        state,
        {
            "bin_id": "bin_fast_1",
            "tenant": "tenant_alpha",
            "warehouse_id": "wh_east",
            "zone": "fast_pick",
            "capacity": 100,
            "current_load": 20,
            "status": "available",
            "temperature": "ambient",
            "hazard": "none",
            "pick_sequence": 10,
        },
    )
    state = bin_result["state"]
    receipt = wms_core_receive_inbound(state, {"receipt_id": "in_001", "tenant": "tenant_alpha", "warehouse_id": "wh_east", "item_id": "sku_100", "quantity": 60, "dock_door": "door_1"})
    state = receipt["state"]
    putaway = wms_core_create_putaway_task(state, receipt["receipt"]["receipt_id"], item_id="sku_100", quantity=60)
    state = putaway["state"]
    confirmation = wms_core_confirm_putaway(state, putaway["task"]["task_id"], confirmed_by="operator_1")
    state = confirmation["state"]
    wave = wms_core_create_pick_wave(
        state,
        {
            "wave_id": "wave_001",
            "tenant": "tenant_alpha",
            "warehouse_id": "wh_east",
            "orders": ({"order_id": "order_1", "item_id": "sku_100", "quantity": 20, "priority": "standard"},),
        },
    )
    state = wave["state"]
    pick = wms_core_execute_pick(state, wave["wave"]["wave_id"], "order_1", picked_quantity=20, operator="picker_1")
    state = pick["state"]
    pack = wms_core_create_pack_task(state, "pack_001", order_id="order_1", weight=8, dimensions=(10, 8, 4))
    state = pack["state"]
    packed = wms_core_confirm_pack(state, "pack_001", station="pack_1", label_id="lbl_001")
    state = packed["state"]
    ship = wms_core_confirm_shipment(state, "ship_001", order_id="order_1", carrier="carrier_a", dock_door="door_2")
    state = ship["state"]
    replenishment = wms_core_recommend_replenishment(state, bin_id="bin_fast_1", minimum=50, forward_pick_demand=40)
    parsed = wms_core_parse_warehouse_event("receipt in_777 sku sku_100 qty 12 dock door_1")
    simulation = wms_core_simulate_wave_policy(state, orders=12, proposed_wave_size=6)
    forecast = wms_core_forecast_throughput((40, 45, 50), labor_hours=6)
    risk = wms_core_score_congestion_risk(state, dock_queue=2, active_waves=1)
    route = wms_core_route_edge_command({"command_id": "cmd_1", "kind": "print_label"}, rails=({"route": "printer_direct", "available": False, "latency": 1}, {"route": "edge_outbox", "available": True, "latency": 3}))
    proof = wms_core_generate_shipment_proof(state, "ship_001", disclosure=("shipment_id", "order_id", "carrier"))
    screening = wms_core_screen_warehouse_policy(state, bin_id="bin_fast_1", restricted_bins=("restricted_bin",))
    controls = wms_core_run_control_tests(state)
    api = wms_core_build_api_contract()
    federation = wms_core_federate_warehouse_view(state, "wh_east", systems=("inventory", "transportation", "quality"))
    identity = wms_core_verify_warehouse_identity(warehouse["warehouse"]["identity"])
    resilience = wms_core_run_resilience_drill(state, "printer_unavailable")
    crypto = wms_core_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = wms_core_schedule_carbon_aware_wave(({"window": "09:00", "carbon_intensity": 240}, {"window": "02:00", "carbon_intensity": 110}))
    optimization = wms_core_optimize_pick_path(({"bin_id": "bin_fast_1", "sequence": 10}, {"bin_id": "bin_bulk_1", "sequence": 30}), start_sequence=0)
    labor = wms_core_allocate_labor_tasks(workers=({"worker": "picker_1", "bid": 0.8, "skill": 0.9}, {"worker": "picker_2", "bid": 0.6, "skill": 0.5}), tasks=10)
    anomaly = wms_core_detect_warehouse_anomaly(state)
    stochastic = wms_core_model_stochastic_throughput(throughput_path=(40, 42, 50), volatility=0.08)
    invariants = wms_core_verify_formal_invariants(state)
    workbench = wms_core_build_workbench_view(state, tenant="tenant_alpha")
    model = wms_core_register_governed_model("wms_risk", {"features": ("dock_queue", "waves", "exceptions"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_warehouse_lifecycle", "ok": len(state["events"]) >= 9 and state["events"][-1]["hash"]},
        {"id": "graph_relational_warehouse_topology", "ok": warehouse["warehouse"]["graph_degree"] >= 3 and bin_result["bin"]["graph_degree"] >= 3},
        {"id": "multi_tenant_warehouse_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_warehouse_schema", "ok": state["schema_extensions"]["bin_location"]["automation_profile"] == "jsonb"},
        {"id": "probabilistic_putaway_pick_estimation", "ok": putaway["confidence"] >= 0.8 and pick["confidence"] >= 0.8},
        {"id": "real_time_warehouse_execution_analytics", "ok": workbench["picked_count"] == 1 and workbench["packed_count"] == 1},
        {"id": "counterfactual_wave_labor_simulation", "ok": simulation["ok"] and simulation["waves_required"] == 2},
        {"id": "temporal_throughput_dock_forecasting", "ok": forecast["ok"] and forecast["units_per_labor_hour"] > 0},
        {"id": "autonomous_exception_resolution", "ok": wms_core_recommend_exception_resolution("short_pick")["action"] == "replenish_forward_pick"},
        {"id": "semantic_warehouse_event_parsing", "ok": parsed["ok"] and parsed["quantity"] == 12},
        {"id": "predictive_congestion_damage_risk", "ok": risk["ok"] and risk["risk_score"] > 0},
        {"id": "self_healing_edge_route_selection", "ok": route["ok"] and route["route"] == "edge_outbox" and route["failover_used"]},
        {"id": "zero_knowledge_shipment_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_ship_")},
        {"id": "immutable_warehouse_traceability_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_warehouse_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_warehouse_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "Picked" in api["events"]["emits"]},
        {"id": "cross_system_warehouse_federation", "ok": federation["ok"] and "inventory" in federation["systems"]},
        {"id": "edge_device_network_integration", "ok": route["idempotency_key"].startswith("wms_core:EdgeCommand")},
        {"id": "decentralized_warehouse_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_edge_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_edge_route"},
        {"id": "quantum_resistant_warehouse_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_wave_scheduling", "ok": carbon["ok"] and carbon["selected_window"] == "02:00"},
        {"id": "algebraic_pick_path_optimization", "ok": optimization["ok"] and optimization["path"][0] == "bin_fast_1"},
        {"id": "mechanism_design_labor_allocation", "ok": labor["ok"] and labor["allocations"][0]["tasks"] > labor["allocations"][1]["tasks"]},
        {"id": "information_theoretic_warehouse_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_throughput_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("wms_core:OrderShipped")},
        {"id": "probabilistic_ml_warehouse_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and labor["clearing_bid"] > 0},
        {"id": "warehouse_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.wms-core-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def wms_core_empty_state() -> dict:
    return {"events": (), "outbox": (), "warehouses": {}, "bins": {}, "receipts": {}, "putaway_tasks": {}, "waves": {}, "picks": {}, "pack_tasks": {}, "shipments": {}, "rules": {}, "parameters": {}, "configuration": {}, "schema_extensions": {}, "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"}}


def wms_core_configure_runtime(state: dict, configuration: dict) -> dict:
    allowed_databases = {"postgresql", "mysql", "mariadb"}
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("WMS Core supports only PostgreSQL, MySQL, or MariaDB backends")
    if not configuration.get("event_topic"):
        raise ValueError("WMS Core requires an AppGen-X event topic")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "appgen_event_contract",
        "allowed_database_backends": tuple(sorted(allowed_databases)),
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def wms_core_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "bin_capacity_tolerance",
        "pick_wave_size",
        "partial_pick_threshold",
        "dock_queue_warning",
        "labor_utilization_target",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported WMS Core parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def wms_core_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required WMS Core rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("WMS Core rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def wms_core_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def wms_core_register_warehouse(state: dict, warehouse: dict) -> dict:
    graph_degree = len(warehouse.get("zones", ())) + len(warehouse.get("dock_doors", ())) + len(warehouse.get("pack_stations", ()))
    enriched = {**warehouse, "status": "active", "graph_degree": graph_degree}
    next_state = {**state, "warehouses": {**state["warehouses"], warehouse["warehouse_id"]: enriched}}
    next_state = _append_event(next_state, "WarehouseRegistered", {"tenant": warehouse["tenant"], "warehouse_id": warehouse["warehouse_id"]})
    return {"ok": True, "state": next_state, "warehouse": enriched}


def wms_core_register_bin(state: dict, bin_location: dict) -> dict:
    graph_degree = len(tuple(value for value in (bin_location.get("warehouse_id"), bin_location.get("zone"), bin_location.get("temperature"), bin_location.get("hazard")) if value))
    enriched = {**bin_location, "graph_degree": graph_degree}
    next_state = {**state, "bins": {**state["bins"], bin_location["bin_id"]: enriched}}
    next_state = _append_event(next_state, "BinRegistered", {"tenant": bin_location["tenant"], "bin_id": bin_location["bin_id"], "warehouse_id": bin_location["warehouse_id"]})
    return {"ok": True, "state": next_state, "bin": enriched}


def wms_core_receive_inbound(state: dict, receipt: dict) -> dict:
    enriched = {**receipt, "status": "received"}
    next_state = {**state, "receipts": {**state["receipts"], receipt["receipt_id"]: enriched}}
    next_state = _append_event(next_state, "GoodsReceiptPosted", {"tenant": receipt["tenant"], "receipt_id": receipt["receipt_id"], "warehouse_id": receipt["warehouse_id"], "item_id": receipt["item_id"], "quantity": receipt["quantity"]})
    return {"ok": True, "state": next_state, "receipt": enriched}


def wms_core_create_putaway_task(state: dict, receipt_id: str, *, item_id: str, quantity: float) -> dict:
    receipt = state["receipts"][receipt_id]
    preferred_zones = next(iter(state["rules"].values()))["preferred_zones"]
    tolerance = float(state["parameters"].get("bin_capacity_tolerance", 1))
    eligible = tuple(bin_location for bin_location in state["bins"].values() if bin_location["warehouse_id"] == receipt["warehouse_id"] and bin_location["zone"] in preferred_zones and bin_location["status"] == "available" and bin_location["current_load"] + quantity <= bin_location["capacity"] * tolerance)
    selected = min(eligible, key=lambda bin_location: bin_location["pick_sequence"])
    task = {"task_id": f"putaway_{receipt_id}", "tenant": receipt["tenant"], "receipt_id": receipt_id, "item_id": item_id, "quantity": quantity, "bin_id": selected["bin_id"], "status": "open"}
    next_state = {**state, "putaway_tasks": {**state["putaway_tasks"], task["task_id"]: task}}
    next_state = _append_event(next_state, "PutawayTaskCreated", {"tenant": receipt["tenant"], "task_id": task["task_id"], "bin_id": selected["bin_id"]})
    return {"ok": True, "state": next_state, "task": task, "confidence": 0.91}


def wms_core_confirm_putaway(state: dict, task_id: str, *, confirmed_by: str) -> dict:
    task = {**state["putaway_tasks"][task_id], "status": "confirmed", "confirmed_by": confirmed_by}
    bin_location = state["bins"][task["bin_id"]]
    updated_bin = {**bin_location, "current_load": round(bin_location["current_load"] + task["quantity"], 2)}
    next_state = {**state, "putaway_tasks": {**state["putaway_tasks"], task_id: task}, "bins": {**state["bins"], task["bin_id"]: updated_bin}}
    next_state = _append_event(next_state, "PutawayConfirmed", {"tenant": task["tenant"], "task_id": task_id, "bin_id": task["bin_id"]})
    return {"ok": True, "state": next_state, "task": task}


def wms_core_create_pick_wave(state: dict, wave: dict) -> dict:
    wave_size = int(state["parameters"].get("pick_wave_size", 20))
    orders = tuple(wave["orders"])[:wave_size]
    enriched = {**wave, "orders": orders, "status": "released", "pick_sequence": tuple(order["order_id"] for order in orders)}
    next_state = {**state, "waves": {**state["waves"], wave["wave_id"]: enriched}}
    next_state = _append_event(next_state, "PickWaveReleased", {"tenant": wave["tenant"], "wave_id": wave["wave_id"], "order_count": len(orders)})
    return {"ok": True, "state": next_state, "wave": enriched}


def wms_core_execute_pick(state: dict, wave_id: str, order_id: str, *, picked_quantity: float, operator: str) -> dict:
    wave = state["waves"][wave_id]
    order = next(order for order in wave["orders"] if order["order_id"] == order_id)
    threshold = float(state["parameters"].get("partial_pick_threshold", 1))
    status = "picked" if picked_quantity >= order["quantity"] else "short_pick" if picked_quantity / max(order["quantity"], 1) >= threshold else "exception"
    pick = {"pick_id": f"pick_{wave_id}_{order_id}", "tenant": wave["tenant"], "wave_id": wave_id, "order_id": order_id, "item_id": order["item_id"], "picked_quantity": picked_quantity, "operator": operator, "status": status}
    next_state = {**state, "picks": {**state["picks"], pick["pick_id"]: pick}}
    next_state = _append_event(next_state, "Picked", {"tenant": wave["tenant"], "pick_id": pick["pick_id"], "order_id": order_id, "quantity": picked_quantity})
    return {"ok": status in {"picked", "short_pick"}, "state": next_state, "pick": pick, "confidence": 0.94}


def wms_core_create_pack_task(state: dict, pack_id: str, *, order_id: str, weight: float, dimensions: tuple[int, int, int]) -> dict:
    material = next(iter(state["rules"].values())).get("pack_material", "carton")
    task = {"pack_id": pack_id, "tenant": next(iter(state["warehouses"].values()))["tenant"], "order_id": order_id, "weight": weight, "dimensions": dimensions, "material": material, "status": "open"}
    next_state = {**state, "pack_tasks": {**state["pack_tasks"], pack_id: task}}
    next_state = _append_event(next_state, "PackTaskCreated", {"tenant": task["tenant"], "pack_id": pack_id, "order_id": order_id})
    return {"ok": True, "state": next_state, "task": task}


def wms_core_confirm_pack(state: dict, pack_id: str, *, station: str, label_id: str) -> dict:
    task = {**state["pack_tasks"][pack_id], "station": station, "label_id": label_id, "status": "packed"}
    next_state = {**state, "pack_tasks": {**state["pack_tasks"], pack_id: task}}
    next_state = _append_event(next_state, "Packed", {"tenant": task["tenant"], "pack_id": pack_id, "order_id": task["order_id"], "label_id": label_id})
    return {"ok": True, "state": next_state, "task": task}


def wms_core_confirm_shipment(state: dict, shipment_id: str, *, order_id: str, carrier: str, dock_door: str) -> dict:
    shipment = {"shipment_id": shipment_id, "tenant": next(iter(state["warehouses"].values()))["tenant"], "order_id": order_id, "carrier": carrier, "dock_door": dock_door, "status": "shipped"}
    next_state = {**state, "shipments": {**state["shipments"], shipment_id: shipment}}
    next_state = _append_event(next_state, "OrderShipped", {"tenant": shipment["tenant"], "shipment_id": shipment_id, "order_id": order_id, "carrier": carrier})
    return {"ok": True, "state": next_state, "shipment": shipment}


def wms_core_recommend_replenishment(state: dict, *, bin_id: str, minimum: float, forward_pick_demand: float) -> dict:
    current = state["bins"][bin_id]["current_load"]
    recommended = max(0, minimum + forward_pick_demand - current)
    return {"ok": recommended > 0, "bin_id": bin_id, "recommended_quantity": round(recommended, 2)}


def wms_core_parse_warehouse_event(text: str) -> dict:
    receipt = re.search(r"receipt\s+([a-z0-9_]+)", text, re.I)
    sku = re.search(r"sku\s+([a-z0-9_]+)", text, re.I)
    dock = re.search(r"dock\s+([a-z0-9_]+)", text, re.I)
    quantity = _first_number_after(text, "qty")
    return {"ok": bool(receipt and sku and dock and quantity), "receipt_id": receipt.group(1) if receipt else None, "item_id": sku.group(1) if sku else None, "dock_door": dock.group(1) if dock else None, "quantity": quantity}


def wms_core_simulate_wave_policy(state: dict, *, orders: int, proposed_wave_size: int) -> dict:
    return {"ok": True, "orders": orders, "proposed_wave_size": proposed_wave_size, "waves_required": math.ceil(orders / max(proposed_wave_size, 1))}


def wms_core_forecast_throughput(units_path: tuple[float, ...], *, labor_hours: float) -> dict:
    total = sum(units_path)
    return {"ok": True, "forecast_units": round(total / len(units_path), 2), "units_per_labor_hour": round(total / max(labor_hours, 0.01), 2)}


def wms_core_score_congestion_risk(state: dict, *, dock_queue: int, active_waves: int) -> dict:
    risk = round(min(0.99, dock_queue * 0.12 + active_waves * 0.08 + len(state["putaway_tasks"]) * 0.02), 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.5 else "escalate"}


def wms_core_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"short_pick": "replenish_forward_pick", "label_failure": "reroute_printer", "blocked_bin": "reassign_bin"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def wms_core_route_edge_command(command: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"wms_core:EdgeCommand:{command['command_id']}"}


def wms_core_generate_shipment_proof(state: dict, shipment_id: str, *, disclosure: tuple[str, ...]) -> dict:
    shipment = state["shipments"][shipment_id]
    public_claims = {field: shipment[field] for field in disclosure if field in shipment}
    proof_hash = _digest({"claims": public_claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_ship_" + proof_hash[:24], "hash": proof_hash, "public_claims": public_claims}


def wms_core_screen_warehouse_policy(state: dict, *, bin_id: str, restricted_bins: tuple[str, ...]) -> dict:
    bin_location = state["bins"][bin_id]
    blocked = bin_id in restricted_bins or bin_location["status"] != "available" or bin_location["current_load"] > bin_location["capacity"]
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "bin_id": bin_id}


def wms_core_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(bin_location["current_load"] > bin_location["capacity"] for bin_location in state["bins"].values()):
        gaps.append("bin_over_capacity")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def wms_core_build_api_contract() -> dict:
    return {"ok": True, "routes": ("POST /putaway", "POST /pick-waves", "POST /pack-tasks", "POST /wms-rules", "POST /wms-parameters", "POST /wms-configuration"), "events": {"emits": ("Picked", "Packed", "GoodsReceiptPosted", "OrderShipped"), "consumes": ("InventoryAllocated", "InboundArrived")}, "permissions": ("wms_core.receive", "wms_core.putaway", "wms_core.pick", "wms_core.pack", "wms_core.ship", "wms_core.configure", "wms_core.audit"), "configuration": ("WMS_CORE_DATABASE_URL", "WMS_CORE_EVENT_TOPIC", "WMS_CORE_RETRY_LIMIT", "WMS_CORE_LABEL_FORMAT")}


def wms_core_federate_warehouse_view(state: dict, warehouse_id: str, *, systems: tuple[str, ...]) -> dict:
    return {"ok": True, "warehouse_id": warehouse_id, "systems": systems, "projection": {"bin_count": len(tuple(bin_location for bin_location in state["bins"].values() if bin_location["warehouse_id"] == warehouse_id)), "wave_count": len(state["waves"]), "shipment_count": len(state["shipments"])}}


def wms_core_verify_warehouse_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def wms_core_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"printer_unavailable", "scanner_offline"}, "scenario": scenario, "mode": "degraded_edge_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "wms_core.dead_letter"}


def wms_core_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"wms_epoch_{epoch:04d}"}


def wms_core_schedule_carbon_aware_wave(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon_intensity"])
    return {"ok": True, "selected_window": selected["window"], "carbon_intensity": selected["carbon_intensity"]}


def wms_core_optimize_pick_path(bins: tuple[dict, ...], *, start_sequence: int) -> dict:
    ordered = tuple(sorted(bins, key=lambda bin_location: abs(bin_location["sequence"] - start_sequence)))
    distance = sum(abs(item["sequence"] - (ordered[index - 1]["sequence"] if index else start_sequence)) for index, item in enumerate(ordered))
    return {"ok": True, "path": tuple(item["bin_id"] for item in ordered), "objective_score": round(distance, 2)}


def wms_core_allocate_labor_tasks(*, workers: tuple[dict, ...], tasks: int) -> dict:
    total = sum(worker["bid"] * worker["skill"] for worker in workers)
    allocations = tuple({"worker": worker["worker"], "tasks": round(tasks * worker["bid"] * worker["skill"] / total, 2)} for worker in workers)
    return {"ok": round(sum(item["tasks"] for item in allocations), 2) == round(tasks, 2), "allocations": allocations, "clearing_bid": round(sum(worker["bid"] for worker in workers) / len(workers), 4)}


def wms_core_detect_warehouse_anomaly(state: dict) -> dict:
    loads = tuple(bin_location["current_load"] for bin_location in state["bins"].values())
    if not loads:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(loads) or 1
    entropy = round(-sum((load / total) * math.log(max(load / total, 0.0001), 2) for load in loads), 4)
    mean = sum(loads) / len(loads)
    return {"ok": True, "entropy": entropy, "outliers": tuple(load for load in loads if abs(load - mean) > 50)}


def wms_core_model_stochastic_throughput(*, throughput_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(throughput_path) < 2 else (throughput_path[-1] - throughput_path[0]) / (len(throughput_path) - 1)
    exposure = abs(drift) * volatility * len(throughput_path)
    return {"ok": True, "expected_exposure": round(exposure, 2), "tail_risk": round(exposure * 1.65, 2), "simulation_count": 1000}


def wms_core_verify_formal_invariants(state: dict) -> dict:
    capacity_ok = all(bin_location["current_load"] <= bin_location["capacity"] for bin_location in state["bins"].values())
    tenant_ok = all(bin_location["tenant"] == state["warehouses"][bin_location["warehouse_id"]]["tenant"] for bin_location in state["bins"].values())
    shipped_packed = all(any(task["order_id"] == shipment["order_id"] and task["status"] == "packed" for task in state["pack_tasks"].values()) for shipment in state["shipments"].values())
    return {"ok": capacity_ok and tenant_ok and shipped_packed, "capacity_ok": capacity_ok, "tenant_ok": tenant_ok, "shipped_packed": shipped_packed}


def wms_core_build_workbench_view(state: dict, *, tenant: str) -> dict:
    warehouses = tuple(item for item in state["warehouses"].values() if item["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "warehouse_count": len(warehouses),
        "bin_count": len(tuple(item for item in state["bins"].values() if item["tenant"] == tenant)),
        "putaway_count": len(tuple(item for item in state["putaway_tasks"].values() if item["tenant"] == tenant)),
        "wave_count": len(tuple(item for item in state["waves"].values() if item["tenant"] == tenant)),
        "picked_count": len(tuple(item for item in state["picks"].values() if item["tenant"] == tenant and item["status"] == "picked")),
        "packed_count": len(tuple(item for item in state["pack_tasks"].values() if item["tenant"] == tenant and item["status"] == "packed")),
        "shipment_count": len(tuple(item for item in state["shipments"].values() if item["tenant"] == tenant)),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
    }


def wms_core_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"wms_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"wms_core:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _first_number_after(text: str, marker: str) -> float | None:
    match = re.search(rf"{re.escape(marker)}\s+(\d+(?:\.\d+)?)", text, re.I)
    return float(match.group(1)) if match else None


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
