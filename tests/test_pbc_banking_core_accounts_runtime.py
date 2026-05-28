from pyAppGen.pbcs.banking_core_accounts import implementation_contract, banking_core_accounts_runtime_capabilities, banking_core_accounts_runtime_smoke, banking_core_accounts_build_schema_contract, banking_core_accounts_build_service_contract, banking_core_accounts_build_release_evidence, banking_core_accounts_receive_event, banking_core_accounts_verify_owned_table_boundary, banking_core_accounts_configure_runtime, banking_core_accounts_set_parameter, banking_core_accounts_register_rule, banking_core_accounts_empty_state
from pyAppGen.pbcs.banking_core_accounts.ui import banking_core_accounts_ui_contract, banking_core_accounts_render_workbench


def test_banking_core_accounts_runtime_capabilities_and_contracts():
    runtime = banking_core_accounts_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/banking_core_accounts'
    assert banking_core_accounts_build_schema_contract()['ok'] is True
    assert banking_core_accounts_build_service_contract()['ok'] is True
    assert banking_core_accounts_build_release_evidence()['ok'] is True
    assert banking_core_accounts_runtime_smoke()['ok'] is True


def test_banking_core_accounts_events_ui_boundary_and_configuration():
    state = banking_core_accounts_empty_state()
    assert banking_core_accounts_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.banking_core_accounts.events'})['ok'] is True
    assert banking_core_accounts_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert banking_core_accounts_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert banking_core_accounts_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert banking_core_accounts_ui_contract()['ok'] is True
    assert banking_core_accounts_render_workbench()['ok'] is True
    assert banking_core_accounts_verify_owned_table_boundary((f'banking_core_accounts_owned_table', 'foreign_table'))['ok'] is False
