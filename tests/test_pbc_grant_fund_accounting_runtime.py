from pyAppGen.pbcs.grant_fund_accounting import implementation_contract, grant_fund_accounting_runtime_capabilities, grant_fund_accounting_runtime_smoke, grant_fund_accounting_build_schema_contract, grant_fund_accounting_build_service_contract, grant_fund_accounting_build_release_evidence, grant_fund_accounting_receive_event, grant_fund_accounting_ui_contract, grant_fund_accounting_verify_owned_table_boundary, grant_fund_accounting_configure_runtime, grant_fund_accounting_set_parameter, grant_fund_accounting_register_rule


def test_grant_fund_accounting_runtime_capabilities_and_smoke():
    runtime = grant_fund_accounting_runtime_capabilities()
    smoke = grant_fund_accounting_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'grant_fund_accounting'


def test_grant_fund_accounting_contracts_events_workbench_and_boundary():
    assert grant_fund_accounting_build_schema_contract()['ok'] is True
    assert grant_fund_accounting_build_service_contract()['ok'] is True
    assert grant_fund_accounting_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'grant_fund_accounting'
    assert grant_fund_accounting_receive_event(grant_fund_accounting_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.grant_fund_accounting.events'})['state'], {'event_type': ('JournalPosted', 'ExpenseApproved', 'PaymentCaptured')[0], 'event_id': 'evt'})['ok'] is True
    assert grant_fund_accounting_ui_contract()['ok'] is True  # workbench ui_contract
    assert grant_fund_accounting_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert grant_fund_accounting_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.grant_fund_accounting.events'})['ok'] is True
    assert grant_fund_accounting_set_parameter(state, 'threshold', 1)['ok'] is True
    assert grant_fund_accounting_register_rule(state, {'rule_id':'r1'})['ok'] is True
