"""Standalone one-PBC application surface for the Checkout Processing package."""
from __future__ import annotations
from tempfile import NamedTemporaryFile
from . import agent, ui
from .repository import CheckoutProcessingStandaloneRepository, standalone_repository_contract, standalone_repository_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import CheckoutProcessingStandaloneService, standalone_service_operation_contracts

def checkout_processing_standalone_app_contract():
    repo=standalone_repository_contract(); services=standalone_service_operation_contracts(); routes=standalone_route_contracts(); workbench=ui.checkout_processing_standalone_workbench_blueprint(); workspace=agent.standalone_agent_workspace_contract()
    return {'format':'appgen.checkout-processing-standalone-app.v1','ok':all(i.get('ok') is True for i in (repo,services,routes,workbench,workspace)),'pbc':'checkout_processing','repository':repo,'services':services,'routes':routes,'ui':workbench,'agent':workspace,'side_effects':()}
def checkout_processing_bootstrap_standalone_app(database_path=':memory:',*,tenant='tenant_demo',seed_demo=True):
    repo=CheckoutProcessingStandaloneRepository(database_path=database_path); service=CheckoutProcessingStandaloneService(repo); seeded=repo.seed_demo_workspace(tenant=tenant) if seed_demo else {'ok':True,'tenant':tenant}
    return {'ok':seeded['ok'],'pbc':'checkout_processing','repository':repo,'service':service,'seeded':seeded,'contract':checkout_processing_standalone_app_contract(),'side_effects':()}
def checkout_processing_standalone_app_smoke():
    bundle=checkout_processing_bootstrap_standalone_app(seed_demo=False); service=bundle['service']
    try:
        seed_route=dispatch_standalone_route('POST','/app/checkout-processing/demo-workspace',{'tenant':'tenant_demo'},service=service)
        workbench=dispatch_standalone_route('GET','/app/checkout-processing/workbench',{'tenant':'tenant_demo'},service=service)
        proof=dispatch_standalone_route('POST','/app/checkout-processing/proofs',{'tenant':'tenant_demo','session_id':'chk_demo_100','disclosure':('session_id','order_id','status','total')},service=service)
        rendered=ui.checkout_processing_render_standalone_workbench(workbench['result'])
        return {'ok':bundle['contract']['ok'] and seed_route['ok'] and workbench['ok'] and proof['ok'] and rendered['ok'] and standalone_repository_smoke_test()['ok'],'contract':bundle['contract'],'seed_route':seed_route,'workbench':workbench,'proof':proof,'rendered':rendered,'side_effects':()}
    finally: service.close()
def standalone_release_snapshot():
    with NamedTemporaryFile(suffix='.sqlite3') as handle:
        app=checkout_processing_bootstrap_standalone_app(database_path=handle.name,seed_demo=True)
        try:
            workbench=app['service'].build_workbench('tenant_demo')
            return {'ok':app['ok'] and workbench['ok'],'app':app['contract'],'workbench':workbench,'read_model':app['repository'].read_model('tenant_demo'),'side_effects':()}
        finally: app['service'].close()
