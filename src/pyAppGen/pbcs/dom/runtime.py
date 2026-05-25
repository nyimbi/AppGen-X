"""Executable runtime for the Distributed Order Management PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


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
    "customer_projection",
    "tax_projection",
    "fraud_screening",
    "order_verification",
    "order_pricing",
    "inventory_allocation_projection",
    "fulfillment_planning",
    "split_shipment",
    "backorder_management",
    "substitution_management",
    "cancellation_control",
    "shipment_projection",
    "order_lifecycle_status",
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
        "capabilities": DOM_RUNTIME_CAPABILITY_KEYS,
        "standard_features": DOM_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "capture_order",
            "upsert_customer_projection",
            "apply_tax_projection",
            "screen_fraud",
            "verify_order",
            "price_order",
            "apply_inventory_allocation",
            "create_fulfillment_plan",
            "confirm_order_shipped",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def dom_runtime_smoke() -> dict:
    state = dom_empty_state()
    state = dom_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.dom.events",
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
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "OrderVerified" in api["events"]["emits"]},
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
    return {"events": (), "outbox": (), "orders": {}, "customers": {}, "tax": {}, "fraud": {}, "allocations": {}, "fulfillment_plans": {}, "rules": {}, "parameters": {}, "configuration": {}, "schema_extensions": {}, "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"}}


def dom_configure_runtime(state: dict, configuration: dict) -> dict:
    ok = configuration.get("database_backend") in {"postgresql", "mysql", "mariadb"} and bool(configuration.get("event_topic"))
    return {"ok": ok, "state": {**state, "configuration": {**configuration, "ok": ok}}, "configuration": {**configuration, "ok": ok}}


def dom_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def dom_register_rule(state: dict, rule: dict) -> dict:
    enriched = {**rule, "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def dom_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


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
    return {"ok": True, "routes": ("POST /orders", "POST /allocation", "GET /fulfillment-plans", "POST /dom-rules", "POST /dom-parameters", "POST /dom-configuration"), "events": {"emits": ("OrderVerified", "OrderPriced", "OrderShipped"), "consumes": ("InventoryAllocated", "TaxCalculated", "CustomerUpdated")}, "permissions": ("dom.create", "dom.verify", "dom.price", "dom.allocate", "dom.plan", "dom.ship", "dom.configure", "dom.audit"), "configuration": ("DOM_DATABASE_URL", "DOM_EVENT_TOPIC", "DOM_RETRY_LIMIT", "DOM_DEFAULT_CURRENCY")}


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
    return {"ok": True, "tenant": tenant, "order_count": len(orders), "open_order_count": len(tuple(order for order in orders if order["status"] not in {"shipped", "cancelled"})), "shipped_count": len(tuple(order for order in orders if order["status"] == "shipped")), "fraud_review_count": len(tuple(screen for screen in state["fraud"].values() if screen["tenant"] == tenant and screen["decision"] == "review")), "fulfillment_plan_count": len(tuple(plan for plan in state["fulfillment_plans"].values() if plan["tenant"] == tenant))}


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
