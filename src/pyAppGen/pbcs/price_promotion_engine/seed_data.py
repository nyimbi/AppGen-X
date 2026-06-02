"""Executable seed-data contract for the price_promotion_engine PBC."""

PBC_KEY = 'price_promotion_engine'
SEED_DATA = ({'table': 'price_promotion_engine_price_rule', 'rows': ({'code': 'PRICE_PROMOTION_ENGINE-001', 'status': 'active'},)}, {'table': 'price_promotion_engine_promotion', 'rows': ({'code': 'PRICE_PROMOTION_ENGINE-002', 'status': 'active'},)})


def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item['table'] for item in SEED_DATA))
    return {
        'ok': bool(SEED_DATA),
        'pbc': PBC_KEY,
        'tables': tables,
        'rows': SEED_DATA,
        'side_effects': (),
    }


def validate_seed_data():
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item['table'] for item in SEED_DATA if not item.get('table', '').startswith(f'{PBC_KEY}_')
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get('rows', ())
        if not row.get('code') or not row.get('status')
    )
    plan = seed_plan()
    return {
        'ok': plan['ok'] and not invalid_tables and not invalid_rows,
        'pbc': PBC_KEY,
        'plan': plan,
        'invalid_tables': invalid_tables,
        'invalid_rows': invalid_rows,
        'side_effects': (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()



def standalone_seed_bundle(*, tenant='tenant_demo'):
    return {
        'pbc': PBC_KEY, 'tenant': tenant,
        'configuration': {'database_backend':'postgresql','event_topic':'appgen.price_promotion.events','retry_limit':3,'default_currency':'USD','supported_currencies':('USD','EUR'),'supported_regions':('US','EU'),'pricing_calendars':('standard','holiday'),'default_timezone':'UTC','decision_mode':'guided','workbench_limit':100,'approval_mode':'manager','simulation_horizon_days':30,'telemetry_window_minutes':15},
        'parameters': {'margin_floor_percent':20,'promotion_stack_limit':2,'elasticity_weight':0.2,'forecast_weight':0.2,'segment_weight':0.2,'loyalty_weight':0.1,'risk_review_threshold':0.9,'discount_ceiling_percent':40,'decision_ttl_minutes':60,'workbench_limit':100,'approval_discount_threshold_percent':10,'campaign_budget_guardrail':0.8,'coupon_reuse_limit':3},
        'rules': ({'rule_id':'price.demo.policy','tenant':tenant,'scope':'quote','status':'active','allowed_currencies':('USD','EUR'),'allowed_regions':('US','EU'),'allowed_segments':('standard','vip'),'promotion_policy':{'enabled':True},'margin_policy':{'floor_percent':20},'stacking_policy':{'limit':2},'exclusion_policy':{'mutual_group':'default'},'approval_policy':{'discount_threshold_percent':10},'budget_policy':{'guardrail':0.8}},),
        'events': ({'event_id':'seg_evt_demo','event_type':'CustomerSegmentUpdated','payload':{'tenant':tenant,'customer_id':'cust_demo_100','segment':'vip','loyalty_tier_id':'tier_gold'}}, {'event_id':'forecast_evt_demo','event_type':'ForecastUpdated','payload':{'tenant':tenant,'sku':'SKU-DEMO-100','demand_index':0.8,'risk_index':0.1}}),
        'price_rule': {'price_rule_id':'price_rule_demo_100','tenant':tenant,'sku':'SKU-DEMO-100','region':'US','currency':'USD','base_price':100.0,'cost':55.0,'segments':('standard','vip'),'volume_breaks':((10,0.05),(25,0.08)),'status':'active','channel':'digital_store','customer_id':'cust_demo_100'},
        'price_agreement': {'agreement_id':'agreement_demo_100','tenant':tenant,'customer_id':'cust_demo_100','sku':'SKU-DEMO-100','region':'US','currency':'USD','contracted_price':92.0,'effective_from':'2026-01-01','effective_to':'2026-12-31','status':'active'},
        'promotion': {'promotion_id':'promo_demo_100','tenant':tenant,'code':'PROMO10','discount_percent':10.0,'segments':('vip',),'regions':('US',),'currencies':('USD',),'channels':('digital_store',),'stackable':True,'status':'active','budget_amount':10000.0,'approval_required':True,'approval_status':'pending'},
        'loyalty_tier': {'tier_id':'tier_gold','tenant':tenant,'name':'Gold','rank':1,'discount_percent':3.0,'status':'active'},
        'quote': {'decision_id':'decision_demo_100','tenant':tenant,'customer_id':'cust_demo_100','sku':'SKU-DEMO-100','region':'US','currency':'USD','quantity':12,'promotion_codes':('PROMO10',),'channel':'digital_store'},
        'trade_promotion_plan': {'plan_id':'plan_demo_100','tenant':tenant,'promotion_id':'promo_demo_100','calendar':'standard','target_uplift_percent':12.0,'spend_amount':2500.0,'owner_role':'trade_marketing','status':'active'},
        'price_exception': {'exception_id':'exception_demo_100','tenant':tenant,'subject_type':'campaign_budget','subject_id':'promo_demo_100:budget','severity':'medium','reason':'budget_review'},
        'document':'Promotion brief for SKU-DEMO-100 customer cust_demo_100 with VIP segment, PROMO10 coupon, campaign budget, and quote request.',
        'instructions':'Create price rule, approve promotion, quote customer price, redeem coupon, accrue and settle promotion, and surface pricing workbench controls.',
    }
