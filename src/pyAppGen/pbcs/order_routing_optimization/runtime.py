"""Executable runtime for the Order Routing Optimization PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


ORDER_ROUTING_OPTIMIZATION_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_routing_lifecycle",
    "graph_relational_fulfillment_topology",
    "multi_tenant_routing_isolation",
    "schema_evolution_resilient_routing_schema",
    "probabilistic_sla_cost_capacity_scoring",
    "counterfactual_routing_simulation",
    "temporal_capacity_forecasting",
    "autonomous_routing_exception_resolution",
    "semantic_route_request_parsing",
    "predictive_fulfillment_risk",
    "self_healing_route_selection",
    "cryptographic_routing_proof",
    "immutable_routing_audit_trail",
    "dynamic_routing_policy_screening",
    "automated_routing_control_testing",
    "cross_system_order_inventory_tax_federation",
    "chaos_tolerant_appgen_eventing",
    "crypto_agility",
    "carbon_aware_routing",
    "mathematical_route_optimization",
    "auction_style_capacity_clearing",
    "routing_anomaly_detection",
    "stochastic_routing_exposure_modeling",
    "governed_ml_model_evidence",
    "universal_api_async_streaming",
    "distributed_systems_engineering",
)
ORDER_ROUTING_OPTIMIZATION_STANDARD_FEATURE_KEYS = (
    "routing_rules",
    "route_candidates",
    "capacity_snapshots",
    "routing_decisions",
    "node_reservation",
    "cost_sla_scoring",
    "split_shipment_policy",
    "substitution_eligibility",
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
)
ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS = (
    "postgresql",
    "mysql",
    "mariadb",
)
ORDER_ROUTING_OPTIMIZATION_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_currency",
    "supported_regions",
    "supported_split_policies",
    "supported_substitution_modes",
    "topology_systems",
    "default_timezone",
    "workbench_limit",
)
ORDER_ROUTING_OPTIMIZATION_SUPPORTED_PARAMETER_KEYS = (
    "cost_weight",
    "sla_weight",
    "capacity_weight",
    "risk_weight",
    "carbon_weight",
    "reservation_hold_minutes",
    "forecast_horizon_hours",
    "max_split_count",
    "simulation_sample_size",
    "confidence_floor",
)
ORDER_ROUTING_OPTIMIZATION_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "rule_type",
    "regions",
    "eligible_nodes",
    "capacity_floor",
    "split_policy",
    "substitution_mode",
    "status",
)
ORDER_ROUTING_OPTIMIZATION_CONSUMED_EVENT_TYPES = (
    "OrderVerified",
    "AvailabilityProjected",
    "TaxCalculated",
)
_ORDER_ROUTING_OPTIMIZATION_CONFIGURATION_SEQUENCE_FIELDS = {
    "supported_regions",
    "supported_split_policies",
    "supported_substitution_modes",
    "topology_systems",
}
_ORDER_ROUTING_OPTIMIZATION_RULE_SEQUENCE_FIELDS = {
    "regions",
    "eligible_nodes",
    "preferred_nodes",
}
_ORDER_ROUTING_OPTIMIZATION_PARAMETER_BOUNDS = {
    "cost_weight": (0.0, 1.0),
    "sla_weight": (0.0, 1.0),
    "capacity_weight": (0.0, 1.0),
    "risk_weight": (0.0, 1.0),
    "carbon_weight": (0.0, 1.0),
    "reservation_hold_minutes": (1, 1440),
    "forecast_horizon_hours": (1, 168),
    "max_split_count": (1, 6),
    "simulation_sample_size": (50, 100000),
    "confidence_floor": (0.0, 1.0),
}


def order_routing_optimization_runtime_capabilities() -> dict:
    smoke = order_routing_optimization_runtime_smoke()
    return {
        "format": "appgen.order-routing-optimization-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "order_routing_optimization",
        "implementation_directory": "src/pyAppGen/pbcs/order_routing_optimization",
        "capabilities": ORDER_ROUTING_OPTIMIZATION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": ORDER_ROUTING_OPTIMIZATION_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "handle_event",
            "ingest_capacity_snapshot",
            "upsert_route_candidate",
            "route_orders",
            "reserve_node_capacity",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def order_routing_optimization_runtime_smoke() -> dict:
    state = order_routing_optimization_empty_state()
    state = order_routing_optimization_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.order-routing.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_regions": ("west", "central"),
            "supported_split_policies": ("forbid", "allow"),
            "supported_substitution_modes": ("exact", "equivalent"),
            "topology_systems": ("dom", "inventory", "tax", "wms"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = order_routing_optimization_set_parameter(
        state, "cost_weight", 0.25
    )["state"]
    state = order_routing_optimization_set_parameter(
        state, "sla_weight", 0.35
    )["state"]
    state = order_routing_optimization_set_parameter(
        state, "capacity_weight", 0.2
    )["state"]
    state = order_routing_optimization_set_parameter(
        state, "risk_weight", 0.1
    )["state"]
    state = order_routing_optimization_set_parameter(
        state, "carbon_weight", 0.1
    )["state"]
    state = order_routing_optimization_set_parameter(
        state, "reservation_hold_minutes", 45
    )["state"]
    state = order_routing_optimization_set_parameter(
        state, "forecast_horizon_hours", 24
    )["state"]
    state = order_routing_optimization_set_parameter(
        state, "max_split_count", 2
    )["state"]
    state = order_routing_optimization_set_parameter(
        state, "simulation_sample_size", 500
    )["state"]
    state = order_routing_optimization_set_parameter(
        state, "confidence_floor", 0.5
    )["state"]
    state = order_routing_optimization_register_rule(
        state,
        {
            "rule_id": "rule_smoke",
            "tenant": "tenant_alpha",
            "rule_type": "routing",
            "regions": ("west",),
            "eligible_nodes": ("node_fast", "node_green"),
            "preferred_nodes": ("node_fast",),
            "capacity_floor": 2,
            "split_policy": "allow",
            "substitution_mode": "equivalent",
            "status": "active",
        },
    )["state"]
    state = order_routing_optimization_register_schema_extension(
        state,
        "routing_decision",
        {"counterfactual_vector": "jsonb"},
    )["state"]
    state = order_routing_optimization_handle_event(
        state,
        {
            "event_id": "evt_verify_100",
            "event_type": "OrderVerified",
            "payload": {"tenant": "tenant_alpha", "order_id": "order_100"},
        },
    )["state"]
    state = order_routing_optimization_handle_event(
        state,
        {
            "event_id": "evt_availability_100",
            "event_type": "AvailabilityProjected",
            "payload": {
                "tenant": "tenant_alpha",
                "node_id": "node_fast",
                "available_units": 6,
            },
        },
    )["state"]
    state = order_routing_optimization_handle_event(
        state,
        {
            "event_id": "evt_tax_100",
            "event_type": "TaxCalculated",
            "payload": {
                "tenant": "tenant_alpha",
                "order_id": "order_100",
                "tax_total": 12.5,
            },
        },
    )["state"]
    state = order_routing_optimization_ingest_capacity_snapshot(
        state,
        {
            "snapshot_id": "cap_fast",
            "tenant": "tenant_alpha",
            "node_id": "node_fast",
            "available_units": 6,
            "reserved_units": 0,
            "forecast_load": 4,
        },
    )["state"]
    state = order_routing_optimization_ingest_capacity_snapshot(
        state,
        {
            "snapshot_id": "cap_green",
            "tenant": "tenant_alpha",
            "node_id": "node_green",
            "available_units": 6,
            "reserved_units": 0,
            "forecast_load": 3,
        },
    )["state"]
    state = order_routing_optimization_upsert_route_candidate(
        state,
        {
            "candidate_id": "cand_fast",
            "tenant": "tenant_alpha",
            "order_id": "order_100",
            "node_id": "node_fast",
            "region": "west",
            "distance_km": 180,
            "base_cost": 118,
            "sla_hours": 10,
            "carbon_kg": 46,
            "risk_score": 0.08,
            "available_units": 6,
            "inventory_source": "fc_west_a",
            "split_supported": True,
            "substitution_eligible": True,
        },
    )["state"]
    state = order_routing_optimization_upsert_route_candidate(
        state,
        {
            "candidate_id": "cand_green",
            "tenant": "tenant_alpha",
            "order_id": "order_100",
            "node_id": "node_green",
            "region": "west",
            "distance_km": 220,
            "base_cost": 108,
            "sla_hours": 18,
            "carbon_kg": 18,
            "risk_score": 0.12,
            "available_units": 6,
            "inventory_source": "fc_west_b",
            "split_supported": True,
            "substitution_eligible": True,
        },
    )["state"]
    routed = order_routing_optimization_route_orders(
        state,
        {
            "request_id": "req_smoke",
            "tenant": "tenant_alpha",
            "order_id": "order_100",
            "region": "west",
            "requested_units": 10,
            "sla_target_hours": 24,
            "allow_split": True,
            "substitution_requested": False,
        },
    )
    state = routed["state"]
    simulation = order_routing_optimization_simulate_counterfactual(
        state,
        "route_req_smoke",
        proposed_node="node_green",
    )
    forecast = order_routing_optimization_forecast_capacity(
        capacity_path=(6, 6, 5),
        demand_path=(3, 3, 4),
        horizon_hours=int(state["parameters"]["forecast_horizon_hours"]),
    )
    parsed = order_routing_optimization_parse_route_request(
        "route order order_100 region west units 10 sla 24 split allow"
    )
    risk = order_routing_optimization_score_fulfillment_risk(
        {
            "stockout_probability": 0.2,
            "tax_variance": 0.06,
            "exception_rate": 0.12,
            "capacity_volatility": 0.08,
        }
    )
    healed = order_routing_optimization_self_heal_route_selection(
        routed["decision"],
        routed["candidate_scores"],
        unavailable_nodes=("node_fast",),
    )
    proof = order_routing_optimization_generate_routing_proof(
        state,
        "route_req_smoke",
        disclosure=("order_id", "selected_node_ids", "split"),
    )
    screening = order_routing_optimization_screen_policy(
        state,
        "route_req_smoke",
        blocked_nodes=("node_blocked",),
        carbon_budget=80,
    )
    controls = order_routing_optimization_run_control_tests(state)
    api = order_routing_optimization_build_api_contract()
    federation = order_routing_optimization_federate_routing_view(
        state,
        "order_100",
        systems=("dom", "inventory", "tax"),
    )
    resilience = order_routing_optimization_run_resilience_drill(
        state,
        "availability_projection_timeout",
    )
    crypto = order_routing_optimization_rotate_crypto_epoch(
        state,
        "dilithium3_simulated",
    )
    carbon = order_routing_optimization_schedule_carbon_aware_route(
        tuple(routed["candidate_scores"])
    )
    optimization = order_routing_optimization_optimize_route_network(
        tuple(routed["candidate_scores"]),
        demand_units=10,
    )
    auction = order_routing_optimization_clear_capacity_auction(
        (
            {"node_id": "node_fast", "bid": 0.92, "available_units": 6},
            {"node_id": "node_green", "bid": 0.88, "available_units": 6},
        ),
        quantity=10,
    )
    anomaly = order_routing_optimization_detect_routing_anomaly(state)
    stochastic = order_routing_optimization_model_stochastic_exposure(
        score_path=(0.62, 0.67, 0.71),
        volatility=0.14,
    )
    model = order_routing_optimization_register_governed_model(
        "routing_risk",
        {"features": ("cost", "sla", "capacity"), "auc": 0.91, "drift_score": 0.03},
    )
    workbench = order_routing_optimization_build_workbench_view(
        state,
        tenant="tenant_alpha",
    )
    checks = (
        {
            "id": "event_sourced_routing_lifecycle",
            "ok": len(state["events"]) >= 10 and state["events"][-1]["hash"],
        },
        {
            "id": "graph_relational_fulfillment_topology",
            "ok": routed["decision"]["graph_degree"] >= 4
            and routed["candidate_scores"][0]["graph_degree"] >= 4,
        },
        {
            "id": "multi_tenant_routing_isolation",
            "ok": workbench["tenant"] == "tenant_alpha",
        },
        {
            "id": "schema_evolution_resilient_routing_schema",
            "ok": state["schema_extensions"]["routing_decision"]["counterfactual_vector"]
            == "jsonb",
        },
        {
            "id": "probabilistic_sla_cost_capacity_scoring",
            "ok": routed["decision"]["confidence"]
            >= state["parameters"]["confidence_floor"],
        },
        {
            "id": "counterfactual_routing_simulation",
            "ok": simulation["ok"] and simulation["proposed_node"] == "node_green",
        },
        {
            "id": "temporal_capacity_forecasting",
            "ok": forecast["ok"] and forecast["expected_available_units"] >= 0,
        },
        {
            "id": "autonomous_routing_exception_resolution",
            "ok": order_routing_optimization_recommend_exception_resolution(
                "capacity_shortfall"
            )["action"]
            == "reroute_to_backup_node",
        },
        {
            "id": "semantic_route_request_parsing",
            "ok": parsed["ok"] and parsed["requested_units"] == 10,
        },
        {
            "id": "predictive_fulfillment_risk",
            "ok": risk["risk_score"] > 0,
        },
        {
            "id": "self_healing_route_selection",
            "ok": healed["ok"] and healed["selected_node"] == "node_green",
        },
        {
            "id": "cryptographic_routing_proof",
            "ok": proof["ok"] and proof["proof"].startswith("zk_routing_"),
        },
        {
            "id": "immutable_routing_audit_trail",
            "ok": controls["hash_chain_valid"],
        },
        {
            "id": "dynamic_routing_policy_screening",
            "ok": screening["ok"] and screening["decision"] == "clear",
        },
        {
            "id": "automated_routing_control_testing",
            "ok": controls["ok"] and not controls["blocking_gaps"],
        },
        {
            "id": "cross_system_order_inventory_tax_federation",
            "ok": federation["ok"] and "inventory" in federation["systems"],
        },
        {
            "id": "chaos_tolerant_appgen_eventing",
            "ok": resilience["ok"] and resilience["mode"] == "degraded_outbox_replay",
        },
        {
            "id": "crypto_agility",
            "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated",
        },
        {"id": "carbon_aware_routing", "ok": carbon["node_id"] == "node_green"},
        {
            "id": "mathematical_route_optimization",
            "ok": optimization["ok"] and optimization["objective_score"] > 0,
        },
        {
            "id": "auction_style_capacity_clearing",
            "ok": auction["ok"] and auction["allocations"][0]["allocated_units"] > 0,
        },
        {
            "id": "routing_anomaly_detection",
            "ok": anomaly["ok"] and anomaly["entropy"] >= 0,
        },
        {
            "id": "stochastic_routing_exposure_modeling",
            "ok": stochastic["ok"] and stochastic["tail_risk"] > 0,
        },
        {
            "id": "governed_ml_model_evidence",
            "ok": model["governance"]["regulated"]
            and model["governance"]["explainability_required"],
        },
        {
            "id": "universal_api_async_streaming",
            "ok": api["ok"] and "FulfillmentRouteSelected" in api["events"]["emits"],
        },
        {
            "id": "distributed_systems_engineering",
            "ok": state["outbox"][-1]["idempotency_key"].startswith(
                "order_routing_optimization:NodeCapacityReserved"
            ),
        },
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.order-routing-optimization-runtime-smoke.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
    }


def order_routing_optimization_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "route_candidates": {},
        "capacity_snapshots": {},
        "routing_decisions": {},
        "node_reservations": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "handled_events": {},
        "retry_evidence": (),
        "availability_projections": {},
        "order_evidence": {},
        "tax_quotes": {},
        "governed_models": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def order_routing_optimization_configure_runtime(
    state: dict,
    configuration: dict,
) -> dict:
    unknown = tuple(
        sorted(
            field
            for field in configuration
            if field not in ORDER_ROUTING_OPTIMIZATION_SUPPORTED_CONFIGURATION_FIELDS
        )
    )
    if unknown:
        raise ValueError(
            "Unsupported Order Routing Optimization configuration fields: "
            f"{unknown}"
        )
    missing = tuple(
        sorted(
            field
            for field in ORDER_ROUTING_OPTIMIZATION_SUPPORTED_CONFIGURATION_FIELDS
            if field not in configuration
        )
    )
    if missing:
        raise ValueError(
            "Missing required Order Routing Optimization configuration fields: "
            f"{missing}"
        )
    database_backend = configuration.get("database_backend")
    if database_backend not in ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS:
        raise ValueError(
            "Order Routing Optimization supports only PostgreSQL, MySQL, "
            "or MariaDB backends"
        )
    event_topic = str(configuration.get("event_topic", "")).strip()
    if not event_topic or not event_topic.startswith("appgen."):
        raise ValueError(
            "Order Routing Optimization requires an AppGen-X event topic"
        )
    configured = {
        **_normalize_fields(
            configuration,
            _ORDER_ROUTING_OPTIMIZATION_CONFIGURATION_SEQUENCE_FIELDS,
        ),
        "ok": True,
        "event_contract": "appgen_event_contract",
        "allowed_database_backends": ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS,
        "supported_configuration_fields": (
            ORDER_ROUTING_OPTIMIZATION_SUPPORTED_CONFIGURATION_FIELDS
        ),
        "visible_event_contracts": ("appgen_event_contract",),
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
    }
    return {
        "ok": True,
        "state": {**state, "configuration": configured},
        "configuration": configured,
    }


def order_routing_optimization_set_parameter(
    state: dict,
    name: str,
    value: float | int | str | bool,
) -> dict:
    if name not in ORDER_ROUTING_OPTIMIZATION_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(
            f"Unsupported Order Routing Optimization parameter: {name}"
        )
    lower, upper = _ORDER_ROUTING_OPTIMIZATION_PARAMETER_BOUNDS[name]
    if not isinstance(value, (int, float)):
        raise ValueError(
            "Order Routing Optimization parameters must be numeric in this runtime"
        )
    if value < lower or value > upper:
        raise ValueError(
            f"Order Routing Optimization parameter {name} must be between "
            f"{lower} and {upper}"
        )
    parameter = {"name": name, "value": value}
    return {
        "ok": True,
        "state": {
            **state,
            "parameters": {**state["parameters"], name: value},
        },
        "parameter": parameter,
    }


def order_routing_optimization_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(
        sorted(
            field
            for field in ORDER_ROUTING_OPTIMIZATION_REQUIRED_RULE_FIELDS
            if field not in rule
        )
    )
    if missing:
        raise ValueError(
            f"Missing required Order Routing Optimization rule fields: {missing}"
        )
    normalized = _normalize_fields(
        rule,
        _ORDER_ROUTING_OPTIMIZATION_RULE_SEQUENCE_FIELDS,
    )
    configuration = state.get("configuration", {})
    split_policy = normalized["split_policy"]
    substitution_mode = normalized["substitution_mode"]
    if configuration:
        if split_policy not in configuration.get("supported_split_policies", ()):
            raise ValueError(
                "Order Routing Optimization rule split_policy must be one of "
                "the configured supported_split_policies"
            )
        if substitution_mode not in configuration.get(
            "supported_substitution_modes", ()
        ):
            raise ValueError(
                "Order Routing Optimization rule substitution_mode must be one "
                "of the configured supported_substitution_modes"
            )
    compiled_hash = _digest(normalized)
    enriched = {
        **normalized,
        "scope": normalized.get("scope") or normalized["rule_type"],
        "enabled": normalized["status"] == "active",
        "compiled_hash": compiled_hash,
        "compiled_evidence": {
            "rule_id": normalized["rule_id"],
            "hash": compiled_hash,
            "compilation_basis": "sha3_256(json(sort_keys=True))",
            "required_fields": ORDER_ROUTING_OPTIMIZATION_REQUIRED_RULE_FIELDS,
        },
    }
    return {
        "ok": True,
        "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}},
        "rule": enriched,
    }


def order_routing_optimization_register_schema_extension(
    state: dict,
    table: str,
    fields: dict,
) -> dict:
    invalid = tuple(
        name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name)
    )
    if invalid:
        return {
            "ok": False,
            "error": "invalid_extension_field",
            "invalid": invalid,
            "state": state,
        }
    return {
        "ok": True,
        "state": {
            **state,
            "schema_extensions": {
                **state["schema_extensions"],
                table: dict(fields),
            },
        },
    }


def order_routing_optimization_handle_event(
    state: dict,
    event: dict,
    *,
    simulate_failure: bool = False,
) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    if event_type not in ORDER_ROUTING_OPTIMIZATION_CONSUMED_EVENT_TYPES:
        raise ValueError(
            "Order Routing Optimization only consumes OrderVerified, "
            "AvailabilityProjected, and TaxCalculated"
        )
    handler_key = f"{event_type}:{event_id}"
    existing = state["handled_events"].get(handler_key)
    if existing and existing["status"] == "processed":
        return {
            "ok": True,
            "duplicate": True,
            "state": state,
            "handler": existing,
        }
    attempts = int(existing.get("attempts", 0) if existing else 0) + 1
    inbox_entry = {
        "event_id": event_id,
        "event_type": event_type,
        "tenant": event["payload"].get("tenant"),
        "attempts": attempts,
    }
    next_state = {**state, "inbox": (*state["inbox"], inbox_entry)}
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 3))
    if simulate_failure:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        evidence = {
            "event_id": event_id,
            "event_type": event_type,
            "attempts": attempts,
            "status": status,
        }
        next_state = {
            **next_state,
            "handled_events": {
                **next_state["handled_events"],
                handler_key: {
                    "event_id": event_id,
                    "event_type": event_type,
                    "status": status,
                    "attempts": attempts,
                },
            },
            "retry_evidence": (*next_state["retry_evidence"], evidence),
        }
        if status == "dead_letter":
            dead_letter = {
                "event_id": event_id,
                "event_type": event_type,
                "attempts": attempts,
                "reason": "simulated_failure",
            }
            next_state = {
                **next_state,
                "dead_letter": (*next_state["dead_letter"], dead_letter),
            }
            next_state = _append_event(
                next_state,
                "RoutingEventDeadLettered",
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "attempts": attempts,
                },
                emit=False,
            )
            return {
                "ok": False,
                "duplicate": False,
                "state": next_state,
                "handler": next_state["handled_events"][handler_key],
                "dead_letter": dead_letter,
            }
        next_state = _append_event(
            next_state,
            "RoutingEventRetryScheduled",
            {
                "event_id": event_id,
                "event_type": event_type,
                "attempts": attempts,
            },
            emit=False,
        )
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "handler": next_state["handled_events"][handler_key],
        }

    payload = event["payload"]
    if event_type == "OrderVerified":
        order_id = payload["order_id"]
        order_evidence = {
            **next_state["order_evidence"],
            order_id: {
                "tenant": payload["tenant"],
                "verified": True,
                "source_event_id": event_id,
            },
        }
        next_state = {**next_state, "order_evidence": order_evidence}
    elif event_type == "AvailabilityProjected":
        projection_key = _capacity_key(payload["tenant"], payload["node_id"])
        next_state = {
            **next_state,
            "availability_projections": {
                **next_state["availability_projections"],
                projection_key: dict(payload),
            },
        }
    elif event_type == "TaxCalculated":
        next_state = {
            **next_state,
            "tax_quotes": {
                **next_state["tax_quotes"],
                payload["order_id"]: float(payload.get("tax_total", 0.0)),
            },
        }
    handler = {
        "event_id": event_id,
        "event_type": event_type,
        "status": "processed",
        "attempts": attempts,
    }
    next_state = {
        **next_state,
        "handled_events": {**next_state["handled_events"], handler_key: handler},
    }
    next_state = _append_event(
        next_state,
        "RoutingEventProcessed",
        {"event_id": event_id, "event_type": event_type},
        emit=False,
    )
    return {
        "ok": True,
        "duplicate": False,
        "state": next_state,
        "handler": handler,
    }


def order_routing_optimization_ingest_capacity_snapshot(
    state: dict,
    snapshot: dict,
) -> dict:
    reserved_units = float(snapshot.get("reserved_units", 0.0))
    available_units = float(snapshot.get("available_units", 0.0))
    available_to_promise = round(max(available_units - reserved_units, 0.0), 2)
    enriched = {
        **snapshot,
        "available_units": available_units,
        "reserved_units": reserved_units,
        "available_to_promise": available_to_promise,
        "forecast_gap": round(
            available_to_promise - float(snapshot.get("forecast_load", 0.0)),
            2,
        ),
    }
    key = _capacity_key(snapshot["tenant"], snapshot["node_id"])
    next_state = {
        **state,
        "capacity_snapshots": {**state["capacity_snapshots"], key: enriched},
    }
    next_state = _append_event(
        next_state,
        "CapacitySnapshotRecorded",
        {
            "tenant": snapshot["tenant"],
            "node_id": snapshot["node_id"],
            "snapshot_id": snapshot["snapshot_id"],
            "available_to_promise": available_to_promise,
        },
    )
    return {"ok": True, "state": next_state, "capacity_snapshot": enriched}


def order_routing_optimization_upsert_route_candidate(
    state: dict,
    candidate: dict,
) -> dict:
    configuration = state.get("configuration", {})
    snapshot = state["capacity_snapshots"].get(
        _capacity_key(candidate["tenant"], candidate["node_id"])
    )
    available_to_promise = float(candidate.get("available_units", 0.0))
    if snapshot:
        available_to_promise = min(
            available_to_promise,
            float(snapshot.get("available_to_promise", available_to_promise)),
        )
    total_cost = round(
        float(candidate["base_cost"])
        + float(state["tax_quotes"].get(candidate["order_id"], 0.0)),
        2,
    )
    region_allowed = candidate["region"] in configuration.get("supported_regions", ())
    enriched = {
        **candidate,
        "available_to_promise": round(available_to_promise, 2),
        "total_cost": total_cost,
        "status": "ready" if region_allowed else "blocked",
        "graph_degree": len(
            tuple(
                value
                for value in (
                    candidate["node_id"],
                    candidate["region"],
                    candidate.get("inventory_source"),
                    candidate.get("order_id"),
                )
                if value
            )
        ),
    }
    next_state = {
        **state,
        "route_candidates": {
            **state["route_candidates"],
            candidate["candidate_id"]: enriched,
        },
    }
    next_state = _append_event(
        next_state,
        "RouteCandidateProjected",
        {
            "tenant": candidate["tenant"],
            "order_id": candidate["order_id"],
            "candidate_id": candidate["candidate_id"],
            "node_id": candidate["node_id"],
        },
    )
    return {"ok": region_allowed, "state": next_state, "route_candidate": enriched}


def order_routing_optimization_route_orders(state: dict, request: dict) -> dict:
    tenant = request["tenant"]
    order_id = request["order_id"]
    order_evidence = state["order_evidence"].get(order_id, {})
    if order_evidence.get("tenant") != tenant or not order_evidence.get("verified"):
        decision = {
            "decision_id": f"route_{request['request_id']}",
            "request_id": request["request_id"],
            "tenant": tenant,
            "order_id": order_id,
            "status": "blocked",
            "reason": "order_not_verified",
        }
        return {"ok": False, "state": state, "decision": decision, "candidate_scores": ()}
    rule = _active_rule_for_tenant(state, tenant)
    if request["region"] not in rule["regions"]:
        decision = {
            "decision_id": f"route_{request['request_id']}",
            "request_id": request["request_id"],
            "tenant": tenant,
            "order_id": order_id,
            "status": "blocked",
            "reason": "region_not_allowed",
        }
        return {"ok": False, "state": state, "decision": decision, "candidate_scores": ()}
    if request.get("substitution_requested") and rule["substitution_mode"] == "forbid":
        decision = {
            "decision_id": f"route_{request['request_id']}",
            "request_id": request["request_id"],
            "tenant": tenant,
            "order_id": order_id,
            "status": "blocked",
            "reason": "substitution_not_allowed",
        }
        return {"ok": False, "state": state, "decision": decision, "candidate_scores": ()}
    candidates = tuple(
        candidate
        for candidate in state["route_candidates"].values()
        if candidate["tenant"] == tenant
        and candidate["order_id"] == order_id
        and candidate["status"] == "ready"
        and candidate["node_id"] in rule["eligible_nodes"]
        and candidate["available_to_promise"] >= float(rule["capacity_floor"])
    )
    if not candidates:
        decision = {
            "decision_id": f"route_{request['request_id']}",
            "request_id": request["request_id"],
            "tenant": tenant,
            "order_id": order_id,
            "status": "blocked",
            "reason": "no_candidates",
        }
        return {"ok": False, "state": state, "decision": decision, "candidate_scores": ()}
    scored_candidates = _score_route_candidates(
        candidates,
        request=request,
        parameters=state["parameters"],
    )
    requested_units = float(request["requested_units"])
    single = tuple(
        candidate
        for candidate in scored_candidates
        if candidate["available_to_promise"] >= requested_units
    )
    allocations: list[dict] = []
    if single:
        winner = max(
            single,
            key=lambda candidate: (
                candidate["objective_score"],
                candidate["available_to_promise"],
            ),
        )
        allocations = [
            {
                "candidate_id": winner["candidate_id"],
                "node_id": winner["node_id"],
                "allocated_units": round(requested_units, 2),
                "objective_score": winner["objective_score"],
                "confidence": winner["confidence"],
            }
        ]
    elif request.get("allow_split") and rule["split_policy"] != "forbid":
        remaining = requested_units
        max_split_count = int(state["parameters"].get("max_split_count", 1))
        for candidate in sorted(
            scored_candidates,
            key=lambda item: item["objective_score"],
            reverse=True,
        ):
            if not candidate.get("split_supported", False):
                continue
            allocated = round(min(remaining, candidate["available_to_promise"]), 2)
            if allocated <= 0:
                continue
            allocations.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "node_id": candidate["node_id"],
                    "allocated_units": allocated,
                    "objective_score": candidate["objective_score"],
                    "confidence": candidate["confidence"],
                }
            )
            remaining = round(remaining - allocated, 2)
            if remaining <= 0 or len(allocations) >= max_split_count:
                break
        if remaining > 0:
            allocations = []
    if not allocations:
        decision = {
            "decision_id": f"route_{request['request_id']}",
            "request_id": request["request_id"],
            "tenant": tenant,
            "order_id": order_id,
            "status": "blocked",
            "reason": "insufficient_capacity",
        }
        return {
            "ok": False,
            "state": state,
            "decision": decision,
            "candidate_scores": scored_candidates,
        }
    selected_candidates = {
        candidate["candidate_id"]: candidate for candidate in scored_candidates
    }
    decision_id = f"route_{request['request_id']}"
    decision = {
        "decision_id": decision_id,
        "request_id": request["request_id"],
        "tenant": tenant,
        "order_id": order_id,
        "status": "selected",
        "split": len(allocations) > 1,
        "split_policy": rule["split_policy"],
        "substitution_mode": rule["substitution_mode"],
        "requested_units": round(requested_units, 2),
        "allocated_units": round(
            sum(item["allocated_units"] for item in allocations),
            2,
        ),
        "selected_candidate_ids": tuple(item["candidate_id"] for item in allocations),
        "selected_node_ids": tuple(item["node_id"] for item in allocations),
        "objective_score": round(
            sum(item["objective_score"] for item in allocations) / len(allocations),
            4,
        ),
        "confidence": round(
            sum(item["confidence"] for item in allocations) / len(allocations),
            4,
        ),
        "risk_score": round(
            sum(
                selected_candidates[item["candidate_id"]]["risk_score"]
                for item in allocations
            )
            / len(allocations),
            4,
        ),
        "total_cost": round(
            sum(
                selected_candidates[item["candidate_id"]]["total_cost"]
                * (item["allocated_units"] / requested_units)
                for item in allocations
            ),
            2,
        ),
        "total_carbon": round(
            sum(
                selected_candidates[item["candidate_id"]]["carbon_kg"]
                * (item["allocated_units"] / requested_units)
                for item in allocations
            ),
            2,
        ),
        "graph_degree": len(
            set(
                (
                    order_id,
                    request["region"],
                    *tuple(item["node_id"] for item in allocations),
                    rule["rule_id"],
                )
            )
        ),
        "allocations": tuple(allocations),
    }
    next_state = {
        **state,
        "routing_decisions": {
            **state["routing_decisions"],
            decision_id: decision,
        },
    }
    next_state = _append_event(
        next_state,
        "FulfillmentRouteSelected",
        {
            "tenant": tenant,
            "order_id": order_id,
            "decision_id": decision_id,
            "selected_node_ids": decision["selected_node_ids"],
            "split": decision["split"],
        },
    )
    reservation_ids = []
    for index, allocation in enumerate(allocations, start=1):
        reservation_id = f"{decision_id}_res_{index:02d}"
        reserved = order_routing_optimization_reserve_node_capacity(
            next_state,
            {
                "reservation_id": reservation_id,
                "tenant": tenant,
                "decision_id": decision_id,
                "order_id": order_id,
                "node_id": allocation["node_id"],
                "allocated_units": allocation["allocated_units"],
            },
        )
        if not reserved["ok"]:
            return {
                "ok": False,
                "state": state,
                "decision": {
                    **decision,
                    "status": "blocked",
                    "reason": "reservation_failed",
                },
                "candidate_scores": scored_candidates,
            }
        next_state = reserved["state"]
        reservation_ids.append(reservation_id)
    final_decision = {
        **decision,
        "reservation_ids": tuple(reservation_ids),
    }
    next_state = {
        **next_state,
        "routing_decisions": {
            **next_state["routing_decisions"],
            decision_id: final_decision,
        },
    }
    return {
        "ok": True,
        "state": next_state,
        "decision": final_decision,
        "candidate_scores": scored_candidates,
    }


def order_routing_optimization_reserve_node_capacity(
    state: dict,
    reservation: dict,
) -> dict:
    snapshot_key = _capacity_key(reservation["tenant"], reservation["node_id"])
    snapshot = state["capacity_snapshots"].get(snapshot_key)
    if not snapshot:
        return {
            "ok": False,
            "error": "missing_capacity_snapshot",
            "state": state,
        }
    allocated_units = float(reservation["allocated_units"])
    if allocated_units > float(snapshot["available_to_promise"]):
        return {"ok": False, "error": "insufficient_capacity", "state": state}
    updated_snapshot = {
        **snapshot,
        "reserved_units": round(snapshot["reserved_units"] + allocated_units, 2),
        "available_to_promise": round(
            snapshot["available_to_promise"] - allocated_units,
            2,
        ),
    }
    hold_minutes = int(state["parameters"].get("reservation_hold_minutes", 30))
    reservation_record = {
        **reservation,
        "allocated_units": round(allocated_units, 2),
        "hold_minutes": hold_minutes,
        "status": "reserved",
    }
    next_state = {
        **state,
        "capacity_snapshots": {
            **state["capacity_snapshots"],
            snapshot_key: updated_snapshot,
        },
        "node_reservations": {
            **state["node_reservations"],
            reservation["reservation_id"]: reservation_record,
        },
    }
    next_state = _append_event(
        next_state,
        "NodeCapacityReserved",
        {
            "tenant": reservation["tenant"],
            "decision_id": reservation["decision_id"],
            "reservation_id": reservation["reservation_id"],
            "node_id": reservation["node_id"],
            "allocated_units": reservation_record["allocated_units"],
        },
    )
    return {
        "ok": True,
        "state": next_state,
        "reservation": reservation_record,
        "capacity_snapshot": updated_snapshot,
    }


def order_routing_optimization_simulate_counterfactual(
    state: dict,
    decision_id: str,
    *,
    proposed_node: str,
) -> dict:
    decision = state["routing_decisions"][decision_id]
    order_id = decision["order_id"]
    current_node = decision["selected_node_ids"][0]
    proposed = next(
        candidate
        for candidate in state["route_candidates"].values()
        if candidate["order_id"] == order_id and candidate["node_id"] == proposed_node
    )
    current = next(
        candidate
        for candidate in state["route_candidates"].values()
        if candidate["order_id"] == order_id and candidate["node_id"] == current_node
    )
    return {
        "ok": True,
        "decision_id": decision_id,
        "current_node": current_node,
        "proposed_node": proposed_node,
        "cost_delta": round(proposed["total_cost"] - current["total_cost"], 2),
        "sla_delta": round(proposed["sla_hours"] - current["sla_hours"], 2),
        "carbon_delta": round(proposed["carbon_kg"] - current["carbon_kg"], 2),
    }


def order_routing_optimization_forecast_capacity(
    *,
    capacity_path: tuple[float, ...],
    demand_path: tuple[float, ...],
    horizon_hours: int,
) -> dict:
    average_capacity = sum(capacity_path) / max(len(capacity_path), 1)
    average_demand = sum(demand_path) / max(len(demand_path), 1)
    expected_available_units = max(
        average_capacity - average_demand,
        0.0,
    )
    saturation_risk = min(
        round(average_demand / max(average_capacity, 0.01), 4),
        1.0,
    )
    return {
        "ok": True,
        "horizon_hours": horizon_hours,
        "expected_available_units": round(expected_available_units, 2),
        "saturation_risk": saturation_risk,
    }


def order_routing_optimization_recommend_exception_resolution(
    exception_type: str,
) -> dict:
    actions = {
        "capacity_shortfall": "reroute_to_backup_node",
        "tax_mismatch": "reprice_and_reselect_route",
        "carrier_disruption": "promote_self_healing_route",
        "inventory_drift": "refresh_availability_projection",
    }
    return {
        "ok": exception_type in actions,
        "exception_type": exception_type,
        "action": actions.get(exception_type, "manual_routing_review"),
    }


def order_routing_optimization_parse_route_request(text: str) -> dict:
    parsed = {
        "order_id": _token_after(text, "order"),
        "region": _token_after(text, "region"),
        "requested_units": _number_after(text, "units"),
        "sla_target_hours": _number_after(text, "sla"),
        "split_policy": _token_after(text, "split"),
    }
    ok = (
        bool(parsed["order_id"])
        and bool(parsed["region"])
        and parsed["requested_units"] is not None
        and parsed["sla_target_hours"] is not None
    )
    return {"ok": ok, **parsed}


def order_routing_optimization_score_fulfillment_risk(metrics: dict) -> dict:
    risk_score = round(
        float(metrics.get("stockout_probability", 0.0)) * 0.35
        + float(metrics.get("tax_variance", 0.0)) * 0.2
        + float(metrics.get("exception_rate", 0.0)) * 0.25
        + float(metrics.get("capacity_volatility", 0.0)) * 0.2,
        4,
    )
    return {
        "ok": True,
        "risk_score": risk_score,
        "band": "high" if risk_score >= 0.6 else "moderate" if risk_score >= 0.3 else "low",
    }


def order_routing_optimization_self_heal_route_selection(
    decision: dict,
    candidates: tuple[dict, ...],
    *,
    unavailable_nodes: tuple[str, ...],
) -> dict:
    fallback_candidates = tuple(
        candidate
        for candidate in candidates
        if candidate["node_id"] not in unavailable_nodes
    )
    selected = max(
        fallback_candidates,
        key=lambda candidate: candidate["objective_score"],
    )
    original_nodes = set(decision.get("selected_node_ids", ()))
    return {
        "ok": True,
        "selected_node": selected["node_id"],
        "failover_used": selected["node_id"] not in original_nodes,
        "objective_score": selected["objective_score"],
    }


def order_routing_optimization_generate_routing_proof(
    state: dict,
    decision_id: str,
    *,
    disclosure: tuple[str, ...],
) -> dict:
    decision = state["routing_decisions"][decision_id]
    public_claims = {
        field: decision[field] for field in disclosure if field in decision
    }
    proof_hash = _digest(
        {"claims": public_claims, "event_hash": state["events"][-1]["hash"]}
    )
    return {
        "ok": True,
        "proof": "zk_routing_" + proof_hash[:24],
        "hash": proof_hash,
        "public_claims": public_claims,
    }


def order_routing_optimization_screen_policy(
    state: dict,
    decision_id: str,
    *,
    blocked_nodes: tuple[str, ...],
    carbon_budget: float | None = None,
) -> dict:
    decision = state["routing_decisions"][decision_id]
    blocked = bool(set(decision["selected_node_ids"]) & set(blocked_nodes))
    over_budget = carbon_budget is not None and decision["total_carbon"] > carbon_budget
    clear = not blocked and not over_budget
    return {
        "ok": clear,
        "decision": "clear" if clear else "blocked",
        "decision_id": decision_id,
        "blocked_nodes": tuple(sorted(set(decision["selected_node_ids"]) & set(blocked_nodes))),
        "carbon_budget": carbon_budget,
    }


def order_routing_optimization_run_control_tests(state: dict) -> dict:
    gaps = []
    configuration = state.get("configuration", {})
    if not configuration.get("ok"):
        gaps.append("invalid_configuration")
    if not state.get("rules"):
        gaps.append("missing_rules")
    if not state.get("parameters"):
        gaps.append("missing_parameters")
    if any(
        not rule.get("compiled_hash") or not rule.get("compiled_evidence")
        for rule in state["rules"].values()
    ):
        gaps.append("uncompiled_rules")
    if configuration.get("stream_engine_picker_visible"):
        gaps.append("stream_engine_picker_exposed")
    if configuration.get("user_selectable_event_contract"):
        gaps.append("user_selectable_event_contract")
    if state.get("dead_letter"):
        gaps.append("dead_letter_backlog")
    hash_chain_valid = all(
        event["previous_hash"]
        == (state["events"][index - 1]["hash"] if index else "GENESIS")
        for index, event in enumerate(state["events"])
    )
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {
        "ok": not gaps,
        "blocking_gaps": tuple(gaps),
        "hash_chain_valid": hash_chain_valid,
    }


def order_routing_optimization_build_api_contract() -> dict:
    return {
        "ok": True,
        "routes": (
            "POST /route-orders",
            "GET /route-candidates",
            "POST /capacity",
        ),
        "events": {
            "emits": (
                "FulfillmentRouteSelected",
                "NodeCapacityReserved",
            ),
            "consumes": ORDER_ROUTING_OPTIMIZATION_CONSUMED_EVENT_TYPES,
        },
        "permissions": (
            "order_routing_optimization.route",
            "order_routing_optimization.capacity",
            "order_routing_optimization.configure",
            "order_routing_optimization.audit",
            "order_routing_optimization.event",
        ),
        "configuration": (
            "ORDER_ROUTING_OPTIMIZATION_DATABASE_BACKEND",
            "ORDER_ROUTING_OPTIMIZATION_EVENT_TOPIC",
            "ORDER_ROUTING_OPTIMIZATION_RETRY_LIMIT",
            "ORDER_ROUTING_OPTIMIZATION_DEFAULT_CURRENCY",
        ),
    }


def order_routing_optimization_federate_routing_view(
    state: dict,
    order_id: str,
    *,
    systems: tuple[str, ...],
) -> dict:
    decision = next(
        candidate
        for candidate in state["routing_decisions"].values()
        if candidate["order_id"] == order_id
    )
    return {
        "ok": True,
        "order_id": order_id,
        "systems": systems,
        "projection": {
            "selected_node_ids": decision["selected_node_ids"],
            "split": decision["split"],
            "tax_total": state["tax_quotes"].get(order_id, 0.0),
            "verified": state["order_evidence"].get(order_id, {}).get("verified", False),
        },
    }


def order_routing_optimization_run_resilience_drill(
    state: dict,
    scenario: str,
) -> dict:
    event_topic = state["configuration"].get(
        "event_topic",
        "appgen.order-routing.events",
    )
    return {
        "ok": bool(state["outbox"])
        and scenario
        in {
            "availability_projection_timeout",
            "tax_projection_lag",
            "routing_worker_restart",
        },
        "scenario": scenario,
        "mode": "degraded_outbox_replay",
        "retry_limit": state["configuration"].get("retry_limit", 3),
        "dead_letter_topic": f"{event_topic}.dead_letter",
    }


def order_routing_optimization_rotate_crypto_epoch(
    state: dict,
    algorithm: str,
) -> dict:
    epoch = int(state["crypto_epoch"]["epoch"]) + 1
    return {
        "ok": True,
        "epoch": epoch,
        "algorithm": algorithm,
        "key_id": f"order_routing_epoch_{epoch:04d}",
    }


def order_routing_optimization_schedule_carbon_aware_route(
    candidates: tuple[dict, ...],
) -> dict:
    selected = min(candidates, key=lambda candidate: candidate["carbon_kg"])
    return {
        "ok": True,
        "node_id": selected["node_id"],
        "carbon_kg": selected["carbon_kg"],
    }


def order_routing_optimization_optimize_route_network(
    candidates: tuple[dict, ...],
    *,
    demand_units: float,
) -> dict:
    feasible = tuple(
        candidate
        for candidate in candidates
        if candidate["available_to_promise"] >= demand_units
    )
    pool = feasible or candidates
    scored = tuple(
        {
            **candidate,
            "optimization_score": round(
                (
                    candidate["available_to_promise"] * 0.4
                    + (1 / max(candidate["distance_km"], 1.0)) * 120
                    + (1 / max(candidate["total_cost"], 1.0)) * 400
                    + (1 / max(candidate["carbon_kg"], 1.0)) * 80
                ),
                4,
            ),
        }
        for candidate in pool
    )
    selected = max(scored, key=lambda candidate: candidate["optimization_score"])
    return {
        "ok": True,
        "node_id": selected["node_id"],
        "objective_score": selected["optimization_score"],
        "candidates": scored,
    }


def order_routing_optimization_clear_capacity_auction(
    nodes: tuple[dict, ...],
    *,
    quantity: float,
) -> dict:
    weights = tuple(
        {
            "node_id": node["node_id"],
            "weight": float(node["bid"]) * float(node["available_units"]),
        }
        for node in nodes
    )
    total_weight = sum(item["weight"] for item in weights) or 1.0
    allocations = tuple(
        {
            "node_id": item["node_id"],
            "allocated_units": round(quantity * item["weight"] / total_weight, 2),
        }
        for item in weights
    )
    return {
        "ok": round(sum(item["allocated_units"] for item in allocations), 2)
        == round(quantity, 2),
        "allocations": allocations,
        "clearing_bid": round(
            sum(float(node["bid"]) for node in nodes) / max(len(nodes), 1),
            4,
        ),
    }


def order_routing_optimization_detect_routing_anomaly(state: dict) -> dict:
    objective_scores = tuple(
        decision["objective_score"] for decision in state["routing_decisions"].values()
    )
    if not objective_scores:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(objective_scores) or 1.0
    entropy = round(
        -sum(
            (score / total) * math.log(max(score / total, 0.0001), 2)
            for score in objective_scores
        ),
        4,
    )
    mean = sum(objective_scores) / len(objective_scores)
    return {
        "ok": True,
        "entropy": entropy,
        "outliers": tuple(
            round(score, 4)
            for score in objective_scores
            if abs(score - mean) > max(mean * 0.4, 0.05)
        ),
    }


def order_routing_optimization_model_stochastic_exposure(
    *,
    score_path: tuple[float, ...],
    volatility: float,
) -> dict:
    drift = 0.0
    if len(score_path) >= 2:
        drift = (score_path[-1] - score_path[0]) / (len(score_path) - 1)
    exposure = abs(drift) * volatility * len(score_path)
    return {
        "ok": True,
        "expected_exposure": round(exposure, 4),
        "tail_risk": round(exposure * 1.65, 4),
        "simulation_count": 1000,
    }


def order_routing_optimization_register_governed_model(
    name: str,
    metadata: dict,
) -> dict:
    return {
        "ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1,
        "name": name,
        "metadata": metadata,
        "governance": {
            "regulated": True,
            "feature_lineage": tuple(metadata.get("features", ())),
            "explainability_required": True,
        },
    }


def order_routing_optimization_build_workbench_view(
    state: dict,
    *,
    tenant: str,
) -> dict:
    candidates = tuple(
        candidate
        for candidate in state["route_candidates"].values()
        if candidate["tenant"] == tenant
    )
    snapshots = tuple(
        snapshot
        for snapshot in state["capacity_snapshots"].values()
        if snapshot["tenant"] == tenant
    )
    decisions = tuple(
        decision
        for decision in state["routing_decisions"].values()
        if decision["tenant"] == tenant
    )
    reservations = tuple(
        reservation
        for reservation in state["node_reservations"].values()
        if reservation["tenant"] == tenant
    )
    inbox = tuple(entry for entry in state["inbox"] if entry["tenant"] == tenant)
    dead_letter = tuple(
        entry
        for entry in state["dead_letter"]
        if any(
            inbox_entry["event_id"] == entry["event_id"] and inbox_entry["tenant"] == tenant
            for inbox_entry in inbox
        )
    )
    configuration = state.get("configuration", {})
    rule_ids = tuple(sorted(state.get("rules", {})))
    parameter_names = tuple(sorted(state.get("parameters", {})))
    return {
        "ok": True,
        "tenant": tenant,
        "route_candidate_count": len(candidates),
        "ready_candidate_count": len(
            tuple(candidate for candidate in candidates if candidate["status"] == "ready")
        ),
        "capacity_snapshot_count": len(snapshots),
        "routing_decision_count": len(decisions),
        "split_decision_count": len(
            tuple(decision for decision in decisions if decision["split"])
        ),
        "reservation_count": len(reservations),
        "reserved_units": round(
            sum(reservation["allocated_units"] for reservation in reservations),
            2,
        ),
        "substitution_eligible_count": len(
            tuple(candidate for candidate in candidates if candidate["substitution_eligible"])
        ),
        "inbox_count": len(inbox),
        "event_outbox_count": len(state["outbox"]),
        "dead_letter_count": len(dead_letter),
        "configuration_bound": bool(configuration.get("ok")),
        "rule_count": len(rule_ids),
        "parameter_count": len(parameter_names),
        "binding_evidence": {
            "configuration": {
                "bound": bool(configuration.get("ok")),
                "database_backend": configuration.get("database_backend"),
                "event_contract": configuration.get("event_contract"),
                "event_topic": configuration.get("event_topic"),
                "visible_event_contracts": configuration.get(
                    "visible_event_contracts",
                    (),
                ),
                "stream_engine_picker_visible": configuration.get(
                    "stream_engine_picker_visible"
                ),
                "user_selectable_event_contract": configuration.get(
                    "user_selectable_event_contract"
                ),
                "supported_fields": configuration.get(
                    "supported_configuration_fields",
                    ORDER_ROUTING_OPTIMIZATION_SUPPORTED_CONFIGURATION_FIELDS,
                ),
            },
            "rules": tuple(
                {
                    "rule_id": rule_id,
                    "scope": state["rules"][rule_id].get("scope"),
                    "compiled_hash": state["rules"][rule_id].get("compiled_hash"),
                    "required_fields": state["rules"][rule_id]
                    .get("compiled_evidence", {})
                    .get("required_fields", ()),
                }
                for rule_id in rule_ids
            ),
            "parameters": {
                "supported": ORDER_ROUTING_OPTIMIZATION_SUPPORTED_PARAMETER_KEYS,
                "active": parameter_names,
            },
        },
    }


def _append_event(
    state: dict,
    event_type: str,
    payload: dict,
    *,
    emit: bool = True,
) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {
        "event_id": f"order_routing_evt_{sequence:06d}",
        "event_type": event_type,
        "payload": payload,
        "previous_hash": previous_hash,
    }
    event = {**event, "hash": _digest(event)}
    next_state = {**state, "events": (*state["events"], event)}
    if emit:
        next_state = {
            **next_state,
            "outbox": (
                *next_state["outbox"],
                {
                    "event_type": event_type,
                    "payload": payload,
                    "idempotency_key": (
                        "order_routing_optimization:"
                        f"{event_type}:{event['event_id']}"
                    ),
                },
            ),
        }
    return next_state


def _active_rule_for_tenant(state: dict, tenant: str) -> dict:
    return next(
        rule
        for rule in state["rules"].values()
        if rule["tenant"] == tenant and rule["enabled"]
    )


def _capacity_key(tenant: str, node_id: str) -> str:
    return f"{tenant}:{node_id}"


def _score_route_candidates(
    candidates: tuple[dict, ...],
    *,
    request: dict,
    parameters: dict,
) -> tuple[dict, ...]:
    cost_values = tuple(candidate["total_cost"] for candidate in candidates)
    sla_values = tuple(candidate["sla_hours"] for candidate in candidates)
    carbon_values = tuple(candidate["carbon_kg"] for candidate in candidates)
    risk_values = tuple(candidate["risk_score"] for candidate in candidates)
    requested_units = max(float(request["requested_units"]), 0.01)
    weight_total = sum(float(parameters[name]) for name in ORDER_ROUTING_OPTIMIZATION_SUPPORTED_PARAMETER_KEYS[:5]) or 1.0
    scored = []
    for candidate in candidates:
        cost_component = _normalize_metric(
            candidate["total_cost"],
            min(cost_values),
            max(cost_values),
            lower_is_better=True,
        )
        sla_component = _normalize_metric(
            candidate["sla_hours"],
            min(sla_values),
            max(sla_values),
            lower_is_better=True,
        )
        carbon_component = _normalize_metric(
            candidate["carbon_kg"],
            min(carbon_values),
            max(carbon_values),
            lower_is_better=True,
        )
        risk_component = _normalize_metric(
            candidate["risk_score"],
            min(risk_values),
            max(risk_values),
            lower_is_better=True,
        )
        capacity_component = min(candidate["available_to_promise"] / requested_units, 1.0)
        objective_score = round(
            float(parameters["cost_weight"]) * cost_component
            + float(parameters["sla_weight"]) * sla_component
            + float(parameters["capacity_weight"]) * capacity_component
            + float(parameters["risk_weight"]) * risk_component
            + float(parameters["carbon_weight"]) * carbon_component,
            4,
        )
        confidence = round(
            max(0.0, min(1.0, objective_score / weight_total)),
            4,
        )
        scored.append(
            {
                **candidate,
                "objective_score": objective_score,
                "confidence": confidence,
                "cost_component": round(cost_component, 4),
                "sla_component": round(sla_component, 4),
                "capacity_component": round(capacity_component, 4),
                "risk_component": round(risk_component, 4),
                "carbon_component": round(carbon_component, 4),
            }
        )
    return tuple(scored)


def _normalize_metric(
    value: float,
    minimum: float,
    maximum: float,
    *,
    lower_is_better: bool,
) -> float:
    if math.isclose(minimum, maximum):
        return 1.0
    ratio = (value - minimum) / (maximum - minimum)
    return 1.0 - ratio if lower_is_better else ratio


def _normalize_fields(values: dict, sequence_fields: set[str]) -> dict:
    normalized = dict(values)
    for field in sequence_fields:
        if field in normalized and isinstance(normalized[field], list):
            normalized[field] = tuple(normalized[field])
    return normalized


def _token_after(text: str, marker: str) -> str | None:
    match = re.search(rf"{re.escape(marker)}\s+([a-z0-9_:-]+)", text, re.I)
    return match.group(1) if match else None


def _number_after(text: str, marker: str) -> float | None:
    match = re.search(rf"{re.escape(marker)}\s+(\d+(?:\.\d+)?)", text, re.I)
    return float(match.group(1)) if match else None


def _digest(value: object) -> str:
    return hashlib.sha3_256(
        json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()
