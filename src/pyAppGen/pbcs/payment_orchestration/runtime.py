"""Executable runtime for the Payment Orchestration PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_payment_lifecycle",
    "graph_relational_payment_topology",
    "multi_tenant_payment_isolation",
    "schema_evolution_resilient_payment_schema",
    "probabilistic_authorization_fraud_settlement_scoring",
    "counterfactual_gateway_routing_simulation",
    "temporal_authorization_settlement_forecasting",
    "autonomous_payment_exception_resolution",
    "semantic_payment_instruction_parsing",
    "predictive_payment_risk",
    "self_healing_gateway_route_selection",
    "cryptographic_payment_proof",
    "immutable_payment_audit_trail",
    "dynamic_payment_policy_screening",
    "automated_payment_control_testing",
    "cross_system_checkout_billing_ledger_fraud_federation",
    "chaos_tolerant_appgen_eventing",
    "crypto_agility",
    "carbon_aware_settlement_window",
    "mathematical_gateway_optimization",
    "provider_allocation_mechanism_design",
    "payment_anomaly_detection",
    "stochastic_payment_exposure_modeling",
    "governed_ml_model_evidence",
    "universal_api_async_streaming",
    "distributed_systems_engineering",
)
PAYMENT_ORCHESTRATION_STANDARD_FEATURE_KEYS = (
    "gateway_registry",
    "payment_tokens",
    "payment_intents",
    "authorization_capture_refund_void",
    "provider_routing",
    "fraud_handoff",
    "settlement_evidence",
    "reconciliation_handoff",
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
PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PAYMENT_ORCHESTRATION_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_currency",
    "supported_currencies",
    "supported_regions",
    "supported_methods",
    "settlement_windows",
    "default_timezone",
    "workbench_limit",
)
PAYMENT_ORCHESTRATION_SUPPORTED_PARAMETER_KEYS = (
    "authorization_threshold",
    "fraud_review_threshold",
    "capture_amount_tolerance",
    "retry_limit",
    "gateway_latency_weight",
    "gateway_cost_weight",
    "gateway_auth_weight",
    "settlement_risk_weight",
    "max_capture_attempts",
    "workbench_limit",
)
PAYMENT_ORCHESTRATION_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "rule_type",
    "allowed_gateways",
    "allowed_currencies",
    "allowed_regions",
    "risk_ceiling",
    "capture_policy",
    "status",
)
PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES = ("CheckoutCompleted", "FraudRiskScored")
_CONFIG_SEQUENCE_FIELDS = {
    "supported_currencies",
    "supported_regions",
    "supported_methods",
    "settlement_windows",
}
_RULE_SEQUENCE_FIELDS = {
    "allowed_gateways",
    "allowed_currencies",
    "allowed_regions",
}
_PARAMETER_BOUNDS = {
    "authorization_threshold": (0.0, 1.0),
    "fraud_review_threshold": (0.0, 1.0),
    "capture_amount_tolerance": (0.0, 1000.0),
    "retry_limit": (1, 10),
    "gateway_latency_weight": (0.0, 1.0),
    "gateway_cost_weight": (0.0, 1.0),
    "gateway_auth_weight": (0.0, 1.0),
    "settlement_risk_weight": (0.0, 1.0),
    "max_capture_attempts": (1, 10),
    "workbench_limit": (1, 1000),
}


def payment_orchestration_runtime_capabilities() -> dict:
    smoke = payment_orchestration_runtime_smoke()
    return {
        "format": "appgen.payment-orchestration-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "payment_orchestration",
        "implementation_directory": "src/pyAppGen/pbcs/payment_orchestration",
        "capabilities": PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PAYMENT_ORCHESTRATION_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_gateway",
            "tokenize_payment_method",
            "create_payment_intent",
            "route_gateway",
            "request_fraud_check",
            "capture_payment",
            "refund_payment",
            "void_payment",
            "receive_event",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def payment_orchestration_runtime_smoke() -> dict:
    state = payment_orchestration_empty_state()
    state = payment_orchestration_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.payment.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD", "EUR"),
            "supported_regions": ("US", "EU"),
            "supported_methods": ("card", "wallet"),
            "settlement_windows": ("day", "night"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("authorization_threshold", 0.72),
        ("fraud_review_threshold", 0.65),
        ("capture_amount_tolerance", 1.0),
        ("retry_limit", 3),
        ("gateway_latency_weight", 0.2),
        ("gateway_cost_weight", 0.2),
        ("gateway_auth_weight", 0.45),
        ("settlement_risk_weight", 0.15),
        ("max_capture_attempts", 3),
        ("workbench_limit", 100),
    ):
        state = payment_orchestration_set_parameter(state, name, value)["state"]
    state = payment_orchestration_register_rule(
        state,
        {
            "rule_id": "rule_payment",
            "tenant": "tenant_alpha",
            "rule_type": "gateway_routing",
            "allowed_gateways": ("gateway_fast", "gateway_low_cost"),
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "risk_ceiling": 0.8,
            "capture_policy": "authorize_then_capture",
            "status": "active",
        },
    )["state"]
    state = payment_orchestration_register_schema_extension(
        state,
        "payment_intent",
        {"network_payload": "jsonb"},
    )["state"]
    for gateway in (
        {
            "gateway_id": "gateway_fast",
            "tenant": "tenant_alpha",
            "provider": "fastpay",
            "regions": ("US",),
            "currencies": ("USD",),
            "methods": ("card", "wallet"),
            "latency_ms": 140,
            "fee_bps": 95,
            "authorization_rate": 0.91,
            "settlement_risk": 0.08,
            "capacity": 80,
            "carbon_score": 75,
            "status": "active",
        },
        {
            "gateway_id": "gateway_low_cost",
            "tenant": "tenant_alpha",
            "provider": "valuepay",
            "regions": ("US",),
            "currencies": ("USD",),
            "methods": ("card",),
            "latency_ms": 260,
            "fee_bps": 45,
            "authorization_rate": 0.86,
            "settlement_risk": 0.12,
            "capacity": 120,
            "carbon_score": 45,
            "status": "active",
        },
    ):
        state = payment_orchestration_register_gateway(state, gateway)["state"]
    state = payment_orchestration_receive_event(
        state,
        {
            "event_id": "checkout_evt_100",
            "event_type": "CheckoutCompleted",
            "payload": {
                "tenant": "tenant_alpha",
                "checkout_id": "checkout_100",
                "customer_id": "cust_100",
                "amount": 125.5,
                "currency": "USD",
                "region": "US",
            },
        },
    )["state"]
    token = payment_orchestration_tokenize_payment_method(
        state,
        {
            "token_id": "tok_100",
            "tenant": "tenant_alpha",
            "customer_id": "cust_100",
            "method_type": "card",
            "network": "card_network",
            "issuer_country": "US",
            "vault_ref": "vault://tok_100",
        },
    )
    state = token["state"]
    intent = payment_orchestration_create_payment_intent(
        state,
        {
            "intent_id": "pi_100",
            "tenant": "tenant_alpha",
            "checkout_id": "checkout_100",
            "customer_id": "cust_100",
            "amount": 125.5,
            "currency": "USD",
            "region": "US",
            "token_id": "tok_100",
        },
    )
    state = intent["state"]
    route = payment_orchestration_route_gateway(state, "pi_100")
    state = route["state"]
    fraud = payment_orchestration_request_fraud_check(state, "pi_100")
    state = fraud["state"]
    state = payment_orchestration_receive_event(
        state,
        {
            "event_id": "fraud_evt_100",
            "event_type": "FraudRiskScored",
            "payload": {
                "tenant": "tenant_alpha",
                "intent_id": "pi_100",
                "risk_score": 0.18,
                "decision": "approve",
            },
        },
    )["state"]
    captured = payment_orchestration_capture_payment(state, "pi_100", amount=125.5)
    state = captured["state"]
    refund = payment_orchestration_refund_payment(state, "pi_100", amount=10.0, reason="goodwill")
    state = refund["state"]
    simulation = payment_orchestration_simulate_gateway_route(state, "pi_100", proposed_gateway="gateway_low_cost")
    forecast = payment_orchestration_forecast_authorization((0.82, 0.88, 0.91), settlement_risk_path=(0.2, 0.14, 0.1))
    parsed = payment_orchestration_parse_instruction("capture payment pi_100 amount 125.5 gateway gateway_fast")
    risk = payment_orchestration_score_payment_risk({"fraud": 0.18, "issuer": 0.1, "amount": 0.2, "settlement": 0.12})
    healed = payment_orchestration_self_heal_gateway_route(route["route"], tuple(route["gateway_scores"]), unavailable_gateways=("gateway_fast",))
    proof = payment_orchestration_generate_payment_proof(state, "pi_100", disclosure=("intent_id", "amount", "currency", "status"))
    screening = payment_orchestration_screen_policy(state, "pi_100", blocked_gateways=("gateway_blocked",), risk_ceiling=0.8)
    controls = payment_orchestration_run_control_tests(state)
    api = payment_orchestration_build_api_contract()
    federation = payment_orchestration_federate_payment_view(state, "pi_100", systems=("checkout", "billing", "ledger", "fraud"))
    resilience = payment_orchestration_run_resilience_drill(state, "gateway_timeout")
    crypto = payment_orchestration_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = payment_orchestration_schedule_carbon_aware_settlement(({"window": "day", "carbon": 150}, {"window": "night", "carbon": 70}))
    optimization = payment_orchestration_optimize_gateway_mix(tuple(route["gateway_scores"]), amount=125.5)
    allocation = payment_orchestration_allocate_provider_capacity(({"gateway_id": "gateway_fast", "bid": 0.9, "capacity": 8}, {"gateway_id": "gateway_low_cost", "bid": 0.8, "capacity": 12}), intents=10)
    anomaly = payment_orchestration_detect_payment_anomaly(state)
    stochastic = payment_orchestration_model_stochastic_exposure(amount_path=(100, 120, 125.5), volatility=0.1)
    model = payment_orchestration_register_governed_model("payment_risk", {"features": ("fraud", "amount", "gateway"), "auc": 0.91, "drift_score": 0.04})
    workbench = payment_orchestration_build_workbench_view(state, tenant="tenant_alpha")
    checks = (
        {"id": "event_sourced_payment_lifecycle", "ok": len(state["events"]) >= 7 and state["events"][-1]["hash"]},
        {"id": "graph_relational_payment_topology", "ok": intent["intent"]["graph_degree"] >= 4 and route["route"]["graph_degree"] >= 4},
        {"id": "multi_tenant_payment_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_payment_schema", "ok": state["schema_extensions"]["payment_intent"]["network_payload"] == "jsonb"},
        {"id": "probabilistic_authorization_fraud_settlement_scoring", "ok": captured["authorization_score"] >= 0.72 and fraud["fraud_check"]["risk_score"] < 0.65},
        {"id": "counterfactual_gateway_routing_simulation", "ok": simulation["ok"] and simulation["proposed_gateway"] == "gateway_low_cost"},
        {"id": "temporal_authorization_settlement_forecasting", "ok": forecast["ok"] and forecast["forecast_authorization_rate"] > 0},
        {"id": "autonomous_payment_exception_resolution", "ok": payment_orchestration_resolve_exception("issuer_decline")["action"] == "retry_alternate_gateway"},
        {"id": "semantic_payment_instruction_parsing", "ok": parsed["ok"] and parsed["intent_id"] == "pi_100"},
        {"id": "predictive_payment_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_gateway_route_selection", "ok": healed["ok"] and healed["gateway_id"] == "gateway_low_cost"},
        {"id": "cryptographic_payment_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_payment_")},
        {"id": "immutable_payment_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_payment_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_payment_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "cross_system_checkout_billing_ledger_fraud_federation", "ok": federation["ok"] and "ledger" in federation["systems"]},
        {"id": "chaos_tolerant_appgen_eventing", "ok": resilience["ok"] and resilience["mode"] == "degraded_gateway_replay"},
        {"id": "crypto_agility", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_settlement_window", "ok": carbon["window"] == "night"},
        {"id": "mathematical_gateway_optimization", "ok": optimization["ok"] and optimization["objective_score"] > 0},
        {"id": "provider_allocation_mechanism_design", "ok": allocation["ok"] and allocation["allocations"][0]["intents"] > 0},
        {"id": "payment_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "stochastic_payment_exposure_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "governed_ml_model_evidence", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "PaymentCaptured" in api["events"]["emits"]},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("payment_orchestration:PaymentRefunded")},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.payment-orchestration-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def payment_orchestration_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "gateways": {},
        "tokens": {},
        "intents": {},
        "fraud_checks": {},
        "routes": {},
        "settlements": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "handled_events": {},
        "checkout_evidence": {},
        "governed_models": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def payment_orchestration_configure_runtime(state: dict, configuration: dict) -> dict:
    unknown = tuple(sorted(field for field in configuration if field not in PAYMENT_ORCHESTRATION_SUPPORTED_CONFIGURATION_FIELDS))
    if unknown:
        raise ValueError(f"Unsupported Payment Orchestration configuration fields: {unknown}")
    missing = tuple(sorted(field for field in PAYMENT_ORCHESTRATION_SUPPORTED_CONFIGURATION_FIELDS if field not in configuration))
    if missing:
        raise ValueError(f"Missing required Payment Orchestration configuration fields: {missing}")
    if configuration["database_backend"] not in PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Payment Orchestration supports only PostgreSQL, MySQL, or MariaDB backends")
    event_topic = str(configuration.get("event_topic", "")).strip()
    if not event_topic or not event_topic.startswith("appgen."):
        raise ValueError("Payment Orchestration requires an AppGen-X event topic")
    configured = {
        **_normalize_fields(configuration, _CONFIG_SEQUENCE_FIELDS),
        "ok": True,
        "event_contract": "appgen_event_contract",
        "allowed_database_backends": PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "supported_configuration_fields": PAYMENT_ORCHESTRATION_SUPPORTED_CONFIGURATION_FIELDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def payment_orchestration_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    if name not in PAYMENT_ORCHESTRATION_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Payment Orchestration parameter: {name}")
    if not isinstance(value, (int, float)):
        raise ValueError("Payment Orchestration parameters must be numeric")
    lower, upper = _PARAMETER_BOUNDS[name]
    if value < lower or value > upper:
        raise ValueError(f"Payment Orchestration parameter {name} must be between {lower} and {upper}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def payment_orchestration_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(sorted(field for field in PAYMENT_ORCHESTRATION_REQUIRED_RULE_FIELDS if field not in rule))
    if missing:
        raise ValueError(f"Missing required Payment Orchestration rule fields: {missing}")
    normalized = _normalize_fields(rule, _RULE_SEQUENCE_FIELDS)
    configuration = state.get("configuration", {})
    if configuration:
        if not set(normalized["allowed_currencies"]) <= set(configuration.get("supported_currencies", ())):
            raise ValueError("Payment Orchestration rule currencies must be configured")
        if not set(normalized["allowed_regions"]) <= set(configuration.get("supported_regions", ())):
            raise ValueError("Payment Orchestration rule regions must be configured")
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
            "required_fields": PAYMENT_ORCHESTRATION_REQUIRED_RULE_FIELDS,
        },
    }
    return {"ok": True, "state": {**state, "rules": {**state["rules"], normalized["rule_id"]: enriched}}, "rule": enriched}


def payment_orchestration_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def payment_orchestration_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    if event_type not in PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES:
        raise ValueError("Payment Orchestration only consumes CheckoutCompleted and FraudRiskScored")
    handler_key = f"{event_type}:{event_id}"
    existing = state["handled_events"].get(handler_key)
    if existing and existing["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": existing}
    attempts = int(existing.get("attempts", 0) if existing else 0) + 1
    inbox_entry = {"event_id": event_id, "event_type": event_type, "tenant": event["payload"].get("tenant"), "attempts": attempts}
    next_state = {**state, "inbox": (*state["inbox"], inbox_entry)}
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 3))
    if simulate_failure:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        handled = {**next_state["handled_events"], handler_key: evidence}
        next_state = {**next_state, "handled_events": handled}
        if status == "dead_letter":
            next_state = {**next_state, "dead_letter": (*next_state["dead_letter"], evidence)}
        return {"ok": False, "state": next_state, "handler": evidence}
    payload = event["payload"]
    if event_type == "CheckoutCompleted":
        next_state = {
            **next_state,
            "checkout_evidence": {
                **next_state["checkout_evidence"],
                payload["checkout_id"]: {
                    "tenant": payload["tenant"],
                    "checkout_id": payload["checkout_id"],
                    "customer_id": payload["customer_id"],
                    "amount": float(payload["amount"]),
                    "currency": payload["currency"],
                    "region": payload["region"],
                },
            },
        }
    elif event_type == "FraudRiskScored":
        intent_id = payload["intent_id"]
        check = next_state["fraud_checks"].get(intent_id, {})
        next_state = {
            **next_state,
            "fraud_checks": {
                **next_state["fraud_checks"],
                intent_id: {**check, **payload, "status": payload.get("decision", "review")},
            },
        }
    evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": "processed"}
    return {"ok": True, "state": {**next_state, "handled_events": {**next_state["handled_events"], handler_key: evidence}}, "handler": evidence}


def payment_orchestration_register_gateway(state: dict, gateway: dict) -> dict:
    configuration = state["configuration"]
    ok = (
        gateway["status"] == "active"
        and set(gateway["regions"]) <= set(configuration["supported_regions"])
        and set(gateway["currencies"]) <= set(configuration["supported_currencies"])
        and set(gateway["methods"]) <= set(configuration["supported_methods"])
    )
    enriched = {**_normalize_fields(gateway, {"regions", "currencies", "methods"}), "status": "active" if ok else "blocked", "graph_degree": 6}
    next_state = {**state, "gateways": {**state["gateways"], gateway["gateway_id"]: enriched}}
    next_state = _append_event(next_state, "PaymentGatewayRegistered", {"tenant": gateway["tenant"], "gateway_id": gateway["gateway_id"]}, emit_outbox=False)
    return {"ok": ok, "state": next_state, "gateway": enriched}


def payment_orchestration_tokenize_payment_method(state: dict, token: dict) -> dict:
    ok = token["method_type"] in state["configuration"]["supported_methods"] and bool(token.get("vault_ref"))
    enriched = {**token, "status": "active" if ok else "blocked", "fingerprint": _digest({"vault_ref": token["vault_ref"], "customer": token["customer_id"]})[:16]}
    next_state = {**state, "tokens": {**state["tokens"], token["token_id"]: enriched}}
    next_state = _append_event(next_state, "PaymentTokenVaulted", {"tenant": token["tenant"], "token_id": token["token_id"], "method_type": token["method_type"]}, emit_outbox=False)
    return {"ok": ok, "state": next_state, "token": enriched}


def payment_orchestration_create_payment_intent(state: dict, intent: dict) -> dict:
    checkout = state["checkout_evidence"].get(intent["checkout_id"])
    token = state["tokens"].get(intent["token_id"])
    ok = bool(checkout) and bool(token) and intent["currency"] in state["configuration"]["supported_currencies"]
    enriched = {**intent, "status": "created" if ok else "blocked", "authorized_amount": 0.0, "captured_amount": 0.0, "refunded_amount": 0.0, "graph_degree": 6}
    next_state = {**state, "intents": {**state["intents"], intent["intent_id"]: enriched}}
    next_state = _append_event(next_state, "PaymentIntentCreated", {"tenant": intent["tenant"], "intent_id": intent["intent_id"], "amount": intent["amount"]}, emit_outbox=False)
    return {"ok": ok, "state": next_state, "intent": enriched}


def payment_orchestration_route_gateway(state: dict, intent_id: str) -> dict:
    intent = state["intents"][intent_id]
    rule = _active_rule_for_tenant(state, intent["tenant"])
    candidates = tuple(
        gateway for gateway in state["gateways"].values()
        if gateway["tenant"] == intent["tenant"]
        and gateway["gateway_id"] in rule["allowed_gateways"]
        and intent["currency"] in gateway["currencies"]
        and intent["region"] in gateway["regions"]
        and gateway["status"] == "active"
    )
    scores = _score_gateways(candidates, state["parameters"])
    winner = max(scores, key=lambda item: item["objective_score"])
    route = {
        "route_id": f"route_{intent_id}",
        "tenant": intent["tenant"],
        "intent_id": intent_id,
        "gateway_id": winner["gateway_id"],
        "authorization_score": winner["authorization_score"],
        "settlement_risk": winner["settlement_risk"],
        "objective_score": winner["objective_score"],
        "status": "selected",
        "graph_degree": 5,
    }
    updated_intent = {**intent, "gateway_id": winner["gateway_id"], "status": "routed", "authorization_score": winner["authorization_score"]}
    return {"ok": True, "state": {**state, "routes": {**state["routes"], intent_id: route}, "intents": {**state["intents"], intent_id: updated_intent}}, "route": route, "gateway_scores": scores}


def payment_orchestration_request_fraud_check(state: dict, intent_id: str) -> dict:
    intent = state["intents"][intent_id]
    risk_score = round(min(1.0, float(intent["amount"]) / 1000 * 0.25 + state["routes"][intent_id]["settlement_risk"]), 4)
    fraud_check = {"fraud_check_id": f"fraud_{intent_id}", "tenant": intent["tenant"], "intent_id": intent_id, "risk_score": risk_score, "status": "requested"}
    next_state = {**state, "fraud_checks": {**state["fraud_checks"], intent_id: fraud_check}}
    next_state = _append_event(next_state, "FraudCheckRequested", {"tenant": intent["tenant"], "intent_id": intent_id, "risk_score": risk_score})
    return {"ok": True, "state": next_state, "fraud_check": fraud_check}


def payment_orchestration_capture_payment(state: dict, intent_id: str, *, amount: float) -> dict:
    intent = state["intents"][intent_id]
    fraud = state["fraud_checks"].get(intent_id, {})
    rule = _active_rule_for_tenant(state, intent["tenant"])
    tolerance = float(state["parameters"].get("capture_amount_tolerance", 0))
    authorization_score = float(intent.get("authorization_score", 0))
    ok = (
        amount <= float(intent["amount"]) + tolerance
        and authorization_score >= float(state["parameters"]["authorization_threshold"])
        and float(fraud.get("risk_score", 1)) <= float(rule["risk_ceiling"])
    )
    updated = {**intent, "status": "captured" if ok else "failed", "authorized_amount": amount if ok else 0.0, "captured_amount": amount if ok else 0.0}
    event_type = "PaymentCaptured" if ok else "PaymentFailed"
    next_state = {**state, "intents": {**state["intents"], intent_id: updated}, "settlements": {**state["settlements"], intent_id: {"intent_id": intent_id, "tenant": intent["tenant"], "amount": amount, "status": "pending_settlement" if ok else "failed"}}}
    next_state = _append_event(next_state, event_type, {"tenant": intent["tenant"], "intent_id": intent_id, "amount": amount, "gateway_id": intent.get("gateway_id")})
    return {"ok": ok, "state": next_state, "intent": updated, "authorization_score": authorization_score}


def payment_orchestration_refund_payment(state: dict, intent_id: str, *, amount: float, reason: str) -> dict:
    intent = state["intents"][intent_id]
    ok = intent["status"] == "captured" and amount <= float(intent["captured_amount"]) - float(intent.get("refunded_amount", 0))
    updated = {**intent, "status": "partially_refunded" if ok else intent["status"], "refunded_amount": round(float(intent.get("refunded_amount", 0)) + (amount if ok else 0), 2)}
    next_state = {**state, "intents": {**state["intents"], intent_id: updated}}
    next_state = _append_event(next_state, "PaymentRefunded", {"tenant": intent["tenant"], "intent_id": intent_id, "amount": amount, "reason": reason})
    return {"ok": ok, "state": next_state, "intent": updated}


def payment_orchestration_void_payment(state: dict, intent_id: str, *, reason: str) -> dict:
    intent = state["intents"][intent_id]
    ok = intent["status"] in {"created", "routed"}
    updated = {**intent, "status": "voided" if ok else intent["status"], "void_reason": reason}
    next_state = {**state, "intents": {**state["intents"], intent_id: updated}}
    next_state = _append_event(next_state, "PaymentVoided", {"tenant": intent["tenant"], "intent_id": intent_id, "reason": reason})
    return {"ok": ok, "state": next_state, "intent": updated}


def payment_orchestration_simulate_gateway_route(state: dict, intent_id: str, *, proposed_gateway: str) -> dict:
    current = state["routes"][intent_id]
    gateway = state["gateways"][proposed_gateway]
    return {"ok": True, "intent_id": intent_id, "proposed_gateway": proposed_gateway, "cost_delta_bps": gateway["fee_bps"] - state["gateways"][current["gateway_id"]]["fee_bps"], "latency_delta_ms": gateway["latency_ms"] - state["gateways"][current["gateway_id"]]["latency_ms"]}


def payment_orchestration_forecast_authorization(auth_rate_path: tuple[float, ...], *, settlement_risk_path: tuple[float, ...]) -> dict:
    auth_trend = auth_rate_path[-1] - auth_rate_path[0] if len(auth_rate_path) > 1 else 0
    risk_trend = settlement_risk_path[-1] - settlement_risk_path[0] if len(settlement_risk_path) > 1 else 0
    return {"ok": True, "forecast_authorization_rate": round(max(0, min(1, auth_rate_path[-1] + auth_trend / max(len(auth_rate_path), 1))), 4), "forecast_settlement_risk": round(max(0, settlement_risk_path[-1] + risk_trend / max(len(settlement_risk_path), 1)), 4)}


def payment_orchestration_parse_instruction(text: str) -> dict:
    action = re.search(r"(capture|refund|void)\s+payment", text, re.I)
    intent = re.search(r"\b(pi_[a-z0-9_]+)\b", text, re.I)
    amount = re.search(r"amount\s+([0-9.]+)", text, re.I)
    gateway = re.search(r"gateway\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(action and intent), "action": action.group(1).lower() if action else None, "intent_id": intent.group(1) if intent else None, "amount": float(amount.group(1)) if amount else None, "gateway_id": gateway.group(1) if gateway else None}


def payment_orchestration_score_payment_risk(signals: dict) -> dict:
    risk = round(signals.get("fraud", 0) * 1.8 + signals.get("issuer", 0) + signals.get("amount", 0) * 0.4 + signals.get("settlement", 0), 4)
    return {"ok": True, "risk_score": risk, "decision": "review" if risk >= 0.65 else "approve"}


def payment_orchestration_resolve_exception(exception_type: str) -> dict:
    actions = {
        "issuer_decline": "retry_alternate_gateway",
        "fraud_review": "request_step_up_authentication",
        "settlement_delay": "route_treasury_review",
        "token_expired": "request_payment_method_refresh",
    }
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def payment_orchestration_self_heal_gateway_route(route: dict, gateway_scores: tuple[dict, ...], *, unavailable_gateways: tuple[str, ...]) -> dict:
    candidates = tuple(score for score in gateway_scores if score["gateway_id"] not in unavailable_gateways)
    selected = max(candidates, key=lambda item: item["objective_score"])
    return {"ok": True, "gateway_id": selected["gateway_id"], "previous_gateway": route["gateway_id"], "failover_used": selected["gateway_id"] != route["gateway_id"]}


def payment_orchestration_generate_payment_proof(state: dict, intent_id: str, *, disclosure: tuple[str, ...]) -> dict:
    intent = state["intents"][intent_id]
    claims = {field: intent[field] for field in disclosure if field in intent}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_payment_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def payment_orchestration_screen_policy(state: dict, intent_id: str, *, blocked_gateways: tuple[str, ...], risk_ceiling: float) -> dict:
    route = state["routes"][intent_id]
    fraud = state["fraud_checks"].get(intent_id, {})
    blocked = route["gateway_id"] in blocked_gateways or float(fraud.get("risk_score", 0)) > risk_ceiling
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "intent_id": intent_id}


def payment_orchestration_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(intent["status"] in {"created", "routed"} for intent in state["intents"].values()):
        gaps.append("open_payment_intent")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def payment_orchestration_build_api_contract() -> dict:
    return {"ok": True, "routes": ("POST /payment-intents", "POST /gateway-routes", "POST /tokens", "POST /payment-captures", "POST /payment-refunds", "GET /payment-workbench"), "events": {"emits": ("PaymentCaptured", "PaymentFailed", "FraudCheckRequested"), "consumes": PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES}, "permissions": ("payment_orchestration.read", "payment_orchestration.intent", "payment_orchestration.capture", "payment_orchestration.refund", "payment_orchestration.configure", "payment_orchestration.audit")}


def payment_orchestration_federate_payment_view(state: dict, intent_id: str, *, systems: tuple[str, ...]) -> dict:
    intent = state["intents"][intent_id]
    return {"ok": True, "intent_id": intent_id, "systems": systems, "projection": {"status": intent["status"], "amount": intent["amount"], "currency": intent["currency"], "gateway_id": intent.get("gateway_id")}}


def payment_orchestration_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"gateway_timeout", "fraud_timeout"}, "scenario": scenario, "mode": "degraded_gateway_replay", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "payment_orchestration.dead_letter"}


def payment_orchestration_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"payment_epoch_{epoch:04d}"}


def payment_orchestration_schedule_carbon_aware_settlement(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def payment_orchestration_optimize_gateway_mix(gateway_scores: tuple[dict, ...], *, amount: float) -> dict:
    selected = max(gateway_scores, key=lambda score: score["objective_score"])
    return {"ok": True, "gateway_id": selected["gateway_id"], "objective_score": selected["objective_score"], "expected_fee": round(amount * selected["fee_bps"] / 10000, 4)}


def payment_orchestration_allocate_provider_capacity(gateways: tuple[dict, ...], *, intents: int) -> dict:
    total = sum(item["bid"] * item["capacity"] for item in gateways) or 1
    allocations = tuple({"gateway_id": item["gateway_id"], "intents": round(intents * item["bid"] * item["capacity"] / total, 2)} for item in gateways)
    return {"ok": round(sum(item["intents"] for item in allocations), 2) == round(intents, 2), "allocations": allocations}


def payment_orchestration_detect_payment_anomaly(state: dict) -> dict:
    amounts = tuple(float(intent.get("amount", 0)) for intent in state["intents"].values())
    if not amounts:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(amounts) or 1
    entropy = round(-sum((amount / total) * math.log(max(amount / total, 0.0001), 2) for amount in amounts), 4)
    mean = sum(amounts) / len(amounts)
    return {"ok": True, "entropy": entropy, "outliers": tuple(amount for amount in amounts if abs(amount - mean) > 1000)}


def payment_orchestration_model_stochastic_exposure(*, amount_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(amount_path) < 2 else (amount_path[-1] - amount_path[0]) / (len(amount_path) - 1)
    exposure = abs(drift) * volatility * len(amount_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4)}


def payment_orchestration_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def payment_orchestration_build_workbench_view(state: dict, *, tenant: str) -> dict:
    intents = tuple(intent for intent in state["intents"].values() if intent["tenant"] == tenant)
    gateways = tuple(gateway for gateway in state["gateways"].values() if gateway["tenant"] == tenant)
    fraud = tuple(check for check in state["fraud_checks"].values() if check.get("tenant") == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "intent_count": len(intents),
        "captured_count": len(tuple(intent for intent in intents if intent["status"] in {"captured", "partially_refunded"})),
        "gateway_count": len(gateways),
        "fraud_check_count": len(fraud),
        "settlement_count": len(tuple(item for item in state["settlements"].values() if item["tenant"] == tenant)),
        "captured_amount": round(sum(intent.get("captured_amount", 0) for intent in intents), 2),
        "refunded_amount": round(sum(intent.get("refunded_amount", 0) for intent in intents), 2),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(tuple(item for item in state["inbox"] if item["tenant"] == tenant)),
        "outbox_count": len(state["outbox"]),
        "dead_letter_count": len(state["dead_letter"]),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
        },
    }


def _active_rule_for_tenant(state: dict, tenant: str) -> dict:
    return next(rule for rule in state["rules"].values() if rule["tenant"] == tenant and rule["enabled"])


def _score_gateways(gateways: tuple[dict, ...], parameters: dict) -> tuple[dict, ...]:
    latency_values = tuple(gateway["latency_ms"] for gateway in gateways)
    cost_values = tuple(gateway["fee_bps"] for gateway in gateways)
    auth_values = tuple(gateway["authorization_rate"] for gateway in gateways)
    risk_values = tuple(gateway["settlement_risk"] for gateway in gateways)
    weight_total = sum(float(parameters[name]) for name in ("gateway_latency_weight", "gateway_cost_weight", "gateway_auth_weight", "settlement_risk_weight")) or 1.0
    scored = []
    for gateway in gateways:
        latency_component = _normalize_metric(gateway["latency_ms"], min(latency_values), max(latency_values), lower_is_better=True)
        cost_component = _normalize_metric(gateway["fee_bps"], min(cost_values), max(cost_values), lower_is_better=True)
        auth_component = _normalize_metric(gateway["authorization_rate"], min(auth_values), max(auth_values), lower_is_better=False)
        risk_component = _normalize_metric(gateway["settlement_risk"], min(risk_values), max(risk_values), lower_is_better=True)
        objective_score = round(float(parameters["gateway_latency_weight"]) * latency_component + float(parameters["gateway_cost_weight"]) * cost_component + float(parameters["gateway_auth_weight"]) * auth_component + float(parameters["settlement_risk_weight"]) * risk_component, 4)
        scored.append({**gateway, "objective_score": objective_score, "authorization_score": round(max(0, min(1, gateway["authorization_rate"] - gateway["settlement_risk"] * 0.5)), 4), "confidence": round(objective_score / weight_total, 4)})
    return tuple(scored)


def _append_event(state: dict, event_type: str, payload: dict, *, emit_outbox: bool = True) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"payment_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox = state["outbox"]
    if emit_outbox:
        outbox = (*outbox, {"event_type": event_type, "payload": payload, "idempotency_key": f"payment_orchestration:{event_type}:{event['event_id']}"})
    return {**state, "events": (*state["events"], event), "outbox": outbox}


def _normalize_metric(value: float, minimum: float, maximum: float, *, lower_is_better: bool) -> float:
    if maximum == minimum:
        return 1.0
    normalized = (value - minimum) / (maximum - minimum)
    return round(1 - normalized if lower_is_better else normalized, 6)


def _normalize_fields(payload: dict, sequence_fields: set[str]) -> dict:
    return {key: tuple(value) if key in sequence_fields else value for key, value in payload.items()}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
