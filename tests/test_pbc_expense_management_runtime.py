from pyAppGen.pbcs.expense_management import implementation_contract, expense_management_runtime_capabilities, expense_management_runtime_smoke, expense_management_build_schema_contract, expense_management_build_service_contract, expense_management_build_release_evidence, expense_management_receive_event, expense_management_ui_contract, expense_management_verify_owned_table_boundary, expense_management_configure_runtime, expense_management_set_parameter, expense_management_register_rule


def test_expense_management_runtime_capabilities_and_smoke():
    runtime = expense_management_runtime_capabilities()
    smoke = expense_management_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'expense_management'


def test_expense_management_contracts_events_workbench_and_boundary():
    assert expense_management_build_schema_contract()['ok'] is True
    assert expense_management_build_service_contract()['ok'] is True
    assert expense_management_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'expense_management'
    assert expense_management_receive_event(expense_management_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.expense_management.events'})['state'], {'event_type': ('EmployeeProvisioned', 'PaymentCaptured', 'AccessPolicyChanged')[0], 'event_id': 'evt'})['ok'] is True
    assert expense_management_ui_contract()['ok'] is True  # workbench ui_contract
    assert expense_management_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert expense_management_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.expense_management.events'})['ok'] is True
    assert expense_management_set_parameter(state, 'threshold', 1)['ok'] is True
    assert expense_management_register_rule(state, {'rule_id':'r1'})['ok'] is True
