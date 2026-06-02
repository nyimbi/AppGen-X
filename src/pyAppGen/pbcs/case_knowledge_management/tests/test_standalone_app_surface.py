from pyAppGen.pbcs.case_knowledge_management import implementation_contract, smoke_test
from pyAppGen.pbcs.case_knowledge_management.agent import composed_agent_contribution, document_instruction_plan
from pyAppGen.pbcs.case_knowledge_management.app_surface import (
    app_surface_smoke_test,
    case_knowledge_management_controls_contract,
    case_knowledge_management_forms_contract,
    case_knowledge_management_wizards_contract,
    single_pbc_case_knowledge_management_app_contract,
    standalone_route_contracts,
)
from pyAppGen.pbcs.case_knowledge_management.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.case_knowledge_management.routes import api_route_contracts
from pyAppGen.pbcs.case_knowledge_management.ui import case_knowledge_management_ui_contract


def test_single_pbc_case_knowledge_management_app_is_functional():
    app = single_pbc_case_knowledge_management_app_contract()

    assert app['ok'] is True
    assert app['application_mode'] == 'single_pbc_standalone'
    assert len(app['owned_tables']) >= 24
    assert len(app['forms']['forms']) >= 7
    assert app['wizards']['supports_case_to_resolution'] is True
    assert app['wizards']['supports_knowledge_authoring'] is True
    assert app['dependency_boundary']['writes_foreign_tables'] is False
    assert app['dependency_boundary']['event_contract'] == 'AppGen-X'


def test_forms_wizards_controls_cover_case_and_knowledge_work():
    forms = case_knowledge_management_forms_contract()
    wizards = case_knowledge_management_wizards_contract()
    controls = case_knowledge_management_controls_contract()

    assert 'create_support_case' in forms['covered_operations']
    assert 'publish_knowledge_article' in forms['covered_operations']
    assert wizards['supports_agent_document_intake'] is True
    assert 'agent_grounding_toggle' in controls['control_ids']
    assert 'freshness_watchlist' in controls['control_ids']


def test_document_instruction_agent_targets_only_owned_tables():
    plan = document_instruction_plan(
        'Customer case asks for escalation and a knowledge article update.',
        'create case and update knowledge article after confirmation',
    )

    assert plan['ok'] is True
    assert plan['requires_human_confirmation'] is True
    assert plan['single_pbc_ready'] is True
    assert all(table.startswith('case_knowledge_management_') for table in plan['candidate_tables'])


def test_routes_ui_agent_and_release_include_standalone_surface():
    route_paths = tuple(route['path'] for route in standalone_route_contracts())
    api = api_route_contracts()
    ui = case_knowledge_management_ui_contract()
    agent = composed_agent_contribution()
    release = build_release_evidence()

    assert '/case-knowledge-management/app' in route_paths
    assert any(route['path'] == '/case-knowledge-management/app' for route in api['standalone_routes'])
    assert ui['single_pbc_app']['ok'] is True
    assert agent['standalone_app']['ok'] is True
    assert release['standalone_app_smoke']['ok'] is True
    assert validate_release_evidence()['ok'] is True


def test_package_smoke_and_implementation_expose_app_surface():
    app_surface = app_surface_smoke_test()
    implementation = implementation_contract()
    package_smoke = smoke_test()

    assert app_surface['ok'] is True
    assert implementation['single_pbc_app']['ok'] is True
    assert implementation['app_surface_smoke']['ok'] is True
    assert package_smoke['ok'] is True
