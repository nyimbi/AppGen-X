from pyAppGen.pbcs.livestock_herd_management import implementation_contract, livestock_herd_management_runtime_capabilities, livestock_herd_management_runtime_smoke, livestock_herd_management_build_schema_contract, livestock_herd_management_build_service_contract, livestock_herd_management_build_release_evidence, livestock_herd_management_receive_event, livestock_herd_management_verify_owned_table_boundary, livestock_herd_management_configure_runtime, livestock_herd_management_set_parameter, livestock_herd_management_register_rule, livestock_herd_management_empty_state
from pyAppGen.pbcs.livestock_herd_management.ui import livestock_herd_management_ui_contract, livestock_herd_management_render_workbench


def test_livestock_herd_management_runtime_capabilities_and_contracts():
    runtime = livestock_herd_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/livestock_herd_management'
    assert livestock_herd_management_build_schema_contract()['ok'] is True
    assert livestock_herd_management_build_service_contract()['ok'] is True
    assert livestock_herd_management_build_release_evidence()['ok'] is True
    assert livestock_herd_management_runtime_smoke()['ok'] is True


def test_livestock_herd_management_events_ui_boundary_and_configuration():
    state = livestock_herd_management_empty_state()
    assert livestock_herd_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.livestock_herd_management.events'})['ok'] is True
    assert livestock_herd_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert livestock_herd_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert livestock_herd_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert livestock_herd_management_ui_contract()['ok'] is True
    assert livestock_herd_management_render_workbench()['ok'] is True
    assert livestock_herd_management_verify_owned_table_boundary((f'livestock_herd_management_owned_table', 'foreign_table'))['ok'] is False
