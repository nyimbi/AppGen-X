"""Focused standalone one-PBC tests for production_control."""
from pathlib import Path
from .. import agent, release_evidence, routes, services, standalone, ui
from ..repository import ProductionControlStandaloneRepository

def test_repository_persists_seeded_production_workspace():
    repo=ProductionControlStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); workbench=repo.build_workbench('tenant_demo'); read_model=repo.read_model('tenant_demo'); proof=repo.generate_completion_proof('tenant_demo','order_demo_100',('order_id','item','completed_qty'))
        assert seeded['ok'] is True; assert workbench['ok'] is True; assert read_model['ok'] is True; assert proof['ok'] is True
        assert read_model['work_center_count']==1; assert read_model['order_count']==1; assert read_model['completed_order_count']==1; assert read_model['completed_qty']==9
    finally: repo.close()

def test_standalone_routes_ui_agent_and_release_surface():
    service=services.ProductionControlStandaloneService()
    try:
        seed_route=routes.dispatch_standalone_route('POST','/app/production-control/demo-workspace',{'tenant':'tenant_route_test'},service=service)
        workbench=routes.dispatch_standalone_route('GET','/app/production-control/workbench',{'tenant':'tenant_route_test'},service=service)
        proof=routes.dispatch_standalone_route('POST','/app/production-control/proofs',{'tenant':'tenant_route_test','order_id':'order_demo_100'},service=service)
        rendered=ui.production_control_render_standalone_workbench(workbench['result']['result'])
        document_plan=agent.document_instruction_plan('shop floor packet','start operation confirm complete proof')
        crud_plan=agent.datastore_crud_plan('create','production_control_production_order',{'order_id':'order_demo_100'})
        app_contract=standalone.production_control_standalone_app_contract(); smoke=standalone.production_control_standalone_app_smoke(); evidence=release_evidence.build_release_evidence()
        assert seed_route['ok'] is True; assert workbench['ok'] is True; assert proof['ok'] is True; assert rendered['ok'] is True
        assert document_plan['wizard_candidates']; assert crud_plan['route_candidates']; assert app_contract['ok'] is True; assert smoke['ok'] is True; assert evidence['standalone_app']['ok'] is True; assert evidence['standalone_repository']['ok'] is True
    finally: service.close()

def test_package_local_docs_exist_for_release_evidence():
    base=Path(__file__).resolve().parent.parent
    for name in ('README.md','RELEASE_EVIDENCE.md','repository.py','standalone.py'):
        assert (base/name).exists() is True
