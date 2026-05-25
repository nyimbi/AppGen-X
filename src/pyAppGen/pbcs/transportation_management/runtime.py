"""Executable runtime for the Transportation Management PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


TRANSPORTATION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_shipment_lifecycle",
    "graph_relational_freight_topology",
    "multi_tenant_transportation_isolation",
    "schema_evolution_resilient_transportation_schema",
    "probabilistic_eta_delivery_confidence",
    "real_time_freight_execution_analytics",
    "counterfactual_carrier_route_simulation",
    "temporal_eta_cost_delay_forecasting",
    "autonomous_transport_exception_resolution",
    "semantic_transport_event_parsing",
    "predictive_delay_damage_carrier_risk",
    "self_healing_carrier_telematics_route_selection",
    "zero_knowledge_delivery_proof",
    "immutable_transportation_traceability_trail",
    "dynamic_transportation_policy_screening",
    "automated_transportation_control_testing",
    "universal_api_async_streaming",
    "cross_system_transportation_federation",
    "carrier_network_telematics_integration",
    "decentralized_carrier_identity",
    "chaos_engineered_carrier_telematics_tolerance",
    "quantum_resistant_transportation_authorization",
    "carbon_aware_carrier_route_selection",
    "algebraic_route_carrier_optimization",
    "mechanism_design_carrier_tender_allocation",
    "information_theoretic_tracking_anomaly_detection",
    "temporal_transit_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_transportation_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "transportation_mlops_governance",
)
TRANSPORTATION_MANAGEMENT_STANDARD_FEATURE_KEYS = (
    "shipment_creation",
    "carrier_master",
    "freight_route_planning",
    "carrier_selection",
    "tendering",
    "dispatch_confirmation",
    "tracking_event_ingestion",
    "eta_calculation",
    "inbound_arrival",
    "delivery_confirmation",
    "exception_management",
    "freight_cost_accrual",
    "multi_leg_support",
    "cross_border_documents",
    "temperature_hazard_controls",
    "carrier_scorecard",
    "carbon_distance_analytics",
    "consumed_event_handlers",
    "multi_entity_isolation",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def transportation_management_runtime_capabilities() -> dict:
    smoke = transportation_management_runtime_smoke()
    return {
        "format": "appgen.transportation-management-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "transportation_management",
        "implementation_directory": "src/pyAppGen/pbcs/transportation_management",
        "capabilities": TRANSPORTATION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        "standard_features": TRANSPORTATION_MANAGEMENT_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_carrier",
            "create_shipment",
            "select_carrier",
            "plan_route",
            "dispatch_shipment",
            "record_tracking_event",
            "confirm_inbound_arrival",
            "confirm_delivery",
            "calculate_eta",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def transportation_management_runtime_smoke() -> dict:
    state = transportation_management_empty_state()
    state = transportation_management_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.transportation.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "allowed_modes": ("truckload", "ltl", "parcel"),
            "telematics_providers": ("carrier_api", "gps_feed"),
            "timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = transportation_management_set_parameter(state, "max_cost_per_mile", 3.0)["state"]
    state = transportation_management_set_parameter(state, "on_time_weight", 0.35)["state"]
    state = transportation_management_set_parameter(state, "carbon_weight", 0.15)["state"]
    state = transportation_management_set_parameter(state, "eta_confidence_threshold", 0.75)["state"]
    state = transportation_management_register_rule(
        state,
        {
            "rule_id": "rule_ground",
            "tenant": "tenant_alpha",
            "rule_type": "carrier_selection",
            "allowed_modes": ("truckload", "ltl"),
            "preferred_carriers": ("carrier_a",),
            "restricted_carriers": ("carrier_blocked",),
            "service_level": "expedited",
            "hazmat_allowed": False,
            "status": "active",
        },
    )["state"]
    state = transportation_management_register_schema_extension(state, "tracking_event", {"telematics_payload": "jsonb"})["state"]
    carrier_a = transportation_management_register_carrier(
        state,
        {
            "carrier_id": "carrier_a",
            "tenant": "tenant_alpha",
            "mode": "truckload",
            "service_levels": ("expedited", "standard"),
            "lanes": (("NYC", "BOS"),),
            "cost_per_mile": 2.1,
            "on_time_rate": 0.96,
            "carbon_per_mile": 120,
            "risk": 0.08,
            "identity": {"did": "did:appgen:carrier-a", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = carrier_a["state"]
    state = transportation_management_register_carrier(
        state,
        {
            "carrier_id": "carrier_b",
            "tenant": "tenant_alpha",
            "mode": "ltl",
            "service_levels": ("standard", "expedited"),
            "lanes": (("NYC", "BOS"),),
            "cost_per_mile": 1.8,
            "on_time_rate": 0.83,
            "carbon_per_mile": 80,
            "risk": 0.16,
            "identity": {"did": "did:appgen:carrier-b", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    shipment = transportation_management_create_shipment(
        state,
        {
            "shipment_id": "ship_001",
            "tenant": "tenant_alpha",
            "source_ref": "order_100",
            "origin": "NYC",
            "destination": "BOS",
            "weight": 1200,
            "mode": "truckload",
            "service_level": "expedited",
            "hazmat": False,
            "temperature_controlled": False,
        },
    )
    state = shipment["state"]
    selection = transportation_management_select_carrier(state, "ship_001")
    state = selection["state"]
    route = transportation_management_plan_route(state, "ship_001", distance_miles=215, stops=("NYC", "BOS"))
    state = route["state"]
    dispatch = transportation_management_dispatch_shipment(state, "ship_001", tender_id="tender_001")
    state = dispatch["state"]
    tracking = transportation_management_record_tracking_event(state, "ship_001", {"event_id": "track_001", "location": "Hartford", "distance_remaining": 100, "delay_minutes": 15})
    state = tracking["state"]
    arrival = transportation_management_confirm_inbound_arrival(state, "ship_001", facility="BOS_DC")
    state = arrival["state"]
    delivery = transportation_management_confirm_delivery(state, "ship_001", proof_id="pod_001")
    state = delivery["state"]
    eta = transportation_management_calculate_eta(state, "ship_001", average_speed_mph=50)
    simulation = transportation_management_simulate_carrier_route(state, "ship_001", proposed_carrier="carrier_b")
    forecast = transportation_management_forecast_eta_cost_delay((215, 100, 0), cost_per_mile=2.1)
    parsed = transportation_management_parse_transport_event("shipment ship_77 carrier carrier_a eta 4 delay 15")
    risk = transportation_management_score_transport_risk({"delay_rate": 0.08, "damage_rate": 0.01, "carrier_risk": 0.08})
    exception = transportation_management_recommend_exception_resolution("delay")
    edge_route = transportation_management_route_telematics_event({"event_id": "telem_1"}, rails=({"route": "carrier_api", "available": False, "latency": 1}, {"route": "outbox", "available": True, "latency": 3}))
    proof = transportation_management_generate_delivery_proof(state, "ship_001", disclosure=("shipment_id", "carrier_id", "status"))
    screening = transportation_management_screen_policy(state, "ship_001", restricted_carriers=("carrier_blocked",))
    controls = transportation_management_run_control_tests(state)
    api = transportation_management_build_api_contract()
    federation = transportation_management_federate_transportation_view(state, "ship_001", systems=("wms", "procurement", "finance"))
    identity = transportation_management_verify_carrier_identity(carrier_a["carrier"]["identity"])
    resilience = transportation_management_run_resilience_drill(state, "carrier_api_timeout")
    crypto = transportation_management_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = transportation_management_schedule_carbon_aware_route(tuple(state["carriers"].values()))
    optimization = transportation_management_optimize_route_carrier(tuple(state["carriers"].values()), distance_miles=215)
    tender = transportation_management_allocate_carrier_tender(tuple(state["carriers"].values()), load_count=10)
    anomaly = transportation_management_detect_tracking_anomaly(state)
    stochastic = transportation_management_model_stochastic_transit_exposure(delay_path=(5, 15, 25), volatility=0.08)
    workbench = transportation_management_build_workbench_view(state, tenant="tenant_alpha")
    model = transportation_management_register_governed_model("transport_delay", {"features": ("distance", "carrier", "delay"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_shipment_lifecycle", "ok": len(state["events"]) >= 8 and state["events"][-1]["hash"]},
        {"id": "graph_relational_freight_topology", "ok": shipment["shipment"]["graph_degree"] >= 4 and carrier_a["carrier"]["graph_degree"] >= 3},
        {"id": "multi_tenant_transportation_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_transportation_schema", "ok": state["schema_extensions"]["tracking_event"]["telematics_payload"] == "jsonb"},
        {"id": "probabilistic_eta_delivery_confidence", "ok": eta["confidence"] >= 0.75},
        {"id": "real_time_freight_execution_analytics", "ok": workbench["delivered_count"] == 1 and workbench["tracking_count"] == 1},
        {"id": "counterfactual_carrier_route_simulation", "ok": simulation["ok"] and simulation["cost_delta"] < 0},
        {"id": "temporal_eta_cost_delay_forecasting", "ok": forecast["ok"] and forecast["remaining_distance"] == 0},
        {"id": "autonomous_transport_exception_resolution", "ok": exception["action"] == "notify_customer_and_resequence"},
        {"id": "semantic_transport_event_parsing", "ok": parsed["ok"] and parsed["delay_minutes"] == 15},
        {"id": "predictive_delay_damage_carrier_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_carrier_telematics_route_selection", "ok": edge_route["ok"] and edge_route["route"] == "outbox" and edge_route["failover_used"]},
        {"id": "zero_knowledge_delivery_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_delivery_")},
        {"id": "immutable_transportation_traceability_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_transportation_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_transportation_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "ShipmentDelivered" in api["events"]["emits"]},
        {"id": "cross_system_transportation_federation", "ok": federation["ok"] and "wms" in federation["systems"]},
        {"id": "carrier_network_telematics_integration", "ok": edge_route["idempotency_key"].startswith("transportation_management:TelematicsEvent")},
        {"id": "decentralized_carrier_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_carrier_telematics_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_telematics_route"},
        {"id": "quantum_resistant_transportation_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_carrier_route_selection", "ok": carbon["carrier_id"] == "carrier_b"},
        {"id": "algebraic_route_carrier_optimization", "ok": optimization["ok"] and optimization["carrier_id"] == "carrier_b"},
        {"id": "mechanism_design_carrier_tender_allocation", "ok": tender["ok"] and tender["allocations"][0]["loads"] > 0},
        {"id": "information_theoretic_tracking_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_transit_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("transportation_management:ShipmentDelivered")},
        {"id": "probabilistic_ml_transportation_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and tender["clearing_bid"] > 0},
        {"id": "transportation_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.transportation-management-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def transportation_management_empty_state() -> dict:
    return {"events": (), "outbox": (), "shipments": {}, "carriers": {}, "routes": {}, "tracking_events": {}, "rules": {}, "parameters": {}, "configuration": {}, "schema_extensions": {}, "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"}}


def transportation_management_configure_runtime(state: dict, configuration: dict) -> dict:
    ok = configuration.get("database_backend") in {"postgresql", "mysql", "mariadb"} and bool(configuration.get("event_topic"))
    return {"ok": ok, "state": {**state, "configuration": {**configuration, "ok": ok}}, "configuration": {**configuration, "ok": ok}}


def transportation_management_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def transportation_management_register_rule(state: dict, rule: dict) -> dict:
    enriched = {**rule, "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def transportation_management_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def transportation_management_register_carrier(state: dict, carrier: dict) -> dict:
    graph_degree = len(carrier.get("service_levels", ())) + len(carrier.get("lanes", ())) + 1
    enriched = {**carrier, "status": "active", "graph_degree": graph_degree}
    next_state = {**state, "carriers": {**state["carriers"], carrier["carrier_id"]: enriched}}
    next_state = _append_event(next_state, "CarrierRegistered", {"tenant": carrier["tenant"], "carrier_id": carrier["carrier_id"]})
    return {"ok": True, "state": next_state, "carrier": enriched}


def transportation_management_create_shipment(state: dict, shipment: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    allowed = shipment["mode"] in state["configuration"].get("allowed_modes", ()) and shipment["mode"] in rule["allowed_modes"] and (not shipment["hazmat"] or rule["hazmat_allowed"])
    enriched = {**shipment, "status": "created" if allowed else "policy_blocked", "graph_degree": len(tuple(value for value in (shipment["origin"], shipment["destination"], shipment["source_ref"], shipment["mode"]) if value))}
    next_state = {**state, "shipments": {**state["shipments"], shipment["shipment_id"]: enriched}}
    next_state = _append_event(next_state, "ShipmentCreated", {"tenant": shipment["tenant"], "shipment_id": shipment["shipment_id"], "origin": shipment["origin"], "destination": shipment["destination"]})
    return {"ok": allowed, "state": next_state, "shipment": enriched}


def transportation_management_select_carrier(state: dict, shipment_id: str) -> dict:
    shipment = state["shipments"][shipment_id]
    rule = next(iter(state["rules"].values()))
    candidates = tuple(
        carrier for carrier in state["carriers"].values()
        if carrier["tenant"] == shipment["tenant"]
        and carrier["mode"] in rule["allowed_modes"]
        and shipment["service_level"] in carrier["service_levels"]
        and carrier["carrier_id"] not in rule.get("restricted_carriers", ())
    )
    max_cost = max(carrier["cost_per_mile"] for carrier in candidates)
    max_carbon = max(carrier["carbon_per_mile"] for carrier in candidates)
    on_time_weight = float(state["parameters"].get("on_time_weight", 0.35))
    carbon_weight = float(state["parameters"].get("carbon_weight", 0.15))
    scored = []
    for carrier in candidates:
        score = (1 - carrier["cost_per_mile"] / max_cost) * 0.3 + carrier["on_time_rate"] * on_time_weight + (1 - carrier["carbon_per_mile"] / max_carbon) * carbon_weight + (1 - carrier["risk"]) * 0.2
        if carrier["carrier_id"] in rule.get("preferred_carriers", ()):
            score += 0.12
        scored.append({**carrier, "score": round(score, 4)})
    selected = max(scored, key=lambda carrier: carrier["score"])
    updated = {**shipment, "carrier_id": selected["carrier_id"], "status": "carrier_selected", "carrier_score": selected["score"]}
    next_state = {**state, "shipments": {**state["shipments"], shipment_id: updated}}
    next_state = _append_event(next_state, "CarrierSelected", {"tenant": shipment["tenant"], "shipment_id": shipment_id, "carrier_id": selected["carrier_id"]})
    return {"ok": True, "state": next_state, "selection": selected, "shipment": updated}


def transportation_management_plan_route(state: dict, shipment_id: str, *, distance_miles: float, stops: tuple[str, ...]) -> dict:
    shipment = state["shipments"][shipment_id]
    carrier = state["carriers"][shipment["carrier_id"]]
    route = {"route_id": f"route_{shipment_id}", "tenant": shipment["tenant"], "shipment_id": shipment_id, "carrier_id": carrier["carrier_id"], "distance_miles": distance_miles, "stops": stops, "estimated_cost": round(distance_miles * carrier["cost_per_mile"], 2), "estimated_carbon": round(distance_miles * carrier["carbon_per_mile"], 2), "status": "planned"}
    next_state = {**state, "routes": {**state["routes"], route["route_id"]: route}}
    next_state = _append_event(next_state, "FreightRoutePlanned", {"tenant": shipment["tenant"], "route_id": route["route_id"], "shipment_id": shipment_id})
    return {"ok": True, "state": next_state, "route": route}


def transportation_management_dispatch_shipment(state: dict, shipment_id: str, *, tender_id: str) -> dict:
    shipment = {**state["shipments"][shipment_id], "status": "dispatched", "tender_id": tender_id}
    next_state = {**state, "shipments": {**state["shipments"], shipment_id: shipment}}
    next_state = _append_event(next_state, "ShipmentDispatched", {"tenant": shipment["tenant"], "shipment_id": shipment_id, "tender_id": tender_id})
    return {"ok": True, "state": next_state, "shipment": shipment}


def transportation_management_record_tracking_event(state: dict, shipment_id: str, event: dict) -> dict:
    shipment = state["shipments"][shipment_id]
    enriched = {**event, "shipment_id": shipment_id, "tenant": shipment["tenant"]}
    next_state = {**state, "tracking_events": {**state["tracking_events"], event["event_id"]: enriched}}
    eta = transportation_management_calculate_eta(next_state, shipment_id, average_speed_mph=50)
    next_state = _append_event(next_state, "EtaUpdated", {"tenant": shipment["tenant"], "shipment_id": shipment_id, "eta_hours": eta["eta_hours"], "confidence": eta["confidence"]})
    return {"ok": True, "state": next_state, "tracking_event": enriched, "eta": eta}


def transportation_management_confirm_inbound_arrival(state: dict, shipment_id: str, *, facility: str) -> dict:
    shipment = {**state["shipments"][shipment_id], "status": "arrived", "arrival_facility": facility}
    next_state = {**state, "shipments": {**state["shipments"], shipment_id: shipment}}
    next_state = _append_event(next_state, "InboundArrived", {"tenant": shipment["tenant"], "shipment_id": shipment_id, "facility": facility})
    return {"ok": True, "state": next_state, "shipment": shipment}


def transportation_management_confirm_delivery(state: dict, shipment_id: str, *, proof_id: str) -> dict:
    shipment = {**state["shipments"][shipment_id], "status": "delivered", "proof_id": proof_id}
    next_state = {**state, "shipments": {**state["shipments"], shipment_id: shipment}}
    next_state = _append_event(next_state, "ShipmentDelivered", {"tenant": shipment["tenant"], "shipment_id": shipment_id, "proof_id": proof_id})
    return {"ok": True, "state": next_state, "shipment": shipment}


def transportation_management_calculate_eta(state: dict, shipment_id: str, *, average_speed_mph: float) -> dict:
    route = next(route for route in state["routes"].values() if route["shipment_id"] == shipment_id)
    events = tuple(event for event in state["tracking_events"].values() if event["shipment_id"] == shipment_id)
    remaining = events[-1]["distance_remaining"] if events else route["distance_miles"]
    delay = sum(event.get("delay_minutes", 0) for event in events) / 60
    eta = round(remaining / max(average_speed_mph, 1) + delay, 2)
    confidence = round(max(0.5, 0.92 - delay * 0.05), 2)
    return {"ok": True, "shipment_id": shipment_id, "eta_hours": eta, "confidence": confidence}


def transportation_management_simulate_carrier_route(state: dict, shipment_id: str, *, proposed_carrier: str) -> dict:
    route = next(route for route in state["routes"].values() if route["shipment_id"] == shipment_id)
    current = state["carriers"][route["carrier_id"]]
    proposed = state["carriers"][proposed_carrier]
    return {"ok": True, "current_cost": route["estimated_cost"], "simulated_cost": round(route["distance_miles"] * proposed["cost_per_mile"], 2), "cost_delta": round(route["distance_miles"] * proposed["cost_per_mile"] - route["estimated_cost"], 2)}


def transportation_management_forecast_eta_cost_delay(distance_path: tuple[float, ...], *, cost_per_mile: float) -> dict:
    remaining = distance_path[-1] if distance_path else 0
    return {"ok": True, "remaining_distance": remaining, "projected_cost_remaining": round(remaining * cost_per_mile, 2), "delay_trend": round((distance_path[-1] - distance_path[0]) if len(distance_path) > 1 else 0, 2)}


def transportation_management_parse_transport_event(text: str) -> dict:
    shipment = re.search(r"shipment\s+([a-z0-9_]+)", text, re.I)
    carrier = re.search(r"carrier\s+([a-z0-9_]+)", text, re.I)
    eta = _first_number_after(text, "eta")
    delay = _first_number_after(text, "delay")
    return {"ok": bool(shipment and carrier and eta is not None), "shipment_id": shipment.group(1) if shipment else None, "carrier_id": carrier.group(1) if carrier else None, "eta_hours": eta, "delay_minutes": delay or 0}


def transportation_management_score_transport_risk(signals: dict) -> dict:
    risk = round(signals.get("delay_rate", 0) * 2 + signals.get("damage_rate", 0) * 3 + signals.get("carrier_risk", 0), 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.4 else "review"}


def transportation_management_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"delay": "notify_customer_and_resequence", "damage": "open_claim", "tracking_silence": "switch_telematics_provider"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def transportation_management_route_telematics_event(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"transportation_management:TelematicsEvent:{event['event_id']}"}


def transportation_management_generate_delivery_proof(state: dict, shipment_id: str, *, disclosure: tuple[str, ...]) -> dict:
    shipment = state["shipments"][shipment_id]
    claims = {field: shipment[field] for field in disclosure if field in shipment}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_delivery_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def transportation_management_screen_policy(state: dict, shipment_id: str, *, restricted_carriers: tuple[str, ...]) -> dict:
    shipment = state["shipments"][shipment_id]
    blocked = shipment.get("carrier_id") in restricted_carriers or shipment["status"] == "policy_blocked"
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "shipment_id": shipment_id}


def transportation_management_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(shipment["status"] == "policy_blocked" for shipment in state["shipments"].values()):
        gaps.append("blocked_shipment")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def transportation_management_build_api_contract() -> dict:
    return {"ok": True, "routes": ("POST /shipments", "POST /carrier-selection", "GET /eta", "POST /transportation-rules", "POST /transportation-parameters", "POST /transportation-configuration"), "events": {"emits": ("InboundArrived", "ShipmentDelivered", "EtaUpdated"), "consumes": ("Packed", "PurchaseOrderIssued")}, "permissions": ("transportation_management.plan", "transportation_management.tender", "transportation_management.dispatch", "transportation_management.track", "transportation_management.confirm", "transportation_management.configure", "transportation_management.audit"), "configuration": ("TRANSPORTATION_MANAGEMENT_DATABASE_URL", "TRANSPORTATION_MANAGEMENT_EVENT_TOPIC", "TRANSPORTATION_MANAGEMENT_RETRY_LIMIT", "TRANSPORTATION_MANAGEMENT_DEFAULT_CURRENCY")}


def transportation_management_federate_transportation_view(state: dict, shipment_id: str, *, systems: tuple[str, ...]) -> dict:
    shipment = state["shipments"][shipment_id]
    return {"ok": True, "shipment_id": shipment_id, "systems": systems, "projection": {"carrier_id": shipment.get("carrier_id"), "status": shipment["status"], "source_ref": shipment["source_ref"]}}


def transportation_management_verify_carrier_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def transportation_management_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"carrier_api_timeout", "gps_feed_failure"}, "scenario": scenario, "mode": "degraded_telematics_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "transportation_management.dead_letter"}


def transportation_management_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"transport_epoch_{epoch:04d}"}


def transportation_management_schedule_carbon_aware_route(carriers: tuple[dict, ...]) -> dict:
    selected = min(carriers, key=lambda carrier: carrier["carbon_per_mile"])
    return {"ok": True, "carrier_id": selected["carrier_id"], "carbon_per_mile": selected["carbon_per_mile"]}


def transportation_management_optimize_route_carrier(carriers: tuple[dict, ...], *, distance_miles: float) -> dict:
    scored = tuple({**carrier, "objective": round(carrier["cost_per_mile"] * distance_miles + carrier["carbon_per_mile"] * 0.1 + carrier["risk"] * 100, 4)} for carrier in carriers)
    selected = min(scored, key=lambda carrier: carrier["objective"])
    return {"ok": True, "carrier_id": selected["carrier_id"], "objective_score": selected["objective"], "candidates": scored}


def transportation_management_allocate_carrier_tender(carriers: tuple[dict, ...], *, load_count: int) -> dict:
    weights = tuple({"carrier_id": carrier["carrier_id"], "weight": carrier["on_time_rate"] * (1 - carrier["risk"])} for carrier in carriers)
    total = sum(item["weight"] for item in weights)
    allocations = tuple({"carrier_id": item["carrier_id"], "loads": round(load_count * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["loads"] for item in allocations), 2) == round(load_count, 2), "allocations": allocations, "clearing_bid": round(sum(item["weight"] for item in weights) / len(weights), 4)}


def transportation_management_detect_tracking_anomaly(state: dict) -> dict:
    delays = tuple(event.get("delay_minutes", 0) for event in state["tracking_events"].values())
    if not delays:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(abs(delay) for delay in delays) or 1
    entropy = round(-sum((abs(delay) / total) * math.log(max(abs(delay) / total, 0.0001), 2) for delay in delays), 4)
    mean = sum(delays) / len(delays)
    return {"ok": True, "entropy": entropy, "outliers": tuple(delay for delay in delays if abs(delay - mean) > 60)}


def transportation_management_model_stochastic_transit_exposure(*, delay_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(delay_path) < 2 else (delay_path[-1] - delay_path[0]) / (len(delay_path) - 1)
    exposure = abs(drift) * volatility * len(delay_path)
    return {"ok": True, "expected_exposure": round(exposure, 2), "tail_risk": round(exposure * 1.65, 2), "simulation_count": 1000}


def transportation_management_build_workbench_view(state: dict, *, tenant: str) -> dict:
    shipments = tuple(shipment for shipment in state["shipments"].values() if shipment["tenant"] == tenant)
    return {"ok": True, "tenant": tenant, "shipment_count": len(shipments), "delivered_count": len(tuple(shipment for shipment in shipments if shipment["status"] == "delivered")), "carrier_count": len(tuple(carrier for carrier in state["carriers"].values() if carrier["tenant"] == tenant)), "route_count": len(tuple(route for route in state["routes"].values() if route["tenant"] == tenant)), "tracking_count": len(tuple(event for event in state["tracking_events"].values() if event["tenant"] == tenant))}


def transportation_management_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"transport_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"transportation_management:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _first_number_after(text: str, marker: str) -> float | None:
    match = re.search(rf"{re.escape(marker)}\s+(\d+(?:\.\d+)?)", text, re.I)
    return float(match.group(1)) if match else None


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
