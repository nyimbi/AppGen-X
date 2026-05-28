from pyAppGen.pbcs.research_grants_management import implementation_contract, research_grants_management_runtime_capabilities, research_grants_management_runtime_smoke, research_grants_management_build_schema_contract, research_grants_management_build_service_contract, research_grants_management_build_release_evidence, research_grants_management_receive_event, research_grants_management_verify_owned_table_boundary, research_grants_management_configure_runtime, research_grants_management_set_parameter, research_grants_management_register_rule, research_grants_management_empty_state
from pyAppGen.pbcs.research_grants_management.ui import research_grants_management_ui_contract, research_grants_management_render_workbench


def test_research_grants_management_runtime_capabilities_and_contracts():
    runtime = research_grants_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/research_grants_management'
    assert research_grants_management_build_schema_contract()['ok'] is True
    assert research_grants_management_build_service_contract()['ok'] is True
    assert research_grants_management_build_release_evidence()['ok'] is True
    assert research_grants_management_runtime_smoke()['ok'] is True


def test_research_grants_management_events_ui_boundary_and_configuration():
    state = research_grants_management_empty_state()
    assert research_grants_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.research_grants_management.events'})['ok'] is True
    assert research_grants_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert research_grants_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert research_grants_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert research_grants_management_ui_contract()['ok'] is True
    assert research_grants_management_render_workbench()['ok'] is True
    assert research_grants_management_verify_owned_table_boundary((f'research_grants_management_owned_table', 'foreign_table'))['ok'] is False
