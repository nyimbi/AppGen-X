from pyAppGen.pbcs.library_archives_management import implementation_contract, library_archives_management_runtime_capabilities, library_archives_management_runtime_smoke, library_archives_management_build_schema_contract, library_archives_management_build_service_contract, library_archives_management_build_release_evidence, library_archives_management_receive_event, library_archives_management_verify_owned_table_boundary, library_archives_management_configure_runtime, library_archives_management_set_parameter, library_archives_management_register_rule, library_archives_management_empty_state
from pyAppGen.pbcs.library_archives_management.ui import library_archives_management_ui_contract, library_archives_management_render_workbench


def test_library_archives_management_runtime_capabilities_and_contracts():
    runtime = library_archives_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/library_archives_management'
    assert library_archives_management_build_schema_contract()['ok'] is True
    assert library_archives_management_build_service_contract()['ok'] is True
    assert library_archives_management_build_release_evidence()['ok'] is True
    assert library_archives_management_runtime_smoke()['ok'] is True


def test_library_archives_management_events_ui_boundary_and_configuration():
    state = library_archives_management_empty_state()
    assert library_archives_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.library_archives_management.events'})['ok'] is True
    assert library_archives_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert library_archives_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert library_archives_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert library_archives_management_ui_contract()['ok'] is True
    assert library_archives_management_render_workbench()['ok'] is True
    assert library_archives_management_verify_owned_table_boundary((f'library_archives_management_owned_table', 'foreign_table'))['ok'] is False
