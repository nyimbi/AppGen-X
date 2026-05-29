from pyAppGen.pbcs.eam import implementation_contract, smoke_test
from pyAppGen.pbcs.eam.agent import composed_agent_contribution, document_instruction_plan
from pyAppGen.pbcs.eam.app_surface import (
    app_surface_smoke_test,
    eam_controls_contract,
    eam_forms_contract,
    eam_wizards_contract,
    end_to_end_maintenance_execution_proof,
    single_pbc_eam_app_contract,
    standalone_route_contracts,
)
from pyAppGen.pbcs.eam.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.eam.routes import api_route_contracts
from pyAppGen.pbcs.eam.ui import eam_ui_contract


def test_single_pbc_eam_app_covers_improve1_surface():
    app = single_pbc_eam_app_contract()

    assert app['ok'] is True
    assert app['application_mode'] == 'single_pbc_standalone'
    assert len(app['owned_tables']) >= 16
    assert len(app['forms']['covered_improve1_items']) == 50
    assert len(app['wizards']['covered_improve1_items']) == 50
    assert len(app['controls']['covered_improve1_items']) == 50
    assert app['dependency_boundary']['writes_foreign_tables'] is False
    assert app['dependency_boundary']['event_contract'] == 'AppGen-X'


def test_forms_wizards_controls_cover_maintenance_execution():
    forms = eam_forms_contract()
    wizards = eam_wizards_contract()
    controls = eam_controls_contract()

    assert 'register_equipment' in forms['covered_operations']
    assert 'create_work_order' in forms['covered_operations']
    assert 'complete_work_order' in forms['covered_operations']
    assert wizards['supports_equipment_to_completion'] is True
    assert wizards['supports_resilience_release_proof'] is True
    assert 'permit_isolation_gate' in controls['control_ids']
    assert 'appgen_event_reliability' in controls['control_ids']
    assert controls['stream_engine_picker_visible'] is False


def test_agent_document_plan_is_owned_and_safety_gated():
    plan = document_instruction_plan(
        'Compressor has vibration, needs bearing kit and electrical isolation.',
        'create predictive work order and spare issue after planner confirmation',
    )

    assert plan['ok'] is True
    assert plan['requires_human_confirmation'] is True
    assert plan['single_pbc_ready'] is True
    assert all(table.startswith('eam_') for table in plan['candidate_tables'])
    assert plan['safety_gates']


def test_routes_ui_agent_release_and_end_to_end_proof_include_surface():
    route_paths = tuple(route['path'] for route in standalone_route_contracts())
    api = api_route_contracts()
    ui = eam_ui_contract()
    agent = composed_agent_contribution()
    release = build_release_evidence()
    proof = end_to_end_maintenance_execution_proof()

    assert '/eam/app' in route_paths
    assert any(route['path'] == '/eam/app' for route in api['standalone_routes'])
    assert ui['single_pbc_app']['ok'] is True
    assert agent['standalone_app']['ok'] is True
    assert release['standalone_app_smoke']['ok'] is True
    assert proof['ok'] is True
    assert validate_release_evidence()['ok'] is True


def test_package_smoke_and_implementation_expose_app_surface():
    app_surface = app_surface_smoke_test()
    implementation = implementation_contract()
    package_smoke = smoke_test()

    assert app_surface['ok'] is True
    assert implementation['single_pbc_app']['ok'] is True
    assert implementation['app_surface_smoke']['ok'] is True
    assert package_smoke['ok'] is True
