from pyAppGen.pbcs.cybersecurity_operations_center import implementation_contract, cybersecurity_operations_center_runtime_capabilities, cybersecurity_operations_center_runtime_smoke, cybersecurity_operations_center_build_schema_contract, cybersecurity_operations_center_build_service_contract, cybersecurity_operations_center_build_release_evidence, cybersecurity_operations_center_receive_event, cybersecurity_operations_center_verify_owned_table_boundary, cybersecurity_operations_center_configure_runtime, cybersecurity_operations_center_set_parameter, cybersecurity_operations_center_register_rule, cybersecurity_operations_center_empty_state
from pyAppGen.pbcs.cybersecurity_operations_center.ui import cybersecurity_operations_center_ui_contract, cybersecurity_operations_center_render_workbench


def test_cybersecurity_operations_center_runtime_capabilities_and_contracts():
    runtime = cybersecurity_operations_center_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/cybersecurity_operations_center'
    assert cybersecurity_operations_center_build_schema_contract()['ok'] is True
    assert cybersecurity_operations_center_build_service_contract()['ok'] is True
    assert cybersecurity_operations_center_build_release_evidence()['ok'] is True
    assert cybersecurity_operations_center_runtime_smoke()['ok'] is True


def test_cybersecurity_operations_center_events_ui_boundary_and_configuration():
    state = cybersecurity_operations_center_empty_state()
    assert cybersecurity_operations_center_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.cybersecurity_operations_center.events'})['ok'] is True
    assert cybersecurity_operations_center_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert cybersecurity_operations_center_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert cybersecurity_operations_center_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert cybersecurity_operations_center_ui_contract()['ok'] is True
    assert cybersecurity_operations_center_render_workbench()['ok'] is True
    assert cybersecurity_operations_center_verify_owned_table_boundary((f'cybersecurity_operations_center_owned_table', 'foreign_table'))['ok'] is False
