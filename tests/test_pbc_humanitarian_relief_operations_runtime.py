from pyAppGen.pbcs.humanitarian_relief_operations import implementation_contract, humanitarian_relief_operations_runtime_capabilities, humanitarian_relief_operations_runtime_smoke, humanitarian_relief_operations_build_schema_contract, humanitarian_relief_operations_build_service_contract, humanitarian_relief_operations_build_release_evidence, humanitarian_relief_operations_receive_event, humanitarian_relief_operations_verify_owned_table_boundary, humanitarian_relief_operations_configure_runtime, humanitarian_relief_operations_set_parameter, humanitarian_relief_operations_register_rule, humanitarian_relief_operations_empty_state
from pyAppGen.pbcs.humanitarian_relief_operations.ui import humanitarian_relief_operations_ui_contract, humanitarian_relief_operations_render_workbench


def test_humanitarian_relief_operations_runtime_capabilities_and_contracts():
    runtime = humanitarian_relief_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/humanitarian_relief_operations'
    assert humanitarian_relief_operations_build_schema_contract()['ok'] is True
    assert humanitarian_relief_operations_build_service_contract()['ok'] is True
    assert humanitarian_relief_operations_build_release_evidence()['ok'] is True
    assert humanitarian_relief_operations_runtime_smoke()['ok'] is True


def test_humanitarian_relief_operations_events_ui_boundary_and_configuration():
    state = humanitarian_relief_operations_empty_state()
    assert humanitarian_relief_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.humanitarian_relief_operations.events'})['ok'] is True
    assert humanitarian_relief_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert humanitarian_relief_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert humanitarian_relief_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert humanitarian_relief_operations_ui_contract()['ok'] is True
    assert humanitarian_relief_operations_render_workbench()['ok'] is True
    assert humanitarian_relief_operations_verify_owned_table_boundary((f'humanitarian_relief_operations_owned_table', 'foreign_table'))['ok'] is False
