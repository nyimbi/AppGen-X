from pyAppGen.pbcs.mining_operations_management import implementation_contract, mining_operations_management_runtime_capabilities, mining_operations_management_runtime_smoke, mining_operations_management_build_schema_contract, mining_operations_management_build_service_contract, mining_operations_management_build_release_evidence, mining_operations_management_receive_event, mining_operations_management_verify_owned_table_boundary, mining_operations_management_configure_runtime, mining_operations_management_set_parameter, mining_operations_management_register_rule, mining_operations_management_empty_state
from pyAppGen.pbcs.mining_operations_management.ui import mining_operations_management_ui_contract, mining_operations_management_render_workbench


def test_mining_operations_management_runtime_capabilities_and_contracts():
    runtime = mining_operations_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/mining_operations_management'
    assert mining_operations_management_build_schema_contract()['ok'] is True
    assert mining_operations_management_build_service_contract()['ok'] is True
    assert mining_operations_management_build_release_evidence()['ok'] is True
    assert mining_operations_management_runtime_smoke()['ok'] is True


def test_mining_operations_management_events_ui_boundary_and_configuration():
    state = mining_operations_management_empty_state()
    assert mining_operations_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.mining_operations_management.events'})['ok'] is True
    assert mining_operations_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert mining_operations_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert mining_operations_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert mining_operations_management_ui_contract()['ok'] is True
    assert mining_operations_management_render_workbench()['ok'] is True
    assert mining_operations_management_verify_owned_table_boundary((f'mining_operations_management_owned_table', 'foreign_table'))['ok'] is False
