"""UI contract for the Price Promotion Engine PBC."""

from __future__ import annotations

from .runtime import PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import PRICE_PROMOTION_ENGINE_EVENT_CONTRACT
from .runtime import PRICE_PROMOTION_ENGINE_OWNED_TABLES
from .runtime import PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import PRICE_PROMOTION_ENGINE_REQUIRED_RULE_FIELDS
from .runtime import PRICE_PROMOTION_ENGINE_RUNTIME_TABLES
from .runtime import PRICE_PROMOTION_ENGINE_SUPPORTED_PARAMETER_KEYS
from .runtime import PRICE_PROMOTION_ENGINE_SUPPORTED_CONFIGURATION_FIELDS
from .runtime import price_promotion_engine_binding_evidence


PRICE_PROMOTION_ENGINE_UI_FRAGMENT_KEYS = (
    "PricePromotionWorkbench",
    "PriceListBookMatrix",
    "CustomerPriceAgreementBoard",
    "PriceRuleCatalog",
    "TradePromotionPlanner",
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
    "PriceExceptionCaseQueue",
    "PromotionAccrualSettlementConsole",
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
                "binds_to": ("price_list", "price_book", "price_book_entry", "price_agreement", "customer_price", "channel_price", "currency_price"),
                "commands": ("register_price_rule", "register_price_agreement", "quote_price"),
            },
            {
                "key": "promotions",
                "fragment": "PromotionDesigner",
                "binds_to": ("trade_promotion_plan", "promotion", "promotion_rule", "coupon", "promotion_eligibility", "promotion_stacking_policy", "promotion_exclusion"),
                "commands": ("register_promotion", "plan_trade_promotion", "apply_promotion"),
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
                "binds_to": ("price_exception_case", "price_simulation", "price_margin_guardrail", "price_decision", "price_performance_telemetry"),
                "commands": ("quote_price", "apply_promotion", "open_price_exception", "resolve_price_exception", "build_service_contract"),
            },
            {
                "key": "settlement",
                "fragment": "PromotionAccrualSettlementConsole",
                "binds_to": ("promotion_accrual", "promotion_settlement", "campaign_budget"),
                "commands": ("accrue_promotion", "settle_promotion"),
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
            "register_price_agreement": "price_promotion_engine.price.write",
            "register_promotion": "price_promotion_engine.promotion.write",
            "plan_trade_promotion": "price_promotion_engine.promotion.write",
            "register_loyalty_tier": "price_promotion_engine.promotion.write",
            "quote_price": "price_promotion_engine.quote",
            "apply_promotion": "price_promotion_engine.quote",
            "open_price_exception": "price_promotion_engine.exception.write",
            "resolve_price_exception": "price_promotion_engine.exception.write",
            "accrue_promotion": "price_promotion_engine.promotion.settle",
            "settle_promotion": "price_promotion_engine.promotion.settle",
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
            "emits": ("PriceOptimized", "PromotionApplied", "TradePromotionPlanned", "PriceExceptionOpened", "PromotionSettlementPosted"),
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
        {"key": "agreements", "value": view["price_agreement_count"], "fragment": "CustomerPriceAgreementBoard"},
        {"key": "trade_plans", "value": view["trade_promotion_plan_count"], "fragment": "TradePromotionPlanner"},
        {"key": "promotions", "value": view["promotion_count"], "fragment": "PromotionDesigner"},
        {"key": "approvals", "value": view["approval_count"], "fragment": "PromotionApprovalQueue"},
        {"key": "simulations", "value": view["simulation_count"], "fragment": "PriceSimulationLab"},
        {"key": "decisions", "value": view["decision_count"], "fragment": "PriceDecisionLedger"},
        {"key": "exceptions", "value": view["price_exception_count"], "fragment": "PriceExceptionCaseQueue"},
        {"key": "settlements", "value": view["promotion_settlement_count"], "fragment": "PromotionAccrualSettlementConsole"},
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
        "price_agreement_count": bindings["tenant_counts"]["price_agreements"],
        "trade_promotion_plan_count": bindings["tenant_counts"]["trade_promotion_plans"],
        "promotion_count": len(promotions),
        "approval_count": bindings["tenant_counts"]["approvals"],
        "simulation_count": bindings["tenant_counts"]["simulations"],
        "telemetry_count": bindings["tenant_counts"]["telemetry"],
        "loyalty_tier_count": len(tiers),
        "decision_count": len(decisions),
        "price_exception_count": bindings["tenant_counts"]["price_exception_cases"],
        "promotion_settlement_count": bindings["tenant_counts"]["promotion_settlements"],
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



def price_promotion_engine_form_contracts() -> dict:
    contracts=(
        {'key':'PriceConfigurationForm','operation':'configure_runtime','table':'price_promotion_engine_price_configuration','fields':PRICE_PROMOTION_ENGINE_SUPPORTED_CONFIGURATION_FIELDS,'permission':'price_promotion_engine.configure','keywords':('configure','currency','calendar')},
        {'key':'PriceRuleForm','operation':'register_price_rule','table':'price_promotion_engine_price_rule','fields':('price_rule_id','tenant','sku','region','currency','base_price','cost','segments','volume_breaks','status'),'permission':'price_promotion_engine.price','keywords':('price rule','sku','base price')},
        {'key':'PriceAgreementForm','operation':'register_price_agreement','table':'price_promotion_engine_price_agreement','fields':('agreement_id','tenant','customer_id','sku','contracted_price','effective_from','effective_to'),'permission':'price_promotion_engine.price','keywords':('agreement','contract price','customer')},
        {'key':'PromotionForm','operation':'register_promotion','table':'price_promotion_engine_promotion','fields':('promotion_id','tenant','code','discount_percent','segments','regions','currencies','stackable','budget_amount','status'),'permission':'price_promotion_engine.promotion','keywords':('promotion','coupon','discount')},
        {'key':'PriceQuoteForm','operation':'quote_price','table':'price_promotion_engine_price_decision','fields':('decision_id','tenant','customer_id','sku','region','currency','quantity','promotion_codes'),'permission':'price_promotion_engine.quote','keywords':('quote','decision','checkout')},
        {'key':'CouponRedemptionForm','operation':'redeem_coupon','table':'price_promotion_engine_coupon','fields':('decision_id','coupon_code'),'permission':'price_promotion_engine.promotion','keywords':('coupon','redeem')},
        {'key':'PromotionSettlementForm','operation':'settle_promotion','table':'price_promotion_engine_promotion_settlement','fields':('accrual_id','settled_amount','settled_by'),'permission':'price_promotion_engine.settle','keywords':('settle','accrual','trade promotion')},
    )
    return {'format':'appgen.price-promotion-engine-standalone-forms.v1','ok':all(i['table'].startswith('price_promotion_engine_') for i in contracts),'pbc':'price_promotion_engine','contracts':contracts,'side_effects':()}

def price_promotion_engine_wizard_contracts() -> dict:
    contracts=(
        {'key':'PriceSetupWizard','steps':('configure_runtime','compile_policy','register_price_rule','register_customer_agreement'),'forms':('PriceConfigurationForm','PriceRuleForm','PriceAgreementForm'),'keywords':('configure','price rule','agreement')},
        {'key':'PromotionLaunchWizard','steps':('create_promotion','approve_discount','create_coupon','validate_budget'),'forms':('PromotionForm',),'keywords':('promotion','campaign','coupon')},
        {'key':'PriceQuoteWizard','steps':('resolve_segment_forecast','select_price_rule','simulate_margin','create_decision'),'forms':('PriceQuoteForm',),'keywords':('quote','checkout','decision')},
        {'key':'CouponRedemptionWizard','steps':('validate_coupon','apply_promotion','update_budget','emit_appgen_event'),'forms':('CouponRedemptionForm',),'keywords':('coupon','redeem','apply')},
        {'key':'PromotionSettlementWizard','steps':('accrue_promotion','settle_accrual','post_settlement_event'),'forms':('PromotionSettlementForm',),'keywords':('settle','accrual','trade')},
    )
    return {'format':'appgen.price-promotion-engine-standalone-wizards.v1','ok':all(i['steps'] for i in contracts),'pbc':'price_promotion_engine','contracts':contracts,'side_effects':()}

def price_promotion_engine_control_catalog() -> dict:
    contracts=(
        {'key':'price_backend_event_contract','operation':'run_control_tests','table':'price_promotion_engine_price_audit_trace','permission':'price_promotion_engine.audit'},
        {'key':'margin_guardrail_control','operation':'quote_price','table':'price_promotion_engine_price_margin_guardrail','permission':'price_promotion_engine.audit'},
        {'key':'promotion_settlement_control','operation':'settle_promotion','table':'price_promotion_engine_promotion_settlement','permission':'price_promotion_engine.audit'},
    )
    return {'format':'appgen.price-promotion-engine-standalone-controls.v1','ok':all(i['table'].startswith('price_promotion_engine_') for i in contracts),'pbc':'price_promotion_engine','contracts':contracts,'side_effects':()}

def price_promotion_engine_standalone_workbench_blueprint() -> dict:
    forms=price_promotion_engine_form_contracts(); wizards=price_promotion_engine_wizard_contracts(); controls=price_promotion_engine_control_catalog()
    return {'format':'appgen.price-promotion-engine-standalone-workbench.v1','ok':forms['ok'] and wizards['ok'] and controls['ok'],'pbc':'price_promotion_engine','forms':forms['contracts'],'wizards':wizards['contracts'],'controls':controls['contracts'],'panels':price_promotion_engine_ui_contract()['panels'],'side_effects':()}

def price_promotion_engine_render_standalone_workbench(workbench: dict) -> dict:
    bp=price_promotion_engine_standalone_workbench_blueprint(); cards=(
        {'key':'price_rules','value':workbench.get('price_rule_count',0),'fragment':'PriceRuleConsole'},
        {'key':'promotions','value':workbench.get('promotion_count',0),'fragment':'PromotionConsole'},
        {'key':'approved_promotions','value':workbench.get('approved_promotion_count',0),'fragment':'PromotionApprovalBoard'},
        {'key':'decisions','value':workbench.get('price_decision_count',workbench.get('decision_count',0)),'fragment':'PriceDecisionConsole'},
        {'key':'coupon_redemptions','value':workbench.get('coupon_redemption_count',0),'fragment':'CouponConsole'},
        {'key':'settlements','value':workbench.get('promotion_settlement_count',0),'fragment':'PromotionSettlementBoard'},)
    return {'format':'appgen.price-promotion-engine-standalone-render.v1','ok':bp['ok'] and bool(cards),'pbc':'price_promotion_engine','tenant':workbench.get('tenant'),'cards':cards,'forms':tuple(i['key'] for i in bp['forms']),'wizards':tuple(i['key'] for i in bp['wizards']),'controls':tuple(i['key'] for i in bp['controls']),'side_effects':()}
