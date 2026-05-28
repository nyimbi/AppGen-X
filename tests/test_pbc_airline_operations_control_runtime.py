from pyAppGen.pbcs.airline_operations_control import implementation_contract, airline_operations_control_runtime_capabilities, airline_operations_control_runtime_smoke, airline_operations_control_build_schema_contract, airline_operations_control_build_service_contract, airline_operations_control_build_release_evidence, airline_operations_control_receive_event, airline_operations_control_verify_owned_table_boundary, airline_operations_control_configure_runtime, airline_operations_control_set_parameter, airline_operations_control_register_rule, airline_operations_control_empty_state
from pyAppGen.pbcs.airline_operations_control.ui import airline_operations_control_ui_contract, airline_operations_control_render_workbench


def test_airline_operations_control_runtime_capabilities_and_contracts():
    runtime = airline_operations_control_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/airline_operations_control'
    assert airline_operations_control_build_schema_contract()['ok'] is True
    assert airline_operations_control_build_service_contract()['ok'] is True
    assert airline_operations_control_build_release_evidence()['ok'] is True
    assert airline_operations_control_runtime_smoke()['ok'] is True


def test_airline_operations_control_events_ui_boundary_and_configuration():
    state = airline_operations_control_empty_state()
    assert airline_operations_control_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.airline_operations_control.events'})['ok'] is True
    assert airline_operations_control_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert airline_operations_control_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert airline_operations_control_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert airline_operations_control_ui_contract()['ok'] is True
    assert airline_operations_control_render_workbench()['ok'] is True
    assert airline_operations_control_verify_owned_table_boundary((f'airline_operations_control_owned_table', 'foreign_table'))['ok'] is False
