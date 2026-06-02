"""Focused standalone one-PBC tests for product_catalog_pim."""
from pathlib import Path
from .. import agent, release_evidence, routes, services, standalone, ui
from ..repository import ProductCatalogPimStandaloneRepository

def test_repository_persists_seeded_catalog_workspace():
    repo=ProductCatalogPimStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); workbench=repo.build_workbench('tenant_demo'); read_model=repo.read_model('tenant_demo'); proof=repo.generate_publication_proof('tenant_demo','prod_demo_100',('product_id','sku','lifecycle_state','completeness'))
        assert seeded['ok'] is True; assert workbench['ok'] is True; assert read_model['ok'] is True; assert proof['ok'] is True
        assert read_model['family_count']==1; assert read_model['product_count']==1; assert read_model['published_product_count']==1; assert read_model['publication_count']==1; assert read_model['average_completeness']==1.0
    finally: repo.close()

def test_standalone_routes_ui_agent_and_release_surface():
    service=services.ProductCatalogPimStandaloneService()
    try:
        seed_route=routes.dispatch_standalone_route('POST','/app/product-catalog-pim/demo-workspace',{'tenant':'tenant_route_test'},service=service)
        workbench=routes.dispatch_standalone_route('GET','/app/product-catalog-pim/workbench',{'tenant':'tenant_route_test'},service=service)
        proof=routes.dispatch_standalone_route('POST','/app/product-catalog-pim/publication-proofs',{'tenant':'tenant_route_test','product_id':'prod_demo_100'},service=service)
        rendered=ui.product_catalog_pim_render_standalone_workbench(workbench['result']['result'])
        document_plan=agent.document_instruction_plan('supplier SKU sheet with taxonomy media price claim','register enrich publish proof')
        crud_plan=agent.datastore_crud_plan('create','product_catalog_pim_product',{'product_id':'prod_demo_100'})
        app_contract=standalone.product_catalog_pim_standalone_app_contract(); smoke=standalone.product_catalog_pim_standalone_app_smoke(); evidence=release_evidence.build_release_evidence()
        assert seed_route['ok'] is True; assert workbench['ok'] is True; assert proof['ok'] is True; assert rendered['ok'] is True
        assert document_plan['wizard_candidates']; assert crud_plan['route_candidates']; assert app_contract['ok'] is True; assert smoke['ok'] is True; assert evidence['standalone_app']['ok'] is True; assert evidence['standalone_repository']['ok'] is True
    finally: service.close()

def test_package_local_docs_exist_for_release_evidence():
    base=Path(__file__).resolve().parent.parent
    for name in ('README.md','RELEASE_EVIDENCE.md','repository.py','standalone.py'):
        assert (base/name).exists() is True
