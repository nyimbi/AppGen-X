from pyAppGen.pbcs.smart_city_mobility_operations import implementation_contract, smart_city_mobility_operations_runtime_capabilities, smart_city_mobility_operations_runtime_smoke, smart_city_mobility_operations_build_schema_contract, smart_city_mobility_operations_build_service_contract, smart_city_mobility_operations_build_release_evidence, smart_city_mobility_operations_receive_event, smart_city_mobility_operations_verify_owned_table_boundary, smart_city_mobility_operations_configure_runtime, smart_city_mobility_operations_set_parameter, smart_city_mobility_operations_register_rule, smart_city_mobility_operations_empty_state
from pyAppGen.pbcs.smart_city_mobility_operations.ui import smart_city_mobility_operations_ui_contract, smart_city_mobility_operations_render_workbench


def test_smart_city_mobility_operations_runtime_capabilities_and_contracts():
    runtime = smart_city_mobility_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/smart_city_mobility_operations'
    assert smart_city_mobility_operations_build_schema_contract()['ok'] is True
    assert smart_city_mobility_operations_build_service_contract()['ok'] is True
    assert smart_city_mobility_operations_build_release_evidence()['ok'] is True
    assert smart_city_mobility_operations_runtime_smoke()['ok'] is True


def test_smart_city_mobility_operations_events_ui_boundary_and_configuration():
    state = smart_city_mobility_operations_empty_state()
    assert smart_city_mobility_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.smart_city_mobility_operations.events'})['ok'] is True
    assert smart_city_mobility_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert smart_city_mobility_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert smart_city_mobility_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert smart_city_mobility_operations_ui_contract()['ok'] is True
    assert smart_city_mobility_operations_render_workbench()['ok'] is True
    assert smart_city_mobility_operations_verify_owned_table_boundary((f'smart_city_mobility_operations_owned_table', 'foreign_table'))['ok'] is False
