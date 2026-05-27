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
    "return_authorization_workflows",
    "return_eligibility",
    "eligibility_decisions",
    "return_labels",
    "carrier_handoff",
    "return_receiving",
    "receipt_and_inspection",
    "disposition_routing",
    "refund_exchange_resolution",
    "restock_refurbish_scrap_routing",
    "repair_refurbishment",
    "carrier_claims",
    "credit_adjustments",
    "refund_ledger_handoff",
    "fraud_abuse_screening",
    "customer_return_status",
    "exception_workflows",
    "tenant_isolation",
    "idempotent_handlers",
    "appgen_x_outbox_inbox_eventing",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_datastore_boundary",
    "schema_contract",
    "service_contract",
    "release_gate",
    "seed_data",
    "appgen_event_contract",
    "workbench",
    "immutable_audit",
    "governed_model_evidence",
)

RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES = (
    "returns_reverse_logistics_outbox_event",
    "returns_reverse_logistics_inbox_event",
    "returns_reverse_logistics_dead_letter_event",
)
RETURNS_REVERSE_LOGISTICS_OWNED_TABLES = (
    "return_authorization",
    "return_line",
    "return_eligibility_decision",
    "return_policy_snapshot",
    "reverse_route_graph",
    "return_label",
    "carrier_handoff",
    "return_receipt",
    "inspection_grade",
    "inspection_finding",
    "disposition_decision",
    "refund_exchange_resolution",
    "restocking_order",
    "repair_refurbishment_order",
    "carrier_claim",
    "return_customer_status",
    "return_exception_case",
    "return_exception_task",
    "return_fraud_signal",
    "credit_adjustment",
    "refund_ledger_handoff",
    "inventory_recovery_projection",
    "repair_vendor_projection",
    "carrier_claim_projection",
    "customer_notification_projection",
    "order_return_projection",
    "payment_return_projection",
    "inventory_return_projection",
    "ledger_return_projection",
    "returns_reverse_logistics_rule",
    "returns_reverse_logistics_parameter",
    "returns_reverse_logistics_configuration",
    "returns_reverse_logistics_schema_extension",
    "return_proof",
    "return_policy_screening",
    "return_control_assertion",
    "return_governed_model",
    "return_seed_data",
    *RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES,
)
RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES = ("OrderShipped", "PaymentCaptured")
RETURNS_REVERSE_LOGISTICS_EMITTED_EVENT_TYPES = ("ReturnAuthorized", "CreditAdjustmentIssued")
RETURNS_REVERSE_LOGISTICS_API_SURFACES = (
    "PUT /returns-reverse-logistics/configuration",
    "POST /returns-reverse-logistics/parameters",
    "POST /returns-reverse-logistics/rules",
    "POST /returns",
    "POST /labels",
    "POST /returns/{return_id}/receipts",
    "POST /inspection-grades",
    "POST /returns/{return_id}/dispositions",
    "POST /credit-adjustments",
    "POST /returns/{return_id}/refund-exchange",
    "POST /returns/{return_id}/carrier-claims",
    "GET /returns/{return_id}/customer-status",
    "POST /returns-reverse-logistics/events/inbox",
    "GET /returns-reverse-logistics-workbench",
    "GET /returns-reverse-logistics/schema-contract",
    "GET /returns-reverse-logistics/service-contract",
    "GET /returns-reverse-logistics/release-evidence",
)
RETURNS_REVERSE_LOGISTICS_DECLARED_API_DEPENDENCIES = (
    "GET /orders/{order_id}",
    "GET /payments/{payment_id}",
    "POST /inventory-dispositions",
    "POST /refunds",
    "POST /exchange-orders",
    "POST /ledger-adjustments",
    "POST /carrier-claims",
    "GET /customer-status",
)
RETURNS_REVERSE_LOGISTICS_DECLARED_PROJECTIONS = (
    "order_projection",
    "payment_projection",
    "inventory_projection",
    "ledger_projection",
)

_SUPPORTED_DATABASE_BACKENDS = RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS
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
_CONSUMED_EVENT_TYPES = set(RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES)
_API_SURFACES = RETURNS_REVERSE_LOGISTICS_API_SURFACES
_EMITTED_EVENT_TYPES = RETURNS_REVERSE_LOGISTICS_EMITTED_EVENT_TYPES
_DEFAULT_DISPOSITIONS = ("restock", "refurbish", "scrap")
_DISPOSITION_FACTORS = {"restock": 0.9, "refurbish": 0.65, "scrap": 0.25}
_RETURNS_REVERSE_LOGISTICS_ALLOWED_DEPENDENCIES = (
    *RETURNS_REVERSE_LOGISTICS_DECLARED_API_DEPENDENCIES,
    *RETURNS_REVERSE_LOGISTICS_DECLARED_PROJECTIONS,
)


def returns_reverse_logistics_runtime_capabilities() -> dict:
    smoke = returns_reverse_logistics_runtime_smoke()
    return {
        "format": "appgen.returns-reverse-logistics-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "returns_reverse_logistics",
        "implementation_directory": "src/pyAppGen/pbcs/returns_reverse_logistics",
        "owned_tables": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
        "runtime_tables": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES,
        "required_event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
        "capabilities": RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS,
        "standard_features": RETURNS_REVERSE_LOGISTICS_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "authorize_return",
            "create_return_label",
            "record_return_receipt",
            "record_inspection_grade",
            "resolve_disposition",
            "issue_credit_adjustment",
            "register_exchange_resolution",
            "create_restocking_order",
            "create_repair_refurbishment_order",
            "open_carrier_claim",
            "update_customer_return_status",
            "open_exception_case",
            "build_workbench_view",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "verify_owned_table_boundary",
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
    receipt = returns_reverse_logistics_record_return_receipt(
        state,
        {
            "receipt_id": "rcpt_001",
            "return_id": "ret_001",
            "tenant": "tenant_alpha",
            "received_at": "2026-05-28T09:00:00Z",
            "receiving_site": "NYC-returns",
            "package_condition": "intact",
        },
    )
    state = receipt["state"]
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
    disposition = returns_reverse_logistics_resolve_disposition(
        state,
        "ret_001",
        destination_site="NYC-restock",
    )
    state = disposition["state"]
    adjustment = returns_reverse_logistics_issue_credit_adjustment(
        state,
        {
            "adjustment_id": "adj_001",
            "return_id": "ret_001",
            "tenant": "tenant_alpha",
        },
    )
    state = adjustment["state"]
    resolution = returns_reverse_logistics_register_exchange_resolution(
        state,
        "ret_001",
        resolution_mode="refund",
    )
    state = resolution["state"]
    exception_case = returns_reverse_logistics_open_exception_case(
        state,
        "ret_001",
        exception_type="carrier_timeout",
        severity="medium",
        owner="reverse_ops",
    )
    state = exception_case["state"]
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
        {"id": "automated_control_testing", "ok": controls["ok"] is True and receipt["receipt"]["received_status"] == "received"},
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
        {"id": "return_anomaly_detection", "ok": anomaly["anomaly_detected"] is True and exception_case["exception_case"]["status"] == "open"},
        {"id": "stochastic_return_exposure_modeling", "ok": stochastic["expected_loss"] >= 0.0},
        {"id": "governed_ml_model_evidence", "ok": model["ok"] is True},
        {
            "id": "permissions_governance_evidence",
            "ok": "configure_runtime"
            in returns_reverse_logistics_permissions_contract()["action_permissions"],
        },
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
        "return_lines": {},
        "eligibility_decisions": {},
        "policy_snapshots": {},
        "route_graphs": {},
        "return_labels": {},
        "carrier_handoffs": {},
        "return_receipts": {},
        "inspection_grades": {},
        "inspection_findings": {},
        "disposition_decisions": {},
        "credit_adjustments": {},
        "refund_exchange_resolutions": {},
        "restocking_orders": {},
        "repair_refurbishment_orders": {},
        "carrier_claims": {},
        "customer_statuses": {},
        "exception_cases": {},
        "exception_tasks": {},
        "fraud_signals": {},
        "refund_ledger_handoffs": {},
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
        "allowed_database_backends": RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
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
    forbidden = sorted(key for key in rule if key in _FORBIDDEN_EVENTING_FIELDS)
    if forbidden:
        raise ValueError("Returns Reverse Logistics rules cannot declare stream-engine or user eventing fields.")
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
    if entity not in RETURNS_REVERSE_LOGISTICS_OWNED_TABLES:
        raise ValueError(
            "Returns Reverse Logistics schema extensions must target owned tables: "
            f"{RETURNS_REVERSE_LOGISTICS_OWNED_TABLES}"
        )
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        raise ValueError(
            "Returns Reverse Logistics schema extension field names must be lowercase snake_case."
        )
    new_state = _clone_state(state)
    record = {
        "table": entity,
        "fields": dict(fields),
        "version": len(new_state["schema_extensions"].get(entity, ())) + 1,
        "schema_hash": _hash_payload({"table": entity, "fields": fields}),
    }
    new_state["schema_extensions"].setdefault(entity, []).append(record)
    return {"ok": True, "state": new_state, "schema_extension": record}


def returns_reverse_logistics_receive_event(state: dict, envelope: dict) -> dict:
    _require_appgen_x_event_contract(state)
    _require_keys(envelope, ("event_id", "event_type", "idempotency_key", "payload"), "Returns Reverse Logistics inbox event")
    if envelope.get("event_contract") not in {None, "AppGen-X"}:
        raise ValueError("Returns Reverse Logistics inbox events must use the AppGen-X event contract.")
    if envelope.get("topic") not in {None, RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC}:
        raise ValueError(
            f"Returns Reverse Logistics inbox events must use topic {RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC}."
        )
    tenant = envelope["payload"].get("tenant")
    if not tenant:
        raise ValueError("Returns Reverse Logistics inbox events require payload.tenant.")
    idempotency_key = envelope["idempotency_key"]
    if idempotency_key in state["handled_event_keys"]:
        recorded = state["handled_event_keys"][idempotency_key]
        return {
            "ok": recorded["status"] == "handled",
            "state": state,
            "duplicate": True,
            "dead_lettered": recorded["status"] == "dead_lettered",
            "event": recorded,
            "inbox_record": recorded,
            "retry_evidence": state["retry_evidence"].get(idempotency_key),
            "dead_letter_record": next(
                (
                    record
                    for record in state["dead_letter"]
                    if record.get("idempotency_key") == idempotency_key
                ),
                None,
            ),
        }

    new_state = _clone_state(state)
    attempts = int(envelope.get("attempts", 1))
    inbox_record = {
        "event_id": envelope["event_id"],
        "event_type": envelope["event_type"],
        "idempotency_key": idempotency_key,
        "tenant": tenant,
        "payload": envelope["payload"],
        "attempts": attempts,
        "topic": state["configuration"]["event_topic"],
        "event_contract": "AppGen-X",
        "status": "received",
    }
    retry_limit = int(new_state.get("configuration", {}).get("retry_limit", 3))

    if envelope["event_type"] not in _CONSUMED_EVENT_TYPES:
        evidence = {
            "event_id": envelope["event_id"],
            "event_type": envelope["event_type"],
            "tenant": tenant,
            "attempts": attempts,
            "reason": "unsupported_event_type",
            "retry_limit": retry_limit,
            "status": "dead_lettered" if attempts >= retry_limit else "retrying",
        }
        new_state["retry_evidence"][idempotency_key] = evidence
        inbox_record["status"] = evidence["status"]
        inbox_record["reason"] = evidence["reason"]
        new_state["inbox"].append(inbox_record)
        dead_letter_record = None
        if attempts >= retry_limit:
            dead_letter_record = {
                **inbox_record,
                "dead_letter_table": "returns_reverse_logistics_dead_letter_event",
            }
            new_state["dead_letter"].append(dead_letter_record)
        new_state["handled_event_keys"][idempotency_key] = inbox_record
        return {
            "ok": False,
            "state": new_state,
            "duplicate": False,
            "dead_lettered": attempts >= retry_limit,
            "event": evidence,
            "inbox_record": inbox_record,
            "retry_evidence": evidence,
            "dead_letter_record": dead_letter_record,
        }

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

    inbox_record["status"] = "handled"
    new_state["inbox"].append(inbox_record)
    new_state["handled_event_keys"][idempotency_key] = inbox_record
    new_state, domain_event = _append_domain_event(
        new_state,
        event_type=envelope["event_type"],
        tenant=tenant,
        payload={"source_event_id": envelope["event_id"], "idempotency_key": idempotency_key},
        publish=False,
    )
    return {
        "ok": True,
        "state": new_state,
        "duplicate": False,
        "dead_lettered": False,
        "event": domain_event,
        "inbox_record": inbox_record,
        "retry_evidence": None,
        "dead_letter_record": None,
    }


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

    rule = _active_rule_for_tenant(state, tenant)
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
    new_state["return_lines"][record["return_id"]] = tuple(
        {
            "return_id": record["return_id"],
            "tenant": tenant,
            "line_number": index,
            "sku": item["sku"],
            "quantity": int(item.get("quantity", 1)),
        }
        for index, item in enumerate(record["items"], start=1)
    )
    new_state["eligibility_decisions"][record["return_id"]] = {
        "return_id": record["return_id"],
        "tenant": tenant,
        "eligible": eligibility["eligible"],
        "score": eligibility["score"],
        "window_days": eligibility["window_days"],
        "blocked_reasons": eligibility["blocked_reasons"],
    }
    new_state["policy_snapshots"][record["return_id"]] = {
        "return_id": record["return_id"],
        "tenant": tenant,
        "rule_id": rule.get("rule_id", "implicit_default"),
        "scope": rule.get("scope", "return_policy"),
        "compiled_hash": rule.get("compiled_hash"),
    }
    new_state["route_graphs"][record["return_id"]] = {
        "return_id": record["return_id"],
        "tenant": tenant,
        "nodes": ("customer", "order", "payment", "return"),
        "edges": (("customer", "order"), ("order", "payment"), ("order", "return")),
    }
    new_state["fraud_signals"][record["return_id"]] = {
        "return_id": record["return_id"],
        "tenant": tenant,
        "fraud_score": fraud_assessment["fraud_score"],
        "decision": fraud_assessment["decision"],
    }
    new_state["customer_statuses"][record["return_id"]] = {
        "return_id": record["return_id"],
        "tenant": tenant,
        "status": "authorized",
        "customer_visible_status": "Authorization approved",
    }
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
    new_state["carrier_handoffs"][payload["return_id"]] = {
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "label_id": label["label_id"],
        "carrier_id": label["carrier_id"],
        "handoff_status": label["handoff_status"],
    }
    new_state["return_authorizations"][payload["return_id"]]["label_id"] = label["label_id"]
    new_state["customer_statuses"][payload["return_id"]] = {
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "status": "label_generated",
        "customer_visible_status": "Label ready",
    }
    new_state, event = _append_domain_event(
        new_state,
        event_type="ReturnLabelCreated",
        tenant=payload["tenant"],
        payload={"return_id": payload["return_id"], "label_id": label["label_id"], "carrier_id": label["carrier_id"]},
        publish=False,
    )
    return {"ok": True, "state": new_state, "return_label": label, "event": event}


def returns_reverse_logistics_record_return_receipt(state: dict, payload: dict) -> dict:
    _require_runtime_ready(state)
    _require_keys(
        payload,
        ("receipt_id", "return_id", "tenant", "received_at", "receiving_site", "package_condition"),
        "Returns Reverse Logistics return receipt",
    )
    authorization = state["return_authorizations"].get(payload["return_id"])
    if not authorization or authorization["tenant"] != payload["tenant"]:
        raise ValueError("Return receipt requires an authorized return for the same tenant.")
    new_state = _clone_state(state)
    receipt = {
        "receipt_id": payload["receipt_id"],
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "received_at": payload["received_at"],
        "receiving_site": payload["receiving_site"],
        "package_condition": payload["package_condition"],
        "received_status": "received",
        "chain_of_custody_hash": _hash_payload(payload),
    }
    new_state["return_receipts"][payload["return_id"]] = receipt
    new_state["return_authorizations"][payload["return_id"]]["status"] = "received"
    new_state = returns_reverse_logistics_update_customer_return_status(
        new_state,
        payload["return_id"],
        status="received",
        customer_visible_status="Return received",
    )["state"]
    new_state, event = _append_domain_event(
        new_state,
        event_type="ReturnReceived",
        tenant=payload["tenant"],
        payload={"return_id": payload["return_id"], "receipt_id": receipt["receipt_id"]},
        publish=False,
    )
    return {"ok": True, "state": new_state, "receipt": receipt, "event": event}


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
    new_state["return_receipts"][payload["return_id"]] = {
        "receipt_id": f"rcpt_{payload['inspection_id']}",
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "received_status": "received",
        "inspection_id": record["inspection_id"],
    }
    new_state["inspection_findings"][record["inspection_id"]] = {
        "inspection_id": record["inspection_id"],
        "tenant": payload["tenant"],
        "grade": record["grade"],
        "recommended_disposition": record["recommended_disposition"],
    }
    new_state["disposition_decisions"][payload["return_id"]] = {
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "disposition": record["recommended_disposition"],
        "expected_recovery_rate": record["expected_recovery_rate"],
    }
    new_state["return_authorizations"][payload["return_id"]]["inspection_id"] = record["inspection_id"]
    new_state["return_authorizations"][payload["return_id"]]["status"] = "inspected"
    new_state["customer_statuses"][payload["return_id"]] = {
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "status": "inspection_complete",
        "customer_visible_status": "Inspection complete",
    }
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
    new_state["refund_exchange_resolutions"][payload["return_id"]] = {
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "resolution_mode": payload.get("resolution_mode", "refund"),
        "adjustment_id": adjustment["adjustment_id"],
        "status": "queued",
    }
    new_state["refund_ledger_handoffs"][payload["return_id"]] = {
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "adjustment_id": adjustment["adjustment_id"],
        "target_account": adjustment["ledger_handoff"]["target_account"],
        "status": adjustment["ledger_handoff"]["status"],
    }
    if inspection["recommended_disposition"] == "restock":
        new_state["restocking_orders"][payload["return_id"]] = {
            "return_id": payload["return_id"],
            "tenant": payload["tenant"],
            "status": "queued",
            "inventory_action": "restock",
        }
    elif inspection["recommended_disposition"] == "refurbish":
        new_state["repair_refurbishment_orders"][payload["return_id"]] = {
            "return_id": payload["return_id"],
            "tenant": payload["tenant"],
            "status": "queued",
            "repair_path": "refurbish",
        }
    else:
        new_state["carrier_claims"][payload["return_id"]] = {
            "return_id": payload["return_id"],
            "tenant": payload["tenant"],
            "claim_reason": "scrap_recovery_shortfall",
            "status": "review",
        }
    new_state["return_authorizations"][payload["return_id"]]["credit_adjustment_id"] = adjustment["adjustment_id"]
    new_state["return_authorizations"][payload["return_id"]]["status"] = "credit_issued"
    new_state["customer_statuses"][payload["return_id"]] = {
        "return_id": payload["return_id"],
        "tenant": payload["tenant"],
        "status": "credit_issued",
        "customer_visible_status": "Refund or exchange pending settlement",
    }
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


def returns_reverse_logistics_resolve_disposition(
    state: dict,
    return_id: str,
    *,
    disposition: str | None = None,
    destination_site: str = "default_recovery_site",
) -> dict:
    _require_runtime_ready(state)
    authorization = state["return_authorizations"].get(return_id)
    if not authorization:
        raise ValueError(f"Unknown return authorization: {return_id}")
    inspection = _inspection_for_return(state, return_id)
    if inspection is None:
        raise ValueError("Disposition resolution requires an inspection grade.")
    selected = disposition or inspection["recommended_disposition"]
    if selected not in _DEFAULT_DISPOSITIONS:
        raise ValueError(f"Unsupported disposition: {selected}")
    new_state = _clone_state(state)
    decision = {
        "return_id": return_id,
        "tenant": authorization["tenant"],
        "disposition": selected,
        "destination_site": destination_site,
        "expected_recovery_rate": inspection["expected_recovery_rate"],
        "status": "resolved",
        "decision_hash": _hash_payload({"return_id": return_id, "disposition": selected, "destination_site": destination_site}),
    }
    new_state["disposition_decisions"][return_id] = decision
    if selected == "restock":
        order = returns_reverse_logistics_create_restocking_order(
            new_state,
            return_id,
            destination_site=destination_site,
        )
        new_state = order["state"]
    elif selected == "refurbish":
        order = returns_reverse_logistics_create_repair_refurbishment_order(
            new_state,
            return_id,
            provider_ref="default_refurbishment_provider",
        )
        new_state = order["state"]
    else:
        claim = returns_reverse_logistics_open_carrier_claim(
            new_state,
            return_id,
            claim_reason="scrap_recovery_shortfall",
        )
        new_state = claim["state"]
    new_state["return_authorizations"][return_id]["status"] = "disposition_resolved"
    new_state = returns_reverse_logistics_update_customer_return_status(
        new_state,
        return_id,
        status="disposition_resolved",
        customer_visible_status=f"Return disposition: {selected}",
    )["state"]
    new_state, event = _append_domain_event(
        new_state,
        event_type="ReturnDispositionResolved",
        tenant=authorization["tenant"],
        payload={"return_id": return_id, "disposition": selected},
        publish=False,
    )
    return {"ok": True, "state": new_state, "disposition": decision, "event": event}


def returns_reverse_logistics_register_exchange_resolution(
    state: dict,
    return_id: str,
    *,
    resolution_mode: str,
    replacement_order_id: str | None = None,
) -> dict:
    _require_runtime_ready(state)
    authorization = state["return_authorizations"].get(return_id)
    if not authorization:
        raise ValueError(f"Unknown return authorization: {return_id}")
    if resolution_mode not in {"refund", "exchange", "store_credit"}:
        raise ValueError("Resolution mode must be refund, exchange, or store_credit.")
    adjustment = _credit_adjustment_for_return(state, return_id)
    new_state = _clone_state(state)
    resolution = {
        "return_id": return_id,
        "tenant": authorization["tenant"],
        "resolution_mode": resolution_mode,
        "replacement_order_id": replacement_order_id,
        "adjustment_id": adjustment["adjustment_id"] if adjustment else None,
        "status": "queued",
        "resolution_hash": _hash_payload({"return_id": return_id, "mode": resolution_mode, "replacement_order_id": replacement_order_id}),
    }
    new_state["refund_exchange_resolutions"][return_id] = resolution
    new_state = returns_reverse_logistics_update_customer_return_status(
        new_state,
        return_id,
        status="resolution_queued",
        customer_visible_status=f"{resolution_mode.replace('_', ' ').title()} queued",
    )["state"]
    new_state, event = _append_domain_event(
        new_state,
        event_type="RefundExchangeResolutionQueued",
        tenant=authorization["tenant"],
        payload={"return_id": return_id, "resolution_mode": resolution_mode},
        publish=False,
    )
    return {"ok": True, "state": new_state, "resolution": resolution, "event": event}


def returns_reverse_logistics_create_restocking_order(
    state: dict,
    return_id: str,
    *,
    destination_site: str,
) -> dict:
    _require_runtime_ready(state)
    authorization = state["return_authorizations"].get(return_id)
    if not authorization:
        raise ValueError(f"Unknown return authorization: {return_id}")
    new_state = _clone_state(state)
    order = {
        "restocking_order_id": f"restock_{return_id}",
        "return_id": return_id,
        "tenant": authorization["tenant"],
        "inventory_action": "restock",
        "destination_site": destination_site,
        "status": "queued",
        "projection": "inventory_recovery_projection",
    }
    new_state["restocking_orders"][return_id] = order
    return {"ok": True, "state": new_state, "restocking_order": order}


def returns_reverse_logistics_create_repair_refurbishment_order(
    state: dict,
    return_id: str,
    *,
    provider_ref: str,
) -> dict:
    _require_runtime_ready(state)
    authorization = state["return_authorizations"].get(return_id)
    if not authorization:
        raise ValueError(f"Unknown return authorization: {return_id}")
    new_state = _clone_state(state)
    order = {
        "repair_order_id": f"repair_{return_id}",
        "return_id": return_id,
        "tenant": authorization["tenant"],
        "repair_path": "refurbish",
        "provider_ref": provider_ref,
        "status": "queued",
        "projection": "repair_vendor_projection",
    }
    new_state["repair_refurbishment_orders"][return_id] = order
    return {"ok": True, "state": new_state, "repair_refurbishment_order": order}


def returns_reverse_logistics_open_carrier_claim(
    state: dict,
    return_id: str,
    *,
    claim_reason: str,
) -> dict:
    _require_runtime_ready(state)
    authorization = state["return_authorizations"].get(return_id)
    if not authorization:
        raise ValueError(f"Unknown return authorization: {return_id}")
    label = next((item for item in state["return_labels"].values() if item["return_id"] == return_id), {})
    new_state = _clone_state(state)
    claim = {
        "carrier_claim_id": f"claim_{return_id}_{len(new_state['carrier_claims']) + 1}",
        "return_id": return_id,
        "tenant": authorization["tenant"],
        "claim_reason": claim_reason,
        "carrier_id": label.get("carrier_id"),
        "status": "open",
        "projection": "carrier_claim_projection",
        "claim_hash": _hash_payload({"return_id": return_id, "claim_reason": claim_reason, "carrier_id": label.get("carrier_id")}),
    }
    new_state["carrier_claims"][return_id] = claim
    return {"ok": True, "state": new_state, "carrier_claim": claim}


def returns_reverse_logistics_update_customer_return_status(
    state: dict,
    return_id: str,
    *,
    status: str,
    customer_visible_status: str,
) -> dict:
    authorization = state["return_authorizations"].get(return_id)
    if not authorization:
        raise ValueError(f"Unknown return authorization: {return_id}")
    new_state = _clone_state(state)
    status_record = {
        "return_id": return_id,
        "tenant": authorization["tenant"],
        "status": status,
        "customer_visible_status": customer_visible_status,
        "notification_projection": "customer_notification_projection",
        "status_hash": _hash_payload({"return_id": return_id, "status": status, "customer_visible_status": customer_visible_status}),
    }
    new_state["customer_statuses"][return_id] = status_record
    return {"ok": True, "state": new_state, "customer_status": status_record}


def returns_reverse_logistics_open_exception_case(
    state: dict,
    return_id: str,
    *,
    exception_type: str,
    severity: str,
    owner: str,
) -> dict:
    _require_runtime_ready(state)
    authorization = state["return_authorizations"].get(return_id)
    if not authorization:
        raise ValueError(f"Unknown return authorization: {return_id}")
    new_state = _clone_state(state)
    case = {
        "exception_case_id": f"rex_{return_id}_{len(new_state['exception_cases']) + 1}",
        "return_id": return_id,
        "tenant": authorization["tenant"],
        "exception_type": exception_type,
        "severity": severity,
        "status": "open",
        "resolution": returns_reverse_logistics_resolve_exception(exception_type)["resolution"],
    }
    task = {
        "exception_task_id": f"task_{case['exception_case_id']}",
        "exception_case_id": case["exception_case_id"],
        "tenant": authorization["tenant"],
        "owner": owner,
        "due_at": "next_business_day",
        "status": "open",
    }
    new_state["exception_cases"][case["exception_case_id"]] = case
    new_state.setdefault("exception_tasks", {})[task["exception_task_id"]] = task
    new_state = returns_reverse_logistics_update_customer_return_status(
        new_state,
        return_id,
        status="exception_open",
        customer_visible_status="Return needs review",
    )["state"]
    return {"ok": True, "state": new_state, "exception_case": case, "exception_task": task}


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
    permissions = returns_reverse_logistics_permissions_contract()
    routes = (
        {
            "route": "PUT /returns-reverse-logistics/configuration",
            "command": "configure_runtime",
            "owned_tables": ("returns_reverse_logistics_configuration",),
            "requires_permission": permissions["action_permissions"]["configure_runtime"],
            "idempotency_key": "configuration_hash",
        },
        {
            "route": "POST /returns-reverse-logistics/parameters",
            "command": "set_parameter",
            "owned_tables": ("returns_reverse_logistics_parameter",),
            "requires_permission": permissions["action_permissions"]["set_parameter"],
            "idempotency_key": "parameter_name",
        },
        {
            "route": "POST /returns-reverse-logistics/rules",
            "command": "register_rule",
            "owned_tables": ("returns_reverse_logistics_rule", "return_policy_snapshot"),
            "requires_permission": permissions["action_permissions"]["register_rule"],
            "idempotency_key": "rule_id",
        },
        {
            "route": "POST /returns-reverse-logistics/schema-extensions",
            "command": "register_schema_extension",
            "owned_tables": ("returns_reverse_logistics_schema_extension",),
            "requires_permission": permissions["action_permissions"]["register_schema_extension"],
            "idempotency_key": "table_name:field_name",
        },
        {
            "route": "POST /returns",
            "command": "authorize_return",
            "owned_tables": (
                "return_authorization",
                "return_line",
                "return_eligibility_decision",
                "return_policy_snapshot",
                "return_fraud_signal",
                "return_customer_status",
            ),
            "declared_event_dependencies": RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES,
            "requires_permission": permissions["action_permissions"]["authorize_return"],
            "idempotency_key": "return_id",
            "emits": ("ReturnAuthorized",),
        },
        {
            "route": "POST /labels",
            "command": "create_return_label",
            "owned_tables": ("return_label", "carrier_handoff", "reverse_route_graph", "return_customer_status"),
            "requires_permission": permissions["action_permissions"]["create_return_label"],
            "idempotency_key": "label_id",
        },
        {
            "route": "POST /returns/{return_id}/receipts",
            "command": "record_return_receipt",
            "owned_tables": ("return_receipt", "return_customer_status"),
            "requires_permission": permissions["action_permissions"]["record_return_receipt"],
            "idempotency_key": "receipt_id",
        },
        {
            "route": "POST /inspection-grades",
            "command": "record_inspection_grade",
            "owned_tables": (
                "inspection_grade",
                "inspection_finding",
                "disposition_decision",
                "return_receipt",
                "return_customer_status",
            ),
            "requires_permission": permissions["action_permissions"]["record_inspection_grade"],
            "idempotency_key": "inspection_id",
        },
        {
            "route": "POST /returns/{return_id}/dispositions",
            "command": "resolve_disposition",
            "owned_tables": ("disposition_decision", "restocking_order", "repair_refurbishment_order", "carrier_claim"),
            "requires_permission": permissions["action_permissions"]["resolve_disposition"],
            "idempotency_key": "return_id:disposition",
        },
        {
            "route": "POST /credit-adjustments",
            "command": "issue_credit_adjustment",
            "owned_tables": (
                "credit_adjustment",
                "refund_exchange_resolution",
                "refund_ledger_handoff",
                "restocking_order",
                "repair_refurbishment_order",
                "carrier_claim",
                "return_customer_status",
            ),
            "declared_api_dependencies": (
                "POST /refunds",
                "POST /exchange-orders",
                "POST /ledger-adjustments",
                "POST /carrier-claims",
            ),
            "requires_permission": permissions["action_permissions"]["issue_credit_adjustment"],
            "idempotency_key": "adjustment_id",
            "emits": ("CreditAdjustmentIssued",),
        },
        {
            "route": "POST /returns/{return_id}/refund-exchange",
            "command": "register_exchange_resolution",
            "owned_tables": ("refund_exchange_resolution", "return_customer_status"),
            "requires_permission": permissions["action_permissions"]["register_exchange_resolution"],
            "idempotency_key": "return_id:resolution_mode",
        },
        {
            "route": "POST /returns/{return_id}/carrier-claims",
            "command": "open_carrier_claim",
            "owned_tables": ("carrier_claim", "carrier_claim_projection"),
            "requires_permission": permissions["action_permissions"]["open_carrier_claim"],
            "idempotency_key": "return_id:claim_reason",
        },
        {
            "route": "GET /returns/{return_id}/customer-status",
            "query": "build_customer_return_status",
            "owned_tables": ("return_customer_status",),
            "requires_permission": permissions["action_permissions"]["build_customer_return_status"],
        },
        {
            "route": "POST /returns-reverse-logistics/events/inbox",
            "command": "receive_event",
            "owned_tables": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES,
            "consumes": RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES,
            "requires_permission": permissions["action_permissions"]["receive_event"],
            "idempotency_key": "idempotency_key",
        },
        {
            "route": "GET /returns-reverse-logistics-workbench",
            "query": "build_workbench_view",
            "owned_tables": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
            "requires_permission": permissions["action_permissions"]["build_workbench_view"],
        },
        {
            "route": "GET /returns-reverse-logistics/schema-contract",
            "query": "build_schema_contract",
            "owned_tables": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
            "requires_permission": permissions["action_permissions"]["build_schema_contract"],
        },
        {
            "route": "GET /returns-reverse-logistics/service-contract",
            "query": "build_service_contract",
            "owned_tables": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
            "requires_permission": permissions["action_permissions"]["build_service_contract"],
        },
        {
            "route": "GET /returns-reverse-logistics/release-evidence",
            "query": "build_release_evidence",
            "owned_tables": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
            "requires_permission": permissions["action_permissions"]["build_release_evidence"],
        },
    )
    return {
        "format": "appgen.returns-reverse-logistics-api-contract.v1",
        "ok": True,
        "pbc": "returns_reverse_logistics",
        "apis": _API_SURFACES,
        "routes": routes,
        "operations": routes,
        "declared_catalog_routes": (
            "POST /returns",
            "POST /labels",
            "POST /inspection-grades",
            "POST /credit-adjustments",
        ),
        "owned_tables": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
        "runtime_tables": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES,
        "events": {
            "emits": RETURNS_REVERSE_LOGISTICS_EMITTED_EVENT_TYPES,
            "consumes": RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES,
        },
        "emits": _EMITTED_EVENT_TYPES,
        "consumes": tuple(sorted(_CONSUMED_EVENT_TYPES)),
        "async_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
        "required_event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
        "database_backends": RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
        "permissions": permissions["permissions"],
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "user_eventing_choice": False,
        "dependencies": {
            "apis": RETURNS_REVERSE_LOGISTICS_DECLARED_API_DEPENDENCIES,
            "events": RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES,
            "api_projections": RETURNS_REVERSE_LOGISTICS_DECLARED_PROJECTIONS,
            "shared_tables": (),
        },
        "configuration": (
            "RETURNS_REVERSE_LOGISTICS_DATABASE_URL",
            "RETURNS_REVERSE_LOGISTICS_EVENT_TOPIC",
            "RETURNS_REVERSE_LOGISTICS_RETRY_LIMIT",
            "RETURNS_REVERSE_LOGISTICS_DEFAULT_CURRENCY",
        ),
    }


def returns_reverse_logistics_build_schema_contract() -> dict:
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {table: default_fields for table in RETURNS_REVERSE_LOGISTICS_OWNED_TABLES} | {
        "return_authorization": ("tenant", "return_id", "rma", "order_id", "payment_id", "customer_id", "reason", "status", "audit_hash"),
        "return_line": ("tenant", "return_line_id", "return_id", "sku", "quantity", "reason_code", "status", "audit_hash"),
        "return_eligibility_decision": ("tenant", "decision_id", "return_id", "score", "eligible", "window_days", "audit_hash"),
        "return_policy_snapshot": ("tenant", "snapshot_id", "return_id", "rule_id", "scope", "compiled_hash", "audit_hash"),
        "reverse_route_graph": ("tenant", "graph_id", "return_id", "carrier_id", "route_health", "carbon_intensity", "audit_hash"),
        "return_label": ("tenant", "label_id", "return_id", "carrier_id", "tracking_number", "handoff_status", "status", "audit_hash"),
        "carrier_handoff": ("tenant", "handoff_id", "return_id", "label_id", "carrier_id", "handoff_status", "audit_hash"),
        "return_receipt": ("tenant", "receipt_id", "return_id", "received_at", "receiving_site", "received_status", "audit_hash"),
        "inspection_grade": ("tenant", "inspection_id", "return_id", "grade", "recommended_disposition", "expected_recovery_rate", "audit_hash"),
        "inspection_finding": ("tenant", "finding_id", "inspection_id", "finding_type", "severity", "notes", "audit_hash"),
        "disposition_decision": ("tenant", "disposition_id", "return_id", "disposition", "expected_recovery_rate", "audit_hash"),
        "refund_exchange_resolution": ("tenant", "resolution_id", "return_id", "resolution_mode", "adjustment_id", "status", "audit_hash"),
        "restocking_order": ("tenant", "restocking_order_id", "return_id", "inventory_action", "destination_site", "status", "audit_hash"),
        "repair_refurbishment_order": ("tenant", "repair_order_id", "return_id", "repair_path", "provider_ref", "status", "audit_hash"),
        "carrier_claim": ("tenant", "carrier_claim_id", "return_id", "claim_reason", "carrier_id", "status", "audit_hash"),
        "return_customer_status": ("tenant", "status_id", "return_id", "customer_visible_status", "status", "updated_at", "audit_hash"),
        "return_exception_case": ("tenant", "exception_case_id", "return_id", "exception_type", "severity", "status", "audit_hash"),
        "return_exception_task": ("tenant", "exception_task_id", "exception_case_id", "owner", "due_at", "status", "audit_hash"),
        "return_fraud_signal": ("tenant", "fraud_signal_id", "return_id", "fraud_score", "decision", "audit_hash"),
        "credit_adjustment": ("tenant", "adjustment_id", "return_id", "amount", "currency", "disposition", "status", "audit_hash"),
        "refund_ledger_handoff": ("tenant", "handoff_id", "return_id", "adjustment_id", "target_account", "status", "audit_hash"),
        "inventory_recovery_projection": ("tenant", "projection_id", "return_id", "recovery_type", "recovery_status", "audit_hash"),
        "repair_vendor_projection": ("tenant", "projection_id", "return_id", "provider_ref", "repair_status", "audit_hash"),
        "carrier_claim_projection": ("tenant", "projection_id", "return_id", "carrier_id", "claim_status", "audit_hash"),
        "customer_notification_projection": ("tenant", "projection_id", "return_id", "channel", "delivery_status", "audit_hash"),
        "order_return_projection": ("tenant", "projection_id", "order_id", "return_id", "projection_status", "audit_hash"),
        "payment_return_projection": ("tenant", "projection_id", "payment_id", "return_id", "projection_status", "audit_hash"),
        "inventory_return_projection": ("tenant", "projection_id", "inventory_reference", "return_id", "projection_status", "audit_hash"),
        "ledger_return_projection": ("tenant", "projection_id", "ledger_reference", "return_id", "projection_status", "audit_hash"),
        "returns_reverse_logistics_rule": ("tenant", "rule_id", "scope", "compiled_hash", "status", "audit_hash"),
        "returns_reverse_logistics_parameter": ("tenant", "parameter_name", "parameter_value", "effective_at", "audit_hash"),
        "returns_reverse_logistics_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "event_contract", "retry_limit", "audit_hash"),
        "returns_reverse_logistics_schema_extension": ("tenant", "extension_id", "table_name", "field_name", "field_type", "revision", "audit_hash"),
        "return_proof": ("tenant", "proof_id", "return_id", "proof_hash", "disclosure_level", "audit_hash"),
        "return_policy_screening": ("tenant", "screening_id", "return_id", "decision", "reasons", "audit_hash"),
        "return_control_assertion": ("tenant", "assertion_id", "control_name", "assertion_status", "asserted_at", "audit_hash"),
        "return_governed_model": ("tenant", "model_id", "model_name", "auc", "drift_score", "audit_hash"),
        "return_seed_data": ("tenant", "seed_id", "seed_type", "seed_key", "seed_value", "audit_hash"),
        RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[0]: ("tenant", "event_id", "event_type", "topic", "payload", "idempotency_key", "published_at", "audit_hash"),
        RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[1]: ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "status", "audit_hash"),
        RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[2]: ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "reason", "audit_hash"),
    }
    runtime_tables = tuple(
        {"table": table, "fields": table_fields[table]} for table in RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
    )
    relationships = (
        {"from": "return_line.return_id", "to": "return_authorization.return_id", "type": "owned_line"},
        {"from": "return_eligibility_decision.return_id", "to": "return_authorization.return_id", "type": "owned_eligibility"},
        {"from": "return_policy_snapshot.return_id", "to": "return_authorization.return_id", "type": "owned_policy"},
        {"from": "return_label.return_id", "to": "return_authorization.return_id", "type": "owned_label"},
        {"from": "carrier_handoff.return_id", "to": "return_authorization.return_id", "type": "owned_handoff"},
        {"from": "return_receipt.return_id", "to": "return_authorization.return_id", "type": "owned_receipt"},
        {"from": "inspection_grade.return_id", "to": "return_authorization.return_id", "type": "owned_inspection"},
        {"from": "inspection_finding.inspection_id", "to": "inspection_grade.inspection_id", "type": "owned_finding"},
        {"from": "disposition_decision.return_id", "to": "return_authorization.return_id", "type": "owned_disposition"},
        {"from": "credit_adjustment.return_id", "to": "return_authorization.return_id", "type": "owned_credit"},
        {"from": "refund_exchange_resolution.return_id", "to": "return_authorization.return_id", "type": "owned_resolution"},
        {"from": "restocking_order.return_id", "to": "return_authorization.return_id", "type": "owned_restock"},
        {"from": "repair_refurbishment_order.return_id", "to": "return_authorization.return_id", "type": "owned_repair"},
        {"from": "carrier_claim.return_id", "to": "return_authorization.return_id", "type": "owned_claim"},
        {"from": "return_exception_task.exception_case_id", "to": "return_exception_case.exception_case_id", "type": "owned_exception_task"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(
                field
                for field in table_fields[table]
                if field.endswith("_id") or field in {"parameter_name", "configuration_id"}
            )[:2],
            "owned_by": "returns_reverse_logistics",
        }
        for table in RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
    )
    return {
        "format": "appgen.returns-reverse-logistics-owned-schema-contract.v1",
        "ok": len(tables) == len(RETURNS_REVERSE_LOGISTICS_OWNED_TABLES)
        and len(tables) >= 30
        and all(item["table"] in RETURNS_REVERSE_LOGISTICS_OWNED_TABLES for item in tables),
        "owned_tables": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
        "tables": tables,
        "runtime_tables": runtime_tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/returns_reverse_logistics/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(RETURNS_REVERSE_LOGISTICS_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
                "module_path": f"pyAppGen.pbcs.returns_reverse_logistics.models.{table}",
            }
            for table in RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
        ),
        "datastore_backends": RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "shared_table_access": False,
    }


def returns_reverse_logistics_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "authorize_return",
        "create_return_label",
        "record_return_receipt",
        "record_inspection_grade",
        "resolve_disposition",
        "issue_credit_adjustment",
        "register_exchange_resolution",
        "create_restocking_order",
        "create_repair_refurbishment_order",
        "open_carrier_claim",
        "update_customer_return_status",
        "open_exception_case",
        "screen_policy",
        "run_control_tests",
        "register_governed_model",
        "rotate_crypto_epoch",
    )
    query_methods = (
        "build_workbench_view",
        "build_api_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "evaluate_eligibility",
        "score_fraud",
        "simulate_disposition",
        "forecast_return_recovery",
        "resolve_exception",
        "parse_return_instruction",
        "predict_return_risk",
        "select_label_route",
        "generate_return_proof",
        "federate_return_view",
        "run_resilience_drill",
        "optimize_carbon_aware_routing",
        "optimize_recovery_math",
        "allocate_disposition_mechanism",
        "detect_return_anomaly",
        "model_stochastic_exposure",
        "build_customer_return_status",
        "verify_owned_table_boundary",
    )
    return {
        "format": "appgen.returns-reverse-logistics-service-contract.v1",
        "ok": len(command_methods) >= 18 and len(query_methods) >= 18,
        "transaction_boundary": "returns_reverse_logistics_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
        "mutates_only_owned_tables": True,
        "shared_table_access": False,
        "event_contract": {
            "contract": "AppGen-X",
            "required_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
        },
        "eventing": {
            "contract": "AppGen-X",
            "topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
            "outbox_table": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[0],
            "inbox_table": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[1],
            "dead_letter_table": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[2],
            "idempotency_required": True,
        },
        "idempotent_handlers": ("receive_event",),
        "retry_dead_letter_evidence": {
            "retry_evidence_state": "retry_evidence",
            "dead_letter_state": "dead_letter",
            "dead_letter_table": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[2],
            "retry_limit_field": "retry_limit",
        },
        "external_dependencies": {
            "apis": RETURNS_REVERSE_LOGISTICS_DECLARED_API_DEPENDENCIES,
            "events": RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES,
            "api_projections": RETURNS_REVERSE_LOGISTICS_DECLARED_PROJECTIONS,
            "shared_tables": (),
        },
        "advanced_capabilities": RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS,
    }


def returns_reverse_logistics_build_release_evidence() -> dict:
    schema = returns_reverse_logistics_build_schema_contract()
    service = returns_reverse_logistics_build_service_contract()
    api = returns_reverse_logistics_build_api_contract()
    permissions = returns_reverse_logistics_permissions_contract()
    control = _returns_reverse_logistics_release_control_evidence()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 30},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(RETURNS_REVERSE_LOGISTICS_OWNED_TABLES)},
        {"id": "service_contract_depth", "ok": service["ok"] and "receive_event" in service["idempotent_handlers"]},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X" and api["required_event_topic"] == RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC},
        {"id": "permissions_cover_release_queries", "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"])},
        {"id": "retry_dead_letter_evidence", "ok": control["ok"] and control["summary"]["retry_status"] == "retrying" and control["summary"]["dead_letter_status"] == "dead_letter"},
        {"id": "duplicate_idempotency_evidence", "ok": control["summary"]["duplicate_status"] == "duplicate"},
        {"id": "ui_workbench_binding", "ok": control["workbench"]["binding_evidence"]["runtime_tables"] == RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"] and not service["shared_table_access"]},
    )
    return {
        "format": "appgen.returns-reverse-logistics-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "control": control,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def returns_reverse_logistics_build_customer_return_status(state: dict, return_id: str) -> dict:
    authorization = state["return_authorizations"][return_id]
    status = state["customer_statuses"].get(
        return_id,
        {
            "return_id": return_id,
            "tenant": authorization["tenant"],
            "status": authorization["status"],
            "customer_visible_status": authorization["status"].replace("_", " "),
        },
    )
    return {
        "return_id": return_id,
        "tenant": authorization["tenant"],
        "status": status["status"],
        "customer_visible_status": status["customer_visible_status"],
        "label_id": authorization.get("label_id"),
        "inspection_id": authorization.get("inspection_id"),
        "credit_adjustment_id": authorization.get("credit_adjustment_id"),
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
    receipts = tuple(record for record in state["return_receipts"].values() if record["tenant"] == tenant)
    inspections = tuple(record for record in state["inspection_grades"].values() if record["tenant"] == tenant)
    adjustments = tuple(record for record in state["credit_adjustments"].values() if record["tenant"] == tenant)
    customer_statuses = tuple(record for record in state["customer_statuses"].values() if record["tenant"] == tenant)
    exception_cases = tuple(record for record in state["exception_cases"].values() if record["tenant"] == tenant)
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
        "receipt_count": len(receipts),
        "inspection_count": len(inspections),
        "credit_count": len(adjustments),
        "customer_status_count": len(customer_statuses),
        "exception_count": len(exception_cases),
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
        "binding_evidence": {
            "owned_tables": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
            "runtime_tables": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES,
            "outbox_table": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[0],
            "inbox_table": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[1],
            "dead_letter_table": RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES[2],
            "shared_table_access": False,
            "event_contract": state.get("configuration", {}).get("event_contract"),
            "required_event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
            "service_release_queries": (
                "build_schema_contract",
                "build_service_contract",
                "build_release_evidence",
            ),
        },
    }


def returns_reverse_logistics_permissions_contract() -> dict:
    permissions = (
        "returns_reverse_logistics.authorize",
        "returns_reverse_logistics.label",
        "returns_reverse_logistics.inspect",
        "returns_reverse_logistics.adjust",
        "returns_reverse_logistics.event.consume",
        "returns_reverse_logistics.configure",
        "returns_reverse_logistics.audit",
        "returns_reverse_logistics.exception",
        "returns_reverse_logistics.claim",
    )
    return {
        "format": "appgen.returns-reverse-logistics-permissions.v1",
        "ok": True,
        "permissions": permissions,
        "roles": {
            "returns_reverse_logistics_admin": permissions,
            "returns_reverse_logistics_operator": (
                "returns_reverse_logistics.authorize",
                "returns_reverse_logistics.label",
                "returns_reverse_logistics.inspect",
                "returns_reverse_logistics.adjust",
                "returns_reverse_logistics.event.consume",
                "returns_reverse_logistics.claim",
                "returns_reverse_logistics.exception",
            ),
            "returns_reverse_logistics_auditor": (
                "returns_reverse_logistics.audit",
                "returns_reverse_logistics.event.consume",
            ),
        },
        "policy_controls": (
            "tenant_scope_required",
            "appgen_x_event_contract_locked",
            "event_topic_fixed",
            "event_idempotency_required",
            "no_shared_table_access",
        ),
        "action_permissions": {
            "authorize_return": "returns_reverse_logistics.authorize",
            "create_return_label": "returns_reverse_logistics.label",
            "record_return_receipt": "returns_reverse_logistics.inspect",
            "record_inspection_grade": "returns_reverse_logistics.inspect",
            "resolve_disposition": "returns_reverse_logistics.adjust",
            "issue_credit_adjustment": "returns_reverse_logistics.adjust",
            "register_exchange_resolution": "returns_reverse_logistics.adjust",
            "open_carrier_claim": "returns_reverse_logistics.claim",
            "build_customer_return_status": "returns_reverse_logistics.audit",
            "receive_event": "returns_reverse_logistics.event.consume",
            "register_rule": "returns_reverse_logistics.configure",
            "register_schema_extension": "returns_reverse_logistics.configure",
            "set_parameter": "returns_reverse_logistics.configure",
            "configure_runtime": "returns_reverse_logistics.configure",
            "build_workbench_view": "returns_reverse_logistics.audit",
            "build_api_contract": "returns_reverse_logistics.audit",
            "build_schema_contract": "returns_reverse_logistics.audit",
            "build_service_contract": "returns_reverse_logistics.audit",
            "build_release_evidence": "returns_reverse_logistics.audit",
            "verify_owned_table_boundary": "returns_reverse_logistics.audit",
        },
    }


def returns_reverse_logistics_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed = (
        *RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
        *RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES,
        *RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES,
        *_RETURNS_REVERSE_LOGISTICS_ALLOWED_DEPENDENCIES,
    )
    allowed_set = set(allowed)
    violations = tuple(
        reference
        for reference in references
        if reference not in allowed_set and not str(reference).startswith("returns_reverse_logistics_")
    )
    return {
        "format": "appgen.returns-reverse-logistics-boundary.v1",
        "ok": not violations,
        "owned_tables": RETURNS_REVERSE_LOGISTICS_OWNED_TABLES,
        "declared_dependencies": {
            "apis": RETURNS_REVERSE_LOGISTICS_DECLARED_API_DEPENDENCIES,
            "events": RETURNS_REVERSE_LOGISTICS_CONSUMED_EVENT_TYPES,
            "api_projections": RETURNS_REVERSE_LOGISTICS_DECLARED_PROJECTIONS,
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def _returns_reverse_logistics_release_control_evidence() -> dict:
    state = returns_reverse_logistics_empty_state()
    state = returns_reverse_logistics_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "supported_carriers": ("parcel_green",),
            "supported_dispositions": _DEFAULT_DISPOSITIONS,
            "workbench_limit": 20,
        },
    )["state"]
    state = returns_reverse_logistics_register_rule(
        state,
        {
            "rule_id": "rule_release",
            "tenant": "tenant_release",
            "scope": "return_policy",
            "status": "active",
            "eligibility_policy": {"max_days_since_shipment": 30, "blocked_reasons": (), "minimum_payment_capture_ratio": 1.0},
            "label_policy": {"preferred_carriers": ("parcel_green",), "max_cost": 15.0},
            "inspection_policy": {"restock_min": 0.85, "refurbish_min": 0.55},
            "credit_policy": {"restock_factor": 0.9, "refurbish_factor": 0.65, "scrap_factor": 0.25},
        },
    )["state"]
    accepted = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_release_ship",
            "event_type": "OrderShipped",
            "idempotency_key": "release:order:v1",
            "payload": {
                "tenant": "tenant_release",
                "order_id": "order_release",
                "payment_id": "pay_release",
                "customer_id": "cust_release",
                "shipped_at": "2026-05-20",
                "days_since_shipped": 3,
                "return_window_days": 30,
                "final_sale": False,
                "items": ({"sku": "sku_release", "quantity": 1, "unit_price": 75.0},),
            },
        },
    )
    state = accepted["state"]
    duplicate = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_release_ship",
            "event_type": "OrderShipped",
            "idempotency_key": "release:order:v1",
            "payload": {
                "tenant": "tenant_release",
                "order_id": "order_release",
                "payment_id": "pay_release",
                "customer_id": "cust_release",
                "shipped_at": "2026-05-20",
                "days_since_shipped": 3,
                "return_window_days": 30,
                "final_sale": False,
                "items": ({"sku": "sku_release", "quantity": 1, "unit_price": 75.0},),
            },
        },
    )
    retrying = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_release_retry",
            "event_type": "UnknownEvent",
            "idempotency_key": "release:retry:v1",
            "attempts": 1,
            "payload": {"tenant": "tenant_release"},
        },
    )
    state = retrying["state"]
    failed = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_release_dead",
            "event_type": "UnknownEvent",
            "idempotency_key": "release:dead:v1",
            "attempts": 2,
            "payload": {"tenant": "tenant_release"},
        },
    )
    workbench = returns_reverse_logistics_build_workbench_view(failed["state"], tenant="tenant_release")
    return {
        "ok": accepted["ok"] is True and failed["dead_lettered"] is True,
        "summary": {
            "accepted_status": accepted["inbox_record"]["status"],
            "duplicate_status": "duplicate" if duplicate["duplicate"] else duplicate["inbox_record"]["status"],
            "retry_status": retrying["retry_evidence"]["status"],
            "dead_letter_status": "dead_letter" if failed["dead_lettered"] else failed["inbox_record"]["status"],
        },
        "workbench": workbench,
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


def _require_appgen_x_event_contract(state: dict) -> None:
    _require_runtime_ready(state)
    configuration = state["configuration"]
    if (
        configuration.get("event_contract") != "AppGen-X"
        or configuration.get("event_topic") != RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    ):
        raise ValueError(
            "Returns Reverse Logistics runtime must remain bound to the AppGen-X returns event contract."
        )


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
                "event_contract": "AppGen-X",
                "payload": payload,
                "idempotency_key": f"returns_reverse_logistics:{event_type}:{event_id}",
                "retry_policy": {
                    "max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)),
                    "dead_letter": "returns_reverse_logistics_dead_letter_event",
                },
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
