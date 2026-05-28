from pyAppGen.pbcs.energy_trading_risk import implementation_contract, energy_trading_risk_runtime_capabilities, energy_trading_risk_runtime_smoke, energy_trading_risk_build_schema_contract, energy_trading_risk_build_service_contract, energy_trading_risk_build_release_evidence, energy_trading_risk_receive_event, energy_trading_risk_verify_owned_table_boundary, energy_trading_risk_configure_runtime, energy_trading_risk_set_parameter, energy_trading_risk_register_rule, energy_trading_risk_empty_state
from pyAppGen.pbcs.energy_trading_risk.ui import energy_trading_risk_ui_contract, energy_trading_risk_render_workbench


def test_energy_trading_risk_runtime_capabilities_and_contracts():
    runtime = energy_trading_risk_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/energy_trading_risk'
    assert energy_trading_risk_build_schema_contract()['ok'] is True
    assert energy_trading_risk_build_service_contract()['ok'] is True
    assert energy_trading_risk_build_release_evidence()['ok'] is True
    assert energy_trading_risk_runtime_smoke()['ok'] is True


def test_energy_trading_risk_events_ui_boundary_and_configuration():
    state = energy_trading_risk_empty_state()
    assert energy_trading_risk_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.energy_trading_risk.events'})['ok'] is True
    assert energy_trading_risk_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert energy_trading_risk_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert energy_trading_risk_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert energy_trading_risk_ui_contract()['ok'] is True
    assert energy_trading_risk_render_workbench()['ok'] is True
    assert energy_trading_risk_verify_owned_table_boundary((f'energy_trading_risk_owned_table', 'foreign_table'))['ok'] is False
