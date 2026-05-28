from pyAppGen.pbcs.capital_markets_trading_ops import implementation_contract, capital_markets_trading_ops_runtime_capabilities, capital_markets_trading_ops_runtime_smoke, capital_markets_trading_ops_build_schema_contract, capital_markets_trading_ops_build_service_contract, capital_markets_trading_ops_build_release_evidence, capital_markets_trading_ops_receive_event, capital_markets_trading_ops_verify_owned_table_boundary, capital_markets_trading_ops_configure_runtime, capital_markets_trading_ops_set_parameter, capital_markets_trading_ops_register_rule, capital_markets_trading_ops_empty_state
from pyAppGen.pbcs.capital_markets_trading_ops.ui import capital_markets_trading_ops_ui_contract, capital_markets_trading_ops_render_workbench


def test_capital_markets_trading_ops_runtime_capabilities_and_contracts():
    runtime = capital_markets_trading_ops_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/capital_markets_trading_ops'
    assert capital_markets_trading_ops_build_schema_contract()['ok'] is True
    assert capital_markets_trading_ops_build_service_contract()['ok'] is True
    assert capital_markets_trading_ops_build_release_evidence()['ok'] is True
    assert capital_markets_trading_ops_runtime_smoke()['ok'] is True


def test_capital_markets_trading_ops_events_ui_boundary_and_configuration():
    state = capital_markets_trading_ops_empty_state()
    assert capital_markets_trading_ops_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.capital_markets_trading_ops.events'})['ok'] is True
    assert capital_markets_trading_ops_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert capital_markets_trading_ops_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert capital_markets_trading_ops_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert capital_markets_trading_ops_ui_contract()['ok'] is True
    assert capital_markets_trading_ops_render_workbench()['ok'] is True
    assert capital_markets_trading_ops_verify_owned_table_boundary((f'capital_markets_trading_ops_owned_table', 'foreign_table'))['ok'] is False
