from pyAppGen.pbcs.mining_safety_permits import implementation_contract, mining_safety_permits_runtime_capabilities, mining_safety_permits_runtime_smoke, mining_safety_permits_build_schema_contract, mining_safety_permits_build_service_contract, mining_safety_permits_build_release_evidence, mining_safety_permits_receive_event, mining_safety_permits_verify_owned_table_boundary, mining_safety_permits_configure_runtime, mining_safety_permits_set_parameter, mining_safety_permits_register_rule, mining_safety_permits_empty_state
from pyAppGen.pbcs.mining_safety_permits.ui import mining_safety_permits_ui_contract, mining_safety_permits_render_workbench


def test_mining_safety_permits_runtime_capabilities_and_contracts():
    runtime = mining_safety_permits_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/mining_safety_permits'
    assert mining_safety_permits_build_schema_contract()['ok'] is True
    assert mining_safety_permits_build_service_contract()['ok'] is True
    assert mining_safety_permits_build_release_evidence()['ok'] is True
    assert mining_safety_permits_runtime_smoke()['ok'] is True


def test_mining_safety_permits_events_ui_boundary_and_configuration():
    state = mining_safety_permits_empty_state()
    assert mining_safety_permits_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.mining_safety_permits.events'})['ok'] is True
    assert mining_safety_permits_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert mining_safety_permits_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert mining_safety_permits_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert mining_safety_permits_ui_contract()['ok'] is True
    assert mining_safety_permits_render_workbench()['ok'] is True
    assert mining_safety_permits_verify_owned_table_boundary((f'mining_safety_permits_owned_table', 'foreign_table'))['ok'] is False
