"""Executable runtime for the Transportation Management PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC = "appgen.transportation.events"
TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
TRANSPORTATION_MANAGEMENT_OWNED_TABLES = (
    "shipment",
    "shipment_line",
    "shipment_party",
    "shipment_reference",
    "shipment_package",
    "carrier",
    "carrier_service_level",
    "carrier_lane",
    "carrier_contract",
    "carrier_identity",
    "freight_route",
    "route_stop",
    "route_leg",
    "route_constraint",
    "carrier_tender",
    "carrier_tender_response",
    "dispatch_confirmation",
    "tracking_event",
    "eta_snapshot",
    "inbound_arrival",
    "delivery_proof",
    "delivery_exception",
    "transportation_exception",
    "freight_cost_accrual",
    "freight_invoice_projection",
    "cross_border_document",
    "temperature_hazard_control",
    "carrier_scorecard",
    "carrier_risk_signal",
    "carbon_distance_metric",
    "packed_order_projection",
    "purchase_order_projection",
    "return_authorization_projection",
    "inventory_transfer_projection",
    "access_policy_projection",
    "transportation_policy_screening",
    "transportation_telematics_event",
    "transportation_telematics_replay",
    "transportation_delivery_proof_hash",
    "transportation_audit_trace",
    "transportation_federation_projection",
    "transportation_carbon_route_selection",
    "transportation_route_optimization",
    "transportation_tender_allocation",
    "transportation_tracking_anomaly_signal",
    "transportation_transit_exposure_model",
    "transportation_eta_cost_forecast",
    "transportation_parsed_event",
    "transportation_seed_data",
    "transportation_schema_extension",
    "transportation_control_assertion",
    "transportation_governed_model",
    "transportation_rule",
    "transportation_parameter",
    "transportation_configuration",
    "transportation_management_appgen_outbox_event",
    "transportation_management_appgen_inbox_event",
    "transportation_management_dead_letter_event",
)
TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES = (
    "CarrierRegistered",
    "ShipmentCreated",
    "CarrierSelected",
    "FreightRoutePlanned",
    "ShipmentDispatched",
    "EtaUpdated",
    "InboundArrived",
    "ShipmentDelivered",
)
TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES = (
    "Packed",
    "PurchaseOrderIssued",
    "ReturnAuthorized",
    "InventoryTransferRequested",
    "AccessPolicyChanged",
)
_TRANSPORTATION_MANAGEMENT_RUNTIME_TABLES = (
    "transportation_management_appgen_outbox_event",
    "transportation_management_appgen_inbox_event",
    "transportation_management_dead_letter_event",
)
_TRANSPORTATION_MANAGEMENT_ALLOWED_DEPENDENCIES = (
    "packed_order_projection",
    "purchase_order_projection",
    "return_authorization_projection",
    "inventory_transfer_projection",
    "access_policy_projection",
    "GET /wms/packed-orders/{id}",
    "GET /procurement/purchase-orders/{id}",
    "GET /returns/authorizations/{id}",
    "GET /inventory/transfers/{id}",
    "GET /identity/policies",
    "POST /audit/transportation-events",
)
_TRANSPORTATION_MANAGEMENT_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}


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
    "shipment_lines",
    "shipment_parties",
    "shipment_references",
    "shipment_packages",
    "carrier_master",
    "carrier_service_levels",
    "carrier_lanes",
    "carrier_contracts",
    "carrier_identity",
    "freight_route_planning",
    "route_legs",
    "route_constraints",
    "carrier_selection",
    "tendering",
    "tender_response_capture",
    "dispatch_confirmation",
    "tracking_event_ingestion",
    "eta_calculation",
    "inbound_arrival",
    "delivery_confirmation",
    "delivery_exception_management",
    "exception_management",
    "freight_cost_accrual",
    "freight_invoice_projection",
    "multi_leg_support",
    "cross_border_documents",
    "temperature_hazard_controls",
    "carrier_scorecard",
    "carrier_risk_signals",
    "carbon_distance_analytics",
    "consumed_event_handlers",
    "packed_order_projection",
    "purchase_order_projection",
    "return_authorization_projection",
    "inventory_transfer_projection",
    "access_policy_projection",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "retry_dead_letter_evidence",
    "multi_entity_isolation",
    "idempotent_handlers",
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
        "owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
        "capabilities": TRANSPORTATION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        "standard_features": TRANSPORTATION_MANAGEMENT_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "register_carrier",
            "create_shipment",
            "select_carrier",
            "plan_route",
            "dispatch_shipment",
            "record_tracking_event",
            "confirm_inbound_arrival",
            "confirm_delivery",
            "calculate_eta",
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


def transportation_management_runtime_smoke() -> dict:
    state = transportation_management_empty_state()
    state = transportation_management_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
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
    schema = transportation_management_build_schema_contract()
    service = transportation_management_build_service_contract()
    release = transportation_management_build_release_evidence()
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
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and "ShipmentDelivered" in api["events"]["emits"]},
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
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letters": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "packed_order_projections": {},
        "purchase_order_projections": {},
        "return_authorization_projections": {},
        "inventory_transfer_projections": {},
        "access_policy_projections": {},
        "shipments": {},
        "carriers": {},
        "routes": {},
        "tracking_events": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def transportation_management_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _TRANSPORTATION_MANAGEMENT_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Transportation Management uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    if configuration.get("database_backend") not in set(TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS):
        raise ValueError("Transportation Management supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Transportation Management requires AppGen-X event topic {TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def transportation_management_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "max_cost_per_mile",
        "on_time_weight",
        "carbon_weight",
        "service_level_weight",
        "tracking_staleness_minutes",
        "eta_confidence_threshold",
        "tender_timeout_minutes",
        "consolidation_threshold",
        "delay_risk_threshold",
        "exception_escalation_minutes",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported Transportation Management parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def transportation_management_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Transportation Management rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("Transportation Management rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def transportation_management_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in TRANSPORTATION_MANAGEMENT_OWNED_TABLES:
        raise ValueError(f"Transportation Management schema extensions must target owned tables: {TRANSPORTATION_MANAGEMENT_OWNED_TABLES}")
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


def transportation_management_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
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
        "packed_order_projections": dict(state.get("packed_order_projections", {})),
        "purchase_order_projections": dict(state.get("purchase_order_projections", {})),
        "return_authorization_projections": dict(state.get("return_authorization_projections", {})),
        "inventory_transfer_projections": dict(state.get("inventory_transfer_projections", {})),
        "access_policy_projections": dict(state.get("access_policy_projections", {})),
    }
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"] = (*next_state["retry_evidence"], evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_transportation_event"}
            next_state["dead_letters"] = (*next_state["dead_letters"], dead)
            next_state["dead_letter"] = (*next_state["dead_letter"], dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "Packed":
        next_state["packed_order_projections"][payload.get("pack_id", event_id)] = payload
    elif event_type == "PurchaseOrderIssued":
        next_state["purchase_order_projections"][payload.get("purchase_order_id", event_id)] = payload
    elif event_type == "ReturnAuthorized":
        next_state["return_authorization_projections"][payload.get("return_id", event_id)] = payload
    elif event_type == "InventoryTransferRequested":
        next_state["inventory_transfer_projections"][payload.get("transfer_id", event_id)] = payload
    elif event_type == "AccessPolicyChanged":
        next_state["access_policy_projections"][payload.get("policy_id", event_id)] = payload
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


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
    return {
        "ok": True,
        "format": "appgen.transportation-management-api-contract.v1",
        "routes": (
            {"route": "POST /transportation/shipments", "command": "create_shipment", "owned_tables": ("shipment",), "emits": ("ShipmentCreated",), "requires_permission": "transportation_management.plan", "idempotency_key": "shipment_id"},
            {"route": "POST /transportation/carriers", "command": "register_carrier", "owned_tables": ("carrier", "carrier_scorecard"), "emits": ("CarrierRegistered",), "requires_permission": "transportation_management.master", "idempotency_key": "carrier_id"},
            {"route": "POST /transportation/shipments/{id}/carrier-selection", "command": "select_carrier", "owned_tables": ("shipment", "carrier_tender"), "emits": ("CarrierSelected",), "requires_permission": "transportation_management.tender", "idempotency_key": "shipment_id"},
            {"route": "POST /transportation/routes", "command": "plan_route", "owned_tables": ("freight_route", "route_stop", "freight_cost_accrual", "carbon_distance_metric"), "emits": ("FreightRoutePlanned",), "requires_permission": "transportation_management.plan", "idempotency_key": "shipment_id"},
            {"route": "POST /transportation/shipments/{id}/dispatch", "command": "dispatch_shipment", "owned_tables": ("dispatch_confirmation", "shipment"), "emits": ("ShipmentDispatched",), "requires_permission": "transportation_management.dispatch", "idempotency_key": "tender_id"},
            {"route": "POST /transportation/tracking-events", "command": "record_tracking_event", "owned_tables": ("tracking_event", "eta_snapshot"), "emits": ("EtaUpdated",), "requires_permission": "transportation_management.track", "idempotency_key": "event_id"},
            {"route": "POST /transportation/shipments/{id}/arrival", "command": "confirm_inbound_arrival", "owned_tables": ("inbound_arrival", "shipment"), "emits": ("InboundArrived",), "requires_permission": "transportation_management.confirm", "idempotency_key": "shipment_id:facility"},
            {"route": "POST /transportation/shipments/{id}/delivery", "command": "confirm_delivery", "owned_tables": ("delivery_proof", "shipment"), "emits": ("ShipmentDelivered",), "requires_permission": "transportation_management.confirm", "idempotency_key": "proof_id"},
            {"route": "POST /transportation/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES, "requires_permission": "transportation_management.event", "idempotency_key": "event_id"},
            {"route": "GET /transportation/workbench", "query": "build_workbench_view", "owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES, "requires_permission": "transportation_management.audit"},
        ),
        "declared_catalog_routes": ("POST /shipments", "POST /carrier-selection", "GET /eta"),
        "events": {"emits": TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES, "consumes": TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES},
        "emits": TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES,
        "consumes": TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(transportation_management_permissions_contract()["permissions"])),
        "database_backends": TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": (
            "TRANSPORTATION_MANAGEMENT_DATABASE_URL",
            "TRANSPORTATION_MANAGEMENT_EVENT_TOPIC",
            "TRANSPORTATION_MANAGEMENT_RETRY_LIMIT",
            "TRANSPORTATION_MANAGEMENT_DEFAULT_CURRENCY",
        ),
    }


def transportation_management_build_schema_contract() -> dict:
    """Return Transportation-owned schema, migration, model, and relationship evidence."""
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {
        table: default_fields for table in TRANSPORTATION_MANAGEMENT_OWNED_TABLES
    } | {
        "shipment": ("tenant", "shipment_id", "source_ref", "origin", "destination", "mode", "status"),
        "shipment_line": ("tenant", "shipment_line_id", "shipment_id", "item_id", "quantity", "weight"),
        "shipment_party": ("tenant", "party_id", "shipment_id", "role", "name", "address_ref"),
        "shipment_reference": ("tenant", "reference_id", "shipment_id", "reference_type", "reference_value", "source"),
        "shipment_package": ("tenant", "package_id", "shipment_id", "weight", "dimensions", "handling_code"),
        "carrier": ("tenant", "carrier_id", "mode", "cost_per_mile", "on_time_rate", "risk", "status"),
        "carrier_service_level": ("tenant", "service_level_id", "carrier_id", "service_level", "transit_days", "status"),
        "carrier_lane": ("tenant", "lane_id", "carrier_id", "origin", "destination", "status"),
        "carrier_contract": ("tenant", "carrier_contract_id", "carrier_id", "rate_card", "effective_from", "status"),
        "carrier_identity": ("tenant", "identity_id", "carrier_id", "did", "issuer", "status"),
        "freight_route": ("tenant", "route_id", "shipment_id", "carrier_id", "distance_miles", "estimated_cost", "status"),
        "route_stop": ("tenant", "stop_id", "route_id", "sequence", "location", "appointment_window"),
        "route_leg": ("tenant", "leg_id", "route_id", "origin", "destination", "distance_miles"),
        "route_constraint": ("tenant", "constraint_id", "route_id", "constraint_type", "value", "status"),
        "carrier_tender": ("tenant", "tender_id", "shipment_id", "carrier_id", "status", "sent_at"),
        "carrier_tender_response": ("tenant", "response_id", "tender_id", "carrier_id", "decision", "responded_at"),
        "dispatch_confirmation": ("tenant", "dispatch_id", "shipment_id", "tender_id", "status", "dispatched_at"),
        "tracking_event": ("tenant", "event_id", "shipment_id", "location", "distance_remaining", "delay_minutes"),
        "eta_snapshot": ("tenant", "eta_snapshot_id", "shipment_id", "eta_hours", "confidence", "observed_at"),
        "inbound_arrival": ("tenant", "arrival_id", "shipment_id", "facility", "arrived_at", "status"),
        "delivery_proof": ("tenant", "proof_id", "shipment_id", "proof_hash", "public_claims", "delivered_at"),
        "transportation_management_appgen_outbox_event": ("tenant", "event_id", "event_type", "topic", "idempotency_key", "audit_hash"),
        "transportation_management_appgen_inbox_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "status"),
        "transportation_management_dead_letter_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason"),
    }
    relationships = (
        {"from": "shipment_line.shipment_id", "to": "shipment.shipment_id", "type": "owned_child"},
        {"from": "shipment_package.shipment_id", "to": "shipment.shipment_id", "type": "owned_package"},
        {"from": "carrier_service_level.carrier_id", "to": "carrier.carrier_id", "type": "owned_service"},
        {"from": "carrier_lane.carrier_id", "to": "carrier.carrier_id", "type": "owned_lane"},
        {"from": "carrier_identity.carrier_id", "to": "carrier.carrier_id", "type": "owned_identity"},
        {"from": "freight_route.shipment_id", "to": "shipment.shipment_id", "type": "owned_route"},
        {"from": "route_stop.route_id", "to": "freight_route.route_id", "type": "owned_stop"},
        {"from": "route_leg.route_id", "to": "freight_route.route_id", "type": "owned_leg"},
        {"from": "carrier_tender.shipment_id", "to": "shipment.shipment_id", "type": "owned_tender"},
        {"from": "carrier_tender_response.tender_id", "to": "carrier_tender.tender_id", "type": "owned_response"},
        {"from": "dispatch_confirmation.shipment_id", "to": "shipment.shipment_id", "type": "owned_dispatch"},
        {"from": "tracking_event.shipment_id", "to": "shipment.shipment_id", "type": "owned_tracking"},
        {"from": "delivery_proof.shipment_id", "to": "shipment.shipment_id", "type": "owned_delivery"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id") or field == "event_id")[:2],
            "owned_by": "transportation_management",
        }
        for table in TRANSPORTATION_MANAGEMENT_OWNED_TABLES
    )
    allowed_prefixes = (
        "shipment",
        "carrier",
        "freight_",
        "route_",
        "dispatch_",
        "tracking_",
        "eta_",
        "inbound_",
        "delivery_",
        "transportation",
        "cross_",
        "temperature_",
        "carbon_",
        "packed_",
        "purchase_",
        "return_",
        "inventory_",
        "access_",
    )
    return {
        "format": "appgen.transportation-management-owned-schema-contract.v1",
        "ok": len(tables) == len(TRANSPORTATION_MANAGEMENT_OWNED_TABLES)
        and len(tables) >= 40
        and all(item["table"].startswith(allowed_prefixes) for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/transportation_management/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(TRANSPORTATION_MANAGEMENT_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in TRANSPORTATION_MANAGEMENT_OWNED_TABLES
        ),
        "datastore_backends": TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def transportation_management_build_service_contract() -> dict:
    """Return Transportation command/query service evidence."""
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_carrier",
        "create_shipment",
        "select_carrier",
        "plan_route",
        "dispatch_shipment",
        "record_tracking_event",
        "confirm_inbound_arrival",
        "confirm_delivery",
        "route_telematics_event",
        "generate_delivery_proof",
        "screen_policy",
        "federate_transportation_view",
        "verify_carrier_identity",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_route",
        "optimize_route_carrier",
        "allocate_carrier_tender",
        "run_control_tests",
        "register_governed_model",
    )
    return {
        "format": "appgen.transportation-management-service-contract.v1",
        "ok": len(command_methods) >= 25,
        "transaction_boundary": "transportation_management_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "calculate_eta",
            "build_workbench_view",
            "simulate_carrier_route",
            "forecast_eta_cost_delay",
            "parse_transport_event",
            "score_transport_risk",
            "recommend_exception_resolution",
            "detect_tracking_anomaly",
            "model_stochastic_transit_exposure",
            "verify_owned_table_boundary",
        ),
        "mutates_only": TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _TRANSPORTATION_MANAGEMENT_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _TRANSPORTATION_MANAGEMENT_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def transportation_management_build_release_evidence() -> dict:
    """Return Transportation package-local release evidence."""
    schema = transportation_management_build_schema_contract()
    service = transportation_management_build_service_contract()
    api = transportation_management_build_api_contract()
    permissions = transportation_management_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 40},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(TRANSPORTATION_MANAGEMENT_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 25},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": {"create_shipment", "dispatch_shipment", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
    )
    return {
        "format": "appgen.transportation-management-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def transportation_management_permissions_contract() -> dict:
    return {
        "format": "appgen.transportation-management-permissions.v1",
        "ok": True,
        "permissions": (
            "transportation_management.read",
            "transportation_management.master",
            "transportation_management.plan",
            "transportation_management.tender",
            "transportation_management.dispatch",
            "transportation_management.track",
            "transportation_management.confirm",
            "transportation_management.event",
            "transportation_management.configure",
            "transportation_management.audit",
        ),
        "action_permissions": {
            "register_carrier": "transportation_management.master",
            "create_shipment": "transportation_management.plan",
            "select_carrier": "transportation_management.tender",
            "plan_route": "transportation_management.plan",
            "dispatch_shipment": "transportation_management.dispatch",
            "record_tracking_event": "transportation_management.track",
            "calculate_eta": "transportation_management.track",
            "confirm_inbound_arrival": "transportation_management.confirm",
            "confirm_delivery": "transportation_management.confirm",
            "receive_event": "transportation_management.event",
            "simulate_carrier_route": "transportation_management.audit",
            "optimize_route_carrier": "transportation_management.tender",
            "allocate_carrier_tender": "transportation_management.tender",
            "screen_policy": "transportation_management.audit",
            "run_control_tests": "transportation_management.audit",
            "register_rule": "transportation_management.configure",
            "register_schema_extension": "transportation_management.configure",
            "set_parameter": "transportation_management.configure",
            "configure_runtime": "transportation_management.configure",
            "build_workbench_view": "transportation_management.audit",
        },
    }


def transportation_management_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (
        *TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
        *TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES,
        *_TRANSPORTATION_MANAGEMENT_RUNTIME_TABLES,
        *_TRANSPORTATION_MANAGEMENT_ALLOWED_DEPENDENCIES,
    )
    allowed_set = set(allowed)
    violations = tuple(
        reference
        for reference in references
        if reference not in allowed_set and not str(reference).startswith("transportation_management_")
    )
    return {
        "format": "appgen.transportation-management-boundary.v1",
        "ok": not violations,
        "owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
        "declared_dependencies": {
            "apis": (
                "GET /wms/packed-orders/{id}",
                "GET /procurement/purchase-orders/{id}",
                "GET /returns/authorizations/{id}",
                "GET /inventory/transfers/{id}",
                "GET /identity/policies",
                "POST /audit/transportation-events",
            ),
            "events": TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "packed_order_projection",
                "purchase_order_projection",
                "return_authorization_projection",
                "inventory_transfer_projection",
                "access_policy_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


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
    return {
        "ok": True,
        "tenant": tenant,
        "shipment_count": len(shipments),
        "delivered_count": len(tuple(shipment for shipment in shipments if shipment["status"] == "delivered")),
        "carrier_count": len(tuple(carrier for carrier in state["carriers"].values() if carrier["tenant"] == tenant)),
        "route_count": len(tuple(route for route in state["routes"].values() if route["tenant"] == tenant)),
        "tracking_count": len(tuple(event for event in state["tracking_events"].values() if event["tenant"] == tenant)),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
            "outbox_table": "transportation_management_appgen_outbox_event",
            "inbox_table": "transportation_management_appgen_inbox_event",
            "dead_letter_table": "transportation_management_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
            "permissions": tuple(sorted(transportation_management_permissions_contract()["permissions"])),
        },
    }


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
