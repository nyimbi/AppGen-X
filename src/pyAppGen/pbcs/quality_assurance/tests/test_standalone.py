"""Focused standalone one-PBC tests for quality_assurance."""

from pathlib import Path

from .. import agent, release_evidence, routes, seed_data, services, standalone, ui
from ..repository import QualityAssuranceStandaloneRepository


def test_repository_persists_seeded_quality_workspace():
    repository = QualityAssuranceStandaloneRepository()
    try:
        seeded = repository.seed_demo_workspace()
        workbench = repository.build_workbench('tenant_demo')
        read_model = repository.read_model('tenant_demo')
        controls = repository.run_control_tests('tenant_demo')
        proof = repository.generate_quality_proof('tenant_demo', 'result_demo_100', ('result_id', 'lot_id', 'decision'))
        assert seeded['ok'] is True
        assert workbench['ok'] is True
        assert read_model['ok'] is True
        assert controls['ok'] is True
        assert proof['ok'] is True
        assert read_model['plan_count'] == 1
        assert read_model['result_count'] == 1
        assert read_model['hold_count'] == 1
    finally:
        repository.close()


def test_standalone_routes_ui_agent_and_release_surface():
    service = services.QualityAssuranceStandaloneService()
    try:
        seed_route = routes.dispatch_standalone_route('POST', '/app/quality-assurance/demo-workspace', {'tenant': 'tenant_route_test'}, service=service)
        workbench = routes.dispatch_standalone_route('GET', '/app/quality-assurance/workbench', {'tenant': 'tenant_route_test'}, service=service)
        controls = routes.dispatch_standalone_route('GET', '/app/quality-assurance/controls', {'tenant': 'tenant_route_test'}, service=service)
        rendered = ui.quality_assurance_render_standalone_workbench(workbench['result']['result'])
        document_plan = agent.document_instruction_plan('inspection certificate for lot', 'create hold and nonconformance disposition')
        crud_plan = agent.datastore_crud_plan('create', 'quality_assurance_inspection_plan', {'plan_id': 'plan_demo_100'})
        app_contract = standalone.quality_assurance_standalone_app_contract()
        smoke = standalone.quality_assurance_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert seed_route['ok'] is True
        assert workbench['ok'] is True
        assert controls['ok'] is True
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
