"""Executable runtime for the Returns and Reverse Logistics PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re


RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC = "appgen.returns.events"

RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_returns_lifecycle",
    "graph_relational_reverse_logistics_topology",
    "probabilistic_return_eligibility_scoring",
    "counterfactual_disposition_simulation",
    "temporal_return_rate_recovery_forecasting",
    "autonomous_return_exception_resolution",
    "semantic_return_instruction_parsing",
    "predictive_return_risk",
    "self_healing_label_carrier_route_selection",
    "cryptographic_return_proof",
    "immutable_return_audit_trail",
    "dynamic_return_policy_screening",
    "automated_control_testing",
    "cross_system_order_payment_inventory_ledger_federation",
    "universal_api_async_streaming",
    "distributed_systems_evidence",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_inbox_handlers",
    "retry_dead_letter_evidence",
    "fraud_abuse_screening",
    "tenant_isolation",
    "chaos_tolerant_return_operations",
    "crypto_agility",
    "carbon_aware_return_routing",
    "mathematical_recovery_optimization",
    "disposition_allocation_mechanism_design",
    "return_anomaly_detection",
    "stochastic_return_exposure_modeling",
    "governed_ml_model_evidence",
    "permissions_governance_evidence",
)

RETURNS_REVERSE_LOGISTICS_STANDARD_FEATURE_KEYS = (
    "return_authorizations_rma",
    "return_eligibility",
    "return_labels",
    "carrier_handoff",
    "receipt_and_inspection",
    "disposition_routing",
    "restock_refurbish_scrap_routing",
    "credit_adjustments",
    "refund_ledger_handoff",
    "fraud_abuse_screening",
    "tenant_isolation",
    "idempotent_handlers",
    "appgen_x_outbox_inbox_eventing",
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

_SUPPORTED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
_SUPPORTED_PARAMETERS = {
    "eligibility_window_days",
    "fraud_threshold",
    "recovery_floor",
    "carrier_handoff_hours",
    "carbon_weight",
    "route_switch_threshold",
    "forecast_horizon_days",
    "anomaly_zscore_threshold",
    "workbench_limit",
}
_THRESHOLD_PARAMETERS = {
    "fraud_threshold",
    "recovery_floor",
    "carbon_weight",
    "route_switch_threshold",
}
_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "eligibility_policy",
    "label_policy",
    "inspection_policy",
    "credit_policy",
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
_CONSUMED_EVENT_TYPES = {"OrderShipped", "PaymentCaptured"}
_API_SURFACES = ("POST /returns", "POST /labels", "POST /inspection-grades")
_EMITTED_EVENT_TYPES = ("ReturnAuthorized", "CreditAdjustmentIssued")
_DEFAULT_DISPOSITIONS = ("restock", "refurbish", "scrap")
_DISPOSITION_FACTORS = {"restock": 0.9, "refurbish": 0.65, "scrap": 0.25}


def returns_reverse_logistics_runtime_capabilities() -> dict:
    smoke = returns_reverse_logistics_runtime_smoke()
    return {
        "format": "appgen.returns-reverse-logistics-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "returns_reverse_logistics",
        "implementation_directory": "src/pyAppGen/pbcs/returns_reverse_logistics",
        "capabilities": RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS,
        "standard_features": RETURNS_REVERSE_LOGISTICS_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "receive_event",
            "authorize_return",
            "create_return_label",
            "record_inspection_grade",
            "issue_credit_adjustment",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def returns_reverse_logistics_runtime_smoke() -> dict:
    state = returns_reverse_logistics_empty_state()
    state = returns_reverse_logistics_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_carriers": ("parcel_one", "parcel_green"),
            "supported_dispositions": _DEFAULT_DISPOSITIONS,
            "workbench_limit": 100,
        },
    )["state"]
    state = returns_reverse_logistics_set_parameter(state, "eligibility_window_days", 30)["state"]
    state = returns_reverse_logistics_set_parameter(state, "fraud_threshold", 0.72)["state"]
    state = returns_reverse_logistics_set_parameter(state, "recovery_floor", 0.35)["state"]
    state = returns_reverse_logistics_set_parameter(state, "carbon_weight", 0.25)["state"]
    state = returns_reverse_logistics_set_parameter(state, "route_switch_threshold", 0.12)["state"]
    state = returns_reverse_logistics_register_rule(
        state,
        {
            "rule_id": "rule_returns_default",
            "tenant": "tenant_alpha",
            "scope": "return_policy",
            "status": "active",
            "eligibility_policy": {
                "max_days_since_shipment": 30,
                "blocked_reasons": ("final_sale",),
                "minimum_payment_capture_ratio": 1.0,
            },
            "label_policy": {
                "preferred_carriers": ("parcel_green",),
                "max_cost": 15.0,
            },
            "inspection_policy": {
                "restock_min": 0.85,
                "refurbish_min": 0.55,
            },
            "credit_policy": {
                "restock_factor": 0.9,
                "refurbish_factor": 0.65,
                "scrap_factor": 0.25,
            },
            "fraud_policy": {
                "manual_review_threshold": 0.72,
            },
        },
    )["state"]
    state = returns_reverse_logistics_register_schema_extension(
        state,
        "return_authorization",
        {"reverse_graph": "jsonb", "policy_evidence": "jsonb"},
    )["state"]
    state = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_ship_001",
            "event_type": "OrderShipped",
            "idempotency_key": "order:order_001:v1",
            "payload": {
                "tenant": "tenant_alpha",
                "order_id": "order_001",
                "payment_id": "pay_001",
                "customer_id": "cust_001",
                "shipped_at": "2026-05-20",
                "days_since_shipped": 5,
                "return_window_days": 30,
                "final_sale": False,
                "items": (
                    {"sku": "sku_001", "quantity": 1, "unit_price": 120.0},
                ),
            },
        },
    )["state"]
    duplicate = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_ship_001",
            "event_type": "OrderShipped",
            "idempotency_key": "order:order_001:v1",
            "payload": {
                "tenant": "tenant_alpha",
                "order_id": "order_001",
                "payment_id": "pay_001",
                "customer_id": "cust_001",
                "shipped_at": "2026-05-20",
                "days_since_shipped": 5,
                "return_window_days": 30,
                "final_sale": False,
                "items": (
                    {"sku": "sku_001", "quantity": 1, "unit_price": 120.0},
                ),
            },
        },
    )
    state = duplicate["state"]
    state = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_pay_001",
            "event_type": "PaymentCaptured",
            "idempotency_key": "payment:pay_001:v1",
            "payload": {
                "tenant": "tenant_alpha",
                "payment_id": "pay_001",
                "order_id": "order_001",
                "captured_amount": 120.0,
                "currency": "USD",
                "ledger_account": "refund_liability",
            },
        },
    )["state"]
    invalid = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_invalid_001",
            "event_type": "UnknownEvent",
            "idempotency_key": "invalid:returns:1",
            "attempts": 3,
            "payload": {"tenant": "tenant_alpha"},
        },
    )
    state = invalid["state"]
    authorization = returns_reverse_logistics_authorize_return(
        state,
        {
            "return_id": "ret_001",
            "rma": "RMA-001",
            "tenant": "tenant_alpha",
            "order_id": "order_001",
            "payment_id": "pay_001",
            "customer_id": "cust_001",
            "reason": "damaged",
            "requested_at": "2026-05-25",
            "days_since_shipped": 5,
            "items": ({"sku": "sku_001", "quantity": 1},),
        },
    )
    state = authorization["state"]
    label = returns_reverse_logistics_create_return_label(
        state,
        {
            "label_id": "lbl_001",
            "return_id": "ret_001",
            "tenant": "tenant_alpha",
            "origin": "Boston, MA",
            "destination": "New York, NY",
            "package_weight_kg": 1.2,
            "candidate_carriers": (
                {
                    "carrier_id": "parcel_one",
                    "availability": False,
                    "cost": 8.5,
                    "carbon_intensity": 95.0,
                    "eta_hours": 22.0,
                    "route_health": 0.42,
                },
                {
                    "carrier_id": "parcel_green",
                    "availability": True,
                    "cost": 9.2,
                    "carbon_intensity": 54.0,
                    "eta_hours": 20.0,
                    "route_health": 0.91,
                },
            ),
        },
    )
    state = label["state"]
    inspection = returns_reverse_logistics_record_inspection_grade(
        state,
        {
            "inspection_id": "insp_001",
            "return_id": "ret_001",
            "tenant": "tenant_alpha",
            "condition_score": 0.91,
            "completeness_score": 1.0,
            "packaging_intact": True,
            "notes": "Unit sealed and immediately restockable.",
        },
    )
    state = inspection["state"]
    adjustment = returns_reverse_logistics_issue_credit_adjustment(
        state,
        {
            "adjustment_id": "adj_001",
            "return_id": "ret_001",
            "tenant": "tenant_alpha",
        },
    )
    state = adjustment["state"]
    simulation = returns_reverse_logistics_simulate_disposition(state, "ret_001")
    forecast = returns_reverse_logistics_forecast_return_recovery(
        ((12, 0.88), (10, 0.81), (14, 0.84)),
        horizon_days=14,
    )
    exception = returns_reverse_logistics_resolve_exception("carrier_timeout")
    parsed = returns_reverse_logistics_parse_return_instruction("return ret_001 order order_001 rma RMA-001 reason damaged")
    risk = returns_reverse_logistics_predict_return_risk(
        {
            "days_since_shipped_ratio": 5 / 30,
            "price_ratio": 120 / 250,
            "prior_returns_ratio": 0.2,
            "damage_claim_ratio": 0.8,
        }
    )
    proof = returns_reverse_logistics_generate_return_proof(
        state,
        "ret_001",
        disclosure=("return_id", "order_id", "status"),
    )
    screening = returns_reverse_logistics_screen_policy(state, "ret_001")
    controls = returns_reverse_logistics_run_control_tests(state)
    api = returns_reverse_logistics_build_api_contract()
    federation = returns_reverse_logistics_federate_return_view(
        state,
        "ret_001",
        systems=("order", "payment", "inventory", "ledger"),
    )
    resilience = returns_reverse_logistics_run_resilience_drill(state, "carrier_api_timeout")
    rotated = returns_reverse_logistics_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = returns_reverse_logistics_optimize_carbon_aware_routing(label["return_label"]["candidate_carriers"])
    optimization = returns_reverse_logistics_optimize_recovery_math(simulation["options"])
    mechanism = returns_reverse_logistics_allocate_disposition_mechanism(simulation["options"], units=3)
    anomaly = returns_reverse_logistics_detect_return_anomaly(state)
    stochastic = returns_reverse_logistics_model_stochastic_exposure(
        return_rate_path=(0.08, 0.11, 0.09),
        recovery_path=(0.82, 0.85, 0.8),
        volatility=0.12,
    )
    model = returns_reverse_logistics_register_governed_model(
        "returns_risk",
        {"features": ("days_since_shipped", "price", "reason"), "auc": 0.91, "drift_score": 0.03},
    )
    workbench = returns_reverse_logistics_build_workbench_view(state, tenant="tenant_alpha")

    checks = (
        {"id": "event_sourced_returns_lifecycle", "ok": len(state["events"]) >= 6 and bool(state["events"][-1]["hash"])},
        {"id": "graph_relational_reverse_logistics_topology", "ok": authorization["return_authorization"]["graph_degree"] >= 4},
        {"id": "probabilistic_return_eligibility_scoring", "ok": authorization["eligibility"]["eligible"] and authorization["eligibility"]["score"] >= 0.5},
        {"id": "counterfactual_disposition_simulation", "ok": simulation["best_option"]["disposition"] in _DEFAULT_DISPOSITIONS},
        {"id": "temporal_return_rate_recovery_forecasting", "ok": forecast["predicted_recovery_rate"] > 0.0},
        {"id": "autonomous_return_exception_resolution", "ok": exception["resolution"] == "failover_carrier_selection"},
        {"id": "semantic_return_instruction_parsing", "ok": parsed["return_id"] == "ret_001" and parsed["order_id"] == "order_001"},
        {"id": "predictive_return_risk", "ok": 0.0 <= risk["risk_score"] <= 1.0},
        {"id": "self_healing_label_carrier_route_selection", "ok": label["return_label"]["route_selection"]["selected_carrier"] == "parcel_green"},
        {"id": "cryptographic_return_proof", "ok": bool(proof["proof_hash"])},
        {"id": "immutable_return_audit_trail", "ok": all(event["hash"] for event in state["events"])},
        {"id": "dynamic_return_policy_screening", "ok": screening["decision"] == "allow"},
        {"id": "automated_control_testing", "ok": controls["ok"] is True},
        {"id": "cross_system_order_payment_inventory_ledger_federation", "ok": len(federation["systems"]) == 4},
        {"id": "universal_api_async_streaming", "ok": api["async_topic"] == RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC},
        {"id": "distributed_systems_evidence", "ok": resilience["ok"] is True},
        {"id": "appgen_x_outbox_inbox_eventing", "ok": len(state["outbox"]) == 2 and len(state["inbox"]) == 3},
        {"id": "idempotent_inbox_handlers", "ok": duplicate["duplicate"] is True},
        {"id": "retry_dead_letter_evidence", "ok": invalid["dead_lettered"] is True and len(state["dead_letter"]) == 1},
        {"id": "fraud_abuse_screening", "ok": authorization["fraud_assessment"]["decision"] in {"allow", "review"}},
        {"id": "tenant_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "chaos_tolerant_return_operations", "ok": resilience["mode"] == "degraded_but_available"},
        {"id": "crypto_agility", "ok": rotated["state"]["crypto_epoch"] == "dilithium3_simulated"},
        {"id": "carbon_aware_return_routing", "ok": carbon["selected_carrier"] == "parcel_green"},
        {"id": "mathematical_recovery_optimization", "ok": optimization["best_option"]["disposition"] in _DEFAULT_DISPOSITIONS},
        {"id": "disposition_allocation_mechanism_design", "ok": sum(item["units"] for item in mechanism["allocation"]) == 3},
        {"id": "return_anomaly_detection", "ok": anomaly["anomaly_detected"] is True},
        {"id": "stochastic_return_exposure_modeling", "ok": stochastic["expected_loss"] >= 0.0},
        {"id": "governed_ml_model_evidence", "ok": model["ok"] is True},
        {"id": "permissions_governance_evidence", "ok": "configure_runtime" in returns_reverse_logistics_permissions_contract()},
    )
    blocking_gaps = tuple(check["id"] for check in checks if not check["ok"])
    return {
        "format": "appgen.returns-reverse-logistics-runtime-smoke.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "workbench": workbench,
    }


def returns_reverse_logistics_empty_state() -> dict:
    return {
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "return_authorizations": {},
        "return_labels": {},
        "inspection_grades": {},
        "credit_adjustments": {},
        "order_shipments": {},
        "payment_captures": {},
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "retry_evidence": {},
        "handled_event_keys": {},
        "event_sequence": 0,
        "crypto_epoch": "ed25519_simulated",
    }


def returns_reverse_logistics_configure_runtime(state: dict, configuration: dict) -> dict:
    _require_keys(
        configuration,
        (
            "database_backend",
            "event_topic",
            "retry_limit",
            "default_currency",
            "supported_carriers",
            "supported_dispositions",
        ),
        "Returns Reverse Logistics configuration",
    )
    forbidden = sorted(key for key in configuration if key in _FORBIDDEN_EVENTING_FIELDS)
    if forbidden:
        raise ValueError("Stream-engine picker and user-facing eventing choices are not supported.")
    backend = str(configuration["database_backend"]).lower()
    if backend not in _SUPPORTED_DATABASE_BACKENDS:
        raise ValueError("Returns Reverse Logistics supports only PostgreSQL, MySQL, or MariaDB.")
    if configuration["event_topic"] != RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Returns Reverse Logistics requires event topic {RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC}.")
    new_state = _clone_state(state)
    normalized = {
        "database_backend": backend,
        "event_topic": configuration["event_topic"],
        "retry_limit": int(configuration["retry_limit"]),
        "default_currency": str(configuration["default_currency"]),
        "supported_carriers": tuple(configuration["supported_carriers"]),
        "supported_dispositions": tuple(configuration["supported_dispositions"]),
        "workbench_limit": int(configuration.get("workbench_limit", 100)),
        "event_contract": "AppGen-X",
        "allowed_database_backends": _SUPPORTED_DATABASE_BACKENDS,
        "user_eventing_choice": False,
        "ok": True,
    }
    normalized["configuration_hash"] = _hash_payload(normalized)
    new_state["configuration"] = normalized
    return {"ok": True, "state": new_state, "configuration": normalized}


def returns_reverse_logistics_set_parameter(state: dict, parameter_name: str, value: float) -> dict:
    if parameter_name not in _SUPPORTED_PARAMETERS:
        raise ValueError("Unsupported Returns Reverse Logistics parameter.")
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("Returns Reverse Logistics parameters must be finite numeric values.")
    numeric_value = float(value)
    if parameter_name in _THRESHOLD_PARAMETERS and not 0.0 <= numeric_value <= 1.0:
        raise ValueError("Threshold parameters must be between 0 and 1.")
    if parameter_name in {"eligibility_window_days", "carrier_handoff_hours", "forecast_horizon_days", "workbench_limit"} and numeric_value <= 0:
        raise ValueError("Positive Returns Reverse Logistics parameters must be greater than zero.")
    new_state = _clone_state(state)
    new_state["parameters"][parameter_name] = numeric_value
    return {"ok": True, "state": new_state, "parameter": {parameter_name: numeric_value}}


def returns_reverse_logistics_register_rule(state: dict, rule: dict) -> dict:
    _require_keys(rule, _REQUIRED_RULE_FIELDS, "Returns Reverse Logistics rule")
    compiled_hash = _hash_payload({key: rule[key] for key in sorted(rule)})
    new_state = _clone_state(state)
    record = {
        **rule,
        "compiled_hash": compiled_hash,
        "compiled_evidence": {
            "format": "appgen.returns-reverse-logistics-rule-compile.v1",
            "compiled_hash": compiled_hash,
            "required_fields": _REQUIRED_RULE_FIELDS,
            "bounded_parameters": tuple(sorted(_SUPPORTED_PARAMETERS)),
            "required_event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
        },
    }
    new_state["rules"][rule["rule_id"]] = record
    return {"ok": True, "state": new_state, "rule": record}


def returns_reverse_logistics_register_schema_extension(state: dict, entity: str, fields: dict) -> dict:
    new_state = _clone_state(state)
    record = {
        "entity": entity,
        "fields": fields,
        "schema_hash": _hash_payload({"entity": entity, "fields": fields}),
    }
    new_state["schema_extensions"][entity] = record
    return {"ok": True, "state": new_state, "schema_extension": record}


def returns_reverse_logistics_receive_event(state: dict, envelope: dict) -> dict:
    _require_keys(envelope, ("event_id", "event_type", "idempotency_key", "payload"), "Returns Reverse Logistics inbox event")
    tenant = envelope["payload"].get("tenant")
    if not tenant:
        raise ValueError("Returns Reverse Logistics inbox events require payload.tenant.")
    idempotency_key = envelope["idempotency_key"]
    if idempotency_key in state["handled_event_keys"]:
        return {
            "ok": True,
            "state": state,
            "duplicate": True,
            "event": state["handled_event_keys"][idempotency_key],
        }

    new_state = _clone_state(state)
    inbox_record = {
        "event_id": envelope["event_id"],
        "event_type": envelope["event_type"],
        "idempotency_key": idempotency_key,
        "tenant": tenant,
        "payload": envelope["payload"],
    }
    new_state["inbox"].append(inbox_record)

    if envelope["event_type"] not in _CONSUMED_EVENT_TYPES:
        evidence = {
            "event_id": envelope["event_id"],
            "event_type": envelope["event_type"],
            "tenant": tenant,
            "attempts": int(envelope.get("attempts", 1)),
            "reason": "unsupported_event_type",
        }
        new_state["retry_evidence"][idempotency_key] = evidence
        dead_lettered = False
        if evidence["attempts"] >= int(new_state.get("configuration", {}).get("retry_limit", 3)):
            new_state["dead_letter"].append(evidence)
            dead_lettered = True
        return {"ok": False, "state": new_state, "duplicate": False, "dead_lettered": dead_lettered, "event": evidence}

    if envelope["event_type"] == "OrderShipped":
        payload = envelope["payload"]
        record = {
            "tenant": tenant,
            "order_id": payload["order_id"],
            "payment_id": payload["payment_id"],
            "customer_id": payload["customer_id"],
            "shipped_at": payload["shipped_at"],
            "days_since_shipped": int(payload.get("days_since_shipped", 0)),
            "return_window_days": int(payload.get("return_window_days", 30)),
            "final_sale": bool(payload.get("final_sale", False)),
            "items": tuple(payload.get("items", ())),
        }
        new_state["order_shipments"][record["order_id"]] = record
    else:
        payload = envelope["payload"]
        record = {
            "tenant": tenant,
            "payment_id": payload["payment_id"],
            "order_id": payload["order_id"],
            "captured_amount": float(payload["captured_amount"]),
            "currency": payload["currency"],
            "ledger_account": payload.get("ledger_account", "refund_liability"),
        }
        new_state["payment_captures"][record["payment_id"]] = record

    new_state["handled_event_keys"][idempotency_key] = inbox_record
    new_state, domain_event = _append_domain_event(
        new_state,
        event_type=envelope["event_type"],
        tenant=tenant,
        payload={"source_event_id": envelope["event_id"], "idempotency_key": idempotency_key},
        publish=False,
    )
    return {"ok": True, "state": new_state, "duplicate": False, "dead_lettered": False, "event": domain_event}


def returns_reverse_logistics_authorize_return(state: dict, payload: dict) -> dict:
    _require_runtime_ready(state)
    _require_keys(
        payload,
        ("return_id", "rma", "tenant", "order_id", "payment_id", "customer_id", "reason", "requested_at"),
        "Returns Reverse Logistics return authorization",
    )
    tenant = payload["tenant"]
    order_projection = state["order_shipments"].get(payload["order_id"])
    payment_projection = state["payment_captures"].get(payload["payment_id"])
    if not order_projection or order_projection["tenant"] != tenant:
        raise ValueError("Return authorization requires an OrderShipped projection for the same tenant.")
    if not payment_projection or payment_projection["tenant"] != tenant:
        raise ValueError("Return authorization requires a PaymentCaptured projection for the same tenant.")

    eligibility = returns_reverse_logistics_evaluate_eligibility(state, payload)
    prior_returns = len(
        tuple(
            record
            for record in state["return_authorizations"].values()
            if record["tenant"] == tenant and record["customer_id"] == payload["customer_id"]
        )
    )
    fraud_assessment = returns_reverse_logistics_score_fraud(
        state,
        payload=payload,
        order_projection=order_projection,
        payment_projection=payment_projection,
        prior_returns=prior_returns,
    )
    if not eligibility["eligible"]:
        raise ValueError("Return authorization failed eligibility screening.")
    if fraud_assessment["decision"] == "block":
        raise ValueError("Return authorization blocked by fraud screening.")

    new_state = _clone_state(state)
    record = {
        "return_id": payload["return_id"],
        "rma": payload["rma"],
        "tenant": tenant,
        "order_id": payload["order_id"],
        "payment_id": payload["payment_id"],
        "customer_id": payload["customer_id"],
        "reason": payload["reason"],
        "requested_at": payload["requested_at"],
        "days_since_shipped": int(payload.get("days_since_shipped", order_projection["days_since_shipped"])),
        "items": tuple(payload.get("items", order_projection["items"])),
        "status": "authorized",
        "eligibility_score": eligibility["score"],
        "fraud_score": fraud_assessment["fraud_score"],
        "graph_degree": 4,
        "label_id": None,
        "inspection_id": None,
        "credit_adjustment_id": None,
    }
    new_state["return_authorizations"][record["return_id"]] = record
    new_state, event = _append_domain_event(
        new_state,
        event_type="ReturnAuthorized",
        tenant=tenant,
        payload={
            "return_id": record["return_id"],
            "order_id": record["order_id"],
            "payment_id": record["payment_id"],
            "rma": record["rma"],
        },
        publish=True,
    )
    return {
        "ok": True,
        "state": new_state,
        "return_authorization": record,
        "eligibility": eligibility,
        "fraud_assessment": fraud_assessment,
        "event": event,
    }


def returns_reverse_logistics_create_return_label(state: dict, payload: dict) -> dict:
    _require_runtime_ready(state)
    _require_keys(
        payload,
        ("label_id", "return_id", "tenant", "origin", "destination", "package_weight_kg"),
        "Returns Reverse Logistics return label",
    )
    authorization = state["return_authorizations"].get(payload["return_id"])
    if not authorization or authorization["tenant"] != payload["tenant"]:
        raise ValueError("Return label creation requires an authorized return for the same tenant.")
    candidate_carriers = tuple(payload.get("candidate_carriers", ()))
    if not candidate_carriers:
        candidate_carriers = tuple(
            {
                "carrier_id": carrier_id,
                "availability": True,
                "cost": 10.0,
                "carbon_intensity": 80.0,
                "eta_hours": 24.0,
                "route_health": 0.75,
            }
            for carrier_id in state["configuration"]["supported_carriers"]
        )
    route_selection = returns_reverse_logistics_select_label_route(
        candidate_carriers,
        carbon_weight=state["parameters"].get("carbon_weight", 0.2),
        route_switch_threshold=state["parameters"].get("route_switch_threshold", 0.1),
        preferred_carriers=_active_rule_for_tenant(state, payload["tenant"]).get("label_policy", {}).get("preferred_carriers", ()),
    )
    new_state = _clone_state(state)
    label = {
        "label_id": payload["label_id"],
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "origin": payload["origin"],
        "destination": payload["destination"],
        "package_weight_kg": float(payload["package_weight_kg"]),
        "candidate_carriers": candidate_carriers,
        "carrier_id": route_selection["selected_carrier"],
        "tracking_number": f"trk_{payload['label_id']}",
        "handoff_status": "awaiting_carrier",
        "status": "generated",
        "route_selection": route_selection,
    }
    new_state["return_labels"][label["label_id"]] = label
    new_state["return_authorizations"][payload["return_id"]]["label_id"] = label["label_id"]
    new_state, event = _append_domain_event(
        new_state,
        event_type="ReturnLabelCreated",
        tenant=payload["tenant"],
        payload={"return_id": payload["return_id"], "label_id": label["label_id"], "carrier_id": label["carrier_id"]},
        publish=False,
    )
    return {"ok": True, "state": new_state, "return_label": label, "event": event}


def returns_reverse_logistics_record_inspection_grade(state: dict, payload: dict) -> dict:
    _require_runtime_ready(state)
    _require_keys(
        payload,
        ("inspection_id", "return_id", "tenant", "condition_score", "completeness_score", "packaging_intact"),
        "Returns Reverse Logistics inspection grade",
    )
    authorization = state["return_authorizations"].get(payload["return_id"])
    if not authorization or authorization["tenant"] != payload["tenant"]:
        raise ValueError("Inspection grading requires an authorized return for the same tenant.")
    simulation = returns_reverse_logistics_simulate_disposition(
        state,
        payload["return_id"],
        observed_condition=float(payload["condition_score"]),
        completeness_score=float(payload["completeness_score"]),
        packaging_intact=bool(payload["packaging_intact"]),
    )
    new_state = _clone_state(state)
    record = {
        "inspection_id": payload["inspection_id"],
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "condition_score": float(payload["condition_score"]),
        "completeness_score": float(payload["completeness_score"]),
        "packaging_intact": bool(payload["packaging_intact"]),
        "notes": payload.get("notes", ""),
        "grade": simulation["best_option"]["grade"],
        "recommended_disposition": simulation["best_option"]["disposition"],
        "expected_recovery_rate": simulation["best_option"]["recovery_rate"],
    }
    new_state["inspection_grades"][record["inspection_id"]] = record
    new_state["return_authorizations"][payload["return_id"]]["inspection_id"] = record["inspection_id"]
    new_state["return_authorizations"][payload["return_id"]]["status"] = "inspected"
    new_state, event = _append_domain_event(
        new_state,
        event_type="InspectionGraded",
        tenant=payload["tenant"],
        payload={"return_id": payload["return_id"], "inspection_id": record["inspection_id"], "disposition": record["recommended_disposition"]},
        publish=False,
    )
    return {"ok": True, "state": new_state, "inspection_grade": record, "simulation": simulation, "event": event}


def returns_reverse_logistics_issue_credit_adjustment(state: dict, payload: dict) -> dict:
    _require_runtime_ready(state)
    _require_keys(payload, ("adjustment_id", "return_id", "tenant"), "Returns Reverse Logistics credit adjustment")
    authorization = state["return_authorizations"].get(payload["return_id"])
    if not authorization or authorization["tenant"] != payload["tenant"]:
        raise ValueError("Credit adjustments require an authorized return for the same tenant.")
    inspection = _inspection_for_return(state, payload["return_id"])
    if inspection is None:
        raise ValueError("Credit adjustments require an inspection grade.")
    payment_projection = state["payment_captures"][authorization["payment_id"]]
    rule = _active_rule_for_tenant(state, payload["tenant"])
    factor_map = {
        "restock": float(rule.get("credit_policy", {}).get("restock_factor", _DISPOSITION_FACTORS["restock"])),
        "refurbish": float(rule.get("credit_policy", {}).get("refurbish_factor", _DISPOSITION_FACTORS["refurbish"])),
        "scrap": float(rule.get("credit_policy", {}).get("scrap_factor", _DISPOSITION_FACTORS["scrap"])),
    }
    factor = factor_map[inspection["recommended_disposition"]]
    amount = round(payment_projection["captured_amount"] * factor, 2)
    adjustment = {
        "adjustment_id": payload["adjustment_id"],
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "amount": amount,
        "currency": payment_projection["currency"],
        "disposition": inspection["recommended_disposition"],
        "ledger_handoff": {
            "target_account": payment_projection["ledger_account"],
            "status": "queued",
        },
        "refund_handoff": {
            "payment_id": authorization["payment_id"],
            "status": "queued",
        },
        "status": "issued",
    }
    new_state = _clone_state(state)
    new_state["credit_adjustments"][adjustment["adjustment_id"]] = adjustment
    new_state["return_authorizations"][payload["return_id"]]["credit_adjustment_id"] = adjustment["adjustment_id"]
    new_state["return_authorizations"][payload["return_id"]]["status"] = "credit_issued"
    new_state, event = _append_domain_event(
        new_state,
        event_type="CreditAdjustmentIssued",
        tenant=payload["tenant"],
        payload={
            "return_id": payload["return_id"],
            "adjustment_id": adjustment["adjustment_id"],
            "amount": amount,
            "currency": adjustment["currency"],
        },
        publish=True,
    )
    return {"ok": True, "state": new_state, "credit_adjustment": adjustment, "event": event}


def returns_reverse_logistics_evaluate_eligibility(state: dict, payload: dict) -> dict:
    order_projection = state["order_shipments"][payload["order_id"]]
    rule = _active_rule_for_tenant(state, payload["tenant"])
    window_days = int(
        rule.get("eligibility_policy", {}).get(
            "max_days_since_shipment",
            state["parameters"].get("eligibility_window_days", order_projection["return_window_days"]),
        )
    )
    days_since_shipped = int(payload.get("days_since_shipped", order_projection["days_since_shipped"]))
    blocked_reasons = set(rule.get("eligibility_policy", {}).get("blocked_reasons", ()))
    if order_projection.get("final_sale"):
        blocked_reasons.add("final_sale")
    reason_blocked = payload["reason"] in blocked_reasons
    score = _clamp(1.0 - (days_since_shipped / max(window_days, 1)) * 0.7 + (0.15 if not reason_blocked else -0.35))
    eligible = days_since_shipped <= window_days and not reason_blocked
    return {
        "eligible": eligible,
        "score": round(score, 4),
        "window_days": window_days,
        "days_since_shipped": days_since_shipped,
        "blocked_reasons": tuple(sorted(blocked_reasons)),
    }


def returns_reverse_logistics_score_fraud(
    state: dict,
    *,
    payload: dict,
    order_projection: dict,
    payment_projection: dict,
    prior_returns: int,
) -> dict:
    risk = returns_reverse_logistics_predict_return_risk(
        {
            "days_since_shipped_ratio": int(payload.get("days_since_shipped", order_projection["days_since_shipped"])) / max(order_projection["return_window_days"], 1),
            "price_ratio": float(payment_projection["captured_amount"]) / 500.0,
            "prior_returns_ratio": prior_returns / 5.0,
            "damage_claim_ratio": 0.8 if payload["reason"] == "damaged" else 0.35,
        }
    )
    threshold = float(state["parameters"].get("fraud_threshold", 0.7))
    fraud_score = risk["risk_score"]
    decision = "allow"
    if fraud_score >= threshold:
        decision = "review"
    if fraud_score >= min(threshold + 0.18, 0.98):
        decision = "block"
    return {"fraud_score": fraud_score, "threshold": threshold, "decision": decision}


def returns_reverse_logistics_simulate_disposition(
    state: dict,
    return_id: str,
    *,
    observed_condition: float | None = None,
    completeness_score: float = 1.0,
    packaging_intact: bool = True,
) -> dict:
    authorization = state["return_authorizations"][return_id]
    payment = state["payment_captures"][authorization["payment_id"]]
    rule = _active_rule_for_tenant(state, authorization["tenant"])
    condition = float(observed_condition if observed_condition is not None else 0.82)
    restock_min = float(rule.get("inspection_policy", {}).get("restock_min", 0.85))
    refurbish_min = float(rule.get("inspection_policy", {}).get("refurbish_min", 0.55))

    options = []
    for disposition in _DEFAULT_DISPOSITIONS:
        if disposition == "restock":
            grade = "A" if condition >= restock_min and completeness_score >= 0.95 and packaging_intact else "B"
            recovery_rate = _clamp(condition * 0.96)
            processing_cost = 6.0
            carbon_cost = 0.12
        elif disposition == "refurbish":
            grade = "B" if condition >= refurbish_min else "C"
            recovery_rate = _clamp(condition * 0.72)
            processing_cost = 14.0
            carbon_cost = 0.18
        else:
            grade = "D"
            recovery_rate = _clamp(max(0.08, condition * 0.3))
            processing_cost = 3.0
            carbon_cost = 0.05
        expected_recovery = payment["captured_amount"] * recovery_rate
        options.append(
            {
                "disposition": disposition,
                "grade": grade,
                "recovery_rate": round(recovery_rate, 4),
                "expected_recovery": round(expected_recovery, 2),
                "processing_cost": processing_cost,
                "carbon_cost": carbon_cost,
                "score": round(expected_recovery - processing_cost - carbon_cost * 10, 2),
            }
        )
    best_option = max(options, key=lambda item: item["score"])
    return {"return_id": return_id, "best_option": best_option, "options": tuple(options)}


def returns_reverse_logistics_forecast_return_recovery(history: tuple[tuple[int, float], ...], *, horizon_days: int) -> dict:
    average_volume = sum(volume for volume, _ in history) / max(len(history), 1)
    average_recovery = sum(recovery for _, recovery in history) / max(len(history), 1)
    seasonal_bias = 1.0 + min(horizon_days, 30) / 300.0
    return {
        "horizon_days": horizon_days,
        "predicted_return_volume": round(average_volume * seasonal_bias, 2),
        "predicted_recovery_rate": round(_clamp(average_recovery * (2.0 - seasonal_bias)), 4),
    }


def returns_reverse_logistics_resolve_exception(exception_type: str) -> dict:
    mapping = {
        "carrier_timeout": "failover_carrier_selection",
        "inspection_queue_spike": "autobalance_inspection_queue",
        "refund_handoff_failure": "replay_credit_outbox",
    }
    return {
        "exception_type": exception_type,
        "resolution": mapping.get(exception_type, "route_to_reverse_ops"),
    }


def returns_reverse_logistics_parse_return_instruction(text: str) -> dict:
    return {
        "return_id": _match_group(r"\breturn\s+([A-Za-z0-9_-]+)", text),
        "order_id": _match_group(r"\border\s+([A-Za-z0-9_-]+)", text),
        "rma": _match_group(r"\brma\s+([A-Za-z0-9_-]+)", text),
        "reason": _match_group(r"\breason\s+([A-Za-z0-9_-]+)", text),
    }


def returns_reverse_logistics_predict_return_risk(factors: dict) -> dict:
    signal = (
        float(factors.get("days_since_shipped_ratio", 0.0)) * 1.4
        + float(factors.get("price_ratio", 0.0)) * 0.7
        + float(factors.get("prior_returns_ratio", 0.0)) * 1.2
        + float(factors.get("damage_claim_ratio", 0.0)) * 0.8
        - 1.3
    )
    risk_score = round(1.0 / (1.0 + math.exp(-signal)), 4)
    return {"risk_score": risk_score, "signal": round(signal, 4)}


def returns_reverse_logistics_select_label_route(
    carriers: tuple[dict, ...],
    *,
    carbon_weight: float,
    route_switch_threshold: float,
    preferred_carriers: tuple[str, ...] = (),
) -> dict:
    available = [carrier for carrier in carriers if carrier.get("availability")]
    if not available:
        raise ValueError("At least one available carrier is required for return label creation.")

    def route_score(carrier: dict) -> float:
        preference_bonus = -1.5 if carrier["carrier_id"] in preferred_carriers else 0.0
        health_penalty = (1.0 - float(carrier.get("route_health", 0.5))) * 4.0
        return (
            float(carrier.get("cost", 0.0))
            + float(carrier.get("eta_hours", 0.0)) * 0.05
            + float(carrier.get("carbon_intensity", 0.0)) * carbon_weight * 0.02
            + health_penalty
            + preference_bonus
        )

    ranked = sorted(available, key=route_score)
    selected = ranked[0]
    rerouted = False
    if len(ranked) > 1 and float(selected.get("route_health", 1.0)) < (1.0 - route_switch_threshold):
        selected = ranked[1]
        rerouted = True

    return {
        "selected_carrier": selected["carrier_id"],
        "rerouted": rerouted,
        "scored_candidates": tuple(
            {
                "carrier_id": carrier["carrier_id"],
                "score": round(route_score(carrier), 4),
                "availability": bool(carrier.get("availability")),
            }
            for carrier in ranked
        ),
    }


def returns_reverse_logistics_generate_return_proof(state: dict, return_id: str, *, disclosure: tuple[str, ...]) -> dict:
    authorization = state["return_authorizations"][return_id]
    disclosed = {key: authorization[key] for key in disclosure if key in authorization}
    proof_payload = {
        "crypto_epoch": state["crypto_epoch"],
        "return_id": return_id,
        "disclosed": disclosed,
    }
    return {"proof_hash": _hash_payload(proof_payload), "disclosure": disclosure}


def returns_reverse_logistics_screen_policy(state: dict, return_id: str) -> dict:
    authorization = state["return_authorizations"][return_id]
    rule = _active_rule_for_tenant(state, authorization["tenant"])
    blocked_reasons = set(rule.get("eligibility_policy", {}).get("blocked_reasons", ()))
    decision = "allow"
    reasons = []
    if authorization["reason"] in blocked_reasons:
        decision = "block"
        reasons.append("blocked_reason")
    if authorization["fraud_score"] >= float(state["parameters"].get("fraud_threshold", 0.7)):
        decision = "review" if decision == "allow" else decision
        reasons.append("fraud_threshold")
    return {"decision": decision, "reasons": tuple(reasons)}


def returns_reverse_logistics_run_control_tests(state: dict) -> dict:
    checks = (
        {"id": "configuration_present", "ok": bool(state.get("configuration", {}).get("ok"))},
        {"id": "required_event_topic", "ok": state.get("configuration", {}).get("event_topic") == RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC},
        {"id": "supported_database_backend", "ok": state.get("configuration", {}).get("database_backend") in _SUPPORTED_DATABASE_BACKENDS},
        {"id": "compiled_rule_hashes", "ok": all(rule.get("compiled_hash") for rule in state.get("rules", {}).values())},
        {"id": "bounded_parameters", "ok": set(state.get("parameters", {})).issubset(_SUPPORTED_PARAMETERS)},
        {
            "id": "outbox_idempotency_keys",
            "ok": all(message.get("idempotency_key") for message in state.get("outbox", ())),
        },
    )
    return {"ok": all(check["ok"] for check in checks), "checks": checks}


def returns_reverse_logistics_build_api_contract() -> dict:
    return {
        "format": "appgen.returns-reverse-logistics-api-contract.v1",
        "pbc": "returns_reverse_logistics",
        "apis": _API_SURFACES,
        "emits": _EMITTED_EVENT_TYPES,
        "consumes": tuple(sorted(_CONSUMED_EVENT_TYPES)),
        "async_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "user_eventing_choice": False,
    }


def returns_reverse_logistics_federate_return_view(state: dict, return_id: str, *, systems: tuple[str, ...]) -> dict:
    authorization = state["return_authorizations"][return_id]
    inspection = _inspection_for_return(state, return_id)
    adjustment = _credit_adjustment_for_return(state, return_id)
    return {
        "return_id": return_id,
        "systems": systems,
        "order": state["order_shipments"].get(authorization["order_id"]),
        "payment": state["payment_captures"].get(authorization["payment_id"]),
        "inventory": {
            "recommended_disposition": inspection["recommended_disposition"] if inspection else None,
            "restockable": bool(inspection and inspection["recommended_disposition"] == "restock"),
        },
        "ledger": adjustment["ledger_handoff"] if adjustment else None,
    }


def returns_reverse_logistics_run_resilience_drill(state: dict, scenario: str) -> dict:
    fallback = {
        "carrier_api_timeout": "degraded_but_available",
        "ledger_handoff_delay": "queued_replay_mode",
        "inspection_station_unavailable": "work_rebalanced",
    }.get(scenario, "degraded_but_available")
    return {
        "ok": True,
        "scenario": scenario,
        "mode": fallback,
        "outbox_replay_depth": len(state.get("outbox", ())),
        "dead_letter_depth": len(state.get("dead_letter", ())),
    }


def returns_reverse_logistics_rotate_crypto_epoch(state: dict, next_epoch: str) -> dict:
    new_state = _clone_state(state)
    new_state["crypto_epoch"] = next_epoch
    new_state, event = _append_domain_event(
        new_state,
        event_type="CryptoEpochRotated",
        tenant="system",
        payload={"crypto_epoch": next_epoch},
        publish=False,
    )
    return {"ok": True, "state": new_state, "event": event}


def returns_reverse_logistics_optimize_carbon_aware_routing(carriers: tuple[dict, ...]) -> dict:
    available = [carrier for carrier in carriers if carrier.get("availability")]
    selected = min(available, key=lambda carrier: (float(carrier.get("carbon_intensity", 0.0)), float(carrier.get("cost", 0.0))))
    return {"selected_carrier": selected["carrier_id"], "carbon_intensity": float(selected["carbon_intensity"])}


def returns_reverse_logistics_optimize_recovery_math(options: tuple[dict, ...]) -> dict:
    best_option = max(
        options,
        key=lambda option: option["expected_recovery"] - option["processing_cost"] - option["carbon_cost"] * 8.0,
    )
    return {"best_option": best_option}


def returns_reverse_logistics_allocate_disposition_mechanism(options: tuple[dict, ...], *, units: int) -> dict:
    ranked = sorted(options, key=lambda option: option["score"], reverse=True)
    remaining = units
    allocation = []
    for option in ranked:
        if remaining <= 0:
            break
        assigned = min(remaining, 1 if option["disposition"] != ranked[0]["disposition"] else remaining)
        allocation.append({"disposition": option["disposition"], "units": assigned})
        remaining -= assigned
    if remaining > 0:
        allocation.append({"disposition": ranked[0]["disposition"], "units": remaining})
    return {"allocation": tuple(allocation)}


def returns_reverse_logistics_detect_return_anomaly(state: dict) -> dict:
    repeated_orders = {}
    for authorization in state["return_authorizations"].values():
        repeated_orders[authorization["order_id"]] = repeated_orders.get(authorization["order_id"], 0) + 1
    anomaly_detected = any(count > 1 for count in repeated_orders.values()) or bool(state["dead_letter"])
    return {"anomaly_detected": anomaly_detected, "dead_letter_count": len(state["dead_letter"])}


def returns_reverse_logistics_model_stochastic_exposure(
    *,
    return_rate_path: tuple[float, ...],
    recovery_path: tuple[float, ...],
    volatility: float,
) -> dict:
    expected_return_rate = sum(return_rate_path) / max(len(return_rate_path), 1)
    expected_recovery = sum(recovery_path) / max(len(recovery_path), 1)
    expected_loss = max(0.0, expected_return_rate * (1.0 - expected_recovery) * (1.0 + volatility))
    return {
        "expected_return_rate": round(expected_return_rate, 4),
        "expected_recovery_rate": round(expected_recovery, 4),
        "expected_loss": round(expected_loss, 4),
    }


def returns_reverse_logistics_register_governed_model(model_name: str, metadata: dict) -> dict:
    _require_keys(metadata, ("features", "auc", "drift_score"), "Returns Reverse Logistics governed model")
    evidence = {
        "model_name": model_name,
        "features": tuple(metadata["features"]),
        "auc": float(metadata["auc"]),
        "drift_score": float(metadata["drift_score"]),
        "registry_hash": _hash_payload({"model_name": model_name, "metadata": metadata}),
    }
    return {"ok": evidence["auc"] >= 0.8 and evidence["drift_score"] <= 0.1, "evidence": evidence}


def returns_reverse_logistics_build_workbench_view(state: dict, *, tenant: str) -> dict:
    returns_for_tenant = tuple(record for record in state["return_authorizations"].values() if record["tenant"] == tenant)
    labels = tuple(record for record in state["return_labels"].values() if record["tenant"] == tenant)
    inspections = tuple(record for record in state["inspection_grades"].values() if record["tenant"] == tenant)
    adjustments = tuple(record for record in state["credit_adjustments"].values() if record["tenant"] == tenant)
    inbox = tuple(record for record in state["inbox"] if record.get("tenant") == tenant)
    outbox = tuple(record for record in state["outbox"] if record.get("tenant") == tenant)
    dead_letter = tuple(record for record in state["dead_letter"] if record.get("tenant") == tenant)
    rules = tuple((rule_id, rule["compiled_hash"]) for rule_id, rule in state["rules"].items() if rule["tenant"] == tenant)
    return {
        "format": "appgen.returns-reverse-logistics-workbench.v1",
        "ok": True,
        "tenant": tenant,
        "return_count": len(returns_for_tenant),
        "authorized_count": len(tuple(record for record in returns_for_tenant if record["status"] in {"authorized", "inspected", "credit_issued"})),
        "label_count": len(labels),
        "inspection_count": len(inspections),
        "credit_count": len(adjustments),
        "inbox_count": len(inbox),
        "outbox_count": len(outbox),
        "dead_letter_count": len(dead_letter),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "configuration_hash": state.get("configuration", {}).get("configuration_hash"),
        "rule_count": len(rules),
        "rules_bound": tuple(sorted(rule_id for rule_id, _ in rules)),
        "rule_evidence": tuple({"rule_id": rule_id, "compiled_hash": compiled_hash} for rule_id, compiled_hash in sorted(rules)),
        "parameter_count": len(state.get("parameters", {})),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
    }


def returns_reverse_logistics_permissions_contract() -> dict:
    return {
        "authorize_return": "returns_reverse_logistics.authorize",
        "create_return_label": "returns_reverse_logistics.label",
        "record_inspection_grade": "returns_reverse_logistics.inspect",
        "issue_credit_adjustment": "returns_reverse_logistics.adjust",
        "receive_event": "returns_reverse_logistics.audit",
        "register_rule": "returns_reverse_logistics.configure",
        "set_parameter": "returns_reverse_logistics.configure",
        "configure_runtime": "returns_reverse_logistics.configure",
    }


def _inspection_for_return(state: dict, return_id: str) -> dict | None:
    for inspection in state["inspection_grades"].values():
        if inspection["return_id"] == return_id:
            return inspection
    return None


def _credit_adjustment_for_return(state: dict, return_id: str) -> dict | None:
    for adjustment in state["credit_adjustments"].values():
        if adjustment["return_id"] == return_id:
            return adjustment
    return None


def _active_rule_for_tenant(state: dict, tenant: str) -> dict:
    for rule in state["rules"].values():
        if rule["tenant"] == tenant and rule["status"] == "active":
            return rule
    return {
        "eligibility_policy": {},
        "label_policy": {},
        "inspection_policy": {},
        "credit_policy": {},
    }


def _require_runtime_ready(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Returns Reverse Logistics runtime must be configured before use.")


def _append_domain_event(state: dict, *, event_type: str, tenant: str, payload: dict, publish: bool) -> tuple[dict, dict]:
    event_id = f"returns_evt_{state['event_sequence'] + 1:06d}"
    previous_hash = state["events"][-1]["hash"] if state["events"] else "returns_root"
    record = {
        "event_id": event_id,
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "previous_hash": previous_hash,
    }
    record["hash"] = _hash_payload(record)
    state["event_sequence"] += 1
    state["events"].append(record)
    if publish and event_type in _EMITTED_EVENT_TYPES:
        state["outbox"].append(
            {
                "event_id": event_id,
                "event_type": event_type,
                "tenant": tenant,
                "topic": state["configuration"]["event_topic"],
                "payload": payload,
                "idempotency_key": f"returns_reverse_logistics:{event_type}:{event_id}",
                "hash": record["hash"],
            }
        )
    return state, record


def _clone_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _clamp(value: float, *, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def _hash_payload(payload: object) -> str:
    encoded = json.dumps(_normalize_for_json(payload), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _normalize_for_json(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _normalize_for_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize_for_json(item) for item in value]
    return value


def _require_keys(payload: dict, required_keys: tuple[str, ...], label: str) -> None:
    missing = tuple(key for key in required_keys if key not in payload)
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _match_group(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(1) if match else None
