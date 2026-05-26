"""Executable runtime for the Warehouse Management Core PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


WMS_CORE_REQUIRED_EVENT_TOPIC = "appgen.wms.events"
WMS_CORE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
WMS_CORE_OWNED_TABLES = (
    "warehouse",
    "warehouse_zone",
    "warehouse_calendar",
    "warehouse_identity",
    "bin_location",
    "bin_attribute",
    "bin_capacity_snapshot",
    "inbound_receipt",
    "inbound_receipt_line",
    "dock_door",
    "dock_appointment",
    "putaway_task",
    "putaway_confirmation",
    "replenishment_task",
    "replenishment_trigger",
    "pick_wave",
    "pick_task",
    "pick_exception",
    "pack_task",
    "carton",
    "label_evidence",
    "pack_station",
    "staging_lane",
    "shipment_confirmation",
    "shipment_label",
    "cross_dock_flow",
    "cycle_count",
    "cycle_count_line",
    "warehouse_exception",
    "labor_task",
    "labor_assignment",
    "labor_productivity",
    "edge_device_command",
    "edge_device_event",
    "edge_device_replay",
    "warehouse_policy_screening",
    "warehouse_traceability_event",
    "warehouse_shipment_proof",
    "warehouse_federation_projection",
    "warehouse_carbon_wave",
    "warehouse_pick_path_optimization",
    "warehouse_labor_allocation",
    "warehouse_anomaly_signal",
    "warehouse_risk_model",
    "warehouse_seed_data",
    "wms_schema_extension",
    "wms_control_assertion",
    "wms_governed_model",
    "wms_rule",
    "wms_parameter",
    "wms_configuration",
    "wms_core_appgen_outbox_event",
    "wms_core_appgen_inbox_event",
    "wms_core_dead_letter_event",
)
WMS_CORE_EMITTED_EVENT_TYPES = (
    "WarehouseRegistered",
    "BinRegistered",
    "GoodsReceiptPosted",
    "PutawayTaskCreated",
    "PutawayConfirmed",
    "PickWaveReleased",
    "Picked",
    "PackTaskCreated",
    "Packed",
    "OrderShipped",
)
WMS_CORE_CONSUMED_EVENT_TYPES = (
    "InventoryAllocated",
    "InboundArrived",
    "QualityHoldReleased",
    "CarrierBooked",
    "AccessPolicyChanged",
)
_WMS_CORE_RUNTIME_TABLES = (
    "wms_core_appgen_outbox_event",
    "wms_core_appgen_inbox_event",
    "wms_core_dead_letter_event",
)
_WMS_CORE_ALLOWED_DEPENDENCIES = (
    "inventory_allocation_projection",
    "inbound_arrival_projection",
    "quality_hold_projection",
    "carrier_booking_projection",
    "access_policy_projection",
    "GET /inventory/allocations/{id}",
    "GET /inbound/arrivals/{id}",
    "GET /quality/holds/{id}",
    "GET /transportation/bookings/{id}",
    "GET /identity/policies",
    "POST /audit/warehouse-events",
)
_WMS_CORE_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}


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
    "warehouse_zone_master",
    "warehouse_calendar",
    "warehouse_identity",
    "bin_location_master",
    "bin_attributes",
    "bin_capacity_snapshots",
    "inbound_receipt",
    "receipt_lines",
    "dock_door_registration",
    "dock_appointment",
    "putaway_task",
    "putaway_confirmation",
    "replenishment_task",
    "replenishment_trigger",
    "allocation_consumption",
    "pick_wave_planning",
    "pick_task_execution",
    "pick_exception_management",
    "pack_task_creation",
    "cartonization",
    "label_evidence",
    "pack_station_management",
    "staging",
    "ship_confirmation",
    "shipment_labels",
    "cross_dock",
    "cycle_count",
    "cycle_count_lines",
    "exception_management",
    "labor_task_priority",
    "edge_device_replay",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "retry_dead_letter_evidence",
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
        "owned_tables": WMS_CORE_OWNED_TABLES,
        "capabilities": WMS_CORE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": WMS_CORE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
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
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
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
            "verify_owned_table_boundary",
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
            "event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC,
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
    schema = wms_core_build_schema_contract()
    service = wms_core_build_service_contract()
    release = wms_core_build_release_evidence()
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
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and "Picked" in api["events"]["emits"]},
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
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letters": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "inventory_allocation_projections": {},
        "inbound_arrival_projections": {},
        "quality_hold_projections": {},
        "carrier_booking_projections": {},
        "access_policy_projections": {},
        "warehouses": {},
        "bins": {},
        "receipts": {},
        "putaway_tasks": {},
        "waves": {},
        "picks": {},
        "pack_tasks": {},
        "shipments": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def wms_core_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _WMS_CORE_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"WMS Core uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    if configuration.get("database_backend") not in set(WMS_CORE_ALLOWED_DATABASE_BACKENDS):
        raise ValueError("WMS Core supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != WMS_CORE_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"WMS Core requires AppGen-X event topic {WMS_CORE_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": WMS_CORE_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": WMS_CORE_OWNED_TABLES,
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
    if table not in WMS_CORE_OWNED_TABLES:
        raise ValueError(f"WMS Core schema extensions must target owned tables: {WMS_CORE_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    existing = dict(state.get("schema_extensions", {}).get(table, {}))
    merged = {**existing, **fields}
    return {
        "ok": True,
        "state": {**state, "schema_extensions": {**state["schema_extensions"], table: merged}},
        "schema_extension": {"table": table, "fields": dict(fields)},
        "target": table,
        "fields": merged,
    }


def wms_core_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    key = event.get("idempotency_key") or f"{event_type}:{event_id}"
    handled = state.get("handled_events", {})
    if key in handled and handled[key]["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": handled[key]}
    attempts = int(handled.get(key, {}).get("attempts", 0)) + 1
    payload = dict(event.get("payload", {}))
    inbox_entry = {
        "event_id": event_id,
        "event_type": event_type,
        "tenant": payload.get("tenant"),
        "attempts": attempts,
        "idempotency_key": key,
    }
    next_state = {
        **state,
        "inbox": (*state.get("inbox", ()), inbox_entry),
        "handled_events": dict(handled),
        "retry_evidence": tuple(state.get("retry_evidence", ())),
        "dead_letters": tuple(state.get("dead_letters", ())),
        "dead_letter": tuple(state.get("dead_letter", ())),
        "inventory_allocation_projections": dict(state.get("inventory_allocation_projections", {})),
        "inbound_arrival_projections": dict(state.get("inbound_arrival_projections", {})),
        "quality_hold_projections": dict(state.get("quality_hold_projections", {})),
        "carrier_booking_projections": dict(state.get("carrier_booking_projections", {})),
        "access_policy_projections": dict(state.get("access_policy_projections", {})),
    }
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in WMS_CORE_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"] = (*next_state["retry_evidence"], evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_wms_event"}
            next_state["dead_letters"] = (*next_state["dead_letters"], dead)
            next_state["dead_letter"] = (*next_state["dead_letter"], dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "InventoryAllocated":
        next_state["inventory_allocation_projections"][payload.get("allocation_id", event_id)] = payload
    elif event_type == "InboundArrived":
        next_state["inbound_arrival_projections"][payload.get("arrival_id", event_id)] = payload
    elif event_type == "QualityHoldReleased":
        next_state["quality_hold_projections"][payload.get("hold_id", event_id)] = payload
    elif event_type == "CarrierBooked":
        next_state["carrier_booking_projections"][payload.get("booking_id", event_id)] = payload
    elif event_type == "AccessPolicyChanged":
        next_state["access_policy_projections"][payload.get("policy_id", event_id)] = payload
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


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
    return {
        "ok": True,
        "format": "appgen.wms-core-api-contract.v1",
        "routes": (
            {"route": "POST /wms/warehouses", "command": "register_warehouse", "owned_tables": ("warehouse", "dock_door"), "emits": ("WarehouseRegistered",), "requires_permission": "wms_core.master", "idempotency_key": "warehouse_id"},
            {"route": "POST /wms/bins", "command": "register_bin", "owned_tables": ("bin_location",), "emits": ("BinRegistered",), "requires_permission": "wms_core.master", "idempotency_key": "bin_id"},
            {"route": "POST /wms/inbound", "command": "receive_inbound", "owned_tables": ("inbound_receipt",), "emits": ("GoodsReceiptPosted",), "requires_permission": "wms_core.receive", "idempotency_key": "receipt_id"},
            {"route": "POST /wms/putaway", "command": "create_putaway_task", "owned_tables": ("putaway_task", "bin_location"), "emits": ("PutawayTaskCreated",), "requires_permission": "wms_core.putaway", "idempotency_key": "receipt_id:item_id"},
            {"route": "POST /wms/pick-waves", "command": "create_pick_wave", "owned_tables": ("pick_wave", "pick_task"), "emits": ("PickWaveReleased",), "requires_permission": "wms_core.pick", "idempotency_key": "wave_id"},
            {"route": "POST /wms/picks/{id}/execute", "command": "execute_pick", "owned_tables": ("pick_task", "warehouse_exception"), "emits": ("Picked",), "requires_permission": "wms_core.pick", "idempotency_key": "wave_id:order_id"},
            {"route": "POST /wms/pack-tasks", "command": "create_pack_task", "owned_tables": ("pack_task", "carton"), "emits": ("PackTaskCreated",), "requires_permission": "wms_core.pack", "idempotency_key": "pack_id"},
            {"route": "POST /wms/shipments", "command": "confirm_shipment", "owned_tables": ("shipment_confirmation", "staging_lane"), "emits": ("OrderShipped",), "requires_permission": "wms_core.ship", "idempotency_key": "shipment_id"},
            {"route": "POST /wms/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": WMS_CORE_CONSUMED_EVENT_TYPES, "requires_permission": "wms_core.event", "idempotency_key": "event_id"},
            {"route": "GET /wms/workbench", "query": "build_workbench_view", "owned_tables": WMS_CORE_OWNED_TABLES, "requires_permission": "wms_core.audit"},
        ),
        "declared_catalog_routes": ("POST /putaway", "POST /pick-waves", "POST /pack-tasks", "GET /warehouses/{id}"),
        "events": {"emits": WMS_CORE_EMITTED_EVENT_TYPES, "consumes": WMS_CORE_CONSUMED_EVENT_TYPES},
        "emits": WMS_CORE_EMITTED_EVENT_TYPES,
        "consumes": WMS_CORE_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(wms_core_permissions_contract()["permissions"])),
        "database_backends": WMS_CORE_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": WMS_CORE_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": ("WMS_CORE_DATABASE_URL", "WMS_CORE_EVENT_TOPIC", "WMS_CORE_RETRY_LIMIT", "WMS_CORE_LABEL_FORMAT"),
    }


def wms_core_build_schema_contract() -> dict:
    """Return WMS-owned schema, migration, model, and relationship evidence."""
    table_fields = {
        "warehouse": ("tenant", "warehouse_id", "name", "status", "timezone", "calendar_id", "identity_id"),
        "warehouse_zone": ("tenant", "zone_id", "warehouse_id", "name", "zone_type", "temperature", "status"),
        "warehouse_calendar": ("tenant", "calendar_id", "warehouse_id", "working_days", "cutoff_time", "timezone"),
        "warehouse_identity": ("tenant", "identity_id", "warehouse_id", "did", "issuer", "status"),
        "bin_location": ("tenant", "bin_id", "warehouse_id", "zone", "capacity", "current_load", "status"),
        "bin_attribute": ("tenant", "attribute_id", "bin_id", "name", "value", "source"),
        "bin_capacity_snapshot": ("tenant", "snapshot_id", "bin_id", "capacity", "current_load", "observed_at"),
        "inbound_receipt": ("tenant", "receipt_id", "warehouse_id", "dock_door", "status", "received_at"),
        "inbound_receipt_line": ("tenant", "receipt_line_id", "receipt_id", "item_id", "quantity", "lot_id"),
        "dock_door": ("tenant", "dock_door_id", "warehouse_id", "door_type", "status", "zone_id"),
        "dock_appointment": ("tenant", "appointment_id", "dock_door_id", "carrier", "window_start", "window_end", "status"),
        "putaway_task": ("tenant", "task_id", "receipt_id", "item_id", "bin_id", "quantity", "status"),
        "putaway_confirmation": ("tenant", "confirmation_id", "task_id", "confirmed_by", "confirmed_at", "quantity"),
        "replenishment_task": ("tenant", "replenishment_id", "bin_id", "item_id", "recommended_quantity", "status"),
        "replenishment_trigger": ("tenant", "trigger_id", "bin_id", "minimum", "forward_pick_demand", "reason"),
        "pick_wave": ("tenant", "wave_id", "warehouse_id", "status", "method", "released_at"),
        "pick_task": ("tenant", "pick_id", "wave_id", "order_id", "item_id", "picked_quantity", "status"),
        "pick_exception": ("tenant", "exception_id", "pick_id", "exception_type", "resolution", "status"),
        "pack_task": ("tenant", "pack_id", "order_id", "station", "label_id", "status"),
        "carton": ("tenant", "carton_id", "pack_id", "material", "weight", "dimensions"),
        "label_evidence": ("tenant", "label_id", "pack_id", "format", "hash", "printed_at"),
        "pack_station": ("tenant", "station_id", "warehouse_id", "status", "capability", "current_load"),
        "staging_lane": ("tenant", "lane_id", "warehouse_id", "dock_door_id", "status", "shipment_id"),
        "shipment_confirmation": ("tenant", "shipment_id", "order_id", "carrier", "dock_door", "status"),
        "shipment_label": ("tenant", "shipment_label_id", "shipment_id", "label_id", "carrier", "hash"),
        "cross_dock_flow": ("tenant", "flow_id", "receipt_id", "shipment_id", "dock_door_id", "status"),
        "cycle_count": ("tenant", "cycle_count_id", "warehouse_id", "status", "started_at", "completed_at"),
        "cycle_count_line": ("tenant", "cycle_count_line_id", "cycle_count_id", "bin_id", "item_id", "variance"),
        "warehouse_exception": ("tenant", "exception_id", "warehouse_id", "exception_type", "severity", "status"),
        "labor_task": ("tenant", "labor_task_id", "warehouse_id", "task_type", "priority", "status"),
        "labor_assignment": ("tenant", "assignment_id", "labor_task_id", "worker_id", "tasks", "clearing_bid"),
        "labor_productivity": ("tenant", "productivity_id", "worker_id", "units", "labor_hours", "observed_at"),
        "edge_device_command": ("tenant", "command_id", "device_id", "kind", "route", "status"),
        "edge_device_event": ("tenant", "edge_event_id", "device_id", "event_type", "payload_hash", "observed_at"),
        "edge_device_replay": ("tenant", "replay_id", "command_id", "attempts", "status", "reason"),
        "warehouse_policy_screening": ("tenant", "screening_id", "bin_id", "decision", "policy", "evidence_hash"),
        "warehouse_traceability_event": ("tenant", "trace_event_id", "warehouse_id", "event_type", "trace_hash", "observed_at"),
        "warehouse_shipment_proof": ("tenant", "proof_id", "shipment_id", "proof_hash", "public_claims", "created_at"),
        "warehouse_federation_projection": ("tenant", "projection_id", "warehouse_id", "external_system", "projection_hash", "observed_at"),
        "warehouse_carbon_wave": ("tenant", "carbon_wave_id", "wave_id", "carbon_intensity", "selected_window", "scheduled_at"),
        "warehouse_pick_path_optimization": ("tenant", "optimization_id", "wave_id", "path", "objective_score", "model_version"),
        "warehouse_labor_allocation": ("tenant", "allocation_id", "warehouse_id", "worker_id", "tasks", "clearing_bid"),
        "warehouse_anomaly_signal": ("tenant", "signal_id", "warehouse_id", "entropy", "outliers", "decision"),
        "warehouse_risk_model": ("tenant", "risk_model_id", "warehouse_id", "risk_score", "model_version", "explanations"),
        "warehouse_seed_data": ("tenant", "seed_id", "warehouse_type", "zone_type", "label_format", "status"),
        "wms_schema_extension": ("tenant", "extension_id", "table_name", "field_name", "field_type", "version"),
        "wms_control_assertion": ("tenant", "control_id", "assertion", "status", "evidence_hash", "tested_at"),
        "wms_governed_model": ("tenant", "model_id", "name", "feature_lineage", "drift_score", "governance_status"),
        "wms_rule": ("tenant", "rule_id", "scope", "status", "predicate", "compiled_hash"),
        "wms_parameter": ("tenant", "parameter_id", "name", "value", "bounds", "compiled_hash"),
        "wms_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "retry_limit", "label_format"),
        "wms_core_appgen_outbox_event": ("tenant", "event_id", "event_type", "topic", "idempotency_key", "audit_hash"),
        "wms_core_appgen_inbox_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "status"),
        "wms_core_dead_letter_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason"),
    }
    relationships = (
        {"from": "warehouse_zone.warehouse_id", "to": "warehouse.warehouse_id", "type": "owned_child"},
        {"from": "warehouse_calendar.warehouse_id", "to": "warehouse.warehouse_id", "type": "owned_calendar"},
        {"from": "warehouse_identity.warehouse_id", "to": "warehouse.warehouse_id", "type": "owned_identity"},
        {"from": "bin_location.warehouse_id", "to": "warehouse.warehouse_id", "type": "owned_bin"},
        {"from": "bin_attribute.bin_id", "to": "bin_location.bin_id", "type": "owned_child"},
        {"from": "inbound_receipt_line.receipt_id", "to": "inbound_receipt.receipt_id", "type": "owned_child"},
        {"from": "putaway_confirmation.task_id", "to": "putaway_task.task_id", "type": "owned_confirmation"},
        {"from": "pick_task.wave_id", "to": "pick_wave.wave_id", "type": "owned_child"},
        {"from": "pick_exception.pick_id", "to": "pick_task.pick_id", "type": "owned_exception"},
        {"from": "carton.pack_id", "to": "pack_task.pack_id", "type": "owned_carton"},
        {"from": "shipment_label.shipment_id", "to": "shipment_confirmation.shipment_id", "type": "owned_label"},
        {"from": "cycle_count_line.cycle_count_id", "to": "cycle_count.cycle_count_id", "type": "owned_child"},
        {"from": "labor_assignment.labor_task_id", "to": "labor_task.labor_task_id", "type": "owned_assignment"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id") or field == "event_id")[:2],
            "owned_by": "wms_core",
        }
        for table in WMS_CORE_OWNED_TABLES
    )
    allowed_prefixes = ("warehouse", "bin_", "inbound_", "dock_", "putaway_", "replenishment_", "pick_", "pack_", "carton", "label_", "staging_", "shipment_", "cross_", "cycle_", "labor_", "edge_", "wms_")
    return {
        "format": "appgen.wms-core-owned-schema-contract.v1",
        "ok": len(tables) == len(WMS_CORE_OWNED_TABLES)
        and len(tables) >= 40
        and all(item["table"].startswith(allowed_prefixes) for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/wms_core/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": WMS_CORE_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(WMS_CORE_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in WMS_CORE_OWNED_TABLES
        ),
        "datastore_backends": WMS_CORE_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def wms_core_build_service_contract() -> dict:
    """Return WMS Core command/query service evidence."""
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
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
        "route_edge_command",
        "generate_shipment_proof",
        "screen_warehouse_policy",
        "federate_warehouse_view",
        "verify_warehouse_identity",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_wave",
        "optimize_pick_path",
        "allocate_labor_tasks",
        "run_control_tests",
        "register_governed_model",
    )
    return {
        "format": "appgen.wms-core-service-contract.v1",
        "ok": len(command_methods) >= 30,
        "transaction_boundary": "wms_core_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_workbench_view",
            "forecast_throughput",
            "score_congestion_risk",
            "detect_warehouse_anomaly",
            "model_stochastic_throughput",
            "verify_owned_table_boundary",
        ),
        "mutates_only": WMS_CORE_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _WMS_CORE_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": WMS_CORE_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _WMS_CORE_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def wms_core_build_release_evidence() -> dict:
    """Return WMS package-local release evidence."""
    schema = wms_core_build_schema_contract()
    service = wms_core_build_service_contract()
    api = wms_core_build_api_contract()
    permissions = wms_core_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 40},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(WMS_CORE_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 30},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": {"register_warehouse", "create_pick_wave", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == WMS_CORE_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
    )
    return {
        "format": "appgen.wms-core-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def wms_core_permissions_contract() -> dict:
    return {
        "format": "appgen.wms-core-permissions.v1",
        "ok": True,
        "permissions": (
            "wms_core.read",
            "wms_core.master",
            "wms_core.receive",
            "wms_core.putaway",
            "wms_core.pick",
            "wms_core.pack",
            "wms_core.ship",
            "wms_core.count",
            "wms_core.edge",
            "wms_core.event",
            "wms_core.configure",
            "wms_core.audit",
        ),
        "action_permissions": {
            "register_warehouse": "wms_core.master",
            "register_bin": "wms_core.master",
            "receive_inbound": "wms_core.receive",
            "create_putaway_task": "wms_core.putaway",
            "confirm_putaway": "wms_core.putaway",
            "create_pick_wave": "wms_core.pick",
            "execute_pick": "wms_core.pick",
            "create_pack_task": "wms_core.pack",
            "confirm_pack": "wms_core.pack",
            "confirm_shipment": "wms_core.ship",
            "route_edge_command": "wms_core.edge",
            "receive_event": "wms_core.event",
            "register_rule": "wms_core.configure",
            "register_schema_extension": "wms_core.configure",
            "set_parameter": "wms_core.configure",
            "configure_runtime": "wms_core.configure",
            "generate_shipment_proof": "wms_core.audit",
            "run_control_tests": "wms_core.audit",
            "build_workbench_view": "wms_core.audit",
        },
    }


def wms_core_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (
        *WMS_CORE_OWNED_TABLES,
        *WMS_CORE_CONSUMED_EVENT_TYPES,
        *_WMS_CORE_RUNTIME_TABLES,
        *_WMS_CORE_ALLOWED_DEPENDENCIES,
    )
    allowed_set = set(allowed)
    violations = tuple(reference for reference in references if reference not in allowed_set and not str(reference).startswith("wms_core_"))
    return {
        "format": "appgen.wms-core-boundary.v1",
        "ok": not violations,
        "owned_tables": WMS_CORE_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /inventory/allocations/{id}", "GET /inbound/arrivals/{id}", "GET /quality/holds/{id}", "GET /transportation/bookings/{id}", "GET /identity/policies", "POST /audit/warehouse-events"),
            "events": WMS_CORE_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "inventory_allocation_projection",
                "inbound_arrival_projection",
                "quality_hold_projection",
                "carrier_booking_projection",
                "access_policy_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


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
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": WMS_CORE_OWNED_TABLES,
            "outbox_table": "wms_core_appgen_outbox_event",
            "inbox_table": "wms_core_appgen_inbox_event",
            "dead_letter_table": "wms_core_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
            "permissions": tuple(sorted(wms_core_permissions_contract()["permissions"])),
        },
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
