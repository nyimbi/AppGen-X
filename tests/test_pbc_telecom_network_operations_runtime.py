from pyAppGen.pbcs.telecom_network_operations import implementation_contract, telecom_network_operations_runtime_capabilities, telecom_network_operations_runtime_smoke, telecom_network_operations_build_schema_contract, telecom_network_operations_build_service_contract, telecom_network_operations_build_release_evidence, telecom_network_operations_receive_event, telecom_network_operations_verify_owned_table_boundary, telecom_network_operations_configure_runtime, telecom_network_operations_set_parameter, telecom_network_operations_register_rule, telecom_network_operations_empty_state
from pyAppGen.pbcs.telecom_network_operations.ui import telecom_network_operations_ui_contract, telecom_network_operations_render_workbench


def test_telecom_network_operations_runtime_capabilities_and_contracts():
    runtime = telecom_network_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/telecom_network_operations'
    assert telecom_network_operations_build_schema_contract()['ok'] is True
    assert telecom_network_operations_build_service_contract()['ok'] is True
    assert telecom_network_operations_build_release_evidence()['ok'] is True
    assert telecom_network_operations_runtime_smoke()['ok'] is True


def test_telecom_network_operations_events_ui_boundary_and_configuration():
    state = telecom_network_operations_empty_state()
    assert telecom_network_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.telecom_network_operations.events'})['ok'] is True
    assert telecom_network_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert telecom_network_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert telecom_network_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert telecom_network_operations_ui_contract()['ok'] is True
    assert telecom_network_operations_render_workbench()['ok'] is True
    assert telecom_network_operations_verify_owned_table_boundary((f'telecom_network_operations_owned_table', 'foreign_table'))['ok'] is False
