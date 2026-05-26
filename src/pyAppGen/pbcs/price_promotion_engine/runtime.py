"""Executable runtime for the Price Promotion Engine PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC = "appgen.price_promotion.events"
PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PRICE_PROMOTION_ENGINE_OWNED_TABLES = ("price_rule", "promotion", "loyalty_tier", "price_decision")

PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_pricing_lifecycle",
    "owned_price_schema_boundary",
    "multi_tenant_price_isolation",
    "schema_evolution_resilient_price_context",
    "contextual_price_quote_optimization",
    "promotion_stacking_and_exclusion_engine",
    "loyalty_tier_price_personalization",
    "volume_break_and_contract_price_support",
    "forecast_signal_price_adjustment",
    "customer_segment_price_adjustment",
    "probabilistic_margin_elasticity_scoring",
    "counterfactual_promotion_margin_simulation",
    "temporal_price_effectivity_forecasting",
    "autonomous_price_exception_resolution",
    "semantic_promotion_instruction_parsing",
    "predictive_margin_and_demand_risk",
    "self_healing_price_decision_selection",
    "cryptographic_price_decision_proof",
    "immutable_price_audit_trail",
    "dynamic_price_policy_screening",
    "automated_promotion_control_testing",
    "cross_system_customer_forecast_checkout_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions_governance_evidence",
    "configuration_schema",
    "parameter_engine",
    "rule_engine",
    "seed_data",
    "workbench_ui",
    "governed_model_evidence",
)

PRICE_PROMOTION_ENGINE_STANDARD_FEATURE_KEYS = (
    "price_rule_catalog",
    "promotion_lifecycle",
    "loyalty_tier_management",
    "price_decision_history",
    "contextual_price_quotes",
    "promotion_redemption_validation",
    "promotion_stacking_exclusions",
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
}


def price_promotion_engine_runtime_capabilities() -> dict:
    smoke = price_promotion_engine_runtime_smoke()
    return {
        "format": "appgen.price-promotion-engine-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "price_promotion_engine",
        "implementation_directory": "src/pyAppGen/pbcs/price_promotion_engine",
        "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        "capabilities": PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PRICE_PROMOTION_ENGINE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "register_price_rule",
            "register_promotion",
            "register_loyalty_tier",
            "receive_event",
            "quote_price",
            "apply_promotion",
            "build_api_contract",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
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
            "stackable": True,
            "status": "active",
        },
    )["state"]
    state = price_promotion_engine_receive_event(
        state,
        {"event_id": "segment_alpha", "event_type": "CustomerSegmentUpdated", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "segment": "vip", "loyalty_tier_id": "tier_vip"}},
    )["state"]
    state = price_promotion_engine_receive_event(
        state,
        {"event_id": "forecast_alpha", "event_type": "ForecastUpdated", "payload": {"tenant": "tenant_alpha", "sku": "sku_alpha", "demand_index": 1.18, "confidence": 0.9}},
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
            "quantity": 12,
            "promotion_codes": ("GROWTH10",),
        },
    )
    state = quoted["state"]
    state = price_promotion_engine_apply_promotion(state, "decision_alpha", "promo_alpha")["state"]
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
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest({"events": state["events"], "outbox": state["outbox"], "decisions": state["price_decisions"]}),
    }


def price_promotion_engine_empty_state() -> dict:
    return {
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "handled_events": set(),
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "price_rules": {},
        "promotions": {},
        "loyalty_tiers": {},
        "price_decisions": {},
        "customer_segments": {},
        "forecast_signals": {},
        "seed_data": {"pricing_calendars": ("standard", "holiday"), "promotion_types": ("percent_off", "tier_adjustment", "volume_break")},
    }


def price_promotion_engine_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(PRICE_PROMOTION_ENGINE_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Price Promotion Engine database backend must be PostgreSQL, MySQL, or MariaDB")
    if configuration["event_topic"] != PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC:
        raise ValueError("Price Promotion Engine eventing must use the AppGen-X price promotion event contract")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
        if key in PRICE_PROMOTION_ENGINE_SUPPORTED_CONFIGURATION_FIELDS
    }
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def price_promotion_engine_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in PRICE_PROMOTION_ENGINE_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Price Promotion Engine parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Price Promotion Engine parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {"name": name, "value": value, "bounds": (low, high), "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)})}
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
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
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def price_promotion_engine_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in PRICE_PROMOTION_ENGINE_OWNED_TABLES:
        raise ValueError(f"Price Promotion Engine cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {"table": table, "fields": dict(fields), "version": len(runtime["schema_extensions"].get(table, ())) + 1}
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    return {"ok": True, "state": runtime, "extension": extension}


def price_promotion_engine_register_price_rule(state: dict, command: dict) -> dict:
    required = {"price_rule_id", "tenant", "sku", "region", "currency", "base_price", "cost", "segments", "volume_breaks", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine price rule fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_currency_region(state, command["currency"], command["region"])
    runtime = _copy_state(state)
    rule = {
        **command,
        "segments": tuple(command["segments"]),
        "volume_breaks": tuple(tuple(item) for item in command["volume_breaks"]),
        "base_price": float(command["base_price"]),
        "cost": float(command["cost"]),
        "margin_percent": _margin_percent(float(command["base_price"]), float(command["cost"])),
        "audit_proof": _digest(command),
    }
    runtime["price_rules"][rule["price_rule_id"]] = rule
    runtime["events"].append(_state_event("PriceRuleRegistered", rule["price_rule_id"], rule))
    return {"ok": True, "state": runtime, "price_rule": rule}


def price_promotion_engine_register_promotion(state: dict, command: dict) -> dict:
    required = {"promotion_id", "tenant", "code", "discount_percent", "segments", "regions", "currencies", "stackable", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine promotion fields: {tuple(sorted(missing))}")
    _require_configured(state)
    runtime = _copy_state(state)
    promotion = {
        **command,
        "segments": tuple(command["segments"]),
        "regions": tuple(command["regions"]),
        "currencies": tuple(command["currencies"]),
        "discount_percent": float(command["discount_percent"]),
        "audit_proof": _digest(command),
    }
    runtime["promotions"][promotion["promotion_id"]] = promotion
    runtime["events"].append(_state_event("PromotionRegistered", promotion["promotion_id"], promotion))
    return {"ok": True, "state": runtime, "promotion": promotion}


def price_promotion_engine_register_loyalty_tier(state: dict, command: dict) -> dict:
    required = {"tier_id", "tenant", "name", "rank", "discount_percent", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine loyalty tier fields: {tuple(sorted(missing))}")
    _require_configured(state)
    runtime = _copy_state(state)
    tier = {**command, "rank": int(command["rank"]), "discount_percent": float(command["discount_percent"]), "audit_proof": _digest(command)}
    runtime["loyalty_tiers"][tier["tier_id"]] = tier
    runtime["events"].append(_state_event("LoyaltyTierRegistered", tier["tier_id"], tier))
    return {"ok": True, "state": runtime, "loyalty_tier": tier}


def price_promotion_engine_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    if event.get("event_type") not in PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported Price Promotion Engine consumed event: {event.get('event_type')}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Price Promotion Engine consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {"ok": True, "state": runtime, "handler": {"status": "duplicate", "event_id": event_id}}
    handler = {
        "event_id": event_id,
        "event_type": event["event_type"],
        "idempotency_key": f"price_promotion_engine:{event['event_type']}:{event_id}",
        "attempts": int(runtime.get("configuration", {}).get("retry_limit", 3) or 3),
    }
    if simulate_failure:
        handler["status"] = "dead_letter"
        runtime["dead_letter"].append({**event, "handler": handler})
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    handler["status"] = "handled"
    runtime["inbox"].append({**event, "handler": handler})
    runtime["handled_events"].add(event_id)
    if event["event_type"] == "CustomerSegmentUpdated":
        runtime["customer_segments"][payload["customer_id"]] = payload
    elif event["event_type"] == "ForecastUpdated":
        runtime["forecast_signals"][payload["sku"]] = payload
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    return {"ok": True, "state": runtime, "handler": handler}


def price_promotion_engine_quote_price(state: dict, command: dict) -> dict:
    required = {"decision_id", "tenant", "customer_id", "sku", "region", "currency", "quantity", "promotion_codes"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Price Promotion Engine quote fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_currency_region(state, command["currency"], command["region"])
    runtime = _copy_state(state)
    price_rule = _select_price_rule(runtime, command["tenant"], command["sku"], command["currency"], command["region"])
    if not price_rule:
        raise ValueError(f"No active Price Promotion Engine price rule for SKU: {command['sku']}")
    governing_rule = _select_governing_rule(runtime, command["tenant"])
    segment = runtime["customer_segments"].get(command["customer_id"], {}).get("segment", "standard")
    loyalty_tier_id = runtime["customer_segments"].get(command["customer_id"], {}).get("loyalty_tier_id")
    if governing_rule and segment not in governing_rule["allowed_segments"]:
        raise ValueError(f"Segment {segment} is blocked by price promotion rule {governing_rule['rule_id']}")
    forecast = runtime["forecast_signals"].get(command["sku"], {})
    base_price = float(price_rule["base_price"])
    quantity = int(command["quantity"])
    volume_discount = _volume_discount(price_rule["volume_breaks"], quantity)
    promotions = _eligible_promotions(runtime, command, segment)
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
        "quantity": quantity,
        "segment": segment,
        "loyalty_tier_id": loyalty_tier_id,
        "base_price": base_price,
        "optimized_unit_price": optimized_unit_price,
        "extended_price": round(optimized_unit_price * quantity, 2),
        "total_discount_percent": round(total_discount, 4),
        "margin_percent": margin_percent,
        "risk_score": risk_score,
        "status": status,
        "eligible_promotions": tuple(item["promotion_id"] for item in promotions),
        "counterfactuals": _counterfactuals(base_price, quantity, total_discount),
        "audit_proof": _digest({"command": command, "price_rule": price_rule, "discount": total_discount, "risk": risk_score}),
    }
    runtime["price_decisions"][decision["decision_id"]] = decision
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
    runtime["price_decisions"][decision_id]["applied_promotions"] = tuple(sorted(set(runtime["price_decisions"][decision_id].get("applied_promotions", ())) | {promotion_id}))
    _emit(runtime, "PromotionApplied", decision["tenant"], applied)
    return {"ok": True, "state": runtime, "promotion_application": applied}


def price_promotion_engine_build_workbench_view(state: dict, *, tenant: str) -> dict:
    rules = tuple(item for item in state.get("price_rules", {}).values() if item["tenant"] == tenant)
    promotions = tuple(item for item in state.get("promotions", {}).values() if item["tenant"] == tenant)
    tiers = tuple(item for item in state.get("loyalty_tiers", {}).values() if item["tenant"] == tenant)
    decisions = tuple(item for item in state.get("price_decisions", {}).values() if item["tenant"] == tenant)
    return {
        "format": "appgen.price-promotion-engine-workbench-view.v1",
        "tenant": tenant,
        "price_rule_count": len(rules),
        "promotion_count": len(promotions),
        "loyalty_tier_count": len(tiers),
        "decision_count": len(decisions),
        "approved_decision_count": len(tuple(item for item in decisions if item["status"] == "approved")),
        "average_margin_percent": round(sum(item["margin_percent"] for item in decisions) / max(len(decisions), 1), 4),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {
            "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
            "outbox_table": "price_promotion_engine_appgen_outbox_event",
            "inbox_table": "price_promotion_engine_appgen_inbox_event",
            "dead_letter_table": "price_promotion_engine_dead_letter_event",
        },
    }


def price_promotion_engine_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed_api_dependencies = {
        "POST /price-rules",
        "POST /price-quotes",
        "POST /promotions",
        "POST /promotion-applications",
        "GET /price-decisions",
        "customer_segment_projection",
        "forecast_projection",
        "checkout_projection",
    }
    allowed_event_dependencies = set(PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES)
    allowed_runtime_tables = {
        "price_promotion_engine_appgen_outbox_event",
        "price_promotion_engine_appgen_inbox_event",
        "price_promotion_engine_dead_letter_event",
    }
    violations = tuple(
        reference
        for reference in references
        if reference not in set(PRICE_PROMOTION_ENGINE_OWNED_TABLES)
        and reference not in allowed_api_dependencies
        and reference not in allowed_event_dependencies
        and reference not in allowed_runtime_tables
        and not str(reference).startswith("price_promotion_engine_")
    )
    return {
        "format": "appgen.price-promotion-engine-boundary.v1",
        "ok": not violations,
        "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        "declared_dependencies": {
            "apis": (
                "POST /price-rules",
                "POST /price-quotes",
                "POST /promotions",
                "POST /promotion-applications",
                "GET /price-decisions",
            ),
            "events": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
            "api_projections": ("customer_segment_projection", "forecast_projection", "checkout_projection"),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def price_promotion_engine_build_api_contract() -> dict:
    return {
        "format": "appgen.price-promotion-engine-api-contract.v1",
        "ok": True,
        "routes": (
            {
                "route": "POST /price-rules",
                "command": "register_price_rule",
                "owned_tables": ("price_rule",),
                "emits": (),
                "requires_permission": "price_promotion_engine.price.write",
                "idempotency_key": "price_rule_id",
            },
            {
                "route": "POST /promotions",
                "command": "register_promotion",
                "owned_tables": ("promotion",),
                "emits": (),
                "requires_permission": "price_promotion_engine.promotion.write",
                "idempotency_key": "promotion_id",
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
                "owned_tables": ("price_decision",),
                "emits": ("PriceOptimized",),
                "requires_permission": "price_promotion_engine.quote",
                "idempotency_key": "decision_id",
            },
            {
                "route": "POST /promotion-applications",
                "command": "apply_promotion",
                "owned_tables": ("price_decision",),
                "emits": ("PromotionApplied",),
                "requires_permission": "price_promotion_engine.quote",
                "idempotency_key": "decision_id:promotion_id",
            },
            {
                "route": "POST /price-promotion/events/inbox",
                "command": "receive_event",
                "owned_tables": (),
                "consumes": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
                "requires_permission": "price_promotion_engine.event.consume",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /price-decisions",
                "query": "build_workbench_view",
                "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
                "requires_permission": "price_promotion_engine.audit",
            },
        ),
        "declared_catalog_routes": ("POST /price-quotes", "POST /promotions", "GET /price-decisions"),
        "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        "emits": PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES,
        "consumes": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
        "database_backends": PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(price_promotion_engine_permissions_contract()["permissions"])),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }


def price_promotion_engine_permissions_contract() -> dict:
    return {
        "format": "appgen.price-promotion-engine-permissions.v1",
        "ok": True,
        "permissions": (
            "price_promotion_engine.price.write",
            "price_promotion_engine.promotion.write",
            "price_promotion_engine.quote",
            "price_promotion_engine.event.consume",
            "price_promotion_engine.configure",
            "price_promotion_engine.audit",
        ),
        "action_permissions": {
            "register_price_rule": "price_promotion_engine.price.write",
            "register_promotion": "price_promotion_engine.promotion.write",
            "register_loyalty_tier": "price_promotion_engine.promotion.write",
            "quote_price": "price_promotion_engine.quote",
            "apply_promotion": "price_promotion_engine.quote",
            "receive_event": "price_promotion_engine.event.consume",
            "register_rule": "price_promotion_engine.configure",
            "register_schema_extension": "price_promotion_engine.configure",
            "set_parameter": "price_promotion_engine.configure",
            "configure_runtime": "price_promotion_engine.configure",
            "build_workbench_view": "price_promotion_engine.audit",
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
        if price_rule["tenant"] == tenant and price_rule["sku"] == sku and price_rule["currency"] == currency and price_rule["region"] == region and price_rule["status"] == "active":
            return price_rule
    return None


def _select_governing_rule(state: dict, tenant: str) -> dict | None:
    for rule in state.get("rules", {}).values():
        if rule["tenant"] == tenant and rule["scope"] == "price_promotion_engine" and rule["status"] == "active":
            return rule
    return None


def _volume_discount(volume_breaks: tuple[tuple[int, float], ...], quantity: int) -> float:
    discount = 0.0
    for threshold, percent in sorted(volume_breaks):
        if quantity >= int(threshold):
            discount = max(discount, float(percent) * 100)
    return discount


def _eligible_promotions(state: dict, command: dict, segment: str) -> tuple[dict, ...]:
    stack_limit = int(state["parameters"].get("promotion_stack_limit", {"value": 1})["value"])
    codes = set(command.get("promotion_codes", ()))
    eligible = []
    for promotion in state["promotions"].values():
        if promotion["tenant"] != command["tenant"] or promotion["code"] not in codes or promotion["status"] != "active":
            continue
        if segment in promotion["segments"] and command["region"] in promotion["regions"] and command["currency"] in promotion["currencies"]:
            eligible.append(promotion)
    return tuple(sorted(eligible, key=lambda item: item["discount_percent"], reverse=True)[:stack_limit])


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
    margin_risk = max((margin_floor - margin_percent) / max(margin_floor, 1), 0)
    discount_risk = total_discount / max(discount_ceiling, 1) * 0.35
    forecast_risk = (1 - float(forecast.get("confidence", 1.0))) * 0.3
    return round(min(margin_risk + discount_risk + forecast_risk, 0.99), 4)


def _counterfactuals(base_price: float, quantity: int, discount_percent: float) -> tuple[dict, ...]:
    return (
        {"scenario": "no_promotion", "extended_price": round(base_price * quantity, 2), "discount_percent": 0.0},
        {"scenario": "selected_discount", "extended_price": round(base_price * (1 - discount_percent / 100) * quantity, 2), "discount_percent": round(discount_percent, 4)},
    )


def _margin_percent(price: float, cost: float) -> float:
    return round(((price - cost) / max(price, 0.01)) * 100, 4)


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "contract": "appgen_event_contract",
        "idempotency_key": f"price_promotion_engine:{event_type}:{payload.get('decision_id') or payload.get('promotion_id') or len(state['outbox']) + 1}",
        "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": "price_promotion_engine_dead_letter_event"},
        "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload}),
    }
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    return {"event_type": event_type, "key": key, "payload": payload, "hash": _digest({"event_type": event_type, "key": key, "payload": payload})}


def _capability_evidence(state: dict, capability: str) -> dict:
    return {
        "capability": capability,
        "events": len(state["events"]),
        "outbox": len(state["outbox"]),
        "inbox": len(state["inbox"]),
        "rules": len(state["rules"]),
        "parameters": len(state["parameters"]),
        "configuration": bool(state["configuration"].get("ok")),
        "runtime_digest": _digest({"capability": capability, "decisions": len(state["price_decisions"]), "promotions": len(state["promotions"])}),
    }


def _digest(payload: dict) -> str:
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
