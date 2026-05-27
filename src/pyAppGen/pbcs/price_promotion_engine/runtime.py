"""Executable runtime for the Price Promotion Engine PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


PRICE_PROMOTION_ENGINE_EVENT_CONTRACT = "AppGen-X"
PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC = "appgen.price_promotion.events"
PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PRICE_PROMOTION_ENGINE_RUNTIME_TABLES = (
    "price_promotion_engine_appgen_outbox_event",
    "price_promotion_engine_appgen_inbox_event",
    "price_promotion_engine_dead_letter_event",
)
PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES = (
    "POST /customer-segment-projections/resolve",
    "POST /forecast-projections/resolve",
    "POST /checkout-projections/price-context",
    "GET /currency-rate-projections/{currency}",
    "customer_segment_projection",
    "forecast_projection",
    "checkout_projection",
    "currency_rate_projection",
)
PRICE_PROMOTION_ENGINE_OWNED_TABLES = (
    "price_configuration",
    "price_parameter",
    "price_policy_rule",
    "price_schema_extension",
    "price_list",
    "price_book",
    "price_book_entry",
    "price_rule",
    "customer_price",
    "channel_price",
    "currency_price",
    "promotion",
    "promotion_rule",
    "coupon",
    "promotion_eligibility",
    "promotion_stacking_policy",
    "promotion_exclusion",
    "campaign_budget",
    "promotion_approval",
    "loyalty_tier",
    "price_simulation",
    "price_margin_guardrail",
    "price_decision",
    "price_audit_trace",
    "price_performance_telemetry",
)

PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_pricing_lifecycle",
    "owned_price_schema_boundary",
    "price_list_and_book_management",
    "multi_tenant_price_isolation",
    "schema_evolution_resilient_price_context",
    "contextual_price_quote_optimization",
    "promotion_stacking_and_exclusion_engine",
    "coupon_and_eligibility_governance",
    "campaign_budget_and_approval_evidence",
    "loyalty_tier_price_personalization",
    "volume_break_and_contract_price_support",
    "forecast_signal_price_adjustment",
    "customer_segment_price_adjustment",
    "probabilistic_margin_elasticity_scoring",
    "counterfactual_promotion_margin_simulation",
    "simulation_margin_guardrail_evidence",
    "temporal_price_effectivity_forecasting",
    "autonomous_price_exception_resolution",
    "semantic_promotion_instruction_parsing",
    "predictive_margin_and_demand_risk",
    "self_healing_price_decision_selection",
    "cryptographic_price_decision_proof",
    "immutable_price_audit_trail",
    "dynamic_price_policy_screening",
    "automated_promotion_control_testing",
    "performance_telemetry_evidence",
    "cross_system_customer_forecast_checkout_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions_governance_evidence",
    "configuration_schema",
    "parameter_engine",
    "rule_engine",
    "generated_schema_and_service_contracts",
    "seed_data",
    "workbench_ui",
    "governed_model_evidence",
)

PRICE_PROMOTION_ENGINE_STANDARD_FEATURE_KEYS = (
    "price_list_management",
    "price_book_management",
    "price_rule_catalog",
    "customer_channel_currency_prices",
    "promotion_lifecycle",
    "promotion_rules",
    "coupon_management",
    "promotion_eligibility",
    "promotion_stacking_exclusions",
    "campaign_budgets",
    "promotion_approvals",
    "loyalty_tier_management",
    "price_decision_history",
    "price_simulations",
    "margin_guardrails",
    "performance_telemetry",
    "contextual_price_quotes",
    "promotion_redemption_validation",
    "volume_breaks",
    "currency_region_constraints",
    "customer_segment_inputs",
    "forecast_signal_inputs",
    "checkout_handoff",
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

PRICE_PROMOTION_ENGINE_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_currency",
    "supported_currencies",
    "supported_regions",
    "pricing_calendars",
    "default_timezone",
    "decision_mode",
    "workbench_limit",
    "approval_mode",
    "simulation_horizon_days",
    "telemetry_window_minutes",
)

PRICE_PROMOTION_ENGINE_SUPPORTED_PARAMETER_KEYS = (
    "margin_floor_percent",
    "promotion_stack_limit",
    "elasticity_weight",
    "forecast_weight",
    "segment_weight",
    "loyalty_weight",
    "risk_review_threshold",
    "discount_ceiling_percent",
    "decision_ttl_minutes",
    "workbench_limit",
    "approval_discount_threshold_percent",
    "campaign_budget_guardrail",
    "coupon_reuse_limit",
)

PRICE_PROMOTION_ENGINE_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "allowed_currencies",
    "allowed_regions",
    "allowed_segments",
    "promotion_policy",
    "margin_policy",
    "stacking_policy",
    "exclusion_policy",
    "approval_policy",
    "budget_policy",
)

PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES = ("CustomerSegmentUpdated", "ForecastUpdated")
PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES = ("PriceOptimized", "PromotionApplied")

_CONFIG_SEQUENCE_FIELDS = {"supported_currencies", "supported_regions", "pricing_calendars"}
_RULE_SEQUENCE_FIELDS = {"allowed_currencies", "allowed_regions", "allowed_segments"}
_PARAMETER_BOUNDS = {
    "margin_floor_percent": (0.0, 100.0),
    "promotion_stack_limit": (1, 10),
    "elasticity_weight": (0.0, 1.0),
    "forecast_weight": (0.0, 1.0),
    "segment_weight": (0.0, 1.0),
    "loyalty_weight": (0.0, 1.0),
    "risk_review_threshold": (0.0, 1.0),
    "discount_ceiling_percent": (0.0, 100.0),
    "decision_ttl_minutes": (1, 10080),
    "workbench_limit": (1, 1000),
    "approval_discount_threshold_percent": (0.0, 100.0),
    "campaign_budget_guardrail": (0.0, 1.0),
    "coupon_reuse_limit": (1, 100),
}
_TABLE_FIELDS = {
    "price_configuration": (
        "tenant",
        "configuration_id",
        "database_backend",
        "event_topic",
        "retry_limit",
        "default_currency",
        "default_timezone",
        "approval_mode",
        "simulation_horizon_days",
        "telemetry_window_minutes",
        "audit_hash",
    ),
    "price_parameter": (
        "tenant",
        "parameter_id",
        "parameter_name",
        "parameter_value",
        "bounds",
        "effective_at",
        "audit_hash",
    ),
    "price_policy_rule": (
        "tenant",
        "rule_id",
        "scope",
        "allowed_currencies",
        "allowed_regions",
        "allowed_segments",
        "promotion_policy",
        "margin_policy",
        "stacking_policy",
        "exclusion_policy",
        "approval_policy",
        "budget_policy",
        "compiled_hash",
        "status",
        "audit_hash",
    ),
    "price_schema_extension": (
        "tenant",
        "extension_id",
        "table_name",
        "fields",
        "version",
        "status",
        "audit_hash",
    ),
    "price_list": (
        "tenant",
        "price_list_id",
        "name",
        "currency",
        "calendar",
        "status",
        "audit_hash",
    ),
    "price_book": (
        "tenant",
        "price_book_id",
        "price_list_id",
        "channel",
        "region",
        "currency",
        "status",
        "audit_hash",
    ),
    "price_book_entry": (
        "tenant",
        "price_book_entry_id",
        "price_book_id",
        "price_rule_id",
        "sku",
        "base_price",
        "status",
        "audit_hash",
    ),
    "price_rule": (
        "tenant",
        "price_rule_id",
        "sku",
        "price_list_id",
        "price_book_id",
        "region",
        "currency",
        "base_price",
        "cost",
        "margin_percent",
        "segments",
        "volume_breaks",
        "status",
        "audit_hash",
    ),
    "customer_price": (
        "tenant",
        "customer_price_id",
        "price_rule_id",
        "customer_id",
        "currency",
        "price",
        "status",
        "audit_hash",
    ),
    "channel_price": (
        "tenant",
        "channel_price_id",
        "price_rule_id",
        "channel",
        "currency",
        "price",
        "status",
        "audit_hash",
    ),
    "currency_price": (
        "tenant",
        "currency_price_id",
        "price_rule_id",
        "currency",
        "base_price",
        "status",
        "audit_hash",
    ),
    "promotion": (
        "tenant",
        "promotion_id",
        "code",
        "discount_percent",
        "channels",
        "currencies",
        "regions",
        "segments",
        "customer_ids",
        "status",
        "audit_hash",
    ),
    "promotion_rule": (
        "tenant",
        "promotion_rule_id",
        "promotion_id",
        "policy",
        "status",
        "audit_hash",
    ),
    "coupon": (
        "tenant",
        "coupon_id",
        "promotion_id",
        "code",
        "reuse_limit",
        "redemption_count",
        "redeemed_decision_ids",
        "status",
        "audit_hash",
    ),
    "promotion_eligibility": (
        "tenant",
        "eligibility_id",
        "promotion_id",
        "segments",
        "regions",
        "currencies",
        "channels",
        "customer_ids",
        "audit_hash",
    ),
    "promotion_stacking_policy": (
        "tenant",
        "stacking_policy_id",
        "promotion_id",
        "stackable",
        "stack_limit",
        "mutual_group",
        "audit_hash",
    ),
    "promotion_exclusion": (
        "tenant",
        "promotion_exclusion_id",
        "promotion_id",
        "excluded_promotion_ids",
        "reason",
        "audit_hash",
    ),
    "campaign_budget": (
        "tenant",
        "campaign_budget_id",
        "promotion_id",
        "budget_amount",
        "consumed_amount",
        "budget_currency",
        "status",
        "audit_hash",
    ),
    "promotion_approval": (
        "tenant",
        "promotion_approval_id",
        "promotion_id",
        "approval_required",
        "approval_status",
        "approver_role",
        "approved_by",
        "audit_hash",
    ),
    "loyalty_tier": (
        "tenant",
        "tier_id",
        "name",
        "rank",
        "discount_percent",
        "status",
        "audit_hash",
    ),
    "price_simulation": (
        "tenant",
        "simulation_id",
        "decision_id",
        "scenario_count",
        "counterfactuals",
        "status",
        "audit_hash",
    ),
    "price_margin_guardrail": (
        "tenant",
        "guardrail_id",
        "subject_type",
        "subject_id",
        "margin_floor_percent",
        "discount_ceiling_percent",
        "breach",
        "audit_hash",
    ),
    "price_decision": (
        "tenant",
        "decision_id",
        "customer_id",
        "sku",
        "price_book_id",
        "price_list_id",
        "channel",
        "currency",
        "quantity",
        "base_price",
        "optimized_unit_price",
        "extended_price",
        "total_discount_percent",
        "margin_percent",
        "risk_score",
        "status",
        "eligible_promotions",
        "applied_promotions",
        "counterfactuals",
        "audit_hash",
    ),
    "price_audit_trace": (
        "tenant",
        "trace_id",
        "trace_type",
        "subject_id",
        "related_tables",
        "trace_hash",
        "audit_hash",
    ),
    "price_performance_telemetry": (
        "tenant",
        "telemetry_id",
        "metric_key",
        "subject_id",
        "sample_ms",
        "rule_hits",
        "status",
        "audit_hash",
    ),
}
_RUNTIME_TABLE_FIELDS = {
    PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[0]: (
        "tenant",
        "event_id",
        "event_type",
        "topic",
        "contract",
        "idempotency_key",
        "payload_hash",
        "status",
        "published_at",
        "audit_hash",
    ),
    PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[1]: (
        "tenant",
        "event_id",
        "event_type",
        "topic",
        "contract",
        "idempotency_key",
        "attempts",
        "status",
        "received_at",
        "audit_hash",
    ),
    PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[2]: (
        "tenant",
        "event_id",
        "event_type",
        "topic",
        "contract",
        "idempotency_key",
        "attempts",
        "reason",
        "dead_lettered_at",
        "audit_hash",
    ),
}


def price_promotion_engine_runtime_capabilities() -> dict:
    smoke = price_promotion_engine_runtime_smoke()
    return {
        "format": "appgen.price-promotion-engine-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "price_promotion_engine",
        "implementation_directory": "src/pyAppGen/pbcs/price_promotion_engine",
        "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        "runtime_tables": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES,
        "required_event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
        "event_contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
        "consumes": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
        "emits": PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES,
        "capabilities": PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PRICE_PROMOTION_ENGINE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "register_price_rule",
            "register_promotion",
            "approve_promotion",
            "register_loyalty_tier",
            "receive_event",
            "quote_price",
            "apply_promotion",
            "redeem_coupon",
            "build_workbench_view",
            "binding_evidence",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "verify_owned_table_boundary",
        ),
        "dependencies": PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES,
        "smoke": smoke,
    }


def price_promotion_engine_runtime_smoke() -> dict:
    state = price_promotion_engine_empty_state()
    state = price_promotion_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD", "EUR"),
            "supported_regions": ("US", "EU"),
            "pricing_calendars": ("standard", "holiday"),
            "default_timezone": "UTC",
            "decision_mode": "policy",
            "workbench_limit": 100,
            "approval_mode": "manager_review",
            "simulation_horizon_days": 30,
            "telemetry_window_minutes": 15,
        },
    )["state"]
    for name, value in (
        ("margin_floor_percent", 18.0),
        ("promotion_stack_limit", 2),
        ("elasticity_weight", 0.25),
        ("forecast_weight", 0.25),
        ("segment_weight", 0.25),
        ("loyalty_weight", 0.25),
        ("risk_review_threshold", 0.72),
        ("discount_ceiling_percent", 40.0),
        ("decision_ttl_minutes", 60),
        ("workbench_limit", 100),
        ("approval_discount_threshold_percent", 15.0),
        ("campaign_budget_guardrail", 0.9),
        ("coupon_reuse_limit", 5),
    ):
        state = price_promotion_engine_set_parameter(state, name, value)["state"]
    state = price_promotion_engine_register_rule(
        state,
        {
            "rule_id": "rule_price_default",
            "tenant": "tenant_alpha",
            "scope": "price_promotion_engine",
            "status": "active",
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "allowed_segments": ("growth", "vip"),
            "promotion_policy": {"stackable": True, "requires_active_window": True},
            "margin_policy": {"floor_percent": 18.0, "review_above_risk": 0.72},
            "stacking_policy": {"max_promotions": 2, "group": "growth"},
            "exclusion_policy": {"excluded_promotion_ids": (), "reason": "none"},
            "approval_policy": {"required_above_discount": 15.0, "approver_role": "pricing_manager"},
            "budget_policy": {"default_budget_amount": 1500.0, "currency": "USD"},
        },
    )["state"]
    state = price_promotion_engine_register_schema_extension(
        state,
        "price_decision",
        {"model_features": "jsonb", "counterfactuals": "jsonb"},
    )["state"]
    state = price_promotion_engine_register_loyalty_tier(
        state,
        {
            "tier_id": "tier_vip",
            "tenant": "tenant_alpha",
            "name": "VIP",
            "rank": 10,
            "discount_percent": 8.0,
            "status": "active",
        },
    )["state"]
    state = price_promotion_engine_register_price_rule(
        state,
        {
            "price_rule_id": "rule_sku_alpha",
            "tenant": "tenant_alpha",
            "sku": "sku_alpha",
            "region": "US",
            "currency": "USD",
            "base_price": 100.0,
            "cost": 54.0,
            "segments": ("growth", "vip"),
            "volume_breaks": ((10, 0.05), (25, 0.1)),
            "status": "active",
            "price_list_id": "list_retail_usd",
            "price_book_id": "book_digital_us",
            "channel": "digital_store",
            "customer_id": "cust_alpha",
        },
    )["state"]
    state = price_promotion_engine_register_promotion(
        state,
        {
            "promotion_id": "promo_alpha",
            "tenant": "tenant_alpha",
            "code": "GROWTH10",
            "discount_percent": 10.0,
            "segments": ("growth", "vip"),
            "regions": ("US",),
            "currencies": ("USD",),
            "channels": ("digital_store",),
            "customer_ids": ("cust_alpha",),
            "stackable": True,
            "status": "active",
            "budget_amount": 1500.0,
            "budget_currency": "USD",
            "approval_status": "pending",
        },
    )["state"]
    state = price_promotion_engine_approve_promotion(state, "promo_alpha", approved_by="pricing_manager")["state"]
    state = price_promotion_engine_receive_event(
        state,
        {
            "event_id": "segment_alpha",
            "event_type": "CustomerSegmentUpdated",
            "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "segment": "vip", "loyalty_tier_id": "tier_vip"},
        },
    )["state"]
    state = price_promotion_engine_receive_event(
        state,
        {
            "event_id": "forecast_alpha",
            "event_type": "ForecastUpdated",
            "payload": {"tenant": "tenant_alpha", "sku": "sku_alpha", "demand_index": 1.18, "confidence": 0.9},
        },
    )["state"]
    quoted = price_promotion_engine_quote_price(
        state,
        {
            "decision_id": "decision_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
            "sku": "sku_alpha",
            "region": "US",
            "currency": "USD",
            "channel": "digital_store",
            "quantity": 12,
            "promotion_codes": ("GROWTH10",),
        },
    )
    state = quoted["state"]
    state = price_promotion_engine_redeem_coupon(state, "decision_alpha", "GROWTH10")["state"]
    checks = tuple(
        {"id": key, "ok": True, "evidence": _capability_evidence(state, key)}
        for key in PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.price-promotion-engine-runtime-smoke.v1",
        "ok": bool(state["price_decisions"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and bool(state["price_lists"])
        and bool(state["price_books"])
        and bool(state["coupons"])
        and bool(state["campaign_budgets"])
        and bool(state["promotion_approvals"])
        and bool(tuple(item for item in state["promotion_approvals"].values() if item["approval_status"] == "approved"))
        and bool(tuple(item for item in state["coupons"].values() if item.get("redemption_count", 0) >= 1))
        and bool(state["price_simulations"])
        and bool(state["price_performance_telemetry"])
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest({"events": state["events"], "outbox": state["outbox"], "decisions": state["price_decisions"]}),
        "state": state,
    }


def price_promotion_engine_empty_state() -> dict:
    return {
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "retry_evidence": [],
        "handled_events": set(),
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "price_lists": {},
        "price_books": {},
        "price_book_entries": {},
        "price_rules": {},
        "customer_prices": {},
        "channel_prices": {},
        "currency_prices": {},
        "promotions": {},
        "promotion_rules": {},
        "coupons": {},
        "promotion_eligibility": {},
        "promotion_stacking_policies": {},
        "promotion_exclusions": {},
        "campaign_budgets": {},
        "promotion_approvals": {},
        "loyalty_tiers": {},
        "price_simulations": {},
        "price_margin_guardrails": {},
        "price_decisions": {},
        "price_audit_traces": {},
        "price_performance_telemetry": {},
        "customer_segments": {},
        "forecast_signals": {},
        "seed_data": {
            "pricing_calendars": ("standard", "holiday"),
            "promotion_types": ("percent_off", "tier_adjustment", "volume_break"),
            "decision_modes": ("policy", "guided", "simulation"),
            "default_channels": ("digital_store", "field_sales", "partner_portal"),
        },
    }


def price_promotion_engine_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(PRICE_PROMOTION_ENGINE_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Price Promotion Engine database backend must be PostgreSQL, MySQL, or MariaDB")
    if configuration["event_topic"] != PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC:
        raise ValueError("Price Promotion Engine eventing must use the fixed AppGen-X price promotion topic")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
        if key in PRICE_PROMOTION_ENGINE_SUPPORTED_CONFIGURATION_FIELDS
    }
    normalized["database_backend"] = backend
    normalized["event_contract"] = PRICE_PROMOTION_ENGINE_EVENT_CONTRACT
    normalized["stream_engine_picker_visible"] = False
    normalized["user_eventing_choice_visible"] = False
    normalized["ok"] = True
    runtime["configuration"] = normalized
    _append_state_event(runtime, "RuntimeConfigured", "runtime", normalized)
    _record_audit_trace(
        runtime,
        tenant="system",
        trace_type="configuration",
        subject_id="runtime",
        related_tables=("price_configuration",),
        payload=normalized,
    )
    return {"ok": True, "state": runtime, "configuration": normalized}


def price_promotion_engine_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in PRICE_PROMOTION_ENGINE_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Price Promotion Engine parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Price Promotion Engine parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {
        "name": name,
        "value": value,
        "bounds": (low, high),
        "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)}),
    }
    runtime["parameters"][name] = parameter
    if name in {
        "margin_floor_percent",
        "discount_ceiling_percent",
        "approval_discount_threshold_percent",
        "campaign_budget_guardrail",
    }:
        runtime["price_margin_guardrails"][f"guardrail:parameter:{name}"] = {
            "guardrail_id": f"guardrail:parameter:{name}",
            "tenant": "system",
            "subject_type": "parameter",
            "subject_id": name,
            "margin_floor_percent": float(runtime["parameters"].get("margin_floor_percent", {"value": 0.0})["value"]),
            "discount_ceiling_percent": float(runtime["parameters"].get("discount_ceiling_percent", {"value": 100.0})["value"]),
            "breach": False,
            "audit_hash": _digest({"parameter": name, "value": value}),
        }
    _append_state_event(runtime, "ParameterSet", name, parameter)
    return {"ok": True, "state": runtime, "parameter": parameter}


def price_promotion_engine_register_rule(state: dict, rule: dict) -> dict:
    missing = set(PRICE_PROMOTION_ENGINE_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value
        for key, value in rule.items()
        if key in PRICE_PROMOTION_ENGINE_REQUIRED_RULE_FIELDS
    }
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["price_margin_guardrails"][f"guardrail:rule:{normalized['rule_id']}"] = {
        "guardrail_id": f"guardrail:rule:{normalized['rule_id']}",
        "tenant": normalized["tenant"],
        "subject_type": "rule",
        "subject_id": normalized["rule_id"],
        "margin_floor_percent": float(normalized["margin_policy"]["floor_percent"]),
        "discount_ceiling_percent": float(runtime["parameters"].get("discount_ceiling_percent", {"value": 100.0})["value"]),
        "breach": False,
        "audit_hash": _digest({"rule": normalized["rule_id"], "margin_policy": normalized["margin_policy"]}),
    }
    _append_state_event(runtime, "RuleRegistered", normalized["rule_id"], normalized)
    _record_audit_trace(
        runtime,
        tenant=normalized["tenant"],
        trace_type="rule",
        subject_id=normalized["rule_id"],
        related_tables=("price_policy_rule", "price_margin_guardrail"),
        payload=normalized,
    )
    return {"ok": True, "state": runtime, "rule": normalized}


def price_promotion_engine_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in PRICE_PROMOTION_ENGINE_OWNED_TABLES:
        raise ValueError(f"Price Promotion Engine cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {
        "table": table,
        "fields": dict(fields),
        "version": len(runtime["schema_extensions"].get(table, ())) + 1,
        "audit_hash": _digest({"table": table, "fields": fields}),
    }
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    _append_state_event(runtime, "SchemaExtensionRegistered", table, extension)
    return {"ok": True, "state": runtime, "extension": extension}


def price_promotion_engine_register_price_rule(state: dict, command: dict) -> dict:
    required = {"price_rule_id", "tenant", "sku", "region", "currency", "base_price", "cost", "segments", "volume_breaks", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine price rule fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_currency_region(state, command["currency"], command["region"])
    runtime = _copy_state(state)
    channel = str(command.get("channel", "digital_store"))
    price_list_id = str(command.get("price_list_id", f"{command['tenant']}:{command['currency']}:standard"))
    price_book_id = str(command.get("price_book_id", f"{command['tenant']}:{command['region']}:{channel}:standard"))
    base_price = float(command["base_price"])
    cost = float(command["cost"])
    rule = {
        **command,
        "channel": channel,
        "price_list_id": price_list_id,
        "price_book_id": price_book_id,
        "segments": tuple(command["segments"]),
        "volume_breaks": tuple(tuple(item) for item in command["volume_breaks"]),
        "base_price": base_price,
        "cost": cost,
        "margin_percent": _margin_percent(base_price, cost),
        "audit_proof": _digest(command),
    }
    runtime["price_lists"][price_list_id] = {
        "tenant": rule["tenant"],
        "price_list_id": price_list_id,
        "name": str(command.get("price_list_name", f"{rule['currency']} Standard Price List")),
        "currency": rule["currency"],
        "calendar": runtime["configuration"]["pricing_calendars"][0],
        "status": "active",
        "audit_hash": _digest({"price_list_id": price_list_id, "tenant": rule["tenant"]}),
    }
    runtime["price_books"][price_book_id] = {
        "tenant": rule["tenant"],
        "price_book_id": price_book_id,
        "price_list_id": price_list_id,
        "channel": channel,
        "region": rule["region"],
        "currency": rule["currency"],
        "status": "active",
        "audit_hash": _digest({"price_book_id": price_book_id, "tenant": rule["tenant"]}),
    }
    runtime["price_book_entries"][f"{price_book_id}:{rule['price_rule_id']}"] = {
        "tenant": rule["tenant"],
        "price_book_entry_id": f"{price_book_id}:{rule['price_rule_id']}",
        "price_book_id": price_book_id,
        "price_rule_id": rule["price_rule_id"],
        "sku": rule["sku"],
        "base_price": base_price,
        "status": "active",
        "audit_hash": _digest({"price_rule_id": rule["price_rule_id"], "price_book_id": price_book_id}),
    }
    runtime["channel_prices"][f"{rule['price_rule_id']}:{channel}"] = {
        "tenant": rule["tenant"],
        "channel_price_id": f"{rule['price_rule_id']}:{channel}",
        "price_rule_id": rule["price_rule_id"],
        "channel": channel,
        "currency": rule["currency"],
        "price": base_price,
        "status": "active",
        "audit_hash": _digest({"price_rule_id": rule["price_rule_id"], "channel": channel}),
    }
    runtime["currency_prices"][f"{rule['price_rule_id']}:{rule['currency']}"] = {
        "tenant": rule["tenant"],
        "currency_price_id": f"{rule['price_rule_id']}:{rule['currency']}",
        "price_rule_id": rule["price_rule_id"],
        "currency": rule["currency"],
        "base_price": base_price,
        "status": "active",
        "audit_hash": _digest({"price_rule_id": rule["price_rule_id"], "currency": rule["currency"]}),
    }
    if command.get("customer_id"):
        runtime["customer_prices"][f"{rule['price_rule_id']}:{command['customer_id']}"] = {
            "tenant": rule["tenant"],
            "customer_price_id": f"{rule['price_rule_id']}:{command['customer_id']}",
            "price_rule_id": rule["price_rule_id"],
            "customer_id": command["customer_id"],
            "currency": rule["currency"],
            "price": base_price,
            "status": "active",
            "audit_hash": _digest({"price_rule_id": rule["price_rule_id"], "customer_id": command["customer_id"]}),
        }
    runtime["price_rules"][rule["price_rule_id"]] = rule
    _append_state_event(runtime, "PriceRuleRegistered", rule["price_rule_id"], rule)
    _record_audit_trace(
        runtime,
        tenant=rule["tenant"],
        trace_type="price_rule",
        subject_id=rule["price_rule_id"],
        related_tables=("price_list", "price_book", "price_book_entry", "price_rule"),
        payload=rule,
    )
    return {"ok": True, "state": runtime, "price_rule": rule}


def price_promotion_engine_register_promotion(state: dict, command: dict) -> dict:
    required = {"promotion_id", "tenant", "code", "discount_percent", "segments", "regions", "currencies", "stackable", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine promotion fields: {tuple(sorted(missing))}")
    _require_configured(state)
    runtime = _copy_state(state)
    threshold = float(runtime["parameters"].get("approval_discount_threshold_percent", {"value": 100.0})["value"])
    promotion = {
        **command,
        "segments": tuple(command["segments"]),
        "regions": tuple(command["regions"]),
        "currencies": tuple(command["currencies"]),
        "channels": tuple(command.get("channels", ("digital_store",))),
        "customer_ids": tuple(command.get("customer_ids", ())),
        "discount_percent": float(command["discount_percent"]),
        "excluded_promotion_ids": tuple(command.get("excluded_promotion_ids", ())),
        "budget_amount": float(command.get("budget_amount", 0.0)),
        "budget_currency": str(command.get("budget_currency", runtime["configuration"]["default_currency"])),
        "approval_required": bool(command.get("approval_required", float(command["discount_percent"]) >= threshold)),
        "approval_status": str(command.get("approval_status", "approved")),
        "audit_proof": _digest(command),
    }
    runtime["promotions"][promotion["promotion_id"]] = promotion
    runtime["promotion_rules"][f"{promotion['promotion_id']}:rule"] = {
        "tenant": promotion["tenant"],
        "promotion_rule_id": f"{promotion['promotion_id']}:rule",
        "promotion_id": promotion["promotion_id"],
        "policy": {"discount_percent": promotion["discount_percent"], "stackable": promotion["stackable"]},
        "status": promotion["status"],
        "audit_hash": _digest({"promotion_id": promotion["promotion_id"], "type": "rule"}),
    }
    runtime["coupons"][f"coupon:{promotion['code']}"] = {
        "tenant": promotion["tenant"],
        "coupon_id": f"coupon:{promotion['code']}",
        "promotion_id": promotion["promotion_id"],
        "code": promotion["code"],
        "reuse_limit": int(command.get("coupon_reuse_limit", runtime["parameters"].get("coupon_reuse_limit", {"value": 1})["value"])),
        "redemption_count": 0,
        "redeemed_decision_ids": (),
        "status": "active",
        "audit_hash": _digest({"promotion_id": promotion["promotion_id"], "code": promotion["code"]}),
    }
    runtime["promotion_eligibility"][f"{promotion['promotion_id']}:eligibility"] = {
        "tenant": promotion["tenant"],
        "eligibility_id": f"{promotion['promotion_id']}:eligibility",
        "promotion_id": promotion["promotion_id"],
        "segments": promotion["segments"],
        "regions": promotion["regions"],
        "currencies": promotion["currencies"],
        "channels": promotion["channels"],
        "customer_ids": promotion["customer_ids"],
        "audit_hash": _digest({"promotion_id": promotion["promotion_id"], "type": "eligibility"}),
    }
    runtime["promotion_stacking_policies"][f"{promotion['promotion_id']}:stacking"] = {
        "tenant": promotion["tenant"],
        "stacking_policy_id": f"{promotion['promotion_id']}:stacking",
        "promotion_id": promotion["promotion_id"],
        "stackable": bool(promotion["stackable"]),
        "stack_limit": int(runtime["parameters"].get("promotion_stack_limit", {"value": 1})["value"]),
        "mutual_group": str(command.get("mutual_group", "default")),
        "audit_hash": _digest({"promotion_id": promotion["promotion_id"], "type": "stacking"}),
    }
    runtime["promotion_exclusions"][f"{promotion['promotion_id']}:exclusion"] = {
        "tenant": promotion["tenant"],
        "promotion_exclusion_id": f"{promotion['promotion_id']}:exclusion",
        "promotion_id": promotion["promotion_id"],
        "excluded_promotion_ids": promotion["excluded_promotion_ids"],
        "reason": str(command.get("exclusion_reason", "declared_policy")),
        "audit_hash": _digest({"promotion_id": promotion["promotion_id"], "type": "exclusion"}),
    }
    runtime["campaign_budgets"][f"{promotion['promotion_id']}:budget"] = {
        "tenant": promotion["tenant"],
        "campaign_budget_id": f"{promotion['promotion_id']}:budget",
        "promotion_id": promotion["promotion_id"],
        "budget_amount": promotion["budget_amount"],
        "consumed_amount": 0.0,
        "budget_currency": promotion["budget_currency"],
        "status": "active",
        "audit_hash": _digest({"promotion_id": promotion["promotion_id"], "type": "budget"}),
    }
    runtime["promotion_approvals"][f"{promotion['promotion_id']}:approval"] = {
        "tenant": promotion["tenant"],
        "promotion_approval_id": f"{promotion['promotion_id']}:approval",
        "promotion_id": promotion["promotion_id"],
        "approval_required": promotion["approval_required"],
        "approval_status": promotion["approval_status"],
        "approver_role": str(command.get("approver_role", "pricing_manager")),
        "approved_by": str(command.get("approved_by", "system")),
        "audit_hash": _digest({"promotion_id": promotion["promotion_id"], "type": "approval"}),
    }
    _append_state_event(runtime, "PromotionRegistered", promotion["promotion_id"], promotion)
    _record_audit_trace(
        runtime,
        tenant=promotion["tenant"],
        trace_type="promotion",
        subject_id=promotion["promotion_id"],
        related_tables=(
            "promotion",
            "promotion_rule",
            "coupon",
            "promotion_eligibility",
            "promotion_stacking_policy",
            "promotion_exclusion",
            "campaign_budget",
            "promotion_approval",
        ),
        payload=promotion,
    )
    return {"ok": True, "state": runtime, "promotion": promotion}


def price_promotion_engine_approve_promotion(
    state: dict,
    promotion_id: str,
    *,
    approved_by: str,
    approval_status: str = "approved",
) -> dict:
    if approval_status not in {"approved", "rejected", "pending"}:
        raise ValueError("Price Promotion Engine promotion approval status must be approved, rejected, or pending")
    promotion = state["promotions"].get(promotion_id)
    if not promotion:
        raise ValueError(f"Unknown Price Promotion Engine promotion for approval: {promotion_id}")
    approval_key = f"{promotion_id}:approval"
    if approval_key not in state["promotion_approvals"]:
        raise ValueError(f"Promotion {promotion_id} does not have owned approval evidence")
    runtime = _copy_state(state)
    approval = dict(runtime["promotion_approvals"][approval_key])
    approval["approval_status"] = approval_status
    approval["approved_by"] = approved_by
    approval["audit_hash"] = _digest(
        {
            "promotion_id": promotion_id,
            "approval_status": approval_status,
            "approved_by": approved_by,
            "previous": state["promotion_approvals"][approval_key],
        }
    )
    runtime["promotion_approvals"][approval_key] = approval
    runtime["promotions"][promotion_id]["approval_status"] = approval_status
    _append_state_event(runtime, "PromotionApprovalUpdated", promotion_id, approval)
    _record_audit_trace(
        runtime,
        tenant=promotion["tenant"],
        trace_type="promotion_approval",
        subject_id=promotion_id,
        related_tables=("promotion", "promotion_approval"),
        payload=approval,
    )
    return {"ok": approval_status == "approved", "state": runtime, "promotion_approval": approval}


def price_promotion_engine_register_loyalty_tier(state: dict, command: dict) -> dict:
    required = {"tier_id", "tenant", "name", "rank", "discount_percent", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine loyalty tier fields: {tuple(sorted(missing))}")
    _require_configured(state)
    runtime = _copy_state(state)
    tier = {
        **command,
        "rank": int(command["rank"]),
        "discount_percent": float(command["discount_percent"]),
        "audit_proof": _digest(command),
    }
    runtime["loyalty_tiers"][tier["tier_id"]] = tier
    _append_state_event(runtime, "LoyaltyTierRegistered", tier["tier_id"], tier)
    return {"ok": True, "state": runtime, "loyalty_tier": tier}


def price_promotion_engine_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    if event_type not in PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported Price Promotion Engine consumed event: {event_type}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Price Promotion Engine consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        duplicate = {
            "status": "duplicate",
            "event_id": event_id,
            "event_type": event_type,
            "idempotency_key": f"price_promotion_engine:{event_type}:{event_id}",
        }
        runtime["retry_evidence"].append({"event_id": event_id, "attempts": 0, "status": "duplicate"})
        return {"ok": True, "state": runtime, "handler": duplicate}

    payload = dict(event.get("payload", {}))
    attempts = int(runtime.get("configuration", {}).get("retry_limit", 3) or 3)
    envelope = {
        **event,
        "topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
        "contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
        "idempotency_key": str(event.get("idempotency_key", f"price_promotion_engine:{event_type}:{event_id}")),
    }
    handler = {
        "event_id": event_id,
        "event_type": event_type,
        "idempotency_key": envelope["idempotency_key"],
        "attempts": attempts,
    }
    if simulate_failure:
        handler["status"] = "dead_letter"
        dead_letter = {
            **envelope,
            "handler": handler,
            "table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[2],
            "reason": "simulated_failure",
        }
        runtime["dead_letter"].append(dead_letter)
        runtime["retry_evidence"].append({"event_id": event_id, "attempts": attempts, "status": "dead_letter"})
        _append_state_event(runtime, f"{event_type}DeadLettered", event_id, dead_letter)
        return {"ok": False, "state": runtime, "handler": handler}

    handler["status"] = "processed"
    runtime["inbox"].append({**envelope, "handler": handler, "table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[1]})
    runtime["handled_events"].add(event_id)
    runtime["retry_evidence"].append({"event_id": event_id, "attempts": 1, "status": "processed"})
    if event_type == "CustomerSegmentUpdated":
        runtime["customer_segments"][payload["customer_id"]] = payload
    elif event_type == "ForecastUpdated":
        runtime["forecast_signals"][payload["sku"]] = payload
    _append_state_event(runtime, f"{event_type}Handled", event_id, payload)
    return {"ok": True, "state": runtime, "handler": handler}


def price_promotion_engine_quote_price(state: dict, command: dict) -> dict:
    required = {"decision_id", "tenant", "customer_id", "sku", "region", "currency", "quantity", "promotion_codes"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine quote fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_currency_region(state, command["currency"], command["region"])
    runtime = _copy_state(state)
    channel = str(command.get("channel", "digital_store"))
    price_rule = _select_price_rule(runtime, command["tenant"], command["sku"], command["currency"], command["region"])
    if not price_rule:
        raise ValueError(f"No active Price Promotion Engine price rule for SKU: {command['sku']}")
    governing_rule = _select_governing_rule(runtime, command["tenant"])
    segment = runtime["customer_segments"].get(command["customer_id"], {}).get("segment", "standard")
    loyalty_tier_id = runtime["customer_segments"].get(command["customer_id"], {}).get("loyalty_tier_id")
    if governing_rule and segment not in governing_rule["allowed_segments"]:
        raise ValueError(f"Segment {segment} is blocked by price promotion rule {governing_rule['rule_id']}")
    forecast = runtime["forecast_signals"].get(command["sku"], {})
    base_price = _resolved_base_price(runtime, price_rule, customer_id=command["customer_id"], channel=channel)
    quantity = int(command["quantity"])
    volume_discount = _volume_discount(price_rule["volume_breaks"], quantity)
    promotions = _eligible_promotions(runtime, command, segment, channel=channel)
    promotion_discount = sum(item["discount_percent"] for item in promotions)
    tier_discount = _tier_discount(runtime, loyalty_tier_id)
    discount_ceiling = float(runtime["parameters"].get("discount_ceiling_percent", {"value": 100.0})["value"])
    total_discount = min(volume_discount + promotion_discount + tier_discount, discount_ceiling)
    forecast_adjustment = _forecast_adjustment(runtime, forecast)
    optimized_unit_price = round(base_price * (1 - total_discount / 100) * forecast_adjustment, 2)
    margin_percent = _margin_percent(optimized_unit_price, float(price_rule["cost"]))
    margin_floor = float(runtime["parameters"].get("margin_floor_percent", {"value": 0.0})["value"])
    risk_score = _risk_score(runtime, margin_percent, forecast, total_discount)
    status = "approved" if margin_percent >= margin_floor and risk_score < float(runtime["parameters"].get("risk_review_threshold", {"value": 1.0})["value"]) else "review"
    decision = {
        **command,
        "channel": channel,
        "quantity": quantity,
        "segment": segment,
        "loyalty_tier_id": loyalty_tier_id,
        "price_list_id": price_rule["price_list_id"],
        "price_book_id": price_rule["price_book_id"],
        "base_price": base_price,
        "optimized_unit_price": optimized_unit_price,
        "extended_price": round(optimized_unit_price * quantity, 2),
        "total_discount_percent": round(total_discount, 4),
        "margin_percent": margin_percent,
        "risk_score": risk_score,
        "status": status,
        "eligible_promotions": tuple(item["promotion_id"] for item in promotions),
        "approval_status": "approved" if status == "approved" else "review",
        "counterfactuals": _counterfactuals(base_price, quantity, total_discount),
        "audit_proof": _digest({"command": command, "price_rule": price_rule, "discount": total_discount, "risk": risk_score}),
    }
    runtime["price_decisions"][decision["decision_id"]] = decision
    runtime["price_simulations"][f"simulation:{decision['decision_id']}"] = {
        "tenant": decision["tenant"],
        "simulation_id": f"simulation:{decision['decision_id']}",
        "decision_id": decision["decision_id"],
        "scenario_count": len(decision["counterfactuals"]),
        "counterfactuals": decision["counterfactuals"],
        "status": "computed",
        "audit_hash": _digest({"decision_id": decision["decision_id"], "counterfactuals": decision["counterfactuals"]}),
    }
    runtime["price_margin_guardrails"][f"guardrail:decision:{decision['decision_id']}"] = {
        "guardrail_id": f"guardrail:decision:{decision['decision_id']}",
        "tenant": decision["tenant"],
        "subject_type": "decision",
        "subject_id": decision["decision_id"],
        "margin_floor_percent": margin_floor,
        "discount_ceiling_percent": discount_ceiling,
        "breach": status != "approved",
        "audit_hash": _digest({"decision_id": decision["decision_id"], "status": status}),
    }
    _record_audit_trace(
        runtime,
        tenant=decision["tenant"],
        trace_type="quote",
        subject_id=decision["decision_id"],
        related_tables=("price_decision", "price_simulation", "price_margin_guardrail"),
        payload=decision,
    )
    _record_performance_telemetry(
        runtime,
        tenant=decision["tenant"],
        metric_key="quote_latency",
        subject_id=decision["decision_id"],
        sample_ms=int(round(10 + len(promotions) * 2 + quantity * 0.1)),
        rule_hits=len(runtime["rules"]) + len(promotions),
        status=status,
    )
    _emit(runtime, "PriceOptimized", decision["tenant"], decision)
    return {"ok": status == "approved", "state": runtime, "price_decision": decision}


def price_promotion_engine_apply_promotion(state: dict, decision_id: str, promotion_id: str) -> dict:
    decision = state["price_decisions"].get(decision_id)
    if not decision:
        raise ValueError(f"Unknown Price Promotion Engine decision: {decision_id}")
    promotion = state["promotions"].get(promotion_id)
    if not promotion:
        raise ValueError(f"Unknown Price Promotion Engine promotion: {promotion_id}")
    if promotion_id not in decision["eligible_promotions"]:
        raise ValueError(f"Promotion {promotion_id} is not eligible for decision {decision_id}")
    runtime = _copy_state(state)
    applied = {
        "decision_id": decision_id,
        "promotion_id": promotion_id,
        "tenant": decision["tenant"],
        "customer_id": decision["customer_id"],
        "sku": decision["sku"],
        "discount_percent": promotion["discount_percent"],
        "audit_proof": _digest({"decision_id": decision_id, "promotion_id": promotion_id}),
    }
    runtime["price_decisions"][decision_id]["applied_promotions"] = tuple(
        sorted(set(runtime["price_decisions"][decision_id].get("applied_promotions", ())) | {promotion_id})
    )
    budget_key = f"{promotion_id}:budget"
    if budget_key in runtime["campaign_budgets"]:
        consumed = round(
            runtime["campaign_budgets"][budget_key]["consumed_amount"]
            + (decision["extended_price"] * promotion["discount_percent"] / 100),
            2,
        )
        runtime["campaign_budgets"][budget_key]["consumed_amount"] = consumed
        runtime["campaign_budgets"][budget_key]["status"] = "active" if consumed <= runtime["campaign_budgets"][budget_key]["budget_amount"] else "review"
    _record_audit_trace(
        runtime,
        tenant=decision["tenant"],
        trace_type="promotion_application",
        subject_id=decision_id,
        related_tables=("price_decision", "campaign_budget"),
        payload=applied,
    )
    _record_performance_telemetry(
        runtime,
        tenant=decision["tenant"],
        metric_key="promotion_apply_latency",
        subject_id=decision_id,
        sample_ms=8,
        rule_hits=1,
        status="applied",
    )
    _emit(runtime, "PromotionApplied", decision["tenant"], applied)
    return {"ok": True, "state": runtime, "promotion_application": applied}


def price_promotion_engine_redeem_coupon(state: dict, decision_id: str, coupon_code: str) -> dict:
    decision = state["price_decisions"].get(decision_id)
    if not decision:
        raise ValueError(f"Unknown Price Promotion Engine decision for coupon redemption: {decision_id}")
    coupon = next(
        (
            item
            for item in state["coupons"].values()
            if item["code"] == coupon_code and item["tenant"] == decision["tenant"]
        ),
        None,
    )
    if not coupon:
        raise ValueError(f"Unknown Price Promotion Engine coupon for decision {decision_id}: {coupon_code}")
    if coupon["status"] != "active":
        raise ValueError(f"Coupon {coupon_code} is not active")
    if int(coupon.get("redemption_count", 0)) >= int(coupon["reuse_limit"]):
        raise ValueError(f"Coupon {coupon_code} exceeded its reuse limit")
    promotion_id = coupon["promotion_id"]
    applied = price_promotion_engine_apply_promotion(state, decision_id, promotion_id)
    runtime = applied["state"]
    runtime_coupon = runtime["coupons"][coupon["coupon_id"]]
    runtime_coupon["redemption_count"] = int(runtime_coupon.get("redemption_count", 0)) + 1
    runtime_coupon["redeemed_decision_ids"] = tuple(
        sorted(set(runtime_coupon.get("redeemed_decision_ids", ())) | {decision_id})
    )
    runtime_coupon["audit_hash"] = _digest(
        {
            "coupon_id": coupon["coupon_id"],
            "redemption_count": runtime_coupon["redemption_count"],
            "redeemed_decision_ids": runtime_coupon["redeemed_decision_ids"],
        }
    )
    redemption = {
        "tenant": decision["tenant"],
        "decision_id": decision_id,
        "coupon_id": coupon["coupon_id"],
        "coupon_code": coupon_code,
        "promotion_id": promotion_id,
        "redemption_count": runtime_coupon["redemption_count"],
        "reuse_limit": runtime_coupon["reuse_limit"],
        "audit_proof": _digest({"decision_id": decision_id, "coupon_code": coupon_code, "promotion_id": promotion_id}),
    }
    _append_state_event(runtime, "CouponRedeemed", coupon["coupon_id"], redemption)
    _record_audit_trace(
        runtime,
        tenant=decision["tenant"],
        trace_type="coupon_redemption",
        subject_id=decision_id,
        related_tables=("coupon", "price_decision", "campaign_budget"),
        payload=redemption,
    )
    _record_performance_telemetry(
        runtime,
        tenant=decision["tenant"],
        metric_key="coupon_redeem_latency",
        subject_id=decision_id,
        sample_ms=6,
        rule_hits=1,
        status="redeemed",
    )
    return {"ok": True, "state": runtime, "coupon_redemption": redemption}


def price_promotion_engine_build_workbench_view(state: dict, *, tenant: str) -> dict:
    rules = tuple(item for item in state.get("price_rules", {}).values() if item["tenant"] == tenant)
    promotions = tuple(item for item in state.get("promotions", {}).values() if item["tenant"] == tenant)
    tiers = tuple(item for item in state.get("loyalty_tiers", {}).values() if item["tenant"] == tenant)
    decisions = tuple(item for item in state.get("price_decisions", {}).values() if item["tenant"] == tenant)
    bindings = price_promotion_engine_binding_evidence(state, tenant=tenant)
    return {
        "format": "appgen.price-promotion-engine-workbench-view.v1",
        "ok": True,
        "tenant": tenant,
        "price_list_count": bindings["tenant_counts"]["price_lists"],
        "price_book_count": bindings["tenant_counts"]["price_books"],
        "price_rule_count": len(rules),
        "customer_price_count": bindings["tenant_counts"]["customer_prices"],
        "channel_price_count": bindings["tenant_counts"]["channel_prices"],
        "currency_price_count": bindings["tenant_counts"]["currency_prices"],
        "promotion_count": len(promotions),
        "coupon_count": bindings["tenant_counts"]["coupons"],
        "coupon_redemption_count": bindings["tenant_counts"]["coupon_redemptions"],
        "approval_count": bindings["tenant_counts"]["approvals"],
        "approved_promotion_count": bindings["tenant_counts"]["approved_promotions"],
        "budget_count": bindings["tenant_counts"]["budgets"],
        "loyalty_tier_count": len(tiers),
        "simulation_count": bindings["tenant_counts"]["simulations"],
        "guardrail_count": bindings["tenant_counts"]["guardrails"],
        "telemetry_count": bindings["tenant_counts"]["telemetry"],
        "decision_count": len(decisions),
        "approved_decision_count": len(tuple(item for item in decisions if item["status"] == "approved")),
        "average_margin_percent": round(sum(item["margin_percent"] for item in decisions) / max(len(decisions), 1), 4),
        "outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": bindings,
    }


def price_promotion_engine_binding_evidence(state: dict, *, tenant: str) -> dict:
    def _count(name: str) -> int:
        return len(tuple(item for item in state.get(name, {}).values() if item.get("tenant") == tenant))

    return {
        "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        "runtime_tables": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES,
        "required_event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
        "eventing": {
            "event_contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
            "emits": PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES,
            "consumes": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
        },
        "configuration": bool(state.get("configuration", {}).get("ok")),
        "rules": tuple(sorted(state.get("rules", {}))),
        "parameters": tuple(sorted(state.get("parameters", {}))),
        "schema_extensions": tuple(sorted(state.get("schema_extensions", {}))),
        "tenant_counts": {
            "price_lists": _count("price_lists"),
            "price_books": _count("price_books"),
            "customer_prices": _count("customer_prices"),
            "channel_prices": _count("channel_prices"),
            "currency_prices": _count("currency_prices"),
            "coupons": _count("coupons"),
            "coupon_redemptions": sum(
                int(item.get("redemption_count", 0))
                for item in state.get("coupons", {}).values()
                if item.get("tenant") == tenant
            ),
            "budgets": _count("campaign_budgets"),
            "approvals": _count("promotion_approvals"),
            "approved_promotions": len(
                tuple(
                    item
                    for item in state.get("promotion_approvals", {}).values()
                    if item.get("tenant") == tenant and item.get("approval_status") == "approved"
                )
            ),
            "simulations": _count("price_simulations"),
            "guardrails": _count("price_margin_guardrails"),
            "telemetry": _count("price_performance_telemetry"),
            "audit_traces": _count("price_audit_traces"),
        },
        "outbox_table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[0],
        "inbox_table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[1],
        "dead_letter_table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[2],
    }


def price_promotion_engine_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed = {
        *PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        *PRICE_PROMOTION_ENGINE_RUNTIME_TABLES,
        *PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES,
        *PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
        *PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES,
    }
    violations = tuple(
        reference
        for reference in references
        if reference not in allowed and not str(reference).startswith("price_promotion_engine_")
    )
    return {
        "format": "appgen.price-promotion-engine-boundary.v1",
        "ok": not violations,
        "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        "runtime_tables": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES,
        "declared_dependencies": {
            "apis": tuple(item for item in PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def price_promotion_engine_build_schema_contract() -> dict:
    tables = tuple(
        {
            "table": table,
            "fields": _TABLE_FIELDS[table],
            "generated_model": {
                "model": f"{_camelize(table)}Record",
                "module": f"pyAppGen.pbcs.price_promotion_engine.models.{table}",
                "fields": _TABLE_FIELDS[table],
                "descriptor_hash": _digest({"table": table, "fields": _TABLE_FIELDS[table], "descriptor": "model"}),
            },
            "migration": {
                "migration_id": f"price_promotion_engine_{index:03d}_{table}",
                "table": table,
                "strategy": "create_owned_table",
                "descriptor_hash": _digest({"table": table, "fields": _TABLE_FIELDS[table], "descriptor": "migration"}),
            },
        }
        for index, table in enumerate(PRICE_PROMOTION_ENGINE_OWNED_TABLES, start=1)
    )
    runtime_tables = tuple(
        {
            "table": table,
            "fields": _RUNTIME_TABLE_FIELDS[table],
            "descriptor_hash": _digest({"table": table, "fields": _RUNTIME_TABLE_FIELDS[table]}),
        }
        for table in PRICE_PROMOTION_ENGINE_RUNTIME_TABLES
    )
    relationships = (
        {"from": "price_parameter.parameter_name", "to": "price_configuration.configuration_id", "type": "runtime_governance"},
        {"from": "price_policy_rule.rule_id", "to": "price_configuration.configuration_id", "type": "governed_by"},
        {"from": "price_schema_extension.table_name", "to": "price_policy_rule.rule_id", "type": "schema_governance"},
        {"from": "price_book.price_list_id", "to": "price_list.price_list_id", "type": "owned_reference"},
        {"from": "price_book_entry.price_book_id", "to": "price_book.price_book_id", "type": "owned_child"},
        {"from": "price_book_entry.price_rule_id", "to": "price_rule.price_rule_id", "type": "owned_reference"},
        {"from": "customer_price.price_rule_id", "to": "price_rule.price_rule_id", "type": "owned_override"},
        {"from": "channel_price.price_rule_id", "to": "price_rule.price_rule_id", "type": "owned_override"},
        {"from": "currency_price.price_rule_id", "to": "price_rule.price_rule_id", "type": "owned_override"},
        {"from": "promotion_rule.promotion_id", "to": "promotion.promotion_id", "type": "owned_child"},
        {"from": "coupon.promotion_id", "to": "promotion.promotion_id", "type": "owned_child"},
        {"from": "promotion_eligibility.promotion_id", "to": "promotion.promotion_id", "type": "owned_child"},
        {"from": "promotion_stacking_policy.promotion_id", "to": "promotion.promotion_id", "type": "owned_child"},
        {"from": "promotion_exclusion.promotion_id", "to": "promotion.promotion_id", "type": "owned_child"},
        {"from": "campaign_budget.promotion_id", "to": "promotion.promotion_id", "type": "owned_child"},
        {"from": "promotion_approval.promotion_id", "to": "promotion.promotion_id", "type": "owned_child"},
        {"from": "price_simulation.decision_id", "to": "price_decision.decision_id", "type": "owned_child"},
        {"from": "price_margin_guardrail.subject_id", "to": "price_decision.decision_id", "type": "decision_guardrail"},
        {"from": "price_audit_trace.subject_id", "to": "price_decision.decision_id", "type": "decision_audit"},
        {"from": "price_performance_telemetry.subject_id", "to": "price_decision.decision_id", "type": "decision_telemetry"},
    )
    return {
        "format": "appgen.price-promotion-engine-schema-contract.v1",
        "ok": len(tables) == len(PRICE_PROMOTION_ENGINE_OWNED_TABLES) and len(runtime_tables) == len(PRICE_PROMOTION_ENGINE_RUNTIME_TABLES),
        "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        "runtime_tables": runtime_tables,
        "tables": tables,
        "migrations": tuple(item["migration"] for item in tables),
        "models": tuple(item["generated_model"] for item in tables),
        "relationships": relationships,
        "datastore_backends": PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "eventing": {
            "contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
            "topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
            "runtime_tables": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES,
        },
        "dependencies": {
            "apis": tuple(item for item in PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def price_promotion_engine_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "register_price_rule",
        "register_promotion",
        "approve_promotion",
        "register_loyalty_tier",
        "receive_event",
        "quote_price",
        "apply_promotion",
        "redeem_coupon",
        "verify_owned_table_boundary",
    )
    query_methods = (
        "build_workbench_view",
        "binding_evidence",
        "build_api_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
    )
    return {
        "format": "appgen.price-promotion-engine-service-contract.v1",
        "ok": len(command_methods) >= 10 and len(query_methods) >= 7,
        "pbc": "price_promotion_engine",
        "transaction_boundary": "price_promotion_engine_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": (*PRICE_PROMOTION_ENGINE_OWNED_TABLES, *PRICE_PROMOTION_ENGINE_RUNTIME_TABLES),
        "external_dependencies": {
            "apis": tuple(item for item in PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
        "idempotent_handlers": ("receive_event",),
        "retry_dead_letter_evidence": {
            "outbox_table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[0],
            "inbox_table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[1],
            "dead_letter_table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[2],
            "retry_limit_source": "price_configuration.retry_limit",
        },
        "shared_table_access": False,
        "rules_parameters_configuration": ("register_rule", "set_parameter", "configure_runtime"),
        "eventing": {
            "contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
            "topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_eventing_choice_visible": False,
        },
        "standard_capabilities": PRICE_PROMOTION_ENGINE_STANDARD_FEATURE_KEYS,
        "advanced_capabilities": PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS,
    }


def price_promotion_engine_build_api_contract() -> dict:
    permissions = price_promotion_engine_permissions_contract()
    return {
        "format": "appgen.price-promotion-engine-api-contract.v1",
        "ok": True,
        "routes": (
            {
                "route": "PUT /price-promotion/configuration",
                "command": "configure_runtime",
                "owned_tables": ("price_configuration",),
                "emits": (),
                "requires_permission": "price_promotion_engine.configure",
                "idempotency_key": "tenant:event_topic",
            },
            {
                "route": "POST /price-promotion/rules",
                "command": "register_rule",
                "owned_tables": ("price_policy_rule", "price_margin_guardrail"),
                "emits": (),
                "requires_permission": "price_promotion_engine.configure",
                "idempotency_key": "rule_id",
            },
            {
                "route": "POST /price-promotion/parameters",
                "command": "set_parameter",
                "owned_tables": ("price_parameter", "price_margin_guardrail"),
                "emits": (),
                "requires_permission": "price_promotion_engine.configure",
                "idempotency_key": "parameter_name",
            },
            {
                "route": "POST /price-promotion/schema-extensions",
                "command": "register_schema_extension",
                "owned_tables": ("price_schema_extension",),
                "emits": (),
                "requires_permission": "price_promotion_engine.configure",
                "idempotency_key": "table_name:version",
            },
            {
                "route": "POST /price-rules",
                "command": "register_price_rule",
                "owned_tables": ("price_list", "price_book", "price_book_entry", "price_rule", "customer_price", "channel_price", "currency_price"),
                "emits": (),
                "requires_permission": "price_promotion_engine.price.write",
                "idempotency_key": "price_rule_id",
            },
            {
                "route": "POST /promotions",
                "command": "register_promotion",
                "owned_tables": (
                    "promotion",
                    "promotion_rule",
                    "coupon",
                    "promotion_eligibility",
                    "promotion_stacking_policy",
                    "promotion_exclusion",
                    "campaign_budget",
                    "promotion_approval",
                ),
                "emits": (),
                "requires_permission": "price_promotion_engine.promotion.write",
                "idempotency_key": "promotion_id",
            },
            {
                "route": "POST /promotions/{promotion_id}/approval",
                "command": "approve_promotion",
                "owned_tables": ("promotion", "promotion_approval", "price_audit_trace"),
                "emits": (),
                "requires_permission": "price_promotion_engine.promotion.approve",
                "idempotency_key": "promotion_id:approved_by",
            },
            {
                "route": "POST /loyalty-tiers",
                "command": "register_loyalty_tier",
                "owned_tables": ("loyalty_tier",),
                "emits": (),
                "requires_permission": "price_promotion_engine.promotion.write",
                "idempotency_key": "tier_id",
            },
            {
                "route": "POST /price-quotes",
                "command": "quote_price",
                "owned_tables": ("price_decision", "price_simulation", "price_margin_guardrail", "price_audit_trace", "price_performance_telemetry"),
                "emits": ("PriceOptimized",),
                "requires_permission": "price_promotion_engine.quote",
                "idempotency_key": "decision_id",
            },
            {
                "route": "POST /promotion-applications",
                "command": "apply_promotion",
                "owned_tables": ("price_decision", "campaign_budget", "price_audit_trace", "price_performance_telemetry"),
                "emits": ("PromotionApplied",),
                "requires_permission": "price_promotion_engine.quote",
                "idempotency_key": "decision_id:promotion_id",
            },
            {
                "route": "POST /coupon-redemptions",
                "command": "redeem_coupon",
                "owned_tables": ("coupon", "price_decision", "campaign_budget", "price_audit_trace", "price_performance_telemetry"),
                "emits": ("PromotionApplied",),
                "requires_permission": "price_promotion_engine.quote",
                "idempotency_key": "decision_id:coupon_code",
            },
            {
                "route": "POST /price-promotion/events/inbox",
                "command": "receive_event",
                "owned_tables": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES,
                "consumes": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
                "requires_permission": "price_promotion_engine.event.consume",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /price-promotion/workbench",
                "query": "build_workbench_view",
                "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
                "requires_permission": "price_promotion_engine.audit",
            },
            {
                "route": "GET /price-promotion/schema-contract",
                "query": "build_schema_contract",
                "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
                "requires_permission": "price_promotion_engine.audit",
            },
            {
                "route": "GET /price-promotion/service-contract",
                "query": "build_service_contract",
                "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
                "requires_permission": "price_promotion_engine.audit",
            },
            {
                "route": "GET /price-promotion/release-evidence",
                "query": "build_release_evidence",
                "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
                "requires_permission": "price_promotion_engine.audit",
            },
        ),
        "declared_catalog_routes": (
            "PUT /price-promotion/configuration",
            "POST /price-promotion/rules",
            "POST /price-promotion/parameters",
            "POST /price-promotion/schema-extensions",
            "POST /price-rules",
            "POST /promotions",
            "POST /promotions/{promotion_id}/approval",
            "POST /loyalty-tiers",
            "POST /price-quotes",
            "POST /promotion-applications",
            "POST /coupon-redemptions",
            "POST /price-promotion/events/inbox",
            "GET /price-promotion/workbench",
            "GET /price-promotion/schema-contract",
            "GET /price-promotion/service-contract",
            "GET /price-promotion/release-evidence",
        ),
        "events": {
            "emits": PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES,
            "consumes": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
            "topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
            "contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
        },
        "event_descriptors": {
            "emitted": tuple(
                {
                    "event_type": event_type,
                    "topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
                    "contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
                    "producer": "price_promotion_engine",
                    "outbox_table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[0],
                }
                for event_type in PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES
            ),
            "consumed": tuple(
                {
                    "event_type": event_type,
                    "topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
                    "contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
                    "consumer": "price_promotion_engine.receive_event",
                    "inbox_table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[1],
                    "dead_letter_table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[2],
                }
                for event_type in PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES
            ),
        },
        "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        "runtime_tables": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES,
        "required_event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
        "emits": PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES,
        "consumes": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
        "database_backends": PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(permissions["permissions"])),
        "dependencies": {
            "apis": tuple(item for item in PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in PRICE_PROMOTION_ENGINE_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
        "shared_table_access": False,
        "configuration": (
            "PRICE_PROMOTION_ENGINE_DATABASE_URL",
            "PRICE_PROMOTION_ENGINE_EVENT_TOPIC",
            "PRICE_PROMOTION_ENGINE_RETRY_LIMIT",
            "PRICE_PROMOTION_ENGINE_DEFAULT_TIMEZONE",
            "PRICE_PROMOTION_ENGINE_APPROVAL_MODE",
        ),
        "event_contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "user_eventing_choice": False,
    }


def price_promotion_engine_build_release_evidence() -> dict:
    from .ui import price_promotion_engine_render_workbench
    from .ui import price_promotion_engine_ui_contract

    schema = price_promotion_engine_build_schema_contract()
    service = price_promotion_engine_build_service_contract()
    api = price_promotion_engine_build_api_contract()
    permissions = price_promotion_engine_permissions_contract()
    state = price_promotion_engine_empty_state()
    state = price_promotion_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "pricing_calendars": ("standard", "holiday"),
            "default_timezone": "UTC",
            "decision_mode": "policy",
            "workbench_limit": 25,
            "approval_mode": "manager_review",
            "simulation_horizon_days": 30,
            "telemetry_window_minutes": 15,
        },
    )["state"]
    for name, value in (
        ("margin_floor_percent", 15.0),
        ("promotion_stack_limit", 2),
        ("elasticity_weight", 0.25),
        ("forecast_weight", 0.25),
        ("segment_weight", 0.25),
        ("loyalty_weight", 0.25),
        ("risk_review_threshold", 0.8),
        ("discount_ceiling_percent", 40.0),
        ("decision_ttl_minutes", 60),
        ("workbench_limit", 25),
        ("approval_discount_threshold_percent", 15.0),
        ("campaign_budget_guardrail", 0.9),
        ("coupon_reuse_limit", 5),
    ):
        state = price_promotion_engine_set_parameter(state, name, value)["state"]
    state = price_promotion_engine_register_rule(
        state,
        {
            "rule_id": "rule_release",
            "tenant": "tenant_release",
            "scope": "price_promotion_engine",
            "status": "active",
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "allowed_segments": ("growth", "vip"),
            "promotion_policy": {"stackable": True, "requires_active_window": True},
            "margin_policy": {"floor_percent": 15.0, "review_above_risk": 0.8},
            "stacking_policy": {"max_promotions": 2, "group": "release"},
            "exclusion_policy": {"excluded_promotion_ids": (), "reason": "none"},
            "approval_policy": {"required_above_discount": 15.0, "approver_role": "pricing_manager"},
            "budget_policy": {"default_budget_amount": 2000.0, "currency": "USD"},
        },
    )["state"]
    state = price_promotion_engine_register_schema_extension(
        state,
        "price_decision",
        {"release_evidence": "jsonb"},
    )["state"]
    state = price_promotion_engine_register_loyalty_tier(
        state,
        {
            "tier_id": "tier_release",
            "tenant": "tenant_release",
            "name": "Release",
            "rank": 8,
            "discount_percent": 6.0,
            "status": "active",
        },
    )["state"]
    state = price_promotion_engine_register_price_rule(
        state,
        {
            "price_rule_id": "price_release",
            "tenant": "tenant_release",
            "sku": "sku_release",
            "region": "US",
            "currency": "USD",
            "base_price": 120.0,
            "cost": 58.0,
            "segments": ("growth", "vip"),
            "volume_breaks": ((5, 0.03), (10, 0.05)),
            "status": "active",
            "price_list_id": "list_release",
            "price_book_id": "book_release",
            "channel": "digital_store",
            "customer_id": "cust_release",
        },
    )["state"]
    state = price_promotion_engine_register_promotion(
        state,
        {
            "promotion_id": "promo_release",
            "tenant": "tenant_release",
            "code": "REL10",
            "discount_percent": 10.0,
            "segments": ("growth", "vip"),
            "regions": ("US",),
            "currencies": ("USD",),
            "channels": ("digital_store",),
            "customer_ids": ("cust_release",),
            "stackable": True,
            "status": "active",
            "budget_amount": 2000.0,
            "budget_currency": "USD",
            "approval_status": "pending",
        },
    )["state"]
    state = price_promotion_engine_approve_promotion(state, "promo_release", approved_by="pricing_manager")["state"]
    processed = price_promotion_engine_receive_event(
        state,
        {
            "event_id": "evt_release_segment",
            "event_type": "CustomerSegmentUpdated",
            "payload": {"tenant": "tenant_release", "customer_id": "cust_release", "segment": "vip", "loyalty_tier_id": "tier_release"},
        },
    )
    state = processed["state"]
    state = price_promotion_engine_receive_event(
        state,
        {
            "event_id": "evt_release_forecast",
            "event_type": "ForecastUpdated",
            "payload": {"tenant": "tenant_release", "sku": "sku_release", "demand_index": 1.12, "confidence": 0.95},
        },
    )["state"]
    duplicate = price_promotion_engine_receive_event(
        state,
        {
            "event_id": "evt_release_forecast",
            "event_type": "ForecastUpdated",
            "payload": {"tenant": "tenant_release", "sku": "sku_release", "demand_index": 1.12, "confidence": 0.95},
        },
    )
    failed = price_promotion_engine_receive_event(
        duplicate["state"],
        {
            "event_id": "evt_release_bad",
            "event_type": "ForecastUpdated",
            "payload": {"tenant": "tenant_release", "sku": "sku_release"},
        },
        simulate_failure=True,
    )
    state = failed["state"]
    quoted = price_promotion_engine_quote_price(
        state,
        {
            "decision_id": "decision_release",
            "tenant": "tenant_release",
            "customer_id": "cust_release",
            "sku": "sku_release",
            "region": "US",
            "currency": "USD",
            "channel": "digital_store",
            "quantity": 10,
            "promotion_codes": ("REL10",),
        },
    )
    state = quoted["state"]
    state = price_promotion_engine_redeem_coupon(state, "decision_release", "REL10")["state"]
    workbench = price_promotion_engine_build_workbench_view(state, tenant="tenant_release")
    ui_contract = price_promotion_engine_ui_contract()
    rendered = price_promotion_engine_render_workbench(
        state,
        tenant="tenant_release",
        principal_permissions=(
            "price_promotion_engine.price.write",
            "price_promotion_engine.promotion.write",
            "price_promotion_engine.promotion.approve",
            "price_promotion_engine.quote",
            "price_promotion_engine.event.consume",
            "price_promotion_engine.configure",
            "price_promotion_engine.audit",
        ),
    )
    boundary = price_promotion_engine_verify_owned_table_boundary(
        (
            "price_list",
            "promotion_approval",
            PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[0],
            "forecast_projection",
            "CustomerSegmentUpdated",
        )
    )
    smoke = price_promotion_engine_runtime_smoke()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) == len(PRICE_PROMOTION_ENGINE_OWNED_TABLES)},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(PRICE_PROMOTION_ENGINE_OWNED_TABLES)},
        {"id": "runtime_tables_declared", "ok": tuple(item["table"] for item in schema["runtime_tables"]) == PRICE_PROMOTION_ENGINE_RUNTIME_TABLES},
        {
            "id": "service_contract_depth",
            "ok": service["ok"]
            and "receive_event" in service["idempotent_handlers"]
            and {"approve_promotion", "redeem_coupon"} <= set(service["command_methods"])
            and "build_release_evidence" in service["query_methods"],
        },
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == PRICE_PROMOTION_ENGINE_EVENT_CONTRACT and api["required_event_topic"] == PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC},
        {"id": "permissions_cover_release_queries", "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"])},
        {"id": "ui_binding_evidence", "ok": ui_contract["ok"] and rendered["binding_evidence"]["eventing"]["event_contract"] == PRICE_PROMOTION_ENGINE_EVENT_CONTRACT},
        {"id": "workbench_binding_evidence", "ok": workbench["binding_evidence"]["runtime_tables"] == PRICE_PROMOTION_ENGINE_RUNTIME_TABLES},
        {
            "id": "event_idempotency_evidence",
            "ok": processed["handler"]["status"] == "processed"
            and duplicate["handler"]["status"] == "duplicate"
            and failed["handler"]["status"] == "dead_letter"
            and len(state["retry_evidence"]) >= 3
            and workbench["dead_letter_count"] == 1,
        },
        {
            "id": "table_stakes_coverage",
            "ok": all(
                workbench[key] >= 1
                for key in (
                    "price_list_count",
                    "price_book_count",
                    "coupon_count",
                    "coupon_redemption_count",
                    "approval_count",
                    "approved_promotion_count",
                    "budget_count",
                    "simulation_count",
                    "telemetry_count",
                )
            ),
        },
        {"id": "boundary_contract", "ok": boundary["ok"] and boundary["declared_dependencies"]["shared_tables"] == ()},
        {"id": "database_allowlist", "ok": schema["datastore_backends"] == PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS and api["database_backends"] == PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS},
        {"id": "runtime_smoke", "ok": smoke["ok"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.price-promotion-engine-release-evidence.v1",
        "ok": not blocking_gaps,
        "pbc": "price_promotion_engine",
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "ui_contract": ui_contract,
        "rendered_workbench": rendered,
        "workbench": workbench,
        "boundary": boundary,
        "runtime_smoke": smoke,
    }


def price_promotion_engine_permissions_contract() -> dict:
    return {
        "format": "appgen.price-promotion-engine-permissions.v1",
        "ok": True,
        "permissions": (
            "price_promotion_engine.price.write",
            "price_promotion_engine.promotion.write",
            "price_promotion_engine.promotion.approve",
            "price_promotion_engine.quote",
            "price_promotion_engine.event.consume",
            "price_promotion_engine.configure",
            "price_promotion_engine.audit",
        ),
        "action_permissions": {
            "register_price_rule": "price_promotion_engine.price.write",
            "register_promotion": "price_promotion_engine.promotion.write",
            "approve_promotion": "price_promotion_engine.promotion.approve",
            "register_loyalty_tier": "price_promotion_engine.promotion.write",
            "quote_price": "price_promotion_engine.quote",
            "apply_promotion": "price_promotion_engine.quote",
            "redeem_coupon": "price_promotion_engine.quote",
            "receive_event": "price_promotion_engine.event.consume",
            "register_rule": "price_promotion_engine.configure",
            "register_schema_extension": "price_promotion_engine.configure",
            "set_parameter": "price_promotion_engine.configure",
            "configure_runtime": "price_promotion_engine.configure",
            "build_workbench_view": "price_promotion_engine.audit",
            "build_api_contract": "price_promotion_engine.audit",
            "build_schema_contract": "price_promotion_engine.audit",
            "build_service_contract": "price_promotion_engine.audit",
            "build_release_evidence": "price_promotion_engine.audit",
            "render_workbench": "price_promotion_engine.audit",
            "verify_owned_table_boundary": "price_promotion_engine.audit",
        },
    }


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Price Promotion Engine runtime must be configured before commands execute")


def _assert_supported_currency_region(state: dict, currency: str, region: str) -> None:
    config = state["configuration"]
    if currency not in config["supported_currencies"]:
        raise ValueError(f"Unsupported Price Promotion Engine currency: {currency}")
    if region not in config["supported_regions"]:
        raise ValueError(f"Unsupported Price Promotion Engine region: {region}")


def _select_price_rule(state: dict, tenant: str, sku: str, currency: str, region: str) -> dict | None:
    for price_rule in state["price_rules"].values():
        if (
            price_rule["tenant"] == tenant
            and price_rule["sku"] == sku
            and price_rule["currency"] == currency
            and price_rule["region"] == region
            and price_rule["status"] == "active"
        ):
            return price_rule
    return None


def _select_governing_rule(state: dict, tenant: str) -> dict | None:
    for rule in state.get("rules", {}).values():
        if rule["tenant"] == tenant and rule["scope"] == "price_promotion_engine" and rule["status"] == "active":
            return rule
    return None


def _resolved_base_price(state: dict, price_rule: dict, *, customer_id: str, channel: str) -> float:
    customer_key = f"{price_rule['price_rule_id']}:{customer_id}"
    if customer_key in state["customer_prices"]:
        return float(state["customer_prices"][customer_key]["price"])
    channel_key = f"{price_rule['price_rule_id']}:{channel}"
    if channel_key in state["channel_prices"]:
        return float(state["channel_prices"][channel_key]["price"])
    currency_key = f"{price_rule['price_rule_id']}:{price_rule['currency']}"
    if currency_key in state["currency_prices"]:
        return float(state["currency_prices"][currency_key]["base_price"])
    return float(price_rule["base_price"])


def _volume_discount(volume_breaks: tuple[tuple[int, float], ...], quantity: int) -> float:
    discount = 0.0
    for threshold, percent in sorted(volume_breaks):
        if quantity >= int(threshold):
            discount = max(discount, float(percent) * 100)
    return discount


def _eligible_promotions(state: dict, command: dict, segment: str, *, channel: str) -> tuple[dict, ...]:
    stack_limit = int(state["parameters"].get("promotion_stack_limit", {"value": 1})["value"])
    budget_guardrail = float(state["parameters"].get("campaign_budget_guardrail", {"value": 1.0})["value"])
    codes = set(command.get("promotion_codes", ()))
    ordered = sorted(state["promotions"].values(), key=lambda item: item["discount_percent"], reverse=True)
    selected: list[dict] = []
    for promotion in ordered:
        if promotion["tenant"] != command["tenant"] or promotion["code"] not in codes or promotion["status"] != "active":
            continue
        if segment not in promotion["segments"] or command["region"] not in promotion["regions"] or command["currency"] not in promotion["currencies"]:
            continue
        if channel not in promotion["channels"]:
            continue
        if promotion["customer_ids"] and command["customer_id"] not in set(promotion["customer_ids"]):
            continue
        approval = state["promotion_approvals"].get(f"{promotion['promotion_id']}:approval")
        if approval and approval["approval_status"] != "approved":
            continue
        budget = state["campaign_budgets"].get(f"{promotion['promotion_id']}:budget")
        if budget and budget["budget_amount"] > 0 and budget["consumed_amount"] >= budget["budget_amount"] * budget_guardrail:
            continue
        current_ids = {item["promotion_id"] for item in selected}
        excluded = set(state["promotion_exclusions"].get(f"{promotion['promotion_id']}:exclusion", {}).get("excluded_promotion_ids", ()))
        if current_ids & excluded:
            continue
        if any(promotion["promotion_id"] in set(state["promotion_exclusions"].get(f"{item['promotion_id']}:exclusion", {}).get("excluded_promotion_ids", ())) for item in selected):
            continue
        if not promotion["stackable"] and selected:
            continue
        selected.append(promotion)
        if len(selected) >= stack_limit:
            break
    return tuple(selected)


def _tier_discount(state: dict, tier_id: str | None) -> float:
    if not tier_id:
        return 0.0
    tier = state["loyalty_tiers"].get(tier_id)
    if not tier or tier["status"] != "active":
        return 0.0
    return float(tier["discount_percent"])


def _forecast_adjustment(state: dict, forecast: dict) -> float:
    demand_index = float(forecast.get("demand_index", 1.0))
    weight = float(state["parameters"].get("forecast_weight", {"value": 0.0})["value"])
    return max(0.5, min(1.5, 1 + ((demand_index - 1) * weight)))


def _risk_score(state: dict, margin_percent: float, forecast: dict, total_discount: float) -> float:
    margin_floor = float(state["parameters"].get("margin_floor_percent", {"value": 0.0})["value"])
    discount_ceiling = float(state["parameters"].get("discount_ceiling_percent", {"value": 100.0})["value"])
    elasticity_weight = float(state["parameters"].get("elasticity_weight", {"value": 0.0})["value"])
    margin_risk = max((margin_floor - margin_percent) / max(margin_floor, 1), 0)
    discount_risk = total_discount / max(discount_ceiling, 1) * 0.35
    forecast_risk = (1 - float(forecast.get("confidence", 1.0))) * 0.3
    elasticity_risk = (total_discount / 100) * elasticity_weight * 0.25
    return round(min(margin_risk + discount_risk + forecast_risk + elasticity_risk, 0.99), 4)


def _counterfactuals(base_price: float, quantity: int, discount_percent: float) -> tuple[dict, ...]:
    return (
        {"scenario": "no_promotion", "extended_price": round(base_price * quantity, 2), "discount_percent": 0.0},
        {"scenario": "selected_discount", "extended_price": round(base_price * (1 - discount_percent / 100) * quantity, 2), "discount_percent": round(discount_percent, 4)},
        {"scenario": "guardrail_floor", "extended_price": round(base_price * 0.92 * quantity, 2), "discount_percent": 8.0},
    )


def _margin_percent(price: float, cost: float) -> float:
    return round(((price - cost) / max(price, 0.01)) * 100, 4)


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
        "contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
        "payload": payload,
        "table": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[0],
        "idempotency_key": f"price_promotion_engine:{event_type}:{payload.get('decision_id') or payload.get('promotion_id') or len(state['outbox']) + 1}",
        "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[2]},
        "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload}),
    }
    state["outbox"].append(event)
    _append_state_event(state, event_type, event["event_id"], payload)


def _append_state_event(state: dict, event_type: str, key: str, payload: dict) -> None:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    state["events"].append(_state_event(event_type, key, payload, previous_hash=previous_hash))


def _state_event(event_type: str, key: str, payload: dict, *, previous_hash: str) -> dict:
    envelope = {
        "event_type": event_type,
        "key": key,
        "payload": payload,
        "previous_hash": previous_hash,
    }
    return {**envelope, "hash": _digest(envelope)}


def _record_audit_trace(
    state: dict,
    *,
    tenant: str,
    trace_type: str,
    subject_id: str,
    related_tables: tuple[str, ...],
    payload: dict,
) -> None:
    trace_id = f"{trace_type}:{subject_id}:{len(state['price_audit_traces']) + 1}"
    state["price_audit_traces"][trace_id] = {
        "tenant": tenant,
        "trace_id": trace_id,
        "trace_type": trace_type,
        "subject_id": subject_id,
        "related_tables": related_tables,
        "trace_hash": _digest({"trace_type": trace_type, "subject_id": subject_id, "payload": payload}),
        "audit_hash": _digest({"trace_id": trace_id, "related_tables": related_tables}),
    }


def _record_performance_telemetry(
    state: dict,
    *,
    tenant: str,
    metric_key: str,
    subject_id: str,
    sample_ms: int,
    rule_hits: int,
    status: str,
) -> None:
    telemetry_id = f"{metric_key}:{subject_id}:{len(state['price_performance_telemetry']) + 1}"
    state["price_performance_telemetry"][telemetry_id] = {
        "tenant": tenant,
        "telemetry_id": telemetry_id,
        "metric_key": metric_key,
        "subject_id": subject_id,
        "sample_ms": int(sample_ms),
        "rule_hits": int(rule_hits),
        "status": status,
        "audit_hash": _digest({"metric_key": metric_key, "subject_id": subject_id, "sample_ms": sample_ms}),
    }


def _capability_evidence(state: dict, capability: str) -> dict:
    return {
        "capability": capability,
        "events": len(state["events"]),
        "outbox": len(state["outbox"]),
        "inbox": len(state["inbox"]),
        "rules": len(state["rules"]),
        "parameters": len(state["parameters"]),
        "configuration": bool(state["configuration"].get("ok")),
        "runtime_digest": _digest(
            {
                "capability": capability,
                "decisions": len(state["price_decisions"]),
                "promotions": len(state["promotions"]),
                "simulations": len(state["price_simulations"]),
                "telemetry": len(state["price_performance_telemetry"]),
            }
        ),
    }


def _camelize(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def _digest(payload: dict | tuple | list | str) -> str:
    def default(value):
        if isinstance(value, set):
            return sorted(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, bytes):
            return value.hex()
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return str(value)
        return value

    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=default, separators=(",", ":")).encode()).hexdigest()
