"""Standalone one-PBC application surface for the Production Control package."""
from __future__ import annotations
from tempfile import NamedTemporaryFile
from . import agent, ui
from .repository import ProductionControlStandaloneRepository, standalone_repository_contract, standalone_repository_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import ProductionControlStandaloneService, standalone_service_operation_contracts

def production_control_standalone_app_contract():
    repo=standalone_repository_contract(); services=standalone_service_operation_contracts(); routes=standalone_route_contracts(); workbench=ui.production_control_standalone_workbench_blueprint(); workspace=agent.standalone_agent_workspace_contract()
    return {'format':'appgen.production-control-standalone-app.v1','ok':all(i.get('ok') is True for i in (repo,services,routes,workbench,workspace)),'pbc':'production_control','repository':repo,'services':services,'routes':routes,'ui':workbench,'agent':workspace,'side_effects':()}
def production_control_bootstrap_standalone_app(database_path=':memory:',*,tenant='tenant_demo',seed_demo=True):
    repo=ProductionControlStandaloneRepository(database_path=database_path); service=ProductionControlStandaloneService(repo); seeded=repo.seed_demo_workspace(tenant=tenant) if seed_demo else {'ok':True,'tenant':tenant}
    return {'ok':seeded['ok'],'pbc':'production_control','repository':repo,'service':service,'seeded':seeded,'contract':production_control_standalone_app_contract(),'side_effects':()}
def production_control_standalone_app_smoke():
    bundle=production_control_bootstrap_standalone_app(seed_demo=False); service=bundle['service']
    try:
        seed_route=dispatch_standalone_route('POST','/app/production-control/demo-workspace',{'tenant':'tenant_demo'},service=service)
        workbench=dispatch_standalone_route('GET','/app/production-control/workbench',{'tenant':'tenant_demo'},service=service)
        proof=dispatch_standalone_route('POST','/app/production-control/proofs',{'tenant':'tenant_demo','order_id':'order_demo_100','disclosure':('order_id','item','completed_qty')},service=service)
        rendered=ui.production_control_render_standalone_workbench(workbench['result']['result'])
        return {'ok':bundle['contract']['ok'] and seed_route['ok'] and workbench['ok'] and proof['ok'] and rendered['ok'] and standalone_repository_smoke_test()['ok'],'contract':bundle['contract'],'seed_route':seed_route,'workbench':workbench,'proof':proof,'rendered':rendered,'side_effects':()}
    finally: service.close()
def standalone_release_snapshot():
    with NamedTemporaryFile(suffix='.sqlite3') as handle:
        app=production_control_bootstrap_standalone_app(database_path=handle.name,seed_demo=True)
        try:
            workbench=app['service'].build_workbench('tenant_demo')
            return {'ok':app['ok'] and workbench['ok'],'app':app['contract'],'workbench':workbench,'read_model':app['repository'].read_model('tenant_demo'),'side_effects':()}
        finally: app['service'].close()
