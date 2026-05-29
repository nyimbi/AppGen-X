"""Executable seed-data contract for the checkout_processing PBC."""

from __future__ import annotations


PBC_KEY = "checkout_processing"
SEED_DATA = (
    {
        "table": "checkout_processing_checkout_configuration",
        "rows": (
            {
                "configuration_id": "cfg_default",
                "database_backend": "postgresql",
                "event_topic": "appgen.checkout.events",
                "default_currency": "USD",
                "default_country": "US",
            },
        ),
    },
    {
        "table": "checkout_processing_checkout_parameter",
        "rows": (
            {"parameter_id": "param_risk_threshold", "name": "risk_threshold", "value": "0.65", "tenant_scope": "default"},
            {"parameter_id": "param_retry_limit", "name": "max_retry_attempts", "value": "3", "tenant_scope": "default"},
        ),
    },
    {
        "table": "checkout_processing_checkout_rule",
        "rows": (
            {
                "rule_id": "rule_checkout_default",
                "tenant": "tenant_alpha",
                "scope": "checkout_guard",
                "status": "active",
            },
        ),
    },
)


def seed_plan() -> dict:
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not any(key.endswith("_id") or key == "rule_id" for key in row)
    )
    plan = seed_plan()
    return {
        "ok": plan["ok"] and not invalid_tables and not invalid_rows,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise seed validation without writing rows."""
    return validate_seed_data()



def standalone_seed_bundle(*, tenant='tenant_demo'):
    return {
        'pbc': PBC_KEY, 'tenant': tenant,
        'configuration': {'database_backend':'postgresql','event_topic':'appgen.checkout.events','retry_limit':3,'default_currency':'USD','default_country':'US','supported_shipping_options':('standard','express','pickup'),'supported_payment_methods':('card','wallet'),'workbench_limit':100},
        'parameters': {'cart_ttl_minutes':60,'session_ttl_minutes':30,'risk_threshold':0.65,'max_retry_attempts':3,'promotion_cap_rate':0.15,'shipping_cost_weight':0.5,'carbon_cost_weight':0.1,'abandonment_horizon_hours':24,'route_switch_threshold':0.25,'workbench_limit':100},
        'rules': ({'rule_id':'checkout.demo.guard','tenant':tenant,'scope':'checkout_guard','status':'active','promotion_policy':{'max_discount_rate':0.15,'stackable':False},'shipping_policy':{'allowed_countries':('US','CA'),'preferred_options':('standard','express')},'risk_policy':{'manual_review_threshold':0.65,'block_threshold':0.9},'payment_policy':{'allowed_methods':('card','wallet'),'capture_mode':'authorize_then_capture'}},),
        'events': ({'event_id':'product_evt_demo','event_type':'ProductPublished','idempotency_key':'product:SKU-DEMO-100:v1','payload':{'tenant':tenant,'product_id':'SKU-DEMO-100','name':'Travel Pack','category':'bags'}}, {'event_id':'price_evt_demo','event_type':'PriceOptimized','idempotency_key':'price:SKU-DEMO-100:v1','payload':{'tenant':tenant,'product_id':'SKU-DEMO-100','unit_price':100.0,'currency':'USD'}}, {'event_id':'tax_evt_demo','event_type':'TaxCalculated','idempotency_key':'tax:calc_demo_100:v1','payload':{'tenant':tenant,'calculation_id':'calc_demo_100','tax_total':7.5}}),
        'cart': {'cart_id':'cart_demo_100','tenant':tenant,'customer_id':'cust_demo_100','channel':'web','currency':'USD','market':'US'},
        'cart_line': {'line_id':'line_demo_100','tenant':tenant,'cart_id':'cart_demo_100','product_id':'SKU-DEMO-100','quantity':2},
        'coupon': {'coupon_code':'SAVE10','requested_rate':0.10,'campaign':'launch'},
        'address': {'country':'US','region':'CA','city':'San Francisco','postal_code':'94105','shipping_option':'standard'},
        'session': {'session_id':'chk_demo_100','tenant':tenant,'cart_id':'cart_demo_100','order_id':'order_demo_100'},
        'pricing_handoff': {'pricing_handoff_id':'pricing_demo_100','tenant':tenant,'pricing_decision_id':'decision_demo_100'},
        'tax_quote': {'tenant':tenant,'calculation_id':'calc_demo_100','tax_total':7.5},
        'inventory_reservation': {'tenant':tenant,'reservation_id':'res_demo_100','lines':({'product_id':'SKU-DEMO-100','quantity':2},),'confidence':0.95},
        'risk_signals': {'account_age':2.5,'address_match':1.0,'payment_reputation':1.0,'velocity':0.0},
        'payment_intent': {'tenant':tenant,'payment_intent_id':'pay_demo_100','method':'card'},
        'document':'Checkout packet for cart_demo_100 SKU-DEMO-100 with SAVE10, standard US shipping, inventory reservation, card authorization and capture.',
        'instructions':'Create cart, add line, apply coupon, validate address, open checkout, apply pricing and tax, reserve and confirm inventory, authorize and capture payment, complete checkout.',
    }
