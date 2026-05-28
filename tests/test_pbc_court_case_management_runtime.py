from pyAppGen.pbcs.court_case_management import implementation_contract, court_case_management_runtime_capabilities, court_case_management_runtime_smoke, court_case_management_build_schema_contract, court_case_management_build_service_contract, court_case_management_build_release_evidence, court_case_management_receive_event, court_case_management_verify_owned_table_boundary, court_case_management_configure_runtime, court_case_management_set_parameter, court_case_management_register_rule, court_case_management_empty_state
from pyAppGen.pbcs.court_case_management.ui import court_case_management_ui_contract, court_case_management_render_workbench


def test_court_case_management_runtime_capabilities_and_contracts():
    runtime = court_case_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/court_case_management'
    assert court_case_management_build_schema_contract()['ok'] is True
    assert court_case_management_build_service_contract()['ok'] is True
    assert court_case_management_build_release_evidence()['ok'] is True
    assert court_case_management_runtime_smoke()['ok'] is True


def test_court_case_management_events_ui_boundary_and_configuration():
    state = court_case_management_empty_state()
    assert court_case_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.court_case_management.events'})['ok'] is True
    assert court_case_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert court_case_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert court_case_management_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert court_case_management_ui_contract()['ok'] is True
    assert court_case_management_render_workbench()['ok'] is True
    assert court_case_management_verify_owned_table_boundary((f'court_case_management_owned_table', 'foreign_table'))['ok'] is False
