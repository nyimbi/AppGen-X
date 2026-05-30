"""Focused standalone one-PBC tests for price_promotion_engine."""
from pathlib import Path
from .. import agent, release_evidence, routes, services, standalone, ui
from ..repository import PricePromotionEngineStandaloneRepository

def test_repository_persists_seeded_pricing_workspace():
    repo=PricePromotionEngineStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); workbench=repo.build_workbench('tenant_demo'); read_model=repo.read_model('tenant_demo')
        assert seeded['ok'] is True; assert workbench['ok'] is True; assert read_model['ok'] is True
        assert read_model['price_rule_count']==1; assert read_model['promotion_count']==1; assert read_model['approved_promotion_count']==1; assert read_model['coupon_redemption_count']==1; assert read_model['settlement_count']==1
    finally: repo.close()

def test_standalone_routes_ui_agent_and_release_surface():
    service=services.PricePromotionEngineStandaloneService()
    try:
        seed_route=routes.dispatch_standalone_route('POST','/app/price-promotion-engine/demo-workspace',{'tenant':'tenant_route_test'},service=service)
        workbench=routes.dispatch_standalone_route('GET','/app/price-promotion-engine/workbench',{'tenant':'tenant_route_test'},service=service)
        quote=routes.dispatch_standalone_route('POST','/app/price-promotion-engine/quotes',{'tenant':'tenant_route_test','decision_id':'decision_route_100','customer_id':'cust_demo_100','sku':'SKU-DEMO-100','region':'US','currency':'USD','quantity':3,'promotion_codes':()},service=service)
        rendered=ui.price_promotion_engine_render_standalone_workbench(workbench['result']['result'])
        document_plan=agent.document_instruction_plan('promotion brief PROMO10 sku quote coupon settlement','create promotion quote redeem settle')
        crud_plan=agent.datastore_crud_plan('create','price_promotion_engine_price_rule',{'sku':'SKU-DEMO-100'})
        app_contract=standalone.price_promotion_engine_standalone_app_contract(); smoke=standalone.price_promotion_engine_standalone_app_smoke(); evidence=release_evidence.build_release_evidence()
        assert seed_route['ok'] is True; assert workbench['ok'] is True; assert quote['ok'] is True; assert rendered['ok'] is True
        assert document_plan['wizard_candidates']; assert crud_plan['route_candidates']; assert app_contract['ok'] is True; assert smoke['ok'] is True; assert evidence['standalone_app']['ok'] is True; assert evidence['standalone_repository']['ok'] is True
    finally: service.close()

def test_package_local_docs_exist_for_release_evidence():
    base=Path(__file__).resolve().parent.parent
    for name in ('README.md','RELEASE_EVIDENCE.md','repository.py','standalone.py'):
        assert (base/name).exists() is True
