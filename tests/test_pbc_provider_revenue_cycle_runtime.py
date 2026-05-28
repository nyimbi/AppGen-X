from pyAppGen.pbcs.provider_revenue_cycle import implementation_contract, provider_revenue_cycle_runtime_capabilities, provider_revenue_cycle_runtime_smoke, provider_revenue_cycle_build_schema_contract, provider_revenue_cycle_build_service_contract, provider_revenue_cycle_build_release_evidence, provider_revenue_cycle_receive_event, provider_revenue_cycle_verify_owned_table_boundary, provider_revenue_cycle_configure_runtime, provider_revenue_cycle_set_parameter, provider_revenue_cycle_register_rule, provider_revenue_cycle_empty_state
from pyAppGen.pbcs.provider_revenue_cycle.ui import provider_revenue_cycle_ui_contract, provider_revenue_cycle_render_workbench


def test_provider_revenue_cycle_runtime_capabilities_and_contracts():
    runtime = provider_revenue_cycle_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/provider_revenue_cycle'
    assert provider_revenue_cycle_build_schema_contract()['ok'] is True
    assert provider_revenue_cycle_build_service_contract()['ok'] is True
    assert provider_revenue_cycle_build_release_evidence()['ok'] is True
    assert provider_revenue_cycle_runtime_smoke()['ok'] is True


def test_provider_revenue_cycle_events_ui_boundary_and_configuration():
    state = provider_revenue_cycle_empty_state()
    assert provider_revenue_cycle_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.provider_revenue_cycle.events'})['ok'] is True
    assert provider_revenue_cycle_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert provider_revenue_cycle_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert provider_revenue_cycle_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert provider_revenue_cycle_ui_contract()['ok'] is True
    assert provider_revenue_cycle_render_workbench()['ok'] is True
    assert provider_revenue_cycle_verify_owned_table_boundary((f'provider_revenue_cycle_owned_table', 'foreign_table'))['ok'] is False
