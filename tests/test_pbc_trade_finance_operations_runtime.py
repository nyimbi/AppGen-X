from pyAppGen.pbcs.trade_finance_operations import implementation_contract, trade_finance_operations_runtime_capabilities, trade_finance_operations_runtime_smoke, trade_finance_operations_build_schema_contract, trade_finance_operations_build_service_contract, trade_finance_operations_build_release_evidence, trade_finance_operations_receive_event, trade_finance_operations_verify_owned_table_boundary, trade_finance_operations_configure_runtime, trade_finance_operations_set_parameter, trade_finance_operations_register_rule, trade_finance_operations_empty_state
from pyAppGen.pbcs.trade_finance_operations.ui import trade_finance_operations_ui_contract, trade_finance_operations_render_workbench


def test_trade_finance_operations_runtime_capabilities_and_contracts():
    runtime = trade_finance_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/trade_finance_operations'
    assert trade_finance_operations_build_schema_contract()['ok'] is True
    assert trade_finance_operations_build_service_contract()['ok'] is True
    assert trade_finance_operations_build_release_evidence()['ok'] is True
    assert trade_finance_operations_runtime_smoke()['ok'] is True


def test_trade_finance_operations_events_ui_boundary_and_configuration():
    state = trade_finance_operations_empty_state()
    assert trade_finance_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.trade_finance_operations.events'})['ok'] is True
    assert trade_finance_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert trade_finance_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert trade_finance_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert trade_finance_operations_ui_contract()['ok'] is True
    assert trade_finance_operations_render_workbench()['ok'] is True
    assert trade_finance_operations_verify_owned_table_boundary((f'trade_finance_operations_owned_table', 'foreign_table'))['ok'] is False
