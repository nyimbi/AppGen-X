from pyAppGen.pbcs.building_information_modeling_ops import implementation_contract, building_information_modeling_ops_runtime_capabilities, building_information_modeling_ops_runtime_smoke, building_information_modeling_ops_build_schema_contract, building_information_modeling_ops_build_service_contract, building_information_modeling_ops_build_release_evidence, building_information_modeling_ops_receive_event, building_information_modeling_ops_verify_owned_table_boundary, building_information_modeling_ops_configure_runtime, building_information_modeling_ops_set_parameter, building_information_modeling_ops_register_rule, building_information_modeling_ops_empty_state
from pyAppGen.pbcs.building_information_modeling_ops.ui import building_information_modeling_ops_ui_contract, building_information_modeling_ops_render_workbench


def test_building_information_modeling_ops_runtime_capabilities_and_contracts():
    runtime = building_information_modeling_ops_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/building_information_modeling_ops'
    assert building_information_modeling_ops_build_schema_contract()['ok'] is True
    assert building_information_modeling_ops_build_service_contract()['ok'] is True
    assert building_information_modeling_ops_build_release_evidence()['ok'] is True
    assert building_information_modeling_ops_runtime_smoke()['ok'] is True


def test_building_information_modeling_ops_events_ui_boundary_and_configuration():
    state = building_information_modeling_ops_empty_state()
    assert building_information_modeling_ops_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.building_information_modeling_ops.events'})['ok'] is True
    assert building_information_modeling_ops_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert building_information_modeling_ops_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert building_information_modeling_ops_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert building_information_modeling_ops_ui_contract()['ok'] is True
    assert building_information_modeling_ops_render_workbench()['ok'] is True
    assert building_information_modeling_ops_verify_owned_table_boundary((f'building_information_modeling_ops_owned_table', 'foreign_table'))['ok'] is False
