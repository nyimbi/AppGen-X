from pyAppGen.pbcs.gaming_casino_operations import implementation_contract, gaming_casino_operations_runtime_capabilities, gaming_casino_operations_runtime_smoke, gaming_casino_operations_build_schema_contract, gaming_casino_operations_build_service_contract, gaming_casino_operations_build_release_evidence, gaming_casino_operations_receive_event, gaming_casino_operations_verify_owned_table_boundary, gaming_casino_operations_configure_runtime, gaming_casino_operations_set_parameter, gaming_casino_operations_register_rule, gaming_casino_operations_empty_state
from pyAppGen.pbcs.gaming_casino_operations.ui import gaming_casino_operations_ui_contract, gaming_casino_operations_render_workbench


def test_gaming_casino_operations_runtime_capabilities_and_contracts():
    runtime = gaming_casino_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/gaming_casino_operations'
    assert gaming_casino_operations_build_schema_contract()['ok'] is True
    assert gaming_casino_operations_build_service_contract()['ok'] is True
    assert gaming_casino_operations_build_release_evidence()['ok'] is True
    assert gaming_casino_operations_runtime_smoke()['ok'] is True


def test_gaming_casino_operations_events_ui_boundary_and_configuration():
    state = gaming_casino_operations_empty_state()
    assert gaming_casino_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.gaming_casino_operations.events'})['ok'] is True
    assert gaming_casino_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert gaming_casino_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert gaming_casino_operations_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert gaming_casino_operations_ui_contract()['ok'] is True
    assert gaming_casino_operations_render_workbench()['ok'] is True
    assert gaming_casino_operations_verify_owned_table_boundary((f'gaming_casino_operations_owned_table', 'foreign_table'))['ok'] is False
