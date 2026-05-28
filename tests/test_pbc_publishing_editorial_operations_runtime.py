from pyAppGen.pbcs.publishing_editorial_operations import implementation_contract, publishing_editorial_operations_runtime_capabilities, publishing_editorial_operations_runtime_smoke, publishing_editorial_operations_build_schema_contract, publishing_editorial_operations_build_service_contract, publishing_editorial_operations_build_release_evidence, publishing_editorial_operations_receive_event, publishing_editorial_operations_verify_owned_table_boundary, publishing_editorial_operations_configure_runtime, publishing_editorial_operations_set_parameter, publishing_editorial_operations_register_rule, publishing_editorial_operations_empty_state
from pyAppGen.pbcs.publishing_editorial_operations.ui import publishing_editorial_operations_ui_contract, publishing_editorial_operations_render_workbench


def test_publishing_editorial_operations_runtime_capabilities_and_contracts():
    runtime = publishing_editorial_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/publishing_editorial_operations'
    assert publishing_editorial_operations_build_schema_contract()['ok'] is True
    assert publishing_editorial_operations_build_service_contract()['ok'] is True
    assert publishing_editorial_operations_build_release_evidence()['ok'] is True
    assert publishing_editorial_operations_runtime_smoke()['ok'] is True


def test_publishing_editorial_operations_events_ui_boundary_and_configuration():
    state = publishing_editorial_operations_empty_state()
    assert publishing_editorial_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.publishing_editorial_operations.events'})['ok'] is True
    assert publishing_editorial_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert publishing_editorial_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert publishing_editorial_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert publishing_editorial_operations_ui_contract()['ok'] is True
    assert publishing_editorial_operations_render_workbench()['ok'] is True
    assert publishing_editorial_operations_verify_owned_table_boundary((f'publishing_editorial_operations_owned_table', 'foreign_table'))['ok'] is False
