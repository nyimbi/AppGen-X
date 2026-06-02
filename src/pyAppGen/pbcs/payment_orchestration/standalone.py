"""Standalone one-PBC application surface for Payment Orchestration."""
from __future__ import annotations
from tempfile import NamedTemporaryFile
from . import agent, ui
from .repository import PaymentOrchestrationStandaloneRepository, standalone_repository_contract, standalone_repository_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import PaymentOrchestrationStandaloneService, standalone_service_operation_contracts

def payment_orchestration_standalone_app_contract():
    repo=standalone_repository_contract(); services=standalone_service_operation_contracts(); routes=standalone_route_contracts(); workbench=ui.payment_orchestration_standalone_workbench_blueprint(); workspace=agent.standalone_agent_workspace_contract()
    return {'format':'appgen.payment-orchestration-standalone-app.v1','ok':all(i.get('ok') is True for i in (repo,services,routes,workbench,workspace)),'pbc':'payment_orchestration','repository':repo,'services':services,'routes':routes,'ui':workbench,'agent':workspace,'side_effects':()}
def payment_orchestration_bootstrap_standalone_app(database_path=':memory:',*,tenant='tenant_demo',seed_demo=True):
    repo=PaymentOrchestrationStandaloneRepository(database_path=database_path); service=PaymentOrchestrationStandaloneService(repo); seeded=repo.seed_demo_workspace(tenant=tenant) if seed_demo else {'ok':True,'tenant':tenant}
    return {'ok':seeded['ok'],'pbc':'payment_orchestration','repository':repo,'service':service,'seeded':seeded,'contract':payment_orchestration_standalone_app_contract(),'side_effects':()}
def payment_orchestration_standalone_app_smoke():
    bundle=payment_orchestration_bootstrap_standalone_app(seed_demo=False); service=bundle['service']
    try:
        seed_route=dispatch_standalone_route('POST','/app/payment-orchestration/demo-workspace',{'tenant':'tenant_demo'},service=service)
        workbench=dispatch_standalone_route('GET','/app/payment-orchestration/workbench',{'tenant':'tenant_demo'},service=service)
        proof=dispatch_standalone_route('POST','/app/payment-orchestration/proofs',{'tenant':'tenant_demo','intent_id':'pi_demo_100','disclosure':('intent_id','amount','currency','status')},service=service)
        rendered=ui.payment_orchestration_render_standalone_workbench(workbench['result'])
        return {'ok':bundle['contract']['ok'] and seed_route['ok'] and workbench['ok'] and proof['ok'] and rendered['ok'] and standalone_repository_smoke_test()['ok'],'contract':bundle['contract'],'seed_route':seed_route,'workbench':workbench,'proof':proof,'rendered':rendered,'side_effects':()}
    finally: service.close()
def standalone_release_snapshot():
    with NamedTemporaryFile(suffix='.sqlite3') as handle:
        app=payment_orchestration_bootstrap_standalone_app(database_path=handle.name,seed_demo=True)
        try:
            workbench=app['service'].build_workbench('tenant_demo')
            return {'ok':app['ok'] and workbench['ok'],'app':app['contract'],'workbench':workbench,'read_model':app['repository'].read_model('tenant_demo'),'side_effects':()}
        finally: app['service'].close()
