from pyAppGen.pbcs.reinsurance_management import implementation_contract, reinsurance_management_runtime_capabilities, reinsurance_management_runtime_smoke, reinsurance_management_build_schema_contract, reinsurance_management_build_service_contract, reinsurance_management_build_release_evidence, reinsurance_management_receive_event, reinsurance_management_verify_owned_table_boundary, reinsurance_management_configure_runtime, reinsurance_management_set_parameter, reinsurance_management_register_rule, reinsurance_management_empty_state
from pyAppGen.pbcs.reinsurance_management.ui import reinsurance_management_ui_contract, reinsurance_management_render_workbench


def test_reinsurance_management_runtime_capabilities_and_contracts():
    runtime = reinsurance_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/reinsurance_management'
    assert reinsurance_management_build_schema_contract()['ok'] is True
    assert reinsurance_management_build_service_contract()['ok'] is True
    assert reinsurance_management_build_release_evidence()['ok'] is True
    assert reinsurance_management_runtime_smoke()['ok'] is True


def test_reinsurance_management_events_ui_boundary_and_configuration():
    state = reinsurance_management_empty_state()
    assert reinsurance_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.reinsurance_management.events'})['ok'] is True
    assert reinsurance_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert reinsurance_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert reinsurance_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert reinsurance_management_ui_contract()['ok'] is True
    assert reinsurance_management_render_workbench()['ok'] is True
    assert reinsurance_management_verify_owned_table_boundary((f'reinsurance_management_owned_table', 'foreign_table'))['ok'] is False
