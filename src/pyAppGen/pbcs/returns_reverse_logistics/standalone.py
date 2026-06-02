"""Standalone one-PBC application surface for Returns Reverse Logistics."""
from __future__ import annotations
from tempfile import NamedTemporaryFile
from . import agent, ui
from .repository import ReturnsReverseLogisticsStandaloneRepository, standalone_repository_contract, standalone_repository_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import ReturnsReverseLogisticsStandaloneService, standalone_service_operation_contracts

def returns_reverse_logistics_standalone_app_contract():
    repo=standalone_repository_contract(); services=standalone_service_operation_contracts(); routes=standalone_route_contracts(); workbench=ui.returns_reverse_logistics_standalone_workbench_blueprint(); workspace=agent.standalone_agent_workspace_contract()
    return {'format':'appgen.returns-reverse-logistics-standalone-app.v1','ok':all(i.get('ok') is True for i in (repo,services,routes,workbench,workspace)),'pbc':'returns_reverse_logistics','repository':repo,'services':services,'routes':routes,'ui':workbench,'agent':workspace,'side_effects':()}
def returns_reverse_logistics_bootstrap_standalone_app(database_path=':memory:',*,tenant='tenant_demo',seed_demo=True):
    repo=ReturnsReverseLogisticsStandaloneRepository(database_path=database_path); service=ReturnsReverseLogisticsStandaloneService(repo); seeded=repo.seed_demo_workspace(tenant=tenant) if seed_demo else {'ok':True,'tenant':tenant}
    return {'ok':seeded['ok'],'pbc':'returns_reverse_logistics','repository':repo,'service':service,'seeded':seeded,'contract':returns_reverse_logistics_standalone_app_contract(),'side_effects':()}
def returns_reverse_logistics_standalone_app_smoke():
    bundle=returns_reverse_logistics_bootstrap_standalone_app(seed_demo=False); service=bundle['service']
    try:
        seed_route=dispatch_standalone_route('POST','/app/returns-reverse-logistics/demo-workspace',{'tenant':'tenant_demo'},service=service)
        workbench=dispatch_standalone_route('GET','/app/returns-reverse-logistics/workbench',{'tenant':'tenant_demo'},service=service)
        proof=dispatch_standalone_route('POST','/app/returns-reverse-logistics/proofs',{'tenant':'tenant_demo','return_id':'ret_demo_100','disclosure':('return_id','order_id','status')},service=service)
        rendered=ui.returns_reverse_logistics_render_standalone_workbench(workbench['result'])
        return {'ok':bundle['contract']['ok'] and seed_route['ok'] and workbench['ok'] and proof['ok'] and rendered['ok'] and standalone_repository_smoke_test()['ok'],'contract':bundle['contract'],'seed_route':seed_route,'workbench':workbench,'proof':proof,'rendered':rendered,'side_effects':()}
    finally: service.close()
def standalone_release_snapshot():
    with NamedTemporaryFile(suffix='.sqlite3') as handle:
        app=returns_reverse_logistics_bootstrap_standalone_app(database_path=handle.name,seed_demo=True)
        try:
            workbench=app['service'].build_workbench('tenant_demo')
            return {'ok':app['ok'] and workbench['ok'],'app':app['contract'],'workbench':workbench,'read_model':app['repository'].read_model('tenant_demo'),'side_effects':()}
        finally: app['service'].close()
