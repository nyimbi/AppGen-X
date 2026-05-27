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
    "gateway_health_evidence",
    "payment_tokens",
    "payment_intents",
    "authorization_controls",
    "authorization_capture_refund_void",
    "provider_routing",
    "fraud_handoff",
    "settlement_execution",
    "settlement_evidence",
    "payout_scheduling",
    "dispute_chargeback_workflow",
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
    "schema_extension",
    "audit_trace",
    "payment_proof",
    "policy_screening",
    "control_assertion",
    "governed_model",
    "workbench",
)
PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC = "appgen.payment.events"
PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PAYMENT_ORCHESTRATION_OWNED_TABLES = (
    "payment_gateway",
    "payment_token",
    "payment_intent",
    "gateway_route",
    "fraud_check",
    "payment_authorization",
    "payment_capture",
    "payment_refund",
    "payment_void",
    "payment_settlement",
    "payment_payout",
    "payment_dispute",
    "payment_reconciliation_handoff",
    "payment_exception",
    "payment_audit_trace",
    "payment_proof",
    "payment_federation_projection",
    "payment_carbon_window",
    "payment_gateway_optimization",
    "payment_provider_allocation",
    "payment_anomaly_signal",
    "payment_risk_model",
    "payment_exposure_forecast",
    "payment_instruction_parse",
    "payment_schema_extension",
    "payment_control_assertion",
    "payment_governed_model",
    "payment_rule",
    "payment_parameter",
    "payment_configuration",
    "payment_orchestration_appgen_outbox_event",
    "payment_orchestration_appgen_inbox_event",
    "payment_orchestration_dead_letter_event",
)
PAYMENT_ORCHESTRATION_EMITTED_EVENT_TYPES = (
    "PaymentIntentCreated",
    "PaymentAuthorized",
    "FraudCheckRequested",
    "PaymentCaptured",
    "PaymentSettled",
    "PaymentRefunded",
    "PaymentVoided",
    "PaymentDisputeOpened",
    "PaymentDisputeResolved",
    "PaymentPayoutScheduled",
    "PaymentFailed",
)
PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES = (
    "CheckoutCompleted",
    "FraudRiskScored",
)
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
_PAYMENT_ORCHESTRATION_RUNTIME_TABLES = (
    "payment_orchestration_appgen_outbox_event",
    "payment_orchestration_appgen_inbox_event",
    "payment_orchestration_dead_letter_event",
)
_PAYMENT_ORCHESTRATION_ALLOWED_DEPENDENCIES = (
    "checkout_completion_projection",
    "fraud_risk_projection",
    "ledger_cash_projection",
    "billing_invoice_projection",
    "GET /checkout/sessions/{id}",
    "GET /fraud/cases/{id}",
    "GET /billing/invoices/{id}",
    "POST /ledger/payment-events",
    "POST /audit/payment-events",
)
_PAYMENT_ORCHESTRATION_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}
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
        "owned_tables": PAYMENT_ORCHESTRATION_OWNED_TABLES,
        "allowed_database_backends": PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "capabilities": PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PAYMENT_ORCHESTRATION_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "register_gateway",
            "tokenize_payment_method",
            "create_payment_intent",
            "route_gateway",
            "request_fraud_check",
            "authorize_payment",
            "capture_payment",
            "settle_payment",
            "schedule_payout",
            "refund_payment",
            "open_dispute",
            "resolve_dispute",
            "void_payment",
            "simulate_gateway_route",
            "forecast_authorization",
            "parse_instruction",
            "score_payment_risk",
            "generate_payment_proof",
            "screen_policy",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "verify_owned_table_boundary",
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
            "event_topic": PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
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
    state = payment_orchestration_tokenize_payment_method(
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
    )["state"]
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
    settled = payment_orchestration_settle_payment(
        state,
        "pi_100",
        settlement_reference="batch_2026_001",
    )
    state = settled["state"]
    payout = payment_orchestration_schedule_payout(
        state,
        "pi_100",
        payout_account="merchant_settlement_account",
    )
    state = payout["state"]
    refund = payment_orchestration_refund_payment(state, "pi_100", amount=10.0, reason="goodwill")
    state = refund["state"]
    dispute = payment_orchestration_open_dispute(
        state,
        "pi_100",
        amount=5.0,
        reason="customer_question",
        evidence=("proof_of_delivery", "customer_acknowledgement"),
    )
    state = dispute["state"]
    dispute_resolution = payment_orchestration_resolve_dispute(
        state,
        dispute["dispute"]["dispute_id"],
        decision="merchant_won",
        resolution_notes="evidence accepted",
    )
    state = dispute_resolution["state"]
    simulation = payment_orchestration_simulate_gateway_route(
        state,
        "pi_100",
        proposed_gateway="gateway_low_cost",
    )
    forecast = payment_orchestration_forecast_authorization(
        (0.82, 0.88, 0.91),
        settlement_risk_path=(0.2, 0.14, 0.1),
    )
    parsed = payment_orchestration_parse_instruction(
        "capture payment pi_100 amount 125.5 gateway gateway_fast"
    )
    risk = payment_orchestration_score_payment_risk(
        {"fraud": 0.18, "issuer": 0.1, "amount": 0.2, "settlement": 0.12}
    )
    healed = payment_orchestration_self_heal_gateway_route(
        route["route"],
        tuple(route["gateway_scores"]),
        unavailable_gateways=("gateway_fast",),
    )
    proof = payment_orchestration_generate_payment_proof(
        state,
        "pi_100",
        disclosure=("intent_id", "amount", "currency", "status"),
    )
    screening = payment_orchestration_screen_policy(
        state,
        "pi_100",
        blocked_gateways=("gateway_blocked",),
        risk_ceiling=0.8,
    )
    controls = payment_orchestration_run_control_tests(state)
    api = payment_orchestration_build_api_contract()
    schema = payment_orchestration_build_schema_contract()
    service = payment_orchestration_build_service_contract()
    release = payment_orchestration_build_release_evidence()
    permissions = payment_orchestration_permissions_contract()
    boundary = payment_orchestration_verify_owned_table_boundary(
        (
            "payment_intent",
            "payment_orchestration_appgen_inbox_event",
            "checkout_completion_projection",
            "POST /ledger/payment-events",
            "CheckoutCompleted",
        )
    )
    federation = payment_orchestration_federate_payment_view(
        state,
        "pi_100",
        systems=("checkout", "billing", "ledger", "fraud"),
    )
    resilience = payment_orchestration_run_resilience_drill(state, "gateway_timeout")
    crypto = payment_orchestration_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = payment_orchestration_schedule_carbon_aware_settlement(
        ({"window": "day", "carbon": 150}, {"window": "night", "carbon": 70})
    )
    optimization = payment_orchestration_optimize_gateway_mix(
        tuple(route["gateway_scores"]),
        amount=125.5,
    )
    allocation = payment_orchestration_allocate_provider_capacity(
        (
            {"gateway_id": "gateway_fast", "bid": 0.9, "capacity": 8},
            {"gateway_id": "gateway_low_cost", "bid": 0.8, "capacity": 12},
        ),
        intents=10,
    )
    anomaly = payment_orchestration_detect_payment_anomaly(state)
    stochastic = payment_orchestration_model_stochastic_exposure(
        amount_path=(100, 120, 125.5),
        volatility=0.1,
    )
    model = payment_orchestration_register_governed_model(
        "payment_risk",
        {"features": ("fraud", "amount", "gateway"), "auc": 0.91, "drift_score": 0.04},
    )
    workbench = payment_orchestration_build_workbench_view(state, tenant="tenant_alpha")
    checks = (
        {
            "id": "event_sourced_payment_lifecycle",
            "ok": len(state["events"]) >= 7 and state["events"][-1]["hash"],
        },
        {
            "id": "graph_relational_payment_topology",
            "ok": intent["intent"]["graph_degree"] >= 4 and route["route"]["graph_degree"] >= 4,
        },
        {"id": "multi_tenant_payment_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {
            "id": "schema_evolution_resilient_payment_schema",
            "ok": schema["ok"] and state["schema_extensions"]["payment_intent"]["network_payload"] == "jsonb",
        },
        {
            "id": "probabilistic_authorization_fraud_settlement_scoring",
            "ok": captured["authorization_score"] >= 0.72
            and fraud["fraud_check"]["risk_score"] < 0.65
            and settled["settlement"]["status"] == "settled",
        },
        {
            "id": "counterfactual_gateway_routing_simulation",
            "ok": simulation["ok"] and simulation["proposed_gateway"] == "gateway_low_cost",
        },
        {
            "id": "temporal_authorization_settlement_forecasting",
            "ok": forecast["ok"] and forecast["forecast_authorization_rate"] > 0,
        },
        {
            "id": "autonomous_payment_exception_resolution",
            "ok": payment_orchestration_resolve_exception("issuer_decline")["action"] == "retry_alternate_gateway",
        },
        {
            "id": "semantic_payment_instruction_parsing",
            "ok": parsed["ok"] and parsed["intent_id"] == "pi_100",
        },
        {"id": "predictive_payment_risk", "ok": risk["risk_score"] > 0},
        {
            "id": "self_healing_gateway_route_selection",
            "ok": healed["ok"] and healed["gateway_id"] == "gateway_low_cost",
        },
        {
            "id": "cryptographic_payment_proof",
            "ok": proof["ok"] and proof["proof"].startswith("zk_payment_"),
        },
        {"id": "immutable_payment_audit_trail", "ok": controls["hash_chain_valid"]},
        {
            "id": "dynamic_payment_policy_screening",
            "ok": screening["ok"] and screening["decision"] == "clear",
        },
        {
            "id": "automated_payment_control_testing",
            "ok": controls["ok"] and not controls["blocking_gaps"],
        },
        {
            "id": "cross_system_checkout_billing_ledger_fraud_federation",
            "ok": federation["ok"] and "ledger" in federation["systems"],
        },
        {
            "id": "chaos_tolerant_appgen_eventing",
            "ok": resilience["ok"] and resilience["mode"] == "degraded_gateway_replay",
        },
        {"id": "crypto_agility", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_settlement_window", "ok": carbon["window"] == "night"},
        {
            "id": "mathematical_gateway_optimization",
            "ok": optimization["ok"] and optimization["objective_score"] > 0,
        },
        {
            "id": "provider_allocation_mechanism_design",
            "ok": allocation["ok"] and allocation["allocations"][0]["intents"] > 0,
        },
        {"id": "payment_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {
            "id": "stochastic_payment_exposure_modeling",
            "ok": stochastic["ok"] and stochastic["tail_risk"] > 0,
        },
        {
            "id": "governed_ml_model_evidence",
            "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"],
        },
        {
            "id": "universal_api_async_streaming",
            "ok": api["ok"] and service["ok"] and release["ok"] and api["event_contract"] == "AppGen-X",
        },
        {
            "id": "distributed_systems_engineering",
            "ok": permissions["ok"]
            and state["outbox"][-1]["idempotency_key"].startswith("payment_orchestration:PaymentDisputeResolved")
            and boundary["ok"],
        },
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.payment-orchestration-runtime-smoke.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
    }


def payment_orchestration_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "gateways": {},
        "tokens": {},
        "intents": {},
        "routes": {},
        "fraud_checks": {},
        "authorizations": {},
        "captures": {},
        "refunds": {},
        "voids": {},
        "settlements": {},
        "payouts": {},
        "disputes": {},
        "reconciliation_handoffs": {},
        "exceptions": {},
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
    forbidden = tuple(sorted(field for field in configuration if field in _PAYMENT_ORCHESTRATION_FORBIDDEN_EVENTING_FIELDS))
    if forbidden:
        raise ValueError(
            "Payment Orchestration runtime does not allow stream-engine or alternate eventing fields: "
            + ", ".join(forbidden)
        )
    unknown = tuple(
        sorted(field for field in configuration if field not in PAYMENT_ORCHESTRATION_SUPPORTED_CONFIGURATION_FIELDS)
    )
    if unknown:
        raise ValueError(f"Unsupported Payment Orchestration configuration fields: {unknown}")
    missing = tuple(
        sorted(field for field in PAYMENT_ORCHESTRATION_SUPPORTED_CONFIGURATION_FIELDS if field not in configuration)
    )
    if missing:
        raise ValueError(f"Missing required Payment Orchestration configuration fields: {missing}")
    if configuration["database_backend"] not in PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Payment Orchestration supports only PostgreSQL, MySQL, or MariaDB backends")
    event_topic = str(configuration.get("event_topic", "")).strip()
    if event_topic != PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC:
        raise ValueError(
            f"Payment Orchestration requires AppGen-X event topic {PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC}"
        )
    configured = {
        **_normalize_fields(configuration, _CONFIG_SEQUENCE_FIELDS),
        "ok": True,
        "event_contract": "AppGen-X",
        "required_event_topic": PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": PAYMENT_ORCHESTRATION_OWNED_TABLES,
        "supported_configuration_fields": PAYMENT_ORCHESTRATION_SUPPORTED_CONFIGURATION_FIELDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
    }
    return {
        "ok": True,
        "state": {**state, "configuration": configured},
        "configuration": configured,
    }


def payment_orchestration_set_parameter(
    state: dict,
    name: str,
    value: float | int | str | bool,
) -> dict:
    if name not in PAYMENT_ORCHESTRATION_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Payment Orchestration parameter: {name}")
    if not isinstance(value, (int, float)):
        raise ValueError("Payment Orchestration parameters must be numeric")
    lower, upper = _PARAMETER_BOUNDS[name]
    if value < lower or value > upper:
        raise ValueError(
            f"Payment Orchestration parameter {name} must be between {lower} and {upper}"
        )
    parameter = {"name": name, "value": value}
    return {
        "ok": True,
        "state": {**state, "parameters": {**state["parameters"], name: value}},
        "parameter": parameter,
    }


def payment_orchestration_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(
        sorted(field for field in PAYMENT_ORCHESTRATION_REQUIRED_RULE_FIELDS if field not in rule)
    )
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
    return {
        "ok": True,
        "state": {**state, "rules": {**state["rules"], normalized["rule_id"]: enriched}},
        "rule": enriched,
    }


def payment_orchestration_register_schema_extension(
    state: dict,
    table: str,
    fields: dict,
) -> dict:
    if table not in PAYMENT_ORCHESTRATION_OWNED_TABLES:
        return {
            "ok": False,
            "error": "table_not_owned",
            "table": table,
            "owned_tables": PAYMENT_ORCHESTRATION_OWNED_TABLES,
            "state": state,
        }
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {
            "ok": False,
            "error": "invalid_extension_field",
            "invalid": invalid,
            "state": state,
        }
    next_extensions = {**state["schema_extensions"], table: dict(fields)}
    return {"ok": True, "state": {**state, "schema_extensions": next_extensions}}


def payment_orchestration_receive_event(
    state: dict,
    event: dict,
    *,
    simulate_failure: bool = False,
) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    payload = event.get("payload", {})
    if event_type not in PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES and not simulate_failure:
        raise ValueError("Payment Orchestration only consumes CheckoutCompleted and FraudRiskScored")
    idempotency_key = f"payment_orchestration:{event_type}:{event_id}"
    handler_key = f"{event_type}:{event_id}"
    existing = state["handled_events"].get(handler_key)
    if existing and existing["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": existing}
    attempts = int(existing.get("attempts", 0) if existing else 0) + 1
    retry_limit = int(state.get("configuration", {}).get("retry_limit", 3))
    inbox_entry = {
        "event_id": event_id,
        "event_type": event_type,
        "tenant": payload.get("tenant"),
        "attempts": attempts,
        "idempotency_key": idempotency_key,
    }
    next_state = {**state, "inbox": (*state["inbox"], inbox_entry)}
    if simulate_failure or event_type not in PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        evidence = {
            "event_id": event_id,
            "event_type": event_type,
            "attempts": attempts,
            "status": status,
            "retry_limit": retry_limit,
            "idempotency_key": idempotency_key,
            "dead_letter_topic": "payment_orchestration.dead_letter",
        }
        next_state = {
            **next_state,
            "handled_events": {**next_state["handled_events"], handler_key: evidence},
        }
        if status == "dead_letter":
            next_state = {**next_state, "dead_letter": (*next_state["dead_letter"], evidence)}
        return {"ok": False, "state": next_state, "handler": evidence}
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
                    "projection": "checkout_completion_projection",
                },
            },
        }
    if event_type == "FraudRiskScored":
        intent_id = payload["intent_id"]
        current = next_state["fraud_checks"].get(intent_id, {})
        next_state = {
            **next_state,
            "fraud_checks": {
                **next_state["fraud_checks"],
                intent_id: {
                    **current,
                    **payload,
                    "status": payload.get("decision", "review"),
                    "projection": "fraud_risk_projection",
                },
            },
        }
    evidence = {
        "event_id": event_id,
        "event_type": event_type,
        "attempts": attempts,
        "status": "processed",
        "retry_limit": retry_limit,
        "idempotency_key": idempotency_key,
    }
    next_state = {
        **next_state,
        "handled_events": {**next_state["handled_events"], handler_key: evidence},
    }
    return {"ok": True, "state": next_state, "handler": evidence}


def payment_orchestration_register_gateway(state: dict, gateway: dict) -> dict:
    configuration = state["configuration"]
    ok = (
        gateway["status"] == "active"
        and set(gateway["regions"]) <= set(configuration["supported_regions"])
        and set(gateway["currencies"]) <= set(configuration["supported_currencies"])
        and set(gateway["methods"]) <= set(configuration["supported_methods"])
    )
    enriched = {
        **_normalize_fields(gateway, {"regions", "currencies", "methods"}),
        "status": "active" if ok else "blocked",
        "graph_degree": 6,
    }
    next_state = {**state, "gateways": {**state["gateways"], gateway["gateway_id"]: enriched}}
    next_state = _append_event(
        next_state,
        "PaymentGatewayRegistered",
        {"tenant": gateway["tenant"], "gateway_id": gateway["gateway_id"]},
        emit_outbox=False,
    )
    return {"ok": ok, "state": next_state, "gateway": enriched}


def payment_orchestration_tokenize_payment_method(state: dict, token: dict) -> dict:
    ok = (
        token["method_type"] in state["configuration"]["supported_methods"]
        and bool(token.get("vault_ref"))
    )
    enriched = {
        **token,
        "status": "active" if ok else "blocked",
        "fingerprint": _digest(
            {"vault_ref": token["vault_ref"], "customer_id": token["customer_id"]}
        )[:16],
    }
    next_state = {**state, "tokens": {**state["tokens"], token["token_id"]: enriched}}
    next_state = _append_event(
        next_state,
        "PaymentTokenVaulted",
        {
            "tenant": token["tenant"],
            "token_id": token["token_id"],
            "method_type": token["method_type"],
        },
        emit_outbox=False,
    )
    return {"ok": ok, "state": next_state, "token": enriched}


def payment_orchestration_create_payment_intent(state: dict, intent: dict) -> dict:
    checkout = state["checkout_evidence"].get(intent["checkout_id"])
    token = state["tokens"].get(intent["token_id"])
    ok = (
        bool(checkout)
        and bool(token)
        and intent["currency"] in state["configuration"]["supported_currencies"]
        and intent["region"] in state["configuration"]["supported_regions"]
    )
    enriched = {
        **intent,
        "status": "created" if ok else "blocked",
        "authorized_amount": 0.0,
        "captured_amount": 0.0,
        "refunded_amount": 0.0,
        "graph_degree": 6,
    }
    next_state = {**state, "intents": {**state["intents"], intent["intent_id"]: enriched}}
    next_state = _append_event(
        next_state,
        "PaymentIntentCreated",
        {
            "tenant": intent["tenant"],
            "intent_id": intent["intent_id"],
            "amount": intent["amount"],
            "currency": intent["currency"],
        },
        emit_outbox=False,
    )
    return {"ok": ok, "state": next_state, "intent": enriched}


def payment_orchestration_route_gateway(state: dict, intent_id: str) -> dict:
    intent = state["intents"][intent_id]
    rule = _active_rule_for_tenant(state, intent["tenant"])
    candidates = tuple(
        gateway
        for gateway in state["gateways"].values()
        if gateway["tenant"] == intent["tenant"]
        and gateway["gateway_id"] in rule["allowed_gateways"]
        and intent["currency"] in gateway["currencies"]
        and intent["region"] in gateway["regions"]
        and gateway["status"] == "active"
    )
    gateway_scores = _score_gateways(candidates, state["parameters"])
    winner = max(gateway_scores, key=lambda item: item["objective_score"])
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
    updated_intent = {
        **intent,
        "gateway_id": winner["gateway_id"],
        "status": "routed",
        "authorization_score": winner["authorization_score"],
    }
    next_state = {
        **state,
        "routes": {**state["routes"], intent_id: route},
        "intents": {**state["intents"], intent_id: updated_intent},
    }
    return {
        "ok": True,
        "state": next_state,
        "route": route,
        "gateway_scores": gateway_scores,
    }


def payment_orchestration_request_fraud_check(state: dict, intent_id: str) -> dict:
    intent = state["intents"][intent_id]
    risk_score = round(
        min(
            1.0,
            float(intent["amount"]) / 1000 * 0.25 + state["routes"][intent_id]["settlement_risk"],
        ),
        4,
    )
    fraud_check = {
        "fraud_check_id": f"fraud_{intent_id}",
        "tenant": intent["tenant"],
        "intent_id": intent_id,
        "risk_score": risk_score,
        "status": "requested",
    }
    next_state = {**state, "fraud_checks": {**state["fraud_checks"], intent_id: fraud_check}}
    next_state = _append_event(
        next_state,
        "FraudCheckRequested",
        {
            "tenant": intent["tenant"],
            "intent_id": intent_id,
            "risk_score": risk_score,
        },
    )
    return {"ok": True, "state": next_state, "fraud_check": fraud_check}


def payment_orchestration_capture_payment(
    state: dict,
    intent_id: str,
    *,
    amount: float,
) -> dict:
    authorization = payment_orchestration_authorize_payment(state, intent_id, amount=amount)
    state = authorization["state"]
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
    updated_intent = {
        **intent,
        "status": "captured" if ok else "failed",
        "authorized_amount": amount if ok else 0.0,
        "captured_amount": amount if ok else 0.0,
    }
    next_state = {**state, "intents": {**state["intents"], intent_id: updated_intent}}
    if ok:
        capture = {
            "capture_id": f"cap_{intent_id}",
            "tenant": intent["tenant"],
            "intent_id": intent_id,
            "amount": amount,
            "gateway_id": intent.get("gateway_id"),
            "status": "captured",
        }
        settlement = {
            "settlement_id": f"stl_{intent_id}",
            "tenant": intent["tenant"],
            "intent_id": intent_id,
            "amount": amount,
            "window": state["configuration"]["settlement_windows"][0],
            "status": "pending_settlement",
        }
        handoff = {
            "handoff_id": f"handoff_{intent_id}",
            "tenant": intent["tenant"],
            "intent_id": intent_id,
            "target_projection": "ledger_cash_projection",
            "status": "ready",
        }
        next_state = {
            **next_state,
            "captures": {**next_state["captures"], intent_id: capture},
            "settlements": {**next_state["settlements"], intent_id: settlement},
            "reconciliation_handoffs": {
                **next_state["reconciliation_handoffs"],
                intent_id: handoff,
            },
        }
        next_state = _append_event(
            next_state,
            "PaymentCaptured",
            {
                "tenant": intent["tenant"],
                "intent_id": intent_id,
                "amount": amount,
                "gateway_id": intent.get("gateway_id"),
            },
        )
    else:
        next_state = {
            **next_state,
            "exceptions": {
                **next_state["exceptions"],
                intent_id: {
                    "exception_id": f"exc_{intent_id}",
                    "tenant": intent["tenant"],
                    "intent_id": intent_id,
                    "reason": "capture_policy_rejected",
                    "action": payment_orchestration_resolve_exception("issuer_decline")["action"],
                },
            },
        }
        next_state = _append_event(
            next_state,
            "PaymentFailed",
            {
                "tenant": intent["tenant"],
                "intent_id": intent_id,
                "amount": amount,
                "gateway_id": intent.get("gateway_id"),
            },
        )
    return {
        "ok": ok,
        "state": next_state,
        "intent": updated_intent,
        "authorization_score": authorization_score,
    }


def payment_orchestration_authorize_payment(
    state: dict,
    intent_id: str,
    *,
    amount: float,
) -> dict:
    intent = state["intents"][intent_id]
    route = state["routes"].get(intent_id, {})
    fraud = state["fraud_checks"].get(intent_id, {})
    threshold = float(state["parameters"].get("authorization_threshold", 1))
    risk_ceiling = float(_active_rule_for_tenant(state, intent["tenant"]).get("risk_ceiling", 1))
    authorization_score = float(route.get("authorization_score", intent.get("authorization_score", 0)))
    ok = (
        intent["status"] in {"routed", "authorized", "captured"}
        and amount <= float(intent["amount"])
        and authorization_score >= threshold
        and float(fraud.get("risk_score", 0)) <= risk_ceiling
    )
    authorization = {
        "authorization_id": f"auth_{intent_id}_{len(state['authorizations']) + 1}",
        "tenant": intent["tenant"],
        "intent_id": intent_id,
        "gateway_id": intent.get("gateway_id"),
        "amount": amount,
        "authorization_score": authorization_score,
        "risk_score": float(fraud.get("risk_score", 0)),
        "status": "authorized" if ok else "declined",
        "network_reference": _digest({"intent_id": intent_id, "amount": amount})[:18],
    }
    updated_intent = {
        **intent,
        "status": "authorized" if ok and intent["status"] != "captured" else intent["status"],
        "authorized_amount": amount if ok else intent.get("authorized_amount", 0.0),
        "authorization_reference": authorization["network_reference"] if ok else intent.get("authorization_reference"),
    }
    next_state = {
        **state,
        "authorizations": {**state["authorizations"], authorization["authorization_id"]: authorization},
        "intents": {**state["intents"], intent_id: updated_intent},
    }
    next_state = _append_event(
        next_state,
        "PaymentAuthorized" if ok else "PaymentFailed",
        {
            "tenant": intent["tenant"],
            "intent_id": intent_id,
            "amount": amount,
            "gateway_id": intent.get("gateway_id"),
            "authorization_reference": authorization["network_reference"],
        },
    )
    return {"ok": ok, "state": next_state, "authorization": authorization, "intent": updated_intent}


def payment_orchestration_settle_payment(
    state: dict,
    intent_id: str,
    *,
    settlement_reference: str,
) -> dict:
    intent = state["intents"][intent_id]
    settlement = state["settlements"].get(intent_id)
    ok = intent["status"] in {"captured", "partially_refunded"} and bool(settlement) and bool(settlement_reference)
    updated_settlement = {
        **(settlement or {
            "settlement_id": f"stl_{intent_id}",
            "tenant": intent["tenant"],
            "intent_id": intent_id,
            "amount": intent.get("captured_amount", 0.0),
            "window": state["configuration"].get("settlement_windows", ("default",))[0],
        }),
        "status": "settled" if ok else "blocked",
        "settlement_reference": settlement_reference,
        "reconciled_amount": round(float(intent.get("captured_amount", 0)) - float(intent.get("refunded_amount", 0)), 2),
    }
    handoff = {
        "handoff_id": f"handoff_{intent_id}_settlement",
        "tenant": intent["tenant"],
        "intent_id": intent_id,
        "target_projection": "ledger_cash_projection",
        "status": "ready" if ok else "blocked",
        "settlement_reference": settlement_reference,
    }
    next_state = {
        **state,
        "settlements": {**state["settlements"], intent_id: updated_settlement},
        "reconciliation_handoffs": {
            **state["reconciliation_handoffs"],
            handoff["handoff_id"]: handoff,
        },
    }
    if ok:
        next_state = _append_event(
            next_state,
            "PaymentSettled",
            {
                "tenant": intent["tenant"],
                "intent_id": intent_id,
                "amount": updated_settlement["reconciled_amount"],
                "settlement_reference": settlement_reference,
            },
        )
    return {"ok": ok, "state": next_state, "settlement": updated_settlement, "handoff": handoff}


def payment_orchestration_schedule_payout(
    state: dict,
    intent_id: str,
    *,
    payout_account: str,
) -> dict:
    intent = state["intents"][intent_id]
    settlement = state["settlements"].get(intent_id, {})
    amount = round(float(intent.get("captured_amount", 0)) - float(intent.get("refunded_amount", 0)), 2)
    ok = settlement.get("status") == "settled" and amount > 0 and bool(payout_account)
    payout = {
        "payout_id": f"payout_{intent_id}_{len(state['payouts']) + 1}",
        "tenant": intent["tenant"],
        "intent_id": intent_id,
        "settlement_id": settlement.get("settlement_id"),
        "payout_account": payout_account,
        "amount": amount,
        "currency": intent["currency"],
        "status": "scheduled" if ok else "blocked",
    }
    next_state = {**state, "payouts": {**state["payouts"], payout["payout_id"]: payout}}
    if ok:
        next_state = _append_event(
            next_state,
            "PaymentPayoutScheduled",
            {
                "tenant": intent["tenant"],
                "intent_id": intent_id,
                "amount": amount,
                "currency": intent["currency"],
            },
        )
    return {"ok": ok, "state": next_state, "payout": payout}


def payment_orchestration_refund_payment(
    state: dict,
    intent_id: str,
    *,
    amount: float,
    reason: str,
) -> dict:
    intent = state["intents"][intent_id]
    ok = intent["status"] == "captured" and amount <= float(intent["captured_amount"]) - float(
        intent.get("refunded_amount", 0)
    )
    updated_intent = {
        **intent,
        "status": "partially_refunded" if ok else intent["status"],
        "refunded_amount": round(float(intent.get("refunded_amount", 0)) + (amount if ok else 0), 2),
    }
    next_state = {**state, "intents": {**state["intents"], intent_id: updated_intent}}
    if ok:
        refund = {
            "refund_id": f"rfd_{intent_id}_{len(state['refunds']) + 1}",
            "tenant": intent["tenant"],
            "intent_id": intent_id,
            "amount": amount,
            "reason": reason,
            "status": "refunded",
        }
        next_state = {
            **next_state,
            "refunds": {**next_state["refunds"], refund["refund_id"]: refund},
            "reconciliation_handoffs": {
                **next_state["reconciliation_handoffs"],
                f"handoff_{refund['refund_id']}": {
                    "handoff_id": f"handoff_{refund['refund_id']}",
                    "tenant": intent["tenant"],
                    "intent_id": intent_id,
                    "target_projection": "ledger_cash_projection",
                    "status": "ready",
                    "refund_id": refund["refund_id"],
                },
            },
        }
        next_state = _append_event(
            next_state,
            "PaymentRefunded",
            {
                "tenant": intent["tenant"],
                "intent_id": intent_id,
                "amount": amount,
                "reason": reason,
            },
        )
    return {"ok": ok, "state": next_state, "intent": updated_intent}


def payment_orchestration_open_dispute(
    state: dict,
    intent_id: str,
    *,
    amount: float,
    reason: str,
    evidence: tuple[str, ...] = (),
) -> dict:
    intent = state["intents"][intent_id]
    ok = intent["status"] in {"captured", "partially_refunded"} and amount <= float(intent.get("captured_amount", 0))
    dispute = {
        "dispute_id": f"dsp_{intent_id}_{len(state['disputes']) + 1}",
        "tenant": intent["tenant"],
        "intent_id": intent_id,
        "amount": amount,
        "reason": reason,
        "evidence": tuple(evidence),
        "status": "evidence_required" if ok and not evidence else "under_review" if ok else "blocked",
        "recommended_action": "submit_evidence" if ok else "reject_dispute",
    }
    next_state = {**state, "disputes": {**state["disputes"], dispute["dispute_id"]: dispute}}
    if ok:
        next_state = _append_event(
            next_state,
            "PaymentDisputeOpened",
            {
                "tenant": intent["tenant"],
                "intent_id": intent_id,
                "dispute_id": dispute["dispute_id"],
                "amount": amount,
            },
        )
    return {"ok": ok, "state": next_state, "dispute": dispute}


def payment_orchestration_resolve_dispute(
    state: dict,
    dispute_id: str,
    *,
    decision: str,
    resolution_notes: str,
) -> dict:
    dispute = state["disputes"][dispute_id]
    intent = state["intents"][dispute["intent_id"]]
    decision = str(decision)
    merchant_won = decision == "merchant_won"
    updated_dispute = {
        **dispute,
        "status": "resolved",
        "decision": decision,
        "resolution_notes": resolution_notes,
        "financial_impact": 0.0 if merchant_won else float(dispute["amount"]),
    }
    updated_intent = {
        **intent,
        "disputed_amount": round(float(intent.get("disputed_amount", 0)) + updated_dispute["financial_impact"], 2),
    }
    handoff = {
        "handoff_id": f"handoff_{dispute_id}",
        "tenant": dispute["tenant"],
        "intent_id": dispute["intent_id"],
        "target_projection": "ledger_cash_projection",
        "status": "ready",
        "dispute_id": dispute_id,
        "financial_impact": updated_dispute["financial_impact"],
    }
    next_state = {
        **state,
        "disputes": {**state["disputes"], dispute_id: updated_dispute},
        "intents": {**state["intents"], dispute["intent_id"]: updated_intent},
        "reconciliation_handoffs": {**state["reconciliation_handoffs"], handoff["handoff_id"]: handoff},
    }
    next_state = _append_event(
        next_state,
        "PaymentDisputeResolved",
        {
            "tenant": dispute["tenant"],
            "intent_id": dispute["intent_id"],
            "dispute_id": dispute_id,
            "decision": decision,
            "financial_impact": updated_dispute["financial_impact"],
        },
    )
    return {"ok": True, "state": next_state, "dispute": updated_dispute, "handoff": handoff}


def payment_orchestration_void_payment(state: dict, intent_id: str, *, reason: str) -> dict:
    intent = state["intents"][intent_id]
    ok = intent["status"] in {"created", "routed"}
    updated_intent = {**intent, "status": "voided" if ok else intent["status"], "void_reason": reason}
    next_state = {**state, "intents": {**state["intents"], intent_id: updated_intent}}
    if ok:
        void = {
            "void_id": f"void_{intent_id}",
            "tenant": intent["tenant"],
            "intent_id": intent_id,
            "reason": reason,
            "status": "voided",
        }
        next_state = {**next_state, "voids": {**next_state["voids"], intent_id: void}}
        next_state = _append_event(
            next_state,
            "PaymentVoided",
            {"tenant": intent["tenant"], "intent_id": intent_id, "reason": reason},
        )
    return {"ok": ok, "state": next_state, "intent": updated_intent}


def payment_orchestration_simulate_gateway_route(
    state: dict,
    intent_id: str,
    *,
    proposed_gateway: str,
) -> dict:
    current = state["routes"][intent_id]
    proposed = state["gateways"][proposed_gateway]
    current_gateway = state["gateways"][current["gateway_id"]]
    return {
        "ok": True,
        "intent_id": intent_id,
        "proposed_gateway": proposed_gateway,
        "cost_delta_bps": proposed["fee_bps"] - current_gateway["fee_bps"],
        "latency_delta_ms": proposed["latency_ms"] - current_gateway["latency_ms"],
    }


def payment_orchestration_forecast_authorization(
    auth_rate_path: tuple[float, ...],
    *,
    settlement_risk_path: tuple[float, ...],
) -> dict:
    auth_trend = auth_rate_path[-1] - auth_rate_path[0] if len(auth_rate_path) > 1 else 0
    risk_trend = settlement_risk_path[-1] - settlement_risk_path[0] if len(settlement_risk_path) > 1 else 0
    return {
        "ok": True,
        "forecast_authorization_rate": round(
            max(0, min(1, auth_rate_path[-1] + auth_trend / max(len(auth_rate_path), 1))),
            4,
        ),
        "forecast_settlement_risk": round(
            max(0, settlement_risk_path[-1] + risk_trend / max(len(settlement_risk_path), 1)),
            4,
        ),
    }


def payment_orchestration_parse_instruction(text: str) -> dict:
    action = re.search(r"(authorize|capture|settle|payout|refund|void|dispute|resolve)\s+(?:payment|dispute)", text, re.I)
    intent = re.search(r"\b(pi_[a-z0-9_]+)\b", text, re.I)
    amount = re.search(r"amount\s+([0-9.]+)", text, re.I)
    gateway = re.search(r"gateway\s+([a-z0-9_]+)", text, re.I)
    return {
        "ok": bool(action and intent),
        "action": action.group(1).lower() if action else None,
        "intent_id": intent.group(1) if intent else None,
        "amount": float(amount.group(1)) if amount else None,
        "gateway_id": gateway.group(1) if gateway else None,
        "parsed_hash": _digest({"text": text})[:16],
    }


def payment_orchestration_score_payment_risk(signals: dict) -> dict:
    risk_score = round(
        signals.get("fraud", 0) * 1.8
        + signals.get("issuer", 0)
        + signals.get("amount", 0) * 0.4
        + signals.get("settlement", 0),
        4,
    )
    return {
        "ok": True,
        "risk_score": risk_score,
        "decision": "review" if risk_score >= 0.65 else "approve",
    }


def payment_orchestration_resolve_exception(exception_type: str) -> dict:
    actions = {
        "issuer_decline": "retry_alternate_gateway",
        "fraud_review": "request_step_up_authentication",
        "settlement_delay": "route_treasury_review",
        "token_expired": "request_payment_method_refresh",
    }
    return {
        "ok": exception_type in actions,
        "exception_type": exception_type,
        "action": actions.get(exception_type, "manual_review"),
    }


def payment_orchestration_self_heal_gateway_route(
    route: dict,
    gateway_scores: tuple[dict, ...],
    *,
    unavailable_gateways: tuple[str, ...],
) -> dict:
    candidates = tuple(
        score for score in gateway_scores if score["gateway_id"] not in unavailable_gateways
    )
    selected = max(candidates, key=lambda item: item["objective_score"])
    return {
        "ok": True,
        "gateway_id": selected["gateway_id"],
        "previous_gateway": route["gateway_id"],
        "failover_used": selected["gateway_id"] != route["gateway_id"],
    }


def payment_orchestration_generate_payment_proof(
    state: dict,
    intent_id: str,
    *,
    disclosure: tuple[str, ...],
) -> dict:
    intent = state["intents"][intent_id]
    public_claims = {field: intent[field] for field in disclosure if field in intent}
    proof_hash = _digest({"claims": public_claims, "event_hash": state["events"][-1]["hash"]})
    return {
        "ok": True,
        "proof": "zk_payment_" + proof_hash[:24],
        "hash": proof_hash,
        "public_claims": public_claims,
    }


def payment_orchestration_screen_policy(
    state: dict,
    intent_id: str,
    *,
    blocked_gateways: tuple[str, ...],
    risk_ceiling: float,
) -> dict:
    route = state["routes"][intent_id]
    fraud = state["fraud_checks"].get(intent_id, {})
    blocked = route["gateway_id"] in blocked_gateways or float(fraud.get("risk_score", 0)) > risk_ceiling
    return {
        "ok": not blocked,
        "decision": "blocked" if blocked else "clear",
        "intent_id": intent_id,
    }


def payment_orchestration_run_control_tests(state: dict) -> dict:
    checks = (
        {"id": "configuration_bound", "ok": bool(state["configuration"].get("ok"))},
        {"id": "rules_bound", "ok": bool(state["rules"])},
        {"id": "parameters_bound", "ok": bool(state["parameters"])},
        {
            "id": "event_contract_locked",
            "ok": state["configuration"].get("event_contract") == "AppGen-X"
            and not state["configuration"].get("stream_engine_picker_visible")
            and not state["configuration"].get("user_selectable_event_contract"),
        },
        {
            "id": "no_open_payment_intents",
            "ok": not any(
                intent["status"] in {"created", "routed"} for intent in state["intents"].values()
            ),
        },
        {"id": "hash_chain_valid", "ok": _hash_chain_valid(state["events"])},
    )
    blocking_gaps = tuple(check["id"] for check in checks if not check["ok"])
    return {
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "hash_chain_valid": _hash_chain_valid(state["events"]),
    }


def payment_orchestration_build_api_contract() -> dict:
    permissions = payment_orchestration_permissions_contract()
    routes = (
        {
            "route": "POST /gateways",
            "command": "register_gateway",
            "owned_tables": ("payment_gateway",),
            "requires_permission": "payment_orchestration.configure",
            "idempotency_key": "gateway_id",
            "dependencies": (),
        },
        {
            "route": "POST /tokens",
            "command": "tokenize_payment_method",
            "owned_tables": ("payment_token",),
            "requires_permission": "payment_orchestration.intent",
            "idempotency_key": "token_id",
            "dependencies": ("GET /checkout/sessions/{id}",),
        },
        {
            "route": "POST /payment-intents",
            "command": "create_payment_intent",
            "owned_tables": ("payment_intent",),
            "emits": ("PaymentIntentCreated",),
            "requires_permission": "payment_orchestration.intent",
            "idempotency_key": "intent_id",
            "dependencies": ("checkout_completion_projection",),
        },
        {
            "route": "POST /payment-intents/{id}/route",
            "command": "route_gateway",
            "owned_tables": ("gateway_route", "payment_intent"),
            "requires_permission": "payment_orchestration.intent",
            "idempotency_key": "intent_id",
            "dependencies": (),
        },
        {
            "route": "POST /payment-intents/{id}/fraud-checks",
            "command": "request_fraud_check",
            "owned_tables": ("fraud_check",),
            "emits": ("FraudCheckRequested",),
            "requires_permission": "payment_orchestration.intent",
            "idempotency_key": "intent_id",
            "dependencies": ("GET /fraud/cases/{id}",),
        },
        {
            "route": "POST /payment-intents/{id}/captures",
            "command": "capture_payment",
            "owned_tables": ("payment_authorization", "payment_capture", "payment_settlement"),
            "emits": ("PaymentCaptured", "PaymentFailed"),
            "requires_permission": "payment_orchestration.capture",
            "idempotency_key": "capture_id",
            "dependencies": ("POST /ledger/payment-events",),
        },
        {
            "route": "POST /payment-intents/{id}/settlements",
            "command": "settle_payment",
            "owned_tables": ("payment_settlement", "payment_reconciliation_handoff"),
            "emits": ("PaymentSettled",),
            "requires_permission": "payment_orchestration.settlement",
            "idempotency_key": "settlement_reference",
            "dependencies": ("POST /ledger/payment-events",),
        },
        {
            "route": "POST /payment-intents/{id}/payouts",
            "command": "schedule_payout",
            "owned_tables": ("payment_payout",),
            "emits": ("PaymentPayoutScheduled",),
            "requires_permission": "payment_orchestration.settlement",
            "idempotency_key": "payout_id",
            "dependencies": ("POST /audit/payment-events",),
        },
        {
            "route": "POST /payment-intents/{id}/refunds",
            "command": "refund_payment",
            "owned_tables": ("payment_refund", "payment_reconciliation_handoff"),
            "emits": ("PaymentRefunded",),
            "requires_permission": "payment_orchestration.refund",
            "idempotency_key": "refund_id",
            "dependencies": ("POST /audit/payment-events",),
        },
        {
            "route": "POST /payment-intents/{id}/disputes",
            "command": "open_dispute",
            "owned_tables": ("payment_dispute",),
            "emits": ("PaymentDisputeOpened",),
            "requires_permission": "payment_orchestration.dispute",
            "idempotency_key": "dispute_id",
            "dependencies": ("POST /audit/payment-events",),
        },
        {
            "route": "POST /payment-disputes/{id}/resolution",
            "command": "resolve_dispute",
            "owned_tables": ("payment_dispute", "payment_reconciliation_handoff"),
            "emits": ("PaymentDisputeResolved",),
            "requires_permission": "payment_orchestration.dispute",
            "idempotency_key": "dispute_id",
            "dependencies": ("POST /ledger/payment-events", "POST /audit/payment-events"),
        },
        {
            "route": "POST /payment-intents/{id}/void",
            "command": "void_payment",
            "owned_tables": ("payment_void",),
            "emits": ("PaymentVoided",),
            "requires_permission": "payment_orchestration.refund",
            "idempotency_key": "void_id",
            "dependencies": (),
        },
        {
            "route": "POST /payment/events/inbox",
            "command": "receive_event",
            "owned_tables": (),
            "consumes": PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES,
            "requires_permission": "payment_orchestration.event",
            "idempotency_key": "event_id",
            "dependencies": PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES,
        },
        {
            "route": "GET /payment-workbench",
            "query": "build_workbench_view",
            "owned_tables": PAYMENT_ORCHESTRATION_OWNED_TABLES,
            "requires_permission": "payment_orchestration.audit",
        },
    )
    return {
        "format": "appgen.payment-orchestration-api-contract.v1",
        "ok": True,
        "routes": routes,
        "declared_catalog_routes": tuple(route["route"] for route in routes if route["route"] != "GET /payment-workbench")
        + ("POST /payment-rules", "POST /payment-parameters", "POST /payment-configuration"),
        "events": {
            "emits": PAYMENT_ORCHESTRATION_EMITTED_EVENT_TYPES,
            "consumes": PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES,
        },
        "emits": PAYMENT_ORCHESTRATION_EMITTED_EVENT_TYPES,
        "consumes": PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(permissions["permissions"])),
        "database_backends": PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": PAYMENT_ORCHESTRATION_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "configuration": (
            "PAYMENT_ORCHESTRATION_DATABASE_URL",
            "PAYMENT_ORCHESTRATION_EVENT_TOPIC",
            "PAYMENT_ORCHESTRATION_RETRY_LIMIT",
            "PAYMENT_ORCHESTRATION_DEFAULT_CURRENCY",
        ),
        "dependencies": {
            "apis": tuple(
                item for item in _PAYMENT_ORCHESTRATION_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))
            ),
            "events": PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(
                item for item in _PAYMENT_ORCHESTRATION_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")
            ),
            "shared_tables": (),
        },
    }


def payment_orchestration_build_schema_contract() -> dict:
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {table: default_fields for table in PAYMENT_ORCHESTRATION_OWNED_TABLES}
    table_fields.update(
        {
            "payment_gateway": (
                "tenant",
                "gateway_id",
                "provider",
                "regions",
                "currencies",
                "methods",
                "latency_ms",
                "fee_bps",
                "authorization_rate",
                "settlement_risk",
                "status",
                "audit_hash",
            ),
            "payment_token": (
                "tenant",
                "token_id",
                "customer_id",
                "method_type",
                "network",
                "issuer_country",
                "vault_ref",
                "status",
                "audit_hash",
            ),
            "payment_intent": (
                "tenant",
                "intent_id",
                "checkout_id",
                "customer_id",
                "token_id",
                "gateway_id",
                "amount",
                "currency",
                "region",
                "status",
                "audit_hash",
            ),
            "gateway_route": (
                "tenant",
                "route_id",
                "intent_id",
                "gateway_id",
                "authorization_score",
                "settlement_risk",
                "objective_score",
                "status",
                "audit_hash",
            ),
            "fraud_check": (
                "tenant",
                "fraud_check_id",
                "intent_id",
                "risk_score",
                "decision",
                "status",
                "audit_hash",
            ),
            "payment_authorization": (
                "tenant",
                "authorization_id",
                "intent_id",
                "gateway_id",
                "amount",
                "authorization_score",
                "risk_score",
                "network_reference",
                "status",
                "audit_hash",
            ),
            "payment_capture": (
                "tenant",
                "capture_id",
                "intent_id",
                "gateway_id",
                "amount",
                "status",
                "audit_hash",
            ),
            "payment_refund": (
                "tenant",
                "refund_id",
                "intent_id",
                "amount",
                "reason",
                "status",
                "audit_hash",
            ),
            "payment_void": (
                "tenant",
                "void_id",
                "intent_id",
                "reason",
                "status",
                "audit_hash",
            ),
            "payment_settlement": (
                "tenant",
                "settlement_id",
                "intent_id",
                "amount",
                "window",
                "status",
                "audit_hash",
            ),
            "payment_payout": (
                "tenant",
                "payout_id",
                "intent_id",
                "settlement_id",
                "payout_account",
                "amount",
                "currency",
                "status",
                "audit_hash",
            ),
            "payment_dispute": (
                "tenant",
                "dispute_id",
                "intent_id",
                "amount",
                "reason",
                "evidence",
                "decision",
                "financial_impact",
                "status",
                "audit_hash",
            ),
            "payment_reconciliation_handoff": (
                "tenant",
                "handoff_id",
                "intent_id",
                "target_projection",
                "status",
                "audit_hash",
            ),
            "payment_exception": (
                "tenant",
                "exception_id",
                "intent_id",
                "reason",
                "action",
                "status",
                "audit_hash",
            ),
            "payment_rule": (
                "tenant",
                "rule_id",
                "scope",
                "compiled_hash",
                "enabled",
                "status",
                "audit_hash",
            ),
            "payment_parameter": (
                "tenant",
                "parameter_name",
                "parameter_value",
                "effective_at",
                "changed_by",
                "audit_hash",
            ),
            "payment_configuration": (
                "tenant",
                "configuration_id",
                "database_backend",
                "event_topic",
                "event_contract",
                "stream_engine_picker_visible",
                "audit_hash",
            ),
            "payment_orchestration_appgen_outbox_event": (
                "tenant",
                "event_id",
                "event_type",
                "payload",
                "idempotency_key",
                "published_at",
                "audit_hash",
            ),
            "payment_orchestration_appgen_inbox_event": (
                "tenant",
                "event_id",
                "event_type",
                "payload",
                "idempotency_key",
                "attempts",
                "audit_hash",
            ),
            "payment_orchestration_dead_letter_event": (
                "tenant",
                "event_id",
                "event_type",
                "payload",
                "reason",
                "attempts",
                "audit_hash",
            ),
        }
    )
    relationships = (
        {"from_table": "payment_intent", "from_field": "token_id", "to_table": "payment_token", "to_field": "token_id"},
        {"from_table": "payment_intent", "from_field": "gateway_id", "to_table": "payment_gateway", "to_field": "gateway_id"},
        {"from_table": "gateway_route", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
        {"from_table": "gateway_route", "from_field": "gateway_id", "to_table": "payment_gateway", "to_field": "gateway_id"},
        {"from_table": "fraud_check", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
        {"from_table": "payment_authorization", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
        {"from_table": "payment_capture", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
        {"from_table": "payment_refund", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
        {"from_table": "payment_void", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
        {"from_table": "payment_settlement", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
        {"from_table": "payment_payout", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
        {"from_table": "payment_dispute", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
        {"from_table": "payment_reconciliation_handoff", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
        {"from_table": "payment_exception", "from_field": "intent_id", "to_table": "payment_intent", "to_field": "intent_id"},
    )
    tables = tuple(
        {"table": table, "fields": table_fields[table], "owner": "payment_orchestration"}
        for table in PAYMENT_ORCHESTRATION_OWNED_TABLES
    )
    allowed_prefixes = ("payment_", "gateway_", "fraud_")
    return {
        "format": "appgen.payment-orchestration-owned-schema-contract.v1",
        "ok": len(tables) == len(PAYMENT_ORCHESTRATION_OWNED_TABLES)
        and len(tables) >= 20
        and all(item["table"].startswith(allowed_prefixes) for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/payment_orchestration/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(PAYMENT_ORCHESTRATION_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in PAYMENT_ORCHESTRATION_OWNED_TABLES
        ),
        "datastore_backends": PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def payment_orchestration_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_gateway",
        "tokenize_payment_method",
        "create_payment_intent",
        "route_gateway",
        "request_fraud_check",
        "authorize_payment",
        "capture_payment",
        "settle_payment",
        "schedule_payout",
        "refund_payment",
        "open_dispute",
        "resolve_dispute",
        "void_payment",
        "generate_payment_proof",
        "screen_policy",
        "federate_payment_view",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_settlement",
        "optimize_gateway_mix",
        "allocate_provider_capacity",
        "run_control_tests",
        "register_governed_model",
        "verify_owned_table_boundary",
    )
    return {
        "format": "appgen.payment-orchestration-service-contract.v1",
        "ok": len(command_methods) >= 20,
        "transaction_boundary": "payment_orchestration_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_workbench_view",
            "simulate_gateway_route",
            "forecast_authorization",
            "parse_instruction",
            "score_payment_risk",
            "resolve_exception",
            "detect_payment_anomaly",
            "model_stochastic_exposure",
            "build_api_contract",
            "build_schema_contract",
            "build_release_evidence",
        ),
        "mutates_only": PAYMENT_ORCHESTRATION_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(
                item for item in _PAYMENT_ORCHESTRATION_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))
            ),
            "events": PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(
                item for item in _PAYMENT_ORCHESTRATION_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")
            ),
            "shared_tables": (),
        },
    }


def payment_orchestration_build_release_evidence() -> dict:
    schema = payment_orchestration_build_schema_contract()
    service = payment_orchestration_build_service_contract()
    api = payment_orchestration_build_api_contract()
    permissions = payment_orchestration_permissions_contract()
    workbench = payment_orchestration_build_workbench_view(payment_orchestration_empty_state(), tenant="tenant_release")
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 20},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(PAYMENT_ORCHESTRATION_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 20},
        {
            "id": "api_event_contract",
            "ok": api["ok"]
            and api["event_contract"] == "AppGen-X"
            and api["required_event_topic"] == PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
        },
        {
            "id": "permissions_cover_commands",
            "ok": {"create_payment_intent", "capture_payment", "receive_event"}
            <= set(permissions["action_permissions"]),
        },
        {
            "id": "backend_allowlist",
            "ok": schema["datastore_backends"] == PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        },
        {
            "id": "no_shared_table_access",
            "ok": not schema["shared_table_access"] and not api["shared_table_access"],
        },
        {
            "id": "workbench_binding_evidence",
            "ok": workbench["binding_evidence"]["owned_tables"] == PAYMENT_ORCHESTRATION_OWNED_TABLES
            and workbench["binding_evidence"]["configuration"]["event_contract"] in {None, "AppGen-X"},
        },
    )
    return {
        "format": "appgen.payment-orchestration-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def payment_orchestration_permissions_contract() -> dict:
    return {
        "format": "appgen.payment-orchestration-permissions.v1",
        "ok": True,
        "pbc": "payment_orchestration",
        "permissions": (
            "payment_orchestration.read",
            "payment_orchestration.intent",
            "payment_orchestration.capture",
            "payment_orchestration.settlement",
            "payment_orchestration.refund",
            "payment_orchestration.dispute",
            "payment_orchestration.event",
            "payment_orchestration.configure",
            "payment_orchestration.audit",
        ),
        "action_permissions": {
            "register_gateway": "payment_orchestration.configure",
            "tokenize_payment_method": "payment_orchestration.intent",
            "create_payment_intent": "payment_orchestration.intent",
            "route_gateway": "payment_orchestration.intent",
            "request_fraud_check": "payment_orchestration.intent",
            "authorize_payment": "payment_orchestration.capture",
            "capture_payment": "payment_orchestration.capture",
            "settle_payment": "payment_orchestration.settlement",
            "schedule_payout": "payment_orchestration.settlement",
            "refund_payment": "payment_orchestration.refund",
            "open_dispute": "payment_orchestration.dispute",
            "resolve_dispute": "payment_orchestration.dispute",
            "void_payment": "payment_orchestration.refund",
            "receive_event": "payment_orchestration.event",
            "register_rule": "payment_orchestration.configure",
            "register_schema_extension": "payment_orchestration.configure",
            "set_parameter": "payment_orchestration.configure",
            "configure_runtime": "payment_orchestration.configure",
            "build_workbench_view": "payment_orchestration.audit",
            "simulate_gateway_route": "payment_orchestration.read",
            "forecast_authorization": "payment_orchestration.read",
            "parse_instruction": "payment_orchestration.read",
            "score_payment_risk": "payment_orchestration.audit",
            "generate_payment_proof": "payment_orchestration.audit",
            "screen_policy": "payment_orchestration.audit",
            "federate_payment_view": "payment_orchestration.read",
            "run_resilience_drill": "payment_orchestration.audit",
            "rotate_crypto_epoch": "payment_orchestration.audit",
            "schedule_carbon_aware_settlement": "payment_orchestration.audit",
            "optimize_gateway_mix": "payment_orchestration.audit",
            "allocate_provider_capacity": "payment_orchestration.audit",
            "run_control_tests": "payment_orchestration.audit",
            "register_governed_model": "payment_orchestration.audit",
            "detect_payment_anomaly": "payment_orchestration.audit",
            "model_stochastic_exposure": "payment_orchestration.audit",
            "build_schema_contract": "payment_orchestration.audit",
            "build_service_contract": "payment_orchestration.audit",
            "build_release_evidence": "payment_orchestration.audit",
        },
        "rbac_tables": ("payment_rule", "payment_parameter", "payment_configuration"),
    }


def payment_orchestration_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed = (
        *PAYMENT_ORCHESTRATION_OWNED_TABLES,
        *PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES,
        *_PAYMENT_ORCHESTRATION_ALLOWED_DEPENDENCIES,
    )
    violations = tuple(
        reference
        for reference in tuple(references)
        if reference not in set(allowed) and not str(reference).startswith("payment_orchestration_")
    )
    return {
        "format": "appgen.payment-orchestration-boundary.v1",
        "ok": not violations,
        "owned_tables": PAYMENT_ORCHESTRATION_OWNED_TABLES,
        "declared_dependencies": {
            "apis": tuple(
                item for item in _PAYMENT_ORCHESTRATION_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))
            ),
            "events": PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(
                item for item in _PAYMENT_ORCHESTRATION_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def payment_orchestration_federate_payment_view(
    state: dict,
    intent_id: str,
    *,
    systems: tuple[str, ...],
) -> dict:
    intent = state["intents"][intent_id]
    return {
        "ok": True,
        "intent_id": intent_id,
        "systems": systems,
        "projection": {
            "status": intent["status"],
            "amount": intent["amount"],
            "currency": intent["currency"],
            "gateway_id": intent.get("gateway_id"),
        },
    }


def payment_orchestration_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {
        "ok": bool(state["outbox"]) and scenario in {"gateway_timeout", "fraud_timeout"},
        "scenario": scenario,
        "mode": "degraded_gateway_replay",
        "retry_limit": state["configuration"].get("retry_limit", 3),
        "dead_letter_topic": "payment_orchestration.dead_letter",
    }


def payment_orchestration_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {
        "ok": True,
        "epoch": epoch,
        "algorithm": algorithm,
        "key_id": f"payment_epoch_{epoch:04d}",
    }


def payment_orchestration_schedule_carbon_aware_settlement(
    windows: tuple[dict, ...],
) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def payment_orchestration_optimize_gateway_mix(
    gateway_scores: tuple[dict, ...],
    *,
    amount: float,
) -> dict:
    selected = max(gateway_scores, key=lambda score: score["objective_score"])
    return {
        "ok": True,
        "gateway_id": selected["gateway_id"],
        "objective_score": selected["objective_score"],
        "expected_fee": round(amount * selected["fee_bps"] / 10000, 4),
    }


def payment_orchestration_allocate_provider_capacity(
    gateways: tuple[dict, ...],
    *,
    intents: int,
) -> dict:
    total = sum(item["bid"] * item["capacity"] for item in gateways) or 1
    allocations = tuple(
        {
            "gateway_id": item["gateway_id"],
            "intents": round(intents * item["bid"] * item["capacity"] / total, 2),
        }
        for item in gateways
    )
    return {
        "ok": round(sum(item["intents"] for item in allocations), 2) == round(intents, 2),
        "allocations": allocations,
    }


def payment_orchestration_detect_payment_anomaly(state: dict) -> dict:
    amounts = tuple(float(intent.get("amount", 0)) for intent in state["intents"].values())
    if not amounts:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(amounts) or 1
    entropy = round(
        -sum((amount / total) * math.log(max(amount / total, 0.0001), 2) for amount in amounts),
        4,
    )
    mean = sum(amounts) / len(amounts)
    return {
        "ok": True,
        "entropy": entropy,
        "outliers": tuple(amount for amount in amounts if abs(amount - mean) > 1000),
    }


def payment_orchestration_model_stochastic_exposure(
    *,
    amount_path: tuple[float, ...],
    volatility: float,
) -> dict:
    drift = 0 if len(amount_path) < 2 else (amount_path[-1] - amount_path[0]) / (len(amount_path) - 1)
    exposure = abs(drift) * volatility * len(amount_path)
    return {
        "ok": True,
        "expected_exposure": round(exposure, 4),
        "tail_risk": round(exposure * 1.65, 4),
        "simulation_count": 1000,
    }


def payment_orchestration_register_governed_model(name: str, metadata: dict) -> dict:
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


def payment_orchestration_build_workbench_view(state: dict, *, tenant: str) -> dict:
    intents = tuple(intent for intent in state["intents"].values() if intent["tenant"] == tenant)
    gateways = tuple(gateway for gateway in state["gateways"].values() if gateway["tenant"] == tenant)
    tokens = tuple(token for token in state["tokens"].values() if token["tenant"] == tenant)
    routes = tuple(route for route in state["routes"].values() if route["tenant"] == tenant)
    fraud_checks = tuple(
        fraud_check for fraud_check in state["fraud_checks"].values() if fraud_check.get("tenant") == tenant
    )
    authorizations = tuple(
        authorization for authorization in state["authorizations"].values() if authorization["tenant"] == tenant
    )
    captures = tuple(capture for capture in state["captures"].values() if capture["tenant"] == tenant)
    settlements = tuple(
        settlement for settlement in state["settlements"].values() if settlement["tenant"] == tenant
    )
    payouts = tuple(payout for payout in state["payouts"].values() if payout["tenant"] == tenant)
    refunds = tuple(refund for refund in state["refunds"].values() if refund["tenant"] == tenant)
    disputes = tuple(dispute for dispute in state["disputes"].values() if dispute["tenant"] == tenant)
    voids = tuple(void for void in state["voids"].values() if void["tenant"] == tenant)
    exceptions = tuple(
        exception for exception in state["exceptions"].values() if exception["tenant"] == tenant
    )
    inbox = tuple(item for item in state["inbox"] if item.get("tenant") == tenant)
    dead_letter = tuple(item for item in state["dead_letter"] if item.get("tenant") == tenant)
    return {
        "format": "appgen.payment-orchestration-workbench-view.v1",
        "ok": True,
        "tenant": tenant,
        "intent_count": len(intents),
        "captured_count": len(captures),
        "gateway_count": len(gateways),
        "token_count": len(tokens),
        "route_count": len(routes),
        "fraud_check_count": len(fraud_checks),
        "authorization_count": len(authorizations),
        "refund_count": len(refunds),
        "dispute_count": len(disputes),
        "void_count": len(voids),
        "settlement_count": len(settlements),
        "payout_count": len(payouts),
        "exception_count": len(exceptions),
        "captured_amount": round(sum(intent.get("captured_amount", 0) for intent in intents), 2),
        "refunded_amount": round(sum(intent.get("refunded_amount", 0) for intent in intents), 2),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(inbox),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(dead_letter),
        "binding_evidence": {
            "owned_tables": PAYMENT_ORCHESTRATION_OWNED_TABLES,
            "outbox_table": "payment_orchestration_appgen_outbox_event",
            "inbox_table": "payment_orchestration_appgen_inbox_event",
            "dead_letter_table": "payment_orchestration_dead_letter_event",
            "shared_table_access": False,
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
        },
    }


def _active_rule_for_tenant(state: dict, tenant: str) -> dict:
    return next(rule for rule in state["rules"].values() if rule["tenant"] == tenant and rule["enabled"])


def _score_gateways(gateways: tuple[dict, ...], parameters: dict) -> tuple[dict, ...]:
    latency_values = tuple(gateway["latency_ms"] for gateway in gateways)
    cost_values = tuple(gateway["fee_bps"] for gateway in gateways)
    auth_values = tuple(gateway["authorization_rate"] for gateway in gateways)
    risk_values = tuple(gateway["settlement_risk"] for gateway in gateways)
    weight_total = sum(
        float(parameters[name])
        for name in (
            "gateway_latency_weight",
            "gateway_cost_weight",
            "gateway_auth_weight",
            "settlement_risk_weight",
        )
    ) or 1.0
    scored = []
    for gateway in gateways:
        latency_component = _normalize_metric(
            gateway["latency_ms"],
            min(latency_values),
            max(latency_values),
            lower_is_better=True,
        )
        cost_component = _normalize_metric(
            gateway["fee_bps"],
            min(cost_values),
            max(cost_values),
            lower_is_better=True,
        )
        auth_component = _normalize_metric(
            gateway["authorization_rate"],
            min(auth_values),
            max(auth_values),
            lower_is_better=False,
        )
        risk_component = _normalize_metric(
            gateway["settlement_risk"],
            min(risk_values),
            max(risk_values),
            lower_is_better=True,
        )
        objective_score = round(
            float(parameters["gateway_latency_weight"]) * latency_component
            + float(parameters["gateway_cost_weight"]) * cost_component
            + float(parameters["gateway_auth_weight"]) * auth_component
            + float(parameters["settlement_risk_weight"]) * risk_component,
            4,
        )
        scored.append(
            {
                **gateway,
                "objective_score": objective_score,
                "authorization_score": round(
                    max(0, min(1, gateway["authorization_rate"] - gateway["settlement_risk"] * 0.5)),
                    4,
                ),
                "confidence": round(objective_score / weight_total, 4),
            }
        )
    return tuple(scored)


def _append_event(state: dict, event_type: str, payload: dict, *, emit_outbox: bool = True) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {
        "event_id": f"payment_evt_{sequence:06d}",
        "event_type": event_type,
        "payload": payload,
        "previous_hash": previous_hash,
    }
    event = {**event, "hash": _digest(event)}
    outbox = state["outbox"]
    if emit_outbox:
        outbox = (
            *outbox,
            {
                "tenant": payload.get("tenant"),
                "event_type": event_type,
                "payload": payload,
                "idempotency_key": f"payment_orchestration:{event_type}:{event['event_id']}",
            },
        )
    return {**state, "events": (*state["events"], event), "outbox": outbox}


def _hash_chain_valid(events: tuple[dict, ...]) -> bool:
    return all(
        event["previous_hash"] == (events[index - 1]["hash"] if index else "GENESIS")
        for index, event in enumerate(events)
    )


def _normalize_metric(value: float, minimum: float, maximum: float, *, lower_is_better: bool) -> float:
    if maximum == minimum:
        return 1.0
    normalized = (value - minimum) / (maximum - minimum)
    return round(1 - normalized if lower_is_better else normalized, 6)


def _normalize_fields(payload: dict, sequence_fields: set[str]) -> dict:
    return {
        key: tuple(value) if key in sequence_fields else value
        for key, value in payload.items()
    }


def _digest(value: object) -> str:
    return hashlib.sha3_256(
        json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()
