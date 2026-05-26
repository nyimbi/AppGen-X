"""UI contract for the Price Promotion Engine PBC."""

from __future__ import annotations

from .runtime import PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import PRICE_PROMOTION_ENGINE_OWNED_TABLES


PRICE_PROMOTION_ENGINE_UI_FRAGMENT_KEYS = (
    "PricePromotionWorkbench",
    "PriceRuleCatalog",
    "PromotionDesigner",
    "LoyaltyTierManager",
    "PriceQuoteConsole",
    "PromotionStackingBoard",
    "ForecastSignalPanel",
    "SegmentPricingPanel",
    "PriceDecisionLedger",
    "PriceRuleStudio",
    "PriceParameterConsole",
    "PriceConfigurationPanel",
    "PriceEventOutbox",
    "PriceDeadLetterQueue",
)


def price_promotion_engine_ui_contract() -> dict:
    return {
        "format": "appgen.price-promotion-engine-ui-contract.v1",
        "ok": True,
        "pbc": "price_promotion_engine",
        "implementation_directory": "src/pyAppGen/pbcs/price_promotion_engine",
        "fragments": PRICE_PROMOTION_ENGINE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/price_promotion_engine",
            "/workbench/pbcs/price_promotion_engine/rules",
            "/workbench/pbcs/price_promotion_engine/promotions",
            "/workbench/pbcs/price_promotion_engine/tiers",
            "/workbench/pbcs/price_promotion_engine/quotes",
            "/workbench/pbcs/price_promotion_engine/decisions",
            "/workbench/pbcs/price_promotion_engine/configuration",
        ),
        "panels": (
            {"key": "rules", "fragment": "PriceRuleCatalog", "binds_to": ("price_rule",), "commands": ("register_price_rule", "quote_price")},
            {"key": "promotions", "fragment": "PromotionDesigner", "binds_to": ("promotion", "price_decision"), "commands": ("register_promotion", "apply_promotion")},
            {"key": "tiers", "fragment": "LoyaltyTierManager", "binds_to": ("loyalty_tier",), "commands": ("register_loyalty_tier",)},
            {"key": "governance", "fragment": "PriceRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "action_permissions": {
            "register_price_rule": "price_promotion_engine.price.write",
            "register_promotion": "price_promotion_engine.promotion.write",
            "register_loyalty_tier": "price_promotion_engine.promotion.write",
            "quote_price": "price_promotion_engine.quote",
            "apply_promotion": "price_promotion_engine.quote",
            "receive_event": "price_promotion_engine.event.consume",
            "register_rule": "price_promotion_engine.configure",
            "set_parameter": "price_promotion_engine.configure",
            "configure_runtime": "price_promotion_engine.configure",
            "run_control_tests": "price_promotion_engine.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone", "decision_mode"),
            "allowed_database_backends": PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
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
            ),
        },
        "rule_editor": {
            "rule_types": ("pricing", "promotion", "margin", "segment", "forecast"),
            "required_fields": ("rule_id", "tenant", "scope", "status", "allowed_currencies", "allowed_regions", "allowed_segments", "promotion_policy", "margin_policy"),
        },
        "event_surfaces": {
            "emits": ("PriceOptimized", "PromotionApplied"),
            "consumes": ("CustomerSegmentUpdated", "ForecastUpdated"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def price_promotion_engine_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = price_promotion_engine_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, permission in action_permissions.items() if permission in permissions)
    view = _view_counts(state, tenant)
    cards = (
        {"key": "price_rules", "value": view["price_rule_count"], "fragment": "PriceRuleCatalog"},
        {"key": "promotions", "value": view["promotion_count"], "fragment": "PromotionDesigner"},
        {"key": "tiers", "value": view["loyalty_tier_count"], "fragment": "LoyaltyTierManager"},
        {"key": "decisions", "value": view["decision_count"], "fragment": "PriceDecisionLedger"},
        {"key": "outbox", "value": view["outbox_count"], "fragment": "PriceEventOutbox"},
        {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "PriceDeadLetterQueue"},
    )
    return {
        "format": "appgen.price-promotion-engine-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/price_promotion_engine",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    rules = tuple(item for item in state.get("price_rules", {}).values() if item["tenant"] == tenant)
    promotions = tuple(item for item in state.get("promotions", {}).values() if item["tenant"] == tenant)
    tiers = tuple(item for item in state.get("loyalty_tiers", {}).values() if item["tenant"] == tenant)
    decisions = tuple(item for item in state.get("price_decisions", {}).values() if item["tenant"] == tenant)
    return {
        "price_rule_count": len(rules),
        "promotion_count": len(promotions),
        "loyalty_tier_count": len(tiers),
        "decision_count": len(decisions),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        },
    }
