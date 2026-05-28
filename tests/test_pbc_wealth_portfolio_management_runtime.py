from pyAppGen.pbcs.wealth_portfolio_management import implementation_contract, wealth_portfolio_management_runtime_capabilities, wealth_portfolio_management_runtime_smoke, wealth_portfolio_management_build_schema_contract, wealth_portfolio_management_build_service_contract, wealth_portfolio_management_build_release_evidence, wealth_portfolio_management_receive_event, wealth_portfolio_management_verify_owned_table_boundary, wealth_portfolio_management_configure_runtime, wealth_portfolio_management_set_parameter, wealth_portfolio_management_register_rule, wealth_portfolio_management_empty_state
from pyAppGen.pbcs.wealth_portfolio_management.ui import wealth_portfolio_management_ui_contract, wealth_portfolio_management_render_workbench


def test_wealth_portfolio_management_runtime_capabilities_and_contracts():
    runtime = wealth_portfolio_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/wealth_portfolio_management'
    assert wealth_portfolio_management_build_schema_contract()['ok'] is True
    assert wealth_portfolio_management_build_service_contract()['ok'] is True
    assert wealth_portfolio_management_build_release_evidence()['ok'] is True
    assert wealth_portfolio_management_runtime_smoke()['ok'] is True


def test_wealth_portfolio_management_events_ui_boundary_and_configuration():
    state = wealth_portfolio_management_empty_state()
    assert wealth_portfolio_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.wealth_portfolio_management.events'})['ok'] is True
    assert wealth_portfolio_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert wealth_portfolio_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert wealth_portfolio_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert wealth_portfolio_management_ui_contract()['ok'] is True
    assert wealth_portfolio_management_render_workbench()['ok'] is True
    assert wealth_portfolio_management_verify_owned_table_boundary((f'wealth_portfolio_management_owned_table', 'foreign_table'))['ok'] is False
