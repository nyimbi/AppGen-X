from pyAppGen.pbcs.agriculture_farm_operations import implementation_contract, agriculture_farm_operations_runtime_capabilities, agriculture_farm_operations_runtime_smoke, agriculture_farm_operations_build_schema_contract, agriculture_farm_operations_build_service_contract, agriculture_farm_operations_build_release_evidence, agriculture_farm_operations_receive_event, agriculture_farm_operations_verify_owned_table_boundary, agriculture_farm_operations_configure_runtime, agriculture_farm_operations_set_parameter, agriculture_farm_operations_register_rule, agriculture_farm_operations_empty_state
from pyAppGen.pbcs.agriculture_farm_operations.ui import agriculture_farm_operations_ui_contract, agriculture_farm_operations_render_workbench


def test_agriculture_farm_operations_runtime_capabilities_and_contracts():
    runtime = agriculture_farm_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/agriculture_farm_operations'
    assert agriculture_farm_operations_build_schema_contract()['ok'] is True
    assert agriculture_farm_operations_build_service_contract()['ok'] is True
    assert agriculture_farm_operations_build_release_evidence()['ok'] is True
    assert agriculture_farm_operations_runtime_smoke()['ok'] is True


def test_agriculture_farm_operations_events_ui_boundary_and_configuration():
    state = agriculture_farm_operations_empty_state()
    assert agriculture_farm_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.agriculture_farm_operations.events'})['ok'] is True
    assert agriculture_farm_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert agriculture_farm_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert agriculture_farm_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert agriculture_farm_operations_ui_contract()['ok'] is True
    assert agriculture_farm_operations_render_workbench()['ok'] is True
    assert agriculture_farm_operations_verify_owned_table_boundary((f'agriculture_farm_operations_owned_table', 'foreign_table'))['ok'] is False
