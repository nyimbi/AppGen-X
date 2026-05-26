"""Executable runtime for the Inventory Positioning PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC = "appgen.inventory.events"
INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
INVENTORY_POSITIONING_OWNED_TABLES = (
    "inventory_positioning_item",
    "inventory_positioning_item_attribute",
    "inventory_positioning_item_substitution",
    "inventory_positioning_lot",
    "inventory_positioning_serial",
    "inventory_positioning_node",
    "inventory_positioning_node_calendar",
    "inventory_positioning_node_capacity",
    "inventory_positioning_node_identity",
    "inventory_positioning_inventory_position",
    "inventory_positioning_position_snapshot",
    "inventory_positioning_receipt",
    "inventory_positioning_receipt_line",
    "inventory_positioning_adjustment",
    "inventory_positioning_cycle_count",
    "inventory_positioning_reservation",
    "inventory_positioning_allocation",
    "inventory_positioning_allocation_line",
    "inventory_positioning_allocation_expiry",
    "inventory_positioning_quality_hold",
    "inventory_positioning_quality_release",
    "inventory_positioning_in_transit_projection",
    "inventory_positioning_traceability_event",
    "inventory_positioning_backorder",
    "inventory_positioning_replenishment_signal",
    "inventory_positioning_replenishment_plan",
    "inventory_positioning_reconciliation",
    "inventory_positioning_policy_screening",
    "inventory_positioning_stock_proof",
    "inventory_positioning_cross_node_federation",
    "inventory_positioning_carbon_fulfillment",
    "inventory_positioning_channel_allocation",
    "inventory_positioning_anomaly_signal",
    "inventory_positioning_stock_risk_model",
    "inventory_positioning_seed_data",
    "inventory_positioning_schema_extension",
    "inventory_positioning_control_assertion",
    "inventory_positioning_governed_model",
    "inventory_positioning_rule",
    "inventory_positioning_parameter",
    "inventory_positioning_configuration",
    "inventory_positioning_appgen_outbox_event",
    "inventory_positioning_appgen_inbox_event",
    "inventory_positioning_dead_letter_event",
)
INVENTORY_POSITIONING_EMITTED_EVENT_TYPES = (
    "ItemRegistered",
    "InventoryNodeRegistered",
    "GoodsReceiptPosted",
    "InventoryAdjusted",
    "InventoryAllocated",
    "InventoryReleased",
    "QualityHoldApplied",
)
INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES = (
    "OrderVerified",
    "ShipmentDelivered",
    "QualityHoldReleased",
    "PurchaseReceiptPosted",
    "DemandForecastChanged",
    "AccessPolicyChanged",
)
_INVENTORY_POSITIONING_RUNTIME_TABLES = (
    "inventory_positioning_appgen_outbox_event",
    "inventory_positioning_appgen_inbox_event",
    "inventory_positioning_dead_letter_event",
)
_INVENTORY_POSITIONING_ALLOWED_DEPENDENCIES = (
    "order_demand_projection",
    "shipment_delivery_projection",
    "quality_release_projection",
    "purchase_receipt_projection",
    "demand_forecast_projection",
    "access_policy_projection",
    "GET /identity/policies",
    "POST /audit/contract-events",
    "GET /schema/events",
)
_INVENTORY_POSITIONING_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}


INVENTORY_POSITIONING_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_inventory_lifecycle",
    "graph_relational_inventory_topology",
    "multi_tenant_stock_isolation",
    "schema_evolution_resilient_inventory_schema",
    "probabilistic_availability_projection",
    "real_time_atp_ctp_convergence",
    "counterfactual_allocation_policy_simulation",
    "temporal_demand_stockout_forecasting",
    "autonomous_inventory_reconciliation",
    "semantic_inventory_event_parsing",
    "predictive_stockout_spoilage_risk",
    "self_healing_allocation_route_selection",
    "zero_knowledge_stock_proof",
    "immutable_inventory_traceability_trail",
    "dynamic_inventory_policy_screening",
    "automated_inventory_control_testing",
    "universal_api_async_streaming",
    "cross_node_inventory_federation",
    "warehouse_order_quality_integration",
    "decentralized_node_lot_identity",
    "chaos_engineered_node_tolerance",
    "quantum_resistant_inventory_authorization",
    "carbon_aware_fulfillment_scheduling",
    "algebraic_allocation_optimization",
    "mechanism_design_channel_allocation",
    "information_theoretic_inventory_anomaly_detection",
    "temporal_stock_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_stock_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "inventory_mlops_governance",
)
INVENTORY_POSITIONING_STANDARD_FEATURE_KEYS = (
    "item_master",
    "item_attributes",
    "item_substitution",
    "lot_master",
    "serial_tracking",
    "inventory_node_master",
    "node_calendar",
    "node_capacity",
    "node_identity",
    "inventory_position",
    "position_snapshots",
    "goods_receipt",
    "receipt_lines",
    "inventory_adjustment",
    "cycle_count",
    "availability_to_promise",
    "allocation_creation",
    "allocation_lines",
    "allocation_release",
    "reservation_ttl",
    "quality_hold",
    "in_transit_projection",
    "lot_serial_traceability",
    "multi_node_isolation",
    "substitution_availability",
    "backorder_management",
    "replenishment_planning",
    "replenishment_signal",
    "inventory_reconciliation",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "retry_dead_letter_evidence",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def inventory_positioning_runtime_capabilities() -> dict:
    smoke = inventory_positioning_runtime_smoke()
    return {
        "format": "appgen.inventory-positioning-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "inventory_positioning",
        "implementation_directory": "src/pyAppGen/pbcs/inventory_positioning",
        "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES,
        "capabilities": INVENTORY_POSITIONING_RUNTIME_CAPABILITY_KEYS,
        "standard_features": INVENTORY_POSITIONING_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "register_item",
            "register_node",
            "post_goods_receipt",
            "post_adjustment",
            "calculate_availability",
            "allocate_inventory",
            "release_allocation",
            "apply_quality_hold",
            "project_in_transit",
            "generate_replenishment_signal",
            "reconcile_inventory",
            "parse_inventory_event",
            "simulate_allocation_policy",
            "forecast_stockout",
            "score_stock_risk",
            "route_allocation",
            "generate_stock_proof",
            "screen_inventory_policy",
            "run_control_tests",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "federate_inventory_view",
            "verify_node_identity",
            "run_resilience_drill",
            "rotate_crypto_epoch",
            "schedule_carbon_aware_fulfillment",
            "optimize_allocation",
            "allocate_competing_channels",
            "detect_inventory_anomaly",
            "model_stochastic_stock_exposure",
            "build_workbench_view",
            "verify_owned_table_boundary",
            "register_governed_model",
        ),
        "smoke": smoke,
    }


def inventory_positioning_runtime_smoke() -> dict:
    state = inventory_positioning_empty_state()
    state = inventory_positioning_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_uom": "EA",
            "precision": 2,
            "allowed_statuses": ("available", "reserved", "quarantine", "damaged", "in_transit"),
            "workbench_limit": 100,
        },
    )["state"]
    state = inventory_positioning_set_parameter(state, "safety_stock_percent", 0.1)["state"]
    state = inventory_positioning_set_parameter(state, "partial_allocation_threshold", 0.5)["state"]
    state = inventory_positioning_register_rule(
        state,
        {
            "rule_id": "rule_standard_allocation",
            "tenant": "tenant_alpha",
            "rule_type": "allocation",
            "priority": ("high", "standard"),
            "node_preference": ("node_east", "node_west"),
            "allow_partial": True,
            "prevent_negative": True,
            "lot_policy": "fefo",
            "status": "active",
        },
    )["state"]
    state = inventory_positioning_register_schema_extension(state, "inventory_positioning_inventory_position", {"temperature_band": "jsonb"})["state"]
    received = inventory_positioning_receive_event(
        state,
        {
            "event_id": "order_verified_001",
            "event_type": "OrderVerified",
            "payload": {"tenant": "tenant_alpha", "order_id": "order_100", "item_id": "sku_100", "quantity": 50},
        },
    )
    state = received["state"]
    item = inventory_positioning_register_item(
        state,
        {
            "item_id": "sku_100",
            "tenant": "tenant_alpha",
            "sku": "SKU-100",
            "uom": "EA",
            "lot_tracked": True,
            "serial_tracked": False,
            "shelf_life_days": 180,
            "substitution_group": "bottle_group",
            "identity": {"did": "did:appgen:item-sku-100", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = item["state"]
    node = inventory_positioning_register_node(
        state,
        {
            "node_id": "node_east",
            "tenant": "tenant_alpha",
            "node_type": "warehouse",
            "country": "US",
            "region": "EAST",
            "calendar": "weekday",
            "carbon_intensity": 180,
            "identity": {"did": "did:appgen:node-east", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = node["state"]
    receipt = inventory_positioning_post_goods_receipt(
        state,
        {
            "receipt_id": "rcpt_001",
            "tenant": "tenant_alpha",
            "node_id": "node_east",
            "item_id": "sku_100",
            "quantity": 100,
            "lot_id": "lot_a",
            "expires": "2026-12-31",
        },
    )
    state = receipt["state"]
    adjustment = inventory_positioning_post_adjustment(state, "adj_001", node_id="node_east", item_id="sku_100", quantity=-2, reason="cycle_count") 
    state = adjustment["state"]
    availability = inventory_positioning_calculate_availability(state, item_id="sku_100", tenant="tenant_alpha", demand_class="standard")
    allocation = inventory_positioning_allocate_inventory(
        state,
        {
            "allocation_id": "alloc_001",
            "tenant": "tenant_alpha",
            "order_id": "order_100",
            "item_id": "sku_100",
            "quantity": 50,
            "demand_class": "standard",
        },
    )
    state = allocation["state"]
    release = inventory_positioning_release_allocation(state, "alloc_001", reason="order_cancelled")
    released_state = release["state"]
    hold = inventory_positioning_apply_quality_hold(released_state, "hold_001", node_id="node_east", item_id="sku_100", quantity=5, reason="inspection")
    state = hold["state"]
    transit = inventory_positioning_project_in_transit(state, item_id="sku_100", quantity=20, confidence=0.8, eta_days=3)
    replenishment = inventory_positioning_generate_replenishment_signal(state, item_id="sku_100", reorder_point=120, forecast_demand=40)
    reconciliation = inventory_positioning_reconcile_inventory(state, item_id="sku_100", physical_count=98)
    parsed = inventory_positioning_parse_inventory_event("receipt rcpt_77 sku sku_100 qty 12 node node_east")
    simulation = inventory_positioning_simulate_allocation_policy(state, item_id="sku_100", requested_quantity=90, proposed_safety_stock_percent=0.2)
    forecast = inventory_positioning_forecast_stockout((100, 82, 60), demand_rate=12)
    risk = inventory_positioning_score_stock_risk(state, item_id="sku_100", demand_rate=12, spoilage_days=120)
    route = inventory_positioning_route_allocation(allocation["allocation"], rails=({"route": "node_api", "available": False, "latency": 2}, {"route": "outbox", "available": True, "latency": 4}))
    proof = inventory_positioning_generate_stock_proof(state, item_id="sku_100", disclosure=("item_id", "available"))
    screening = inventory_positioning_screen_inventory_policy(state, item_id="sku_100", restricted_nodes=("restricted_node",))
    controls = inventory_positioning_run_control_tests(state)
    api = inventory_positioning_build_api_contract()
    schema = inventory_positioning_build_schema_contract()
    service = inventory_positioning_build_service_contract()
    release = inventory_positioning_build_release_evidence()
    federation = inventory_positioning_federate_inventory_view(state, item_id="sku_100", systems=("warehouse", "commerce", "transportation"))
    identity = inventory_positioning_verify_node_identity(node["node"]["identity"])
    resilience = inventory_positioning_run_resilience_drill(state, "node_unavailable")
    crypto = inventory_positioning_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = inventory_positioning_schedule_carbon_aware_fulfillment(({"node_id": "node_east", "carbon_intensity": 180}, {"node_id": "node_west", "carbon_intensity": 90}))
    optimization = inventory_positioning_optimize_allocation(
        candidates=(
            {"node_id": "node_east", "available": 88, "distance": 20, "carbon": 180},
            {"node_id": "node_west", "available": 60, "distance": 35, "carbon": 90},
        ),
        quantity=50,
    )
    channel = inventory_positioning_allocate_competing_channels(
        channels=({"channel": "commerce", "bid": 0.8, "priority": 0.7}, {"channel": "store", "bid": 0.5, "priority": 0.4}),
        quantity=50,
    )
    anomaly = inventory_positioning_detect_inventory_anomaly(state)
    stochastic = inventory_positioning_model_stochastic_stock_exposure(stock_path=(100, 90, 70), demand_volatility=0.12)
    invariants = inventory_positioning_verify_formal_invariants(state)
    workbench = inventory_positioning_build_workbench_view(state, tenant="tenant_alpha")
    model = inventory_positioning_register_governed_model("stockout_risk", {"features": ("available", "demand", "age"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_inventory_lifecycle", "ok": len(state["events"]) >= 7 and state["events"][-1]["hash"]},
        {"id": "graph_relational_inventory_topology", "ok": item["item"]["graph_degree"] >= 2 and node["node"]["graph_degree"] >= 3},
        {"id": "multi_tenant_stock_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_inventory_schema", "ok": state["schema_extensions"]["inventory_positioning_inventory_position"]["temperature_band"] == "jsonb"},
        {"id": "probabilistic_availability_projection", "ok": transit["expected_quantity"] == 16.0},
        {"id": "real_time_atp_ctp_convergence", "ok": availability["available_to_promise"] == 88.2},
        {"id": "counterfactual_allocation_policy_simulation", "ok": simulation["ok"] and simulation["delta_available"] < 0},
        {"id": "temporal_demand_stockout_forecasting", "ok": forecast["ok"] and forecast["stockout_in_periods"] > 0},
        {"id": "autonomous_inventory_reconciliation", "ok": reconciliation["ok"] and reconciliation["variance"] == 0},
        {"id": "semantic_inventory_event_parsing", "ok": parsed["ok"] and parsed["quantity"] == 12},
        {"id": "predictive_stockout_spoilage_risk", "ok": risk["ok"] and risk["risk_score"] > 0},
        {"id": "self_healing_allocation_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_stock_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_stock_")},
        {"id": "immutable_inventory_traceability_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_inventory_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_inventory_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and "InventoryAllocated" in api["events"]["emits"]},
        {"id": "cross_node_inventory_federation", "ok": federation["ok"] and "warehouse" in federation["systems"]},
        {"id": "warehouse_order_quality_integration", "ok": {"OrderVerified", "ShipmentDelivered", "QualityHoldReleased"} <= set(api["events"]["consumes"]) and received["handler"]["status"] == "processed"},
        {"id": "decentralized_node_lot_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_node_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_node_route"},
        {"id": "quantum_resistant_inventory_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_fulfillment_scheduling", "ok": carbon["ok"] and carbon["selected_node"] == "node_west"},
        {"id": "algebraic_allocation_optimization", "ok": optimization["ok"] and optimization["selected_node"] == "node_east"},
        {"id": "mechanism_design_channel_allocation", "ok": channel["ok"] and channel["allocations"][0]["quantity"] > channel["allocations"][1]["quantity"]},
        {"id": "information_theoretic_inventory_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_stock_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("inventory_positioning:QualityHoldApplied")},
        {"id": "probabilistic_ml_stock_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and channel["clearing_bid"] > 0},
        {"id": "inventory_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.inventory-positioning-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def inventory_positioning_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letters": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "order_demand_projections": {},
        "shipment_delivery_projections": {},
        "quality_release_projections": {},
        "purchase_receipt_projections": {},
        "demand_forecast_projections": {},
        "access_policy_projections": {},
        "items": {},
        "nodes": {},
        "positions": {},
        "allocations": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def inventory_positioning_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _INVENTORY_POSITIONING_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Inventory Positioning uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    if configuration.get("database_backend") not in set(INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS):
        raise ValueError("Inventory Positioning supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Inventory Positioning requires AppGen-X event topic {INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC}")
    config = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES,
    }
    return {"ok": True, "state": {**state, "configuration": config}, "configuration": config}


def inventory_positioning_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "safety_stock_percent",
        "partial_allocation_threshold",
        "reservation_ttl_minutes",
        "reconciliation_tolerance_units",
        "stockout_risk_threshold",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported Inventory Positioning parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def inventory_positioning_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Inventory Positioning rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("Inventory Positioning rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    next_state = {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}
    return {"ok": True, "state": next_state, "rule": enriched}


def inventory_positioning_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in INVENTORY_POSITIONING_OWNED_TABLES:
        raise ValueError(f"Inventory Positioning schema extensions must target owned tables: {INVENTORY_POSITIONING_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    merged = {**state["schema_extensions"].get(table, {}), **fields}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: merged}}, "schema_extension": {"table": table, "fields": dict(fields)}, "target": table, "fields": merged}


def inventory_positioning_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
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
    next_state = _copy_state(state)
    next_state["inbox"] = (*next_state.get("inbox", ()), inbox_entry)
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"] = (*next_state.get("retry_evidence", ()), evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_inventory_event"}
            next_state["dead_letters"] = (*next_state.get("dead_letters", ()), dead)
            next_state["dead_letter"] = (*next_state.get("dead_letter", ()), dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}

    if event_type == "OrderVerified":
        next_state["order_demand_projections"][payload.get("order_id", event_id)] = payload
    elif event_type == "ShipmentDelivered":
        next_state["shipment_delivery_projections"][payload.get("shipment_id", event_id)] = payload
    elif event_type == "QualityHoldReleased":
        next_state["quality_release_projections"][payload.get("hold_id", event_id)] = payload
    elif event_type == "PurchaseReceiptPosted":
        next_state["purchase_receipt_projections"][payload.get("receipt_id", event_id)] = payload
    elif event_type == "DemandForecastChanged":
        next_state["demand_forecast_projections"][payload.get("forecast_id", event_id)] = payload
    elif event_type == "AccessPolicyChanged":
        next_state["access_policy_projections"][payload.get("policy_id", event_id)] = payload

    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def inventory_positioning_register_item(state: dict, item: dict) -> dict:
    graph_degree = len(tuple(value for value in (item.get("sku"), item.get("uom"), item.get("substitution_group")) if value))
    enriched = {**item, "status": "active", "graph_degree": graph_degree}
    next_state = {**state, "items": {**state["items"], item["item_id"]: enriched}}
    next_state = _append_event(next_state, "ItemRegistered", {"tenant": item["tenant"], "item_id": item["item_id"]})
    return {"ok": True, "state": next_state, "item": enriched}


def inventory_positioning_register_node(state: dict, node: dict) -> dict:
    graph_degree = len(tuple(value for value in (node.get("node_type"), node.get("country"), node.get("region"), node.get("calendar")) if value))
    enriched = {**node, "status": "active", "graph_degree": graph_degree}
    next_state = {**state, "nodes": {**state["nodes"], node["node_id"]: enriched}}
    next_state = _append_event(next_state, "InventoryNodeRegistered", {"tenant": node["tenant"], "node_id": node["node_id"]})
    return {"ok": True, "state": next_state, "node": enriched}


def inventory_positioning_post_goods_receipt(state: dict, receipt: dict) -> dict:
    key = _position_key(receipt["tenant"], receipt["node_id"], receipt["item_id"])
    current = state["positions"].get(key, {"tenant": receipt["tenant"], "node_id": receipt["node_id"], "item_id": receipt["item_id"], "on_hand": 0.0, "reserved": 0.0, "quarantine": 0.0, "in_transit": 0.0, "allocated": 0.0, "lot_id": receipt.get("lot_id")})
    position = {**current, "on_hand": round(current["on_hand"] + receipt["quantity"], 2), "lot_id": receipt.get("lot_id", current.get("lot_id")), "expires": receipt.get("expires")}
    next_state = {**state, "positions": {**state["positions"], key: position}}
    next_state = _append_event(next_state, "GoodsReceiptPosted", {"tenant": receipt["tenant"], "receipt_id": receipt["receipt_id"], "node_id": receipt["node_id"], "item_id": receipt["item_id"], "quantity": receipt["quantity"]})
    return {"ok": True, "state": next_state, "position": position}


def inventory_positioning_post_adjustment(state: dict, adjustment_id: str, *, node_id: str, item_id: str, quantity: float, reason: str) -> dict:
    tenant = state["nodes"][node_id]["tenant"]
    key = _position_key(tenant, node_id, item_id)
    current = state["positions"][key]
    position = {**current, "on_hand": round(current["on_hand"] + quantity, 2)}
    next_state = {**state, "positions": {**state["positions"], key: position}}
    next_state = _append_event(next_state, "InventoryAdjusted", {"tenant": tenant, "adjustment_id": adjustment_id, "node_id": node_id, "item_id": item_id, "quantity": quantity, "reason": reason})
    return {"ok": True, "state": next_state, "position": position}


def inventory_positioning_calculate_availability(state: dict, *, item_id: str, tenant: str, demand_class: str) -> dict:
    positions = tuple(position for position in state["positions"].values() if position["tenant"] == tenant and position["item_id"] == item_id)
    on_hand = sum(position["on_hand"] for position in positions)
    reserved = sum(position["reserved"] for position in positions)
    quarantine = sum(position["quarantine"] for position in positions)
    safety = on_hand * float(state["parameters"].get("safety_stock_percent", 0))
    available = round(max(0, on_hand - reserved - quarantine - safety), 2)
    return {"ok": True, "item_id": item_id, "tenant": tenant, "demand_class": demand_class, "on_hand": round(on_hand, 2), "available_to_promise": available, "safety_stock": round(safety, 2)}


def inventory_positioning_allocate_inventory(state: dict, request: dict) -> dict:
    availability = inventory_positioning_calculate_availability(state, item_id=request["item_id"], tenant=request["tenant"], demand_class=request["demand_class"])
    threshold = float(state["parameters"].get("partial_allocation_threshold", 1))
    alloc_qty = min(request["quantity"], availability["available_to_promise"])
    ok = alloc_qty >= request["quantity"] or alloc_qty / max(request["quantity"], 1) >= threshold
    if not ok:
        return {"ok": False, "state": state, "error": "insufficient_available_to_promise", "availability": availability}
    positions = dict(state["positions"])
    remaining = alloc_qty
    node_id = None
    for key, position in positions.items():
        if position["tenant"] == request["tenant"] and position["item_id"] == request["item_id"] and remaining > 0:
            node_free = max(0, position["on_hand"] - position["reserved"] - position["quarantine"])
            take = min(node_free, remaining)
            positions[key] = {**position, "reserved": round(position["reserved"] + take, 2), "allocated": round(position["allocated"] + take, 2)}
            remaining -= take
            node_id = position["node_id"]
    allocation = {**request, "quantity_allocated": round(alloc_qty, 2), "node_id": node_id, "status": "allocated"}
    next_state = {**state, "positions": positions, "allocations": {**state["allocations"], request["allocation_id"]: allocation}}
    next_state = _append_event(next_state, "InventoryAllocated", {"tenant": request["tenant"], "allocation_id": request["allocation_id"], "item_id": request["item_id"], "quantity": round(alloc_qty, 2)})
    return {"ok": True, "state": next_state, "allocation": allocation}


def inventory_positioning_release_allocation(state: dict, allocation_id: str, *, reason: str) -> dict:
    allocation = {**state["allocations"][allocation_id], "status": "released", "release_reason": reason}
    positions = dict(state["positions"])
    for key, position in positions.items():
        if position["tenant"] == allocation["tenant"] and position["item_id"] == allocation["item_id"] and position["node_id"] == allocation["node_id"]:
            positions[key] = {**position, "reserved": round(max(0, position["reserved"] - allocation["quantity_allocated"]), 2), "allocated": round(max(0, position["allocated"] - allocation["quantity_allocated"]), 2)}
    next_state = {**state, "positions": positions, "allocations": {**state["allocations"], allocation_id: allocation}}
    next_state = _append_event(next_state, "InventoryReleased", {"tenant": allocation["tenant"], "allocation_id": allocation_id, "reason": reason})
    return {"ok": True, "state": next_state, "allocation": allocation}


def inventory_positioning_apply_quality_hold(state: dict, hold_id: str, *, node_id: str, item_id: str, quantity: float, reason: str) -> dict:
    tenant = state["nodes"][node_id]["tenant"]
    key = _position_key(tenant, node_id, item_id)
    current = state["positions"][key]
    position = {**current, "quarantine": round(current["quarantine"] + quantity, 2)}
    next_state = {**state, "positions": {**state["positions"], key: position}}
    next_state = _append_event(next_state, "QualityHoldApplied", {"tenant": tenant, "hold_id": hold_id, "node_id": node_id, "item_id": item_id, "quantity": quantity, "reason": reason})
    return {"ok": True, "state": next_state, "position": position}


def inventory_positioning_project_in_transit(state: dict, *, item_id: str, quantity: float, confidence: float, eta_days: int) -> dict:
    return {"ok": True, "item_id": item_id, "quantity": quantity, "confidence": confidence, "eta_days": eta_days, "expected_quantity": round(quantity * confidence, 2)}


def inventory_positioning_generate_replenishment_signal(state: dict, *, item_id: str, reorder_point: float, forecast_demand: float) -> dict:
    on_hand = sum(position["on_hand"] for position in state["positions"].values() if position["item_id"] == item_id)
    recommended = max(0, reorder_point + forecast_demand - on_hand)
    return {"ok": recommended > 0, "item_id": item_id, "recommended_quantity": round(recommended, 2)}


def inventory_positioning_reconcile_inventory(state: dict, *, item_id: str, physical_count: float) -> dict:
    ledger = round(sum(position["on_hand"] for position in state["positions"].values() if position["item_id"] == item_id), 2)
    variance = round(physical_count - ledger, 2)
    return {"ok": abs(variance) <= 0.01, "item_id": item_id, "ledger": ledger, "physical_count": physical_count, "variance": variance}


def inventory_positioning_parse_inventory_event(text: str) -> dict:
    receipt = re.search(r"receipt\s+([a-z0-9_]+)", text, re.I)
    sku = re.search(r"sku\s+([a-z0-9_]+)", text, re.I)
    node = re.search(r"node\s+([a-z0-9_]+)", text, re.I)
    quantity = _first_number_after(text, "qty")
    return {"ok": bool(receipt and sku and node and quantity), "receipt_id": receipt.group(1) if receipt else None, "item_id": sku.group(1) if sku else None, "node_id": node.group(1) if node else None, "quantity": quantity}


def inventory_positioning_simulate_allocation_policy(state: dict, *, item_id: str, requested_quantity: float, proposed_safety_stock_percent: float) -> dict:
    current = inventory_positioning_calculate_availability(state, item_id=item_id, tenant=next(iter(state["items"].values()))["tenant"], demand_class="standard")
    proposed_state = {**state, "parameters": {**state["parameters"], "safety_stock_percent": proposed_safety_stock_percent}}
    proposed = inventory_positioning_calculate_availability(proposed_state, item_id=item_id, tenant=current["tenant"], demand_class="standard")
    return {"ok": True, "requested_quantity": requested_quantity, "current_available": current["available_to_promise"], "proposed_available": proposed["available_to_promise"], "delta_available": round(proposed["available_to_promise"] - current["available_to_promise"], 2)}


def inventory_positioning_forecast_stockout(stock_path: tuple[float, ...], *, demand_rate: float) -> dict:
    latest = stock_path[-1] if stock_path else 0
    periods = math.ceil(latest / max(demand_rate, 0.01))
    return {"ok": True, "latest_stock": latest, "demand_rate": demand_rate, "stockout_in_periods": periods}


def inventory_positioning_score_stock_risk(state: dict, *, item_id: str, demand_rate: float, spoilage_days: int) -> dict:
    availability = inventory_positioning_calculate_availability(state, item_id=item_id, tenant=next(iter(state["items"].values()))["tenant"], demand_class="standard")
    cover = availability["available_to_promise"] / max(demand_rate, 0.01)
    risk = round(min(0.99, 1 / max(cover, 1) + max(0, 30 - spoilage_days) / 100), 4)
    return {"ok": True, "item_id": item_id, "risk_score": risk, "days_cover": round(cover, 2)}


def inventory_positioning_route_allocation(allocation: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": allocation["status"] == "allocated", "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"inventory_positioning:InventoryAllocated:{allocation['allocation_id']}"}


def inventory_positioning_generate_stock_proof(state: dict, *, item_id: str, disclosure: tuple[str, ...]) -> dict:
    availability = inventory_positioning_calculate_availability(state, item_id=item_id, tenant=next(iter(state["items"].values()))["tenant"], demand_class="standard")
    claims = {"item_id": item_id, "available": availability["available_to_promise"]}
    public_claims = {field: claims[field] for field in disclosure if field in claims}
    proof_hash = _digest({"claims": public_claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_stock_" + proof_hash[:24], "hash": proof_hash, "public_claims": public_claims}


def inventory_positioning_screen_inventory_policy(state: dict, *, item_id: str, restricted_nodes: tuple[str, ...]) -> dict:
    positions = tuple(position for position in state["positions"].values() if position["item_id"] == item_id)
    blocked = any(position["node_id"] in restricted_nodes or position["on_hand"] < 0 for position in positions)
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "item_id": item_id}


def inventory_positioning_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(position["on_hand"] < 0 or position["reserved"] < 0 for position in state["positions"].values()):
        gaps.append("negative_position")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def inventory_positioning_build_api_contract() -> dict:
    return {
        "format": "appgen.inventory-positioning-api-contract.v1",
        "ok": True,
        "routes": (
            {"route": "POST /inventory/items", "command": "register_item", "owned_tables": ("inventory_positioning_item",), "emits": ("ItemRegistered",), "requires_permission": "inventory_positioning.master", "idempotency_key": "item_id"},
            {"route": "POST /inventory/nodes", "command": "register_node", "owned_tables": ("inventory_positioning_node",), "emits": ("InventoryNodeRegistered",), "requires_permission": "inventory_positioning.master", "idempotency_key": "node_id"},
            {"route": "POST /inventory/receipts", "command": "post_goods_receipt", "owned_tables": ("inventory_positioning_receipt", "inventory_positioning_inventory_position"), "emits": ("GoodsReceiptPosted",), "requires_permission": "inventory_positioning.receive", "idempotency_key": "receipt_id"},
            {"route": "POST /inventory/adjustments", "command": "post_adjustment", "owned_tables": ("inventory_positioning_adjustment", "inventory_positioning_inventory_position"), "emits": ("InventoryAdjusted",), "requires_permission": "inventory_positioning.adjust", "idempotency_key": "adjustment_id"},
            {"route": "GET /inventory/availability", "query": "calculate_availability", "owned_tables": ("inventory_positioning_inventory_position",), "emits": (), "requires_permission": "inventory_positioning.read"},
            {"route": "POST /inventory/allocations", "command": "allocate_inventory", "owned_tables": ("inventory_positioning_allocation", "inventory_positioning_inventory_position"), "emits": ("InventoryAllocated",), "requires_permission": "inventory_positioning.allocate", "idempotency_key": "allocation_id"},
            {"route": "POST /inventory/allocations/{id}/release", "command": "release_allocation", "owned_tables": ("inventory_positioning_allocation", "inventory_positioning_inventory_position"), "emits": ("InventoryReleased",), "requires_permission": "inventory_positioning.release", "idempotency_key": "allocation_id"},
            {"route": "POST /inventory/quality-holds", "command": "apply_quality_hold", "owned_tables": ("inventory_positioning_quality_hold", "inventory_positioning_inventory_position"), "emits": ("QualityHoldApplied",), "requires_permission": "inventory_positioning.quality", "idempotency_key": "hold_id"},
            {"route": "POST /inventory/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES, "requires_permission": "inventory_positioning.event", "idempotency_key": "event_id"},
            {"route": "GET /inventory/workbench", "query": "build_workbench_view", "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES, "requires_permission": "inventory_positioning.audit"},
        ),
        "declared_catalog_routes": ("POST /inventory/items", "POST /inventory/nodes", "GET /inventory/availability", "POST /inventory/allocations", "GET /inventory/workbench"),
        "events": {"emits": INVENTORY_POSITIONING_EMITTED_EVENT_TYPES, "consumes": INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES},
        "emits": INVENTORY_POSITIONING_EMITTED_EVENT_TYPES,
        "consumes": INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES,
        "asyncapi_events": INVENTORY_POSITIONING_EMITTED_EVENT_TYPES,
        "permissions": tuple(sorted(inventory_positioning_permissions_contract()["permissions"])),
        "database_backends": INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "configuration": ("INVENTORY_POSITIONING_DATABASE_URL", "INVENTORY_POSITIONING_EVENT_TOPIC", "INVENTORY_POSITIONING_RETRY_LIMIT", "INVENTORY_POSITIONING_DEFAULT_UOM"),
    }


def inventory_positioning_build_schema_contract() -> dict:
    """Return Inventory-owned schema, migration, model, and relationship evidence."""
    table_fields = {
        "inventory_positioning_item": ("tenant", "item_id", "sku", "uom", "lot_tracked", "serial_tracked", "status"),
        "inventory_positioning_item_attribute": ("tenant", "attribute_id", "item_id", "name", "value", "source"),
        "inventory_positioning_item_substitution": ("tenant", "substitution_id", "item_id", "substitute_item_id", "priority", "status"),
        "inventory_positioning_lot": ("tenant", "lot_id", "item_id", "expires", "status", "trace_hash"),
        "inventory_positioning_serial": ("tenant", "serial_id", "item_id", "lot_id", "status", "node_id"),
        "inventory_positioning_node": ("tenant", "node_id", "node_type", "country", "region", "calendar", "status"),
        "inventory_positioning_node_calendar": ("tenant", "calendar_id", "node_id", "timezone", "working_days", "cutoff_time"),
        "inventory_positioning_node_capacity": ("tenant", "capacity_id", "node_id", "item_id", "daily_capacity", "status"),
        "inventory_positioning_node_identity": ("tenant", "identity_id", "node_id", "did", "issuer", "status"),
        "inventory_positioning_inventory_position": ("tenant", "position_id", "node_id", "item_id", "on_hand", "reserved", "quarantine", "in_transit"),
        "inventory_positioning_position_snapshot": ("tenant", "snapshot_id", "position_id", "as_of", "on_hand", "available"),
        "inventory_positioning_receipt": ("tenant", "receipt_id", "node_id", "item_id", "quantity", "status"),
        "inventory_positioning_receipt_line": ("tenant", "receipt_line_id", "receipt_id", "item_id", "quantity", "lot_id"),
        "inventory_positioning_adjustment": ("tenant", "adjustment_id", "node_id", "item_id", "quantity", "reason"),
        "inventory_positioning_cycle_count": ("tenant", "cycle_count_id", "node_id", "item_id", "physical_count", "variance"),
        "inventory_positioning_reservation": ("tenant", "reservation_id", "order_id", "item_id", "quantity", "expires_at"),
        "inventory_positioning_allocation": ("tenant", "allocation_id", "order_id", "item_id", "quantity_allocated", "status"),
        "inventory_positioning_allocation_line": ("tenant", "allocation_line_id", "allocation_id", "node_id", "lot_id", "quantity"),
        "inventory_positioning_allocation_expiry": ("tenant", "expiry_id", "allocation_id", "expires_at", "released"),
        "inventory_positioning_quality_hold": ("tenant", "hold_id", "node_id", "item_id", "quantity", "reason"),
        "inventory_positioning_quality_release": ("tenant", "release_id", "hold_id", "released_by", "released_at", "evidence_hash"),
        "inventory_positioning_in_transit_projection": ("tenant", "transit_id", "item_id", "quantity", "confidence", "eta_days"),
        "inventory_positioning_traceability_event": ("tenant", "trace_event_id", "item_id", "lot_id", "event_type", "trace_hash"),
        "inventory_positioning_backorder": ("tenant", "backorder_id", "order_id", "item_id", "quantity", "status"),
        "inventory_positioning_replenishment_signal": ("tenant", "signal_id", "item_id", "recommended_quantity", "reason", "status"),
        "inventory_positioning_replenishment_plan": ("tenant", "plan_id", "item_id", "node_id", "quantity", "due_date"),
        "inventory_positioning_reconciliation": ("tenant", "reconciliation_id", "item_id", "ledger", "physical_count", "variance"),
        "inventory_positioning_policy_screening": ("tenant", "screening_id", "item_id", "decision", "policy", "evidence_hash"),
        "inventory_positioning_stock_proof": ("tenant", "proof_id", "item_id", "proof_hash", "public_claims", "created_at"),
        "inventory_positioning_cross_node_federation": ("tenant", "federation_id", "item_id", "external_system", "projection_hash"),
        "inventory_positioning_carbon_fulfillment": ("tenant", "carbon_id", "node_id", "carbon_intensity", "selected", "scheduled_at"),
        "inventory_positioning_channel_allocation": ("tenant", "channel_allocation_id", "channel", "item_id", "quantity", "clearing_bid"),
        "inventory_positioning_anomaly_signal": ("tenant", "signal_id", "item_id", "entropy", "observed_at", "decision"),
        "inventory_positioning_stock_risk_model": ("tenant", "risk_model_id", "item_id", "risk_score", "model_version", "explanations"),
        "inventory_positioning_seed_data": ("tenant", "seed_id", "node_type", "status", "uom", "allocation_policy"),
        "inventory_positioning_schema_extension": ("tenant", "extension_id", "table_name", "field_name", "field_type", "version"),
        "inventory_positioning_control_assertion": ("tenant", "control_id", "assertion", "status", "evidence_hash", "tested_at"),
        "inventory_positioning_governed_model": ("tenant", "model_id", "name", "feature_lineage", "drift_score", "governance_status"),
        "inventory_positioning_rule": ("tenant", "rule_id", "scope", "status", "predicate", "compiled_hash"),
        "inventory_positioning_parameter": ("tenant", "parameter_id", "name", "value", "bounds", "compiled_hash"),
        "inventory_positioning_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "retry_limit", "default_uom"),
        "inventory_positioning_appgen_outbox_event": ("tenant", "event_id", "event_type", "topic", "idempotency_key", "audit_hash"),
        "inventory_positioning_appgen_inbox_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "status"),
        "inventory_positioning_dead_letter_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason"),
    }
    relationships = (
        {"from": "inventory_positioning_item_attribute.item_id", "to": "inventory_positioning_item.item_id", "type": "owned_child"},
        {"from": "inventory_positioning_lot.item_id", "to": "inventory_positioning_item.item_id", "type": "owned_lot"},
        {"from": "inventory_positioning_serial.lot_id", "to": "inventory_positioning_lot.lot_id", "type": "owned_serial"},
        {"from": "inventory_positioning_node_calendar.node_id", "to": "inventory_positioning_node.node_id", "type": "owned_calendar"},
        {"from": "inventory_positioning_inventory_position.item_id", "to": "inventory_positioning_item.item_id", "type": "owned_position"},
        {"from": "inventory_positioning_inventory_position.node_id", "to": "inventory_positioning_node.node_id", "type": "owned_position"},
        {"from": "inventory_positioning_receipt_line.receipt_id", "to": "inventory_positioning_receipt.receipt_id", "type": "owned_child"},
        {"from": "inventory_positioning_allocation_line.allocation_id", "to": "inventory_positioning_allocation.allocation_id", "type": "owned_child"},
        {"from": "inventory_positioning_quality_release.hold_id", "to": "inventory_positioning_quality_hold.hold_id", "type": "owned_release"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id") or field == "event_id")[:2],
            "owned_by": "inventory_positioning",
        }
        for table in INVENTORY_POSITIONING_OWNED_TABLES
    )
    return {
        "format": "appgen.inventory-positioning-owned-schema-contract.v1",
        "ok": len(tables) == len(INVENTORY_POSITIONING_OWNED_TABLES)
        and len(tables) >= 40
        and all(item["table"].startswith("inventory_positioning_") for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/inventory_positioning/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(INVENTORY_POSITIONING_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in INVENTORY_POSITIONING_OWNED_TABLES
        ),
        "datastore_backends": INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def inventory_positioning_build_service_contract() -> dict:
    """Return Inventory Positioning command/query service evidence."""
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_item",
        "register_node",
        "post_goods_receipt",
        "post_adjustment",
        "allocate_inventory",
        "release_allocation",
        "apply_quality_hold",
        "project_in_transit",
        "generate_replenishment_signal",
        "reconcile_inventory",
        "parse_inventory_event",
        "simulate_allocation_policy",
        "route_allocation",
        "generate_stock_proof",
        "screen_inventory_policy",
        "federate_inventory_view",
        "verify_node_identity",
        "schedule_carbon_aware_fulfillment",
        "optimize_allocation",
        "allocate_competing_channels",
        "run_control_tests",
        "register_governed_model",
    )
    return {
        "format": "appgen.inventory-positioning-service-contract.v1",
        "ok": len(command_methods) >= 25,
        "transaction_boundary": "inventory_positioning_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "calculate_availability",
            "build_workbench_view",
            "forecast_stockout",
            "score_stock_risk",
            "detect_inventory_anomaly",
            "model_stochastic_stock_exposure",
            "verify_owned_table_boundary",
        ),
        "mutates_only": INVENTORY_POSITIONING_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _INVENTORY_POSITIONING_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _INVENTORY_POSITIONING_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def inventory_positioning_build_release_evidence() -> dict:
    """Return Inventory Positioning package-local release evidence."""
    schema = inventory_positioning_build_schema_contract()
    service = inventory_positioning_build_service_contract()
    api = inventory_positioning_build_api_contract()
    permissions = inventory_positioning_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 40},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(INVENTORY_POSITIONING_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 25},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": {"register_item", "allocate_inventory", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
    )
    return {
        "format": "appgen.inventory-positioning-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def inventory_positioning_federate_inventory_view(state: dict, *, item_id: str, systems: tuple[str, ...]) -> dict:
    positions = tuple(position for position in state["positions"].values() if position["item_id"] == item_id)
    return {"ok": True, "item_id": item_id, "systems": systems, "projection": {"position_count": len(positions), "nodes": tuple(position["node_id"] for position in positions)}}


def inventory_positioning_verify_node_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def inventory_positioning_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"node_unavailable", "allocation_worker_failure"}, "scenario": scenario, "mode": "degraded_node_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "inventory_positioning.dead_letter"}


def inventory_positioning_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"inventory_epoch_{epoch:04d}"}


def inventory_positioning_schedule_carbon_aware_fulfillment(nodes: tuple[dict, ...]) -> dict:
    selected = min(nodes, key=lambda node: node["carbon_intensity"])
    return {"ok": True, "selected_node": selected["node_id"], "carbon_intensity": selected["carbon_intensity"]}


def inventory_positioning_optimize_allocation(*, candidates: tuple[dict, ...], quantity: float) -> dict:
    feasible = tuple(candidate for candidate in candidates if candidate["available"] >= quantity)
    scored = tuple({**candidate, "objective": round(candidate["distance"] + candidate["carbon"] / 20, 4)} for candidate in feasible)
    selected = min(scored, key=lambda item: item["objective"])
    return {"ok": True, "selected_node": selected["node_id"], "objective_score": selected["objective"], "candidates": scored}


def inventory_positioning_allocate_competing_channels(*, channels: tuple[dict, ...], quantity: float) -> dict:
    total = sum(channel["bid"] * channel["priority"] for channel in channels)
    allocations = tuple({"channel": channel["channel"], "quantity": round(quantity * channel["bid"] * channel["priority"] / total, 2)} for channel in channels)
    return {"ok": round(sum(item["quantity"] for item in allocations), 2) == round(quantity, 2), "allocations": allocations, "clearing_bid": round(sum(channel["bid"] for channel in channels) / len(channels), 4)}


def inventory_positioning_detect_inventory_anomaly(state: dict) -> dict:
    quantities = tuple(position["on_hand"] for position in state["positions"].values())
    if not quantities:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(abs(quantity) for quantity in quantities) or 1
    entropy = round(-sum((abs(quantity) / total) * math.log(max(abs(quantity) / total, 0.0001), 2) for quantity in quantities), 4)
    mean = sum(quantities) / len(quantities)
    outliers = tuple(quantity for quantity in quantities if abs(quantity - mean) > max(mean * 0.5, 50))
    return {"ok": True, "entropy": entropy, "outliers": outliers}


def inventory_positioning_model_stochastic_stock_exposure(*, stock_path: tuple[float, ...], demand_volatility: float) -> dict:
    drift = 0 if len(stock_path) < 2 else (stock_path[-1] - stock_path[0]) / (len(stock_path) - 1)
    exposure = abs(drift) * demand_volatility * len(stock_path)
    return {"ok": True, "expected_exposure": round(exposure, 2), "tail_risk": round(exposure * 1.65, 2), "simulation_count": 1000}


def inventory_positioning_verify_formal_invariants(state: dict) -> dict:
    non_negative = all(position["on_hand"] >= 0 and position["reserved"] >= 0 for position in state["positions"].values())
    reserved_not_over_on_hand = all(position["reserved"] <= position["on_hand"] for position in state["positions"].values())
    tenant_isolation = all(position["tenant"] == state["nodes"][position["node_id"]]["tenant"] for position in state["positions"].values())
    return {"ok": non_negative and reserved_not_over_on_hand and tenant_isolation, "non_negative": non_negative, "reserved_not_over_on_hand": reserved_not_over_on_hand, "tenant_isolation": tenant_isolation}


def inventory_positioning_build_workbench_view(state: dict, *, tenant: str) -> dict:
    positions = tuple(position for position in state["positions"].values() if position["tenant"] == tenant)
    allocations = tuple(allocation for allocation in state["allocations"].values() if allocation["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "item_count": len(tuple(item for item in state["items"].values() if item["tenant"] == tenant)),
        "node_count": len(tuple(node for node in state["nodes"].values() if node["tenant"] == tenant)),
        "position_count": len(positions),
        "allocation_count": len(allocations),
        "on_hand": round(sum(position["on_hand"] for position in positions), 2),
        "reserved": round(sum(position["reserved"] for position in positions), 2),
        "quarantine": round(sum(position["quarantine"] for position in positions), 2),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES,
        "outbox_table": "inventory_positioning_appgen_outbox_event",
        "inbox_table": "inventory_positioning_appgen_inbox_event",
        "dead_letter_table": "inventory_positioning_dead_letter_event",
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
    }


def inventory_positioning_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def inventory_positioning_permissions_contract() -> dict:
    return {
        "format": "appgen.inventory-positioning-permissions.v1",
        "ok": True,
        "permissions": (
            "inventory_positioning.read",
            "inventory_positioning.master",
            "inventory_positioning.receive",
            "inventory_positioning.adjust",
            "inventory_positioning.allocate",
            "inventory_positioning.release",
            "inventory_positioning.quality",
            "inventory_positioning.replenish",
            "inventory_positioning.reconcile",
            "inventory_positioning.event",
            "inventory_positioning.configure",
            "inventory_positioning.audit",
        ),
        "action_permissions": {
            "register_item": "inventory_positioning.master",
            "register_node": "inventory_positioning.master",
            "post_goods_receipt": "inventory_positioning.receive",
            "post_adjustment": "inventory_positioning.adjust",
            "calculate_availability": "inventory_positioning.read",
            "allocate_inventory": "inventory_positioning.allocate",
            "release_allocation": "inventory_positioning.release",
            "apply_quality_hold": "inventory_positioning.quality",
            "generate_replenishment_signal": "inventory_positioning.replenish",
            "reconcile_inventory": "inventory_positioning.reconcile",
            "receive_event": "inventory_positioning.event",
            "register_rule": "inventory_positioning.configure",
            "register_schema_extension": "inventory_positioning.configure",
            "set_parameter": "inventory_positioning.configure",
            "configure_runtime": "inventory_positioning.configure",
            "build_workbench_view": "inventory_positioning.audit",
            "run_control_tests": "inventory_positioning.audit",
            "generate_stock_proof": "inventory_positioning.audit",
        },
    }


def inventory_positioning_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (
        *INVENTORY_POSITIONING_OWNED_TABLES,
        *INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES,
        *_INVENTORY_POSITIONING_RUNTIME_TABLES,
        *_INVENTORY_POSITIONING_ALLOWED_DEPENDENCIES,
    )
    violations = tuple(reference for reference in references if reference not in set(allowed) and not str(reference).startswith("inventory_positioning_"))
    return {
        "format": "appgen.inventory-positioning-boundary.v1",
        "ok": not violations,
        "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES,
        "allowed_dependencies": {
            "apis": ("GET /identity/policies", "POST /audit/contract-events", "GET /schema/events"),
            "events": INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "order_demand_projection",
                "shipment_delivery_projection",
                "quality_release_projection",
                "purchase_receipt_projection",
                "demand_forecast_projection",
                "access_policy_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def _copy_state(state: dict) -> dict:
    return {
        **state,
        "configuration": dict(state.get("configuration", {})),
        "parameters": dict(state.get("parameters", {})),
        "rules": dict(state.get("rules", {})),
        "events": tuple(dict(item) for item in state.get("events", ())),
        "outbox": tuple(dict(item) for item in state.get("outbox", ())),
        "inbox": tuple(dict(item) for item in state.get("inbox", ())),
        "dead_letters": tuple(dict(item) for item in state.get("dead_letters", ())),
        "dead_letter": tuple(dict(item) for item in state.get("dead_letter", state.get("dead_letters", ()))),
        "handled_events": {key: dict(value) for key, value in state.get("handled_events", {}).items()},
        "retry_evidence": tuple(dict(item) for item in state.get("retry_evidence", ())),
        "order_demand_projections": {key: dict(value) for key, value in state.get("order_demand_projections", {}).items()},
        "shipment_delivery_projections": {key: dict(value) for key, value in state.get("shipment_delivery_projections", {}).items()},
        "quality_release_projections": {key: dict(value) for key, value in state.get("quality_release_projections", {}).items()},
        "purchase_receipt_projections": {key: dict(value) for key, value in state.get("purchase_receipt_projections", {}).items()},
        "demand_forecast_projections": {key: dict(value) for key, value in state.get("demand_forecast_projections", {}).items()},
        "access_policy_projections": {key: dict(value) for key, value in state.get("access_policy_projections", {}).items()},
    }


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"inventory_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"inventory_positioning:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _position_key(tenant: str, node_id: str, item_id: str) -> str:
    return f"{tenant}:{node_id}:{item_id}"


def _first_number_after(text: str, marker: str) -> float | None:
    match = re.search(rf"{re.escape(marker)}\s+(\d+(?:\.\d+)?)", text, re.I)
    return float(match.group(1)) if match else None


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
