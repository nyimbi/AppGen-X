from pyAppGen.pbcs.oil_gas_field_operations import implementation_contract, oil_gas_field_operations_runtime_capabilities, oil_gas_field_operations_runtime_smoke, oil_gas_field_operations_build_schema_contract, oil_gas_field_operations_build_service_contract, oil_gas_field_operations_build_release_evidence, oil_gas_field_operations_receive_event, oil_gas_field_operations_verify_owned_table_boundary, oil_gas_field_operations_configure_runtime, oil_gas_field_operations_set_parameter, oil_gas_field_operations_register_rule, oil_gas_field_operations_empty_state
from pyAppGen.pbcs.oil_gas_field_operations.ui import oil_gas_field_operations_ui_contract, oil_gas_field_operations_render_workbench


def test_oil_gas_field_operations_runtime_capabilities_and_contracts():
    runtime = oil_gas_field_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/oil_gas_field_operations'
    assert oil_gas_field_operations_build_schema_contract()['ok'] is True
    assert oil_gas_field_operations_build_service_contract()['ok'] is True
    assert oil_gas_field_operations_build_release_evidence()['ok'] is True
    assert oil_gas_field_operations_runtime_smoke()['ok'] is True


def test_oil_gas_field_operations_events_ui_boundary_and_configuration():
    state = oil_gas_field_operations_empty_state()
    assert oil_gas_field_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.oil_gas_field_operations.events'})['ok'] is True
    assert oil_gas_field_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert oil_gas_field_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert oil_gas_field_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert oil_gas_field_operations_ui_contract()['ok'] is True
    assert oil_gas_field_operations_render_workbench()['ok'] is True
    assert oil_gas_field_operations_verify_owned_table_boundary((f'oil_gas_field_operations_owned_table', 'foreign_table'))['ok'] is False
