from pyAppGen.pbcs.bank_payments_clearing import implementation_contract, bank_payments_clearing_runtime_capabilities, bank_payments_clearing_runtime_smoke, bank_payments_clearing_build_schema_contract, bank_payments_clearing_build_service_contract, bank_payments_clearing_build_release_evidence, bank_payments_clearing_receive_event, bank_payments_clearing_verify_owned_table_boundary, bank_payments_clearing_configure_runtime, bank_payments_clearing_set_parameter, bank_payments_clearing_register_rule, bank_payments_clearing_empty_state
from pyAppGen.pbcs.bank_payments_clearing.ui import bank_payments_clearing_ui_contract, bank_payments_clearing_render_workbench


def test_bank_payments_clearing_runtime_capabilities_and_contracts():
    runtime = bank_payments_clearing_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/bank_payments_clearing'
    assert bank_payments_clearing_build_schema_contract()['ok'] is True
    assert bank_payments_clearing_build_service_contract()['ok'] is True
    assert bank_payments_clearing_build_release_evidence()['ok'] is True
    assert bank_payments_clearing_runtime_smoke()['ok'] is True


def test_bank_payments_clearing_events_ui_boundary_and_configuration():
    state = bank_payments_clearing_empty_state()
    assert bank_payments_clearing_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.bank_payments_clearing.events'})['ok'] is True
    assert bank_payments_clearing_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert bank_payments_clearing_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert bank_payments_clearing_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert bank_payments_clearing_ui_contract()['ok'] is True
    assert bank_payments_clearing_render_workbench()['ok'] is True
    assert bank_payments_clearing_verify_owned_table_boundary((f'bank_payments_clearing_owned_table', 'foreign_table'))['ok'] is False
