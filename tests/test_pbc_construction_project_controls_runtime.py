from pyAppGen.pbcs.construction_project_controls import implementation_contract, construction_project_controls_runtime_capabilities, construction_project_controls_runtime_smoke, construction_project_controls_build_schema_contract, construction_project_controls_build_service_contract, construction_project_controls_build_release_evidence, construction_project_controls_receive_event, construction_project_controls_verify_owned_table_boundary, construction_project_controls_configure_runtime, construction_project_controls_set_parameter, construction_project_controls_register_rule, construction_project_controls_empty_state
from pyAppGen.pbcs.construction_project_controls.ui import construction_project_controls_ui_contract, construction_project_controls_render_workbench


def test_construction_project_controls_runtime_capabilities_and_contracts():
    runtime = construction_project_controls_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/construction_project_controls'
    assert construction_project_controls_build_schema_contract()['ok'] is True
    assert construction_project_controls_build_service_contract()['ok'] is True
    assert construction_project_controls_build_release_evidence()['ok'] is True
    assert construction_project_controls_runtime_smoke()['ok'] is True


def test_construction_project_controls_events_ui_boundary_and_configuration():
    state = construction_project_controls_empty_state()
    assert construction_project_controls_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.construction_project_controls.events'})['ok'] is True
    assert construction_project_controls_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert construction_project_controls_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert construction_project_controls_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert construction_project_controls_ui_contract()['ok'] is True
    assert construction_project_controls_render_workbench()['ok'] is True
    assert construction_project_controls_verify_owned_table_boundary((f'construction_project_controls_owned_table', 'foreign_table'))['ok'] is False
