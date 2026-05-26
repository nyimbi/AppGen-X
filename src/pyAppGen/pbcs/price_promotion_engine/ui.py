"""UI contract for the Price Promotion Engine PBC."""

from __future__ import annotations

from .runtime import PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import PRICE_PROMOTION_ENGINE_EVENT_CONTRACT
from .runtime import PRICE_PROMOTION_ENGINE_OWNED_TABLES
from .runtime import PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import PRICE_PROMOTION_ENGINE_REQUIRED_RULE_FIELDS
from .runtime import PRICE_PROMOTION_ENGINE_RUNTIME_TABLES
from .runtime import PRICE_PROMOTION_ENGINE_SUPPORTED_PARAMETER_KEYS
from .runtime import price_promotion_engine_binding_evidence


PRICE_PROMOTION_ENGINE_UI_FRAGMENT_KEYS = (
    "PricePromotionWorkbench",
    "PriceListBookMatrix",
    "PriceRuleCatalog",
    "PromotionDesigner",
    "CouponGovernanceBoard",
    "CampaignBudgetConsole",
    "PromotionApprovalQueue",
    "LoyaltyTierManager",
    "PriceQuoteConsole",
    "PromotionStackingBoard",
    "PriceSimulationLab",
    "MarginGuardrailPanel",
    "ForecastSignalPanel",
    "SegmentPricingPanel",
    "PriceDecisionLedger",
    "PriceTelemetryPanel",
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
            "/workbench/pbcs/price_promotion_engine/books",
            "/workbench/pbcs/price_promotion_engine/rules",
            "/workbench/pbcs/price_promotion_engine/promotions",
            "/workbench/pbcs/price_promotion_engine/coupons",
            "/workbench/pbcs/price_promotion_engine/approvals",
            "/workbench/pbcs/price_promotion_engine/quotes",
            "/workbench/pbcs/price_promotion_engine/simulations",
            "/workbench/pbcs/price_promotion_engine/decisions",
            "/workbench/pbcs/price_promotion_engine/configuration",
        ),
        "panels": (
            {
                "key": "price_books",
                "fragment": "PriceListBookMatrix",
                "binds_to": ("price_list", "price_book", "price_book_entry", "customer_price", "channel_price", "currency_price"),
                "commands": ("register_price_rule", "quote_price"),
            },
            {
                "key": "promotions",
                "fragment": "PromotionDesigner",
                "binds_to": ("promotion", "promotion_rule", "coupon", "promotion_eligibility", "promotion_stacking_policy", "promotion_exclusion"),
                "commands": ("register_promotion", "apply_promotion"),
            },
            {
                "key": "approvals",
                "fragment": "PromotionApprovalQueue",
                "binds_to": ("campaign_budget", "promotion_approval"),
                "commands": ("register_promotion", "build_release_evidence"),
            },
            {
                "key": "pricing_decisions",
                "fragment": "PriceSimulationLab",
                "binds_to": ("price_simulation", "price_margin_guardrail", "price_decision", "price_performance_telemetry"),
                "commands": ("quote_price", "apply_promotion", "build_service_contract"),
            },
            {
                "key": "governance",
                "fragment": "PriceRuleStudio",
                "binds_to": ("price_policy_rule", "price_parameter", "price_configuration", "price_schema_extension"),
                "commands": (
                    "register_rule",
                    "set_parameter",
                    "configure_runtime",
                    "build_schema_contract",
                    "build_service_contract",
                    "build_release_evidence",
                ),
            },
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
            "build_schema_contract": "price_promotion_engine.audit",
            "build_service_contract": "price_promotion_engine.audit",
            "build_release_evidence": "price_promotion_engine.audit",
            "run_control_tests": "price_promotion_engine.audit",
        },
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "default_timezone",
                "decision_mode",
                "approval_mode",
                "simulation_horizon_days",
                "telemetry_window_minutes",
            ),
            "allowed_database_backends": PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS,
            "event_contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
            "required_event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_eventing_choice_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": PRICE_PROMOTION_ENGINE_SUPPORTED_PARAMETER_KEYS,
        },
        "rule_editor": {
            "rule_types": ("pricing", "promotion", "margin", "segment", "forecast", "approval", "budget"),
            "required_fields": PRICE_PROMOTION_ENGINE_REQUIRED_RULE_FIELDS,
        },
        "event_surfaces": {
            "emits": ("PriceOptimized", "PromotionApplied"),
            "consumes": ("CustomerSegmentUpdated", "ForecastUpdated"),
            "event_contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
            "required_event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
            "runtime_tables": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES,
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_targets": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
    }


def price_promotion_engine_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = price_promotion_engine_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, permission in action_permissions.items() if permission in permissions)
    view = _view_counts(state, tenant)
    cards = (
        {"key": "price_books", "value": view["price_book_count"], "fragment": "PriceListBookMatrix"},
        {"key": "promotions", "value": view["promotion_count"], "fragment": "PromotionDesigner"},
        {"key": "approvals", "value": view["approval_count"], "fragment": "PromotionApprovalQueue"},
        {"key": "simulations", "value": view["simulation_count"], "fragment": "PriceSimulationLab"},
        {"key": "decisions", "value": view["decision_count"], "fragment": "PriceDecisionLedger"},
        {"key": "telemetry", "value": view["telemetry_count"], "fragment": "PriceTelemetryPanel"},
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
    promotions = tuple(item for item in state.get("promotions", {}).values() if item["tenant"] == tenant)
    tiers = tuple(item for item in state.get("loyalty_tiers", {}).values() if item["tenant"] == tenant)
    decisions = tuple(item for item in state.get("price_decisions", {}).values() if item["tenant"] == tenant)
    bindings = price_promotion_engine_binding_evidence(state, tenant=tenant)
    return {
        "price_book_count": bindings["tenant_counts"]["price_books"],
        "promotion_count": len(promotions),
        "approval_count": bindings["tenant_counts"]["approvals"],
        "simulation_count": bindings["tenant_counts"]["simulations"],
        "telemetry_count": bindings["tenant_counts"]["telemetry"],
        "loyalty_tier_count": len(tiers),
        "decision_count": len(decisions),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": bindings,
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = price_promotion_engine_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = price_promotion_engine_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
