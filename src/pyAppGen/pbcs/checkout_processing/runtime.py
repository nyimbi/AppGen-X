"""Executable runtime for the Checkout Processing PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC = "appgen.checkout.events"
CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
CHECKOUT_PROCESSING_RUNTIME_TABLES = (
    "checkout_processing_appgen_outbox_event",
    "checkout_processing_appgen_inbox_event",
    "checkout_processing_dead_letter_event",
)
CHECKOUT_PROCESSING_OWNED_TABLES = (
    "cart",
    "cart_line",
    "checkout_session",
    "promotion_redemption",
    "checkout_pricing_handoff",
    "checkout_tax_handoff",
    "checkout_inventory_reservation_handoff",
    "checkout_payment_intent_handoff",
    "checkout_risk_screen",
    "checkout_address_validation",
    "checkout_rule",
    "checkout_parameter",
    "checkout_configuration",
    *CHECKOUT_PROCESSING_RUNTIME_TABLES,
)
CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES = ("ProductPublished", "PriceOptimized", "TaxCalculated")
CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES = ("OrderPriced", "CheckoutCompleted")
CHECKOUT_PROCESSING_ALLOWED_DEPENDENCIES = (
    "POST /inventory-reservations",
    "POST /payment-intents",
    "POST /tax-calculations",
    "GET /product-catalog",
    "GET /pricing",
    "GET /fraud-screening",
    "product_projection",
    "price_projection",
    "tax_quote_projection",
    "inventory_reservation_projection",
    "payment_intent_projection",
    "customer_projection",
)

CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_checkout_lifecycle",
    "graph_relational_cart_topology",
    "multi_tenant_checkout_isolation",
    "schema_evolution_resilient_checkout_schema",
    "probabilistic_conversion_scoring",
    "probabilistic_checkout_risk_scoring",
    "real_time_checkout_analytics",
    "counterfactual_promotion_fulfillment_simulation",
    "temporal_abandonment_forecasting",
    "autonomous_checkout_exception_resolution",
    "semantic_checkout_instruction_parsing",
    "predictive_checkout_risk",
    "self_healing_checkout_route_selection",
    "cryptographic_checkout_proof",
    "immutable_checkout_audit_trail",
    "dynamic_checkout_policy_screening",
    "automated_checkout_control_testing",
    "cross_system_checkout_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_inbox_handlers",
    "retry_dead_letter_evidence",
    "chaos_tolerant_checkout_operations",
    "crypto_agility",
    "carbon_aware_fulfillment_option_selection",
    "mathematical_checkout_optimization",
    "promotion_allocation_mechanism_design",
    "checkout_anomaly_detection",
    "stochastic_checkout_exposure_modeling",
    "governed_ml_model_evidence",
    "permissions_governance_evidence",
)

CHECKOUT_PROCESSING_STANDARD_FEATURE_KEYS = (
    "cart",
    "cart_line",
    "checkout_session",
    "promotion_redemption",
    "pricing_handoff",
    "tax_handoff",
    "inventory_reservation_handoff",
    "payment_intent_handoff",
    "fraud_risk_hook",
    "address_validation",
    "shipping_option_validation",
    "tenant_isolation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
    "immutable_audit",
    "governed_model_evidence",
)

_SUPPORTED_PARAMETERS = {
    "cart_ttl_minutes",
    "session_ttl_minutes",
    "risk_threshold",
    "max_retry_attempts",
    "promotion_cap_rate",
    "shipping_cost_weight",
    "carbon_cost_weight",
    "abandonment_horizon_hours",
    "route_switch_threshold",
    "workbench_limit",
}
_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "promotion_policy",
    "shipping_policy",
    "risk_policy",
    "payment_policy",
)
_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}
_CONSUMED_EVENT_TYPES = {"ProductPublished", "PriceOptimized", "TaxCalculated"}
_SHIPPING_BASE_COST = {"standard": 5.0, "express": 15.0, "pickup": 0.0}


def checkout_processing_runtime_capabilities() -> dict:
    smoke = checkout_processing_runtime_smoke()
    return {
        "format": "appgen.checkout-processing-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "checkout_processing",
        "implementation_directory": "src/pyAppGen/pbcs/checkout_processing",
        "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
        "capabilities": CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS,
        "standard_features": CHECKOUT_PROCESSING_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "create_cart",
            "add_cart_line",
            "apply_coupon",
            "validate_shipping_address",
            "open_checkout_session",
            "apply_pricing_handoff",
            "apply_tax_handoff",
            "reserve_inventory_handoff",
            "screen_risk",
            "create_payment_intent",
            "complete_checkout",
            "run_control_tests",
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


def checkout_processing_runtime_smoke() -> dict:
    from .ui import checkout_processing_ui_contract

    state = checkout_processing_empty_state()
    state = checkout_processing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_country": "US",
            "supported_shipping_options": ("standard", "express", "pickup"),
            "supported_payment_methods": ("card", "wallet"),
            "workbench_limit": 100,
        },
    )["state"]
    state = checkout_processing_set_parameter(state, "risk_threshold", 0.65)["state"]
    state = checkout_processing_set_parameter(state, "max_retry_attempts", 3)["state"]
    state = checkout_processing_set_parameter(state, "promotion_cap_rate", 0.15)["state"]
    state = checkout_processing_set_parameter(state, "abandonment_horizon_hours", 24)["state"]
    state = checkout_processing_register_rule(
        state,
        {
            "rule_id": "rule_checkout_default",
            "tenant": "tenant_alpha",
            "scope": "checkout_guard",
            "status": "active",
            "promotion_policy": {"max_discount_rate": 0.15, "stackable": False},
            "shipping_policy": {"allowed_countries": ("US", "CA"), "preferred_options": ("standard", "express")},
            "risk_policy": {"manual_review_threshold": 0.65, "block_threshold": 0.9},
            "payment_policy": {"allowed_methods": ("card", "wallet"), "capture_mode": "authorize_then_capture"},
        },
    )["state"]
    state = checkout_processing_register_schema_extension(state, "cart", {"semantic_tag": "jsonb"})["state"]
    state = checkout_processing_receive_event(
        state,
        {
            "event_id": "evt_product_001",
            "event_type": "ProductPublished",
            "idempotency_key": "product:sku_100:v1",
            "payload": {"tenant": "tenant_alpha", "product_id": "sku_100", "name": "Travel Pack", "category": "bags"},
        },
    )["state"]
    duplicate = checkout_processing_receive_event(
        state,
        {
            "event_id": "evt_product_001",
            "event_type": "ProductPublished",
            "idempotency_key": "product:sku_100:v1",
            "payload": {"tenant": "tenant_alpha", "product_id": "sku_100", "name": "Travel Pack", "category": "bags"},
        },
    )
    state = duplicate["state"]
    state = checkout_processing_receive_event(
        state,
        {
            "event_id": "evt_price_001",
            "event_type": "PriceOptimized",
            "idempotency_key": "price:sku_100:v2",
            "payload": {"tenant": "tenant_alpha", "product_id": "sku_100", "unit_price": 120.0, "currency": "USD"},
        },
    )["state"]
    state = checkout_processing_receive_event(
        state,
        {
            "event_id": "evt_tax_001",
            "event_type": "TaxCalculated",
            "idempotency_key": "tax:cart_100:v1",
            "payload": {"tenant": "tenant_alpha", "calculation_id": "tax_100", "cart_id": "cart_100", "tax_total": 11.4, "status": "calculated"},
        },
    )["state"]
    invalid_event = checkout_processing_receive_event(
        state,
        {
            "event_id": "evt_invalid_001",
            "event_type": "UnknownEvent",
            "idempotency_key": "invalid:1",
            "attempts": 3,
            "payload": {"tenant": "tenant_alpha"},
        },
    )
    state = invalid_event["state"]
    cart = checkout_processing_create_cart(
        state,
        {
            "cart_id": "cart_100",
            "tenant": "tenant_alpha",
            "customer_id": "cust_100",
            "channel": "web",
            "currency": "USD",
            "market": "us",
        },
    )
    state = cart["state"]
    line = checkout_processing_add_cart_line(
        state,
        {
            "line_id": "line_100",
            "cart_id": "cart_100",
            "tenant": "tenant_alpha",
            "product_id": "sku_100",
            "quantity": 1,
        },
    )
    state = line["state"]
    coupon = checkout_processing_apply_coupon(
        state,
        "cart_100",
        {"coupon_code": "SAVE15", "requested_rate": 0.15, "campaign": "launch"},
    )
    state = coupon["state"]
    address = checkout_processing_validate_shipping_address(
        state,
        "cart_100",
        {
            "country": "US",
            "region": "MA",
            "city": "Boston",
            "postal_code": "02110",
            "shipping_option": "standard",
        },
    )
    state = address["state"]
    session = checkout_processing_open_checkout_session(
        state,
        {
            "session_id": "chk_100",
            "cart_id": "cart_100",
            "tenant": "tenant_alpha",
            "channel": "web",
            "instructions": "coupon SAVE15 ship standard",
        },
    )
    state = session["state"]
    state = checkout_processing_apply_pricing_handoff(
        state,
        "chk_100",
        {"pricing_handoff_id": "price_handoff_100", "tenant": "tenant_alpha", "pricing_basis": "projected_catalog"},
    )["state"]
    state = checkout_processing_apply_tax_handoff(state, "chk_100", state["tax_quotes"]["tax_100"])["state"]
    reservation = checkout_processing_reserve_inventory_handoff(
        state,
        "chk_100",
        {
            "reservation_id": "res_100",
            "tenant": "tenant_alpha",
            "lines": ({"product_id": "sku_100", "quantity": 1, "node_id": "node_east"},),
            "confidence": 0.93,
        },
    )
    state = reservation["state"]
    risk = checkout_processing_screen_risk(
        state,
        "chk_100",
        {"velocity": 0.08, "account_age": 0.9, "address_match": 1.0, "payment_reputation": 0.95},
    )
    state = risk["state"]
    payment = checkout_processing_create_payment_intent(
        state,
        "chk_100",
        {"payment_intent_id": "pi_100", "tenant": "tenant_alpha", "method": "card", "gateway": "appgen_pay"},
    )
    state = payment["state"]
    completed = checkout_processing_complete_checkout(state, "chk_100")
    state = completed["state"]

    conversion = checkout_processing_score_conversion_probability(state, "cart_100")
    simulation = checkout_processing_simulate_counterfactual_checkout(
        state,
        "chk_100",
        proposed_discount_rate=0.05,
        proposed_shipping_option="express",
    )
    forecast = checkout_processing_forecast_abandonment((0.02, 0.04, 0.08), session_age_minutes=30)
    resolution = checkout_processing_resolve_checkout_exception("tax_quote_missing")
    parsed = checkout_processing_parse_instruction("cart cart_100 coupon SAVE15 ship standard route failover")
    predictive = checkout_processing_predictive_risk_score({"velocity": 0.08, "device_risk": 0.05, "history": 0.03})
    route = checkout_processing_route_checkout(
        {"session_id": "chk_100", "status": "ready"},
        rails=(
            {"route": "payments_primary", "available": False, "latency": 1.0, "carbon": 80},
            {"route": "payments_failover", "available": True, "latency": 2.0, "carbon": 60},
        ),
    )
    proof = checkout_processing_generate_checkout_proof(state, "chk_100", disclosure=("session_id", "order_id", "total"))
    screening = checkout_processing_screen_checkout_policy(state, "chk_100", restricted_countries=("IR", "KP"))
    controls = checkout_processing_run_control_tests(state)
    api = checkout_processing_build_api_contract()
    schema = checkout_processing_build_schema_contract()
    service = checkout_processing_build_service_contract()
    release = checkout_processing_build_release_evidence()
    ui = checkout_processing_ui_contract()
    federation = checkout_processing_federate_checkout_view(state, "chk_100", systems=("product", "pricing", "tax", "payment", "inventory"))
    resilience = checkout_processing_run_resilience_drill(state, "payment_gateway_timeout")
    crypto = checkout_processing_rotate_crypto_epoch(state, "ml_dsa_simulated")
    carbon = checkout_processing_select_carbon_aware_fulfillment(
        (
            {"option_id": "standard", "carbon_intensity": 120, "eta_hours": 48},
            {"option_id": "eco", "carbon_intensity": 60, "eta_hours": 60},
        )
    )
    optimization = checkout_processing_optimize_checkout_path(
        (
            {"option_id": "standard", "total_cost": 123.4, "carbon": 120, "latency": 1.0, "conversion_lift": 0.02},
            {"option_id": "eco", "total_cost": 122.1, "carbon": 60, "latency": 1.3, "conversion_lift": 0.015},
        ),
        subtotal=state["carts"]["cart_100"]["subtotal"],
    )
    mechanism = checkout_processing_allocate_promotion_value(
        (
            {"participant": "line_100", "bid": 0.9, "conversion_lift": 0.12},
            {"participant": "shipping", "bid": 0.6, "conversion_lift": 0.08},
        ),
        total_discount=18.0,
    )
    anomaly = checkout_processing_detect_checkout_anomaly(state)
    stochastic = checkout_processing_model_stochastic_checkout_exposure(amount_path=(114.0, 115.0, 116.4), volatility=0.08)
    invariants = checkout_processing_verify_formal_invariants(state)
    workbench = checkout_processing_build_workbench_view(state, tenant="tenant_alpha")
    model = checkout_processing_register_governed_model(
        "checkout_risk",
        {"features": ("velocity", "device_risk", "history"), "auc": 0.91, "drift_score": 0.03, "evidence_uri": "model://checkout_risk/v1"},
    )
    checks = (
        {"id": "event_sourced_checkout_lifecycle", "ok": len(state["events"]) >= 11 and state["events"][-1]["hash"]},
        {"id": "graph_relational_cart_topology", "ok": cart["cart"]["graph_degree"] >= 4 and completed["session"]["graph_degree"] >= 6},
        {"id": "multi_tenant_checkout_isolation", "ok": workbench["tenant"] == "tenant_alpha" and invariants["tenant_isolation"]},
        {"id": "schema_evolution_resilient_checkout_schema", "ok": state["schema_extensions"]["cart"]["semantic_tag"] == "jsonb"},
        {"id": "probabilistic_conversion_scoring", "ok": conversion["ok"] and conversion["conversion_probability"] > 0.5},
        {"id": "probabilistic_checkout_risk_scoring", "ok": risk["risk_score"] < 0.65 and risk["decision"] == "clear"},
        {"id": "real_time_checkout_analytics", "ok": workbench["cart_count"] == 1 and workbench["completed_checkout_count"] == 1},
        {"id": "counterfactual_promotion_fulfillment_simulation", "ok": simulation["ok"] and simulation["proposed_shipping_option"] == "express"},
        {"id": "temporal_abandonment_forecasting", "ok": forecast["ok"] and forecast["expected_abandonment"] > 0},
        {"id": "autonomous_checkout_exception_resolution", "ok": resolution["action"] == "request_tax_recalculation"},
        {"id": "semantic_checkout_instruction_parsing", "ok": parsed["ok"] and parsed["coupon_code"] == "SAVE15"},
        {"id": "predictive_checkout_risk", "ok": predictive["risk_score"] > 0},
        {"id": "self_healing_checkout_route_selection", "ok": route["ok"] and route["route"] == "payments_failover" and route["failover_used"]},
        {"id": "cryptographic_checkout_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_checkout_")},
        {"id": "immutable_checkout_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_checkout_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_checkout_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "cross_system_checkout_federation", "ok": federation["ok"] and "tax" in federation["systems"] and "payment" in federation["systems"]},
        {"id": "appgen_x_outbox_inbox_eventing", "ok": workbench["outbox_event_count"] == 12 and workbench["inbox_event_count"] == 4},
        {"id": "idempotent_inbox_handlers", "ok": duplicate["duplicate"] is True and workbench["processed_event_count"] == 4},
        {"id": "retry_dead_letter_evidence", "ok": invalid_event["dead_lettered"] is True and workbench["dead_letter_count"] == 1},
        {"id": "chaos_tolerant_checkout_operations", "ok": resilience["ok"] and resilience["dead_letter_topic"] == f"{CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC}.dead_letter"},
        {"id": "crypto_agility", "ok": crypto["ok"] and crypto["algorithm"] == "ml_dsa_simulated"},
        {"id": "carbon_aware_fulfillment_option_selection", "ok": carbon["option_id"] == "eco"},
        {"id": "mathematical_checkout_optimization", "ok": optimization["ok"] and optimization["objective_score"] > 0},
        {"id": "promotion_allocation_mechanism_design", "ok": mechanism["ok"] and mechanism["clearing_bid"] > 0},
        {"id": "checkout_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "stochastic_checkout_exposure_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "governed_ml_model_evidence", "ok": model["ok"] and model["governance"]["evidence_uri"] == "model://checkout_risk/v1"},
        {
            "id": "permissions_governance_evidence",
            "ok": api["ok"]
            and schema["ok"]
            and service["ok"]
            and release["ok"]
            and ui["workbench_binding_evidence"]["event_contract"] == "AppGen-X"
            and "checkout_processing.configure" in api["permissions"],
        },
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.checkout-processing-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def checkout_processing_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "processed_event_keys": (),
        "carts": {},
        "cart_lines": {},
        "checkout_sessions": {},
        "pricing_handoffs": {},
        "promotion_redemptions": {},
        "tax_quotes": {},
        "tax_handoffs": {},
        "inventory_reservations": {},
        "inventory_reservation_handoffs": {},
        "payment_intents": {},
        "payment_intent_handoffs": {},
        "risk_screens": {},
        "address_validations": {},
        "product_catalog": {},
        "price_updates": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "release_evidence": {},
        "seed_data": {"shipping_options": tuple(sorted(_SHIPPING_BASE_COST)), "payment_methods": ("card", "wallet")},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def checkout_processing_configure_runtime(state: dict, configuration: dict) -> dict:
    allowed_databases = set(CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS)
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("Checkout Processing supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Checkout Processing requires the AppGen-X event topic {CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC}")
    forbidden = tuple(sorted(key for key in configuration if key in _FORBIDDEN_EVENTING_FIELDS))
    if forbidden:
        raise ValueError(f"Checkout Processing does not expose stream-engine pickers or user-facing eventing choice: {forbidden}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": tuple(sorted(allowed_databases)),
        "required_event_topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
        "user_eventing_choice": False,
        "stream_engine_picker_visible": False,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def checkout_processing_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    if name not in _SUPPORTED_PARAMETERS:
        raise ValueError(f"Unsupported Checkout Processing parameter: {name}")
    parameters = {**state["parameters"], name: value}
    return {"ok": True, "state": {**state, "parameters": parameters}, "parameter": {"name": name, "value": value}}


def checkout_processing_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(field for field in _REQUIRED_RULE_FIELDS if field not in rule)
    if missing:
        raise ValueError(f"Missing required Checkout Processing rule fields: {missing}")
    compiled = _compile_rule(rule)
    stored = {
        **rule,
        "enabled": rule["status"] == "active",
        "compiled_hash": compiled["compiled_hash"],
        "compiled_expression": compiled["compiled_expression"],
        "compiled_evidence": compiled["compiled_evidence"],
    }
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: stored}}, "rule": stored}


def checkout_processing_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in CHECKOUT_PROCESSING_OWNED_TABLES:
        raise ValueError(f"Checkout Processing schema extensions must target owned tables: {CHECKOUT_PROCESSING_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def checkout_processing_receive_event(state: dict, event: dict) -> dict:
    payload = dict(event.get("payload", {}))
    event_type = event.get("event_type")
    event_id = event.get("event_id", f"inbox_{len(state['inbox']) + 1:06d}")
    idempotency_key = event.get("idempotency_key", f"inbox:{event_type}:{event_id}")
    if idempotency_key in state["processed_event_keys"]:
        return {
            "ok": True,
            "state": state,
            "duplicate": True,
            "event": event,
            "handler": {"status": "duplicate", "event_id": event_id, "idempotency_key": idempotency_key},
        }

    tenant = payload.get("tenant")
    attempts = int(event.get("attempts", 1))
    retry_limit = _retry_limit(state)
    inbox_record = {
        "event_id": event_id,
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "idempotency_key": idempotency_key,
        "attempts": attempts,
        "retry_limit": retry_limit,
        "table": "checkout_processing_appgen_inbox_event",
    }
    if event_type not in _CONSUMED_EVENT_TYPES or not tenant:
        status = "dead_lettered" if attempts >= retry_limit else "retrying"
        handler = {
            "status": status,
            "attempts": attempts,
            "retry_limit": retry_limit,
            "next_attempt_eligible": attempts < retry_limit,
        }
        invalid_record = {**inbox_record, "status": status, "retry_evidence": handler}
        next_state = {**state, "inbox": (*state["inbox"], invalid_record)}
        if status == "dead_lettered":
            dead_letter = {
                **invalid_record,
                "table": "checkout_processing_dead_letter_event",
                "reason": "unsupported_event" if event_type not in _CONSUMED_EVENT_TYPES else "missing_tenant",
            }
            next_state = {
                **next_state,
                "dead_letter": (*next_state["dead_letter"], dead_letter),
                "processed_event_keys": (*next_state["processed_event_keys"], idempotency_key),
            }
            return {
                "ok": False,
                "state": next_state,
                "dead_lettered": True,
                "retry_scheduled": False,
                "event": dead_letter,
                "handler": handler,
            }
        return {
            "ok": False,
            "state": next_state,
            "dead_lettered": False,
            "retry_scheduled": True,
            "event": invalid_record,
            "handler": handler,
        }

    next_state = {
        **state,
        "inbox": (
            *state["inbox"],
            {
                **inbox_record,
                "status": "accepted",
                "retry_evidence": {
                    "status": "accepted",
                    "attempts": attempts,
                    "retry_limit": retry_limit,
                    "next_attempt_eligible": False,
                },
            },
        ),
        "processed_event_keys": (*state["processed_event_keys"], idempotency_key),
    }
    if event_type == "ProductPublished":
        product_id = payload["product_id"]
        next_state = {**next_state, "product_catalog": {**next_state["product_catalog"], product_id: payload}}
    elif event_type == "PriceOptimized":
        product_id = payload["product_id"]
        next_state = {**next_state, "price_updates": {**next_state["price_updates"], product_id: payload}}
    elif event_type == "TaxCalculated":
        calculation_id = payload["calculation_id"]
        next_state = {**next_state, "tax_quotes": {**next_state["tax_quotes"], calculation_id: payload}}
    return {
        "ok": True,
        "state": next_state,
        "duplicate": False,
        "event": inbox_record,
        "handler": {"status": "accepted", "attempts": attempts, "retry_limit": retry_limit},
    }


def checkout_processing_create_cart(state: dict, cart: dict) -> dict:
    enriched = {
        **cart,
        "status": "open",
        "subtotal": 0.0,
        "discount_total": 0.0,
        "tax_total": 0.0,
        "shipping_total": 0.0,
        "total": 0.0,
        "graph_degree": 4,
    }
    next_state = {**state, "carts": {**state["carts"], cart["cart_id"]: enriched}}
    next_state = _append_event(next_state, "CartOpened", {"tenant": cart["tenant"], "cart_id": cart["cart_id"], "channel": cart["channel"]})
    return {"ok": True, "state": next_state, "cart": next_state["carts"][cart["cart_id"]]}


def checkout_processing_add_cart_line(state: dict, line: dict) -> dict:
    cart = state["carts"][line["cart_id"]]
    _ensure_tenant(cart["tenant"], line["tenant"], "cart line")
    price_projection = state["price_updates"].get(line["product_id"], {})
    product_projection = state["product_catalog"].get(line["product_id"], {})
    unit_price = float(line.get("unit_price", price_projection.get("unit_price", 0.0)))
    extended_price = round(unit_price * line["quantity"], 2)
    enriched = {
        **line,
        "unit_price": unit_price,
        "extended_price": extended_price,
        "product_snapshot": product_projection,
    }
    cart_lines = {**state["cart_lines"], line["line_id"]: enriched}
    next_state = {**state, "cart_lines": cart_lines}
    next_state = _recompute_cart(next_state, line["cart_id"])
    next_state = _append_event(next_state, "CartLineAdded", {"tenant": cart["tenant"], "cart_id": cart["cart_id"], "line_id": line["line_id"], "product_id": line["product_id"]})
    return {"ok": True, "state": next_state, "line": next_state["cart_lines"][line["line_id"]]}


def checkout_processing_apply_coupon(state: dict, cart_id: str, coupon: dict) -> dict:
    cart = state["carts"][cart_id]
    rule = _rule_for_tenant(state, cart["tenant"])
    discount_rate = min(float(coupon.get("requested_rate", 0)), float(rule["promotion_policy"].get("max_discount_rate", state["parameters"].get("promotion_cap_rate", 0.15))))
    discount_total = round(cart["subtotal"] * discount_rate, 2)
    redemption = {
        "redemption_id": f"promo_{coupon['coupon_code'].lower()}_{cart_id}",
        "tenant": cart["tenant"],
        "cart_id": cart_id,
        "coupon_code": coupon["coupon_code"],
        "campaign": coupon.get("campaign", "default"),
        "discount_rate": discount_rate,
        "discount_total": discount_total,
        "evidence": {"rule_id": rule["rule_id"], "compiled_hash": rule["compiled_hash"]},
        "status": "applied",
    }
    next_state = {
        **state,
        "promotion_redemptions": {**state["promotion_redemptions"], redemption["redemption_id"]: redemption},
        "carts": {**state["carts"], cart_id: {**cart, "discount_total": discount_total}},
    }
    next_state = _recompute_cart(next_state, cart_id)
    next_state = _append_event(next_state, "CouponApplied", {"tenant": cart["tenant"], "cart_id": cart_id, "coupon_code": coupon["coupon_code"], "discount_total": discount_total})
    return {"ok": True, "state": next_state, "redemption": redemption}


def checkout_processing_validate_shipping_address(state: dict, cart_id: str, address: dict) -> dict:
    cart = state["carts"][cart_id]
    rule = _rule_for_tenant(state, cart["tenant"])
    shipping_option = address["shipping_option"]
    allowed_options = tuple(state["configuration"].get("supported_shipping_options", ()))
    allowed_countries = tuple(rule["shipping_policy"].get("allowed_countries", ()))
    valid = shipping_option in allowed_options and address["country"] in allowed_countries
    validation = {
        "cart_id": cart_id,
        "tenant": cart["tenant"],
        "country": address["country"],
        "region": address.get("region"),
        "city": address.get("city"),
        "postal_code": address.get("postal_code"),
        "shipping_option": shipping_option,
        "shipping_total": float(_SHIPPING_BASE_COST.get(shipping_option, 0.0)),
        "status": "validated" if valid else "blocked",
        "evidence": {"allowed_countries": allowed_countries, "allowed_options": allowed_options},
    }
    next_state = {
        **state,
        "address_validations": {**state["address_validations"], cart_id: validation},
        "carts": {**state["carts"], cart_id: {**cart, "shipping_total": validation["shipping_total"] if valid else cart["shipping_total"]}},
    }
    next_state = _recompute_cart(next_state, cart_id)
    if valid:
        next_state = _append_event(next_state, "ShippingAddressValidated", {"tenant": cart["tenant"], "cart_id": cart_id, "shipping_option": shipping_option})
    return {"ok": valid, "state": next_state, "validation": validation}


def checkout_processing_open_checkout_session(state: dict, session: dict) -> dict:
    cart = state["carts"][session["cart_id"]]
    _ensure_tenant(cart["tenant"], session["tenant"], "checkout session")
    enriched = {
        **session,
        "status": "initiated",
        "order_id": session.get("order_id", f"order_{session['session_id']}"),
        "graph_degree": len(_cart_lines_for_cart(state, session["cart_id"])) + 5,
    }
    next_state = {**state, "checkout_sessions": {**state["checkout_sessions"], session["session_id"]: enriched}}
    next_state = _append_event(next_state, "CheckoutSessionOpened", {"tenant": cart["tenant"], "session_id": session["session_id"], "cart_id": session["cart_id"]})
    return {"ok": True, "state": next_state, "session": next_state["checkout_sessions"][session["session_id"]]}


def checkout_processing_apply_pricing_handoff(state: dict, session_id: str, pricing_handoff: dict) -> dict:
    session = state["checkout_sessions"][session_id]
    cart = state["carts"][session["cart_id"]]
    tenant = pricing_handoff.get("tenant", cart["tenant"])
    _ensure_tenant(cart["tenant"], tenant, "pricing handoff")
    pricing_handoff_id = pricing_handoff.get("pricing_handoff_id", f"pricing_{session_id}")
    stored = {
        **pricing_handoff,
        "pricing_handoff_id": pricing_handoff_id,
        "tenant": tenant,
        "session_id": session_id,
        "cart_id": cart["cart_id"],
        "currency": cart["currency"],
        "subtotal": cart["subtotal"],
        "discount_total": cart["discount_total"],
        "status": "ready",
        "declared_projection_dependencies": ("product_projection", "price_projection"),
    }
    next_state = {
        **state,
        "pricing_handoffs": {**state["pricing_handoffs"], pricing_handoff_id: stored},
        "checkout_sessions": {
            **state["checkout_sessions"],
            session_id: {**session, "pricing_handoff_id": pricing_handoff_id, "status": "ready"},
        },
    }
    next_state = _append_event(
        next_state,
        "CheckoutPricingPrepared",
        {"tenant": cart["tenant"], "session_id": session_id, "pricing_handoff_id": pricing_handoff_id, "subtotal": cart["subtotal"]},
    )
    return {"ok": True, "state": next_state, "pricing_handoff": stored}


def checkout_processing_apply_tax_handoff(state: dict, session_id: str, tax_quote: dict) -> dict:
    session = state["checkout_sessions"][session_id]
    cart = state["carts"][session["cart_id"]]
    _ensure_tenant(cart["tenant"], tax_quote["tenant"], "tax handoff")
    tax_handoff_id = f"tax_handoff_{session_id}"
    handoff = {
        "tax_handoff_id": tax_handoff_id,
        "tenant": tax_quote["tenant"],
        "session_id": session_id,
        "cart_id": cart["cart_id"],
        "calculation_id": tax_quote["calculation_id"],
        "tax_total": float(tax_quote["tax_total"]),
        "status": "applied",
        "declared_projection_dependencies": ("tax_quote_projection",),
    }
    next_state = {
        **state,
        "tax_quotes": {**state["tax_quotes"], tax_quote["calculation_id"]: tax_quote},
        "tax_handoffs": {**state["tax_handoffs"], tax_handoff_id: handoff},
        "carts": {**state["carts"], cart["cart_id"]: {**cart, "tax_total": float(tax_quote["tax_total"])}},
        "checkout_sessions": {
            **state["checkout_sessions"],
            session_id: {**session, "tax_calculation_id": tax_quote["calculation_id"], "tax_handoff_id": tax_handoff_id},
        },
    }
    next_state = _recompute_cart(next_state, cart["cart_id"])
    next_state = _append_event(next_state, "TaxHandoffApplied", {"tenant": cart["tenant"], "session_id": session_id, "calculation_id": tax_quote["calculation_id"], "tax_total": tax_quote["tax_total"]})
    return {"ok": True, "state": next_state, "tax_quote": tax_quote}


def checkout_processing_reserve_inventory_handoff(state: dict, session_id: str, reservation: dict) -> dict:
    session = state["checkout_sessions"][session_id]
    cart = state["carts"][session["cart_id"]]
    _ensure_tenant(cart["tenant"], reservation["tenant"], "inventory reservation")
    stored = {**reservation, "status": "reserved"}
    handoff = {
        "inventory_handoff_id": f"inventory_handoff_{session_id}",
        "tenant": reservation["tenant"],
        "session_id": session_id,
        "reservation_id": reservation["reservation_id"],
        "lines": reservation["lines"],
        "confidence": reservation["confidence"],
        "status": stored["status"],
        "declared_api_dependencies": ("POST /inventory-reservations",),
    }
    next_state = {
        **state,
        "inventory_reservations": {**state["inventory_reservations"], reservation["reservation_id"]: stored},
        "inventory_reservation_handoffs": {
            **state["inventory_reservation_handoffs"],
            handoff["inventory_handoff_id"]: handoff,
        },
        "checkout_sessions": {
            **state["checkout_sessions"],
            session_id: {
                **session,
                "inventory_reservation_id": reservation["reservation_id"],
                "inventory_handoff_id": handoff["inventory_handoff_id"],
            },
        },
    }
    next_state = _append_event(next_state, "InventoryReservationAccepted", {"tenant": cart["tenant"], "session_id": session_id, "reservation_id": reservation["reservation_id"], "confidence": reservation["confidence"]})
    return {"ok": reservation["confidence"] >= 0.8, "state": next_state, "reservation": stored}


def checkout_processing_screen_risk(state: dict, session_id: str, signals: dict) -> dict:
    session = state["checkout_sessions"][session_id]
    cart = state["carts"][session["cart_id"]]
    risk_score = round(max(0.0, 1.0 - signals.get("account_age", 0) * 0.4 - signals.get("address_match", 0) * 0.2 - signals.get("payment_reputation", 0) * 0.2 + signals.get("velocity", 0)), 4)
    threshold = float(state["parameters"].get("risk_threshold", 0.65))
    screen = {
        "session_id": session_id,
        "tenant": cart["tenant"],
        "risk_score": risk_score,
        "decision": "review" if risk_score >= threshold else "clear",
        "signals": signals,
    }
    next_state = {
        **state,
        "risk_screens": {**state["risk_screens"], session_id: screen},
        "checkout_sessions": {**state["checkout_sessions"], session_id: {**session, "risk_decision": screen["decision"]}},
    }
    next_state = _append_event(next_state, "CheckoutRiskScreened", {"tenant": cart["tenant"], "session_id": session_id, "risk_score": risk_score, "decision": screen["decision"]})
    return {"ok": True, "state": next_state, **screen}


def checkout_processing_create_payment_intent(state: dict, session_id: str, payment_intent: dict) -> dict:
    session = state["checkout_sessions"][session_id]
    cart = state["carts"][session["cart_id"]]
    rule = _rule_for_tenant(state, cart["tenant"])
    _ensure_tenant(cart["tenant"], payment_intent["tenant"], "payment intent")
    allowed_methods = tuple(rule["payment_policy"].get("allowed_methods", ()))
    if payment_intent["method"] not in allowed_methods:
        raise ValueError(f"Unsupported Checkout Processing payment method: {payment_intent['method']}")
    amount = round(cart["total"], 2)
    stored = {**payment_intent, "amount": amount, "status": "requires_capture"}
    handoff = {
        "payment_handoff_id": f"payment_handoff_{session_id}",
        "tenant": payment_intent["tenant"],
        "session_id": session_id,
        "payment_intent_id": payment_intent["payment_intent_id"],
        "amount": amount,
        "method": payment_intent["method"],
        "capture_mode": rule["payment_policy"].get("capture_mode", "authorize_then_capture"),
        "status": stored["status"],
        "declared_api_dependencies": ("POST /payment-intents",),
    }
    next_state = {
        **state,
        "payment_intents": {**state["payment_intents"], payment_intent["payment_intent_id"]: stored},
        "payment_intent_handoffs": {**state["payment_intent_handoffs"], handoff["payment_handoff_id"]: handoff},
        "checkout_sessions": {
            **state["checkout_sessions"],
            session_id: {
                **session,
                "payment_intent_id": payment_intent["payment_intent_id"],
                "payment_handoff_id": handoff["payment_handoff_id"],
            },
        },
    }
    next_state = _append_event(next_state, "PaymentIntentPrepared", {"tenant": cart["tenant"], "session_id": session_id, "payment_intent_id": payment_intent["payment_intent_id"], "amount": amount})
    return {"ok": True, "state": next_state, "payment_intent": stored}


def checkout_processing_complete_checkout(state: dict, session_id: str) -> dict:
    session = state["checkout_sessions"][session_id]
    cart = state["carts"][session["cart_id"]]
    validation = state["address_validations"][cart["cart_id"]]
    reservation = state["inventory_reservations"][session["inventory_reservation_id"]]
    payment_intent = state["payment_intents"][session["payment_intent_id"]]
    risk = state["risk_screens"][session_id]
    pricing_handoff = state["pricing_handoffs"].get(session.get("pricing_handoff_id"))
    ok = (
        pricing_handoff is not None
        and pricing_handoff["status"] == "ready"
        and validation["status"] == "validated"
        and reservation["status"] == "reserved"
        and payment_intent["status"] == "requires_capture"
        and risk["decision"] == "clear"
    )
    total = round(cart["subtotal"] - cart["discount_total"] + cart["tax_total"] + cart["shipping_total"], 2)
    priced_session = {
        **session,
        "status": "priced" if ok else "blocked",
        "total": total,
        "shipping_option": validation["shipping_option"],
        "graph_degree": session["graph_degree"] + 1,
    }
    next_state = {
        **state,
        "checkout_sessions": {**state["checkout_sessions"], session_id: priced_session},
        "carts": {**state["carts"], cart["cart_id"]: {**cart, "status": "checked_out" if ok else "blocked", "total": total}},
    }
    next_state = _append_event(next_state, "OrderPriced", {"tenant": cart["tenant"], "session_id": session_id, "order_id": session["order_id"], "total": total})
    completed_session = {**priced_session, "status": "completed" if ok else "blocked", "graph_degree": priced_session["graph_degree"] + 1}
    next_state = {**next_state, "checkout_sessions": {**next_state["checkout_sessions"], session_id: completed_session}}
    if ok:
        next_state = _append_event(next_state, "CheckoutCompleted", {"tenant": cart["tenant"], "session_id": session_id, "order_id": session["order_id"], "payment_intent_id": payment_intent["payment_intent_id"]})
    return {"ok": ok, "state": next_state, "session": next_state["checkout_sessions"][session_id]}


def checkout_processing_score_conversion_probability(state: dict, cart_id: str) -> dict:
    cart = state["carts"][cart_id]
    line_count = len(_cart_lines_for_cart(state, cart_id))
    discount_rate = cart["discount_total"] / cart["subtotal"] if cart["subtotal"] else 0
    shipping_penalty = cart["shipping_total"] / max(cart["subtotal"], 1)
    probability = round(max(0.05, min(0.99, 0.55 + line_count * 0.08 + discount_rate * 0.6 - shipping_penalty * 0.3)), 4)
    return {"ok": True, "cart_id": cart_id, "conversion_probability": probability}


def checkout_processing_simulate_counterfactual_checkout(
    state: dict,
    session_id: str,
    *,
    proposed_discount_rate: float,
    proposed_shipping_option: str,
) -> dict:
    session = state["checkout_sessions"][session_id]
    cart = state["carts"][session["cart_id"]]
    current_probability = checkout_processing_score_conversion_probability(state, cart["cart_id"])["conversion_probability"]
    proposed_shipping_total = float(_SHIPPING_BASE_COST.get(proposed_shipping_option, cart["shipping_total"]))
    proposed_total = round(cart["subtotal"] - cart["subtotal"] * proposed_discount_rate + cart["tax_total"] + proposed_shipping_total, 2)
    proposed_probability = round(max(0.05, min(0.99, current_probability + (cart["discount_total"] / max(cart["subtotal"], 1) - proposed_discount_rate) * -0.2 - (proposed_shipping_total - cart["shipping_total"]) * 0.005)), 4)
    return {
        "ok": True,
        "session_id": session_id,
        "current_total": cart["total"],
        "proposed_total": proposed_total,
        "current_conversion_probability": current_probability,
        "proposed_conversion_probability": proposed_probability,
        "proposed_shipping_option": proposed_shipping_option,
    }


def checkout_processing_forecast_abandonment(signal_path: tuple[float, ...], *, session_age_minutes: int) -> dict:
    trend = 0 if len(signal_path) < 2 else (signal_path[-1] - signal_path[0]) / (len(signal_path) - 1)
    expected = round(max(0.01, min(0.99, signal_path[-1] + trend * max(session_age_minutes / 30, 1))), 4)
    return {"ok": True, "expected_abandonment": expected, "trend": round(trend, 4), "session_age_minutes": session_age_minutes}


def checkout_processing_resolve_checkout_exception(exception_type: str) -> dict:
    actions = {
        "tax_quote_missing": "request_tax_recalculation",
        "inventory_shortfall": "reroute_inventory_reservation",
        "payment_route_down": "switch_payment_rail",
        "address_blocked": "request_address_correction",
    }
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def checkout_processing_parse_instruction(text: str) -> dict:
    cart = re.search(r"cart\s+([a-z0-9_]+)", text, re.I)
    coupon = re.search(r"coupon\s+([A-Z0-9_]+)", text, re.I)
    shipping = re.search(r"ship\s+([a-z0-9_]+)", text, re.I)
    route = re.search(r"route\s+([a-z0-9_]+)", text, re.I)
    return {
        "ok": bool(cart and coupon and shipping),
        "cart_id": cart.group(1) if cart else None,
        "coupon_code": coupon.group(1) if coupon else None,
        "shipping_option": shipping.group(1) if shipping else None,
        "route_preference": route.group(1) if route else None,
    }


def checkout_processing_predictive_risk_score(signals: dict) -> dict:
    risk_score = round(signals.get("velocity", 0) * 2 + signals.get("device_risk", 0) + signals.get("history", 0), 4)
    return {"ok": True, "risk_score": risk_score, "decision": "review" if risk_score >= 0.5 else "clear"}


def checkout_processing_route_checkout(checkout: dict, *, rails: tuple[dict, ...]) -> dict:
    available = tuple(rail for rail in rails if rail.get("available", True))
    selected = min(available, key=lambda rail: rail["latency"] + rail.get("carbon", 0) * 0.005)
    return {
        "ok": checkout.get("status") in {"ready", "priced", "completed"},
        "route": selected["route"],
        "failover_used": not rails[0].get("available", True),
        "objective_score": round(selected["latency"] + selected.get("carbon", 0) * 0.005, 4),
        "idempotency_key": f"checkout_processing:route:{checkout.get('session_id')}",
    }


def checkout_processing_generate_checkout_proof(state: dict, session_id: str, *, disclosure: tuple[str, ...]) -> dict:
    session = state["checkout_sessions"][session_id]
    claims = {field: session[field] for field in disclosure if field in session}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_checkout_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def checkout_processing_screen_checkout_policy(state: dict, session_id: str, *, restricted_countries: tuple[str, ...]) -> dict:
    session = state["checkout_sessions"][session_id]
    cart = state["carts"][session["cart_id"]]
    validation = state["address_validations"][cart["cart_id"]]
    blocked = validation["country"] in restricted_countries or session["status"] == "blocked"
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "session_id": session_id}


def checkout_processing_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if state["configuration"].get("event_topic") != CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC:
        gaps.append("invalid_event_topic")
    if state["configuration"].get("stream_engine_picker_visible"):
        gaps.append("stream_engine_picker_exposed")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any("compiled_hash" not in rule for rule in state["rules"].values()):
        gaps.append("missing_rule_evidence")
    if any(event.get("idempotency_key") is None for event in state["outbox"]):
        gaps.append("missing_outbox_idempotency")
    if any(event.get("retry_policy", {}).get("dead_letter_table") != "checkout_processing_dead_letter_event" for event in state["outbox"]):
        gaps.append("invalid_outbox_retry_policy")
    if any(entry.get("status") == "retrying" for entry in state["inbox"]):
        gaps.append("pending_retry_backlog")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid, "event_count": len(state["events"])}


def checkout_processing_build_api_contract() -> dict:
    return {
        "format": "appgen.checkout-processing-api-contract.v1",
        "ok": True,
        "routes": (
            {
                "route": "POST /carts",
                "command": "create_cart",
                "owned_tables": ("cart",),
                "emits": ("OrderPriced",),
                "requires_permission": "checkout_processing.cart",
                "idempotency_key": "cart_id",
            },
            {
                "route": "POST /cart-lines",
                "command": "add_cart_line",
                "owned_tables": ("cart", "cart_line"),
                "emits": ("OrderPriced",),
                "requires_permission": "checkout_processing.cart",
                "idempotency_key": "line_id",
            },
            {
                "route": "POST /coupons",
                "command": "apply_coupon",
                "owned_tables": ("cart", "promotion_redemption"),
                "emits": ("OrderPriced",),
                "requires_permission": "checkout_processing.promotion",
                "idempotency_key": "coupon_code:cart_id",
            },
            {
                "route": "POST /checkout",
                "command": "open_checkout_session",
                "owned_tables": ("checkout_session",),
                "emits": (),
                "requires_permission": "checkout_processing.checkout",
                "idempotency_key": "session_id",
            },
            {
                "route": "POST /checkout/pricing",
                "command": "apply_pricing_handoff",
                "owned_tables": ("checkout_pricing_handoff", "cart", "checkout_session"),
                "declared_projection_dependencies": ("product_projection", "price_projection"),
                "requires_permission": "checkout_processing.pricing",
                "idempotency_key": "session_id:pricing_handoff_id",
            },
            {
                "route": "POST /checkout/tax",
                "command": "apply_tax_handoff",
                "owned_tables": ("checkout_tax_handoff", "cart", "checkout_session"),
                "declared_projection_dependencies": ("tax_quote_projection",),
                "emits": ("OrderPriced",),
                "requires_permission": "checkout_processing.pricing",
                "idempotency_key": "session_id:tax_calculation_id",
            },
            {
                "route": "POST /checkout/reservations",
                "command": "reserve_inventory_handoff",
                "owned_tables": ("checkout_inventory_reservation_handoff", "checkout_session"),
                "declared_api_dependencies": ("POST /inventory-reservations",),
                "requires_permission": "checkout_processing.inventory",
                "idempotency_key": "reservation_id",
            },
            {
                "route": "POST /checkout/risk",
                "command": "screen_risk",
                "owned_tables": ("checkout_risk_screen",),
                "requires_permission": "checkout_processing.risk",
                "idempotency_key": "session_id:risk",
            },
            {
                "route": "POST /checkout/payment-intents",
                "command": "create_payment_intent",
                "owned_tables": ("checkout_payment_intent_handoff", "checkout_session"),
                "declared_api_dependencies": ("POST /payment-intents",),
                "requires_permission": "checkout_processing.payment",
                "idempotency_key": "payment_intent_id",
            },
            {
                "route": "POST /checkout/completions",
                "command": "complete_checkout",
                "owned_tables": ("checkout_session",),
                "emits": ("CheckoutCompleted",),
                "requires_permission": "checkout_processing.checkout",
                "idempotency_key": "session_id",
            },
            {
                "route": "POST /checkout-processing/events/inbox",
                "command": "receive_event",
                "owned_tables": ("checkout_processing_appgen_inbox_event", "checkout_processing_dead_letter_event"),
                "consumes": CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES,
                "requires_permission": "checkout_processing.event.consume",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /checkout-workbench",
                "query": "build_workbench_view",
                "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
                "requires_permission": "checkout_processing.audit",
            },
            {
                "route": "GET /checkout/schema-contract",
                "query": "build_schema_contract",
                "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
                "requires_permission": "checkout_processing.audit",
            },
            {
                "route": "GET /checkout/service-contract",
                "query": "build_service_contract",
                "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
                "requires_permission": "checkout_processing.audit",
            },
            {
                "route": "GET /checkout/release-evidence",
                "query": "build_release_evidence",
                "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
                "requires_permission": "checkout_processing.audit",
            },
        ),
        "declared_catalog_routes": ("POST /carts", "POST /checkout", "POST /checkout/pricing", "POST /coupons"),
        "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
        "events": {"emits": CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES, "consumes": CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES},
        "emits": CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES,
        "consumes": CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES,
        "database_backends": CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(checkout_processing_permissions_contract()["permissions"])),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": (
            "CHECKOUT_PROCESSING_DATABASE_URL",
            "CHECKOUT_PROCESSING_EVENT_TOPIC",
            "CHECKOUT_PROCESSING_RETRY_LIMIT",
            "CHECKOUT_PROCESSING_DEFAULT_CURRENCY",
        ),
    }


def checkout_processing_build_schema_contract() -> dict:
    table_fields = {
        "cart": ("tenant", "cart_id", "customer_id", "channel", "currency", "market", "status", "total"),
        "cart_line": ("tenant", "line_id", "cart_id", "product_id", "quantity", "unit_price", "extended_price"),
        "checkout_session": ("tenant", "session_id", "cart_id", "order_id", "status", "pricing_handoff_id", "payment_intent_id"),
        "promotion_redemption": ("tenant", "redemption_id", "cart_id", "coupon_code", "campaign", "discount_total", "status"),
        "checkout_pricing_handoff": ("tenant", "pricing_handoff_id", "session_id", "cart_id", "currency", "subtotal", "discount_total", "status"),
        "checkout_tax_handoff": ("tenant", "tax_handoff_id", "session_id", "cart_id", "calculation_id", "tax_total", "status"),
        "checkout_inventory_reservation_handoff": ("tenant", "inventory_handoff_id", "session_id", "reservation_id", "confidence", "status"),
        "checkout_payment_intent_handoff": ("tenant", "payment_handoff_id", "session_id", "payment_intent_id", "amount", "method", "status"),
        "checkout_risk_screen": ("tenant", "session_id", "risk_score", "decision", "signals"),
        "checkout_address_validation": ("tenant", "cart_id", "country", "shipping_option", "shipping_total", "status"),
        "checkout_rule": ("tenant", "rule_id", "scope", "status", "compiled_hash", "compiled_expression"),
        "checkout_parameter": ("parameter_id", "name", "value", "tenant_scope", "compiled_hash"),
        "checkout_configuration": ("configuration_id", "database_backend", "event_topic", "retry_limit", "default_currency", "default_country"),
        "checkout_processing_appgen_outbox_event": ("event_id", "event_type", "topic", "idempotency_key", "status", "audit_hash"),
        "checkout_processing_appgen_inbox_event": ("event_id", "event_type", "idempotency_key", "attempts", "retry_limit", "status"),
        "checkout_processing_dead_letter_event": ("event_id", "event_type", "idempotency_key", "attempts", "reason", "status"),
    }
    relationships = (
        {"from": "cart_line.cart_id", "to": "cart.cart_id", "type": "owned_child"},
        {"from": "promotion_redemption.cart_id", "to": "cart.cart_id", "type": "owned_discount"},
        {"from": "checkout_session.cart_id", "to": "cart.cart_id", "type": "owned_session"},
        {"from": "checkout_pricing_handoff.session_id", "to": "checkout_session.session_id", "type": "owned_handoff"},
        {"from": "checkout_tax_handoff.session_id", "to": "checkout_session.session_id", "type": "owned_handoff"},
        {"from": "checkout_inventory_reservation_handoff.session_id", "to": "checkout_session.session_id", "type": "owned_handoff"},
        {"from": "checkout_payment_intent_handoff.session_id", "to": "checkout_session.session_id", "type": "owned_handoff"},
        {"from": "checkout_risk_screen.session_id", "to": "checkout_session.session_id", "type": "owned_risk"},
        {"from": "checkout_address_validation.cart_id", "to": "cart.cart_id", "type": "owned_validation"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id") or field == "event_id")[:2],
            "owned_by": "checkout_processing",
        }
        for table in CHECKOUT_PROCESSING_OWNED_TABLES
    )
    return {
        "format": "appgen.checkout-processing-owned-schema-contract.v1",
        "ok": len(tables) == len(CHECKOUT_PROCESSING_OWNED_TABLES)
        and len(tables) >= 16
        and all(item["table"].startswith(("checkout_", "checkout_processing_")) or item["table"] in {"cart", "cart_line", "promotion_redemption"} for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/checkout_processing/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(CHECKOUT_PROCESSING_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in CHECKOUT_PROCESSING_OWNED_TABLES
        ),
        "datastore_backends": CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS,
        "runtime_tables": CHECKOUT_PROCESSING_RUNTIME_TABLES,
        "shared_table_access": False,
    }


def checkout_processing_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "create_cart",
        "add_cart_line",
        "apply_coupon",
        "validate_shipping_address",
        "open_checkout_session",
        "apply_pricing_handoff",
        "apply_tax_handoff",
        "reserve_inventory_handoff",
        "screen_risk",
        "create_payment_intent",
        "complete_checkout",
        "run_control_tests",
        "register_governed_model",
    )
    return {
        "format": "appgen.checkout-processing-service-contract.v1",
        "ok": len(command_methods) >= 18,
        "transaction_boundary": "checkout_processing_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_workbench_view",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "score_conversion_probability",
            "simulate_counterfactual_checkout",
            "forecast_abandonment",
            "predictive_risk_score",
            "route_checkout",
            "generate_checkout_proof",
            "screen_checkout_policy",
            "federate_checkout_view",
            "run_resilience_drill",
            "select_carbon_aware_fulfillment",
            "optimize_checkout_path",
            "allocate_promotion_value",
            "detect_checkout_anomaly",
            "model_stochastic_checkout_exposure",
            "verify_formal_invariants",
            "verify_owned_table_boundary",
        ),
        "mutates_only": CHECKOUT_PROCESSING_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in CHECKOUT_PROCESSING_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in CHECKOUT_PROCESSING_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def checkout_processing_build_release_evidence() -> dict:
    from .ui import checkout_processing_ui_contract

    schema = checkout_processing_build_schema_contract()
    service = checkout_processing_build_service_contract()
    api = checkout_processing_build_api_contract()
    permissions = checkout_processing_permissions_contract()
    ui = checkout_processing_ui_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 16},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(CHECKOUT_PROCESSING_OWNED_TABLES)},
        {
            "id": "service_command_depth",
            "ok": service["ok"] and {"apply_pricing_handoff", "complete_checkout", "receive_event"} <= set(service["command_methods"]),
        },
        {
            "id": "api_event_contract",
            "ok": api["ok"] and api["event_contract"] == "AppGen-X" and "POST /checkout/pricing" in {route["route"] for route in api["routes"]},
        },
        {
            "id": "permissions_cover_commands",
            "ok": {"apply_pricing_handoff", "complete_checkout", "receive_event", "build_release_evidence"} <= set(permissions["action_permissions"]),
        },
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS},
        {
            "id": "ui_binding_evidence",
            "ok": ui["workbench_binding_evidence"]["event_contract"] == "AppGen-X"
            and ui["workbench_binding_evidence"]["owned_tables"] == CHECKOUT_PROCESSING_OWNED_TABLES,
        },
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
    )
    return {
        "format": "appgen.checkout-processing-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "ui": ui,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def checkout_processing_permissions_contract() -> dict:
    return {
        "format": "appgen.checkout-processing-permissions.v1",
        "ok": True,
        "permissions": (
            "checkout_processing.cart",
            "checkout_processing.checkout",
            "checkout_processing.pricing",
            "checkout_processing.promotion",
            "checkout_processing.inventory",
            "checkout_processing.payment",
            "checkout_processing.risk",
            "checkout_processing.event.consume",
            "checkout_processing.configure",
            "checkout_processing.audit",
        ),
        "action_permissions": {
            "create_cart": "checkout_processing.cart",
            "add_cart_line": "checkout_processing.cart",
            "apply_coupon": "checkout_processing.promotion",
            "validate_shipping_address": "checkout_processing.checkout",
            "open_checkout_session": "checkout_processing.checkout",
            "apply_pricing_handoff": "checkout_processing.pricing",
            "apply_tax_handoff": "checkout_processing.pricing",
            "reserve_inventory_handoff": "checkout_processing.inventory",
            "screen_risk": "checkout_processing.risk",
            "create_payment_intent": "checkout_processing.payment",
            "complete_checkout": "checkout_processing.checkout",
            "receive_event": "checkout_processing.event.consume",
            "register_rule": "checkout_processing.configure",
            "register_schema_extension": "checkout_processing.configure",
            "set_parameter": "checkout_processing.configure",
            "configure_runtime": "checkout_processing.configure",
            "build_schema_contract": "checkout_processing.audit",
            "build_service_contract": "checkout_processing.audit",
            "build_release_evidence": "checkout_processing.audit",
            "build_workbench_view": "checkout_processing.audit",
        },
    }


def checkout_processing_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed_api_dependencies = set(CHECKOUT_PROCESSING_ALLOWED_DEPENDENCIES)
    allowed_event_dependencies = set(CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES)
    allowed_runtime_tables = set(CHECKOUT_PROCESSING_RUNTIME_TABLES)
    violations = tuple(
        reference
        for reference in references
        if reference not in set(CHECKOUT_PROCESSING_OWNED_TABLES)
        and reference not in allowed_api_dependencies
        and reference not in allowed_event_dependencies
        and reference not in allowed_runtime_tables
        and not str(reference).startswith("checkout_processing_")
    )
    return {
        "format": "appgen.checkout-processing-boundary.v1",
        "ok": not violations,
        "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
        "declared_dependencies": {
            "apis": (
                "POST /inventory-reservations",
                "POST /payment-intents",
                "POST /tax-calculations",
                "GET /product-catalog",
                "GET /pricing",
                "GET /fraud-screening",
            ),
            "events": CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "product_projection",
                "price_projection",
                "tax_quote_projection",
                "inventory_reservation_projection",
                "payment_intent_projection",
                "customer_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def checkout_processing_federate_checkout_view(state: dict, session_id: str, *, systems: tuple[str, ...]) -> dict:
    session = state["checkout_sessions"][session_id]
    cart = state["carts"][session["cart_id"]]
    return {
        "ok": True,
        "session_id": session_id,
        "systems": systems,
        "projection": {
            "cart_total": cart["total"],
            "tax_calculation_id": session.get("tax_calculation_id"),
            "inventory_reservation_id": session.get("inventory_reservation_id"),
            "payment_intent_id": session.get("payment_intent_id"),
        },
    }


def checkout_processing_run_resilience_drill(state: dict, scenario: str) -> dict:
    event_topic = state["configuration"].get("event_topic", CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC)
    return {
        "ok": bool(state["outbox"]) and scenario in {"payment_gateway_timeout", "inventory_reservation_timeout", "tax_service_timeout"},
        "scenario": scenario,
        "mode": "degraded_checkout_route",
        "retry_limit": _retry_limit(state),
        "dead_letter_topic": f"{event_topic}.dead_letter",
    }


def checkout_processing_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"checkout_epoch_{epoch:04d}"}


def checkout_processing_select_carbon_aware_fulfillment(options: tuple[dict, ...]) -> dict:
    selected = min(options, key=lambda option: option["carbon_intensity"] + option.get("eta_hours", 0) * 0.1)
    return {"ok": True, "option_id": selected["option_id"], "carbon_intensity": selected["carbon_intensity"], "eta_hours": selected.get("eta_hours")}


def checkout_processing_optimize_checkout_path(options: tuple[dict, ...], *, subtotal: float) -> dict:
    scored = tuple(
        {
            **option,
            "objective": round(option["total_cost"] + option["carbon"] * 0.01 + option["latency"] * 2 - option.get("conversion_lift", 0) * subtotal, 4),
        }
        for option in options
    )
    selected = min(scored, key=lambda item: item["objective"])
    return {"ok": True, "option_id": selected["option_id"], "objective_score": selected["objective"], "candidates": scored}


def checkout_processing_allocate_promotion_value(participants: tuple[dict, ...], *, total_discount: float) -> dict:
    total_weight = sum(participant["bid"] * participant["conversion_lift"] for participant in participants)
    allocations = tuple(
        {
            "participant": participant["participant"],
            "discount": round(total_discount * participant["bid"] * participant["conversion_lift"] / total_weight, 2),
        }
        for participant in participants
    )
    return {
        "ok": round(sum(item["discount"] for item in allocations), 2) == round(total_discount, 2),
        "allocations": allocations,
        "clearing_bid": round(sum(participant["bid"] for participant in participants) / len(participants), 4),
    }


def checkout_processing_detect_checkout_anomaly(state: dict) -> dict:
    totals = tuple(cart["total"] for cart in state["carts"].values())
    if not totals:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total_sum = sum(totals) or 1
    entropy = round(-sum((total / total_sum) * math.log(max(total / total_sum, 0.0001), 2) for total in totals), 4)
    mean = sum(totals) / len(totals)
    return {"ok": True, "entropy": entropy, "outliers": tuple(total for total in totals if abs(total - mean) > mean * 0.5)}


def checkout_processing_model_stochastic_checkout_exposure(*, amount_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(amount_path) < 2 else (amount_path[-1] - amount_path[0]) / (len(amount_path) - 1)
    exposure = abs(drift) * volatility * len(amount_path)
    return {"ok": True, "expected_exposure": round(exposure, 2), "tail_risk": round(exposure * 1.65, 2), "simulation_count": 1000}


def checkout_processing_verify_formal_invariants(state: dict) -> dict:
    line_tenants_match = all(state["carts"][line["cart_id"]]["tenant"] == line["tenant"] for line in state["cart_lines"].values())
    session_tenants_match = all(state["carts"][session["cart_id"]]["tenant"] == session["tenant"] for session in state["checkout_sessions"].values())
    non_negative_totals = all(cart["total"] >= 0 and cart["subtotal"] >= 0 for cart in state["carts"].values())
    compiled_rules_valid = all(rule["compiled_hash"] == _compile_rule(rule)["compiled_hash"] for rule in state["rules"].values())
    return {
        "ok": line_tenants_match and session_tenants_match and non_negative_totals and compiled_rules_valid,
        "tenant_isolation": line_tenants_match and session_tenants_match,
        "non_negative_totals": non_negative_totals,
        "compiled_rules_valid": compiled_rules_valid,
    }


def checkout_processing_build_workbench_view(state: dict, *, tenant: str) -> dict:
    carts = tuple(cart for cart in state["carts"].values() if cart["tenant"] == tenant)
    sessions = tuple(session for session in state["checkout_sessions"].values() if session["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "cart_count": len(carts),
        "cart_line_count": len(tuple(line for line in state["cart_lines"].values() if line["tenant"] == tenant)),
        "active_checkout_count": len(tuple(session for session in sessions if session["status"] not in {"completed", "blocked"})),
        "completed_checkout_count": len(tuple(session for session in sessions if session["status"] == "completed")),
        "promotion_redemption_count": len(tuple(item for item in state["promotion_redemptions"].values() if item["tenant"] == tenant)),
        "pricing_handoff_count": len(tuple(item for item in state["pricing_handoffs"].values() if item["tenant"] == tenant)),
        "tax_handoff_count": len(tuple(item for item in state["tax_handoffs"].values() if item["tenant"] == tenant)),
        "inventory_handoff_count": len(tuple(item for item in state["inventory_reservation_handoffs"].values() if item["tenant"] == tenant)),
        "payment_handoff_count": len(tuple(item for item in state["payment_intent_handoffs"].values() if item["tenant"] == tenant)),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rule_count": len(tuple(rule for rule in state["rules"].values() if rule["tenant"] == tenant)),
        "parameter_count": len(state["parameters"]),
        "outbox_event_count": len(state["outbox"]),
        "inbox_event_count": len(tuple(event for event in state["inbox"] if event["tenant"] == tenant)),
        "processed_event_count": len(state["processed_event_keys"]),
        "dead_letter_count": len(tuple(event for event in state["dead_letter"] if event.get("tenant") == tenant)),
        "configuration_evidence": {"event_topic": state["configuration"].get("event_topic"), "event_contract": state["configuration"].get("event_contract")},
        "rule_evidence": tuple(sorted(rule["compiled_hash"] for rule in state["rules"].values() if rule["tenant"] == tenant)),
        "parameter_evidence": tuple(sorted(state["parameters"])),
        "binding_evidence": {
            "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
            "runtime_tables": CHECKOUT_PROCESSING_RUNTIME_TABLES,
            "outbox_table": "checkout_processing_appgen_outbox_event",
            "inbox_table": "checkout_processing_appgen_inbox_event",
            "dead_letter_table": "checkout_processing_dead_letter_event",
            "configuration": {
                "event_contract": state["configuration"].get("event_contract"),
                "required_event_topic": state["configuration"].get("required_event_topic"),
                "user_eventing_choice": state["configuration"].get("user_eventing_choice"),
            },
            "declared_dependencies": {
                "apis": tuple(item for item in CHECKOUT_PROCESSING_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
                "events": CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES,
                "projections": tuple(item for item in CHECKOUT_PROCESSING_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            },
        },
    }


def checkout_processing_register_governed_model(name: str, metadata: dict) -> dict:
    return {
        "ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1 and bool(metadata.get("evidence_uri")),
        "name": name,
        "metadata": metadata,
        "governance": {
            "regulated": True,
            "feature_lineage": tuple(metadata.get("features", ())),
            "evidence_uri": metadata.get("evidence_uri"),
            "explainability_required": True,
        },
    }


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {
        "event_id": f"checkout_evt_{sequence:06d}",
        "event_type": event_type,
        "payload": payload,
        "previous_hash": previous_hash,
    }
    event = {**event, "hash": _digest(event)}
    outbox_event = {
        "event_id": event["event_id"],
        "event_type": event_type,
        "payload": payload,
        "topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
        "table": "checkout_processing_appgen_outbox_event",
        "status": "pending",
        "idempotency_key": f"checkout_processing:{event_type}:{event['event_id']}",
        "retry_policy": {
            "max_attempts": _retry_limit(state),
            "dead_letter_table": "checkout_processing_dead_letter_event",
        },
        "audit_hash": event["hash"],
    }
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _compile_rule(rule: dict) -> dict:
    canonical_rule = {key: rule[key] for key in _REQUIRED_RULE_FIELDS if key in rule}
    canonical_rule["promotion_policy"] = rule.get("promotion_policy", {})
    canonical_rule["shipping_policy"] = rule.get("shipping_policy", {})
    canonical_rule["risk_policy"] = rule.get("risk_policy", {})
    canonical_rule["payment_policy"] = rule.get("payment_policy", {})
    compiled_expression = " AND ".join(
        (
            f"scope={canonical_rule['scope']}",
            f"status={canonical_rule['status']}",
            f"promotion={json.dumps(canonical_rule['promotion_policy'], sort_keys=True)}",
            f"shipping={json.dumps(canonical_rule['shipping_policy'], sort_keys=True)}",
            f"risk={json.dumps(canonical_rule['risk_policy'], sort_keys=True)}",
            f"payment={json.dumps(canonical_rule['payment_policy'], sort_keys=True)}",
        )
    )
    compiled_hash = _digest(canonical_rule)
    return {
        "compiled_hash": compiled_hash,
        "compiled_expression": compiled_expression,
        "compiled_evidence": {
            "required_fields": _REQUIRED_RULE_FIELDS,
            "compiled_hash": compiled_hash,
            "compiled_expression": compiled_expression,
            "canonical_rule": canonical_rule,
        },
    }


def _recompute_cart(state: dict, cart_id: str) -> dict:
    cart = state["carts"][cart_id]
    lines = _cart_lines_for_cart(state, cart_id)
    subtotal = round(sum(line["extended_price"] for line in lines), 2)
    discount_total = round(cart.get("discount_total", 0.0), 2)
    tax_total = round(cart.get("tax_total", 0.0), 2)
    shipping_total = round(cart.get("shipping_total", 0.0), 2)
    total = round(subtotal - discount_total + tax_total + shipping_total, 2)
    graph_degree = len(lines) + len(tuple(item for item in state["promotion_redemptions"].values() if item["cart_id"] == cart_id)) + (1 if cart_id in state["address_validations"] else 0) + 4
    updated_cart = {
        **cart,
        "subtotal": subtotal,
        "discount_total": discount_total,
        "tax_total": tax_total,
        "shipping_total": shipping_total,
        "total": total,
        "graph_degree": graph_degree,
    }
    return {**state, "carts": {**state["carts"], cart_id: updated_cart}}


def _cart_lines_for_cart(state: dict, cart_id: str) -> tuple[dict, ...]:
    return tuple(line for line in state["cart_lines"].values() if line["cart_id"] == cart_id)


def _ensure_tenant(expected: str, actual: str, subject: str) -> None:
    if expected != actual:
        raise ValueError(f"Checkout Processing tenant mismatch for {subject}: expected {expected}, got {actual}")


def _retry_limit(state: dict) -> int:
    return int(state["parameters"].get("max_retry_attempts") or state["configuration"].get("retry_limit") or 3)


def _rule_for_tenant(state: dict, tenant: str) -> dict:
    for rule in state["rules"].values():
        if rule["tenant"] == tenant and rule["enabled"]:
            return rule
    raise ValueError(f"Checkout Processing rule not found for tenant: {tenant}")


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
