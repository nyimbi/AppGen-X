"""Focused standalone one-PBC tests for asset_lifecycle."""
from pathlib import Path
from .. import agent, release_evidence, routes, services, standalone, ui
from ..repository import AssetLifecycleStandaloneRepository

def test_repository_persists_seeded_asset_workspace():
    repo=AssetLifecycleStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(); workbench=repo.build_workbench('tenant_demo'); read_model=repo.read_model('tenant_demo'); proof=repo.generate_asset_audit_proof('tenant_demo','asset_demo_100',('asset_id','status','book_value','location'))
        assert seeded['ok'] is True; assert workbench['ok'] is True; assert read_model['ok'] is True; assert proof['ok'] is True
        assert read_model['asset_count']==1; assert read_model['in_service_count']==1; assert read_model['net_book_value'] < 120000; assert workbench['active_schedule_versions']['asset_demo_100'] == 2
    finally: repo.close()

def test_standalone_routes_ui_agent_and_release_surface():
    service=services.AssetLifecycleStandaloneService()
    try:
        seed_route=routes.dispatch_standalone_route('POST','/app/asset-lifecycle/demo-workspace',{'tenant':'tenant_route_test'},service=service)
        workbench=routes.dispatch_standalone_route('GET','/app/asset-lifecycle/workbench',{'tenant':'tenant_route_test'},service=service)
        proof=routes.dispatch_standalone_route('POST','/app/asset-lifecycle/audit-proofs',{'tenant':'tenant_route_test','asset_id':'asset_demo_100'},service=service)
        rendered=ui.asset_lifecycle_render_standalone_workbench(workbench['result']['result'])
        document_plan=agent.document_instruction_plan('capitalization packet cost 120000 life 60 component spindle','register service depreciation transfer proof')
        crud_plan=agent.datastore_crud_plan('create','asset_lifecycle_fixed_asset',{'asset_id':'asset_demo_100'})
        app_contract=standalone.asset_lifecycle_standalone_app_contract(); smoke=standalone.asset_lifecycle_standalone_app_smoke(); evidence=release_evidence.build_release_evidence()
        assert seed_route['ok'] is True; assert workbench['ok'] is True; assert proof['ok'] is True; assert rendered['ok'] is True
        assert document_plan['wizard_candidates']; assert crud_plan['route_candidates']; assert app_contract['ok'] is True; assert smoke['ok'] is True; assert evidence['standalone_app']['ok'] is True; assert evidence['standalone_repository']['ok'] is True
    finally: service.close()

def test_package_local_docs_exist_for_release_evidence():
    base=Path(__file__).resolve().parent.parent
    for name in ('README.md','RELEASE_EVIDENCE.md','repository.py','standalone.py'):
        assert (base/name).exists() is True
