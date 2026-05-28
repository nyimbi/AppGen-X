from pyAppGen.pbcs.restaurant_operations import implementation_contract, restaurant_operations_runtime_capabilities, restaurant_operations_runtime_smoke, restaurant_operations_build_schema_contract, restaurant_operations_build_service_contract, restaurant_operations_build_release_evidence, restaurant_operations_receive_event, restaurant_operations_verify_owned_table_boundary, restaurant_operations_configure_runtime, restaurant_operations_set_parameter, restaurant_operations_register_rule, restaurant_operations_empty_state
from pyAppGen.pbcs.restaurant_operations.ui import restaurant_operations_ui_contract, restaurant_operations_render_workbench


def test_restaurant_operations_runtime_capabilities_and_contracts():
    runtime = restaurant_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/restaurant_operations'
    assert restaurant_operations_build_schema_contract()['ok'] is True
    assert restaurant_operations_build_service_contract()['ok'] is True
    assert restaurant_operations_build_release_evidence()['ok'] is True
    assert restaurant_operations_runtime_smoke()['ok'] is True


def test_restaurant_operations_events_ui_boundary_and_configuration():
    state = restaurant_operations_empty_state()
    assert restaurant_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.restaurant_operations.events'})['ok'] is True
    assert restaurant_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert restaurant_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert restaurant_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert restaurant_operations_ui_contract()['ok'] is True
    assert restaurant_operations_render_workbench()['ok'] is True
    assert restaurant_operations_verify_owned_table_boundary((f'restaurant_operations_owned_table', 'foreign_table'))['ok'] is False
