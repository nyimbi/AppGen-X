from pyAppGen.pbcs.it_service_management import implementation_contract, it_service_management_runtime_capabilities, it_service_management_runtime_smoke, it_service_management_build_schema_contract, it_service_management_build_service_contract, it_service_management_build_release_evidence, it_service_management_receive_event, it_service_management_verify_owned_table_boundary, it_service_management_configure_runtime, it_service_management_set_parameter, it_service_management_register_rule, it_service_management_empty_state
from pyAppGen.pbcs.it_service_management.ui import it_service_management_ui_contract, it_service_management_render_workbench


def test_it_service_management_runtime_capabilities_and_contracts():
    runtime = it_service_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/it_service_management'
    assert it_service_management_build_schema_contract()['ok'] is True
    assert it_service_management_build_service_contract()['ok'] is True
    assert it_service_management_build_release_evidence()['ok'] is True
    assert it_service_management_runtime_smoke()['ok'] is True


def test_it_service_management_events_ui_boundary_and_configuration():
    state = it_service_management_empty_state()
    assert it_service_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.it_service_management.events'})['ok'] is True
    assert it_service_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert it_service_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert it_service_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert it_service_management_ui_contract()['ok'] is True
    assert it_service_management_render_workbench()['ok'] is True
    assert it_service_management_verify_owned_table_boundary((f'it_service_management_owned_table', 'foreign_table'))['ok'] is False
