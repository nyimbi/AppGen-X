from pyAppGen.pbcs.waste_recycling_operations import implementation_contract, waste_recycling_operations_runtime_capabilities, waste_recycling_operations_runtime_smoke, waste_recycling_operations_build_schema_contract, waste_recycling_operations_build_service_contract, waste_recycling_operations_build_release_evidence, waste_recycling_operations_receive_event, waste_recycling_operations_verify_owned_table_boundary, waste_recycling_operations_configure_runtime, waste_recycling_operations_set_parameter, waste_recycling_operations_register_rule, waste_recycling_operations_empty_state
from pyAppGen.pbcs.waste_recycling_operations.ui import waste_recycling_operations_ui_contract, waste_recycling_operations_render_workbench


def test_waste_recycling_operations_runtime_capabilities_and_contracts():
    runtime = waste_recycling_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/waste_recycling_operations'
    assert waste_recycling_operations_build_schema_contract()['ok'] is True
    assert waste_recycling_operations_build_service_contract()['ok'] is True
    assert waste_recycling_operations_build_release_evidence()['ok'] is True
    assert waste_recycling_operations_runtime_smoke()['ok'] is True


def test_waste_recycling_operations_events_ui_boundary_and_configuration():
    state = waste_recycling_operations_empty_state()
    assert waste_recycling_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.waste_recycling_operations.events'})['ok'] is True
    assert waste_recycling_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert waste_recycling_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert waste_recycling_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert waste_recycling_operations_ui_contract()['ok'] is True
    assert waste_recycling_operations_render_workbench()['ok'] is True
    assert waste_recycling_operations_verify_owned_table_boundary((f'waste_recycling_operations_owned_table', 'foreign_table'))['ok'] is False
