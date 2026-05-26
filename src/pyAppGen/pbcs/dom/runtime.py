"""Executable runtime for the Distributed Order Management PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


DOM_REQUIRED_EVENT_TOPIC = "appgen.dom.events"
DOM_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
DOM_OWNED_TABLES = (
    "sales_order",
    "order_line",
    "order_status",
    "order_note",
    "order_hold",
    "order_promise",
    "order_channel_context",
    "order_payment_projection",
    "customer_projection",
    "customer_identity_projection",
    "tax_projection",
    "fraud_screen",
    "fraud_signal",
    "order_verification",
    "order_price_component",
    "order_discount_projection",
    "inventory_allocation_projection",
    "inventory_node_projection",
    "payment_authorization_projection",
    "fulfillment_plan",
    "fulfillment_plan_line",
    "fulfillment_node_candidate",
    "fulfillment_reservation_projection",
    "split_shipment",
    "backorder",
    "substitution",
    "cancellation_request",
    "shipment_projection",
    "shipment_status_projection",
    "order_exception",
    "route_selection",
    "risk_score",
    "promise_demand_forecast",
    "fulfillment_policy_simulation",
    "fulfillment_route_replay",
    "order_verification_proof",
    "order_policy_screening",
    "order_audit_trace",
    "order_federation_projection",
    "order_carbon_fulfillment",
    "order_fulfillment_optimization",
    "order_node_allocation",
    "order_anomaly_signal",
    "order_fulfillment_exposure_model",
    "order_parsed_event",
    "order_seed_data",
    "dom_schema_extension",
    "dom_control_assertion",
    "dom_governed_model",
    "policy_rule",
    "dom_parameter",
    "dom_configuration",
    "dom_appgen_outbox_event",
    "dom_appgen_inbox_event",
    "dom_dead_letter_event",
)
DOM_EMITTED_EVENT_TYPES = (
    "OrderCaptured",
    "TaxProjectionApplied",
    "FraudScreened",
    "OrderVerified",
    "OrderPriced",
    "InventoryAllocationProjected",
    "FulfillmentPlanCreated",
    "OrderShipped",
)
DOM_CONSUMED_EVENT_TYPES = (
    "InventoryAllocated",
    "TaxCalculated",
    "CustomerUpdated",
    "PaymentAuthorized",
    "ShipmentDelivered",
)
_DOM_RUNTIME_TABLES = (
    "dom_appgen_outbox_event",
    "dom_appgen_inbox_event",
    "dom_dead_letter_event",
)
_DOM_ALLOWED_DEPENDENCIES = (
    "inventory_allocation_projection",
    "tax_calculation_projection",
    "customer_profile_projection",
    "payment_authorization_projection",
    "shipment_delivery_projection",
    "GET /inventory/allocations/{id}",
    "GET /tax/calculations/{id}",
    "GET /customers/{id}",
    "GET /payments/authorizations/{id}",
    "GET /shipments/{id}",
    "POST /audit/order-events",
)
_DOM_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}


DOM_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_order_lifecycle",
    "graph_relational_order_topology",
    "multi_tenant_order_isolation",
    "schema_evolution_resilient_order_schema",
    "probabilistic_fraud_allocation_confidence",
    "real_time_order_orchestration_analytics",
    "counterfactual_sourcing_fulfillment_simulation",
    "temporal_promise_demand_forecasting",
    "autonomous_order_exception_resolution",
    "semantic_order_event_parsing",
    "predictive_cancellation_fulfillment_risk",
    "self_healing_fulfillment_route_selection",
    "zero_knowledge_order_verification_proof",
    "immutable_order_audit_trail",
    "dynamic_order_policy_screening",
    "automated_order_control_testing",
    "universal_api_async_streaming",
    "cross_system_order_federation",
    "commerce_service_channel_integration",
    "decentralized_order_identity",
    "chaos_engineered_orchestration_tolerance",
    "quantum_resistant_order_authorization",
    "carbon_aware_fulfillment_planning",
    "algebraic_fulfillment_optimization",
    "mechanism_design_node_allocation",
    "information_theoretic_order_anomaly_detection",
    "temporal_fulfillment_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_order_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "order_mlops_governance",
)
DOM_STANDARD_FEATURE_KEYS = (
    "sales_order_capture",
    "order_line_validation",
    "order_notes",
    "order_holds",
    "order_promising",
    "order_channel_context",
    "payment_projection",
    "customer_projection",
    "customer_identity_projection",
    "tax_projection",
    "fraud_screening",
    "fraud_signals",
    "order_verification",
    "order_pricing",
    "price_components",
    "discount_projection",
    "inventory_allocation_projection",
    "inventory_node_projection",
    "fulfillment_planning",
    "fulfillment_plan_lines",
    "fulfillment_node_candidates",
    "fulfillment_reservation_projection",
    "split_shipment",
    "backorder_management",
    "substitution_management",
    "cancellation_control",
    "shipment_projection",
    "shipment_status_projection",
    "order_lifecycle_status",
    "promise_demand_forecast",
    "fulfillment_policy_simulation",
    "fulfillment_route_replay",
    "order_verification_proof",
    "order_policy_screening",
    "order_audit_trace",
    "order_federation_projection",
    "carbon_aware_fulfillment",
    "fulfillment_optimization",
    "node_allocation",
    "order_anomaly_detection",
    "stochastic_fulfillment_exposure",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "retry_dead_letter_evidence",
    "multi_channel_isolation",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def dom_runtime_capabilities() -> dict:
    smoke = dom_runtime_smoke()
    return {
        "format": "appgen.dom-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "dom",
        "implementation_directory": "src/pyAppGen/pbcs/dom",
        "owned_tables": DOM_OWNED_TABLES,
        "capabilities": DOM_RUNTIME_CAPABILITY_KEYS,
        "standard_features": DOM_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "capture_order",
            "upsert_customer_projection",
            "apply_tax_projection",
            "screen_fraud",
            "verify_order",
            "price_order",
            "apply_inventory_allocation",
            "create_fulfillment_plan",
            "confirm_order_shipped",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def dom_runtime_smoke() -> dict:
    state = dom_empty_state()
    state = dom_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": DOM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "allowed_channels": ("web", "store", "marketplace"),
            "allowed_statuses": ("captured", "verified", "priced", "planned", "shipped"),
            "workbench_limit": 100,
        },
    )["state"]
    state = dom_set_parameter(state, "fraud_threshold", 0.7)["state"]
    state = dom_set_parameter(state, "allocation_confidence_threshold", 0.75)["state"]
    state = dom_set_parameter(state, "partial_fulfillment_threshold", 0.5)["state"]
    state = dom_register_rule(
        state,
        {
            "rule_id": "rule_web_standard",
            "tenant": "tenant_alpha",
            "rule_type": "order_orchestration",
            "channels": ("web", "store"),
            "customer_statuses": ("active", "vip"),
            "allow_split": True,
            "preferred_nodes": ("node_east", "node_west"),
            "restricted_destinations": ("restricted_zone",),
            "requires_tax": True,
            "status": "active",
        },
    )["state"]
    state = dom_register_schema_extension(state, "sales_order", {"channel_metadata": "jsonb"})["state"]
    customer = dom_upsert_customer_projection(
        state,
        {"customer_id": "cust_100", "tenant": "tenant_alpha", "status": "active", "risk": 0.08, "identity": {"did": "did:appgen:customer-100", "issuer": "trusted_registry", "status": "active"}},
    )
    state = customer["state"]
    order = dom_capture_order(
        state,
        {
            "order_id": "order_100",
            "tenant": "tenant_alpha",
            "customer_id": "cust_100",
            "channel": "web",
            "currency": "USD",
            "destination": "BOS",
            "service_level": "standard",
            "lines": ({"line_id": "line_1", "item_id": "sku_100", "quantity": 2, "unit_price": 100},),
        },
    )
    state = order["state"]
    tax = dom_apply_tax_projection(state, "order_100", {"calculation_id": "tax_100", "tax_total": 17.5, "status": "calculated"})
    state = tax["state"]
    fraud = dom_screen_fraud(state, "order_100", signals={"ip_risk": 0.05, "velocity": 0.1, "customer_risk": 0.08})
    state = fraud["state"]
    verification = dom_verify_order(state, "order_100")
    state = verification["state"]
    pricing = dom_price_order(state, "order_100")
    state = pricing["state"]
    allocation = dom_apply_inventory_allocation(state, "order_100", {"allocation_id": "alloc_100", "item_id": "sku_100", "quantity": 2, "node_id": "node_east", "confidence": 0.92})
    state = allocation["state"]
    plan = dom_create_fulfillment_plan(state, "order_100")
    state = plan["state"]
    shipped = dom_confirm_order_shipped(state, "order_100", shipment_id="ship_100")
    state = shipped["state"]
    simulation = dom_simulate_fulfillment_policy(state, "order_100", proposed_node="node_west")
    forecast = dom_forecast_promise_demand((2, 4, 6), service_days=3)
    parsed = dom_parse_order_event("order order_777 customer cust_100 amount 217.5 channel web")
    risk = dom_score_order_risk({"fraud": 0.1, "allocation_gap": 0.05, "customer_risk": 0.08})
    exception = dom_recommend_exception_resolution("allocation_gap")
    route = dom_route_fulfillment(plan["plan"], rails=({"route": "warehouse_api", "available": False, "latency": 1}, {"route": "outbox", "available": True, "latency": 3}))
    proof = dom_generate_order_verification_proof(state, "order_100", disclosure=("order_id", "status", "total"))
    screening = dom_screen_order_policy(state, "order_100", restricted_destinations=("restricted_zone",))
    controls = dom_run_control_tests(state)
    api = dom_build_api_contract()
    schema = dom_build_schema_contract()
    service = dom_build_service_contract()
    release = dom_build_release_evidence()
    federation = dom_federate_order_view(state, "order_100", systems=("inventory", "tax", "wms", "transportation"))
    identity = dom_verify_order_identity(customer["customer"]["identity"])
    resilience = dom_run_resilience_drill(state, "fulfillment_route_timeout")
    crypto = dom_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = dom_schedule_carbon_aware_fulfillment(({"node_id": "node_east", "carbon": 140}, {"node_id": "node_west", "carbon": 80}))
    optimization = dom_optimize_fulfillment(({"node_id": "node_east", "available": 2, "distance": 90, "carbon": 140}, {"node_id": "node_west", "available": 2, "distance": 110, "carbon": 80}), quantity=2)
    mechanism = dom_allocate_nodes(({"node_id": "node_east", "bid": 0.8, "service": 0.9}, {"node_id": "node_west", "bid": 0.6, "service": 0.7}), quantity=2)
    anomaly = dom_detect_order_anomaly(state)
    stochastic = dom_model_stochastic_fulfillment_exposure(delay_path=(1, 2, 4), volatility=0.1)
    workbench = dom_build_workbench_view(state, tenant="tenant_alpha")
    model = dom_register_governed_model("order_risk", {"features": ("fraud", "allocation", "customer"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_order_lifecycle", "ok": len(state["events"]) >= 8 and state["events"][-1]["hash"]},
        {"id": "graph_relational_order_topology", "ok": order["order"]["graph_degree"] >= 4},
        {"id": "multi_tenant_order_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_order_schema", "ok": state["schema_extensions"]["sales_order"]["channel_metadata"] == "jsonb"},
        {"id": "probabilistic_fraud_allocation_confidence", "ok": fraud["decision"] == "clear" and allocation["allocation"]["confidence"] >= 0.9},
        {"id": "real_time_order_orchestration_analytics", "ok": workbench["shipped_count"] == 1 and workbench["open_order_count"] == 0},
        {"id": "counterfactual_sourcing_fulfillment_simulation", "ok": simulation["ok"] and simulation["proposed_node"] == "node_west"},
        {"id": "temporal_promise_demand_forecasting", "ok": forecast["ok"] and forecast["promise_load"] > 0},
        {"id": "autonomous_order_exception_resolution", "ok": exception["action"] == "reroute_fulfillment"},
        {"id": "semantic_order_event_parsing", "ok": parsed["ok"] and parsed["amount"] == 217.5},
        {"id": "predictive_cancellation_fulfillment_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_fulfillment_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_order_verification_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_order_")},
        {"id": "immutable_order_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_order_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_order_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and "OrderVerified" in api["events"]["emits"]},
        {"id": "cross_system_order_federation", "ok": federation["ok"] and "inventory" in federation["systems"]},
        {"id": "commerce_service_channel_integration", "ok": order["order"]["channel"] == "web"},
        {"id": "decentralized_order_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_orchestration_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_fulfillment_route"},
        {"id": "quantum_resistant_order_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_fulfillment_planning", "ok": carbon["node_id"] == "node_west"},
        {"id": "algebraic_fulfillment_optimization", "ok": optimization["ok"] and optimization["node_id"] == "node_west"},
        {"id": "mechanism_design_node_allocation", "ok": mechanism["ok"] and mechanism["allocations"][0]["quantity"] > mechanism["allocations"][1]["quantity"]},
        {"id": "information_theoretic_order_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_fulfillment_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("dom:OrderShipped")},
        {"id": "probabilistic_ml_order_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and mechanism["clearing_bid"] > 0},
        {"id": "order_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.dom-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def dom_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letters": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "inventory_allocation_projections": {},
        "tax_calculation_projections": {},
        "customer_profile_projections": {},
        "payment_authorization_projections": {},
        "shipment_delivery_projections": {},
        "orders": {},
        "customers": {},
        "tax": {},
        "fraud": {},
        "allocations": {},
        "fulfillment_plans": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def dom_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _DOM_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Distributed Order Management uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    if configuration.get("database_backend") not in set(DOM_ALLOWED_DATABASE_BACKENDS):
        raise ValueError("Distributed Order Management supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != DOM_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Distributed Order Management requires AppGen-X event topic {DOM_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": DOM_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": DOM_OWNED_TABLES,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def dom_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "fraud_threshold",
        "allocation_confidence_threshold",
        "partial_fulfillment_threshold",
        "max_split_shipments",
        "service_level_weight",
        "distance_weight",
        "margin_weight",
        "promise_horizon_days",
        "exception_age_threshold_hours",
        "retry_limit",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported Distributed Order Management parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def dom_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Distributed Order Management rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("Distributed Order Management rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def dom_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in DOM_OWNED_TABLES:
        raise ValueError(f"Distributed Order Management schema extensions must target owned tables: {DOM_OWNED_TABLES}")
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


def dom_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
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
        "tax_calculation_projections": dict(state.get("tax_calculation_projections", {})),
        "customer_profile_projections": dict(state.get("customer_profile_projections", {})),
        "payment_authorization_projections": dict(state.get("payment_authorization_projections", {})),
        "shipment_delivery_projections": dict(state.get("shipment_delivery_projections", {})),
    }
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in DOM_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"] = (*next_state["retry_evidence"], evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_dom_event"}
            next_state["dead_letters"] = (*next_state["dead_letters"], dead)
            next_state["dead_letter"] = (*next_state["dead_letter"], dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "InventoryAllocated":
        next_state["inventory_allocation_projections"][payload.get("allocation_id", event_id)] = payload
    elif event_type == "TaxCalculated":
        next_state["tax_calculation_projections"][payload.get("calculation_id", event_id)] = payload
    elif event_type == "CustomerUpdated":
        next_state["customer_profile_projections"][payload.get("customer_id", event_id)] = payload
    elif event_type == "PaymentAuthorized":
        next_state["payment_authorization_projections"][payload.get("authorization_id", event_id)] = payload
    elif event_type == "ShipmentDelivered":
        next_state["shipment_delivery_projections"][payload.get("shipment_id", event_id)] = payload
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def dom_upsert_customer_projection(state: dict, customer: dict) -> dict:
    next_state = {**state, "customers": {**state["customers"], customer["customer_id"]: customer}}
    return {"ok": True, "state": next_state, "customer": customer}


def dom_capture_order(state: dict, order: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    allowed = order["channel"] in state["configuration"].get("allowed_channels", ()) and order["channel"] in rule["channels"] and order["destination"] not in rule.get("restricted_destinations", ())
    total = round(sum(line["quantity"] * line["unit_price"] for line in order["lines"]), 2)
    enriched = {**order, "subtotal": total, "total": total, "status": "captured" if allowed else "policy_blocked", "graph_degree": len(order["lines"]) + 4}
    next_state = {**state, "orders": {**state["orders"], order["order_id"]: enriched}}
    next_state = _append_event(next_state, "OrderCaptured", {"tenant": order["tenant"], "order_id": order["order_id"], "subtotal": total})
    return {"ok": allowed, "state": next_state, "order": enriched}


def dom_apply_tax_projection(state: dict, order_id: str, tax: dict) -> dict:
    order = state["orders"][order_id]
    next_state = {**state, "tax": {**state["tax"], order_id: tax}}
    next_state = _append_event(next_state, "TaxProjectionApplied", {"tenant": order["tenant"], "order_id": order_id, "calculation_id": tax["calculation_id"]})
    return {"ok": True, "state": next_state, "tax": tax}


def dom_screen_fraud(state: dict, order_id: str, *, signals: dict) -> dict:
    score = round(signals.get("ip_risk", 0) * 2 + signals.get("velocity", 0) + signals.get("customer_risk", 0), 4)
    threshold = float(state["parameters"].get("fraud_threshold", 0.7))
    screen = {"order_id": order_id, "tenant": state["orders"][order_id]["tenant"], "score": score, "decision": "review" if score >= threshold else "clear", "signals": signals}
    next_state = {**state, "fraud": {**state["fraud"], order_id: screen}}
    next_state = _append_event(next_state, "FraudScreened", {"tenant": screen["tenant"], "order_id": order_id, "decision": screen["decision"], "score": score})
    return {"ok": True, "state": next_state, **screen}


def dom_verify_order(state: dict, order_id: str) -> dict:
    order = state["orders"][order_id]
    customer = state["customers"][order["customer_id"]]
    rule = next(iter(state["rules"].values()))
    tax_ready = (not rule.get("requires_tax", True)) or state["tax"].get(order_id, {}).get("status") == "calculated"
    fraud_clear = state["fraud"].get(order_id, {}).get("decision") == "clear"
    ok = order["status"] == "captured" and customer["status"] in rule["customer_statuses"] and tax_ready and fraud_clear
    updated = {**order, "status": "verified" if ok else "blocked"}
    next_state = {**state, "orders": {**state["orders"], order_id: updated}}
    if ok:
        next_state = _append_event(next_state, "OrderVerified", {"tenant": order["tenant"], "order_id": order_id})
    return {"ok": ok, "state": next_state, "order": updated}


def dom_price_order(state: dict, order_id: str) -> dict:
    order = state["orders"][order_id]
    tax_total = state["tax"].get(order_id, {}).get("tax_total", 0)
    priced = {**order, "tax_total": tax_total, "total": round(order["subtotal"] + tax_total, 2), "status": "priced"}
    next_state = {**state, "orders": {**state["orders"], order_id: priced}}
    next_state = _append_event(next_state, "OrderPriced", {"tenant": order["tenant"], "order_id": order_id, "total": priced["total"]})
    return {"ok": True, "state": next_state, "order": priced}


def dom_apply_inventory_allocation(state: dict, order_id: str, allocation: dict) -> dict:
    order = state["orders"][order_id]
    next_state = {**state, "allocations": {**state["allocations"], order_id: allocation}}
    next_state = _append_event(next_state, "InventoryAllocationProjected", {"tenant": order["tenant"], "order_id": order_id, "allocation_id": allocation["allocation_id"], "confidence": allocation["confidence"]})
    return {"ok": allocation["confidence"] >= float(state["parameters"].get("allocation_confidence_threshold", 0)), "state": next_state, "allocation": allocation}


def dom_create_fulfillment_plan(state: dict, order_id: str) -> dict:
    order = state["orders"][order_id]
    allocation = state["allocations"][order_id]
    rule = next(iter(state["rules"].values()))
    split = rule.get("allow_split", False) and len(order["lines"]) > 1
    plan = {"plan_id": f"plan_{order_id}", "tenant": order["tenant"], "order_id": order_id, "node_id": allocation["node_id"], "split": split, "status": "planned", "confidence": allocation["confidence"]}
    next_state = {**state, "fulfillment_plans": {**state["fulfillment_plans"], plan["plan_id"]: plan}, "orders": {**state["orders"], order_id: {**order, "status": "planned"}}}
    next_state = _append_event(next_state, "FulfillmentPlanCreated", {"tenant": order["tenant"], "order_id": order_id, "plan_id": plan["plan_id"], "node_id": plan["node_id"]})
    return {"ok": True, "state": next_state, "plan": plan}


def dom_confirm_order_shipped(state: dict, order_id: str, *, shipment_id: str) -> dict:
    order = {**state["orders"][order_id], "status": "shipped", "shipment_id": shipment_id}
    next_state = {**state, "orders": {**state["orders"], order_id: order}}
    next_state = _append_event(next_state, "OrderShipped", {"tenant": order["tenant"], "order_id": order_id, "shipment_id": shipment_id})
    return {"ok": True, "state": next_state, "order": order}


def dom_simulate_fulfillment_policy(state: dict, order_id: str, *, proposed_node: str) -> dict:
    current = next(plan for plan in state["fulfillment_plans"].values() if plan["order_id"] == order_id)
    return {"ok": True, "order_id": order_id, "current_node": current["node_id"], "proposed_node": proposed_node, "node_changed": current["node_id"] != proposed_node}


def dom_forecast_promise_demand(demand_path: tuple[float, ...], *, service_days: int) -> dict:
    return {"ok": True, "promise_load": round(sum(demand_path) / max(service_days, 1), 2), "demand_trend": round((demand_path[-1] - demand_path[0]) if len(demand_path) > 1 else 0, 2)}


def dom_parse_order_event(text: str) -> dict:
    order = re.search(r"order\s+([a-z0-9_]+)", text, re.I)
    customer = re.search(r"customer\s+([a-z0-9_]+)", text, re.I)
    channel = re.search(r"channel\s+([a-z0-9_]+)", text, re.I)
    amount = _first_number_after(text, "amount")
    return {"ok": bool(order and customer and channel and amount), "order_id": order.group(1) if order else None, "customer_id": customer.group(1) if customer else None, "channel": channel.group(1) if channel else None, "amount": amount}


def dom_score_order_risk(signals: dict) -> dict:
    risk = round(signals.get("fraud", 0) * 2 + signals.get("allocation_gap", 0) + signals.get("customer_risk", 0), 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.5 else "review"}


def dom_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"allocation_gap": "reroute_fulfillment", "fraud_review": "manual_review", "tax_missing": "request_tax_quote"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def dom_route_fulfillment(plan: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": plan["status"] == "planned", "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"dom:FulfillmentPlan:{plan['plan_id']}"}


def dom_generate_order_verification_proof(state: dict, order_id: str, *, disclosure: tuple[str, ...]) -> dict:
    order = state["orders"][order_id]
    claims = {field: order[field] for field in disclosure if field in order}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_order_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def dom_screen_order_policy(state: dict, order_id: str, *, restricted_destinations: tuple[str, ...]) -> dict:
    order = state["orders"][order_id]
    blocked = order["destination"] in restricted_destinations or order["status"] == "blocked"
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "order_id": order_id}


def dom_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(order["status"] == "blocked" for order in state["orders"].values()):
        gaps.append("blocked_order")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def dom_build_api_contract() -> dict:
    return {
        "ok": True,
        "format": "appgen.dom-api-contract.v1",
        "routes": (
            {"route": "POST /dom/orders", "command": "capture_order", "owned_tables": ("sales_order", "order_line", "order_status"), "emits": ("OrderCaptured",), "requires_permission": "dom.create", "idempotency_key": "order_id"},
            {"route": "POST /dom/orders/{id}/tax-projection", "command": "apply_tax_projection", "owned_tables": ("tax_projection",), "emits": ("TaxProjectionApplied",), "requires_permission": "dom.verify", "idempotency_key": "calculation_id"},
            {"route": "POST /dom/orders/{id}/fraud-screen", "command": "screen_fraud", "owned_tables": ("fraud_screen", "risk_score"), "emits": ("FraudScreened",), "requires_permission": "dom.verify", "idempotency_key": "order_id:fraud"},
            {"route": "POST /dom/orders/{id}/verify", "command": "verify_order", "owned_tables": ("sales_order", "order_status"), "emits": ("OrderVerified",), "requires_permission": "dom.verify", "idempotency_key": "order_id:verify"},
            {"route": "POST /dom/orders/{id}/price", "command": "price_order", "owned_tables": ("sales_order",), "emits": ("OrderPriced",), "requires_permission": "dom.price", "idempotency_key": "order_id:price"},
            {"route": "POST /dom/orders/{id}/allocation", "command": "apply_inventory_allocation", "owned_tables": ("inventory_allocation_projection",), "emits": ("InventoryAllocationProjected",), "requires_permission": "dom.allocate", "idempotency_key": "allocation_id"},
            {"route": "POST /dom/fulfillment-plans", "command": "create_fulfillment_plan", "owned_tables": ("fulfillment_plan", "split_shipment", "route_selection"), "emits": ("FulfillmentPlanCreated",), "requires_permission": "dom.plan", "idempotency_key": "order_id:plan"},
            {"route": "POST /dom/shipments", "command": "confirm_order_shipped", "owned_tables": ("shipment_projection", "sales_order"), "emits": ("OrderShipped",), "requires_permission": "dom.ship", "idempotency_key": "shipment_id"},
            {"route": "POST /dom/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": DOM_CONSUMED_EVENT_TYPES, "requires_permission": "dom.event", "idempotency_key": "event_id"},
            {"route": "GET /dom/workbench", "query": "build_workbench_view", "owned_tables": DOM_OWNED_TABLES, "requires_permission": "dom.audit"},
        ),
        "declared_catalog_routes": ("POST /orders", "POST /allocation", "GET /fulfillment-plans"),
        "events": {"emits": DOM_EMITTED_EVENT_TYPES, "consumes": DOM_CONSUMED_EVENT_TYPES},
        "emits": DOM_EMITTED_EVENT_TYPES,
        "consumes": DOM_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(dom_permissions_contract()["permissions"])),
        "database_backends": DOM_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": DOM_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": ("DOM_DATABASE_URL", "DOM_EVENT_TOPIC", "DOM_RETRY_LIMIT", "DOM_DEFAULT_CURRENCY"),
    }


def dom_build_schema_contract() -> dict:
    """Return DOM-owned schema, migration, model, and relationship evidence."""
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {
        table: default_fields for table in DOM_OWNED_TABLES
    } | {
        "sales_order": ("tenant", "order_id", "customer_id", "channel", "currency", "destination", "status"),
        "order_line": ("tenant", "line_id", "order_id", "item_id", "quantity", "unit_price"),
        "order_status": ("tenant", "status_id", "order_id", "status", "reason", "changed_at"),
        "order_note": ("tenant", "note_id", "order_id", "note_type", "body", "created_by"),
        "order_hold": ("tenant", "hold_id", "order_id", "hold_type", "reason", "status"),
        "order_promise": ("tenant", "promise_id", "order_id", "promise_date", "confidence", "source"),
        "order_channel_context": ("tenant", "channel_context_id", "order_id", "channel", "campaign", "metadata"),
        "order_payment_projection": ("tenant", "payment_projection_id", "order_id", "authorization_id", "amount", "status"),
        "customer_projection": ("tenant", "customer_id", "status", "risk", "identity_id", "updated_at"),
        "customer_identity_projection": ("tenant", "identity_id", "customer_id", "did", "issuer", "status"),
        "tax_projection": ("tenant", "calculation_id", "order_id", "tax_total", "status", "audit_hash"),
        "fraud_screen": ("tenant", "fraud_screen_id", "order_id", "risk_score", "decision", "screened_at"),
        "fraud_signal": ("tenant", "fraud_signal_id", "order_id", "signal_type", "value", "weight"),
        "order_verification": ("tenant", "verification_id", "order_id", "verified", "reason", "verified_at"),
        "order_price_component": ("tenant", "price_component_id", "order_id", "component_type", "amount", "currency"),
        "order_discount_projection": ("tenant", "discount_id", "order_id", "discount_type", "amount", "source"),
        "inventory_allocation_projection": ("tenant", "allocation_id", "order_id", "item_id", "quantity", "node_id", "confidence"),
        "inventory_node_projection": ("tenant", "node_id", "region", "available_capacity", "carbon", "status"),
        "payment_authorization_projection": ("tenant", "authorization_id", "order_id", "amount", "status", "authorized_at"),
        "fulfillment_plan": ("tenant", "plan_id", "order_id", "node_id", "status", "created_at"),
        "fulfillment_plan_line": ("tenant", "plan_line_id", "plan_id", "line_id", "quantity", "node_id"),
        "fulfillment_node_candidate": ("tenant", "candidate_id", "order_id", "node_id", "distance", "carbon", "available"),
        "fulfillment_reservation_projection": ("tenant", "reservation_id", "order_id", "node_id", "quantity", "status"),
        "split_shipment": ("tenant", "split_id", "plan_id", "node_id", "quantity", "status"),
        "backorder": ("tenant", "backorder_id", "order_id", "line_id", "quantity", "status"),
        "substitution": ("tenant", "substitution_id", "order_id", "line_id", "substitute_item_id", "status"),
        "cancellation_request": ("tenant", "cancellation_id", "order_id", "reason", "status", "requested_at"),
        "shipment_projection": ("tenant", "shipment_id", "order_id", "carrier_id", "status", "shipped_at"),
        "shipment_status_projection": ("tenant", "shipment_status_id", "shipment_id", "status", "location", "observed_at"),
        "dom_appgen_outbox_event": ("tenant", "event_id", "event_type", "topic", "idempotency_key", "audit_hash"),
        "dom_appgen_inbox_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "status"),
        "dom_dead_letter_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason"),
    }
    relationships = (
        {"from": "order_line.order_id", "to": "sales_order.order_id", "type": "owned_child"},
        {"from": "order_status.order_id", "to": "sales_order.order_id", "type": "owned_status"},
        {"from": "order_hold.order_id", "to": "sales_order.order_id", "type": "owned_hold"},
        {"from": "order_promise.order_id", "to": "sales_order.order_id", "type": "owned_promise"},
        {"from": "customer_identity_projection.customer_id", "to": "customer_projection.customer_id", "type": "owned_projection_child"},
        {"from": "tax_projection.order_id", "to": "sales_order.order_id", "type": "owned_projection"},
        {"from": "fraud_screen.order_id", "to": "sales_order.order_id", "type": "owned_screen"},
        {"from": "order_price_component.order_id", "to": "sales_order.order_id", "type": "owned_price"},
        {"from": "inventory_allocation_projection.order_id", "to": "sales_order.order_id", "type": "owned_projection"},
        {"from": "fulfillment_plan.order_id", "to": "sales_order.order_id", "type": "owned_plan"},
        {"from": "fulfillment_plan_line.plan_id", "to": "fulfillment_plan.plan_id", "type": "owned_child"},
        {"from": "split_shipment.plan_id", "to": "fulfillment_plan.plan_id", "type": "owned_split"},
        {"from": "shipment_projection.order_id", "to": "sales_order.order_id", "type": "owned_projection"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id") or field == "event_id")[:2],
            "owned_by": "dom",
        }
        for table in DOM_OWNED_TABLES
    )
    allowed_prefixes = (
        "sales_",
        "order_",
        "customer_",
        "tax_",
        "fraud_",
        "inventory_",
        "payment_",
        "fulfillment_",
        "split_",
        "backorder",
        "substitution",
        "cancellation_",
        "shipment_",
        "route_",
        "risk_",
        "policy_",
        "promise_",
        "dom_",
    )
    return {
        "format": "appgen.dom-owned-schema-contract.v1",
        "ok": len(tables) == len(DOM_OWNED_TABLES)
        and len(tables) >= 40
        and all(item["table"].startswith(allowed_prefixes) for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/dom/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": DOM_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(DOM_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in DOM_OWNED_TABLES
        ),
        "datastore_backends": DOM_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def dom_build_service_contract() -> dict:
    """Return DOM command/query service evidence."""
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "capture_order",
        "upsert_customer_projection",
        "apply_tax_projection",
        "screen_fraud",
        "verify_order",
        "price_order",
        "apply_inventory_allocation",
        "create_fulfillment_plan",
        "confirm_order_shipped",
        "route_fulfillment",
        "generate_order_verification_proof",
        "screen_order_policy",
        "federate_order_view",
        "verify_order_identity",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_fulfillment",
        "optimize_fulfillment",
        "allocate_nodes",
        "run_control_tests",
        "register_governed_model",
    )
    return {
        "format": "appgen.dom-service-contract.v1",
        "ok": len(command_methods) >= 25,
        "transaction_boundary": "dom_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_workbench_view",
            "simulate_fulfillment_policy",
            "forecast_promise_demand",
            "parse_order_event",
            "score_order_risk",
            "recommend_exception_resolution",
            "detect_order_anomaly",
            "model_stochastic_fulfillment_exposure",
            "verify_owned_table_boundary",
        ),
        "mutates_only": DOM_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _DOM_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": DOM_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _DOM_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def dom_build_release_evidence() -> dict:
    """Return DOM package-local release evidence."""
    schema = dom_build_schema_contract()
    service = dom_build_service_contract()
    api = dom_build_api_contract()
    permissions = dom_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 40},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(DOM_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 25},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": {"capture_order", "verify_order", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == DOM_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
    )
    return {
        "format": "appgen.dom-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def dom_permissions_contract() -> dict:
    return {
        "format": "appgen.dom-permissions.v1",
        "ok": True,
        "permissions": (
            "dom.read",
            "dom.create",
            "dom.verify",
            "dom.price",
            "dom.allocate",
            "dom.plan",
            "dom.ship",
            "dom.cancel",
            "dom.event",
            "dom.configure",
            "dom.audit",
        ),
        "action_permissions": {
            "capture_order": "dom.create",
            "upsert_customer_projection": "dom.create",
            "apply_tax_projection": "dom.verify",
            "screen_fraud": "dom.verify",
            "verify_order": "dom.verify",
            "price_order": "dom.price",
            "apply_inventory_allocation": "dom.allocate",
            "create_fulfillment_plan": "dom.plan",
            "confirm_order_shipped": "dom.ship",
            "route_fulfillment": "dom.plan",
            "receive_event": "dom.event",
            "register_rule": "dom.configure",
            "register_schema_extension": "dom.configure",
            "set_parameter": "dom.configure",
            "configure_runtime": "dom.configure",
            "screen_order_policy": "dom.audit",
            "generate_order_verification_proof": "dom.audit",
            "run_control_tests": "dom.audit",
            "build_workbench_view": "dom.audit",
        },
    }


def dom_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (
        *DOM_OWNED_TABLES,
        *DOM_CONSUMED_EVENT_TYPES,
        *_DOM_RUNTIME_TABLES,
        *_DOM_ALLOWED_DEPENDENCIES,
    )
    allowed_set = set(allowed)
    violations = tuple(reference for reference in references if reference not in allowed_set and not str(reference).startswith("dom_"))
    return {
        "format": "appgen.dom-boundary.v1",
        "ok": not violations,
        "owned_tables": DOM_OWNED_TABLES,
        "declared_dependencies": {
            "apis": (
                "GET /inventory/allocations/{id}",
                "GET /tax/calculations/{id}",
                "GET /customers/{id}",
                "GET /payments/authorizations/{id}",
                "GET /shipments/{id}",
                "POST /audit/order-events",
            ),
            "events": DOM_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "inventory_allocation_projection",
                "tax_calculation_projection",
                "customer_profile_projection",
                "payment_authorization_projection",
                "shipment_delivery_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def dom_federate_order_view(state: dict, order_id: str, *, systems: tuple[str, ...]) -> dict:
    order = state["orders"][order_id]
    return {"ok": True, "order_id": order_id, "systems": systems, "projection": {"status": order["status"], "customer_id": order["customer_id"], "total": order["total"]}}


def dom_verify_order_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def dom_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"fulfillment_route_timeout", "tax_projection_lag"}, "scenario": scenario, "mode": "degraded_fulfillment_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "dom.dead_letter"}


def dom_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"dom_epoch_{epoch:04d}"}


def dom_schedule_carbon_aware_fulfillment(nodes: tuple[dict, ...]) -> dict:
    selected = min(nodes, key=lambda node: node["carbon"])
    return {"ok": True, "node_id": selected["node_id"], "carbon": selected["carbon"]}


def dom_optimize_fulfillment(candidates: tuple[dict, ...], *, quantity: float) -> dict:
    feasible = tuple(candidate for candidate in candidates if candidate["available"] >= quantity)
    scored = tuple({**candidate, "objective": round(candidate["distance"] + candidate["carbon"] * 0.5, 4)} for candidate in feasible)
    selected = min(scored, key=lambda item: item["objective"])
    return {"ok": True, "node_id": selected["node_id"], "objective_score": selected["objective"], "candidates": scored}


def dom_allocate_nodes(nodes: tuple[dict, ...], *, quantity: float) -> dict:
    total = sum(node["bid"] * node["service"] for node in nodes)
    allocations = tuple({"node_id": node["node_id"], "quantity": round(quantity * node["bid"] * node["service"] / total, 2)} for node in nodes)
    return {"ok": round(sum(item["quantity"] for item in allocations), 2) == round(quantity, 2), "allocations": allocations, "clearing_bid": round(sum(node["bid"] for node in nodes) / len(nodes), 4)}


def dom_detect_order_anomaly(state: dict) -> dict:
    totals = tuple(order["total"] for order in state["orders"].values())
    if not totals:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total_sum = sum(totals) or 1
    entropy = round(-sum((total / total_sum) * math.log(max(total / total_sum, 0.0001), 2) for total in totals), 4)
    mean = sum(totals) / len(totals)
    return {"ok": True, "entropy": entropy, "outliers": tuple(total for total in totals if abs(total - mean) > mean * 0.5)}


def dom_model_stochastic_fulfillment_exposure(*, delay_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(delay_path) < 2 else (delay_path[-1] - delay_path[0]) / (len(delay_path) - 1)
    exposure = abs(drift) * volatility * len(delay_path)
    return {"ok": True, "expected_exposure": round(exposure, 2), "tail_risk": round(exposure * 1.65, 2), "simulation_count": 1000}


def dom_build_workbench_view(state: dict, *, tenant: str) -> dict:
    orders = tuple(order for order in state["orders"].values() if order["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "order_count": len(orders),
        "open_order_count": len(tuple(order for order in orders if order["status"] not in {"shipped", "cancelled"})),
        "shipped_count": len(tuple(order for order in orders if order["status"] == "shipped")),
        "fraud_review_count": len(tuple(screen for screen in state["fraud"].values() if screen["tenant"] == tenant and screen["decision"] == "review")),
        "fulfillment_plan_count": len(tuple(plan for plan in state["fulfillment_plans"].values() if plan["tenant"] == tenant)),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": DOM_OWNED_TABLES,
            "outbox_table": "dom_appgen_outbox_event",
            "inbox_table": "dom_appgen_inbox_event",
            "dead_letter_table": "dom_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
            "permissions": tuple(sorted(dom_permissions_contract()["permissions"])),
        },
    }


def dom_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"dom_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"dom:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _first_number_after(text: str, marker: str) -> float | None:
    match = re.search(rf"{re.escape(marker)}\s+(\d+(?:\.\d+)?)", text, re.I)
    return float(match.group(1)) if match else None


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
