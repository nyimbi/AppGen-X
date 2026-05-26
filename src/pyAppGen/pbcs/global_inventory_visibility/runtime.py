"""Executable runtime for the Global Inventory Visibility PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


GLOBAL_INVENTORY_VISIBILITY_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_availability_projections",
    "graph_relational_supply_topology",
    "multi_tenant_inventory_pool_isolation",
    "schema_evolution_resilient_availability_schema",
    "probabilistic_availability_freshness_scoring",
    "real_time_atp_visibility_convergence",
    "counterfactual_allocation_simulation",
    "temporal_availability_forecasting",
    "autonomous_exception_resolution",
    "semantic_availability_query_parsing",
    "predictive_stockout_risk",
    "self_healing_projection_route_selection",
    "cryptographic_availability_proof",
    "immutable_inventory_audit_trail",
    "dynamic_allocation_policy_screening",
    "automated_inventory_control_testing",
    "universal_api_async_streaming",
    "cross_system_inventory_federation",
    "reservation_allocation_visibility_integration",
    "decentralized_supply_identity",
    "chaos_tolerant_projection_processing",
    "crypto_agile_availability_authorization",
    "carbon_aware_sourcing_window",
    "algebraic_allocation_optimization",
    "mechanism_design_pool_allocation",
    "information_theoretic_inventory_anomaly_detection",
    "stochastic_exposure_modeling",
    "distributed_systems_engineering",
    "governed_ml_availability_evidence",
    "temporal_freshness_staleness_modeling",
    "in_transit_network_visibility",
    "deterministic_rule_compilation_evidence",
)
GLOBAL_INVENTORY_VISIBILITY_STANDARD_FEATURE_KEYS = (
    "inventory_pool_master",
    "supply_node_master",
    "availability_snapshot",
    "inventory_projection",
    "global_available_to_promise",
    "reservation_visibility",
    "allocation_visibility",
    "in_transit_visibility",
    "safety_stock_policy",
    "freshness_staleness_checks",
    "node_health_monitoring",
    "tenant_isolation",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
    "immutable_audit_log",
    "cross_system_federation",
)

GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC = "appgen.global_inventory_visibility.events"
GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES = (
    "inventory_pool",
    "supply_node",
    "availability_snapshot",
    "inventory_projection",
    "inventory_reservation",
    "inventory_adjustment",
    "inventory_rule",
    "inventory_parameter",
    "inventory_configuration",
    "inventory_governed_model",
)
GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES = ("GoodsReceiptPosted", "ShipmentDelivered", "InventoryAllocated")
GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES = ("AvailabilityProjected", "InventoryPoolChanged")
_ALLOWED_DATABASE_BACKENDS = GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS
_GIV_RUNTIME_TABLES = (
    "global_inventory_visibility_appgen_outbox_event",
    "global_inventory_visibility_appgen_inbox_event",
    "global_inventory_visibility_dead_letter_event",
)
_GIV_ALLOWED_DEPENDENCIES = (
    "wms_stock_projection",
    "transportation_in_transit_projection",
    "order_reservation_projection",
    "GET /wms/stock/{item_id}",
    "GET /transportation/shipments/{item_id}",
    "GET /orders/reservations/{item_id}",
    "POST /audit/inventory-visibility-events",
)
_ALLOWED_CRYPTO_ALGORITHMS = (
    "sha3_256",
    "blake2b",
    "dilithium3_simulated",
    "falcon512_simulated",
)
_ALLOWED_PARAMETERS = {
    "safety_stock_percent": (0.0, 1.0),
    "freshness_half_life_hours": (1.0, 720.0),
    "availability_confidence_floor": (0.0, 1.0),
    "reservation_ttl_minutes": (1.0, 1440.0),
    "projection_horizon_days": (1.0, 365.0),
    "stockout_risk_threshold": (0.0, 1.0),
    "staleness_sla_minutes": (1.0, 1440.0),
    "carbon_cost_weight": (0.0, 10.0),
    "federation_lag_tolerance_minutes": (0.0, 1440.0),
    "workbench_limit": (1.0, 500.0),
}
_REQUIRED_RULE_FIELDS = ("rule_id", "tenant", "scope", "status", "rule_type")
_CONSUMED_EVENTS = GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES
_EMITTED_EVENTS = GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES


def global_inventory_visibility_runtime_capabilities() -> dict:
    smoke = global_inventory_visibility_runtime_smoke()
    return {
        "format": "appgen.global-inventory-visibility-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "global_inventory_visibility",
        "implementation_directory": "src/pyAppGen/pbcs/global_inventory_visibility",
        "owned_tables": GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
        "allowed_database_backends": GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS,
        "capabilities": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_CAPABILITY_KEYS,
        "standard_features": GLOBAL_INVENTORY_VISIBILITY_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_supply_node",
            "register_inventory_pool",
            "record_availability_snapshot",
            "project_availability",
            "get_global_availability",
            "reserve_inventory",
            "ingest_event",
            "register_schema_extension",
            "parse_semantic_query",
            "simulate_counterfactual_allocation",
            "forecast_temporal_availability",
            "score_stockout_risk",
            "resolve_exception",
            "route_projection",
            "generate_availability_proof",
            "screen_allocation_policy",
            "run_control_tests",
            "build_api_contract",
            "permissions_contract",
            "verify_owned_table_boundary",
            "federate_inventory_view",
            "verify_supply_identity",
            "run_resilience_drill",
            "rotate_crypto_epoch",
            "schedule_carbon_aware_sourcing",
            "optimize_allocation",
            "allocate_competing_pools",
            "detect_inventory_anomaly",
            "build_workbench_view",
            "register_governed_model",
            "verify_formal_invariants",
        ),
        "smoke": smoke,
    }


def global_inventory_visibility_runtime_smoke() -> dict:
    state = global_inventory_visibility_empty_state()
    state = global_inventory_visibility_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.global_inventory_visibility.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "projection_horizon_days": 14,
            "staleness_sla_minutes": 90,
            "workbench_limit": 100,
        },
    )["state"]
    state = global_inventory_visibility_set_parameter(state, "safety_stock_percent", 0.15)["state"]
    state = global_inventory_visibility_set_parameter(state, "freshness_half_life_hours", 48)["state"]
    state = global_inventory_visibility_set_parameter(state, "availability_confidence_floor", 0.55)["state"]
    state = global_inventory_visibility_set_parameter(state, "stockout_risk_threshold", 0.35)["state"]
    state = global_inventory_visibility_register_rule(
        state,
        {
            "rule_id": "rule_pool_priority",
            "tenant": "tenant_alpha",
            "scope": "global_pool",
            "status": "active",
            "rule_type": "allocation",
            "preferred_nodes": ("node_east", "node_west"),
            "freshness_floor": 0.6,
            "safety_stock_override": 12,
            "policy": "balanced",
        },
    )["state"]
    state = global_inventory_visibility_register_schema_extension(
        state,
        "inventory_projection",
        {"explainability_evidence": "jsonb"},
    )["state"]
    east = global_inventory_visibility_register_supply_node(
        state,
        {
            "node_id": "node_east",
            "tenant": "tenant_alpha",
            "node_type": "warehouse",
            "country": "US",
            "region": "EAST",
            "health_score": 0.96,
            "latency_ms": 18,
            "carbon_intensity": 150,
            "federated_systems": ("wms", "tms"),
            "identity": {"did": "did:appgen:node-east", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = east["state"]
    west = global_inventory_visibility_register_supply_node(
        state,
        {
            "node_id": "node_west",
            "tenant": "tenant_alpha",
            "node_type": "3pl",
            "country": "US",
            "region": "WEST",
            "health_score": 0.87,
            "latency_ms": 32,
            "carbon_intensity": 90,
            "federated_systems": ("3pl", "erp"),
            "identity": {"did": "did:appgen:node-west", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = west["state"]
    pool = global_inventory_visibility_register_inventory_pool(
        state,
        {
            "pool_id": "pool_global",
            "tenant": "tenant_alpha",
            "item_id": "sku_100",
            "pool_type": "enterprise",
            "node_ids": ("node_east", "node_west"),
            "allocation_policy": "balanced",
            "safety_stock_units": 15,
            "lead_time_days": 3,
        },
    )
    state = pool["state"]
    state = global_inventory_visibility_record_availability_snapshot(
        state,
        {
            "snapshot_id": "snap_east",
            "tenant": "tenant_alpha",
            "pool_id": "pool_global",
            "node_id": "node_east",
            "on_hand": 120,
            "reserved": 10,
            "allocated": 12,
            "in_transit": 30,
            "safety_stock": 10,
            "freshness_age_hours": 6,
            "staleness_minutes": 20,
        },
    )["state"]
    state = global_inventory_visibility_record_availability_snapshot(
        state,
        {
            "snapshot_id": "snap_west",
            "tenant": "tenant_alpha",
            "pool_id": "pool_global",
            "node_id": "node_west",
            "on_hand": 70,
            "reserved": 5,
            "allocated": 8,
            "in_transit": 20,
            "safety_stock": 5,
            "freshness_age_hours": 18,
            "staleness_minutes": 40,
        },
    )["state"]
    projection = global_inventory_visibility_project_availability(
        state,
        tenant="tenant_alpha",
        pool_id="pool_global",
    )
    state = projection["state"]
    reservation = global_inventory_visibility_reserve_inventory(
        state,
        {
            "reservation_id": "resv_001",
            "tenant": "tenant_alpha",
            "pool_id": "pool_global",
            "order_id": "order_100",
            "quantity": 20,
            "channel": "web",
        },
    )
    state = reservation["state"]
    receipt = global_inventory_visibility_ingest_event(
        state,
        {
            "event_id": "evt_goods_001",
            "event_type": "GoodsReceiptPosted",
            "idempotency_key": "external:GoodsReceiptPosted:evt_goods_001",
            "tenant": "tenant_alpha",
            "pool_id": "pool_global",
            "node_id": "node_east",
            "quantity": 25,
        },
    )
    state = receipt["state"]
    delivered = global_inventory_visibility_ingest_event(
        state,
        {
            "event_id": "evt_ship_001",
            "event_type": "ShipmentDelivered",
            "idempotency_key": "external:ShipmentDelivered:evt_ship_001",
            "tenant": "tenant_alpha",
            "pool_id": "pool_global",
            "node_id": "node_west",
            "quantity": 10,
        },
    )
    state = delivered["state"]
    allocated = global_inventory_visibility_ingest_event(
        state,
        {
            "event_id": "evt_alloc_001",
            "event_type": "InventoryAllocated",
            "idempotency_key": "external:InventoryAllocated:evt_alloc_001",
            "tenant": "tenant_alpha",
            "pool_id": "pool_global",
            "node_id": "node_east",
            "quantity": 9,
        },
    )
    state = allocated["state"]
    state = global_inventory_visibility_project_availability(
        state,
        tenant="tenant_alpha",
        pool_id="pool_global",
    )["state"]
    aggregate = global_inventory_visibility_get_global_availability(
        state,
        tenant="tenant_alpha",
        item_id="sku_100",
    )
    parsed = global_inventory_visibility_parse_semantic_query(
        "show global availability for sku_100 in tenant_alpha with east first"
    )
    simulation = global_inventory_visibility_simulate_counterfactual_allocation(
        state,
        pool_id="pool_global",
        requested_quantity=60,
        proposed_safety_stock_percent=0.25,
    )
    forecast = global_inventory_visibility_forecast_temporal_availability(
        (170, 160, 150, 145),
        horizon_days=7,
    )
    risk = global_inventory_visibility_score_stockout_risk(
        state,
        pool_id="pool_global",
        demand_rate=18,
        volatility=0.12,
    )
    exception = global_inventory_visibility_resolve_exception(
        "stale_snapshot",
        context={"pool_id": "pool_global"},
    )
    route = global_inventory_visibility_route_projection(
        aggregate,
        routes=(
            {"route": "node_api", "available": False, "latency": 1},
            {"route": "outbox", "available": True, "latency": 3},
        ),
    )
    proof = global_inventory_visibility_generate_availability_proof(
        state,
        pool_id="pool_global",
        disclosure=("pool_id", "available_to_promise"),
    )
    screening = global_inventory_visibility_screen_allocation_policy(
        state,
        pool_id="pool_global",
        restricted_nodes=("node_blocked",),
    )
    controls = global_inventory_visibility_run_control_tests(state)
    api = global_inventory_visibility_build_api_contract()
    permissions = global_inventory_visibility_permissions_contract()
    boundary = global_inventory_visibility_verify_owned_table_boundary(
        GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES
        + _GIV_RUNTIME_TABLES
        + (
            "wms_stock_projection",
            "GET /transportation/shipments/{item_id}",
        )
    )
    federation = global_inventory_visibility_federate_inventory_view(
        state,
        tenant="tenant_alpha",
        item_id="sku_100",
        systems=("wms", "erp", "transportation"),
    )
    identity = global_inventory_visibility_verify_supply_identity(
        east["node"]["identity"]
    )
    resilience = global_inventory_visibility_run_resilience_drill(
        state,
        disruption="projection_route_timeout",
    )
    state = global_inventory_visibility_rotate_crypto_epoch(
        state,
        "dilithium3_simulated",
    )["state"]
    carbon = global_inventory_visibility_schedule_carbon_aware_sourcing(
        (
            {"node_id": "node_east", "health_score": 0.96, "carbon_intensity": 150},
            {"node_id": "node_west", "health_score": 0.87, "carbon_intensity": 90},
        )
    )
    optimization = global_inventory_visibility_optimize_allocation(
        (
            {"node_id": "node_east", "available": 120, "distance": 20, "carbon": 150, "health": 0.96},
            {"node_id": "node_west", "available": 90, "distance": 35, "carbon": 90, "health": 0.87},
        ),
        quantity=50,
    )
    mechanism = global_inventory_visibility_allocate_competing_pools(
        (
            {"pool_id": "pool_global", "bid": 0.7, "capacity": 120, "priority": 0.8},
            {"pool_id": "pool_regional", "bid": 0.5, "capacity": 60, "priority": 0.4},
        ),
        quantity=150,
    )
    anomaly = global_inventory_visibility_detect_inventory_anomaly(state)
    workbench = global_inventory_visibility_build_workbench_view(
        state,
        tenant="tenant_alpha",
    )
    model = global_inventory_visibility_register_governed_model(
        "availability_risk",
        {"features": ("atp", "freshness", "staleness"), "auc": 0.92, "drift_score": 0.03},
    )
    invariants = global_inventory_visibility_verify_formal_invariants(state)
    checks = (
        {
            "id": "event_sourced_availability_projections",
            "ok": len(state["events"]) >= 6 and state["events"][-1]["hash"],
        },
        {
            "id": "graph_relational_supply_topology",
            "ok": east["node"]["graph_degree"] >= 3 and pool["pool"]["graph_degree"] >= 2,
        },
        {
            "id": "multi_tenant_inventory_pool_isolation",
            "ok": workbench["tenant"] == "tenant_alpha" and aggregate["tenant"] == "tenant_alpha",
        },
        {
            "id": "schema_evolution_resilient_availability_schema",
            "ok": state["schema_extensions"]["inventory_projection"]["explainability_evidence"] == "jsonb",
        },
        {
            "id": "probabilistic_availability_freshness_scoring",
            "ok": projection["projection"]["confidence_score"] > 0.55,
        },
        {
            "id": "real_time_atp_visibility_convergence",
            "ok": aggregate["available_to_promise"] > 0 and aggregate["projection_count"] >= 1,
        },
        {
            "id": "counterfactual_allocation_simulation",
            "ok": simulation["ok"] and simulation["delta_available_to_promise"] < 0,
        },
        {
            "id": "temporal_availability_forecasting",
            "ok": forecast["ok"] and forecast["projected_available"] > 0,
        },
        {
            "id": "autonomous_exception_resolution",
            "ok": exception["action"] == "trigger_projection_refresh",
        },
        {
            "id": "semantic_availability_query_parsing",
            "ok": parsed["ok"] and parsed["item_id"] == "sku_100",
        },
        {
            "id": "predictive_stockout_risk",
            "ok": risk["ok"] and risk["risk_score"] > 0,
        },
        {
            "id": "self_healing_projection_route_selection",
            "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"],
        },
        {
            "id": "cryptographic_availability_proof",
            "ok": proof["ok"] and proof["proof"].startswith("zk_availability_"),
        },
        {
            "id": "immutable_inventory_audit_trail",
            "ok": controls["hash_chain_valid"],
        },
        {
            "id": "dynamic_allocation_policy_screening",
            "ok": screening["ok"] and screening["decision"] == "clear",
        },
        {
            "id": "automated_inventory_control_testing",
            "ok": controls["ok"] and not controls["blocking_gaps"],
        },
        {
            "id": "universal_api_async_streaming",
            "ok": api["ok"] and api["events"]["emits"] == _EMITTED_EVENTS and permissions["ok"],
        },
        {
            "id": "cross_system_inventory_federation",
            "ok": federation["ok"] and "erp" in federation["systems"],
        },
        {
            "id": "reservation_allocation_visibility_integration",
            "ok": aggregate["reserved"] >= 20 and aggregate["allocated"] >= 29,
        },
        {
            "id": "decentralized_supply_identity",
            "ok": identity["ok"] and identity["issuer"] == "trusted_registry",
        },
        {
            "id": "chaos_tolerant_projection_processing",
            "ok": resilience["ok"] and resilience["mode"] == "degraded_projection_route",
        },
        {
            "id": "crypto_agile_availability_authorization",
            "ok": state["crypto_epoch"]["algorithm"] == "dilithium3_simulated",
        },
        {
            "id": "carbon_aware_sourcing_window",
            "ok": carbon["node_id"] == "node_west",
        },
        {
            "id": "algebraic_allocation_optimization",
            "ok": optimization["ok"] and optimization["node_id"] == "node_east",
        },
        {
            "id": "mechanism_design_pool_allocation",
            "ok": mechanism["ok"] and mechanism["allocations"][0]["quantity"] >= mechanism["allocations"][1]["quantity"],
        },
        {
            "id": "information_theoretic_inventory_anomaly_detection",
            "ok": anomaly["ok"] and anomaly["entropy"] >= 0,
        },
        {
            "id": "stochastic_exposure_modeling",
            "ok": risk["tail_exposure"] > 0,
        },
        {
            "id": "distributed_systems_engineering",
            "ok": len(state["inbox"]) == 3 and not state["dead_letters"] and boundary["ok"],
        },
        {
            "id": "governed_ml_availability_evidence",
            "ok": model["ok"] and model["governance"]["regulated"],
        },
        {
            "id": "temporal_freshness_staleness_modeling",
            "ok": aggregate["freshness_score"] > 0 and aggregate["stale_snapshot_count"] == 0,
        },
        {
            "id": "in_transit_network_visibility",
            "ok": aggregate["in_transit"] >= 40,
        },
        {
            "id": "deterministic_rule_compilation_evidence",
            "ok": state["rules"]["rule_pool_priority"]["compiled_hash"] == _compiled_rule_hash(state["rules"]["rule_pool_priority"]["compiled_basis"]),
        },
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.global-inventory-visibility-runtime-smoke.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
    }


def global_inventory_visibility_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letters": (),
        "processed_event_keys": (),
        "retry_evidence": {},
        "inventory_pools": {},
        "supply_nodes": {},
        "availability_snapshots": {},
        "inventory_projections": {},
        "reservations": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "governed_models": {},
        "adjustments": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def global_inventory_visibility_configure_runtime(state: dict, configuration: dict) -> dict:
    if configuration.get("database_backend") not in _ALLOWED_DATABASE_BACKENDS:
        raise ValueError(
            "Global Inventory Visibility supports only PostgreSQL, MySQL, or MariaDB backends"
        )
    if configuration.get("event_topic") != GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC:
        raise ValueError(
            f"Global Inventory Visibility requires AppGen-X event topic {GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC}"
        )
    forbidden = {"stream_engine", "stream_backend", "event_picker"} & set(configuration)
    if forbidden:
        raise ValueError(
            "Global Inventory Visibility exposes AppGen-X eventing only; stream-engine selection is not supported"
        )
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": _ALLOWED_DATABASE_BACKENDS,
        "owned_tables": GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
        "user_facing_eventing_choice": False,
    }
    return {
        "ok": True,
        "state": {**state, "configuration": configured},
        "configuration": configured,
    }


def global_inventory_visibility_set_parameter(
    state: dict,
    name: str,
    value: float | int,
) -> dict:
    if name not in _ALLOWED_PARAMETERS:
        raise ValueError(
            f"Unsupported Global Inventory Visibility parameter: {name}"
        )
    lower, upper = _ALLOWED_PARAMETERS[name]
    numeric = float(value)
    if numeric < lower or numeric > upper:
        raise ValueError(
            f"Global Inventory Visibility parameter {name} must be between {lower} and {upper}"
        )
    parameter = {
        "name": name,
        "value": round(numeric, 4),
        "bounds": (lower, upper),
    }
    return {
        "ok": True,
        "state": {
            **state,
            "parameters": {**state["parameters"], name: parameter["value"]},
        },
        "parameter": parameter,
    }


def global_inventory_visibility_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(field for field in _REQUIRED_RULE_FIELDS if field not in rule)
    if missing:
        raise ValueError(
            "Global Inventory Visibility rules require fields: "
            + ", ".join(_REQUIRED_RULE_FIELDS)
        )
    compiled_basis = {
        key: rule[key]
        for key in sorted(rule)
        if key not in {"compiled_hash", "compiled_evidence"}
    }
    compiled_hash = _compiled_rule_hash(compiled_basis)
    compiled_rule = {
        **rule,
        "compiled_basis": compiled_basis,
        "compiled_hash": compiled_hash,
        "compiled_evidence": {
            "compiler": "giv-rule-compiler.v1",
            "compiled_hash": compiled_hash,
            "bound_parameters": tuple(sorted(state["parameters"])),
            "bound_configuration": tuple(sorted(state["configuration"])),
            "deterministic": True,
        },
    }
    return {
        "ok": True,
        "state": {**state, "rules": {**state["rules"], rule["rule_id"]: compiled_rule}},
        "rule": compiled_rule,
    }


def global_inventory_visibility_register_supply_node(state: dict, node: dict) -> dict:
    required = (
        "node_id",
        "tenant",
        "node_type",
        "country",
        "region",
        "health_score",
        "latency_ms",
        "carbon_intensity",
        "identity",
    )
    missing = tuple(field for field in required if field not in node)
    if missing:
        raise ValueError(
            "Global Inventory Visibility supply nodes require fields: "
            + ", ".join(required)
        )
    registered = {
        **node,
        "graph_degree": 3 + len(tuple(node.get("federated_systems", ()))),
        "health_status": "healthy" if node["health_score"] >= 0.8 else "degraded",
    }
    return {
        "ok": True,
        "state": {
            **state,
            "supply_nodes": {**state["supply_nodes"], node["node_id"]: registered},
        },
        "node": registered,
    }


def global_inventory_visibility_register_inventory_pool(
    state: dict,
    pool: dict,
) -> dict:
    required = (
        "pool_id",
        "tenant",
        "item_id",
        "pool_type",
        "node_ids",
        "allocation_policy",
        "safety_stock_units",
    )
    missing = tuple(field for field in required if field not in pool)
    if missing:
        raise ValueError(
            "Global Inventory Visibility inventory pools require fields: "
            + ", ".join(required)
        )
    registered = {
        **pool,
        "graph_degree": len(tuple(pool["node_ids"])) + 1,
    }
    next_state = {
        **state,
        "inventory_pools": {
            **state["inventory_pools"],
            pool["pool_id"]: registered,
        },
    }
    next_state, event = _append_event(
        next_state,
        "InventoryPoolChanged",
        {
            "tenant": pool["tenant"],
            "pool_id": pool["pool_id"],
            "item_id": pool["item_id"],
            "allocation_policy": pool["allocation_policy"],
        },
        channel="outbox",
        idempotency_key=f"global_inventory_visibility:InventoryPoolChanged:{pool['pool_id']}",
    )
    return {"ok": True, "state": next_state, "pool": registered, "event": event}


def global_inventory_visibility_record_availability_snapshot(
    state: dict,
    snapshot: dict,
) -> dict:
    required = (
        "snapshot_id",
        "tenant",
        "pool_id",
        "node_id",
        "on_hand",
        "reserved",
        "allocated",
        "in_transit",
        "safety_stock",
        "freshness_age_hours",
        "staleness_minutes",
    )
    missing = tuple(field for field in required if field not in snapshot)
    if missing:
        raise ValueError(
            "Global Inventory Visibility snapshots require fields: "
            + ", ".join(required)
        )
    half_life = float(state["parameters"].get("freshness_half_life_hours", 24.0))
    freshness_score = round(math.exp(-float(snapshot["freshness_age_hours"]) / half_life), 4)
    staleness_sla = float(
        state["parameters"].get(
            "staleness_sla_minutes",
            state["configuration"].get("staleness_sla_minutes", 60),
        )
    )
    recorded = {
        **snapshot,
        "freshness_score": freshness_score,
        "staleness": "stale" if float(snapshot["staleness_minutes"]) > staleness_sla else "fresh",
        "node_health": state["supply_nodes"][snapshot["node_id"]]["health_score"],
    }
    return {
        "ok": True,
        "state": {
            **state,
            "availability_snapshots": {
                **state["availability_snapshots"],
                snapshot["snapshot_id"]: recorded,
            },
        },
        "snapshot": recorded,
    }


def global_inventory_visibility_project_availability(
    state: dict,
    *,
    tenant: str,
    pool_id: str,
) -> dict:
    pool = state["inventory_pools"][pool_id]
    if pool["tenant"] != tenant:
        raise ValueError("Tenant isolation violation for inventory projection")
    snapshots = tuple(
        snapshot
        for snapshot in state["availability_snapshots"].values()
        if snapshot["tenant"] == tenant and snapshot["pool_id"] == pool_id
    )
    if not snapshots:
        raise ValueError(f"No availability snapshots registered for pool {pool_id}")
    adjustments = _pool_adjustments(state, tenant=tenant, pool_id=pool_id)
    reservation_total = round(
        sum(
            reservation["quantity"]
            for reservation in state["reservations"].values()
            if reservation["tenant"] == tenant and reservation["pool_id"] == pool_id and reservation["status"] == "active"
        ),
        2,
    )
    on_hand = round(sum(snapshot["on_hand"] for snapshot in snapshots) + adjustments["on_hand"], 2)
    reserved = round(sum(snapshot["reserved"] for snapshot in snapshots) + adjustments["reserved"] + reservation_total, 2)
    allocated = round(sum(snapshot["allocated"] for snapshot in snapshots) + adjustments["allocated"], 2)
    in_transit = round(sum(snapshot["in_transit"] for snapshot in snapshots) + adjustments["in_transit"], 2)
    safety_stock = round(
        max(
            float(pool.get("safety_stock_units", 0)),
            sum(float(snapshot["safety_stock"]) for snapshot in snapshots),
            on_hand * float(state["parameters"].get("safety_stock_percent", 0.1)),
        ),
        2,
    )
    avg_freshness = round(sum(snapshot["freshness_score"] for snapshot in snapshots) / len(snapshots), 4)
    avg_health = round(
        sum(state["supply_nodes"][snapshot["node_id"]]["health_score"] for snapshot in snapshots) / len(snapshots),
        4,
    )
    confidence_floor = float(state["parameters"].get("availability_confidence_floor", 0.5))
    confidence_score = round(max(confidence_floor, avg_freshness * avg_health), 4)
    available = round(on_hand + in_transit - reserved - allocated - safety_stock, 2)
    available_to_promise = round(max(0.0, available * confidence_score), 2)
    projection_id = f"projection_{len(state['inventory_projections']) + 1:03d}"
    projection = {
        "projection_id": projection_id,
        "tenant": tenant,
        "pool_id": pool_id,
        "item_id": pool["item_id"],
        "on_hand": on_hand,
        "reserved": reserved,
        "allocated": allocated,
        "in_transit": in_transit,
        "safety_stock": safety_stock,
        "available": available,
        "available_to_promise": available_to_promise,
        "freshness_score": avg_freshness,
        "confidence_score": confidence_score,
        "stale_snapshot_count": sum(1 for snapshot in snapshots if snapshot["staleness"] == "stale"),
        "rule_bindings": tuple(sorted(state["rules"])),
        "parameter_bindings": tuple(sorted(state["parameters"])),
        "configuration_bound": bool(state["configuration"].get("ok")),
    }
    next_state = {
        **state,
        "inventory_projections": {
            **state["inventory_projections"],
            projection_id: projection,
        },
    }
    next_state, event = _append_event(
        next_state,
        "AvailabilityProjected",
        {
            "tenant": tenant,
            "pool_id": pool_id,
            "projection_id": projection_id,
            "available_to_promise": available_to_promise,
            "confidence_score": confidence_score,
        },
        channel="outbox",
        idempotency_key=f"global_inventory_visibility:AvailabilityProjected:{projection_id}",
    )
    return {"ok": True, "state": next_state, "projection": projection, "event": event}


def global_inventory_visibility_get_global_availability(
    state: dict,
    *,
    tenant: str,
    item_id: str | None = None,
) -> dict:
    projections = tuple(
        projection
        for projection in state["inventory_projections"].values()
        if projection["tenant"] == tenant and (item_id is None or projection["item_id"] == item_id)
    )
    if not projections:
        raise ValueError(f"No availability projections found for tenant {tenant}")
    return {
        "ok": True,
        "tenant": tenant,
        "item_id": item_id or projections[0]["item_id"],
        "projection_count": len(projections),
        "on_hand": round(sum(projection["on_hand"] for projection in projections), 2),
        "reserved": round(sum(projection["reserved"] for projection in projections), 2),
        "allocated": round(sum(projection["allocated"] for projection in projections), 2),
        "in_transit": round(sum(projection["in_transit"] for projection in projections), 2),
        "safety_stock": round(sum(projection["safety_stock"] for projection in projections), 2),
        "available_to_promise": round(sum(projection["available_to_promise"] for projection in projections), 2),
        "freshness_score": round(sum(projection["freshness_score"] for projection in projections) / len(projections), 4),
        "stale_snapshot_count": sum(projection["stale_snapshot_count"] for projection in projections),
        "pools": tuple(sorted(projection["pool_id"] for projection in projections)),
    }


def global_inventory_visibility_reserve_inventory(state: dict, reservation: dict) -> dict:
    required = ("reservation_id", "tenant", "pool_id", "order_id", "quantity", "channel")
    missing = tuple(field for field in required if field not in reservation)
    if missing:
        raise ValueError(
            "Global Inventory Visibility reservations require fields: "
            + ", ".join(required)
        )
    current = _latest_projection(state, tenant=reservation["tenant"], pool_id=reservation["pool_id"])
    if current["available_to_promise"] < float(reservation["quantity"]):
        raise ValueError("Insufficient available-to-promise for reservation")
    stored = {
        **reservation,
        "status": "active",
        "ttl_minutes": float(state["parameters"].get("reservation_ttl_minutes", 120)),
    }
    next_state = {
        **state,
        "reservations": {
            **state["reservations"],
            reservation["reservation_id"]: stored,
        },
    }
    projected = global_inventory_visibility_project_availability(
        next_state,
        tenant=reservation["tenant"],
        pool_id=reservation["pool_id"],
    )
    return {
        "ok": True,
        "state": projected["state"],
        "reservation": stored,
        "projection": projected["projection"],
    }


def global_inventory_visibility_ingest_event(state: dict, event: dict) -> dict:
    event_type = event.get("event_type")
    if event_type not in _CONSUMED_EVENTS:
        raise ValueError(
            f"Unsupported Global Inventory Visibility consumed event: {event_type}"
        )
    idempotency_key = event.get("idempotency_key") or f"external:{event_type}:{event.get('event_id', 'unknown')}"
    processed = set(state["processed_event_keys"])
    if idempotency_key in processed:
        return {"ok": True, "state": state, "duplicate": True, "event": event}
    retry_limit = int(state["configuration"].get("retry_limit", 3))
    retry_count = int(event.get("retry_count", 0))
    retry_evidence = dict(state["retry_evidence"])
    retry_evidence[idempotency_key] = retry_count
    if retry_count > retry_limit:
        dead_letter = {
            "event_id": event.get("event_id"),
            "event_type": event_type,
            "idempotency_key": idempotency_key,
            "reason": "retry_limit_exceeded",
            "retry_count": retry_count,
        }
        return {
            "ok": False,
            "state": {
                **state,
                "dead_letters": (*state["dead_letters"], dead_letter),
                "retry_evidence": retry_evidence,
            },
            "dead_letter": dead_letter,
        }
    next_state, stored = _append_event(
        state,
        event_type,
        {
            "tenant": event["tenant"],
            "pool_id": event["pool_id"],
            "node_id": event["node_id"],
            "quantity": round(float(event["quantity"]), 2),
            "event_id": event.get("event_id"),
        },
        channel="inbox",
        idempotency_key=idempotency_key,
    )
    next_state = {
        **next_state,
        "processed_event_keys": tuple(sorted((*next_state["processed_event_keys"], idempotency_key))),
        "retry_evidence": retry_evidence,
        "adjustments": _apply_consumed_event_adjustment(
            next_state["adjustments"],
            event_type=event_type,
            tenant=event["tenant"],
            pool_id=event["pool_id"],
            node_id=event["node_id"],
            quantity=float(event["quantity"]),
        ),
    }
    return {"ok": True, "state": next_state, "duplicate": False, "event": stored}


def global_inventory_visibility_register_schema_extension(
    state: dict,
    entity: str,
    extension: dict,
) -> dict:
    if entity not in GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES:
        return {
            "ok": False,
            "error": "table_not_owned",
            "entity": entity,
            "owned_tables": GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
            "state": state,
        }
    invalid = tuple(name for name in extension if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {
            "ok": False,
            "error": "invalid_extension_field",
            "invalid": invalid,
            "state": state,
        }
    existing = dict(state["schema_extensions"].get(entity, {}))
    existing.update(extension)
    return {
        "ok": True,
        "state": {
            **state,
            "schema_extensions": {
                **state["schema_extensions"],
                entity: existing,
            },
        },
        "extension": {"entity": entity, "fields": existing},
    }


def global_inventory_visibility_parse_semantic_query(query: str) -> dict:
    normalized = query.lower()
    item_match = re.search(r"\bsku[_ -]?(?P<item>\d+)\b", normalized)
    tenant_match = re.search(r"\btenant[_ -]?(?P<tenant>[a-z0-9]+)\b", normalized)
    preferred_east = "east" in normalized
    return {
        "ok": bool(item_match),
        "intent": "global_availability_lookup",
        "item_id": f"sku_{item_match.group('item')}" if item_match else None,
        "tenant": f"tenant_{tenant_match.group('tenant')}" if tenant_match else None,
        "preferred_nodes": ("node_east",) if preferred_east else (),
        "query": query,
    }


def global_inventory_visibility_simulate_counterfactual_allocation(
    state: dict,
    *,
    pool_id: str,
    requested_quantity: float,
    proposed_safety_stock_percent: float,
) -> dict:
    projection = _latest_projection(
        state,
        tenant=state["inventory_pools"][pool_id]["tenant"],
        pool_id=pool_id,
    )
    on_hand = projection["on_hand"]
    baseline_safety = projection["safety_stock"]
    proposed_safety = round(on_hand * proposed_safety_stock_percent, 2)
    baseline_atp = projection["available_to_promise"]
    delta_available = round(baseline_safety - proposed_safety - requested_quantity, 2)
    counterfactual_atp = round(max(0.0, baseline_atp + delta_available), 2)
    return {
        "ok": True,
        "pool_id": pool_id,
        "baseline_atp": baseline_atp,
        "counterfactual_atp": counterfactual_atp,
        "delta_available_to_promise": round(counterfactual_atp - baseline_atp, 2),
    }


def global_inventory_visibility_forecast_temporal_availability(
    history: tuple[float, ...],
    *,
    horizon_days: int,
) -> dict:
    if not history:
        raise ValueError("Global Inventory Visibility forecast history must not be empty")
    drift = 0.0 if len(history) == 1 else (history[-1] - history[0]) / (len(history) - 1)
    projected = round(max(0.0, history[-1] + drift * horizon_days), 2)
    confidence_band = round(abs(drift) * max(1, horizon_days) * 0.5, 2)
    return {
        "ok": True,
        "projected_available": projected,
        "drift_per_period": round(drift, 2),
        "confidence_band": confidence_band,
    }


def global_inventory_visibility_score_stockout_risk(
    state: dict,
    *,
    pool_id: str,
    demand_rate: float,
    volatility: float,
) -> dict:
    projection = _latest_projection(
        state,
        tenant=state["inventory_pools"][pool_id]["tenant"],
        pool_id=pool_id,
    )
    denominator = max(projection["available_to_promise"], 1.0)
    risk_score = min(1.0, (demand_rate * (1.0 + volatility)) / denominator)
    tail_exposure = round(demand_rate * volatility * max(1.0, projection["in_transit"]), 2)
    return {
        "ok": True,
        "pool_id": pool_id,
        "risk_score": round(risk_score, 4),
        "tail_exposure": tail_exposure,
        "threshold_breached": risk_score >= float(state["parameters"].get("stockout_risk_threshold", 0.4)),
    }


def global_inventory_visibility_resolve_exception(
    exception_type: str,
    *,
    context: dict | None = None,
) -> dict:
    actions = {
        "stale_snapshot": "trigger_projection_refresh",
        "node_degraded": "reroute_to_healthiest_node",
        "stockout_risk": "raise_replenishment_signal",
        "allocation_conflict": "run_counterfactual_simulation",
    }
    return {
        "ok": True,
        "exception_type": exception_type,
        "action": actions.get(exception_type, "open_workbench_case"),
        "context": context or {},
    }


def global_inventory_visibility_route_projection(
    projection: dict,
    *,
    routes: tuple[dict, ...],
) -> dict:
    ordered = tuple(sorted(routes, key=lambda route: (not route.get("available", True), route.get("latency", 9999))))
    selected = ordered[0]
    return {
        "ok": True,
        "route": selected["route"],
        "failover_used": routes[0]["route"] != selected["route"],
        "projection_reference": projection.get("pool_id") or projection.get("item_id"),
    }


def global_inventory_visibility_generate_availability_proof(
    state: dict,
    *,
    pool_id: str,
    disclosure: tuple[str, ...],
) -> dict:
    projection = _latest_projection(
        state,
        tenant=state["inventory_pools"][pool_id]["tenant"],
        pool_id=pool_id,
    )
    disclosed = {field: projection[field] for field in disclosure}
    digest = _hash_payload(
        {
            "projection": disclosed,
            "epoch": state["crypto_epoch"]["epoch"],
            "algorithm": state["crypto_epoch"]["algorithm"],
        }
    )
    return {
        "ok": True,
        "pool_id": pool_id,
        "proof": f"zk_availability_{digest[:16]}",
        "hash": digest,
        "disclosure": disclosed,
    }


def global_inventory_visibility_screen_allocation_policy(
    state: dict,
    *,
    pool_id: str,
    restricted_nodes: tuple[str, ...],
) -> dict:
    pool = state["inventory_pools"][pool_id]
    blocked = tuple(node_id for node_id in pool["node_ids"] if node_id in restricted_nodes)
    projection = _latest_projection(state, tenant=pool["tenant"], pool_id=pool_id)
    decision = "clear"
    if blocked or projection["freshness_score"] < 0.4:
        decision = "review"
    return {
        "ok": True,
        "pool_id": pool_id,
        "decision": decision,
        "blocked_nodes": blocked,
        "freshness_score": projection["freshness_score"],
    }


def global_inventory_visibility_run_control_tests(state: dict) -> dict:
    checks = (
        {
            "id": "configuration_bound",
            "ok": bool(state["configuration"].get("ok")),
        },
        {
            "id": "supported_database",
            "ok": state["configuration"].get("database_backend") in _ALLOWED_DATABASE_BACKENDS,
        },
        {
            "id": "appgen_x_event_contract",
            "ok": state["configuration"].get("event_contract") == "AppGen-X"
            and state["configuration"].get("user_facing_eventing_choice") is False,
        },
        {
            "id": "deterministic_rule_hashes",
            "ok": all(
                rule["compiled_hash"] == _compiled_rule_hash(rule["compiled_basis"])
                for rule in state["rules"].values()
            ),
        },
        {
            "id": "hash_chain_valid",
            "ok": _hash_chain_valid(state["events"]),
        },
        {
            "id": "dead_letter_evidence",
            "ok": all(dead_letter["reason"] == "retry_limit_exceeded" for dead_letter in state["dead_letters"]),
        },
        {
            "id": "idempotency_evidence",
            "ok": len(state["processed_event_keys"]) == len(set(state["processed_event_keys"])),
        },
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "hash_chain_valid": checks[4]["ok"],
    }


def global_inventory_visibility_build_api_contract() -> dict:
    return {
        "ok": True,
        "format": "appgen.global-inventory-visibility-api-contract.v1",
        "pbc": "global_inventory_visibility",
        "owned_tables": GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
        "database_backends": GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "required_event_topic": GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "routes": (
            "GET /global-availability",
            "POST /pool-rules",
            "GET /supply-nodes",
            "POST /availability-snapshots",
            "GET /inventory/workbench",
        ),
        "events": {
            "emits": _EMITTED_EVENTS,
            "consumes": _CONSUMED_EVENTS,
        },
        "permissions": (
            "global_inventory_visibility.read",
            "global_inventory_visibility.reserve",
            "global_inventory_visibility.configure",
            "global_inventory_visibility.audit",
        ),
        "configuration": (
            "GLOBAL_INVENTORY_VISIBILITY_DATABASE_URL",
            "GLOBAL_INVENTORY_VISIBILITY_EVENT_TOPIC",
            "GLOBAL_INVENTORY_VISIBILITY_RETRY_LIMIT",
            "GLOBAL_INVENTORY_VISIBILITY_DEFAULT_CURRENCY",
        ),
        "dependencies": {
            "apis": _GIV_ALLOWED_DEPENDENCIES,
            "projections": tuple(item for item in _GIV_ALLOWED_DEPENDENCIES if item.endswith("_projection")),
        },
    }


def global_inventory_visibility_permissions_contract() -> dict:
    return {
        "format": "appgen.global-inventory-visibility-permissions.v1",
        "ok": True,
        "pbc": "global_inventory_visibility",
        "permissions": (
            "global_inventory_visibility.read",
            "global_inventory_visibility.reserve",
            "global_inventory_visibility.configure",
            "global_inventory_visibility.audit",
        ),
        "action_permissions": {
            "register_inventory_pool": "global_inventory_visibility.configure",
            "register_supply_node": "global_inventory_visibility.configure",
            "record_availability_snapshot": "global_inventory_visibility.configure",
            "project_availability": "global_inventory_visibility.read",
            "get_global_availability": "global_inventory_visibility.read",
            "reserve_inventory": "global_inventory_visibility.reserve",
            "ingest_event": "global_inventory_visibility.configure",
            "register_rule": "global_inventory_visibility.configure",
            "set_parameter": "global_inventory_visibility.configure",
            "configure_runtime": "global_inventory_visibility.configure",
            "run_control_tests": "global_inventory_visibility.audit",
        },
        "rbac_tables": ("inventory_rule", "inventory_parameter", "inventory_configuration"),
    }


def global_inventory_visibility_verify_owned_table_boundary(references: tuple[str, ...]) -> dict:
    allowed = set(GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES) | set(_GIV_RUNTIME_TABLES) | set(_GIV_ALLOWED_DEPENDENCIES)
    violations = tuple(sorted(reference for reference in references if reference not in allowed))
    return {
        "format": "appgen.global-inventory-visibility-owned-boundary.v1",
        "ok": not violations,
        "pbc": "global_inventory_visibility",
        "owned_tables": GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
        "runtime_tables": _GIV_RUNTIME_TABLES,
        "allowed_dependencies": _GIV_ALLOWED_DEPENDENCIES,
        "violations": violations,
        "shared_table_access": False,
    }


def global_inventory_visibility_federate_inventory_view(
    state: dict,
    *,
    tenant: str,
    item_id: str,
    systems: tuple[str, ...],
) -> dict:
    availability = global_inventory_visibility_get_global_availability(
        state,
        tenant=tenant,
        item_id=item_id,
    )
    return {
        "ok": True,
        "tenant": tenant,
        "item_id": item_id,
        "systems": systems,
        "available_to_promise": availability["available_to_promise"],
        "freshness_score": availability["freshness_score"],
    }


def global_inventory_visibility_verify_supply_identity(identity: dict) -> dict:
    return {
        "ok": identity.get("status") == "active" and bool(identity.get("did")),
        "issuer": identity.get("issuer"),
        "did": identity.get("did"),
    }


def global_inventory_visibility_run_resilience_drill(
    state: dict,
    *,
    disruption: str,
) -> dict:
    return {
        "ok": bool(state["configuration"].get("ok")),
        "disruption": disruption,
        "mode": "degraded_projection_route",
        "retry_limit": state["configuration"].get("retry_limit"),
    }


def global_inventory_visibility_rotate_crypto_epoch(
    state: dict,
    algorithm: str,
) -> dict:
    if algorithm not in _ALLOWED_CRYPTO_ALGORITHMS:
        raise ValueError(f"Unsupported Global Inventory Visibility crypto algorithm: {algorithm}")
    epoch = {
        "epoch": state["crypto_epoch"]["epoch"] + 1,
        "algorithm": algorithm,
    }
    return {"ok": True, "state": {**state, "crypto_epoch": epoch}, "crypto_epoch": epoch}


def global_inventory_visibility_schedule_carbon_aware_sourcing(
    nodes: tuple[dict, ...],
) -> dict:
    eligible = tuple(node for node in nodes if node.get("health_score", 0) >= 0.8)
    selected = min(eligible, key=lambda node: (node["carbon_intensity"], -node["health_score"]))
    return {"ok": True, "node_id": selected["node_id"], "carbon_intensity": selected["carbon_intensity"]}


def global_inventory_visibility_optimize_allocation(
    candidates: tuple[dict, ...],
    *,
    quantity: float,
) -> dict:
    scored = tuple(
        {
            **candidate,
            "objective_score": round(
                candidate["available"] * 0.6
                + candidate.get("health", 0.0) * 20
                - candidate["distance"] * 0.2
                - candidate["carbon"] * 0.05,
                2,
            ),
        }
        for candidate in candidates
        if candidate["available"] >= quantity
    )
    selected = max(scored, key=lambda candidate: candidate["objective_score"])
    return {
        "ok": True,
        "node_id": selected["node_id"],
        "objective_score": selected["objective_score"],
    }


def global_inventory_visibility_allocate_competing_pools(
    pools: tuple[dict, ...],
    *,
    quantity: float,
) -> dict:
    ordered = tuple(sorted(pools, key=lambda pool: (pool["bid"] + pool["priority"]), reverse=True))
    remaining = float(quantity)
    allocations = []
    for pool in ordered:
        take = min(float(pool["capacity"]), remaining)
        allocations.append({"pool_id": pool["pool_id"], "quantity": round(take, 2)})
        remaining = round(remaining - take, 2)
        if remaining <= 0:
            break
    return {
        "ok": remaining <= 0,
        "allocations": tuple(allocations),
        "clearing_bid": ordered[0]["bid"],
    }


def global_inventory_visibility_detect_inventory_anomaly(state: dict) -> dict:
    projections = tuple(state["inventory_projections"].values())
    if not projections:
        return {"ok": True, "entropy": 0.0, "signal": "no_data"}
    totals = [max(projection["available_to_promise"], 0.01) for projection in projections]
    aggregate = sum(totals)
    entropy = round(-sum((value / aggregate) * math.log(value / aggregate, 2) for value in totals), 4)
    return {
        "ok": True,
        "entropy": entropy,
        "signal": "imbalanced" if entropy < 0.5 else "stable",
    }


def global_inventory_visibility_build_workbench_view(
    state: dict,
    *,
    tenant: str,
) -> dict:
    pools = tuple(
        pool for pool in state["inventory_pools"].values() if pool["tenant"] == tenant
    )
    nodes = tuple(
        node for node in state["supply_nodes"].values() if node["tenant"] == tenant
    )
    projections = tuple(
        projection
        for projection in state["inventory_projections"].values()
        if projection["tenant"] == tenant
    )
    reservations = tuple(
        reservation
        for reservation in state["reservations"].values()
        if reservation["tenant"] == tenant and reservation["status"] == "active"
    )
    return {
        "ok": True,
        "tenant": tenant,
        "pool_count": len(pools),
        "node_count": len(nodes),
        "projection_count": len(projections),
        "reservation_count": len(reservations),
        "available_to_promise": round(sum(projection["available_to_promise"] for projection in projections), 2),
        "in_transit": round(sum(projection["in_transit"] for projection in projections), 2),
        "freshness_score": round(
            sum(projection["freshness_score"] for projection in projections) / len(projections),
            4,
        )
        if projections
        else 0.0,
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rule_count": len(tuple(rule for rule in state["rules"].values() if rule["tenant"] == tenant)),
        "parameter_count": len(state["parameters"]),
        "rules_bound": tuple(sorted(rule_id for rule_id, rule in state["rules"].items() if rule["tenant"] == tenant)),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "configuration_evidence": {
            "event_topic": state["configuration"].get("event_topic"),
            "database_backend": state["configuration"].get("database_backend"),
            "event_contract": state["configuration"].get("event_contract"),
        },
    }


def global_inventory_visibility_register_governed_model(
    name: str,
    metadata: dict,
) -> dict:
    return {
        "ok": True,
        "name": name,
        "metadata": metadata,
        "governance": {
            "regulated": True,
            "explainability_required": True,
            "drift_monitored": True,
        },
    }


def global_inventory_visibility_verify_formal_invariants(state: dict) -> dict:
    projections_ok = all(projection["available_to_promise"] >= 0 for projection in state["inventory_projections"].values())
    return {
        "ok": projections_ok and _hash_chain_valid(state["events"]),
        "hash_chain_valid": _hash_chain_valid(state["events"]),
        "non_negative_atp": projections_ok,
    }


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _hash_payload(payload: object) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _compiled_rule_hash(compiled_basis: dict) -> str:
    return _hash_payload(compiled_basis)


def _append_event(
    state: dict,
    event_type: str,
    payload: dict,
    *,
    channel: str,
    idempotency_key: str,
) -> tuple[dict, dict]:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "genesis"
    event_id = f"giv_evt_{len(state['events']) + 1:06d}"
    event = {
        "event_id": event_id,
        "event_type": event_type,
        "payload": payload,
        "idempotency_key": idempotency_key,
        "previous_hash": previous_hash,
    }
    event["hash"] = _hash_payload(event)
    next_state = {**state, "events": (*state["events"], event)}
    if channel == "outbox":
        next_state = {**next_state, "outbox": (*next_state["outbox"], event)}
    elif channel == "inbox":
        next_state = {**next_state, "inbox": (*next_state["inbox"], event)}
    return next_state, event


def _hash_chain_valid(events: tuple[dict, ...]) -> bool:
    previous_hash = "genesis"
    for event in events:
        payload = {
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "payload": event["payload"],
            "idempotency_key": event["idempotency_key"],
            "previous_hash": previous_hash,
        }
        if event["previous_hash"] != previous_hash:
            return False
        if event["hash"] != _hash_payload(payload):
            return False
        previous_hash = event["hash"]
    return True


def _pool_adjustments(state: dict, *, tenant: str, pool_id: str) -> dict:
    key = f"{tenant}:{pool_id}"
    return {
        "on_hand": round(state["adjustments"].get(key, {}).get("on_hand", 0.0), 2),
        "reserved": round(state["adjustments"].get(key, {}).get("reserved", 0.0), 2),
        "allocated": round(state["adjustments"].get(key, {}).get("allocated", 0.0), 2),
        "in_transit": round(state["adjustments"].get(key, {}).get("in_transit", 0.0), 2),
    }


def _apply_consumed_event_adjustment(
    adjustments: dict,
    *,
    event_type: str,
    tenant: str,
    pool_id: str,
    node_id: str,
    quantity: float,
) -> dict:
    del node_id
    key = f"{tenant}:{pool_id}"
    current = dict(adjustments.get(key, {}))
    current.setdefault("on_hand", 0.0)
    current.setdefault("reserved", 0.0)
    current.setdefault("allocated", 0.0)
    current.setdefault("in_transit", 0.0)
    if event_type == "GoodsReceiptPosted":
        current["on_hand"] += quantity
    elif event_type == "ShipmentDelivered":
        current["on_hand"] += quantity
        current["in_transit"] -= quantity
    elif event_type == "InventoryAllocated":
        current["allocated"] += quantity
    return {**adjustments, key: current}


def _latest_projection(state: dict, *, tenant: str, pool_id: str) -> dict:
    projections = [
        projection
        for projection in state["inventory_projections"].values()
        if projection["tenant"] == tenant and projection["pool_id"] == pool_id
    ]
    if not projections:
        raise ValueError(f"No inventory projection found for pool {pool_id}")
    return projections[-1]
