from pyAppGen.pbcs.revenue_recognition import implementation_contract, smoke_test
from pyAppGen.pbcs.revenue_recognition.agent import composed_agent_contribution, document_instruction_plan
from pyAppGen.pbcs.revenue_recognition.app_surface import (
    app_surface_smoke_test,
    revenue_recognition_controls_contract,
    revenue_recognition_forms_contract,
    revenue_recognition_wizards_contract,
    single_pbc_revenue_recognition_app_contract,
    standalone_route_contracts,
)
from pyAppGen.pbcs.revenue_recognition.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.revenue_recognition.routes import api_route_contracts
from pyAppGen.pbcs.revenue_recognition.ui import revenue_recognition_ui_contract


def test_single_pbc_revenue_recognition_app_is_functional():
    app = single_pbc_revenue_recognition_app_contract()

    assert app['ok'] is True
    assert app['application_mode'] == 'single_pbc_standalone'
    assert len(app['owned_tables']) >= 20
    assert len(app['forms']['forms']) >= 6
    assert app['wizards']['supports_five_step_model'] is True
    assert app['wizards']['supports_modifications_and_close'] is True
    assert app['dependency_boundary']['writes_foreign_tables'] is False
    assert app['dependency_boundary']['event_contract'] == 'AppGen-X'


def test_forms_wizards_controls_cover_revenue_table_stakes():
    forms = revenue_recognition_forms_contract()
    wizards = revenue_recognition_wizards_contract()
    controls = revenue_recognition_controls_contract()

    assert 'command_revenue_contract' in forms['covered_operations']
    assert 'run_close_readiness_check' in wizards['terminal_operations']
    assert 'ssp_allocation_control' in controls['control_ids']
    assert 'variable_consideration_constraint' in controls['control_ids']
    assert controls['stream_engine_picker_visible'] is False


def test_document_instruction_agent_targets_only_revenue_owned_tables():
    plan = document_instruction_plan(
        'Modification adds variable usage fees and requires a hold before recognition.',
        'create modification assessment and update allocation evidence',
    )

    assert plan['ok'] is True
    assert plan['requires_human_confirmation'] is True
    assert plan['single_pbc_ready'] is True
    assert all(table.startswith('revenue_recognition_') for table in plan['candidate_tables'])


def test_routes_ui_agent_and_release_include_standalone_surface():
    route_paths = tuple(route['path'] for route in standalone_route_contracts())
    api = api_route_contracts()
    ui = revenue_recognition_ui_contract()
    agent = composed_agent_contribution()
    release = build_release_evidence()

    assert '/revenue-recognition/app' in route_paths
    assert any(route['path'] == '/revenue-recognition/app' for route in api['standalone_routes'])
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
