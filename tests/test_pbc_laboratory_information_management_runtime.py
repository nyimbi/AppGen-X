from pyAppGen.pbcs.laboratory_information_management import implementation_contract, laboratory_information_management_runtime_capabilities, laboratory_information_management_runtime_smoke, laboratory_information_management_build_schema_contract, laboratory_information_management_build_service_contract, laboratory_information_management_build_release_evidence, laboratory_information_management_receive_event, laboratory_information_management_verify_owned_table_boundary, laboratory_information_management_configure_runtime, laboratory_information_management_set_parameter, laboratory_information_management_register_rule, laboratory_information_management_empty_state
from pyAppGen.pbcs.laboratory_information_management.ui import laboratory_information_management_ui_contract, laboratory_information_management_render_workbench


def test_laboratory_information_management_runtime_capabilities_and_contracts():
    runtime = laboratory_information_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/laboratory_information_management'
    assert laboratory_information_management_build_schema_contract()['ok'] is True
    assert laboratory_information_management_build_service_contract()['ok'] is True
    assert laboratory_information_management_build_release_evidence()['ok'] is True
    assert laboratory_information_management_runtime_smoke()['ok'] is True


def test_laboratory_information_management_events_ui_boundary_and_configuration():
    state = laboratory_information_management_empty_state()
    assert laboratory_information_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.laboratory_information_management.events'})['ok'] is True
    assert laboratory_information_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert laboratory_information_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert laboratory_information_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert laboratory_information_management_ui_contract()['ok'] is True
    assert laboratory_information_management_render_workbench()['ok'] is True
    assert laboratory_information_management_verify_owned_table_boundary((f'laboratory_information_management_owned_table', 'foreign_table'))['ok'] is False
