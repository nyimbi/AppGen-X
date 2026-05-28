from pyAppGen.pbcs.maritime_shipping_operations import implementation_contract, maritime_shipping_operations_runtime_capabilities, maritime_shipping_operations_runtime_smoke, maritime_shipping_operations_build_schema_contract, maritime_shipping_operations_build_service_contract, maritime_shipping_operations_build_release_evidence, maritime_shipping_operations_receive_event, maritime_shipping_operations_verify_owned_table_boundary, maritime_shipping_operations_configure_runtime, maritime_shipping_operations_set_parameter, maritime_shipping_operations_register_rule, maritime_shipping_operations_empty_state
from pyAppGen.pbcs.maritime_shipping_operations.ui import maritime_shipping_operations_ui_contract, maritime_shipping_operations_render_workbench


def test_maritime_shipping_operations_runtime_capabilities_and_contracts():
    runtime = maritime_shipping_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/maritime_shipping_operations'
    assert maritime_shipping_operations_build_schema_contract()['ok'] is True
    assert maritime_shipping_operations_build_service_contract()['ok'] is True
    assert maritime_shipping_operations_build_release_evidence()['ok'] is True
    assert maritime_shipping_operations_runtime_smoke()['ok'] is True


def test_maritime_shipping_operations_events_ui_boundary_and_configuration():
    state = maritime_shipping_operations_empty_state()
    assert maritime_shipping_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.maritime_shipping_operations.events'})['ok'] is True
    assert maritime_shipping_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert maritime_shipping_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert maritime_shipping_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert maritime_shipping_operations_ui_contract()['ok'] is True
    assert maritime_shipping_operations_render_workbench()['ok'] is True
    assert maritime_shipping_operations_verify_owned_table_boundary((f'maritime_shipping_operations_owned_table', 'foreign_table'))['ok'] is False
