"""Focused standalone one-PBC tests for mrp_engine."""

from pathlib import Path

from .. import agent, release_evidence, routes, services, standalone, ui
from ..repository import MrpEngineStandaloneRepository


def test_repository_persists_seeded_mrp_workspace():
    repository = MrpEngineStandaloneRepository()
    try:
        seeded = repository.seed_demo_workspace()
        workbench = repository.build_workbench('tenant_demo')
        read_model = repository.read_model('tenant_demo')
        proof = repository.generate_supply_proof('tenant_demo', 'po_run_demo_100_component_a', ('planned_order_id', 'item', 'quantity'))
        assert seeded['ok'] is True
        assert workbench['ok'] is True
        assert read_model['ok'] is True
        assert proof['ok'] is True
        assert read_model['bom_count'] == 1
        assert read_model['demand_count'] == 1
        assert read_model['planned_order_count'] == 1
        assert read_model['released_order_count'] == 1
    finally:
        repository.close()


def test_standalone_routes_ui_agent_and_release_surface():
    service = services.MrpEngineStandaloneService()
    try:
        seed_route = routes.dispatch_standalone_route('POST', '/app/mrp-engine/demo-workspace', {'tenant': 'tenant_route_test'}, service=service)
        workbench = routes.dispatch_standalone_route('GET', '/app/mrp-engine/workbench', {'tenant': 'tenant_route_test'}, service=service)
        proof = routes.dispatch_standalone_route('POST', '/app/mrp-engine/proofs', {'tenant': 'tenant_route_test', 'planned_order_id': 'po_run_demo_100_component_a'}, service=service)
        rendered = ui.mrp_engine_render_standalone_workbench(workbench['result']['result'])
        document_plan = agent.document_instruction_plan('BOM and demand instruction', 'run mrp and release planned order')
        crud_plan = agent.datastore_crud_plan('create', 'mrp_engine_bill_of_material', {'bom_id': 'bom_demo_100'})
        app_contract = standalone.mrp_engine_standalone_app_contract()
        smoke = standalone.mrp_engine_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert seed_route['ok'] is True
        assert workbench['ok'] is True
        assert proof['ok'] is True
        assert rendered['ok'] is True
        assert document_plan['wizard_candidates']
        assert crud_plan['route_candidates']
        assert app_contract['ok'] is True
        assert smoke['ok'] is True
        assert evidence['standalone_app']['ok'] is True
        assert evidence['standalone_repository']['ok'] is True
    finally:
        service.close()


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ('README.md', 'RELEASE_EVIDENCE.md', 'repository.py', 'standalone.py'):
        assert (base / name).exists() is True
