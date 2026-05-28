from pyAppGen.pbcs.port_terminal_operations import implementation_contract, port_terminal_operations_runtime_capabilities, port_terminal_operations_runtime_smoke, port_terminal_operations_build_schema_contract, port_terminal_operations_build_service_contract, port_terminal_operations_build_release_evidence, port_terminal_operations_receive_event, port_terminal_operations_verify_owned_table_boundary, port_terminal_operations_configure_runtime, port_terminal_operations_set_parameter, port_terminal_operations_register_rule, port_terminal_operations_empty_state
from pyAppGen.pbcs.port_terminal_operations.ui import port_terminal_operations_ui_contract, port_terminal_operations_render_workbench


def test_port_terminal_operations_runtime_capabilities_and_contracts():
    runtime = port_terminal_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/port_terminal_operations'
    assert port_terminal_operations_build_schema_contract()['ok'] is True
    assert port_terminal_operations_build_service_contract()['ok'] is True
    assert port_terminal_operations_build_release_evidence()['ok'] is True
    assert port_terminal_operations_runtime_smoke()['ok'] is True


def test_port_terminal_operations_events_ui_boundary_and_configuration():
    state = port_terminal_operations_empty_state()
    assert port_terminal_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.port_terminal_operations.events'})['ok'] is True
    assert port_terminal_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert port_terminal_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert port_terminal_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert port_terminal_operations_ui_contract()['ok'] is True
    assert port_terminal_operations_render_workbench()['ok'] is True
    assert port_terminal_operations_verify_owned_table_boundary((f'port_terminal_operations_owned_table', 'foreign_table'))['ok'] is False
